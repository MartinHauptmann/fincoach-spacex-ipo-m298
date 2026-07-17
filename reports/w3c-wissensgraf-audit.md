# Prüfbericht: „Nexus zu lernen"-Wissensgraf vs. W3C-Wissensgraf-Definition

**Modul-Kontext:** FinCoach AI · TheNextGenerationBanking · M298 / M299
**Stichtag der Prüfung:** 2026-07-17
**Prüfgegenstand:** M-DBOM (Module Data Bill of Materials), Schema `fincoach.m-dbom.v1`
**Referenz-Standard:** W3C Semantic Web Stack (IRIs, RDF, RDFS/OWL, SHACL, SPARQL, Open-World-Annahme)

---

## 0 · Vorbemerkung zur Begriffsklärung (wichtig)

Der in der Aufgabe genannte Begriff **„Nexus zu lernen"-Wissensgraf** kommt **wörtlich weder im
Repository noch in der Git-Historie vor** (geprüft: Volltext- und `-S`/Pickaxe-Suche über alle Commits).
Der einzige tatsächlich implementierte, wissensgraf-**artige** Aufbau in diesem Projekt ist das
**M-DBOM** — eine als JSON-LD ausgezeichnete Provenienz-/Fakten-Struktur, die:

- in `modul.html` und `m299.html` **eingebettet** ist (`<script type="application/ld+json" id="module-provenance">`),
- extern als `provenance/m299.dbom.json` (und referenziert `provenance/m298.dbom.json`, **Datei fehlt aktuell**) vorliegt,
- über `data-source="FACT_…"` / `data-fact-class="…"` mit den sichtbaren KPIs/Aussagen im DOM verknüpft ist,
- per **Live-Audit-JavaScript** referenzielle Integrität prüft.

Diese Prüfung behandelt daher das **M-DBOM als den konkreten „Nexus"-Wissensgraf**. Sollte mit
„Nexus zu lernen" ein *anderes*, außerhalb dieses Repos liegendes System gemeint sein, ist dieser
Bericht auf dessen Definition zu übertragen — die Kriterienstruktur bleibt identisch.

---

## 1 · Kurz-Fazit (Executive Summary)

Von den **sechs strengen W3C-Säulen** erfüllt das M-DBOM **keine vollständig**. Zwei werden
**dem Sinn nach teilweise** getroffen (Validierung, Open-World-Epistemik), vier sind **nicht erfüllt**.

| # | W3C-Säule | Urteil | Kern-Grund |
|---|-----------|--------|-----------|
| 1 | Globale eindeutige Identität (IRIs) | ❌ **nicht erfüllt** | Lokale String-IDs (`FACT_…`, `SRC_…`, `M298`), keine dereferenzierbaren IRIs |
| 2 | Atomare Tripel-Struktur (RDF) | ❌ **nicht erfüllt** | Verschachteltes JSON, keine S-P-O-Tripel; `@context` ist (vermutlich) JSON-Schema, kein RDF-Kontext |
| 3 | Formale Ontologie (RDFS/OWL) + Reasoner | ❌ **nicht erfüllt** | Nur informelle Enum-Klassifikation; keine `rdfs:Class`/OWL-Axiome, keine Inferenz |
| 4 | Struktur-/Datenvalidierung (SHACL) | 🟡 **teilweise (Sinn erfüllt, Standard nicht)** | Validierung existiert (Integritäts-Audit, JSON-Schema, Daily-Score) — aber kein SHACL über RDF |
| 5 | Föderierte Abfrage (SPARQL) | ❌ **nicht erfüllt** | Kein SPARQL-Endpoint, kein HTTP-Query-Protokoll; Zugriff nur via `fetch()` auf JSON |
| 6 | Open-World-Annahme (OWA) | 🟡 **teilweise** | Epistemik OWA-nah (unbekannt ≠ falsch via Verdict/Caveat), Technik aber Closed-World (fehlender Fact = Fehler) |

**Gesamtbild:** Das M-DBOM ist **kein W3C-konformer Wissensgraf**, sondern ein
**proprietärer, provenienz- und vertrauens­orientierter „Fakten-Stückliste"-Graph** (Property-Graph-/
JSON-LD-Look) mit eigenem Zweck: **epistemische Ehrlichkeit** (CONFIRMED vs. SCENARIO_PROJECTION,
Konfidenzen, Caveats, Quellen-Trace). Dieser Zweck ist mit W3C-Semantik **nicht identisch** und wird
von ihr auch nicht direkt abgedeckt.

---

## 2 · Detailprüfung je Kriterium

### Kriterium 1 — Globale und eindeutige Identität (IRIs) → ❌ NICHT ERFÜLLT

**W3C-Regel:** Jeder Knoten und jede Kante muss über einen global eindeutigen **IRI** identifiziert
sein; keine lokalen, isolierten Bezeichner.

**Ist-Zustand im M-DBOM:**
- Knoten tragen **lokale String-IDs**: Fakten `FACT_INST_RETAIL_SPLIT`, `FACT_GREENSHOE_15` …,
  Quellen `SRC_NYSE_IPO_GUIDE`, `SRC_SEC_REGM` …, Modul `M298`/`M299`.
- Diese IDs sind **nicht dereferenzierbar** und **nicht global namensraum-gesichert** — außerhalb des
  Moduls kollisionsanfällig (`M298` ist nirgends als `http…/M298` auflösbar).
- Prädikate/Beziehungen (`source_id`, `claim`, `verdict`, `class`, `confidence`) sind **JSON-Schlüssel**,
  keine IRIs.
- **Teil-Ansatz vorhanden:** `@context` und `$schema_id` verweisen auf URLs
  (`https://www.thenextgenerationbanking.com/schemas/m-dbom/v1.json`). Das identifiziert das *Schema*,
  **nicht die Entitäten**.

**Urteil:** ❌ Nicht erfüllt. Es existiert kein einziger Entitäts-IRI. Damit ist auch die von W3C
geforderte **weltweite verschmelzbare Identität** nicht gegeben.

---

### Kriterium 2 — Atomare Tripel-Struktur (RDF) → ❌ NICHT ERFÜLLT

**W3C-Regel:** Daten zwingend als **S-P-O-Tripel** (RDF). Kanten-Metadaten nur via Reifizierung / RDF-Star.

**Ist-Zustand:**
- Die Daten sind **verschachtelte JSON-Objekte** (`facts: [ { id, verdict, class, confidence, claim,
  source_id, caveat } ]`), **keine Tripel**.
- Der MIME-Typ `application/ld+json` und der `@context`-Schlüssel *suggerieren* JSON-LD — aber der
  `@context` zeigt auf `…/m-dbom/v1.json`, was nach Benennung (`$schema_id`, Feld `$schema`) **eine
  JSON-Schema-Datei zur Validierung** ist, **kein JSON-LD-Term-Mapping**. Ohne echten JSON-LD-Kontext,
  der `facts`, `claim`, `verdict` … auf Prädikat-IRIs abbildet, **expandiert das Dokument nicht zu
  RDF-Tripeln**. Der `ld+json`-Typ ist hier **kosmetisch**.
- Positiv im Sinne der *Idee* von RDF-Star: Fakt-Metadaten (`confidence`, `caveat`, `status`) hängen
  direkt am Fakt-Objekt — konzeptuell wie **Kanten-/Aussage-Eigenschaften**. Das entspricht eher einem
  **Property-Graph**-Denken als klassischem RDF, ist aber **nicht** RDF-Star-Syntax.

**Urteil:** ❌ Nicht erfüllt. Struktur ist JSON, nicht RDF. (Anmerkung: Dies ist der Punkt, an dem
das Dokument am ehesten den *Anschein* von Konformität erweckt, ihn aber technisch nicht einlöst.)

---

### Kriterium 3 — Formale Ontologie & Semantik (RDFS/OWL) + Reasoner → ❌ NICHT ERFÜLLT

**W3C-Regel:** Zwingend eine logische, maschinenlesbare Schema-Ebene (RDFS-Taxonomien, OWL-Axiome),
aus der ein **Reasoner** neue Fakten **inferiert**.

**Ist-Zustand:**
- Es gibt eine **informelle Klassifikations-Vokabular-Ebene**: Verdicts `CONFIRMED` /
  `SCENARIO_PROJECTION` und Klassen `PRIMARY_OFFICIAL`, `PRIMARY_INSTITUTIONAL`, `INDUSTRY_PRACTICE`,
  `REGULATORY_FRAMEWORK`, `SCENARIO_PROJECTION`.
- Diese sind **Enum-Strings**, **keine** `rdfs:Class` mit `rdfs:subClassOf`-Hierarchie, **keine**
  `rdf:Property`-Definitionen, **keine** OWL-Axiome (transitiv/symmetrisch/Kardinalität/`owl:sameAs` …).
- **Keine Inferenz / kein Reasoner.** Es werden keine impliziten Fakten abgeleitet; das Live-Audit prüft
  nur, es *schließt* nicht.
- Das vorhandene „Schema" (`$schema_id`) ist **Validierung (JSON Schema)**, **nicht Semantik (Ontologie)**.

**Urteil:** ❌ Nicht erfüllt. Es existiert ein *kontrolliertes Vokabular*, aber keine formale Ontologie
und keine Inferenzfähigkeit.

---

### Kriterium 4 — Struktur-/Datenvalidierung (SHACL) → 🟡 TEILWEISE (Sinn erfüllt, Standard nicht)

**W3C-Regel:** **SHACL-Shapes** als automatisierter Vertrag über dem RDF-Graphen; regelwidrige Daten
werden abgewiesen.

**Ist-Zustand — das ist die konzeptuell stärkste Säule des M-DBOM:**
- **Referenzielle Integrität** wird zur Laufzeit erzwungen: Das Live-Audit-JS (`liveAudit()` in
  `modul.html`) sammelt alle `data-source="FACT_…"`-Attribute und prüft, ob jede referenzierte
  Fact-ID **tatsächlich im DBOM existiert** — fehlende werden rot markiert (`DBOM-MISSING`) und im Banner
  als Fehler gemeldet.
- Es existiert ein **JSON-Schema-Vertrag** (`$schema_id: "fincoach.m-dbom.v1"`).
- Es gibt einen **Daily-Compliance-Score** (`reports/compliance/<date>.json`, Score-Pill je Modul).
- **Aber:** All das ist **kein SHACL** und **operiert nicht über RDF**. Es gibt keine `sh:NodeShape`,
  keine `sh:property`/`sh:minCount`/`sh:datatype`-Constraints. Validierung ist imperativ (JS) +
  JSON-Schema, nicht deklarativ-graphbasiert.

**Urteil:** 🟡 Teilweise. **Die Absicht von SHACL — „Daten, die dem Vertrag widersprechen, kommen nicht
durch" — ist funktional vorhanden**, aber die **W3C-Technologie SHACL ist nicht umgesetzt**. Dies ist die
Säule mit der geringsten inhaltlichen Lücke.

---

### Kriterium 5 — Föderierte, standardisierte Abfrage (SPARQL) → ❌ NICHT ERFÜLLT

**W3C-Regel:** Abfrage über **SPARQL** inkl. HTTP-Protokoll und öffentlichem **SPARQL-Endpoint**;
weltweite Föderation mehrerer Graphen in einer Abfrage.

**Ist-Zustand:**
- **Kein SPARQL.** Datenzugriff erfolgt ausschließlich per `fetch('provenance/m298.dbom.json')` und
  JavaScript-Objektzugriff.
- **Kein Endpoint, kein Query-Protokoll, keine Föderation.** Die Graphen (M298/M299) sind isolierte
  JSON-Dateien; eine gemeinsame Abfrage über verteilte Wissensgrafen ist nicht möglich.

**Urteil:** ❌ Nicht erfüllt.

---

### Kriterium 6 — Open-World-Annahme (OWA) → 🟡 TEILWEISE

**W3C-Regel:** Fehlende Information bedeutet **„unbekannt"**, nicht **„falsch"** (Open World).

**Ist-Zustand — zwiespältig:**
- **Epistemisch OWA-nah (positiv):** Das gesamte Design unterscheidet bewusst zwischen *bestätigt*,
  *Szenario/unbekannt* und *nicht unabhängig verifiziert*: `verdict: CONFIRMED` vs.
  `SCENARIO_PROJECTION`, `confidence`-Werte, `caveat`-Felder, `honest_disclosure` („dem System aktuell
  *unbekannt*", „nicht unabhängig verifiziert"). Genau das ist der **Geist der OWA**: Abwesenheit von
  Bestätigung ≠ Falschheit.
- **Technisch Closed-World (negativ):** Das Validierungsmodell ist geschlossen. Ein `data-source`, das
  **nicht** im DBOM steht, gilt als **Fehler** (`DBOM-MISSING`), nicht als „vielleicht anderswo wahr".
  `fact_summary.total` fixiert die Faktenmenge. Das entspricht der **Closed-World-Annahme**.

**Urteil:** 🟡 Teilweise. Die **Denkweise** ist OWA-kompatibel, die **technische Umsetzung** ist CWA.

---

## 3 · Sammel-Aufstellung: erfüllt / nicht erfüllt

**Vollständig erfüllt (W3C-konform):** — *keine Säule.*

**Teilweise / dem Sinn nach erfüllt:**
- ✅(Sinn) **Validierung** — Integritäts-Audit + JSON-Schema + Daily-Score (aber kein SHACL).
- ✅(Sinn) **Open-World-Epistemik** — Verdict/Confidence/Caveat trennen „unbekannt" von „falsch"
  (aber technisch CWA-Validierung).
- ✅(Ansatz) **Identität/Schema-Referenz** — `@context`/`$schema_id` als URL (aber nur fürs Schema,
  nicht für Entitäten).
- ✅(Ansatz) **Fakt-Metadaten am Fakt** — konzeptuell wie RDF-Star/Property-Graph
  (aber keine RDF-Star-Syntax).

**Nicht erfüllt:**
- ❌ **IRIs** für Knoten und Kanten (nur lokale IDs).
- ❌ **RDF-Tripel-Struktur** (verschachteltes JSON, `ld+json` nur nominell).
- ❌ **RDFS/OWL-Ontologie + Reasoner/Inferenz** (nur Enum-Vokabular).
- ❌ **SHACL** als W3C-Standard.
- ❌ **SPARQL** / Endpoint / Föderation.
- ❌ **Technische OWA** (Validierung ist Closed-World).

---

## 4 · Erforderliche Änderungen, Auswirkungen und Aufwände

> Grundsatzfrage vorab: **Braucht der „Nexus"-Graf überhaupt W3C-Konformität?** Sein Zweck
> (Provenienz + Vertrauens-/Ehrlichkeits-Kennzeichnung publizierter Aussagen) verlangt **nicht** die
> Semantic-Web-Föderation. Volle W3C-Konformität ist daher **eine strategische Option, keine Pflicht**.
> Die folgende Staffelung erlaubt, den Nutzen gezielt zu heben, ohne alles umzubauen.

### Stufe A — „W3C-nah ohne Bruch" (kleiner Aufwand, hoher Ehrlichkeitsgewinn)
| Änderung | Auswirkung | Aufwand |
|---|---|---|
| `@context` ehrlich benennen: entweder echten JSON-LD-Kontext bereitstellen **oder** MIME auf `application/json` + Feld `$schema` (JSON Schema) ändern, um den irreführenden `ld+json`-Schein zu beenden | Beseitigt die Fehlwahrnehmung „ist JSON-LD/RDF". Keine funktionale Regression | **S** (0,5–1 PT) |
| Fehlende `provenance/m298.dbom.json` nachliefern (aktuell referenziert, aber nicht vorhanden) | Live-Audit läuft nicht mehr in den `catch`-Zweig; Integrität real prüfbar | **S** (0,5 PT) |
| Enum-Klassen als kleines **kontrolliertes Vokabular** dokumentieren (Definitionen der Verdict-/Class-Werte) | Vorstufe zu RDFS/SKOS; verbessert Nachvollziehbarkeit | **S** (0,5–1 PT) |

### Stufe B — „Echtes JSON-LD → RDF" (mittlerer Aufwand)
| Änderung | Auswirkung | Aufwand |
|---|---|---|
| **Realen JSON-LD-`@context`** schreiben, der `facts/claim/verdict/source_id/…` auf Prädikat-**IRIs** mappt; Entitäten als IRIs (`https://…/fact/FACT_GREENSHOE_15`) vergeben (**Krit. 1 + 2**) | Dokument expandiert dann tatsächlich zu **RDF-Tripeln**; Knoten/Kanten global identifizierbar & verschmelzbar. Bricht keine bestehende HTML-Anzeige (JSON bleibt lesbar) | **M** (3–6 PT) |
| **SKOS/RDFS-Vokabular** für Verdict-/Class-Hierarchie (`skos:ConceptScheme`, `rdfs:subClassOf`) (**Krit. 3, Basis**) | Maschinenlesbare Taxonomie; ermöglicht einfache Ableitungen | **M** (2–4 PT) |
| **SHACL-Shapes** aus den bestehenden impliziten Regeln generieren (jede KPI-Referenz muss auf existierenden Fakt zeigen; jeder Fakt braucht `verdict`, `confidence∈[0,1]`, `source_id`) (**Krit. 4**) | Ersetzt/ergänzt das JS-Audit durch **standardkonforme, deklarative** Validierung; wiederverwendbar in jedem SHACL-Tool | **M** (2–4 PT) |

### Stufe C — „Voller Semantic-Web-Stack" (großer Aufwand, meist nicht nötig)
| Änderung | Auswirkung | Aufwand |
|---|---|---|
| **OWL-Ontologie + Reasoner** (Transitivität, Kardinalität, Inferenz) (**Krit. 3, voll**) | Automatische Fakten-Ableitung. Nutzen für ein Publishing-Modul **gering**; erhöht Komplexität/Wartung stark | **L** (5–10+ PT) |
| **Triple-Store + SPARQL-Endpoint** (z. B. Fuseki/GraphDB) hosten, DBOMs laden, Föderation (**Krit. 5**) | Weltweite föderierte Abfragen möglich — **aber**: bricht das Kern-Versprechen „**kein Build-Step**, rein statisch auf Netlify" (siehe README). Erfordert Server-Backend, Betrieb, Security, DSGVO-Neubewertung | **L** (10+ PT + laufender Betrieb) |
| **Technische OWA** umsetzen (Validierung nicht mehr „fehlender Fakt = Fehler") (**Krit. 6**) | Konfligiert mit dem Provenienz-Zweck (dort ist eine geschlossene, auditierbare Faktenmenge *gewollt*). Nur sinnvoll bei echter Föderation | **M–L**, konzeptuell heikel |

### Wesentliche Konflikte / Nebenwirkungen (explizit)
1. **Architektur-Bruch bei SPARQL:** Das Projekt ist bewusst **statisch, ohne Build/Backend** (README §1,
   `netlify.toml`). Ein SPARQL-Endpoint erzwingt ein **Server-Backend** → Widerspruch zum Produktversprechen,
   Betriebs-/Sicherheits-/Datenschutzaufwand.
2. **OWA vs. Provenienz-Zweck:** Das M-DBOM will *gerade* eine **geschlossene, prüfbare** Aussagenmenge
   (Audit „alle Referenzen aufgelöst"). Echte technische OWA würde diesen Kernnutzen schwächen.
3. **Reasoner-Nutzen gering:** Inferenz bringt einem redaktionellen Publishing-Graphen wenig, kostet aber
   Komplexität und neue Fehlerquellen (falsch abgeleitete Fakten in einem Modul, das mit „Ehrlichkeit" wirbt).

---

## 5 · Empfehlung

1. **Ehrlichkeit der Auszeichnung zuerst (Stufe A):** Den `ld+json`-Schein auflösen und die fehlende
   `m298.dbom.json` liefern — kleiner Aufwand, beseitigt die größte *Fehlwahrnehmung* „das ist schon
   W3C/RDF". Für ein Modul, dessen Markenkern **Provenienz-Ehrlichkeit** ist, ist das die wichtigste Maßnahme.
2. **Optionaler Konformitäts-Layer (Stufe B):** Wenn W3C-Anschlussfähigkeit gewünscht ist, ist der
   **beste Hebel** ein echter JSON-LD-Kontext + IRIs + SHACL — das macht den Graphen **tripel- und
   SHACL-fähig, ohne die statische Architektur zu brechen** (alles bleibt Datei-basiert).
3. **Stufe C nur bei echtem Föderationsbedarf.** Solange keine graphübergreifende, weltweite Abfrage
   gebraucht wird, sind OWL-Reasoner und SPARQL-Endpoint **überdimensioniert** und stehen im Konflikt zur
   „kein Build-Step / statisch"-Doktrin.

**Kernaussage:** Das M-DBOM ist ein **guter Provenienz-/Vertrauens-Graph**, aber **kein W3C-Wissensgraf**.
Es erfüllt heute **0 von 6** Säulen vollständig (2 dem Sinn nach). Mit **Stufe A+B** (grob **10–20 PT**)
ließe sich echte **RDF-/SHACL-Konformität** (Säulen 1, 2, 4 und Basis von 3) herstellen, ohne die
statische Publishing-Architektur aufzugeben; **SPARQL/OWL/technische OWA** (Säulen 5, 3-voll, 6) sind
architektonisch teuer und für den aktuellen Zweck **nicht empfohlen**.
