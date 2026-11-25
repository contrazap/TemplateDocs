import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Version of this web bundle, e.g. 202611242130. Release builds set WEB_VERSION so the APK and the live-update
// bundle agree; local builds get the current time. Newer bundles have larger numbers.
const now = new Date();
const pad = (n: number) => String(n).padStart(2, '0');
const WEB_VERSION = process.env.WEB_VERSION || `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}${pad(now.getHours())}${pad(now.getMinutes())}`;

export default defineConfig({
  plugins: [react()],
  define: { __WEB_VERSION__: JSON.stringify(WEB_VERSION) },
  base: './',
  build: { outDir: 'dist', target: 'es2020' },
});
