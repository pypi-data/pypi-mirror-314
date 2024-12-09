import os

from blockly_executor.executor import BlocklyExecutor
from .test_simple_json import TestSimpleJson

current_dir = os.path.dirname(__file__)


class TestSimpleXml(TestSimpleJson):

    def setUp(self) -> None:
        self.algorithm = 'simple'
        self.executor = BlocklyExecutor()
        with open(os.path.join(self.workspaces_dir, 'simple.xml'), 'r', encoding='utf-8') as file:
            self.workspace_raw = file.read()

    async def test_root(self):
        await super().test_root()

    async def test_step_by_step_root(self):
        await super().test_step_by_step_root()

    async def test_endpoint_test1(self):
        await super().test_endpoint_test1()
