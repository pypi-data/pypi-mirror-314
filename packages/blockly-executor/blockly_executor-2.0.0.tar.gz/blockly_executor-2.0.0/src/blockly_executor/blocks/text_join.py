from blockly_executor.block import Block


class TextJoin(Block):
    async def _execute(self, node, path, context, block_context):
        text_count = int(self.workspace.find_mutation_by_name(node, 'items', 0))
        result = ""
        for j in range(text_count):
            _key = f'ADD{j}'
            complete = _key in block_context
            if complete:
                result = block_context.get(_key)
            else:
                node_text = self.workspace.find_input_by_name(node, f'ADD{j}')
                next_node_result = await self.execute_all_next(node_text, f'{path}.add{j}', context, block_context)
                result += str(next_node_result)
        return result
