class InvalidLLMResponseException(Exception):
    """Base exception for all invalid LLM response cases."""

    def __init__(self, message="The LLM response was invalid"):
        self.message = message
        super().__init__(self.message)


class ContentPolicyViolationException(Exception):
    """Exception raised when content violates the content management policy."""

    def __init__(
        self,
        message="The response was filtered for not respecting the content management policy",
    ):
        super().__init__(message)
