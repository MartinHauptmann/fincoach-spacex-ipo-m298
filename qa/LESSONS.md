# FinCoach AI · Fehlerkatalog (Lessons Learned)

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

---

## Offene Befunde in Altmodulen (vom Check gefunden, nicht behoben)

`python3 qa/check_module.py m299.html` (Stand 2026-10-07) meldet 6 Blocker:

- L01 und L02: gleicher Basisfehler wie M300
- L04: kein Hero-Disclaimer
- L07: Zählungen nicht an die DBOM gebunden
- L07c: JSON-LD nennt 10 Fakten, die DBOM enthält 12
- L08b: 5 Fakten ungebunden

`modul.html` (M298) ist ungeprüft. Behebung ist Maßnahme M12 im Prüfbericht `analysen/m300-qa-report-2026-10-07.md`.
