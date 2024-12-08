from fun_with_ast.source_matchers.constant_source_match import ConstantSourceMatcher
from fun_with_ast.source_matchers.joined_str_config import MARKER_FOR_JSTR_STRING_LITERAL


class ConstantJstrMatcher(ConstantSourceMatcher):
    def __init__(self, node, starting_parens=None, parent_node=None):
        ConstantSourceMatcher.__init__(self, node, starting_parens, parent_node)
        self.added_quote = '"'
    def _match(self, string):
        string_literal_marker = False
        if string.find('"') != -1 and self.node.n.find('"') != -1:
            self.added_quote = '\''
        if string.startswith(MARKER_FOR_JSTR_STRING_LITERAL):
            string = string.replace(MARKER_FOR_JSTR_STRING_LITERAL, '')
            self.node.s = self.node.n = self.node.value = string
        elif '{' in string or '}'  in string:
            string = string.replace('{', '{{').replace('}','}}')
            self.node.s = self.node.n = self.node.value = string
        string = self.added_quote + string + self.added_quote
        result = super(ConstantJstrMatcher, self)._match(string)
        result = self.GetSource()
        return result

    def GetSource(self):
        result = super(ConstantJstrMatcher, self).GetSource()
        if not (result.startswith('\'') or result.startswith('\"')):
            raise ValueError('ConstantJstrMatcher.GetSource does not start with \'')
        if not (result.endswith('\'') or result.endswith('\"')):
            raise ValueError('ConstantJstrMatcher.GetSource does not end with \'')
        result = result[1:-1]
        return result
