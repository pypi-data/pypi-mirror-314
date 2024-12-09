from blockly_executor.block_templates.simple_block import SimpleBlockNoStep


class ControlsForeach(SimpleBlockNoStep):
    required_param = ['VAR', 'LIST']
    statement_inputs = ['DO']

    async def _calc_value(self, node, path, context, block_context):
        if '_INDEX' not in block_context:
            block_context['_INDEX'] = 0
        if block_context['LIST']:
            node_loop = self.workspace.find_statement_by_name(node, self.statement_inputs[0])
            while block_context['_INDEX'] < len(block_context['LIST']):
                self._check_step(context, block_context)
                self.set_variable(context, block_context['VAR'], block_context['LIST'][block_context['_INDEX']])
                await self.execute_all_next(node_loop, path, context, block_context, True)
                block_context['_INDEX'] += 1
                context.is_next_step = True
