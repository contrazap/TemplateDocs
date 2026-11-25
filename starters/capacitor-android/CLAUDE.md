# __APP_NAME__

Android app (Capacitor 8 + React/TypeScript) in `app/`. Full docs: `app/README.md`.

- Test: `cd app && npm test` (and `npx tsc -b`). UI changes: check visually in a browser (`npm run dev`, phone-size devtools).
- Publish changes to the phones (see README "Releasing updates"):
  - web-only changes → `npm run release -- --notes "..."` (silent update)
  - native changes (plugins, manifest, capacitor.config.ts, Java, icons) → `npm run release:apk -- --notes "..."`
  - Needs Firebase CLI login and `gh` ("C:\Program Files\GitHub CLI\gh.exe") login. Never rename APKs to get around Firebase's free-plan block on executables.
  - In PowerShell use `npm.cmd run release -- ...`: the `npm.ps1` shim drops the `--`.
- Never commit `app/android-signing/`, API keys or APKs. Commit/push only when the user asks.
- Data model changes: add a migration in `normalizeData` (`app/src/store.ts`); phone-only settings (`device`: theme, API keys, reminders) must not sync or export.
