from blockly_executor.block import Block
from blockly_executor.exceptions import ServiceException, ErrorInBlock


class ControlsIf(Block):
    async def _execute(self, node, path, context, block_context):
        try:
            if self.workspace == 'json':
                mutation_else_if = 'elseif'
                mutation_else = 'else'
            else:
                mutation_else_if = 'elseIfCount'
                mutation_else = 'hasElse'

            if_count = int(self.workspace.find_mutation_by_name(node, mutation_else_if, 0)) + 1
            defined_else = int(self.workspace.find_mutation_by_name(node, mutation_else, 0))
            if_complete = False
            j = None
            for j in range(if_count):
                # рассчитываем все if
                _key = f'IF{j}'
                complete = _key in block_context
                if complete:
                    result = block_context.get(_key)
                else:
                    node_if = self.workspace.find_input_by_name(node, f'IF{j}')
                    if node_if is None:
                        raise Exception(f'Bad {_key} {path}')
                    result = await self.execute_all_next(node_if, f'{path}.if{j}', context, block_context)
                    block_context[_key] = result
                if result:
                    if_complete = True
                    break
            self._check_step(context, block_context)
            if if_complete and j is not None:
                if '_do' not in block_context:
                    node_do = self.workspace.find_statement_by_name(node, f'DO{j}')
                    if node_do is None:
                        return
                        # raise Exception(f'Bad if DO {j} {path}')
                    await self.execute_all_next(node_do, f'{path}.do{j}', context, block_context, True)
                    block_context['_do'] = None
            else:
                if defined_else:
                    if '_do' not in block_context:
                        node_do = self.workspace.find_statement_by_name(node, 'ELSE')
                        if node_do is None:
                            return
                            # raise Exception(f'Bad else DO {path}')
                        await self.execute_all_next(node_do, f'{path}.else', context, block_context, True)
                        block_context['_do'] = None
        except ServiceException as err:
            raise err from err
        except Exception as err:
            raise ErrorInBlock(parent=err)
