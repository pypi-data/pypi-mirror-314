import ast


class ConstantForJstr(ast.Constant):
    def __init__(self, value):
        super(ConstantForJstr, self).__init__(value)

class NameForJstr(ast.Name):
    def __init__(self, name_node):
        super(NameForJstr, self).__init__(name_node.id, name_node.ctx)
