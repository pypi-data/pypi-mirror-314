from fun_with_ast.placeholders.base_match import MatchPlaceholderList
from fun_with_ast.placeholders.composite import FieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher


class WithItemSourceMatcher(SourceMatcher):
    def __init__(self, node, starting_parens=None, parent=None):
        super(WithItemSourceMatcher, self).__init__(node, starting_parens)
        self.context_expr = FieldPlaceholder('context_expr')
        self.optional_vars = FieldPlaceholder(
            'optional_vars',
            before_placeholder=TextPlaceholder(r' *as *', ' as '))


    def _match(self, string):
        #    if 'as' not in string:
        #      return MatchPlaceholder(string, self.node, self.context_expr)
        placeholder_list = [self.context_expr,
                            self.optional_vars]
        remaining_string = MatchPlaceholderList(
            string, self.node, placeholder_list)

        if not remaining_string:
            return string
        return string[:len(remaining_string)]

    def GetSource(self):
        source_list = []
        placeholder_list = [self.context_expr,
                            self.optional_vars]
        source_list = [p.GetSource(self.node) for p in placeholder_list]
        return ''.join(source_list)
