from abc import ABC, abstractmethod
from typing import Any


class BaseLLMOutputParser(ABC):
    """Abstract base class for parsing the outputs of a model."""

    @abstractmethod
    def parse(self, response: str) -> Any:
        """
        Parses the response from the LLM calculation.

        Args:
            response (str): The response from the LLM calculation.

        Returns:
            Any: The parsed response.
        """
        pass

    @property
    def _type(self) -> str:
        """Return the output parser type for serialization."""
        raise NotImplementedError(
            f"_type property is not implemented in class {self.__class__.__name__}."
            " This is required for serialization."
        )

    def dict(self, **kwargs: Any) -> dict:
        """Return dictionary representation of output parser."""
        output_parser_dict = super().dict(**kwargs)
        try:
            output_parser_dict["_type"] = self._type
        except NotImplementedError:
            pass

        return output_parser_dict
