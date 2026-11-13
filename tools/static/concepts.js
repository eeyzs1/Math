/* Shared source for the two offline concept checklists. */
(() => {
  'use strict';
  const messages = __MESSAGES__;
  const boxes = [...document.querySelectorAll('.concept input')];
  const ids = new Set(boxes.map(box => box.id));
  const sections = [...document.querySelectorAll('[data-module]')].map(section => ({
    counter: section.querySelector('[data-count]'),
    lessons: [...section.querySelectorAll('.concept')].map(lesson => ({
      boxes: [...lesson.querySelectorAll('input')], counter: lesson.querySelector('[data-count]'),
    })),
  }));
  const status = document.getElementById('storage-status');
  let state = Object.create(null);

  function read(raw) {
    const parsed = JSON.parse(raw || '{}');
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('Invalid progress');
    const clean = Object.create(null);
    for (const id of ids) if (Object.hasOwn(parsed, id) && parsed[id] === true) clean[id] = true;
    return clean;
  }

  function save(prefix = '') {
    try {
      localStorage.setItem(messages.key, JSON.stringify(state));
      status.textContent = prefix + messages.saved;
    } catch {
      status.textContent = prefix + messages.volatile;
    }
  }

  function refresh() {
    let done = 0;
    for (const section of sections) {
      let sectionDone = 0, sectionTotal = 0;
      for (const lesson of section.lessons) {
        let lessonDone = 0;
        for (const box of lesson.boxes) {
          box.checked = state[box.id] === true;
          if (box.checked) lessonDone++;
        }
        lesson.counter.textContent = `${lessonDone}/${lesson.boxes.length}`;
        sectionDone += lessonDone; sectionTotal += lesson.boxes.length;
      }
      section.counter.textContent = `${sectionDone}/${sectionTotal}`;
      done += sectionDone;
    }
    document.getElementById('total').textContent = messages.total + done + ' / ' + boxes.length + messages.items;
  }

  try { state = read(localStorage.getItem(messages.key)); }
  catch (error) { status.textContent = error instanceof SyntaxError || error.message === 'Invalid progress' ? messages.corrupt : messages.volatile; }
  for (const box of boxes) box.addEventListener('change', () => {
    if (box.checked) state[box.id] = true; else delete state[box.id];
    save(); refresh();
  });
  document.getElementById('reset').addEventListener('click', () => {
    if (confirm(messages.confirmReset)) { state = Object.create(null); save(); refresh(); }
  });
  document.getElementById('export').addEventListener('click', () => {
    const backup = {version: 1, checked: [...ids].filter(id => state[id] === true)};
    const url = URL.createObjectURL(new Blob([JSON.stringify(backup, null, 2)], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url; link.download = 'math-progress.json';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
    status.textContent = messages.exported;
  });
  document.getElementById('import').addEventListener('change', async event => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      if (file.size > 1024 * 1024) throw new Error('Oversized backup');
      const backup = JSON.parse(await file.text());
      if (!backup || backup.version !== 1 || !Array.isArray(backup.checked)
          || backup.checked.some(id => typeof id !== 'string' || !ids.has(id))) throw new Error('Invalid backup');
      if (Object.keys(state).length && !confirm(messages.confirmImport)) return;
      const next = Object.create(null);
      for (const id of backup.checked) next[id] = true;
      state = next; save(messages.imported + ' '); refresh();
    } catch { status.textContent = messages.invalid; }
    finally { event.target.value = ''; }
  });
  addEventListener('storage', event => {
    if (event.key !== messages.key && event.key !== null) return;
    try { state = read(event.newValue); refresh(); }
    catch { status.textContent = messages.corrupt; }
  });
  refresh();
})();
