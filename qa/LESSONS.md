# FinCoach AI · Fehlerkatalog (Lessons Learned)

> L10b–L16 stammen aus der unabhängigen Zweitprüfung durch den Agenten `fincoach-qa-reviewer` am 2026-10-07.
> Sie belegen, dass die Zweitprüfung Fehlerklassen findet, die die automatischen Tests noch nicht kannten.

Jeder Fehler, der eine Veröffentlichung erreicht hat oder im Review gefunden wurde, bekommt hier eine **L-Nummer**.
Ein Eintrag gilt erst als abgeschlossen, wenn drei Dinge existieren:

1. **Regel:** eine verbindliche Anweisung in `.claude/skills/fincoach-module-qa/SKILL.md` und, wenn inhaltlich, im
   Modul-Prompt unter `prompts/`
2. **Automatischer Test:** in `qa/check_module.py` (statisch) oder `qa/render_audit.cjs` (Browser) mit derselben L-Nummer
3. **Regressionsnachweis:** Der Test schlägt auf der fehlerhaften Version fehl und besteht auf der korrigierten

Ein Fehler, für den sich kein Test schreiben lässt, bekommt einen Pflichtpunkt in der manuellen Checkliste des Skills
(Kennzeichnung „manuell“).

---

| L | Datum | Modul | Fehler (Symptom) | Ursache | Regel | Test | Regression |
|---|---|---|---|---|---|---|---|
| L01 | 2026-10-07 | M300 | Tabellen, Formeln und Rechner im Artifact-Viewer fast schwarz auf Dunkelblau (305 Elemente, Kontrast ~1,1 : 1); Schrift fiel auf Systemschrift mit 14 px zurück | Styleguide-Basis nur auf `html`; die Einbettung setzt `body{color:#141413;font:14px …}`, das schlägt die Vererbung | Basisfarbe #E2E8F0, Inter und 1rem **zusätzlich auf `body`**; jede Seite in **Plain- und Viewer-Fassung** testen | `check_module` L01 · `render_audit` L01 (Fremdfarben, body-Basis, viewer = plain) | c56f4d5: ✗ 305 Elemente · cbe8e5b: ✓ |
| L02 | 2026-10-07 | M300 | Chart.js-Standardtextfarbe #666 (≈ 3 : 1 auf Karte) | Nur Achsen explizit gefärbt, Default nicht gesetzt | `Chart.defaults.color='#94A3B8'` vor dem ersten Diagramm | `check_module` L02 · `render_audit` L02 | c56f4d5: ✗ · cbe8e5b: ✓ |
| L03 | 2026-10-07 | M300 | QA-Score 89,5 % angezeigt, tatsächlich 81,6 % | Score als fester Text geschrieben, Gates nicht erneut bewertet | Score **aus den Gate-Zellen berechnen** (`data-qa-score`); Freigaberegel maschinell ableiten | `check_module` L03, L03b | c56f4d5: ✗ nicht gebunden · v1.0.1: ✓ |
| L04 | 2026-10-07 | M300 | Kein Beratungsausschluss am Seitenanfang (Gate C1) | C1 nur an der Markdown-Analyse geprüft, nicht an der HTML-Ausgabe | C1 gilt **für jede Ausgabeform**; Kurz-Disclaimer im Hero mit `data-qa="hero-disclaimer"` | `check_module` L04 | c56f4d5: ✗ · v1.0.1: ✓ |
| L05 | 2026-10-07 | M300 | Medienangabe (Konf. 0,60) als „belegt“ gezählt und grün umrandet | Verdict CONFIRMED vergeben, ohne Klasse/Konfidenz abzugleichen | CONFIRMED nur bei Primär- oder Herstellerquelle und Konfidenz ≥ 0,7; `confirmed-kpi` nur für CONFIRMED | `check_module` L05, L05b | c56f4d5: ✗ · v1.0.1: ✓ |
| L06 | 2026-10-07 | M300 | KPI „0 von 6“, obwohl ein Feld „n. v.“ war | Allaussage aus unvollständiger Matrix | Quantor-Aussagen (0 von N, alle, kein) nur über belegte Fälle; n. v.-Fälle im KPI nennen | `check_module` L06 (WARN) + manuell | c56f4d5: ! · v1.0.1: ✓ |
| L07 | 2026-10-07 | M300 | „6 Herstellerangaben“ im Text, 5 in der DBOM | Zahlen von Hand in den Text geschrieben | Faktenzahlen nur über `data-dbom-count` (vom Live-Audit befüllt, vom Check verglichen); JSON-LD = DBOM | `check_module` L07, L07b, L07c | c56f4d5: ✗ · v1.0.1: ✓ |
| L08 | 2026-10-07 | M300 | K5-Fakt ohne Seitenbindung, vom Live-Audit nicht prüfbar | Fakten in DBOM angelegt, Bindung vergessen | Jeder DBOM-Fakt hat mindestens ein Element mit `data-source` | `check_module` L08a, L08b | c56f4d5: ✗ · v1.0.1: ✓ |
| L09 | 2026-10-07 | alle | Styleguide-Tokens #64748B, #E6399A, #9933FF unter WCAG AA (125–129 Elemente) | Token-Definition, nicht Umsetzung | **Offen (Styleguide-Entscheidung M7):** bis dahin als WARN gemeldet, nicht blockierend | `render_audit` L09 (WARN) | – |
| L10 | 2026-10-07 | Prozess | Styleguide-Check auf ✓ gesetzt, ohne in der Zielumgebung gemessen zu haben | Test nur in einer Umgebung; Check „behauptet“ statt gemessen | Kein ✓ ohne Messung. Ein Gate gilt erst als bestanden, wenn `check_module.py` **und** `render_audit.cjs` mit Exit 0 laufen; die Ausgabe gehört in den Bericht | Skill-Pflicht (Schritt 4) | – |

| L10b | 2026-10-07 | M300 | Nach M2–M6 standen C4, Q2, Q4 und Q7 auf ✓, obwohl Offen-Punkte und Widersprüche bestanden (Zweitprüfung: 78,9 % statt 89,5 %) | Gates einzeln „abgehakt“, ohne Abgleich mit der eigenen Offen-Liste | Offen-Punkte tragen `data-gate`; ein Gate mit Offen-Punkt darf nicht ✓ sein | `check_module` L10b | v1.0.1 mit `data-gate`, C4 auf ✓ gesetzt: ✗ · v1.0.2: ✓ |
| L11 | 2026-10-07 | M300 | Fließtext „SpotGamma und Volland stärker bei höheren Greeks“ widerspricht der eigenen Matrix | Wertender Satz aus der Analyse übernommen, nicht gegen die Tabelle gelesen | Jeder Vergleichs- oder Wertungssatz muss sich aus den Zellen der zugehörigen Tabelle ableiten lassen | manuell (Skill-Checkliste) | – |
| L12 | 2026-10-07 | M300 | Zahlen (OPRA, BSW-Quoten, BGBl.-Fundstellen, Preise) ohne DBOM-Fakt | L08 prüfte nur DBOM → Seite, nicht Seite → DBOM | Jede Zahl mit Einheit, Prozent, Datum oder Fundstelle braucht `data-source` oder EST-Kennzeichnung | `check_module` L12 (BLOCKER, Elternkette) | 018c8ce: ✗ 8 Angaben · v1.1.0: ✓ |
| L13 | 2026-10-07 | M300 | DBOM der Analyse und externe DBOM haben verschiedene Faktensätze; K10 auf der Seite ◐, in der Analyse ✓ | Zwei Provenienzlisten getrennt gepflegt | Eine führende DBOM (extern). Die Analyse referenziert deren IDs, Phase-A-Ergebnisse sind auf Seite und Analyse identisch | `check_module` L13, L13b (BLOCKER) | 018c8ce: ✗ K2/K3/K10, eigene Faktenliste · v1.1.0: ✓ |
| L14 | 2026-10-07 | M300 | Quellenliste der Seite spiegelt die DBOM nicht; eine Quelle von keinem Fakt genutzt | Liste von Hand gepflegt | Quellenliste aus `dbom.sources` rendern; jede Quelle ≥ 1 Fakt, jeder Fakt mit existierender Quelle | `check_module` L14 (BLOCKER, inkl. `additional_sources`) | 018c8ce: ✗ SRC_BFH_IR2514 · v1.1.0: ✓ |
| L15 | 2026-10-07 | M300 | Tooltip nannte „125 Elemente“, gemessen 129 | Messwert von Hand in die QA-Sektion übertragen | Messwerte nie von Hand; auf die Skriptausgabe verweisen | `check_module` L15 (WARN) | v1.0.1: ! · v1.0.2: ✓ |
| L16 | 2026-10-07 | M300 | „0DTE 59 % Gesamtjahr 2025“ mit einer Quelle zum August-Rekord (62 %) belegt | Bezugszeitraum der Quelle nicht mit dem Claim abgeglichen | CONFIRMED-Fakten führen ein Feld `period`; Quelle und Claim müssen denselben Zeitraum haben | `check_module` L16 (BLOCKER: CONFIRMED braucht `period`) + manuell (Zeitraum = Claim) | 018c8ce: ✗ 14 Fakten · v1.1.0: ✓ |

---

## Offene Befunde in Altmodulen (vom Check gefunden, nicht behoben)

`python3 qa/check_module.py m299.html` (Stand 2026-10-07) meldet 6 Blocker:

- L01 und L02: gleicher Basisfehler wie M300
- L04: kein Hero-Disclaimer
- L07: Zählungen nicht an die DBOM gebunden
- L07c: JSON-LD nennt 10 Fakten, die DBOM enthält 12
- L08b: 5 Fakten ungebunden

`modul.html` (M298) ist ungeprüft. Behebung ist Maßnahme M12 im Prüfbericht `analysen/m300-qa-report-2026-10-07.md`.

### Behobene Inhaltsbefunde der Zweitprüfung (v1.1.0)

- **L11:** S09-Satz aus der Matrix abgeleitet (Volland: Gamma/Vanna/Charm belegt; SpotGamma: HIRO).
- **L06:** Fazit und Analyse „… belegt (MenthorQ: n. v.)“.
- **L12:** Neue Fakten `FACT_TERMIN_HISTORY`, `FACT_OPRA_CAPACITY`, `FACT_OPRA_BURSTS`, `FACT_BSW_SHARES` (UNVERIFIED),
  `FACT_VENDOR_PRICES`, `FACT_EUREX_SPECS`.
- **L13:** Analyse nutzt die externe DBOM; K2, K3, K10 und K11 angeglichen.
- **L14:** Quellenliste aus `dbom.sources` gerendert.
- **L16:** Cboe-Quelle auf die Jahresmeldung 2025 umgestellt; `period` für alle CONFIRMED.
- **C8:** § 80 Abs. 4 WpHG (Pflichten) bzw. Abs. 5 (Definition) statt Abs. 2.
- **Neu:** Verdict `UNVERIFIED` für Primärquellen mit unklarem Bezugszeitraum (L05c: Liste zulässiger Verdicts).
