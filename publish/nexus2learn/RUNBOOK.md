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

## 1 · Schritte im FinCoach-Root (alle Pfade absolut)

Konvention: `$ROOT` = FinCoach-Root, `$PKG` = Publish-Paket (Repo `nexus2learn-website`), `$REPO` = lokaler Klon
dieses Repositories (Pfad anpassen, falls abweichend).

```powershell
$ROOT = 'C:\Users\User\AI Financecoach'
$PKG  = 'C:\Users\User\AI Financecoach\publish-nexus2learn'
$REPO = 'C:\Users\User\fincoach-spacex-ipo-m298'   # <- Pfad des lokalen Klons dieses Repositories

# 0) Vorbedingung (Befund 2026-09-24): M449 ist auf der Website belegt (E-Bike-Modul), im Root aber unbekannt.
#    Die irrtuemliche PISA-Zeile fuer M449 aus dem Lockfile entfernen, M449 fuer das E-Bike-Modul nachtragen:
notepad "$ROOT\reserved-numbers.txt"     # Zeile "M449 ... slug=pisa-2025-deep-dive" loeschen
pwsh "$ROOT\scripts\compliance\reserve-number.ps1" -Backfill 449 -Slug 'ebike-kompakt-ergonomie-radbauer'

# 1) Nummer reservieren, oberhalb der hoechsten oeffentlich vergebenen Nummer (M478 auf der Website)
pwsh "$ROOT\scripts\compliance\reserve-number.ps1" -Reserve -Slug 'pisa-2025-deep-dive' -Min 479
#    -> gibt die Nummer MNNN aus und schreibt sie nach $ROOT\reserved-numbers.txt

# 2) Paket mit der reservierten Nummer bauen (liest die Nummer aus dem Lockfile)
python "$REPO\publish\nexus2learn\build.py" --lock "$ROOT\reserved-numbers.txt"
#    alternativ: python "$REPO\publish\nexus2learn\build.py" --number NNN
#    Ergebnis: $REPO\publish\nexus2learn\out\

# 3) Dateien in den FinCoach-Root uebernehmen (NNN ersetzen)
Copy-Item "$REPO\publish\nexus2learn\out\modul-mNNN-pisa-2025-deep-dive.html" "$ROOT\modul-mNNN-pisa-2025-deep-dive.html"
Copy-Item "$REPO\publish\nexus2learn\out\provenance\mNNN.dbom.json"       "$ROOT\provenance\mNNN.dbom.json"
New-Item -ItemType Directory -Force "$ROOT\assets\mNNN" | Out-Null
Copy-Item "$REPO\publish\nexus2learn\out\assets\mNNN\*"                   "$ROOT\assets\mNNN\"
Copy-Item "$REPO\publish\nexus2learn\media\mNNN-pisa-2025-1200x627.png"     "$PKG\assets\og\mNNN-pisa-2025-1200x627.png"

# 4) Registry/Matrix synchronisieren (Single Source of Truth)
pwsh "$ROOT\scripts\compliance\sync-modules.ps1"

# 5) Gates laut RUNBOOK-DEEPDIVE-TO-PUBLISH.md Teil C
pwsh "$ROOT\scripts\styleguide\audit-module.ps1" -Module "$ROOT\modul-mNNN-pisa-2025-deep-dive.html"
node "$ROOT\scripts\regression\check-interactive-diagrams.mjs" "$ROOT\modul-mNNN-pisa-2025-deep-dive.html"
pwsh "$ROOT\scripts\regression\guard.ps1" -Module "$ROOT\modul-mNNN-pisa-2025-deep-dive.html"
```

Hinweise zu den Gates: Das Modul hat keine `input[type=range]`-Slider und keine KaTeX-Formeln; die
Regression-Invarianten „Slider verändert Output“ und „keine `.katex-error`“ greifen daher nicht. Es
verwendet ausschließlich eigenes SVG-Rendering, keine ECharts/Chart.js.

## 2 · Freigabe im Publish-Paket (`$PKG` = Repo `nexus2learn-website`)

```powershell
# 6) Allowlist: "MNNN" in $PKG\modules-public.json ergaenzen
#    (Snippet: $REPO\publish\nexus2learn\out\snippets\modules-public-add.txt)
notepad "$PKG\modules-public.json"

# 7) Transfer: kopiert HTML + Companions (provenance/, assets/mNNN/) nach $PKG\module\,
#    schreibt $PKG\module\index.json, erzeugt den Teaser $PKG\module\assets\teaser\mNNN.jpg
pwsh "$PKG\tools\release-modules.ps1"
#    Fallback ohne Teaser-Toolchain:
pwsh "$PKG\tools\release-modules.ps1" -SkipTeasers
Copy-Item "$REPO\publish\nexus2learn\media\mNNN.jpg" "$PKG\module\assets\teaser\mNNN.jpg"

# 8) Sitemap: Zeile aus $REPO\publish\nexus2learn\out\snippets\sitemap-line.xml in $PKG\sitemap.xml eintragen
notepad "$PKG\sitemap.xml"

# 9) Startseite (optional, empfohlen): Karte aus $REPO\publish\nexus2learn\out\snippets\index-html-card.html
#    als erste Karte in Sektion "AKTUELL · FINCOACH AI ANALYSEN" von $PKG\index.html einfuegen
notepad "$PKG\index.html"

# 10) Veroeffentlichen (Netlify-Auto-Deploy)
git -C "$PKG" add -A
git -C "$PKG" commit -m "feat(mNNN): PISA 2025 Deep Dive freigegeben"
git -C "$PKG" push
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

1. Nummer reservieren (mit `-Min 479`, nach Backfill von M449) und Build wiederholen (Abschnitt 1).
2. Netlify-Site der Schwestermodule prüfen (Abschnitt 3), sonst externe Links im `build.py` anpassen.
3. Registry-Eintrag entsteht durch `sync-modules.ps1`; ohne Eintrag würde `release-modules.ps1` die Datei
   beim nächsten Lauf aus `module/` entfernen (kein Alt-Leak-Schutz greift für unbekannte Dateien).
4. Der FinCoach-Root auf GitHub (`fincoach-ai`) ist ein älterer Stand (Registry bis M444); maßgeblich ist der
   lokale Root.
