import pytest

from nest_gen_accelerator_azure.components.output_parsers import JsonOutputParser
from nest_gen_accelerator_azure.components.outputs import ExitStrategy
from nest_gen_accelerator_azure.components.outputs.llm_response import LLMResponse
from nest_gen_accelerator_azure.exceptions import InvalidLLMResponseException


@pytest.fixture
def valid_llm_response():
    return {
        "choices": [
            {
                "message": {
                    "content": '{"content": "Do you know where my orders FR6A0889826 and FR6A0898073 are?", "callToAction": {"type": "NONE"}, "exitStrategy": ""}'
                }
            }
        ],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": {"seed": 42, "temperature": 0.7},
    }


@pytest.fixture
def handover_response():
    return {
        "choices": [
            {
                "message": {
                    "content": '{"content": "Can I talk to an agent?", "callToAction": {"type": "TO_LIVE_AGENT", "value": true}, "exitStrategy": ""}'
                }
            }
        ],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": {"seed": 42, "temperature": 0.7},
    }


@pytest.fixture
def invalid_llm_response():
    return {
        "choices": [],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": {"seed": 42, "temperature": 0.7},
    }


@pytest.fixture
def policy_violation_response():
    return {
        "errorMessage": {
            "error": {
                "message": "Content policy violation",
                "innererror": {"code": "ResponsibleAIPolicyViolation"},
            },
        },
    }


class TestValidResponses:
    def test_from_json_valid_response(self, valid_llm_response):
        tracking_id = "test-tracking-id"
        response = LLMResponse.from_json(valid_llm_response, tracking_id)

        assert (
            response.content
            == "Do you know where my orders FR6A0889826 and FR6A0898073 are?"
        )
        assert response.call_to_action.type == "NONE"
        assert response.exit_strategy == ExitStrategy.EMPTY
        assert response.model_details["name"] == "test-model"
        assert response.model_details["total_tokens"] == 30
        assert response.model_details["params"] == {"seed": 42, "temperature": 0.7}

    def test_from_json_handover_response(self, handover_response):
        tracking_id = "test-tracking-id"
        response = LLMResponse.from_json(handover_response, tracking_id)

        assert response.content == "Can I talk to an agent?"
        assert response.call_to_action.type == "TO_LIVE_AGENT"
        assert response.call_to_action.value is True
        assert response.exit_strategy == ExitStrategy.EMPTY
        assert response.model_details["name"] == "test-model"
        assert response.model_details["total_tokens"] == 30

    def test_to_json_serialization(self, valid_llm_response):
        tracking_id = "test-tracking-id"
        response = LLMResponse.from_json(valid_llm_response, tracking_id)
        serialized = response.to_dict()

        assert isinstance(serialized, dict)
        assert (
            serialized["content"]
            == "Do you know where my orders FR6A0889826 and FR6A0898073 are?"
        )
        assert serialized["callToAction"] == {"type": "NONE"}
        assert serialized["exitStrategy"] == ""
        assert serialized["modelStats"] == {
            "name": "test-model",
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
            "params": {"seed": 42, "temperature": 0.7},
        }


class TestErrorHandling:
    def test_from_json_invalid_response(self, invalid_llm_response):
        tracking_id = "test-tracking-id"
        response = LLMResponse.from_json(invalid_llm_response, tracking_id)

        assert response.call_to_action.type == "NONE"
        assert response.exit_strategy == ExitStrategy.ON_ERROR
        assert response.model_details["name"] == "test-model"
        assert response.model_details["total_tokens"] == 30

    def test_from_json_parsing_error(self, mocker, valid_llm_response):
        tracking_id = "test-tracking-id"
        mocker.patch.object(
            JsonOutputParser, "parse", side_effect=ValueError("Parsing error")
        )

        response = LLMResponse.from_json(valid_llm_response, tracking_id)

        assert response.call_to_action.type == "NONE"
        assert response.exit_strategy == ExitStrategy.ON_ERROR
        assert response.model_details["name"] == "test-model"
        assert response.model_details["total_tokens"] == 30

    def test_content_policy_violation(self, policy_violation_response):
        tracking_id = "test-tracking-id"
        response = LLMResponse.from_json(policy_violation_response, tracking_id)

        assert response.call_to_action.type == "NONE"
        assert response.exit_strategy == ExitStrategy.OUT_OF_DOMAIN
