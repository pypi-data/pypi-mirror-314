import rich
from rich.table import Table
from rich.console import Console
import typer

from inferless_cli.commands.integration import integration_sub_prompts
from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import log_exception
from inferless_cli.utils.services import get_accounts

app = typer.Typer(
    no_args_is_help=True,
)

app.add_typer(
    integration_sub_prompts.app,
    name="add",
    help="Add an integration to your workspace",
)

@app.command("list", help="List all integrations")
def list_integrations():
    try:
        res = get_accounts()

        accounts_status = res.get('accounts_status', {})

        # Initialize the Rich Console
        console = Console()

        # Create a table
        table = Table(title="Integration Status", show_lines=True)
        table.add_column("Account Name", style="cyan", justify="center")
        table.add_column("Integration Name", style="magenta", justify="center")
        table.add_column("Status", style="green", justify="center")

        # Populate the table with data
        for key, details in accounts_status.items():
            if key in ["AWS", "GCP"]:  # Exclude "AWS" and "GCP"
                continue
            account_name = key
            integration_name = details.get('name', '-') or '-'  # Fallback to "-" if name is empty
            status = details.get('status', False)
            status_text = "[green]Connected[/green]" if status else "[red]Not Connected[/red]"
            
            table.add_row(account_name, integration_name, status_text)

        # Print the table
        console.print(table)

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)
    


def get_account_status(import_type):
    res = get_accounts()
    accounts_status = res.get('accounts_status', {})

    # Check if the import type exists and its status
    account = accounts_status.get(import_type)
    if account and account.get('status'):
        return account  # Return the account details if status is True
    return None  # Return None if status is False or import type is not found
