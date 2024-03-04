$installDir = "C:\Program Files\Fake PowerShell"

New-Item -Path $installDir -ItemType Directory -Force

Invoke-WebRequest -Uri "https://github.com/Zinkelburger/Fake-Powershell/blob/main/script.exe?raw=true" -OutFile "$installDir\script.exe"
Invoke-WebRequest -Uri "https://github.com/Zinkelburger/Fake-Powershell/blob/main/powershell.ico?raw=true" -OutFile "$installDir\powershell.ico"

$windowsPowerShellDir = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Windows PowerShell"
New-Item -Path $windowsPowerShellDir -ItemType Directory -Force

# Issues with creating (x86) shorcut. It ranked higher than the main one, and a ZWSP to make it rank higher was not liked by powershell
$shortcutNames = @("Windows PowerShell")
foreach ($name in $shortcutNames) {
    $shortcutPath = "$windowsPowerShellDir\$name.lnk"
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "$installDir\script.exe"
    $shortcut.IconLocation = "$installDir\powershell.ico"
    $shortcut.WorkingDirectory = $installDir
    $shortcut.Save()
}

$oldPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$newPath = "$installDir;$oldPath"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
