// App state (zustand). Two kinds of saved state:
//   data   – the app's content. This is what export/import and any sync would carry.
//   device – settings that belong to this phone only (theme; later API keys, reminders, "whose phone").
//            Never synced or exported, and kept when data is replaced.
// Every change to `data`'s shape needs a step in normalizeData, so older saves and imports keep working.
import { create } from 'zustand';
import { dailyBackup, flush, loadState, saveBackup, saveDebounced, writeBackup } from './lib/storage';
import type { UpdateState } from './lib/updates';

export const SCHEMA_VERSION = 1;

export interface Item {
  id: string;
  text: string;
  done: boolean;
  createdAt: number;
}

export interface AppData {
  schemaVersion: number;
  items: Item[];
}

export interface DeviceSettings {
  theme: 'system' | 'light' | 'dark';
}

interface Persisted {
  data: AppData;
  device: DeviceSettings;
}

export type Page = 'settings';

interface Store extends Persisted {
  hydrated: boolean;
  /** In-app update status (not saved). */
  appUpdate: UpdateState;
  setAppUpdate: (patch: Partial<UpdateState>) => void;
  pages: Page[];
  toast: string | null;
  hydrate: () => Promise<void>;
  update: (fn: (d: AppData) => AppData) => void;
  /** Replace all data (import, restore). A backup of the current data is saved first. */
  replaceData: (d: Partial<AppData>, reason: string) => Promise<void>;
  setDevice: (patch: Partial<DeviceSettings>) => void;
  openPage: (p: Page) => void;
  closePage: () => void;
  showToast: (text: string) => void;
  addItem: (text: string) => void;
  toggleItem: (id: string) => void;
  removeItem: (id: string) => void;
}

export const emptyData = (): AppData => ({ schemaVersion: SCHEMA_VERSION, items: [] });
export const defaultDevice = (): DeviceSettings => ({ theme: 'system' });

/** Upgrades data saved by any older version (or imported) and fills missing fields, so the app never crashes on old data. */
export function normalizeData(raw: Partial<AppData> | null | undefined): AppData {
  const r = raw ?? {};
  // Migrations go here, oldest first, keyed on r.schemaVersion, e.g.
  //   if ((r.schemaVersion ?? 0) < 2) items = items.map((i) => ({ ...i, tags: [] }));
  const items = (r.items ?? []).map((i) => ({ ...i, done: !!i.done, createdAt: i.createdAt ?? Date.now() }));
  return { ...emptyData(), ...r, items, schemaVersion: SCHEMA_VERSION };
}

export const useStore = create<Store>((set, get) => {
  const upd = (fn: (d: AppData) => AppData) => set((s) => ({ data: fn(s.data) }));
  let hydrating = false;
  let toastTimer: ReturnType<typeof setTimeout> | undefined;

  return {
    data: emptyData(),
    device: defaultDevice(),
    hydrated: false,
    appUpdate: {},
    setAppUpdate: (patch) => set((s) => ({ appUpdate: { ...s.appUpdate, ...patch } })),
    pages: [],
    toast: null,

    hydrate: async () => {
      if (hydrating) return;
      hydrating = true;
      const saved = await loadState<Persisted>();
      if (saved?.data) {
        const data = normalizeData(saved.data);
        const device = { ...defaultDevice(), ...(saved.device ?? {}) };
        set({ data, device });
        writeBackup(JSON.stringify({ data, device })).catch(() => {});
        dailyBackup(data).catch(() => {});
      }
      set({ hydrated: true });
      useStore.subscribe((s, prev) => {
        if (s.data !== prev.data || s.device !== prev.device) saveDebounced(JSON.stringify({ data: s.data, device: s.device }));
      });
    },

    update: upd,
    replaceData: async (d, reason) => {
      await saveBackup(`before ${reason}`, get().data);
      set({ data: normalizeData(d) });
    },
    setDevice: (patch) => set((s) => ({ device: { ...s.device, ...patch } })),
    openPage: (p) => set((s) => ({ pages: [...s.pages, p] })),
    closePage: () => set((s) => ({ pages: s.pages.slice(0, -1) })),
    showToast: (text) => {
      clearTimeout(toastTimer);
      set({ toast: text });
      toastTimer = setTimeout(() => set({ toast: null }), 3500);
    },

    addItem: (text) => upd((d) => ({ ...d, items: [...d.items, { id: crypto.randomUUID(), text, done: false, createdAt: Date.now() }] })),
    toggleItem: (id) => upd((d) => ({ ...d, items: d.items.map((i) => (i.id === id ? { ...i, done: !i.done } : i)) })),
    removeItem: (id) => upd((d) => ({ ...d, items: d.items.filter((i) => i.id !== id) })),
  };
});

export { flush };
