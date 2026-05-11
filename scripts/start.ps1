$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\.."

New-Item -ItemType Directory -Force -Path logs | Out-Null
if (-not (Test-Path .env)) { Copy-Item .env.example .env }

if (Test-Path server.pid) {
    $pid = Get-Content server.pid
    if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
        Write-Host "already running (pid $pid)"
        exit 0
    }
}

$workers = if ($env:WORKER_COUNT) { $env:WORKER_COUNT } else { "2" }
$h = if ($env:HOST) { $env:HOST } else { "0.0.0.0" }
$p = if ($env:PORT) { $env:PORT } else { "8000" }

$proc = Start-Process -FilePath "uvicorn" `
    -ArgumentList "app.main:app","--host",$h,"--port",$p,"--workers",$workers `
    -RedirectStandardOutput "logs\uvicorn.out" `
    -RedirectStandardError  "logs\uvicorn.err" `
    -PassThru -WindowStyle Hidden

$proc.Id | Out-File -Encoding ascii server.pid
Write-Host "started pid $($proc.Id) on $h`:$p"
