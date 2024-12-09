import json
import xml.etree.ElementTree as XmlTree

from blockly_executor import ExtException
from blockly_executor.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.blocks.procedures_defreturn import ProceduresDefreturn
from .workspace import Workspace


class WorkspaceXml(Workspace):
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    version = 'xml'

    def __init__(self, data, name, logger, *, own=None):
        data = self.workspace_to_tree(data)
        super().__init__(data, name, logger, own=own)
        self.blocks = self.data

    @staticmethod
    def workspace_to_tree(workspace_raw):
        XmlTree.register_namespace('', 'https://developers.google.com/blockly/xml')
        return XmlTree.fromstring(workspace_raw)

    def read_procedures_and_functions(self):
        self.functions = {}
        for node in self.data.findall("./b:block[@type='procedures_defreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = (ProceduresDefreturn, node)
            # self.functions[name] = ProceduresDefreturn.init(self.executor, name, node, logger=self.logger)

        for node in self.data.findall("./b:block[@type='procedures_defnoreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = (ProceduresDefnoreturn, node)
            # self.functions[name] = ProceduresDefnoreturn.init(self.executor, name, node, logger=self.logger)

    def init_procedure_block(self, executor, name):
        block_class, block_node = self.functions[name]
        return block_class.init(executor, name, block_node, logger=self.logger)

    def read_variables(self):
        self.variables = {}
        for node in self.data.findall("./b:variables/b:variable", self.ns):
            name = node.text
            _id = node.attrib.get('id')
            self.variables[_id] = name
        return self.variables

    @classmethod
    def read_child_block(cls, node):
        child = None
        if node:
            child = node.find('./b:block', cls.ns)
            if child is None:
                child = node.find('./b:shadow', cls.ns)
        return child

    @classmethod
    def find_child_blocks(cls, node):
        blocks = []
        if node:
            for child in node:
                if child.tag.endswith('block'):
                    blocks.append(child)
        return blocks

    @classmethod
    def find_field_by_name(cls, node, name):
        return node.find(f"./b:field[@name='{name}']", cls.ns).text

    @classmethod
    def find_statement_by_name(cls, node, name=None):
        if name:
            return node.find(f"./b:statement[@name='{name}']", cls.ns)
        else:
            return node.find(f"./b:statement", cls.ns)

    @classmethod
    def find_statements(cls, node):
        return node.find(f"./b:statement", cls.ns)

    @classmethod
    def find_next_statement(cls, node):
        return node.find(f"./b:next", cls.ns)

    @classmethod
    def find_mutations(cls, node):
        mutations = node.find(f"./b:mutation", cls.ns)
        result = {}
        if mutations is not None:
            for mutation in mutations.attrib:
                result[mutation] = mutations.get(mutation)
        return result

    @classmethod
    def find_mutation_by_name(cls, node, name, default=None):
        mutation = node.find(f"./b:mutation", cls.ns)
        if mutation is None:
            return default
        return mutation.get(name, default)

    @classmethod
    def set_mutation_value(cls, node, mutation_name, mutation_value):
        mutation = node.find(f"./b:mutation", cls.ns)
        if mutation is not None:
            mutation.set(mutation_name, mutation_value)

    @classmethod
    def find_mutation_args(cls, node):
        result = []
        args = node.findall(f'./b:mutation/b:arg', cls.ns)
        if args is not None:
            for arg in args:
                result.append(arg.get('name'))
        return result

    @classmethod
    def find_inputs(cls, node):
        result = {}
        for child in node:
            if child.tag[43:] in ['value', 'statement']:  # 43 - len namespace
                input_name = child.get('name')
                result[input_name] = child
        return result

    @classmethod
    def find_input_by_name(cls, node, name):
        return node.find(f"./b:value[@name='{name}']", cls.ns)

    def find_fields(self, node, result=None):
        result = result if result else {}
        fields = node.findall("./b:field", self.ns)

        if not fields:
            return None

        for i in range(len(fields)):
            _param_name = fields[i].get('name')
            result[_param_name] = fields[i].text
        return result

    async def execute_inputs(self, block, node, path, context, block_context):
        inputs = node.findall("./b:value", self.ns)
        if inputs is None:
            return

        for i in range(len(inputs)):
            _param_name = inputs[i].get('name')
            if _param_name not in block_context:
                block_context[_param_name] = await block.execute_all_next(
                    inputs[i], f'{path}.{_param_name}', context, block_context)

    @classmethod
    def move_block(cls, block, new_parent_block, input_name):
        try:
            input_node = cls.find_input_by_name(new_parent_block['node'], input_name)
            if not input_node:
                input_node = cls.find_statement_by_name(new_parent_block['node'], input_name)
            child_block = cls.read_child_block(input_node)
            input_node.remove(child_block)
            input_node.append(block['node'])
        except Exception as err:
            raise ExtException(parent=err)

    @classmethod
    def set_field_value(cls, node, field_name, field_value):
        field_node = node.find(f"./b:field[@name='{field_name}']", cls.ns)
        if field_node is None:
            field_node = XmlTree.SubElement(node, 'field')
            field_node.set('name', field_name)

        field_node.text = field_value

    @classmethod
    def delete_field(cls, node, field_name):
        raise NotImplementedError()

    def get_raw(self):
        return XmlTree.tostring(self.data, encoding='unicode')

    def root_append_block(self, block):
        self.blocks.append(block)

    def root_delete_block(self, block):
        raise NotImplementedError()

    @classmethod
    def set_input(cls, block, input_name, value):
        try:
            input_node = cls.find_input_by_name(block, input_name)
            if input_node is None:
                input_node = cls.find_statement_by_name(block, input_name)
            child_block = cls.read_child_block(input_node)
            if child_block is not None:
                input_node.remove(child_block)
            if value:
                input_node.append(value)
        except Exception as err:
            raise ExtException(parent=err)

    @classmethod
    def delete_input(cls, block, input_name):
        try:
            input_node = cls.find_input_by_name(block, input_name)
            if input_node is None:
                input_node = cls.find_statement_by_name(block, input_name)
            if input_node is not None:
                block.remove(input_node)
        except Exception as err:
            raise ExtException(parent=err)

    def gluer_result_update(self, base, changes, errors, warnings):
        field_node = XmlTree.SubElement(self.data, 'gluer')
        gluer = json.dumps(self._gluer_result(base, changes, errors, warnings), ensure_ascii=False)
        field_node.text = gluer
        return self.get_raw()

    def gluer_result_read(self):
        node = self.data.find(f"./b:gluer", self.ns)
        if node is not None:
            return json.loads(node.text)
        return {}
