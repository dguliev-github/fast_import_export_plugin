# Fast import export plugin
Import fbx file in Blender by clicking on it, edit it, and save it in one click. Designed for Unity-Blender-Unity workflow.

![fast_import_export_usage](https://github.com/dguliev-github/fast_import_export_plugin/assets/64034875/706d9055-b85c-43d4-b513-2fc608a8a036)

### Installation

1. Download this repository as a zip and install by `Edit > Preferences > Add-ons > Install`.
2. In addon preferences `Open Addon Folder`. 
3. Change .fbx file association to the `blender_to_os.bat`. To do that you have to right click any .fbx file, click  `Properties` and change `Opens with` preference. Click on `more apps↓`, scroll down and select `Look for another app on this PC`. In explorer window, locate your fast_export_import addon location and choose `blender_to_os.bat`. You can copy path location from the explorer window opened on a step 2.

    For convenience, I provided addon with the `test_cube.fbx` file. Use it for setting file association.
4. Test addon by opening `test_cube.fbx` file. It should almost immediately open in a new blender instance without a splash screen.

### Usage

This addon is designed for fast fbx file modification and benefits multiple software workflows, such as `Blender to Unity`.

You can open fbx files from the windows explorer, Unity Project window, Unity inspector (by double clicking on a mesh field).
![ways_to_open_fbx](https://github.com/dguliev-github/fast_import_export_plugin/assets/64034875/5f83770b-7f07-4344-b727-91b4df53f5a9)

Edit imported objects, select those which you want to export, and click `export` button at the top left corner of the 3D view. The new fbx file containing selected objects will overwrite the old one.

### Limitations

Currently does not support ASCII fbx files. I am planning to add [better-fbx-exporter](https://blendermarket.com/products/better-fbx-importer--exporter) as an optional export preset. Preset would be activated if better-fbx-exporter plugin installation has been detected in blender.

Default export preset assumes no space transforms and no additional transform baking. In case of `blender to unity` pipeline this means that you have to manually rotate mesh or parent empty by 90 degrees X in Blender in order for it to be positioned properly in Unity. The reason of this is to be able to freely change fbx file later and be able to cascade multiple edits without space transforms at each step.

Importer may not work ideally when it comes to skinned meshes with bones. You'll have to set your own import preset in `settings.json` in case of unsatisfactory results with the default one.

Mac and Linux support are not implemented yet. There are some mac integration snippets in the corresponding folder if you want to do it using Automator though.  

### Default settings
#### Import
![image](https://github.com/dguliev-github/fast_import_export_plugin/assets/64034875/bb7e1c78-e51b-4541-b50f-63b3cd43bab8)

The same as default blender with only one change:

- [x] Automatic Bone Orientation

#### Export
![image](https://github.com/dguliev-github/fast_import_export_plugin/assets/64034875/772a28e5-7a55-4e01-94eb-8b270c9af4ad)

The same as default blender but with changes:
- [x] Limit to Selected Objects
* Apply Scalings `FBX All`
* Forward `-X`
* Up `Z Up`
- [ ] Add Leaf Bones 

### Technical Notes
This addon works by opening mesh file type with a custom script by invoking `bpy.ops.import_scene.fbx(path_to_file,**arguments_from_settings.json)` at blender.exe start. `path_to_file` is saved in a string-type scene custom propriety named `export_path`. 

On `Export` button click mesh file is being exported at `export_path` which basically rewrites it with a new version at the original location. It uses `bpy.ops.export_scene.fbx(export_path,**arguments_from_settings.json)`.

It is possible (and encouraged) for user to change `export_path` by directly changing file path in `Scene > Custom Properties` if they want to keep the original file intact and just make a copy at another location or with the different name.

![image](https://github.com/dguliev-github/fast_import_export_plugin/assets/64034875/120f0042-8a02-427e-84b5-be2646a1f3d5)

Every opened fbx file invokes separate blender instance. This is intentional behavior and is meant to work using edit-and-forget methodology. If user is done with editing and exports new fbx file version they can close blender without saving .blend file. If there is a need to change this file again, user can reimport that file by simply opening it in blender.

Note that if there are any heavy memory-demanding addons installed it will affect speed at which every instance will be opened.