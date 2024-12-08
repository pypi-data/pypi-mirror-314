import _ast
import ast

from fun_with_ast.source_matchers.matcher_resolver import GetDynamicMatcher


def GetSource(field, text=None, starting_parens=None, assume_no_indent=False,
              parent_node=None, assume_elif=False):
    """Gets the source corresponding with a given field.

    If the node is not a string or a node with a .matcher function,
    this will get the matcher for the node, attach the matcher, and
    match the text provided. If no text is provided, it will rely on defaults.

    Args:
      field: {str|_ast.AST} The field we want the source from.
      text: {str} The text to match if a matcher doesn't exist.
      starting_parens: {[TextPlaceholder]} The list of parens that the field
          starts with.
      assume_no_indent: {bool} True if we can assume the node isn't indented.
          Used for things like new nodes that aren't yet in a module.

    Returns:
      A string, representing the source code for the node.

    Raises:
      ValueError: When passing in a stmt node that has no string or module_node.
          This is an error because we have no idea how much to indent it.
    """
    if field is None and isinstance(parent_node, ast.Constant):
        return 'None'
    if field is None:
        return ''
    if starting_parens is None:
        starting_parens = []
    if isinstance(field, str):
        return field
    if isinstance(field, bool):
        return str(field)
    if isinstance(field, int):
        return _str_from_int(field, parent_node, text)
    if isinstance(field, float):
        return _handle_non_standard_scientific_notation(field, parent_node)
    if isinstance(field, complex):
        return str(field)

    if isinstance(field, ast.Constant) and field.value == Ellipsis:
        return "..."

    if hasattr(field, 'node_matcher') and field.node_matcher:
        source = field.node_matcher.GetSource()
        return source
    else:
        field.node_matcher = GetDynamicMatcher(field, starting_parens, parent_node=parent_node)
        _match_text(assume_no_indent, field, text, parent_node)
        _set_elif(assume_elif, field)
        source_code = field.node_matcher.GetSource()
        return source_code


def _handle_non_standard_scientific_notation(field, parent_node):
    if parent_node.node_matcher.num_matcher.is_non_standard_scientific_notation:
        return parent_node.node_matcher.num_matcher.is_non_standard_scientific_text
    return str(field)


def _set_elif(assume_elif, field):
    if isinstance(field, _ast.If):
        if (assume_elif or (hasattr(field, 'is_alif') and field.is_alif)):
            field.matcher.is_elif = assume_elif


def _match_text(assume_no_indent, field, text, parent_node):
    if text:
        field.parent_node = parent_node
        field.node_matcher._match(text)
    elif isinstance(field, _ast.stmt) and not assume_no_indent:
#       if not hasattr(field, 'module_node'):
        if not isinstance(parent_node, ast.Module):
            raise ValueError(
                'No text was provided, and we try to get source from node {} which'
                'is a statement, so it must have a .module_node field defined. '
                'To add this automatically, call ast_annotate.AddBasicAnnotations'
                .format(field))


def _guess_base_from_string(string, field):
    if string.startswith('0x'):
        return 16
    if string.startswith('0b'):
        return 2
    if string.startswith('0o'):
        return 8
    return 10


def _str_from_int(field, parent_node, string):
    if parent_node is None:
        return str(field)
    if not isinstance(parent_node, (ast.Constant, ast.Assign)):
        raise ValueError('not a Constant node, not supported')
    if not hasattr(parent_node, 'base'):
        if string is not None:
            parent_node.base = _guess_base_from_string(string, field)
        else:
            return str(field)
    if parent_node.base == 2:
        return bin(field)
    if parent_node.base == 8:
        return oct(field)
    if parent_node.base == 16:
        return hex(field)
    return str(field)

