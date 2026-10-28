# FinCoach AI · Deep-Dive-Prime-Analyse · Modul M300

**ATAS Options X-Ray · Dealer-Greeks · Eurex-Börsenoptionen vs. verbriefte Derivate · Termingeschäfte im Steuerrecht**

| Feld | Wert |
|---|---|
| Modul | M300 (Platzhalter-ID) |
| Version | 1.22.0 (Entwurf) |
| Stichtag | 2026-10-05 |
| Zielstufe (CAT-Level) | Experte |
| Grundlage | Prompt `prompts/m300-atas-options-xray-deep-dive-prompt.md` v1.7.0; Quelltext vom 2026-10-05 (USER_PROVIDED) |
| Freigabeempfehlung | **ÜBERARBEITUNG** (siehe QA-Scorecard, Abschnitt 8) |

> **Disclaimer (Kurzfassung):** Diese Analyse ist eine allgemeine Information zu Bildungszwecken. Sie ist
> keine Anlageberatung oder Anlagevermittlung im Sinne von WpIG/KWG, keine Rechtsberatung im Sinne des RDG
> und keine Steuerberatung im Sinne des StBerG. Sie enthält keine Anlageempfehlung im Sinne von Art. 3 Abs. 1
> Nr. 34 und 35 MAR. Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind Hebelprodukte mit dem
> Risiko des Totalverlusts. Bei Futures und Stillhaltergeschäften (Verkauf von Optionen gegen Prämie) können die Verluste den Kapitaleinsatz
> übersteigen. Diese Produkte sind nur für erfahrene Anleger geeignet, die Hebel- und Knock-out-Mechanik
> verstehen und Verluste bis zum Totalverlust tragen können. Steuerliche Aussagen geben den recherchierten Rechtsstand zum Stichtag wieder und ersetzen
> keine individuelle Prüfung durch Steuerberater oder Rechtsanwalt.

> **Methodischer Vorbehalt:** Die Recherche lief über eine Netzwerkumgebung, die den direkten Abruf der
> meisten Primärquellen gesperrt hat, darunter gesetze-im-internet.de, recht.bund.de, eurex.com, atas.net und die Anbieterseiten.
> Recherchiert wurde deshalb über Suchtreffer, die auf diese Primärquellen verweisen; die URLs stehen im
> Quellenverzeichnis. Der Herausgeber hat am 2026-10-11 jeden Beleg zum Stichtag an seiner Quelle abgeglichen: Primär- und
> Herstellerquellen am Original (`evidence: fulltext`), ausgenommen die fünf Medienangaben, die an ihrer
> Sekundärquelle geprüft sind (`evidence: secondary`), und der Quantor `FACT_NO_EUREX_GEX`, der aus zwei geprüften
> Herstellerangaben abgeleitet ist (`evidence: derived`), ebenso ausgenommen die spätere GEX-Metrix-Momentaufnahme
> vom 2026-10-23 (`FACT_GEXMETRIX_SPX`, `evidence: screenshot`), die auf einer Bildschirmkopie des Herausgebers beruht,
> mit daraus berechneten Differenzen (`FACT_GEXMETRIX_DERIVED`) und der ungeprüften Wall-Ablesung (`FACT_GEXMETRIX_WALLS_READ`).

> **Aufbau:** Diese Analyse ist eine faktgebundene Kurzfassung. Jede Angabe nennt die Fakt-ID ihres Belegs aus
> `provenance/m300.dbom.json` mit Verdict und Konfidenz; Zitate des Quelltexts sind als solche gekennzeichnet.
> Abschnitt 2, die Module in Abschnitt 3 und das Glossar erzeugt `qa/sync_module.py` aus Modulseite und DBOM. Die ausführliche
> Darstellung mit Diagrammen und Rechner steht auf der Modulseite `m300.html`.

---

## 1 · Executive Summary

Kernergebnisse; jede Aussage mit Fakt-ID:

- **Steuerlicher Rahmen (Stichtag 2026-10-05):** Verluste aus Termingeschäften im Privatvermögen unterliegen keiner
  gesonderten Verlustverrechnungsbeschränkung (`FACT_JSTG2024_REPEAL`).
- **Kapitalgesellschaften:** § 15 Abs. 4 Satz 3 EStG gilt über § 8 Abs. 1 KStG auch für sie (`FACT_P15_KSTG`).
- **Market Maker:** Eine gesetzliche Pflicht zum Orderbuch-Hedging besteht nicht (`FACT_MM_NO_HEDGE_DUTY`).
- **Produkt:** Die Suite umfasst zehn Indikatoren auf Basis eines 1-Minuten-CBOE-Feeds, nur für SPX-Optionen
  (`FACT_XRAY_10_IND`, `FACT_XRAY_1MIN_SPX`). Optionen sind in ATAS derzeit nicht handelbar (`FACT_ATAS_NO_OPT_TRADING`).
- **Modell:** Das GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (`FACT_DEALER_CONVENTION`,
  SCENARIO_PROJECTION, keine Prognose-Konfidenz).
- **Wettbewerb:** Von sechs verglichenen Anbietern ist nur für einen bestimmbar, dass er in den ausgewerteten Funktionen
  keine intraday-fähige Eurex-GEX bietet, für ATAS selbst; für SpotGamma, MenthorQ, Volland, Bookmap und die IBKR TWS ist das n. v. (`FACT_NO_EUREX_GEX`, belegt, Konfidenz 0,75).
- **Einschätzung [SZENARIO]:** Der Wert einer Eurex-Erweiterung läge in einer möglichen Analyselücke (bisher nur
  für einen Anbieter bestimmbar), nicht in einem Steuervorteil (`FACT_ROADMAP`, SCENARIO_PROJECTION, keine Prognose-Konfidenz). Das ist keine Prognose.

---

## 2 · Phase A: Faktenprüfung K1–K9

### 2.1 Claim-Tabelle

<!-- sync:CLAIMS -->
Legende: ✓ bestätigt · ◐ präzisiert · ✗ falsch · [N. V.] nicht verifiziert. Die Aussagen in Spalte 2 zitieren den Quelltext (USER_PROVIDED) und sind keine Tatsachenbehauptungen dieser Analyse.

| ID | Aussage | Kategorie | Ergebnis | Belege | Schwächster Beleg |
|---|---|---|---|---|---|
| A01 | Quelltext: Market Maker sind gesetzlich gezwungen, über das zentrale Orderbuch zu hedgen | Mikrostruktur | ✗ | (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85) | belegt |
| A02 | Quelltext: Emittenten netten intern und hedgen über OTC-Swaps; keine Orderbuchspuren im FDAX | Mikrostruktur | ◐ | (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6) | Medienangabe |
| A03 | Quelltext: Für vermögensverwaltende Kapitalgesellschaften gilt keine Verlustverrechnungsbeschränkung | Steuer/Recht | ✗ | (`FACT_P15_KSTG`, belegt, Konfidenz 0,85) | belegt |
| A04 | Quelltext: Options X-Ray besteht aus zehn Indikatoren | Produkt | ✓ | (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85) | belegt |
| A05 | Quelltext: Datenbasis CBOE/OptionsDepth, 60-Sekunden-Snapshots | Produkt | ✓ | (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85) | belegt |
| A06 | Quelltext: Beschränkung auf den SPX-Komplex | Produkt | ✓ | (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85) | belegt |
| A07 | Quelltext: Broker-Konnektivität Rithmic, IB, CQG | Produkt | ◐ | (`FACT_XRAY_CONNECTIVITY`, belegt, Konfidenz 0,7), (`FACT_ATAS_CONNECTIONS`, belegt, Konfidenz 0,85) | belegt |
| A08 | Quelltext: ES/MES-Cross-Trading vorhanden | Produkt | ✓ | (`FACT_CROSS_TRADING`, belegt, Konfidenz 0,85) | belegt |
| A09 | Quelltext: Options Board und Strategy Analyzer in Entwicklung | Produkt | ◐ | (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8) | belegt |
| A10 | Quelltext: Fehlende native Multi-Leg-Spread-Routing-Engine | Produkt | ◐ | (`FACT_IB_BAG`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8) | belegt |
| A11 | Quelltext: NDX/NQ zeigt überproportionale 0DTE-Dynamik | Markt | [N. V.] | [N. V.] | – |
| A12 | Quelltext: Wettbewerbsfelder (SpotGamma, MenthorQ, Volland, Bookmap, TWS) | Wettbewerb | ◐ | (`FACT_SPOTGAMMA_SPEC`, belegt, Konfidenz 0,75), (`FACT_MENTHORQ_SPEC`, belegt, Konfidenz 0,75), (`FACT_VOLLAND_SPEC`, Medienangabe, Konfidenz 0,65), (`FACT_BOOKMAP_SPEC`, belegt, Konfidenz 0,75), (`FACT_TWS_SPEC`, belegt, Konfidenz 0,75) | Medienangabe |
| A13 | Quelltext: Vier Roadmap-Erweiterungen | Vorschlag | Szenario | (`FACT_ROADMAP`, SCENARIO_PROJECTION, keine Prognose-Konfidenz) | SCENARIO_PROJECTION |
| A14 | Quelltext: Warrant-Fair-Value-Tool zeigt „verdeckte Marge“ | Vorschlag | ◐ | (`FACT_ROADMAP`, SCENARIO_PROJECTION, keine Prognose-Konfidenz), (`FACT_PRIIPS_UWG`, belegt, Konfidenz 0,75) | SCENARIO_PROJECTION |
| A15 | Quelltext: Börsengehandelte Optionen sind gegenüber Optionsscheinen steuerlich benachteiligt | Steuer/Recht | ✗ | (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9) | belegt |

<!-- /sync:CLAIMS -->

### 2.2 Prüfprotokoll K1–K9

<!-- sync:K -->
**K1 · Kapitalgesellschaft.** Quelltext: „keine Verlustverrechnungsbeschränkung“. Über § 8 Abs. 1 KStG gilt § 15 Abs. 4 Satz 3 EStG: eigener Verlustkreis für Termingeschäfte (BFH I R 25/14). Ausnahmen bestehen nur für Institute und Sicherungsgeschäfte. Belege: (`FACT_P15_KSTG`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (KRITISCH)

**K2 · Hedging-Pflicht Market Maker.** Quelltext: Market Maker „gesetzlich gezwungen“, über das Orderbuch zu hedgen. Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition in Abs. 5) regeln Quotierungs- und Vertragspflichten. Delta-Hedging ist Risikomanagement und kann über viele Kanäle erfolgen. Belege: (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (WESENTLICH)

**K3 · GEX-Prämisse.** Quelltext: Dealer-Hedging als feste Mechanik. Die Positionskonvention ist eine Modellannahme. Beim SPX ist sie durch Teilnehmer-markierte Cboe-Daten besser fundiert, bleibt aber anfällig für Spreads, Overwriting und Intraday-Volumen. (Modellannahme; Cboe-Daten: Medienangabe; Anfälligkeit: Einschätzung) Belege: (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, keine Prognose-Konfidenz), (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (WESENTLICH)

**K4 · Emittenten-Hedging.** Quelltext: „keine“ Hedging-Spuren im FDAX. Emittenten hedgen dynamisch, auch über Basiswert und Gegengeschäfte. Die Spur ist schwach und nicht zurechenbar, aber nicht null. (Hedging: Medienangabe; Stärke der Spur: Einschätzung) Belege: (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (HINWEIS)

**K5 · ATAS-Produktangaben.** Quelltext: 10 Indikatoren, CBOE/OptionsDepth, 60 s, nur SPX. Bestätigt durch Hilfe- und Lernseiten des Herstellers. Ergänzung: Optionen in ATAS derzeit nicht handelbar; Options Board/Strategy Analyzer als Beta. Belege: (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85), (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8). **Ergebnis: ✓** (HINWEIS)

**K6 · Wettbewerber.** Quelltext: Vergleich SpotGamma, MenthorQ, Volland, Bookmap, TWS. Herstellerangaben von SpotGamma, MenthorQ, Bookmap und TWS (belegt); Volland über die Partnerseite ORATS (Volland: Medienangabe); einzelne Felder n. v. Belege: (`FACT_SPOTGAMMA_SPEC`, belegt, Konfidenz 0,75), (`FACT_MENTHORQ_SPEC`, belegt, Konfidenz 0,75), (`FACT_VOLLAND_SPEC`, Medienangabe, Konfidenz 0,65), (`FACT_BOOKMAP_SPEC`, belegt, Konfidenz 0,75), (`FACT_TWS_SPEC`, belegt, Konfidenz 0,75). **Ergebnis: ◐** (HINWEIS)

**K7 · Eurex-Spezifikationen.** Quelltext: FDAX/FESX-Optionsketten, „Hexensabbat“. Für den Ausgangstext maßgeblich sind die Indexoptionen ODAX (5 €/Pkt.) und OESX (10 €/Pkt.). Fachbegriff: Quartalsverfall; bei den Standard-Monats- und Quartalsoptionen ist der letzte Handelstag der dritte Freitag. Daneben gibt es End-of-Day-Optionen (OEXP, ODAP); für OEXP sind seit 05.01.2026 Verfälle an zehn Handelstagen gelistet. Belege: (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85), (`FACT_OESX_MULT`, belegt, Konfidenz 0,85), (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85), (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8). **Ergebnis: ◐** (HINWEIS)

**K8 · IBKR-Combo-Orders.** Quelltext: native Spread-Engine fehlt. Für ATAS zutreffend, aber zu präzisieren. Die IB-API unterstützt BAG-Combo-Orders (bis 6 Legs, Netto-Limit) bereits. Offen ist die Einbindung in ATAS (Oberfläche, Risikoprüfung, Positionsführung). (Einschätzung) Belege: (`FACT_IB_BAG`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8). **Ergebnis: ◐** (WESENTLICH)

**K9 · Warrant-Fair-Value-Tool.** Quelltext: „verdeckte Marge“, „künstliche Spread-Ausweitung“. Wertende Begriffe mit UWG-Risiko. Neutral: Fair-Value-Differenz, Emittentenaufschlag. Abgleich mit PRIIPs-KID; Emittentenbonität ist ein realer Wert, keine Marge.  Belege: (`FACT_PRIIPS_UWG`, belegt, Konfidenz 0,75). **Ergebnis: ◐** (WESENTLICH)

<!-- /sync:K -->

### 2.3 Korrekturliste zum Quelltext

<!-- sync:KORR -->
| Nr. | Schwere | Prüfpunkt | Ergebnis |
|---|---|---|---|
| K1 | KRITISCH | Kapitalgesellschaft: „keine Verlustverrechnungsbeschränkung“ | ✗ |
| K2 | WESENTLICH | Hedging-Pflicht Market Maker: Market Maker „gesetzlich gezwungen“, über das Orderbuch zu hedgen | ✗ |
| K3 | WESENTLICH | GEX-Prämisse: Dealer-Hedging als feste Mechanik | ◐ |
| K4 | HINWEIS | Emittenten-Hedging: „keine“ Hedging-Spuren im FDAX | ◐ |
| K6 | HINWEIS | Wettbewerber: Vergleich SpotGamma, MenthorQ, Volland, Bookmap, TWS | ◐ |
| K7 | HINWEIS | Eurex-Spezifikationen: FDAX/FESX-Optionsketten, „Hexensabbat“ | ◐ |
| K8 | WESENTLICH | IBKR-Combo-Orders: native Spread-Engine fehlt | ◐ |
| K9 | WESENTLICH | Warrant-Fair-Value-Tool: „verdeckte Marge“, „künstliche Spread-Ausweitung“ | ◐ |

<!-- /sync:KORR -->

---

## 3 · Phase B: Module 1–7 (faktgebundene Kurzfassung)

Je Modul die gebundenen Fakten aus der DBOM. Wertungen stehen nur in Modul 8 (aus dem Fazit der Modulseite) und sind als Einschätzung markiert.

<!-- sync:MOD -->
#### Modul 1 · Technologische Dekonstruktion der Options X-Ray Suite

- Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile). (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85)
- Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY. (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85)
- OptionsDepth deckt derzeit nur SPX und VIX ab. (`FACT_OPTIONSDEPTH_SCOPE`, belegt, Konfidenz 0,75)
- SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt. (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6)
- GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls). (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, keine Prognose-Konfidenz)
- Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES. (`FACT_GEX_EXAMPLE`, SCENARIO_PROJECTION, keine Prognose-Konfidenz)
- Kontraktdaten: Multiplikator SPX 100 USD je Indexpunkt, SPXW-Optionen mit Verfällen an jedem Wochentag (0DTE möglich; Cboe); E-mini S&P 500 50 USD und Micro E-mini 5 USD je Indexpunkt (CME); Eurex-Standardoptionen auf Indizes (Monats- und Quartalsverfälle): letzter Handelstag ist der dritte Freitag des Verfallsmonats (Quartalsverfall im März, Juni, September und Dezember). (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8)

#### Modul 2 · Datenfeed-Architektur, Latenzprofil und Validierung

- Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung. (`FACT_XRAY_CONNECTIVITY`, belegt, Konfidenz 0,7)
- OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster. (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7)
- Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab. (`FACT_CHAIN_SUITE`, belegt, Konfidenz 0,85)

#### Modul 3 · Handels- und Ausführungsmöglichkeiten

- ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed. (`FACT_ATAS_CONNECTIONS`, belegt, Konfidenz 0,85)
- Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan). (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8)
- ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026). (`FACT_CROSS_TRADING`, belegt, Konfidenz 0,85)
- IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit. (`FACT_IB_BAG`, belegt, Konfidenz 0,85)
- § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). (`FACT_ALGO_TRADING`, belegt, Konfidenz 0,85)
- Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85)
- Laut ATAS-Changelog vom 04.08.2026 ist ein MBO-Bundle (Iceberg-, Stop-Runs- und Sweeps-Tracker) für Ultra-Nutzer zur Erprobung verfügbar; MBO-Daten erfordern eine Rithmic-Anbindung. (`FACT_ATAS_MBO`, belegt, Konfidenz 0,8)
- ATAS bietet Footprint-Charts (Cluster-Charts) auf Basis von Tick-Daten der Börse mit Darstellungen wie Volumen, Bid × Ask und Delta. (`FACT_ATAS_FOOTPRINT`, belegt, Konfidenz 0,8)

#### Modul 4 · Mikro-Makro-Synergien im praktischen Trading

- Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %. (`FACT_SPX_0DTE_59`, belegt, Konfidenz 0,85)
- Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. (`FACT_MAR_RECO`, belegt, Konfidenz 0,85)

#### Modul 5 · Globaler Wettbewerbsvergleich (Matrix auf der Modulseite S09)

- SpotGamma – Gamma-Levels, Research · HIRO/TRACE intraday, Levels vor Eröffnung · GEX ja, Vanna als Modell, Charm n. v. · Abdeckung SPX, NDX, ETFs, Einzelaktien · Orderflow/MBO n. v. · keine eigene Ausführung. (`FACT_SPOTGAMMA_SPEC`, belegt, Konfidenz 0,75)
- MenthorQ – Gamma-Levels, Modelle, Ausbildung · Optionsdaten EOD und alle 5 Min. · GEX ja, Vanna und Charm n. v. · Abdeckung inkl. Futures-Optionen (Umfang n. v.) · Orderflow/MBO n. v. · Ausführung über Partnerplattformen · Eurex-GEX n. v.. (`FACT_MENTHORQ_SPEC`, belegt, Konfidenz 0,75)
- Volland – Notional-Greeks Dealer-Buch · Optionsdaten EOD bis alle 5 Min. · Gamma, Vanna und Charm · Abdeckung Auswahl nach Notional (Umfang n. v.) · Orderflow/MBO n. v. · Ausführung n. v.. (`FACT_VOLLAND_SPEC`, Medienangabe, Konfidenz 0,65)
- Bookmap – Orderbuch-Heatmap, Ausführung · keine nativen Optionsdaten · Greeks nur über Add-ons · Abdeckung Futures, Aktien, Krypto · Heatmap, MBO via Rithmic · eigene Ausführung. (`FACT_BOOKMAP_SPEC`, belegt, Konfidenz 0,75)
- IBKR TWS – Broker, Portfoliorisiko · Echtzeit-Optionsdaten (Abo) · aggregiertes Greek-Exposure nur für eigene Positionen · Abdeckung global inkl. ODAX/OESX · Orderflow/MBO n. v. · eigene Ausführung. (`FACT_TWS_SPEC`, belegt, Konfidenz 0,75)
- Von sechs verglichenen Anbietern ist nur für einen bestimmbar, dass er keine intraday-fähige Eurex-GEX anbietet: In den ausgewerteten ATAS-Funktionen deckt Options X-Ray nur SPX ab und die Options Chain Suite nur ES, NQ, CL und GC auf EOD-Basis; für die übrigen fünf (SpotGamma, MenthorQ, Volland, Bookmap, IBKR TWS) n. v. (`FACT_NO_EUREX_GEX`, belegt, Konfidenz 0,75)

#### Modul 6 · DACH-Marktspezifika und steuerlicher Rahmen

- Verluste aus Termingeschäften im Privatvermögen unterliegen keiner gesonderten Verlustverrechnungsbeschränkung; es gelten die allgemeinen Regeln für Einkünfte aus Kapitalvermögen (§ 20 Abs. 6 EStG in der Fassung des JStG 2024, BGBl. 2024 I Nr. 387). Daraus folgt: Börsengehandelte Optionen und Optionsscheine werden insoweit nicht unterschiedlich behandelt. (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9)
- § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016. (`FACT_P15_KSTG`, belegt, Konfidenz 0,85)
- Börsengehandelte Eurex-Optionen werden über die Eurex Clearing AG als zentrale Gegenpartei abgewickelt (Zulassung nach EMIR durch die BaFin am 10.04.2014); die Teilnehmer hinterlegen Sicherheiten (Margin). (`FACT_CCP_ISSUER`, belegt, Konfidenz 0,8)
- Optionsscheine sind vom Emittenten ausgegebene Wertpapiere; ihr Wert hängt von dessen Bonität ab (Emittentenrisiko). (`FACT_OS_ISSUER`, Medienangabe, Konfidenz 0,7)
- ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet. (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85)
- OESX (EURO-STOXX-50-Indexoptionen): 10 € je Indexpunkt, europäisch, Barausgleich. (`FACT_OESX_MULT`, belegt, Konfidenz 0,85)
- Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. (`FACT_EUREX_OI`, belegt, Konfidenz 0,85)
- Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen. (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85)
- Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte. (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6)
- BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen. (`FACT_BAFIN_TURBO`, belegt, Konfidenz 0,85)
- BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023. (`FACT_BAFIN_STUDY`, Medienangabe, Konfidenz 0,65)
- Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG. (`FACT_PRIIPS_UWG`, belegt, Konfidenz 0,75)
- Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG. (`FACT_ANGEMESSENHEIT`, belegt, Konfidenz 0,7)

#### Modul 7 · Strategische Produkt-Roadmap [SZENARIO]

- Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge. (`FACT_ROADMAP`, SCENARIO_PROJECTION, keine Prognose-Konfidenz)

<!-- /sync:MOD -->

### 3.8 Modellrechnung [MODELL]

Die Berechnungslogik der Indikatoren ist in den eingesehenen Herstellerquellen nicht dokumentiert (`FACT_XRAY_10_IND`). Die folgenden Formeln sind die
fachübliche Referenzmodellierung und nicht die belegte Implementierung des Herstellers (`FACT_DEALER_CONVENTION`,
`FACT_GEX_EXAMPLE`).

Ausgangspunkt ist das Dollar-Gamma je Strike. Es gibt an, um wie viele Dollar sich das Hedge-Delta der
Dealer bei einer Bewegung des Basiswerts um ein Prozent verändert:

$$
GEX_K \;=\; \sum_{i \in K} s_i \cdot \Gamma_i \cdot OI_i \cdot M \cdot S^2 \cdot 0{,}01
$$

Dabei ist $\Gamma_i$ das Black-Scholes-Gamma der Option $i$ je Indexpunkt, $OI_i$ ihr Open Interest in
Kontrakten, $M$ der Kontraktmultiplikator (SPX: 100; `FACT_CONTRACT_SPECS`) und $S$ der Indexstand. $s_i \in \{+1,-1\}$ ist die
angenommene Dealer-Position: $+1$ steht für Dealer long, $-1$ für Dealer short. Die Summe über alle Strikes
ergibt das Netto-Gamma-Exposure. Der Preis, bei dem es das Vorzeichen wechselt, ist der **GEX-Flip**
(auch Zero Gamma).

Ökonomisch liegt der Unterschied zwischen Dämpfung und Beschleunigung im Vorzeichen der Hedge-Reaktion. Ein
Dealer, der netto long Gamma ist, erhält bei steigenden Kursen zusätzliches Long-Delta und verkauft Futures,
um neutral zu bleiben. Bei fallenden Kursen kauft er. Sein Hedging wirkt gegen die Bewegung und verringert
die realisierte Volatilität. Im Short-Gamma-Regime kehrt sich das um: Der Dealer muss steigenden Kursen
hinterherkaufen und fallenden hinterherverkaufen. Sein Hedging verstärkt die Bewegung. Daraus folgt modellgemäß der
Effekt zweiter Ordnung, der für Orderflow-Händler entscheidend ist. Prozyklische Hedge-Orders treffen auf
ein Orderbuch, aus dem Market Maker in Stressphasen ihre Limits zurückziehen. Die Markttiefe sinkt also
gerade dann, wenn der Hedge-Bedarf steigt. Als Effekt dritter Ordnung kann die gestiegene realisierte
Volatilität die implizite Volatilität anheben. Über Vanna verschiebt das die Deltas erneut und erzeugt
weiteren Hedge-Bedarf.

Diese Volatilitätsrückkopplung beschreibt **Vanna**, die Sensitivität des Deltas gegenüber der impliziten
Volatilität:

$$
\text{Vanna} \;=\; \frac{\partial \Delta}{\partial \sigma} \;=\; -e^{-q\tau}\,\varphi(d_1)\,\frac{d_2}{\sigma}
$$

**Charm** ist die zeitliche Änderung des Deltas. Hier wird die Konvention $\text{Charm} = \partial\Delta/\partial t
= -\partial\Delta/\partial\tau$ verwendet, mit $\tau$ als Restlaufzeit in Jahren. Für einen Call gilt im
Black-Scholes-Merton-Modell mit Dividendenrendite $q$ und Zins $r$:

$$
\text{Charm}_{C} \;=\; q\,e^{-q\tau}N(d_1) \;-\; e^{-q\tau}\,\varphi(d_1)\,
\frac{2(r-q)\tau - d_2\,\sigma\sqrt{\tau}}{2\tau\,\sigma\sqrt{\tau}}
$$

Für den Put gilt $\text{Charm}_P = \text{Charm}_C - q\,e^{-q\tau}$. Mit
$d_{1,2} = \frac{\ln(S/K) + (r - q \pm \sigma^2/2)\tau}{\sigma\sqrt{\tau}}$ steht $\varphi$ für die Dichte und
$N$ für die Verteilungsfunktion der Standardnormalverteilung.

Charm erklärt einen Flow, der allein durch den Zeitablauf entsteht. Bei sehr kurzer Restlaufzeit, also im
0DTE-Segment, fällt der Betrag des Deltas aus dem Geld liegender Optionen rasch gegen null. Halten Dealer
modellgemäß Short-Puts aus Absicherungskäufen der Kunden **[MODELL]**, sind sie netto long Delta und dagegen
short Futures abgesichert. Verliert das Put-Delta im Tagesverlauf an Betrag, müssen sie diese
Futures-Absicherung zurückkaufen. Das ist der oft beschriebene stützende Charm-Flow in den Handelsschluss
und vor Verfallsterminen. Die Charm Heatmap projiziert diesen zeitgetriebenen Hedge-Bedarf über Preis und
Zeit. Ihr Nutzen hängt allerdings vollständig von der Richtigkeit der Positionsannahme $s_i$ ab (K3).

Die Umrechnung in **ES-Äquivalente** macht die Größen für Futures-Händler lesbar. Das Hedge-Delta der Dealer
in Indexeinheiten ist $\sum_i s_i\,\Delta_i\,OI_i\,M_{SPX}$. Geteilt durch den ES-Multiplikator ergibt sich
die Kontraktzahl (Multiplikatoren: `FACT_CONTRACT_SPECS`):

$$
N_{ES} \;=\; \frac{\sum_i s_i\,\Delta_i\,OI_i\,M_{SPX}}{M_{ES}}, \qquad M_{SPX}=100,\; M_{ES}=50,\; M_{MES}=5
$$

Bei der Umrechnung ist die Basis zwischen SPX-Kassaindex und ES-Future zu beachten, also Zinsen minus
Dividenden bis zum Futures-Verfall. Preisniveaus aus der SPX-Kette müssen mit dieser Basis auf den ES-Chart
verschoben werden, sonst liegen die Walls um die Basis versetzt.

**Zahlenbeispiel [SZENARIO, hypothetische Werte; `FACT_GEX_EXAMPLE`]:** Angenommen sind ein SPX-Stand $S = 6.500$, ein Strike mit
$OI = 10.000$ Calls, $\Gamma = 0{,}0020$ je Punkt und Dealer long ($s = +1$). Dann gilt
$\Gamma\cdot OI\cdot M = 0{,}002 \cdot 10.000 \cdot 100 = 2.000$ Indexeinheiten Delta je Punkt. Eine
Bewegung von 1 % entspricht $65$ Punkten. Daraus ergibt sich eine Delta-Änderung von $2.000 \cdot 65 =
130.000$ Indexeinheiten, in Dollar $GEX = 2.000 \cdot 6.500^2 \cdot 0{,}01 = 845$ Mio. USD. In
ES-Äquivalenten sind das $130.000 / 50 = 2.600$ ES-Kontrakte oder $26.000$ MES. Probe:
$2.600 \cdot 50 \cdot 6.500 = 845$ Mio. USD. Im Long-Gamma-Fall würden Dealer bei einem Anstieg um 1 %
modellgemäß rund 2.600 ES verkaufen. Ob diese Menge das Orderbuch spürbar bewegt, hängt von der
Markttiefe in diesem Moment ab. Dieses Bindeglied liefert erst die Kombination mit MBO- und
Footprint-Daten (Modul 4).

---

## 4 · Modul 8: Fazit und Synthese

<!-- sync:FAZIT -->
#### Modul 8 · Fazit und Synthese [Einschätzung, aus dem Fazit der Modulseite]

**✓ Bleibt**

- X-Ray zeigt aus SPX-Optionsdaten abgeleitete Kennzahlen auf ES, MES und SPY an. (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85)
- Minuten-Snapshots lösen das Skalierungsproblem, kosten aber Aktualität bei Makro-Events. (Einschätzung, gestützt auf (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7))
- Für Optionen fehlt eine native Ausführung. (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8)
- Positionierung plus MBO in einer Oberfläche: für ATAS belegt (MBO-Bundle zur Erprobung); Bookmap hat MBO und Greeks nur über Add-ons; für SpotGamma, MenthorQ, Volland und TWS ist ein MBO-Werkzeug n. v. Ob die Kombination ein Differenzierungsmerkmal ist, bleibt damit offen. (Einschätzung, gestützt auf (`FACT_SPOTGAMMA_SPEC`, belegt, Konfidenz 0,75), (`FACT_MENTHORQ_SPEC`, belegt, Konfidenz 0,75), (`FACT_VOLLAND_SPEC`, Medienangabe, Konfidenz 0,65), (`FACT_BOOKMAP_SPEC`, belegt, Konfidenz 0,75), (`FACT_TWS_SPEC`, belegt, Konfidenz 0,75), (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_ATAS_MBO`, belegt, Konfidenz 0,8))

**◐ Relativiert**

- Market Maker hedgen aus Kalkül, nicht aus gesetzlichem Zwang. (Einschätzung, gestützt auf (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85))
- GEX beruht auf einer Positionsannahme; beim SPX durch markierte Cboe-Daten besser, anderswo schwächer fundiert. (Einschätzung, gestützt auf (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, keine Prognose-Konfidenz), (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6))
- Optionsscheine hinterlassen eine schwache, nicht zurechenbare Hedge-Spur, aber keine Nullspur. (Einschätzung, gestützt auf (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6))

**✗ Entfällt**

- Ein steuerlicher Nachteil börsengehandelter Optionen gegenüber Optionsscheinen im Privatvermögen. (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9)
- „Keine Verlustbeschränkung“ für Kapitalgesellschaften. (`FACT_P15_KSTG`, belegt, Konfidenz 0,85)

**Strategische These [SZENARIO]:** Der Wert einer Eurex-Erweiterung läge nicht in einem Steuervorteil, sondern in einer möglichen Analyselücke. Für ODAX und OESX ist von sechs verglichenen Anbietern nur für einen bestimmbar, dass er in den ausgewerteten Funktionen keine intraday-fähige Eurex-GEX bietet, für ATAS selbst; für SpotGamma, MenthorQ, Volland, Bookmap und die IBKR TWS ist das n. v.. Für die GEX-Spezialisten ist damit offen, ob eine Lücke besteht; ob ATAS sie füllen kann, hängt von Datenlizenzen, Validierung und der offenen Kommunikation der schwächeren Positionsannahme ab. (`FACT_NO_EUREX_GEX`, belegt, Konfidenz 0,75) (`FACT_ROADMAP`, SCENARIO_PROJECTION, keine Prognose-Konfidenz)

<!-- /sync:FAZIT -->

---

## 5 · Glossar

<!-- sync:GLOSSAR -->
| Begriff | Definition (Fortgeschritten) | Einordnung (Experte) |
|---|---|---|
| Delta | Erste Ableitung des Optionspreises nach dem Basiswert. | $\Delta=\partial V/\partial S$; Grundlage jeder Hedge-Menge. |
| Gamma | Zweite Ableitung des Optionspreises nach dem Basiswert. | $\Gamma=\partial^2 V/\partial S^2$; bestimmt den Nachsicherungsbedarf. |
| Open Interest | Bestand nicht glattgestellter Kontrakte je Serie. | Eurex veröffentlicht es täglich je Serie; Basis der GEX-Profile. (`FACT_EUREX_OI`, belegt, Konfidenz 0,85) |
| Implizite Volatilität | Aus dem Optionspreis zurückgerechnete Volatilität. | Fläche über Strike und Laufzeit; Eingang für Vanna-Effekte. |
| Delta-Divergenz | Abweichung zwischen Preisverlauf und kumuliertem Delta. | Schwächeres Umkehrsignal im Short-Gamma-Regime. |
| BAG / Combo-Order | IB-Ordertyp für Spreads mit Netto-Limit. | Schützt vor Legging-Risiko; in ATAS derzeit nicht integriert. (`FACT_IB_BAG`, belegt, Konfidenz 0,85) (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8) |
| Angemessenheitsprüfung | Abfrage von Kenntnissen und Erfahrungen vor dem Handel. | Für komplexe Produkte vorgeschrieben. (`FACT_ANGEMESSENHEIT`, belegt, Konfidenz 0,7) |
| Optionsschein | Verbriefte Option, vom Emittenten ausgegeben. | Emittentenrisiko: Der Wert hängt von der Bonität des Emittenten ab. (`FACT_OS_ISSUER`, Medienangabe, Konfidenz 0,7) |
| 0DTE | Zero Days to Expiration; beim SPX an jedem Wochentag. | Großer Teil des SPX-Volumens (Kennzahl in Modulseite S01); erzeugt Intraday-Positionen ohne OI-Spur. (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8) (`FACT_SPX_0DTE_59`, belegt, Konfidenz 0,85) |
| GEX | Gamma Exposure: aggregiertes Dollar-Gamma der Dealer-Positionen. | $\sum s_i\Gamma_i OI_i M S^2\cdot 0{,}01$; Vorzeichen hängt an der Positionsannahme. |
| GEX-Flip | Preis, an dem das Netto-Gamma das Vorzeichen wechselt. | Grenze zwischen dämpfendem und verstärkendem Hedging-Regime. |
| Call/Put Wall | Strikes mit der höchsten Call- bzw. Put-Gamma-Konzentration. | Modellhafte Widerstands-/Unterstützungszonen; keine Preisgarantie. |
| Charm | Änderung des Deltas pro Zeiteinheit. | $\partial\Delta/\partial t$; stark bei 0DTE und vor Verfall. |
| Vanna | Änderung des Deltas pro Änderung der impliziten Volatilität. | $\partial\Delta/\partial\sigma$; treibt Flows nach IV-Crush/-Spikes. |
| ES-Äquivalent | Hedge-Delta geteilt durch den ES-Multiplikator (50). | SPX-Multiplikator 100 / ES 50 / MES 5; Basis SPX↔ES beachten. (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8) |
| OPRA | Options Price Reporting Authority. | Projizierte Spitzenlast je Stream im Gbit/s-Bereich (Kennzahlen in Modulseite S07). (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7) |
| MBO | Market by Order (Level 3). | Erlaubt Queue-Position, Iceberg- und Sweep-Erkennung. |
| Footprint | Volumen getrennt nach Bid/Ask je Kerze. | Grundlage für Absorption und Delta-Divergenz. |
| Absorption | Aggressives Volumen wird von passiven Orders aufgenommen. | Bestätigungssignal für Wall-Thesen im Long-Gamma-Regime. |
| Sweep | Aggressive Order über mehrere Levels in einem Zug. | Widerlegungssignal für Wall-Thesen; oft Short-Gamma-Beschleunigung. |
| Iceberg | Order mit verdecktem Volumen, die nachgefüllt wird. | Im MBO über wiederholte Ausführungen derselben Order-ID erkennbar. |
| Termingeschäft (steuerlich) | Options-, Futures- oder Swapgeschäft mit Differenzausgleich oder Lieferung; Einkünfte nach § 20 EStG. | Im Privatvermögen keine gesonderte Verlustverrechnungsbeschränkung (JStG 2024). (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9) |
| Knock-out-Zertifikat | Hebelprodukt mit Knock-out-Barriere; Ausgestaltung hier n. v. | Für Turbos gilt eine BaFin-Allgemeinverfügung (Details in Modulseite S10). (`FACT_BAFIN_TURBO`, belegt, Konfidenz 0,85) |
| CCP | Central Counterparty, hier Eurex Clearing. | Ersetzt bilaterales Kontrahentenrisiko; Teilnehmer hinterlegen Sicherheiten (Margin). (`FACT_CCP_ISSUER`, belegt, Konfidenz 0,8) |
| PRIIPs-KID | EU-Basisinformationsblatt (VO (EU) 1286/2014). | Referenz für Kostenvergleiche verbriefter Derivate. (`FACT_PRIIPS_UWG`, belegt, Konfidenz 0,75) |
| Quartalsverfall | Dritter Freitag der Quartalsmonate. | Umgangssprachlich „Hexensabbat“; OI-Verschiebungen davor relevant. (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8) |

<!-- /sync:GLOSSAR -->

---

## 6 · Quellenverzeichnis

Recherchiert vom 2026-10-05 bis 2026-10-11 über Suchtreffer; der Herausgeber hat am 2026-10-11 Primär- und
Herstellerquellen am Original abgeglichen, ausgenommen die fünf Medienangaben (an ihrer Sekundärquelle), den
abgeleiteten Quantor `FACT_NO_EUREX_GEX` (siehe Methodischer Vorbehalt) und die GEX-Metrix-Momentaufnahme nach dem
Stichtag vom 2026-10-23, die auf einer Bildschirmkopie des Herausgebers beruht (`FACT_GEXMETRIX_SPX`), mit daraus
berechneten Differenzen und der ungeprüften Wall-Ablesung (`FACT_GEXMETRIX_WALLS_READ`). Das Verzeichnis ist ein
Auszug aus `provenance/m300.dbom.json` (Lehre L13/L14) und wird von dort erzeugt, nicht von Hand gepflegt. Die
S-Nummern sind die Belegverweise in dieser Analyse. „abgeglichen“ nennt das Datum, an dem der Herausgeber Fakten
dieser Quelle zuletzt geprüft hat; sonst gilt der Recherchezeitraum.

<!-- sync:QUELLEN -->
### Primärquellen

| Nr. | Quelle | DBOM-ID | Abruf / Abgleich | URL |
|---|---|---|---|---|
| S1 | Jahressteuergesetz 2024, BGBl. 2024 I Nr. 387 | `SRC_BGBL_JSTG2024` | abgeglichen 2026-10-11 | https://www.recht.bund.de/bgbl/1/2024/387/regelungstext.pdf |
| S2 | BT-Drs. 20/13419, 20/13420, 20/12780 (JStG 2024) | `SRC_BT_DRS` | abgeglichen 2026-10-11 | https://dserver.bundestag.de/btd/20/134/2013420.pdf |
| S9 | BaFin · Allgemeinverfügung Turbo-Zertifikate | `SRC_BAFIN_TURBO` | abgeglichen 2026-10-11 | https://www.bafin.de/SharedDocs/Downloads/DE/Aufsichtsrecht/Verfuegungen/dl_vf_allgemeinverfuegung_turbo_zertifikate.html |
| S10 | BaFin · FAQ HFT-Gesetz | `SRC_BAFIN_HFT` | abgeglichen 2026-10-11 | https://www.bafin.de/SharedDocs/FAQs/DE/HFT-Gesetz/160_hft_faq.html |
| S11 | § 80 WpHG (Abs. 2 algorithmischer Handel; Abs. 4 Market-Making-Pflichten; Abs. 5 Definition) | `SRC_WPHG_80` | abgeglichen 2026-10-11 | https://www.gesetze-im-internet.de/wphg/__80.html |
| S13 | § 15 EStG | `SRC_ESTG_15` | abgeglichen 2026-10-11 | https://www.gesetze-im-internet.de/estg/__15.html |
| S14 | BFH, Urteil v. 06.07.2016, I R 25/14 | `SRC_BFH_IR2514` | abgeglichen 2026-10-11 | https://www.bundesfinanzhof.de/en/entscheidungen/entscheidungen-online/decision-detail/STRE201610211/ |
| S29 | Eurex · Produktseiten und Kontraktspezifikationen DAX-Optionen (ODAX), Micro-DAX-Optionen (ODXS), EURO STOXX 50 Options | `SRC_EUREX_SPECS` | abgeglichen 2026-10-11 | https://www.eurex.com/ex-en/markets/idx/dax/DAX-Options-139884 |
| S30 | Eurex Circulars OEXP 047/23 und 117/25 | `SRC_EUREX_CIRCULARS` | abgeglichen 2026-10-11 | https://www.eurex.com/ex-en/find/circulars/circular-4844340 |
| S32 | Cboe · Trading Volume December and Full Year 2025 | `SRC_CBOE_FY2025` | abgeglichen 2026-10-11 | https://ir.cboe.com/news/news-details/2026/Cboe-Global-Markets-Reports-Trading-Volume-for-December-and-Full-Year-2025/default.aspx |
| S33 | OPRA · Capacity Projections Update (Sept. 2025) | `SRC_OPRA` | abgeglichen 2026-10-11 | https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf |
| S35 | Delegierte VO (EU) 2016/958 (Anlageempfehlungen) | `SRC_DELVO_958` | abgeglichen 2026-10-11 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0958 |
| S44 | VO (EU) Nr. 1286/2014 (PRIIPs) | `SRC_PRIIPS` | abgeglichen 2026-10-11 | https://eur-lex.europa.eu/eli/reg/2014/1286/oj |
| S46 | Eurex · Daily Options (OEXP/ODAP) | `SRC_EUREX_DAILY` | abgeglichen 2026-10-11 | https://www.eurex.com/ex-en/markets/idx/daily-opt |
| S47 | § 63 WpHG (Wohlverhaltenspflichten) | `SRC_WPHG_63` | abgeglichen 2026-10-11 | https://www.gesetze-im-internet.de/wphg/__63.html |
| S50 | Eurex · Statistiken / Extended Market Data Service (Open Interest) | `SRC_EUREX_STATS` | abgeglichen 2026-10-11 | https://www.eurex.com/ex-en/data/statistics |
| S51 | Cboe · S&P 500 Index Options (SPX/SPXW) Product Specifications | `SRC_CBOE_SPX` | abgeglichen 2026-10-11 | https://www.cboe.com/tradable-products/sp-500/spx-options/spx-specifications |
| S52 | CME Group · Micro E-mini Equity Index Futures – Products Overview | `SRC_CME_MICRO` | abgeglichen 2026-10-11 | https://www.cmegroup.com/education/courses/understanding-micro-futures-contracts-at-cme-group/micro-e-mini-futures/micro-e-mini-equity-index-futures-products-overview.html |
| S54 | Eurex · EURO STOXX 50 Index Options Contract Specifications | `SRC_EUREX_OESX_SPEC` | abgeglichen 2026-10-11 | https://www.eurex.com/ex-en/markets/idx/stx/euro-stoxx-50-derivatives/products/EURO-STOXX-50-Index-Options-46548 |
| S55 | BaFin · Zulassung der Eurex Clearing AG als zentrale Gegenpartei nach EMIR (10.04.2014) | `SRC_BAFIN_EUREX_CLEARING` | abgeglichen 2026-10-11 | https://bafin.de/SharedDocs/Veroeffentlichungen/EN/Meldung/2014/meldung_140410_emir_erlaubnis_eurex_en.html |

### Herstellerquellen

| Nr. | Quelle | DBOM-ID | Abruf / Abgleich | URL |
|---|---|---|---|---|
| S15 | ATAS Hilfe · Options X-Ray | `SRC_ATAS_HELP` | abgeglichen 2026-10-11 | https://help.atas.net/en/support/solutions/articles/72000662222-options-x-ray-expected-move |
| S16 | ATAS Learn · Options | `SRC_ATAS_LEARN` | abgeglichen 2026-10-11 | https://learn.atas.net/options/ |
| S17 | ATAS Changelog | `SRC_ATAS_CHANGELOG` | abgeglichen 2026-10-11 | https://feedback.atas.net/changelog |
| S18 | ATAS Hilfe · Options Chain Suite / GEX Profile | `SRC_ATAS_CHAIN` | abgeglichen 2026-10-11 | https://help.atas.net/en/support/solutions/articles/72000661536-options-gex-profile |
| S19 | ATAS · Connections | `SRC_ATAS_CONNECTIONS` | abgeglichen 2026-10-11 | https://atas.net/connections/ |
| S20 | ATAS 8.0.12 · Cross-Trading | `SRC_ATAS_8012` | abgeglichen 2026-10-11 | https://help.atas.net/en/support/solutions/articles/72000657084-cross-trading |
| S21 | ATAS Changelog · MBO-Bundle und Optionsanalyse | `SRC_ATAS_MBO` | abgeglichen 2026-10-11 | https://feedback.atas.net/changelog/new-mbo-bundle-and-options-analysis-are-now-in-atas |
| S22 | IB TWS API · Spread Contracts | `SRC_IB_API` | abgeglichen 2026-10-11 | https://interactivebrokers.github.io/tws-api/spread_contracts.html |
| S23 | SpotGamma (HIRO) | `SRC_SPOTGAMMA` | abgeglichen 2026-10-11 | https://spotgamma.com/hiro-indicator/ |
| S24 | MenthorQ (Abdeckung) | `SRC_MENTHORQ` | abgeglichen 2026-10-11 | https://menthorq.com/guide/menthorq-asset-coverage/ |
| S26 | Bookmap (Konnektivität) | `SRC_BOOKMAP` | abgeglichen 2026-10-11 | https://bookmap.com/en/packages-comparison |
| S27 | Interactive Brokers · OptionTrader / TWS | `SRC_IBKR` | abgeglichen 2026-10-11 | https://www.interactivebrokers.com/en/software/pdfhighlights/PDF-OptionTrader.php |
| S28 | Gamma Cockpit (DAX-GEX, Beta) | `SRC_GAMMACOCKPIT` | abgeglichen 2026-10-11 | https://gammacockpit.com/ |
| S49 | OptionsDepth (Abdeckung, API) | `SRC_OPTIONSDEPTH` | abgeglichen 2026-10-11 | https://optionsdepth.com/ |
| S59 | ATAS · Footprint-Charts (Volumenanalyse) | `SRC_ATAS_FOOTPRINT` | abgeglichen 2026-10-11 | https://atas.net/volume-analysis/footprint-charts/ |
| S60 | GEX-Metrix Dashboard · SPX (Bildschirmkopie des Herausgebers, 2026-10-23 05:28 ET; Bild nicht auf der Seite und in keinem Branch des Repositorys, SHA-256 e4b56d890e706e8c…) | `SRC_GEXMETRIX` | abgeglichen 2026-10-23 | https://www.gexmetrix.com/gex/spx |

### Sekundärquellen

| Nr. | Quelle | DBOM-ID | Abruf / Abgleich | URL |
|---|---|---|---|---|
| S12 | Emittenten-Hedging (Morgan Stanley Produktwissen, ideas-Magazin; Sekundärquellen) | `SRC_ISSUER_HEDGE` | abgeglichen 2026-10-11 | https://zertifikate.morganstanley.com/services/produktwissen/optionsscheine/ |
| S25 | Volland (ORATS-Partnerseite, User Guide) | `SRC_VOLLAND` | abgeglichen 2026-10-11 | https://orats.com/volland |
| S36 | CMS · Verlustverrechnung bei Termingeschäften nach dem JStG 2024 (Sekundärquelle) | `SRC_CMS` | abgeglichen 2026-10-11 | https://cms.law/de/deu/legal-updates/Ade-Verlustabzugsbeschraenkung-fuer-Termingeschaefte-Gesetzgeber-bereinigt-Verfassungswidrigkeit |
| S42 | MenthorQ · Cboe Market-Maker-Tagged Data erklärt (Sekundärquelle) | `SRC_MENTHORQ_GUIDE` | abgeglichen 2026-10-11 | https://menthorq.com/guide/cboe-market-maker-tagged-data-explained/ |
| S48 | Sutor Bank · Formular Angemessenheit nach § 63 Abs. 10 WpHG (Sekundärquelle) | `SRC_SUTOR` | abgeglichen 2026-10-11 | https://www.sutorbank.de/fileadmin/Dateien/Service/Formulare/Investmentsparvertraege/Angaben-zur-Feststellung-der-Angemessenheit.pdf |
| S56 | Deutsche Börse · Clearing: zentrale Gegenpartei und Sicherheiten (Margin) | `SRC_DB_CLEARING` | abgeglichen 2026-10-11 | https://www.deutsche-boerse-cash-market.com/resource/blob/244872/f8a90e944e2f40c38cabcf6420dde59c/data/db-aktuell-clearing-may2018_de.pdf.pdf |
| S57 | Deutscher Derivate Verband · Muster-Produktinformation Call-Optionsschein | `SRC_DDV_OS_MUSTER` | abgeglichen 2026-10-11 | https://www.derivateverband.de/DE/MediaLibrary/Document/Muster/Call%20Optionsschein-d.pdf |
| S58 | Stiftung Warentest · Studie zu Turbo-Zertifikaten: Die meisten Anleger machen Verluste | `SRC_TESTDE_TURBO` | abgeglichen 2026-10-11 | https://www.test.de/Studie-zu-Turbo-Zertifikaten-Die-meisten-Anleger-machen-mit-Turbo-Zertifikaten-Verluste-6227752-0/ |

<!-- /sync:QUELLEN -->

---

## 7 · M-DBOM (Data Bill of Materials)

Führende Provenienzliste ist **`provenance/m300.dbom.json`** (Lehre L13: eine DBOM für Seite und Analyse).

**M-DBOM als JSON-LD** (Schema des Modul-Prompts, aus `provenance/m300.dbom.json` erzeugt und byte-genau geprüft):
Jeder Fakt trägt genau ein Provenienz-Tag (`provenance`, Schema des Prompts; UNVERIFIED nach Q4 für ungeprüfte
Angaben). Die feinere Einordnung der M-DBOM (`verdict`, `class`, `evidence`) steht getrennt unter `x-m-dbom`.
`retrieved` ist das Datum des Abgleichs durch den Herausgeber, sonst `null`.
Die Zählung der Tags weicht bewusst von den Zählungen der Seite ab: Die Seite zählt „belegt“ nach dem Verdict
CONFIRMED (Primär-, Hersteller- und abgeleitete Fakten zusammen), das Tag `provenance` trennt dagegen Herstellerangaben
(VENDOR_CLAIM) von den übrigen bestätigten Fakten (CONFIRMED).

<!-- sync:JSONLD -->
```json
{
 "@context": "https://schema.org",
 "@type": "Dataset",
 "name": "M300 · M-DBOM v1",
 "dateModified": "2026-10-05",
 "version": "1.22.0",
 "facts": [
  {
   "id": "FACT_JSTG2024_REPEAL",
   "claim": "Verluste aus Termingeschäften im Privatvermögen unterliegen keiner gesonderten Verlustverrechnungsbeschränkung; es gelten die allgemeinen Regeln für Einkünfte aus Kapitalvermögen (§ 20 Abs. 6 EStG in der Fassung des JStG 2024, BGBl. 2024 I Nr. 387). Daraus folgt: Börsengehandelte Optionen und Optionsscheine werden insoweit nicht unterschiedlich behandelt.",
   "provenance": "CONFIRMED",
   "confidence": 0.9,
   "source": "https://www.recht.bund.de/bgbl/1/2024/387/regelungstext.pdf",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_P15_KSTG",
   "claim": "§ 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.gesetze-im-internet.de/estg/__15.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_MM_NO_HEDGE_DUTY",
   "claim": "Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.gesetze-im-internet.de/wphg/__80.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ALGO_TRADING",
   "claim": "§ 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II).",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.gesetze-im-internet.de/wphg/__80.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_MAR_RECO",
   "claim": "Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0958",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_PRIIPS_UWG",
   "claim": "Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG.",
   "provenance": "CONFIRMED",
   "confidence": 0.75,
   "source": "https://eur-lex.europa.eu/eli/reg/2014/1286/oj",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ANGEMESSENHEIT",
   "claim": "Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG.",
   "provenance": "CONFIRMED",
   "confidence": 0.7,
   "source": "https://www.gesetze-im-internet.de/wphg/__63.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_BAFIN_TURBO",
   "claim": "BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.bafin.de/SharedDocs/Downloads/DE/Aufsichtsrecht/Verfuegungen/dl_vf_allgemeinverfuegung_turbo_zertifikate.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_BAFIN_STUDY",
   "claim": "BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023.",
   "provenance": "MEDIA_REPORT",
   "confidence": 0.65,
   "source": "https://www.test.de/Studie-zu-Turbo-Zertifikaten-Die-meisten-Anleger-machen-mit-Turbo-Zertifikaten-Verluste-6227752-0/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "MEDIA_REPORT",
    "class": "MEDIA_REPORT",
    "evidence": "secondary"
   }
  },
  {
   "id": "FACT_XRAY_10_IND",
   "claim": "Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile).",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://help.atas.net/en/support/solutions/articles/72000662222-options-x-ray-expected-move",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_XRAY_1MIN_SPX",
   "claim": "Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://learn.atas.net/options/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_OPTIONSDEPTH_SCOPE",
   "claim": "OptionsDepth deckt derzeit nur SPX und VIX ab.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://optionsdepth.com/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_XRAY_CONNECTIVITY",
   "claim": "Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.7,
   "source": "https://feedback.atas.net/changelog",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ATAS_CONNECTIONS",
   "claim": "ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://atas.net/connections/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_CHAIN_SUITE",
   "claim": "Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://help.atas.net/en/support/solutions/articles/72000661536-options-gex-profile",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ATAS_NO_OPT_TRADING",
   "claim": "Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan).",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.8,
   "source": "https://learn.atas.net/options/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ATAS_MBO",
   "claim": "Laut ATAS-Changelog vom 04.08.2026 ist ein MBO-Bundle (Iceberg-, Stop-Runs- und Sweeps-Tracker) für Ultra-Nutzer zur Erprobung verfügbar; MBO-Daten erfordern eine Rithmic-Anbindung.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.8,
   "source": "https://feedback.atas.net/changelog/new-mbo-bundle-and-options-analysis-are-now-in-atas",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ATAS_FOOTPRINT",
   "claim": "ATAS bietet Footprint-Charts (Cluster-Charts) auf Basis von Tick-Daten der Börse mit Darstellungen wie Volumen, Bid × Ask und Delta.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.8,
   "source": "https://atas.net/volume-analysis/footprint-charts/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_CROSS_TRADING",
   "claim": "ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026).",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://help.atas.net/en/support/solutions/articles/72000657084-cross-trading",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_IB_BAG",
   "claim": "IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.85,
   "source": "https://interactivebrokers.github.io/tws-api/spread_contracts.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_CBOE_OPENCLOSE",
   "claim": "SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt.",
   "provenance": "MEDIA_REPORT",
   "confidence": 0.6,
   "source": "https://menthorq.com/guide/cboe-market-maker-tagged-data-explained/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "MEDIA_REPORT",
    "class": "MEDIA_REPORT",
    "evidence": "secondary"
   }
  },
  {
   "id": "FACT_SPX_0DTE_59",
   "claim": "Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://ir.cboe.com/news/news-details/2026/Cboe-Global-Markets-Reports-Trading-Volume-for-December-and-Full-Year-2025/default.aspx",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_OPRA_CAPACITY",
   "claim": "OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster.",
   "provenance": "CONFIRMED",
   "confidence": 0.7,
   "source": "https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ODAX_SPECS",
   "claim": "ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.eurex.com/ex-en/markets/idx/dax/DAX-Options-139884",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_EUREX_OI",
   "claim": "Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.eurex.com/ex-en/data/statistics",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_OESX_MULT",
   "claim": "OESX (EURO-STOXX-50-Indexoptionen): 10 € je Indexpunkt, europäisch, Barausgleich.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.eurex.com/ex-en/markets/idx/stx/euro-stoxx-50-derivatives/products/EURO-STOXX-50-Index-Options-46548",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_EUREX_DAILY_LAUNCH",
   "claim": "Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen.",
   "provenance": "CONFIRMED",
   "confidence": 0.85,
   "source": "https://www.eurex.com/ex-en/find/circulars/circular-4844340",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_ISSUER_HEDGING",
   "claim": "Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte.",
   "provenance": "MEDIA_REPORT",
   "confidence": 0.6,
   "source": "https://zertifikate.morganstanley.com/services/produktwissen/optionsscheine/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "MEDIA_REPORT",
    "class": "MEDIA_REPORT",
    "evidence": "secondary"
   }
  },
  {
   "id": "FACT_SPOTGAMMA_SPEC",
   "claim": "SpotGamma – Gamma-Levels, Research · HIRO/TRACE intraday, Levels vor Eröffnung · GEX ja, Vanna als Modell, Charm n. v. · Abdeckung SPX, NDX, ETFs, Einzelaktien · Orderflow/MBO n. v. · keine eigene Ausführung.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://spotgamma.com/hiro-indicator/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_MENTHORQ_SPEC",
   "claim": "MenthorQ – Gamma-Levels, Modelle, Ausbildung · Optionsdaten EOD und alle 5 Min. · GEX ja, Vanna und Charm n. v. · Abdeckung inkl. Futures-Optionen (Umfang n. v.) · Orderflow/MBO n. v. · Ausführung über Partnerplattformen · Eurex-GEX n. v..",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://menthorq.com/guide/menthorq-asset-coverage/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_VOLLAND_SPEC",
   "claim": "Volland – Notional-Greeks Dealer-Buch · Optionsdaten EOD bis alle 5 Min. · Gamma, Vanna und Charm · Abdeckung Auswahl nach Notional (Umfang n. v.) · Orderflow/MBO n. v. · Ausführung n. v..",
   "provenance": "MEDIA_REPORT",
   "confidence": 0.65,
   "source": "https://orats.com/volland",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "MEDIA_REPORT",
    "class": "MEDIA_REPORT",
    "evidence": "secondary"
   }
  },
  {
   "id": "FACT_BOOKMAP_SPEC",
   "claim": "Bookmap – Orderbuch-Heatmap, Ausführung · keine nativen Optionsdaten · Greeks nur über Add-ons · Abdeckung Futures, Aktien, Krypto · Heatmap, MBO via Rithmic · eigene Ausführung.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://bookmap.com/en/packages-comparison",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_TWS_SPEC",
   "claim": "IBKR TWS – Broker, Portfoliorisiko · Echtzeit-Optionsdaten (Abo) · aggregiertes Greek-Exposure nur für eigene Positionen · Abdeckung global inkl. ODAX/OESX · Orderflow/MBO n. v. · eigene Ausführung.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://www.interactivebrokers.com/en/software/pdfhighlights/PDF-OptionTrader.php",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_NO_EUREX_GEX",
   "claim": "Von sechs verglichenen Anbietern ist nur für einen bestimmbar, dass er keine intraday-fähige Eurex-GEX anbietet: In den ausgewerteten ATAS-Funktionen deckt Options X-Ray nur SPX ab und die Options Chain Suite nur ES, NQ, CL und GC auf EOD-Basis; für die übrigen fünf (SpotGamma, MenthorQ, Volland, Bookmap, IBKR TWS) n. v.",
   "provenance": "CONFIRMED",
   "confidence": 0.75,
   "source": "https://learn.atas.net/options/",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "DERIVED",
    "evidence": "derived"
   }
  },
  {
   "id": "FACT_GAMMACOCKPIT_SPEC",
   "claim": "Gamma Cockpit (nicht im Vergleichsfeld) liefert DAX-GEX nur auf Tagesbasis (Beta).",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://gammacockpit.com/",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_DEALER_CONVENTION",
   "claim": "GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls).",
   "provenance": "MODEL_ASSUMPTION",
   "confidence": null,
   "source": "SRC_MODEL",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "SCENARIO_PROJECTION",
    "class": "MODEL_ASSUMPTION",
    "evidence": "model"
   }
  },
  {
   "id": "FACT_GEX_EXAMPLE",
   "claim": "Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES.",
   "provenance": "SCENARIO_PROJECTION",
   "confidence": null,
   "source": "SRC_MODEL",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "SCENARIO_PROJECTION",
    "class": "SCENARIO_PROJECTION",
    "evidence": "model"
   }
  },
  {
   "id": "FACT_GEX_LEVELS_EXAMPLE",
   "claim": "Rechenbeispiel GEX-Marken: Index 7.740, GEX-Flip 7.675, Call Wall 7.800, Put Wall 7.600; Szenarien A (7.740 → 7.790), B (7.740 → 7.660) und C (7.660 → 7.600) mit modellhafter Dealer-Reaktion.",
   "provenance": "SCENARIO_PROJECTION",
   "confidence": null,
   "source": "SRC_MODEL",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "SCENARIO_PROJECTION",
    "class": "SCENARIO_PROJECTION",
    "evidence": "model"
   }
  },
  {
   "id": "FACT_GEXMETRIX_SPX",
   "claim": "GEX-Metrix (Intraday-Modell, Verfälle bis 2026-11-20, kostenlose Stufe mit 15 Minuten Verzögerung), Zeitstempel 2026-10-23 05:28 ET (vor Handelsbeginn): Indexstand 7.663,43; Zero Gamma (GEX-Flip) 7.861,0; Max Pain 7.725; Call-Gamma 61,56 und Put-Gamma 112,13 Mrd. USD je 1 %. Verlaufsgrafik: Gamma-Exposure bis 14.10.2026 positiv, danach überwiegend negativ, letzter Punkt deutlich negativer als die Differenz der Kopfwerte; Index von rund 7.800 auf 7.663,43.",
   "provenance": "VENDOR_CLAIM",
   "confidence": 0.75,
   "source": "https://www.gexmetrix.com/gex/spx",
   "retrieved": "2026-10-23",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "VENDOR_CLAIM",
    "evidence": "screenshot"
   }
  },
  {
   "id": "FACT_GEXMETRIX_DERIVED",
   "claim": "Aus FACT_GEXMETRIX_SPX berechnet: Differenz der Kopfwerte Call-Gamma minus Put-Gamma 61,56 − 112,13 = −50,57 Mrd. USD je 1 % (nicht der Netto-Wert des Anbieters); Abstand Index zum GEX-Flip 7.663,43 − 7.861,0 = −197,57 Punkte.",
   "provenance": "CONFIRMED",
   "confidence": 0.7,
   "source": "https://www.gexmetrix.com/gex/spx",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "DERIVED",
    "evidence": "derived"
   }
  },
  {
   "id": "FACT_GEXMETRIX_WALLS_READ",
   "claim": "Im angezeigten Strike-Bereich 7.625–7.850 der Bildschirmkopie ist der längste Call-Balken bei 7.800 und der längste Put-Balken bei 7.650; Strikes außerhalb des Ausschnitts sind nicht sichtbar, bei 7.800 und 7.750 sind die Call-Balken fast gleich lang.",
   "provenance": "UNVERIFIED",
   "confidence": 0.5,
   "source": "https://www.gexmetrix.com/gex/spx",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "UNVERIFIED",
    "class": "READING",
    "evidence": "screenshot"
   }
  },
  {
   "id": "FACT_ROADMAP",
   "claim": "Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge.",
   "provenance": "USER_PROVIDED",
   "confidence": null,
   "source": "SRC_USER_TEXT",
   "retrieved": null,
   "x-m-dbom": {
    "verdict": "SCENARIO_PROJECTION",
    "class": "SCENARIO_PROJECTION",
    "evidence": "model"
   }
  },
  {
   "id": "FACT_CONTRACT_SPECS",
   "claim": "Kontraktdaten: Multiplikator SPX 100 USD je Indexpunkt, SPXW-Optionen mit Verfällen an jedem Wochentag (0DTE möglich; Cboe); E-mini S&P 500 50 USD und Micro E-mini 5 USD je Indexpunkt (CME); Eurex-Standardoptionen auf Indizes (Monats- und Quartalsverfälle): letzter Handelstag ist der dritte Freitag des Verfallsmonats (Quartalsverfall im März, Juni, September und Dezember).",
   "provenance": "CONFIRMED",
   "confidence": 0.8,
   "source": "https://www.cboe.com/tradable-products/sp-500/spx-options/spx-specifications",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "MARKET_DATA",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_CCP_ISSUER",
   "claim": "Börsengehandelte Eurex-Optionen werden über die Eurex Clearing AG als zentrale Gegenpartei abgewickelt (Zulassung nach EMIR durch die BaFin am 10.04.2014); die Teilnehmer hinterlegen Sicherheiten (Margin).",
   "provenance": "CONFIRMED",
   "confidence": 0.8,
   "source": "https://bafin.de/SharedDocs/Veroeffentlichungen/EN/Meldung/2014/meldung_140410_emir_erlaubnis_eurex_en.html",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "CONFIRMED",
    "class": "REGULATORY_FRAMEWORK",
    "evidence": "fulltext"
   }
  },
  {
   "id": "FACT_OS_ISSUER",
   "claim": "Optionsscheine sind vom Emittenten ausgegebene Wertpapiere; ihr Wert hängt von dessen Bonität ab (Emittentenrisiko).",
   "provenance": "MEDIA_REPORT",
   "confidence": 0.7,
   "source": "https://www.derivateverband.de/DE/MediaLibrary/Document/Muster/Call%20Optionsschein-d.pdf",
   "retrieved": "2026-10-11",
   "x-m-dbom": {
    "verdict": "MEDIA_REPORT",
    "class": "MEDIA_REPORT",
    "evidence": "secondary"
   }
  }
 ]
}
```
<!-- /sync:JSONLD -->

## 8 · QA-Scorecard

> **Automatisch erzeugt** aus den Gate-Zellen von `m300.html` (`qa/sync_module.py`, L49). Nicht von Hand ändern.

| Gate | Status | Begründung |
|---|---|---|
| C1 Disclaimer Anfang/Ende | ✓ | Zweitprüfung: alle sechs Pflichtbestandteile in Hero, Schluss, Analyse Anfang/Ende gelesen; L42-Test · 24. Zweitprüfung 2026-10-27: Hero, Schluss und Analyse Anfang/Ende mit allen Pflichtbestandteilen |
| C2 Keine Anlageempfehlung (MAR) | ✓ | Keine Kursziele, Einstiege oder Empfehlungen (Zweitprüfung 2026-10-11 gelesen); Empfehlungsformen geprüft (L62) · 24. Zweitprüfung 2026-10-27: auch das SPX-Beispiel vom 2026-10-23 im Konjunktiv, historisch, ohne Handelssignal |
| C3 Steuer/Recht mit Primärquelle | ✓ | Steuer- und Rechtsaussagen vom Herausgeber am 2026-10-11 am Original geprüft (Gesetzesquellen im Volltext) · 24. Zweitprüfung 2026-10-27: Stichtag, Normzitate und Hinweis auf Steuerberater vorhanden |
| C4 Neutralität / Interessenkonflikte | ◐ | Einheitliche Bestimmbarkeitsregel für alle Anbieter (Abdeckungsangabe je ausgewerteter GEX-Funktion, ATAS: Options X-Ray und Options Chain Suite); Hero-Kennzahl als Funktionsangabe „nur SPX“; Interessenkonflikte: keine. Bestätigung durch Zweitprüfung und Sichtprüfung des Herausgebers ausstehend |
| C5 Marken beschreibend | ◐ | Bildschirmkopie des GEX-Metrix-Dashboards nicht auf der Seite und in keinem Branch des Repositorys; über die alte Commit-Kennung 6465f29 bei GitHub noch abrufbar, Löschung durch den Herausgeber zu beantragen; Markenhinweis in Seite und Analyse vollständig; Bestätigung durch Zweitprüfung ausstehend |
| C6 UWG-konforme Begriffe | ◐ | Einheitliche Bestimmbarkeitsregel: Abdeckungsangabe je ausgewerteter GEX-Funktion (ATAS: Options X-Ray, Options Chain Suite); TWS ohne belegte GEX-Funktion n. v.; Aussage zu Walls auf die Bildschirmkopie begrenzt; Bestätigung durch Zweitprüfung ausstehend |
| C7 Ausgewogene Risikodarstellung | ✓ | Modellgrenzen, Latenz, Fehlsignale, Totalverlust und BaFin-Quote dargestellt (Zweitprüfung 2026-10-11) · 24. Zweitprüfung 2026-10-27: Modellgrenzen auch beim echten Beispiel benannt |
| C8 Regulatorische Bezüge belegt | ✓ | § 80 WpHG, PRIIPs/UWG und § 63 Abs. 10 WpHG vom Herausgeber am 2026-10-11 am Original geprüft · 24. Zweitprüfung 2026-10-27: ohne Befund |
| C9 Datenschutz | ✓ | Datenschutzerklärung und Impressum vom Herausgeber freigegeben (2026-10-11); Speicherangaben = Messung an allen Modulseiten (L38); Modul ohne Drittanbieter-Abrufe und ohne Speicher (L20) · 24. Zweitprüfung 2026-10-27: Bildschirmkopie ohne Personendaten |
| Q1 Faktencheck K1–K9 vollständig | ✓ | 24. Zweitprüfung 2026-10-27: A01–A15 und K1–K9 stimmen nach L61 überein; A11 als [N. V.] nach Q9 zulässig |
| Q2 Aktualität / Stichtag | ◐ | Stichtag und Momentaufnahme gekennzeichnet; Ausnahmelisten in Daten-Transparenz, Datenherkunft, Legende, honest_disclosure und Analyse einheitlich (Medienangaben, Quantor, GEX-Metrix-Beispiel mit Differenzen und Wall-Ablesung); Bestätigung durch Zweitprüfung ausstehend |
| Q3 Mathematische Konsistenz | ✓ | GEX 845 Mio. USD, 2.600 ES / 26.000 MES, Probe, Vanna und Charm nachgerechnet (Zweitprüfung 2026-10-11); Rechner rechnet gleich · 24. Zweitprüfung 2026-10-27: GEX 845 Mio. USD, 2.600 ES / 26.000 MES und die Differenzen des echten Beispiels nachgerechnet |
| Q4 Provenienz je Fakt | ◐ | Wall-Ablesung als Klasse READING (UNVERIFIED), Bildschirmkopie mit Konfidenz 0,75, Herausgeber-Prüfdaten nur aus publisher_checks; Bestätigung durch Zweitprüfung und Sichtprüfung des Herausgebers ausstehend |
| Q5 Quellenqualität | ✓ | Rechtsrahmen-Fakten mit Primärquelle (L19c); Sekundärquellen als Hauptbeleg nur bei Medienangaben; Abgleich durch den Herausgeber am Original, bei Medienangaben an der Sekundärquelle · 24. Zweitprüfung 2026-10-27: ohne Befund |
| Q6 Vollständigkeit | ✓ | 24. Zweitprüfung 2026-10-27: Matrix belegt oder n. v., Validierungsverfahren in S07 methodisch im Konjunktiv, Modul-6-Zeilen n. v. |
| Q7 Widerspruchsfreiheit | ◐ | Ausnahmelisten einheitlich; Hero-Zählung getrennt nach am Original, abgeleitet, Bildschirmkopie; Zuordnung der JSON-LD-Tags in der Analyse erläutert; Bestätigung durch Zweitprüfung und Sichtprüfung des Herausgebers ausstehend |
| Q8 Glossar | ✓ | Zweitprüfung: alle 15 Pflichtbegriffe vorhanden · 24. Zweitprüfung 2026-10-27: 15 Pflichtbegriffe im Glossar abgeglichen |
| Q9 Keine Überzeichnung / Halluzination | ◐ | Aussage zu Walls auf die Bildschirmkopie begrenzt, Walls als ungeprüfte Ablesung, Hero-Kennzahl ohne Statistik-Eindruck; Bestätigung durch Zweitprüfung und Sichtprüfung des Herausgebers ausstehend |
| Q10 Formatvorgaben | ◐ | Analyse in der Reihenfolge des Prompts (Module 1–7, Modul 8 als Abschnitt 4, Glossar 5, Quellen 6, M-DBOM 7, Scorecard mit offenen Prüfpunkten 8), Quellen nach Stufe mit Herausgeber-Daten, JSON-LD mit einem Provenienz-Tag; Bestätigung durch Zweitprüfung ausstehend |

**Gesamtscore:** 11 × ✓ + 8 × ◐ = 15 von 19 Punkten = **78,9 %**.
**Freigabeempfehlung: ÜBERARBEITUNG.**

### 8.2 · Offene Prüfpunkte vor Veröffentlichung

- Kennzeichnung von Quantor und Gamma Cockpit durch Zweitprüfung und Herausgeber bestätigen lassen
- Belegstufen der Medienangaben und des abgeleiteten Quantors durch Zweitprüfung und Herausgeber bestätigen lassen
- Widerspruchsfreiheit von These und Belegstufen-Definition durch Zweitprüfung bestätigen lassen
- Einschränkung der Bewertung „Nutzen“ der Eurex-Erweiterung durch Zweitprüfung bestätigen lassen
- Claim A11 (NDX/NQ-0DTE-Dynamik) bleibt als [N. V.] gekennzeichnet, bis eine Quelle vorliegt
- Löschung des alten Commits 6465f29 mit der Bildschirmkopie beim GitHub-Support beantragen und den Abruf danach erneut prüfen
- Ergänzte Freitexte zum Prüfzeitraum und verschärfte Regel L78b durch Zweitprüfung bestätigen lassen
- Bestimmbarkeitsregel (Abdeckung je ausgewerteter GEX-Funktion) gilt für alle Anbieter gleich, TWS n. v., „keine Walls“ nur für die Bildschirmkopie; durch Zweitprüfung bestätigen lassen
- Ausgabestruktur der Analyse (Quellen nach Stufe mit Abruf/Abgleich, M-DBOM als JSON-LD) durch Zweitprüfung bestätigen lassen

---

## 9 · Disclaimer, Marken-Hinweis, Interessenkonflikte

**Disclaimer.** Diese Analyse dient ausschließlich der allgemeinen Information und Bildung. Sie stellt keine
Anlageberatung, Anlagevermittlung oder Finanzportfolioverwaltung im Sinne von WpIG, KWG oder WpHG dar.
Sie ist keine Rechtsdienstleistung im Sinne des RDG und keine Hilfeleistung in Steuersachen im Sinne des
StBerG. Sie enthält keine Anlageempfehlung und keine Empfehlung einer Anlagestrategie im Sinne von Art. 3
Abs. 1 Nr. 34 und 35 MAR. Derivate wie Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind
komplexe Produkte mit Hebelwirkung. Sie können zum Totalverlust führen. Bei Futures und Stillhaltergeschäften
sind Verluste über den Kapitaleinsatz hinaus möglich. Diese Produkte sind nur für erfahrene Anleger geeignet,
die Hebel- und Knock-out-Mechanik verstehen und Verluste bis zum Totalverlust tragen können. Optionsscheine tragen zusätzlich das
Emittentenrisiko; für Knock-out-Zertifikate ist die Ausgestaltung hier nicht ausgewertet (n. v.), maßgeblich
sind die Emissionsbedingungen. Vergangene Marktmuster und Modellausgaben sind kein verlässlicher Indikator für künftige
Entwicklungen. Steuerliche Ausführungen geben den recherchierten Rechtsstand zum 05.10.2026 wieder und
können sich ändern. Für Ihre persönliche Situation wenden Sie sich an einen Steuerberater oder Rechtsanwalt.
Alle Angaben ohne Gewähr.

**Marken-Hinweis.** ATAS, Options X-Ray, OptionsDepth, SpotGamma, HIRO, MenthorQ, Volland, Bookmap,
Interactive Brokers, TWS, Rithmic, CQG, Eurex, Cboe, VIX, OPRA, DAX, EURO STOXX 50, S&P 500, SPX, Nasdaq-100, NDX,
Gamma Cockpit, GEX-Metrix, CME, E-mini, SPDR, SPY, SPXW, dxFeed, IQFeed, TRACE, IBKR, OptionTrader, Options Chain Suite, Options Board, Strategy Analyzer, MBO-Bundle, Ultra, EOBI, Extended Market Data Service, CMS, ideas, ORATS, Morgan Stanley, Sutor, Deutscher Derivate Verband (DDV), Stiftung Warentest und Deutsche Börse sind Marken oder Produktbezeichnungen ihrer jeweiligen Inhaber. Sie werden hier rein
beschreibend genannt; das gilt auch für weitere genannte Produkt-, Index- und Kontraktbezeichnungen (etwa NQ, ES, MES, ODAX,
OESX, ODXS, OEXP, ODAP, FDAX, FESX). Es besteht keine Verbindung zu den Inhabern und keine Billigung durch sie.

**Interessenkonflikte.** Es bestehen keine Interessenkonflikte, insbesondere keine Affiliate-, Partner- oder
Vergütungsbeziehungen zu den genannten Anbietern (Erklärung des Herausgebers vom 2026-10-11).
