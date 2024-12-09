from inferless_cli.utils.exceptions import InferlessCLIError
from inferless_cli.utils.helpers import log_exception, read_yaml, create_yaml


class Convertors:
    @staticmethod
    def get_cuda_version(cuda_version: str) -> str:
        cuda_version = float(cuda_version)
        if 11.0 <= cuda_version < 12.0:
            return "11.8.0"
        if cuda_version >= 12.0:
            return "12.1.1"
        raise InferlessCLIError("CUDA version not supported.")

    @staticmethod
    def convert_cog_to_runtime_yaml(source_file: str, destination_file: str):
        cog_yaml = read_yaml(source_file)

        filtered_data = {"build": {}}
        if cog_yaml is not None:
            for key, value in cog_yaml.get("build", {}).items():
                if key in ["cuda", "python_packages", "system_packages"]:
                    if key == "cuda":
                        try:
                            filtered_data["build"]["cuda_version"] = (
                                Convertors.get_cuda_version(value)
                            )
                        except Exception as e:
                            log_exception(e)
                            raise InferlessCLIError("CUDA version not supported.")
                    else:
                        filtered_data["build"][key] = value
        else:
            raise InferlessCLIError("[bold red]Error:[/bold red] cog.yaml not found.")

        create_yaml(filtered_data, destination_file)
