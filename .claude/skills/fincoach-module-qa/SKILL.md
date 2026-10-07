---
name: fincoach-module-qa
description: Pflicht-Qualitätssicherung für FinCoach-AI-Module (HTML-Seiten mXXX.html, M-DBOM-JSON, Analysen, Prompts). Verwenden vor JEDER Veröffentlichung, jedem Artifact-Publish, jedem Commit an einer Modulseite und immer, wenn ein QA-Status, Score oder Styleguide-Check gesetzt oder berichtet wird. Enthält die Gates C1–C9, Q1–Q10, die Styleguide-Basis und den Fehlerkatalog L01–L10 mit automatischen Tests.
---

# FinCoach-AI · Modul-QA

Dieser Skill ist die verbindliche Prüfprozedur. Er bündelt den Styleguide, die Gates aus dem Modul-Prompt und alle
Lehren aus dem Fehlerkatalog `qa/LESSONS.md`. **Grundsatz (L10): Kein ✓ ohne Messung.** Ein Status, der nicht durch
einen Testlauf oder eine dokumentierte Einzelprüfung belegt ist, ist ◐.

## 1 · Styleguide-Basis (TNGB) – nicht verhandelbar

- **Farbtokens:** bg #0A0F1A · card #121A2E · border #1E293B · cyan #00CFFF · emerald #00CC7A · magenta #E6399A ·
  orange #FF6B00 · lavender #9933FF · gold #DFAF0F · indigo #4472C4 · muted #64748B
- **Text:** Basis #E2E8F0 · Überschriften #F1F5F9 · Fließtext sekundär #CBD5E1 / #94A3B8 · Diagrammtext #94A3B8
- **Schriften (self-hosted, `fonts.css`):** Inter (Text), Space Grotesk (Überschriften), JetBrains Mono (Daten/Code)
- **L01:** Basisfarbe, Schrift und Größe stehen auf `html` **und** `body`:
  `body{background:var(--bg);color:#E2E8F0;font-family:'Inter',system-ui,sans-serif;font-size:1rem;}`
  Grund: Einbettungen wie Artifact-Viewer, iFrame oder CMS setzen eigene `body`-Regeln, die die Vererbung von `html`
  überschreiben.
- **L02:** `Chart.defaults.color='#94A3B8'` vor dem ersten `new Chart(...)`
- **L09 (offen):** #64748B nicht für Lauftext unter 18,66 px fett verwenden, sobald die Styleguide-Entscheidung M7
  gefallen ist. Bis dahin meldet der Audit dies als WARN.

## 2 · Inhaltsregeln (aus Fehlern gelernt)

- **L04 / C1:** Jede Ausgabeform (Markdown, HTML, Artifact) hat am Anfang **und** am Ende den Beratungsausschluss. Im
  HTML steht er als Kurzfassung im Hero (`data-qa="hero-disclaimer"`), vollständig in der Schlusssektion.
- **L05 / Q4:** `verdict: CONFIRMED` nur bei Primär- oder Herstellerquelle **und** Konfidenz ≥ 0,7. Medienangaben
  erhalten `MEDIA_REPORT`, Modellannahmen und Szenarien `SCENARIO_PROJECTION`. Die KPI-Klasse `confirmed-kpi` steht nur
  auf CONFIRMED-Fakten, alles andere bekommt `scenario-kpi`.
- **L06 / Q9:** Quantor-Aussagen wie „0 von N“, „alle“, „kein Anbieter“ nur über **belegte** Fälle. n. v.-Fälle stehen
  im selben Element.
- **L07 / Q7:** Faktenzahlen nie von Hand schreiben, sondern als `<span data-dbom-count="total|confirmed|media|scenario|vendor">`.
  Der Live-Audit befüllt sie, der Check vergleicht sie. Das JSON-LD `fact_summary` entspricht der externen DBOM.
- **L08 / Q4:** Jeder DBOM-Fakt ist an mindestens ein Element mit `data-source="FACT_…"` gebunden.
- **L03:** Der QA-Score wird aus den Gate-Zellen berechnet (`data-qa-score`, `data-qa-points`). Freigabe nur, wenn
  alle C-Gates ✓ sind und der Score ≥ 90 % liegt; sonst ÜBERARBEITUNG.

## 3 · Gates (aus dem Modul-Prompt, Kurzfassung)

C1 Disclaimer Anfang+Ende · C2 keine Anlageempfehlung (MAR) · C3 Steuer/Recht mit Stichtag+Primärquelle ·
C4 Neutralität/Interessenkonflikte · C5 Marken · C6 UWG · C7 Risikodarstellung · C8 Regulatorik belegt · C9 Datenschutz ·
Q1 Faktencheck vollständig · Q2 Aktualität · Q3 Mathematik · Q4 Provenienz · Q5 Quellenqualität · Q6 Vollständigkeit ·
Q7 Widerspruchsfreiheit · Q8 Glossar · Q9 keine Überzeichnung/Halluzination · Q10 Format

## 4 · Ablauf vor jeder Veröffentlichung (Pflicht)

1. **Statische Prüfung:** `python3 qa/check_module.py mXXX.html` → muss mit Exit 0 enden
2. **Browser-Audit in allen Zielumgebungen:** `node qa/render_audit.cjs mXXX.html [--vendor DIR]` → Exit 0. Er prüft
   Plain, Viewer und 390 px.
   Ohne CDN-Zugriff `--vendor` mit lokalen Kopien von chart.umd.js, katex.min.js, auto-render.min.js, katex.min.css und
   einem mit der Seiten-Konfiguration kompilierten Tailwind-v3-CSS (tw.css).
3. **Manuelle Pflichtpunkte**, die kein Skript prüfen kann. Jeden einzeln abhaken und im Bericht nennen:
   - [ ] Jede Allaussage gegen die Quelltabelle gelesen (L06)
   - [ ] Formeln nachgerechnet und Zahlenbeispiel mit Probe (Q3)
   - [ ] Screenshots Viewer-Fassung der Sektionen mit Tabellen, Formeln und Diagrammen angesehen
   - [ ] Rechtsstand-Aussagen mit Stichtag und Fundstelle (C3)
4. **Gates bewerten:** Nur Gates mit belegtem Testlauf oder dokumentierter Einzelprüfung dürfen ✓ sein (L10). Die
   Testausgaben von Schritt 1 und 2 gehören wörtlich in den QA-Bericht oder die Commit-Nachricht.
5. **Neuer Fehler gefunden?** → Abschnitt 5.

## 5 · Aus Fehlern lernen (Pflicht bei jedem neuen Befund)

1. Eintrag in `qa/LESSONS.md` mit nächster L-Nummer: Symptom, **Ursache** (nicht nur Symptom), Regel
2. Regel hier in Abschnitt 1 oder 2 ergänzen, bei inhaltlichen Regeln auch im Modul-Prompt (`prompts/…`, Gate-Text)
3. Test in `qa/check_module.py` oder `qa/render_audit.cjs` mit derselben L-Nummer im Regelnamen
4. **Regressionsnachweis:** Test gegen die fehlerhafte Version (`git show <commit>:datei`) → muss fehlschlagen;
   gegen die korrigierte Version → muss bestehen. Beide Ergebnisse in die Spalte „Regression“ eintragen.
5. Altmodule mit dem neuen Test prüfen und Befunde in `qa/LESSONS.md` unter „Offene Befunde in Altmodulen“ eintragen.

## 6 · Unabhängige Zweitprüfung

Vor einer Freigabe (Status FREIGABE oder öffentliches Teilen) den Agenten `fincoach-qa-reviewer` starten. Er prüft
ohne Kenntnis der Erstellung gegen diesen Skill und berichtet Befunde. Er korrigiert nicht selbst.
