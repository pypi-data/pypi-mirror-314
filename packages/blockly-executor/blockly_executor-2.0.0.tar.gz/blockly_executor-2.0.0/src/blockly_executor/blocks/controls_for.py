from blockly_executor.block_templates.simple_block import SimpleBlockNoStep
from blockly_executor.exceptions import ServiceException, ErrorInBlock


class ControlsFor(SimpleBlockNoStep):
    required_param = []
    statement_inputs = ['DO']

    async def _calc_value(self, node, path, context, block_context):
        try:
            if 'INDEX' not in block_context:
                block_context['INDEX'] = block_context['FROM']
            node_loop = self.workspace.find_statement_by_name(node, self.statement_inputs[0])
            while block_context['INDEX'] <= block_context['TO']:
                self._check_step(context, block_context)
                self.set_variable(context, block_context['VAR'], block_context['INDEX'])
                await self.execute_all_next(node_loop, path, context, block_context, True)
                block_context['INDEX'] += block_context['BY']
                context.is_next_step = True
        except ServiceException as err:
            raise err from err
        except Exception as err:
            raise ErrorInBlock(parent=err)