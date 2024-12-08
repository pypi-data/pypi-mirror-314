import ast

from fun_with_ast.common_utils.parenthese_stack import ParanthesisStack
from fun_with_ast.placeholders.whitespace import WSStartOfLinePlaceholder, EOLCommentMatcher, EOLPlaceholder, \
    WSEndOfLinePlaceholder, WSEndOfFilePlaceholder
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class SourceMatcher(object):
    """Base class for all SourceMatcher objects.

    These are designed to match the source that corresponds to a given node.
    """
    parentheses_stack = ParanthesisStack()
    def __init__(self, node, stripped_parens=None):
        self.node = node
        self.EOL_comment_matcher = [EOLCommentMatcher()]
        self.EOL_matcher = EOLPlaceholder()
        self.end_paren_matchers = []
        self.start_whitespace_matchers =  [WSStartOfLinePlaceholder()]
        self.end_whitespace_matchers =  [WSEndOfLinePlaceholder(), WSEndOfFilePlaceholder()]
        self.paren_wrapped = False
        self.end_of_line_comment = '' #TODO: remove this use EOL_comment_matcher
        if not stripped_parens:
            stripped_parens = []
        self.start_paren_matchers = stripped_parens
        self.matched = False
        self.matched_source = None
        self.parentheses_stack_depth = self.parentheses_stack.size


    def do_match(self, string):
        self._check_balance_parentheses(string)
        SourceMatcher.parentheses_stack.reset()
        if self.node:
            self.node.parent_node = None
        result = self._match(string)
        if len(result) < len(string):
            self._validate_python_module(string)
        return result

    def _validate_python_module(self, string):
        try:
            ast.parse(string)
        except Exception:
            raise BadlySpecifiedTemplateError(f'string {string} is not valid python, unballaced parens?')


    def _match(self, string):
        raise NotImplementedError

    def GetSource(self):
        raise NotImplementedError


    def FixIndentation(self, new_ident):
        """Fix the indentation of the source."""
        current_ws = self.start_whitespace_matchers[0].matched_text
        if current_ws:
            current_ident = len(self.start_whitespace_matchers[0].matched_text)
            if current_ident == new_ident:
                return
        else:
            self.start_whitespace_matchers[0].matched_text = ' ' * new_ident
        self.matched = False
        self.matched_source = None
        self.node.col_offset = new_ident
        self.GetSource()


    def MatchStartParens(self, string, retrun=None):
        """Matches the starting parens in a string."""

        return self.parentheses_stack.MatchStartParens(self, string)

    def MatchEndParen(self, string):
        """Matches the ending parens in a string."""
        return self.parentheses_stack.MatchEndParens(self,string)


    # nice example for creating unit test
    def MatchCommentEOL(self, string):
        if string is None:
            return ''
        try:
            self.end_of_line_comment  = self.EOL_comment_matcher[0]._match(None, string)
            remaining_string = string[len(self.end_of_line_comment):]
        except BadlySpecifiedTemplateError:
            return string
        return remaining_string



    def GetStartParenText(self):
        result = ''
        for matcher in self.start_paren_matchers:
            result += matcher.GetSource(None)
        return result

    def GetWhiteSpaceText(self, in_matcher):
        result = ''
        if in_matcher:
            result = ''.join(matcher.GetSource(None)
                           for matcher in in_matcher)
        return result

    def GetEndParenText(self):
#        if self.paren_wrapped:
        return ''.join(matcher.GetSource(None)
                       for matcher in self.end_paren_matchers)
        return ''

    def add_newline_to_source(self):
        self.EOL_matcher.matched_text = '\n'
        self.matched_source = None
        self.matched = False
    def validated_call_to_match(self):
        if self.matched and self.matched_source is None:
            raise ValueError('Internal Error: matched_text must be set if is_matched is True')
        if not self.matched and self.matched_source is not None:
            raise ValueError('Internal Error: matched_text must be None if is_matched is False')
        if hasattr(self, 'matched_text'):
            raise ValueError('Internal Error: dont have this field - ever')

    def _check_balance_parentheses(self, string):
        left = right = 0
        for c in string:
            if c == '(':
                left += 1
            elif c == ')':
                right += 1

        if left != right:
            self._validate_python_module(string)

    def MatchNewLine(self, remaining_string):
        try:
            if self.EOL_matcher == None:
                return remaining_string
            match_nl = self.EOL_matcher._match(None, remaining_string)
        except BadlySpecifiedTemplateError:
            return remaining_string
        remaining_string = remaining_string[len(match_nl):]
        return remaining_string


