from fun_with_ast.placeholders.node import ValidateStart
from fun_with_ast.placeholders.string_parser import StripStartParens
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


def MatchPlaceholder(string, node, placeholder):
    """Match a placeholder against a string."""
    matched_text = placeholder._match(node, string)
    if not matched_text:
        return string
    ValidateStart(string, matched_text)
    if not isinstance(placeholder, TextPlaceholder):
        matched_text = StripStartParens(matched_text)
    before, after = string.split(matched_text, 1)
    if StripStartParens(before):
        raise BadlySpecifiedTemplateError(
            'string "{}" should have started with placeholder "{}"'
                .format(string, placeholder))
    return after


def MatchPlaceholderList(string, node, placeholders, starting_parens=None):
    remaining_string = string
    for placeholder in placeholders:
        if remaining_string == string:
            placeholder.SetStartingParens(starting_parens)
        remaining_string = MatchPlaceholder(
            remaining_string, node, placeholder)
    return remaining_string
