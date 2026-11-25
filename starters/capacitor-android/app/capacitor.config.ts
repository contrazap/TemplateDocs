import type { CapacitorConfig } from '@capacitor/cli';

// Changing this file is a native change: publish it with `npm run release:apk`.
const config: CapacitorConfig = {
  appId: '__APP_ID__',
  appName: '__APP_NAME__',
  webDir: 'dist',
  android: { allowMixedContent: false },
  plugins: {
    SystemBars: { insetsHandling: 'css', style: 'DEFAULT' },
    // Live (web bundle) updates from our own Firebase Hosting, checked by src/lib/updates.ts. Nothing goes to Capgo's servers.
    CapacitorUpdater: { autoUpdate: false, updateUrl: '', channelUrl: '', statsUrl: '', resetWhenUpdate: true, autoDeleteFailed: true, autoDeletePrevious: true, appReadyTimeout: 15000 },
  },
};

export default config;
