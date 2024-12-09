from blockly_executor.exceptions import WorkspaceNotFound
from .context import Context


class ContextMemory(Context):
    def __init__(self):
        super().__init__()
        self.workspaces = {}

    @classmethod
    def init(cls, *, debug_mode=None, current_block=None, current_workspace=None, workspace_name=None, data=None,
             workspaces: dict = None, **kwargs):
        _self = super().init(debug_mode=debug_mode, current_block=current_block, current_workspace=current_workspace,
                             workspace_name=workspace_name, data=data, **kwargs)
        _self.workspaces = workspaces if workspaces is not None else {}
        return _self

    def init_nested(self, block_context, workspace_name):
        _self: ContextMemory = super().init_nested(block_context, workspace_name)
        _self.workspaces = self.workspaces
        return _self

    async def workspace_read(self):
        try:
            return self.workspaces[self.workspace_name]
        except KeyError:
            raise WorkspaceNotFound(self.workspace_name)
