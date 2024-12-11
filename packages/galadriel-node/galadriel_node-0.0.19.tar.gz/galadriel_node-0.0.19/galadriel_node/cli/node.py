import asyncio
import json
import logging
import signal
import subprocess
import sys
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional
from urllib.parse import urljoin, urlparse

import aiohttp
import openai
import rich
import typer
import websockets
from websockets.frames import CloseCode

from galadriel_node.sdk import long_benchmark
from galadriel_node.config import config
from galadriel_node.llm_backends import vllm
from galadriel_node.sdk.entities import AuthenticationError, SdkError
from galadriel_node.sdk.image_generation import (
    ImageGeneration,
    validate_image_generation_request,
)
from galadriel_node.sdk.jobs.api_ping_job import ApiPingJob
from galadriel_node.sdk.util.locked_counter import LockedCounter
from galadriel_node.sdk.jobs.reconnect_request_job import wait_for_reconnect
from galadriel_node.sdk.llm import Llm
from galadriel_node.sdk.logging_utils import init_logging, get_node_logger
from galadriel_node.sdk.protocol import protocol_settings
from galadriel_node.sdk.protocol.entities import InferenceRequest
from galadriel_node.sdk.protocol.health_check_protocol import HealthCheckProtocol
from galadriel_node.sdk.protocol.ping_pong_protocol import PingPongProtocol
from galadriel_node.sdk.protocol.protocol_handler import ProtocolHandler
from galadriel_node.sdk.system.report_hardware import report_hardware
from galadriel_node.sdk.system.report_performance import report_performance
from galadriel_node.sdk.upgrade import version_aware_get

# pylint: disable=invalid-name
llm: Optional[Llm] = None
# pylint: disable=invalid-name
image_generation_engine: Optional[ImageGeneration] = None

node_app = typer.Typer(
    name="node",
    help="Galadriel tool to manage node",
    no_args_is_help=True,
)

BACKOFF_MIN = 24  # Minimum backoff time in seconds
BACKOFF_INCREMENT = 6  # Incremental backoff time in seconds
BACKOFF_MAX = 300  # Maximum backoff time in seconds

logger = get_node_logger()


@dataclass
class ConnectionResult:
    retry: bool
    reset_backoff: bool = True


async def process_request(
    request: InferenceRequest,
    websocket,
    send_lock: asyncio.Lock,
    inference_status_counter: LockedCounter,
) -> None:
    """
    Handles a single inference request and sends the response back in chunks.
    """
    if llm is None:
        logger.error("LLM is not initialized.")
        return
    try:
        await inference_status_counter.increment()
        logging.debug(f"REQUEST {request.id} START")
        async for chunk in llm.execute(request):
            logging.debug(f"Sending chunk: {chunk}")
            async with send_lock:
                await websocket.send(chunk.to_json())
            logging.debug(f"REQUEST {request.id} END")
    except Exception as _:
        logging.error(
            "Error occurred while processing inference request", exc_info=True
        )
    finally:
        await inference_status_counter.decrement()


# pylint: disable=R0912, R0914
async def connect_and_process(
    uri: str, headers: dict, node_id: str, api_ping_job: ApiPingJob
) -> ConnectionResult:
    """
    Establishes the WebSocket connection and processes incoming requests concurrently.
    """
    send_lock = asyncio.Lock()
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # Initialize the protocol handler and register the protocols
        protocol_handler = ProtocolHandler(node_id, websocket)
        ping_pong_protocol = PingPongProtocol(api_ping_job)
        protocol_handler.register(
            protocol_settings.PING_PONG_PROTOCOL_NAME, ping_pong_protocol
        )
        health_check_protocol = HealthCheckProtocol()
        protocol_handler.register(
            HealthCheckProtocol.PROTOCOL_NAME, health_check_protocol
        )
        # TODO better handle the inference status and reconnection request with encapsulations
        # Currently we have locks and counters all in the loop here, and it's really messy to handle
        # these and it could easily go wrong if anyone touches these later. so my meaning is to
        # encapsulate these stuff in functions or better classes so in this function connect_and_process,
        # we just simply instantiate an object and call the function it exposes, without worrying about
        # all these low-level stuff.
        inference_status_counter = LockedCounter()
        while True:
            try:
                logger.info("Waiting for incoming messages...")

                # Create tasks for receiving messages and waiting for reconnect requests
                reconnect_request_job = asyncio.create_task(
                    wait_for_reconnect(
                        inference_status_counter,
                        image_generation_engine,
                        ping_pong_protocol,
                    )
                )
                websocket_recv_job = asyncio.create_task(websocket.recv())

                # Wait for incoming messages or reconnect request
                done, pending = await asyncio.wait(
                    [websocket_recv_job, reconnect_request_job],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                # Cancel pending tasks
                for task in pending:
                    task.cancel()

                if reconnect_request_job in done:
                    logger.info("Reconnect requested. Closing the connection...")
                    await ping_pong_protocol.set_reconnect_requested(False)
                    return ConnectionResult(retry=True, reset_backoff=True)

                if websocket_recv_job in done:
                    # Receive and parse incoming messages
                    data = await websocket_recv_job
                    parsed_data = json.loads(data)

                    # Check if the message is an inference request
                    inference_request = InferenceRequest.get_inference_request(
                        parsed_data
                    )
                    if inference_request is not None and llm is not None:
                        asyncio.create_task(
                            process_request(
                                inference_request,
                                websocket,
                                send_lock,
                                inference_status_counter,
                            )
                        )
                    elif image_generation_engine is not None:
                        image_request = validate_image_generation_request(
                            data=parsed_data
                        )
                        if image_request is not None:
                            asyncio.create_task(
                                image_generation_engine.process_request(
                                    image_request, websocket, send_lock
                                )
                            )
                        else:
                            await protocol_handler.handle(parsed_data, send_lock)
                    else:
                        await protocol_handler.handle(parsed_data, send_lock)
            except json.JSONDecodeError:
                logger.info("Error while parsing json message")
                return ConnectionResult(
                    retry=True, reset_backoff=True
                )  # for now, just retry
            except websockets.ConnectionClosed as e:
                logger.info(f"Received error: {e}")
                match e.code:
                    case CloseCode.POLICY_VIOLATION:
                        return ConnectionResult(retry=True, reset_backoff=False)
                    case CloseCode.TRY_AGAIN_LATER:
                        return ConnectionResult(retry=True, reset_backoff=False)
                logger.info(f"Connection closed: {e}")
                return ConnectionResult(retry=True, reset_backoff=True)
            except Exception as _:
                logger.error("Error occurred while processing message.", exc_info=True)
                return ConnectionResult(retry=True, reset_backoff=True)
            finally:
                reconnect_request_job.cancel()
                websocket_recv_job.cancel()


async def retry_connection(rpc_url: str, api_key: str, node_id: str):
    """
    Attempts to reconnect to the Galadriel server with exponential backoff.
    """
    uri = f"{rpc_url}/ws"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Model": config.GALADRIEL_MODEL_ID,
        "Model-Type": config.GALADRIEL_MODEL_TYPE,
        "Node-Id": node_id,
    }
    retries = 0
    backoff_time = BACKOFF_MIN

    # Start the API ping job
    api_ping_job = ApiPingJob(config.GALADRIEL_API_DOMAIN or _get_domain_from_url(uri))
    asyncio.create_task(api_ping_job.run())

    while True:
        try:
            result = await connect_and_process(uri, headers, node_id, api_ping_job)
            if result.retry:
                retries += 1
                if result.reset_backoff:
                    retries = 0
                    backoff_time = BACKOFF_MIN
                logger.info(f"Retry #{retries} in {backoff_time} seconds...")
            else:
                break
        except websockets.ConnectionClosedError as e:
            retries += 1
            logger.error(f"WebSocket connection closed: {e}. Retrying...")
        except websockets.InvalidStatusCode as e:
            retries += 1
            logger.error(f"Invalid status code: {e}. Retrying...")
        except Exception as _:
            retries += 1
            logger.error(
                f"Websocket connection failed. Retry #{retries} in {backoff_time} seconds..."
            )
            logger.error("Connection error", exc_info=True)

        # Exponential backoff with offset
        await asyncio.sleep(backoff_time)
        backoff_time = min(
            BACKOFF_MIN + (BACKOFF_INCREMENT * (2 ** (retries - 1))), BACKOFF_MAX
        )


def handle_termination(loop, llm_pid):
    for task in asyncio.all_tasks(loop):
        task.cancel()

    if llm_pid is not None:
        vllm.stop(llm_pid)
        logger.info(f"vLLM process with PID {llm_pid} has been stopped.")


# pylint: disable=R0917:
# pylint: disable=W0603
async def run_node(
    api_url: str,
    rpc_url: str,
    api_key: Optional[str],
    node_id: Optional[str],
    llm_base_url: Optional[str],
):
    global llm
    global image_generation_engine

    if not api_key:
        raise SdkError("GALADRIEL_API_KEY env variable not set")
    if not node_id:
        raise SdkError("GALADRIEL_NODE_ID env variable not set")

    # Check version compatibility with the backend. This way it doesn't have to be checked inside report* commands
    await version_aware_get(
        api_url, "node/info", api_key, query_params={"node_id": node_id}
    )
    try:
        if config.GALADRIEL_MODEL_TYPE == "DIFFUSION":
            # Initialize image generation engine with the specified model
            image_generation_engine = ImageGeneration(config.GALADRIEL_MODEL_ID)
            await report_hardware(api_url, api_key, node_id)
            # TODO Need to report performance for image generation node
            await retry_connection(rpc_url, api_key, node_id)
        else:
            if llm_base_url:
                result = await check_llm(llm_base_url, config.GALADRIEL_MODEL_ID)
                if not result:
                    raise SdkError(
                        'LLM check failed. Please make sure "GALADRIEL_LLM_BASE_URL" is correct.'
                    )
            else:
                llm_pid = await run_llm(config.GALADRIEL_MODEL_ID)
                loop = asyncio.get_running_loop()
                for sig in (signal.SIGINT, signal.SIGTERM):
                    loop.add_signal_handler(
                        sig, lambda: handle_termination(loop, llm_pid)
                    )
                llm_base_url = vllm.LLM_BASE_URL
            # Initialize llm with llm_base_url
            llm = Llm(llm_base_url)
            await llm.detect_llm_engine()
            await report_hardware(api_url, api_key, node_id)
            await report_performance(
                api_url, api_key, node_id, llm_base_url, config.GALADRIEL_MODEL_ID
            )
            await retry_connection(rpc_url, api_key, node_id)
    except asyncio.CancelledError:
        logger.error("Stopping the node.")


async def llm_http_check(llm_base_url: str, total_timeout: float = 60.0):
    timeout = aiohttp.ClientTimeout(total=total_timeout)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        return await session.get(llm_base_url + "/v1/models/")


async def llm_sanity_check(
    llm_base_url: str,
    model_id: str,
):
    base_url: str = urljoin(llm_base_url, "/v1")
    client = openai.AsyncOpenAI(base_url=base_url, api_key="sk-no-key-required")
    return await client.chat.with_raw_response.completions.create(
        model=model_id,
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            },
        ],
        max_tokens=5,
        timeout=5,
    )


async def check_llm(llm_base_url: str, model_id: str) -> bool:
    try:
        response = await llm_http_check(llm_base_url)
        if response.ok:
            logger.info(
                f"[bold green]\N{CHECK MARK} LLM server at {llm_base_url} is accessible via HTTP.[/bold green]"
            )
        else:
            logger.info(
                f"[bold red]\N{CROSS MARK} LLM server at {llm_base_url} "
                f"returned status code: {response.status}[/bold red]"
            )
            return False
    except Exception as e:
        logger.error(
            f"[bold red]\N{CROSS MARK} Failed to reach LLM server at {llm_base_url}: \n{e}[/bold red]",
            e,
        )
        return False

    try:
        response = await llm_sanity_check(llm_base_url, model_id)
        if response.status_code == HTTPStatus.OK:
            logger.info(
                f"[bold green]\N{CHECK MARK} LLM server at {llm_base_url} successfully generated tokens.[/bold green]"
            )
            return True
    except openai.APIStatusError as e:
        logger.info(
            f"[bold red]\N{CROSS MARK} LLM server at {llm_base_url} "
            f"failed to generate tokens. APIStatusError: \n{e}[/bold red]"
        )
        return False
    except Exception as e:
        logger.error(
            f"[bold red]\N{CROSS MARK} LLM server at {llm_base_url} "
            f"failed to generate tokens. Exception occurred: {e}[/bold red]"
        )
        return False
    return False


async def run_llm(model_id: str) -> Optional[int]:
    if vllm.is_installed():
        logger.info("Starting vLLM...")
        pid = vllm.start(model_id)
        if pid is None:
            raise SdkError(
                'Failed to start vLLM. Please check "vllm.log" for more information.'
            )
        logger.info("vLLM started successfully.")
        logger.info("Waiting for vLLM to be ready.")
        while True:
            if not vllm.is_process_running(pid):
                raise SdkError(
                    f"vLLM process (PID: {pid}) died unexpectedly. Please check 'vllm.log'."
                )
            rich.print(".", flush=True, end="")
            try:
                response = await llm_http_check(vllm.LLM_BASE_URL, total_timeout=1.0)
                if response.ok:
                    logging.info("\nvLLM is ready.")
                    break
            except Exception:
                continue
            finally:
                await asyncio.sleep(1.0)
        result = await check_llm(vllm.LLM_BASE_URL, model_id)
        if not result:
            raise SdkError(
                'LLM check failed. Please check "vllm.log" for more details.'
            )
        return pid
    raise SdkError(
        "vLLM is not installed, please set GALADRIEL_LLM_BASE_URL in ~/.galadrielenv"
    )


def _get_domain_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc


# pylint: disable=R0917:
@node_app.command("run", help="Run the Galadriel node")
def node_run(
    api_url: str = typer.Option(config.GALADRIEL_API_URL, help="API url"),
    rpc_url: str = typer.Option(config.GALADRIEL_RPC_URL, help="RPC url"),
    api_key: str = typer.Option(config.GALADRIEL_API_KEY, help="API key"),
    node_id: str = typer.Option(config.GALADRIEL_NODE_ID, help="Node ID"),
    llm_base_url: Optional[str] = typer.Option(
        config.GALADRIEL_LLM_BASE_URL, help="LLM base url"
    ),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    """
    Entry point for running the node with retry logic and connection handling.
    """
    init_logging(debug)
    config.validate()
    try:
        asyncio.run(run_node(api_url, rpc_url, api_key, node_id, llm_base_url))
    except AuthenticationError:
        logger.error("Authentication failed. Please check your API key and try again.")
    except SdkError as e:
        logger.error(f"Got an Exception when trying to run the node: {e}")
    except Exception:
        logger.error(
            "Got an unexpected Exception when trying to run the node: ", exc_info=True
        )


@node_app.command("status", help="Get node status")
def node_status(
    api_url: str = typer.Option(config.GALADRIEL_API_URL, help="API url"),
    api_key: str = typer.Option(config.GALADRIEL_API_KEY, help="API key"),
    node_id: str = typer.Option(config.GALADRIEL_NODE_ID, help="Node ID"),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    init_logging(debug)
    config.validate()
    status, response_json = asyncio.run(
        version_aware_get(
            api_url, "node/info", api_key, query_params={"node_id": node_id}
        )
    )
    if status == HTTPStatus.OK and response_json:
        run_status = response_json.get("status")
        if run_status:
            status_text = typer.style(run_status, fg=typer.colors.WHITE, bold=True)
            typer.echo("status: " + status_text)
        run_duration = response_json.get("run_duration_seconds")
        if run_duration:
            logger.info(f"run_duration_seconds: {run_duration}")
        excluded_keys = ["status", "run_duration_seconds"]
        for k, v in response_json.items():
            if k not in excluded_keys:
                rich.print(f"{k}: {v}", flush=True)
    elif status == HTTPStatus.NOT_FOUND:
        logger.info("Node has not been registered yet..")
    else:
        logger.info("Failed to get node status..")


@node_app.command("llm-status", help="Get LLM status")
def llm_status(
    model_id: str = typer.Option(config.GALADRIEL_MODEL_ID, help="Model ID"),
    llm_base_url: Optional[str] = typer.Option(
        config.GALADRIEL_LLM_BASE_URL, help="LLM base url"
    ),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    init_logging(debug)
    config.validate()
    if not llm_base_url:
        llm_base_url = vllm.LLM_BASE_URL
    asyncio.run(check_llm(llm_base_url, model_id))


@node_app.command("benchmark", help="Benchmarks the node")
def benchmark(
    model_id: str = typer.Option(config.GALADRIEL_MODEL_ID, help="Model ID"),
    llm_base_url: Optional[str] = typer.Option(
        config.GALADRIEL_LLM_BASE_URL, help="LLM base url"
    ),
    concurrency: int = typer.Option(2, help="How many concurrent requests"),
    requests: int = typer.Option(10, help="How many requests per worker"),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    init_logging(debug)
    config.validate()
    if not llm_base_url:
        llm_base_url = vllm.LLM_BASE_URL
    asyncio.run(long_benchmark.execute(llm_base_url, model_id, concurrency, requests))


@node_app.command("stats", help="Get node stats")
def node_stats(
    api_url: str = typer.Option(config.GALADRIEL_API_URL, help="API url"),
    api_key: str = typer.Option(config.GALADRIEL_API_KEY, help="API key"),
    node_id: str = typer.Option(config.GALADRIEL_NODE_ID, help="Node ID"),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    init_logging(debug)
    config.validate()
    status, response_json = asyncio.run(
        version_aware_get(
            api_url, "node/stats", api_key, query_params={"node_id": node_id}
        )
    )
    if status == HTTPStatus.OK and response_json:
        rich.print("Received stats:")
        excluded_keys = ["completed_inferences"]
        for k, v in response_json.items():
            if k not in excluded_keys:
                rich.print(f"{k}: {v if v is not None else '<UNKNOWN>'}", flush=True)
        if response_json.get("completed_inferences"):
            rich.print("Latest completed inferences:", flush=True)
        for i in response_json.get("completed_inferences", []):
            rich.print(i, flush=True)


@node_app.command("upgrade", help="Upgrade the node to the latest version")
def node_upgrade(
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    init_logging(debug)
    try:
        logger.info("Updating galadriel CLI to the latest version...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "galadriel-node"]
        )
        logger.info(
            "galadriel CLI has been successfully updated to the latest version."
        )
    except subprocess.CalledProcessError:
        logger.info(
            "An error occurred while updating galadriel CLI. Please check your internet connection and try again.",
        )
    except Exception as _:
        logger.error("An unexpected error occurred.", exc_info=True)


if __name__ == "__main__":
    try:
        init_logging(True)
        asyncio.run(
            run_node(
                config.GALADRIEL_API_URL,
                config.GALADRIEL_RPC_URL,
                config.GALADRIEL_API_KEY,
                config.GALADRIEL_NODE_ID,
                config.GALADRIEL_LLM_BASE_URL,
            )
        )
    except SdkError as e:
        logger.error("Got an Exception when trying to run the node.", exc_info=True)
    except Exception as e:
        logger.error(
            "Got an unexpected Exception when trying to run the node.", exc_info=True
        )
