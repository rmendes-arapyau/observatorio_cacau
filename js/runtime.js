/*
 * Observatório do Cacau — runtime estático.
 * Implementa a pequena API `dash` que a página usa (dados, cálculos, desenhos e filtros),
 * para que o painel funcione como site estático (GitHub Pages ou qualquer servidor de arquivos).
 */
(function () {
  'use strict';
  const calcs = {}, draws = {}, raw = {}, status = {}, cache = {}, subs = [];
  const params = Object.assign({}, window.OBS_PARAMS || {});
  const q = new URLSearchParams(location.search);
  Object.keys(params).forEach((k) => { if (q.has(k)) params[k] = q.get(k); });

  let pending = false;
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; run(); });
  }

  function run() {
    Object.keys(draws).forEach((name) => {
      document.querySelectorAll('[data-draw="' + name + '"]').forEach((el) => {
        try { draws[name](el); } catch (e) { console.error('Desenho "' + name + '":', e); }
      });
    });
    subs.forEach((f) => { try { f(); } catch (e) { console.error(e); } });
  }

  function data(id) {
    if (id in status) return { status: status[id], data: raw[id] };
    const c = calcs[id];
    if (!c) return { status: 'missing', data: null };
    if (id in cache) return cache[id];
    const inputs = c.inputs.map(data);
    const bad = inputs.find((d) => d.status !== 'ok');
    if (bad) return { status: bad.status === 'loading' ? 'loading' : 'error', data: null };
    try {
      cache[id] = { status: 'ok', data: c.fn(...inputs.map((d) => d.data)) };
    } catch (e) {
      console.error('Cálculo "' + id + '":', e);
      cache[id] = { status: 'error', data: null };
    }
    return cache[id];
  }

  function clearCache() { Object.keys(cache).forEach((k) => delete cache[k]); }

  window.dash = {
    colors: ['var(--obs-c0)', 'var(--obs-c1)', 'var(--obs-c2)', 'var(--obs-c3)', 'var(--obs-c4)', 'var(--obs-c5)', 'var(--obs-c6)', 'var(--obs-c7)'],
    calc: (id, opts) => { calcs[id] = opts; },
    draw: (name, fn) => { draws[name] = fn; schedule(); },
    data: data,
    params: () => Object.assign({}, params),
    setParams: (obj) => {
      Object.assign(params, obj);
      clearCache();
      const u = new URL(location.href);
      Object.keys(params).forEach((k) => {
        if (String(params[k]) === String((window.OBS_PARAMS || {})[k])) u.searchParams.delete(k);
        else u.searchParams.set(k, params[k]);
      });
      history.replaceState(null, '', u);
      schedule();
    },
    setLink: (id) => { history.replaceState(null, '', location.pathname + location.search + (id ? '#' + id : '')); },
    onData: (fn) => { subs.push(fn); }
  };

  async function load() {
    const manifest = await fetch('data/manifest.json').then((r) => r.json());
    Object.keys(manifest).forEach((id) => { status[id] = 'loading'; });
    schedule();
    await Promise.all(Object.entries(manifest).map(async ([id, path]) => {
      try {
        const res = await fetch(path);
        if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
        if (path.endsWith('.csv')) raw[id] = d3.csvParse(await res.text());
        else { const j = await res.json(); raw[id] = Array.isArray(j) ? j : (j.rows || j.data || []); }
        status[id] = 'ok';
      } catch (e) {
        console.error('Base "' + id + '":', e);
        status[id] = 'error';
      }
      clearCache();
      schedule();
    }));
  }

  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(schedule, 120); });
  document.addEventListener('DOMContentLoaded', () => { schedule(); load(); });
})();
