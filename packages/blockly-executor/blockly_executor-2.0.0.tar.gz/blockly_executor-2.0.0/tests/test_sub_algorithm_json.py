import json
import os
from unittest import IsolatedAsyncioTestCase

from blockly_executor import ExtException
from blockly_executor.context_memory import ContextMemory
from blockly_executor.context_file import ContextFile
from blockly_executor.executor import BlocklyExecutor

current_dir = os.path.dirname(__file__)


class TestSubAlgorithm(IsolatedAsyncioTestCase):
    workspaces_dir = os.path.join(current_dir, 'workspaces')

    def setUp(self) -> None:
        self.algorithm = 'SubAlgorithm'
        self.executor = BlocklyExecutor()
        with open(os.path.join(self.workspaces_dir, f'{self.algorithm}.json'), 'r', encoding='utf-8') as file:
            self.workspace_raw = json.load(file)
        with open(os.path.join(self.workspaces_dir, f'{self.algorithm}1.json'), 'r', encoding='utf-8') as file:
            self.workspace_raw1 = json.load(file)
        with open(os.path.join(self.workspaces_dir, f'{self.algorithm}2.json'), 'r', encoding='utf-8') as file:
            self.workspace_raw2 = json.load(file)

    async def test_memory_run_child_workspace_loaded(self):
        context = ContextMemory.init(workspace_name=self.algorithm)
        context.workspaces = dict(
            SubAlgorithm=self.workspace_raw,
            SubAlgorithm1=self.workspace_raw1,
            SubAlgorithm2=self.workspace_raw2,
        )
        resp = await self.executor.execute(context)

        if resp.status == 'error':
            raise ExtException(parent=resp.result)
        self.assertEqual(16, resp.result)
        pass

    async def test_memory_step_by_step_child_workspace_not_loaded(self):
        all_workspaces = dict(
            SubAlgorithm1=self.workspace_raw1,
            SubAlgorithm2=self.workspace_raw2,
        )
        workspaces = dict(
            SubAlgorithm=self.workspace_raw,
        )
        params = dict(
            workspace_name=self.algorithm, debug_mode='step'
        )
        resp = None
        i = 0
        for i in range(20):
            context = ContextMemory.init(data=params, workspaces=workspaces, **params)
            resp = await self.executor.execute(context)
            if resp.status == 'error':
                if resp.result['message'] == 'WorkspaceNotFound':
                    workspaces[resp.result['detail']] = all_workspaces[resp.result['detail']]
                    params = resp.to_dict()
                    continue
                raise ExtException(parent=resp.result)
            elif resp.status == 'run':
                params = resp.to_dict()
                continue
            else:
                break

        self.assertEqual(16, resp.result)
        self.assertEqual(14, i)
        pass

    async def test_file_step_be_step_child_workspace_not_loaded(self):
        workspaces = os.path.join(os.path.dirname(__file__), 'workspaces')
        params = dict(
            workspace_name=self.algorithm, debug_mode='step'
        )
        resp = None
        i = 0
        for i in range(20):
            context = ContextFile.init(data=params, workspaces=workspaces, **params)
            resp = await self.executor.execute(context)
            if resp.status == 'error':
                if resp.result['message'] == 'WorkspaceNotFound':
                    params = resp.to_dict()
                    continue
                raise ExtException(parent=resp.result)
            elif resp.status == 'run':
                params = resp.to_dict()
                continue
            else:
                break

        self.assertEqual(16, resp.result)
        self.assertEqual(12, i)
        pass
