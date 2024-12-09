from blockly_executor.block import Block


class ProceduresDefnoreturn(Block):
    async def _execute(self, node, path, context, block_context):
        self._check_step(context, block_context)
        code = self.workspace.find_statement_by_name(node, 'STACK')
        name = self.workspace.find_field_by_name(node, 'NAME')
        if code and '_stack' not in block_context:
            await self.execute_all_next(code, f'{path}.{name}', context, block_context, True)
            block_context['_stack'] = None


