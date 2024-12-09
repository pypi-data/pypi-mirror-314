import json
import os
from unittest import IsolatedAsyncioTestCase

from blockly_executor import ExtException
from blockly_executor.context_memory import ContextMemory
from blockly_executor.executor import BlocklyExecutor

current_dir = os.path.dirname(__file__)


class TestSimpleJson(IsolatedAsyncioTestCase):
    workspaces_dir = os.path.join(current_dir, 'workspaces')

    def setUp(self) -> None:
        self.algorithm = 'simple'
        self.executor = BlocklyExecutor()
        with open(os.path.join(self.workspaces_dir, f'{self.algorithm}.json'), 'r', encoding='utf-8') as file:
            self.workspace_raw = json.load(file)

    async def test_root(self):
        context = ContextMemory.init(workspace_name=self.algorithm)
        context.variables = {'test': 1}
        context.workspaces = {self.algorithm: self.workspace_raw}
        resp = await self.executor.execute(context)

        if resp.status == 'error':
            raise ExtException(parent=resp.result)

        variables: dict = context.variables
        self.assertEqual('Bye Test', variables['test'], 'var test')
        self.assertEqual('Bye Y', variables['y'], 'var y')

    async def test_step_by_step_root(self):
        debug_mode = 'step'
        params = {
            'debug_mode': debug_mode,
            'workspace_name': self.algorithm
        }
        i = 0
        context = ContextMemory()
        for i in range(20):
            context = ContextMemory.init(data=params, **params)
            context.workspaces = {self.algorithm: self.workspace_raw}
            resp = await self.executor.execute(context)
            params = resp.to_dict()
            if resp.status == 'complete':
                break
            if resp.status == 'error':
                raise ExtException(parent=resp.result)

        variables: dict = context.variables
        self.assertEqual('Bye Test', variables['test'], 'var test')
        self.assertEqual(4, i, 'count iteration')
        self.assertEqual('Bye Y', variables['y'], 'var y')

    async def test_endpoint_test1(self):
        context = ContextMemory.init()
        context.variables = {'test': 1}
        context.workspaces = {self.algorithm: self.workspace_raw}
        resp = await self.executor.execute(self.algorithm, context, endpoint='test1')

        if resp.status == 'error':
            raise ExtException(parent=resp.result)

        self.assertEqual(6, resp.result, 'result')
