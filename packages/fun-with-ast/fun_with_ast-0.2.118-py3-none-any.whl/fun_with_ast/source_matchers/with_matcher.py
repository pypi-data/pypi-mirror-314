
from fun_with_ast.placeholders.list_placeholder import SeparatedListFieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.body import BodyPlaceholder
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher


class WithSourceMatcher(DefaultSourceMatcher):


    def __init__(self, node, starting_parens=None, Parent=None):
        super(WithSourceMatcher, self).__init__(node,  expected_parts=[
            TextPlaceholder(r' *(with)? *', 'with '),  # with
            SeparatedListFieldPlaceholder('items',
                                          before_separator_placeholder=TextPlaceholder(r', *', ', ')),
            TextPlaceholder(r':\n?', ':\n'),
            BodyPlaceholder('body')
        ])

