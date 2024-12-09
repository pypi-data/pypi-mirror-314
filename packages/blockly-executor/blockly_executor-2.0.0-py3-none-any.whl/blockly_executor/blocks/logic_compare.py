from blockly_executor.block_templates.simple_block import SimpleBlock
from blockly_executor.exceptions import ErrorInBlock


class LogicCompare(SimpleBlock):
    required_param = ['A', 'B', 'OP']

    async def _calc_value(self, node, path, context, block_context):
        operation = block_context['OP']
        try:
            return _operation[operation](block_context)
        except KeyError:
            raise ErrorInBlock(detail=f'{self.__class__.__name__}: Operation {operation} not supported')


def _eq(block_context):
    return block_context['A'] == block_context['B']


def _neq(block_context):
    return block_context['A'] != block_context['B']


def _gt(block_context):
    return block_context['A'] > block_context['B']


def _gte(block_context):
    return block_context['A'] >= block_context['B']


def _lt(block_context):
    return block_context['A'] < block_context['B']


def _lte(block_context):
    return block_context['A'] <= block_context['B']


_operation = dict(
    EQ=_eq,
    NEQ=_neq,
    GT=_gt,
    GTE=_gte,
    LT=_lt,
    LTE=_lte,
)
