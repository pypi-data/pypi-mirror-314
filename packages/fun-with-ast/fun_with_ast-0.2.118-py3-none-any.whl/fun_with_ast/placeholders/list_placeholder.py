from fun_with_ast.manipulate_node.syntax_free_line_node import SyntaxFreeLine
from fun_with_ast.placeholders.composite import CompositePlaceholder
from fun_with_ast.placeholders.node import NodePlaceholder
from fun_with_ast.source_matchers.exceptions import BadlySpecifiedTemplateError


class ListFieldPlaceholder(CompositePlaceholder):
    """Placeholder for a field which is a list of child nodes."""

    def __init__(self, field_name,
                 before_placeholder=None, after_placeholder=None,
                 prefix_placeholder=None,
                 exclude_first_before=False,
                 exclude_last_after=False):
        """Initializes a field which is a list of child nodes.

        Args:
          field_name: {str} The name of the field
          before_placeholder: {TextPlaceholder} Text to expect to come before the
            child element.
          after_placeholder: {TextPlaceholder} Text to expect to come after the
            child element.
          prefix_placeholder: {TextPlaceholder} Text to expect to come before
            the list.
          exclude_first_before: {bool} Whether to exclude the last
            before_placholder, used for SeparatorListFieldPlaceholder.
        """
        super(ListFieldPlaceholder, self).__init__()
        self.field_name = field_name
        self.prefix_placeholder = prefix_placeholder
        self.before_placeholder = before_placeholder
        self.after_placeholder = after_placeholder
        self.exclude_first_before = exclude_first_before
        self.exclude_last_after = exclude_last_after
        self.matched_before = []
        self.matched_after = []

    def _GetBeforePlaceholder(self, index):
        if index < len(self.matched_before):
            return self.matched_before[index]
        new_placeholder = self.before_placeholder.Copy()
        self.matched_before.append(new_placeholder)
        return new_placeholder

    def _GetAfterPlaceholder(self, index):
        if index < len(self.matched_after):
            return self.matched_after[index]
        new_placeholder = self.after_placeholder.Copy()
        self.matched_after.append(new_placeholder)
        return new_placeholder

    def GetValueAtIndex(self, values, index, is_last_node=False):
        """Gets the set of node in values at index, including before and after."""
        elements = []
        child_value = values[index]
        if isinstance(child_value, SyntaxFreeLine):
            return [NodePlaceholder(child_value)]
        if (self.before_placeholder and
                not (self.exclude_first_before and index == 0)):
            before_index = index - 1 if self.exclude_first_before else index
            elements.append(self._GetBeforePlaceholder(before_index))
        elements.append(NodePlaceholder(child_value))
        if self.after_placeholder and not (self.exclude_last_after and is_last_node):
            elements.append(self._GetAfterPlaceholder(index))
        return elements

    def GetElements(self, node):
        field_value = getattr(node, self.field_name) or []
        elements = []
        if self.prefix_placeholder and field_value:
            elements.append(self.prefix_placeholder)
        for i in range(len(field_value)):
            elements.extend(self.GetValueAtIndex(field_value, i, is_last_node= i == len(field_value) - 1))
        return elements

    def Validate(self, node):
        field_value = getattr(node, self.field_name)
        if field_value and not isinstance(field_value, (list, tuple)):
            raise BadlySpecifiedTemplateError(
                'Field {} of node {} is a not list, so please use a FieldPlaceholder'
                'instead of a ListFieldPlaceholder'.format(self.field_name, node))

    def __repr__(self):
        return ('ListFieldPlaceholder for field "{}" with before placeholder "{}"'
                'and after placeholder "{}"'.format(
            self.field_name, self.before_placeholder,
            self.after_placeholder))

class SeparatedListFieldPlaceholder(ListFieldPlaceholder):

    def __init__(self, field_name, before_separator_placeholder=[],
                 after__separator_placeholder=[],
                 exclude_last_after=False):
        super(SeparatedListFieldPlaceholder, self).__init__(
            field_name, before_placeholder=before_separator_placeholder,
            after_placeholder=after__separator_placeholder,
            exclude_first_before=True,
            exclude_last_after=exclude_last_after)

