import json

import pytest
import requests
from promptflow.connections import CustomConnection

from nest_gen_accelerator_azure.tools.llm_tool import llm_tool


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    return CustomConnection(
        {
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
        {
            "endpoint": "my-endpoint",
        },
    )


@pytest.fixture
def my_llm_mock_response():
    return {
        "usage": {"total_tokens": 42},
        "choices": [{"message": {"content": "This is a mock response"}}],
    }


def test_llm_tool(mocker, my_custom_connection, my_llm_mock_response):
    mock_requests_post = mocker.patch(
        "nest_gen_accelerator_azure.tools.llm_tool.requests.post"
    )
    mock_requests_post.return_value.json.return_value = my_llm_mock_response
    mock_requests_post.return_value.status_code = 200

    result = llm_tool(my_custom_connection, rendered_prompt="user:\nThis is a test")
    assert result["usage"]["total_tokens"] > 0
    assert result["choices"][0]["message"]["content"] == "This is a mock response"


def test_llm_tool_http_500_no_healthy_upstream(mocker, my_custom_connection):
    mock_requests_post = mocker.patch(
        "nest_gen_accelerator_azure.tools.llm_tool.requests.post"
    )
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "no healthy upstream"
    mock_response.json.side_effect = json.JSONDecodeError(
        "Expecting value", "no healthy upstream", 0
    )
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error: Server Error for url: https://example.com"
    )
    mock_requests_post.return_value = mock_response

    result = llm_tool(my_custom_connection, rendered_prompt="user:\nThis is a test")
    assert "error" in result and result["error"] == "HTTP error"
    assert "details" in result
    assert "status_code" in result and result["status_code"] == 500
    assert "response" in result and result["response"] == "no healthy upstream"
    assert "params" in result


def test_llm_tool_request_exception(mocker, my_custom_connection):
    mock_requests_post = mocker.patch(
        "nest_gen_accelerator_azure.tools.llm_tool.requests.post"
    )
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException(
        "Request error"
    )
    mock_requests_post.return_value = mock_response

    result = llm_tool(my_custom_connection, rendered_prompt="user:\nThis is a test")
    assert "error" in result and result["error"] == "Request error"
    assert "details" in result and "Request error" in result["details"]


def test_llm_tool_json_decode_error(mocker, my_custom_connection):
    mock_requests_post = mocker.patch(
        "nest_gen_accelerator_azure.tools.llm_tool.requests.post"
    )
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "Invalid JSON response"
    mock_response.json.side_effect = json.JSONDecodeError(
        "Expecting value", "Invalid JSON response", 0
    )
    mock_requests_post.return_value = mock_response

    result = llm_tool(my_custom_connection, rendered_prompt="user:\nThis is a test")
    assert "error" in result and result["error"] == "Invalid JSON object"
    assert "details" in result and "Expecting value" in result["details"]
