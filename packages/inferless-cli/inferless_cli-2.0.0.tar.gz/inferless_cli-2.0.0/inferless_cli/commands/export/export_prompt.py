import rich
import os
import typer
from typing import Optional
from prompt_toolkit import prompt
from inferless_cli.commands.export.convertors import Convertors
from inferless_cli.utils.constants import (
    PROVIDER_EXPORT_CHOICES,
    DEFAULT_RUNTIME_FILE_NAME,
)
from inferless_cli.utils.exceptions import InferlessCLIError
from inferless_cli.utils.helpers import log_exception


def export_runtime_configuration(
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
    try:
        if not os.path.exists(source_file):
            rich.print(
                f"[bold red]Error:[/bold red] File '{source_file}' does not exist."
            )
            raise typer.Exit()

        if destination_file == DEFAULT_RUNTIME_FILE_NAME and os.path.exists(
            destination_file
        ):
            rich.print(
                f"[yellow]Warning:[/yellow] File '{destination_file}' already exists. It will be overwritten."
            )
            answer = prompt("Do you want to continue? (y/n) ", default="n")
            if answer != "y":
                raise typer.Exit()

        if from_provider not in PROVIDER_EXPORT_CHOICES:
            rich.print(
                f"Error: '--from' must be one of {PROVIDER_EXPORT_CHOICES}, got '{from_provider}' instead."
            )
            raise typer.Exit()

        Convertors.convert_cog_to_runtime_yaml(source_file, destination_file)

        rich.print(
            f"[green]Success:[/green] Runtime configuration exported to '{destination_file}'"
        )
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print("\n[red]Something went wrong[/red]")
        raise typer.Abort(1)
