from blockly_executor.block import Block
from blockly_executor.exceptions import ReturnFromFunction


class ProceduresCallnoreturn(Block):

    async def _execute2(self, node, path, context, block_context):
        try:
            if self._result not in block_context:
                endpoint = self.workspace.find_mutation_by_name(node, 'name')
                if '__params' not in block_context:
                    block_context['__params'] = await self.calc_param_value(node, path, context, block_context)

                handler = self.workspace.init_procedure_block(self.executor, endpoint)
                self._check_step(context, block_context)

                context.variable_scope_add(block_context, block_context['__params'])
                res = await handler.execute(handler.node, path, context, block_context)
                block_context[self._result] = res
                context.variable_scope_remove(block_context)
            return block_context[self._result]
        except ReturnFromFunction as err:
            context.set_next_step(self.block_id)
            context.clear_child_context(block_context)
            return err.args[0]

    async def calc_param_value(self, node, path, context, block_context):
        args = self.workspace.find_mutation_args(node)
        inputs = self.workspace.find_inputs(node)
        function_params = {}
        if inputs:
            for i in range(len(args)):
                arg_name = args[i]
                if arg_name not in block_context:
                    arg_node = inputs.get(f'ARG{i}')
                    _value = None
                    if arg_node:
                        _value = await self.execute_all_next(arg_node, f'{path}.{i}', context, block_context)
                    block_context[arg_name] = _value
                    function_params[arg_name] = _value
        return function_params

    async def _execute(self, node, path, context, block_context):
        await self._execute2(node, path, context, block_context)
        return self.workspace.find_next_statement(node)
