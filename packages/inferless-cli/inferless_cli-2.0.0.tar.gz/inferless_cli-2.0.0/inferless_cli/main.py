# EXTERNAL PACKAGES
import os
import rich
import typer
import sys
from typing import Optional, List

# COMMANDS
from inferless_cli.commands.deploy.deploy_prompt import deploy_prompt
from inferless_cli.commands.export.export_prompt import export_runtime_configuration
from inferless_cli.commands.init import init_default
from inferless_cli.commands.integration import integration_prompt
from inferless_cli.commands.log.log_prompt import log_prompt
from inferless_cli.commands.region import region_prompt
from inferless_cli.commands.run.run_prompt import run_prompt
from inferless_cli.commands.scaffold import scaffold_prompt
from inferless_cli.commands.volume import volume_prompt
from inferless_cli.commands.token import token_prompt
from inferless_cli.commands.login.login_prompt import login_prompt
from inferless_cli.commands.secret import secret_prompt
from inferless_cli.commands.workspace import workspace_prompt
from inferless_cli.commands.model import model_prompt
from inferless_cli.commands.runtime import runtime_prompt
from inferless_cli.commands.remote_run.remote_run_prompt import remote_run_prompt


# UTILS
from inferless_cli.utils.constants import (
    DEFAULT_RUNTIME_FILE_NAME,
    DEFAULT_YAML_FILE_NAME,
    PROVIDER_CHOICES,
)
from inferless_cli.utils.exceptions import InferlessCLIError
from inferless_cli.utils.helpers import sentry_init, set_env_mode, version_callback
from inferless_cli.utils.services import (
    callback_with_auth_validation,
    min_version_required,
)

sys.tracebacklimit = 0
sentry_init()


app = typer.Typer(
    name="Inferless CLI",
    add_completion=True,
    rich_markup_mode="markdown",
    no_args_is_help=True,
    pretty_exceptions_enable=True,
    help="""
    Inferless - Deploy Machine Learning Models in Minutes.

    See the website at https://inferless.com/ for documentation and more information
    about running code on Inferless.
    """,
    callback=sentry_init,
)


@app.callback()
def inferless(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback),
):
    """
    This function is currently empty because it is intended to be used as a callback for the `inferless` command.
    The `inferless` command is not yet implemented, but this function is included here as a placeholder for future development.
    """


@app.command("mode", help="Change mode", hidden=True)
def run_mode(
    mode: str = typer.Argument(
        ..., help="The mode to run the application in, either 'DEV' or 'PROD'."
    )
):
    """Runs the application in the specified mode."""
    try:
        mode = mode.upper()  # Ensure mode is uppercase
        if mode not in ["DEV", "PROD"]:
            raise InferlessCLIError("[red] Mode must be 'DEV' or 'PROD'[/red]")

        if mode == "DEV":
            set_env_mode(mode)
            rich.print("[green]Running in development mode[/green]")
            # Insert your development mode code here
        else:
            set_env_mode(mode)
            rich.print("[green]Running in production mode[/green]")
            # Insert your production mode code here
    except InferlessCLIError as e:
        rich.print(e)
        raise typer.Exit()
    except Exception:
        raise typer.Abort(1)


app.add_typer(
    token_prompt.app,
    name="token",
    help="Manage Inferless tokens",
    callback=min_version_required,
)
app.add_typer(
    workspace_prompt.app,
    name="workspace",
    help="Manage Inferless workspaces (can be used to switch between workspaces)",
    callback=callback_with_auth_validation,
)
app.add_typer(
    model_prompt.app,
    name="model",
    help="Manage Inferless models (list , delete , activate , deactivate , rebuild the models)",
    callback=callback_with_auth_validation,
)
app.add_typer(
    secret_prompt.app,
    name="secret",
    help="Manage Inferless secrets (list secrets)",
    callback=callback_with_auth_validation,
)

app.add_typer(
    volume_prompt.app,
    name="volume",
    help="Manage Inferless volumes (can be used to list volumes and create new volumes)",
    callback=callback_with_auth_validation,
)

app.add_typer(
    runtime_prompt.app,
    name="runtime",
    help="Manage Inferless runtimes (can be used to list runtimes and upload new runtimes)",
    callback=callback_with_auth_validation,
)

app.add_typer(
    init_default.init_app,
    name="init",
    help="Initialize a new Inferless model",
    # callback=callback_with_auth_validation,
)

app.add_typer(
    integration_prompt.app,
    name="integration",
    help="Manage Inferless integrations",
    callback=callback_with_auth_validation,
)


@app.command(
    "export",
    help="Export the runtime configuration of another provider to Inferless runtime config",
)
def export_def(
    source_file: Optional[str] = typer.Option(
        "cog.yaml",
        "--runtime",
        "-r",
        help="The runtime configuration file of another provider",
    ),
    destination_file: Optional[str] = typer.Option(
        DEFAULT_RUNTIME_FILE_NAME,
        "--destination",
        "-d",
        help="The destination file for the Inferless runtime configuration",
    ),
    from_provider: Optional[str] = typer.Option(
        "replicate",
        "--from",
        "-f",
        help="The provider from which to export the runtime configuration",
    ),
):
    callback_with_auth_validation()
    export_runtime_configuration(source_file, destination_file, from_provider)


@app.command("log", help="Inferless models logs (view build logs or call logs)")
def log_def(
    model_id: str = typer.Argument(None, help="Model id or model import id"),
    import_logs: bool = typer.Option(False, "--import-logs", "-i", help="Import logs"),
    logs_type: str = typer.Option(
        "BUILD", "--type", "-t", help="Logs type [BUILD, CALL]]"
    ),
):
    callback_with_auth_validation()
    log_prompt(model_id, logs_type, import_logs)



@app.command(
    "deploy",
    help="Deploy a model to Inferless",
    no_args_is_help=True,
)
def deploy_def(
    gpu: str = typer.Option(
        ..., "--gpu", help="Denotes the machine type (A10/A100/T4)."
    ),
    region: str = typer.Option(
        None, "--region", help="Inferless region. Defaults to Inferless default region."
    ),
    beta: bool = typer.Option(
        False, "--beta", help="Deploys the model with v2 endpoints."
    ),
    fractional: bool = typer.Option(
        False, "--fractional", help="Use fractional machine type (default: dedicated)."
    ),
    runtime: str = typer.Option(
        None,
        "--runtime",
        help="Runtime name or file location. if not provided default Inferless runtime will be used.",
    ),
    volume: str = typer.Option(None, "--volume", help="Volume name."),
    volume_mount_path: str = typer.Option(None, "--volume-mount-path", help="Custom volume mount path."),
    env: List[str] = typer.Option(
        [], "--env", help="Key-value pairs for model environment variables."
    ),
    inference_timeout: int = typer.Option(
        180, "--inference-timeout", help="Inference timeout in seconds."
    ),
    scale_down_timeout: int = typer.Option(
        600, "--scale-down-timeout", help="Scale down timeout in seconds."
    ),
    container_concurrency: int = typer.Option(
        1, "--container-concurrency", help="Container concurrency level."
    ),
    secret: List[str] = typer.Option(
        [], "--secret", help="Secret names to attach to the deployment."
    ),
    runtime_version: str = typer.Option(
        None, "--runtimeversion", help="Runtime version (default: latest version of runtime)."
    ),
    max_replica: int = typer.Option(
        1, "--max-replica", help="Maximum number of replicas."
    ),
    min_replica: int = typer.Option(
        0, "--min-replica", help="Minimum number of replicas."
    ),
    config_file_name: str = typer.Option(
        DEFAULT_YAML_FILE_NAME,
        "--config",
        "-c",
        help="Inferless config file path to override from inferless.yaml",
    ),
):
    callback_with_auth_validation()
    is_local_runtime = False
    gpu = gpu.upper()
    if gpu not in ["A10", "A100", "T4"]:
            raise typer.BadParameter("GPU must be one of A10, A100, or T4.")
    
    if not os.path.isfile(config_file_name):
        raise typer.BadParameter("Config file not found.")
    
    # Runtime validation
    if runtime is not None:
        if os.path.isfile(runtime):
            is_local_runtime = True
    else:
        typer.echo("No runtime specified; using default Inferless runtime.")

    # Inference timeout validation
    if not (1 <= inference_timeout <= 7200):
        raise typer.BadParameter(
            "Inference timeout must be between 1 and 7200 seconds."
        )

    # validate max and min replicas also check if its number
    if max_replica < min_replica:
        raise typer.BadParameter(
            "Max replicas must be greater than or equal to min replicas."
        )
    if not isinstance(max_replica, int) or not isinstance(min_replica, int):
        raise typer.BadParameter("Max replicas and min replicas must be integers.")

    deploy_prompt(
        gpu=gpu,
        region=region,
        beta=beta,
        fractional=fractional,
        runtime=runtime,
        volume=volume,
        env=env,
        inference_timeout=inference_timeout,
        scale_down_timeout=scale_down_timeout,
        container_concurrency=container_concurrency,
        secrets=secret,
        runtime_version=runtime_version,
        max_replica=max_replica,
        min_replica=min_replica,
        config_file_name=config_file_name,
        redeploy=False,
        is_local_runtime=is_local_runtime,
        volume_mount_path=volume_mount_path
    )


@app.command("run", help="Run a model locally", no_args_is_help=True)
def run_local_def(
    runtime_path: str = typer.Option(
        None,
        "--runtime",
        "-r",
        help="custom runtime name or file location. if not provided default Inferless runtime will be used.",
    ),
    runtime_type: str = typer.Option(
        None,
        "--type",
        "-t",
        help="Type of runtime to run [inferless, replicate]",
    ),
    name: str = typer.Option(
        "inferless-model",
        "--name",
        "-n",
        help="Name of the model to deploy on inferless",
    ),
    env_file: Optional[str] = typer.Option(
        None,
        "--env-file",
        "-f",
        help="Path to an env file containing environment variables (one per line in KEY=VALUE format)",
    ),
    env_vars: List[str] = typer.Option(
        [],
        "--env",
        "-e",
        help="Environment variables to set for the runtime (e.g. 'KEY=VALUE'). If the env variable contains special chars please escape them.",
    ),
    docker_base_url: Optional[str] = typer.Option(
        None,
        "--docker-base-url",
        "-u",
        help="Docker base url. Defaults to system default, feteched from env",
    ),
    volume: str = typer.Option(None, "--volume", help="Volume name."),
    framework: str = typer.Option(
        "PYTORCH",
        "--framework",
        "-f",
        help="Framework type. (PYTORCH, ONNX, TENSORFLOW)",
    ),
    input_schema_path: str = typer.Option(
        "input_schema.py",
        "--input-schema",
        "-i",
        help="Input schema path. (Default: input_schema.json)",
    ),
    input_json_path: str = typer.Option(
        None,
        "--input",
        "-i",
        help="Input json path",
    ),
    output_json_path: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output json path",
    ),
    runtime_version: str = typer.Option(
        None, "--runtimeversion", help="Runtime version (default: latest)."
    ),
):
    callback_with_auth_validation()
    is_local_runtime = False
    if runtime_path is not None:
        if os.path.isfile(runtime_path):
            is_local_runtime = True
    else:
        typer.echo("No runtime specified; using default Inferless runtime.")

    if runtime_type is not None and runtime_type not in PROVIDER_CHOICES:
        rich.print(
            f"Error: '--type' must be one of {PROVIDER_CHOICES}, got '{runtime_type}' instead."
        )
        raise typer.Exit()

    if runtime_type is None and runtime_path is not None:
        rich.print("[yellow]Type not given. Assuming type as Inferless.[/yellow]")
        runtime_type = "inferless"

    env_dict = {}
    if env_file:
        with open(env_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                env_dict[key] = value

    for env_var in env_vars:
        key, value = env_var.split("=", 1)
        env_dict[key] = value

    run_prompt(
        runtime_path, 
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
    )


@app.command("remote-run", help="Remotely run code on inferless")
def remote_run(
    file_path: str = typer.Argument(
        default=None,
        help="The path to the file to run on Inferless",
    ),
    config_file_path: str = typer.Option(
        None,
        "--config",
        "-c",
        help="The path to the Inferless config file",
    ),
    exclude: str = typer.Option(
        None,
        "--exclude",
        "-e",
        help="The path to the file to exclude from the run, use .gitignore format. If not provided, .gitignore "
        "will be used if present in the directory.",
    ),
):
    callback_with_auth_validation()
    try:
        if file_path is None:
            raise InferlessCLIError(
                "[red]Error: Please provide a file path to run on Inferless[/red]"
            )
        if config_file_path is None:
            raise InferlessCLIError(
                "[red]Error: Please provide a config file path to run on Inferless[/red]"
            )

        remote_run_prompt(file_path, config_file_path, exclude)
    except InferlessCLIError as e:
        rich.print(e)
        raise typer.Exit()
    except Exception:
        rich.print("[red]Something went wrong[/red]")
        raise typer.Abort(1)


@app.command("login", help="Login to Inferless")
def login_def():
    min_version_required()
    login_prompt()

@app.command("scaffold", help="Scaffold a demo Inferless project")
def scaffold_def(demo: bool = typer.Option(..., "--demo", "-d", help="Demo name")):
    callback_with_auth_validation()
    scaffold_prompt.scaffold_prompt(demo)



app.add_typer(
    region_prompt.app,
    name="region",
    help="Manage Inferless regions",
    callback=callback_with_auth_validation,
)

if __name__ == "__main__":
    app()
