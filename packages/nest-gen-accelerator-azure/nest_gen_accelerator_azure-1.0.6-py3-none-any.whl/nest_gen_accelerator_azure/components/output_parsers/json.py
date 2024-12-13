import json
import re
from typing import Any, Callable

from nest_gen_accelerator_azure.components.output_parsers import BaseLLMOutputParser


class JsonOutputParser(BaseLLMOutputParser):
    """Parse the output of an LLM to a JSON object."""

    _json_strip_chars = " \n\r\t`"
    _json_markdown_re = re.compile(r"```(json)?(.*)", re.DOTALL)

    @staticmethod
    def parse_partial_json(s: str, *, strict: bool = False) -> Any:
        """Parse a JSON string that may be missing closing braces.

        Args:
            s: The JSON string to parse.
            strict: Whether to use strict parsing. Defaults to False.

        Returns:
            The parsed JSON object as a Python dictionary.
        """
        # Attempt to parse the string as-is.
        try:
            return json.loads(s, strict=strict)
        except json.JSONDecodeError:
            pass

        # Initialize variables.
        new_chars = []
        stack = []
        is_inside_string = False
        escaped = False

        # Process each character in the string one at a time.
        for char in s:
            if is_inside_string:
                if char == '"' and not escaped:
                    is_inside_string = False
                elif char == "\n" and not escaped:
                    char = (
                        "\\n"  # Replace the newline character with the escape sequence.
                    )
                elif char == "\\":
                    escaped = not escaped
                else:
                    escaped = False
            else:
                if char == '"':
                    is_inside_string = True
                    escaped = False
                elif char == "{":
                    stack.append("}")
                elif char == "[":
                    stack.append("]")
                elif char == "}" or char == "]":
                    if stack and stack[-1] == char:
                        stack.pop()
                    else:
                        # Mismatched closing character; the input is malformed.
                        return None

            # Append the processed character to the new string.
            new_chars.append(char)

        # If we're still inside a string at the end of processing,
        # we need to close the string.
        if is_inside_string:
            new_chars.append('"')

        # Reverse the stack to get the closing characters.
        stack.reverse()

        # Try to parse mods of string until we succeed or run out of characters.
        while new_chars:
            # Close any remaining open structures in the reverse
            # order that they were opened.
            # Attempt to parse the modified string as JSON.
            try:
                return json.loads("".join(new_chars + stack), strict=strict)
            except json.JSONDecodeError:
                # If we still can't parse the string as JSON,
                # try removing the last character
                new_chars.pop()

        # If we got here, we ran out of characters to remove
        # and still couldn't parse the string as JSON, so return the parse error
        # for the original string.
        return json.loads(s, strict=strict)

    @staticmethod
    def _replace_new_line(match: re.Match[str]) -> str:
        """
        Replace newlines, tabs, and quotes in the matched string with their escaped counterparts.
        """
        value = match.group(2)
        value = re.sub(r"\n", r"\\n", value)
        value = re.sub(r"\r", r"\\r", value)
        value = re.sub(r"\t", r"\\t", value)
        value = re.sub(r'(?<!\\)"', r"\"", value)

        return match.group(1) + value + match.group(3)

    @staticmethod
    def _custom_parser(multiline_string: str) -> str:
        """
        The LLM response for `action_input` may be a multiline
        string containing unescaped newlines, tabs or quotes. This function
        replaces those characters with their escaped counterparts.
        (newlines in JSON must be double-escaped: `\\n`)
        """
        if isinstance(multiline_string, (bytes, bytearray)):
            multiline_string = multiline_string.decode()

        multiline_string = re.sub(
            r'("action_input"\:\s*")(.*?)(")',
            JsonOutputParser._replace_new_line,
            multiline_string,
            flags=re.DOTALL,
        )

        return multiline_string

    @staticmethod
    def _parse_json(json_str: str, *, parser: Callable[[str], Any] = None) -> dict:
        if parser is None:
            parser = JsonOutputParser.parse_partial_json

        # Strip whitespace,newlines,backtick from the start and end
        json_str = json_str.strip(JsonOutputParser._json_strip_chars)

        # handle newlines and other special characters inside the returned value
        json_str = JsonOutputParser._custom_parser(json_str)

        # Parse the JSON string into a Python dictionary
        return parser(json_str)

    @staticmethod
    def parse_json_markdown(
        json_string: str, *, parser: Callable[[str], Any] = None
    ) -> dict:
        """Parse a JSON string from a Markdown string.

        Args:
            json_string: The Markdown string.

        Returns:
            The parsed JSON object as a Python dictionary.
        """
        if parser is None:
            parser = JsonOutputParser.parse_partial_json

        try:
            return JsonOutputParser._parse_json(json_string, parser=parser)

        except json.JSONDecodeError:
            # Try to find JSON string within triple backticks
            match = JsonOutputParser._json_markdown_re.search(json_string)

            # If no match found, assume the entire string is a JSON string
            # Else, use the content within the backticks
            json_str = json_string if match is None else match.group(2)

        return JsonOutputParser._parse_json(json_str, parser=parser)

    @classmethod
    def parse(cls, text: str) -> dict:
        """Parse the output of an LLM call to a JSON object.

        Args:
            text: The output of the LLM call.

        Returns:
            The parsed JSON object.
        """
        text = text.strip()
        try:
            return cls.parse_json_markdown(text)

        except json.JSONDecodeError:
            raise ValueError(f"Could not parse JSON string: {text}")

    @property
    def _type(self) -> str:
        """Snake-case string identifier for an output parser type."""
        return "json_output_parser"
