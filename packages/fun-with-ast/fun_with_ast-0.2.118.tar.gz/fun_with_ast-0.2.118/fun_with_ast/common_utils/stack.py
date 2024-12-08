from fun_with_ast.source_matchers.exceptions import EmptyStackException


class Stack():
  def __init__(self):
    self.__index = []

  def __len__(self):
    return len(self.__index)

  def reset(self):
    self.__index = []
  def push(self,item):
    self.__index.insert(0,item)

  def peek(self):
    if len(self) == 0:
      raise EmptyStackException("peek() called on empty stack.")
    return self.__index[0]

  def pop(self):
    if len(self) == 0:
      raise EmptyStackException("pop() called on empty stack.")
    return self.__index.pop(0)
  @property
  def size(self):
    return len(self.__index)
  def __str__(self):
    return str(self.__index)