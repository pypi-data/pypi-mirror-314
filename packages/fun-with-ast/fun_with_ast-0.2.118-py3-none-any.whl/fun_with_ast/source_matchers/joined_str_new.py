import ast
import re
from string import Formatter

from fun_with_ast.get_source import GetSource
from fun_with_ast.manipulate_node.call_args_node import CallArgs
from fun_with_ast.manipulate_node.get_node_from_input import GetNodeFromInput
from fun_with_ast.manipulate_node.nodes_for_jstr import ConstantForJstr
from fun_with_ast.placeholders.base_match import MatchPlaceholder
from fun_with_ast.placeholders.node import NodePlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher
from fun_with_ast.source_matchers.joined_str_config import SUPPORTED_QUOTES, JstrConfig, MARKER_FOR_JSTR_STRING_LITERAL
from fun_with_ast.source_matchers.matcher_resolver import GetDynamicMatcher


class JoinedStrSourceMatcherNew(DefaultSourceMatcher):
    MAX_LINES_IN_JSTR = 10
    def __init__(self, node, starting_parens=None, parent=None):
        expected_parts = [
            TextPlaceholder(r'[ \t]*(f"""|f["\'])', 'f\''),
         TextPlaceholder(r'(\"\"\"|[\'\"])', '\'')
     ]
        super(JoinedStrSourceMatcherNew, self).__init__(
            node, expected_parts, starting_parens)
        self.padding_quote = None
        self.jstr_meta_data = []
        self.jstr_in_call_args = False


    def _match(self, string):
        remaining_string = self.MatchStartParens(string)
        self._split_jstr_into_lines(remaining_string)
        source = ''

        if len(self.jstr_meta_data) > 1: # this is multi line jstr
            self._mark_node_values_as_potentially_matched()
            for index, line in enumerate(self.jstr_meta_data):
                string_to_match = line.full_jstr_including_prefix
                if index != len(self.jstr_meta_data)-1:
                    string_to_match += "\n"
                one_line_node = GetNodeFromInput(string_to_match.removeprefix(line.prefix_str))
                matcher = GetDynamicMatcher(one_line_node)
                matched_line_text = matcher._match(string_to_match)
                matcher.matched_source = matched_line_text
                source += matched_line_text
                self.expected_parts.insert(index + 1, NodePlaceholder(one_line_node))
            self.expected_parts.pop(0)
            self.expected_parts.pop()
            remaining_string = remaining_string[len(source):]
            self._conclude_jstr_match(remaining_string)

        elif len(self.jstr_meta_data) == 1:
            source =  self._match_single_line_jstr(remaining_string,0)
        return source

    def _match_single_line_jstr(self, string, index):
        remaining_string = MatchPlaceholder(string, self.node, self.expected_parts[0])
        format_string = self._get_format_string(index)
        format_parts = self._get_format_parts(format_string)
        format_string_source = self._match_format_parts(format_parts)
        self.matched = False  # ugly hack to force the next line to work
        self.matched_source = None
        remaining_string = remaining_string[len(format_string_source):]
        remaining_string = MatchPlaceholder(remaining_string, self.node, self.expected_parts[-1])
        return self._conclude_jstr_match( remaining_string)

    def _conclude_jstr_match(self, remaining_string):
        remaining_string = self.MatchEndParen(remaining_string)

        self._conclude_match(remaining_string)
        matched_source = self.GetSource()
        self.matched = True
        self.matched_source = matched_source
        return matched_source

    def _get_format_string(self, index):
        config = self.jstr_meta_data[index]
        format_string = config.format_string
        return format_string

    def _get_format_parts(self, format_string):
        format_parts = list(Formatter().parse(format_string))
        if '{{' in format_string:
            mew_parts = []
            self._consolidate_parts(format_parts, new_parts=mew_parts)
            return  mew_parts
        # handling fomated string with '='
        self._handle_equal_literal_in_formatted_value(format_parts)
        return format_parts

    def _handle_equal_literal_in_formatted_value(self, format_parts):
        new_parts = []
        literal_found = 0
        for index, part in enumerate(format_parts):
            if part[1] and part[1].endswith('=') and part[2] == '':
                const_part = MARKER_FOR_JSTR_STRING_LITERAL + part[0] + '{' + part[1] + '}'
                name_part = None
                new_parts.append((index, (const_part, name_part, part[2], part[3])))
                del self.node.values[index + 1]
                literal_found += 1
        if new_parts == []:
            return
        for new_part in new_parts:
            format_parts[new_part[0]] = new_part[1]
        if len(format_parts) > 1:
            self._consolidate_parts(format_parts, new_parts=new_parts)
        return format_parts
    def _get_quote_type(self):
        return self.jstr_meta_data[0].quote_type

    def _split_jstr_into_lines(self, orig_string):
        quote_type = self._determine_quote_type(orig_string)
        if quote_type == '"""':
            lines = [orig_string]
        else:
            lines = self._split_into_syntactic_lines(orig_string)
        jstr_lines = []


        for index, line in enumerate(lines):
            if self._is_jstr(line, index, quote_type):
                jstr_lines.append(line)
            else:
                break
        if len(jstr_lines) >= self.MAX_LINES_IN_JSTR-1:
            raise ValueError('too many lines in jstr string')
        self._update_jstr_meta_data_based_on_context(jstr_lines, lines)

    def _split_into_syntactic_lines(self, orig_string):
        if isinstance(self.node.parent_node, ast.Dict):
            lines = re.split(r'[\n:]', orig_string, maxsplit=self.MAX_LINES_IN_JSTR * 2)
            if 'http' in lines[0]:
                full_http_string = lines[0] + ':' +lines[1]
                lines = [full_http_string] + lines[2:]
        elif isinstance(self.node.parent_node, (ast.List, ast.Tuple, CallArgs)):
            lines = self._identify_jstr_in_compound_structure(orig_string)
        else:
            lines = orig_string.split('\n', self.MAX_LINES_IN_JSTR)
        return lines

    def _identify_jstr_in_compound_structure(self, orig_string):
        lines = orig_string.split('\n', self.MAX_LINES_IN_JSTR * 2)
        for index, line in enumerate(lines):
            match = re.search(r'[ \t]*,\s*$', line)
            if match:
                lines[index] = line[:match.start()]
                lines = lines[:index + 1]
                break
        if isinstance(self.node.parent_node, CallArgs):
            self.jstr_in_call_args = True
        return lines

    def _determine_quote_type(self, orig_string):
        quote_type = None
        for quote in SUPPORTED_QUOTES:
            if re.match(r'[ \t]*f?' + quote, orig_string):
                quote_type = quote
                break
        assert quote_type is not None
        return quote_type
    # not clear why we need this fucntion below
    def _update_jstr_meta_data_based_on_context(self, jstr_lines, lines): # this function mostly for debugging purposes
        if len(jstr_lines) == 0:
            raise ValueError('could not find jstr lines')
        if len(jstr_lines) == 1: # simple case
            self.__append_jstr_lines_to_metadata(jstr_lines)
            return

        last_jstr_line = jstr_lines[len(jstr_lines)-1]
        len_jstr_lines = len(jstr_lines)
        if re.search(r'[ \t]*\)[ \t]*$', last_jstr_line): # this is call_args context
            self.__append_jstr_lines_to_metadata(jstr_lines)      # closing ')' at the end of a line
            return
        elif len_jstr_lines < len(lines)  and re.match(r'[ \t\n]*\)', lines[len_jstr_lines]):
            self.__append_jstr_lines_to_metadata(jstr_lines) # this is call_args context - single ')'
            return                                          # at separate line
        elif self.jstr_in_call_args :
#        elif re.search(r'[ \t]*\)[ \t]*#.*$', last_jstr_line):  # this is call_args context
            self.__append_jstr_lines_to_metadata(jstr_lines)            # ')' and a following comment
            return
        # elif re.search(r'[ \t]*\)[ \t]*from.*$', last_jstr_line):  # this is raise context
        #     if not self.jstr_in_call_args:
        #         raise ValueError('not in call_args context')
        #     self.__append_jstr_lines_to_metadata(jstr_lines)
        # elif re.search(r'[ \t]*\'.*?\':[ \t]*\'.*\'[ \t]*\}', last_jstr_line): # dict context
        #     self.__append_jstr_lines_to_metadata(jstr_lines)
        else:
            raise ValueError("Not supported - jstr string not in call_args context ")

    def __append_jstr_lines_to_metadata(self, jstr_lines):
        for line_index, line in enumerate(jstr_lines):
            self.jstr_meta_data.append(JstrConfig(line, line_index))

    def _is_jstr(self, line, line_index, quote_type):
        # TODO: this is really ugly -- we simply need to build a parser that identifies the end of the f string
        if line_index > 0 and isinstance(self.node.parent_node, (ast.Dict, ast.List, ast.Tuple)):
            return False # we assume that the dict/list has only one-liners as jstr
        if line_index > 0 and isinstance(self.node.parent_node, CallArgs):
            call_node = self.node.parent_node.parent_node.parent_node
            if isinstance(call_node, ast.Dict):
                return False
        if line_index == 0 and quote_type == '"""':
            return True
        for quote in SUPPORTED_QUOTES:
            expr = r'^[ \t]*f?' + quote
            match = re.match(expr, line)
            if match:
                return True
        if quote_type == '"""' and '{' not in line:
            return True
        return False

    def _match_format_parts(self, format_parts):
         format_string = ''
         index_in_jstr_values = 0
         for part in format_parts:
             literal_part = part[0]
             conversion_part = part[3]
             field_name_part = part[1:3]
             format_string_literal = format_string_field_name = ''
             if literal_part:
                format_string_literal = self._handle_jstr_constant(index_in_jstr_values, literal_part)
                index_in_jstr_values += 1
             if field_name_part[0] is not None:
                format_string_field_name = self._handle_jstr_field_name(index_in_jstr_values,
                                                                        conversion_part, field_name_part)
                #if not literal_part:
                index_in_jstr_values += 1
             format_string += format_string_literal + format_string_field_name
         return format_string
    def _handle_jstr_field_name(self, index, conversion, field_name_part):
        format_value_node = self.node.values[index]
        if not isinstance(format_value_node, ast.FormattedValue):
            raise ValueError('value node is not FormattedValue')
        value_node = format_value_node.value

        stripped_format  = GetSource(value_node, text=field_name_part[0])
        ws_parts = field_name_part[0].split(stripped_format)
        if len(ws_parts) == 1:
            stripped_format = self._fix_quotes_in_format_string(stripped_format, field_name_part[0])
            ws_parts = ["",""]
        elif len(ws_parts) != 2:
            raise ValueError('none whitespace in format string')

        stripped_format = ws_parts[0] + stripped_format + ws_parts[1]
        if stripped_format != field_name_part[0]:
            raise ValueError('format string does not match')
        if conversion:
            stripped_format = stripped_format + "!"+ conversion
        matcher = GetDynamicMatcher(format_value_node)
        format_string = "{" + stripped_format + "}"
        matched_string = matcher._match(format_string)

        self.expected_parts.insert(index + 1, NodePlaceholder(format_value_node))
        return format_string

    def _handle_jstr_constant(self, index, format_part_source):
        constant_node = self.node.values[index]
        value = constant_node.value
        constant_node_for_jstr = ConstantForJstr(value)
        constant_node_for_jstr.default_quote = self._get_quote_type()
        matcher = GetDynamicMatcher(constant_node_for_jstr)
        matched_string = matcher._match(format_part_source)
        self.node.values[index] = constant_node_for_jstr
        self.expected_parts.insert(index + 1, NodePlaceholder(constant_node_for_jstr))
        return matched_string

    def _mark_node_values_as_potentially_matched(self):
        for node in self.node.values:
            if isinstance(node, ast.FormattedValue):
                for child in ast.walk(node):
                    child.no_matchers_ok = True
            node.no_matchers_ok = True

    def _fix_quotes_in_format_string(self, matched_text, original):
        if len(matched_text) != len(original):
            raise ValueError('cannot fix quotes on different lengths of string')
        result = matched_text.replace("\"", "'")
        if result != original:
            raise ValueError('cannot fix quotes')
        return result

    def _is_escape_string(self, source_from_format, matched_string):
        with_escape = matched_string.replace("\n", "\\n")
        if with_escape == source_from_format:
            return True
        return False

    def _consolidate_parts(self, format_parts, new_parts=[]):
        if not format_parts:
            return
        if len(format_parts) == 1:
            part_1 = format_parts[0]
            part_0 = new_parts[-1]
            if part_0[0] and not part_0[1]:
                if part_1[0]:
                    new_part = self._merge_parts(part_0, part_1)
                    new_parts[-1] = new_part
                    return
        part_0  = format_parts[0]
        part_1 = format_parts[1]
        if part_0[0] and not part_0[1]:
            if part_1[0]:
                new_part = self._merge_parts(part_0, part_1)
                new_parts.append(new_part)
                self._consolidate_parts(format_parts[2:], new_parts)
    def _merge_parts(self, part_0, part_1):
        return (part_0[0] + part_1[0], part_1[1], None, None)
