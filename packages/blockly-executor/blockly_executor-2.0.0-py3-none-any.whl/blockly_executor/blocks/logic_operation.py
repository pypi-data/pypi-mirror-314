from blockly_executor.block_templates.simple_block import SimpleBlock
from blockly_executor.exceptions import ErrorInBlock


class LogicOperation(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        if block_context['OP'] == 'AND':
            return block_context['A'] and block_context['B']
        elif block_context['OP'] == 'OR':
            return block_context['A'] or block_context['B']
        else:
            raise ErrorInBlock(detail=f'{self.__class__.__name__}: Operation {block_context["OP"]} not supported')
