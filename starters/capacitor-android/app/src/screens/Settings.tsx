import { useStore, type DeviceSettings } from '../store';
import { UpdatesCard } from '../components/UpdateBanner';

export function Settings() {
  const theme = useStore((s) => s.device.theme);
  const { setDevice, closePage } = useStore.getState();
  return (
    <div className="page">
      <header className="top">
        <button className="icon-btn" aria-label="Back" onClick={closePage}>
          ←
        </button>
        <h1 className="grow">Settings</h1>
      </header>
      <div className="content">
        <div className="section-title">Theme</div>
        <div className="card row">
          {(['system', 'light', 'dark'] as DeviceSettings['theme'][]).map((t) => (
            <button key={t} className={`btn sm ${theme === t ? '' : 'soft'}`} onClick={() => setDevice({ theme: t })}>
              {t[0].toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        <div className="section-title">App updates</div>
        <UpdatesCard />
      </div>
    </div>
  );
}
