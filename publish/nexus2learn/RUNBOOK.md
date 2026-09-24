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
| `release-pisa.ps1` | gezielter Freigabe-Transfer nur der PISA-Serie ins Publish-Paket (Ersatz für `release-modules.ps1`, siehe Warnung in Abschnitt 2) |
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

**Warnung (Befund 2026-09-24): `release-modules.ps1` nicht aus diesem Root-Stand ausführen.** Das Skript entfernt alle
HTMLs in `module\`, die es nicht in Root-Registry + Allowlist findet. Der Root kennt acht öffentliche Module nicht
(M449, M465, M466, M468, M469, M471, M477, M478 wurden außerhalb des Root gebaut); der Lauf würde sie von der Website
löschen. Zusätzlich stoppt der Companion-Drift-Wächter (services/agent-audit-renderer.js, templates/hero-visual/*.js
sind auf der Website neuer als im Root). Beides ist unabhängig von PISA und vorher im Root zu bereinigen.

Deshalb gezielter Transfer nur der PISA-Serie mit dem beiliegenden Skript (macht für die vier Module exakt die
Schritte von `release-modules.ps1`, fasst nichts anderes an):

```powershell
# 6) Vorschau, was passieren wuerde
pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\release-pisa.ps1" -DryRun
# 7) Transfer: Module mit Link-Rewrite nach module\, Companions (komplettes assets\mNNN\ + DBOM, erwartet 16), index.json-Eintraege, Teaser, OG-Bild, Sitemap, Allowlist
pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\release-pisa.ps1"

# 8a) Auditor einmalig Base-faehig machen (patches\run-audit-base-aware.patch, siehe Abschnitt 3):
#     S-LINK-INTERN-RESOLVE prueft Links bei gesetztem -Base per HTTP relativ zur Seite statt gegen den Root-Ordner;
#     S-TOKEN-FONT akzeptiert self-hosted @font-face (Inter, Space Grotesk, JetBrains Mono) als Alternative zum Google-Link.
#     Ohne -Base bleibt das Verhalten unveraendert. Anwendung textbasiert (git apply scheitert an CRLF im Arbeitsverzeichnis):
pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\patches\apply-run-audit-patch.ps1" -DryRun
pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\patches\apply-run-audit-patch.ps1"

# 8b) Golden-Baseline der vier Module einmalig gegen die Publish-Fassung setzen (die erste Baseline entstand
#     beim Root-Lauf mit 404-Seiten und altem Build-Stand; ueberschreibt nur scripts\regression\golden\modul-m479..m482.json)
# 8c) Gates gegen das Publish-Paket (Vorschau-Server aus Abschnitt 1; Port frei waehlen, 8089 kann belegt sein)
foreach ($f in 'modul-m479-pisa-2025-deep-dive.html','modul-m480-pisa-explorer.html','modul-m481-pisa-2025-finanzbildung.html','modul-m482-pisa-hub.html') {
  pwsh "C:\Users\User\AI Financecoach\scripts\regression\guard.ps1" -Module $f -Base http://localhost:8091/publish-nexus2learn/module -Update
  pwsh "C:\Users\User\AI Financecoach\scripts\styleguide\audit-module.ps1" -Module $f -Base http://localhost:8091/publish-nexus2learn/module
  node "C:\Users\User\AI Financecoach\scripts\regression\check-interactive-diagrams.mjs" "C:\Users\User\AI Financecoach\publish-nexus2learn\module\$f" --base=http://localhost:8091/publish-nexus2learn/module
  pwsh "C:\Users\User\AI Financecoach\scripts\regression\guard.ps1" -Module $f -Base http://localhost:8091/publish-nexus2learn/module
}

# 9) Startseite (empfohlen): Karte aus out\snippets\index-html-card.html als erste Karte in
#    Sektion "AKTUELL · FINCOACH AI ANALYSEN"
notepad "C:\Users\User\AI Financecoach\publish-nexus2learn\index.html"

# 10) Veroeffentlichen (Netlify-Auto-Deploy) — vorher git status pruefen: nur PISA-Dateien, index.json, Allowlist, Sitemap, ggf. index.html
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" status
# nur PISA-Dateien stagen (im Paket koennen Fremdaenderungen liegen, z. B. M449 aus einem abgebrochenen release-modules.ps1-Lauf)
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" add module/index.json modules-public.json sitemap.xml assets/og/pisa-2025-serie-1200x627.png module/modul-m479-pisa-2025-deep-dive.html module/modul-m480-pisa-explorer.html module/modul-m481-pisa-2025-finanzbildung.html module/modul-m482-pisa-hub.html module/assets/m479 module/assets/m480 module/assets/m481 module/assets/teaser/m479.jpg module/assets/teaser/m480.jpg module/assets/teaser/m481.jpg module/assets/teaser/m482.jpg module/provenance/m479.dbom.json module/provenance/m480.dbom.json module/provenance/m481.dbom.json module/provenance/m482.dbom.json
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" status --short
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" commit -m "feat(pisa-2025): Serie freigegeben (M479 Deep Dive, M480 Explorer, M481 Finanzbildung, M482 Hub)"
git -C "C:\Users\User\AI Financecoach\publish-nexus2learn" push
```

## 3 · Prüfergebnisse und Gate-Befunde (Stand 2026-09-24)

**Veröffentlicht am 2026-09-24**: nexus2learn-website `main` 5e7945a → 3e52f1b (28 Dateien). Live-Kontrolle per HEAD: die vier
Modul-Seiten, `module/provenance/m479.dbom.json`, `module/assets/m479/pisa-regions.json`, Teaser m479 und das OG-Bild liefern 200.
Gates vor dem Push gegen das Publish-Paket: Styleguide PASS (0 FAIL) ×4, Interactive PASS ×4, Guard „Keine Regressionen“ ×4.
Root-Commit 3da1058c (Branch `feat/json-api-lovable-integration`): Auditor-Patch + Golden-Baselines.

Website-Klon (http und file://), alle vier Module: 0 JS-Fehler, 0 externe Requests, Live-QA vollständig grün
(35/28/25/22 Checks), Rücklink `../module.html`, kein Überlauf bei 375 px, kein `<img>`, kein roher
`localStorage`-Zugriff, kein `fetch()`.

Gate-Läufe vom 2026-09-24 (Root-Base, danach Publish-Base) und Reaktion. Nach Patch und Golden-Update, hier gegen den
Website-Klon geprüft: Styleguide PASS für alle vier (0 FAIL; WARNs: Landmarks, Touch-Targets, Kontrast, Schriftgröße,
Tooltip-Felder), Interactive PASS (nur ECharts-WARNs).

| Befund | Ursache | Status |
|---|---|---|
| `localstorage-guarded` (Regression) | roher `localStorage.getItem` | behoben: `safeLS`-Shim + Kapselung |
| `F-IDA-STATIC` Explorer (99 Rasterbilder) | Flaggen-Icons als `<img>` | behoben: Inline-SVG |
| `S-CANVAS-WRAP` (7×) | Canvas-Wrapper ohne Inline-Höhe | behoben: `style="height:…"` wie M478 |
| `S-TOKEN-COLOR` | kategoriale Paletten und UI-Farben außerhalb der TNGB-Tokens | behoben: auf Tokens abgebildet (`COLORMAP` in `build.py`, auch in `pisa-regions.json`/`pisa-explorer.json`); Hinweis: die Token-Palette ist nicht auf Farbsinnschwäche validiert, die Reihen sind beschriftet |
| `S-AGENT-AUDIT` | kein §13-Manifest | ergänzt: Sektion 13 + `module-agents-used`; Deep Dive und Finanzbildung (Typ `tiefenmodul`) führen Council und Wikipedia-Synthese ehrlich als **pending** (nicht durchgeführt) → `agent-audit-check.ps1` meldet Warnung, kein kritischer Befund; vor Publish nachholen oder Ausnahme dokumentieren |
| `S-JS-ERROR` / `no-js-errors` (404) | `vendor\`/`assets\fonts\` fehlen im Root | Umgebung: Gates gegen Publish-Paket als Base (Schritt 5) oder Ordner in den Root kopieren |
| `S-TOKEN-FONT` | Auditor verlangt einen Google-Fonts-`<link>`; die Website-CSP (`style-src 'self'`, `font-src 'self' data:`) verbietet ihn, M478 hat ihn ebenfalls nicht | Auditor-Patch `patches/run-audit-base-aware.patch`: self-hosted `@font-face` für alle drei Familien gilt als erfüllt |
| `S-LINK-INTERN-RESOLVE` (6× je Modul: `../index.html`, `../module.html`, `../impressum.html`, `../datenschutz.html`) | Auditor löst `<a href>` aus dem DOM gegen den Root-Ordner auf; die Publish-Fassung liegt in `module\` und verlinkt nach oben | derselbe Patch: bei gesetztem `-Base` HTTP-HEAD relativ zur Seite, Duplikate zusammengefasst; ohne `-Base` unverändert |
| `golden-snapshot` (Regression, 1 Abweichung je Modul) | erste Baseline entstand beim Root-Lauf (404 auf vendor/fonts, alter Build) | Baseline einmalig mit `guard.ps1 -Update` gegen die Publish-Fassung setzen (Schritt 8b) |
| `F-IDA-LEVEL/TOOLTIP/NO-DRILLDOWN/STATIC-LABELS` (WARN) | ECharts-spezifische Muster | keine Blocker; Module rendern mit eigenem SVG |

## 4 · Danach: Quelle der Wahrheit wechselt

Nach Schritt 4 sind die Dateien im FinCoach-Root kanonisch (Registry, Matrix, Gates). Weitere inhaltliche Änderungen
erfolgen dort; `build.py` in diesem Repository dient nur noch der einmaligen Überführung. Dieses Repository bleibt
als Herkunft im DBOM (`module.publication.source_module_id`, `source_repo` nur im DBOM, nicht auf der Seite).

## 5 · Offene Punkte

- Root-Repo: PISA-Dateien gezielt committen (vier HTMLs, vier DBOMs, `assets/m479..m481`, Registry, Matrix, `reserved-numbers.txt`);
  vorher `git diff --cached --stat` prüfen, weil Registry/Matrix/Reservierung Fremdänderungen tragen können.
- Publish-Paket: `module/modul-m449-…html` (+1137 Zeilen) und `module/assets/m449/` stammen aus dem abgebrochenen
  `release-modules.ps1`-Lauf, nicht aus dieser Serie; Entscheidung übernehmen oder verwerfen steht aus.

1. Reservierungen erledigt (M479–M482); Paket ist damit gebaut. Teaser entstehen bei `release-modules.ps1` neu (Fallback: `media/m479..m482.jpg`).
2. Registry-Einträge entstehen durch `sync-modules.ps1`; ohne sie entfernt `release-modules.ps1` die Dateien wieder.
3. Hub-Kriterienkatalog verweist auf die „FinCoach-Modulvorlage“ (vorher M298/M299); inhaltlich unverändert.
4. Optional später: Umbenennung dieses Repositories und der Netlify-Site (rein kosmetisch, betrifft LinkedIn-Links).
