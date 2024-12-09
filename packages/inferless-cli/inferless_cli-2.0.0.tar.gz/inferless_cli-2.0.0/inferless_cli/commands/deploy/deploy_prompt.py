import os
import tempfile
import time
import uuid
import rich
import typer
from inferless_cli.commands.deploy.constants import FAILED_TO_CREATE_MODEL_MESSAGE
from inferless_cli.commands.init.helpers import get_region_id
from inferless_cli.commands.runtime.runtime_prompt import upload_runtime_to_cloud
from inferless_cli.commands.volume.volume_prompt import find_volume_by_id
from inferless_cli.utils.constants import (
    GIT,
    SPINNER_DESCRIPTION,
)
from inferless_cli.utils.exceptions import (
    ConfigurationError,
    InferlessCLIError,
    ServerError,
)
from rich.progress import Progress, SpinnerColumn, TextColumn
from inferless_cli.utils.helpers import (
    convert_inferless_yaml_v1_to_v2,
    create_zip_file,
    decrypt_tokens,
    get_current_mode,
    is_inferless_yaml_present,
    log_exception,
    read_yaml,
    yaml
)
from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    create_presigned_io_upload_url,
    create_presigned_upload_url_hf_files_upload,
    get_machines,
    get_model_import_details,
    get_model_import_status,
    get_templates_list,
    get_workspace_regions,
    get_workspaces_list,
    import_model,
    rebuild_model,
    set_env_variables,
    set_onboarding_status,
    start_import_model,
    update_main_model_configuration,
    update_model_configuration,
    upload_file,
    upload_io,
    validate_github_url_permissions,
    validate_import_model,
    get_volume_by_name,
    get_runtime_by_name,
    get_secrets_by_name,
)


def deploy_prompt(
    gpu,
    region,
    beta,
    fractional,
    runtime,
    volume,
    env,
    inference_timeout,
    scale_down_timeout,
    container_concurrency,
    secrets,
    runtime_version,
    max_replica,
    min_replica,
    config_file_name,
    redeploy,
    is_local_runtime,
    volume_mount_path,
):
    region = validate_machine(gpu, region, fractional, beta)
    rich.print("\nWelcome to the Inferless Model Deployment! \n")

    try:
        is_old_config = convert_inferless_yaml_v1_to_v2(config_file_name)
        if is_old_config:
            rich.print(
                "[yellow]We have converted your inferless.yaml to the latest version. Please run the `inferless deploy --help` for more information on required arguments.[/yellow]"
            )

        config = InferlessConfigHandler()
        yaml_data = config_initilizer(config_file_name)
        setConfigData(
            config,
            yaml_data,
            gpu,
            region,
            beta,
            fractional,
            runtime,
            volume,
            env,
            inference_timeout,
            scale_down_timeout,
            container_concurrency,
            secrets,
            runtime_version,
            min_replica,
            max_replica,
            is_local_runtime,
            volume_mount_path
        )
        validate_yaml_data(yaml_data)
        config.set_loaded_config(yaml_data)
        check_serverless_access(config)
        check_for_old_deployment(config, config_file_name, redeploy)
        handle_model_import(config, redeploy)
        if config.get_value("import_source") != "DOCKER":
            handle_input_output_upload(config)
        model_validator(config)
        update_model_secrets(config)
        handle_model_configuration(config)
        handle_model_import_complete(config, config_file_name, redeploy)

    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)


def setConfigData(
    config,
    yaml_data,
    gpu,
    region,
    beta,
    fractional,
    runtime,
    volume,
    env,
    inference_timeout,
    scale_down_timeout,
    container_concurrency,
    secrets,
    runtime_version,
    min_replica,
    max_replica,
    is_local_runtime,
    volume_mount_path
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    secrets_ids = []
    if secrets:
        for secret in secrets:
            res = get_secrets_by_name(secret_name=secret)
            try:
                secrets_ids.append(res["id"])
            except:
                raise InferlessCLIError(f"Secret {secret} not found")

        yaml_data["secrets"] = secrets_ids
    config.set_loaded_config(yaml_data)

    if "import_source" in yaml_data and yaml_data["import_source"] == "FILE":
        yaml_data["io_schema"] = False
    else:
        yaml_data["io_schema"] = True

    config.update_config("configuration.gpu_type", gpu)
    config.update_config("configuration.is_serverless", beta)
    config.update_config("configuration.region", region)
    config.update_config("configuration.is_dedicated", not fractional)

    env_dict = {}
    for env_var in env:
        key, value = env_var.split("=", 1)
        env_dict[key] = value
    config.update_config("env", env_dict)

    config.update_config("configuration.inference_time", inference_timeout)
    config.update_config("configuration.scale_down_delay", scale_down_timeout)
    config.update_config("configuration.container_concurrency", container_concurrency)
    config.update_config("configuration.max_replica", max_replica)
    config.update_config("configuration.min_replica", min_replica)

    if runtime:
        if yaml_data["import_source"] == "DOCKER":
            rich.print("[yellow]Ignoring runtime selection. Runtime is not supported for Docker import type[/yellow]")
        else:
            if not is_local_runtime:
                res = get_runtime_by_name(workspace_id=workspace_id, runtime_name=runtime)
                config.update_config("configuration.custom_runtime_id", res["id"])
                if runtime_version:
                    config.update_config(
                        "configuration.custom_runtime_version", runtime_version
                    )

            if is_local_runtime:
                uid = uuid.uuid4()
                file_name = os.path.basename(runtime)
                payload = {
                    "url_for": "YAML_FILE_UPLOAD",
                    "file_name": f'{uid}/{file_name.replace(" ", "")}',
                }
                runtime_name = (
                    yaml_data.get("name") + "-" + "runtime" + "-" + str(uid).split("-")[0]
                )
                res = upload_runtime_to_cloud(
                    payload,
                    uid,
                    runtime_name,
                    region,
                    file_name,
                    runtime,
                    workspace_id,
                    False,
                    None,
                )
                if "id" in res and "name" in res:
                    config.update_config("configuration.custom_runtime_id", res["id"])

    if volume:
        res = get_volume_by_name(workspace_id=workspace_id, volume_name=volume)
        regions = get_workspace_regions({"workspace_id": workspace_id})
        region_value = get_region_id(
                region, regions
            )
        if res.get("region", None) != region_value:
            raise InferlessCLIError(
                f"Volume {volume} is not present in region {region}"
            )
        if "volume_id" in res:
            config.update_config("configuration.custom_volume_id", res["volume_id"])
            config.update_config("configuration.custom_volume_name", res["volume_name"])
            if volume_mount_path:
                config.update_config("configuration.custom_volume_mount", volume_mount_path)


def config_initilizer(config_file_name):
    is_yaml_present = is_inferless_yaml_present(config_file_name)

    if not is_yaml_present:
        raise ConfigurationError("Config file not found")

    yaml_data = read_yaml(config_file_name)
    if not yaml_data:
        raise ConfigurationError("Config Data not found")

    return yaml_data


def validate_yaml_data(yaml_data):
    required_fields = [
        "name",
        "import_source",
        "source_framework_type",
        "configuration.gpu_type",
        "configuration.inference_time",
        "configuration.is_dedicated",
        "configuration.is_serverless",
        "configuration.max_replica",
        "configuration.min_replica",
        "configuration.scale_down_delay",
        "configuration.region",
    ]

    # Function to recursively check for nested keys
    def check_nested_keys(data, key_path):
        keys = key_path.split(".")
        current_data = data
        for key in keys:
            if key not in current_data:
                raise ConfigurationError(
                    f"{key_path} is missing from the inferless.yaml file"
                )
            current_data = current_data[key]

    # Validate each required field
    for field in required_fields:
        check_nested_keys(yaml_data, field)


def check_serverless_access(config):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()
        if config.get_value("configuration.is_serverless"):
            with Progress(
                SpinnerColumn(),
                TextColumn(SPINNER_DESCRIPTION),
                transient=True,
            ) as progress:
                progress.add_task(
                    description="Checking Permissons. Please wait...", total=None
                )
                workspaces = get_workspaces_list()
            allow_serverless = False
            for workspace in workspaces:
                if workspace["id"] == workspace_id:
                    allow_serverless = workspace["allow_serverless"]
                    break
            if not allow_serverless:
                email_address = "nilesh@inferless.com"
                rich.print(
                    f"[red]Serverless is not enabled for your account [yellow](beta feature)[/yellow][/red] \nplease contact [blue]{email_address}[/blue]",
                )
                raise InferlessCLIError("Serverless is not enabled for your account")
    except Exception as e:
        raise Exception(f"Error at check_serverless_access - {e}")


def check_for_old_deployment(config, config_file_name, redeploy):

    if config.get_value("model_import_id"):
        if config.get_value("import_source") == GIT:
            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless redeploy`[/blue]\n"
            )
            raise InferlessCLIError(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )

        is_failed = False
        old_response = get_model_import_details(config.get_value("model_import_id"))
        if old_response and old_response.get("model_import").get("status") == "FAILURE":
            is_failed = True

        if not is_failed and not redeploy:

            rich.print(
                "if you want to redeploy the model please use this command [blue]`inferless redeploy`[/blue]\n"
            )
            raise InferlessCLIError(
                f"[red]model_import_id already exists in {config_file_name}.[/red] \nremove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]\n"
            )

        if config.get_value("name") != old_response.get("model_import").get("name"):

            raise InferlessCLIError(
                f"[red]name mismatch.[/red] Remove model_import_id from the {config_file_name} file for the new deployment and run command [blue]`inferless deploy`[/blue]"
            )

    if redeploy and not config.get_value("model_import_id"):
        raise InferlessCLIError(
            f"[red]model_import_id not found in {config_file_name}[/red]. To deploy run command [blue]`inferless deploy`[/blue]"
        )


def handle_model_import(config, redeploy):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:

        task_id = progress.add_task(description="Getting warmed up...", total=None)
        if config.get_value("import_source") == GIT:
            rich.print(
                "Deploying from git (make sure you have pushed your code to git)"
            )
            progress.update(task_id, description="Creating model...")
            details = handle_git_deployment(config)
        elif config.get_value("import_source") == "LOCAL":
            title = "Redeploying" if redeploy else "Deploying"
            description = (
                f"{title} from local directory (make sure you have saved your code)"
            )
            rich.print(description)
            rich.print("\n Make sure your [blue]app.py[/blue] is in this directory.")
            progress.update(task_id, description=f"{title} model...")
            details = handle_local_deployment(config, redeploy, progress, task_id,is_file=False)
        elif config.get_value("import_source") == "FILE":
            progress.update(task_id, description="Importing model...")
            details = handle_cloud_deployment(config, redeploy, progress, task_id)
        elif config.get_value("source_location") == "DOCKERFILE_REPO":
            source_location = config.get_value("source_location")
            rich.print(f"Deploying from {source_location}")
            progress.update(task_id, description="Importing model...")
            details = handle_dockerfile_deployment(config)
        elif config.get_value("source_location") == "DOCKER_REGISTRY":
            source_location = config.get_value("source_location")
            rich.print(f"Deploying from {source_location}")
            progress.update(task_id, description="Importing model...")
            details = handle_dockerhub_ecr_deployment(config)
        elif config.get_value("import_source") == "HUGGINGFACE":
            progress.update(task_id, description="Importing hf model...")
            details = handle_hf_deployment(config)
        else:
            details = None

        if details is None or not details.get("model_import").get("id"):
            raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)

        config.update_config("model_import_id", details.get("model_import").get("id"))
        rich.print("[green]Model initilized...![/green]")
        progress.remove_task(task_id)
        return details


def handle_git_deployment(config):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
    details = {}
    if config.get_value("provider") == "GITLAB":
        details = {
            "is_auto_build": False,
            "webhook_url": "",
            "gitlab_url": config.get_value("model_url"),
            "runtime": "PYTORCH",
        }
    else:
        details = {
            "is_auto_build": False,
            "webhook_url": "",
            "github_url": config.get_value("model_url"),
            "runtime": "PYTORCH",
        }
    payload = {
        "name": config.get_value("name"),
        "details": details,
        "import_source": GIT,
        "source_framework_type": config.get_value("source_framework_type"),
        "provider": config.get_value("provider"),
        "workspace": workspace_id,
    }
    details = import_model(payload)
    return details


def handle_cloud_deployment(config, redeploy, progress, task_id):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    
    provider = config.get_value("provider")
    if config.get_value("source_location") == "LOCAL_FILE":
        rich.print("Deploying from local file")
        details = handle_local_deployment(config, redeploy, progress, task_id, is_file=True)
        return details

    if config.get_value("source_location") == "CLOUD_URL":
        rich.print(
                f"Deploying from cloud url"
            )
        rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
        payload = {
            "name": config.get_value("name"),
            "details": {
                "is_auto_build": False,
                "webhook_url": "",
                "model_url": config.get_value("model_url"),
                "runtime": "PYTORCH",
            },
            "import_source": "FILE",
            "source_framework_type": config.get_value("source_framework_type"),
            "source_location": "CLOUD_URL",
            "provider": provider,
            "workspace": workspace_id,
        }
        details = import_model(payload)
        return details


def handle_dockerhub_ecr_deployment(config):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
    provider = (
        config.get_value("import_source") == "ECR" and "AMAZON_ECR" or "DOCKER_HUB"
    )

    payload = {
        "name": config.get_value("name"),
        "details": {
            "is_auto_build": False,
            "image_url": config.get_value("model_url"),
            "runtime": "PYTORCH",
            "health_api": config.get_value("health_api"),
            "infer_api": config.get_value("infer_api"),
            "port": str(config.get_value("server_port")),
        },
        "import_source": "DOCKER",
        "source_framework_type": config.get_value("source_framework_type"),
        "source_location": "DOCKER_REGISTRY",
        "provider": provider,
        "workspace": workspace_id,
    }

    details = import_model(payload)
    return details


def handle_dockerfile_deployment(config):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
    provider = config.get_value("provider")

    if(provider == "GITLAB"):
        details = {
                "is_auto_build": False,
                "dockerfile_path": config.get_value("docker_file_path"),
                "gitlab_url": config.get_value("model_url"),
                "runtime": "PYTORCH",
                "health_api": config.get_value("health_api"),
                "infer_api": config.get_value("infer_api"),
                "port": str(config.get_value("server_port")),
        }
    else:
        details = {
                "is_auto_build": False,
                "dockerfile_path": config.get_value("docker_file_path"),
                "github_url": config.get_value("model_url"),
                "runtime": "PYTORCH",
                "health_api": config.get_value("health_api"),
                "infer_api": config.get_value("infer_api"),
                "port": str(config.get_value("server_port")),
        }

    payload = {
        "name": config.get_value("name"),
        "details": details,
        "import_source": "DOCKER",
        "source_framework_type": config.get_value("source_framework_type"),
        "source_location": "DOCKERFILE_REPO",
        "provider": provider,
        "workspace": workspace_id,
    }
    details = import_model(payload)
    return details


def handle_hf_deployment(config):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    if (
        os.path.isfile("app.py")
        and os.path.isfile("input_schema.py")
    ):

        rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
        payload = {
            "name": config.get_value("name"),
            "details": {
                "huggingface_type": config.get_value("model_type"),
                "task_type": config.get_value("task_type"),
                "huggingface_name": config.get_value("hf_model_name"),
                "hf_files_url": "",
            },
            "import_source": "HUGGINGFACE",
            "source_framework_type": "PYTORCH",
            "provider": "GITHUB",
            "workspace": workspace_id,
        }
        details = import_model(payload)
        if details.get("model_import").get("id"):
            model_import_id = details.get("model_import").get("id")
            payload = {
                "url_for": "HUGGINGFACE_UPLOAD",
                "file_name": f"hf_import_files/{model_import_id}/app.py",
            }
            create_presigned_upload_url_hf_files_upload(payload, "app.py")
            payload_io = {
                "url_for": "HUGGINGFACE_UPLOAD",
                "file_name": f"hf_import_files/{model_import_id}/input_schema.py",
            }
            create_presigned_upload_url_hf_files_upload(payload_io, "input_schema.py")
            
            payload = {
                "name": config.get_value("name"),
                "details": {
                    "huggingface_type": config.get_value("model_type"),
                    "task_type": config.get_value("task_type"),
                    "huggingface_name": config.get_value("hf_model_name"),
                    "hf_files_url": f"hf_import_files/{model_import_id}",
                },
                "import_source": "HUGGINGFACE",
                "source_framework_type": "PYTORCH",
                "provider": "GITHUB",
                "workspace": workspace_id,
                "id": model_import_id,
            }
            details = import_model(payload)


        return details
    else:
        raise InferlessCLIError(
            "Missing required files. (app.py, input_schema.py)"
        )


def handle_local_deployment(config, redeploy, progress, task_id, is_file=False):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()
    rich.print(f"Using Workspace: [blue]{workspace_name}[/blue]")
    details = {
            "is_auto_build": False,
            "webhook_url": "",
            "upload_type": "local",
            "runtime": "PYTORCH",
        }
    if not is_file:
        details["is_cli_deploy"] = True

    payload = {
        "name": config.get_value("name"),
        "details": details,
        "import_source": "FILE",
        "source_framework_type": config.get_value("source_framework_type"),
        "source_location": "LOCAL_FILE",
        "workspace": workspace_id,
    }
    new_model, _ = checkMainModelStatus(config.get_value("model_import_id"))

    if redeploy:
        payload["id"] = config.get_value("model_import_id")

    if new_model:
        details = import_model(payload)
    else:
        details = get_model_import_details(config.get_value("model_import_id"))
        custom_runtime_url = (
            details.get("model_import")
            .get("configuration")
            .get("custom_docker_config", None)
        )
        if custom_runtime_url:
            config.update_config("configuration.custom_runtime_url", custom_runtime_url)

    if not details.get("model_import").get("id"):
        raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)

    progress.update(task_id, description="Uploading model to secure location...")

    payload["id"] = details.get("model_import").get("id")
    details = upload_model(payload,is_file=is_file)

    return details


def upload_model(payload, is_file=False):

    with tempfile.TemporaryDirectory() as temp_dir:
        directory_to_snapshot = os.getcwd()  # Current working directory

        model_id = payload.get("id")
        zip_filename = os.path.join(
            temp_dir, f"{os.path.basename(directory_to_snapshot)}.zip"
        )
        create_zip_file(zip_filename, directory_to_snapshot)
        if is_file:
            s3_key = (
                f"model_zip_files/{model_id}/{os.path.basename(directory_to_snapshot)}.zip"
            )
        else: 
            s3_key = (
                f"cli_zip_files/{model_id}/{os.path.basename(directory_to_snapshot)}.zip"
            )

        file_size = os.path.getsize(zip_filename)
        with open(zip_filename, "rb") as zip_file:

            model_url = upload_file(zip_file, s3_key, file_size, upload_type="ZIP")
            payload["details"]["model_url"] = model_url
            payload["id"] = model_id

        details = import_model(payload)
        if not details.get("model_import").get("id"):
            raise InferlessCLIError(FAILED_TO_CREATE_MODEL_MESSAGE)
        return details


def handle_input_output_upload(config):

    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Uploading input_schema.py / input.json and output.json",
            total=None,
        )
        model_id = config.get_value("model_import_id")
        io_schema = False

        if config.get_value("io_schema"):
            io_schema = config.get_value("io_schema")

        if not io_schema:

            input_file_name = f"{model_id}/input.json"
            output_file_name = f"{model_id}/output.json"
            input_payload = {
                "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                "file_name": input_file_name,
            }
            output_payload = {
                "url_for": "INPUT_OUTPUT_JSON_UPLOAD",
                "file_name": output_file_name,
            }
            create_presigned_io_upload_url(
                input_payload, "input.json"
            )
            create_presigned_io_upload_url(
                output_payload, "output.json"
            )
            S3_BUCKET_NAME = "infer-data"
            if get_current_mode() == "DEV":
                S3_BUCKET_NAME = "infer-data-dev"
            s3_input_url = f"s3://{S3_BUCKET_NAME}/{input_file_name}"
            s3_output_url = f"s3://{S3_BUCKET_NAME}/{output_file_name}"
            _ = upload_io(
                {
                    "id": model_id,
                    "input_json": {"s3_infer_data_url": s3_input_url},
                    "output_json": {"s3_infer_data_url": s3_output_url},
                }
            )


def model_validator(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        progress.add_task(
            description="Validating the model...",
            total=None,
        )
        model_id = config.get_value("model_import_id")
        if not model_id:
            raise InferlessCLIError("Model id is not available. Please try again.")

        if config.get_value("import_source") == GIT and config.get_value("provider") == "GITHUB":
            validate_github_url_permissions(url=config.get_value("model_url"))
        start_import_model({"id": model_id})
        status, res = poll_model_status(model_id)

        if status == "FAILURE":
            error_msg = res["model_import"]["import_error"]["message"]
            rich.print(f"[red]{error_msg}[/red]")
            raise InferlessCLIError(error_msg)
        rich.print("[green]Model Validated...![/green]")


def poll_model_status(id):
    start_time = time.time()
    while True:

        response = get_model_import_details(id)

        status = response.get("model_import", {}).get("status")

        if status in ["FILE_STRUCTURE_VALIDATED", "SUCCESS", "FAILURE"]:
            return status, response

        if status in ["FILE_STRUCTURE_VALIDATION_FAILED", "IMPORT_FAILED"]:
            raise InferlessCLIError(f"Status was {status}, response was: {response}")

        elapsed_time = time.time() - start_time
        if elapsed_time >= 5 * 60:
            raise InferlessCLIError("Structure validation timed out after 5 minutes")

        time.sleep(5)


def handle_model_configuration(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        _, _, _, workspace_id, _ = decrypt_tokens()
        progress.add_task(
            description="Updating model configuration...",
            total=None,
        )
        region_value = "AZURE"

        if config.get_value("configuration.region"):
            regions = get_workspace_regions({"workspace_id": workspace_id})
            region_value = get_region_id(
                config.get_value("configuration.region"), regions
            )
            if region_value is None:
                region_value = "AZURE"
        else:
            raise InferlessCLIError(
                "Region not found in inferless.yaml. Please add it and try again."
            )

        new_model, model_id = checkMainModelStatus(config.get_value("model_import_id"))

       
        config_payload = {
            "id": config.get_value("model_import_id"),
            "configuration": {
                "region": region_value,
                "runtime": "PYTORCH",
                "inference_time": str(config.get_value("configuration.inference_time")),
                "is_auto_build": False,
                "is_dedicated": config.get_value("configuration.is_dedicated"),
                "machine_type": config.get_value("configuration.gpu_type"),
                "is_serverless": config.get_value("configuration.is_serverless"),
                "max_replica": str(config.get_value("configuration.max_replica")),
                "min_replica": str(config.get_value("configuration.min_replica")),
                "scale_down_delay": str(config.get_value("configuration.scale_down_delay")),
                "container_concurrency": config.get_value("configuration.container_concurrency"),
                "is_transformers_accelerated": False,
                "skip_validation": True
            },
        }


        if config.get_value("branch"):
            config_payload["configuration"]["build_branch"] = config.get_value("branch")

        if config.get_value("configuration.custom_volume_id") and config.get_value(
            "configuration.custom_volume_name"
        ):
            volume_data = find_volume_by_id(
                workspace_id, config.get_value("configuration.custom_volume_id")
            )
            if not volume_data or volume_data.get("region") != region_value:
                raise InferlessCLIError(
                    "Volume id not found. Please check the volume id and try again."
                )

            config_payload["configuration"]["custom_volume_config"] = config.get_value(
                "configuration.custom_volume_id"
            )
            config_payload["configuration"]["custom_volume_name"] = config.get_value(
                "configuration.custom_volume_name"
            )
            if config.get_value("configuration.custom_volume_mount"):
                config_payload["configuration"]["custom_volume_mount"] = config.get_value(
                    "configuration.custom_volume_mount"
                )

        if config.get_value("configuration.custom_runtime_id"):
            runtimes = get_templates_list(workspace_id)

            runtime_id = config.get_value("configuration.custom_runtime_id")
            runtime = None

            for rt in runtimes:

                if rt["id"] == runtime_id and rt["region"] == region_value:
                    runtime = rt
                    break

            if runtime is None:
                raise InferlessCLIError(
                    "Runtime id not found. Please check the runtime id and try again."
                )

            config_payload["configuration"]["custom_docker_template"] = runtime_id
            if config.get_value("configuration.custom_runtime_version"):
                config_payload["configuration"]["custom_docker_version"] = int(
                    config.get_value("configuration.custom_runtime_version")
                )
            if config.get_value("configuration.custom_runtime_url") and not new_model:
                config_payload["configuration"]["custom_docker_config"] = (
                    config.get_value("configuration.custom_runtime_url")
                )
            else:
                config_payload["configuration"]["custom_docker_config"] = ""
                
        if new_model:
            update_model_configuration(config_payload)
        elif not new_model and model_id:
            payload = config_payload["configuration"]
            payload["model_id"] = model_id
            update_main_model_configuration(payload)

        rich.print("[green]Model Configuration Updated...![/green]")


def update_model_secrets(config):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:

        if config.get_value("env") or config.get_value("secrets"):
            progress.add_task(
                description="Setting environment variables...",
                total=None,
            )
            env_payload = {
                "model_import_id": config.get_value("model_import_id"),
                "variables": config.get_value("env") or {},
                "credential_ids": config.get_value("secrets") or [],
                "patch": False,
            }
            set_env_variables(env_payload)
            rich.print("[green]Model Environment/Secrets Updated...![/green]")


def handle_model_import_complete(config, config_file_name, redeploy):
    with Progress(
        SpinnerColumn(),
        TextColumn(SPINNER_DESCRIPTION),
        transient=True,
    ) as progress:
        model_id = config.get_value("model_import_id")
        progress.add_task(
            description="Finalizing model import...",
            total=None,
        )

        new_model, _ = checkMainModelStatus(config.get_value("model_import_id"))
        if new_model:
            validate_import_model({"id": model_id})
        elif not new_model and model_id:
            rebuild_model(model_id)

        description = "Model import started, here is your model_import_id: "
        if redeploy:
            description = "Redeploying the model, here is your model_import_id: "
        config.save_config(config_file_name)

        rich.print(f"\n{description} [blue]{model_id}[/blue] \n")
        message = (
            "You can check the logs by running this command:\n\n"
            f"[blue]inferless log -i {model_id}[/blue]"
        )
        set_onboarding_status({"onboarding_type": "cli", "state": "deployed"})
        rich.print(message)


def checkMainModelStatus(model_import_id):
    new_model = True
    model_id = None
    try:
        res = get_model_import_status(model_import_id)
        new_model = False
        model_id = res.get("model_id", None)
    except ServerError:
        pass
    except Exception:
        pass
    return new_model, model_id


def validate_machine(machine_type, region=None, fractional=False, beta=False):
    # _, _, _, workspace_id, _ = decrypt_tokens()
    # regions = get_workspace_regions({"workspace_id": workspace_id})
    # Define default regions
    default_regions_non_beta = {'T4': 'region-1', 'A100': 'region-2', 'A10': 'region-1'}
    default_regions_beta = {'T4': 'region-3', 'A100': 'region-6', 'A10': 'region-3'}

    # Determine machine type and deploy type
    machine_type_actual = 'SHARED' if fractional else 'DEDICATED'

    # Fetch all machines
    machines = get_machines()

    # Filter machines matching the machine_type and deploy_type
    filtered_machines = [
        m for m in machines if m['name'] == machine_type and m['machine_type'] == machine_type_actual
    ]

    if not filtered_machines:
        raise InferlessCLIError(f"No machines found for type '{machine_type}' with type '{machine_type_actual}'.")

    # If region is None, return default region
    if region is None:
        default_region = default_regions_beta[machine_type] if beta else default_regions_non_beta[machine_type]
        return default_region

    # Check if region is valid
    available_regions = {m['region_name'] for m in filtered_machines}
    if region not in available_regions:
        raise InferlessCLIError(
            f"The machine type '{machine_type}' is not available in region '{region}'. "
            f"Available regions: {', '.join(available_regions)}"
        )

    # Additional beta logic
    if beta:
        expected_region = default_regions_beta[machine_type]
        if region != expected_region:
            raise InferlessCLIError(f"Use '{expected_region}' for beta.")

    return region
