# Veröffentlichung der PISA-2025-Serie auf www.nexus2learn.com · FinCoach AI Module

Stand 2026-09-24 · Variante „strukturell“: die vier PISA-Bausteine werden **reguläre Registry-Module** des
FinCoach-Root mit internen Querverweisen. Dieses Repository bleibt nur noch Herkunft (Provenienz), nicht Adresse.

| Baustein | Quelle hier | Slug (Reservierung) | Fassung |
|---|---|---|---|
| PISA 2025 Deep Dive | `m302.html` v1.3.1 | `pisa-2025-deep-dive` | `modul-m<NNN>-pisa-2025-deep-dive.html` |
| PISA Explorer (3D) | `m301.html` v1.2.1 | `pisa-explorer` | `modul-m<NNN>-pisa-explorer.html` |
| PISA 2025 & Finanzbildung | `m300.html` v1.0.1 | `pisa-2025-finanzbildung` | `modul-m<NNN>-pisa-2025-finanzbildung.html` |
| PISA-Hub (Verknüpfungs-App) | `pisa-hub.html` v1.0.1 | `pisa-hub` | `modul-m<NNN>-pisa-hub.html` |

Warum neue Nummern: M299–M303 und M449 sind im zentralen Bestand bzw. auf der Website bereits vergeben (M449:
E-Bike-Modul, nur auf der Website, im Root unbekannt). Nummern vergibt ausschließlich `reserve-number.ps1`.

## 0 · Inhalt dieses Pakets

| Datei | Zweck |
|---|---|
| `build.py` | erzeugt `out/` für alle vier Module; Nummern aus `--lock <reserved-numbers.txt>` (je Slug) oder `--numbers deep=…,explorer=…,fb=…,hub=…`. **`out/` liegt fertig gebaut im Repository** (Nummern aus `reserved-numbers.excerpt.txt`, den vier Reservierungen vom 2026-09-24) |
| `out/modul-m<NNN>-<slug>.html` (4×) | Root-Fassungen nach Website-Konventionen: `../assets/fonts/fonts.css`, `../vendor/tailwind.js`, KaTeX/Chart.js aus `../vendor/`, Geschwister-Links `index.html`/`impressum.html`/`datenschutz.html`/`modul-matrix.html` (werden von `release-modules.ps1` auf `../` umgeschrieben), Querverweise der Serie als `modul-m<NNN>-<slug>.html` |
| `out/provenance/m<NNN>.dbom.json` (4×) | M-DBOM je Modul (Companion) mit `module.publication` (Herkunft, Status der Nummer) |
| `out/assets/m<NNN>/*` | Companions: Deep Dive 8 Datenpakete · Explorer `pisa-explorer.json`, `pisa-stats.js`, Tests · Finanzbildung `fincoach_module_check.py` |
| `out/snippets/*` | `index-json-entries.json`, `modules-public-add.txt`, `sitemap-lines.xml`, `index-html-card.html` |
| `media/m479.jpg` … `media/m482.jpg` | Hero-Teaser 640×400 (Konvention `generate-teasers.mjs`); `release-modules.ps1` erzeugt sie ohnehin neu |
| `media/pisa-2025-serie-1200x627.png` | Open-Graph-Bild der Serie → `publish-nexus2learn/assets/og/` (alle vier Module verweisen darauf) |
| `qa-and-teasers.js` | Headless-Prüfung (Fehler, externe Requests, Live-QA, Rücklink, 375 px) + Teaser; Playwright erforderlich |

Was in allen vier Fassungen gleich ist: kein `fetch()` zur Laufzeit (DBOM eingebettet als `#dbom-inline`, Regel R033 file://-Fallback) · Fakten-/Quellen-IDs (`FACT_*`, `SRC_*`) unverändert, damit alle
`data-source`-Referenzen auflösen · Bezüge auf die SpaceX-Module (M298/M299, `modul.html`, `ipo-prozess.html`)
entfernt · Fußzeile „powered by Nexus2Learn.com“, Hinweis Art. 50 EU-KI-VO, Links auf die drei Schwestermodule ·
Canonical/OG-Meta · Prüfanzeigen ausgeblendet (`?audit=1` zeigt sie) · kein externer Abruf (CSP `self`).

## 1 · Nummern reservieren und Paket bauen (FinCoach-Root; alle Pfade absolut)

```powershell
$ROOT = 'C:\Users\User\AI Financecoach'
$PKG  = 'C:\Users\User\AI Financecoach\publish-nexus2learn'
$REPO = 'C:\Users\User\fincoach-spacex-ipo-m298'   # <- Pfad des lokalen Klons dieses Repositories anpassen

# 0) Reparatur (Befund 2026-09-24): irrtuemliche Zeile "M449 ... slug=pisa-2025-deep-dive" aus dem Lockfile loeschen,
#    dann M449 fuer das E-Bike-Modul nachtragen (belegt auf der Website, im Root unbekannt)
notepad "C:\Users\User\AI Financecoach\reserved-numbers.txt"
pwsh "C:\Users\User\AI Financecoach\scripts\compliance\reserve-number.ps1" -Backfill 449 -Slug 'ebike-kompakt-ergonomie-radbauer'

# 1) ERLEDIGT am 2026-09-24: M449 nachgetragen, reserviert M479 Deep Dive · M480 Explorer · M481 Finanzbildung · M482 Hub

# 2) Fertiges Paket holen (kein Python noetig — out\ ist mit den reservierten Nummern gebaut und im Repository)
git clone --branch claude/pisa-2025-finanzbildung-qekrl6 https://github.com/MartinHauptmann/fincoach-spacex-ipo-m298 "C:\Users\User\fincoach-spacex-ipo-m298"
#    bereits vorhanden? dann:  git -C "C:\Users\User\fincoach-spacex-ipo-m298" pull
#    Inhalt: C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\out\  (4 Module, provenance\, assets\m479..m482\, snippets\)

# 3) Dateien in den FinCoach-Root uebernehmen (Module, DBOMs, Companions, OG-Bild)
Copy-Item "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\out\modul-m*.html"   "C:\Users\User\AI Financecoach\"
Copy-Item "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\out\provenance\*"    "C:\Users\User\AI Financecoach\provenance\"
Copy-Item "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\out\assets\*"        "C:\Users\User\AI Financecoach\assets\" -Recurse -Force
Copy-Item "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\media\pisa-2025-serie-1200x627.png" "C:\Users\User\AI Financecoach\publish-nexus2learn\assets\og\pisa-2025-serie-1200x627.png"

# 4) Registry/Matrix synchronisieren (Single Source of Truth)
pwsh "C:\Users\User\AI Financecoach\scripts\compliance\sync-modules.ps1"

# 5) Gates laut RUNBOOK-DEEPDIVE-TO-PUBLISH.md Teil C
#    -Module erwartet den DATEINAMEN (die Skripte loesen ihn gegen den Root auf).
#    Befund 2026-09-24: Der Root hat weder vendor\ noch assets\fonts\ (sie liegen in publish-nexus2learn\);
#    ../vendor/ und ../assets/fonts/ (Konvention der Website-Module, auch M478) loesen im Root deshalb auf 404.
#    Daher: erst Freigabe-Transfer (Schritt 6-7), dann Gates gegen das Publish-Paket als Base:
Start-Process pwsh -ArgumentList '-NoExit','-Command',"npx http-server 'C:\Users\User\AI Financecoach' -c-1 -p 8089"
foreach ($f in 'modul-m479-pisa-2025-deep-dive.html','modul-m480-pisa-explorer.html','modul-m481-pisa-2025-finanzbildung.html','modul-m482-pisa-hub.html') {
  pwsh "C:\Users\User\AI Financecoach\scripts\styleguide\audit-module.ps1" -Module $f -Base http://localhost:8089/publish-nexus2learn/module
  node "C:\Users\User\AI Financecoach\scripts\regression\check-interactive-diagrams.mjs" $f --base=http://localhost:8089/publish-nexus2learn/module
  pwsh "C:\Users\User\AI Financecoach\scripts\regression\guard.ps1" -Module $f -Base http://localhost:8089/publish-nexus2learn/module
}
#    Alternative ohne Umweg: vendor\ und assets\fonts\ aus publish-nexus2learn\ in den Root kopieren (dann Base http://localhost:8089).
```

Hinweise zu den Gates: Der Explorer hat einen Range-Slider (`#simLE`, Linking Error), der die Trend-Tabelle
verändert und damit die Regression-Invariante „Slider verändert Output“ erfüllt; die anderen drei Module haben
keine Slider. KaTeX nur im Modul „PISA 2025 & Finanzbildung“ (vendor 0.16.11 statt CDN 0.16.9, gleiche API);
Chart.js dort aus `vendor/chart-4.4.3.min.js` (statt CDN 4.4.4, API-kompatibel).

## 2 · Freigabe im Publish-Paket (`C:\Users\User\AI Financecoach\publish-nexus2learn` = Repo `nexus2learn-website`)

```powershell
# 6) Allowlist: die vier IDs in modules-public.json ergaenzen (Snippet: out\snippets\modules-public-add.txt)
notepad "C:\Users\User\AI Financecoach\publish-nexus2learn\modules-public.json"

# 7) Transfer: kopiert HTML + Companions nach module\, schreibt module\index.json, erzeugt Teaser
pwsh "C:\Users\User\AI Financecoach\publish-nexus2learn\tools\release-modules.ps1"
#    Fallback ohne Teaser-Toolchain:
pwsh "C:\Users\User\AI Financecoach\publish-nexus2learn\tools\release-modules.ps1" -SkipTeasers
Copy-Item "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\media\m*.jpg" "C:\Users\User\AI Financecoach\publish-nexus2learn\module\assets\teaser\"   # nur bei uebereinstimmenden Nummern

# 8) Sitemap: vier Zeilen aus out\snippets\sitemap-lines.xml eintragen
notepad "C:\Users\User\AI Financecoach\publish-nexus2learn\sitemap.xml"

# 9) Startseite (empfohlen): Karte aus out\snippets\index-html-card.html als erste Karte in
#    Sektion "AKTUELL · FINCOACH AI ANALYSEN"
notepad "C:\Users\User\AI Financecoach\publish-nexus2learn\index.html"

# 10) Veroeffentlichen (Netlify-Auto-Deploy)
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" add -A
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" commit -m "feat(pisa-2025): Serie freigegeben (Deep Dive, Explorer, Finanzbildung, Hub)"
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" push
```

## 3 · Prüfergebnisse und Gate-Befunde (Stand 2026-09-24)

Website-Klon (http und file://), alle vier Module: 0 JS-Fehler, 0 externe Requests, Live-QA vollständig grün
(35/28/25/22 Checks), Rücklink `../module.html`, kein Überlauf bei 375 px, kein `<img>`, kein roher
`localStorage`-Zugriff, kein `fetch()`.

Gate-Lauf im Root (Base http://localhost:8089) vom 2026-09-24 und Reaktion:

| Befund | Ursache | Status |
|---|---|---|
| `localstorage-guarded` (Regression) | roher `localStorage.getItem` | behoben: `safeLS`-Shim + Kapselung |
| `F-IDA-STATIC` Explorer (99 Rasterbilder) | Flaggen-Icons als `<img>` | behoben: Inline-SVG |
| `S-CANVAS-WRAP` (7×) | Canvas-Wrapper ohne Inline-Höhe | behoben: `style="height:…"` wie M478 |
| `S-TOKEN-COLOR` | kategoriale Paletten und UI-Farben außerhalb der TNGB-Tokens | behoben: auf Tokens abgebildet (`COLORMAP` in `build.py`, auch in `pisa-regions.json`/`pisa-explorer.json`); Hinweis: die Token-Palette ist nicht auf Farbsinnschwäche validiert, die Reihen sind beschriftet |
| `S-AGENT-AUDIT` | kein §13-Manifest | ergänzt: Sektion 13 + `module-agents-used`; Deep Dive und Finanzbildung (Typ `tiefenmodul`) führen Council und Wikipedia-Synthese ehrlich als **pending** (nicht durchgeführt) → `agent-audit-check.ps1` meldet Warnung, kein kritischer Befund; vor Publish nachholen oder Ausnahme dokumentieren |
| `S-JS-ERROR` / `no-js-errors` (404) | `vendor\`/`assets\fonts\` fehlen im Root | Umgebung: Gates gegen Publish-Paket als Base (Schritt 5) oder Ordner in den Root kopieren |
| `S-TOKEN-FONT` | Auditor verlangt einen Google-Fonts-`<link>`; die Website-CSP (`style-src 'self'`, `font-src 'self' data:`) verbietet ihn, M478 hat ihn ebenfalls nicht | Regelkonflikt Auditor ↔ CSP; Entscheidung: Auditor-Regel auf self-hosted `assets/fonts/fonts.css` erweitern oder Befund als bekannt akzeptieren |
| `F-IDA-LEVEL/TOOLTIP/NO-DRILLDOWN/STATIC-LABELS` (WARN) | ECharts-spezifische Muster | keine Blocker; Module rendern mit eigenem SVG |

## 4 · Danach: Quelle der Wahrheit wechselt

Nach Schritt 4 sind die Dateien im FinCoach-Root kanonisch (Registry, Matrix, Gates). Weitere inhaltliche Änderungen
erfolgen dort; `build.py` in diesem Repository dient nur noch der einmaligen Überführung. Dieses Repository bleibt
als Herkunft im DBOM (`module.publication.source_module_id`, `source_repo` nur im DBOM, nicht auf der Seite).

## 5 · Offene Punkte

1. Reservierungen erledigt (M479–M482); Paket ist damit gebaut. Teaser entstehen bei `release-modules.ps1` neu (Fallback: `media/m479..m482.jpg`).
2. Registry-Einträge entstehen durch `sync-modules.ps1`; ohne sie entfernt `release-modules.ps1` die Dateien wieder.
3. Hub-Kriterienkatalog verweist auf die „FinCoach-Modulvorlage“ (vorher M298/M299); inhaltlich unverändert.
4. Optional später: Umbenennung dieses Repositories und der Netlify-Site (rein kosmetisch, betrifft LinkedIn-Links).
