import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
import typer
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from inferless_cli.commands.init.helpers import (
    get_region_id,
    get_region_region_id,
    get_region_types,
)
from inferless_cli.commands.init.validators import validate_region_types
from inferless_cli.utils.constants import (
    DEFAULT_YAML_FILE_NAME,
    SPINNER_DESCRIPTION,
)
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import (
    key_bindings,
    decrypt_tokens,
    is_inferless_yaml_present,
    log_exception,
)

from prompt_toolkit.validation import Validator
from inferless_cli.utils.services import (
    delete_volume_files_url,
    create_presigned_download_url,
    create_presigned_upload_url,
    delete_volume_temp_dir,
    get_file_download,
    get_volume_by_name,
    get_volume_info,
    get_volume_info_with_id,
    get_volumes_list,
    create_volume,
    get_workspace_regions,
    sync_s3_to_nfs,
    sync_s3_to_s3,
    get_volume_files,
    upload_file,
)
from pathlib import Path

app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = SPINNER_DESCRIPTION
no_volumes = "[red]No volumes found in your account[/red]"


@app.command(
    "list",
    help="List all existing volumes",
)
def list_volumes():
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            volumes = get_volumes_list(workspace_id=workspace_id)
            progress.remove_task(task_id)

        if len(volumes) == 0:
            raise InferlessCLIError(no_volumes)

        regions = get_regions_values()

        table = Table(
            title="Volume List",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column(
            "Name",
        )
        table.add_column(
            "Region",
        )
        table.add_column("Infer path")
        for volume in volumes:
            volume_name = volume["name"]
            # path = volume["path"]
            region = volume["region"]
            mapped_region = get_regions(region, regions)
            table.add_row(
                volume_name,
                mapped_region,
                f"infer://volumes/{mapped_region}/{volume_name}",
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


@app.command(
    "create",
    help="Create a new volume",
)
def create(
    name: str = typer.Option(
        None, "--name", "-n", help="Assign a name to the new volume."
    ),
):
    try:
        if name is None:
            name = prompt(
                "Enter the name for volume: ",
            )

        res = None
        region = get_regions_prompt()
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            _, _, _, workspace_id, workspace_name = decrypt_tokens()
            task_id = progress.add_task(
                description=f"Creating volume in [blue]{workspace_name}[/blue] workspace",
                total=None,
            )

            regions = get_regions_values()

            res = create_volume(
                workspace_id=workspace_id,
                name=name,
                region=get_region_id(region, regions),
            )
            progress.remove_task(task_id)

        if "id" in res and "name" in res:
            rich.print(
                f"[green]Volume [bold]{res['name']}[/bold] created successfully[/green]"
            )
            # is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)

            # if is_yaml_present:
            #     is_update = typer.confirm(
            #         f"Found {DEFAULT_YAML_FILE_NAME} file. Do you want to update it? ",
            #         default=True,
            #     )
            #     if is_update:
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

def extract_volume_name(path):
    try:
        # Find the part of the path after 'volumes/'
        start_index = path.index("volumes/") + len("volumes/")
        # Extract everything after 'volumes/' and split by '/'
        dynamic_region_and_volume = path[start_index:].split("/")
        # Return the second part (volume name)
        return dynamic_region_and_volume[1]
    except (IndexError, ValueError):
        return None


def extract_path_after_volume(path):
    try:
        # Find the position after 'infer://volumes/'
        start_index = path.index("infer://volumes/") + len("infer://volumes/")
        # Extract everything after 'infer://volumes/'
        relative_path = path[start_index:]
        # Split the path by '/' and check if there are more than two segments
        parts = relative_path.split("/", 2)
        if len(parts) > 2:
            return parts[2]  # Return everything after the region and volume name
        return ""  # No extra path after the volume name
    except (IndexError, ValueError):
        return None

@app.command(
    "ls",
    help="List files and directories within a volume",
)
def list_files(
    path: str = typer.Argument(
        ...,
        help="Specify the infer path to the directory",
    ),
    directory_only: bool = typer.Option(
        False, "--directory", "-d", help="List only directories."
    ),
    files_only: bool = typer.Option(False, "--files", "-f", help="List only files."),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Recursively list contents of directories."
    ),
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()
        volume_name = extract_volume_name(path)
        old_path = path
        path = extract_path_after_volume(path)

        res = get_volume_by_name(workspace_id=workspace_id, volume_name=volume_name)
        id = res.get("volume_id")
        if res is None:
            raise InferlessCLIError(
                "\n[red]Error: Volume not found[/red]\n"
            )

        volume_data = find_volume_by_id(workspace_id, id)
        volume_name = volume_data["name"]

        table = Table(show_header=False, box=None)
        list_directory(
            path or "",
            table,
            volume_name,
            volume_data,
            directory_only,
            files_only,
            recursive,
        )
        rich.print(
            f"\n [green][bold]Volume: {volume_name}[/bold][/green] (Path: {path or '/'}) \n"
        )
        rich.print(table)
        rich.print("\n")
        if not recursive:
            rich.print(
                f"You can run `[blue]inferless volume ls {old_path}/<DIR_NAME>[/blue]` for viewing files inside dir\n"
            )
            rich.print(
                "[green]Tip: Use the --recursive (-r) flag to list contents of directories recursively.[/green]\n\n"
            )
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


def list_directory(
    path, table, volume_name, volume_data, directory_only, files_only, recursive
):
    _, _, _, workspace_id, _ = decrypt_tokens()
    payload = {
        "volume_name": volume_name,
        "workspace_id": workspace_id,
        "volume_id": volume_data["id"],
    }

    if path != "":
        payload["file_path"] = path

    response = {}
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task("fetching files and directories")
        response = get_volume_files(payload)

    progress.remove_task(task_id)
    if not response and not response["details"]:
        table.add_row(f"[yellow]No files or directories found at '{path}'[/yellow]")

    for item in response["details"]:
        if directory_only and item["type"] != "directory":
            continue
        if files_only and item["type"] != "file":
            continue

        path_new = path + "/" if path else ""

        table.add_row(
            f"[blue]{path_new}{item['name']}[/blue]",
            item["type"],
            str(item["file_size"]),
            item["created_at"],
        )
        if recursive and item["type"] == "directory":
            list_directory(
                f"{path_new}{item['name']}",
                table,
                volume_name,
                volume_data,
                directory_only,
                files_only,
                recursive,
            )


# @app.command(
#     "select", help="Select a volume for updates in the Inferless configuration."
# )
# def select(
#     path: str = typer.Option(
#         None,
#         "--path",
#         "-p",
#         help="Path to the Inferless configuration file (typically inferless.yaml)",
#     ),
#     id: str = typer.Option(None, "--id", "-i", help="The ID of the volume to select."),
# ):
#     try:
#         _, _, _, workspace_id, _ = decrypt_tokens()
#         if id is None:
#             raise InferlessCLIError(
#                 "\n[red]--id is required. Please use `[blue]inferless volume list[/blue]` to get the id[/red]\n"
#             )

#         if path is None:
#             path = prompt(
#                 "Enter path of inferless config file : ",
#                 default=f"{DEFAULT_YAML_FILE_NAME}",
#             )

#         volume = find_volume_by_id(workspace_id, id)

#         rich.print("Updating yaml file")
#         update_config_file(path, volume)

#     except ServerError as error:
#         rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
#         log_exception(error)
#         raise typer.Exit()
#     except InferlessCLIError as error:
#         rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
#         log_exception(error)
#         raise typer.Exit()
#     except Exception as error:
#         log_exception(error)
#         rich.print("\n[red]Something went wrong[/red]")
#         raise typer.Abort(1)


@app.command("cp", help="Add a file or directory to a volume.")
def copy(
    source: str = typer.Option(
        None,
        "--source",
        "-s",
        help="Specify the source path (either a local directory/file path or an Inferless path)",
    ),
    destination: str = typer.Option(
        None,
        "--destination",
        "-d",
        help="Specify the destination path (either a local directory/file path or an Inferless path)",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively copy the contents of a directory to the destination.",
    ),
):
    try:
        _, _, _, workspace_id, _ = decrypt_tokens()

        cp_type, volume_name, volume_region = validate_and_check_cp_action(
            source, destination
        )
        regions = get_regions_values()
        volume_data = find_volume_by_name(
            workspace_id, volume_name, get_region_id(volume_region, regions)
        )
        if volume_data is None:
            raise InferlessCLIError(
                f"[red]Error: No volume found with {volume_name}.[/red]"
            )
        if cp_type == "UPLOAD":
            if os.path.isdir(source) and not recursive:
                raise InferlessCLIError(
                    "[red]Please provide `-r` or `--recursive` flag to copy the directroy [/red]"
                )
            copy_files_v2(source, destination, volume_data, workspace_id)

        if cp_type == "DOWNLOAD":
            download_files(source, destination, volume_data, workspace_id)

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


def validate_and_check_cp_action(source, destination):
    if not source:
        raise InferlessCLIError("\n[red]--source is a required param")

    if not destination:
        raise InferlessCLIError("\n[red]--destination is a required param")

    if source and not source.startswith("infer://"):
        source = make_absolute(source)
    elif destination and not destination.startswith("infer://"):
        destination = make_absolute(destination)

    volume_name = ""
    volume_region = ""
    cp_type = None
    if source.startswith("infer://"):
        volume_name, volume_region = extract_volume_info(source)
        cp_type = "DOWNLOAD"
        return cp_type, volume_name, volume_region

    if destination.startswith("infer://"):
        volume_name, volume_region = extract_volume_info(destination)
        cp_type = "UPLOAD"
        return cp_type, volume_name, volume_region

    raise InferlessCLIError(
        "\n[red]--source or --destination should start with infer://"
    )


def copy_files_v2(source, destination, volume_data, workspace_id):
    s3_path = destination.split("infer://")[1]
    vol_id = volume_data["id"]
    vol_name = volume_data["name"]
    region = volume_data["region"] if volume_data["region"] else "AZURE"

    s3_path = get_s3_path_from_infer_path(destination, region, workspace_id, vol_id)
    s3_path.replace("volumes/", "volumes_temp/")
    try:
        base_temp_s3_path = generate_s3_base_path(
            "volumes_temp",
            region,
            workspace_id,
            vol_id,
            vol_name,
        )
        payload = {"s3_path": base_temp_s3_path, "volume_id": vol_id}
        delete_volume_temp_dir(payload)
    except Exception:
        """If delete fails please proceed"""

    try:
        volume_data["volume_id"] = volume_data["id"]
        if os.path.isfile(source):
            process_file(source, s3_path, source)
        elif os.path.isdir(source):
            for root, _, files in os.walk(source):
                for file in files:
                    file_path = Path(root) / file
                    unix_file_path = file_path.as_posix()
                    process_file(unix_file_path, s3_path, source)
                    # if size if more than 1GB then post_copy function to sync the s3-s3 and s3-nfs now
                    if os.path.getsize(unix_file_path) > 1024**3:
                        post_copy(s3_path, region, workspace_id, vol_id, vol_name)
        post_copy(s3_path, region, workspace_id, vol_id, vol_name)
    except Exception as e:
        log_exception(e)
        raise InferlessCLIError("\n[red]Upload unsuccessful[/red]\n\n")


def post_copy(s3_path, region, workspace_id, vol_id, vol_name):
    rich.print("verifiying upload...")
    s3_path_original = s3_path.replace("volumes_temp/", "volumes/")
    payload = {"source": s3_path, "destination": s3_path_original}
    sync_s3_to_s3(payload)
    base_s3_path = generate_s3_base_path(
        "volumes",
        region,
        workspace_id,
        vol_id,
        vol_name,
    )
    sync_s3_to_nfs({"s3_path": base_s3_path, "volume_id": vol_id})
    rich.print("\n[green]Upload successful[/green]\n\n")


def copy_files(source, destination, volume_data, workspace_id):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        s3_path = destination.split("infer://")[1]
        vol_id = volume_data["id"]
        vol_name = volume_data["name"]
        region = volume_data["region"] if volume_data["region"] else "AZURE"

        s3_path = get_s3_path_from_infer_path(destination, region, workspace_id, vol_id)
        s3_path.replace("volumes/", "volumes_temp/")
        try:
            base_temp_s3_path = generate_s3_base_path(
                "volumes_temp",
                region,
                workspace_id,
                vol_id,
                vol_name,
            )
            payload = {"s3_path": base_temp_s3_path, "volume_id": vol_id}
            delete_volume_temp_dir(payload)
        except Exception:
            """If delete fails please proceed"""

        volume_data["volume_id"] = volume_data["id"]
        futures = []
        if os.path.isfile(source):
            futures.append(
                executor.submit(
                    process_file,
                    source,
                    s3_path,
                    source,
                )
            )

        elif os.path.isdir(source):
            futures += process_directory(
                executor,
                source,
                s3_path,
                source,
            )

        results = [future.result() for future in futures]
        if all(results):
            rich.print("verifiying upload...")
            s3_path_original = s3_path.replace("volumes_temp/", "volumes/")
            payload = {"source": s3_path, "destination": s3_path_original}
            sync_s3_to_s3(payload)
            base_s3_path = generate_s3_base_path(
                "volumes",
                region,
                workspace_id,
                vol_id,
                vol_name,
            )
            sync_s3_to_nfs({"s3_path": base_s3_path, "volume_id": vol_id})
            rich.print("\n[green]Upload successful[/green]\n\n")
        else:
            raise InferlessCLIError("\n[red]Upload unsuccessful[/red]\n\n")


def generate_s3_base_path(volume_type, region, workspace_id, vol_id, vol_name):
    return f"{volume_type}/{region}/{workspace_id}/{vol_id}/{vol_name}"


def download_files(source, destination, volume_data, workspace_id):
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description="Downloading..", total=None)

        vol_id = volume_data["id"]
        region = volume_data["region"]
        s3_path = s3_path = get_s3_path_from_infer_path(
            source, region, workspace_id, vol_id
        )
        payload = {
            "url_for": "VOLUME_FOLDER_DOWNLOAD",
            "file_name": f"{s3_path}",
        }
        res = create_presigned_download_url(payload)

        download_files_in_parallel(res, destination)
        progress.remove_task(task_id)
    rich.print(f"[green]downloaded successfully and saved at '{destination}'[/green]")


@app.command(
    "rm", help="Specify the Inferless path to the file or directory you want to delete."
)
def delete(
    path: str = typer.Option(
        None, "--path", "-p", help="Infer Path to the file/dir your want to delete"
    ),
):
    try:
        if not path:
            raise InferlessCLIError("\n[red]--path is a required param\n")

        _, _, _, workspace_id, _ = decrypt_tokens()
        volume_name, volume_region = extract_volume_info(path)
        if id is None:
            raise InferlessCLIError(
                "\n[red]--id is required. Please use `[blue]inferless volume list[/blue]` to get the id[/red]\n"
            )
        regions = get_regions_values()

        volume_data = find_volume_by_name(
            workspace_id, volume_name, get_region_id(volume_region, regions)
        )
        if volume_data is None:
            raise InferlessCLIError(
                f"[red]Error: No volume found with name {volume_name}.[/red]"
            )

        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description="deleting...", total=None)
            region = volume_data["region"] if "region" in volume_data else "AZURE"
            vol_id = volume_data["id"]
            s3_path = get_s3_path_from_infer_path(path, region, workspace_id, vol_id)
            payload = {"s3_path": s3_path, "volume_id": vol_id}

            res = delete_volume_files_url(payload)

            if res == "Deleted Successfully":
                rich.print("[green]File successfully deleted.[/green]")
            else:
                rich.print("[red]Failed to delete file.[/red]")

            progress.remove_task(task_id)
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


def get_s3_path_from_infer_path(path, region, workspace_id, vol_id):
    s3_path = path.split("infer://")[1]
    regions = get_regions_values()
    mapped_region = get_regions(region, regions)
    s3_path = s3_path.replace(
        f"volumes/{mapped_region}/",
        f"volumes/{region}/{workspace_id}/{vol_id}/",
    )
    return s3_path


def find_volume_by_name(workspace_id, volume_name, volume_region):
    volume = get_volume_info(workspace_id, volume_name, volume_region)
    return volume


def find_volume_by_id(workspace_id, volume_id):
    volume = get_volume_info_with_id(workspace_id, volume_id)
    if volume is None:
        raise InferlessCLIError(f"[red]Error: No volume found with id {id}.[/red]")
    return volume


def process_file(path: str, s3_path, root_path):
    try:
        unix_file_path = Path(path).as_posix()
        unix_root_path = Path(root_path).as_posix()

        if unix_root_path == unix_file_path:
            save_path = s3_path
        else:
            relative_path = unix_file_path[len(unix_root_path) :].lstrip("/")
            save_path = f"{s3_path}/{relative_path}"

        if save_path.startswith("/"):
            save_path = save_path[1:]
        file_size = os.path.getsize(path)

        if file_size > 2 * 1024**3:  # File size is more than 5GB
            with open(path, "rb") as file:
                rich.print(f"Uploading {path}")
                save_path = save_path.replace("volumes_temp", "volumes")

                url = upload_file(file, save_path, file_size, upload_type="ANY")

                if url:
                    return True
                return False
        else:
            payload = {
                "url_for": "VOLUME_FILE_UPLOAD",
                "file_name": save_path,
            }

            res = create_presigned_upload_url(payload, path)

            if "status" in res and res["status"] == "success":
                return True
            return False
    except Exception as e:
        log_exception(e)
        return True


def process_directory(executor, dir_path: str, s3_path, root_path):
    futures = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = Path(root) / file
            unix_file_path = file_path.as_posix()
            future = executor.submit(process_file, unix_file_path, s3_path, root_path)
            futures.append(future)

    return futures


def extract_volume_info(input_string):
    # Splitting the URL by '/'
    parts = input_string.split("/")

    # Extracting workspace_id, volume_id, and volume_name
    # The indices are based on the structure of your URL
    volume_region = parts[3] if len(parts) > 3 else None
    volume_name = parts[4] if len(parts) > 4 else None

    return volume_name, volume_region


def make_request(url, destination):
    response = get_file_download(url)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "wb") as file:
            file.write(response.content)
    else:
        rich.print(f"Failed to download {url}")


def download_files_in_parallel(file_dict, dest):
    # Using ThreadPoolExecutor to download files in parallel
    with ThreadPoolExecutor() as executor:
        # Creating a list of futures
        futures = []
        for local_path, url in file_dict.items():
            destination = os.path.join(dest, local_path)
            rich.print(f"Downloading {local_path} to {destination}")
            # Submitting the download task
            futures.append(executor.submit(make_request, url, destination))

        # Waiting for all futures to complete
        for future in futures:
            future.result()


def make_absolute(path):
    # Check if the path is either '.' (current directory) or a relative path
    if path == "." or not os.path.isabs(path):
        # Use os.path.abspath to convert to an absolute path
        return os.path.abspath(path)

    # If the path is already absolute, return it as is
    return path
