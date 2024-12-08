from fun_with_ast.placeholders.args import ArgsDefaultsPlaceholder


class KwOnlyArgsPlaceholder(ArgsDefaultsPlaceholder):
    """Placeholder to handle args and defaults for _ast.argument.

    These fields behave differently than most other fields and therefore
    don't fall into any of the other placeholders. Therefore, we have to define
    a custom placeholder.
    """

    def __init__(self, kwonlyarg_separator_placeholder, kw_only_defaults_seperator_placeholder):
        super(KwOnlyArgsPlaceholder, self).__init__(kwonlyarg_separator_placeholder,
                                                    kw_only_defaults_seperator_placeholder)

    def _GetArgsKwargs(self, node):
        if len(node.kwonlyargs) != len(node.kw_defaults):
            raise ValueError('kwonlyargs and kw_defaults must be of equal length')
        kwonlyargs_with_defaults = []
        kwonlyargs = []
        for kwonlyarg, kw_default in zip(node.kwonlyargs, node.kw_defaults):
            if kw_default is None:
                kwonlyargs.append(kwonlyarg)
            else:
                kwonlyargs_with_defaults.append((kwonlyarg, kw_default))
        return kwonlyargs, kwonlyargs_with_defaults
