# Remember your real powershell is C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
$backupDir = "C:\Program Files\Fake Powershell\PowerShellShortcutsBackup"

$userProfiles = Get-ChildItem -Path "C:\Users" -Directory

$adminToolsDir = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Administrative Tools"
$adShortcutName = "Active Directory PowerShell Snap-In.lnk"

if (Test-Path "$backupDir\$adShortcutName") {
    Copy-Item -Path "$backupDir\$adShortcutName" -Destination $adminToolsDir -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "The shortcut '$adShortcutName' was not found in the backup directory."
}

foreach ($user in $userProfiles) {
    $powershellDir = "$($user.FullName)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Windows PowerShell"
    if (Test-Path $powershellDir) {
        Copy-Item -Path "$backupDir\*" -Destination $powershellDir -Force
    }
}
