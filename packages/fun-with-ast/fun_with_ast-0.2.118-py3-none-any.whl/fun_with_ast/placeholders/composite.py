import _ast
import ast
from types import NoneType

from fun_with_ast.manipulate_node.syntax_free_line_node import SyntaxFreeLine
from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.placeholders.node import NodePlaceholder
from fun_with_ast.placeholders.string_parser import StringParser
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class CompositePlaceholder(Placeholder):

    """Node which wraps one or more other nodes."""

    def _match(self, node, string):
        """Makes sure node.(self.field_name) is in string."""
        self.Validate(node)
        elements = self.GetElements(node)
        elements = self._set_parents(elements, node)
        parser = StringParser(
            string, elements, starting_parens=self.starting_parens)
        matched_text = parser.GetMatchedText()
        return matched_text

    def _set_parents(self, elements, node):
        if isinstance(node, ast.Constant):
            if not isinstance(node.s, int) and not isinstance(node.s, NoneType):
                if not hasattr(node, 'default_quote'):
                    raise ValueError('Constant nodes must of type string must have a default_quote attribute')
        for element in elements:
            element.parent = node
        return elements

    def GetSource(self, node):
        source = ''
        elements = self.GetElements(node)
        for element in elements:
            source += element.GetSource(node)
        return source
    def Validate(self, unused_node):
        return True


class FieldPlaceholder(CompositePlaceholder):
    """Placeholder for a field."""

    def __init__(
            self, field_name, before_placeholder=None, after_placeholder=None):
        super(FieldPlaceholder, self).__init__()
        self.field_name = field_name
        self.before_placeholder = before_placeholder
        self.after_placeholder = after_placeholder

    def GetElements(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        else:
            field_value = getattr(node, self.field_name)

        if not self._isNoneLiteral(field_value, node):
            return []

        elements = []
        if self.before_placeholder:
            elements.append(self.before_placeholder)
        elements.append(NodePlaceholder(field_value))
        if self.after_placeholder:
            elements.append(self.after_placeholder)

        return elements

    def _match(self, node, string):
        return super(FieldPlaceholder, self)._match(node, string)

    def Validate(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        else:
            field_value = getattr(node, self.field_name)
        if isinstance(field_value, (list, tuple)):
            raise BadlySpecifiedTemplateError(
                'Field {} of node {} is a list. please use a ListFieldPlaceholder'
                'instead of a FieldPlaceholder'.format(self.field_name, node))

    def __repr__(self):
        return 'FieldPlaceholder for field "{}"'.format(
            self.field_name)

    def _isNoneLiteral(self, field_value, node):
        if (self.field_name == 'vararg' and field_value == None and
                isinstance(node, _ast.arguments) and node.kwonlyargs):
            return True # see test testArgsWithVarargsAndKwonlyargs
        # TODO: this seems like a hack to identify None in source code as opposed to None in the AST
        if not field_value and field_value != 0:
            if isinstance(node, SyntaxFreeLine) and field_value == '':
                return False
            elif isinstance(node, (ast.arguments, ast.Call, ast.withitem,   ast.alias,
                                   ast.Slice, ast.excepthandler, ast.Assert)):
                return False
            elif isinstance(node, ast.Constant) and field_value is not None:
                raise ValueError('None field value for non constant node')
        return True

