# https://docs.blender.org/api/current/bpy.types.Operator.html
# https://blenderartists.org/t/do-all-buttons-on-a-menu-need-to-be-an-operator/1253523

bl_info = {
    "name": "Fast Import Export",
    "author": "Damir Guliev, Robert Guetzkow",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "3D View",
    "description": "Adds an export button to the 3D menu header.",
    "wiki_url": "",
    "warning": "Variables are hardcoded!",
    "category": "Import-Export"}

import bpy
import json
import os

def generate_blender_path(filename: str): # suggested to use "blender_executable_path.txt"
    """
    read the text file. if there is no file then make one, if contents is not bpy.app.binary_path when rewrite 
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    blender_executable_path = bpy.app.binary_path

    if os.path.exists(filename):
        with open(filename,"r+") as file:
            if not (file.readline == blender_executable_path):
                file.write(blender_executable_path)
            else:
                pass
    else:
        with open(filename,"x") as file:
            file.write(blender_executable_path)
            
                
    
def set_settings(type, setup): #type = import, export; setup = props, characters
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #TODO - add default settings.json generator
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
    return dict(settings["fbx"][type][setup])

fbx_export_settings = set_settings(type = "export",setup = "props")
generate_blender_path("blender_executable_path.txt")
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
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', **fbx_export_settings)
        else:
            bpy.ops.export_scene.fbx(filepath = export_path, **fbx_export_settings)
        return {"FINISHED"}
        
class FASTIO_OT_settings(bpy.types.Operator):
    bl_idname = "export.settings"
    bl_label = "Export"
    bl_description = "Currently does nothing"
    bl_options = {"REGISTER"}

    def execute(self, context):
        return {"FINISHED"}


def draw(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator(FASTIO_OT_button.bl_idname, icon = "EXPORT")
    row.operator(FASTIO_OT_settings.bl_idname, text = "" , icon = "PREFERENCES")

classes = (FASTIO_OT_button,FASTIO_OT_settings)

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

    import bpy
    fbx_import_settings = set_settings(type = "import",setup = "standard") 
    bpy.context.preferences.view.show_splash = False
    for f in argv:
        ext = os.path.splitext(f)[1].lower()

        if ext == ".fbx":
            bpy.ops.import_scene.fbx(filepath=f, **fbx_import_settings)
        else:
            print("Extension %r is not known!" % ext)
        bpy.data.scenes['Scene']["export_path"] = str(argv[0])
    if not argv:
        print("No files passed")

if __name__ == "__main__":
    importer()