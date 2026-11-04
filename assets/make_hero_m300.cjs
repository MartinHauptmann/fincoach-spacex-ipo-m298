#!/usr/bin/env node
// FinCoach AI · Hero-/LinkedIn-Grafik M300 (1080 × 1350) im Stil der Grafiken zu M298/M299.
// Zahlen kommen aus der M-DBOM und der Seite (L07: nie von Hand), das GEX-Profil ist illustrativ (wie Diagramm S05).
// Aufruf im Repo-Wurzelverzeichnis: node assets/make_hero_m300.cjs  →  assets/hero-m300.png
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const dbom = JSON.parse(fs.readFileSync(path.join(root, 'provenance/m300.dbom.json'), 'utf8'));
const page = fs.readFileSync(path.join(root, 'm300.html'), 'utf8');
const fact = id => dbom.facts.find(f => f.id === id);
for (const id of ['FACT_XRAY_1MIN_SPX', 'FACT_XRAY_10_IND', 'FACT_SPX_0DTE_59', 'FACT_DEALER_CONVENTION']) {
  if (!fact(id)) throw new Error(`Fakt ${id} fehlt in der M-DBOM`);
}
if (!/nur SPX/.test(fact('FACT_XRAY_1MIN_SPX').claim)) throw new Error('FACT_XRAY_1MIN_SPX trägt „nur SPX“ nicht mehr');
if (!/zehn Indikatoren/.test(fact('FACT_XRAY_10_IND').claim)) throw new Error('FACT_XRAY_10_IND trägt „zehn Indikatoren“ nicht mehr');
const m0dte = fact('FACT_SPX_0DTE_59').claim.match(/rund (\d+) %/);
if (!m0dte) throw new Error('FACT_SPX_0DTE_59 ohne Prozentwert');
const ks = (page.match(/const KS=\[(.*?)\n\];/s) || [, ''])[1].match(/^\s*\["K\d+"/gm) || [];
const nK = ks.length;
if (!nK) throw new Error('K-Zeilen nicht gefunden');
const nFacts = dbom.facts.length;
const st = dbom.module.stichtag;
const stDE = st.split('-').reverse().join('.');

// Illustratives Profil wie Diagramm „Gamma-Regime im Profil“ (S05): Flip 7.675, Call Wall 7.800, Put Wall 7.600
const bars = [];
for (let p = 7500; p <= 7900; p += 25) {
  const v = Math.tanh((p - 7675) / 90) * 1.6 + (p === 7800 ? 0.9 : 0) + (p === 7600 ? -0.7 : 0);
  bars.push({ p, v });
}
const cw = 760, ch = 205, x0 = 60, mid = 108, scale = 42, bw = cw / bars.length;
const svgBars = bars.map((b, i) => {
  const h = Math.abs(b.v) * scale, x = x0 + i * bw + 4, y = b.v >= 0 ? mid - h : mid;
  const wall = b.p === 7800 || b.p === 7600;
  return `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${(bw - 8).toFixed(1)}" height="${Math.max(h, 1).toFixed(1)}" rx="3" fill="${b.v >= 0 ? '#00CC7A' : '#E6399A'}" ${wall ? 'stroke="#DFAF0F" stroke-width="3"' : ''}/>`;
}).join('');
const xAt = p => x0 + ((p - 7500) / 25) * bw + bw / 2;
const svg = `<svg viewBox="0 0 ${cw + 2 * x0} ${ch + 40}" width="100%">
  <line x1="${x0}" x2="${x0 + cw}" y1="${mid}" y2="${mid}" stroke="#334155" stroke-width="1.5"/>
  ${svgBars}
  <line x1="${xAt(7675)}" x2="${xAt(7675)}" y1="8" y2="${ch - 4}" stroke="#00CFFF" stroke-width="2.5" stroke-dasharray="7 5"/>
  <text x="${xAt(7675) - 10}" y="26" text-anchor="end" fill="#00CFFF" font-family="JetBrains Mono" font-size="20" font-weight="700">GEX-Flip</text>
  <text x="${xAt(7800)}" y="${ch + 6}" text-anchor="middle" fill="#DFAF0F" font-family="JetBrains Mono" font-size="19" font-weight="700">Call Wall</text>
  <text x="${xAt(7600)}" y="${ch + 6}" text-anchor="middle" fill="#DFAF0F" font-family="JetBrains Mono" font-size="19" font-weight="700">Put Wall</text>
</svg>`;

const html = `<!doctype html><html lang="de"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://${path.join(root, 'fonts.css')}">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;font-family:Inter,sans-serif;color:#E8F0F8;
 background:radial-gradient(circle at 105% -5%,rgba(0,207,255,.10) 0,rgba(0,207,255,.04) 30%,transparent 46%),linear-gradient(180deg,#0A0F1A 0%,#0D1426 100%);padding:60px 72px;position:relative;overflow:hidden}
.hdr{display:flex;justify-content:space-between;align-items:center}
.logo{display:flex;align-items:center;gap:22px}
.brand{font-family:'Space Grotesk';font-weight:700;font-size:32px}
.by{color:#64748B;font-size:18px;margin-top:2px}
.pill{font-family:'JetBrains Mono';font-weight:700;font-size:17px;color:#00CFFF;border:1.5px solid #1E293B;background:#121A2E;border-radius:999px;padding:10px 20px;letter-spacing:.04em}
.kick{font-family:'JetBrains Mono';font-weight:700;font-size:20px;letter-spacing:.16em;color:#00CFFF;margin-top:38px}
h1{font-family:'Space Grotesk';font-weight:700;font-size:62px;line-height:1.05;margin-top:14px;letter-spacing:-.01em}
h1 span{background:linear-gradient(135deg,#DFAF0F 0%,#FF6B00 60%,#E6399A 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:25px;color:#CBD5E1;margin-top:16px;line-height:1.35}
.chart{margin-top:22px;background:#121A2E;border:1.5px solid #1E293B;border-radius:18px;padding:18px 10px 6px}
.leg{display:flex;justify-content:center;gap:34px;font-size:18px;font-weight:600;color:#CBD5E1;margin:4px 0 8px}.leg i{display:inline-block;width:16px;height:16px;border-radius:4px;margin-right:8px;vertical-align:-2px}
.cap{font-family:'JetBrains Mono';font-size:15px;color:#94A3B8;text-align:center;margin:2px 0 6px;letter-spacing:.02em}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px}
.kpi{background:#121A2E;border:1.5px solid #1E293B;border-left:6px solid var(--c);border-radius:16px;padding:20px 22px}
.kpi b{display:block;font-family:'Space Grotesk';font-weight:700;font-size:42px;color:var(--c);line-height:1}
.kpi .t{font-weight:600;font-size:18px;margin-top:10px;line-height:1.25}
.kpi .s{font-size:14.5px;color:#94A3B8;margin-top:6px;font-family:'JetBrains Mono'}
.band{margin-top:18px;font-family:'JetBrains Mono';font-weight:700;font-size:18px;color:#DFAF0F;letter-spacing:.02em;text-align:center}
.warn{margin-top:18px;background:rgba(230,57,154,.08);border:1.5px solid rgba(230,57,154,.35);border-left:6px solid #E6399A;border-radius:16px;padding:18px 24px}
.warn .k{font-family:'JetBrains Mono';font-weight:700;font-size:16px;color:#E6399A;letter-spacing:.06em}
.warn .v{font-family:'Space Grotesk';font-weight:700;font-size:23px;margin-top:6px;line-height:1.3}
.foot{position:absolute;left:72px;right:72px;bottom:52px;border-top:1.5px solid #1E293B;padding-top:20px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.foot .l{font-size:16.5px;color:#64748B;line-height:1.5}
.foot .r{font-family:'JetBrains Mono';font-weight:700;font-size:18px;color:#00CFFF;white-space:nowrap}
</style></head><body>
<div class="hdr"><div class="logo">
 <svg width="64" height="74" viewBox="0 0 64 74"><rect x="0" y="40" width="13" height="32" rx="6.5" fill="#E6399A"/><rect x="17" y="27" width="13" height="45" rx="6.5" fill="#00CFFF"/><rect x="34" y="14" width="13" height="58" rx="6.5" fill="#00CC7A"/><rect x="51" y="0" width="13" height="72" rx="6.5" fill="#FF6B00"/></svg>
 <div><div class="brand">FinCoach AI</div><div class="by">by TheNextGenerationBanking.com</div></div></div>
 <div class="pill">OPTIONS ANALYTICS · MODUL M300</div></div>
<div class="kick">DEEP-DIVE · FAKTENCHECK · STICHTAG ${stDE}</div>
<h1>Was zeigt ATAS<br><span>Options X-Ray</span> wirklich?</h1>
<div class="sub">Dealer-Greeks, GEX-Flip, Call &amp; Put Walls – erklärt in drei Wissensniveaus, und wo das Modell endet.</div>
<div class="chart">${svg}<div class="leg"><span><i style="background:#E6399A"></i>Short Gamma · verstärkend</span><span><i style="background:#00CC7A"></i>Long Gamma · dämpfend</span><span><i style="background:transparent;border:3px solid #DFAF0F"></i>Walls</span></div><div class="cap">Illustratives Netto-GEX-Profil · Modellannahme · keine Marktdaten</div></div>
<div class="kpis">
 <div class="kpi" style="--c:#00CFFF"><b>nur SPX</b><div class="t">Optionsdaten von Options X-Ray im Minutentakt</div><div class="s">Herstellerangabe</div></div>
 <div class="kpi" style="--c:#9933FF"><b>10</b><div class="t">Indikatoren in der Options X-Ray Suite</div><div class="s">Herstellerangabe</div></div>
 <div class="kpi" style="--c:#00CC7A"><b>~${m0dte[1]} %</b><div class="t">0DTE-Anteil am SPX-Optionsvolumen 2025</div><div class="s">Marktdaten · Cboe</div></div>
</div>
<div class="band">${nK} Kernaussagen im Faktencheck · ${nFacts} Fakten mit Herkunftsnachweis (M-DBOM)</div>
<div class="warn"><div class="k">MODELL, KEINE PROGNOSE</div><div class="v">GEX beruht auf einer Annahme über die Position der Dealer. Flip und Walls sind Rechenergebnisse, keine Preisgarantien.</div></div>
<div class="foot"><div class="l">Stichtag ${st} · Herstellerangaben am Original geprüft · keine Verbindung zu den genannten Anbietern.<br>Keine Anlage-, Steuer- oder Rechtsberatung.</div><div class="r">fincoach-spacex-ipo-m298</div></div>
</body></html>`;

(async () => {
  const tmp = path.join(require('os').tmpdir(), `hero-m300-${process.pid}.html`);
  fs.writeFileSync(tmp, html);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + tmp);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const out = path.join(root, 'assets/hero-m300.png');
  await p.screenshot({ path: out });
  await b.close();
  fs.unlinkSync(tmp);
  console.log(`geschrieben: ${out} (Stichtag ${st}, ${nK} K, ${nFacts} Fakten, 0DTE ${m0dte[1]} %)`);
})();
