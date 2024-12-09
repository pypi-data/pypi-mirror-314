import rich
from inferless_cli.utils.helpers import open_url
from inferless_cli.utils.constants import CLI_AUTH_URL


def login_prompt():
    rich.print(
        "This command will authenticate with Inferless cli. You will need a Inferless account.\n"
    )

    if open_url(CLI_AUTH_URL):
        rich.print(
            "The web browser should have opened for you to authenticate and get an API token.\n"
            "If it didn't, please copy this URL into your web browser manually:\n"
        )
    else:
        rich.print(
            "[red]Was not able to launch web browser[/red]\n"
            "Please go to this URL manually and complete the flow:\n"
        )
    rich.print(f"[link={CLI_AUTH_URL}]{CLI_AUTH_URL}[/link]\n")

    rich.print(
        "Once logged in, paste the authentication key and secret command here, then hit enter"
    )
