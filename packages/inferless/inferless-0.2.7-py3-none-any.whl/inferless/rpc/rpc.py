import base64
import json
import os
import dill
import requests
import rich
from . import config_yaml
from inferless.auth.token import auth_header
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from inferless.utils import get_working_dir_zip

RUNTIME_BUILD_COMPLETED = "RUNTIME_BUILD_COMPLETED"
RUNTIME_BUILD_STARTED = "RUNTIME_BUILD_STARTED"
INFERENCE_COMPLETED = "INFERENCE_COMPLETED"
INFERENCE_STARTED = "INFERENCE_STARTED"
RUNTIME_CACHE_HIT = "RUNTIME_CACHE_HIT"


def call_rpc(data, entrypoint_file, config_path, ignore_file, gpu):
    is_exception_handled = False
    event = None
    try:
        console = Console()
        spinner = Spinner("dots", "Processing...")
        live = Live(spinner, refresh_per_second=10, transient=True)
        live.start()
        payload = get_rpc_payload(data, entrypoint_file, config_path, ignore_file, gpu)
        headers = auth_header()
        url = get_rpc_url(gpu)
        spinner.text = "Getting Infra ready..."
        live.update(spinner)
        with requests.post(url, json=payload, stream=True, headers=headers, timeout=600) as response:
            for line in response.iter_lines():
                if line:
                    msg_type = line.decode("utf-8").split(":")[0]
                    if msg_type == "event":
                        event = line.decode("utf-8")[6:]
                        if event == RUNTIME_BUILD_STARTED:
                            live.stop()
                            console.print("[green]Infra is ready \u2713[/green]")
                            spinner.text = "Building runtime..."
                            live = Live(spinner, refresh_per_second=10, transient=True)
                            live.start()
                        elif event == RUNTIME_BUILD_COMPLETED:
                            live.stop()
                            console.print("[green]Runtime is ready \u2713[/green]")
                            spinner.text = "Waiting for inference to start..."
                            live = Live(spinner, refresh_per_second=10, transient=True)
                            live.start()
                        elif event == RUNTIME_CACHE_HIT:
                            live.stop()
                            console.print("[green]Infra is ready \u2713[/green]")
                            console.print("[green]Runtime is ready \u2713[/green]")
                            spinner.text = "Waiting for inference to start..."
                            live = Live(spinner, refresh_per_second=10, transient=True)
                            live.start()
                        elif event == INFERENCE_STARTED:
                            live.stop()
                            spinner.text = "Execution started..."
                            live = Live(spinner, refresh_per_second=10, transient=True)
                            live.start()
                        elif event == INFERENCE_COMPLETED:
                            live.stop()
                            console.print("[green]Execution \u2713[/green]")
                            spinner.text = "Waiting for result..."
                            live = Live(spinner, refresh_per_second=10, transient=True)
                            live.start()
                    elif msg_type == "result":
                        live.stop()
                        result = line.decode("utf-8")[7:]
                        return get_rpc_result(result)
                    elif msg_type == "error":
                        live.stop()
                        error_msg = line.decode("utf-8")[6:]
                        rich.print(f"[red]{error_msg}[/red]")
                        is_exception_handled = True
                        raise SystemExit
    except KeyboardInterrupt:
        live.stop()
        rich.print("\n[red]Execution interrupted by user[/red]")
        is_exception_handled = True
        raise SystemExit
    except Exception as e:
        live.stop()
        rich.print(f"[red]Failed to call the RPC[/red]")
        rich.print(f"[red]{e}[/red]")
        is_exception_handled = True
        raise SystemExit
    finally:
        live.stop()
        if event != INFERENCE_COMPLETED and is_exception_handled is False:
            rich.print(f"[red]Internal Server Error[/red]")
            raise SystemExit


def get_rpc_payload(data, entrypoint_file, config_path, ignore_file, gpu):
    payload = {}
    configuration_yaml = config_yaml.get_config_yaml(config_path, gpu)
    payload["execution_data"] = base64.b64encode(dill.dumps(data, recurse=True)).decode("utf-8")
    base_dir = os.path.dirname(entrypoint_file)
    working_dir_data = get_working_dir_zip(base_dir, ignore_file)
    payload["working_dir"] = working_dir_data
    json_data = json.dumps(payload)
    payload = {
        "rpc_payload": json_data,
        "configuration_yaml": configuration_yaml,
    }
    return payload


def get_rpc_headers():
    token_header = auth_header()
    headers = token_header.update(
        {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Transfer-Encoding": "chunked",
            "Connection": "keep-alive"
        }
    )
    return headers


def get_rpc_result(result):
    data = json.loads(result)
    request_id = data.get("request_id")
    result = data.get("result")
    try:
        output = json.loads(result)
        if output.get("error"):
            rich.print(f"\n[red]{output['error_msg']}[/red]\n")
            rich.print(f"{output['error']}")
            rich.print("\n[white].............................[/white]")
            raise SystemExit
        if output.get("logs"):
            rich.print(f"[blue]Standard Output[/blue]\n")
            rich.print(f"{output['logs']}")
            rich.print("\n[white].............................[/white]")
        if output.get("result"):
            return output.get("result")
        else:
            rich.print(f"[yellow]No result returned[/yellow]")
            return None
    except SystemExit:
        raise SystemExit
    except Exception as e:
        raise Exception(f"Internal error occurred. Request ID for reference: {request_id}, error: {e}")


def get_rpc_url(gpu):
    if os.getenv("INFERLESS_ENV") == "DEV":
        return "http://aab1b24401e6d40ee819a4a85da88501-394555867.us-east-1.elb.amazonaws.com/api/v1/rpc/start"
    elif gpu == "A100":
        return "https://serverless-v3.inferless.com/api/v1/rpc/start"

    return "https://serverless-region-v1.inferless.com/api/v1/rpc/start"
