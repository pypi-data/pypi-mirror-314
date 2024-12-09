from .workspace_gluer import WorkspaceGluer
from .workspace_xml import WorkspaceXml


class WorkspaceGluerXml(WorkspaceGluer):
    workspace = WorkspaceXml

    # @classmethod
    # def compare_field(cls, result, field_name, custom_field, base_field):
    #     custom_value = custom_field.text if custom_field else None
    #     base_value = base_field.text if base_field else None
    #     if custom_value != base_value:
    #         result[field_name] = (base_value, custom_value)
