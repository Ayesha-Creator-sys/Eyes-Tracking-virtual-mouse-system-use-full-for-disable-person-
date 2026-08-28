# create_shortcut_now.ps1
# Run this once to place the shortcut on the desktop.

$ExePath  = 'C:\Users\Musharab Ali\OneDrive\Desktop\Fianl project\dist\EyeMouse AI Ultra.exe'
$WorkDir  = 'C:\Users\Musharab Ali\OneDrive\Desktop\Fianl project\dist'
$Desktop  = [Environment]::GetFolderPath('Desktop')
$LnkPath  = Join-Path $Desktop 'Eye Tracking Mouse System.lnk'

Write-Host "Desktop  : $Desktop"
Write-Host "EXE      : $ExePath"
Write-Host "Shortcut : $LnkPath"

if (-not (Test-Path $ExePath)) {
    Write-Error "EXE not found: $ExePath"
    exit 1
}

$ws  = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut($LnkPath)
$lnk.TargetPath       = $ExePath
$lnk.WorkingDirectory = $WorkDir
$lnk.IconLocation     = "$ExePath,0"
$lnk.Description      = 'Eye Tracking Mouse System - AI Powered Eye Control'
$lnk.WindowStyle      = 1   # Normal window
$lnk.Save()

if (Test-Path $LnkPath) {
    Write-Host "SUCCESS: Shortcut created at $LnkPath" -ForegroundColor Green
} else {
    Write-Error "FAILED: Shortcut was not created."
}
