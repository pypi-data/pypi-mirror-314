import io
import requests
from urllib.parse import urlencode

from ..utils import log_func_result, handle_http_response
from ..sdk import BaseCraftAiSdk


@log_func_result("Endpoint trigger")
def trigger_endpoint(
    sdk: BaseCraftAiSdk,
    endpoint_name,
    endpoint_token,
    inputs={},
    wait_for_completion=True,
):
    """Trigger an endpoint.

    Args:
        endpoint_name (:obj:`str`): Name of the endpoint.
        endpoint_token (:obj:`str`): Token to access endpoint.
        inputs (:obj:`dict`, optional): Dictionary of inputs to pass to the endpoint
            with input names as keys and corresponding values as values.
            For files, the value should be an instance of io.IOBase.
            For json, string, number, boolean and array inputs, the size of all values
            should be less than 0.06MB.
            Defaults to {}.
        wait_for_completion (:obj:`bool`, optional): Automatically call
            `retrieve_endpoint_results` and returns the execution result.
            Defaults to `True`.

    Returns:
        :obj:`dict`: Created pipeline execution represented as :obj:`dict` with the
        following keys:

        * ``"execution_id"`` (:obj:`str`): ID of the execution.
        * ``"outputs"`` (:obj:`dict`): Dictionary of outputs of the pipeline with
          output names as keys and corresponding values as values. Note that this
          key is only returned if ``wait_for_completion`` is `True`.
    """

    body = {}
    files = {}
    for input_name, input_value in inputs.items():
        if isinstance(input_value, io.IOBase) and input_value.readable():
            files[input_name] = input_value
        else:
            body[input_name] = input_value

    url = f"{sdk.base_environment_url}/endpoints/{endpoint_name}"
    post_result = requests.post(
        url,
        headers={
            "Authorization": f"EndpointToken {endpoint_token}",
            "craft-ai-client": f"craft-ai-sdk@{sdk._version}",
        },
        allow_redirects=False,
        json=body,
        files=files,
    )
    handle_http_response(post_result)
    execution_id = post_result.headers.get("Craft-Ai-Execution-Id", "")
    if wait_for_completion and 200 <= post_result.status_code < 400:
        return retrieve_endpoint_results(
            sdk, endpoint_name, execution_id, endpoint_token
        )
    return {"execution_id": execution_id}


@log_func_result("Endpoint result retrieval")
def retrieve_endpoint_results(
    sdk: BaseCraftAiSdk, endpoint_name, execution_id, endpoint_token
):
    """Get the results of an endpoint execution.

    Args:
        endpoint_name (:obj:`str`): Name of the endpoint.
        execution_id (:obj:`str`): ID of the execution returned by
            `trigger_endpoint`.
        endpoint_token (:obj:`str`): Token to access endpoint.

    Returns:
        :obj:`dict`: Created pipeline execution represented as :obj:`dict` with the
        following keys:

        * ``"outputs"`` (:obj:`dict`): Dictionary of outputs of the pipeline with
          output names as keys and corresponding values as values.
    """

    url = (
        f"{sdk.base_environment_url}"
        f"/endpoints/{endpoint_name}/executions/{execution_id}"
    )
    query = urlencode({"token": endpoint_token})
    response = requests.get(f"{url}?{query}")

    # 500 is returned if the pipeline failed too. In that case, it is not a
    # standard API error
    if response.status_code == 500:
        try:
            return handle_http_response(response)
        except KeyError:
            return response.json()

    if "application/octet-stream" in response.headers.get("Content-Type", ""):
        content_disposition = response.headers.get("Content-Disposition", "")
        output_name = content_disposition.split(f"_{execution_id}_")[1]
        return {
            "outputs": {output_name: handle_http_response(response)},
            "execution_id": execution_id,
        }
    else:
        return {**handle_http_response(response), "execution_id": execution_id}


def generate_new_endpoint_token(sdk: BaseCraftAiSdk, endpoint_name):
    """Generate a new endpoint token for an endpoint.

    Args:
        endpoint_name (:obj:`str`): Name of the endpoint.

    Returns:
        :obj:`dict[str, str]`: New endpoint token represented as :obj:`dict` with
        the following keys:

        * ``"endpoint_token"`` (:obj:`str`): New endpoint token.
    """
    url = (
        f"{sdk.base_environment_api_url}"
        f"/endpoints/{endpoint_name}/generate-new-token"
    )
    return sdk._post(url)
