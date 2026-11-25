import { useState } from 'react';
import { Capacitor } from '@capacitor/core';
import { useStore } from '../store';
import { applyBundleNow, checkForUpdates, installApk, WEB_VERSION } from '../lib/updates';

const fmtWeb = (v: string) => (v.length === 12 ? `${v.slice(6, 8)}/${v.slice(4, 6)} ${v.slice(8, 10)}:${v.slice(10)}` : v);

async function startInstall(toast: (t: string) => void) {
  try {
    if (!(await installApk())) toast('Turn on “Allow from this source” for __APP_NAME__, come back, then tap Update again.');
  } catch (e) {
    toast((e as Error).message);
  }
}

/** Shown on the home screen when a newer app or web update is available. */
export function UpdateBanner() {
  const u = useStore((s) => s.appUpdate);
  const toast = useStore((s) => s.showToast);
  const [busy, setBusy] = useState(false);
  if (u.downloading !== undefined) return <div className="banner">Downloading update… {u.downloading}%</div>;
  if (u.apk)
    return (
      <div className="banner">
        <b>__APP_NAME__ {u.apk.versionName} is available.</b>
        {u.apk.notes && <div className="small">{u.apk.notes}</div>}
        <div className="small muted">Android will ask you to confirm the install. Your data stays.</div>
        <button className="btn sm" disabled={busy} onClick={() => (setBusy(true), startInstall(toast).finally(() => setBusy(false)))}>
          Update
        </button>
      </div>
    );
  if (u.bundleReady)
    return (
      <div className="banner">
        <b>Update downloaded.</b> It switches on the next time you open the app.
        {u.bundleReady.notes && <div className="small">{u.bundleReady.notes}</div>}
        <button className="btn sm" onClick={() => applyBundleNow().catch((e) => toast((e as Error).message))}>
          Restart now
        </button>
      </div>
    );
  return null;
}

/** Settings card: versions, last check, "Check now". */
export function UpdatesCard() {
  const u = useStore((s) => s.appUpdate);
  const toast = useStore((s) => s.showToast);
  if (!Capacitor.isNativePlatform()) return <div className="card small muted">Updates are checked in the phone app. Web version {fmtWeb(WEB_VERSION)}.</div>;
  return (
    <div className="card">
      <div className="small">
        App {u.installed ? `${u.installed.versionName} (${u.installed.versionCode})` : '…'} · content {fmtWeb(WEB_VERSION)}
      </div>
      <div className="small muted">
        {u.checking
          ? 'Checking…'
          : u.error
            ? `Last check failed: ${u.error}`
            : u.apk
              ? `Version ${u.apk.versionName} is available.`
              : u.bundleReady
                ? 'An update is downloaded and switches on next start.'
                : u.checkedAt
                  ? `Up to date · checked ${new Date(u.checkedAt).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}`
                  : 'Checks automatically when the app opens.'}
      </div>
      <div className="row">
        <button className="btn soft sm" disabled={u.checking} onClick={() => checkForUpdates(false)}>
          Check now
        </button>
        {u.apk && (
          <button className="btn sm" disabled={u.downloading !== undefined} onClick={() => startInstall(toast)}>
            {u.downloading !== undefined ? `Downloading ${u.downloading}%` : `Install ${u.apk.versionName}`}
          </button>
        )}
        {u.bundleReady && !u.apk && (
          <button className="btn sm" onClick={() => applyBundleNow().catch((e) => toast((e as Error).message))}>
            Restart now
          </button>
        )}
      </div>
    </div>
  );
}
