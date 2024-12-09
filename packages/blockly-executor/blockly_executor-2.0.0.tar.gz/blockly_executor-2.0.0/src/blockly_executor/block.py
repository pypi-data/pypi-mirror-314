import logging
from typing import TYPE_CHECKING
from uuid import uuid4

from blockly_executor import ExtException
from blockly_executor.exceptions import StepForward, DeferredOperation, ServiceException, ErrorInBlock

if TYPE_CHECKING:
    from .executor import BlocklyExecutor
    from .workspace import Workspace


class Block:
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    _result = '_result'
    statement_inputs = None

    def __init__(self, executor, **kwargs):
        self.executor: BlocklyExecutor = executor
        self.workspace: Workspace = executor.workspace
        self.block_id = None
        self.logger = kwargs.get('logger', logging)

    @classmethod
    def init(cls, executor, name, node, **kwargs):
        self = cls(executor, **kwargs)
        self.name = name
        self.node = node
        return self

    def _check_step(self, context, block_context):
        if context.debug_mode:
            if context.is_next_step:
                if context.debug_mode == 'step':
                    raise StepForward(self.block_id, context, block_context, self.executor.workspace.name)
                else:
                    context.current_block = self.block_id
                    context.current_workspace = self.executor.workspace.name
            if self.block_id == context.current_block and context.current_workspace == self.executor.workspace.name:
                if self.executor.current_algorithm_breakpoints:
                    if self.block_id in self.executor.current_algorithm_breakpoints and context.is_next_step:
                        raise StepForward(self.block_id, context, block_context, self.executor.workspace.name)
                if context.debug_mode == 'step':
                    if context.is_next_step is False:  # встаем на этом шаге
                        raise StepForward(self.block_id, context, block_context, self.executor.workspace.name)
                    else:
                        context.is_next_step = True  # встаем на следующем шаге

    async def _before_execute(self, node, path, context, block_context):
        self.block_id = node.get('id')
        self.block_type = node.get('type')
        block_context['__id'] = self.block_id
        block_context['__path'] = f'{path}.{self.block_type}'
        # context.init_block_context(block_context, self.block_id, path)
        pass

    async def execute_all_next(self, node, path, context, block_context, statement=False):
        statement_number = 0
        child_context = context.get_child_context(block_context)
        result = None
        while True:
            if statement:
                try:
                    _child_context = child_context[
                        str(statement_number)]  # приводим к строке ключ потому что в json сохраняем
                except KeyError:
                    child_context[str(statement_number)] = {}
                    _child_context = child_context[str(statement_number)]
            else:
                _child_context = child_context

            child = self.executor.workspace.read_child_block(node)

            next_node = None

            if child is not None:
                next_node = self.workspace.find_next_statement(child) if statement else None
                if '__result' not in _child_context:
                    result = await self.execute_child_block(child, block_context['__path'], context, _child_context)
                else:
                    self.logger.debug(f'{child.get("id")} skip')
            else:
                result = None
                # raise Exception(f'{self.__class__.__name__} не хватает блока. path: {path} ')

            if next_node:
                node = next_node
                # помечаем блок который выполнили
                _child_context['__result'] = True
                statement_number += 1
            else:
                context.clear_child_context(block_context)
                return result

    async def _execute(self, node, path, context, block_context):
        return await self.execute_all_next(node, path, context, block_context)
        pass

    async def execute_child_block(self, child_node, path, context, child_block_context):
        block_type = child_node.get('type')
        _class = self.executor.get_block_class(block_type)
        try:
            return await _class(self.executor, logger=self.logger).execute(
                child_node, path, context, child_block_context)
        except (ServiceException, ErrorInBlock) as err:
            raise err from err
        except ExtException as err:
            raise err from err
        except Exception as err:
            raise ExtException(message='Ошибка в блоке',
                               detail=f'{block_type}: {err}',
                               parent=err,
                               dump=dict(
                                   block=self.block_id,
                                   algorithm=self.executor.workspace.name
                               ),
                               skip_traceback=1)

    async def execute(self, node, path, context, block_context):
        try:
            await self._before_execute(node, path, context, block_context)
            self.logger.debug(f'{self.full_name} begin execute id="{self.block_id}"')
            return await self._execute(node, path, context, block_context)
        except ServiceException as err:
            raise err from err

    @property
    def full_name(self):
        # return f'{self.block_id}'
        return f'{self.__class__.__name__}'

    def command_send(self, command_name, command_params, context, block_context):
        command_uuid = str(uuid4())
        block_context['__deferred'] = command_uuid
        context.commands.append(
            {
                'name': command_name,
                'params': command_params,
                'uuid': command_uuid
            }
        )
        raise DeferredOperation(command_uuid, context, block_context)

    @staticmethod
    def command_sended(block_context):
        return '__deferred' in block_context

    def command_get_result(self, command_uuid):
        try:
            commands_result_data = self.executor.commands_result.pop(command_uuid)
        except KeyError:
            raise ExtException(
                message='Command no response',
                detail=f'block {self.full_name} command_uuid {command_uuid}'
            )
        try:
            _status = commands_result_data['status']
            _data = commands_result_data['result']
        except KeyError:
            raise ExtException(
                message='Bad format command result',
                detail=f'block {self.full_name} command_uuid {command_uuid}',
                dump={'result': commands_result_data}
            )
        if _status.upper() == 'COMPLETE':
            return _data
        if _status.upper() == 'ERROR':
            if isinstance(_data, dict):
                raise ExtException(parent=_data)
            else:
                raise Exception(_data)
        raise ExtException(
            message='Not supported command result type',
            detail=f'block {self.full_name} result type {_status}',
        )

    @classmethod
    def defined_variable(cls, context, name):
        try:
            return name in context.debug['__thread_vars'] or name in context.variables
        except KeyError:
            return False

    @classmethod
    def get_variable(cls, context, name):
        try:
            return context.block_context['__thread_vars'][name]
        except KeyError:
            return context.variables[name]

    def set_variable(self, context, name, value):
        if self.executor.multi_thread_mode:
            context.block_context['__thread_vars'][name] = value
        context.variables[name] = value
