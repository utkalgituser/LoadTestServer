$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\.."

if (-not (Test-Path server.pid)) { Write-Host "no pid file"; exit 0 }
$pid = Get-Content server.pid
$proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Id $pid -Force
    Write-Host "stopped $pid"
} else {
    Write-Host "stale pid $pid"
}
Remove-Item server.pid -Force -ErrorAction SilentlyContinue
