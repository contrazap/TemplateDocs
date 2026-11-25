import { describe, expect, it } from 'vitest';
import { normalizeData, SCHEMA_VERSION } from '../src/store';

describe('normalizeData', () => {
  it('turns missing or partial data into a complete current-version object', () => {
    expect(normalizeData(undefined)).toEqual({ schemaVersion: SCHEMA_VERSION, items: [] });
    const d = normalizeData({ items: [{ id: 'a', text: 'Milk' } as never] });
    expect(d.schemaVersion).toBe(SCHEMA_VERSION);
    expect(d.items[0]).toMatchObject({ id: 'a', text: 'Milk', done: false });
  });
});
