from .helpers.data_getters_setter import data_getter_root, data_setter_root


class ContextProps:
    def __init__(self):
        self.data = {}
        self.current_variable_scope = 0

    @property
    def variables(self):
        return self.variable_scopes[self.current_variable_scope]

    @variables.setter
    def variables(self, value):
        self.variable_scopes[self.current_variable_scope] = value

    @property
    def variable_scopes(self):
        return data_getter_root(self, 'variable_scopes', [{}])

    @variable_scopes.setter
    def variable_scopes(self, value):
        data_setter_root(self, 'variable_scopes', value)

    @property
    def block_context(self):
        return data_getter_root(self, 'block_context', {})

    @block_context.setter
    def block_context(self, value):
        data_setter_root(self, 'block_context', value)

    @property
    def current_workspace(self):
        return data_getter_root(self, 'current_workspace', '')

    @current_workspace.setter
    def current_workspace(self, value):
        data_setter_root(self, 'current_workspace', value)

    @property
    def current_variables(self):
        return data_getter_root(self, 'current_variables', {})

    @current_variables.setter
    def current_variables(self, value):
        data_setter_root(self, 'current_variables', value)

    @property
    def deferred(self):
        return data_getter_root(self, 'deferred', [])

    @deferred.setter
    def deferred(self, value):
        data_setter_root(self, 'deferred', value)

    @property
    def status(self):
        return data_getter_root(self, 'status', '')

    @status.setter
    def status(self, value):
        data_setter_root(self, 'status', value)

    @property
    def result(self):
        return data_getter_root(self, 'result', {})

    @result.setter
    def result(self, value):
        data_setter_root(self, 'result', value)

    @property
    def commands(self):
        return data_getter_root(self, 'commands', {})

    @commands.setter
    def commands(self, value):
        data_setter_root(self, 'commands', value)

    @property
    def workspace_name(self):
        return data_getter_root(self, 'algorithm', '')

    @workspace_name.setter
    def workspace_name(self, value):
        data_setter_root(self, 'algorithm', value)

    @property
    def current_block(self):
        return data_getter_root(self, 'current_block', '')

    @current_block.setter
    def current_block(self, value):
        data_setter_root(self, 'current_block', value)

    @property
    def debug_mode(self):
        return data_getter_root(self, 'debug_mode', None)

    @debug_mode.setter
    def debug_mode(self, value):
        data_setter_root(self, 'debug_mode', value)
