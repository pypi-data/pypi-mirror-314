import os

import requests
from prompt_toolkit.validation import ValidationError
from ruamel import yaml


def validate_workspaces(choice, options):
    valid_choices = [item["name"] for item in options]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice


def validate_volumes(choice, volumes):
    valid_choices = [item["name"] for item in volumes]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice


def validate_models(choice, models):
    valid_choices = [item["name"] for item in models]
    if choice not in valid_choices:
        raise ValidationError(
            message=f"Invalid choice. Please select from {', '.join(valid_choices)}"
        )
    return choice


def validate_remote_run(file_path, config_path):
    # check if file exists
    if not os.path.exists(file_path):
        raise ValidationError(message="File does not exist")

    validate_remote_run_code(file_path)
    validate_remote_run_config(config_path)


def validate_remote_run_code(file_path):
    # check if file is a python file
    if not file_path.endswith(".py"):
        raise ValidationError(message="File must be a python file")

    # check for syntax errors using ast
    try:
        with open(file_path) as f:
            code = f.read()
            if code == "":
                raise ValidationError(message="File is empty")
            compile(code, file_path, "exec")

    except SyntaxError as e:
        raise ValidationError(message=f"Syntax error in file: {e}")
    except Exception as e:
        raise ValidationError(message=f"Error in file: {e}")


def validate_remote_run_config(config_path):
    # check if file exists
    if not os.path.exists(config_path):
        raise ValidationError(message="Config file does not exist")

    # check if file is a yaml file
    if not config_path.endswith(".yaml"):
        raise ValidationError(message="Config file must be a yaml file")

    # the yaml should have the following structure
    # build:
    #   system_packages:
    #     - libgl1-mesa-glx
    #     - ...etc.,
    #   python_packages
    #     - numpy
    #     - ...etc., pip packages
    #   run_commands
    #     - python3 main.py
    #     - ...etc., shell to run

    # check if the yaml file has the correct structure and validate the values
    validate_remote_run_config_yaml(config_path)


def validate_remote_run_config_yaml(config_yaml):
    try:
        safe_yaml = yaml.YAML(typ="safe", pure=True)
        config = safe_yaml.load(open(config_yaml))
    except yaml.YAMLError as e:
        raise ValidationError(message=f"Error in config file: {e}")

    if config is None:
        raise ValidationError(message="Config file is empty")

    if "build" in config:
        build = config["build"]
        if "python_packages" in build:
            validate_python_packages(build["python_packages"])


def check_pypi_package(package_name, version=None):
    if version:
        url = f"https://pypi.org/pypi/{package_name}/{version}/json"
    else:
        url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    return response.status_code == 200


def parse_package_string(package_string):
    if '==' in package_string:
        package_name, version = package_string.split('==')
    else:
        package_name = package_string
        version = None
    return package_name, version


def validate_python_packages(package_list):
    for package_string in package_list:
        package_name, version = parse_package_string(package_string)
        if not check_pypi_package(package_name, version):
            raise ValidationError(message=f"Package {package_name} not found on PyPI")
