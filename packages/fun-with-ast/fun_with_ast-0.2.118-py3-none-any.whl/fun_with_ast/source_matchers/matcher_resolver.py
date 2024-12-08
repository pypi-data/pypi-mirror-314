# A mapping of node_type: expected_parts
import _ast
import sys

import fun_with_ast.manipulate_node.call_args_node
import fun_with_ast.manipulate_node.create_node
import fun_with_ast.manipulate_node.nodes_for_jstr
import fun_with_ast.manipulate_node.syntax_free_line_node


def GetDynamicMatcher(node, starting_parens=None, parent_node=None, parts_in=None):
    """Gets an initialized matcher for the given node (doesnt call .Match).

    If there is no corresponding matcher in _matchers, this will return a
    default matcher, which starts with a placeholder for the first field, ends
    with a placeholder for the last field, and includes TextPlaceholders
    with ['.*' regexes between.

    Args:
      node: The node to get a matcher for.
      starting_parens: The parens the matcher may start with.

    Returns:
      A matcher corresponding to that node, or the default matcher (see above).
    """
    if starting_parens is None:
        starting_parens = []
    parts_or_matcher_string = _dynamic_matchers[node.__class__][0]
    parts_or_matcher_module = _dynamic_matchers[node.__class__][1]
    current_module = sys.modules[parts_or_matcher_module]
    parts_or_matcher = getattr(current_module, parts_or_matcher_string)
    try:
        if not parts_in :
            parts = parts_or_matcher()
        else:
            parts = parts_in
        default_source_matcher = current_module.DefaultSourceMatcher
        matcher = default_source_matcher(node, parts, starting_parens, parent_node)
        node.node_matcher = matcher
        return matcher
    except TypeError:
        matcher = parts_or_matcher(node, starting_parens, parent_node)
        node.node_matcher = matcher
        return matcher

_dynamic_matchers = {
    _ast.Add: ['get_Add_expected_parts', 'fun_with_ast.source_match'],
    _ast.alias: ['get_alias_expected_parts', 'fun_with_ast.source_match'],
    _ast.And: ['get_And_expected_parts', 'fun_with_ast.source_match'],
    _ast.Assert: ['get_Assert_expected_parts', 'fun_with_ast.source_match'],
    _ast.Assign: ['get_Assign_expected_parts', 'fun_with_ast.source_match'],
    _ast.AnnAssign: ['get_AnnAssign_expected_parts', 'fun_with_ast.source_match'],
    _ast.Attribute: ['get_Attribute_expected_parts', 'fun_with_ast.source_match'],
    _ast.AugAssign: ['get_AugAssign_expected_parts', 'fun_with_ast.source_match'],
    _ast.arguments: ['get_arguments_expected_parts', 'fun_with_ast.source_match'],
    _ast.arg: ['get_arg_expected_parts', 'fun_with_ast.source_match'],
    _ast.Await: ['get_Await_expected_parts', 'fun_with_ast.source_match'],
    _ast.BinOp: ['get_BinOp_expected_parts', 'fun_with_ast.source_match'],
    _ast.BitAnd: ['get_BitAnd_expected_parts', 'fun_with_ast.source_match'],
    _ast.BitOr: ['get_BitOr_expected_parts', 'fun_with_ast.source_match'],
    _ast.BitXor: ['get_BitXor_expected_parts', 'fun_with_ast.source_match'],
    _ast.BoolOp: ['BoolOpSourceMatcher', 'fun_with_ast.source_match'],
    _ast.Break: ['get_Break_expected_parts', 'fun_with_ast.source_match'],
    _ast.Call: ['get_Call_expected_parts', 'fun_with_ast.source_match'],
    _ast.ClassDef: ['get_ClassDef_expected_parts', 'fun_with_ast.source_match'],
    _ast.Compare: ['get_Compare_expected_parts', 'fun_with_ast.source_match'],
    _ast.comprehension: ['get_comprehension_expected_parts', 'fun_with_ast.source_match'],
    _ast.Continue: ['get_Continue_expected_parts', 'fun_with_ast.source_match'],
    _ast.Delete: ['get_Delete_expected_parts', 'fun_with_ast.source_match'],
    _ast.Dict: ['get_Dict_expected_parts', 'fun_with_ast.source_match'],
    _ast.DictComp: ['get_DictComp_expected_parts', 'fun_with_ast.source_match'],
    _ast.Div: ['get_Div_expected_parts', 'fun_with_ast.source_match'],
    _ast.Eq: ['get_Eq_expected_parts', 'fun_with_ast.source_match'],
    _ast.Expr: ['get_Expr_expected_parts', 'fun_with_ast.source_match'],
    _ast.ExceptHandler: ['get_ExceptHandler_expected_parts', 'fun_with_ast.source_match'],
    _ast.FloorDiv: ['get_FloorDiv_expected_parts', 'fun_with_ast.source_match'],
    _ast.For: ['get_For_expected_parts', 'fun_with_ast.source_match'],
    _ast.FunctionDef: ['get_FunctionDef_expected_parts', 'fun_with_ast.source_match'],
    _ast.AsyncFunctionDef: ['get_FunctionDef_expected_parts', 'fun_with_ast.source_match'],
    _ast.GeneratorExp: ['get_GeneratorExp_expected_parts', 'fun_with_ast.source_match'],
    _ast.Global: ['get_Global_expected_parts', 'fun_with_ast.source_match'],
    _ast.Gt: ['get_Gt_expected_parts', 'fun_with_ast.source_match'],
    _ast.GtE: ['get_GtE_expected_parts', 'fun_with_ast.source_match'],
    _ast.If: ['IfSourceMatcher', 'fun_with_ast.source_matchers.if_source_match'],
    _ast.IfExp: ['get_IfExp_expected_parts', 'fun_with_ast.source_match'],
    _ast.Import: ['get_Import_expected_parts', 'fun_with_ast.source_match'],
    _ast.ImportFrom: ['get_ImportFrom_expected_parts', 'fun_with_ast.source_match'],
    _ast.In: ['get_In_expected_parts', 'fun_with_ast.source_match'],
    _ast.Invert: ['get_Invert_expected_parts', 'fun_with_ast.source_match'],
    _ast.Is: ['get_Is_expected_parts', 'fun_with_ast.source_match'],
    _ast.IsNot: ['get_IsNot_expected_parts', 'fun_with_ast.source_match'],
    _ast.keyword: ['get_keyword_expected_parts', 'fun_with_ast.source_match'],
    _ast.Lambda:['LambdaSourceMatcher', 'fun_with_ast.source_matchers.lambda_matcher'],
    _ast.List: ['get_List_expected_parts', 'fun_with_ast.source_match'],
    _ast.ListComp: ['get_ListComp_expected_parts', 'fun_with_ast.source_match'],
    _ast.LShift: ['get_LShift_expected_parts', 'fun_with_ast.source_match'],
    _ast.Lt: ['get_Lt_expected_parts', 'fun_with_ast.source_match'],
    _ast.LtE: ['get_LtE_expected_parts', 'fun_with_ast.source_match'],
    _ast.Mod: ['get_Mod_expected_parts', 'fun_with_ast.source_match'],
    _ast.Module: ['get_Module_expected_parts', 'fun_with_ast.source_match'],
    _ast.Mult: ['get_Mult_expected_parts', 'fun_with_ast.source_match'],
    _ast.Name: ['get_Name_expected_parts', 'fun_with_ast.source_match'],
    _ast.NamedExpr: ['get_NamedExpr_expected_parts', 'fun_with_ast.source_match'],
    _ast.Nonlocal: ['get_Nonlocal_expected_parts', 'fun_with_ast.source_match'],
    _ast.Not: ['get_Not_expected_parts', 'fun_with_ast.source_match'],
    _ast.NotIn: ['get_NotIn_expected_parts', 'fun_with_ast.source_match'],
    _ast.NotEq: ['get_NotEq_expected_parts', 'fun_with_ast.source_match'],
    _ast.Or: ['get_Or_expected_parts', 'fun_with_ast.source_match'],
    _ast.Pass: ['get_Pass_expected_parts', 'fun_with_ast.source_match'],
    _ast.Pow: ['get_Pow_expected_parts', 'fun_with_ast.source_match'],
    _ast.Raise: ['get_Raise_expected_parts', 'fun_with_ast.source_match'],
    _ast.Return: ['get_Return_expected_parts', 'fun_with_ast.source_match'],
    _ast.RShift: ['get_RShift_expected_parts', 'fun_with_ast.source_match'],
    _ast.Slice: ['get_Slice_expected_parts', 'fun_with_ast.source_match'],
    _ast.Sub: ['get_Sub_expected_parts', 'fun_with_ast.source_match'],
    _ast.Set: ['get_Set_expected_parts', 'fun_with_ast.source_match'],
    _ast.SetComp: ['get_SetComp_expected_parts', 'fun_with_ast.source_match'],
    _ast.Subscript: ['get_Subscript_expected_parts', 'fun_with_ast.source_match'],
    _ast.Constant: ['ConstantSourceMatcher', 'fun_with_ast.source_match'],
    _ast.Tuple: ['get_Tuple_expected_parts', 'fun_with_ast.source_match'],
    _ast.JoinedStr: ['JoinedStrSourceMatcherNew', 'fun_with_ast.source_matchers.joined_str_new'],
    _ast.Try: ['get_TryExcept_expected_parts', 'fun_with_ast.source_match'],
    _ast.Starred: ['get_Starred_expected_parts', 'fun_with_ast.source_match'],
    _ast.FormattedValue: ['get_FormattedValue_expected_parts', 'fun_with_ast.source_match'],
    _ast.UAdd: ['get_UAdd_expected_parts', 'fun_with_ast.source_match'],
    _ast.UnaryOp: ['get_UnaryOp_expected_parts', 'fun_with_ast.source_match'],
    _ast.USub: ['get_USub_expected_parts', 'fun_with_ast.source_match'],
    _ast.While: ['get_While_expected_parts', 'fun_with_ast.source_match'],
    _ast.With: ['WithSourceMatcher', 'fun_with_ast.source_match'],
    _ast.withitem: ['WithItemSourceMatcher', 'fun_with_ast.source_matchers.withitem'],
    _ast.Yield: ['get_Yield_expected_parts', 'fun_with_ast.source_match'],
    fun_with_ast.manipulate_node.syntax_free_line_node.SyntaxFreeLine: ['SyntaxFreeLineMatcher',
                                                                        'fun_with_ast.source_matchers.syntaxfreeline'],
    fun_with_ast.manipulate_node.create_node.Comment: ['get_Comment_expected_parts', 'fun_with_ast.source_match'],
    fun_with_ast.manipulate_node.call_args_node.LambdaArg: ['get_LambdaArg_expected_parts', 'fun_with_ast.source_match'],
#    fun_with_ast.source_matchers.: ['get_CallArgs_expected_parts', 'fun_with_ast.source_match'],
#    fun_with_ast.manipulate_node.lambda_arg.LambdaArg: ['get_LambdaArg_expected_parts', 'fun_with_ast.source_match'],

    fun_with_ast.manipulate_node.call_args_node.CallArgs: ['get_CallArgs_expected_parts', 'fun_with_ast.source_match'],

    fun_with_ast.manipulate_node.call_args_node.KWKeyword: ['get_KWKeyword_expected_parts', 'fun_with_ast.source_match'],
    fun_with_ast.manipulate_node.nodes_for_jstr.ConstantForJstr: ['ConstantJstrMatcher',
                                                                     'fun_with_ast.source_matchers.constant_jstr_matcher'],
    fun_with_ast.manipulate_node.nodes_for_jstr.NameForJstr: ['NameJstrMatcher',
                                                               'fun_with_ast.source_matchers.name_jstr_matcher'],
}