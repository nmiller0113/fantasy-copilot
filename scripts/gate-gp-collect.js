// Games played, once per pass (it is the same in every league). Paste into a Yahoo Fantasy tab AFTER setting
// window.GATE_GP = {prefix: 'gate_DATE_', lid: ANY_LEAGUE_ID}. Saves key prefix + 'GP'; done: window.GPDONE.
// 16 pages (400 players) of all players sorted by season points and by last-4 points, with GP* per player.
window.GPLOG = []; window.GPDONE = false;
(async () => {
  const C = window.GATE_GP, sleep = ms => new Promise(r => setTimeout(r, ms));
  const clean = s => (s || '').replace(/[-]/g, '').replace(/\s+/g, ' ').trim();
  const out = [], cov = [];
  for (const [label, stat] of [['GP ALL season2026', 'S_S_2026'], ['GP ALL last4wk', 'S_L4W']]) {
    out.push('## ' + label); let got = 0, ok = true, note = '';
    for (let p = 0; p < 16; p++) {
      let d = null;
      for (let a = 1; a <= 4 && !d; a++) {
        await sleep(a === 1 ? 450 : 3000 * a);
        try { const r = await fetch(`/f1/${C.lid}/players?status=ALL&pos=O&stat1=${stat}&cut_type=9&myteam=0&sort=PTS&sdir=1&count=${p * 25}`, { credentials: 'include' });
          if (r.status !== 200) { note = 'HTTP ' + r.status; continue; }
          const x = new DOMParser().parseFromString(await r.text(), 'text/html');
          if (/There was a problem/i.test(x.title)) { note = 'error page'; continue; }
          d = x; } catch (e) { note = String(e); }
      }
      const t = d && [...d.querySelectorAll('table')].find(x => x.tHead && /GP/.test(x.tHead.textContent) && x.tBodies[0] && x.tBodies[0].rows.length > 1);
      if (!t) { ok = false; note = note || ('page ' + p + ' no table'); break; }
      const h = [...t.tHead.rows[t.tHead.rows.length - 1].cells].flatMap(c => Array(c.colSpan || 1).fill(clean(c.textContent)));
      const gi = h.findIndex(x => /^GP\*?$/.test(x)), pi = h.findIndex(x => /^(Offense|Player|Players)$/.test(x));
      for (const r of t.tBodies[0].rows) { const c = [...r.cells]; const a = c[pi] && (c[pi].querySelector('a.name') || c[pi].querySelector('.ysf-player-name a')); if (!a) continue;
        const name = clean(a.textContent); const rest = clean(c[pi].textContent).replace(name, '').trim();
        out.push(`slot: | ${name} {${rest}} | GP*:${clean((c[gi] || {}).textContent)}`); got++; }
    }
    cov.push(['COV', 'GP', label, '400 rows', got, ok && got >= 390 ? 'OK' : 'FAIL', note].join('|'));
  }
  out.push('## COVERAGE'); out.push(...cov);
  localStorage.setItem(C.prefix + 'GP', out.join('\n')); GPLOG.push('GP saved ' + out.length + ' lines'); GPDONE = true;
})();
'GP collector started';
