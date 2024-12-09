import json
from blockly_executor import ExtException
from blockly_executor.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.blocks.procedures_defreturn import ProceduresDefreturn
from .workspace import Workspace


class WorkspaceJson(Workspace):
    version = 'json'

    def __init__(self, data, name, logger, *, own=None):
        super().__init__(data, name, logger, own=own)
        try:
            self.blocks = data['blocks']['blocks']
        except (KeyError, TypeError):
            self.blocks = []

        self.read_variables()

    def read_procedures_and_functions(self):
        self.functions = {}
        _handler = {
            'procedures_defreturn': ProceduresDefreturn,
            'procedures_defnoreturn': ProceduresDefnoreturn
        }
        for node in self.blocks:
            if node['type'] in _handler:
                name = node['fields']['NAME']
                self.functions[name] = (_handler[node['type']], node)

    def init_procedure_block(self, executor, name):
        block_class, block_node = self.functions[name]
        return block_class.init(executor, name, block_node, logger=self.logger)

    def read_variables(self):
        self.variables = {}
        for var in self.data.get('variables', []):
            self.variables[var['id']] = var['name']
        return self.variables

    @classmethod
    def read_child_block(cls, node):
        child = None
        if node:
            if isinstance(node, dict):
                child = node.get('block')
                if child is None:
                    return node.get('shadow')
            elif isinstance(node, list):  # root
                for elem in node:
                    if elem['type'] not in ['procedures_defreturn', 'procedures_defnoreturn']:
                        return elem

        return child

    @classmethod
    def find_child_blocks(cls, node):
        blocks = []
        if node:
            if isinstance(node, dict):
                child = node.get('block')
                if child is None:
                    child = node.get('shadow')
                if child is not None:
                    blocks.append(child)
            elif isinstance(node, list):  # root
                blocks = node
        return blocks

    @classmethod
    def find_field_by_name(cls, node, name):
        try:
            return node['fields'][name]
        except (KeyError, TypeError):
            return None

    @classmethod
    def find_statement_by_name(cls, node, name):
        return cls.find_input_by_name(node, name)

    @classmethod
    def find_next_statement(cls, node):
        try:
            return node['next']
        except (KeyError, TypeError):
            return None

    @classmethod
    def find_mutations(cls, node):
        return node.get('extraState')

    @classmethod
    def find_mutation_by_name(cls, node, name, default=None):
        mutation = cls.find_mutations(node)
        if mutation is not None:
            return mutation.get(name, default)
        return default

    @classmethod
    def set_mutation_value(cls, node, mutation_name, mutation_value):
        raise NotImplementedError()

    @classmethod
    def find_mutation_args(cls, node):
        mutation = cls.find_mutations(node)
        if mutation is not None:
            return mutation.get('params')
        return None

    @classmethod
    def find_inputs(cls, node):
        return node.get('inputs', {})

    @classmethod
    def find_input_by_name(cls, node, name):
        try:
            return node['inputs'][name]
        except (KeyError, TypeError):
            return None

    def find_fields(self, node, result=None):
        result = result if result else {}
        fields = node.get('fields')
        if fields is not None:
            for _param_name in fields:
                _value = fields[_param_name]
                if isinstance(_value, dict):
                    result[_param_name] = self.variables[_value['id']]
                else:
                    result[_param_name] = _value
        return result

    async def execute_inputs(self, block, node, path, context, block_context):
        inputs = node.get('inputs')
        if inputs is not None:
            for name in inputs:
                if block.statement_inputs and name in block.statement_inputs:
                    continue
                if name not in block_context:
                    block_context[name] = await block.execute_all_next(
                        inputs[name], f'{path}.{name}', context, block_context)

    @classmethod
    def set_field_value(cls, node, field_name, field_value):
        if 'fields' not in node:
            node['fields'] = {}
        node['fields'][field_name] = field_value

    @classmethod
    def delete_field(cls, node, field_name):
        raise NotImplementedError()

    def get_raw(self):
        return self.data
        # return json.dumps(self.data, ensure_ascii=False, indent=2)

    def root_append_block(self, block):
        self.blocks.append(block)

    def root_delete_block(self, block):
        raise NotImplementedError()

    @classmethod
    def set_input(cls, block, input_name, value):
        try:
            if value:
                block['inputs'][input_name] = {'block': value}
            else:
                block['inputs'].pop(input_name, {})
        except Exception as err:
            raise ExtException(parent=err)

    @classmethod
    def delete_input(cls, block, input_name):
        try:
            block['inputs'].pop(input_name, None)
        except Exception as err:
            raise ExtException(parent=err)

    def gluer_result_update(self, base, changes, errors, warnings):
        self.data['gluer'] = self._gluer_result(base, changes, errors, warnings)
        return self.get_raw()

    def gluer_result_read(self):
        return self.data.get('gluer', {})
