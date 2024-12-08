import re

from fun_with_ast.manipulate_node.call_args_node import CallArgs
from fun_with_ast.placeholders.composite import CompositePlaceholder
from fun_with_ast.placeholders.list_placeholder import SeparatedListFieldPlaceholder
from fun_with_ast.placeholders.node import NodePlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.matcher_resolver import GetDynamicMatcher


class ArgsDefaultsPlaceholder(CompositePlaceholder):
    """Placeholder to handle args and defaults for _ast.argument.

    These fields behave differently than most other fields and therefore
    don't fall into any of the other placeholders. Therefore, we have to define
    a custom placeholder.
    """

    def __init__(self, arg_separator_placeholder, kwarg_separator_placeholder):
        super(ArgsDefaultsPlaceholder, self).__init__()
        self.arg_separator_placeholder = arg_separator_placeholder
        self.kwarg_separator_placeholder = kwarg_separator_placeholder
        self.arg_separators = []
        self.kwarg_separators = []

    def _GetArgSeparator(self, index):
        if index < len(self.arg_separators):
            return self.arg_separators[index]
        new_placeholder = self.arg_separator_placeholder.Copy()
        self.arg_separators.append(new_placeholder)
        return new_placeholder

    def _GetKwargSeparator(self, index):
        if index < len(self.kwarg_separators):
            return self.kwarg_separators[index]
        new_placeholder = self.kwarg_separator_placeholder.Copy()
        self.kwarg_separators.append(new_placeholder)
        return new_placeholder

    def _GetArgsKwargs(self, node):
        kwargs = list(zip(node.args[len(node.args) - len(node.defaults):], node.defaults))
        args = node.args[:-len(kwargs)] if kwargs else node.args
        
        return args, kwargs

    def GetElements(self, node):
        """Gets the basic elements of this composite placeholder."""
        args, kwargs = self._GetArgsKwargs(node)
        elements = []
        arg_index = 0
        kwarg_index = 0
        for index, arg in enumerate(args):
            elements.append(NodePlaceholder(arg))
            if index is not len(args) - 1 or kwargs:
                elements.append(self._GetArgSeparator(arg_index))
                arg_index += 1
        for index, (key, val) in enumerate(kwargs):
            elements.append(NodePlaceholder(key))
            elements.append(self._GetKwargSeparator(kwarg_index))
            kwarg_index += 1
            elements.append(NodePlaceholder(val))
            if index is not len(kwargs) - 1:
                elements.append(self._GetArgSeparator(arg_index))
                arg_index += 1
        return elements

    def __repr__(self):
        return ('ArgsDefaultsPlaceholder separating args with "{}" '
                'and kwargs with "{}" _id:{}'
                .format(self.arg_separator_placeholder,
                        self.kwarg_separator_placeholder, self._id))



class KeysValuesPlaceholder(ArgsDefaultsPlaceholder):

    def _GetArgsKwargs(self, node):
        return [], list(zip(node.keys, node.values))


class ArgsKeywordsPlaceholder(ArgsDefaultsPlaceholder):

    def __init__(self, arg_separator_placeholder, kwarg_separator_placeholder):
        super(ArgsKeywordsPlaceholder, self).__init__(
            arg_separator_placeholder, kwarg_separator_placeholder)
        self.stararg_separator = TextPlaceholder(r'\s*,?\s*\*', ', *')
        self.start_paren_matchers = []
        self.args_matcher = None
    def _match(self, node, string):
        default_matcher_result = self._use_default_matcher(node, string)
        return default_matcher_result
    def GetElements(self, node):
        if self.args_matcher:
            elements = []
            elements.extend(self.args_matcher.start_paren_matchers)
            elements.extend(self.args_matcher.expected_parts)
            elements.extend(self.args_matcher.end_paren_matchers)
            elements.extend(self.args_matcher.EOL_comment_matcher)
            elements.extend(self.args_matcher.end_whitespace_matchers)
            if self.args_matcher.EOL_matcher:
                elements.append(self.args_matcher.EOL_matcher)

            return elements
        elif not self.args_matcher:
            parts = self._get_parts_for_default_matcher(0, node, '')
            start_paren = TextPlaceholder(r'\(\s*', '(')
            end_paren = TextPlaceholder(r'\s*,?\s*\)', ')')
            parts.insert(0, start_paren)
            parts.append(end_paren)
            return parts
        else:
            raise ValueError('old implementation not supported anymore')

    def _use_default_matcher(self, node, string):
        arg_index = len(node.args)
        args_node = CallArgs(node.args, node.keywords, node)
        node.keywords = args_node.keywords # not nice
        parts = self._get_parts_for_default_matcher(arg_index, node, string)
        self.args_matcher = GetDynamicMatcher(args_node, parts_in=parts)
        self.args_matcher.EOL_matcher = None # args will not end with '\n' -- parent node will consume it

        matched_string = self.args_matcher._match(string)
        return matched_string

    def _get_parts_for_default_matcher(self, arg_index, node, string):
        parts = []
        args_seperator_placeholder = TextPlaceholder(r'(\s*,\s*)?([ \t]*#.*\n*[ \t]*)*', default='', no_transform=True )
        exclude_last_after = self._should_exclude_last_after(string)
        parts.append(SeparatedListFieldPlaceholder(r'args',
                                                    after__separator_placeholder=args_seperator_placeholder,
                                                    exclude_last_after=exclude_last_after))
        if node.keywords:
            if node.args:
                parts.append(args_seperator_placeholder)
            parts.append(SeparatedListFieldPlaceholder(r'keywords', after__separator_placeholder=args_seperator_placeholder,
                                                        exclude_last_after=exclude_last_after))
        if getattr(node, 'starargs', False):
            ValueError('This should not happen in python 3.10; starred args are part of args')
            parts.append(self.stararg_separator)
            parts.append(NodePlaceholder(node.starargs))
            if node.keywords:
                arg_seperator = self._GetArgSeparator(arg_index)
                parts.append(arg_seperator)
                arg_index += 1
            for index, arg in enumerate(node.keywords):
                parts.append(NodePlaceholder(arg))
                if index != len(node.keywords) - 1:
                    parts.append(self._GetArgSeparator(arg_index))
                    arg_index += 1
        return parts

    def _should_exclude_last_after(self, string):
        if string == '':
            return True
        parens_pairs = self._find_external_parens_of_args(string)
        if not parens_pairs:
            return True
        first_pair = parens_pairs[0]
        current_string = string[:first_pair[1]+1]
        if re.search(r'[ \t]*,[ \t\n]*\)$', current_string):
            return False
        if re.search(r'(\s*,\s*)?([ \t]*#.*\n*[ \t]*)', current_string):
            return False
        return  True

    def _find_external_parens_of_args(self, s): # from stack overflow
        toret = {}
        pstack = []

        for i, c in enumerate(s):
            if c == '(':
                pstack.append(i)
            elif c == ')':
                if len(pstack) == 0:
                    break
                toret[pstack.pop()] = i

        if len(pstack) > 0:
            to_return = self._ignore_parens_in_string_arguments(pstack, toret)
        result = [(x,y) for x,y in toret.items()]
        result.sort()
        return result

    # this method trying to address the following "foo('(')"
    # the problem is that the parens are not part of the args, but part of the string
    # so we need to ignore them
    # this method is not perfect, but it is good enough for now
    def _ignore_parens_in_string_arguments(self, pstack, to_return):
        result = {}
        if not pstack:
            raise ValueError("pstack must have at least one element")
        if pstack[0] != 0 and not to_return.get(0,None):
            raise ValueError("pstack should start with 0")
        elif pstack[0] != 0 and to_return.get(0,None):
            result[0] = to_return[0]
            return result
        if len(to_return) == 0 :
            raise ValueError("to_return should not be empty at this point")

        for i,(k,v) in enumerate(to_return.items()):
            if i == 0:
                result[0] = v
            else :
                result[k] = v
        return result

class OpsComparatorsPlaceholder(ArgsDefaultsPlaceholder):

    def _GetArgsKwargs(self, node):
        return [], list(zip(node.ops, node.comparators))

