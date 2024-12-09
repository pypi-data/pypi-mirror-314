import logging
import os
from typing import Optional

from blockly_executor import Action
from blockly_executor import ExtException
from blockly_executor import Helper
from blockly_executor.exceptions import DeferredOperation, StepForward, LimitCommand, WorkspaceNotFound
from .workspace import Workspace


class BlocklyExecutor:
    _blocks_index = None
    _blocks_class = {}

    def __init__(self, *, logger=None, plugins: Optional[list] = None, breakpoints: Optional[dict] = None, **kwargs):
        """
        :param logger: класс обеспечивающий вывод лога
        :param plugins: список модулей содержащих реализацию блоков
        :param breakpoints: список идентификаторов блоков на которых требуется остановиться в режиме отладки -
                словарь в ключе имя workspace для которого точки, в значении массив с идентификаторами блоков
        :param kwargs:
        """
        # self.current_block = current_block
        # self.current_algorithm = current_algorithm
        # self.current_thread = None
        self.breakpoints = breakpoints
        self.logger = logger if logger else logging.getLogger(self.__class__.__name__)

        self.extend_plugins = plugins

        self.multi_thread_mode = False

        self.gather = []

        self.commands_result = {}

        self.action: Optional[Action] = None
        self.workspace: Optional[Workspace] = None

    async def execute(self, context, *, endpoint=None, commands_result=None):
        try:
            workspace_raw = await context.workspace_read()
            self.workspace = self.init_workspace(workspace_raw, context.workspace_name, self.logger)
            context.status = 'run'
            context.set_command_limit(context.debug_mode)
            self.action = Action('BlocklyExecutor.execute')

            start_block = self.workspace.get_start_block(self, endpoint, context)
        except Exception as err:
            raise ExtException(parent=err, action='executor.execute')
        try:
            self._index_commands_result(context, commands_result)
            context.commands = []

            if context.deferred:
                await self._execute_deferred(start_block, context)
            context.check_command_limit()

            self.logger.debug('')
            self.logger.debug('--------execute----------------------------')
            self.logger.debug(
                f'deferred:{len(context.deferred)}, '
                f'commands:{len(context.commands)}, '
                f'result:{len(self.commands_result.keys())}')

            result = await start_block.execute(start_block.node, '', context, context.block_context)

            context.result = result
            self.logger.debug('Complete')
            context.status = 'complete'
        except (DeferredOperation, LimitCommand) as err:
            self.logger.debug(f'raise {err.__class__.__name__}')
            pass
        except WorkspaceNotFound as err:
            context.status = 'error'
            context.result = {'__name__': err.__class__.__name__, 'detail': str(err)}
            pass
        except StepForward as step:
            context.result = step.args[2]  # block_context
            context.current_variables = step.args[1].variables
            context.current_block = step.args[0]
            context.current_workspace = step.args[3]
            self.logger.debug('raise StepForward')
        except ExtException as err:
            context.status = 'error'
            context.result = err.to_dict()
        except Exception as err:
            context.status = 'error'
            error = ExtException(parent=err, skip_traceback=-2)
            context.result = error.to_dict()
        # context.commands = self.commands
        # context.deferred = self.gather

        self.logger.debug(
            f'commands {len(context.commands)} command'
            f'gather:{len(self.gather)}, '
            f'result:{len(self.commands_result)}')
        # self.logger.block_context(f'------------------')
        self.action.set_end()
        return context

    async def execute_nested(self, context, *, endpoint=None, commands_result=None):
        workspace_raw = await context.workspace_read()
        self.workspace = self.init_workspace(workspace_raw, context.workspace_name, self.logger)
        start_block = self.workspace.get_start_block(self, endpoint, context)

        return await start_block.execute(start_block.node, '', context, context.block_context)

    @property
    def blocks_index(self) -> dict:
        if self._blocks_index is not None:
            return self._blocks_index
        import importlib
        import pkgutil

        discovered_packages = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith('blockly_executor_')
        }
        discovered_packages['blockly_executor'] = importlib.import_module('blockly_executor')

        if self.extend_plugins:
            for elem in self.extend_plugins:
                discovered_packages[elem] = importlib.import_module(elem)

        self._blocks_index = {}

        import blockly_executor
        self._get_block_in_module(blockly_executor, self._blocks_index)

        for package_name in discovered_packages:
            plugin = discovered_packages[package_name]
            self._get_block_in_module(plugin, self._blocks_index)
        return self._blocks_index

    @staticmethod
    def _get_block_in_module(module, blocks_index):
        blocks_dir = os.path.join(module.__path__[0], 'blocks')
        if not os.path.isdir(blocks_dir):
            return
        blocks_files = os.listdir(blocks_dir)
        for file_name in blocks_files:
            if file_name[-3:] != '.py' or file_name == '__init__.py':
                continue
            block_name = file_name[:-3]
            blocks_index[block_name] = module.__name__
            pass

    def get_block_class(self, block_name):
        block_name = block_name.lower()
        try:
            return self._blocks_class[block_name]
        except KeyError:
            pass
        try:
            index = self.blocks_index[block_name]
        except (KeyError, TypeError):
            raise ExtException(message='Block handler not found', detail=block_name)

        try:
            full_name = f'{index}.blocks.{block_name}.{Helper.to_camel_case(block_name)}'
            self._blocks_class[block_name] = Helper.get_class(full_name)
            return self._blocks_class[block_name]
        except Exception as err:
            raise ExtException(message='Block handler not found', detail=block_name, parent=err)

    async def _execute_deferred(self, robot, context):
        self.logger.block_context('')
        self.logger.block_context('--------execute deferred--------------')
        self.logger.block_context(
            f'deferred:{len(context.deferred)}, '
            f'commands:{len(context.commands)}, '
            f'result:{len(self.commands_result)}')
        # if len(self.commands_result) < len(context.deferred):
        #     raise Exception('не все ответы получены')
        _deferred = context.deferred
        _commands = context.commands
        context.commands = []
        # context.deferred = []
        _delete = []
        for i in range(len(_deferred)):
            _context = context.init_deferred(context, _deferred[i])
            try:
                await robot.execute(robot.node, '', _context, _context.block_context)
                _delete.append(i)
            except DeferredOperation as operation:
                context.add_deferred(operation)
                _delete.append(i)
                continue
        _delete.reverse()
        for elem in _delete:
            context.deferred.pop(elem)

    @property
    def current_algorithm_breakpoints(self):
        try:
            return self.breakpoints[self.workspace.name]
        except (KeyError, TypeError):
            return None

    @staticmethod
    def init_workspace(workspace_raw, algorithm, logger):
        if not workspace_raw:
            raise ExtException(message='Передан пустой алгоритм', detail=algorithm)

        if isinstance(workspace_raw, dict):
            from .workspace_json import WorkspaceJson
            return WorkspaceJson(workspace_raw, algorithm, logger)
        elif isinstance(workspace_raw, str):
            from .workspace_xml import WorkspaceXml
            return WorkspaceXml(workspace_raw, algorithm, logger)

    def _index_commands_result(self, context, commands_result):
        if commands_result:
            for command in commands_result:
                if 'uuid' in command:
                    self.commands_result[command['uuid']] = command
                else:
                    raise ExtException(message='У результата команды не указан идентификатор')
        for command in context.commands:
            command_uuid = command.get('uuid')
            if command_uuid and command_uuid not in self.commands_result:
                raise ExtException(message='Не получен ответ на команду', detail=command_uuid)
