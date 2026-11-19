// Yahoo collector with completeness checks. Paste into a Yahoo Fantasy tab (football.fantasysports.yahoo.com)
// AFTER setting: window.GATE_CFG = {week: WEEK, prefix: 'gate_DATE_', leagues: [["KEY", LEAGUE_ID, MY_TEAM_ID, LEAGUE_SIZE], ...]}
//   (each league: [key, lid, myTeamId, leagueSize]).  Progress: window.GLOG; done: window.GDONE === true.
// Every fetch is checked (HTTP 200, not a 999, not an error page, the expected table present) and retried 3 times.
// Team ids come from the league's own team list, never 1..N. Each league's text ends with "## COVERAGE" lines:
//   COV|<league>|<item>|<expected>|<got>|OK or FAIL|<note>     (gate.py check refuses the pass on any FAIL)
Object.keys(localStorage).filter(x => (/^gate_/.test(x) && !x.startsWith(window.GATE_CFG.prefix)) || window.GATE_CFG.leagues.some(([k]) => x === window.GATE_CFG.prefix + k)).forEach(x => localStorage.removeItem(x));  // other passes are on disk; this pass's other leagues stay
window.GLOG = []; window.GDONE = false;
window.GP = (async () => {
  const C = window.GATE_CFG, W = C.week;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const clean = s => (s || '').replace(/Video Forecast|Video Playlist|New Player Note|No new player Notes|Player Note|Video/g, '').replace(/[-]/g, '').replace(/\s+/g, ' ').trim();
  const norm = s => (s || '').replace(/[^A-Za-z0-9%*]/g, '');
  const isErr = d => /There was a problem|document you requested was not found/i.test((d.title || '') + ' ' + (d.body ? d.body.textContent.slice(0, 3000) : ''));
  // get(url, test): fetch, parse, and require test(doc) to be true; retries 3x; returns {d, ok, note, tries}
  const get = async (u, test) => {
    let note = '';
    for (let a = 1; a <= 4; a++) {
      await sleep(a === 1 ? 450 : 3000 * a);
      try {
        const r = await fetch(u, { credentials: 'include' });
        if (r.status === 999) { note = 'HTTP 999 (rate limit)'; GLOG.push('999 ' + u); await sleep(90 * 1000); continue; }
        if (r.status !== 200) { note = 'HTTP ' + r.status; continue; }
        const d = new DOMParser().parseFromString(await r.text(), 'text/html');
        d.querySelectorAll('script,style,noscript').forEach(x => x.remove());
        if (isErr(d)) { note = 'error page'; continue; }
        if (test && !test(d)) { note = 'expected table missing'; continue; }
        return { d, ok: true, note: a > 1 ? 'ok after ' + a + ' tries' : '', tries: a };
      } catch (e) { note = 'fetch error ' + e; }
    }
    return { d: null, ok: false, note, tries: 4 };
  };
  const hdrs = t => [...t.tHead.rows[t.tHead.rows.length - 1].cells].flatMap(c => Array(c.colSpan || 1).fill(clean(c.textContent)));
  const pcell = c => { const a = c.querySelector('a.name') || c.querySelector('.ysf-player-name a'); const name = a ? clean(a.textContent) : ''; let rest = clean(c.textContent); if (name) rest = rest.replace(name, '').trim(); return name ? name + ' {' + rest + '}' : rest; };
  const tableRows = (t, keep) => { const h = hdrs(t); const pi = h.findIndex(x => /^(Offense|Kickers|Defense\/Special Teams|Player|Players)$/.test(x)); return [...t.tBodies[0].rows].filter(r => r.cells.length > 3).map(r => { const c = [...r.cells]; return h.map((name, i) => { if (!keep.map(norm).includes(norm(name)) && i !== pi && i !== 0) return null; const v = i === pi ? pcell(c[i] || { textContent: '' }) : clean((c[i] || {}).textContent); return (i === 0 ? 'slot:' : (i === pi ? '' : name + ':')) + v; }).filter(x => x !== null).join(' | '); }); };
  const statTables = d => [...d.querySelectorAll('table')].filter(t => /^statTable\d/.test(t.id || ''));
  const poolTable = d => [...d.querySelectorAll('table')].find(x => x.tBodies[0] && x.tBodies[0].rows.length > 1 && x.tHead && /Roster Status|Owner/.test(x.tHead.textContent));
  const named = rows => rows.filter(x => / \{/.test(x)).length;  // rows that carry a player
  for (const [k, lid, tid, size] of C.leagues) {
    const out = [], cov = [];
    const COV = (item, exp, got, ok, note) => cov.push(['COV', k, item, exp, got, ok ? 'OK' : 'FAIL', note || ''].join('|'));
    try {
      out.push(`# ${k} Yahoo league ${lid} team ${tid} week ${W} - pulled ${new Date().toLocaleString('en-US')}`);
      // 1. team list from the league page
      let g = await get(`/f1/${lid}`, d => d.querySelectorAll('a').length > 20);
      const teams = new Map();
      if (g.ok) { const re = new RegExp('/f1/' + lid + '/(\\d+)$'); [...g.d.querySelectorAll('a')].forEach(a => { const m = (a.getAttribute('href') || '').match(re); const t = clean(a.textContent); if (m && t && t !== 'My Team') teams.set(m[1], t); }); }
      COV('team list', size, teams.size, g.ok && teams.size === size, g.note);
      out.push('TEAMS: ' + [...teams.entries()].map(([i, t]) => i + '=' + t).join(' || '));
      // standings from the same league page: rank, team id, record, points for and against
      const st = g.ok ? [...g.d.querySelectorAll('table')].find(t => t.tHead && /W-L-T/.test(t.tHead.textContent)) : null;
      const srows = [];
      if (st) { const h = hdrs(st); const iR = h.indexOf('Rank'), iW = h.indexOf('W-L-T'), iF = h.indexOf('PF'), iA = h.indexOf('PA');
        const re2 = new RegExp('/f1/' + lid + '/(\\d+)$');
        [...st.tBodies[0].rows].forEach(r => { const c = [...r.cells]; const a2 = [...r.querySelectorAll('a')].find(x => re2.test(x.getAttribute('href') || '') && clean(x.textContent));
          if (a2) srows.push(['STAND', clean((c[iR] || {}).textContent), (a2.getAttribute('href').match(re2) || [])[1], clean(a2.textContent), clean((c[iW] || {}).textContent), clean((c[iF] || {}).textContent), clean((c[iA] || {}).textContent)].join('|')); }); }
      out.push('## STANDINGS'); out.push(...srows);
      COV('standings', size, srows.length, srows.length === size, st ? '' : 'standings table missing');
      // 2. own team, six views
      const views = [['ROSTER week-' + W + ' projection view', `stat1=P&stat2=PW&week=${W}`, ['Bye', 'Fan Pts', 'Proj Max', 'Proj Min', 'Pos Rank', '% Start', '% Ros']],
        ['ROSTER ROS projection', 'stat1=P&stat2=PSR_2026', ['GP*', 'GP', 'Fan Pts', 'Pos Rank', 'Bye']], ['ROSTER NEXT 4 WEEKS projection', 'stat1=P&stat2=PN4W', ['GP*', 'GP', 'Fan Pts', 'Pos Rank', 'Bye']],
        ['ROSTER SEASON 2026 actual', 'stat1=S&stat2=S_2026', ['GP*', 'GP', 'Fan Pts', 'Pos Rank', 'Bye']], ['ROSTER LAST 4 WEEKS actual total', 'stat1=S&stat2=L4W', ['GP*', 'GP', 'Fan Pts', 'Pos Rank', 'Bye']],
        ['ROSTER WEEK ' + (W - 1) + ' actual', `stat1=S&stat2=W&week=${W - 1}`, ['GP*', 'GP', 'Fan Pts', 'Pos Rank', 'Bye']]];
      for (let vi = 0; vi < views.length; vi++) {
        const [label, q, keep] = views[vi];
        g = await get(`/f1/${lid}/${tid}?${q}`, d => statTables(d).length > 0);
        const rows = g.ok ? statTables(g.d).flatMap(t => tableRows(t, keep)) : [];
        if (vi === 0 && g.ok) { const bt = clean(g.d.body.textContent);
          out.push('HEADER: ' + [(bt.match(/\d+-\d+-\d+\s*\d+\w\w Place/) || [''])[0], (bt.match(/Waiver Priority:?\s*\d+\w\w/) || ['Waiver Priority not shown'])[0], (bt.match(/You have used \d of \d IR positions[^.]*/) || [''])[0], (bt.match(new RegExp('Week ' + W + ' vs [^\\d]{1,60}\\d+\\w\\w')) || [''])[0]].join(' / '));
          out.push('PENDING: ' + ((bt.match(/Pending Transactions.{0,900}/) || ['none shown'])[0]));
          out.push('TRADELINKS: ' + [...g.d.querySelectorAll('a')].filter(a => /viewtrade/i.test(a.getAttribute('href') || '')).map(a => clean(a.textContent).slice(0, 50) + ' -> ' + (a.getAttribute('href') || '').replace(/^.*viewtrade/, 'viewtrade')).join(' || ')); }
        out.push('## ' + label); out.push(...rows);
        COV('own ' + label, '>=12 players', named(rows), g.ok && named(rows) >= 12, g.note);
      }
      // 3. every rival from the team list: ROS + next 4
      for (const [rid, rname] of teams) {
        if (String(rid) === String(tid)) continue;
        for (const [label, q] of [['ROS', 'stat1=P&stat2=PSR_2026'], ['NEXT4', 'stat1=P&stat2=PN4W']]) {
          g = await get(`/f1/${lid}/${rid}?${q}`, d => statTables(d).length > 0);
          const rows = g.ok ? statTables(g.d).flatMap(t => tableRows(t, ['Fan Pts', 'Pos Rank', 'Bye'])) : [];
          out.push(`## RIVAL ${rid} :: ${rname} :: ${label}`); out.push(...rows);
          COV(`rival ${rid} ${rname} ${label}`, '>=12 players', named(rows), g.ok && named(rows) >= 12, g.note);
        }
      }
      // 4. pools
      const PW = `S_PW_${W}`;
      for (const [label, q, pages] of [['POOL O wkproj', `status=A&pos=O&stat1=${PW}`, 4], ['POOL O ROSproj', 'status=A&pos=O&stat1=S_PSR', 3], ['POOL O season2026', 'status=A&pos=O&stat1=S_S_2026', 3], ['POOL O last4wk', 'status=A&pos=O&stat1=S_L4W', 3],
        // games played for rostered players comes from gate-gp-collect.js (once per pass, same in every league)
        ['POOL TE wkproj', `status=A&pos=TE&stat1=${PW}`, 1], ['POOL QB wkproj', `status=A&pos=QB&stat1=${PW}`, 1], ['POOL QB ROSproj', 'status=A&pos=QB&stat1=S_PSR', 1], ['POOL K wkproj', `status=A&pos=K&stat1=${PW}`, 1], ['POOL DEF wkproj', `status=A&pos=DEF&stat1=${PW}`, 1], ['POOL DEF ROSproj', 'status=A&pos=DEF&stat1=S_PSR', 1]]) {
        out.push(`## ${label} (Fan Pts = the stat named; Roster Status FA = free add now, W (date) = on waivers)`);
        let got = 0, okAll = true, notes = [];
        for (let p = 0; p < pages; p++) {
          g = await get(`/f1/${lid}/players?${q}&cut_type=9&myteam=0&sort=PTS&sdir=1&count=${p * 25}`, d => !!poolTable(d));
          if (!g.ok) { okAll = false; notes.push('page ' + p + ': ' + g.note); break; }
          const rows = tableRows(poolTable(g.d), ['Roster Status', 'Owner', 'GP*', 'GP', 'Bye', 'Fan Pts', 'Pos Rank', '% Ros', '% Start']);
          out.push(...rows); got += named(rows);
          if (p < pages - 1 && named(rows) < 25) { okAll = false; notes.push('page ' + p + ' short: ' + named(rows)); }
          if (p === pages - 1 && named(rows) < 10) { okAll = false; notes.push('last page only ' + named(rows) + ' rows'); }
        }
        COV(label, (pages * 25) + ' rows', got, okAll, notes.join('; '));
      }
      // 5. transactions
      g = await get(`/f1/${lid}/transactions`, d => d.querySelectorAll('table tr').length > 3);
      out.push('## TRANSACTIONS (newest first)');
      const tx = g.ok ? [...g.d.querySelectorAll('table tr')].map(tr => clean(tr.textContent)).filter(x => x && /(Added|Dropped|Traded|Waiver|Free Agent|Nov|Oct|Dec)/.test(x) && x.length < 400).slice(0, 60) : [];
      out.push(...tx); COV('transactions', '>=1', tx.length, g.ok && tx.length > 0, g.note);
    } catch (e) { COV('collector', 'no exception', String(e), false, 'exception'); }
    out.push('## COVERAGE'); out.push(...cov);
    const fails = cov.filter(x => x.includes('|FAIL|')).length;
    try { localStorage.setItem(C.prefix + k, out.join('\n')); GLOG.push(`${k} saved ${out.length} lines, ${cov.length} checks, ${fails} FAIL`); }
    catch (e) { GLOG.push(`${k} SAVE FAIL ${e.name}`); }
  }
  GDONE = true;
})();
'gate collector started';
