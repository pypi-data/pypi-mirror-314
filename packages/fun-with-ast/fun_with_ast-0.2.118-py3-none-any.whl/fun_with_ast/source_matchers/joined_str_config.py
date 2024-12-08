import re
from dataclasses import dataclass

SUPPORTED_QUOTES = ['"""', '\'', "\""] # order in list is import triple should go first
MARKER_FOR_JSTR_STRING_LITERAL = "xtFrg_" # marker for f-string WITH {a=1} in it

@dataclass
class JstrConfig:
    line_index: int
    orig_single_line_string: str
    prefix_str: str
    suffix_str: str
    f_part: str
    f_part_location: int
    format_string: str
    full_jstr_including_prefix: str
    end_quote_location: int
    start_quote_location: int
    quote_type: str
    jstr_length: int = 0
    f_part_type: str = 'not_set'
    conversion: str = ''
    def __init__(self, line, line_index):
        self.orig_single_line_string = line
        self._create_config(line_index)

    def _create_config(self, line_index):
        self.line_index = line_index
        self.suffix_str = ''
        self.prefix_str = ''
        self._set_quote_type()
        self._set_f_prefix()
        self._set_start_end_quotes()
        self.suffix_str = self.orig_single_line_string[self.end_quote_location+len(self.quote_type):]
        self.prefix_str = self.orig_single_line_string[:self.f_part_location]
        if self.prefix_str.strip() != '':
            raise ValueError('joined str string in which prefix is not white spaces')
        else:
            self.format_string = self.orig_single_line_string
        self.format_string = self.format_string.removesuffix(self.suffix_str)
        self.full_jstr_including_prefix = self.format_string
        if re.match(r'[ \t]+$', self.suffix_str):
            self.full_jstr_including_prefix += self.suffix_str
        self.format_string = self.format_string.removesuffix(self.quote_type)
        self.format_string = self.format_string.removeprefix(self.prefix_str+self.f_part)
        conversion = re.search(r"![ras]}", self.format_string)
        if conversion:
            self.conversion = conversion.group(0)[0:2]
        self.jstr_length = len(self.full_jstr_including_prefix)

    def _set_start_end_quotes(self):
        len_of_q = len(self.quote_type)
        start = self.orig_single_line_string.find(self.quote_type)
        end = self.orig_single_line_string[start+ len_of_q:].find(self.quote_type)
        end = self._check_for_escaped_quotes(end, start)
        self.end_quote_location = end + start + len_of_q
        self.start_quote_location = start
        if self.start_quote_location == self.end_quote_location:
            raise ValueError('joined str string in which start and end quote locations are the same')
        if self.end_quote_location == -len_of_q:
            raise ValueError('Could not find ending quote')

    def _check_for_escaped_quotes(self, end, start):
        rend = self.orig_single_line_string[start + 1:].rfind(self.quote_type)
        if end != rend:
            if self.orig_single_line_string[end+1] == '\\':
                end = rend
        return end

    def _set_quote_type(self):

        for quote in SUPPORTED_QUOTES:
             if re.match(r'[ \t]*f?'+quote, self.orig_single_line_string):
                self.quote_type = quote
                return
        raise ValueError("could not find quote in single line string")

    def _set_f_prefix(self):
        (f_type, location) = self._set_prefix_type()
        if f_type == 'f':
            self.f_part = self.orig_single_line_string[location:location+len(self.quote_type)+1]
            self.f_part_location = location
            self.f_part_type = 'f'
        elif f_type == 'quote_only':
            self.f_part = self.orig_single_line_string[location:location+1]
            self.f_part_location = location
            self.f_part_type = 'quote_only'
        else:
            raise ValueError('could not find f or quote at the beginning of string')

    def _set_prefix_type(self):
        f_type = self.orig_single_line_string.find("f"+self.quote_type)
        if f_type != -1:
            return ('f',f_type)
        f_type = self.orig_single_line_string.find(self.quote_type)
        if f_type != -1:
            return ('quote_only', f_type)
        raise ValueError("could not find quote of f+quote in single line string")


