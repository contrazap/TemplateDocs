import { useEffect } from 'react';
import { App as CapApp } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';
import { flush, useStore } from './store';
import { checkForUpdates, markAppReady } from './lib/updates';
import { UpdateBanner } from './components/UpdateBanner';
import { Home } from './screens/Home';
import { Settings } from './screens/Settings';

function useTheme() {
  const theme = useStore((s) => s.device.theme);
  useEffect(() => {
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const apply = () => {
      const dark = theme === 'dark' || (theme === 'system' && mq.matches);
      document.documentElement.dataset.theme = dark ? 'dark' : 'light';
      const bg = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim();
      document.querySelector('meta[name=theme-color]')?.setAttribute('content', bg);
    };
    apply();
    mq.addEventListener('change', apply);
    return () => mq.removeEventListener('change', apply);
  }, [theme]);
}

/** Android back button, save on pause, update checks on start and resume. */
function useNativeHooks() {
  useEffect(() => {
    if (!Capacitor.isNativePlatform()) return;
    const back = CapApp.addListener('backButton', () => {
      const s = useStore.getState();
      if (s.pages.length) s.closePage();
      else flush().finally(() => CapApp.exitApp());
    });
    const pause = CapApp.addListener('pause', () => flush());
    markAppReady().then(() => checkForUpdates());
    const resume = CapApp.addListener('resume', () => checkForUpdates());
    return () => {
      back.then((h) => h.remove());
      pause.then((h) => h.remove());
      resume.then((h) => h.remove());
    };
  }, []);
}

export default function App() {
  const hydrated = useStore((s) => s.hydrated);
  const pages = useStore((s) => s.pages);
  const toast = useStore((s) => s.toast);
  const openPage = useStore((s) => s.openPage);
  useTheme();
  useEffect(() => {
    useStore.getState().hydrate();
  }, []);
  useNativeHooks();

  if (!hydrated) return <div className="splash">Loading…</div>;
  const page = pages[pages.length - 1];

  return (
    <div className="app">
      <header className="top">
        <h1>__APP_NAME__</h1>
        <button className="icon-btn" aria-label="Settings" onClick={() => openPage('settings')}>
          ⚙
        </button>
      </header>
      <main className="content">
        <UpdateBanner />
        <Home />
      </main>
      {page === 'settings' && <Settings />}
      {toast && <div className="toast">{toast}</div>}
    </div>
  );
}
