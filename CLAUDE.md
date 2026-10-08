# FinCoach AI · Projektregeln für Claude

Statische Website mit Analyse-Modulen (`modul.html` = M298, `m299.html`, `m300.html`, …), Provenienz-Dateien
(`provenance/*.dbom.json`), Analysen (`analysen/`) und Modul-Prompts (`prompts/`). Kein Build-Step.

## Verbindlich bei jeder Änderung an einem Modul

- Vor Veröffentlichung, Artifact-Publish oder Commit einer Modulseite: Skill **`fincoach-module-qa`** befolgen.
- Abgeleitete Werte nur mit `python3 qa/sync_module.py <seite>` schreiben (L35).
- Beide Prüfskripte müssen mit Exit 0 laufen (Browser-Audit auch für `impressum.html` und `datenschutz.html`, L30):
  - `python3 qa/check_module.py <seite>`
  - `node qa/render_audit.cjs <seite>`
  Die Ausgabe gehört in Bericht oder Commit.
- **Kein ✓ ohne Messung** (L10). Wurde nicht gemessen, gilt ◐.
- Styleguide-Basis auch auf `body` setzen (L01); Faktenzahlen und QA-Score nie von Hand schreiben (L03, L07).
- Bibliotheken nur aus `vendor/` laden, keine CDNs (L20); Tailwind nach Klassenänderungen mit `sh vendor/build-tailwind.sh` neu bauen.
- Hero mit zugänglicher Grafik (L22); Hinweisboxen über volle Breite (L23).
- Neuer Fehler → `qa/LESSONS.md` + Regel im Skill + Test im Skript + Regressionsnachweis (Skill, Abschnitt 5).
- Vor Freigabe oder öffentlichem Teilen: Agent **`fincoach-qa-reviewer`** als unabhängige Zweitprüfung.

## Inhaltliche Grundsätze

Keine Anlage-, Rechts- oder Steuerberatung; Stichtag und Provenienz (M-DBOM) für jede Tatsachenbehauptung; Szenarien
und Modellannahmen klar getrennt; Marken nur beschreibend. Details in den Gates C1–C9 und Q1–Q10 der Modul-Prompts.
