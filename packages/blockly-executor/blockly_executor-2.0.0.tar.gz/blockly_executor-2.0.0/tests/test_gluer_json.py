import json
import os
from unittest import IsolatedAsyncioTestCase

from blockly_executor import ExtException
from blockly_executor.workspace_gluer_json import WorkspaceGluerJson as WorkspaceGluer
from blockly_executor.workspace_json import WorkspaceJson as Workspace

current_dir = os.path.dirname(__file__)


class TestGluerJson(IsolatedAsyncioTestCase):
    workspaces_dir = os.path.join(current_dir, 'workspaces')
    gluer = WorkspaceGluer
    workspace = Workspace

    def setUp(self) -> None:
        self.extension = 'json'

    def file_read(self, name):
        with open(os.path.join(self.workspaces_dir, f'{name}.{self.extension}'), 'r', encoding='utf-8') as file:
            return file.read()

    def workspace_load(self, data, name):
        return self.workspace(json.loads(data), name, None)

    def raw_workspace_save(self, data, name):
        with open(os.path.join(self.workspaces_dir, 'temp', f'{name}.{self.extension}'), 'w', encoding='utf-8') as file:
            return file.write(data)

    async def test_simple_change_field(self):
        name = 'simple-change-field'
        changes = await self.unglue_glue(name, 5)

    async def test_full_changes(self):
        name = 'full-changes'
        changes = await self.unglue_glue(name, 18)

    async def unglue_glue(self, name, count_changes):
        base_name = f'glue-{name}-base'
        custom_name = f'glue-{name}-custom'
        raw_workspace_base = self.file_read(base_name)
        raw_workspace_custom = self.file_read(custom_name)
        changes, errors, warnings = self.gluer.unglue(
            self.workspace_load(raw_workspace_base, base_name),
            self.workspace_load(raw_workspace_custom, custom_name)
        )
        self.assertEqual(count_changes, len(changes), 'Количество отличий')
        raw_workspace_result, errors, warnings = self.gluer.glue(
            self.workspace_load(raw_workspace_base, base_name),
            self.workspace_load(raw_workspace_custom, custom_name),
            changes
        )
        self.raw_workspace_save(raw_workspace_result, custom_name)

        # Сравнение результата склейки с кастомной инишкой
        changes2, errors2, warnings2 = self.gluer.unglue(
            self.workspace_load(raw_workspace_custom, base_name),
            self.workspace_load(raw_workspace_result, custom_name)
        )

        self.assertEqual(0, len(changes2), changes2)

        return changes
        pass
