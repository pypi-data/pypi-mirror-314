import dateutil
import typer
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.utils.constants import SPINNER_DESCRIPTION
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import log_exception

from inferless_cli.utils.services import (
    get_user_secrets,
)


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = SPINNER_DESCRIPTION
no_secrets = "[red]No secrets found in your account[/red]"


@app.command(
    "list",
    help="List all secrets.",
)
def list_secrets():
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            secrets = get_user_secrets()
            progress.remove_task(task_id)

        if len(secrets) == 0:
            raise InferlessCLIError(no_secrets)

        table = Table(
            title="Secrets List",
            box=rich.box.ROUNDED,
            title_style="bold Black underline on white",
        )
        table.add_column("ID", style="yellow")
        table.add_column(
            "Name",
        )
        table.add_column("Created At")
        table.add_column("Last used on")

        for secret in secrets:
            created_at = "-"
            updated_at = "-"
            if secret["created_at"]:
                created_at = dateutil.parser.isoparse(secret["created_at"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            if secret["last_used_in_model_import"]:
                updated_at = dateutil.parser.isoparse(
                    secret["last_used_in_model_import"]
                ).strftime("%Y-%m-%d %H:%M:%S")

            table.add_row(
                secret["id"],
                secret["name"],
                created_at,
                updated_at,
            )

        console = Console()
        console.print(table, "\n")
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
