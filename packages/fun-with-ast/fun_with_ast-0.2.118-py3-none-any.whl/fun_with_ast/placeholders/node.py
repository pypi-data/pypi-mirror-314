import ast
import re

from fun_with_ast.get_source import GetSource
from fun_with_ast.placeholders.base_placeholder import Placeholder
# from source_match import ValidateStart
from fun_with_ast.placeholders.string_parser import StripStartParens
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


def ValidateStart(original_string, matched_string):
    stripped_matched, stripped_original = _get_stripped_strings(original_string, matched_string)
    if not stripped_original.startswith(stripped_matched):
        raise BadlySpecifiedTemplateError(
            'ValidateStart:\n String "{}" should have started with string "{}"'
                .format(stripped_original, stripped_matched))
    return {"stripped_matched": stripped_matched, "stripped_original": stripped_original}


def _get_stripped_strings(original_string, matched_string):
    stripped_original = StripStartParens(original_string)
    stripped_matched = StripStartParens(matched_string)
    return stripped_matched, stripped_original


class NodePlaceholder(Placeholder):
    """Placeholder to wrap an AST node."""

    def __init__(self, node):
        super(NodePlaceholder, self).__init__()
        self.node = node
        self.parent = None

    def _match(self, unused_node, string):
        node_src = GetSource(self.node, string, self.starting_parens,parent_node=self.parent)
        try:
            ValidateStart(string, node_src)
        except BadlySpecifiedTemplateError as e:
            if isinstance(self.node, (ast.Constant)):
                node_src = self._handle_semantic_equivalent_constants(e, node_src, string)
            elif isinstance(self.node, float):
                node_src = self._handle_semantic_equivalent_float(e, node_src, string)
        return node_src

    def _handle_semantic_equivalent_constants(self, e, node_src, string):
        stripped_matched, stripped_original = _get_stripped_strings(string, node_src)
        semantic_match = self._is_semantic_equivalent_strings(string, node_src,
                                                              stripped_matched, stripped_original)
        if not semantic_match:
            raise e
        else:
            original_quote = stripped_original[0]
            current_quote = node_src[0]
            node_src = node_src.replace(current_quote, original_quote)
        return node_src

    def GetSource(self, unused_node):
        if isinstance(self.node, ast.Expr)  and not hasattr(self.node, 'node_matcher') :
            raise NotImplementedError('Expr nodes must have a matcher attribute')
        return GetSource(self.node, parent_node=unused_node)

    def _is_semantic_equivalent_strings(self, original_string, matched_string, stripped_matched, stripped_original):
        if stripped_original == '' or stripped_matched == '':
            raise ValueError("stripped_original and stripped_matched should not be empty")
        original_quote = original_string[0]
        matched_quote = stripped_matched[0]
        if matched_quote == original_quote:
            raise ValueError('we should not get here')
        len_macthed = len(matched_string)
        if original_quote not in ["'", "\""]:
            return False
        if original_quote == "\"\"\"":
            raise NotImplementedError('support for \"\"\" yet to be implemented')
        if original_quote != stripped_original[0]:
            raise ValueError("mismatched start quote")
        if original_quote == matched_string[0] or original_quote == matched_string[-1]:
            raise ValueError("mismatched quotes -- why did we get BadlySpecifiedTemplateError?")
        return True

    def _handle_semantic_equivalent_float(self, e, node_source, original_source):
        if not isinstance(self.parent, ast.Constant):
            raise e

        scientific_notation = re.match(r'^[0-9]*\.?[0-9]+[eE][+-]?[0-9]+', original_source)
        if scientific_notation:
            str_from_source = scientific_notation.group(0)
            value_from_source = float(str_from_source)
            value_from_node_source = float(node_source)
            if value_from_source == value_from_node_source:
#                self.parent.node_matcher.num_matcher.matched = True
#                self.parent.node_matcher.num_matcher.matched_source = str_from_source
                self.parent.node_matcher.num_matcher.is_non_standard_scientific_notation = True
                self.parent.node_matcher.num_matcher.is_non_standard_scientific_text = str_from_source
                return str_from_source
            else:
                raise e
        else:
            raise e


