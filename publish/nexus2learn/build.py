#!/usr/bin/env python3
"""Baut das Nexus2Learn-Publikationspaket des PISA-2025-Deep-Dive (Quelle: m302.html).

Aufruf:  python3 publish/nexus2learn/build.py --number 479
Ergebnis (publish/nexus2learn/out/):
  modul-m<NNN>-pisa-2025-deep-dive.html   Root-Fassung fuer den FinCoach-Root (release-modules.ps1 kopiert sie nach module/)
  provenance/m<NNN>.dbom.json             M-DBOM (Companion, wird vom Release-Skript mitkopiert)
  assets/m<NNN>/*                          Datenpakete (Companion, per href referenziert -> wird mitkopiert)
  snippets/*                               index.json-Eintrag, Allowlist, Sitemap-Zeile, Startseiten-Karte
Die Modulnummer ist PROVISORISCH, bis sie mit scripts/compliance/reserve-number.ps1 reserviert wurde;
danach den Build mit der reservierten Nummer erneut ausfuehren.
"""
import argparse, json, os, re, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap=argparse.ArgumentParser();ap.add_argument('--number',type=int,required=True);ap.add_argument('--date',default='2026-09-24');a=ap.parse_args()
N=a.number;MID=f'M{N}';mid=f'm{N}';SLUG='pisa-2025-deep-dive';FILE=f'modul-{mid}-{SLUG}.html'
OUT=os.path.join(ROOT,'publish','nexus2learn','out');shutil.rmtree(OUT,ignore_errors=True)
for d in ('provenance',f'assets/{mid}','snippets'): os.makedirs(os.path.join(OUT,d),exist_ok=True)
SITE='https://www.nexus2learn.com';NETLIFY='https://fincoach-spacex-ipo-m298.netlify.app';REPO='https://github.com/MartinHauptmann/fincoach-spacex-ipo-m298'
h=open(os.path.join(ROOT,'m302.html'),encoding='utf-8').read();log=[]
def rep(o,n,cnt=None):
    global h
    c=h.count(o)
    if cnt is not None: assert c==cnt,(o[:60],c)
    h=h.replace(o,n);log.append((o[:40],c))
# --- 1) Exakte Ersetzungen (keine der Zeichenketten kommt in den Inline-Datenbloecken vor)
rep('<link rel="stylesheet" href="fonts.css"/>','<link rel="stylesheet" href="../assets/fonts/fonts.css"/>',1)
rep('<script src="https://cdn.tailwindcss.com"></script>','<script src="../vendor/tailwind.js"></script>',1)
rep('<meta property="og:site_name" content="FinCoach AI · TheNextGenerationBanking"/>',
    f'<meta property="og:site_name" content="FinCoach AI · Nexus2Learn"/>\n<meta property="og:url" content="{SITE}/module/{FILE}"/>\n<meta property="og:image" content="{SITE}/assets/og/{mid}-pisa-2025-1200x627.png"/>\n<meta property="og:image:width" content="1200"/>\n<meta property="og:image:height" content="627"/>\n<meta name="twitter:card" content="summary_large_image"/>\n<meta name="twitter:image" content="{SITE}/assets/og/{mid}-pisa-2025-1200x627.png"/>\n<link rel="canonical" href="{SITE}/module/{FILE}"/>',1)
rep('<a href="m300.html" class="text-xs text-tngb-muted">M300</a><a href="m301.html" class="text-xs text-tngb-muted">M301</a><a href="pisa-hub.html" class="text-xs text-tngb-muted">Hub</a><a href="index.html" class="text-xs text-tngb-muted">← Hauptseite</a>',
    f'<a href="{NETLIFY}/m301" target="_blank" rel="noopener" class="text-xs text-tngb-muted">PISA Explorer ↗</a><a href="{NETLIFY}/hub" target="_blank" rel="noopener" class="text-xs text-tngb-muted">PISA-Hub ↗</a><a href="modul-matrix.html" class="text-xs text-tngb-muted">FinCoach AI Module</a><a href="index.html" class="text-xs text-tngb-muted">← Nexus2Learn</a>',1)
rep('<a href="index.html" class="block mb-1">← Hauptseite</a><a href="m300.html" class="block mb-1">M300</a><a href="m301.html" class="block mb-1">M301</a><a href="impressum.html" class="block mb-1">Impressum</a><a href="datenschutz.html" class="block">Datenschutz</a>',
    f'<a href="index.html" class="block mb-1">← Zurück zur Hauptseite</a><a href="modul-matrix.html" class="block mb-1">Alle FinCoach AI Module</a><a href="{NETLIFY}/m301" target="_blank" rel="noopener" class="block mb-1">PISA Explorer (3D) ↗</a><a href="{NETLIFY}/m300" target="_blank" rel="noopener" class="block mb-1">PISA 2025 &amp; Finanzbildung ↗</a><a href="{NETLIFY}/hub" target="_blank" rel="noopener" class="block mb-1">PISA-Hub ↗</a><a href="impressum.html" class="block mb-1">Impressum</a><a href="datenschutz.html" class="block">Datenschutz</a>',1)
rep('<a href="https://www.TheNextGenerationBanking.com" target="_blank" rel="noopener" class="text-sm font-mono" style="color:#00CFFF;">by TheNextGenerationBanking.com</a></div>',
    f'<a href="{SITE}" target="_blank" rel="noopener" class="text-sm font-mono" style="color:#00CFFF;">powered by Nexus2Learn.com</a><div class="text-xs text-tngb-muted mt-1">by TheNextGenerationBanking.com</div></div>',1)
rep('<p class="text-xs text-tngb-muted mt-6 text-center">© 2026 TheNextGenerationBanking — FinCoach AI. Die nächste Generation Banking.</p>',
    f'<p class="text-xs text-tngb-muted mt-6 text-center">© 2026 TheNextGenerationBanking — FinCoach AI · Nexus2Learn. 🤖 Mit KI-Unterstützung erstellt (Art. 50 EU-KI-VO) · keine Anlageberatung · Quellcode und Datenpakete: <a href="{REPO}" target="_blank" rel="noopener" class="text-tngb-cyan">GitHub (Repository-Kennung M302)</a></p>',1)
rep('<td class="mono text-tngb-emerald">M300</td><td>PISA 2025 &amp; Finanzbildung</td><td>T3 · 46</td><td>Diagnostik, OECD/INFE, KI-Anforderungen, Compliance</td><td><a class="text-tngb-cyan" href="m300.html">öffnen →</a></td>',
    f'<td class="mono text-tngb-emerald">PISA·FB</td><td>PISA 2025 &amp; Finanzbildung (extern)</td><td>T3 · 46</td><td>Diagnostik, OECD/INFE, KI-Anforderungen, Compliance</td><td><a class="text-tngb-cyan" href="{NETLIFY}/m300" target="_blank" rel="noopener">öffnen ↗</a></td>',1)
rep('<td class="mono text-tngb-cyan">M301</td><td>PISA Explorer</td><td>T3 · 46</td><td>3D-Vergleich, Statistik-Engine</td><td><a class="text-tngb-cyan" href="m301.html">öffnen →</a></td>',
    f'<td class="mono text-tngb-cyan">PISA·X</td><td>PISA Explorer (extern)</td><td>T3 · 46</td><td>3D-Vergleich, Statistik-Engine</td><td><a class="text-tngb-cyan" href="{NETLIFY}/m301" target="_blank" rel="noopener">öffnen ↗</a></td>',1)
rep('<td class="mono text-tngb-gold">HUB</td><td>PISA-Hub · Verknüpfungs-App</td><td>T3 · 46</td><td>Argumentationskette aller PISA-Module</td><td><a class="text-tngb-cyan" href="pisa-hub.html">öffnen →</a></td>',
    f'<td class="mono text-tngb-gold">HUB</td><td>PISA-Hub · Verknüpfungs-App (extern)</td><td>T3 · 46</td><td>Argumentationskette aller PISA-Module</td><td><a class="text-tngb-cyan" href="{NETLIFY}/hub" target="_blank" rel="noopener">öffnen ↗</a></td>',1)
rep('Werkzeuge: M301 (Explorer), Brücke zur Finanzbildung: M300.','Werkzeuge: PISA Explorer (extern), Brücke zur Finanzbildung: Modul „PISA 2025 &amp; Finanzbildung“ (extern).',1)
rep('(verifiziert in M300)','(verifiziert im Modul „PISA 2025 &amp; Finanzbildung“)',1)
rep('Hinweis für Folge-Module (M300 REQ)','Hinweis für Folge-Module (Anforderungen im Modul „PISA 2025 &amp; Finanzbildung“)',1)
rep('"related_modules": ["M300", "M301"]','"related_modules": [], "related_external": ["'+NETLIFY+'/m300", "'+NETLIFY+'/m301", "'+NETLIFY+'/hub"], "source_module_id": "M302", "source_repo": "'+REPO+'"',1)
rep('provenance/m302.dbom.json',f'provenance/{mid}.dbom.json')
for f in ['pisa-2025-official.json','pisa-history.json','pisa-data-register.csv','pisa-percentiles.json','pisa-regions.json','flags-48.json','world-paths.json']:
    rep(f'href="data/{f}"',f'href="assets/{mid}/{f}"')
FONTS_OLD="add('style','fonts.css self-hosted',!!document.querySelector('link[href=\"fonts.css\"]'));"
FONTS_NEW="add('style','fonts.css self-hosted',!!document.querySelector('link[href$=\"fonts.css\"]'));"
rep(FONTS_OLD,FONTS_NEW,1)
# --- 1b) Kennung nur ausserhalb der Inline-Datenbloecke ersetzen (Register-Zeilen tragen die Quell-Kennung M302/M301)
parts=re.split(r'(<script type="application/json" id="(?:official|history|world|pct|register|regions|flags)-inline">.*?</script>)',h,flags=re.S)
for i in range(0,len(parts),2): parts[i]=parts[i].replace('FACT_M302_','FACT_@@_').replace('M302',MID).replace('FACT_@@_','FACT_M302_')  # Fakten-IDs bleiben (DBOM-Referenzen)
html=''.join(parts)
assert 'cdn.tailwindcss.com' not in html and 'href="data/' not in html and re.sub(r'FACT_M302_','',''.join(parts[i] for i in range(0,len(parts),2))).count('M302')==0
open(os.path.join(OUT,FILE),'w',encoding='utf-8').write(html)
# --- 2) DBOM
d=json.load(open(os.path.join(ROOT,'provenance/m302.dbom.json'),encoding='utf-8'))
d['module']['id']=MID;d['module']['external_dbom']=f'provenance/{mid}.dbom.json';d['module']['related_modules']=[]
d['module']['publication']={'site':SITE,'path':f'/module/{FILE}','module_id':MID,'source_module_id':'M302','source_repo':REPO,'source_version':d['module']['version'],'number_status':'PROVISORISCH — mit scripts/compliance/reserve-number.ps1 -Reserve -Slug pisa-2025-deep-dive bestaetigen','prepared':a.date}
d['module']['data_packages']=[f'assets/{mid}/'+os.path.basename(p) for p in d['module'].get('data_packages',[])]
d.setdefault('changelog',[]).insert(0,{'version':d['module']['version'],'date':a.date,'type':'publication','summary':f'Nexus2Learn-Fassung als {MID}: Fonts und Tailwind self-hosted (CSP der Website), Querverweise auf die PISA-Schwestermodule extern, Datenpakete unter assets/{mid}/; Inhalte, Fakten und Quellen unveraendert (Repository-Kennung M302 v'+d['module']['version']+').'})
json.dump(d,open(os.path.join(OUT,f'provenance/{mid}.dbom.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
# --- 3) Datenpakete
for f in ['pisa-2025-official.json','pisa-history.json','pisa-data-register.csv','pisa-data-register.json','pisa-percentiles.json','pisa-regions.json','flags-48.json','world-paths.json']:
    shutil.copy(os.path.join(ROOT,'data',f),os.path.join(OUT,f'assets/{mid}',f))
# --- 4) Snippets
sn=os.path.join(OUT,'snippets')
json.dump({'id':MID,'number':N,'title':'PISA 2025 Deep Dive','file':FILE,'released':True},open(os.path.join(sn,'index-json-entry.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
open(os.path.join(sn,'modules-public-add.txt'),'w').write(f'"{MID}"\n')
open(os.path.join(sn,'sitemap-line.xml'),'w').write(f'  <url><loc>{SITE}/module/{FILE}</loc><lastmod>{a.date}</lastmod><priority>0.8</priority></url>\n')
open(os.path.join(sn,'index-html-card.html'),'w',encoding='utf-8').write(f'''<!-- Startseite, Sektion "AKTUELL · FINCOACH AI ANALYSEN": als erste Karte in das Karten-Grid einfuegen -->
<a href="module/{FILE}" class="card p-6 block hover:border-cyan-400/50 transition" style="border:1px solid rgba(0,207,255,.55);border-radius:14px;background:#121A2E">
  <div class="text-xs mono mb-1" style="color:#00CFFF">NEU &middot; {a.date} &middot; BILDUNG &amp; DATENKOMPETENZ &middot; {MID}</div>
  <h3 class="font-bold text-lg mb-1">PISA 2025 Deep Dive &mdash; 91 Bildungssysteme, jede Zahl mit Herkunft</h3>
  <p class="text-sm text-slate-400">Weltkarte über fünf Erhebungen (2012–2025), vollständiger Ländervergleich aller <strong class="text-slate-200">91 Systeme mit Konfidenzintervallen und Rangspannen</strong>, Länderflaggen nach Kontinenten und Bündnissen, Deutschland im Detail und ein Register mit 7.319 Zahlen, das die Art jeder Zahl ausweist. Deutschland: 486 Punkte, statistisch auf OECD-Niveau.</p>
</a>
<!-- Optional: Hero-Pill (neben "Neues Modul") -->
<a href="module/{FILE}" class="pill" style="background:rgba(0,207,255,.14);color:#00CFFF;border:1px solid rgba(0,207,255,.5)">🆕 PISA 2025 Deep Dive: 91 Systeme, eine Skala</a>
''')
print('OK', FILE, 'HTML KB', len(html)//1024, '· Ersetzungen:', len(log), '· Nummer', MID, '(provisorisch)')
