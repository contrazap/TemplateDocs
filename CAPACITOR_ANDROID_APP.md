# Capacitor Android app: stack, starter and release pipeline

An optional add-on for personal or household Android apps that are installed directly on a few phones (no Play Store) and run on free services. It records the stack, the one-time PC setup, how to start a new app, the app conventions, and the release pipeline that updates the phones by itself. It was extracted from the Diet Planner app (GitHub `contrazap/DietPlanner`), where all of it is in daily use.

| Part | What it is |
|---|---|
| This file | The stack, setup, conventions, release pipeline, optional modules and lessons learned. |
| `starters/capacitor-android/` | A working starter app with `__PLACEHOLDERS__`: React shell, saving and backups, in-app updates, build and release scripts, project `CLAUDE.md` and `README.md`. `native/` holds the Java files for the Android project. |
| `scripts/new-capacitor-android-app.ps1` | Creates a new app from the starter, adds the Android project, the updater plugin and release signing, and runs the tests. |

**Not for:** Play Store apps (they need an AAB, Play App Signing and store review, and may not install APKs themselves) or iOS. The web code would carry over; the release pipeline would not.

## 1. Stack

| Layer | Choice | Why |
|---|---|---|
| UI and logic | React 19 + TypeScript, Vite 8 | All app logic is web code, so it is built and checked in a desktop browser. |
| Android shell | Capacitor 8 (Android only), minSdk 24, compile/target SDK 36, JDK 21 | The Android project is a thin shell; native code only where the web can't reach. |
| State | zustand | Small, no boilerplate, easy to test outside React. |
| Saving | One JSON file in the app's private storage (`@capacitor/filesystem`, `Directory.Data`); `localStorage` in a browser | Survives updates; easy to export, back up and migrate. |
| Tests | vitest | Pure logic lives in `src/lib/` and is tested without a phone. |
| Web updates | `@capgo/capacitor-updater`, self-hosted (no Capgo account or servers) | Changes to `src/` reach phones silently. |
| APK updates | App-local `ApkUpdater` Java plugin | Downloads the new APK, checks its SHA-256 and opens Android's installer. |
| Update server | Firebase Hosting, free Spark plan | `latest.json`, web bundles and a download page at `https://<project>.web.app`. |
| APK downloads | Releases of a public GitHub repo `<owner>/<ApkName>-releases` | Firebase's free plan refuses APK files. |
| Optional | Firestore sync, local notifications, share, AI assistant | Section 7. |

## 2. One-time PC setup

- **Node** (LTS) and **Git**.
- **JDK 21** at `%LOCALAPPDATA%\Programs\jdk-21`. Capacitor 8 needs 21; the build script sets `JAVA_HOME` for itself only, so an older system JDK can stay.
- **Android SDK** at `%LOCALAPPDATA%\Android\Sdk` (Android Studio or the command-line tools) with platform 36 and build-tools.
- **GitHub CLI** at `C:\Program Files\GitHub CLI\gh.exe`, then `gh auth login`.
- **Firebase CLI** login: `npx firebase-tools login`.
- The **signing keys** of existing apps (`app/android-signing/` of each project) restored from the private backup.

## 3. Starting a new app

1. **Choose the names.** `AppId` (for example `com.household.habittracker`) is permanent: a different id is a different app on the phone. The rest can change later in `app/app.config.json`.
2. **Create the Firebase project** in the console (Analytics off), open *Hosting* and click *Get started* once so the default `<project-id>.web.app` site exists. Note the project id: Firebase often adds a suffix (`diet-planner-19eae`).
3. **Run the scaffolder** from this repository:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\new-capacitor-android-app.ps1 `
     -Path C:\MyFiles\Projects\AiProjects\HabitTracker -AppName "Habit Tracker" `
     -AppId com.household.habittracker -GitHubOwner contrazap -FirebaseProject habit-tracker-1a2b3
   ```

   Optional: `-ApkName`, `-Slug`, `-ReleasesRepo`, `-ThemeColor '#2f7d4f'`, `-SkipInstall` (copy and fill files only). Existing files in the folder (a spec, for example) are kept. Without `-SkipInstall` it runs `npm install`, builds, runs `npx cap add android`, installs the updater plugin and the `REQUEST_INSTALL_PACKAGES` permission, adds release signing to `android/app/build.gradle`, creates a keystore with a random password in `app/android-signing/`, and runs the tests. It ends with the remaining steps.
4. **Back up `app/android-signing/` privately** (password manager or private cloud) straight away.
5. **Create the releases repo:** `gh repo create <owner>/<ApkName>-releases --public --add-readme` (a release needs a commit to tag).
6. **Icons:** put `icon-only.png` (1024 px), `icon-foreground.png`, `icon-background.png`, `splash.png` and `splash-dark.png` in `app/assets/`, then `npx @capacitor/assets generate --android`.
7. **Source repo:** `git init`, commit, `gh repo create <owner>/<Name> --private --source . --push`. `.gitignore` already excludes the keystore, APKs and build output.
8. **First release:** `npm run release:apk -- --notes "First release"` from `app/`, then install from `https://<project-id>.web.app` on each phone (allow "Install unknown apps" for the browser). From then on the app updates itself.
9. **Describe the app:** a spec file at the project root (Diet Planner used `meal-planner-spec.md`), linked from `CLAUDE.md`; fill the README's *Using it* section as screens appear.

**Without the script** (or to repair a project): copy `starters/capacitor-android/` and replace the placeholders; `npm install && npm run build && npx cap add android`; copy `native/*.java` into `android/app/src/main/java/<app id as folders>/`; add `<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />` to `AndroidManifest.xml` (Capacitor's `FileProvider` is already there); add the `signingConfigs` block from the script to `android/app/build.gradle` and `signingConfig signingFile.exists() ? signingConfigs.release : null` to `buildTypes.release`; create the keystore with `keytool -genkeypair` and write `android-signing/keystore.properties` (`storeFile=../../android-signing/<alias>.jks`, `storePassword`, `keyAlias`, `keyPassword`).

## 4. App conventions

The starter follows these; keep them as the app grows.

- **Web first.** Logic and UI are web code. Native code only for what a plugin can't do; every native change means `release:apk`.
- **Two kinds of saved state.** `data` is the app's content (exported, backed up, synced). `device` is phone-only: theme, API keys, reminders, "whose phone". It never syncs or exports, and restoring or importing data keeps it.
- **Migrations.** Every change to the shape of `data` adds a step to `normalizeData` in `src/store.ts` (bump `SCHEMA_VERSION`). Saved files and imports from any older version must still load.
- **Saving.** Writes are debounced; `flush()` runs on pause, on exit from the back button and before an update installs. A backup copy is written at each start (used if the main file is unreadable), and `saveBackup()` keeps the last 7 (one a day plus one before anything that replaces data).
- **Export/import** (recommended once data matters): one JSON file with `app`, `schemaVersion` and named sections; import lets the user pick sections and *merge* (by id) or *replace*. API keys are left out unless asked.
- **Resilience.** `ErrorBoundary` shows a Reload button instead of a blank screen; a web bundle that fails to start rolls back by itself.
- **Android behaviour.** The back button closes the top page, then saves and exits. Safe areas come from `SystemBars insetsHandling: 'css'` as `--sat` / `--sab`. Theme is system/light/dark per phone.
- **Checks.** `npm test` and `npx tsc -b`; UI changes are checked in a browser at phone size (`npm run dev`, devtools device mode).

## 5. Versions and signing

- `build-apk.ps1` bumps `versionCode` in `android/app/build.gradle` on every build; `versionName` is `1.<versionCode>`. A phone only installs an APK with a higher `versionCode`.
- The web bundle version is the build time, `yyyymmddhhmm` (`WEB_VERSION`, compiled in as `__WEB_VERSION__`). The APK and the bundle from one release share it.
- Every APK must be signed with the app's keystore. With a lost key, phones have to uninstall the app (losing data that wasn't exported) before a new build installs.

## 6. Release pipeline

```text
npm run release[:apk] -- --notes "..."              (from app/)
  1. npm test, then build with WEB_VERSION          [--apk: build-apk.ps1 bumps versionCode, cap sync, gradle assembleRelease, signs]
  2. hosting/updates/bundle-<WEB_VERSION>.zip + latest.json, hosting/index.html (download page)
  3. [--apk] gh release create v<versionName> <ApkName>-<versionName>.apk  --repo <releasesRepo>
  4. firebase deploy --only hosting                 (APK first, so latest.json never points at a missing release)

Phone, on start and resume (at most every 3 h) or Settings > Check now:
  GET <site>/updates/latest.json
  apk.versionCode > installed      -> banner "Update" -> download -> SHA-256 check -> Android's Install prompt
  bundle newer and installed >= bundle.minVersionCode
                                   -> download quietly -> switches on next start ("Restart now" for at once)
                                   -> rolled back if the new bundle doesn't call notifyAppReady within 15 s
```

| Command | Use for |
|---|---|
| `npm run release -- --notes "..."` | Anything in `src/` (most releases). Phones see nothing to install. |
| `npm run release:apk -- --notes "..."` | Native changes: plugins added or upgraded, `AndroidManifest.xml`, `capacitor.config.ts`, Java, icons. Phones get the Install prompt. |
| `--no-deploy`, `--skip-tests` | Build everything without publishing; skip the tests. |

- The first release must be `release:apk`. A web-only release reuses the APK entry of the last `latest.json`: the local `hosting/updates/latest.json`, or the live one when it is missing (new PC).
- A bundle's `minVersionCode` is the published APK's `versionCode`, so phones on an older APK are offered the APK instead of a bundle that may need newer native code.
- Names and addresses live in `app/app.config.json` (`appName`, `apkName`, `firebaseProject`, `releasesRepo`, `themeColor`); the release script refuses to run while any is still a placeholder.
- Never rename APKs (or zip them) to get around Firebase's block on executables; that is what the GitHub releases repo is for.
- Publishing reaches every phone: an agent releases only when the user asks.

## 7. Optional modules

Proven in Diet Planner; copy from there when an app needs them. Each new plugin is a native change (`npx cap sync android`, then `release:apk`).

- **Sync between phones (Firestore, free plan).** Anonymous auth. A "household" document whose id is a 12-character join code and whose `members` array (max 10) lists the phones; data lives in per-record documents in subcollections, deletions as tombstones, with offline persistence and live listeners. Device-only settings never sync. Access rules in `firestore.rules` (members only; a phone can only add or remove itself; households can't be listed); publish them in the console or with `npx firebase-tools deploy --only firestore:rules`. The web config in `src/lib/firebaseConfig.ts` is not a secret. Load the sync module lazily, only when a household is set up. Reference: Diet Planner `src/lib/sync.ts`, `firestore.rules`.
- **Reminders:** `@capacitor/local-notifications` with a monochrome small icon (`ic_stat_notify`) and `iconColor` in `capacitor.config.ts`; tapping a reminder opens the relevant screen.
- **Sharing and exports:** `@capacitor/share`, writing the file to the cache directory first.
- **AI assistant:** an OpenAI-compatible chat API with tool calling (Diet Planner uses DeepSeek), the API key entered per phone in `device` settings (never synced, exported or committed). Tools map to store actions; each reply records what it changed so it can be undone on its own. Thinking models need a large `max_tokens` or they return empty answers. Reference: Diet Planner `src/lib/ai.ts`, `src/lib/changes.ts`.
- **Voice input and spoken replies** (free, on-device, no key). The Android WebView has no Web Speech API, so use plugins: `@capacitor-community/speech-recognition` (v7 works on Capacitor 8; adds `RECORD_AUDIO` and the `RecognitionService` query itself) and `@capacitor-community/text-to-speech`. Fill the text box from dictation and let the user send; keep the language and the read-aloud choice in `device` settings. Plugin quirks: with `partialResults` the recognizer's `start()` resolves at once and later errors (silence, no network) are never reported, so poll `isListening()`; the final text arrives after the `stopped` event. TTS `stop()` drops the pending `speak()` promise (it never settles), so resolve it yourself; split long text into chunks (Android takes ~4000 characters) and strip markdown and emoji first; check `isLanguageSupported` for non-English voices. In a desktop browser fall back to `SpeechRecognition`/`speechSynthesis` for `npm run dev`. Reference: Diet Planner `src/lib/voice.ts`.
- **Hands-free voice mode** (on top of the above, plus `@capacitor-community/keep-awake` so the screen doesn't dim mid-conversation). Android ends a recognizer session after 1–2 s of silence, so a turn is a chain of sessions whose text is joined, sent only after a longer silence (2.5 s default, setting) or "send it"; each `start()` destroys the previous recognizer, so restarting can't mix sessions, but wait ~0.8 s after a session ends for its final result. Bare yes/no answers send after ~0.9 s. Spoken commands ("undo", "bye") only as the whole utterance. **Confirm changes in code, not only in the prompt:** in voice mode the agent loop answers the first data-changing tool call (`mutates`) with "not applied, ask first", the reply asks "Shall I?", and only a clear yes on the next turn lets changes run. Turn the model's thinking off for voice turns (latency) and ask for 1–3 spoken sentences; let the fast model escalate by offering a voice-only `think_deeper` tool that the loop intercepts: say a filler line ("Let me think that through…") and restart the turn from fresh messages with thinking on (DeepSeek's thinking mode needs its own reasoning for tool-call turns, and don't escalate once something changed); a "think carefully…" prefix skips the fast try. Keep the mic off while the reply plays and let a tap anywhere on the screen stop it and start listening (see *Lessons learned* on talking over the reply). Pause on the app's `pause` event. Reference: Diet Planner `src/lib/voiceMode.ts`, `src/components/VoiceMode.tsx`, `runAgent` in `src/lib/ai.ts`.
- **First-install mirror:** an itch.io page with the APK (edited by hand) for people who can't reach the download page. Phones don't use it.

## 8. Lessons learned

- **Windows PowerShell 5.1 encodings.** `Get-Content`/`Set-Content` default to ANSI, so a script that rewrites a UTF-8 file corrupts its non-ASCII characters, again on every run (Diet Planner's `build.gradle` comment grew to ~50 KB). Scripts here read and write with explicit UTF-8, and `.ps1` files stay ASCII.
- **`npm run x -- --flag` in PowerShell** loses the `--` (the `npm.ps1` shim eats it). Use `npm.cmd run release -- --notes "..."` in PowerShell, or Git Bash.
- **Line endings:** with `core.autocrlf=true` files mix CRLF and LF; scripts that patch files must match both (`\r?\n`).
- **"Install unknown apps"** is asked once per source: the browser for the first install, the app itself for its updates. The app opens that setting when needed.
- **GitHub downloads** can be very slow on some home networks; mobile data helps.
- **`hosting/` is generated** and git-ignored; never edit it by hand.
- **Talking over a spoken reply doesn't work on the phone's speaker.** Tried in Diet Planner: Android's recognizer gets no echo cancellation for the TTS output and mishears the synthetic voice, so filtering out the reply's own words still lets "new" words through and the reply interrupts itself. Removed in favour of tap-anywhere to interrupt. Only revisit with headphones (native headset detection) or real echo-cancelled capture.
- **React StrictMode runs effects twice in dev:** a `mounted` ref cleared in an effect's cleanup must be set back to `true` in the effect body, or it stays `false` and silently disables whatever checks it. An effect that starts a microphone or recognizer session starts it twice in dev (the first is aborted at once); tests with scripted speech must allow for that.
- **Visual checks without the Chrome extension:** `puppeteer-core` (installed in a scratch folder) driving the installed Chrome at a phone-sized viewport against `npm run dev`. Fake what headless Chrome can't do in `evaluateOnNewDocument` (speech APIs) and answer API calls with `setRequestInterception`; answer the CORS preflight (`OPTIONS`, allowing `authorization`) before the request itself. For multi-step flows (a voice conversation), script the fakes as a queue , log timestamps from the page console, and screenshot at fixed intervals. Don't pipe the script into `head`: it kills the browser run early.

## 9. Workspace integration

- The starter's root `CLAUDE.md` holds the project rules (checks, release commands, secrets, migrations). Workspaces built from the templates in this repository carry the same lines in their conventions.
- Record app-specific facts (Firebase project, releases repo, who uses which phone) in the project README's *Accounts and services* table, not only in agent memory.
- When a project improves the stack or the pipeline, propose the matching change to `starters/capacitor-android/` and this file.
