import typer
import rich
from rich.table import Table
from rich.console import Console

from inferless_cli.commands.init.constants import PROCESSING
from inferless_cli.commands.init.helpers import (
    get_machine_details,
    get_region_id,
    get_region_types,
    get_machine_types,
    handle_connected_accounts,
    generate_input_and_output_files,
    get_machine_types_servers,
    find_requirements_file,
    get_upload_methods,
    get_frameworks,
    read_pyproject_toml,
    read_requirements_txt,
)

from inferless_cli.utils.exceptions import (
    ConfigurationError,
    InferlessCLIError,
    ServerError,
)
from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    get_connected_accounts,
    get_machines,
    get_templates_list,
    get_workspace_regions,
    list_runtime_versions,
)
from inferless_cli.utils.helpers import (
    create_yaml,
    decrypt_tokens,
    is_file_present,
    log_exception,
    yaml,
    key_bindings,
    print_options,
)
from inferless_cli.commands.init.validators import (
    validate_framework,
    validate_machine_types,
    validate_machine_types_server,
    validate_region_types,
    validate_upload_method,
    validate_model_name,
    validate_url,
)
from inferless_cli.utils.constants import (
    DEFAULT_INFERLESS_RUNTIME_YAML_FILE,
    DEFAULT_INPUT_FILE_NAME,
    DEFAULT_OUTPUT_FILE_NAME,
    DEFAULT_RUNTIME_FILE_NAME,
    DEFAULT_YAML_FILE_NAME,
    FRAMEWORKS,
    GITHUB,
    GIT,
    IO_DOCS_URL,
    MACHINE_TYPE_SERVERS_DEF,
    RUNTIME_DOCS_URL,
    SPINNER_DESCRIPTION,
    UPLOAD_METHODS,
)
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from rich.progress import Progress, SpinnerColumn, TextColumn


def init_prompt():
    try:
        """Prompt the user for configuration parameters."""
        rich.print("Welcome to the Inferless Model Initialization!")

        config_file_name = config_file_prompt()
        config = InferlessConfigHandler()

        import_source = import_source_prompt(config)
        source_framework_type_prompt(config)
        model_name_prompt(config)

        if import_source == GIT:
            github_details_prompt(config)
        get_regions_prompt(config)
        server_details_prompt(config)
        machine_details_prompt(config)
        custom_runtime_details_prompt(config)
        input_output_details_prompt(config)
        save_config(config, config_file_name)
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
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
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)


def config_file_prompt():
    config_file_name = prompt(
        "Enter config file name: ",
        default=f"{DEFAULT_YAML_FILE_NAME}",
    )
    return config_file_name


def import_source_prompt(config):
    import_source = prompt(
        f"How do you want to upload the model ({', '.join(str(x) for x in UPLOAD_METHODS)}) ?  ",
        completer=get_upload_methods(),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(validate_upload_method),
        validate_while_typing=False,
    )
    config.update_config("import_source", import_source)
    return import_source


def source_framework_type_prompt(config):
    import_framework_type = prompt(
        f"Select framework ({', '.join(str(x) for x in FRAMEWORKS)}): ",
        completer=get_frameworks(),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(validate_framework),
        validate_while_typing=False,
    )
    config.update_config("source_framework_type", import_framework_type)
    return import_framework_type


def model_name_prompt(config):
    name = prompt(
        "Model name: ",
        validator=Validator.from_callable(validate_model_name),
    )
    config.update_config("name", name)
    return name


def github_details_prompt(config):
    with Progress(
        SpinnerColumn(), TextColumn(SPINNER_DESCRIPTION), transient=True
    ) as progress:
        task_id = progress.add_task(description=PROCESSING, total=None)
        accounts = get_connected_accounts(config.get_value("import_source"))
        progress.remove_task(task_id)
    if handle_connected_accounts(accounts):
        model_url = prompt(
            "github repo URL: ",
            validator=Validator.from_callable(validate_url),
        )
        config.update_config("model_url", model_url)
        config.update_config("provider", GITHUB)


def machine_details_prompt(config):

    with Progress(
        SpinnerColumn(), TextColumn(SPINNER_DESCRIPTION), transient=True
    ) as progress:
        task_id = progress.add_task(description=PROCESSING, total=None)
        machines = get_machines()
        progress.remove_task(task_id)
    region_id = get_region_id(
        config.get_value("configuration.region"), config.get_regions()
    )
    server_type = (
        "DEDICATED" if config.get_value("configuration.is_dedicated") else "SHARED"
    )
    filtered_data = [
        item
        for item in machines
        if item["region_id"] == region_id and item["machine_type"] == server_type
    ]
    flat_map = [item["name"] for item in filtered_data]
    gpu_type = prompt(
        f"GPU Type ({', '.join(str(x) for x in flat_map)}) : ",
        completer=get_machine_types(flat_map),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(
            lambda choice: validate_machine_types(choice, flat_map)
        ),
        validate_while_typing=False,
    )
    selected_machine = get_machine_details(gpu_type, region_id, server_type, machines)
    config.update_config("configuration.vcpu", str(selected_machine["cpu"]))
    config.update_config("configuration.ram", str(selected_machine["memory"]))
    config.update_config("configuration.gpu_type", gpu_type)
    return gpu_type


def server_details_prompt(config):
    print_options("Server type:", MACHINE_TYPE_SERVERS_DEF)
    machine_type_server = prompt(
        "Do you want to use DEDICATED or SHARED server? ",
        completer=get_machine_types_servers(),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(validate_machine_types_server),
        validate_while_typing=False,
    )
    is_dedicated = machine_type_server == "DEDICATED"
    config.update_config("configuration.is_dedicated", is_dedicated)
    return is_dedicated


def custom_runtime_details_prompt(config):
    if typer.confirm("Do you have custom runtime? ", default=False):
        if typer.confirm(
            "Do you want to use existing custom runtimes? ", default=False
        ):
            existing_runtime_details_prompt(config)
        else:
            file_name_full, file_type, file_name = find_requirements_file()
            handle_requirements_file(config, file_name_full, file_type, file_name)


def existing_runtime_details_prompt(config):
    _, _, _, workspace_id, _ = decrypt_tokens()

    runtimes = get_templates_list(workspace_id)
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
    region_id = get_region_id(
        config.get_value("configuration.region"), config.get_regions()
    )

    filtered_data = [item for item in runtimes if item["region"] == region_id]

    if len(filtered_data) == 0:
        raise InferlessCLIError("No runtimes found")

    for runtime in filtered_data:
        table.add_row(
            runtime["id"],
            runtime["name"],
            region_id,
            runtime["status"],
        )

    console = Console()
    console.print("\n", table, "\n")
    runtime_id = prompt(
        "Enter the runtime id you wish to use: ",
    )
    runtime_id = runtime_id.strip()
    runtime = None
    for rt in runtimes:
        if rt["id"] == runtime_id and rt["region"] == region_id:
            runtime = rt
            break
    if runtime is None:
        raise InferlessCLIError("Selected runtime not found")
    latest_version = str(runtime["current_version"])
    runtime_version_list(runtime_id)

    runtime_version = prompt(
        f"Select the version you wish to use (Latest version is {latest_version}): ",
        default=latest_version,
    )
    config.update_config("configuration.custom_runtime_id", runtime_id)
    config.update_config("configuration.custom_runtime_version", runtime_version)


def handle_requirements_file(config, file_name_full, file_type, file_name):
    if file_name_full:
        rich.print(f"\nRequirements file found: {file_name}")
        is_found_file_used = typer.confirm(
            f"Do you want to use {file_name} to load dependencies?", default=True
        )
    else:
        rich.print("\nNo requirements file automatically detected.")
        is_found_file_used = typer.confirm(
            "Do you want to load dependencies?", default=True
        )

    requirements_file_name, requirements_file_type = get_requirements_file(
        is_found_file_used, file_name_full, file_type
    )

    python_packages = load_python_packages(
        requirements_file_name, requirements_file_type
    )
    update_runtime_config(config, python_packages)


def get_requirements_file(is_found_file_used, file_name_full, file_type):
    if is_found_file_used:
        if not file_name_full:
            file_name_prompt = prompt(
                "Select your dependency management file: ",
                default="requirements.txt",
            )
            return file_name_prompt, file_name_prompt.split(".")[-1]
        return file_name_full, file_type
    return None, None


def load_python_packages(requirements_file_name, requirements_file_type):
    if requirements_file_name:
        if requirements_file_type == "txt":
            return read_requirements_txt(requirements_file_name)
        if requirements_file_type == "toml":
            return read_pyproject_toml(requirements_file_name)
    return None


def update_runtime_config(config, python_packages):
    runtime_config = yaml.load(DEFAULT_INFERLESS_RUNTIME_YAML_FILE)

    if python_packages:
        runtime_config["build"]["python_packages"] = python_packages
        config.update_config("optional.runtime_file_name", DEFAULT_RUNTIME_FILE_NAME)
        create_yaml(runtime_config, DEFAULT_RUNTIME_FILE_NAME)
        rich.print(
            f"\n[bold][blue]{DEFAULT_RUNTIME_FILE_NAME}[/bold][/blue] file generated successfully! Also pre-filled `python_packages`. Feel free to modify the file"
        )
        rich.print(
            f"For more information on runtime file, please refer to our docs: [link={RUNTIME_DOCS_URL}]{RUNTIME_DOCS_URL}[/link]"
        )
        rich.print(
            "You can also use [bold][blue]`inferless runtime upload`[/blue][/bold] command to upload runtime\n"
        )
    else:
        rich.print("No dependencies specified or loaded.")


def input_output_details_prompt(config):
    input_file_name = DEFAULT_INPUT_FILE_NAME
    output_file_name = DEFAULT_OUTPUT_FILE_NAME
    is_input_file_present = is_file_present(input_file_name)
    is_output_file_present = is_file_present(output_file_name)
    is_ioschema_file_present = is_file_present("input_schema.py")
    if config.get_value("source_framework_type") == "PYTORCH":
        config.update_config("io_schema", True)
        if not is_ioschema_file_present:
            rich.print(
                f"[bold][blue]input_schema.py[/blue][/bold] file not present. For more information on input_schema.py, please refer to our docs: [link={IO_DOCS_URL}]{IO_DOCS_URL}[/link]"
            )

    if config.get_value("source_framework_type") in ("ONNX", "TENSORFLOW") and not (
        is_input_file_present and is_output_file_present
    ):
        generate_input_and_output_files(
            {},
            {},
            input_file_name,
            output_file_name,
        )
        config.update_config("optional.input_file_name", input_file_name)
        config.update_config("optional.output_file_name", output_file_name)

        rich.print(
            f"\n[bold][blue]{input_file_name}[/blue][/bold] and [bold][blue]{output_file_name}[/blue][/bold] files generated successfully! Also pre-filled jsons. Feel free to modify the files"
        )
        rich.print(
            f"For more information on input and output json, please refer to our docs: [link={IO_DOCS_URL}]{IO_DOCS_URL}[/link]"
        )
        config.update_config("io_schema", False)


def save_config(config, config_file_name):
    config.update_config("configuration.custom_volume_name", "")
    config.update_config("configuration.custom_volume_id", "")
    config.update_config("configuration.min_replica", "0")
    config.update_config("configuration.max_replica", "1")
    config.update_config("configuration.scale_down_delay", "600")
    config.update_config("configuration.inference_time", "180")
    config.update_config("configuration.is_serverless", False)
    config.update_config("version", "1.0.0")
    config.save_config(config_file_name)


def get_regions_prompt(config):
    _, _, _, workspace_id, _ = decrypt_tokens()
    with Progress(
        SpinnerColumn(), TextColumn(SPINNER_DESCRIPTION), transient=True
    ) as progress:
        task_id = progress.add_task(description=PROCESSING, total=None)
        regions = get_workspace_regions({"workspace_id": workspace_id})
        config.set_regions(regions)
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
        config.update_config("configuration.region", region)


def runtime_version_list(runtime_id):

    res = list_runtime_versions({"template_id": runtime_id})
    filtered_data = [item for item in res if item["status"] != "BUILD_FAILED"]
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

    if len(filtered_data) == 0:
        raise InferlessCLIError("No versions found with status READY or PENDING")

    for version in filtered_data:
        table.add_row(
            "version-" + str(version["version_no"]),
            str(version["version_no"]),
            version["status"],
        )

    console = Console()
    console.print("\n", table, "\n")
