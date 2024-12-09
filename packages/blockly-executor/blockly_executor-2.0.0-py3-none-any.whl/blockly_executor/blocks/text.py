from blockly_executor.block import Block


class Text(Block):

    async def _execute(self, node, path, context, block_context):
        return self.workspace.find_field_by_name(node, 'TEXT')
