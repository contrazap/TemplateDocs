// Placeholder screen: a small checklist that proves saving, backups and updates work. Replace with the real app.
import { useState } from 'react';
import { useStore } from '../store';

export function Home() {
  const items = useStore((s) => s.data.items);
  const { addItem, toggleItem, removeItem } = useStore.getState();
  const [text, setText] = useState('');
  const add = () => {
    if (!text.trim()) return;
    addItem(text.trim());
    setText('');
  };
  return (
    <>
      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          add();
        }}
      >
        <input className="grow" value={text} onChange={(e) => setText(e.target.value)} placeholder="Add an item" />
        <button className="btn" type="submit">
          Add
        </button>
      </form>
      {items.length === 0 && <p className="muted small">Nothing here yet.</p>}
      {items.map((i) => (
        <div key={i.id} className="card row">
          <input type="checkbox" checked={i.done} onChange={() => toggleItem(i.id)} />
          <span className={`grow${i.done ? ' muted strike' : ''}`}>{i.text}</span>
          <button className="icon-btn" aria-label="Delete" onClick={() => removeItem(i.id)}>
            ✕
          </button>
        </div>
      ))}
    </>
  );
}
