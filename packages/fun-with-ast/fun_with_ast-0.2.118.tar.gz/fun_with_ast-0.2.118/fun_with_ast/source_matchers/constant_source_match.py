import ast
from types import NoneType

from fun_with_ast.placeholders.composite import FieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher
from fun_with_ast.source_matchers.str import StrSourceMatcher


class ConstantSourceMatcher(SourceMatcher):
    def __init__(self, node, starting_parens=None, parent_node=None):
        SourceMatcher.__init__(self, node)
        if not isinstance(node, ast.Constant):
            raise ValueError("Must be a Constant node")
        self.num_matcher = DefaultSourceMatcher(node, [
                                                       FieldPlaceholder('value'),
        ])
        self.num_matcher.is_non_standard_scientific_notation = False
        self.num_matcher.is_non_standard_scientific_text = None

        self.bool_matcher = DefaultSourceMatcher(node, [
                                                       FieldPlaceholder('value'),
                                                       TextPlaceholder(r'[ \t]*(#+.*)*?', '')])
        self.parent_node = parent_node
        if isinstance(self.parent_node, ast.JoinedStr):
            self.accept_multiparts_string = False
        else:
            self.accept_multiparts_string = True
        if isinstance(node.s, str):
            self.str_matcher = StrSourceMatcher(node, starting_parens, self.accept_multiparts_string)
        else:
            self.str_matcher = None

    def _match(self, string):
        if isinstance(self.node.n, bool):
            return self.bool_matcher._match(string)
        if isinstance(self.node.n, int) and isinstance(self.node.s, int):
            return self.num_matcher._match(string)
        if isinstance(self.node.n, float) and isinstance(self.node.s, float):
            return self.num_matcher._match(string)
        if isinstance(self.node.n, str) and isinstance(self.node.s, str):
            return self.str_matcher._match(string)
        if isinstance(self.node.n, NoneType) and isinstance(self.node.s, NoneType):
            return self.num_matcher._match(string)
        if self.node.n == Ellipsis:
            return self.num_matcher._match(string)
        if isinstance(self.node.n, complex) and isinstance(self.node.s, complex):
            return self.num_matcher._match(string)

        if isinstance(self.node.n, bytes) :
            raise NotImplementedError('bytes tye not supported yet')

        raise NotImplementedError(f'Unknown constant type: {type(self.node.n)}')

    def GetSource(self):
        self.validated_call_to_match()
        if self.matched:
            return self.matched_source
        if isinstance(self.node.n, bool) and isinstance(self.node.s, int):
            return self.bool_matcher.GetSource()
        if isinstance(self.node.n, int) and isinstance(self.node.s, int):
            return self.num_matcher.GetSource()
        if isinstance(self.node.n, NoneType) and isinstance(self.node.s, NoneType):
            return self.num_matcher.GetSource()
        if isinstance(self.node.n, float) and isinstance(self.node.s, float):
            return self.num_matcher.GetSource()
        if isinstance(self.node.n, str) and isinstance(self.node.s, str):
            return self.str_matcher.GetSource()
        if isinstance(self.node.n, complex) and isinstance(self.node.s, complex):
            return self.num_matcher.GetSource()

        raise NotImplementedError("cannot find get source for constant node")
