from blockly_executor.block import Block


class ListsCreateWith(Block):

    async def _execute(self, node, path, context, block_context):
        total_size = self.workspace.find_mutation_by_name(node, 'items', '0')
        result = []
        if not total_size:
            return result
        if 'value' not in block_context:
            block_context['value'] = []
        current_size = len(block_context['value'])
        if current_size != total_size:
            for j in range(current_size, total_size):
                node_value = self.workspace.find_input_by_name(node, f'ADD{j}')
                if node_value is None:
                    raise Exception(f'плохой блок ADD{j}')
                result = await self.execute_all_next(node_value, f'{path}.{j}', context, block_context)
                block_context['value'].append(result)
        self._check_step(context, block_context)
        return block_context['value']
