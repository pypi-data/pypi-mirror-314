from blockly_executor.block_templates.simple_block import SimpleBlockNoStep


class ControlsRepeatExt(SimpleBlockNoStep):
    statement_inputs = ['DO']

    async def _calc_value(self, node, path, context, block_context):
        if '_INDEX' not in block_context:
            block_context['_INDEX'] = 1
        node_loop = self.workspace.find_statement_by_name(node, self.statement_inputs[0])
        while block_context['_INDEX'] <= int(block_context['TIMES']):
            self._check_step(context, block_context)
            await self.execute_all_next(node_loop, path, context, block_context, True)
            block_context['_INDEX'] += 1
            context.is_next_step = True
