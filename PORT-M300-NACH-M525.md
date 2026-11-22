# Port M300 (Staging) → M525 (FinCoach) · Plan

Stand 2026-11-22 · nichts davon ist veröffentlicht.

## Grundsatz: Codename bleibt intern, Port ist ein Build-Schritt

- **M300 ist nur der Staging-Codename.** In FinCoach ist M300 ein anderes Modul („product-development“),
  und M299 ist „erfolgsfaktoren-geschaeftsmodelle-500-jahre“. Die ATAS-Analyse heißt dort **M525**:
  - Registry: `atas-options-xray`.
  - Zentrales Nummern-Hauptbuch: RESERVIERT seit 2026-10-28.
  - Live seit 2026-10-26.
- **Keine Umnummerierung im Staging-Repo.** `m300.html`, `provenance/m300.dbom.json`, `qa/` und die
  7 Regressionsdateien bleiben, wie sie sind. Die QA (check_module.py, render_audit.cjs, Regression)
  läuft weiter auf `m300.html`.
- **Der Port ist einseitig und reproduzierbar.** Ein Skript erzeugt aus dem geprüften Staging-Stand die
  FinCoach-Dateien unter M525. Niemand bearbeitet die M525-Dateien von Hand. Damit entsteht weder eine
  zweite Nummer noch eine Kollision.
- **Freigabe zuerst:** Portiert wird erst, wenn M300 die Release-Regel erfüllt (alle C-Gates ✓ und Score
  ≥ 90 %). Stand jetzt: 84,2 %, offen sind C4, C5, C6, Q4, Q7 und Q9. Vorbereiten lässt sich alles schon jetzt.

## Dateizuordnung

| Staging (Quelle) | FinCoach (Ziel) | Behandlung |
|---|---|---|
| `m300.html` | `modul-m525-atas-options-xray.html` | Kopf auf FinCoach-Konvention (CDN, `tailwind.config`, Agent-Audit-Renderer), M300→M525, Ergänzungen siehe unten |
| `provenance/m300.dbom.json` | `provenance/m525.dbom.json` | M300→M525, Siegel `module.integrity_sha256` und `integrity.dbom_sha256` setzen |
| `analysen/m300-atas-options-xray-deep-dive.md` | Zielordner klären (FinCoach hat kein `analysen/`) | Links im Modul anpassen |
| `assets/hero-m300.png` (1080×1350, LinkedIn-Format) | — | **nicht** übernehmen; FinCoach braucht das Poster 1600×1000 aus `scripts/hero/specs/m525.json` |
| — | `provenance/m525.factcheck.json`, `m525.guardian.json`, `m525-provenance.html` | mit den FinCoach-Werkzeugen neu erzeugen (`guardian-modul-check.mjs` u. a.) |
| — | `api/v1/modules/M525.json`, `data/finchat/module-graph/m525.js` | neu erzeugen; `build-module-graph.mjs m525` am Probe-Port getestet: läuft, 45 Fakten (vorher 42) |
| — | `module-registry.json` | Größe und Hash neu bauen |
| — | `scripts/regression/golden/modul-m525-atas-options-xray.json` | bewusst neu setzen, mit Begründung (siehe Gates) |

## Messung: mechanischer Probe-Port durch die FinCoach-Gates

Lokal in FinCoach auf `claude/m525-port-v1-23`, Commit nicht gepusht, gegen `origin/main` `de5c71732`.

| Gate | Ergebnis | Nötige Arbeit |
|---|---|---|
| Registry-Gate | ✅ keine neuen Befunde | Registry beim Port neu bauen |
| DBOM-Gate | ✅ ok, Hinweise F-DBI-04/05 | Siegel-Felder füllen |
| Hero-Gate | ❌ R-HERO-INTERACT-01 | Hero-Komponente einbauen (siehe unten) |
| Guard: R-M525-HERO-01 | ❌ | Bühne `m525-datenpfad`, 5 Ebenen, Drill-Down auf `s06`, Bild `assets/hero/m525.jpg` |
| Guard: golden-snapshot | ❌ 4 Abweichungen | erwartet, weil neue Abschnitte `s-fz` und `s-qa` hinzukommen und `agent-audit-section` noch fehlt; Golden bewusst erneuern |
| Guard: brand-footer-url | ❌ | Footer-Link auf www.nexus2learn.com ergänzen |
| Guard: no-horizontal-overflow-375 | ❌ in der Sandbox | **Messartefakt:** dort sind die CDNs gesperrt. Mit den selbst gehosteten Bibliotheken gemessen: Seitenbreite 375 = Viewport 375, die breiten Tabellen scrollen im Container. In CI bestätigen. |
| Agent-Nachweise | ❌ F-AGO-05 | `agent-audit-section` und `<script id="module-agents-used">` ergänzen, nur mit belegten Einträgen (QA-Läufe, Zweitprüfungen) |

## Inhaltliche Anpassungen am Hero (FinCoach-Pflicht)

- **Diagramm `m525-datenpfad`:** Die fünf Knoten Daten, Modell, Markt, Wettbewerb und Steuer bleiben.
- **Wettbewerbs-Knoten ist sachlich veraltet:** Live steht dort „Eurex-GEX intraday: bei keinem der zwei
  bestimmbaren“. Er muss den Quantor aus v1.23.0 übernehmen (FACT_NO_EUREX_GEX):
  - bestimmbar ist nur ATAS, weil X-Ray nur SPX liefert und die Chain Suite nur EOD-Daten hat;
  - die übrigen fünf Anbieter sind n. v.
- **Poster:** `scripts/hero/specs/m525.json` gegen die v1.23-Fakten abgleichen. Geprüft und belegt sind bisher:
  - 59 % (FACT_SPX_0DTE_59);
  - 10 Indikatoren (FACT_XRAY_10_IND);
  - ES/MES/SPY (FACT_XRAY_1MIN_SPX);
  - keine Hedge-Pflicht (FACT_MM_NO_HEDGE_DUTY);
  - § 20 Abs. 6 EStG (FACT_JSTG2024_REPEAL).

## Reihenfolge

1. M300 freigabereif machen: 27. Zweitprüfung, Sichtprüfung des Herausgebers, Löschung des Commits `6465f29` bei GitHub (C5).
2. Port-Skript im Staging-Repo schreiben. Es macht die Kopf-Umstellung, M300→M525, Hero-Block, Agent-Audit-Block, Footer-Link und Siegel.
3. Port in einen FinCoach-Zweig erzeugen und die abgeleiteten Dateien neu bauen:
   - Registry;
   - Guardian, Factcheck und Provenienz-Graph;
   - API-Datei und FinChat-Graph;
   - Hero-Poster.
4. FinCoach-Gates lokal grün:
   - Hero-, Registry- und DBOM-Gate;
   - Guard, mit neuem Golden;
   - Agent-Nachweise.
5. Nach `main`, dann Website: `release-single-module.mjs m525` und Teaser `generate-teasers.mjs m525`.
6. Staging-Repo archivieren.
