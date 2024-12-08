import ast

from fun_with_ast.manipulate_node.body_manipulator import BodyManipulator


class IfManipulatorConfig():
    def __init__(self, body_index: int, location_in_body_index: int):
        self._body_index = body_index
        self._location_in_body_index = location_in_body_index
    @property
    def body_index(self) -> int:
        return self._body_index

    @body_index.setter
    def body_index(self, v: int) -> None:
        self._body_index = v
    @property
    def location_in_body_index(self) -> int:
        return self._location_in_body_index

    @location_in_body_index.setter
    def location_in_body_index(self, v: int) -> None:
        self._location_in_body_index = v

class ManipulateIfNode():
    def __init__(self, node, config: IfManipulatorConfig):
        self.node = node
        self.config = config
        if not isinstance(node, ast.If):
            raise ValueError('node must be ast.If')
        is_elif = True if hasattr(node, 'is_elif') and node.is_elif else False
        self.is_elif = is_elif


    def add_nodes(self, nodes: list):
        self._validate_rules_for_insertion(nodes)
        nodes_to_inject = nodes
        body_block_to_manipulate = self._get_block(self.config.body_index)
        body_manipulator = BodyManipulator(body_block_to_manipulate)
        body_manipulator.inject_node(nodes_to_inject, self.config.location_in_body_index)

    def get_body_orelse_source(self):
        if self.config.body_index ==0:
            source = self.node.node_matcher.body_placeholder.GetSource(self.node)
        elif self.config.body_index ==1:
            source = self.node.node_matcher.orelse_placeholder.GetSource(self.node)
        else:
            raise ValueError('Illegal body index')
        return source


    def _validate_rules_for_insertion(self, nodes):
        if len(nodes) > 2:
            raise NotImplementedError("only two node can be added at a time")
        if self.config.location_in_body_index > len(self.node.body):
            raise ValueError("location is out of range")
        if self.config.location_in_body_index < 0:
            raise ValueError("location must be positive")
        if self.config.body_index < 0:
            raise ValueError('Illegal body index')
        if self.config.body_index > 1:
            raise NotImplementedError('elif not supported yet')
        if self.config.body_index == 1:
            if self.is_elif:
                if not isinstance(self.node.orelse[0], ast.If):
                    raise ValueError('orelse is not ast.If and is_elif is True')
                if len(self.node.orelse) > 1:
                    raise ValueError('orelse length is larger than 1 and is_elif is True')
        if self.config.body_index == 1 and not self.node.orelse:
            raise ValueError('No oresle in If but index body is 1')

    def _get_block(self, body_index):
        while True:
            if body_index < 0:
                raise ValueError('Illegal body index')
            if body_index == 0:
                return self.node.body
            if body_index == 1 and not self.node.orelse:
                ValueError('No oresle in If')
            if body_index == 1:
                if self.is_elif:
                    return self.node.orelse[0].body
                return self.node.orelse
            body_index -= 2

    def _set_block(self, body_index, new_block):
        if body_index < 0:
            raise ValueError('Illegal body index')
        if body_index > 1:
            raise NotImplementedError('elif not supported yet')
        if body_index == 0:
            self.node.body = new_block
        if body_index == 1 and not self.node.orelse:
            ValueError('No oresle in If')
        if body_index == 1:
            if self.is_elif:
                self.node.orelse[0].body = new_block
            self.node.orelse = new_block


    def _get_nodes_to_inject(self, nodes):
        return nodes[0]

    def rerplace_body(self, source):
        if not source.endswith('\n'): # we will add new line at the end of the when replacing body
            source += '\n'
        new_body = self._prepare_body_nodes(source)

        if self.config.body_index == 0:
            self.node.body = new_body
            new_body_source = self.node.node_matcher.body_placeholder._match(self.node, source)
            if not new_body_source.endswith('\n'):
                self.node.node_matcher.add_newline_to_source()
            return new_body_source
        elif self.config.body_index == 1:
            self.node.orelse = new_body
            new_else_node_source = self.node.node_matcher.orelse_placeholder._match(self.node, source)
            return new_else_node_source
        else:
            raise ValueError('Illegal body index')

    def _prepare_body_nodes(self, source):
        body_block_to_manipulate = self._get_block(self.config.body_index)
        body_manipulator = BodyManipulator(body_block_to_manipulate)
        new_body = body_manipulator.replace_body(source)
        return new_body


