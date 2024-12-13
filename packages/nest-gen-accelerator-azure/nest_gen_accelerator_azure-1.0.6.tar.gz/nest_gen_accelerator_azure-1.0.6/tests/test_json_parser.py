import json

import pytest

from nest_gen_accelerator_azure.components.output_parsers.json import JsonOutputParser


def test_parse_json_valid():
    json_string = '{"key": "value"}'
    result = JsonOutputParser.parse(json_string)
    assert result == {"key": "value"}


def test_parse_unclosed_json():
    json_string = '{"key": "value"'
    result = JsonOutputParser.parse(json_string)
    assert result == {"key": "value"}


def test_parse_json_markdown_with_backticks():
    json_string = '```json\n{"key": "value"}\n```'
    result = JsonOutputParser.parse(json_string)
    assert result == {"key": "value"}


def test_parse_json_markdown_with_partial_json():
    json_string = '{"key": "value"'
    result = JsonOutputParser.parse_json_markdown(
        json_string, parser=JsonOutputParser.parse_partial_json
    )
    assert result == {"key": "value"}


def test_parse_json_markdown_with_custom_parser():
    def custom_parser(s):
        return {"custom_key": "custom_value"}

    json_string = '{"key": "value"}'
    result = JsonOutputParser.parse_json_markdown(json_string, parser=custom_parser)
    assert result == {"custom_key": "custom_value"}
