$ErrorActionPreference = "SilentlyContinue"
Set-Location "$PSScriptRoot\.."

if (Test-Path server.pid) {
    $pid = Get-Content server.pid
    if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
        Write-Host "running pid $pid"
    } else {
        Write-Host "stopped (stale pid)"
    }
} else {
    Write-Host "stopped"
}

$port = if ($env:PORT) { $env:PORT } else { "8000" }
try {
    $r = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:$port/health"
    Write-Host $r.Content
} catch {
    Write-Host "health check failed"
}
