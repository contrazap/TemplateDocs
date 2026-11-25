// Publish an update to the phones. Names and addresses come from app.config.json.
// The web bundle and latest.json go to Firebase Hosting (https://<firebaseProject>.web.app/updates/);
// APKs go to GitHub releases of the public repo <releasesRepo> (Firebase's free plan doesn't allow APK files). Needs `gh auth login`.
//
//   npm run release -- --notes "What changed"         web-only update: phones switch to it on their own
//   npm run release:apk -- --notes "What changed"     new APK too (needed after native changes: plugins, permissions, capacitor.config.ts)
//   --no-deploy    build everything without publishing
//   --skip-tests   don't run `npm test` first
//
// Writes hosting/updates/{latest.json, bundle-<version>.zip} and hosting/index.html, deploys hosting/;
// with --apk also creates GitHub release v<versionName>.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const withApk = args.includes('--apk');
const deploy = !args.includes('--no-deploy');
const notes = args.includes('--notes') ? args[args.indexOf('--notes') + 1] : '';
const ROOT = fileURLToPath(new URL('..', import.meta.url)); // app/
const HOSTING = join(ROOT, 'hosting');
const UPDATES = join(HOSTING, 'updates');
const config = JSON.parse(readFileSync(join(ROOT, 'app.config.json'), 'utf8'));
for (const [k, v] of Object.entries(config)) if (/^__\w+__$/.test(v)) throw new Error(`Set "${k}" in app.config.json first`);
const { appName, apkName, firebaseProject: PROJECT, releasesRepo: RELEASES_REPO, themeColor } = config;
const SITE = `https://${PROJECT}.web.app`;
const GH = process.env.GH || (process.platform === 'win32' && existsSync('C:/Program Files/GitHub CLI/gh.exe') ? 'C:/Program Files/GitHub CLI/gh.exe' : 'gh');
const win = process.platform === 'win32';

const run = (cmd, argv, env = {}) => execFileSync(cmd, argv, { stdio: 'inherit', cwd: ROOT, env: { ...process.env, ...env }, shell: win });
const sha256 = (file) => createHash('sha256').update(readFileSync(file)).digest('hex');
const pad = (n) => String(n).padStart(2, '0');
const d = new Date();
const WEB_VERSION = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}${pad(d.getHours())}${pad(d.getMinutes())}`;

mkdirSync(UPDATES, { recursive: true });
const latestFile = join(UPDATES, 'latest.json');
let prev = existsSync(latestFile) ? JSON.parse(readFileSync(latestFile, 'utf8')) : null;
if (!prev && !withApk) {
  // New PC or cleaned folder: continue from what the phones see now.
  const r = await fetch(`${SITE}/updates/latest.json?t=${Date.now()}`).catch(() => null);
  if (r?.ok) prev = await r.json();
}
if (!withApk && !prev) throw new Error('The first release must include the APK: npm run release:apk');

// 1. Test and build (the APK and the bundle carry the same WEB_VERSION).
if (!args.includes('--skip-tests')) run('npm', ['test']);
if (withApk) run('powershell', ['-ExecutionPolicy', 'Bypass', '-File', 'build-apk.ps1'], { WEB_VERSION });
else run('npm', ['run', 'build'], { WEB_VERSION });

const gradle = readFileSync(join(ROOT, 'android/app/build.gradle'), 'utf8');
const versionCode = Number(gradle.match(/versionCode (\d+)/)[1]);
const versionName = gradle.match(/versionName "([^"]+)"/)[1];

// 2. Web bundle zip (files at the zip root, forward slashes: Windows' bsdtar does that).
for (const f of readdirSync(UPDATES)) if (f.startsWith('bundle-')) rmSync(join(UPDATES, f));
const zip = join(UPDATES, `bundle-${WEB_VERSION}.zip`);
const tar = win ? 'C:/Windows/System32/tar.exe' : 'tar';
execFileSync(tar, ['-a', '-c', '-f', zip, '-C', join(ROOT, 'dist'), ...readdirSync(join(ROOT, 'dist'))], { stdio: 'inherit' });

// 3. APK (new, or the one already published).
let apk = prev?.apk;
let apkFile;
if (withApk) {
  const name = `${apkName}-${versionName}.apk`;
  apkFile = join(ROOT, 'android/app/build/outputs/apk/release', name);
  copyFileSync(join(ROOT, '..', `${apkName}.apk`), apkFile);
  apk = {
    versionCode,
    versionName,
    url: `https://github.com/${RELEASES_REPO}/releases/download/v${versionName}/${name}`,
    sha256: sha256(apkFile),
    size: statSync(apkFile).size,
  };
}

// A bundle needs the native part it was built with: phones on an older APK are offered the APK instead.
const latest = {
  apk,
  bundle: { version: WEB_VERSION, url: `bundle-${WEB_VERSION}.zip`, checksum: sha256(zip), minVersionCode: apk.versionCode },
  notes,
  publishedAt: Date.now(),
};
writeFileSync(latestFile, JSON.stringify(latest, null, 2));

// 4. A plain download page for first installs.
writeFileSync(
  join(HOSTING, 'index.html'),
  `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${appName}</title>
<style>body{font:16px system-ui,sans-serif;max-width:32rem;margin:3rem auto;padding:0 1rem;color:#1d2a22}a.b{display:inline-block;background:${themeColor};color:#fff;padding:.8rem 1.2rem;border-radius:12px;text-decoration:none}</style>
<h1>${appName}</h1><p>Version ${apk.versionName}. Once installed, the app updates itself.</p>
<p><a class="b" href="${apk.url}">Download for Android</a></p>`,
);

console.log(`\nRelease ready: app ${apk.versionName} (${apk.versionCode}), content ${WEB_VERSION}${notes ? ` — ${notes}` : ''}`);
if (deploy) {
  // APK first, so latest.json never points at a release that doesn't exist yet.
  if (apkFile)
    execFileSync(GH, ['release', 'create', `v${versionName}`, apkFile, '--repo', RELEASES_REPO, '--title', `${appName} ${versionName}`, '--notes', notes || `${appName} ${versionName}`], { stdio: 'inherit' });
  run('npx', ['--yes', 'firebase-tools', 'deploy', '--only', 'hosting', '--project', PROJECT, '--non-interactive']);
  console.log(`Published: ${SITE}`);
}
