import re

from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class TextPlaceholder(Placeholder):
    """Placeholder for text (non-field). For example, 'def (' in FunctionDef."""

    def __init__(self, regex, default=None, longest_match=False, no_transform=False):
        super(TextPlaceholder, self).__init__()
        self.no_transform = no_transform
        self.original_regex = regex
        self.regex = self._TransformRegex(regex)
        self.longest_match = longest_match
        if default is None:
            self.default = regex
        else:
            self.default = default
        self.matched_text = None

    def _TransformRegex(self, regex):
        if self.no_transform:
            return regex
        non_whitespace_parts = regex.split(r'\s*')
        regex = r'\s*(\\\s*|#.*\s*)*'.join(non_whitespace_parts)
        non_linebreak_parts = regex.split(r'\n')
        regex = r'( *#.*\n| *;| *\n)'.join(non_linebreak_parts)
        return regex

    def _match(self, unused_node, string, dotall=False):
        """Attempts to match string against self.regex.

        Saves the matched section for use in GetSource.

        Args:
          unused_node: unused.
          string: The string we attempt to match a substring of.
          dotall: Whether to apply re.DOTALL to the match.

        Raises:
          BadlySpecifiedTemplateError: If the regex doesn't match anywhere.

        Returns:
          The substring of string that matches.
        """
        longest_match_attempt = None
        if dotall:
            match_attempt = re.match(self.regex, string, re.DOTALL)
        elif self.longest_match:
            all_matches = re.findall(self.regex, string)
            longest_match_attempt = max(all_matches)
        else:
            match_attempt = re.match(self.regex, string)
            if not match_attempt:
                raise BadlySpecifiedTemplateError(
                    'string "{}" does not match regex "{}" (technically, "{}")'
                    .format(string, self.original_regex, self.regex))
        if longest_match_attempt:
            self.matched_text = longest_match_attempt
        else:
            self.matched_text = match_attempt.group(0)
        return self.matched_text

    def GetSource(self, unused_node):
        """Returns self.matched_text if it exists, or self.default otherwise."""
        if self.matched_text is None:
            return self.default
        return self.matched_text

    def Copy(self):
        return TextPlaceholder(self.regex, self.default, no_transform=self.no_transform)

    def __repr__(self):
        return 'TextPlaceholder with regex "{}" ("{}") and default "{}"'.format(
            self.original_regex, self.regex, self.default)

class StartParenMatcher(TextPlaceholder):
    def  __init__(self):
        super(StartParenMatcher, self).__init__(r'[ \t]*\(\s*', '')
class EndParenMatcher(TextPlaceholder):
    def  __init__(self):
        super(EndParenMatcher, self).__init__(r'[\s]*\)[ \t]*', '')


def GetStartParenMatcher():
    return TextPlaceholder(r'[ \t]*\(\s*', '')

def GetWhiteSpaceMatcher():
    return TextPlaceholder(r'[ \t]*', '')



