from fun_with_ast.common_utils.utils_source_match import _FindQuoteEnd
from fun_with_ast.placeholders.base_placeholder import Placeholder
from fun_with_ast.placeholders.string_parser import StringParser
from fun_with_ast.placeholders.text import TextPlaceholder


class StringPartPlaceholder(Placeholder):
    """A container object for a single string part.

    Because of implicit concatination, a single _ast.Str node might have
    multiple parts.
    """

    def __init__(self, accept_multiparts_string=True):
        super(StringPartPlaceholder, self).__init__()
        self.prefix_placeholder = TextPlaceholder(r'ur|uR|Ur|UR|u|r|U|R|', '')
        self.quote_match_placeholder = TextPlaceholder(r'"""|\'\'\'|"|\'')
        self.inner_text_placeholder = TextPlaceholder(r'.*', '')
        self.accept_multiparts_string = accept_multiparts_string

    def _match(self, node, string):
        elements = self._get_elements()
        remaining_string = StringParser(string, elements, accept_multiparts_string=self.accept_multiparts_string).remaining_string

        remaining_string = self._match_inner_string_part(remaining_string, string)
        if not remaining_string:
            return string
        result = string[:-len(remaining_string)]
        return result

    def _match_inner_string_part(self, remaining_string, string):

#        if not self.accept_multiparts_string:
#            return remaining_string
        quote_type = self.quote_match_placeholder.matched_text
        end_index = _FindQuoteEnd(remaining_string, quote_type)
        if end_index == -1:
            raise ValueError('String {} does not end properly'.format(string))
        match_inner_string = remaining_string[:end_index]
        self.inner_text_placeholder._match(None, match_inner_string, dotall=True)
        remaining_string = remaining_string[end_index + len(quote_type):]
        return remaining_string

    def _get_elements(self):
        elements = [self.prefix_placeholder, self.quote_match_placeholder]
        return elements

    def GetSource(self, node):
        placeholder_list = [self.prefix_placeholder,
                            self.quote_match_placeholder,
                            self.inner_text_placeholder,
                            self.quote_match_placeholder]
        source_list = [p.GetSource(node) for p in placeholder_list]
        return ''.join(source_list)

class JoinedStringPartPlaceholder(StringPartPlaceholder):

    def __init__(self):
        super(JoinedStringPartPlaceholder, self).__init__()
        self.join_str_prefix_placeholder = TextPlaceholder(r'f', 'f')


    def _get_elements(self):
        elements = [self.join_str_prefix_placeholder, self.quote_match_placeholder]
        return elements

