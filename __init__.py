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
    '''
    import addon_utils
    
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "fast_export_import":
            mod_filepath = os.path.dirname(mod.__file__)
    
    blender_executable_path_file = os.path.join(mod_filepath,filename)
    '''
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

    def execute(self, context):
        try:
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            pass
        if export_path:
            #fix boolean and int conversion from json
            
            bpy.ops.export_scene.fbx(filepath = export_path, **fbx_export_settings) 
            """
            bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection = True, 
            axis_forward = '-Y', 
            axis_up = 'Z',
            # use_visible=False, 
            # use_active_collection=False, 
            # global_scale=1, 
            # apply_unit_scale=True, 
            # apply_scale_options='FBX_SCALE_NONE', 
            #use_space_transform=True,

            bake_space_transform=True, 
            # object_types={'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'MESH', 'OTHER'}, 
            # use_mesh_modifiers=True, 
            # use_mesh_modifiers_render=True, 
            # mesh_smooth_type='OFF', 
            # use_subsurf=False, 
            # use_mesh_edges=False, 
            # use_tspace=False, 
            # use_triangles=False, 
            # use_custom_props=False, 
            add_leaf_bones=False, 
            # primary_bone_axis='Y', 
            # secondary_bone_axis='X', 
            # use_armature_deform_only=False, 
            armature_nodetype="ROOT", 
            # bake_anim=True, 
            # bake_anim_use_all_bones=True, 
            # bake_anim_use_nla_strips=True, 
            # bake_anim_use_all_actions=True, 
            # bake_anim_force_startend_keying=True, 
            # bake_anim_step=1, 
            # bake_anim_simplify_factor=1, 
            # path_mode='AUTO', 
            # embed_textures=False, 
            # batch_mode='OFF', 
            # use_batch_own_dir=True, 
            # use_metadata=True, 
            )
            """
        return {"FINISHED"}


def draw(self, context):
    self.layout.operator(FASTIO_OT_button.bl_idname)

classes = (FASTIO_OT_button,)

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