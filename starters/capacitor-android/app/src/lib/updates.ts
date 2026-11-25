// In-app updates from our Firebase Hosting site (published by `npm run release`).
//
// updates/latest.json says what the newest release is:
//   apk:    full Android app (needed when native parts change). The app downloads it and Android asks "Install?".
//   bundle: the web part only (screens, logic). Downloaded quietly and switched to the next time the app opens,
//           or straight away with "Restart now". Only used by apps whose native part is at least minVersionCode.
import { Capacitor, CapacitorHttp, registerPlugin, type PluginListenerHandle } from '@capacitor/core';
import { App } from '@capacitor/app';
import { CapacitorUpdater } from '@capgo/capacitor-updater';
import config from '../../app.config.json';
import { flush, useStore } from '../store';

declare const __WEB_VERSION__: string;
/** Version of the web code that is running now (yyyymmddhhmm). */
export const WEB_VERSION = __WEB_VERSION__;

export const UPDATES_BASE = `https://${config.firebaseProject}.web.app/updates/`;

export interface Latest {
  apk: { versionCode: number; versionName: string; url: string; sha256: string; size?: number };
  bundle?: { version: string; url: string; checksum: string; minVersionCode: number };
  notes?: string;
  publishedAt?: number;
}

export interface UpdateState {
  checking?: boolean;
  checkedAt?: number;
  error?: string;
  installed?: { versionName: string; versionCode: number; web: string };
  apk?: Latest['apk'] & { notes?: string }; // newer app available: needs the installer
  bundleReady?: { id: string; version: string; notes?: string }; // downloaded, applies on next start
  downloading?: number; // APK download progress, %
}

/** App-local native plugin: android/app/src/main/java/.../ApkUpdaterPlugin.java */
interface ApkUpdater {
  canInstall(): Promise<{ allowed: boolean }>;
  openInstallSettings(): Promise<void>;
  downloadAndInstall(o: { url: string; sha256?: string }): Promise<void>;
  addListener(e: 'progress', cb: (p: { percent: number }) => void): Promise<PluginListenerHandle>;
}
const ApkUpdater = registerPlugin<ApkUpdater>('ApkUpdater');

const set = (patch: Partial<UpdateState>) => useStore.getState().setAppUpdate(patch);
const absolute = (url: string) => new URL(url, UPDATES_BASE).toString();

/** Tell the updater this web bundle started fine (otherwise it rolls back to the previous one). */
export async function markAppReady() {
  if (!Capacitor.isNativePlatform()) return;
  try {
    await CapacitorUpdater.notifyAppReady();
  } catch {
    /* older APK without the plugin */
  }
}

/** Pure decision, kept separate for tests. */
export function decide(latest: Latest, installedCode: number, web: string) {
  return {
    apk: latest.apk && latest.apk.versionCode > installedCode,
    bundle: !!latest.bundle && latest.bundle.version > web && installedCode >= latest.bundle.minVersionCode,
  };
}

let running: Promise<void> | null = null;

/** Check for a newer app or web bundle. `quiet` skips the check if one ran in the last few hours. */
export function checkForUpdates(quiet = true): Promise<void> {
  if (!Capacitor.isNativePlatform()) return Promise.resolve();
  const last = useStore.getState().appUpdate.checkedAt ?? 0;
  if (quiet && Date.now() - last < 3 * 3600000) return Promise.resolve();
  running ??= doCheck().finally(() => (running = null));
  return running;
}

async function doCheck() {
  set({ checking: true, error: undefined });
  try {
    const info = await App.getInfo();
    const installed = { versionName: info.version, versionCode: Number(info.build) || 0, web: WEB_VERSION };
    const r = await CapacitorHttp.get({ url: `${UPDATES_BASE}latest.json?t=${Date.now()}`, connectTimeout: 15000, readTimeout: 20000 });
    if (r.status !== 200) throw new Error(`Update check failed (${r.status})`);
    const latest = (typeof r.data === 'string' ? JSON.parse(r.data) : r.data) as Latest;
    const d = decide(latest, installed.versionCode, WEB_VERSION);
    set({ installed, apk: d.apk ? { ...latest.apk, url: absolute(latest.apk.url), notes: latest.notes } : undefined });
    if (d.bundle) await getBundle(latest.bundle!, latest.notes);
    set({ checkedAt: Date.now() });
  } catch (e) {
    set({ error: (e as Error).message });
  } finally {
    set({ checking: false });
  }
}

async function getBundle(b: NonNullable<Latest['bundle']>, notes?: string) {
  if (useStore.getState().appUpdate.bundleReady?.version === b.version) return;
  const { bundles } = await CapacitorUpdater.list();
  let bundle = bundles.find((x) => x.version === b.version && x.status !== 'error');
  if (!bundle) bundle = await CapacitorUpdater.download({ url: absolute(b.url), version: b.version, checksum: b.checksum });
  await CapacitorUpdater.next({ id: bundle.id });
  set({ bundleReady: { id: bundle.id, version: b.version, notes } });
}

/** Switch to the downloaded web bundle now (the app reloads). */
export async function applyBundleNow() {
  const b = useStore.getState().appUpdate.bundleReady;
  if (!b) return;
  await flush();
  await CapacitorUpdater.set({ id: b.id });
}

/** Download the newer APK and open Android's installer. Returns false when the install permission is needed first. */
export async function installApk(): Promise<boolean> {
  const apk = useStore.getState().appUpdate.apk;
  if (!apk) return true;
  const { allowed } = await ApkUpdater.canInstall();
  if (!allowed) {
    await ApkUpdater.openInstallSettings();
    return false;
  }
  await flush();
  const sub = await ApkUpdater.addListener('progress', (p) => set({ downloading: p.percent }));
  set({ downloading: 0 });
  try {
    await ApkUpdater.downloadAndInstall({ url: apk.url, sha256: apk.sha256 });
  } finally {
    sub.remove();
    set({ downloading: undefined });
  }
  return true;
}
