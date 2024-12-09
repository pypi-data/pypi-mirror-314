import base64
import json
import os
import requests
import time
import rich
import typer
from inferless_cli.commands.run.constants import BUILDING_DOCKER_MSG, MODEL_DIR_STRING
from inferless_cli.commands.run.helpers import (
    build_docker_image,
    check_and_convert_runtime_file,
    get_inferless_config,
    get_inputs_from_input_json,
    get_inputs_from_input_json_pytorch,
    get_runtime_file_location,
    is_docker_running,
    load_yaml_file,
    print_curl_command,
    print_docker_exec_command,
    print_load_model_curl_command,
    print_unload_model_curl_command,
    start_docker_container,
    update_model_file,
    create_config_from_json,
    stop_containers_using_port_8000,
)


from inferless_cli.commands.volume.volume_prompt import find_volume_by_id
from inferless_cli.utils.constants import SPINNER_DESCRIPTION
from rich.progress import Progress, SpinnerColumn, TextColumn

from inferless_cli.utils.exceptions import (
    ConfigurationError,
    InferlessCLIError,
    TritonError,
)
from inferless_cli.utils.helpers import (
    decrypt_tokens,
    log_exception,
)
from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    create_presigned_download_url,
    get_cli_files,
    get_file_download,
    get_templates_list,
    list_runtime_versions,
)


def run_prompt(
    runtime,
    runtime_type,
    name,
    env_dict,
    docker_base_url,
    is_local_runtime,
    volume,
    framework,
    input_schema_path,
    input_json_path,
    output_json_path,
    runtime_version
):
    try:
        config = InferlessConfigHandler()
        with Progress(
            SpinnerColumn(),
            TextColumn(SPINNER_DESCRIPTION),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description="Setting up things...", total=None)
            is_docker_running(docker_base_url)
            yaml_data = get_inferless_config(
                name,
                env_dict,
                is_local_runtime,
                volume,
                framework,
                input_schema_path,
                input_json_path,
                output_json_path,
                runtime,
                runtime_version
            )
            config.set_loaded_config(yaml_data)
            if is_local_runtime:
                check_and_convert_runtime_file(runtime, runtime_type)

            volume_path = get_volume_path(config, progress, task_id)
            model_name = config.get_value("name")
            runtime_file_path = None
            if is_local_runtime:
                runtime_file_path = get_runtime_file_location(runtime, config)

            configure_run_model(
                config,
                progress,
                task_id,
                model_name,
                runtime_file_path,
                volume_path,
                docker_base_url,
            )
    except ConfigurationError as error:
        rich.print(f"[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong {error}[/red]")
        raise typer.Abort(1)


def get_volume_path(config, progress, task_id):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()
        if config.get_value("configuration.custom_volume_id"):
            progress.update(task_id, description="Getting your Volume Mount details...")
            volume_data = find_volume_by_id(
                workspace_id, config.get_value("configuration.custom_volume_id")
            )
            volume_path = volume_data["path"]
            return volume_path
        return None
    except Exception:
        raise InferlessCLIError("\n[red]Error happened while finding volume [/red]\n")


def configure_run_model(
    config,
    progress,
    task_id,
    model_name,
    runtime_file_path,
    volume_path,
    docker_base_url,
):
    if config.get_value("source_framework_type") == "PYTORCH":
        progress.update(
            task_id,
            description="Generating required files for loading model...",
        )
        config_pbtxt_file_contents = get_cli_files("sample_config.pbtxt")
        config_pbtxt_file = base64.b64decode(config_pbtxt_file_contents).decode("utf-8")
        inputs = create_config_from_json(config, config_pbtxt_file)
        input_tensor, output_tensor, model_py_file = get_inputs_from_input_json_pytorch(
            config
        )
        update_model_file(input_tensor, output_tensor, model_py_file)

    else:
        inputs = get_inputs_from_input_json(config)

    runtime_dockerfile = custom_runtime_file(
        config, runtime_file_path, model_name, progress, task_id
    )
    progress.update(
        task_id,
        description=BUILDING_DOCKER_MSG,
    )
    build_docker_image(runtime_dockerfile, docker_base_url=docker_base_url)
    progress.update(
        task_id,
        description="Starting the Docker Container...",
    )
    env_vars = {}
    if config.get_value("env"):
        env_vars = config.get_value("env")
    stop_containers_using_port_8000(docker_base_url)
    if config.get_value("source_framework_type") == "PYTORCH":
        try:
            container = start_docker_container(
                volume_path=volume_path,
                autostart=False,
                env=env_vars,
                docker_base_url=docker_base_url,
            )
            time.sleep(10)
            load_model_template(model_name)
            time.sleep(5)
            infer_model(model_name, inputs)
            unload_model_template(model_name)
            load_model_template(model_name)
        except TritonError as e:
            rich.print(f"[red]Triton Error: [/red] {e}")
            log_exception(e)
    else:
        container = start_docker_container(
            volume_path=volume_path,
            autostart=True,
            env=env_vars,
            docker_base_url=docker_base_url,
        )

    progress.remove_task(task_id)

    rich.print("[green]Container started successfully.[/green]\n")
    rich.print(
        "\n[bold][yellow]Note: [/yellow][/bold]Container usually takes around 15 to 20 seconds to expose the PORT. cURL command should work after that.\n"
    )
    rich.print("\n[bold][underline]CURL COMMAND[/underline][/bold]\n")
    print_curl_command(model_name, inputs)

    rich.print("\n\n[bold][underline]ADVANCE USAGE[/underline][/bold]\n")
    print_docker_exec_command(container.id)

    rich.print(
        "\nInside the container, the app.py and model files are located in the model directory. You can access them by navigating to the following path: `[blue]cd /models/{model_name}/1[/blue]` in the container.\n This directory contains all the files related to your model, including app.py.\n"
    )

    rich.print(
        "\nYou can modify the app.py file and the model files as needed. However, for the changes to take effect, you need to unload and then reload the model using the following steps. \n"
    )

    rich.print("\nTo unload the model, execute the following curl command: \n")
    print_unload_model_curl_command(model_name)

    rich.print(
        "\nAfter modifying the files, reload the model using this curl command:  \n"
    )
    print_load_model_curl_command(model_name)

    rich.print(
        "\nThis command loads the updated model back into memory, making your changes effective.  \n"
    )


def custom_runtime_file(config, runtime_file_path, model_name, progress, task_id):

    progress.update(
        task_id,
        description="Analysing your runtime config...",
    )
    docker_file_contents = get_cli_files("default_template_dockerfile")
    default_template_dockerfile = base64.b64decode(docker_file_contents).decode("utf-8")
    default_template_dockerfile = default_template_dockerfile.replace(
        MODEL_DIR_STRING, f"/models/{model_name}/1/"
    )
    runtime_url = check_remote_runtime(config)
    if config.get_value("source_framework_type") == "PYTORCH":
        default_template_dockerfile = default_template_dockerfile.replace(
            "##configpbtxt##",
            f"COPY config.pbtxt /models/{model_name}/",
        )

    if runtime_file_path is not None and os.path.exists(runtime_file_path):
        runtime_dockerfile = get_local_runtime_docker_file(
            runtime_file_path, default_template_dockerfile
        )
        return runtime_dockerfile

    if runtime_url is not None:
        runtime_dockerfile = get_remote_runtime_docker_file(
            runtime_url, default_template_dockerfile
        )
        return runtime_dockerfile

    rich.print(
        "\n[yellow]No Custom runtime dectected. Using Inferless default runtime [/yellow]\n"
    )
    runtime_dockerfile = get_default_runtime_docker_file(default_template_dockerfile)
    return runtime_dockerfile


def get_default_runtime_docker_file(default_template_dockerfile):
    requirements_text_contents = get_cli_files("requirements.txt")
    requirements_text = base64.b64decode(requirements_text_contents).decode("utf-8")
    requirements_lines = requirements_text.strip().split("\n")
    requirements_lines = [
        line for line in requirements_lines if not line.strip().startswith("#")
    ]
    pip_install_commands = "\n".join(
        f"RUN pip install --no-cache-dir {line}"
        for line in requirements_lines
        if line.strip()
    )
    default_dockerfile = default_template_dockerfile.replace(
        "##piplibraries##", pip_install_commands
    )
    triton_version_string = "23.06-py3"

    default_dockerfile = default_dockerfile.replace(
        "##tritonversion##", triton_version_string
    )

    return default_dockerfile


def get_remote_runtime_docker_file(runtime_url, default_template_dockerfile):
    runtime_url = runtime_url.split("/")
    filename = runtime_url[len(runtime_url) - 2] + "/" + runtime_url[-1]
    payload = {
        "url_for": "YAML_FILE_DOWNLOAD",
        "file_name": filename,
    }
    res = create_presigned_download_url(payload)
    response = get_file_download(res)
    if response.status_code == 200:
        yaml_file = response.content
        default_template_dockerfile = load_yaml_file(
            yaml_file, default_template_dockerfile
        )

    return default_template_dockerfile


def get_local_runtime_docker_file(runtime_file_path, default_template_dockerfile):
    with open(runtime_file_path, "r") as yaml_file:
        default_template_dockerfile = load_yaml_file(
            yaml_file, default_template_dockerfile
        )
        return default_template_dockerfile


def check_remote_runtime(config):
    _, _, _, workspace_id, _ = decrypt_tokens()
    if config.get_value("configuration.custom_runtime_id"):
        runtime_id = config.get_value("configuration.custom_runtime_id")
        runtime_version = config.get_value("configuration.custom_runtime_version")
        runtimes_list = get_templates_list(workspace_id)
        runtime_url = None
        if runtime_version:
            runtime_url = get_runtime_version_url(runtime_id, runtime_version)
        else:
            for item in runtimes_list:
                # Use .get() for safer access to dictionary items
                item_id = item.get("id")
                if item_id == config.get_value("configuration.custom_runtime_id"):
                    runtime_url = item.get("template_url")
                    break

        if not runtime_url:
            raise InferlessCLIError(
                f"[yellow]runtime with id: {runtime_id}, not found! Please check if the rutime is avaliabe in current workspace"
            )

        return runtime_url
    return None


def get_runtime_version_url(runtime_id, runtime_version):
    res = list_runtime_versions({"template_id": runtime_id})
    for item in res:
        if item.get("version_no") == int(runtime_version):
            runtime_url = item.get("template_url")
            break
    if not runtime_url:
        raise InferlessCLIError(
            f"[yellow]runtime with id: {runtime_id}, and version: {runtime_version}, not found! Please check if the rutime is avaliabe in current workspace"
        )
    return runtime_url


def load_model_template(model_name):
    try:
        url = f"http://localhost:8000/v2/repository/models/{model_name}/load"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        log_exception(e)
        raise InferlessCLIError("[red]Failed to load model[/red]")


def unload_model_template(model_name):
    try:
        url = f"http://localhost:8000/v2/repository/models/{model_name}/unload"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        log_exception(e)
        raise TritonError("Failed to unload model")


def infer_model(model_name, inputs):
    try:
        url = f"http://localhost:8000/v2/models/{model_name}/infer"
        headers = {"Content-Type": "application/json"}
        data = json.dumps(inputs)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        log_exception(e)
        raise TritonError("Failed to infer model")
