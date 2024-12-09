import rich
from inferless_cli.utils.helpers import decrypt_tokens, get_current_mode
from inferless_cli.utils.validators import validate_remote_run
import subprocess


def remote_run_prompt(file_path, config_path, exclude_file):
    validate_remote_run(file_path, config_path)
    access_token, _, _, _, _ = decrypt_tokens()
    # execute the command INFERLESS_ACCESS_TOKEN=access_token python3 file_path
    command = f"INFERLESS_ACCESS_TOKEN={access_token} python3 {file_path} {config_path}"
    if get_current_mode() == "DEV":
        command = f"INFERLESS_ENV=DEV {command}"
    if exclude_file:
        command = f"{command} {exclude_file}"
    command = f"IS_REMOTE_RUN=True {command}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        rich.print("\n[red]Something went wrong[/red]")
