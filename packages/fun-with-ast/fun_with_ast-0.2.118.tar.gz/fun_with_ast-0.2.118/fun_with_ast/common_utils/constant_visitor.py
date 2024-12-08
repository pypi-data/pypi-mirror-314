import ast


class ConstantVisitor(ast.NodeTransformer):
  """Tracks the indent level of the current node."""

  def __init__(self, default_quote):
        self.default_quote = default_quote

  def visit_Constant(self, node):
    node.default_quote  = self.default_quote
    self.generic_visit(node)
    return node

