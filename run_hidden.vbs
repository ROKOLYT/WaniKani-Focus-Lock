Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
ScriptDir = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run Chr(34) & ScriptDir & "\launcher.bat" & Chr(34), 0
Set WshShell = Nothing