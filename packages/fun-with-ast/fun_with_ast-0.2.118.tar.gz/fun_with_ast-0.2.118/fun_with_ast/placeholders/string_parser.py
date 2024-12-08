
from fun_with_ast.get_source import GetSource
from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.placeholders.text import StartParenMatcher
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


def StripStartParens(string):
    remaining_string = string
    while remaining_string.startswith('('):
        matcher = StartParenMatcher()
        matched_text = matcher._match(None, remaining_string)
        remaining_string = remaining_string[len(matched_text):]
    return remaining_string

class StringParser(object):
    """Class encapsulating parsing a string while matching placeholders."""

    def __init__(self, string, elements, starting_parens=None, accept_multiparts_string=True):
        if not starting_parens:
            starting_parens = []
        self.starting_parens = starting_parens
        self.string = string
        self.before_string = None
        self.remaining_string = string
        self.elements = elements
        self.matched_substrings = []
        self.accept_multiparts_string = accept_multiparts_string
        self.Parse()

    def _ProcessSubstring(self, substring):
        """Process a substring, validating its state and calculating remaining."""
        if not substring:
            return
        split_start = 1
        stripped_substring = StripStartParens(substring)
        stripped_remaining = StripStartParens(self.remaining_string)
        if not stripped_remaining.startswith(stripped_substring):
            raise BadlySpecifiedTemplateError(
                'string: \n"{}"\nshould be in string: \n"{}"'
                    .format(stripped_substring, stripped_remaining))
        if stripped_substring == '' and substring == '(':
            self.remaining_string = stripped_remaining
        else:
            self.remaining_string = self.remaining_string.split(stripped_substring, 1)[1]
    def _MatchTextPlaceholder(self, element):
        if self.remaining_string == self.string:
            element.SetStartingParens(self.starting_parens)
        matched_text = element._match(None, self.remaining_string)
        self._ProcessSubstring(matched_text)
        self.matched_substrings.append(matched_text)

    def _MatchNode(self, node):
        starting_parens = []
        if self.remaining_string == self.string:
            starting_parens = self.starting_parens
        node_src = GetSource(node, self.remaining_string, starting_parens)
        self._ProcessSubstring(node_src)
        self.matched_substrings.append(node_src)

    def GetMatchedText(self):
        return ''.join(self.matched_substrings)

    def Parse(self):
        """Parses the string, handling nodes and TextPlaceholders."""
        for index, element in enumerate(self.elements):
            if isinstance(element, Placeholder):
                self._MatchTextPlaceholder(element)
            else:
                self._MatchNode(element)
        return
