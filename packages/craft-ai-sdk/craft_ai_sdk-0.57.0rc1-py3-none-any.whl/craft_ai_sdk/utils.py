from datetime import datetime
from enum import Enum
import functools
from io import BytesIO, IOBase, StringIO
import re
import sys
from typing import Callable, Iterable, Union
import xml.etree.ElementTree as ET
from requests import RequestException, Response
from json import JSONDecodeError
import os

from .exceptions import SdkException

_execution_context = None


def get_execution_id():
    global _execution_context
    if _execution_context is None:
        try:
            # File injected in steps
            import __craft_internal_execution_context  # type: ignore

            _execution_context = __craft_internal_execution_context
        except ImportError:
            _execution_context = False
    if _execution_context:
        try:
            return _execution_context.current_execution_id.get()
        except LookupError:
            pass
    return os.environ.get("CRAFT_AI_EXECUTION_ID")


def handle_data_store_response(response):
    """Return the content of a response received from the datastore
    or parse the send error and raise it.

    Args:
        response (requests.Response): A response from the data store.

    Raises:
        SdkException: When the response contains an error.

    Returns:
        :obj:`str`: Content of the response.
    """
    if 200 <= response.status_code < 300:
        return response.content

    try:
        # Parse XML error returned by the data store before raising it
        xml_error_node = ET.fromstring(response.text)
        error_infos = {node.tag: node.text for node in xml_error_node}
        error_code = error_infos.pop("Code")
        error_message = error_infos.pop("Message")
        raise SdkException(
            message=error_message,
            status_code=response.status_code,
            name=error_code,
            additional_data=error_infos,
        )
    except ET.ParseError:
        raise SdkException(
            "Unable to decode response from the data store: "
            f"Content being:\n'{response.text}'",
            status_code=response.status_code,
        )


def _parse_json_response(response):
    if response.status_code == 204 or response.text == "OK":
        return
    try:
        response_json = response.json()
    except JSONDecodeError:
        raise SdkException(
            f"Unable to decode response data into json. Data being:\n'{response.text}'",
            status_code=response.status_code,
        ) from None
    return response_json


def _raise_craft_ai_error_from_response(response: Response):
    try:
        error_content = response.json()
        error_message = error_content.get("message", "The server returned an error")

        # Permission denied inside a running execution
        if response.status_code == 403 and get_execution_id() is not None:
            error_message = (
                "Insufficient permissions. This is probably because "
                "you called an SDK function that is not permitted from "
                "inside a running deployment or execution, even if it "
                "works from your computer. Original error: " + error_message
            )

        raise SdkException(
            message=error_message,
            status_code=response.status_code,
            name=error_content.get("name"),
            request_id=error_content.get("request_id"),
            additional_data=error_content.get("additional_data"),
        )
    except JSONDecodeError:
        raise SdkException(
            "The server returned an invalid response content. "
            f"Content being:\n'{response.text}'",
            status_code=response.status_code,
        ) from None


def handle_http_response(response: Response):
    if 200 <= response.status_code < 400:
        if "application/octet-stream" in response.headers.get(
            "content-type", ""
        ) or "text/csv" in response.headers.get("content-type", ""):
            return response.content
        return _parse_json_response(response)
    _raise_craft_ai_error_from_response(response)


def handle_http_request(request_func):
    def wrapper(*args, **kwargs):
        get_response = kwargs.pop("get_response", False)
        try:
            response = request_func(*args, **kwargs)
        except RequestException as error:
            raise SdkException(
                "Unable to perform the request", name="RequestError"
            ) from error

        content = handle_http_response(response)
        if get_response:
            return content, response
        return content

    return wrapper


def log_action(sdk, message: str, should_log: Union[bool, Callable[[], bool]] = True):
    if sdk.verbose_log and (should_log() if callable(should_log) else should_log):
        print(message, file=sys.stderr)


def log_func_result(message: str, should_log: Union[bool, Callable[[], bool]] = True):
    def decorator_log_func_result(action_func):
        @functools.wraps(action_func)
        def wrapper_log_func_result(*args, **kwargs):
            sdk = args[0]
            try:
                res = action_func(*args, **kwargs)
                log_action(sdk, "{:s} succeeded".format(message), should_log)
                return res
            except SdkException as error:
                log_action(
                    sdk,
                    "{:s} failed ! {}".format(message, error),
                    should_log,
                )
                raise error
            except Exception as error:
                log_action(
                    sdk,
                    "{:s} failed for unexpected reason ! {}".format(message, error),
                    should_log,
                )
                raise error

        return wrapper_log_func_result

    return decorator_log_func_result


def _datetime_to_timestamp_in_ms(dt):
    if not isinstance(dt, datetime):
        raise ValueError("Parameter must be a datetime.datetime object.")
    return int(1_000 * dt.timestamp())


def parse_isodate(date_string):
    """_summary_

    Args:
        date_string (str): date in ISO 8601 format potentially ending with
            "Z" specific character.

    Returns:
        :obj:`datetime.datetime`: A `datetime` corresponding to `date_string`.
    """
    if date_string[-1] == "Z":
        date_string = date_string.rstrip("Z")

    return datetime.fromisoformat(re.sub(r"\.\d+", "", date_string))


def use_authentication(action_func):
    @functools.wraps(action_func)
    def wrapper(sdk, *args, headers=None, **kwargs):
        actual_headers = None
        if (
            sdk._access_token_data is None
            or sdk._access_token_data["exp"]
            < (datetime.now() + sdk._access_token_margin).timestamp()
        ):
            sdk._refresh_access_token()
        actual_headers = {"Authorization": f"Bearer {sdk._access_token}"}
        if headers is not None:
            actual_headers.update(headers)

        response = action_func(sdk, *args, headers=actual_headers, **kwargs)
        if response.status_code == 401:
            sdk._clear_access_token()
        return response

    return wrapper


def remove_none_values(obj):
    return {key: value for key, value in obj.items() if value is not None}


def remove_keys_from_dict(dictionnary: dict, paths_to_remove: set = None):
    if dictionnary is None:
        return None

    paths_to_remove = paths_to_remove or set()
    returned_dictionnary = dictionnary.copy()

    for path in paths_to_remove:
        key, _, subpath = path.partition(".")
        if subpath == "":
            returned_dictionnary.pop(key, None)
        elif isinstance(returned_dictionnary.get(key), dict):
            returned_dictionnary[key] = remove_keys_from_dict(
                returned_dictionnary[key], {subpath}
            )

    return returned_dictionnary


def merge_paths(prefix, path):
    components = (value for value in path.split("/") if value != "")
    return prefix + "/".join(components)


class CREATION_PARAMETER_VALUE(Enum):
    """Enumeration for creation parameters special values."""

    #: Special value to indicate that the parameter should be set to the
    #: project information value.
    FALLBACK_PROJECT = "FALLBACK_PROJECT"
    #: Special value to indicate that the parameter should be set to `None`.
    NULL = "NULL"


def map_container_config_step_parameter(container_config):
    """
    Maps container config with :obj:`CREATION_PARAMETER_VALUE` enum values to final
    container config. `None` is considered to be equivalent to
    :obj:`CREATION_PARAMETER_VALUE.FALLBACK_PROJECT`, and should not be projected to
    output
    """
    ret = {}
    for key in container_config:
        if key == "local_folder":
            continue
        val = container_config[key]
        if val is CREATION_PARAMETER_VALUE.NULL:
            ret[key] = None
        elif val is not CREATION_PARAMETER_VALUE.FALLBACK_PROJECT and val is not None:
            ret[key] = val
    return ret


# From https://stackoverflow.com/a/58767245/4839162
def chunk_buffer(buffer: IOBase, size: int) -> Iterable[Union[BytesIO, StringIO]]:
    size_int = int(size)
    b = buffer.read(size_int)
    next_data = None
    while b:
        chunk = StringIO() if isinstance(b, str) else BytesIO()
        previous_data = next_data
        if previous_data:
            chunk.write(next_data)
        chunk.write(b)
        chunk.seek(0)

        next_data = buffer.read(1)

        data = {
            "chunk": chunk,
            "len": len(b) + (len(previous_data) if previous_data else 0),
            "lastChunk": len(next_data) == 0,
        }
        yield data
        chunk.close()
        b = buffer.read(size_int - 1)


def convert_size(size_in_bytes):
    """
    Convert a size in bytes to a human readable string.
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size_in_bytes < 1024.0:
            break
        size_in_bytes /= 1024.0
    return "{:.2f} {}".format(size_in_bytes, unit)


# Adapted from
# https://gist.github.com/kazqvaizer/4cebebe5db654a414132809f9f88067b#file-multipartify-py-L13-L33
def multipartify(data, parent_key=None) -> dict:
    def formatter(v):
        return (None, v if v is not None else "")

    if type(data) is not dict:
        return {parent_key: formatter(data)}

    converted = []

    for key, value in data.items():
        current_key = key if parent_key is None else f"{parent_key}[{key}]"
        if type(value) is dict:
            converted.extend(multipartify(value, current_key).items())
        elif type(value) is list:
            for ind, list_value in enumerate(value):
                iter_key = f"{current_key}[{ind}]"
                converted.extend(multipartify(list_value, iter_key).items())
        else:
            converted.append((current_key, formatter(value)))

    return dict(converted)


def _wait_create_until_ready(sdk, name, get_func, timeout_s, start_time, get_log_func):
    elapsed_time = sdk._get_time() - start_time
    status = "creation_pending"
    while status == "creation_pending" and (
        timeout_s is None or elapsed_time < timeout_s
    ):
        created_obj = get_func(sdk, name)
        status = created_obj.get("creation_info", {}).get("status", None)
        elapsed_time = sdk._get_time() - start_time

    if status == "creation_failed":
        raise SdkException(
            f'The creation of "{name}" has failed. You can check the logs with '
            f'the "{get_log_func.__name__}" function.',
            name="CreationFailed",
        )
    if status != "ready":
        raise SdkException(
            f'The creation of "{name}" was not ready in time. It is still being '
            "created but this function stopped trying. Please check its status with "
            f'"{get_func.__name__}".',
            name="TimeoutException",
        )
    return created_obj
