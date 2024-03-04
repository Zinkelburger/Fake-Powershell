$backupDir = "C:\Program Files\Fake Powershell\PowerShellShortcutsBackup"

New-Item -Path $backupDir -ItemType Directory -Force

$userProfiles = Get-ChildItem -Path "C:\Users" -Directory

foreach ($user in $userProfiles) {
    $powershellDir = "$($user.FullName)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Windows PowerShell"
    if (Test-Path $powershellDir) {
        Move-Item -Path "$powershellDir\*" -Destination $backupDir -Force -ErrorAction SilentlyContinue
    }
}

$adminToolsDir = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Administrative Tools"
$adShortcutName = "Active Directory PowerShell Snap-In.lnk"

if (Test-Path "$adminToolsDir\$adShortcutName") {
    Move-Item -Path "$adminToolsDir\$adShortcutName" -Destination $backupDir -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "The shortcut '$adShortcutName' does not exist in the Administrative Tools directory."
}
