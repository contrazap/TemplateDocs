// Persistence: a JSON file in the app's private data dir on Android (survives updates), localStorage in a browser.
// Writes are debounced. A backup copy is written on each app start for recovery if the main file is ever unreadable.
import { Capacitor } from '@capacitor/core';
import { Directory, Encoding, Filesystem } from '@capacitor/filesystem';

const FILE = '__APP_SLUG__-data.json';
const BACKUP = '__APP_SLUG__-backup.json';
const native = Capacitor.isNativePlatform();

async function readNative(path: string): Promise<string | null> {
  try {
    const r = await Filesystem.readFile({ path, directory: Directory.Data, encoding: Encoding.UTF8 });
    return typeof r.data === 'string' ? r.data : null;
  } catch {
    return null;
  }
}

/** Returns parsed state, falling back to the backup copy if the main file is unreadable. */
export async function loadState<T>(): Promise<T | null> {
  const candidates = native ? [await readNative(FILE), await readNative(BACKUP)] : [localStorage.getItem(FILE), localStorage.getItem(BACKUP)];
  for (const raw of candidates) {
    if (!raw) continue;
    try {
      return JSON.parse(raw) as T;
    } catch {
      /* try next */
    }
  }
  return null;
}

async function writeNow(json: string) {
  if (!native) localStorage.setItem(FILE, json);
  else await Filesystem.writeFile({ path: FILE, data: json, directory: Directory.Data, encoding: Encoding.UTF8 });
}

export async function writeBackup(json: string) {
  if (!native) localStorage.setItem(BACKUP, json);
  else await Filesystem.writeFile({ path: BACKUP, data: json, directory: Directory.Data, encoding: Encoding.UTF8 });
}

let timer: ReturnType<typeof setTimeout> | undefined;
let pending: string | null = null;

export function saveDebounced(json: string) {
  pending = json;
  clearTimeout(timer);
  timer = setTimeout(flush, 400);
}

/** Write any pending save now. Call before the app pauses, exits, reloads or installs an update. */
export async function flush() {
  clearTimeout(timer);
  if (pending == null) return;
  const json = pending;
  pending = null;
  try {
    await writeNow(json);
  } catch (e) {
    console.error('save failed', e);
    pending = pending ?? json;
  }
}

// ---------------------------------------------------------------- rolling backups
// The last KEEP_BACKUPS copies of the data are kept on the phone: one a day, plus one before anything that
// replaces data (import, restore, reset). The oldest is deleted automatically.

export const KEEP_BACKUPS = 7;
const BACKUP_DIR = 'backups';
const WEB_PREFIX = '__APP_SLUG__-backup:';

export interface BackupInfo {
  name: string;
  at: number;
  reason: string;
}

const parseName = (name: string): BackupInfo | null => {
  const m = name.match(/^backup-(\d+)-(.+)\.json$/);
  return m ? { name, at: Number(m[1]), reason: decodeURIComponent(m[2]) } : null;
};

export async function listBackups(): Promise<BackupInfo[]> {
  let names: string[] = [];
  if (!native) names = Object.keys(localStorage).filter((k) => k.startsWith(WEB_PREFIX)).map((k) => k.slice(WEB_PREFIX.length));
  else {
    try {
      names = (await Filesystem.readdir({ path: BACKUP_DIR, directory: Directory.Data })).files.map((f) => f.name);
    } catch {
      names = [];
    }
  }
  return names
    .map(parseName)
    .filter((b): b is BackupInfo => !!b)
    .sort((a, b) => b.at - a.at);
}

async function removeBackup(name: string) {
  if (!native) localStorage.removeItem(WEB_PREFIX + name);
  else await Filesystem.deleteFile({ path: `${BACKUP_DIR}/${name}`, directory: Directory.Data }).catch(() => {});
}

/** Saves a backup of `data` and deletes the oldest beyond KEEP_BACKUPS. */
export async function saveBackup(reason: string, data: unknown) {
  const at = Date.now();
  const name = `backup-${at}-${encodeURIComponent(reason)}.json`;
  const json = JSON.stringify({ app: '__APP_SLUG__', backupAt: new Date(at).toISOString(), reason, data });
  if (!native) localStorage.setItem(WEB_PREFIX + name, json);
  else await Filesystem.writeFile({ path: `${BACKUP_DIR}/${name}`, data: json, directory: Directory.Data, encoding: Encoding.UTF8, recursive: true });
  const all = await listBackups();
  for (const old of all.slice(KEEP_BACKUPS)) await removeBackup(old.name);
}

/** Backup file contents as text (for restore or sharing). */
export async function readBackup(name: string): Promise<string> {
  if (!native) return localStorage.getItem(WEB_PREFIX + name) ?? '';
  const r = await Filesystem.readFile({ path: `${BACKUP_DIR}/${name}`, directory: Directory.Data, encoding: Encoding.UTF8 });
  return typeof r.data === 'string' ? r.data : '';
}

/** Makes the daily backup if the newest one is older than ~20 hours. */
export async function dailyBackup(data: unknown) {
  const newest = (await listBackups())[0];
  if (!newest || Date.now() - newest.at > 20 * 3600000) await saveBackup('daily', data);
}
