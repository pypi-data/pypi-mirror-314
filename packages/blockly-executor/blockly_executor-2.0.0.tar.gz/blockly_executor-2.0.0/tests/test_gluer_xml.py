import os

from blockly_executor.workspace_gluer_xml import WorkspaceGluerXml as WorkspaceGluer
from blockly_executor.workspace_xml import WorkspaceXml as Workspace
from .test_gluer_json import TestGluerJson

current_dir = os.path.dirname(__file__)


class TestGluerXml(TestGluerJson):
    gluer = WorkspaceGluer
    workspace = Workspace

    def setUp(self) -> None:
        self.extension = 'xml'

    async def test_simple_change_field(self):
        await super().test_simple_change_field()

    async def test_full_changes(self):
        await super().test_full_changes()

    def workspace_load(self, data, name):
        return self.workspace(data, name, None)

