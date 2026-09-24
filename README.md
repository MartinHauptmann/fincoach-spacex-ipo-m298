# SpaceX — Der Weg zum Billionen-IPO · Publishing-Paket (Modul M298)

Eigenständig deploybare, statische Website (FinCoach AI · TheNextGenerationBanking) zur kritischen
SpaceX-IPO-Analyse mit globalem Vergleich.
**Kein Build-Step** — reines HTML/CSS/JS (Schriften self-hosted, übrige Libs via CDN). Direkt auf Netlify hostbar.

---

## 1 · Inhalt des Pakets

| Datei | Zweck |
|---|---|
| `index.html` | Landing-Page mit Disclaimer, Privatfirmen-Hinweis, Themenüberblick, Brand |
| `modul.html` | Vollständiges Analyse-Modul (M298) inkl. Charts/Simulatoren — Schriften via `fonts.css` self-hosted |
| `ipo-prozess.html` | Übersicht des IPO-Prozesses: Phasen, Beteiligte/Zustimmungen, Rolle der Banken, Pflichten vor & nach dem Börsengang |
| `m299.html` | Deep-Dive IPO-Zuteilung (M299): Quoten-Kaskade, Simulator, M-DBOM-Provenienz, Compliance-/Datenqualitäts-Checks |
| `m300.html` | Deep-Dive PISA 2025 & Finanzbildung (M300): verifizierte OECD-Ergebnisse, Verifikationsprotokoll, Diagnostik-Instrumente, DCM-Rechner, OECD/INFE-Kopplung, KI-Anforderungskatalog mit Abnahmetests, Compliance-Klauseln CL-01…CL-12, Live-QA |
| `m301.html` | PISA Explorer (M301): 3D-Ländervergleich mit Zeittrajektorien, SE/KI/Signifikanz inkl. Linking Error, Explainability-Glossar, Diagnostik-Hypothesen, Länderflaggen und Gruppenflächen (Kontinente/Bündnisse) in 3D/2D; Daten in `data/pisa-explorer.json`, Statistik-Engine `assets/pisa-stats.js` (Tests: `node assets/pisa-stats.test.js`) |
| `m302.html` | PISA 2025 Deep Dive (M302): Studiendesign, Methodenwandel 2012–2025, Weltkarte über fünf Erhebungen, Ländervergleich 91 Systeme (OECD-StatLink), Datenregister; Hero-Grafik mit Länderflaggen und Gruppenflächen (Kontinente/Bündnisse); Daten in `data/pisa-2025-official.json`, `data/pisa-history.json`, `data/world-paths.json`, `data/pisa-data-register.csv`, `data/pisa-percentiles.json`, `data/pisa-regions.json` (Kontinent-/Bündniszuordnung, Referenzklasse), `data/flags-48.json` (91 Flaggen aus flag-icons, MIT, eingebettet) |
| `social/linkedin-pisa-2025-91-systeme.{html,png,md}` | LinkedIn-Grafik (1200×1500, aus den M302-Daten gerendert) und Post-Text mit Alt-Text und Zahlenherkunft |
| `publish/nexus2learn/` | Veröffentlichungspaket der PISA-Serie für www.nexus2learn.com: vier Registry-Module (Deep Dive, Explorer, Finanzbildung, Hub) mit Website-Konventionen und internen Querverweisen, DBOMs, Datenpakete, Snippets, Teaser/OG-Bild, QA-Skript, Runbook |
| `pisa-hub.html` | PISA-Hub: interaktiver Argumentationsgraph, 12-Schritte-Kette und Kriterien-Matrix über M300/M301/M302 |
| `provenance/*.dbom.json` | M-DBOM-Provenienz je Modul (Fakten, Verdicts, Konfidenzen, Quellen, Audit-Trail) |
| `provenance/fincoach_module_check.py` | Statische Modul-Prüfung (Compliance / Datenqualität / Styleguide) — `python3 provenance/fincoach_module_check.py m300.html` |
| `impressum.html` | Impressum nach § 5 DDG / § 18 MStV (ausgefüllt) |
| `datenschutz.html` | DSGVO-Datenschutzerklärung (ausgefüllt) |
| `fonts.css` + `fonts/` | Self-gehostete Schriften (Inter, Space Grotesk, JetBrains Mono) — keine Google-CDN-Abrufe |
| `netlify.toml` | Redirects, Security-Header, CSP, Caching |
| `robots.txt`, `sitemap.xml` | SEO (Domain bei eigener Domain ersetzen) |
| `.gitignore` | Git-Ausschlüsse |

---

## 2 · Rechtliche Eckpunkte (bereits umgesetzt)

- **Privatfirmen-/Bewertungs-Disclaimer (M-DBOM-Pflicht):** SpaceX ist seit 12.06.2026 börsennotiert
  (Ticker `SPCX`, NASDAQ). Die genannten Bewertungs-/Finanzzahlen sind dennoch weiterhin medien- bzw.
  nutzerbasierte Schätzungen und nicht unabhängig von FinCoach AI verifiziert (Landing + Modul, Stand
  2026-06-19). Verifizierte Fakten sind von `SCENARIO_PROJECTION`-Annahmen getrennt.
- **Fachlicher Disclaimer:** Keine Rechts-, Steuer- oder Anlageberatung (RDG/StBerG/WpIG/FinDAG); Hinweis auf
  Markt-/Totalverlustrisiko.
- **Marken-Hinweis:** „SpaceX", „Starlink", „Starship" rein beschreibend genannt.
- **Sicherheit:** CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
  (via `netlify.toml`).
- **DSGVO:** Schriften self-hosted; keine Tracking-Cookies/Analyse-Tools; nur technisch notwendige
  Session-Speicherung. AVV mit Netlify in der Datenschutzerklärung verlinkt.

> Vor Go-Live empfohlen: AVV/DPA mit Netlify bestätigen; bei eigener Domain die Domain in
> `sitemap.xml`, `robots.txt`, `index.html` (canonical/OG) eintragen. Die Vorlagen sind **keine Rechtsberatung**.

---

## 2b · Definierte Prüfungen für FinCoach-AI-Module

Jedes Modul muss vor dem Release die dreistufige Prüfung bestehen (identisch als Live-Check im Browser
und als statischer Check per Skript):

```bash

Veröffentlichungsmodus: Provenienz-Leiste (M-DBOM), Live-Audit-Banner und QA-Kennzeichen sind in allen Modulen standardmäßig ausgeblendet (`.audit-ui`). Die Prüfungen laufen trotzdem; die Anzeigen erscheinen in der Prüfansicht über den URL-Parameter `?audit=1` (bzw. `localStorage.fc_audit = "1"`).
python3 provenance/fincoach_module_check.py m299.html m300.html m301.html m302.html pisa-hub.html   # Exit 0 = alle Pflichtprüfungen bestanden
node assets/pisa-stats.test.js                                              # Statistik-Engine (M301)
```

| Stufe | Prüfungen (Auszug) |
|---|---|
| ① Compliance | Disclaimer „keine Anlageberatung“, RDG/StBerG/WpIG/FinDAG, DSGVO, Markennennung, Stichtag, Honest Disclosure, Impressum/Datenschutz, CSP-konforme CDNs, keine Tracker |
| ② Datenqualität | JSON-LD-Provenienz, externe DBOM valide, eindeutige Fakt-IDs, `fact_summary` konsistent, alle `data-source`-Referenzen auflösbar, Quelle/Konfidenz/Verdict je Fakt, Stichtag & Version konsistent |
| ③ Styleguide | fonts.css, CAT-Level, NavDock, Live-Audit-Banner, QA-Sektion, Glossar, Modul-Matrix, TNGB-Farbtoken, EST/REP-Marker, keine unmaskierten `<` im Fließtext |

M300 enthält zusätzlich den Anforderungskatalog REQ-01…REQ-10 (Abnahmetests für KI-Lernsysteme) und
die Compliance-Klauseln CL-01…CL-12 (DSGVO Art. 8/22/35, EU-KI-VO Anhang III inkl. Digital-Omnibus-Fristen,
Zweckbindung Bildung ↔ Bankgeschäft, BFSG/WCAG).

---

### Datenherkunft der PISA-Module (Kurzfassung)

| Klasse | Bedeutung | Vorkommen |
|---|---|---|
| OFFICIAL_STATLINK | OECD StatLink Band I 2025, Kap. 2 (stat.link/xgs41b) | alle 2025-Werte, 91 Systeme |
| DERIVED_OFFICIAL / DERIVED_CI | aus offiziellen Werten berechnet (2022 = 2025 − Δ; SE = KI-Breite/3,92) | 2022-Mittel, 2025-SE |
| OFFICIAL_COUNTRYNOTE | OECD-Ländernotiz, per Suchauszug verifiziert | DE-Detail (M300) |
| SECONDARY_OECDSTAT | OECD.Stat-Spiegel 2003–2015 (kirenz/datasets) | Mathematik 2012/2015, 44 Systeme |
| COMPUTED_MICRODATA | aus OECD-Public-Use-Files gewichtet berechnet (ein Plausible Value; Abweichung zur Tabelle typ. < 2 Pkt.) | 2012/2015/2018 alle Domänen, 2022 ohne Trendwert |
| EST / SCENARIO | Schätzung bzw. Modellannahme | SE 2022, Linking Error, DCM-Demo |

---

## 3 · Deployment — GitHub + Netlify (Auto-Deploy)

Jeder `git push` veröffentlicht automatisch neu.

```bash
cd publish-m298-spacex
git init -b main
git add .
git commit -m "FinCoach AI SpaceX-Analyse M298 — initial site"
gh repo create fincoach-spacex-ipo-m298 --public --source=. --remote=origin --push
```

Dann in Netlify: **Add new site → Import an existing project → GitHub** → Repo wählen → Deploy.
(Build command leer, Publish directory `.` — kommt aus `netlify.toml`.)

### Schnellster Weg ohne GitHub-Verknüpfung: Netlify CLI

```bash
cd publish-m298-spacex
netlify deploy --prod
```

---

## 4 · Updates des Analyse-Moduls

Quelle wird im Hauptprojekt gepflegt (`modul-m298-spacex-ipo-globaler-vergleich.html`). Bei Änderungen:

```bash
cp ../modul-m298-spacex-ipo-globaler-vergleich.html ./modul.html
# danach Google-Fonts-<link> wieder durch fonts.css ersetzen, falls überschrieben
git add modul.html && git commit -m "Modul M298 aktualisiert" && git push
```

---

© 2026 TheNextGenerationBanking · FinCoach AI · Keine Rechts-, Steuer- oder Anlageberatung ·
SpaceX ist seit 12.06.2026 börsennotiert (SPCX/NASDAQ) — Bewertungs-/Finanzzahlen sind dennoch
medien-/nutzerbasiert und nicht unabhängig verifiziert (Schätzungen) · Datenstand 2026-06-19 · Rechtsstand 2026-06-19
