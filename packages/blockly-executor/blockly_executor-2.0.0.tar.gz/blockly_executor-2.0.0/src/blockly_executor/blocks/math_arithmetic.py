from numbers import Number

from blockly_executor import UserError
from blockly_executor.block_templates.simple_block import SimpleBlock


class MathArithmetic(SimpleBlock):
    required_param = ['OP', 'A', 'B']

    async def _calc_value(self, node, path, context, block_context):
        if not isinstance(block_context['A'], Number):
            raise UserError(
                message='В арифметическую операцию передано не числовое значение',
                detail=str(block_context['A']),
                dump={'block_id': self.block_id}
            )
        if not isinstance(block_context['B'], Number):
            raise UserError(
                message='В арифметическую операцию передано не числовое значение',
                detail=str(block_context['A']),
                dump={'block_id': self.block_id}
            )
        return operations[block_context['OP']](block_context['A'], block_context['B'])


def add(a, b):
    return a + b


def minus(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def power(a, b):
    return a ^ b


operations = {
    'ADD': add,
    'MINUS': minus,
    'MULTIPLY': multiply,
    'DIVIDE': divide,
    "POWER": power
}
