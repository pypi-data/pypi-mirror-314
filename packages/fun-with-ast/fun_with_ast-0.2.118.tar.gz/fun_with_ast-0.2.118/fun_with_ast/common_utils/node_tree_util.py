
import _ast
import collections
import copy


# TODO: Handle TryExcept better
TYPE_TO_INDENT_FIELD = {
    _ast.ClassDef: ['body'],
    _ast.ExceptHandler: ['body'],
    _ast.For: ['body'],
    _ast.FunctionDef: ['body'],
    _ast.If: ['body', 'orelse'],
#    _ast.TryExcept: ['body', 'orelse'],
#    _ast.Try: ['finalbody'],
    _ast.While: ['body'],
    _ast.With: ['body'],
}


def IsEmptyModule(nodes):
    if nodes and not isinstance(nodes[0], _ast.Module):
        return False
    return len(nodes[0].body) == 0



def NodeCopy(node_to_copy):
  """Copies the node by recursively copying its fields."""
  if not isinstance(node_to_copy, _ast.AST):
    if isinstance(node_to_copy, list):
      new_list = []
      for child in node_to_copy:
        new_list.append(NodeCopy(child))
      return new_list
    elif isinstance(node_to_copy, str):
      return node_to_copy
    elif isinstance(node_to_copy, collections.Iterable):
      raise NotImplementedError(
          'Unrecognized iterable {}. Please add support'.format(node_to_copy))
    else:
      return copy.copy(node_to_copy)
  new_node = type(node_to_copy)()
  for field_name in node_to_copy._fields:
    setattr(new_node, field_name, NodeCopy(getattr(node_to_copy, field_name)))
  return new_node

