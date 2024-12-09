import json
import os

from blockly_executor.exceptions import WorkspaceNotFound
from .context import Context


class ContextFile(Context):
    def __init__(self):
        super().__init__()
        self.workspaces = ''

    @classmethod
    def init(cls, *, debug_mode=None, current_block=None, current_workspace=None, workspace_name=None, data=None,
             workspaces: str = './', **kwargs):
        _self = super().init(debug_mode=debug_mode, current_block=current_block, current_workspace=current_workspace,
                             workspace_name=workspace_name, data=data, **kwargs)
        _self.workspaces = workspaces
        return _self

    def init_nested(self, block_context, workspace_name):
        _self: ContextFile = super().init_nested(block_context, workspace_name)
        _self.workspaces = self.workspaces
        return _self

    async def workspace_read(self):
        workspace_filename = os.path.join(self.workspaces, self.workspace_name)
        try:
            with open(workspace_filename + '.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            try:
                with open(workspace_filename + '.xml', 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                raise WorkspaceNotFound(self.workspace_name)
