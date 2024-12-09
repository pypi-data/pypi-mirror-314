from blockly_executor import ExtException
from blockly_executor.block import Block
from blockly_executor.exceptions import ServiceException, ErrorInBlock


class Root(Block):

    async def _execute(self, node, path, context, block_context):
        try:
            nodes = self.workspace.find_child_blocks(node)
            if self._result not in block_context:
                block_context[self._result] = {}

            for block_node in nodes:
                block_id = block_node.get('id')
                block_type = block_node.get('type')
                if block_type in ['procedures_defreturn', 'procedures_defnoreturn']:
                    continue
                if block_id not in block_context[self._result]:
                    block_context[self._result][block_id] = {}
                if self._result not in block_context[self._result][block_id]:
                    await self.execute_child_block(
                        block_node, path, context, block_context[self._result][block_id])
                    block_context[self._result][block_id][self._result] = True
                if '_next' not in block_context[self._result][block_id]:
                    next_node = self.workspace.find_next_statement(block_node)
                    if next_node:
                        await self.execute_all_next(next_node, path, context, block_context[self._result][block_id])
                    block_context[self._result][block_id]['_next'] = True
                    context.set_next_step()
        except (ExtException, ServiceException) as err:
            raise err from err
        except Exception as err:
            raise ErrorInBlock(parent=err)

    async def _before_execute(self, node, path, context, block_context):
        self.block_id = 'root'
        self.block_type = 'root'
        block_context['__id'] = self.block_id
        block_context['__path'] = f'{path}.{self.block_type}'
