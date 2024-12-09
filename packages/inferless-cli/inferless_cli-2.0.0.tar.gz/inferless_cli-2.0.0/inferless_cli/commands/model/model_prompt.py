from typing import List
import dateutil
from prompt_toolkit.validation import Validator
import typer
from typing_extensions import Annotated, Optional
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.commands.deploy.deploy_prompt import check_for_old_deployment, config_initilizer, handle_input_output_upload, handle_model_import, model_validator,validate_machine
from inferless_cli.commands.init.helpers import get_region_id
from inferless_cli.commands.runtime.runtime_prompt import get_regions, get_regions_values
from inferless_cli.utils.constants import DEFAULT_YAML_FILE_NAME, SPINNER_DESCRIPTION
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import (
    check_import_source,
    convert_inferless_yaml_v1_to_v2,
    decrypt_tokens,
    get_models,
    get_by_keys,
    is_inferless_yaml_present,
    key_bindings,
    log_exception,
    read_yaml,
)

from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    activate_model,
    deactivate_model,
    delete_model,
    get_secrets_by_name,
    get_templates_list,
    get_volume_by_name,
    get_workspace_models,
    get_workspace_regions,
    rebuild_model,
    get_model_code,
    get_model_details,
    set_env_variables,
    update_main_model_configuration,
)
from inferless_cli.utils.validators import validate_models


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = SPINNER_DESCRIPTION
no_models = "[red]No models found in your workspace[/red]"
model_id_string = "Model ID"


@app.command(
    "rebuild",
    help="rebuild a model. (If you have a inferless.yaml file in your current directory, you can use the --local or -l flag to redeploy the model locally.)",

)
def rebuild(
    model_id: str = typer.Option(None,help="Model ID"),
    local: bool = typer.Option(False, "--local", "-l", help="Local rebuild"),
):
    try:
        is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)
        if (
            is_yaml_present
            and not local
            and check_import_source(DEFAULT_YAML_FILE_NAME)
        ):
            is_old_config = convert_inferless_yaml_v1_to_v2(DEFAULT_YAML_FILE_NAME)
            if is_old_config:
                rich.print(
                    "[yellow]We have converted your inferless.yaml to the latest version."
                )
            config = read_yaml(DEFAULT_YAML_FILE_NAME)
            if "import_source" in config and config["import_source"] == "LOCAL":
                temp_model_id = config.get("model_import_id")
                if temp_model_id:
                    local = typer.confirm(
                        f"Found {DEFAULT_YAML_FILE_NAME} file. do you want to redeploy? "
                    )
        if local:
            config_file_name = DEFAULT_YAML_FILE_NAME
            if check_import_source(config_file_name):
                is_old_config = convert_inferless_yaml_v1_to_v2(config_file_name)
                if is_old_config:
                    rich.print(
                        "[yellow]We have converted your inferless.yaml to the latest version."
                    )
                config = InferlessConfigHandler()
                yaml_data = config_initilizer(config_file_name)
                if "import_source" in yaml_data and yaml_data["import_source"] == "FILE" :
                    yaml_data["io_schema"] = False
                else:
                    yaml_data["io_schema"] = True
                config.set_loaded_config(yaml_data)
                check_for_old_deployment(config, config_file_name, True)
                handle_model_import(config, True)
                model_validator(config)

                if "import_source" in yaml_data and yaml_data["import_source"] == "FILE" :
                    handle_input_output_upload(config)

                rebuild_model(config.get_value("model_import_id"))
                rich.print("[green]Model rebuilt successfully[/green]")
            else:
                rich.print(
                    "[yellow]Warning:[/yellow] Only local models can be rebuilt locally using inferless.yaml, for [blue]GIT[/blue] based deployment don't use [blue]`--local`[/blue] or [blue]-l[/blue] flag"
                )
                rebuild_model_fun(model_id)
        else:
            rebuild_model_fun(model_id)
    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


def rebuild_model_fun(model_id):
    try:
        models = {}
        _, _, _, workspace_id, _ = decrypt_tokens()
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)

            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to rebuild: ",
                completer=get_models(models=models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(
                        choice, models=models["models"]["models"]
                    )
                ),
                validate_while_typing=False,
            )
            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        model_name = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                raise InferlessCLIError(
                    f"Model with id: [bold]{model_id}[/bold] not found"
                )

            details = get_model_details(model_id)
            rebuild_model(details["models"]["model_import"])

            progress.remove_task(task_id)

        rich.print(f"Rebuilding model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "patch",
    help="patch model configuration.",
)
def patch(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
    gpu: str = typer.Option(
        None, "--gpu", help="Denotes the machine type (A10/A100/T4)."
    ),
    fractional: bool = typer.Option(
        False, "--fractional", help="Use fractional machine type (default: dedicated)."
    ),
    volume: str = typer.Option(None, "--volume", help="Volume name."),
    mount_path: str = typer.Option(
        None, "--mount-path", help="Volume Mount path for the volume."
    ),
    env: List[str] = typer.Option(
        None, "--env", help="Key-value pairs for model environment variables."
    ),
    inference_timeout: int = typer.Option(
        None, "--inference-timeout", help="Inference timeout in seconds."
    ),
    scale_down_timeout: int = typer.Option(
        None, "--scale-down-timeout", help="Scale down timeout in seconds."
    ),
    container_concurrency: int = typer.Option(
        None, "--container-concurrency", help="Container concurrency level."
    ),
    secret: List[str] = typer.Option(
        None, "--secret", help="Secret names to attach to the deployment."
    ),
    runtime_version: str = typer.Option(
        None, "--runtimeversion", help="Runtime version (default: latest)."
    ),
    max_replica: int = typer.Option(
        None, "--max-replica", help="Maximum number of replicas."
    ),
    min_replica: int = typer.Option(
        None, "--min-replica", help="Minimum number of replicas."
    ),
):  
    try:
        if model_id is None:
            raise typer.BadParameter("Model ID is required.")
        
        details = get_model_details(model_id)
        regions = get_regions_values()
        gpu = gpu.upper()
        if gpu not in ["A10", "A100", "T4"]:
            raise typer.BadParameter("GPU must be one of A10, A100, or T4.")

        mapped_region = get_regions(details["models"]["configuration"]["region"], regions)
        region = validate_machine(gpu, mapped_region, fractional, details["models"]["configuration"]["is_serverless"] )

        if inference_timeout:   
            if not (1 <= inference_timeout <= 7200):
                raise typer.BadParameter(
                    "Inference timeout must be between 1 and 7200 seconds."
                )

        # validate max and min replicas also check if its number
        if max_replica is not None and min_replica is not None:
            if max_replica < min_replica:
                raise typer.BadParameter(
                    "Max replicas must be greater than or equal to min replicas."
                )
            
            if not isinstance(max_replica, int) or not isinstance(min_replica, int):
                raise typer.BadParameter("Max replicas and min replicas must be integers.")


        with Progress(
            SpinnerColumn(),
            TextColumn(SPINNER_DESCRIPTION),
            transient=True,
        ) as progress:
            _, _, _, workspace_id, _ = decrypt_tokens()


            env_dict = {}
            for env_var in env:
                key, value = env_var.split("=", 1)
                env_dict[key] = value


            secrets_ids = []
            if secret:
                for secretVal in secret:
                    res = get_secrets_by_name(secret_name=secretVal)
                    try:
                        secrets_ids.append(res["id"])
                    except:
                        raise InferlessCLIError(f"Secret {secret} not found")
                    
            if env_dict or secrets_ids:
                progress.add_task(
                    description="Setting environment variables...",
                    total=None,
                )
                env_payload = {
                    "model_import_id": details["models"]["model_import"],
                    "variables": env_dict or {},
                    "credential_ids": secrets_ids or [],
                    "patch": True,
                }
                set_env_variables(env_payload)
                rich.print("[green]Model Environment/Secrets Updated...![/green]")
            
            progress.add_task(
                description="Updating model configuration...",
                total=None,
            )
        

            
            configuration = {}

            if gpu and region:
                configuration["machine_type"] = gpu

            if inference_timeout:
                configuration["inference_time"] = str(inference_timeout)
            
            if max_replica:
                configuration["max_replica"] = str(max_replica)

            if min_replica:
                configuration["min_replica"] = str(min_replica)
            
            if scale_down_timeout:
                configuration["scale_down_delay"] = str(scale_down_timeout)

            if fractional:
                configuration["is_dedicated"] = False
            else:
                configuration["is_dedicated"] = True

            if container_concurrency:
                configuration["container_concurrency"] = container_concurrency

            regions = get_workspace_regions({"workspace_id": workspace_id})
            region_value = get_region_id(
                        region, regions
                    )
            if volume:
                res = get_volume_by_name(workspace_id=workspace_id, volume_name=volume)
               
                if res.get("region", None) != region_value:
                    raise InferlessCLIError(
                        f"Volume {volume} is not present in region {region}"
                    )
                if "volume_id" in res:
                    configuration["custom_volume_config"] = res.get("volume_id")
                    configuration["custom_volume_name"] = res.get("volume_name")
                if mount_path:
                    configuration["custom_volume_mount"] = mount_path
            


        
            if "custom_docker_template" in details["models"]["configuration"]:
                runtimes = get_templates_list(workspace_id)

                runtime_id = details["models"]["configuration"]["custom_docker_template"]
                runtime = None

                for rt in runtimes:

                    if rt["id"] == runtime_id and rt["region"] == region_value:
                        runtime = rt
                        break

                if runtime is None:
                    raise InferlessCLIError(
                        "Custom Runtime not found for this model"
                    )
                
                configuration["custom_docker_template"] = runtime_id
                configuration["custom_docker_version"] = runtime_version
                configuration["custom_docker_config"] = details["models"]["configuration"]["custom_docker_config"]

            configuration["model_id"] = model_id
            update_main_model_configuration(configuration)

            rich.print("[green]Model Configuration Updated...![/green]")

    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
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



@app.command(
    "list",
    help="List all models.",
)
def list_models():
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        table = Table(
            title="Model List",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column("ID", style="yellow")
        table.add_column(
            "Name",
        )
        table.add_column("Created At")
        table.add_column("Updated At")
        table.add_column("Is Serverless")
        table.add_column("Status")

        for model in models["models"]["models"]:
            created_at = "-"
            updated_at = "-"
            try:
                created_at = dateutil.parser.isoparse(model["created_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception as e:
                log_exception(e)
            try:
                updated_at = dateutil.parser.isoparse(model["updated_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            except Exception as e:
                log_exception(e)

            table.add_row(
                model["id"],
                model["name"],
                created_at,
                updated_at,
                "Yes" if model["is_serverless"] else "No",
                model["status"],
            )

        total_models = models["models"]["total_models"]
        total_models_deployed = models["models"]["total_models_deployed"]

        console = Console()
        console.print(table)
        console.print("\n")
        # Display total models and total models deployed
        console.print(f"Total Models: [bold]{total_models}[/bold]\n")
        console.print(f"Total Models Deployed: [bold]{total_models_deployed}[/bold]\n")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "deactivate",
    help="deactivate a model. ",
)
def deactivate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)

            models = get_workspace_models(
                workspace_id=workspace_id, workspace_filter="ACTIVE"
            )

            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(
                "[red]No Active models found in your workspace[/red]"
            )

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to deactivate: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        validate = typer.confirm("Are you sure you want to deactivate this model? ")
        if validate:
            model_name = None
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description=processing, total=None)
                model_name = get_by_keys(
                    models["models"]["models"],
                    model_id,
                    "id",
                    "name",
                )
                if model_name is None:
                    raise InferlessCLIError(
                        f"Model with id: [bold]{model_id}[/bold] not found"
                    )

                deactivate_model(model_id)
                progress.remove_task(task_id)

            rich.print(f"Deactivating model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "activate",
    help="activate a model. ",
)
def activate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(
                workspace_id=workspace_id, workspace_filter="INACTIVE"
            )
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(
                "[red]No Deactivated models found in your workspace[/red]"
            )

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to activate: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                raise InferlessCLIError(
                    f"Model with id: [bold]{model_id}[/bold] not found"
                )

            activate_model(model_id)

            progress.remove_task(task_id)

            rich.print(f"Activating model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command(
    "delete",
    help="delete a model.",
)
def delete(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to delete: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        validate = typer.confirm("Are you sure you want to delete this model? ")
        if validate:
            model_name = None
            with Progress(
                SpinnerColumn(),
                TextColumn(desc),
                transient=True,
            ) as progress:
                task_id = progress.add_task(description=processing, total=None)
                model_name = get_by_keys(
                    models["models"]["models"],
                    model_id,
                    "id",
                    "name",
                )
                if model_name is None:
                    raise InferlessCLIError(
                        f"Model with id: [bold]{model_id}[/bold] not found"
                    )
                delete_model(model_id)
                progress.remove_task(task_id)
            rich.print(f"Deleted model: [bold]{model_name}[/bold]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command("info", help="Get model details.")
def info(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        models = {}

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            models = get_workspace_models(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(models["models"]["models"]) == 0:
            raise InferlessCLIError(no_models)

        if model_id is None:
            modal_name = prompt(
                "Select the model you want to get details for: ",
                completer=get_models(models["models"]["models"]),
                complete_while_typing=True,
                key_bindings=key_bindings,
                validator=Validator.from_callable(
                    lambda choice: validate_models(choice, models["models"]["models"])
                ),
                validate_while_typing=False,
            )

            model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

        model_name = None
        data = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)

            model_name = get_by_keys(
                data=models["models"]["models"],
                value=model_id,
                key1="id",
                key2="name",
            )
            if model_name is None:
                raise InferlessCLIError(
                    f"Model with id: [bold]{model_id}[/bold] not found"
                )

            data = get_model_code(model_id)

            progress.remove_task(task_id)

        if data is not None:
            rich.print("[bold]Details:[/bold]")
            rich.print(f"[green]Name:[/green] {model_name}")
            rich.print(f"[green]ID:[/green] {model_id}")
            rich.print(f"[green]URL:[/green] {data['location']}\n")

    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)
