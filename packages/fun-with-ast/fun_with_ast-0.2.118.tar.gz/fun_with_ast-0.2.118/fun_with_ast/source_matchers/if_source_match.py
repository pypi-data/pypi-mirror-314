import _ast

from fun_with_ast.get_source import GetSource
from fun_with_ast.manipulate_node.syntax_free_line_node import SyntaxFreeLine
from fun_with_ast.placeholders.base_match import MatchPlaceholder, MatchPlaceholderList
from fun_with_ast.placeholders.composite import FieldPlaceholder
from fun_with_ast.placeholders.list_placeholder import ListFieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher
from fun_with_ast.source_matchers.body import BodyPlaceholder


class IfSourceMatcher(SourceMatcher):
    """Class to generate the source for an _ast.If node."""

    def __init__(self, node, starting_parens=None, parent=None):
        super(IfSourceMatcher, self).__init__(node, starting_parens)
        self.if_placeholder = TextPlaceholder(r' *if\s*', 'if ')
        self.test_placeholder = FieldPlaceholder('test')
        self.if_colon_placeholder = TextPlaceholder(r'[ \t]*:[ \t]*\n', ':\n')
        self.body_placeholder = BodyPlaceholder('body')
        self.else_placeholder = TextPlaceholder(r' *else:[ \t]*\n', 'else:\n')
        self.orelse_placeholder = BodyPlaceholder('orelse')
        self.is_elif = False
        self.if_indent = 0

    def _match(self, string):
        self.if_indent = len(string) - len(string.lstrip())
        placeholder_list = self.expected_parts
        remaining_string = MatchPlaceholderList(
            string, self.node, placeholder_list)
        if not self.node.orelse:
            return self._return_from_match()
        else:
            remaining_string = self._match_orelse(remaining_string)
            remaining_string = self.orelse_placeholder._match(
                self.node, remaining_string)
            if not remaining_string:
                raise ValueError('Can we get here?')
            return self._return_from_match()

    def _return_from_match(self):
        result = IfSourceMatcher.GetSource(self)
        self.matched = True
        self.matched_source = result
        return result

    def _match_orelse(self, remaining_string):
        # Handles the case of a blank line before an elif/else statement
        # Can't pass the "match_after" kwarg to self.body_placeholder,
        # because we don't want to match after if we don't have an else.
        self.validated_call_to_match()
        if self.matched:
            return self.matched_source

        while SyntaxFreeLine.is_syntaxfree_line(remaining_string):
            remaining_string, syntax_free_node = (
                self.body_placeholder.MatchSyntaxFreeLine(remaining_string))
            self.node.body.append(syntax_free_node)
        if remaining_string.lstrip().startswith('elif'):
            self.is_elif = True #TODO -- note that we set to True the parent node and not the current node
                                # (the elif). This is confusing and need to be fixed
            indent = len(remaining_string) - len(remaining_string.lstrip())
            remaining_string = (remaining_string[:indent] +
                                remaining_string[indent + 2:])
            # This is a hack to handle the fact that elif is a special case
            # BodyPlaceholder uses the indent of the other child statements
            # to match SyntaxFreeLines, which breaks in this case, because the
            # child isn't indented
            self.orelse_placeholder = ListFieldPlaceholder('orelse')
        else:
            remaining_string = MatchPlaceholder(
                remaining_string, self.node, self.else_placeholder)
        return remaining_string

    @property
    def expected_parts(self):
        return  [self.if_placeholder,
                            self.test_placeholder,
                            self.if_colon_placeholder,
                            self.body_placeholder]

    def GetSource(self):
        placeholder_list = self.expected_parts
        source_list = [p.GetSource(self.node) for p in placeholder_list]
        if not self.node.orelse:
            return ''.join(source_list)
        if (len(self.node.orelse) == 1 and
                isinstance(self.node.orelse[0], _ast.If) and
                self.is_elif):
            elif_source = GetSource(self.node.orelse[0])
            indent = len(elif_source) - len(elif_source.lstrip())
            source_list.append(elif_source[:indent] + 'el' + elif_source[indent:])
        else:
            if self.else_placeholder:
                source_list.append(self.else_placeholder.GetSource(self.node))
            else:
                source_list.append(' ' * self.if_indent)
                source_list.append('else:\n')
            source_list.append(self.orelse_placeholder.GetSource(self.node))
        return ''.join(source_list)

    def add_newline_to_source(self):
        if not self.node.orelse:
            self.node.body[-1].node_matcher.add_newline_to_source()
        else:
            self.node.orelse[-1].node_matcher.add_newline_to_source()