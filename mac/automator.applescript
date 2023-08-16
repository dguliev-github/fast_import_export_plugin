on run {input, parameters}
	set script_location to path to me
	set script_folder to POSIX path of (container of script_location) as text
	repeat with afile in input
		set unix_path to (POSIX path of afile) as text
		do shell script "open -n -a blender --args --python " & script_folder & "import_os.py" & " -- " & "\"" & unix_path & "\""
	end repeat
	return input
end run
