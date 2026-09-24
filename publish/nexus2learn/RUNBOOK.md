# Veröffentlichung „PISA 2025 Deep Dive“ auf www.nexus2learn.com · FinCoach AI Module

Stand 2026-09-24 · Quelle: `m302.html` v1.3.1 dieses Repositories (Repository-Kennung **M302**).
Ziel: Modulkatalog `https://www.nexus2learn.com/module` (Repo `MartinHauptmann/nexus2learn-website`,
Freigabeprozess laut `tools/MODUL-FREIGABE-SETUP.md` und `tools/release-modules.ps1`).

## 0 · Ergebnis der Vorbereitung (dieses Paket)

| Datei | Zweck |
|---|---|
| `build.py` | erzeugt `out/` aus `m302.html` + `provenance/m302.dbom.json` + `data/*` — Parameter `--number <NNN>` |
| `out/modul-m479-pisa-2025-deep-dive.html` | Root-Fassung des Moduls (Konventionen der Website: `../assets/fonts/fonts.css`, `../vendor/tailwind.js`, Geschwister-Links `index.html`/`impressum.html`/`datenschutz.html`/`modul-matrix.html`, die `release-modules.ps1` auf `../` umschreibt) |
| `out/provenance/m479.dbom.json` | M-DBOM als Companion (wird vom Release-Skript nach `module/provenance/` kopiert) |
| `out/assets/m479/*` | Datenpakete als Companions (per `href` referenziert → werden nach `module/assets/m479/` kopiert) |
| `out/snippets/*` | Eintrag für `module/index.json`, Allowlist-Zeile, Sitemap-Zeile, Startseiten-Karte |
| `media/m479.jpg` | Hero-Teaser 640×400 (wie `generate-teasers.mjs`: 1280×800, Faktor 0,5, JPEG 72) → `module/assets/teaser/m479.jpg` |
| `media/m479-pisa-2025-1200x627.png` | Open-Graph-Bild → `assets/og/m479-pisa-2025-1200x627.png` |

**Die Nummer M479 ist provisorisch.** Sie ist die nächste freie Nummer laut `module/index.json` der Website
(höchste vergebene: M478), aber laut `MODULE-REGISTRY-GOVERNANCE.md` (Regel 3) darf eine Nummer nur
`reserve-number.ps1` vergeben. Nach der Reservierung den Build mit der echten Nummer wiederholen.

Warum nicht M302: Auf der Website ist **M302 bereits „IT Operating / IKT-Sicherheit“** (ebenso M299–M301 und
M303 vergeben). Deshalb trägt die Website-Fassung eine neue Nummer; die Herkunft (M302 v1.3.1) steht im DBOM
(`module.publication.source_module_id`) und im Fußtext. Die Fakten-IDs (`FACT_M302_*`) bleiben unverändert,
damit alle `data-source`-Referenzen weiter auflösen.

## 1 · Schritte im FinCoach-Root (`C:\Users\User\AI Financecoach`)

```powershell
# 1) Nummer reservieren (Pflicht, -Slug ist Pflicht)
pwsh scripts/compliance/reserve-number.ps1 -Reserve -Slug 'pisa-2025-deep-dive'
#    -> liefert die Nummer NNN

# 2) Paket mit der reservierten Nummer neu bauen (in diesem Repo)
python3 publish/nexus2learn/build.py --number NNN

# 3) Dateien in den FinCoach-Root übernehmen
#    out/modul-mNNN-pisa-2025-deep-dive.html  -> <Root>/modul-mNNN-pisa-2025-deep-dive.html
#    out/provenance/mNNN.dbom.json            -> <Root>/provenance/mNNN.dbom.json
#    out/assets/mNNN/*                        -> <Root>/assets/mNNN/*
#    media/mNNN-pisa-2025-1200x627.png        -> <Root>/publish-nexus2learn/assets/og/

# 4) Registry/Matrix synchronisieren (Single Source of Truth)
pwsh scripts/compliance/sync-modules.ps1

# 5) Gates laut RUNBOOK-DEEPDIVE-TO-PUBLISH.md Teil C (Design-Auditor, Interactive-Auditor, Regression-Guard)
pwsh scripts/styleguide/audit-module.ps1 -Module modul-mNNN-pisa-2025-deep-dive.html
node scripts/regression/check-interactive-diagrams.mjs modul-mNNN-pisa-2025-deep-dive.html
pwsh scripts/regression/guard.ps1 -Module modul-mNNN-pisa-2025-deep-dive.html
```

Hinweise zu den Gates: Das Modul hat keine `input[type=range]`-Slider und keine KaTeX-Formeln; die
Regression-Invarianten „Slider verändert Output“ und „keine `.katex-error`“ greifen daher nicht. Es
verwendet ausschließlich eigenes SVG/Canvas-freies Rendering, keine ECharts/Chart.js.

## 2 · Freigabe im Publish-Paket (`publish-nexus2learn` = Repo `nexus2learn-website`)

```powershell
# 6) Allowlist: "MNNN" in publish-nexus2learn/modules-public.json ergänzen (Snippet: out/snippets/modules-public-add.txt)
# 7) Transfer: kopiert HTML + Companions (provenance/, assets/mNNN/) nach module/, schreibt module/index.json, erzeugt Teaser
pwsh publish-nexus2learn/tools/release-modules.ps1
#    Fallback ohne Teaser-Toolchain: -SkipTeasers und media/mNNN.jpg manuell nach module/assets/teaser/ legen

# 8) Sitemap: Zeile aus out/snippets/sitemap-line.xml in sitemap.xml eintragen (lastmod = Release-Datum)
# 9) Startseite (optional, empfohlen): Karte aus out/snippets/index-html-card.html als erste Karte in
#    Sektion "AKTUELL · FINCOACH AI ANALYSEN" einfügen; optional Hero-Pill
# 10) Veröffentlichen
git add -A && git commit -m "feat(mNNN): PISA 2025 Deep Dive freigegeben" && git push   # Netlify-Auto-Deploy
```

## 3 · Was die Website-Fassung vom Repository-Original unterscheidet

- Fonts und Tailwind self-hosted (`../assets/fonts/fonts.css`, `../vendor/tailwind.js`): erfüllt die CSP der
  Website (`script-src 'self'`, `font-src 'self' data:`). Kein externer Abruf; Flaggen sind Data-URIs.
- Querverweise auf die PISA-Schwestermodule (Explorer, „PISA 2025 & Finanzbildung“, Hub) zeigen extern auf
  `https://fincoach-spacex-ipo-m298.netlify.app/…` (dort M300/M301/Hub) — auf der Website kollidieren diese
  Nummern mit anderen Modulen. **Vor dem Release prüfen, ob die Netlify-Site live ist**, sonst Links entfernen.
- Kopf: Canonical, `og:url`, `og:image` (1200×627), Twitter-Card. Fußzeile: „powered by Nexus2Learn.com“,
  Hinweis Art. 50 EU-KI-VO, Link auf das Quell-Repository.
- Prüfanzeigen (M-DBOM-Leiste, Live-Audit, QA-Kennzeichen) sind ausgeblendet (`?audit=1` zeigt sie).
- Datenregister: die Spalte „Modul“ trägt die Quell-Kennungen `M302/M301` (Herkunft der Zahl im Repository);
  das ist gewollt und im Fußtext erläutert.

## 4 · Prüfergebnisse der Vorbereitung (Website-Klon, lokal, 2026-09-24)

| Prüfung | Ergebnis |
|---|---|
| Rendering in der Website-Struktur (`module/…`, Companions kopiert wie durch `release-modules.ps1`) | ohne JS-Fehler, ohne fehlgeschlagene Requests |
| Externe Requests (CSP) | keine — alle Ressourcen `self` oder `data:` |
| Live-QA des Moduls | 35/35 Checks, DBOM-Referenzen (42) aufgelöst, Datenpakete konsistent |
| Hero-Grafik | 91 Systeme, Flaggen, Kontinentflächen |
| Katalog-Rücklink `../module.html` | vorhanden (Nav + Fußzeile) |
| Mobil 375 px | kein horizontaler Überlauf (Auswahlfelder auf `max-width:100%` begrenzt, auch im Original nachgezogen) |
| Teaser | 38 KB JPEG, Hero sichtbar |

## 5 · Offene Punkte

1. Nummer reservieren und Build wiederholen (Abschnitt 1).
2. Netlify-Site der Schwestermodule prüfen (Abschnitt 3), sonst externe Links im `build.py` anpassen.
3. Registry-Eintrag entsteht durch `sync-modules.ps1`; ohne Eintrag würde `release-modules.ps1` die Datei
   beim nächsten Lauf aus `module/` entfernen (kein Alt-Leak-Schutz greift für unbekannte Dateien).
4. Der FinCoach-Root auf GitHub (`fincoach-ai`) ist ein älterer Stand (Registry bis M444); maßgeblich ist der
   lokale Root.
