// Draft Sharks collector with completeness checks. Paste into any draftsharks.com tab (signed in)
// AFTER setting: window.GATE_DS = {prefix: 'gate_DATE_', leagues: [["KEY", DS_LEAGUE_ID], ...]}
// FIRST sync each league in the tab (dashboard -> Update Rosters); then, per league, in a hidden same-origin iframe:
// team dashboard -> verify the "Synced" stamp is under 60 minutes old -> read the roster table; then the Free Agent Finder once per position with Load More.
// Progress: window.DLOG; done: window.DDONE === true. Coverage lines as in gate-collect.js (COV|league|item|exp|got|OK/FAIL|note).
Object.keys(localStorage).filter(x => (/^gate_/.test(x) && !x.startsWith(window.GATE_DS.prefix)) || window.GATE_DS.leagues.some(([k]) => x === window.GATE_DS.prefix + 'ds_' + k)).forEach(x => localStorage.removeItem(x));  // other passes are on disk; this pass's other leagues stay
window.DLOG = []; window.DDONE = false;
window.DP = (async () => {
  const C = window.GATE_DS;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const cl = s => (s || '').replace(/[=;]/g, ' ').replace(/[-]/g, '').replace(/\s+/g, ' ').trim();
  const frame = () => { const f = document.createElement('iframe'); f.style.cssText = 'width:1400px;height:900px;position:fixed;left:-6000px;top:0'; document.body.appendChild(f); return f; };
  const load = (f, url, ms = 30 * 1000) => new Promise(res => { let done = false; f.onload = () => { if (!done) { done = true; res(true); } }; setTimeout(() => { if (!done) { done = true; res(false); } }, ms); if (url) f.src = url; });
  const waitFor = async (fn, ms = 15 * 1000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { try { if (fn()) return true; } catch (e) {} await sleep(500); } return false; };
  const rowsOf = t => [...t.rows].map(r => [...r.cells].map(c => { let x = cl(c.innerText); if (x.length > 140) x = x.slice(0, 140) + '..'; return x; }).join(' | '));
  const FRESH = /Synced:\s*(\d+ seconds?|a minute|[1-5]?\d minutes?(?: \d+ seconds?)?) ago/;  // under 60 minutes (gate.py check also requires the DS roster to match the host roster)
  const FULL = { QB: 'Quarterback', RB: 'Running Back', WR: 'Wide Receiver', TE: 'Tight End', K: 'Kicker', DEF: 'Defense' };
  const FLOOR = { QB: 10, RB: 40, WR: 60, TE: 25, K: 10, DEF: 10 }, MORE = { QB: 1, RB: 3, WR: 4, TE: 2, K: 0, DEF: 0 };
  for (const [k, ds] of C.leagues) {
    const out = [], cov = [];
    const COV = (item, exp, got, ok, note) => cov.push(['COV', k, item, exp, got, ok ? 'OK' : 'FAIL', note || ''].join('|'));
    const f = frame();
    try {
      out.push(`# ${k} DS ${ds} - pulled ${new Date().toLocaleString('en-US')}`);
      // dashboard + sync
      let ok = await load(f, `/league/team-dashboard/${ds}`);
      await waitFor(() => /Synced:/.test(f.contentDocument.body.innerText) && f.contentDocument.querySelectorAll('table').length > 1);
      // DS syncs rosters through the top-level page (the button posts the Yahoo rosters the page reads),
      // so the sync is done per league in the tab BEFORE this collector; here it is only verified.
      const synced = ((f.contentDocument.body.innerText.match(/Synced:[\s\S]{0,30}/) || [''])[0]).replace(/\s+/g, ' ');
      COV('ds sync', 'synced under 60 minutes ago', synced.slice(0, 40), FRESH.test(synced), FRESH.test(synced) ? '' : 'run Update Rosters on this dashboard in the tab, then re-run');
      const bt = f.contentDocument.body.innerText;
      out.push('SYNC: ' + synced);
      out.push('SUGGESTED: ' + (bt.match(/SUGGESTED MOVES[\s\S]{0,700}/) || [''])[0].replace(/\s+/g, ' '));
      out.push('## DASHBOARD');
      let roster = 0;
      [...f.contentDocument.querySelectorAll('table')].forEach((t, i) => { if (t.rows.length > 1) { out.push('## dash table ' + i); const r = rowsOf(t); out.push(...r); if (i === 1 || roster === 0) roster = Math.max(roster, r.filter(x => /^(QB|RB|WR|TE|R W T|R W T Q|Q W R T|K|DEF|BN|IR) \| [A-Z]/.test(x)).length); } });
      COV('ds dashboard roster', '>=12 players', roster, roster >= 12, '');
      // free agent finder, one position at a time
      for (let a = 1; a <= 3; a++) {  // the position buttons sometimes render late: reload up to 3 times
        ok = await load(f, `/league/free-agent/${ds}`);
        if (await waitFor(() => [...f.contentDocument.querySelectorAll('button')].some(b => ['WR', 'All Positions'].includes(b.textContent.trim()) && b.offsetParent), 20 * 1000)) break;
      }
      for (const pos of ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']) {
        let btn = [...f.contentDocument.querySelectorAll('button')].find(b => b.textContent.trim() === pos && b.offsetParent);
        if (!btn) {  // some leagues (superflex) show a position dropdown instead of buttons
          const dd = [...f.contentDocument.querySelectorAll('button')].find(b => /^(All Positions|Quarterback|Running Back|Wide Receiver|Tight End|Kicker|Defense|Q\|R\|W\|T|R\|W\|T)$/.test(b.textContent.trim()) && b.offsetParent);
          if (dd) { dd.click(); await sleep(600); }
          btn = [...f.contentDocument.querySelectorAll('[role=option]')].find(o => o.textContent.trim() === FULL[pos]);
        }
        let rows = [], note = '';
        if (!btn) note = 'no ' + pos + ' button or dropdown option';
        else {
          btn.click(); await sleep(3000);
          for (let i = 0; i < MORE[pos]; i++) { const lm = [...f.contentDocument.querySelectorAll('button')].find(x => /^\s*Load More\s*$/i.test(x.textContent) && x.offsetParent); if (!lm) break; lm.click(); await sleep(2500); }
          const t = [...f.contentDocument.querySelectorAll('table')].sort((a, b) => b.rows.length - a.rows.length)[0];
          rows = t ? rowsOf(t) : [];
        }
        const data = rows.filter(x => x.split(' | ').length === 15 && /^\S*\s*\|\s*\d+\s*\|/.test(x));
        const own = data.filter(x => new RegExp(' ' + pos + '\\d* ').test(x.split(' | ')[2] + ' '));  // rows of THIS position (the table keeps earlier ones)
        const mine = own.length;
        const odd = rows.filter(x => /\| \d+ \| /.test(x) && x.split(' | ').length !== 15).length;
        out.push('## FAF ' + pos); out.push(...own);
        COV('ds faf ' + pos, '>=' + FLOOR[pos] + ' ' + pos + ' rows, 0 unparsed', mine + ' ' + pos + ' rows, ' + odd + ' unparsed', mine >= FLOOR[pos] && odd === 0, note);
      }
    } catch (e) { COV('ds collector', 'no exception', String(e), false, 'exception'); }
    f.remove();
    out.push('## COVERAGE'); out.push(...cov);
    const fails = cov.filter(x => x.includes('|FAIL|')).length;
    try { localStorage.setItem(C.prefix + 'ds_' + k, out.join('\n')); DLOG.push(`${k} saved ${out.length} lines, ${cov.length} checks, ${fails} FAIL`); }
    catch (e) { DLOG.push(`${k} SAVE FAIL ${e.name}`); }
  }
  DDONE = true;
})();
'gate DS collector started';
