import ast

from fun_with_ast.manipulate_node.call_args_node import LambdaArg
from fun_with_ast.placeholders.composite import FieldPlaceholder
from fun_with_ast.placeholders.text import TextPlaceholder
from fun_with_ast.source_matchers.defualt_matcher import DefaultSourceMatcher


class LambdaSourceMatcher(DefaultSourceMatcher):
    def __init__(self, node, starting_parens=None, parent=None):
        expected_parts = [
                 TextPlaceholder(r'lambda\s*', 'lambda '),
                 FieldPlaceholder('args'),
                 TextPlaceholder(r'\s*:\s*', ': '),
                 FieldPlaceholder('body'),
             ]
        new_args = []
        for arg in node.args.args:
            if isinstance(arg, ast.arg):
                arg_lambda = LambdaArg(arg)
                new_args.append(arg_lambda)
            else:
                raise ValueError(f'arg is not an instance of ast.arg. arg: {arg}')
        node.args.args = new_args
        if node.args.vararg:
            node.args.vararg = LambdaArg(node.args.vararg)
        super(LambdaSourceMatcher, self).__init__(node, expected_parts, starting_parens)
