# https://docs.blender.org/api/current/bpy.types.Operator.html
# https://blenderartists.org/t/do-all-buttons-on-a-menu-need-to-be-an-operator/1253523
# https://blender.stackexchange.com/questions/32036/is-it-possible-to-associate-non-blend-files-with-blender

bl_info = {
    "name": "Fast Import Export",
    "author": "Damir Guliev, Robert Guetzkow, Campbell Barton (ideasman42)",
    "version": (0, 0, 2),
    "blender": (3, 0, 0),
    "location": "3D View",
    "description": "Adds an export button to the 3D menu header.",
    "wiki_url": "",
    "warning": "Some variables are still hardcoded!",
    "category": "Import-Export"}

import bpy
import json
import os

def generate_executable_bat(blender_work_path, blender_exe_path, addon_path, executable_bat_path):
    new_content = \
f"""
@echo off
pushd "{blender_work_path}\\"
popd
"{blender_exe_path}" --python "{addon_path}\__init__.py" -- %1
"""
    executable_bat_path = addon_path + "\\" + executable_bat_path
    # Check if the file already exists
    if os.path.exists(executable_bat_path):
        with open(executable_bat_path, 'r') as existing_file:
            existing_content = existing_file.read()
            
        # Compare existing content with new content
        if existing_content == new_content:
            return
    
    # Write new content to the file
    with open(executable_bat_path, 'w+') as file:
        file.write(new_content)

def set_settings(type, setup): #type = import, export; setup = props, characters
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #TODO - add default settings.json generator
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
    return dict(settings["fbx"][type][setup])

addon_dir = os.path.dirname(os.path.abspath(__file__))
default_export_preset = "compliance" #TODO fix hardcoded value
generate_executable_bat(os.path.split(bpy.app.binary_path)[0], bpy.app.binary_path, addon_dir, "blender_to_os.bat")

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
            fbx_export_settings = set_settings(type="export",setup=bpy.data.scenes['Scene']["export_preset"])
        except AttributeError:
            fbx_export_settings = set_settings(type = "export",setup = default_export_preset)
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

class AddFolderPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        # layout.label(text="Addon Preferences")

        row = layout.row()
        # row.label(text="Addon Folder:")
        row.operator("addon.open_folder", text="Open Addon Folder")

class OpenFolderOperator(bpy.types.Operator):
    bl_idname = "addon.open_folder"
    bl_label = "Open Addon Folder"

    def execute(self, context):
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        os.system(f'explorer.exe "{addon_dir}"')
        return {'FINISHED'}

classes = (FASTIO_OT_button,FASTIO_OT_settings,AddFolderPreferences,OpenFolderOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)

def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw)    
    for cls in classes:
        bpy.utils.unregister_class(cls)

def importer():
    from sys import argv
    argv = argv[argv.index("--") + 1:]

    fbx_import_settings = set_settings(type = "import",setup = "standard") 
    bpy.context.preferences.view.show_splash = False
    for f in argv:
        ext = os.path.splitext(f)[1].lower()

        if ext == ".fbx":
            bpy.ops.import_scene.fbx(filepath=f, **fbx_import_settings)
        else:
            print("Extension %r is not known!" % ext)
        bpy.data.scenes['Scene']["export_path"] = str(argv[0])
        bpy.data.scenes['Scene']["export_preset"] = default_export_preset 
    if not argv:
        print("No files passed")

if __name__ == "__main__":
    importer()
