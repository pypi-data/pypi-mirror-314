from abc import ABCMeta, abstractmethod

from blockly_executor.blocks.root import Root


class Workspace:
    __metaclass__ = ABCMeta
    version = None

    def __init__(self, data, name, logger, *, own=None):
        self.name = name
        self.own = own
        self.data = data
        self.blocks = None
        self.functions = None
        self.variables = None
        self.read_variables()
        self.logger = logger

    def get_start_block(self, executor, endpoint, context):
        # стартуем с функции
        self.read_procedures_and_functions()
        if endpoint:
            if endpoint not in self.functions:
                context.status = 'error'
                context.result = f'not found endpoint {endpoint}'
                return context
            block = self.init_procedure_block(executor, endpoint)
        else:
            if 'main' in self.functions:
                block = self.init_procedure_block(executor, 'main')
            else:
                block = Root.init(executor, '', self.blocks, logger=self.logger)
        return block

    @abstractmethod
    def gluer_result_read(self):
        raise NotImplementedError()

    @abstractmethod
    def init_procedure_block(self, executor, name):
        raise NotImplementedError()

    @abstractmethod
    def read_procedures_and_functions(self):
        raise NotImplementedError()

    @abstractmethod
    def read_variables(self):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def read_child_block(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_child_blocks(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_field_by_name(cls, node, name):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_statement_by_name(cls, node, name):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_next_statement(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_mutation_by_name(cls, node, name, default=None):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_mutations(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_mutation_args(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_inputs(cls, node) -> dict:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_input_by_name(cls, node, name):
        raise NotImplementedError()

    @abstractmethod
    def find_fields(self, node, result=None):
        raise NotImplementedError()

    @abstractmethod
    async def execute_inputs(self, block, node, path, context, block_context):
        raise NotImplementedError()

    def create_index_of_block(self):
        index = {}
        for node in self.find_child_blocks(self.blocks):
            self._create_index_of_block(index, (None, None), (None, None), node)
        return index

    def _create_index_of_block(self, index, parent, previous, node):
        inputs = self.find_inputs(node)
        block_id = node.get('id')
        block_type = node.get('type')
        index[block_id] = dict(
            parent=parent,
            type=block_type,
            node=node,
            inputs={},
            previous=previous,
            next=None
        )
        for input_name in inputs:
            child_input = inputs[input_name]
            child_node = self.read_child_block(child_input)
            if child_node:
                parent_child = (input_name, block_id)
                index[block_id]['inputs'][input_name] = child_node.get('id')
                self._create_index_of_block(index, parent_child, (None, None), child_node)
            else:
                index[block_id]['inputs'][input_name] = None
        child_input = self.find_next_statement(node)
        if child_input:
            child_node = self.read_child_block(child_input)
            if child_node:
                parent_child = ('next', block_id)
                index[block_id]['next'] = child_node.get('id')
                self._create_index_of_block(index, parent, parent_child, child_node)

    @classmethod
    @abstractmethod
    def set_field_value(cls, block, field_name, field_value):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def delete_field(cls, node, field_name):
        raise NotImplementedError()

    @abstractmethod
    def get_raw(self):
        raise NotImplementedError()

    def root_append_block(self, block):
        raise NotImplementedError()

    def root_delete_block(self, block):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def set_input(cls, block, input_name, value):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def delete_input(cls, block, input_name):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def set_mutation_value(cls, node, mutation_name, mutation_value):
        raise NotImplementedError()

    @abstractmethod
    def gluer_result_update(self, base, changes, errors, warnings):
        raise NotImplementedError()

    @staticmethod
    def _gluer_result(base, changes, errors, warnings):
        return dict(
            base=base,
            changes=changes,
            errors=errors,
            warnings=warnings
        )
