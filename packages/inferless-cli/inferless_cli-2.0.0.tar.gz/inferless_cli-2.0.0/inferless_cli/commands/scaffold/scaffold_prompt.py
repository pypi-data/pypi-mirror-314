import rich
import typer

from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import log_exception
from inferless_cli.utils.services import (
    create_presigned_download_url,
    get_file_download,
    set_onboarding_status,
)


def scaffold_prompt(demo):
    try:
        if demo:
            payload_apppy = {
                "url_for": "ONBOARDING_FILE_DOWNLOAD",
                "file_name": "app.py",
            }
            res = create_presigned_download_url(payload_apppy)
            response_apppy = get_file_download(res)          
            if response_apppy.status_code == 200:
                app_file_path = "app.py"
                with open(app_file_path, "wb") as app_file:
                    app_file.write(response_apppy.content)

            
            payload_io = {
                "url_for": "ONBOARDING_FILE_DOWNLOAD",
                "file_name": "input_schema.py",
            }
            res_io = create_presigned_download_url(payload_io)
            response_io = get_file_download(res_io)
            if response_io.status_code == 200:
                input_schema_file_path = "input_schema.py"
                with open(input_schema_file_path, "wb") as input_schema_file:
                    input_schema_file.write(response_io.content)
            
            
            # config_file_path = "inferless.yaml"
            
            # with open(config_file_path, "w") as config_file:
            #     config_file.write(DEMO_INFERLESS_YAML_FILE)
            set_onboarding_status({"onboarding_type": "cli", "state": "files_downloaded"})
            rich.print("Scaffolding demo project done")

        else:
            rich.print("Scaffolding new project")

    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        rich.print(f"\n[red]Something went wrong {error}[/red]")
        log_exception(error)
        raise typer.Abort(1)
