
import _ast
import ast


class Error(Exception):
    pass


class InvalidCtx(Error):
    pass


def Enum(**enums):
    return type('Enum', (), enums)


CtxEnum = Enum(
    LOAD='load',
    STORE='store',
    DEL='delete',
    PARAM='param')


def _ToArgsWithDefaults(_args, _defaults):
    if not isinstance(_args, list):
        raise ValueError('args must be a list')
    if not isinstance(_defaults, list):
        raise ValueError('defaults must be a list')
    args = []
    defaults = []
    for arg in _args:
        args.append(arg)
    for default in _defaults:
        defaults.append(default)
    args = [_WrapWithArgs(arg) for arg in args]
    defaults = [_WrapWithName(default) for default in defaults]
    return args, defaults


def _WrapWithArgs(to_wrap):
    if isinstance(to_wrap, _ast.AST):
        return to_wrap
    if ':' in to_wrap:
        name, annotation = to_wrap.split(':')
        annotation = _WrapWithName(annotation, ctx_type=CtxEnum.LOAD)
    else:
        name = to_wrap
        annotation = None

    return Arg(name, annotation=annotation)


def _WrapWithName(to_wrap, ctx_type=CtxEnum.LOAD):
    if isinstance(to_wrap, _ast.AST):
        return to_wrap
    if isinstance(to_wrap, int):
        return Constant(to_wrap)
    if isinstance(to_wrap, str):
        return Name(to_wrap, ctx_type=ctx_type)
    raise NotImplementedError


# def _WrapWithTuple(to_wrap, ctx_type=CtxEnum.LOAD):
#     if not isinstance(to_wrap, list):
#         raise NotImplementedError
#     return Tuple(to_wrap, ctx_type=ctx_type)


def _LeftmostNodeInDotVar(node):
    while not hasattr(node, 'id'):
        if not hasattr(node, 'value'):
            return node
        node = node.value
    return node


def FormatAndValidateBody(body):
    if body is None:
        body = [Pass()]
    for child in body:
        if not isinstance(child, _ast.stmt):
            raise ValueError(
                'All body nodes must be stmt nodes, and {} is not. '
                'Try wrapping your node in an Expr node.'
                    .format(child))
    return body


class ChangeCtxTransform(ast.NodeTransformer):

    def __init__(self, new_ctx_type):
        super(ChangeCtxTransform, self).__init__()
        self._new_ctx_type = new_ctx_type

    def generic_visit(self, node):
        node = super(ChangeCtxTransform, self).generic_visit(node)
        if hasattr(node, 'ctx'):
            node.ctx = GetCtx(self._new_ctx_type)
        return node


def ChangeCtx(node, new_ctx_type):
    transform = ChangeCtxTransform(new_ctx_type)
    transform.visit(node)


###############################################################################
# Node Creators
###############################################################################


def arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
              defaults=[]):
    """Creates an _ast.FunctionDef node.

  Args:
    args: A list of args.
    keys: A list of keys, must be the same length as values.
    values: A list of values, correspond to keys.
    vararg_name: The name of the vararg variable, or None.
    kwarg_name: The name of the kwargs variable, or None.

  Raises:
    ValueError: If len(keys) != len(values).

  Returns:
    An _ast.FunctionDef node.
  """
    if not isinstance(args, list):
        raise ValueError('args must be a list')
    if kwarg:
        kwarg = _WrapWithArgs(kwarg)
    if vararg:
        vararg = _WrapWithArgs(vararg)
    args, defaults = _ToArgsWithDefaults(args, defaults)
    return _ast.arguments(
    posonlyargs=posonlyargs,
    args=args,
    vararg=vararg,
    kwonlyargs=kwonlyargs,
    kw_defaults=kw_defaults,
    kwarg=kwarg,
    defaults=defaults)

def Add():
    return _ast.Add()


def And():
    return _ast.And()


def Assert(check, message=None):
    return _ast.Assert(test=check, msg=message)

def AnnAssign(target, value=None, simple=1):
    if ':' not in target:
        raise ValueError('target must have an annotation')
    name, annotation = target.split(':')
    if '.' not in name:
        target_node = _WrapWithName(name, ctx_type=CtxEnum.STORE)
        annotation_node = _WrapWithName(annotation, ctx_type=CtxEnum.LOAD)
    else:
        raise NotImplementedError("Handle attribute names")
    return _ast.AnnAssign(target_node, annotation_node, value=value, simple=simple)

def Assign(left, right):
    """Creates an _ast.Assign node.

  Args:
    left: The node on the left side of the equal sign.
      May either be a node, or a string, which will automatically get
      converted to a name node.
    right: The node on the right side of the equal sign.

  Returns:
    An _ast.Assign node.
  """
    if not isinstance(left, (list, tuple)):
        targets = [left]
    else:
        targets = left
    new_targets = []
    for target in targets:
        if isinstance(target, str):
            new_targets.append(_WrapWithName(target, ctx_type=CtxEnum.STORE))
        else:
            new_targets.append(target)
    base = _extract_base(right)
    result = _ast.Assign(
            targets=new_targets,
            value=right)
    result.base = base
    return result

def AugAssign(left, op, right):
    """Creates an _ast.AugAssign node.

  Args:
    left: The node on the left side of the equal sign.
      May either be a node, or a string, which will automatically get
      converted to a name node.
    op: Operator
    right: The node on the right side of the equal sign.

  Returns:
    An _ast.Assign node.
  """
    left = _WrapWithName(left)
    return _ast.AugAssign(
        target=left,
        op=op,
        value=right)


def BinOp(left, op, right):
    """Creates an _ast.BinOp node.

  Args:
    left: The node on the left side of the equal sign.
    op: The operator. Literal values as strings also accepted:
    right: The node on the right side of the equal sign.

  Returns:
    An _ast.BinOp node.
  """
    if not isinstance(op, _ast.AST):
        op = BinOpMap(op)

    return _ast.BinOp(
        left=left,
        op=op,
        right=right)


def BoolOp(left, *alternating_ops_values):
    """Creates an _ast.BoolOp node.

  Args:
    left: The node on the left side of the equal sign.
    *alternating_ops_values: An alternating list of ops and expressions.
      Note that _ast.Not is not a valid boolean operator, it is considered
      a unary operator.
      For example: (_ast.Or, _ast.Name('a'))

  Returns:
    An _ast.BoolOp node.
  """
    values = [left]
    op = None
    op_next = True
    alternating_ops_values = list(alternating_ops_values)
    while alternating_ops_values:
        op_or_value = alternating_ops_values.pop(0)
        if op_next:
            if not isinstance(op_or_value, _ast.AST):
                op_or_value = BoolOpMap(op_or_value)
            if not op:
                op = op_or_value
            elif op and op == op_or_value:
                continue
            else:
                # Or's take priority over And's
                if isinstance(op, _ast.And):
                    return BoolOp(_ast.BoolOp(op=op, values=values),
                                  op_or_value,
                                  *alternating_ops_values)
                else:
                    last_value = values.pop()
                    values.append(BoolOp(last_value,
                                         op_or_value,
                                         *alternating_ops_values))
                    return _ast.BoolOp(
                        op=_ast.Or(),
                        values=values)
        else:
            values.append(op_or_value)
        op_next = not op_next

    return _ast.BoolOp(op=op, values=values)


def BitAnd():
    return _ast.BitAnd()


def BitOr():
    return _ast.BitOr()


def BitXor():
    return _ast.BitXor()


def keyword(arg, value):
    return _ast.keyword(arg, value)

def  Stared(value, ctx=CtxEnum.LOAD):
    if ctx != CtxEnum.LOAD:
        raise NotImplementedError('Only LOAD context is supported')
    return _ast.Starred(value, ctx=ctx)


def Call(caller, args=[], keywords=[]):

    if not isinstance(args, list):
        raise ValueError('args must be a list')

    if not isinstance(keywords, list):
        raise ValueError('keywords must be a list')

    if isinstance(caller, str):
        caller = VarReference(*caller.split('.'))
    if not isinstance(caller, (_ast.Name, _ast.Attribute)):
        raise ValueError('caller must be a Name or an Attribute')
    args = [_WrapWithName(arg, ctx_type=CtxEnum.LOAD) for arg in args]
    result = _ast.Call(func=caller,args=args,keywords=keywords)
    return result

# def Call(caller, args=[], keywords=[], starargs=None, kwargs={}):
#     """Creates an _ast.Call node.
#   Will be deleted soon
#   Args:
#     caller: Either a node of the appropriate type
#       (_ast.Str, _ast.Name, or _ast.Attribute), or a dot-separated string.
#     args: A list of args.
#     keys: A list of keys, must be the same length as values.
#     values: A list of values, correspond to keys.
#     starargs: A node with a star in front of it. Passing a string will be
#       interpreted as a VarReference.
#     kwargs: A node with two stars in front of it. Passing a string will be
#       interpreted as a VarReference.
#
#   Raises:
#     ValueError: If len(keys) != len(values) or caller is not the right type.
#
#   Returns:
#     An _ast.Call object.
#   """
#     raise NotImplementedError('Use Call310 instead')
#     if not isinstance(args, list):
#         raise ValueError('args must be a list')
#
#         #  if len(keys) != len(values):
#     #    raise ValueError(
#     #        'len(keys)={} != len(values)={}'.format(len(keys), len(values)))
#     if isinstance(caller, str):
#         caller = VarReference(*caller.split('.'))
#     if not isinstance(kwargs, dict):
#         raise ValueError('kwargs must be a ast.Dict')
#     if not isinstance(caller, (_ast.Name, _ast.Attribute)):
#         raise ValueError('caller not the expected value')
#     args = [_WrapWithName(arg, ctx_type=CtxEnum.LOAD) for arg in args]
#     if isinstance(starargs, str):
#         starargs = VarReference(*starargs.split('.'))
#     if isinstance(kwargs, str):
#         kwargs = VarReference(*kwargs.split('.'))
#     result = _ast.Call310(
#         func=caller,
#         args=args,
#         keywords=keywords,
#         starargs=starargs,
#         kwargs=kwargs)
#     return result


def ClassDef(name, bases=[], body=[], keywords=[], starargs=None, kwargs=None, decorator_list=[]):
    """Creates an _ast.ClassDef node.

  Args:
    name: The name of the class.
    bases: The base classes of the class
    body: A list of _ast.stmt nodes that go in the body of the class.
    decorator_list: A list of decorator nodes.

  Raises:
    ValueError: If some body element is not an _ast.stmt node.

  Returns:
    An _ast.ClassDef node.
  """
    if not body:
        raise ValueError('class body must be a non empty')
    if kwargs is not None:
        raise NotImplementedError('Non None kwargs is not supported')
    if starargs is not None:
        raise NotImplementedError('Non None starargs is not supported')
    if not isinstance(bases, list):
        raise ValueError('bases must be a list')
    body = FormatAndValidateBody(body)
    bases = [_WrapWithName(base, ctx_type=CtxEnum.LOAD) for base in bases]
    return _ast.ClassDef(
        name=name,
        bases=bases,
        body=body,
        keywords=keywords,
        decorator_list=list(decorator_list))


def Compare(*args):
    """Creates an _ast.Compare node.

  Args:
    *args: List which should alternate between regular nodes and _ast.cmpop.

  Raises:
    ValueError: If less than 3 args, or odd args are not valid comparison
      operators.

  Returns:
    An _ast.Compare node.
  """
    if len(args) < 3:
        raise ValueError('Must have at least 3 args')
    ops = []
    comparators = []
    for index, arg in enumerate(args):
        if index % 2 == 1:
            if not isinstance(arg, _ast.AST):
                arg = CompareOpMap(arg)
            if not isinstance(arg, _ast.cmpop):
                raise ValueError('Odd args must be instances of _ast.cmpop')
            ops.append(arg)
        else:
            if index != 0:
                comparators.append(_WrapWithName(arg, ctx_type=CtxEnum.LOAD))
    return _ast.Compare(left=_WrapWithName(args[0], ctx_type=CtxEnum.LOAD),
                        ops=ops,
                        comparators=comparators)


def comprehension(for_part, in_part, is_async, *ifs):
    """Create an _ast.comprehension node, used in _ast.ListComprehension.

  Args:
    for_part: The part after "for "
    in_part: The part after "for [for_part] in "
    *ifs: {_ast.Compare}

  Returns:
    {_ast.comprehension}
    :param is_async:
  """
    for_part = _WrapWithName(for_part, ctx_type=CtxEnum.STORE)
    in_part = _WrapWithName(in_part, ctx_type=CtxEnum.LOAD)
    return _ast.comprehension(target=for_part,
                              iter=in_part,
                              ifs=list(ifs),
                              is_async=is_async)


def Dict(keys=(), values=()):
    """Creates an _ast.Dict node. This represents a dict literal.

  Args:
    keys: A list of keys as nodes. Must be the same length as values.
    values: A list of values as nodes. Must be the same length as values.

  Raises:
    ValueError: If len(keys) != len(values).

  Returns:
    An _ast.Dict node.
  """
    if len(keys) != len(values):
        raise ValueError(
            'len(keys)={} != len(values)={}'.format(len(keys), len(values)))
    keys = [_WrapWithName(key) for key in keys]
    values = [_WrapWithName(value) for value in values]
    return _ast.Dict(keys, values)


def DictComp(left_side_key, left_side_value, for_part, in_part, *ifs, is_async=0):
    """Creates _ast.DictComp nodes.

  'left_side', 'left_side_value' for 'for_part' in 'in_part' if 'ifs'

  Args:
    left_side_key: key in leftmost side of the expression.
    left_side_value: value in leftmost side of the expression.
    for_part: The part after '[left_side] for '
    in_part: The part after '[left_side] for [for_part] in '
    *ifs: Any if statements that come at the end.

  Returns:
    {_ast.DictComp}
    :param is_async:
  """
    left_side_key = _WrapWithName(left_side_key, ctx_type=CtxEnum.LOAD)
    left_side_value = _WrapWithName(left_side_value, ctx_type=CtxEnum.LOAD)
    for_part = _WrapWithName(for_part, ctx_type=CtxEnum.STORE)
    in_part = _WrapWithName(in_part, ctx_type=CtxEnum.LOAD)
    return _ast.DictComp(
        key=left_side_key,
        value=left_side_value,
        generators=[comprehension(for_part, in_part, is_async, *ifs)])


def Div():
    return _ast.Div()


def Eq():
    return _ast.Eq()


def ExceptHandler(exception_type=None, name=None, body=None):
    body = FormatAndValidateBody(body)
    return _ast.ExceptHandler(type=exception_type, name=name, body=body)


def Expr(value):
    """Creates an _ast.Expr node.

  Note that this node is mostly used to wrap other nodes so they're treated
  as whole-line statements.

  Args:
    value: The value stored in the node.

  Raises:
    ValueError: If value is an _ast.stmt node.

  Returns:
    An _ast.Expr node.
  """
    if isinstance(value, _ast.stmt):
        raise ValueError(
            'value must not be an _ast.stmt node, because those nodes don\'t need '
            'to be wrapped in an Expr node. Value passed: {}'.format(value))
    return _ast.Expr(value)


def FloorDiv():
    return _ast.FloorDiv()


def FunctionDef(
        name, args=None, body=[], decorator_list=[], returns=None, type_comment=None):
    """Creates an _ast.FunctionDef node.

  Args:
    name: The name of the function.
    args: A list of args.
    keys: A list of keys, must be the same length as values.
    values: A list of values, correspond to keys.
    body: A list of _ast.stmt nodes that go in the body of the function.
    vararg_name: The name of the vararg variable, or None.
    kwarg_name: The name of the kwargs variable, or None.
    decorator_list: A list of decorator nodes.
  Raises:
    ValueError: If len(keys) != len(values).

  Returns:
    An _ast.FunctionDef node.
  """
    if args and not isinstance(args, ast.arguments):
        raise ValueError('args must be a list')
    if not args:
        args = arguments()
    else:
        args = args
    body = FormatAndValidateBody(body)
    return _ast.FunctionDef(
        name=name,
        args=args,
        body=body,
        returns=returns,
        type_comment=type_comment,
        decorator_list=list(decorator_list))


def GeneratorExp(left_side, for_part, in_part, *ifs):
    """Creates _ast.GeneratorExp nodes.

  'left_side' for 'for_part' in 'in_part' if 'ifs'

  Args:
    left_side: leftmost side of the expression.
    for_part: The part after '[left_side] for '
    in_part: The part after '[left_side] for [for_part] in '
    *ifs: Any if statements that come at the end.

  Returns:
    {_ast.GeneratorExp}
  """
    left_side = _WrapWithName(left_side, ctx_type=CtxEnum.LOAD)
    for_part = _WrapWithName(for_part, ctx_type=CtxEnum.STORE)
    in_part = _WrapWithName(in_part, ctx_type=CtxEnum.LOAD)
    result = _ast.GeneratorExp(
        elt=left_side,
        generators=[comprehension(for_part, in_part, 0, *ifs)])
    return result


def Gt():
    return _ast.Gt()


def GtE():
    return _ast.GtE()


def If(conditional, body, orelse=None):
    """Creates an _ast.If node.

  Args:
    conditional: The expression we evaluate for its truthiness.
    body: The list of nodes that make up the body of the if statement.
      Executed if True.
    orelse: {[_ast.If]|[_ast.stmt]|None} Either another If statement as the
      only element in a list, (in which case this becomes an elif), a list of
      stmt nodes (in which case this is an else), or None (in which case, there
      is only the if)

  Raises:
    ValueError: If the body or orelse are lists which contain elements not
      inheriting from _ast.stmt.

  Returns:
    An _ast.If node.
  """
    body = FormatAndValidateBody(body)
    if orelse is None:
        orelse = []
    if isinstance(orelse, (list, tuple)):
        for child in body:
            if not isinstance(child, _ast.stmt):
                raise ValueError(
                    'All body nodes must be stmt nodes, and {} is not. '
                    'Try wrapping your node in an Expr node.'
                        .format(child))
    return _ast.If(test=conditional, body=body, orelse=orelse)


def IfExp(conditional, true_case, false_case):
    """Creates an _ast.IfExp node.

  Note that this is python's ternary operator, not to be confused with _ast.If.

  Args:
    conditional: The expression we evaluate for its truthiness.
    true_case: What to do if conditional is True.
    false_case: What to do if conditional is False.

  Returns:
    An _ast.IfExp node.
  """
    return _ast.IfExp(body=true_case, test=conditional, orelse=false_case)

def ImportFrom(module, names, level=0):
    if not isinstance(names, (list, tuple)):
        raise ValueError('names must be a list or tuple')
    alias_names = []
    for name in names:
        if not isinstance(name, str):
            raise ValueError('All names must be strings')
        alias_names.append(_ast.alias(name=name, asname=None))
    return _ast.ImportFrom(module=module, names=alias_names, level=level)


def Import(import_part='', from_part='', asname=None):
    """Creates either an _ast.Import node or an _ast.ImportFrom node.

  Args:
    import_part: The text that follows "import".
    from_part: The text that follows "from". Optional. Determines if we will
      return an _ast.Import or _ast.ImportFrom node.
    asname: Text that follows "as". Optional.

  Returns:
    An _ast.Import or _ast.ImportFrom node.
  """
    names = [_ast.alias(name=import_part,
                        asname=asname)]
    if from_part:
        return _ast.ImportFrom(
            level=0,
            module=from_part,
            names=names)
    else:
        return _ast.Import(names=names)


def In():
    return _ast.In()


def Index(value):
    return _ast.Index(value)


def Invert():
    return _ast.Invert()


def Is():
    return _ast.Is()


def IsNot():
    return _ast.IsNot()


def Lambda(body, args=[]):
    """Creates an _ast.Lambda object.

  Args:
    body: {_ast.AST}
    args: {_ast.arguments}

  Raises:
    ValueError: If body is a list or tuple.

  Returns:
    {_ast.Lambda}
  """
    if isinstance(body, (list, tuple)):
        raise ValueError('Body should be a single element, not a list or tuple')
    #    if not args:
    #        args = arguments()
    lambda_args = arguments(args=args)
    return _ast.Lambda(args=lambda_args, body=body)


def List(*items, **kwargs):
    """Creates an _ast.List node.

  Automatically adjusts inner ctx attrs.

  Args:
    *items: The items in the list.
    **kwargs: Only recognized kwarg is 'ctx_type', which controls the
      ctx type of the list. See CtxEnum.

  Returns:
    An _ast.List node.
  """
    ctx_type = kwargs.pop('ctx_type', CtxEnum.LOAD)

    for item in items:
        if isinstance(item, _ast.Name):
            item.ctx = GetCtx(ctx_type)
        elif isinstance(item, _ast.Attribute):
            name_node = _LeftmostNodeInDotVar(item)
            name_node.ctx = GetCtx(ctx_type)
    ctx = GetCtx(ctx_type)
    return _ast.List(elts=list(items),
                     ctx=ctx)


def ListComp(left_side, for_part, in_part, *ifs):
    """Creates _ast.ListComp nodes.

  'left_side' for 'for_part' in 'in_part' if 'ifs'

  Args:
    left_side: leftmost side of the expression.
    for_part: The part after '[left_side] for '
    in_part: The part after '[left_side] for [for_part] in '
    *ifs: Any if statements that come at the end.

  Returns:
    {_ast.ListComp}
  """
    left_side = _WrapWithName(left_side, ctx_type=CtxEnum.LOAD)
    for_part = _WrapWithName(for_part, ctx_type=CtxEnum.STORE)
    in_part = _WrapWithName(in_part, ctx_type=CtxEnum.LOAD)
    return _ast.ListComp(
        elt=left_side,
        generators=[comprehension(for_part, in_part, False, *ifs)])


def LShift():
    return _ast.LShift()


def Lt():
    return _ast.Lt()


def LtE():
    return _ast.LtE()


def Mod():
    return _ast.Mod()


def Module(*body_items):
    if not body_items:
        raise ValueError('Must have at least one argument in the body')
    return _ast.Module(body=list(body_items))


def Mult():
    return _ast.Mult()


def Arg(arg, annotation=None):
#    if is_lambda:
#        return LambdaArg(arg)
    result = _ast.arg(arg=arg, annotation=annotation)
    return result


def Constant(value, quote_type =None):
    node = _ast.Constant(value=value)
    if isinstance(value, str):
        if not quote_type:
            raise ValueError('Constant string must be provided with quote type')
        node.default_quote = quote_type
    return node


def validate_id(name_id):
    if not isinstance(name_id, str):
        raise ValueError(f'python id must be a string')
    if name_id is None or name_id[0].isdigit():
        raise ValueError(f'Invalid python id: {name_id}')
    stripped_underscore = name_id.replace('_', '')
    isalnum = stripped_underscore.isalnum()
    if not isalnum:
        raise ValueError(f'Invalid python id: {name_id}')


def Name(name_id, ctx_type=CtxEnum.LOAD):
    """Creates an _ast.Name node.

  Args:
    name_id: Name of the node.
    ctx_type: See CtxEnum for options.

  Returns:
    An _ast.Name node.
  """
    validate_id(name_id)
    ctx = GetCtx(ctx_type)
    return _ast.Name(id=name_id,
                     ctx=ctx)


# def keyword(arg, value):
#  return _ast.keyword(arg, _ast.Constant(value=value,   ctx = GetCtx(CtxEnum.LOAD)))


def Not():
    return _ast.Not()


def NotEq():
    return _ast.NotEq()


def NotIn():
    return _ast.NotIn()


def CreateNone(value):
    if value != 'None':
        raise ValueError('Invalid value for None')
    return _ast.Constant(value=None)
def Num(number):
    """Creates an _ast.Constant node."""
    if not isinstance(number, str):
        raise ValueError(f'number must be a str to support bases')
    base = _extract_base(number)
    if base != 10:
        value = int(number, base)
    elif number[0] == '+' or number[0]=='-':
        value = int(number, base)
    elif number.isdigit():
        value = int(number, base)
    else:
        try:
            value = float(number)
        except ValueError:
            raise ValueError(f'Invalid number type')
    result =  _ast.Constant(value=value)

    result.default_quote = "'" # TODO this is not clean -- as this is not really necessary
    result.base = base
    return result


def _extract_base(number):
    if str(number).startswith('0b'):
        base = 2
    elif str(number).startswith('0o'):
        base = 8
    elif str(number).startswith('0x'):
        base = 16
    else:
        base = 10
    return base


def Bool(boolean):
    """Creates an _ast.Constant node."""
    return _ast.Constant(bool(boolean))

def Or():
    return _ast.Or()


def Pass():
    """Creates an _ast.Pass node."""
    return _ast.Pass()


def Pow():
    return _ast.Pow()


def Return(value, quote_type=None):

    if isinstance(value, int):
        value_node = Num(str(value))
    elif isinstance(value, str):
        if quote_type is None:
            raise ValueError('Must provite quote type when creating a Return node weith type str..')
        value_node = Str(value)
        value_node.default_quote = quote_type
    elif isinstance(value, _ast.AST):
        return _ast.Return(value)
    else:
        raise ValueError('Invalid return value')
    result = _ast.Return(value=value_node)
    return result

def RShift():
    return _ast.RShift()


def Set(*items):
    """Creates an _ast.Set node.

  Args:
    *items: The items in the set.

  Returns:
    An _ast.Set node.
  """
    return _ast.Set(elts=list(items))


def SetComp(left_side, for_part, in_part, *ifs):
    """Creates _ast.SetComp nodes.

  'left_side' for 'for_part' in 'in_part' if 'ifs'

  Args:
    left_side: leftmost side of the expression.
    for_part: The part after '[left_side] for '
    in_part: The part after '[left_side] for [for_part] in '
    *ifs: Any if statements that come at the end.

  Returns:
    {_ast.SetComp}
  """
    left_side = _WrapWithName(left_side, ctx_type=CtxEnum.LOAD)
    for_part = _WrapWithName(for_part, ctx_type=CtxEnum.STORE)
    in_part = _WrapWithName(in_part, ctx_type=CtxEnum.LOAD)
    return _ast.SetComp(
        elt=left_side,
        generators=[comprehension(for_part, in_part, False, *ifs)])


def Slice(lower=None, upper=None, step=None):
    return _ast.Slice(lower=lower, upper=upper, step=step)


def Str(s):
    """Creates an _ast.Str node."""
    #  return _ast.Str(s=s)
    return _ast.Constant(s=s)


def Starred(s):
    """Creates an _ast.Starred node."""
    #  return _ast.Str(s=s)
    return _ast.Starred(value=s, ctx=GetCtx(CtxEnum.LOAD))


def Sub():
    return _ast.Sub()


def Subscript(value, upper=None, lower=None, step=None, ctx=CtxEnum.LOAD):
    value = _WrapWithName(value, ctx)
    new_bound = [None,None,None]
    for index, item in enumerate([upper, lower, step]):
        if item is not None:
            if not isinstance(item, int):
                raise ValueError('Subscript must be an int')
            item = _WrapWithName(item, ctx_type=CtxEnum.LOAD)
            new_bound[index] = item
    return _ast.Subscript(
        value=value, slice=Slice(new_bound[0], new_bound[1], new_bound[2]), ctx=GetCtx(ctx))


class Comment(_ast.stmt):
    def __init__(self, comment):
        super(Comment ,self).__init__()
        if not comment.startswith('#'):
            raise ValueError('Comment must start with #')
        self._fields = []
        self.comment = comment[1:]

    @property
    def source_comment(self):
        if self.comment is not None:
            return f'#{self.comment}'

def Raise(exception=None, cause=None):
    if exception is not None and  not isinstance(exception, (_ast.Name, _ast.Call)):
        raise ValueError('Raise exception must be a Name or Call')
    if cause is not None and  not isinstance(cause, (_ast.Name)):
        raise ValueError('cause exception must be a Name')
    result = _ast.Raise(exc=exception, cause=cause)
    return result

def Tuple(items, **kwargs):
    """Creates an _ast.Tuple node.

  Automatically adjusts inner ctx attrs.

  Args:
    *items: The items in the list.
    **kwargs: Only recognized kwarg is 'ctx_type', which controls the
      ctx type of the list. See CtxEnum.

  Returns:
    An _ast.Tuple node.
  """
    if not isinstance(items, list):
        raise ValueError('items in tuple should be a list')
    ctx_type = kwargs.pop('ctx_type', CtxEnum.LOAD)

    new_items = []
    for item in items:
        if isinstance(item, (str, int, ast.Constant)):
            new_items.append(_WrapWithName(item))
        else:
            raise NotImplementedError('Tuple item type not implemented')

    for item in new_items:
        if isinstance(item, _ast.Name):
            item.ctx = GetCtx(ctx_type)
        elif isinstance(item, _ast.Attribute):
            name_node = _LeftmostNodeInDotVar(item)
            name_node.ctx = GetCtx(ctx_type)
    ctx = GetCtx(ctx_type)
    return _ast.Tuple(elts=new_items,
                      ctx=ctx)


def Try(body, except_handlers=[], finalybody=[], orelse=[]):
    finalbody = FormatAndValidateBody(finalybody)

    if (not except_handlers) or (not isinstance(except_handlers, list)):
        raise ValueError('Exception handlers must be a non-empty list')
    return _ast.Try(body=body, handlers=except_handlers, finalbody=finalbody, orelse=orelse)

def For(target, iter, body, orelse=[]):
    return ast.For(target, iter, body, orelse=[])


def UAdd():
    return _ast.UAdd()


def UnaryOp(operator, operand):
    """Operator literals ('not') also accepted."""
    if not isinstance(operator, _ast.AST):
        operator = UnaryOpMap(operator)
    return _ast.UnaryOp(op=operator, operand=operand)


def USub():
    return _ast.USub()


def withitem(name, optional_vars=None):
    if isinstance(optional_vars, str):
        optional_vars = Name(optional_vars, ctx_type=CtxEnum.STORE)
    elif optional_vars and not isinstance(optional_vars, (ast.Tuple, ast.List)):
        raise ValueError('withitem must be str, tuple, or list')
    return _ast.withitem(Name(name), optional_vars)


def With(withitems, body):
    if not isinstance(body, list):
        raise ValueError('With-body must be a list')

    if not isinstance(withitems, list):
        raise ValueError('withitems must be a list')

    body = FormatAndValidateBody(body)
    #    if as_part:
    #        ChangeCtx(as_part, CtxEnum.STORE)

    return _ast.With(items=withitems,
                     body=body, type_comment=None)

def FormattedValue(value, conversion=-1, format_spec=None):
    if conversion !=-1 or format_spec:
        raise NotImplementedError('conversion and format_spec not supported yet')
    if not isinstance(value, _ast.Name):
        raise NotImplementedError('FormattedValue value must be a Name')
    return _ast.FormattedValue(value=value, conversion=conversion, format_spec=format_spec)


def JoinedStr(values):
    for value in values:
        if not isinstance(value, (ast.Constant, ast.FormattedValue)):
            raise ValueError('JoinedStr values must be Constant or FormattedValue')
    return _ast.JoinedStr(values=values)

###############################################################################
# Other Creators
###############################################################################


def GetCtx(ctx_type):
    """Creates Load, Store, Del, and Param, used in the ctx kwarg."""
    if ctx_type == CtxEnum.LOAD:
        return _ast.Load()
    elif ctx_type == CtxEnum.STORE:
        return _ast.Store()
    elif ctx_type == CtxEnum.DEL:
        return _ast.Del()
    elif ctx_type == CtxEnum.PARAM:
        return _ast.Param()
    raise InvalidCtx('ctx_type {} isn\'t a valid type'.format(ctx_type))


def UnaryOpMap(operator):
    """Maps operator strings for unary operations to their _ast node."""
    op_dict = {
        '+': _ast.UAdd,
        '-': _ast.USub,
        'not': _ast.Not,
        '~': _ast.Invert,
    }

    return op_dict[operator]()


def BinOpMap(operator):
    """Maps operator strings for binary operations to their _ast node."""
    op_dict = {
        '+': _ast.Add,
        '-': _ast.Sub,
        '*': _ast.Mult,
        '**': _ast.Pow,
        '/': _ast.Div,
        '//': _ast.FloorDiv,
        '%': _ast.Mod,
        '<<': _ast.LShift,
        '>>': _ast.RShift,
        '|': _ast.BitOr,
        '&': _ast.BitAnd,
        '^': _ast.BitXor,
    }

    return op_dict[operator]()


def BoolOpMap(operator):
    """Maps operator strings for boolean operations to their _ast node."""
    op_dict = {
        'and': _ast.And,
        'or': _ast.Or,
    }

    return op_dict[operator]()


def CompareOpMap(operator):
    """Maps operator strings for boolean operations to their _ast node."""
    op_dict = {
        '==': _ast.Eq,
        '!=': _ast.NotEq,
        '<': _ast.Lt,
        '<=': _ast.LtE,
        '>': _ast.Gt,
        '>=': _ast.GtE,
        'is': _ast.Is,
        'is not': _ast.IsNot,
        'in': _ast.In,
        'not in': _ast.NotIn,
    }

    return op_dict[operator]()


def VarReference(*parts, **kwargs):
    """By this we mean either a single name string or one or more Attr nodes.

  This is used whenever we have things like 'a' or 'a.b' or 'a.b.c'.

  Args:
    *parts: The parts that should be dot-separated.
    **kwargs: Only recognized kwarg is 'ctx_type', which controls the
      ctx type of the list. See CtxEnum.

  Raises:
    ValueError: When no parts are specified.

  Returns:
    An _ast.Name node or _ast.Attribute node
  """
    ctx_type = kwargs.pop('ctx_type', CtxEnum.LOAD)

    if not parts:
        raise ValueError('Must have at least one part specified')
    if len(parts) == 1:
        if isinstance(parts[0], str):
            return _ast.Name(id=parts[0], ctx=GetCtx(ctx_type))
        return parts[0]
    return _ast.Attribute(
        value=VarReference(*parts[:-1], **kwargs),
        attr=parts[-1],
        ctx=GetCtx(ctx_type))


