# importer_path="$(pwd)"/"import_os.py"
importer_path="~/Library/Application Support/Blender/3.3/scripts/addons/fast_import_export/import_os.py"
# echo "$importer_path"
# cd /Applications/Blender.app/Contents/MacOS
open -n -a blender --args --python "$importer_path" -- "$1"