

import _ast

from fun_with_ast.placeholders.args import ArgsDefaultsPlaceholder, KeysValuesPlaceholder, ArgsKeywordsPlaceholder, \
    OpsComparatorsPlaceholder
# TODO: Consolidate with StringParser
from fun_with_ast.placeholders.base_match import MatchPlaceholder
from fun_with_ast.placeholders.composite import FieldPlaceholder
from fun_with_ast.placeholders.kwonlyargs import KwOnlyArgsPlaceholder
from fun_with_ast.placeholders.list_placeholder import ListFieldPlaceholder, SeparatedListFieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder, GetStartParenMatcher
from fun_with_ast.source_matchers.body import BodyPlaceholder
from fun_with_ast.source_matchers.boolop import BoolOpSourceMatcher
from fun_with_ast.source_matchers.constant_jstr_matcher import ConstantJstrMatcher
from fun_with_ast.source_matchers.constant_source_match import ConstantSourceMatcher
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher
from fun_with_ast.source_matchers.if_source_match import IfSourceMatcher
# from fun_with_ast.source_matchers.joined_str import JoinedStrSourceMatcher
from fun_with_ast.source_matchers.joined_str_new import JoinedStrSourceMatcherNew
from fun_with_ast.source_matchers.lambda_matcher import LambdaSourceMatcher
from fun_with_ast.source_matchers.syntaxfreeline import SyntaxFreeLineMatcher
from fun_with_ast.source_matchers.with_matcher import WithSourceMatcher
from fun_with_ast.source_matchers.withitem import WithItemSourceMatcher

REs= {
'comma_args_seperator': r'\s*,?[ \t\n]*(#+.*)?(\n[ \t]*)?'
}

class DummyNode(BoolOpSourceMatcher, IfSourceMatcher, WithSourceMatcher,
             JoinedStrSourceMatcherNew, ConstantJstrMatcher,
                 ConstantSourceMatcher, SyntaxFreeLineMatcher, WithItemSourceMatcher, LambdaSourceMatcher):
    """A dummy node that can be used for matching."""
    def __init__(self):
        pass


def StripStartParens(string):
    remaining_string = string
    while remaining_string.startswith('('):
        matcher = GetStartParenMatcher()
        matched_text = matcher._match(None, remaining_string)
        remaining_string = remaining_string[len(matched_text):]
    return remaining_string


# TODO: Add an indent placeholder that respects col_offset
def get_Add_expected_parts():
    return [TextPlaceholder(r'\+', '+')]


def get_FormattedValue_expected_parts():
    return [
        TextPlaceholder(r'\{', '{'),
        FieldPlaceholder('value'),
        TextPlaceholder(r"([\t ]*![asr])?[\t ]*}", default='}', longest_match=False)

    ]

def get_alias_expected_parts():
    return [
        FieldPlaceholder('name'),
        FieldPlaceholder(
            'asname',
            before_placeholder=TextPlaceholder(r' *as *', ' as ')),
        TextPlaceholder(r'([ \t]*(#+.*)*)*', '')  # this is the official end of line comment regex WITHOUT EOL
    ]


def get_And_expected_parts():
    return [TextPlaceholder(r'and')]


def get_arg_expected_parts():
    result = [FieldPlaceholder('arg'),
              TextPlaceholder(r'([ \t]*:[ \t]*)*', ''),
              FieldPlaceholder('annotation')
            ]
    return result
def get_LambdaArg_expected_parts():
    result = [FieldPlaceholder('arg'),
            ]
    return result


def get_arguments_expected_parts():
    return [ # note the ',?'. This is a hack to support tuples in the arguments. Tuples are 'eating' the comma
            # similar to issue 340
        ArgsDefaultsPlaceholder(
            TextPlaceholder(r'\s*,?\s*', ', ', no_transform=False),
            TextPlaceholder(r'\s*=\s*', '=', no_transform=True)),
        FieldPlaceholder(
            'vararg',
            before_placeholder=TextPlaceholder(r'\s*,?\s*\*\s*', ', *', no_transform=False),
            after_placeholder=TextPlaceholder(r'\s*,?\s*', ', ', no_transform=True)),
        KwOnlyArgsPlaceholder( # kwonlyargs
            TextPlaceholder(r'\s*,?\s*', ',', no_transform=False),
            TextPlaceholder(r'\s*=\s*', '=', no_transform=True)),
        FieldPlaceholder(
            'kwarg',
            before_placeholder=TextPlaceholder(r'\s*,?\s*\*\*\s*', ', **'))
    ]


def get_Await_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*await[ \t]+', 'await '),
        FieldPlaceholder('value'),
    ]

def get_Assert_expected_parts():
    return [
        TextPlaceholder(r' *assert *', 'assert '),
        FieldPlaceholder('test'),
        # the '?' is a hack to support tuple in the assert statement that is 'eating' the comma
        FieldPlaceholder(
            'msg', before_placeholder=TextPlaceholder(r',?[ \t]*', ', ')),
    ]
def get_Starred_expected_parts():
    return [
        TextPlaceholder(r'\*', '*'),
        FieldPlaceholder('value'),
    ]

def get_Assign_expected_parts():
    return [
        SeparatedListFieldPlaceholder('targets',
                                      after__separator_placeholder=TextPlaceholder(r'\s*=\s*', '=')),
        FieldPlaceholder('value'),
    ]
def get_NamedExpr_expected_parts():
    return [
        FieldPlaceholder('target'),
        TextPlaceholder(r'[ \t]*:=[ \t]*', ':='),
        FieldPlaceholder('value'),
    ]
def get_AnnAssign_expected_parts():
    return [
        FieldPlaceholder('target'),
        TextPlaceholder(r'\s*:', ': '),
        FieldPlaceholder('annotation'),
        TextPlaceholder(r'([ \t]*=[ \t]*)*', '='),
        FieldPlaceholder('value'),
        #TextPlaceholder(r'[ \t]*(#+.*)*\n?', '') # this is the official comment regex
    ]

def get_Attribute_expected_parts():
    return [
        FieldPlaceholder('value'),
        TextPlaceholder(r'\s*\.\s*', '.'),
        FieldPlaceholder('attr')
    ]


def get_AugAssign_expected_parts():
    return [
        FieldPlaceholder('target'),
        TextPlaceholder(r'[ \t]*', ' '),
        FieldPlaceholder('op'),
        TextPlaceholder(r'=[ \t]*', '='),
        FieldPlaceholder('value'),
    ]


# TODO: Handle parens better
def get_BinOp_expected_parts():
    return [
        FieldPlaceholder('left'),
        TextPlaceholder(r'\s*', ' '),
        FieldPlaceholder('op'),
        TextPlaceholder(r'\s*', ' '),
        FieldPlaceholder('right'),

    ]


def get_BitAnd_expected_parts():
    return [TextPlaceholder(r'&', '&')]


def get_BitOr_expected_parts():
    return [
        TextPlaceholder(r'\|', '|'),
    ]


def get_BitXor_expected_parts():
    return [
        TextPlaceholder(r'\^', '^'),
    ]


# TODO: Handle parens better


def get_Break_expected_parts():
    return [TextPlaceholder(r'[ \t]*break[ \t]*\n?', 'break\n')]


def get_Call_expected_parts():
    return [
        FieldPlaceholder('func'),
        ArgsKeywordsPlaceholder(
            TextPlaceholder(r'\s*,\s*', ', '),
            TextPlaceholder('')
        ),
    ]

def get_CallArgs_expected_parts():
    raise NotImplementedError('deprecated')


def get_ClassDef_expected_parts():
    return [
        ListFieldPlaceholder(
            'decorator_list',
            before_placeholder=TextPlaceholder('[ \t]*@', '@'),
            after_placeholder=TextPlaceholder(r'\n*', '')),
        TextPlaceholder(r'[ \t]*class[ \t]*', 'class '),
        FieldPlaceholder('name'),
        TextPlaceholder(r'\(?\s*', '('),
        SeparatedListFieldPlaceholder(
            'bases', TextPlaceholder(r'\s*,\s*', ', ')),
        TextPlaceholder(r'\s*,?\s*\)?:\n', '):\n'),
        BodyPlaceholder('body')
    ]


def get_Compare_expected_parts():
    return [
        FieldPlaceholder('left'),
        TextPlaceholder(r'\s*', ' '),
        OpsComparatorsPlaceholder(
            TextPlaceholder(r'\s*', ' '),
            TextPlaceholder(r'\s*', ' '))
    ]


def get_comprehension_expected_parts():
    return [
        TextPlaceholder(r'\s*for\s*', 'for '),
        FieldPlaceholder('target'),
        TextPlaceholder(r'\s*in\s*', ' in '),
        FieldPlaceholder('iter'),
        ListFieldPlaceholder(
            'ifs',
            before_placeholder=TextPlaceholder(r'\s*if\s*', ' if '))
    ]


def get_Continue_expected_parts():
    return [TextPlaceholder(r' *continue\n')]


def get_Delete_expected_parts():
    return [
        TextPlaceholder(r' *del *'),
        ListFieldPlaceholder('targets', after_placeholder= TextPlaceholder('[ \t]*,[ \t]*', ', '), exclude_last_after=True),
        #TextPlaceholder(r'\n*', ''),
    ]


def get_Dict_expected_parts():
    return [
        TextPlaceholder(r'\s*{\s*', '{'),
        KeysValuesPlaceholder(
            # this is the seperator between key:value pairs
            # note that the '?' might allow incorrect syntax like {"key1":(1,2,) "key2":(3,4)} --
            # see test_Dict_TupleAfterTuple_1_1 -- but the assumption is that we do get valid python
            TextPlaceholder(REs['comma_args_seperator'], ',', no_transform=True),
            #This is the key:value pair
            TextPlaceholder(r'(\*\*\s*)|(\s*:\s*)', ': ', no_transform=True)),
        #last value?
        TextPlaceholder(r'\s*,?\s*}', '}')
    ]


def get_Div_expected_parts():
    return [
        TextPlaceholder(r'/', '/'),
    ]


# TODO: Handle both types of k/v syntax
def get_DictComp_expected_parts():
    return [
        TextPlaceholder(r'\{\s*', '{'),
        FieldPlaceholder('key'),
        TextPlaceholder(r'\s*:\s*', ': '),
        FieldPlaceholder('value'),
        TextPlaceholder(r' *', ' '),
        ListFieldPlaceholder('generators'),
        TextPlaceholder(r'\s*\}', '}'),
    ]


def get_Eq_expected_parts():
    return [TextPlaceholder(r'==', '==')]


def get_ExceptHandler_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*except:?[ \t]*', 'except '),
        FieldPlaceholder('type'),
        FieldPlaceholder(
            'name',
            before_placeholder=TextPlaceholder(r' *as *| *, *', ' as ')),
        TextPlaceholder(r'[ \t]*:?[ \t]*\n', ':\n'),
        BodyPlaceholder('body')
    ]


def get_Expr_expected_parts():
    return [
        TextPlaceholder(r' *', ''),
        FieldPlaceholder('value'),
        #TextPlaceholder(r'([ \t]*(#+.*)*\n?)', '') # this is the official comment regex
        TextPlaceholder(r'([ \t]*(#+.*)*\n)*', '')  # this is the official comment regex
    ]


def get_FloorDiv_expected_parts():
    return [
        TextPlaceholder(r'//', '//'),
    ]


def get_For_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*for[ \t]*', 'for '),
        FieldPlaceholder('target'),
        TextPlaceholder(r'[ \t]*in[ \t]*', ' in '),
        FieldPlaceholder('iter'),
        TextPlaceholder(r':\n', ':\n'),
        BodyPlaceholder('body'),
        BodyPlaceholder(
            'orelse',
            prefix_placeholder=TextPlaceholder(r' *else:\n', 'else:\n')),
    ]


def get_FunctionDef_expected_parts():
    return [
        BodyPlaceholder(
            'decorator_list',
            before_placeholder=TextPlaceholder('[ \t]*@', '@'),
            after_placeholder=TextPlaceholder(r'\n*', '\n')),
        TextPlaceholder(r'([ \t]*async[ \t]+)*[ \t]*def ', 'def '),
        FieldPlaceholder('name'),
        TextPlaceholder(r'\(\s*', '('),
        FieldPlaceholder('args'),
        TextPlaceholder(r',?\s*\)([ \t]*->[ \t*])?',')'),
        FieldPlaceholder('returns'),
        TextPlaceholder(r'[ \t]*:[ \t]*\n', ':\n'),
        BodyPlaceholder('body')
    ]


def get_GeneratorExp_expected_parts():
    return [
        FieldPlaceholder('elt'),
        TextPlaceholder(r'\s*', ' '),
        ListFieldPlaceholder('generators'),
    ]


def get_Global_expected_parts():
    return [
        TextPlaceholder(r' *global *', 'global '),
        SeparatedListFieldPlaceholder(
            r'names',
            TextPlaceholder(r'\s*,\s*', ', ')),
    ]

def get_Nonlocal_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*nonlocal [ \t]*', 'global '),
        SeparatedListFieldPlaceholder(
            r'names',
            TextPlaceholder(r'\s*,\s*', ', ')),
    ]



def get_Gt_expected_parts():
    return [TextPlaceholder(r'>', '>')]


def get_GtE_expected_parts():
    return [TextPlaceholder(r'>=', '>=')]


def get_IfExp_expected_parts():
    return [
        FieldPlaceholder('body'),
        TextPlaceholder(r'\s*if\s*', ' if '),
        FieldPlaceholder('test'),
        TextPlaceholder(r'\s*else\s*', ' else '),
        FieldPlaceholder('orelse'),
    ]


def get_Import_expected_parts():
    return [
        TextPlaceholder(r' *import ', 'import '),
        SeparatedListFieldPlaceholder(
            'names', TextPlaceholder('[ \t]*,[ \t]*', ', ')),
        TextPlaceholder(r'\n*', '\n')
    ]


def get_ImportFrom_expected_parts(): # TODO: Handle path before names better
    return [
        TextPlaceholder(r'[ \t]*from[ \t]+[\.\/]*', 'from '),
        FieldPlaceholder('module'),
        TextPlaceholder(r' import[ \t]*\(?[ \t]*\n?'),
        SeparatedListFieldPlaceholder(
            'names', TextPlaceholder(r'[ \t]*,\n?[ \t]*\n*', '')),
#        TextPlaceholder(r'([ \t]*\n*[ \t]*,?\n*\)?\n?)*', '\n', no_transform=True)
        TextPlaceholder(r'([ \t]*\n*[ \t]*,[\n \t]*\)[ \t]*\n?)|'
                                r'([ \t]*\)[ \t]*\n)|'
                                r'(\n)|([ \t]*\))|'
                                #r'^(?![\s\S])'
                                r'', '\n', no_transform=True)
    ]


def get_In_expected_parts():
    return [TextPlaceholder(r'in', 'in')]


def get_Index_expected_parts():
    return [FieldPlaceholder(r'value')]


def get_Invert_expected_parts():
    return [TextPlaceholder(r'[ \t]*~', '~')]


def get_Is_expected_parts():
    return [TextPlaceholder(r'is', 'is')]


def get_IsNot_expected_parts():
    return [TextPlaceholder(r'is *not', 'is not')]


def get_keyword_expected_parts():
    return [
        FieldPlaceholder('arg'),
        TextPlaceholder(r'\s*=\s*', '='),
        FieldPlaceholder('value'),
    ]

def get_KWKeyword_expected_parts():
    return [
        FieldPlaceholder('value', before_placeholder=TextPlaceholder(r'\*\*', '**'))
    ]



def get_Tuple_expected_parts():
   return  [
           SeparatedListFieldPlaceholder( #note that the '?' might allow incorrect syntax like ((a,b c) -- but it
                                          # seems to work for now to allow both (a,) and (a)
               'elts',
               after__separator_placeholder=TextPlaceholder(r'([\n \t]*,([ \t]*#.*)?[\n \t]*\n?)?', '',
               no_transform=True),
               #exclude_last_after=True),
               exclude_last_after=False),
       ]
def get_List_expected_parts():
    return [
        TextPlaceholder(r'\[\s*', '['),
        SeparatedListFieldPlaceholder(
            'elts', TextPlaceholder(r'\s*,?\s*', ', ')), # note that the '?' might allow incorrect syntax like ((a,b c)
                                                                                 # -- but it is nessary to
                                                                                 # allow both [(1,2), (3,4)]
                                                                                 # issue 234
        #TextPlaceholder(REs['comma_args_seperator'], ']')]
        TextPlaceholder(r'\s*,?\s*\]', ']')]


def get_ListComp_expected_parts():
    return [
        TextPlaceholder(r'\[\s*', '['),
        FieldPlaceholder('elt'),
        TextPlaceholder(r' *', ' '),
        ListFieldPlaceholder('generators'),
        TextPlaceholder(r'\s*\]', ']'),
    ]


def get_LShift_expected_parts():
    return [
        TextPlaceholder(r'<<', '<<'),
    ]


def get_Lt_expected_parts():
    return [TextPlaceholder(r'<', '<')]


def get_LtE_expected_parts():
    return [TextPlaceholder(r'<=', '<=')]


def get_Mod_expected_parts():
    return [TextPlaceholder(r'%')]


def get_Module_expected_parts():
    return [BodyPlaceholder('body')]


def get_Mult_expected_parts():
    return [TextPlaceholder(r'\*', '*')]


def get_Name_expected_parts():
    return [TextPlaceholder(r'[ \t]*', ''),
            FieldPlaceholder('id'),
            TextPlaceholder(r'([ \t]*)(#.*)*', '')
     ]


def get_NotEq_expected_parts():
    return [TextPlaceholder(r'!=')]


def get_Not_expected_parts():
    return [TextPlaceholder(r'not', 'not')]


def get_NotIn_expected_parts():
    return [TextPlaceholder(r'not *in', 'not in')]



def get_Or_expected_parts():
    return [TextPlaceholder(r'or')]


def get_Pass_expected_parts():
    return [TextPlaceholder(r'[ \t]*pass[ \t]*#*.*\n*', 'pass')]


def get_Pow_expected_parts():
    return [
        TextPlaceholder(r'\*\*', '**'),
    ]


# TODO: Support non-nl syntax
def get_Print_expected_parts():
    return [
        TextPlaceholder(r' *print *', 'print '),
        FieldPlaceholder(
            'dest',
            before_placeholder=TextPlaceholder(r'>>', '>>')),
        ListFieldPlaceholder(
            r'values',
            TextPlaceholder(r'\s*,?\s*', ', ')),
        TextPlaceholder(r' *,? *\n', '\n')
    ]



def get_Raise_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*raise[ \t]*', 'raise '),
        FieldPlaceholder('exc'),
        FieldPlaceholder('cause', before_placeholder=TextPlaceholder(r'([ \t]*(from)[ \t]*)*', '')),
    ]


def get_Return_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*return[ \t]*', 'return '),
        FieldPlaceholder('value'),
    ]


def get_RShift_expected_parts():
    return [
        TextPlaceholder(r'>>', '>>'),
    ]


def get_Set_expected_parts():
    return [
        TextPlaceholder(r'\{\s*', '{'),
        SeparatedListFieldPlaceholder(
            'elts', TextPlaceholder(r'\s*,\s*', ', ')),
        TextPlaceholder(r'\s*\}', '}'),
    ]


def get_SetComp_expected_parts():
    return [
        TextPlaceholder(r'\{\s*', '{'),
        FieldPlaceholder('elt'),
        TextPlaceholder(r' *', ' '),
        ListFieldPlaceholder('generators'),
        TextPlaceholder(r'\s*\}', '}'),
    ]


def get_Slice_expected_parts():
    return [
        FieldPlaceholder('lower'),
        TextPlaceholder(r'\s*:?\s*', ':'),
        FieldPlaceholder('upper'),
        TextPlaceholder(r'\s*:?\s*', ':'),
        FieldPlaceholder('step'),
    ]

# def get_Slice_expected_parts():
#      return [
#          FieldPlaceholder('lower', after_placeholder=TextPlaceholder(r'\s*:?\s*', ':')),
#          #TextPlaceholder(r'\s*:?\s*', ':'),
#          FieldPlaceholder('upper', before_placeholder=TextPlaceholder(r'\s*:?\s*', ':')),
#          #TextPlaceholder(r'\s*:?\s*', ':'),
#          FieldPlaceholder('step', before_placeholder=TextPlaceholder(r'\s*:?\s*', ':') ),
#      ]





def get_Sub_expected_parts():
    return [
        TextPlaceholder(r'\-', '-'),
    ]


def get_Subscript_expected_parts():
    return [
        FieldPlaceholder('value'),
        TextPlaceholder(r'\s*\[\s*', '['),
        FieldPlaceholder('slice'),
        TextPlaceholder(r'\s*\]', ']'),
    ]


def get_SyntaxFreeLine_expected_parts():
    return [FieldPlaceholder('full_line'),
            TextPlaceholder(r'\n', '\n')]

def get_Comment_expected_parts():
    return [TextPlaceholder(r'#.*', '#')]


def get_TryExcept_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*try:[ \t]*\n', 'try:\n'),
        BodyPlaceholder('body', match_after=True),
        ListFieldPlaceholder('handlers'),
        BodyPlaceholder(
            'orelse',
            prefix_placeholder=TextPlaceholder(r'[ \t]*else:\n', 'else:\n')),
        BodyPlaceholder(
            'finalbody',
            prefix_placeholder= TextPlaceholder(r'[ \t]*finally:[ \t]*\n', 'finally:\n'))
    ]


# python 3 matching for ast.Constant


class TryFinallySourceMatcher(DefaultSourceMatcher):

    def __init__(self, node, starting_parens=None):
        expected_parts = [
            BodyPlaceholder('body', match_after=True),
            TextPlaceholder(r'[ \t]*finally:[ \t]*\n', 'finally:\n'),
            BodyPlaceholder('finalbody'),
        ]
        super(TryFinallySourceMatcher, self).__init__(
            node, expected_parts, starting_parens)
        self.optional_try = TextPlaceholder(r'[ \t]*try:[ \t]*\n', 'try:\n')

    def Match(self, string):
        remaining_string = string
        if not isinstance(self.node.body[0], _ast.Try):
            remaining_string = MatchPlaceholder(remaining_string, None, self.optional_try)
        return super(TryFinallySourceMatcher, self).Match(remaining_string)

    def GetSource(self):
        source_start = ''
        if not isinstance(self.node.body[0], _ast.TryExcept):
            source_start = self.optional_try.GetSource(None)
        return source_start + super(TryFinallySourceMatcher, self).GetSource()


def get_UAdd_expected_parts():
    return [
        TextPlaceholder(r'\+', '+'),
    ]


def get_UnaryOp_expected_parts():
    return [
        FieldPlaceholder('op'),
        TextPlaceholder(r' *', ' '),
        FieldPlaceholder('operand'),
#        TextPlaceholder(r'[ \t]*(#+.*)*\n?', '')
#        TextPlaceholder(r'[ \t]*#*.*\n*', '')
    ]


def get_USub_expected_parts():
    return [
        TextPlaceholder(r'-', '-'),
    ]


def get_While_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*while[ \t]*', 'while '),
        FieldPlaceholder('test'),
        TextPlaceholder(r'[ \t]*:[ \t]*\n', ':\n'),
        BodyPlaceholder('body'),
    ]


def get_Yield_expected_parts():
    return [
        TextPlaceholder(r'[ \t]*yield[ \t]*', 'yield '),
        FieldPlaceholder('value'),
    ]
