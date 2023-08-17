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

from . import generator
from . import properties
from . import addon

import bpy
import os

addon_dir = os.path.dirname(os.path.abspath(__file__))

generator.generate_executable_bat(os.path.split(bpy.app.binary_path)[0], bpy.app.binary_path, addon_dir, "blender_to_os.bat")

classes = (addon.FASTIO_OT_button,addon.FASTIO_OT_settings,properties.AddFolderPreferences,properties.OpenFolderOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    addon.draw_button()

def unregister():
    addon.undraw_button()   
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
