import sys
from prompt_toolkit.validation import Validator
import typer
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.commands.init.helpers import (
    get_region_id,
    get_region_region_id,
    get_region_types,
)
from inferless_cli.commands.init.validators import validate_region_types


from inferless_cli.utils.constants import (
    DEFAULT_INFERLESS_RUNTIME_YAML_FILE,
    DEFAULT_RUNTIME_FILE_NAME,
    RUNTIME_DOCS_URL,
    SPINNER_DESCRIPTION,
)
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import (
    create_yaml,
    decrypt_tokens,
    key_bindings,
    log_exception,
    yaml,
)
import os

from inferless_cli.utils.services import (
    create_presigned_url,
    get_runtime_by_name,
    get_templates_list,
    get_workspace_regions,
    list_runtime_versions,
)
import uuid
import subprocess


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = SPINNER_DESCRIPTION
no_runtimes = "[red]No runtimes found in your account[/red]"


@app.command(
    "list",
    help="List all runtimes.",
)
def list_runtimes():
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            runtimes = get_templates_list(workspace_id)
            progress.remove_task(task_id)

        if len(runtimes) == 0:
            raise InferlessCLIError(no_runtimes)

        table = Table(
            title="Runtime List",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column("ID", style="yellow")
        table.add_column(
            "Name",
        )
        table.add_column(
            "Region",
        )
        table.add_column("Status")
        regions = get_regions_values()
        for runtime in runtimes:
            table.add_row(
                runtime["id"],
                runtime["name"],
                get_regions(runtime["region"], regions),
                runtime["status"],
            )

        console = Console()
        console.print(table)
        console.print("\n")
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


def get_regions_values():
    _, _, _, workspace_id, _ = decrypt_tokens()

    regions = get_workspace_regions({"workspace_id": workspace_id})

    if regions:
        return regions

    raise InferlessCLIError("Regions not found")


def get_regions(region, regions):

    region_value = get_region_region_id(region, regions)

    if region_value:
        return region_value

    raise InferlessCLIError("Region not found")


@app.command("create", help="Create a runtime.")
def create(
    path: str = typer.Option(None, "--path", "-p", help="Path to the runtime"),
    name: str = typer.Option(None, "--name", "-n", help="Name of the runtime"),
):
    try:
        uid, file_name, payload, region, name, runtime_id, workspace_id, path = (
            validate_runtime_command_inputs(path, False, None, name)
        )
        res = upload_runtime_to_cloud(
            payload,
            uid,
            name,
            region,
            file_name,
            path,
            workspace_id,
            False,
            runtime_id,
        )
        if "id" in res and "name" in res:
            rich.print(f"[green]Runtime {res['name']} uploaded successfully[/green]")
            # is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)

            # if is_yaml_present:
            #     is_update = typer.confirm(
            #         f"Found {DEFAULT_YAML_FILE_NAME} file. Do you want to update it? ",
            #         default=True,
            #     )
            #     if is_update is True:
            #         rich.print("Updating yaml file")
            #         update_config_file(DEFAULT_YAML_FILE_NAME, res)
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


@app.command("patch", help="Update the runtime with the config file.")
def patch(
    path: str = typer.Option(None, "--path", "-p", help="Path to the runtime"),
    runtime_name: str = typer.Option(None, "--name", "-i", help="ID of the runtime"),
):
    try:
        uid, file_name, payload, region, name, runtime_id, workspace_id, path = (
            validate_runtime_command_inputs(path, True, runtime_name, "")
        )
        res = upload_runtime_to_cloud(
            payload,
            uid,
            name,
            region,
            file_name,
            path,
            workspace_id,
            patch,
            runtime_id,
        )
        if "id" in res and "name" in res:
            rich.print(f"[green]Runtime {res['name']} uploaded successfully[/green]")
            # is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)

            # if is_yaml_present:
            #     is_update = typer.confirm(
            #         f"Found {DEFAULT_YAML_FILE_NAME} file. Do you want to update it? ",
            #         default=True,
            #     )
            #     if is_update is True:
            #         rich.print("Updating yaml file")
            #         update_config_file(DEFAULT_YAML_FILE_NAME, res)
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


def validate_runtime_command_inputs(
    path,
    patch,
    runtime_name,
    name,
):
    _, _, _, workspace_id, _ = decrypt_tokens()
    runtime_id = None
    if runtime_name:
        res = get_runtime_by_name(workspace_id=workspace_id, runtime_name=runtime_name)
        runtime_id = res["id"]

    if path is None:
        path = prompt(
            "Enter path of runtime config yaml file : ",
            default=f"{DEFAULT_RUNTIME_FILE_NAME}",
        )
    if not patch and runtime_id:
        raise InferlessCLIError("Please use --patch flag to patch runtime")

    if patch:
        if not runtime_id:
            list_runtimes()
            runtime_id = prompt(
                "Enter the runtime id: ",
            )
    else:
        if name is None:
            name = prompt(
                "Enter the name for runtime: ",
            )
        region = get_regions_prompt()

    if runtime_id:
        runtime_id = runtime_id.strip()
        runtimes = get_templates_list(workspace_id)
        runtime = get_runtime_details(runtimes, runtime_id)
        region = runtime["region"]
        name = runtime["name"]

    uid = uuid.uuid4()
    file_name = os.path.basename(path)
    payload = {
        "url_for": "YAML_FILE_UPLOAD",
        "file_name": f'{uid}/{file_name.replace(" ", "")}',
    }
    return uid, file_name, payload, region, name, runtime_id, workspace_id, path


def get_runtime_details(runtimes, runtime_id):
    for runtime in runtimes:
        if runtime["id"] == runtime_id:
            return runtime

    raise InferlessCLIError("Runtime not found")


def upload_runtime_to_cloud(
    payload,
    uid,
    name,
    region,
    file_name,
    path,
    workspace_id,
    patch,
    runtime_id,
):
    # with Progress(
    #     SpinnerColumn(),
    #     TextColumn(desc),
    #     transient=True,
    # ) as progress:
    # if runtime_id is not None:
    #     task_id = progress.add_task(
    #         description="Uploading runtime config as a new version", total=None
    #     )
    # else:
    #     task_id = progress.add_task(
    #         description="Uploading runtime config", total=None
    #     )
    regions = get_regions_values()

    res = create_presigned_url(
        payload,
        uid,
        name,
        get_region_id(region, regions),
        file_name.replace(" ", ""),
        path,
        workspace_id,
        patch,
        runtime_id,
    )

        # progress.remove_task(task_id)

    return res


# @app.command("select", help="use to update the runtime in inferless config file")
# def select(
#     path: str = typer.Option(
#         None, "--path", "-p", help="Path to the inferless config file (inferless.yaml)"
#     ),
#     id: str = typer.Option(None, "--id", "-i", help="runtime id"),
# ):
#     _, _, _, workspace_id, _ = decrypt_tokens()
#     if id is None:
#         rich.print(
#             "\n[red]--id is required. Please use `[blue]inferless runtime list[/blue]` to get the id[/red]\n"
#         )
#         raise typer.Exit(1)

#     with Progress(
#         SpinnerColumn(),
#         TextColumn(desc),
#         transient=True,
#     ) as progress:
#         task_id = progress.add_task(description=processing, total=None)
#         runtimes = get_templates_list(workspace_id)
#         progress.remove_task(task_id)
#         runtime = None
#         for rt in runtimes:
#             if rt["id"] == id:
#                 runtime = rt
#                 break
#         if runtime is None:
#             raise InferlessCLIError("Runtime not found")

#     if path is None:
#         path = prompt(
#             "Enter path of inferless config file : ",
#             default=f"{DEFAULT_YAML_FILE_NAME}",
#         )

#     rich.print("Updating yaml file")
#     update_config_file(path, runtime)


@app.command("version-list", help="use to list the runtime versions")
def runtime_version_list(
    runtime_name: str = typer.Option(None, "--name", "-n", help="runtime name"),
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        id = None
        if runtime_name:
            res = get_runtime_by_name(workspace_id=workspace_id, runtime_name=runtime_name)
            id = res["id"]
        
        if id is None:
            raise InferlessCLIError("Runtime not found")

        res = list_runtime_versions({"template_id": id})
        table = Table(
            title="Selected Runtime Versions",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column("version", style="yellow")
        table.add_column(
            "Version Number",
        )
        table.add_column("Status")

        if len(res) == 0:
            raise InferlessCLIError("No versions found")

        for version in res:
            table.add_row(
                "version-" + str(version["version_no"]),
                str(version["version_no"]),
                version["status"],
            )

        console = Console()
        console.print("\n", table, "\n")
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\nAn error occurred: [red]{error}[/red]")
        raise typer.Abort(1)

@app.command(
    "generate", help="use to generate a new runtime from your local environment"
)
def generate():

    if sys.prefix == sys.base_prefix:
        rich.print(
            "\n[yellow]Warning:[/yellow] It's recommended to use a virtual environment (venv) to get proper package isolation.\n"
        )

    try:
        # Get installed Python packages using `pip freeze`
        result = subprocess.run(
            ["pip3", "freeze"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            rich.prino(f"Error running pip freeze: {result.stderr}")
            return

        packages = result.stdout.splitlines()
        python_packages = [pkg for pkg in packages]
        runtime_config = yaml.load(DEFAULT_INFERLESS_RUNTIME_YAML_FILE)
        # Append packages to the DEFAULT_INFERLESS_RUNTIME_YAML_FILE
        runtime_config["build"]["python_packages"] = python_packages

        # Output the updated YAML content
        create_yaml(runtime_config, DEFAULT_RUNTIME_FILE_NAME)
        rich.print(
            f"\n[bold][blue]{DEFAULT_RUNTIME_FILE_NAME}[/bold][/blue] file generated successfully! Also pre-filled `python_packages`. Feel free to modify the file"
        )
        rich.print(
            f"\nFor more information on runtime file, please refer to our docs: [link={RUNTIME_DOCS_URL}]{RUNTIME_DOCS_URL}[/link]"
        )
        rich.print(
            "\nYou can also use [bold][blue]`inferless runtime upload`[/blue][/bold] command to upload runtime\n"
        )

    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\nAn error occurred: [red]{error}[/red]")
        raise typer.Abort(1)


def get_regions_prompt():
    _, _, _, workspace_id, _ = decrypt_tokens()
    with Progress(
        SpinnerColumn(), TextColumn(SPINNER_DESCRIPTION), transient=True
    ) as progress:
        task_id = progress.add_task(description="processing...", total=None)
        regions = get_workspace_regions({"workspace_id": workspace_id})
        progress.remove_task(task_id)
    if regions:
        regions_names = [region["region_name"] for region in regions]
        region = prompt(
            f"Select Region ({', '.join(regions_names)}) : ",
            completer=get_region_types(regions_names),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_region_types(choice, regions_names)
            ),
            validate_while_typing=False,
        )

        return region

    raise InferlessCLIError("Regions not found")
