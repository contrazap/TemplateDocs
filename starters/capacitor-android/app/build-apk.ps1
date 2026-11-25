# Builds a signed release APK and copies it to ..\<apkName>.apk (apkName from app.config.json).
# Usage (from this folder):  npm run apk   or   powershell -ExecutionPolicy Bypass -File .\build-apk.ps1 [-NoBump]
param([switch]$NoBump)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$utf8 = New-Object Text.UTF8Encoding $false   # read and write files as UTF-8: Windows PowerShell's default (ANSI) mangles non-ASCII text on every build

$env:JAVA_HOME = "$env:LOCALAPPDATA\Programs\jdk-21"   # Capacitor 8 needs JDK 21
if (-not (Test-Path "$env:JAVA_HOME\bin\java.exe")) { throw "JDK 21 not found at $env:JAVA_HOME (see the add-on's one-time PC setup)" }
$env:CI = '1'                                          # no interactive CLI prompts
if (-not (Test-Path 'android-signing\keystore.properties')) { throw 'android-signing\keystore.properties is missing: restore it from your backup (an APK signed with another key will not install over the existing app)' }

$config = [IO.File]::ReadAllText((Resolve-Path 'app.config.json'), $utf8) | ConvertFrom-Json

# Bump versionCode so the phone accepts the APK as an update (data is kept). versionName is 1.<versionCode>.
$gradle = (Resolve-Path 'android\app\build.gradle').Path
if (-not $NoBump) {
  $text = [IO.File]::ReadAllText($gradle, $utf8)
  $code = [int]([regex]::Match($text, 'versionCode (\d+)').Groups[1].Value) + 1
  $text = $text -replace 'versionCode \d+', "versionCode $code" -replace 'versionName "[^"]*"', "versionName `"1.$code`""
  [IO.File]::WriteAllText($gradle, $text, $utf8)
  Write-Host "versionCode -> $code"
}

npm run build
if ($LASTEXITCODE) { throw 'web build failed' }
npx cap sync android
if ($LASTEXITCODE) { throw 'cap sync failed' }
Push-Location android
.\gradlew.bat assembleRelease --no-daemon
$ok = $LASTEXITCODE
Pop-Location
if ($ok) { throw 'gradle build failed' }
$out = "..\$($config.apkName).apk"
Copy-Item android\app\build\outputs\apk\release\app-release.apk $out -Force
Write-Host "APK ready: $(Resolve-Path $out)"
