$ErrorActionPreference = 'Stop'

$packagesDirectory = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages'
$sourceFile = Join-Path $PSScriptRoot 'keys_user.config'
$prefsSourceFile = Join-Path $PSScriptRoot 'prefs_user.config'

if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
    throw "Source file not found: $sourceFile"
}
if (-not (Test-Path -LiteralPath $prefsSourceFile -PathType Leaf)) {
    throw "Source file not found: $prefsSourceFile"
}

if (-not (Test-Path -LiteralPath $packagesDirectory -PathType Container)) {
    throw "WinGet Packages directory not found: $packagesDirectory"
}

$targets = @(
    Get-ChildItem -LiteralPath $packagesDirectory -Directory |
        Where-Object { $_.Name -match 'sioyek' } |
        ForEach-Object { Join-Path $_.FullName 'sioyek-release-windows' } |
        Where-Object { Test-Path -LiteralPath $_ -PathType Container }
)

if ($targets.Count -eq 0) {
    throw "Could not find a Sioyek install folder under $packagesDirectory"
}

foreach ($target in $targets) {
    $destinationFile = Join-Path $target 'keys_user.config'
    $destinationFile2 = Join-Path $target 'prefs_user.config'

    Copy-Item -LiteralPath $sourceFile -Destination $destinationFile -Force
    Write-Host "Copied keys_user.config to $destinationFile"
    Copy-Item -LiteralPath $prefsSourceFile -Destination $destinationFile2 -Force
    Write-Host "Copied prefs_user.config to $destinationFile2"
}
