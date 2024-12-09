import json
import requests
from inferless_cli.utils.exceptions import InferlessCLIError
from inferless_cli.utils.helpers import decrypt_tokens
from sentry_sdk import capture_exception, flush


def make_request(
    url,
    method="GET",
    data=None,
    headers=None,
    params=None,
    auth=True,
    convert_json=True,
):
    """
    Make a GET, PUT, DELETE, or POST request.
    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use ('GET' or 'POST'). Default is 'GET'.
        data (dict): The request data to include in the request body for POST requests.
        headers (dict): Additional headers to include in the request.
        params (dict): URL parameters for the request.
        auth (boolean): Boolean True or False.
        convert_json (boolean): Boolean True or False.
    Returns:
        requests.Response: The response object from the request.

    Raises:
        requests.HTTPError: If the request encounters an error.
        InferlessCLIError: If the request encounters an error.
        Exception: If the request encounters an error.

    """
    try:
        method = check_and_validate_menthods(method)
        headers = get_headers(headers)

        if auth:
            headers = get_auth_header(headers)

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(
                url, headers=headers, data=convert_json and json.dumps(data) or data
            )
        elif method == "PUT":
            response = requests.put(
                url, headers=headers, data=convert_json and json.dumps(data) or data
            )
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        response.raise_for_status()

        return response

    except requests.HTTPError as http_err:
        error_message = capture_and_get_error_message(error=http_err, response=response)
        raise requests.HTTPError(error_message, response=response)

    except Exception as error:
        error_message = capture_and_get_error_message(error, response)
        raise Exception(error_message)


def capture_and_get_error_message(error, response):
    capture_exception(error)
    flush()
    # Handle HTTPError specifically

    error_message = "Something went wrong"
    if hasattr(response, "json") and callable(response.json):
        error = response.json()
        if "reason" in error:
            error_message = error["reason"]
        elif "details" in error:
            error_message = error["details"]
        elif "detail" in error:
            error_message = error["detail"]

    return error_message


def check_and_validate_menthods(method):
    method = method.upper()  # Ensure the method is in uppercase.

    if method not in ("GET", "POST", "PUT", "DELETE"):
        raise ValueError("Invalid HTTP method. Use 'GET', 'PUT', 'DELETE', or 'POST'.")

    return method


def get_auth_header(headers):
    token, _, _, _, _ = decrypt_tokens()
    if not token:
        raise InferlessCLIError(
            "[red]Please login to Inferless using `inferless login`[/red]"
        )

    auth_header = {"Authorization": f"Bearer {token}"}
    headers.update(auth_header)
    return headers


def get_headers(headers):
    default_headers = {
        "Content-Type": "application/json",
    }

    if headers is not None:
        default_headers.update(headers)
    else:
        headers = default_headers

    return headers
