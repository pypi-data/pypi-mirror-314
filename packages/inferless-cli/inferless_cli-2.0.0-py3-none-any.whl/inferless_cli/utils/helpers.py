import json
import logging
import os
import webbrowser
import zipfile
import rich
import sentry_sdk
import jwt
import typer
from sentry_sdk.integrations.logging import LoggingIntegration
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from datetime import datetime, timezone
from inferless_cli import __version__
from ruamel.yaml import YAML
from sentry_sdk import capture_exception, flush
from inferless_cli.utils.credentials import (
    KEYRING,
    load_credentials,
    save_credentials,
    is_keyring_supported,
)
from inferless_cli.utils.exceptions import InferlessCLIError
from .constants import (
    DEFAULT_YAML_FILE_NAME,
    GLITCHTIP_DSN,
    REGION_TYPES,
    DEFAULT_MACHINE_VALUES,
)


yaml = YAML(typ="rt")

key_bindings = KeyBindings()


def get_default_machine_values(gpu_type, is_dedicated, region):
    if is_dedicated not in DEFAULT_MACHINE_VALUES:
        return None
    if region not in DEFAULT_MACHINE_VALUES[is_dedicated]:
        return None
    if gpu_type not in DEFAULT_MACHINE_VALUES[is_dedicated][region]:
        return None
    return DEFAULT_MACHINE_VALUES[is_dedicated][region][gpu_type]


def save_cli_tokens(key, secret):
    if is_keyring_supported():
        try:
            KEYRING.set_password("Inferless", "key", key)
            KEYRING.set_password("Inferless", "secret", secret)
        except KEYRING.errors.KeyringError as ke:
            log_exception(ke)
            raise InferlessCLIError(f"An error occurred while saving the tokens: {ke}")
        except Exception as e:
            log_exception(e)
            raise InferlessCLIError(f"An error occurred while saving the tokens: {e}")
    else:
        save_credentials(key, secret, "", "", "", "", "", "")


def set_env_mode(mode):
    if is_keyring_supported():
        try:
            KEYRING.set_password("Inferless", "mode", mode)
        except Exception as e:
            log_exception(e)
            raise InferlessCLIError(f"An error occurred while saving the env: {e}")
    else:
        save_credentials("", "", "", "", "", "", "", mode)


def save_tokens(token, refresh_token, user_id, workspace_id, workspace_name):

    if is_keyring_supported():
        try:
            KEYRING.set_password("Inferless", "token", token)
            KEYRING.set_password("Inferless", "refresh_token", refresh_token)
            KEYRING.set_password("Inferless", "user_id", user_id)
            KEYRING.set_password("Inferless", "workspace_id", workspace_id)
            KEYRING.set_password("Inferless", "workspace_name", workspace_name)
        except Exception as e:
            log_exception(e)
            raise InferlessCLIError(f"An error occurred while saving the tokens: {e}")
    else:
        save_credentials(
            access_key="",
            access_secret="",
            token=token,
            refresh_token=refresh_token,
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_name=workspace_name,
            mode="",
        )


def create_yaml(config, file_name=DEFAULT_YAML_FILE_NAME):
    try:
        with open(file_name, "w") as yaml_file:
            yaml.dump(
                config,
                yaml_file,
            )
    except Exception as e:
        log_exception(e)
        rich.print(f"Failed to create YAML file: {e}")


@key_bindings.add("c-space")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


# move this to models helper
def get_models(models):
    return WordCompleter(
        [item["name"] for item in models],
        ignore_case=True,
    )


# move this to workspace helper
def get_workspaces(workspaces):
    return WordCompleter(
        [item["name"] for item in workspaces],
        ignore_case=True,
    )


def get_region_types():
    return WordCompleter(
        REGION_TYPES,
        ignore_case=True,
    )


def print_options(options_name, options):
    console = rich.console.Console()
    console.print("\n")
    console.print(f"{options_name}", style="bold")

    for method in options:
        console.print(f"  • {method}", style="green")
    console.print("\n")


def version_callback(value: bool):
    if value:
        typer.echo(f"inferless-cli version: {__version__}")
        raise typer.Exit()


# Function to decrypt tokens
def decrypt_tokens():
    if is_keyring_supported():
        try:
            token = KEYRING.get_password("Inferless", "token")
            refresh_token = KEYRING.get_password("Inferless", "refresh_token")
            user_id = KEYRING.get_password("Inferless", "user_id")
            workspace_id = KEYRING.get_password("Inferless", "workspace_id")
            workspace_name = KEYRING.get_password("Inferless", "workspace_name")
            return token, refresh_token, user_id, workspace_id, workspace_name
        except Exception as e:
            log_exception(e)
            return None, None, None, None, None
    else:
        _, _, token, refresh_token, user_id, workspace_id, workspace_name, _ = (
            load_credentials()
        )
        return (token, refresh_token, user_id, workspace_id, workspace_name)


def get_current_mode():
    if is_keyring_supported():
        try:
            mode = KEYRING.get_password("Inferless", "mode")
            return mode
        except Exception as e:
            log_exception(e)
            return None
    else:
        _, _, _, _, _, _, _, mode = load_credentials()
        return mode


def is_inferless_yaml_present(file_path=DEFAULT_YAML_FILE_NAME):
    file_name = file_path
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)

    return os.path.isfile(file_path)


def decrypt_cli_key():
    if is_keyring_supported():
        try:
            key = KEYRING.get_password("Inferless", "key")
            refresh_token = KEYRING.get_password("Inferless", "secret")
            return key, refresh_token
        except Exception as e:
            log_exception(e)
            return None, None
    else:
        key, secret = load_credentials()[:2]
        return key, secret


def validate_jwt(jwt_token):
    try:
        # Decode the JWT token without verifying it (no secret key)
        payload = jwt.decode(
            jwt_token, options={"verify_signature": False}, algorithms="HS256"
        )
        # Check if the 'exp' (expiration) claim exists and is in the future
        if "exp" in payload:
            exp_timestamp = payload["exp"]
            if isinstance(exp_timestamp, int):
                current_timestamp = datetime.now(timezone.utc).timestamp()
                if exp_timestamp >= current_timestamp:
                    # Token is not expired
                    return True
                return False
            return False
        return False

    except jwt.ExpiredSignatureError as e:
        log_exception(e)
        # Token has expired
        return False
    except jwt.InvalidTokenError as e:
        log_exception(e)
        # Token is invalid or tampered with
        return False


def get_by_keys(data, value, key1, key2):
    if data is None:
        raise ValueError("data is None")
    if value is None:
        raise ValueError("value is None")
    if key1 is None:
        raise ValueError("key1 is None")
    if key2 is None:
        raise ValueError("key2 is None")
    for item in data:
        if item.get(key1) == value:
            return item.get(key2)
    return None


def open_url(url: str) -> bool:
    try:
        browser = webbrowser.get()
        if isinstance(browser, webbrowser.GenericBrowser):
            return False
        if not hasattr(browser, "open_new_tab"):
            return False
        return browser.open_new_tab(url)
    except webbrowser.Error as e:
        log_exception(e)
        return False


def check_import_source(file_name):
    if os.path.isfile(file_name):
        try:
            with open(file_name, "r") as yaml_file:
                inferless_config = yaml.load(yaml_file)
                import_source = inferless_config.get("import_source", "")
                source_location = inferless_config.get("source_location", "")
                if import_source == "LOCAL" or (import_source == "FILE" and source_location == "LOCAL_FILE") :
                    return True
                return False
        except Exception as e:
            log_exception(e)
            rich.print(f"Failed to read YAML file: {e}")

    return None


def read_yaml(file_name):
    try:
        if os.path.isfile(file_name):
            with open(file_name, "r", encoding="utf-8") as yaml_file:
                inferless_config = yaml.load(yaml_file)
                return inferless_config
        else:
            rich.print(f"File not found: {file_name}")
            return None
    except UnicodeDecodeError:
        try:
            with open(file_name, "r", encoding="cp1252") as yaml_file:
                inferless_config = yaml.load(yaml_file)
                return inferless_config
        except Exception as e:
            rich.print(f"Failed to read YAML file with cp1252 encoding: {e}")
            raise
    except Exception as e:
        log_exception(e)
        rich.print(f"Failed to read YAML file: {e}")
        return None


def read_json(file_name):
    try:
        with open(file_name, "r") as json_file:
            file_data = json.load(json_file)
            return file_data
    except Exception as e:
        log_exception(e)
        return None


def create_zip_file(zip_filename, directory_to_snapshot):
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_to_snapshot):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file),
                        directory_to_snapshot,
                    ),
                )


def log_exception(e):
    try:
        capture_exception(e)
        flush()
    except Exception as error:
        print(error)


def sentry_init():
    mode = "prod"
    if get_current_mode() == "DEV":
        mode = "dev"

    if GLITCHTIP_DSN:
        sentry_sdk.init(
            dsn=GLITCHTIP_DSN,
            auto_session_tracking=False,
            integrations=[
                LoggingIntegration(
                    level=logging.INFO,  # Capture info and above as breadcrumbs
                    event_level=logging.ERROR,  # Send errors as events
                ),
            ],
            traces_sample_rate=0.01,
            release=__version__,
            send_default_pii=True,
            environment=mode,
        )


def is_file_present(file_name):
    """
    Check if 'input_schema.py' is present in the current working directory.

    Returns:
    bool: True if the file is found, False otherwise.
    """
    # Get the current working directory
    current_directory = os.getcwd()

    # Combine the directory and the file name
    file_path = os.path.join(current_directory, file_name)

    # Check if the file exists at the specified path
    return os.path.isfile(file_path)


def delete_files(filenames):
    for filename in filenames:
        try:
            os.remove(filename)
        except FileNotFoundError as e:
            log_exception(e)


def merge_dicts(base_dict, new_dict):
    """
    Merges new_dict into base_dict, updating base_dict if new_dict is not empty.

    Args:
    - base_dict (dict): The base dictionary to which the new_dict will be merged.
    - new_dict (dict): The dictionary containing new items to merge into base_dict.

    Returns:
    - dict: The updated base_dict containing items from both base_dict and new_dict, if new_dict is not empty.
    """
    # Check if new_dict is not None and not empty before merging
    if new_dict:
        base_dict.update(new_dict)
    return base_dict


def convert_inferless_yaml_v1_to_v2(config_file = DEFAULT_YAML_FILE_NAME):
    try:
        is_yaml_present = is_inferless_yaml_present(config_file)

        if is_yaml_present:
            yaml_data = read_yaml(config_file)
            if yaml_data["version"] == "1.0.0":
                if not yaml_data:
                    return None
                if "configuration" in yaml_data:
                    del yaml_data["configuration"]
                if "env" in yaml_data:
                    del yaml_data["env"]
                if "optional" in yaml_data:
                    del yaml_data["optional"]
                if "io_schema" in yaml_data:
                    del yaml_data["io_schema"]
                create_yaml(yaml_data, config_file)
                return True
                
            return False
        return False
    except Exception as e:
        log_exception(e)
        return None
