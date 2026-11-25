# __APP_NAME__

<!-- One or two sentences: what the app does and who uses it. -->

**Stack:** React + TypeScript (Vite) running inside Capacitor 8. All app logic is web code; the Android project in `android/` is only a shell plus the small `ApkUpdater` plugin. Data is a single JSON file in the app's private storage.

## Install on the phone

1. Download the APK from https://__FIREBASE_PROJECT__.web.app (or copy `../__APK_NAME__.apk`).
2. Open it and allow "Install unknown apps" for the browser or file manager when Android asks.
3. From then on the app updates itself (see *Releasing updates*). Installing a newer APK over the old one also works. Your data is kept.

## Using it

<!-- A table of screens/tabs and what each does. -->

## Maintaining the code

| File | Purpose |
|---|---|
| `app.config.json` | App name, APK name, Firebase project, releases repo, theme colour. Read by the release script, the build script and the updater. |
| `src/store.ts` | App state and actions (zustand). `data` is the content; `device` is phone-only settings. Data migrations live in `normalizeData`. |
| `src/lib/storage.ts` | Saving to the phone (debounced), backup copy, rolling backups (last 7). |
| `src/lib/updates.ts`, `android/.../ApkUpdaterPlugin.java` | In-app updates (see below). |
| `scripts/release.mjs`, `build-apk.ps1` | Publishing and APK builds. |
| `src/screens/*`, `src/components/*` | UI. Styles are in `src/styles.css`. |
| `tests/*.test.ts` | Tests (`npm test`). |

```bash
npm install
npm run dev      # open http://localhost:5173 in a browser with phone-size devtools
npm test
npm run apk      # signed release APK -> ../__APK_NAME__.apk (bumps versionCode); local only, not published
```

Building needs JDK 21 at `%LOCALAPPDATA%\Programs\jdk-21` and the Android SDK with platform 36.

**Keep `android-signing/` safe.** It holds the keystore and its password. Updates only install over the existing app when they are signed with the same key. If the key is lost, the app has to be uninstalled (losing its data unless exported) before a new build installs.

## Releasing updates

Phones check for updates when the app opens (at most every 3 hours) or with Settings → App updates → **Check now**.

| Command | Use it for | What phones see |
|---|---|---|
| `npm run release -- --notes "What changed"` | Changes to screens and logic (anything in `src/`). Most releases. | Nothing to install: the update downloads by itself and switches on the next app start, or at once with **Restart now**. |
| `npm run release:apk -- --notes "What changed"` | Native changes: new or upgraded Capacitor plugins, `AndroidManifest.xml` (permissions), `capacitor.config.ts`, Java code, icons. | "Update available → **Update**", then Android's **Install** prompt. |

The script runs `npm test` first (`--skip-tests` skips it). Add `--no-deploy` to build without publishing.

**Where things go:**

- Web bundle and `updates/latest.json` → Firebase Hosting, https://__FIREBASE_PROJECT__.web.app/updates/ (`hosting/`, git-ignored, rebuilt by the script). Firebase's free plan does not allow APK files there.
- APKs → GitHub releases of the public repo `__RELEASES_REPO__` (tag `v<versionName>`). The app checks the APK's SHA-256 before installing.

**One-time setup on a new PC:** `npx firebase-tools login`, install the GitHub CLI and run `gh auth login`, and copy `android-signing/` from your backup.

**How it decides:** a bundle only goes to phones whose installed APK `versionCode` is at least the bundle's `minVersionCode` (the APK it was built with), so phones on an older APK get the APK prompt instead. A failed bundle start rolls back to the previous one. Installing a new APK drops downloaded bundles.

## Accounts and services

| What | Where | Notes |
|---|---|---|
| Source code | GitHub (private repo) | Branch `main`. |
| APK downloads | GitHub `__RELEASES_REPO__` (public) | Only APKs; the app downloads from here. |
| Update server | Firebase project `__FIREBASE_PROJECT__` (free Spark plan) | Hosting (`firebase.json`). |

**Secrets, never commit:** `android-signing/` (keystore + password; keep a private backup), API keys. `.gitignore` already excludes them and APKs.

## Troubleshooting

- **Update not showing:** Settings → App updates → **Check now**. Its status line shows the last error.
- **"Allow from this source":** Android asks once before the app may install updates. Turn it on, go back, tap Update again.
- **APK download very slow:** GitHub downloads can be slow on some Wi-Fi networks; try mobile data.
- **Bundle broke the app:** it rolls back to the previous bundle by itself if the app doesn't start. Fix and release again; `release:apk` always resets phones to the APK's built-in code.

## Development notes

- `build-apk.ps1` bumps `versionCode`/`versionName` in `android/app/build.gradle` on every build (versionName is `1.<versionCode>`).
- After adding a Capacitor plugin: `npx cap sync android` (the APK build does this) and release with `release:apk`.
