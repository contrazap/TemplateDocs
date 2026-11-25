<#
Creates a new Capacitor 8 + React Android app from starters/capacitor-android (see CAPACITOR_ANDROID_APP.md).

  powershell -ExecutionPolicy Bypass -File scripts\new-capacitor-android-app.ps1 `
    -Path C:\MyFiles\Projects\AiProjects\HabitTracker -AppName "Habit Tracker" -AppId com.household.habittracker -GitHubOwner contrazap

Copies the starter into <Path> (files that already exist there are kept) and fills in the placeholders. Unless -SkipInstall,
it then runs npm install, builds, adds the Android platform, installs the in-app APK updater plugin and the
REQUEST_INSTALL_PACKAGES permission, sets up release signing with a new keystore in app/android-signing/, and runs the tests.
Needs Node, JDK 21 at %LOCALAPPDATA%\Programs\jdk-21 and the Android SDK (one-time PC setup in the add-on).
#>
param(
  [Parameter(Mandatory = $true)][string]$Path,
  [Parameter(Mandatory = $true)][string]$AppName,
  [Parameter(Mandatory = $true)][string]$AppId,       # e.g. com.household.habittracker; permanent once installed on a phone
  [string]$GitHubOwner,                                 # owner of the public releases repo
  [string]$ApkName,                                     # default: AppName without spaces, e.g. HabitTracker
  [string]$Slug,                                        # default: kebab-case AppName, e.g. habit-tracker
  [string]$FirebaseProject,                             # Firebase project id; can be set later in app/app.config.json
  [string]$ReleasesRepo,                                # default: <GitHubOwner>/<ApkName>-releases
  [string]$ThemeColor = '#2f7d4f',
  [switch]$SkipInstall
)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object Text.UTF8Encoding $false
$starter = (Resolve-Path (Join-Path $PSScriptRoot '..\starters\capacitor-android')).Path
function Read-Utf8([string]$p) { [IO.File]::ReadAllText($p, $utf8) }
function Write-Utf8([string]$p, [string]$t) { [IO.File]::WriteAllText($p, $t, $utf8) }
function Assert-Exit([string]$what) { if ($LASTEXITCODE) { throw "$what failed (exit $LASTEXITCODE)" } }

if ($AppId -cnotmatch '^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$') { throw "AppId must look like com.household.myapp (lowercase, dots): $AppId" }
if ($ThemeColor -notmatch '^#[0-9a-fA-F]{6}$') { throw "ThemeColor must look like #2f7d4f: $ThemeColor" }
if (-not $ApkName) { $ApkName = $AppName -replace '[^A-Za-z0-9]', '' }
if (-not $Slug) { $Slug = ($AppName.ToLower() -replace '[^a-z0-9]+', '-').Trim('-') }
if (-not $FirebaseProject) { $FirebaseProject = '__FIREBASE_PROJECT__' }
if (-not $ReleasesRepo) { $ReleasesRepo = if ($GitHubOwner) { "$GitHubOwner/$ApkName-releases" } else { '__RELEASES_REPO__' } }

$values = [ordered]@{
  '__APP_NAME__'         = $AppName
  '__APP_ID__'           = $AppId
  '__APP_SLUG__'         = $Slug
  '__APK_NAME__'         = $ApkName
  '__FIREBASE_PROJECT__' = $FirebaseProject
  '__RELEASES_REPO__'    = $ReleasesRepo
  '__THEME_COLOR__'      = $ThemeColor
}
function Format-Template([string]$text) { foreach ($k in $values.Keys) { $text = $text.Replace($k, $values[$k]) }; $text }

$Path = [IO.Path]::GetFullPath($Path)
$app = Join-Path $Path 'app'
if (Test-Path $app) { throw "$app already exists" }

# 1. Copy the starter (except native/, which goes into the Android project later) with the placeholders filled in.
$native = Join-Path $starter 'native'
foreach ($f in Get-ChildItem $starter -Recurse -File -Force | Where-Object { -not $_.FullName.StartsWith("$native\") }) {
  $rel = $f.FullName.Substring($starter.Length + 1)
  $dest = Join-Path $Path $rel
  if (Test-Path $dest) { Write-Warning "Kept the existing $rel"; continue }
  New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
  Write-Utf8 $dest (Format-Template (Read-Utf8 $f.FullName))
}
Write-Host "Starter copied to $Path"

if (-not $SkipInstall) {
  Push-Location $app
  try {
    $env:CI = '1'
    npm install; Assert-Exit 'npm install'
    npm run build; Assert-Exit 'npm run build'
    npx cap add android; Assert-Exit 'npx cap add android'

    # 2. In-app APK updater: app-local plugin registered in MainActivity.
    $javaDir = Join-Path $app ('android\app\src\main\java\' + ($AppId -replace '\.', '\'))
    if (-not (Test-Path $javaDir)) { throw "Expected the generated MainActivity in $javaDir" }
    foreach ($n in 'MainActivity.java', 'ApkUpdaterPlugin.java') {
      Write-Utf8 (Join-Path $javaDir $n) (Format-Template (Read-Utf8 (Join-Path $native $n)))
    }

    # 3. Manifest: permission to open the package installer (Capacitor's FileProvider is already declared).
    $manifest = Join-Path $app 'android\app\src\main\AndroidManifest.xml'
    $m = Read-Utf8 $manifest
    if ($m -notmatch 'androidx\.core\.content\.FileProvider') { throw 'AndroidManifest.xml has no FileProvider: add one with authorities ${applicationId}.fileprovider' }
    if ($m -notmatch 'REQUEST_INSTALL_PACKAGES') {
      $m = [regex]::new('(\r?\n[ \t]*)(<uses-permission android:name="android\.permission\.INTERNET" />)').Replace($m,
        '$1$2$1<!-- In-app updates: open the installer for a newer APK of this app -->$1<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />', 1)
      if ($m -notmatch 'REQUEST_INSTALL_PACKAGES') { throw 'Could not add REQUEST_INSTALL_PACKAGES to AndroidManifest.xml' }
      Write-Utf8 $manifest $m
    }

    # 4. Release signing from android-signing/keystore.properties (git-ignored).
    $gradle = Join-Path $app 'android\app\build.gradle'
    $g = Read-Utf8 $gradle
    if ($g -notmatch 'signingProps') {
      $signing = @'
    // Release signing: keystore lives in app/android-signing (keep a backup: updates must be signed with the same key).
    def signingProps = new Properties()
    def signingFile = rootProject.file('../android-signing/keystore.properties')
    if (signingFile.exists()) signingFile.withInputStream { signingProps.load(it) }
    signingConfigs {
        release {
            if (signingFile.exists()) {
                storeFile file(signingProps['storeFile'])
                storePassword signingProps['storePassword']
                keyAlias signingProps['keyAlias']
                keyPassword signingProps['keyPassword']
            }
        }
    }

'@
      # $0 is the matched "buildTypes { release {"; the signing block contains no "$", so it is safe in a replacement string.
      $g = [regex]::new('(?m)^[ \t]*buildTypes\s*\{\s*release\s*\{').Replace($g,
        $signing + '$0' + "`n            signingConfig signingFile.exists() ? signingConfigs.release : null", 1)
      if ($g -notmatch 'signingConfigs\.release') { throw 'Could not add release signing to android/app/build.gradle' }
      Write-Utf8 $gradle $g
    }

    $signDir = Join-Path $app 'android-signing'
    if (-not (Test-Path (Join-Path $signDir 'keystore.properties'))) {
      $keytool = Join-Path $env:LOCALAPPDATA 'Programs\jdk-21\bin\keytool.exe'
      if (-not (Test-Path $keytool)) { $keytool = 'keytool' }
      New-Item -ItemType Directory -Force $signDir | Out-Null
      $alias = $Slug -replace '-', ''
      $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'
      $bytes = New-Object byte[] 24
      [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
      $pass = -join ($bytes | ForEach-Object { $chars[$_ % $chars.Length] })
      & $keytool -genkeypair -keystore (Join-Path $signDir "$alias.jks") -storetype PKCS12 -alias $alias -keyalg RSA -keysize 2048 -validity 10000 `
        -storepass $pass -keypass $pass -dname "CN=$AppName" -noprompt
      Assert-Exit 'keytool'
      Write-Utf8 (Join-Path $signDir 'keystore.properties') "storeFile=../../android-signing/$alias.jks`nstorePassword=$pass`nkeyAlias=$alias`nkeyPassword=$pass`n"
      Write-Host "Release keystore created in $signDir"
    }

    npx cap sync android; Assert-Exit 'npx cap sync android'
    npm test; Assert-Exit 'npm test'
  } finally {
    Pop-Location
  }
}

$todo = @()
if ($SkipInstall) { $todo += 'Run this script again without -SkipInstall in an empty folder, or follow the manual steps in the add-on.' }
$todo += "Back up $app\android-signing\ privately (password manager or private cloud). Without it, updates cannot install."
if ($FirebaseProject -eq '__FIREBASE_PROJECT__') { $todo += 'Create the Firebase project and set "firebaseProject" in app\app.config.json and the two README links.' }
if ($ReleasesRepo -eq '__RELEASES_REPO__') { $todo += 'Set "releasesRepo" in app\app.config.json.' }
$todo += "Create the public releases repo: gh repo create $ReleasesRepo --public --add-readme"
$todo += 'Icons: put icon-only.png, icon-foreground.png, icon-background.png, splash.png, splash-dark.png in app\assets, then: npx @capacitor/assets generate --android'
$todo += 'git init, first commit, then the first release: npm run release:apk -- --notes "First release"'
Write-Host "`nDone. Next steps:"
$i = 0; foreach ($t in $todo) { $i++; Write-Host "  $i. $t" }
