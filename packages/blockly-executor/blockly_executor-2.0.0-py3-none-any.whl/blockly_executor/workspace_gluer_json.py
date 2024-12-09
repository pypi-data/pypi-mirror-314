from .workspace_gluer import WorkspaceGluer
from .workspace_json import WorkspaceJson


class WorkspaceGluerJson(WorkspaceGluer):
    workspace = WorkspaceJson

    # @classmethod
    # def compare_field(cls, result, field_name, custom_field, base_field):
    #     def _get_value(_value):
    #         _result = _value
    #         if _value:
    #             if isinstance(_value, dict):  # это переменная
    #                 return _value.get('id')
    #         return _result
    #     custom_value = _get_value(custom_field)
    #     base_value = _get_value(base_field)
    #     if custom_value != base_value:
    #         result[field_name] = (base_value, custom_value)
