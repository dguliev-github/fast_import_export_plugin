bl_info = {
    "name": "Export Header Button",
    "author": "Damir Guliev, Robert Guetzkow",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "3D View",
    "description": "Adds an export button to the 3D menu header.",
    "wiki_url": "",
    "warning": "Variables are hardcoded!",
    "category": "Import-Export"}

import bpy


class EXAMPLE_OT_something(bpy.types.Operator):
    bl_idname = "example.something"
    bl_label = "Export"
    bl_description = "This operator does something"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            export_path = bpy.data.scenes['Scene']['export_path']
        except KeyError:
            pass
        if export_path: 
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
            use_space_transform=True, 
            #bake_space_transform=True, 
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
            # armature_nodetype='NULL', 
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
        return {"FINISHED"}


def draw(self, context):
    self.layout.operator(EXAMPLE_OT_something.bl_idname)


classes = (EXAMPLE_OT_something,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)


def unregister():
    bpy.types.OUTLINER_HT_header.remove(draw)
    
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
    
# bpy.types.OUTLINER_HT_header.append(draw)