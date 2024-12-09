from blockly_executor.block_templates.simple_block import SimpleBlockNoStep
from blockly_executor import UserError


class VariablesGet(SimpleBlockNoStep):
    required_param = ['VAR']

    async def _calc_value(self, node, path, context, block_context):
        try:
            return self.get_variable(context, block_context['VAR'])
        except KeyError as key:
            raise UserError(message='Variable not defined', detail=str(key))


