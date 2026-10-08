---
name: fincoach-module-qa
description: Pflicht-Qualitätssicherung für FinCoach-AI-Module (HTML-Seiten mXXX.html, M-DBOM-JSON, Analysen, Prompts). Verwenden vor JEDER Veröffentlichung, jedem Artifact-Publish, jedem Commit an einer Modulseite und immer, wenn ein QA-Status, Score oder Styleguide-Check gesetzt oder berichtet wird. Enthält die Gates C1–C9, Q1–Q10, die Styleguide-Basis und den Fehlerkatalog L01–L53 mit automatischen Tests.
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
- **L20:** Keine Drittanbieter-CDNs. Bibliotheken liegen in `vendor/` (Chart.js, KaTeX, statisch gebautes Tailwind:
  `sh vendor/build-tailwind.sh`, neue Seiten in `vendor/tailwind.config.cjs` → `content` eintragen).
- **L22:** S01 enthält eine zugängliche Hero-Grafik (`<svg role="img">` mit `<title>` und `<desc>` oder `<img alt>`);
  Schemata sind als „illustrativ, keine Marktdaten“ gekennzeichnet.
- **L23:** `caveat-box` und `info-box` laufen über die volle Inhaltsbreite (kein `max-w-*`).
- **L24:** SVG-Beschriftungen dürfen sich nicht überlappen (Browser-Messung).
- **L09 (offen):** #64748B nicht für Lauftext unter 18,66 px fett verwenden, sobald die Styleguide-Entscheidung M7
  gefallen ist. Bis dahin meldet der Audit dies als WARN.

## 2 · Inhaltsregeln (aus Fehlern gelernt)

- **L04 / C1:** Jede Ausgabeform (Markdown, HTML, Artifact) hat am Anfang **und** am Ende den Beratungsausschluss. Im
  HTML steht er als Kurzfassung im Hero (`data-qa="hero-disclaimer"`), vollständig in der Schlusssektion.
- **L05 / Q4:** `verdict: CONFIRMED` nur bei Primär- oder Herstellerquelle **und** Konfidenz ≥ 0,7. Medienangaben
  erhalten `MEDIA_REPORT`, Primärquellen mit unklarem Bezugszeitraum `UNVERIFIED`, Modellannahmen und Szenarien
  `SCENARIO_PROJECTION`. Andere Verdicts sind unzulässig (L05c). Die KPI-Klasse `confirmed-kpi` steht nur
  auf CONFIRMED-Fakten, alles andere bekommt `scenario-kpi`.
- **L06 / Q9:** Quantor-Aussagen wie „0 von N“, „alle“, „kein Anbieter“ nur über **belegte** Fälle. n. v.-Fälle stehen
  im selben Element.
- **L07 / Q7:** Faktenzahlen nie von Hand schreiben, sondern als `<span data-dbom-count="total|confirmed|media|unverified|scenario|vendor">`.
  Der Live-Audit befüllt sie, der Check vergleicht sie. Das JSON-LD `fact_summary` entspricht der externen DBOM.
- **L08 / Q4:** Jeder DBOM-Fakt ist an mindestens ein Element mit `data-source="FACT_…"` gebunden.
- **L10b:** Jeder Punkt der Liste „Offen vor Freigabe“ trägt `data-gate="Cx|Qx"`. Ein Gate mit offenem Punkt ist nie ✓.
- **L11:** Wertende Vergleichssätze müssen sich aus den Zellen der eigenen Tabelle ableiten lassen.
- **L12:** Jede Zahl mit Einheit oder Prozent hat in der Elternkette `data-source`, `data-est` oder `data-def`
  (Definition/Konvention) oder ein EST-Zeichen im selben Element.
- **L13:** Es gibt eine führende DBOM (extern); die Analyse nutzt deren IDs; Phase-A-Ergebnisse sind auf Seite und
  Analyse identisch.
- **L14:** Die Quellenliste wird aus `dbom.sources` erzeugt; jede Quelle hat ≥ 1 Fakt.
- **L15:** Keine Messwerte von Hand in die QA-Sektion übertragen, sondern auf die Skriptausgabe verweisen.
- **L16:** Bei CONFIRMED müssen der Bezugszeitraum der Quelle und der Claim übereinstimmen (Feld `period`).
- **L17:** Eine gebundene Zahl muss im `claim`, `period` oder `caveat` des gebundenen Fakts stehen.
- **L18:** Die Grundmenge eines Quantors ist einmal definiert; n. v.-Fälle gehören nicht in den Nenner; Seite = Analyse = DBOM.
- **L19:** Zusammengesetzte Claims werden geteilt oder tragen das schwächste Verdict ihrer Teile. CONFIRMED braucht eine
  Primär- oder Herstellerquelle (`tier`) als Hauptbeleg; Sekundärquellen nur als `supporting_sources`. `period` enthält ein Datum.
- **L20 / C9:** Externe Ressourcen self-hosten oder mit Einwilligung und SRI; C9 nur ✓, wenn L20 sauber ist.
- **L21:** Abgeleitete Kennzahlen (Konfidenz-Spannen, Scores) nie von Hand.
- **L25:** Fundstellen, Jahreszahlen und Beträge in K-Tabelle und Modal stehen im Claim der gebundenen Fakten; KPIs binden
  alle Fakten, deren Werte sie zeigen.
- **L26:** Offen-Punkte tragen `data-open`, `data-gate` und ggf. `data-source`; ein dort genannter Fakt ist nie CONFIRMED.
- **L27:** Elemente mit ausschließlich nicht bestätigten Fakten tragen ein sichtbares Badge (MEDIEN, UNGEPRÜFT, SCENARIO).
- **L28:** Keine Pauschalaussagen zum Prüfstatus („geprüft“, „alle Fakten belegt“, „verifiziert“).
- **L29:** `data-def` nur auf Blattelementen.
- **L30:** Verlinkte Pflichtseiten (Impressum, Datenschutz) mit `render_audit.cjs` prüfen; Datenschutztext = gemessene Abrufe.
- **L31:** SVG-Schrift ≥ 11 px in allen Ansichten; Dialoge mit Fokusführung; Canvas mit `role="img"`, `aria-label` und
  Fallback-Text; `prefers-reduced-motion`.
- **L32:** Lizenzdateien für Schriften und Bibliotheken; Versionen vor Release gegen Sicherheitshinweise prüfen.
- **L33:** Ein Test besteht nie über eine leere Menge.
- **L34/L35:** Abgeleitete Werte (Zählungen, Score, Spannen, Pills, Quellen-, Fakten- und Offen-Tabellen der Analyse) nur
  mit `python3 qa/sync_module.py <seite>` schreiben.
- **L36:** Aktenzeichen (z. B. „I R 25/14“, „2 BvL 3/21“) und Normteile ohne § („Satz 6“) stehen im Claim des
  gebundenen Fakts – in Sektionen, K-Tabelle und Modal. Wer einen UNVERIFIED-Teil nennt, bindet auch diesen Fakt.
- **L37:** DBOM-Freitexte (`honest_disclosure` usw.) enthalten keine Überbehauptungen und keinen Score, der von der
  Seite abweicht; am besten gar keinen Score.
- **L38:** Speicher- und Cookie-Angaben im Datenschutztext entsprechen der Messung an allen Modulseiten; „Stand“ ist
  nicht älter als die letzte Änderung der Datei (Audit der Datenschutzseite, derzeit WARN).
- **L39:** Quellen mit `tier=internal` tragen nur UNVERIFIED (Konfidenz ≤ 0,6) oder SCENARIO_PROJECTION; die interne
  Quelle muss zum Claim passen (Modell ≠ Fachableitung ≠ Nutzertext).
- **L40:** Jedes ◐/✗-Gate und jeder UNVERIFIED-Fakt hat einen Offen-Punkt mit `data-gate` (und `data-source`) als
  Abschlusskriterium.
- **L41 / Q10:** Fachbegriffe beim ersten Auftreten in `<dfn>` mit sichtbarer Erklärung (Liste `qa/fachbegriffe.json`,
  neue Begriffe dort ergänzen). Fundstellen in Glossar-Einträgen (`data-def`) sind an Fakten gebunden (5. Feld in `GLOSSAR`).
- **L41b:** Gewertet wird das erste *sichtbare* Vorkommen. Jede sichtbare Großbuchstaben-Abkürzung steht in
  `qa/fachbegriffe.json`: unter `terms` (wird erklärt, `<dfn>` oder `<abbr title>`) oder unter `known` (Eigenname,
  Produktcode, Normkürzel, UI-Label). Neue Abkürzung → bewusst einordnen.
- **L26b:** Nennt ein Offen-Punkt eine Fundstelle aus einem Fakt, bindet er diesen Fakt (`data-source`); der Fakt ist dann
  nicht CONFIRMED (L26). Teilaussagen mit offenem Punkt werden als eigener Fakt abgetrennt.
- **L36b:** Normteile ohne § („S. 5“, „Sätze“, „Abs. 3“, „Nr. 387“) zählen wie Fundstellen; `data-def` befreit keine
  Fundstelle von der Faktbindung.
- **L42 / C1:** Jeder Disclaimer (Hero, Schluss, Analyse Anfang und Ende) enthält alle C1-Pflichtbestandteile:
  Beratungsausschluss, allgemeine Information, Totalverlust, Hebel, Knock-out, Eignung nur für erfahrene Anleger.
- **L43:** Daten, Paragraphen und Aktenzeichen der Analyse stehen in einem DBOM-Fakt; unbelegte Angaben entfernen.
- **L44:** Die Version steht nur in der DBOM; `sync_module.py` überträgt sie.
- **L45:** Das Live-Audit-Banner zeigt keine Warnung (Browser-Audit liest es aus).
- **L46:** Wird eine Teilaussage als eigener Fakt abgetrennt, bekommt er Leitphrasen (`markers`). Jedes Element mit
  Leitphrase bindet diesen Fakt (und zeigt sein Badge).
- **L47 / Q9:** Starke Rechtsbewertungen („voraussichtlich nicht vereinbar“, „verfassungswidrig“ …) nur, wenn der Claim sie
  wörtlich trägt. Manuell: Modalität jedes Rechtssatzes (Zweifel / Vorlage / Entscheidung) gegen den Claim lesen.
- **L48:** Konfidenzen in der Analyse nur als „(`FACT_…`, …, Konfidenz x,y)“; der Wert kommt per Sync aus der DBOM.
- **L49:** Die QA-Scorecard der Analyse (Abschnitt 8) erzeugt `sync_module.py` aus den Gate-Zellen.
- **L50:** Jeder neue Test wird vor dem Commit mit mindestens einer Umgehung (Verneinung, Markup, anderer Ort) gegengeprüft.
- **L51:** Kennzeichnungsregeln gelten auch für die Analyse: Absatz/Zeile mit Leitphrase nennt den Fakt.
- **L48b / L05d:** In der Analyse keine Hand-Konfidenzen und keine Provenienzkürzel; Angaben als
  „(`FACT_…`, belegt|Medienangabe|ungeprüft|SCENARIO_PROJECTION, Konfidenz x,y)“ – Label und Wert aus der DBOM.
- **L52:** Phrasentests normalisieren den Text (Markup, Leerraum, Groß-/Kleinschreibung) und vergleichen zeilenweise.
- **L53:** Die Analyse ist eine faktgebundene Kurzfassung. Phase A, Module 1–8 und Glossar stehen in
  `<!-- sync:… -->`-Blöcken und werden nur von `sync_module.py` geschrieben (Modulzuordnung: `analysis_modules` in der
  DBOM). Handtext (Kurzfazit, Modellrechnung, Disclaimer) nennt bei jeder Angabe eine Fakt-ID.
- **L03:** Der QA-Score wird aus den Gate-Zellen berechnet (`data-qa-score`, `data-qa-points`). Freigabe nur, wenn
  alle C-Gates ✓ sind und der Score ≥ 90 % liegt; sonst ÜBERARBEITUNG.

## 3 · Gates (aus dem Modul-Prompt, Kurzfassung)

C1 Disclaimer Anfang+Ende · C2 keine Anlageempfehlung (MAR) · C3 Steuer/Recht mit Stichtag+Primärquelle ·
C4 Neutralität/Interessenkonflikte · C5 Marken · C6 UWG · C7 Risikodarstellung · C8 Regulatorik belegt · C9 Datenschutz ·
Q1 Faktencheck vollständig · Q2 Aktualität · Q3 Mathematik · Q4 Provenienz · Q5 Quellenqualität · Q6 Vollständigkeit ·
Q7 Widerspruchsfreiheit · Q8 Glossar · Q9 keine Überzeichnung/Halluzination · Q10 Format

## 4 · Ablauf vor jeder Veröffentlichung (Pflicht)

0. **Synchronisieren:** `python3 qa/sync_module.py mXXX.html` (abgeleitete Werte aus DBOM und Gate-Zellen)
1. **Statische Prüfung:** `python3 qa/check_module.py mXXX.html` → muss mit Exit 0 enden
2. **Browser-Audit in allen Zielumgebungen:** `node qa/render_audit.cjs mXXX.html [--vendor DIR]` → Exit 0. Er prüft
   Plain, Viewer und 390 px.
   Für selbst gehostete Seiten (L20) ohne weitere Optionen; `--vendor DIR` nur noch für Altseiten mit CDN-Einbindung.
   Der Audit prüft zusätzlich Laufzeit-Abrufe an Dritte, lokale Dateien, Formeln, Diagramme und SVG-Überlappungen.
3. **Manuelle Pflichtpunkte**, die kein Skript prüfen kann. Jeden einzeln abhaken und im Bericht nennen:
   - [ ] Jede Allaussage gegen die Quelltabelle gelesen (L06)
   - [ ] Formeln nachgerechnet und Zahlenbeispiel mit Probe (Q3)
   - [ ] Screenshots Viewer-Fassung der Sektionen mit Tabellen, Formeln und Diagrammen angesehen
   - [ ] Rechtsstand-Aussagen mit Stichtag und Fundstelle (C3)
   - [ ] Jeder Wertungssatz gegen seine Tabelle gelesen (L11)
   - [ ] Bezugszeitraum jeder CONFIRMED-Quelle = Zeitraum im Claim (L16)
   - [ ] Phase-A-Ergebnisse Seite = Analyse (L13)
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
