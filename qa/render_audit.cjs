#!/usr/bin/env node
/* FinCoach-AI · Render- und Kontrast-Audit (Gate vor jeder Veröffentlichung)
 *
 * Prüft eine Modulseite im echten Browser in ZWEI Zielumgebungen:
 *   plain  – Seite allein (Netlify)
 *   viewer – Seite eingebettet in das Grundgerüst des Artifact-Viewers
 *            (fremde body-Farbe/-Schrift, color-scheme light) → Lehre L01
 * Für jedes sichtbare Textelement wird der WCAG-Kontrast gegen den tatsächlichen
 * (überlagerten) Hintergrund gemessen.
 *
 * Aufruf:  node qa/render_audit.cjs m300.html [--vendor DIR] [--port 8799]
 *   --vendor DIR  lokale Kopien von chart.umd.js, katex.min.js, auto-render.min.js,
 *                 katex.min.css und tw.css (für Umgebungen ohne CDN-Zugriff)
 * Exit 0 = keine BLOCKER; BLOCKER sind: JS-Fehler, Kontrast < 3:1 bei Nicht-Token-Farben,
 * Abweichung viewer ≠ plain, horizontales Scrollen auf 390 px.
 * Kontrastwerte zwischen 3:1 und 4,5:1 aus bekannten Styleguide-Tokens werden als
 * STYLEGUIDE-DEBT gemeldet (L09), blockieren aber nicht.
 */
const path = require('path'); const fs = require('fs'); const http = require('http');
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/node22/lib/node_modules/playwright'); }
const args = process.argv.slice(2); const page = args[0];
const opt = k => { const i = args.indexOf(k); return i > -1 ? args[i + 1] : null; };
const vendor = opt('--vendor'); const port = +(opt('--port') || 8799);
const root = path.resolve(path.dirname(page)); const file = path.basename(page);
const SKELETON = '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>:root{color-scheme:light}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style></head><body>\n';
const TOKENS = ['#64748B', '#E6399A', '#9933FF', '#FF6B00', '#DFAF0F', '#00CFFF', '#00CC7A', '#4472C4'];
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.md': 'text/markdown' };

const srv = http.createServer((q, s) => {
  let u = decodeURIComponent(q.url.split('?')[0]);
  if (u === '/__viewer') { s.writeHead(200, { 'content-type': 'text/html' }); return s.end(SKELETON + fs.readFileSync(path.join(root, file), 'utf8')); }
  const f = path.join(root, u); if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s);
}).listen(port);

async function route(ctx) {
  if (!vendor) return;
  const V = n => path.join(vendor, n);
  await ctx.route(/cdn\.(jsdelivr\.net|tailwindcss\.com)/, async r => {
    const u = r.request().url();
    if (u.includes('tailwindcss.com')) { const tw = fs.readFileSync(V('tw.css'), 'utf8'); return r.fulfill({ contentType: 'application/javascript', body: `window.tailwind={};document.head.insertAdjacentHTML('beforeend',${JSON.stringify('<style>' + tw + '</style>')});` }); }
    for (const [k, n, t] of [['chart.umd.min.js', 'chart.umd.js', 'application/javascript'], ['katex.min.js', 'katex.min.js', 'application/javascript'], ['auto-render.min.js', 'auto-render.min.js', 'application/javascript'], ['katex.min.css', 'katex.min.css', 'text/css']])
      if (u.endsWith(k) && fs.existsSync(V(n))) return r.fulfill({ contentType: t, body: fs.readFileSync(V(n)) });
    return r.fulfill({ status: 204, body: '' });
  });
}

async function audit(browser, url, vp) {
  const ctx = await browser.newContext({ viewport: vp }); await route(ctx);
  const p = await ctx.newPage(); const errs = [], ext = [], failed = []; p.on('pageerror', e => errs.push(e.message));
  p.on('request', q => { const u = q.url(); if (/^https?:/.test(u) && !u.startsWith(`http://localhost:${port}`)) ext.push(u); });
  p.on('requestfailed', q => { if (q.url().startsWith(`http://localhost:${port}`)) failed.push(q.url()); });
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelectorAll('.scroll-fade').forEach(e => e.classList.add('visible')));
  await p.waitForTimeout(600);
  const r = await p.evaluate(() => {
    const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const a = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: a[0], g: a[1], b: a[2], a: a.length > 3 ? a[3] : 1 }; };
    const over = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
    const L = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
    const hex = c => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
    const bgOf = el => { const ch = []; for (let e = el; e; e = e.parentElement) ch.unshift(e); let b = { r: 255, g: 255, b: 255, a: 1 }; for (const e of ch) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0) b = over(c, b); } return b; };
    const out = [];
    document.querySelectorAll('body *').forEach(el => {
      if (/^(SCRIPT|STYLE|CANVAS)$/.test(el.tagName) || el.closest('svg,.katex-mathml,.lvl-content:not(.active),.k-detail:not(.open),.modal-overlay:not(.open)')) return;
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
      const cs = getComputedStyle(el); const bb = el.getBoundingClientRect();
      if (!own || !bb.width || !bb.height || cs.visibility === 'hidden' || cs.color === 'rgba(0, 0, 0, 0)') return;
      const bg = bgOf(el), fg = over(parse(cs.color), bg); const x = L(fg), y = L(bg);
      const size = parseFloat(cs.fontSize), large = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700);
      out.push({ sec: (el.closest('section') || {}).id || 'top', text: own.slice(0, 40), fgRaw: hex(parse(cs.color)), fg: hex(fg), bg: hex(bg), ratio: +((Math.max(x, y) + .05) / (Math.min(x, y) + .05)).toFixed(2), need: large ? 3 : 4.5, font: cs.fontFamily.split(',')[0] });
    });
    const svgOverlap = [];
    document.querySelectorAll('svg').forEach(sv => { const ts = [...sv.querySelectorAll('text')].map(t => ({ t: t.textContent.trim(), r: t.getBoundingClientRect() })).filter(x => x.r.width && x.r.height);
      for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) { const A = ts[i].r, B = ts[j].r;
        const ox = Math.min(A.right, B.right) - Math.max(A.left, B.left), oy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
        if (ox > 1 && oy > 1) svgOverlap.push(`„${ts[i].t}“ × „${ts[j].t}“`); } });
    const svgSmall = [];
    document.querySelectorAll('svg text').forEach(t => { const m = t.getScreenCTM(); if (!m) return; const px = parseFloat(getComputedStyle(t).fontSize) * Math.hypot(m.a, m.b);
      if (px && px < 11) svgSmall.push(`„${t.textContent.trim().slice(0, 20)}“ ${px.toFixed(1)}px`); });
    return { svgSmall, svgOverlap, katex: document.querySelectorAll('.katex').length, katexErr: document.querySelectorAll('.katex-error').length, charts: window.Chart ? Object.keys(Chart.instances || {}).length : 0, out, bodyFont: getComputedStyle(document.body).fontFamily, bodyColor: getComputedStyle(document.body).color, chartColor: window.Chart ? Chart.defaults.color : null, overflow: document.documentElement.scrollWidth - innerWidth };
  });
  let modalOk = null;
  if (await p.$('.reg-tag')) {
    const vis = p.locator('.reg-tag').first();
    await vis.scrollIntoViewIfNeeded(); await vis.click();
    const inside = () => p.evaluate(() => !!document.activeElement && !!document.activeElement.closest('.modal-overlay.open'));
    let ok = await inside();
    for (let i = 0; i < 4; i++) { await p.keyboard.press('Tab'); ok = ok && await inside(); }
    await p.keyboard.press('Escape');
    const back = await p.evaluate(() => document.activeElement && document.activeElement.classList.contains('reg-tag'));
    modalOk = ok && back;
  }
  await ctx.close(); return { modalOk, ...r, errs, ext: vendor ? ext.filter(u => !/cdn\.(jsdelivr\.net|tailwindcss\.com)/.test(u)) : ext, failed };
}

(async () => {
  const b = await pw.chromium.launch(); const base = `http://localhost:${port}`;
  const plain = await audit(b, `${base}/${file}`, { width: 1366, height: 900 });
  const viewer = await audit(b, `${base}/__viewer`, { width: 1366, height: 900 });
  const mobile = await audit(b, `${base}/__viewer`, { width: 390, height: 844 });
  await b.close(); srv.close();
  let blockers = 0; const line = (ok, lvl, rule, msg) => { if (!ok && lvl === 'BLOCKER') blockers++; console.log(`${ok ? '✓' : lvl === 'BLOCKER' ? '✗' : '!'} ${rule.padEnd(26)} [${lvl}] ${msg}`); };
  for (const [n, r] of [['plain', plain], ['viewer', viewer], ['viewer-390px', mobile]]) {
    line(!r.svgSmall.length, 'BLOCKER', `L31 SVG-Schrift ≥ 11 px (${n})`, r.svgSmall.length ? r.svgSmall.slice(0, 3).join('; ') + (r.svgSmall.length > 3 ? ` (+${r.svgSmall.length - 3})` : '') : 'alle Beschriftungen ≥ 11 px');
    if (r.modalOk !== null) line(r.modalOk, 'BLOCKER', `L31 Dialog-Fokus (${n})`, r.modalOk ? 'Fokus im Dialog, Tab bleibt innen, Escape kehrt zurück' : 'Fokusführung des Dialogs fehlerhaft');
    line(!r.svgOverlap.length, 'BLOCKER', `L24 SVG-Texte (${n})`, r.svgOverlap.length ? 'Überlappung: ' + r.svgOverlap.slice(0, 3).join('; ') : 'keine Überlappung');
    line(!r.errs.length, 'BLOCKER', `JS-Fehler (${n})`, r.errs.length ? r.errs.join(' | ') : 'keine');
    line(!r.ext.length, 'BLOCKER', `L20 Drittanbieter-Abrufe (${n})`, r.ext.length ? [...new Set(r.ext.map(u => new URL(u).host))].join(', ') : 'keine');
    line(!r.failed.length, 'BLOCKER', `Lokale Dateien (${n})`, r.failed.length ? r.failed.slice(0, 3).join(', ') : 'alle geladen');
    line(r.katexErr === 0 && (r.katex > 0 || !/\\\(|\\\[/.test(fs.readFileSync(path.join(root, file), 'utf8'))), 'BLOCKER', `Formeln (${n})`, `${r.katex} gesetzt, ${r.katexErr} Fehler`);
    line(r.charts > 0 || !/new Chart\(/.test(fs.readFileSync(path.join(root, file), 'utf8')), 'BLOCKER', `Diagramme (${n})`, `${r.charts} Instanzen`);
    const hard = r.out.filter(o => o.ratio < o.need && !TOKENS.includes(o.fgRaw));
    line(!hard.length, 'BLOCKER', `L01 Fremdfarben (${n})`, hard.length ? `${hard.length} Elemente, z. B. ${hard.slice(0, 3).map(h => `${h.fg} auf ${h.bg} (${h.ratio}) „${h.text}“`).join('; ')}` : '0 Elemente unter AA außerhalb der Styleguide-Tokens');
    const debt = r.out.filter(o => o.ratio < o.need && TOKENS.includes(o.fgRaw));
    line(!debt.length, 'WARN', `L09 Styleguide-Debt (${n})`, `${debt.length} Token-Elemente unter AA (${[...new Set(debt.map(d => d.fgRaw))].join(', ')})`);
    line(/Inter/.test(r.bodyFont) && r.bodyColor === 'rgb(226, 232, 240)', 'BLOCKER', `L01 body-Basis (${n})`, `${r.bodyFont.split(',')[0]} · ${r.bodyColor}`);
    if (r.chartColor !== null) line(r.chartColor === '#94A3B8', 'BLOCKER', `L02 Chart-Farbe (${n})`, r.chartColor);
  }
  const fails = o => o.out.filter(x => x.ratio < x.need).length;
  line(fails(plain) === fails(viewer), 'BLOCKER', 'L01 viewer = plain', `plain ${fails(plain)} · viewer ${fails(viewer)} Elemente unter AA`);
  line(mobile.overflow <= 0, 'BLOCKER', 'Layout 390 px', mobile.overflow > 0 ? `${mobile.overflow}px horizontaler Überlauf` : 'kein horizontales Scrollen');
  console.log(`\n${file}: ${blockers ? blockers + ' BLOCKER verletzt' : 'alle BLOCKER bestanden'}`);
  process.exit(blockers ? 1 : 0);
})();
