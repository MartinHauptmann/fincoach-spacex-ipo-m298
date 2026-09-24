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

Was in allen vier Fassungen gleich ist: Fakten-/Quellen-IDs (`FACT_*`, `SRC_*`) unverändert, damit alle
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

# 5) Gates laut RUNBOOK-DEEPDIVE-TO-PUBLISH.md Teil C, je Modul (NNN einsetzen)
pwsh "C:\Users\User\AI Financecoach\scripts\styleguide\audit-module.ps1" -Module "C:\Users\User\AI Financecoach\modul-mNNN-pisa-2025-deep-dive.html"
node "C:\Users\User\AI Financecoach\scripts\regression\check-interactive-diagrams.mjs" "C:\Users\User\AI Financecoach\modul-mNNN-pisa-2025-deep-dive.html"
pwsh "C:\Users\User\AI Financecoach\scripts\regression\guard.ps1" -Module "C:\Users\User\AI Financecoach\modul-mNNN-pisa-2025-deep-dive.html"
#    ebenso fuer modul-mNNN-pisa-explorer.html, modul-mNNN-pisa-2025-finanzbildung.html, modul-mNNN-pisa-hub.html
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

## 3 · Prüfergebnisse (Website-Klon, lokal, reservierte Nummern M479–M482)

| Modul | JS-Fehler | externe Requests | Live-QA | Rücklink `../module.html` | 375 px |
|---|---|---|---|---|---|
| Deep Dive | 0 | 0 | 35/35, Datenpakete konsistent | ja | kein Überlauf |
| Explorer | 0 | 0 | 28/28, Engine-Selbsttest bestanden | ja | kein Überlauf |
| Finanzbildung | 0 | 0 | 25/25, 48 Referenzen aufgelöst, 0 KaTeX-Fehler | ja | kein Überlauf |
| Hub | 0 | 0 | 22/22, Graph konsistent | ja | kein Überlauf |

Keine Links mehr auf `m29x/m30x.html`, `modul.html`, `ipo-prozess.html`; Querverweise laufen über die Serien-Dateien.

## 4 · Danach: Quelle der Wahrheit wechselt

Nach Schritt 4 sind die Dateien im FinCoach-Root kanonisch (Registry, Matrix, Gates). Weitere inhaltliche Änderungen
erfolgen dort; `build.py` in diesem Repository dient nur noch der einmaligen Überführung. Dieses Repository bleibt
als Herkunft im DBOM (`module.publication.source_module_id`, `source_repo` nur im DBOM, nicht auf der Seite).

## 5 · Offene Punkte

1. Reservierungen erledigt (M479–M482); Paket ist damit gebaut. Teaser entstehen bei `release-modules.ps1` neu (Fallback: `media/m479..m482.jpg`).
2. Registry-Einträge entstehen durch `sync-modules.ps1`; ohne sie entfernt `release-modules.ps1` die Dateien wieder.
3. Hub-Kriterienkatalog verweist auf die „FinCoach-Modulvorlage“ (vorher M298/M299); inhaltlich unverändert.
4. Optional später: Umbenennung dieses Repositories und der Netlify-Site (rein kosmetisch, betrifft LinkedIn-Links).
