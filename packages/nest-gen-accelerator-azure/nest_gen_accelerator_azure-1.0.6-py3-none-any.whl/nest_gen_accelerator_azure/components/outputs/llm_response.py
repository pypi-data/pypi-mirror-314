import logging
import traceback

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from nest_gen_accelerator_azure.components.output_parsers import JsonOutputParser
from nest_gen_accelerator_azure.components.outputs import CallToAction, ExitStrategy
from nest_gen_accelerator_azure.exceptions import (
    ContentPolicyViolationException,
    InvalidLLMResponseException,
)

logger = logging.getLogger(__name__)


class LLMResponse(BaseModel):
    """LLMResponse class encapsulating the response structure and parsing logic."""

    content: str = Field(alias="content")
    call_to_action: CallToAction = Field(alias="callToAction")
    exit_strategy: ExitStrategy = Field(alias="exitStrategy")
    model_details: dict = Field(alias="modelStats")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        protected_namespaces=(),
    )

    @field_serializer("call_to_action", when_used="json")
    def serialize_call_to_action(self, call_to_action: CallToAction) -> dict:
        return call_to_action.model_dump(exclude_none=True)

    @field_serializer("exit_strategy", when_used="json")
    def serialize_exit_strategy(self, exit_strategy: ExitStrategy) -> str:
        return exit_strategy.value

    @classmethod
    def validate_response_structure(cls, llm_response: dict) -> None:
        """Validates the LLM response structure has all required fields."""
        if not isinstance(llm_response, dict):
            raise InvalidLLMResponseException("LLM response must be a dictionary")

        # Check main required keys
        if not all(
            key in llm_response for key in ["choices", "model", "usage", "params"]
        ):
            raise InvalidLLMResponseException(
                "Missing required top-level keys in LLM response"
            )

        # Validate choices structure
        choices = llm_response.get("choices", [])
        if not choices or not isinstance(choices[0], dict):
            raise InvalidLLMResponseException("Invalid choices structure")

        # Validate message structure
        message = choices[0].get("message", {})
        if not isinstance(message, dict) or "content" not in message:
            raise InvalidLLMResponseException("Invalid message structure")

        # Validate usage structure
        usage = llm_response.get("usage", {})
        required_usage = ["prompt_tokens", "completion_tokens", "total_tokens"]
        if not all(key in usage for key in required_usage):
            raise InvalidLLMResponseException("Missing required usage statistics")

    @classmethod
    def create_error_response(
        cls,
        message: str,
        exit_strategy: ExitStrategy,
        llm_response: dict,
    ) -> "LLMResponse":
        """Creates a standardized error response."""
        return cls(
            content=message,
            call_to_action=CallToAction(type="NONE"),
            exit_strategy=exit_strategy,
            model_details={
                "name": llm_response.get("model", ""),
                "prompt_tokens": llm_response.get("usage", {}).get(
                    "prompt_tokens", None
                ),
                "completion_tokens": 0,
                "total_tokens": llm_response.get("usage", {}).get("total_tokens", None),
                "params": llm_response.get("params", {}),
            },
        )

    @staticmethod
    def handle_policy_violation(error_info: dict) -> None:
        """Handles content policy violations by raising appropriate exception."""
        error_message = error_info.get("message", "Unknown error")
        innererror = error_info.get("innererror", {})

        logger.error(
            "Content policy violation detected",
            extra={"error_message": error_message, "innererror": innererror},
        )

        raise ContentPolicyViolationException(error_message)

    @classmethod
    def process_response_errors(cls, llm_response: dict) -> None:
        """Process any errors in the LLM response and raise appropriate exceptions."""
        error_info = llm_response.get("errorMessage", {}).get("error", {})
        if not error_info:
            return

        if (
            error_info.get("innererror", {}).get("code")
            == "ResponsibleAIPolicyViolation"
        ):
            cls.handle_policy_violation(error_info)

        logger.error(
            "Error in response object",
            extra={
                "error_info": error_info,
                "tracking_id": llm_response.get("tracking_id"),
            },
        )
        raise InvalidLLMResponseException(error_info.get("message", "Unknown error"))

    @classmethod
    def from_json(cls, llm_response: dict, tracking_id: str) -> "LLMResponse":
        try:
            cls.process_response_errors(llm_response)
            cls.validate_response_structure(llm_response)

            choices = llm_response["choices"]
            message = choices[0]["message"]
            message_content = JsonOutputParser.parse(message["content"])
            content = message_content.get("content")

            # TODO Determine call to action through prompt
            if (
                message_content
                and message_content.get("callToAction", {}).get("type")
                == "TO_LIVE_AGENT"
            ) or (content and "dolce-gusto.fr/nous-contacter" in content):
                call_to_action = CallToAction(type="TO_LIVE_AGENT", value=True)
            else:
                call_to_action = CallToAction(type="NONE")

            exit_strategy = message_content.get("exitStrategy")

            model_details = {
                "name": llm_response["model"],
                "prompt_tokens": llm_response["usage"]["prompt_tokens"],
                "completion_tokens": llm_response["usage"]["completion_tokens"],
                "total_tokens": llm_response["usage"]["total_tokens"],
                "params": llm_response["params"],
            }

            response_instance = cls(
                content=content,
                call_to_action=call_to_action,
                exit_strategy=exit_strategy,
                model_details=model_details,
            )

            logger.info(
                "Successfully parsed JSON response.",
                extra={
                    "content": content,
                    "tracking_id": tracking_id,
                    "total_tokens": model_details["total_tokens"],
                    "exit_strategy": exit_strategy,
                },
            )

            return response_instance

        except ContentPolicyViolationException:
            logger.warning(
                "Content policy violation detected",
                extra={"tracking_id": tracking_id},
            )
            return cls.create_error_response(
                "I apologize, but I cannot provide an answer to that query due to content policy restrictions.",
                ExitStrategy.OUT_OF_DOMAIN,
                llm_response,
            )

        except InvalidLLMResponseException as e:
            logger.error(
                "Invalid LLM response structure",
                extra={"error": str(e), "tracking_id": tracking_id},
            )
            return cls.create_error_response(
                "I apologize, but I cannot provide an answer to that query due to an internal error.",
                ExitStrategy.ON_ERROR,
                llm_response,
            )

        except Exception as e:
            logger.error(
                "Unexpected error while parsing LLM response",
                extra={
                    "error": str(e),
                    "tracking_id": tracking_id,
                    "traceback": traceback.format_exc(),
                },
            )
            return cls.create_error_response(
                "I apologize, but I cannot provide an answer to that query due to an internal error.",
                ExitStrategy.ON_ERROR,
                llm_response,
            )

    def to_dict(self) -> dict:
        return self.model_dump(mode="json", by_alias=True)
