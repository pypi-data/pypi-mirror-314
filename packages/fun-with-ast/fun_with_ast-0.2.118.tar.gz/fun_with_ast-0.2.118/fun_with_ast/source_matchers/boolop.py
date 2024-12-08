from fun_with_ast.common_utils.utils_source_match import _GetListDefault
from fun_with_ast.get_source import GetSource
from fun_with_ast.placeholders.string_parser import StringParser
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher


class BoolOpSourceMatcher(SourceMatcher):
    """Class to generate the source for an _ast.BoolOp node."""

    def __init__(self, node, starting_parens=None, parent=None):
        super(BoolOpSourceMatcher, self).__init__(node, starting_parens)
        self.separator_placeholder = TextPlaceholder(r'\s*', ' ')
        self.matched_placeholders = []

    def GetSeparatorCopy(self):
        copy = self.separator_placeholder.Copy()
        self.matched_placeholders.append(copy)
        return copy

    def _match(self, string):
        remaining_string = self.MatchStartParens(string)

        elements = [self.node.values[0]]
        for value in self.node.values[1:]:
            elements.append(self.GetSeparatorCopy())
            elements.append(self.node.op)
            elements.append(self.GetSeparatorCopy())
            elements.append(value)

#        parser = StringParser(remaining_string, elements, self.start_paren_matchers)
        parser = StringParser(remaining_string, elements)
        matched_text = ''.join(parser.matched_substrings)
        remaining_string = parser.remaining_string

        self.MatchEndParen(remaining_string)
        result =  BoolOpSourceMatcher.GetSource(self)
        return result
    def GetSource(self):
        source_list = []
        source_list.append(self.GetStartParenText())

        source_list.append(GetSource(self.node.values[0]))
        index = 0
        for value in self.node.values[1:]:
            source_list.append(_GetListDefault(
                self.matched_placeholders,
                index,
                self.separator_placeholder).GetSource(None))
            source_list.append(GetSource(self.node.op))
            index += 1
            source_list.append(_GetListDefault(
                self.matched_placeholders,
                index,
                self.separator_placeholder).GetSource(None))
            source_list.append(GetSource(value))
            index += 1
        #if self.paren_wrapped:
        source_list.append(self.GetEndParenText())
        return ''.join(source_list)
