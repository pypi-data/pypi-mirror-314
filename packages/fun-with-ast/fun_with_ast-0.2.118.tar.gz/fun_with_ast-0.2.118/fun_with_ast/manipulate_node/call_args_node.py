import _ast
import ast


class KWKeyword(ast.keyword):
    def __init__(self, keyword:ast.keyword):
        if not isinstance(keyword, ast.keyword):
            raise ValueError('incorrect keyword node')
        self.value = keyword.value
        self._fields = [ 'value']
        self.lineno = keyword.lineno
        self.col_offset = keyword.col_offset
        self.end_lineno = keyword.end_lineno
        self.end_col_offset = keyword.end_col_offset


class CallArgs(_ast.stmt):
    """A node for handling arguments for a function call"""

    def __init__(self, args_list, keywords_list, parent_node):
        self._fields = ['args', 'keywords']
        self.args = args_list
        self.parent_node = parent_node
        kw_keywords = []
        for keyword in keywords_list:
            if self.isKWarg(keyword):
                kw_keywords.append(KWKeyword(keyword))
            else:
                kw_keywords.append(keyword)
        self.keywords = kw_keywords


    def isKWarg(self, kw_keyword):
        if not hasattr(kw_keyword,'arg'):
            return True
        elif not kw_keyword.arg:
            return True
        elif isinstance(kw_keyword.arg, str):
            return False
        else:
            raise ValueError('incorrect type for kw_keyword.arg')

class LambdaArg(ast.arg):
    def __init__(self, arg: ast.arg):
        self.arg = arg.arg
        self.annotation = arg.annotation
        self.type_comment = arg.type_comment
        self.type = "lambda_arg"

