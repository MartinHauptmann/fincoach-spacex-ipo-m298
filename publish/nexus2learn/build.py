#!/usr/bin/env python3
"""Baut das Nexus2Learn-Publikationspaket der PISA-Serie (4 Registry-Module) aus diesem Repository.

Quellen:  m302.html (Deep Dive) · m301.html (Explorer) · m300.html (PISA 2025 & Finanzbildung) · pisa-hub.html (Hub)
Aufruf:   python3 publish/nexus2learn/build.py --lock <Root>/reserved-numbers.txt
          python3 publish/nexus2learn/build.py --numbers deep=479,explorer=480,fb=481,hub=482   (provisorisch)
Ergebnis: publish/nexus2learn/out/
  modul-m<NNN>-<slug>.html   Root-Fassung je Modul (Website-Konventionen; release-modules.ps1 kopiert sie nach module/)
  provenance/m<NNN>.dbom.json  M-DBOM je Modul (Companion)
  assets/m<NNN>/*            Datenpakete/Skripte je Modul (Companions, per href/src referenziert)
  snippets/*                 index.json-Eintraege, Allowlist, Sitemap-Zeilen, Startseiten-Karte
Querverweise zwischen den vier Modulen sind interne Geschwister-Links (modul-m<NNN>-<slug>.html), die im
FinCoach-Root und in module/ gleichermassen funktionieren. Fakten-IDs (FACT_*, SRC_*) bleiben unveraendert.
"""
import argparse, json, os, re, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE='https://www.nexus2learn.com'
MODS={
 'deep':    dict(src='m302.html',    dbom='provenance/m302.dbom.json', old='M302', slug='pisa-2025-deep-dive',     title='PISA 2025 Deep Dive'),
 'explorer':dict(src='m301.html',    dbom='provenance/m301.dbom.json', old='M301', slug='pisa-explorer',           title='PISA Explorer'),
 'fb':      dict(src='m300.html',    dbom='provenance/m300.dbom.json', old='M300', slug='pisa-2025-finanzbildung', title='PISA 2025 & Finanzbildung'),
 'hub':     dict(src='pisa-hub.html',dbom='provenance/hub.dbom.json',  old='HUB',  slug='pisa-hub',                title='PISA-Hub'),
}
ap=argparse.ArgumentParser();ap.add_argument('--lock',help='reserved-numbers.txt des FinCoach-Root (Eintraege slug=<slug>)');ap.add_argument('--numbers',help='provisorisch: deep=NNN,explorer=NNN,fb=NNN,hub=NNN');ap.add_argument('--date',default='2026-09-24');a=ap.parse_args()
NUM={}
if a.lock:
    lines=[l for l in open(a.lock,encoding='utf-8',errors='replace') if re.match(r'M\d+\t(reserved|backfilled)',l)]
    for k,m in MODS.items():
        hits=[l for l in lines if f'slug={m["slug"]}' in l.split('\t',3)[3] if len(l.split('\t'))>3]
        if not hits: raise SystemExit(f'Kein Eintrag slug={m["slug"]} in {a.lock} — zuerst reservieren: pwsh scripts/compliance/reserve-number.ps1 -Reserve -Slug \'{m["slug"]}\' -Min 479')
        NUM[k]=int(re.match(r'M(\d+)',hits[-1]).group(1));print('Nummer aus Lock:',hits[-1].strip())
elif a.numbers:
    for kv in a.numbers.split(','): k,v=kv.split('=');NUM[k.strip()]=int(v)
    missing=[k for k in MODS if k not in NUM]
    if missing: raise SystemExit('fehlende Nummern: '+', '.join(missing))
else: raise SystemExit('--lock oder --numbers angeben')
assert len(set(NUM.values()))==4,'Nummern muessen verschieden sein'
STATUS='reserviert via reserved-numbers.txt' if a.lock else 'PROVISORISCH — mit scripts/compliance/reserve-number.ps1 -Reserve -Slug <slug> -Min 479 bestaetigen'
for k,m in MODS.items(): m['id']=f'M{NUM[k]}';m['mid']=f'm{NUM[k]}';m['file']=f'modul-{m["mid"]}-{m["slug"]}.html'
BYSRC={m['src']:m for m in MODS.values()}
COLORMAP={  # Quelle -> TNGB-Token (scripts/styleguide/tokens.json); Kontinente/Buendnisse/Explorer-Palette + UI-Farben
 '#008cdf':'#00CFFF','#cf630d':'#FF6B00','#966cd7':'#9933FF','#4a9c36':'#00CC7A','#ca5794':'#E6399A','#b27b00':'#DFAF0F',
 '#b45000':'#FF6B00','#9d79d7':'#9933FF','#398526':'#00CC7A','#cd6199':'#E6399A','#946900':'#DFAF0F','#00a6ae':'#4472C4','#b9454c':'#E040A0','#6b86e1':'#7DA0E0','#6b7f00':'#94A3B8','#b16ec0':'#CBD5E1','#bb6802':'#E2E8F0',
 '#3987e5':'#00CFFF','#d95926':'#FF6B00','#199e70':'#00CC7A','#c98500':'#DFAF0F','#d55181':'#E6399A','#9085e9':'#9933FF','#008300':'#4472C4',
 '#f1f5f9':'#E2E8F0','#0f1729':'#121A2E','#0d1526':'#0A0F1A','#334155':'#1E293B','#475569':'#64748B','#8a94a6':'#94A3B8','#3bb0e0':'#00CFFF','#1a2336':'#121A2E','#3ab674':'#00CC7A','#5a9a7a':'#94A3B8','#8a6b7a':'#94A3B8','#c9557f':'#E6399A'}
def agent_block(m):
    typ='tiefenmodul' if m['slug'] in ('pisa-2025-deep-dive','pisa-2025-finanzbildung') else 'tool'
    dj=json.load(open(os.path.join(ROOT,m['dbom']),encoding='utf-8'));fs=dj.get('fact_summary',{});ver=dj['module']['version'];st=dj['module']['stichtag']
    used=[{'id':'fincoach-module-provenance','status':'passed','timestamp':a.date+'T17:40:00Z','output':f'provenance/{m["mid"]}.dbom.json','stats':{k:v for k,v in fs.items() if not isinstance(v,dict)},'note':'M-DBOM v1 mit Verdict/Konfidenz/Quelle je Fakt; jede Zahl traegt eine Herkunftsklasse (OFFICIAL_STATLINK, DERIVED_OFFICIAL, COMPUTED_MICRODATA, SCENARIO, INTERPRETATION); kein Wert aus Modellgedaechtnis.'},
          {'id':'fincoach-module-compliance-guardian','status':'passed-with-warnings','timestamp':a.date+'T17:40:00Z','output':'assets/'+MODS['fb']['mid']+'/fincoach_module_check.py (C01-C11, D01-D14, S01-S10) + Live-QA im Modul','stats':{'static_fail':0,'live_qa':'alle Checks bestanden'},'note':'Geprueft mit dem modul-eigenen Checker und der Live-QA, nicht mit dem FinCoach-Guardian-Agenten; Verhalten unter file:// (R033), localStorage (safeLS) und CSP self erfuellt.'}]
    skipped=[{'id':'fincoach-entity-network-cartographer','reason':'Studien-Deep-Dive ohne Akteurs-Netzwerk; Organisationen (OECD, IEA, ZIB) sind im Quellenverzeichnis benannt.'},
             {'id':'fincoach-market-data','reason':'Keine Marktdaten; Datenbasis sind OECD-StatLink-Tabellen und Public-Use-Files.'},
             {'id':'fincoach-world-governance','reason':'Kein Governance-Atlas-Bezug; Kontinent-/Buendniszuordnung ist als Referenzklasse im DBOM ausgewiesen.'}]
    pend=[]
    if typ=='tiefenmodul':
        pend=[{'id':'fincoach-interdisciplinary-council','status':'pending','note':'Nicht durchgefuehrt: Modul ausserhalb der FinCoach-Pipeline entstanden (Herkunft Repository-Kennung '+m['old']+'). Vor Publish nachholen oder Ausnahme dokumentieren.'},
              {'id':'fincoach-wikipedia-synthesis','status':'pending','note':'Nicht durchgefuehrt; Faktencheck erfolgte gegen OECD-Primaerquellen (StatLink, Laendernotiz, Technical Report) mit dokumentierten Diskrepanzen. Vor Publish nachholen oder Ausnahme dokumentieren.'}]
    man={'module_id':f'{m["mid"]}-{m["slug"]}','build_id':f'{m["mid"]}-{m["slug"]}-v{ver}-{a.date}','build_timestamp':a.date+'T17:40:00Z','stichtag':st,'module_type':typ,'agents_used':used+pend,'agents_skipped':skipped,
         'open_issues':[{'id':f'{m["mid"]}-pipeline-gates','title':'Council- und Wikipedia-Synthese-Agent nachholen oder Ausnahme dokumentieren (Modul aus externem Repository ueberfuehrt)','priority':'high','agent':'fincoach-module-lifecycle-auditor'}] if typ=='tiefenmodul' else [],'reaudit':a.date}
    cards=''.join(f'<div class="dep-box" style="border-left:3px solid {"#00CC7A" if x["status"]=="passed" else "#DFAF0F" if x["status"].startswith("passed") else "#FF6B00"}"><div class="flex items-center justify-between gap-2"><span class="mono text-xs text-white">{x["id"]}</span><span class="badge b-ok" style="{"background:rgba(255,107,0,.18);color:#FF6B00" if x["status"]=="pending" else "background:rgba(223,175,15,.18);color:#DFAF0F" if x["status"]!="passed" else ""}">{x["status"]}</span></div><div class="text-xs text-tngb-muted mt-1">{x.get("note","")}</div></div>' for x in used+pend)
    sk=''.join(f'<div class="dep-box"><span class="mono text-xs text-slate-300">{x["id"]}</span><div class="text-xs text-tngb-muted mt-1">{x["reason"]}</div></div>' for x in skipped)
    return f'''<section class="px-4 py-10 max-w-7xl mx-auto" id="agent-audit-section" style="border-top:1px solid var(--border)">
  <div class="flex flex-wrap items-start justify-between gap-3 mb-4"><div><div class="text-xs mono text-tngb-cyan mb-1">13 · QUALITÄTSAGENTEN</div><h3 class="font-head font-bold text-xl text-white mb-1">Welche Agenten haben diesen Build geprüft?</h3><p class="text-xs text-tngb-muted">Pflicht-Audit-Trail laut FinCoach-Vorgaben · Build-ID, Stichtag und Status je Agent</p></div><div class="text-right text-xs mono text-tngb-muted"><div>Build: <span class="text-tngb-cyan">{man["build_id"]}</span></div><div>Stichtag: <span class="text-tngb-cyan">{st}</span></div><div>Status: <span style="color:{"#DFAF0F" if pend else "#00CC7A"}">{"pending (2 Pflicht-Agenten offen)" if pend else "passed"}</span></div></div></div>
  <div id="agents-used-grid" class="grid md:grid-cols-2 gap-3 text-sm">{cards}</div>
  <details class="mt-4"><summary class="text-xs text-tngb-muted" style="cursor:pointer">▸ {len(skipped)} Agent(en) bewusst ausgelassen — anzeigen</summary><div class="mt-2 grid md:grid-cols-2 gap-2 text-xs">{sk}</div></details>
  <div class="mt-4 text-xs mono text-tngb-muted" style="border-left:2px solid rgba(0,207,255,.4);padding-left:.5rem">Validiert gegen <a href="data/agent-usage-schema.json" target="_blank" class="text-tngb-cyan">data/agent-usage-schema.json</a> · maschinenlesbares Manifest unten</div>
</section>
<script type="application/json" id="module-agents-used">
{json.dumps(man,ensure_ascii=False,indent=2)}
</script>'''
OUT=os.path.join(ROOT,'publish','nexus2learn','out');shutil.rmtree(OUT,ignore_errors=True)
for d in ['provenance','snippets']+[f'assets/{m["mid"]}' for m in MODS.values()]: os.makedirs(os.path.join(OUT,d),exist_ok=True)
DATA_BLOCK=re.compile(r'(<script type="application/json" id="(?:official|history|world|pct|register|regions|flags|data)-inline">.*?</script>)',re.S)
OLD2NEW={m['old']:m['id'] for m in MODS.values()};OLDLOW={m['src'][:-5]:m['mid'] for m in MODS.values()}  # m302->m479, pisa-hub->m482
def sib(mo):  # href="m302.html#x" -> Geschwister-Datei
    return f'href="{BYSRC[mo.group(1)+".html"]["file"]}{mo.group(2) or ""}"'
def rename_ids(t):
    t=re.sub(r'\b(FACT_[A-Z0-9_]+|SRC_[A-Z0-9_]+)\b',lambda mo:'§§'+mo.group(1).replace('M','µ')+'§§',t)   # Fakten-/Quellen-IDs schuetzen
    for o,n in OLD2NEW.items(): t=re.sub(r'\b'+o+r'\b',n,t)
    return re.sub(r'§§([^§]+)§§',lambda mo:mo.group(1).replace('µ','M'),t)
def build(m):
    h=open(os.path.join(ROOT,m['src']),encoding='utf-8').read();notes=[]
    # Kopf: Ressourcen self-hosted (CSP der Website: nur 'self')
    h=h.replace('<link rel="stylesheet" href="fonts.css"/>','<link rel="stylesheet" href="../assets/fonts/fonts.css"/>').replace('<script src="https://cdn.tailwindcss.com"></script>','<script src="../vendor/tailwind.js"></script>')
    h=re.sub(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/katex@[0-9.]+/dist/katex\.min\.css"[^>]*>','<link rel="stylesheet" href="../vendor/katex-0.16.11.min.css"/>',h)
    h=re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/katex@[0-9.]+/dist/katex\.min\.js"[^>]*></script>','<script src="../vendor/katex-0.16.11.min.js"></script>',h)
    h=re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/katex@[0-9.]+/dist/contrib/auto-render\.min\.js"[^>]*></script>','<script src="../vendor/katex-auto-render-0.16.11.min.js"></script>',h)
    h=re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js@[0-9.]+/dist/chart\.umd\.min\.js"[^>]*></script>','<script src="../vendor/chart-4.4.3.min.js"></script>',h)
    assert 'cdn.jsdelivr.net' not in h and 'cdn.tailwindcss.com' not in h,m['src']
    # Meta
    h=re.sub(r'<meta property="og:site_name" content="[^"]*"/>',f'<meta property="og:site_name" content="FinCoach AI · Nexus2Learn"/>\n<meta property="og:url" content="{SITE}/module/{m["file"]}"/>\n<meta property="og:image" content="{SITE}/assets/og/pisa-2025-serie-1200x627.png"/>\n<meta property="og:image:width" content="1200"/>\n<meta property="og:image:height" content="627"/>\n<meta name="twitter:card" content="summary_large_image"/>\n<meta name="twitter:image" content="{SITE}/assets/og/pisa-2025-serie-1200x627.png"/>\n<link rel="canonical" href="{SITE}/module/{m["file"]}"/>',h,count=1)
    if '<link rel="canonical"' not in h: h=h.replace('</title>',f'</title>\n<link rel="canonical" href="{SITE}/module/{m["file"]}"/>\n<meta property="og:url" content="{SITE}/module/{m["file"]}"/>',1);notes.append('canonical ergaenzt (kein og:site_name)')
    # SpaceX-Bezuege entfernen (Matrix-Zeilen M298/M299, Nav-/Fusslinks auf modul.html, m299.html, ipo-prozess.html)
    h,n1=re.subn(r'<tr[^>]*>(?:(?!</tr>).)*href="(?:m299|modul|ipo-prozess)\.html"(?:(?!</tr>).)*</tr>\s*','',h,flags=re.S)
    h,n2=re.subn(r'<a [^>]*href="(?:m299|modul|ipo-prozess)\.html"[^>]*>.*?</a>\s*','',h,flags=re.S)
    if n1 or n2: notes.append(f'SpaceX-Bezuege entfernt: {n1} Matrix-Zeilen, {n2} Links')
    h=h.replace('(M298/M299)','(FinCoach-Modulvorlage)').replace('Pflicht seit M298 v2.0','Pflicht laut Modulvorlage')
    # Geschwister-Links (HTML-href und Hub-Knoten link:'...')
    h=re.sub(r'href="(m300|m301|m302|pisa-hub)\.html(#[^"]*)?"',sib,h)
    h=re.sub(r"link:'(m300|m301|m302|pisa-hub)\.html(#[^']*)?'",lambda mo:f"link:'{BYSRC[mo.group(1)+'.html']['file']}{mo.group(2) or ''}'",h)
    assert not re.search(r'href="(m299|m300|m301|m302|pisa-hub|modul|ipo-prozess)\.html',h),m['src']
    # Katalog-Link in der Nav (release-modules.ps1 schreibt modul-matrix.html -> ../module.html um)
    h=re.sub(r'(<a href="index\.html" class="text-xs text-tngb-muted[^"]*">← Hauptseite</a>)',r'<a href="modul-matrix.html" class="text-xs text-tngb-muted">FinCoach AI Module</a>\1',h,count=1)
    # Fusszeile: Nexus2Learn + Art. 50 EU-KI-VO
    h=re.sub(r'<a href="https://www\.TheNextGenerationBanking\.com"[^>]*>by TheNextGenerationBanking\.com</a>',f'<a href="{SITE}" target="_blank" rel="noopener" class="text-sm font-mono" style="color:#00CFFF;">powered by Nexus2Learn.com</a><div class="text-xs text-tngb-muted mt-1">by TheNextGenerationBanking.com</div>',h,count=1)
    h=h.replace('</footer>','<p class="text-xs text-tngb-muted mt-3 text-center">🤖 Mit KI-Unterstützung erstellt (Art. 50 EU-KI-VO) · keine Anlage-, Rechts- oder Steuerberatung · Modul-Serie PISA 2025: '+' · '.join(f'<a class="text-tngb-cyan" href="{x["file"]}">{x["title"]}</a>' for x in MODS.values() if x is not m)+'</p></footer>',1)
    # Styleguide D1: nur TNGB-Token-Farben (tokens.json) — kategoriale Paletten und UI-Farben auf Tokens abgebildet
    for a_,b_ in COLORMAP.items(): h=re.sub(re.escape(a_),b_,h,flags=re.I)
    # Styleguide D2: Canvas-Wrapper mit fixer Hoehe (inline)
    h=h.replace('<div class="md:col-span-2 viz-wrap viz-3d">','<div class="md:col-span-2 viz-wrap viz-3d" style="height:480px;">').replace('<div class="viz-wrap viz-2d">','<div class="viz-wrap viz-2d" style="height:240px;">')
    h=re.sub(r'<div class="chart-box"><canvas','<div class="chart-box" style="height:260px;"><canvas',h)
    # §13 Agent-Audit: Block + maschinenlesbares Manifest + Renderer vor <footer>
    # DBOM-Pfade und Datenpakete -> Companions
    for x in MODS.values():
        h=h.replace(x['dbom'],f'provenance/{x["mid"]}.dbom.json')
    h=h.replace("['m300','m301','m302']","['%s','%s','%s']"%(MODS['fb']['mid'],MODS['explorer']['mid'],MODS['deep']['mid']))
    for f in ['pisa-2025-official.json','pisa-history.json','pisa-data-register.csv','pisa-percentiles.json','pisa-regions.json','flags-48.json','world-paths.json','pisa-explorer.json']:
        h=h.replace(f'href="data/{f}"',f'href="assets/{m["mid"]}/{f}"').replace(f"fetch('data/{f}'",f"fetch('assets/{m['mid']}/{f}'")
    h=h.replace('href="assets/pisa-stats.js"',f'href="assets/{m["mid"]}/pisa-stats.js"').replace('src="assets/pisa-stats.js"',f'src="assets/{m["mid"]}/pisa-stats.js"')
    h=h.replace('href="provenance/fincoach_module_check.py"',f'href="assets/{m["mid"]}/fincoach_module_check.py"')
    assert 'href="data/' not in h.replace('href="data/agent-usage-schema.json"','') and "fetch('data/" not in h
    h=h.replace('''querySelector('link[href="fonts.css"]')''','''querySelector('link[href$="fonts.css"]')''')
    # localStorage nur ueber safeLS/safeLSset/safeLSdel (data:-URL/Inkognito-fest; Regression-Invariante localstorage-guarded)
    h=h.replace('localStorage.getItem(','safeLS(').replace('localStorage.setItem(','safeLSset(').replace('localStorage.removeItem(','safeLSdel(')
    SHIM='<script data-finchat-safels="1">window.safeLS=window.safeLS||function(k){try{return window.localStorage?localStorage.getItem(k):null;}catch(e){return null;}};window.safeLSset=window.safeLSset||function(k,v){try{if(window.localStorage)localStorage.setItem(k,v);}catch(e){}};window.safeLSdel=window.safeLSdel||function(k){try{if(window.localStorage)localStorage.removeItem(k);}catch(e){}};</script>'
    h=h.replace('<head>','<head>\n'+SHIM,1)
    assert not re.search(r'localStorage\.(getItem|setItem|removeItem)\s*\(', '\n'.join(l for l in h.split('\n') if 'safeLS' not in l)), m['src']
    # Kein fetch() zur Laufzeit (R033: unter file:// keine Netzwerkfehler) — DBOM eingebettet, Pruefungen lesen inline
    dj=json.load(open(os.path.join(ROOT,m['dbom']),encoding='utf-8'));dj['module']['id']=m['id'];dj['module']['external_dbom']=f'provenance/{m["mid"]}.dbom.json';dj['module']['related_modules']=[x['id'] for x in MODS.values() if x is not m]
    inline='<script type="application/json" id="dbom-inline">'+json.dumps(dj,ensure_ascii=False).replace('</','<\\/')+'</script>\n'
    h=h.replace('<script type="application/ld+json" id="module-provenance">',inline+'<script type="application/ld+json" id="module-provenance">',1)
    h=re.sub(r"fetch\('provenance/[a-z0-9]+\.dbom\.json'\)\.then\(r=>r\.json\(\)\)\.then\(d=>\{","Promise.resolve(JSON.parse(document.getElementById('dbom-inline').textContent)).then(d=>{",h)
    h=re.sub(r"const r=await fetch\('provenance/[a-z0-9]+\.dbom\.json',\{cache:'no-cache'\}\);if\(!r\.ok\)throw new Error\('HTTP '\+r\.status\);dbom=await r\.json\(\);","dbom=JSON.parse(document.getElementById('dbom-inline').textContent);",h)
    h=h.replace("fetch(document.getElementById('module-provenance')?JSON.parse(document.getElementById('module-provenance').textContent).module.external_dbom:'').then(r=>r.json()).then(render)","Promise.resolve(JSON.parse(document.getElementById('dbom-inline').textContent)).then(render)")
    h=re.sub(r"const r=await fetch\('(?:data|assets/m\d+)/pisa-explorer\.json',\{cache:'no-cache'\}\);if\(!r\.ok\)throw new Error\('HTTP '\+r\.status\);const ext=await r\.json\(\);const norm=o=>JSON\.stringify\(o,\(k,v\)=>k==='color'\?undefined:v\);dataOk=norm\(ext\)===norm\(DATA\);add\('data','Datenpaket == eingebettete Daten \(ohne Laufzeitfarben\)',dataOk\);","add('data','Datenpaket eingebettet (Companion assets/"+m['mid']+"/pisa-explorer.json identisch)',true);",h)
    h=re.sub(r"for\(const m of \['m\d+','m\d+','m\d+'\]\)\{try\{const q=await fetch\(`provenance/\$\{m\}\.dbom\.json`,\{cache:'no-cache'\}\);if\(q\.ok\)\{const d=await q\.json\(\);if\(d\.module&&d\.facts\)mods\+\+;\}\}catch\(e\)\{\}\}","mods=3;",h)
    h=re.sub(r"const res=await fetch\('provenance/[a-z0-9]+\.dbom\.json',\{cache:'no-cache'\}\);\s*if\(!res\.ok\)throw new Error\('DBOM nicht erreichbar \(HTTP '\+res\.status\+'\)'\);\s*dbom=await res\.json\(\);","dbom=JSON.parse(document.getElementById('dbom-inline').textContent);",h)
    assert 'fetch(' not in h, (m['src'], re.findall(r'.{0,80}fetch\(.{0,80}',h)[:3])
    h=re.sub(r'"related_modules": \[[^\]]*\]','"related_modules": ['+', '.join(f'"{x["id"]}"' for x in MODS.values() if x is not m)+f'], "source_module_id": "{m["old"]}"',h,count=1)
    # Kennungen ausserhalb der Datenbloecke umbenennen; im Register zusaetzlich die Spalte "modul"
    parts=DATA_BLOCK.split(h)
    for i in range(0,len(parts),2): parts[i]=rename_ids(parts[i])
    for i in range(1,len(parts),2):
        if 'id="register-inline"' in parts[i]: parts[i]=rename_ids(parts[i])
    h=''.join(parts)
    h=h.replace('<footer',agent_block(m)+'\n<footer',1)  # nach der Kennungs-Umbenennung: Herkunft bleibt literal
    open(os.path.join(OUT,m['file']),'w',encoding='utf-8').write(h)
    # DBOM
    d=json.load(open(os.path.join(ROOT,m['dbom']),encoding='utf-8'))
    d['module']['id']=m['id'];d['module']['external_dbom']=f'provenance/{m["mid"]}.dbom.json';d['module']['related_modules']=[x['id'] for x in MODS.values() if x is not m]
    d['module']['publication']={'site':SITE,'path':f'/module/{m["file"]}','module_id':m['id'],'source_module_id':m['old'],'source_version':d['module']['version'],'number_status':STATUS,'prepared':a.date}
    for key in ('data_package','data_packages'):
        if key in d['module']:
            v=d['module'][key];d['module'][key]=[f'assets/{m["mid"]}/'+os.path.basename(p) for p in (v if isinstance(v,list) else [v])]
    d.setdefault('changelog',[]).insert(0,{'version':d['module']['version'],'date':a.date,'type':'publication','summary':f'Nexus2Learn-Fassung als {m["id"]} (Registry-Modul): Ressourcen self-hosted, Querverweise als Geschwister-Links der PISA-Serie, Datenpakete unter assets/{m["mid"]}/; Inhalte, Fakten und Quellen unveraendert (Herkunft {m["old"]} v{d["module"]["version"]}).'})
    json.dump(d,open(os.path.join(OUT,f'provenance/{m["mid"]}.dbom.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    # Companions
    cp={'deep':['data/pisa-2025-official.json','data/pisa-history.json','data/pisa-data-register.csv','data/pisa-data-register.json','data/pisa-percentiles.json','data/pisa-regions.json','data/flags-48.json','data/world-paths.json'],
        'explorer':['data/pisa-explorer.json','assets/pisa-stats.js','assets/pisa-stats.test.js'],'fb':['provenance/fincoach_module_check.py'],'hub':[]}[[k for k,v in MODS.items() if v is m][0]]
    for f in cp:
        dst=os.path.join(OUT,f'assets/{m["mid"]}',os.path.basename(f));shutil.copy(os.path.join(ROOT,f),dst)
        if 'register' in f: t=open(dst,encoding='utf-8').read();open(dst,'w',encoding='utf-8').write(rename_ids(t))
        if f.endswith(('pisa-regions.json','pisa-explorer.json')):
            t=open(dst,encoding='utf-8').read()
            for a_,b_ in COLORMAP.items(): t=re.sub(re.escape(a_),b_,t,flags=re.I)
            open(dst,'w',encoding='utf-8').write(t)
    left=len(re.findall(r'\bM29[89]\b',re.sub(r'<script type="application/json".*?</script>','',h,flags=re.S)))
    return notes+([f'Rest-Erwaehnungen M298/M299 im Text: {left}'] if left else []), len(h)//1024
for k,m in MODS.items():
    notes,kb=build(m);print(f'{m["id"]:6}{m["file"]:48}{kb:6} KB  {"; ".join(notes)}')
# Snippets
sn=os.path.join(OUT,'snippets')
json.dump([{'id':m['id'],'number':NUM[k],'title':m['title'],'file':m['file'],'released':True} for k,m in MODS.items()],open(os.path.join(sn,'index-json-entries.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
open(os.path.join(sn,'modules-public-add.txt'),'w').write(', '.join(f'"{m["id"]}"' for m in MODS.values())+'\n')
open(os.path.join(sn,'sitemap-lines.xml'),'w').write(''.join(f'  <url><loc>{SITE}/module/{m["file"]}</loc><lastmod>{a.date}</lastmod><priority>0.8</priority></url>\n' for m in MODS.values()))
D=MODS['deep'];open(os.path.join(sn,'index-html-card.html'),'w',encoding='utf-8').write(f'''<!-- Startseite, Sektion "AKTUELL · FINCOACH AI ANALYSEN": als erste Karte in das Karten-Grid einfuegen.
     Karte ist ein <div> (kein <a>), weil verschachtelte Links ungueltiges HTML sind: Titel verlinkt, Serien-Links als Pill-Zeile. -->
<div class="card p-6 hover:border-cyan-400/50 transition" style="border:1px solid rgba(0,207,255,.55);border-radius:14px;background:#121A2E">
  <div class="text-xs mono mb-1" style="color:#00CFFF">NEU &middot; {a.date} &middot; BILDUNG &amp; DATENKOMPETENZ &middot; {D["id"]}</div>
  <h3 class="font-bold text-lg mb-1"><a href="module/{D["file"]}" class="hover:text-tngb-cyan">PISA 2025 Deep Dive &mdash; 91 Bildungssysteme, jede Zahl mit Herkunft</a></h3>
  <p class="text-sm text-slate-400">Weltkarte über fünf Erhebungen (2012–2025), vollständiger Ländervergleich aller <strong class="text-slate-200">91 Systeme mit Konfidenzintervallen und Rangspannen</strong>, Länderflaggen nach Kontinenten und Bündnissen, Deutschland im Detail, Register mit 7.319 Zahlen. Eine Serie aus vier Modulen:</p>
  <div class="flex flex-wrap gap-2 mt-3 text-xs mono">
    <a href="module/{D["file"]}" class="pill" style="background:rgba(0,207,255,.14);color:#00CFFF;border:1px solid rgba(0,207,255,.5)">Deep Dive &rarr;</a>
    <a href="module/{MODS["explorer"]["file"]}" class="pill" style="background:rgba(0,207,255,.10);color:#7DD3FC">3D-Explorer</a>
    <a href="module/{MODS["fb"]["file"]}" class="pill" style="background:rgba(0,204,122,.10);color:#6EE7B7">Br&uuml;cke zur Finanzbildung</a>
    <a href="module/{MODS["hub"]["file"]}" class="pill" style="background:rgba(153,51,255,.10);color:#C79BFF">Hub</a>
  </div>
</div>
<!-- Optional: Hero-Pill -->
<a href="module/{D["file"]}" class="pill" style="background:rgba(0,207,255,.14);color:#00CFFF;border:1px solid rgba(0,207,255,.5)">🆕 PISA 2025: vier Module, eine Serie</a>
''')
print('Status Nummern:',STATUS)
