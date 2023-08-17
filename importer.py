import os
import bpy
import json

#TODO fix hardcoded value
default_export_preset = "compliance"
default_import_preset = "standard"

def settings_set(type, setup):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #TODO - add default settings.json generator
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
    return dict(settings["fbx"][type][setup])

def import_file():
    from sys import argv
    argv = argv[argv.index("--") + 1:]
    fbx_import_settings = settings_set(type = "import",setup = default_import_preset) 
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
    import_file()