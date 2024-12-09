from blockly_executor.blocks.procedures_defnoreturn import ProceduresDefnoreturn


class ProceduresDefreturn(ProceduresDefnoreturn):

    async def _execute(self, node, path, context, block_context):
        await super()._execute(node, path, context, block_context)

        _return_node = self.workspace.find_input_by_name(node, 'RETURN')
        name = self.workspace.find_field_by_name(node, 'NAME')
        context.set_next_step(self.block_id)
        res = await self.execute_all_next(_return_node, f'{path}.{name}', context, block_context)
        return res
