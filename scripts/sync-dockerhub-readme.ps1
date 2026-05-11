# Sync DOCKERHUB_README.md -> Docker Hub repo overview via Hub API.
#
# Usage:
#   $env:DOCKERHUB_USER = "utkalbarik"
#   $env:DOCKERHUB_PAT  = "<personal-access-token>"   # repo:admin scope
#   pwsh scripts/sync-dockerhub-readme.ps1
#
# Create PAT at: https://app.docker.com/settings/personal-access-tokens

param(
    [string]$User = $env:DOCKERHUB_USER,
    [string]$Pat  = $env:DOCKERHUB_PAT,
    [string]$Repo = "loadtest-mockserver",
    [string]$ReadmePath = "$PSScriptRoot/../DOCKERHUB_README.md",
    [string]$ShortDesc = "Lightweight async FastAPI HTTP mock & failure-simulation server for QA, k6, JMeter, Postman"
)

$ErrorActionPreference = "Stop"

if (-not $User) { throw "Set `$env:DOCKERHUB_USER (or pass -User)" }
if (-not $Pat)  { throw "Set `$env:DOCKERHUB_PAT  (or pass -Pat)" }
if (-not (Test-Path $ReadmePath)) { throw "README missing: $ReadmePath" }

$readme = Get-Content -Raw -Path $ReadmePath

Write-Host "Logging in as $User ..."
$loginBody = @{ username = $User; password = $Pat } | ConvertTo-Json -Compress
$loginResp = Invoke-RestMethod -Method Post `
    -Uri "https://hub.docker.com/v2/users/login" `
    -ContentType "application/json" `
    -Body $loginBody
$token = $loginResp.token
if (-not $token) { throw "Login failed: no token returned" }
Write-Host "OK token acquired"

$patchBody = @{
    full_description = $readme
    description      = $ShortDesc
} | ConvertTo-Json -Compress

Write-Host "Patching $User/$Repo ..."
$resp = Invoke-RestMethod -Method Patch `
    -Uri "https://hub.docker.com/v2/repositories/$User/$Repo/" `
    -Headers @{ Authorization = "JWT $token" } `
    -ContentType "application/json" `
    -Body $patchBody

Write-Host "Updated. last_updated=$($resp.last_updated)  size=$($readme.Length) chars"
Write-Host "View: https://hub.docker.com/r/$User/$Repo"
