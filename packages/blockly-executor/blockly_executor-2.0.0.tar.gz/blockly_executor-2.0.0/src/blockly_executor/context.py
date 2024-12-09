from uuid import uuid4

from blockly_executor import Action
from blockly_executor import ExtException
from blockly_executor import Helper, ArrayHelper
from blockly_executor.exceptions import LimitCommand
from .context_props import ContextProps


class Context(ContextProps):
    def __init__(self):
        super().__init__()
        self.uid = None
        self.data = {}
        self.action = Action()
        self.current_thread = None

        self.is_deferred = False
        self.is_next_step = False
        self.deferred_result = None
        self.limit_commands = 25

    @classmethod
    async def init(cls, *, uid=None, debug_mode=None, current_block=None, current_workspace=None, workspace_name=None,
                   data=None, **kwargs):

        self = cls()
        self.uid = uid if uid else str(uuid4())
        self.data = data if data else {}
        self.debug_mode = debug_mode
        self.current_block = current_block
        self.current_workspace = current_workspace if current_workspace else workspace_name
        self.workspace_name = workspace_name
        self.is_next_step = True if not current_block and self.debug_mode else None
        return self

    def init_deferred(self, block_context):
        """
        Контекст для отложенного исполнения

        :param block_context:
        :return:
        """
        _self = self.__class__()
        _self.block_context = block_context['block_context']
        _self.is_deferred = True
        _self.variables = self.variables
        _self.deferred = self.deferred
        return _self

    def init_nested(self, block_context, workspace_name):
        """
        Контекст для запуска вложенного алгоритма
        :param workspace_name:
        :param block_context:
        :return:
        """
        _self = self.__class__()
        _self.data = block_context.get('_child', {})
        _self.workspace_name = workspace_name

        _self.is_deferred = self.is_deferred
        _self.debug_mode = self.debug_mode
        _self.current_block = self.current_block
        _self.current_workspace = self.current_workspace
        _self.is_next_step = self.is_next_step
        return _self

    def to_parallel_dict(self):
        return dict(
            variables=self.variables,
            block_context=self.block_context,
        )

    def to_dict(self):
        return self.data

    def to_result(self):
        res = dict(
            uid=self.uid,
            result=self.result,
            status=self.status,
            commands=self.commands,
        )
        if self.debug_mode:
            res['current_variables'] = self.current_variables
            res['current_block'] = self.current_block
            res['current_workspace'] = self.current_workspace

        return res

    def set_next_step(self, block_id=None):
        if self.debug_mode == 'step':
            if block_id is None or (block_id == self.current_block and self.current_workspace == self.workspace_name):
                self.is_next_step = True

    def set_step(self, block_id):
        if self.debug_mode:
            # if self.executor.current_block != self.block_id:
            self.is_next_step = False
            self.current_block = block_id
            self.current_workspace = self.workspace_name

    @staticmethod
    def get_child_context(block_context):
        try:
            child_context = block_context['__child']
        except KeyError:
            child_context = {}
            block_context['__child'] = child_context
        return child_context

    @staticmethod
    def clear_child_context(block_context, result=None, delete_children=True):
        if delete_children:
            block_context.pop('__child', None)

    def copy(self):
        _self = Context()
        _self.deferred = self.deferred
        _self.block_context = Helper.copy_via_json(self.block_context)
        return _self

    def add_deferred(self, deferred_exception):

        _local_context = deferred_exception.args[2]
        _operation_context = deferred_exception.args[1]
        try:
            i = ArrayHelper.find_by_key(self.deferred, _local_context['__deferred'], key_field='__deferred')
        except KeyError:
            self.deferred.append({})
            i = len(self.deferred) - 1

        self.deferred[i] = {
            '__deferred': _local_context['__deferred'],
            'block_context': Helper.copy_via_json(_operation_context.block_context)
        }

        try:
            i = ArrayHelper.find_by_key(self.commands, _local_context['__path'], key_field=2)
        except KeyError:
            self.commands.append([])
            i = len(self.commands) - 1
        self.commands[i] = deferred_exception.to_command()

    def check_command_limit(self):
        if len(self.commands) >= self.limit_commands:
            raise LimitCommand()

    def set_command_limit(self, debug_mode=None):
        self.limit_commands = 1 if debug_mode else 25

    def variable_scope_add(self, block_context, params):
        if '_variable_scope' in block_context:
            self.current_variable_scope = block_context['_variable_scope']
        else:
            self.variable_scopes.append(params)
            self.current_variable_scope = len(self.variable_scopes) - 1
            block_context['_variable_scope'] = self.current_variable_scope

    def variable_scope_remove(self, block_context):
        if block_context['_variable_scope'] != self.current_variable_scope \
                or len(self.variable_scopes) - 1 != self.current_variable_scope:
            raise ExtException(
                message='Какая то фигня с variable_scope',
            )
        self.variable_scopes.pop(self.current_variable_scope)
        self.current_variable_scope -= 1

    async def workspace_read(self):
        raise NotImplementedError('Context.workspace_read')
