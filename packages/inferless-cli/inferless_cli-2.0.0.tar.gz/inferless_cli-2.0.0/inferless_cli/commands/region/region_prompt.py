


from rich.console import Console
from rich.table import Table
from collections import defaultdict
import typer

from inferless_cli.utils.services import get_machines

app = typer.Typer(
    no_args_is_help=True,
)


@app.command("list", help="List available regions")
def list():
    machines = get_machines()
    grouped_data = defaultdict(lambda: {"machines": defaultdict(set), "availability": {}})
    for item in machines:
        region = item["region_name"]
        machine = item["name"]
        machine_type = item["machine_type"]
        deploy_type = item["deploy_type"]

        # Add machine types to the grouped data
        grouped_data[region]["machines"][machine].add(machine_type)

        # Determine availability
        availability = "Available" if deploy_type == "CONTAINER" else "[yellow]Beta Only[/yellow]"
        grouped_data[region]["availability"][machine] = availability

    # Initialize Rich table
    console = Console()
    table = Table(title="Machine Availability by Region")
    table.add_column("Region", style="cyan", justify="center")
    table.add_column("Machines Available", style="magenta", justify="center")
    table.add_column("Availability", style="green", justify="center")

    # Populate the table
    for region, details in grouped_data.items():
        machines = []
        availability = []

        for machine, types in details["machines"].items():
            machine_types = " and ".join(sorted(types))  # Combine SHARED and DEDICATED
            machines.append(f"{machine} ({machine_types})")
            availability.append(details["availability"][machine])

        table.add_row(
            region,
            "\n".join(machines),  # Machines Available column
            "\n".join(availability),  # Availability column
        )

    # Print the table
    console.print(table)