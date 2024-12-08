import ast
import re

from fun_with_ast.common_utils.constant_visitor import ConstantVisitor


class FailedToCreateNodeFromInput(BaseException):
    pass


def GetNodeFromInput(string, body_index = 0, get_module = False):
    try: 
        generator = FWANodeGenerator()
        return generator.GetNodeFromInputV1(string, body_index, get_module)
    except Exception as e:
        raise FailedToCreateNodeFromInput(f'Error in GetNodeFromInput: {e}')

# will be used in next generation of the library
class FWANodeGenerator():
    def __init__(self):
        pass
    def GetNodeFromInputV1(self, string, body_index = 0, get_module = False):
        parse_result = ast.parse(string)
        if parse_result.body and get_module == False:
            node = parse_result.body[body_index]
        elif parse_result.body and get_module == True:
            node = parse_result
        else:
            return parse_result # empty Module
        if isinstance(node, ast.If) and 'elif' in string:
            node.is_elif = True if 'elif' in string else False
        quote = self.guess_default_quote_for_node(string)
        constant_visitor = ConstantVisitor(quote)
        constant_visitor.visit(node)
        return node

    def guess_default_quote_for_node(self, string):
        lines = string.split('\n')
        quote = "\""
        for line in lines:
            if re.match(r'[\t ]*#', line):
                continue
            elif re.match(r'[\t ]*"""', line):
                quote = "\"\"\""
                break
            elif "\"" in line:
                break
            elif "'" in line:
                quote = "'"
                break
        return quote
