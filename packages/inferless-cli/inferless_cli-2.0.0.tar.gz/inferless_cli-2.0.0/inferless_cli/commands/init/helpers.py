import os
import rich
import json

import toml
from inferless_cli.commands.init.constants import ACCOUNT_NOT_FOUND_MSG
from inferless_cli.utils.constants import (
    FRAMEWORKS,
    GITHUB,
    MACHINE_TYPE_SERVERS,
    UPLOAD_METHODS,
)
from inferless_cli.utils.exceptions import (
    InferlessCLIError,
    VersionNotStringTomlFileError,
)
from inferless_cli.utils.helpers import log_exception
from prompt_toolkit.completion import WordCompleter


def handle_connected_accounts(accounts):
    if len(accounts) > 0:
        for account in accounts:
            if account.get("provider") == GITHUB:
                return True
        raise InferlessCLIError(ACCOUNT_NOT_FOUND_MSG)
    raise InferlessCLIError(ACCOUNT_NOT_FOUND_MSG)


def get_region_types(regions):
    return WordCompleter(
        regions,
        ignore_case=True,
    )


def get_machine_types(machines):
    return WordCompleter(
        machines,
        ignore_case=True,
    )


def get_region_id(region_name, regions):
    for region in regions:
        if region["region_name"] == region_name:
            return region["region_id"]
    return None


def get_region_region_id(region_name, regions):
    for region in regions:
        if region["region_id"] == region_name:
            return region["region_name"]
    return None


def get_machine_details(machine_name, region_id, server_type, machines):
    for machine in machines:
        if (
            machine["name"] == machine_name
            and machine["region_id"] == region_id
            and machine["machine_type"] == server_type
        ):
            return machine
    return None


def generate_input_and_output_files(
    input_data,
    output_data,
    input_file_name="input.json",
    output_file_name="output.json",
):
    """
    Generate input and output JSON files.

    Args:
        input_data (dict): The data to be saved in the input JSON file.
        output_data (dict): The data to be saved in the output JSON file.
        input_file_name (str): The name of the input JSON file. Default is 'input.json'.
        output_file_name (str): The name of the output JSON file. Default is 'output.json'.

    Returns:
        None
    """
    # Save the input data to input.json
    try:
        with open(input_file_name, "w") as input_file:
            json.dump(input_data, input_file, indent=4)
    except Exception as e:
        log_exception(e)
        raise InferlessCLIError("An error occurred while saving the input data.")

    # Save the output data to output.json
    try:
        with open(output_file_name, "w") as output_file:
            json.dump(output_data, output_file, indent=4)
    except Exception as e:
        log_exception(e)
        raise InferlessCLIError("An error occurred while saving the output data.")


def get_machine_types_servers():
    return WordCompleter(
        MACHINE_TYPE_SERVERS,
        ignore_case=True,
    )


def find_requirements_file():
    current_dir = os.getcwd()

    requirements_path = os.path.join(current_dir, "requirements.txt")
    pyproject_path = os.path.join(current_dir, "pyproject.toml")

    if os.path.isfile(requirements_path):
        return requirements_path, "txt", "requirements.txt"
    if os.path.isfile(pyproject_path):
        return pyproject_path, "toml", "pyproject.toml"
    return None, None, None


def get_upload_methods():
    return WordCompleter(
        UPLOAD_METHODS,
        ignore_case=True,
    )


def get_frameworks():
    return WordCompleter(
        FRAMEWORKS,
        ignore_case=True,
    )


def read_requirements_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return [
                line.strip()
                for line in file.readlines()
                if not line.strip().startswith("#")
            ]
    except Exception as e:
        rich.print(f"[red]An error occurred while reading {file_path}: {e}[/red]")
        return []


def read_pyproject_toml(file_path):
    try:
        with open(file_path, "r") as file:
            pyproject_data = toml.load(file)
            dependencies = []

            # Checking for poetry style dependencies
            poetry_deps = pyproject_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            if poetry_deps:
                for package, version in poetry_deps.items():
                    if not isinstance(version, str):
                        raise VersionNotStringTomlFileError(
                            f"Invalid version format for '{package}' in {file_path}."
                        )

                    version_str = str(version).replace("^", "").replace("~", "")
                    dependencies.append(f"{package}=={version_str}")

            # Checking for PEP 621 style dependencies
            pep621_deps = pyproject_data.get("project", {}).get("dependencies", [])
            if pep621_deps:
                dependencies.extend(pep621_deps)
            return dependencies
    except VersionNotStringTomlFileError as e:
        rich.print(f"[red]Error: {e} [/red]")
        return []
    except Exception as e:
        log_exception(e)
        rich.print(f"[red]An error occurred while reading {file_path}[/red]")
        return []
