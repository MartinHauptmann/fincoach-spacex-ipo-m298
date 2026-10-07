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
| `prompts/m300-atas-options-xray-deep-dive-prompt.md` | Deep-Dive-Prime-Prompt M300 (ATAS Options X-Ray, Eurex vs. verbriefte Derivate, § 20 Abs. 6 EStG) mit Faktencheck K1–K12, Compliance-/Qualitäts-Gates und QA-Scorecard |
| `m300.html` | Deep-Dive-Seite M300 im M299-Stil: Faktencheck K1–K12, GEX-/ES-Rechner, Wettbewerbsmatrix, DACH-Vergleich, QA-Scorecard, Live-DBOM-Audit (`provenance/m300.dbom.json`) — Status: Überarbeitung |
| `qa/check_module.py`, `qa/render_audit.cjs` | Pflicht-Prüfskripte vor jeder Veröffentlichung (statisch und Browser in Plain-, Viewer- und 390-px-Fassung) |
| `qa/LESSONS.md` | Fehlerkatalog L01–L10: Symptom, Ursache, Regel, Test, Regressionsnachweis |
| `.claude/skills/fincoach-module-qa/`, `.claude/agents/fincoach-qa-reviewer.md`, `CLAUDE.md` | QA-Skill, unabhängiger Prüf-Agent und Projektregeln für Claude |
| `analysen/m300-qa-report-2026-10-07.md` | QA-Prüfbericht M300 (Lesbarkeitsfehler, Neubewertung aller Gates, Maßnahmen M1–M12) |
| `analysen/m300-atas-options-xray-deep-dive.md` | Ausgeführte Deep-Dive-Analyse M300 (Stichtag 2026-10-05) inkl. Faktencheck, M-DBOM und QA-Scorecard — Status: Überarbeitung |
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
