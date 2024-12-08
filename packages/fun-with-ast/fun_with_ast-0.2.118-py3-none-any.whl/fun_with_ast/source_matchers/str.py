import re

from fun_with_ast.common_utils.utils_source_match import _GetListDefault
from fun_with_ast.placeholders.base_match import MatchPlaceholder
from fun_with_ast.placeholders.string_part import StringPartPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.base_matcher import SourceMatcher
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class StrSourceMatcher(SourceMatcher):
    """Class to generate the source for an _ast.Str node."""
    def __init__(self, node, starting_parens=None, accept_multiparts_string=True):
        super(StrSourceMatcher, self).__init__(node, starting_parens)
        self.separator_placeholder = TextPlaceholder(r'([ \t]*)(#.*)*\n*[ \t]*', '', no_transform=True)
        self.quote_parts = []
        self.separators = []
        self.raw_string = False

        if  hasattr(node, 'default_quote'):
            self.quote_type = node.default_quote
        else:
            raise ValueError('node must have a default_quote attribute')
        self.original_quote_type = None
        self.original_s = None
        self.accept_multiparts_string=accept_multiparts_string

    def _GetMatchedInnerText(self):
        return ''.join(p.inner_text_placeholder.GetSource(self.node)
                       for p in self.quote_parts)

    def _match(self, string):
        self._set_raw_string(string)
        remaining_string = self.MatchStartParens(string)
        self._get_original_string()
        part = self._part_place_holder()
        remaining_string = MatchPlaceholder(remaining_string, None, part)
        self.quote_parts.append(part)

        remaining_string = self._handle_multipart(remaining_string)

        self.MatchEndParen(remaining_string)
        self.original_quote_type = (
            self.quote_parts[0].quote_match_placeholder.matched_text)
        parsed_string = self._match_parsed_string()
        result = StrSourceMatcher.GetSource(self)
        self.matched = True
        self.matched_source = result
        return result

    def _match_parsed_string(self):
        start_paran_text = self.GetStartParenText()
        end_paran_text = self.GetEndParenText()
        start_quote = self.original_quote_type
        end_quote = self.original_quote_type
        #        string_body = string[:-len(remaining_string)]
        string_body = ''
        for part in self.quote_parts:
            string_body +=   part.inner_text_placeholder.matched_text
#            string_body +=   part.quote_match_placeholder.matched_text + \ TODO: code for issue 79
#                            part.inner_text_placeholder.matched_text + \
#                            part.quote_match_placeholder.matched_text

        parsed_string = self._construct_parsed_string(end_paran_text, end_quote, start_paran_text, start_quote,
                                                      string_body)

        return parsed_string

    def _construct_parsed_string(self, end_paran_text, end_quote, start_paran_text, start_quote, string_body):
        if '\\' in string_body and self.raw_string == False:
            string_body = self.__handle_special_chars(string_body)
        if len(string_body) != len(self.original_s):
            raise BadlySpecifiedTemplateError(
                f'can happen in two cases:\n'
                f'1. Real mismatch (i.e., error) - between matched string and original string\n'
                f'2. Not Supported (i.e., false error) : matched string longer than original string\n'
                f'Can happen with two consecutive strings with new-line seperator between them.')

        parsed_string = start_paran_text + start_quote + string_body + end_quote + end_paran_text
        original_string = start_paran_text + start_quote + self.original_s + end_quote + end_paran_text
        if parsed_string != original_string:
                raise BadlySpecifiedTemplateError(f'Parsed body: {parsed_string} does not match node.s: {self.original_s}')
        return parsed_string

    def __handle_special_chars(self, string_body):
        if (not '\n' in self.original_s and
                not '\t' in self.original_s and
                not '\r' in self.original_s and
                not "\\\'" in string_body and
                not '\\' in string_body):
            raise NotImplementedError('special characters besides \\ or \\n or \\t in string body are not supported yet')
        else:
            clean_string = (
                            string_body.replace('\\n', '\n').
                            replace('\\\n', '\\n').
                            replace('\\t', '\t').
                            replace('\\r', '\r').
                            replace("\\\'","'").
                            replace("\\\\","\\")   # TODO: frankly this is a mess
                            )
            if clean_string != self.original_s:
                clean_string = clean_string.replace('\\"','"')
                if clean_string != self.original_s:
                    raise BadlySpecifiedTemplateError(
                    f'String body: {string_body} does not match node.s: {self.original_s}')
            string_body = clean_string
        return string_body

    def _handle_multipart(self, remaining_string):
        if not self.accept_multiparts_string:
            return remaining_string
        while True:
            separator = self.separator_placeholder.Copy()
            trial_string = MatchPlaceholder(remaining_string, None, separator)
            if (not re.match(r'r"|R"|"', trial_string) and
                    not re.match(r"r'|R'|'", trial_string)):
                break
            remaining_string = trial_string
            self.separators.append(separator)
            part = StringPartPlaceholder(self.accept_multiparts_string)
            remaining_string = MatchPlaceholder(remaining_string, None, part)
            self.quote_parts.append(part)
        return remaining_string

    def GetSource(self):
        # We try to preserve the formatting on a best-effort basis
        if self.original_s is not None and self.original_s != self.node.s:
            self.quote_parts = [self.quote_parts[0]]
            self.quote_parts[0].inner_text_placeholder.matched_text = self.node.s

        if self.original_s is None:
            if not self.quote_type:
               raise ValueError('quote_type must be set')
               #self.quote_type = self.original_quote_type or GetDefaultQuoteType()
            return self.quote_type + self.node.s + self.quote_type

        #if self.quote_type:
        #    for part in self.quote_parts:
        #        part.quote_match_placeholder.matched_text = self.quote_type

        source_list = [self.GetStartParenText()]
        source_list.append(_GetListDefault(
            self.quote_parts, 0, None).GetSource(None))
        for index in range(len(self.quote_parts[1:])):
            source_list.append(_GetListDefault(
                self.separators, index,
                self.separator_placeholder).GetSource(None))
            source_list.append(_GetListDefault(
                self.quote_parts, index + 1, None).GetSource(None))

        source_list.append(self.GetEndParenText())
        return ''.join(source_list)

    def _get_original_string(self):
        self.original_s = self.node.s

    def _part_place_holder(self):
        return StringPartPlaceholder(self.accept_multiparts_string)

    def _set_raw_string(self, string):
        match = re.match(r'[rR][\'"]', string)
        if match:
            self.raw_string = True
