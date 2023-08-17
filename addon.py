import bpy
from .importer import settings_set
from .importer import default_export_preset

class FASTIO_OT_button(bpy.types.Operator):
    bl_idname = "export.button"
    bl_label = "Export"
    bl_description = "Export selected to the same file"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        export_path = ""
        try:
            fbx_export_settings = settings_set(type="export", setup=bpy.data.scenes['Scene']["export_preset"])
        except AttributeError:
            fbx_export_settings = settings_set(type = "export", setup = default_export_preset)
        try:
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', **fbx_export_settings)
        else:
            bpy.ops.export_scene.fbx(filepath = export_path, **fbx_export_settings)
        return {"FINISHED"}
        
class FASTIO_OT_settings(bpy.types.Operator):
    bl_idname = "export.settings"
    bl_label = "Export"
    bl_description = "Select Export Preset"
    bl_options = {"REGISTER", "UNDO"}
    # TODO read presets from json. Change json structure so it would contain names and descriptions
    preset_items = [
        ("characters", "Characters", "Export preset for characters"),
        ("props", "Props", "Export preset for props"),
        ("compliance", "Compliance", "Export preset for compliance"),
    ]

    preset_name: bpy.props.EnumProperty(
        items=preset_items,
        name="Export Preset",
        description="Select an export preset",
    )

    def execute(self, context):
        bpy.data.scenes['Scene']["export_preset"] = self.preset_name
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)


def draw(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator(FASTIO_OT_button.bl_idname, icon = "EXPORT")
    row.operator(FASTIO_OT_settings.bl_idname, text = "" , icon = "PREFERENCES")

def draw_button():
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)
def undraw_button():
    bpy.types.VIEW3D_HT_tool_header.remove(draw)