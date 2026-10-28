---
name: fincoach-module-qa
description: Pflicht-Qualitätssicherung für FinCoach-AI-Module (HTML-Seiten mXXX.html, M-DBOM-JSON, Analysen, Prompts). Verwenden vor JEDER Veröffentlichung, jedem Artifact-Publish, jedem Commit an einer Modulseite und immer, wenn ein QA-Status, Score oder Styleguide-Check gesetzt oder berichtet wird. Enthält die Gates C1–C9, Q1–Q10, die Styleguide-Basis und den Fehlerkatalog L01–L87 mit automatischen Tests.
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
  nicht älter als die letzte Änderung der Datei (Audit der Datenschutzseite, BLOCKER seit 2026-10-11).
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
- **L53b:** Erzeugte Blöcke nie von Hand ändern; der Check erzeugt sie mit `sync_module.build_blocks()` neu und vergleicht
  byte-genau. Jede `FACT_…` in der Analyse existiert in der DBOM.
- **L54:** Keine Beleggrad-Aussagen in Handtext (auch nicht in `analysis_modules[].note`); Modul 8 kommt aus dem Fazit der Seite.
- **L55:** Folgeaussagen eines ungeprüften Fakts („erledigt“, „Altjahre“) binden diesen Fakt (Leitphrasen in `markers`).
- **L56:** Angaben in der Analyse müssen im Fakt desselben Absatzes bzw. derselben Tabellenzeile stehen.
- **L57:** „belegt/bestätigt“ nur, wenn ein CONFIRMED-Fakt gebunden ist.
- **L58:** Seitensektionen heißen in der Analyse „Modulseite Sxx“; `Sxx` allein ist dort eine Quelle.
- **L59:** Die Analyse enthält alle Abschnitte 0–9 der Ausgabestruktur des Prompts, die Claim-Tabelle aus `source_claims`.
- **Eigenständigkeit:** Ein Modul verweist nicht auf unveröffentlichte Module und vergleicht sich nicht mit eigenen früheren
  Fassungen; der Verlauf steht nur im `audit_trail` der DBOM und in `qa/LESSONS.md`.
- **L60:** Eigenständigkeit wird geprüft: keine fremden Modul-IDs, Links, „Vormodul“, „frühere Fassung“.
- **L61:** Claim-Ergebnis ✓/✗ nur mit CONFIRMED-Beleg; gleiche Aussage = gleiches Ergebnis wie die K-Zeile (`k`).
- **L62:** Jeder Fazit-Punkt ist als EINSCHÄTZUNG (Badge) oder als Faktwiedergabe (`data-assessment="fact"`) eingeordnet;
  Szenarien stehen im Konjunktiv.
- **L63:** Konstanten eines Fakts (`values`) sind überall gleich und gebunden, auch in Formeln, Labels und Glossar.
- **L27b:** Glossar-Einträge mit nicht bestätigtem Fakt tragen das Badge des schwächsten Verdicts (6. Feld).
- **L06b:** „Alleinstellung“/„einzige(r)“ nur mit Vergleichsbasis und n. v.-Hinweis.
- **L64:** Nur geltendes Recht am Stichtag; frühere Rechtslagen, Übergangsregeln und überholte Grenzbeträge werden nicht
  dargestellt. Geprüft wird normalisiert (inkl. „a.F.“, Markup), in Seite samt JS und Attributen, Analyse, DBOM und
  Prompt (L67).
- **L88:** Belegdateien Dritter (Bildschirmkopien) nie committen (`provenance/evidence/` in `.gitignore`); nur Werte
  und SHA-256 an der Quelle. **L53e:** Abgleichsdaten nur aus `verified.by = Herausgeber`. **L84b:** Marken-Hinweis
  auch in der Analyse vollständig. **L14b:** Quellennummern eindeutig. **L82i:** Abgleichssätze mit „ausgenommen“ nennen
  alle Ausnahmen.
- **L18f:** Jeder Quantor nennt in `basis.rule` seine Bestimmbarkeitsregel; sie gilt für alle Anbieter gleich, und
  die Gegenstandszeile der Matrix trägt `data-quantor-row`. **L76f:** Ausschlussaussagen über Anbieter („bietet keine …“)
  nur mit Gegenstand im Claim. **L82j:** Ausnahmen tragen `exception_label`; alle Transparenztexte (auch ausgeblendete)
  nennen dieselbe Ausnahmeliste. **L53f:** Herausgeber-Prüfdaten nur aus `publisher_checks`.
- **L65:** K-Bereiche „K1–Kn“ und jeder Verweis „Kn“ passen zur Zahl der K-Zeilen, in Seite, Analyse und Prompt. Zahlangaben „n (ausgewählte) Kernaussagen“ gelten auch mit bis zu drei Adjektiven oder Adverbien dazwischen, flektiert und mit Komma (L65c).
- **L66:** Nach jeder Entfernung Folgetexte suchen: Titel, Attribute, Datenherkunft (nur Stellen aus den Quellen) und
  Fazit; jeder Fazit-Punkt unter „Relativiert“/„Entfällt“ nennt seinen Claim (`data-claim`).
- **L68:** Eigenständigkeit gilt auch für JS-Strings und Links mit Anker (`m299.html#…`) und Wörter wie „Vorversion“.
- **L69:** Ein Claim, der Belege mit einer K-Zeile teilt, braucht `k` oder eine Begründung `k_differs`; ◐/Szenario
  nur mit Belegen.
- **L70:** Wertende Wörter im Fazit (besser, Merkmal, empfohlen, leider …) verlangen EINSCHÄTZUNG; Vergleichswörter
  (Vorteil, Nachteil, stark, schwach) zusätzlich eine Claim-Bindung. Vorschläge stehen im Konjunktiv an FACT_ROADMAP.
- **L71:** Faktkonstanten werden auch in Formen wie „SPX-Multiplikator 1000“ und „Multiplikator (ES) 50“ geprüft.
- **L72:** Alleinstellungs-Aussagen (einzigartig, einziger, nur X) brauchen die Vergleichsbasis im selben Satz, auch in
  der JS-K-Tabelle.
- **L27c:** Glossar-Einträge ohne Fakt enthalten keine Tatsachenmerkmale (Institution, Norm, Rechtsnatur, Pflicht).
- **L74:** Footer-Datum und Version kommen per Sync aus der DBOM (`audit_trail`); Prompt-Schweregrade = K-Tabelle.
- **L75:** Jede nicht bestätigte Angabe wird belegt oder gestrichen; was bleibt, trägt in der DBOM ein `keep_reason`.
- **L76:** Jede Zahl und jede Rechtsfolge in einem gebundenen Element steht im Claim des Fakts (z. B. keine
  „Betragsgrenze“, wenn der Fakt sie nicht nennt); Gegensätze zur früheren Rechtslage sind L64-Reste.
- **L77:** Fakt-IDs in DBOM-Freitexten (honest_disclosure, caveat, keep_reason) existieren.
- **L78:** Bezugszeiträume (`period`) liegen am oder vor dem Stichtag; ein späterer Abruf wird als „abgerufen …“
  genannt. Der Abrufzeitraum in Freitexten umfasst den spätesten Abruf.
- **L78b:** Eine datierte Momentaufnahme nach dem Stichtag (z. B. ein vom Herausgeber geliefertes Fallbeispiel) ist nur
  zulässig mit `after_stichtag` (Begründung) im Fakt und dem sichtbaren Hinweis „nach dem Stichtag“ am gebundenen
  Element. Der Stichtag des Moduls wird dafür nicht verschoben.
  Verschärft (L78c): nur VENDOR_CLAIM, MARKET_DATA oder DERIVED mit Zeitstempel (Datum und Uhrzeit) im `period`; die
  Begründung nennt Datum, Momentaufnahme/Fallbeispiel und Stichtag; jede Bindung liegt in einem Block mit
  `data-snapshot`, der den Hinweis „Momentaufnahme nach dem Stichtag“ schlicht sichtbar trägt (kein `style`, kein
  zugeklapptes `details`, nicht verneint, nicht zitiert), oder trägt ihn selbst; die Analyse kennzeichnet die
  Momentaufnahme. Belegstufe einer Bildschirmkopie ist `screenshot` (L82g) mit SHA-256 der Bilddatei an der Quelle;
  die Bilddatei selbst wird nicht veröffentlicht.
- **L79:** Elemente, die nur an Herstellerangaben (VENDOR_CLAIM) gebunden sind, tragen das VENDOR-Kennzeichen.
- **L65b/L68b:** Bereichsangaben „A01–Ann“ passen zur Claim-Tabelle; Tooltips und Offen-Liste beschreiben den
  Zielzustand, nicht den Bearbeitungsverlauf („entfernt“, „angeglichen“, „überarbeitet“, „nach dem Review“).
- **L26c:** Ein Offen-Punkt, der Kontraktdaten oder Fakt-Konstanten nennt, bindet die Fakten (`data-source`); dann
  greift L26 und die Fakten sind nicht CONFIRMED. Allgemeine Volltext-Abgleiche stehen als allgemeiner Offen-Punkt.
- **L80:** Testhärtung wird gegen die Umgehungen der Zweitprüfung und gegen ungesehene Holdout-Fälle nachgewiesen, nie
  nur gegen selbst gewählte Injektionen. Begründungsfelder (`keep_reason`, `k_differs`) brauchen Inhalt und Bezug.
- **L26d:** Ein CONFIRMED-Fakt nennt in caveat oder keep_reason keinen offenen Abgleich. Fakt-spezifische Zweifel
  senken das Verdict; der allgemeine Volltextabgleich aller Snippet-Belege steht als allgemeiner Offen-Punkt.
- **L76b:** Claims verweisen nie auf die Seite („Matrix“, „Tabelle“). Ein Vergleichs-Claim nennt die Werte je
  Anbieter; Zahlen einer Matrixzelle stehen im Claim-Abschnitt ihres Anbieters.
- **L19b:** Quellenstufe `vendor` nur für den Hersteller des beschriebenen Produkts; Rechtsrahmen nie mit vendor-Quelle.
- **L81:** EINSCHÄTZUNG kennzeichnet Wertungen, nicht unbelegte Tatsachen. SCENARIO-Fließtext steht Satz für Satz im
  Konjunktiv.
- **L82:** Jeder Fakt trägt `evidence` (snippet/fulltext/model). Seite und honest_disclosure erklären „belegt
  (Snippet)“; solange Snippet-Belege bestehen, bleiben C3, Q2, Q4 und Q5 ◐.
- **L26e:** Ein Offen-Punkt, der eine Sektion „Sxx“ nennt, trägt `data-source` mit den betroffenen Fakten.
- **L27d:** Gebundene Glossar-Einträge enthalten nur Zahlen, Daten und Rechtsfolgen aus dem Claim.
- **L83:** Kennzeichen zählen nur sichtbar; Zeitangaben brauchen eine Bindung; Matrix-Textzellen stehen im
  Claim-Abschnitt ihres Anbieters. Wortlisten werden nicht weiter ausgebaut; Formulierungsvarianten deckt die
  manuelle Zweitprüfung ab.
- **L27e:** Kein Verdict-Kennzeichen ist schwächer als das Verdict der gebundenen Fakten (nach Hochstufung entfernen).
- **L82b:** Bei Belegstufe `fulltext` keine Snippet-Reste in caveat, keep_reason, honest_disclosure oder Analyse.
- **L76d:** Einschränkungen eines Fakts (`qualifier`: Beta, Erprobung, in Entwicklung) erscheinen überall, wo sein
  Gegenstand genannt wird.
- **L84:** Marken-Inventar `marks` in `qa/fachbegriffe.json` pflegen; jede vorkommende Inventar-Marke steht im
  Markenhinweis.
- **L80b:** Nach jeder Änderung alle Regressionsdateien laufen lassen
  (`python3 qa/run_regression.py qa/regression/*.json`); ANKER FEHLT ist ein Fehler.
- **L82c:** Der Freigabeumfang (`verified.scope`) passt zum caveat; „mehrere/übereinstimmende Berichte“ nur mit
  mindestens zwei Quellen.
- **L38b:** Impressum und Datenschutz ohne Entwurfsvermerke; jedes Datum ≥ letzte Änderung; CDN-Angaben = genutzte
  CDN-Hosts aller Seiten.
- **L03c:** Der Freigabestatus kommt aus `module.release_status`; Seite, JSON-LD, Analyse-Kopf und §8 stimmen exakt
  überein. FREIGABE erst nach Pflicht-Zweitprüfung und Zustimmung des Herausgebers.
- **L85:** Vergleichsfakten je Anbieter; gleiche Quellenstufe ⇒ gleiches Verdict.
- **L76e:** Ein Claim mit Beta, Erprobung oder „in Entwicklung“ trägt ein `qualifier`-Feld.
- **L19c:** Rechtsrahmen-Fakten stützen sich auf eine Primärquelle.
- **Bekannte Grenzen:** Regressionsfälle mit `known_limit` (vom Herausgeber anerkannt) erscheinen als [GRENZE] und
  zählen nicht als Fehler; sie werden nie still entfernt.
- **L27f:** Pauschale Verdict-Wörter („Medienangaben“, „ungeprüft“) nur, wenn alle gebundenen Fakten dieses Verdict
  tragen; sonst je Fakt („Volland: Medienangabe“).
- **L86:** Szenarien tragen keine Konfidenz (`confidence: null`) und erscheinen in keiner Konfidenzanzeige.
- **L85b:** Gleiche Maßstäbe über alle Bindungen einer Vergleichstabelle (Quantor-Fakten mit `basis` ausgenommen).
- **L27g:** Kein pauschales MEDIEN/UNGEPRÜFT über Fakten verschiedener Verdicts: Jedes Kennzeichen und jedes
  Verdict-Wort steht in der Teilaussage seines Gegenstands und nennt keinen Anbieter anderen Verdicts; jede Teilaussage
  über einen Medien-Fakt trägt ihr Kennzeichen.
- **L27h:** Die Kennzeichen-Legende nennt jedes verwendete Kennzeichen; reine Modellannahmen tragen MODELL, nie SCENARIO.
- **L87:** Nicht ausgewertete Gegenstände stehen in der DBOM unter `not_evaluated`; jede Aussage dazu (Glossar,
  Tabellen, Modale, Fließtext, Analyse) nennt „n. v.“ direkt beim Gegenstand oder bindet einen Fakt, der ihn trägt.
- **L82d:** Ausnahmen im Prüfumfang stehen in jedem Satz, der Vollständigkeit am Original oder auf Stufe Volltext
  behauptet (auch „sämtliche“, „jeder Beleg“, Tooltips), mit Namen und Ausnahmewort.
- **L03d:** „Entwurf“ steht sichtbar im Footer (nicht als Kommentar oder versteckt), solange der Status nicht FREIGABE ist.
- **L18b:** Ein Quantor zählt einen Anbieter nur als bestimmbar, wenn dessen eigener Fakt den Gegenstand nennt
  (`basis.determinable_from`, `basis.subject`). Sonst gilt n. v. – auch in Matrix, KPI, Fazit und Analyse.
- **L82e:** Belegstufe `fulltext` nur bei Prüfung am Original; nur Medienbericht oder Studie nicht eingesehen ⇒ `secondary`.
- **L12c:** Jede Datenzelle einer Vergleichstabelle bindet einen Fakt oder ist vollständig „n. v.“.
- **L50d (Rolle der Tests):** Die Prüfskripte sind Rückfallschutz und Strukturprüfung (Bindung, Sichtbarkeit,
  DBOM-Felder, Zählungen). Für inhaltliche Gates (C4 Neutralität, Q4 Provenienz, Q7 Widerspruchsfreiheit, Q9
  Überzeichnung) ist ein grüner Test keine Messung: ✓ nur nach Zweitprüfung und Sichtprüfung des Herausgebers,
  Tooltip nennt diese, nicht „gemessen mit L…“. Formulierungsvarianten, die nur eine Wortliste fangen könnte,
  werden mit Zustimmung des Herausgebers als `known_limit` geführt, nie still entfernt.
- **L18c:** Ein abgeleiteter Quantor trägt das Verdict seiner Basisfakten und die Belegstufe `derived`; Angaben
  Dritter (z. B. ein Anbieter außerhalb des Vergleichsfelds) stehen in einem eigenen Fakt.
- **L82f:** Hauptquelle der Stufe secondary ⇒ Belegstufe `secondary`.
- **L50c (Testhärte):** Neue Tests prüfen Teilaussagen, alle Fundorte und sichtbaren Text, nicht nur die gemeldete
  Stelle. Vor jeder Teständerung schreibt ein eigener Agent einen Holdout, der zuerst committet wird; die
  Erstmessung nach der Härtung wird berichtet, auch wenn später nachgeschärft wird.
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
2b. **Regressionslauf (L80):** `python3 qa/run_regression.py qa/regression/mXXX-bypasses.json` und
   `… mXXX-holdout.json` → Exit 0. Jeder Fall muss vom *zuständigen* Test erkannt werden, nicht zufällig von einem
   anderen. Umgehungen aus jeder Zweitprüfung werden als Fälle in `mXXX-bypasses.json` übernommen; neue Holdout-Fälle
   werden von einem separaten Agenten **ohne Einsicht in die Testskripte** geschrieben, in einem eigenen Commit **vor**
   der Teständerung abgelegt, genau einmal gemessen und mit diesem Ergebnis berichtet. Negativkontrollen
   (`expect: NONE`) gehören in jeden Satz. Fälle, die Text der Analyse-Spiegel ändern, laufen mit `sync: true`.
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
