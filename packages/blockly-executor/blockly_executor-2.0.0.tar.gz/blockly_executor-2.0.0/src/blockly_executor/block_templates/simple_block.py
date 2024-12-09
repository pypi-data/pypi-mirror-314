from blockly_executor import ExtException, UserError
from blockly_executor.block import Block
from blockly_executor.exceptions import ServiceException, ErrorInBlock


class SimpleBlock(Block):
    required_param = []
    step = True

    async def _execute(self, node, path, context, block_context):
        try:
            if self._result not in block_context:
                # todo поддержать поля с именами переменных (список полей декларировать на блоке)
                self.workspace.find_fields(node, block_context)
                await self.workspace.execute_inputs(self, node, path, context, block_context)
                if self.step:
                    self._check_step(context, block_context)
                self.check_required_param_in_block_context(block_context)
                block_context[self._result] = await self._calc_value(node, path, context, block_context)
            else:
                self.logger.debug('skip calc')
            return block_context[self._result]
        except (ExtException, ServiceException) as err:
            raise err from err
        except Exception as err:
            raise ErrorInBlock(parent=err, message=f'{self.__class__.__name__}')

    def check_required_param_in_block_context(self, block_context):
        for param in self.required_param:
            if param not in block_context:
                raise UserError(message="Required param not defined", detail=f'{param} in {self.__class__.__name__}')

    async def _calc_value(self, node, path, context, block_context):
        raise NotImplemented(f'{self.__class__.__name__}._calc_value')


class SimpleBlockNoStep(SimpleBlock):
    step = False
