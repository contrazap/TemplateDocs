import { describe, expect, it } from 'vitest';
import { decide, type Latest } from '../src/lib/updates';

const latest: Latest = {
  apk: { versionCode: 12, versionName: '1.12', url: 'App-1.12.apk', sha256: 'x' },
  bundle: { version: '202611251000', url: 'bundle-202611251000.zip', checksum: 'y', minVersionCode: 12 },
};

describe('update decision', () => {
  it('offers the APK to older apps, and the bundle only to apps with the right native part', () => {
    expect(decide(latest, 11, '202611240900')).toEqual({ apk: true, bundle: false });
    expect(decide(latest, 12, '202611240900')).toEqual({ apk: false, bundle: true });
  });
  it('never goes back to an older or the same bundle', () => {
    expect(decide(latest, 12, '202611251000').bundle).toBe(false);
    expect(decide(latest, 12, '202611261200').bundle).toBe(false);
  });
});
