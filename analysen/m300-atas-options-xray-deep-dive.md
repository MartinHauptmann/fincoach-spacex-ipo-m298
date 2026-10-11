# FinCoach AI · Deep-Dive-Prime-Analyse · Modul M300

**ATAS Options X-Ray · Dealer-Greeks · Eurex-Börsenoptionen vs. verbriefte Derivate · Termingeschäfte im Steuerrecht**

| Feld | Wert |
|---|---|
| Modul | M300 (Platzhalter-ID) |
| Version | 1.10.4 (Entwurf) |
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
> meisten Primärquellen gesperrt hat, darunter gesetze-im-internet.de, recht.bund.de, eurex.com, atas.net und die Anbieterseiten. Die Befunde beruhen auf Suchtreffern, die
> auf diese Primärquellen verweisen. Die URLs sind im Quellenverzeichnis aufgeführt. Fundstellen, deren
> Wortlaut nicht vollständig einsehbar war, tragen ein schwächeres Verdict oder **[N. V.]**.
> Vor einer Veröffentlichung sind sie am Original zu prüfen.

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
  SCENARIO_PROJECTION, Konfidenz 0,5).
- **Wettbewerb:** Intraday-fähige Eurex-GEX bietet keiner der fünf bestimmbaren von sechs verglichenen Anbietern;
  für MenthorQ ist das n. v. (`FACT_NO_EUREX_GEX`, Medienangabe, Konfidenz 0,6).
- **Einschätzung [SZENARIO]:** Der Wert einer Eurex-Erweiterung läge damit in dieser Analyselücke, nicht in einem
  Steuervorteil (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0). Das ist keine Prognose.

---

## 2 · Phase A: Faktenprüfung K1–K9

### 2.1 Claim-Tabelle

<!-- sync:CLAIMS -->
Legende: ✓ bestätigt · ◐ präzisiert · ✗ falsch · [N. V.] nicht verifizierbar. Die Aussagen in Spalte 2 zitieren den Quelltext (USER_PROVIDED) und sind keine Tatsachenbehauptungen dieser Analyse.

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
| A12 | Quelltext: Wettbewerbsfelder (SpotGamma, MenthorQ, Volland, Bookmap, TWS) | Wettbewerb | ◐ | (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65) | Medienangabe |
| A13 | Quelltext: Vier Roadmap-Erweiterungen | Vorschlag | Szenario | (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0) | SCENARIO_PROJECTION |
| A14 | Quelltext: Warrant-Fair-Value-Tool zeigt „verdeckte Marge“ | Vorschlag | ◐ | (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0), (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75) | SCENARIO_PROJECTION |
| A15 | Quelltext: Börsengehandelte Optionen sind gegenüber Optionsscheinen steuerlich benachteiligt | Steuer/Recht | ✗ | (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9) | belegt |

<!-- /sync:CLAIMS -->

### 2.2 Prüfprotokoll K1–K9

<!-- sync:K -->
**K1 · Kapitalgesellschaft.** Quelltext: „keine Verlustverrechnungsbeschränkung“. Über § 8 Abs. 1 KStG gilt § 15 Abs. 4 Satz 3 EStG: eigener Verlustkreis für Termingeschäfte (BFH I R 25/14). Ausnahmen bestehen nur für Institute und Sicherungsgeschäfte. Belege: (`FACT_P15_KSTG`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (KRITISCH)

**K2 · Hedging-Pflicht Market Maker.** Quelltext: Market Maker „gesetzlich gezwungen“, über das Orderbuch zu hedgen. Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition in Abs. 5) regeln Quotierungs- und Vertragspflichten. Delta-Hedging ist Risikomanagement und kann über viele Kanäle erfolgen. Belege: (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (WESENTLICH)

**K3 · GEX-Prämisse.** Quelltext: Dealer-Hedging als feste Mechanik. Die Positionskonvention ist eine Modellannahme. Beim SPX ist sie durch Teilnehmer-markierte Cboe-Daten besser fundiert, bleibt aber anfällig für Spreads, Overwriting und Intraday-Volumen. (Modellannahme; Cboe-Daten: Medienangabe) Belege: (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, Konfidenz 0,5), (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (WESENTLICH)

**K4 · Emittenten-Hedging.** Quelltext: „keine“ Hedging-Spuren im FDAX. Emittenten hedgen dynamisch, auch über Basiswert und Gegengeschäfte. Die Spur ist schwach und nicht zurechenbar, aber nicht null. (Medienangabe) Belege: (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (HINWEIS)

**K5 · ATAS-Produktangaben.** Quelltext: 10 Indikatoren, CBOE/OptionsDepth, 60 s, nur SPX. Bestätigt durch Hilfe- und Lernseiten des Herstellers. Ergänzung: Optionen in ATAS derzeit nicht handelbar; Options Board/Strategy Analyzer als Beta. Belege: (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85), (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8). **Ergebnis: ✓** (HINWEIS)

**K6 · Wettbewerber.** Quelltext: Vergleich SpotGamma, MenthorQ, Volland, Bookmap, TWS. Medienangaben aus Hersteller- und Drittquellen; einzelne Felder n. v. (Medienangaben) Belege: (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65). **Ergebnis: ◐** (HINWEIS)

**K7 · Eurex-Spezifikationen.** Quelltext: FDAX/FESX-Optionsketten, „Hexensabbat“. Für den Ausgangstext maßgeblich sind die Indexoptionen ODAX (5 €/Pkt.) und OESX (10 €/Pkt.). Fachbegriff: Quartalsverfall, letzter Handelstag ist der dritte Freitag. End-of-Day-Optionen: OEXP und ODAP; Verfälle an zehn Handelstagen sind für OEXP belegt. Belege: (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85), (`FACT_OESX_MULT`, belegt, Konfidenz 0,85), (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85), (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8). **Ergebnis: ◐** (HINWEIS)

**K8 · IBKR-Combo-Orders.** Quelltext: native Spread-Engine fehlt. Für ATAS zutreffend, aber zu präzisieren. Die IB-API unterstützt BAG-Combo-Orders (bis 6 Legs, Netto-Limit) bereits. Die Lücke liegt in UI, Risikoprüfung und Positionsführung. Belege: (`FACT_IB_BAG`, belegt, Konfidenz 0,85). **Ergebnis: ◐** (WESENTLICH)

**K9 · Warrant-Fair-Value-Tool.** Quelltext: „verdeckte Marge“, „künstliche Spread-Ausweitung“. Wertende Begriffe mit UWG-Risiko. Neutral: Fair-Value-Differenz, Emittentenaufschlag. Abgleich mit PRIIPs-KID; Emittentenbonität ist ein realer Wert, keine Marge. (Rechtsgrundlagen PRIIPs/UWG: ungeprüft) Belege: (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75). **Ergebnis: ◐** (WESENTLICH)

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

## 3 · Phase B: Module 1–8 (faktgebundene Kurzfassung)

Je Modul die gebundenen Fakten aus der DBOM. Wertungen stehen nur in Modul 8 (aus dem Fazit der Modulseite) und sind als Einschätzung markiert.

<!-- sync:MOD -->
#### Modul 1 · Technologische Dekonstruktion der Options X-Ray Suite

- Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile). (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85)
- Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY. (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85)
- OptionsDepth deckt derzeit nur SPX und VIX ab. (`FACT_OPTIONSDEPTH_SCOPE`, belegt, Konfidenz 0,75)
- SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt. (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6)
- GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls). (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, Konfidenz 0,5)
- Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES. (`FACT_GEX_EXAMPLE`, SCENARIO_PROJECTION, Konfidenz 1,0)
- Kontraktdaten: Multiplikator SPX 100 USD je Indexpunkt, SPXW-Optionen mit Verfällen an jedem Wochentag (0DTE möglich; Cboe); E-mini S&P 500 50 USD und Micro E-mini 5 USD je Indexpunkt (CME); Eurex-Indexoptionen: letzter Handelstag ist der dritte Freitag des Verfallsmonats (Quartalsverfall im März, Juni, September und Dezember). (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8)

#### Modul 2 · Datenfeed-Architektur, Latenzprofil und Validierung

- Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung. (`FACT_XRAY_CONNECTIVITY`, belegt, Konfidenz 0,7)
- OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster. (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7)
- Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab. (`FACT_CHAIN_SUITE`, belegt, Konfidenz 0,85)

#### Modul 3 · Handels- und Ausführungsmöglichkeiten

- ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed. (`FACT_ATAS_CONNECTIONS`, belegt, Konfidenz 0,85)
- Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan). Laut Changelog sind ein MBO-Bundle und eine Optionsanalyse verfügbar. (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8)
- ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026). (`FACT_CROSS_TRADING`, belegt, Konfidenz 0,85)
- IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit. (`FACT_IB_BAG`, belegt, Konfidenz 0,85)
- § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). (`FACT_ALGO_TRADING`, belegt, Konfidenz 0,85)
- Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85)

#### Modul 4 · Mikro-Makro-Synergien im praktischen Trading

- Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %. (`FACT_SPX_0DTE_59`, belegt, Konfidenz 0,85)
- Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. (`FACT_MAR_RECO`, belegt, Konfidenz 0,85)

#### Modul 5 · Globaler Wettbewerbsvergleich (Matrix auf der Modulseite S09)

- Anbieterangaben (Stand 2026-10-05): SpotGamma – Gamma-Levels und Research, HIRO/TRACE intraday, Levels vor Eröffnung, GEX ja, Vanna als Modell, Charm n. v., keine eigene Ausführung; MenthorQ – Gamma-Levels, Modelle, Ausbildung, Optionsdaten EOD und alle 5 Min., GEX ja, Vanna und Charm n. v., Ausführung über Partnerplattformen, Eurex-GEX n. v.; Volland – Notional-Greeks des Dealer-Buchs, Optionsdaten EOD bis alle 5 Min., Gamma, Vanna und Charm, Ausführung n. v.; Bookmap – Orderbuch-Heatmap, keine nativen Optionsdaten, Greeks nur über Add-ons, Heatmap und MBO via Rithmic, eigene Ausführung; IBKR TWS – Broker und Portfoliorisiko, Echtzeit-Optionsdaten (Abo), Greeks nur für eigene Positionen, Abdeckung global inkl. ODAX/OESX, eigene Ausführung. (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65)
- Von sechs verglichenen Anbietern ist für fünf bestimmbar, dass keiner intraday-fähige Eurex-GEX anbietet; für MenthorQ n. v. Gamma Cockpit (nicht im Vergleichsfeld) liefert DAX-GEX nur auf Tagesbasis (Beta). (`FACT_NO_EUREX_GEX`, Medienangabe, Konfidenz 0,6)

#### Modul 6 · DACH-Marktspezifika und steuerlicher Rahmen

- Verluste aus Termingeschäften im Privatvermögen unterliegen keiner gesonderten Verlustverrechnungsbeschränkung; es gelten die allgemeinen Regeln für Einkünfte aus Kapitalvermögen (§ 20 Abs. 6 EStG in der Fassung des JStG 2024, BGBl. 2024 I Nr. 387). Daraus folgt: Börsengehandelte Optionen und Optionsscheine werden insoweit nicht unterschiedlich behandelt. (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9)
- § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016. (`FACT_P15_KSTG`, belegt, Konfidenz 0,85)
- Börsengehandelte Eurex-Optionen werden über die Eurex Clearing AG als zentrale Gegenpartei abgewickelt (Zulassung nach EMIR durch die BaFin am 10.04.2014); die Teilnehmer hinterlegen Sicherheiten (Margin). Optionsscheine sind Inhaberschuldverschreibungen des Emittenten; ihr Wert hängt von dessen Bonität ab. (`FACT_CCP_ISSUER`, belegt, Konfidenz 0,8)
- ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet. (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85)
- OESX (EURO-STOXX-50-Indexoptionen): 10 € je Indexpunkt, europäisch, Barausgleich. (`FACT_OESX_MULT`, belegt, Konfidenz 0,85)
- Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. (`FACT_EUREX_OI`, belegt, Konfidenz 0,85)
- Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen. (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85)
- Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte. (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6)
- BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen. (`FACT_BAFIN_TURBO`, belegt, Konfidenz 0,85)
- BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023. (`FACT_BAFIN_STUDY`, Medienangabe, Konfidenz 0,65)
- Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG. (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75)
- Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG. (`FACT_ANGEMESSENHEIT`, ungeprüft, Konfidenz 0,7)

#### Modul 7 · Strategische Produkt-Roadmap [SZENARIO]

- Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge. (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0)

#### Modul 8 · Fazit und Synthese [Einschätzung, aus dem Fazit der Modulseite]

**✓ Bleibt**

- X-Ray zeigt aus SPX-Optionsdaten abgeleitete Kennzahlen auf ES, MES und SPY an. (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85)
- Minuten-Snapshots lösen das Skalierungsproblem, kosten aber Aktualität bei Makro-Events. (Einschätzung, gestützt auf (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7))
- Für Optionen fehlt eine native Ausführung. (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8)
- Positionierung plus MBO in einer Oberfläche ist laut Matrix ein Differenzierungsmerkmal. (Einschätzung, gestützt auf (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65), (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8))

**◐ Relativiert**

- Market Maker hedgen aus Kalkül, nicht aus gesetzlichem Zwang. (Einschätzung, gestützt auf (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85))
- GEX beruht auf einer Positionsannahme; beim SPX durch markierte Cboe-Daten besser, anderswo schwächer fundiert. (Einschätzung, gestützt auf (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, Konfidenz 0,5), (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6))
- Optionsscheine hinterlassen eine schwache, nicht zurechenbare Hedge-Spur, aber keine Nullspur. (Einschätzung, gestützt auf (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6))

**✗ Entfällt**

- Ein steuerlicher Nachteil börsengehandelter Optionen gegenüber Optionsscheinen im Privatvermögen. (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9)
- „Keine Verlustbeschränkung“ für Kapitalgesellschaften. (`FACT_P15_KSTG`, belegt, Konfidenz 0,85)

**Strategische These [SZENARIO]:** Der Wert einer Eurex-Erweiterung läge nicht in einem Steuervorteil, sondern in einer Analyselücke. Für ODAX und OESX bietet keiner der fünf bestimmbaren von sechs verglichenen Anbietern eine Dealer-Positionierung innerhalb des Tages (MenthorQ: n. v.). Ob ATAS diese Lücke füllen kann, hängt von Datenlizenzen, Validierung und der offenen Kommunikation der schwächeren Positionsannahme ab. (`FACT_NO_EUREX_GEX`, Medienangabe, Konfidenz 0,6) (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0)

<!-- /sync:MOD -->

### 3.9 Modellrechnung [MODELL]

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

## 4 · Glossar

<!-- sync:GLOSSAR -->
| Begriff | Definition (Fortgeschritten) | Einordnung (Experte) |
|---|---|---|
| Delta | Erste Ableitung des Optionspreises nach dem Basiswert. | $\Delta=\partial V/\partial S$; Grundlage jeder Hedge-Menge. |
| Gamma | Zweite Ableitung des Optionspreises nach dem Basiswert. | $\Gamma=\partial^2 V/\partial S^2$; bestimmt den Nachsicherungsbedarf. |
| Open Interest | Bestand nicht glattgestellter Kontrakte je Serie. | Eurex veröffentlicht es täglich je Serie; Basis der GEX-Profile. (`FACT_EUREX_OI`, belegt, Konfidenz 0,85) |
| Implizite Volatilität | Aus dem Optionspreis zurückgerechnete Volatilität. | Fläche über Strike und Laufzeit; Eingang für Vanna-Effekte. |
| Delta-Divergenz | Abweichung zwischen Preisverlauf und kumuliertem Delta. | Schwächeres Umkehrsignal im Short-Gamma-Regime. |
| BAG / Combo-Order | IB-Ordertyp für Spreads mit Netto-Limit. | Schützt vor Legging-Risiko; in ATAS derzeit nicht integriert. (`FACT_IB_BAG`, belegt, Konfidenz 0,85) (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8) |
| Angemessenheitsprüfung | Abfrage von Kenntnissen und Erfahrungen vor dem Handel. | Für komplexe Produkte vorgeschrieben (Fundstelle ungeprüft). (`FACT_ANGEMESSENHEIT`, ungeprüft, Konfidenz 0,7) |
| Optionsschein | Verbriefte Option, rechtlich eine Inhaberschuldverschreibung. | Emittentenrisiko: Der Wert hängt von der Bonität des Emittenten ab. (`FACT_CCP_ISSUER`, belegt, Konfidenz 0,8) |
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
| Knock-out-Zertifikat | Verbriefte Schuldverschreibung mit Knock-out-Barriere. | Für Turbos gilt eine BaFin-Allgemeinverfügung (Details in Modulseite S10). (`FACT_BAFIN_TURBO`, belegt, Konfidenz 0,85) |
| CCP | Central Counterparty, hier Eurex Clearing. | Ersetzt bilaterales Kontrahentenrisiko; Teilnehmer hinterlegen Sicherheiten (Margin). (`FACT_CCP_ISSUER`, belegt, Konfidenz 0,8) |
| PRIIPs-KID | EU-Basisinformationsblatt (VO (EU) 1286/2014, Fundstelle ungeprüft). | Referenz für Kostenvergleiche verbriefter Derivate. (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75) |
| Quartalsverfall | Dritter Freitag der Quartalsmonate. | Umgangssprachlich „Hexensabbat“; OI-Verschiebungen davor relevant. (`FACT_CONTRACT_SPECS`, belegt, Konfidenz 0,8) |

<!-- /sync:GLOSSAR -->

---

## 5 · Quellenverzeichnis

Abgerufen 2026-10-05 bis 2026-10-11, überwiegend über Suchtreffer-Snippets (siehe Methodischer Vorbehalt). Das
Verzeichnis ist ein Auszug aus `provenance/m300.dbom.json` (Lehre L13/L14) und wird von dort erzeugt, nicht von
Hand gepflegt. Die S-Nummern sind die Belegverweise in dieser Analyse.

| Nr. | Quelle | Stufe | DBOM-ID | URL |
|---|---|---|---|---|
| S1 | Jahressteuergesetz 2024, BGBl. 2024 I Nr. 387 | Primärquelle | `SRC_BGBL_JSTG2024` | https://www.recht.bund.de/bgbl/1/2024/387/regelungstext.pdf |
| S2 | BT-Drs. 20/13419, 20/13420, 20/12780 (JStG 2024) | Primärquelle | `SRC_BT_DRS` | https://dserver.bundestag.de/btd/20/134/2013420.pdf |
| S9 | BaFin · Allgemeinverfügung Turbo-Zertifikate | Primärquelle | `SRC_BAFIN_TURBO` | https://www.bafin.de/SharedDocs/Downloads/DE/Aufsichtsrecht/Verfuegungen/dl_vf_allgemeinverfuegung_turbo_zertifikate.html |
| S10 | BaFin · FAQ HFT-Gesetz | Primärquelle | `SRC_BAFIN_HFT` | https://www.bafin.de/SharedDocs/FAQs/DE/HFT-Gesetz/160_hft_faq.html |
| S11 | § 80 WpHG (Abs. 2 algorithmischer Handel; Abs. 4 Market-Making-Pflichten; Abs. 5 Definition) | Primärquelle | `SRC_WPHG_80` | https://www.gesetze-im-internet.de/wphg/__80.html |
| S12 | Emittenten-Hedging (Morgan Stanley Produktwissen, ideas-Magazin; Sekundärquellen) | Sekundärquelle | `SRC_ISSUER_HEDGE` | https://zertifikate.morganstanley.com/services/produktwissen/optionsscheine/ |
| S13 | § 15 EStG | Primärquelle | `SRC_ESTG_15` | https://www.gesetze-im-internet.de/estg/__15.html |
| S14 | BFH, Urteil v. 06.07.2016, I R 25/14 | Primärquelle | `SRC_BFH_IR2514` | https://www.bundesfinanzhof.de/en/entscheidungen/entscheidungen-online/decision-detail/STRE201610211/ |
| S15 | ATAS Hilfe · Options X-Ray | Herstellerquelle | `SRC_ATAS_HELP` | https://help.atas.net/en/support/solutions/articles/72000662222-options-x-ray-expected-move |
| S16 | ATAS Learn · Options | Herstellerquelle | `SRC_ATAS_LEARN` | https://learn.atas.net/options/ |
| S17 | ATAS Changelog | Herstellerquelle | `SRC_ATAS_CHANGELOG` | https://feedback.atas.net/changelog |
| S18 | ATAS Hilfe · Options Chain Suite / GEX Profile | Herstellerquelle | `SRC_ATAS_CHAIN` | https://help.atas.net/en/support/solutions/articles/72000661536-options-gex-profile |
| S19 | ATAS · Connections | Herstellerquelle | `SRC_ATAS_CONNECTIONS` | https://atas.net/connections/ |
| S20 | ATAS 8.0.12 · Cross-Trading | Herstellerquelle | `SRC_ATAS_8012` | https://help.atas.net/en/support/solutions/articles/72000657084-cross-trading |
| S21 | ATAS Changelog · MBO-Bundle und Optionsanalyse | Herstellerquelle | `SRC_ATAS_MBO` | https://feedback.atas.net/changelog/new-mbo-bundle-and-options-analysis-are-now-in-atas |
| S22 | IB TWS API · Spread Contracts | Herstellerquelle | `SRC_IB_API` | https://interactivebrokers.github.io/tws-api/spread_contracts.html |
| S23 | SpotGamma (HIRO) | Herstellerquelle | `SRC_SPOTGAMMA` | https://spotgamma.com/hiro-indicator/ |
| S24 | MenthorQ (Abdeckung) | Herstellerquelle | `SRC_MENTHORQ` | https://menthorq.com/guide/menthorq-asset-coverage/ |
| S25 | Volland (ORATS-Partnerseite, User Guide) | Sekundärquelle | `SRC_VOLLAND` | https://orats.com/volland |
| S26 | Bookmap (Konnektivität) | Herstellerquelle | `SRC_BOOKMAP` | https://bookmap.com/en/packages-comparison |
| S27 | Interactive Brokers · OptionTrader / TWS | Herstellerquelle | `SRC_IBKR` | https://www.interactivebrokers.com/en/software/pdfhighlights/PDF-OptionTrader.php |
| S28 | Gamma Cockpit (DAX-GEX, Beta) | Herstellerquelle | `SRC_GAMMACOCKPIT` | https://gammacockpit.com/ |
| S29 | Eurex · Produktseiten und Kontraktspezifikationen DAX-Optionen (ODAX), Micro-DAX-Optionen (ODXS), EURO STOXX 50 Options | Primärquelle | `SRC_EUREX_SPECS` | https://www.eurex.com/ex-en/markets/idx/dax/DAX-Options-139884 |
| S30 | Eurex Circulars OEXP 047/23 und 117/25 | Primärquelle | `SRC_EUREX_CIRCULARS` | https://www.eurex.com/ex-en/find/circulars/circular-4844340 |
| S32 | Cboe · Trading Volume December and Full Year 2025 | Primärquelle | `SRC_CBOE_FY2025` | https://ir.cboe.com/news/news-details/2026/Cboe-Global-Markets-Reports-Trading-Volume-for-December-and-Full-Year-2025/default.aspx |
| S33 | OPRA · Capacity Projections Update (Sept. 2025) | Primärquelle | `SRC_OPRA` | https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf |
| S35 | Delegierte VO (EU) 2016/958 (Anlageempfehlungen) | Primärquelle | `SRC_DELVO_958` | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0958 |
| S36 | CMS · Verlustverrechnung bei Termingeschäften nach dem JStG 2024 (Sekundärquelle) | Sekundärquelle | `SRC_CMS` | https://cms.law/de/deu/legal-updates/Ade-Verlustabzugsbeschraenkung-fuer-Termingeschaefte-Gesetzgeber-bereinigt-Verfassungswidrigkeit |
| S42 | MenthorQ · Cboe Market-Maker-Tagged Data erklärt (Sekundärquelle) | Sekundärquelle | `SRC_MENTHORQ_GUIDE` | https://menthorq.com/guide/cboe-market-maker-tagged-data-explained/ |
| S44 | VO (EU) Nr. 1286/2014 (PRIIPs) | Primärquelle | `SRC_PRIIPS` | https://eur-lex.europa.eu/eli/reg/2014/1286/oj |
| S46 | Eurex · Daily Options (OEXP/ODAP) | Primärquelle | `SRC_EUREX_DAILY` | https://www.eurex.com/ex-en/markets/idx/daily-opt |
| S47 | § 63 WpHG (Wohlverhaltenspflichten) | Primärquelle | `SRC_WPHG_63` | https://www.gesetze-im-internet.de/wphg/__63.html |
| S48 | Sutor Bank · Formular Angemessenheit nach § 63 Abs. 10 WpHG (Sekundärquelle) | Sekundärquelle | `SRC_SUTOR` | https://www.sutorbank.de/fileadmin/Dateien/Service/Formulare/Investmentsparvertraege/Angaben-zur-Feststellung-der-Angemessenheit.pdf |
| S49 | OptionsDepth (Abdeckung, API) | Herstellerquelle | `SRC_OPTIONSDEPTH` | https://optionsdepth.com/ |
| S50 | Eurex · Statistiken / Extended Market Data Service (Open Interest) | Primärquelle | `SRC_EUREX_STATS` | https://www.eurex.com/ex-en/data/statistics |
| S51 | Cboe · S&P 500 Index Options (SPX/SPXW) Product Specifications | Primärquelle | `SRC_CBOE_SPX` | https://www.cboe.com/tradable-products/sp-500/spx-options/spx-specifications |
| S52 | CME Group · Micro E-mini Equity Index Futures – Products Overview | Primärquelle | `SRC_CME_MICRO` | https://www.cmegroup.com/education/courses/understanding-micro-futures-contracts-at-cme-group/micro-e-mini-futures/micro-e-mini-equity-index-futures-products-overview.html |
| S54 | Eurex · EURO STOXX 50 Index Options Contract Specifications | Primärquelle | `SRC_EUREX_OESX_SPEC` | https://www.eurex.com/ex-en/markets/idx/stx/euro-stoxx-50-derivatives/products/EURO-STOXX-50-Index-Options-46548 |
| S55 | BaFin · Zulassung der Eurex Clearing AG als zentrale Gegenpartei nach EMIR (10.04.2014) | Primärquelle | `SRC_BAFIN_EUREX_CLEARING` | https://bafin.de/SharedDocs/Veroeffentlichungen/EN/Meldung/2014/meldung_140410_emir_erlaubnis_eurex_en.html |
| S56 | Deutsche Börse · Clearing: zentrale Gegenpartei und Sicherheiten (Margin) | Sekundärquelle | `SRC_DB_CLEARING` | https://www.deutsche-boerse-cash-market.com/resource/blob/244872/f8a90e944e2f40c38cabcf6420dde59c/data/db-aktuell-clearing-may2018_de.pdf.pdf |
| S57 | Deutscher Derivate Verband · Muster-Produktinformation Call-Optionsschein | Sekundärquelle | `SRC_DDV_OS_MUSTER` | https://www.derivateverband.de/DE/MediaLibrary/Document/Muster/Call%20Optionsschein-d.pdf |
| S58 | Stiftung Warentest · Studie zu Turbo-Zertifikaten: Die meisten Anleger machen Verluste | Sekundärquelle | `SRC_TESTDE_TURBO` | https://www.test.de/Studie-zu-Turbo-Zertifikaten-Die-meisten-Anleger-machen-mit-Turbo-Zertifikaten-Verluste-6227752-0/ |

---

## 6 · M-DBOM (Data Bill of Materials)

Führende Provenienzliste ist **`provenance/m300.dbom.json`** (Lehre L13: eine DBOM für Seite und Analyse). Die
Tabelle ist ein Auszug daraus und wird bei Änderungen neu erzeugt, nicht von Hand gepflegt. Stand: Modul v1.10.4,
33 Fakten, 44 Quellen.

| ID | Verdict | Klasse | Konf. | Bezugszeitraum | Claim |
|---|---|---|---|---|---|
| `FACT_JSTG2024_REPEAL` | CONFIRMED | REGULATORY_FRAMEWORK | 0,9 | Rechtsstand 2026-10-05 | Verluste aus Termingeschäften im Privatvermögen unterliegen keiner gesonderten Verlustverrechnungsbeschränkung; es gelten die allgemeinen Regeln für Einkünfte aus Kapitalvermögen (§ 20 Abs. 6 EStG in der Fassung des JStG 2024, BGBl. 2024 I Nr. 387). Daraus folgt: Börsengehandelte Optionen und Optionsscheine werden insoweit nicht unterschiedlich behandelt. |
| `FACT_P15_KSTG` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016. |
| `FACT_MM_NO_HEDGE_DUTY` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. |
| `FACT_ALGO_TRADING` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). |
| `FACT_MAR_RECO` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. |
| `FACT_PRIIPS_UWG` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,75 | Rechtsstand 2026-10-05 | Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG. |
| `FACT_ANGEMESSENHEIT` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,7 | Rechtsstand 2026-10-05 | Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG. |
| `FACT_BAFIN_TURBO` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Allgemeinverfügung 15.10.2025, in Kraft 16.06.2026 | BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen. |
| `FACT_BAFIN_STUDY` | MEDIA_REPORT | MEDIA_REPORT | 0,65 | Untersuchungszeitraum 2019–2023 | BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023. |
| `FACT_XRAY_10_IND` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile). |
| `FACT_XRAY_1MIN_SPX` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY. |
| `FACT_OPTIONSDEPTH_SCOPE` | CONFIRMED | VENDOR_CLAIM | 0,75 | Herstellerangabe Stand 2026-10-05 | OptionsDepth deckt derzeit nur SPX und VIX ab. |
| `FACT_XRAY_CONNECTIVITY` | CONFIRMED | VENDOR_CLAIM | 0,7 | Changelog Stand 2026-10-05 | Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung. |
| `FACT_ATAS_CONNECTIONS` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed. |
| `FACT_CHAIN_SUITE` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab. |
| `FACT_ATAS_NO_OPT_TRADING` | CONFIRMED | VENDOR_CLAIM | 0,8 | Herstellerdoku Stand 2026-10-05 | Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan). Laut Changelog sind ein MBO-Bundle und eine Optionsanalyse verfügbar. |
| `FACT_CROSS_TRADING` | CONFIRMED | VENDOR_CLAIM | 0,85 | ATAS 8.0.12 (17.02.2026) | ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026). |
| `FACT_IB_BAG` | CONFIRMED | VENDOR_CLAIM | 0,85 | API-Doku Stand 2026-10-05 | IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit. |
| `FACT_CBOE_OPENCLOSE` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt. |
| `FACT_SPX_0DTE_59` | CONFIRMED | MARKET_DATA | 0,85 | Gesamtjahr 2025 | Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %. |
| `FACT_OPRA_CAPACITY` | CONFIRMED | MARKET_DATA | 0,7 | Projektion Sept. 2025 | OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster. |
| `FACT_ODAX_SPECS` | CONFIRMED | MARKET_DATA | 0,85 | Produktseite Stand 2026-10-05 | ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet. |
| `FACT_EUREX_OI` | CONFIRMED | MARKET_DATA | 0,85 | Stand 2026-10-05 | Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. |
| `FACT_OESX_MULT` | CONFIRMED | MARKET_DATA | 0,85 | Stichtag 2026-10-05 (Kontraktspezifikation abgerufen 2026-10-11) | OESX (EURO-STOXX-50-Indexoptionen): 10 € je Indexpunkt, europäisch, Barausgleich. |
| `FACT_EUREX_DAILY_LAUNCH` | CONFIRMED | MARKET_DATA | 0,85 | Eurex-Circulars 2023–2026 | Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen. |
| `FACT_ISSUER_HEDGING` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte. |
| `FACT_COMPETITOR_MATRIX` | MEDIA_REPORT | MEDIA_REPORT | 0,65 | Stand 2026-10-05 | Anbieterangaben (Stand 2026-10-05): SpotGamma – Gamma-Levels und Research, HIRO/TRACE intraday, Levels vor Eröffnung, GEX ja, Vanna als Modell, Charm n. v., keine eigene Ausführung; MenthorQ – Gamma-Levels, Modelle, Ausbildung, Optionsdaten EOD und alle 5 Min., GEX ja, Vanna und Charm n. v., Ausführung über Partnerplattformen, Eurex-GEX n. v.; Volland – Notional-Greeks des Dealer-Buchs, Optionsdaten EOD bis alle 5 Min., Gamma, Vanna und Charm, Ausführung n. v.; Bookmap – Orderbuch-Heatmap, keine nativen Optionsdaten, Greeks nur über Add-ons, Heatmap und MBO via Rithmic, eigene Ausführung; IBKR TWS – Broker und Portfoliorisiko, Echtzeit-Optionsdaten (Abo), Greeks nur für eigene Positionen, Abdeckung global inkl. ODAX/OESX, eigene Ausführung. |
| `FACT_NO_EUREX_GEX` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | Von sechs verglichenen Anbietern ist für fünf bestimmbar, dass keiner intraday-fähige Eurex-GEX anbietet; für MenthorQ n. v. Gamma Cockpit (nicht im Vergleichsfeld) liefert DAX-GEX nur auf Tagesbasis (Beta). |
| `FACT_DEALER_CONVENTION` | SCENARIO_PROJECTION | MODEL_ASSUMPTION | 0,5 | – | GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls). |
| `FACT_GEX_EXAMPLE` | SCENARIO_PROJECTION | SCENARIO_PROJECTION | 1,0 | – | Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES. |
| `FACT_ROADMAP` | SCENARIO_PROJECTION | SCENARIO_PROJECTION | 0,0 | – | Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge. |
| `FACT_CONTRACT_SPECS` | CONFIRMED | MARKET_DATA | 0,8 | Stichtag 2026-10-05 (Kontraktspezifikationen abgerufen 2026-10-11) | Kontraktdaten: Multiplikator SPX 100 USD je Indexpunkt, SPXW-Optionen mit Verfällen an jedem Wochentag (0DTE möglich; Cboe); E-mini S&P 500 50 USD und Micro E-mini 5 USD je Indexpunkt (CME); Eurex-Indexoptionen: letzter Handelstag ist der dritte Freitag des Verfallsmonats (Quartalsverfall im März, Juni, September und Dezember). |
| `FACT_CCP_ISSUER` | CONFIRMED | REGULATORY_FRAMEWORK | 0,8 | Stichtag 2026-10-05 (Quellen abgerufen 2026-10-11) | Börsengehandelte Eurex-Optionen werden über die Eurex Clearing AG als zentrale Gegenpartei abgewickelt (Zulassung nach EMIR durch die BaFin am 10.04.2014); die Teilnehmer hinterlegen Sicherheiten (Margin). Optionsscheine sind Inhaberschuldverschreibungen des Emittenten; ihr Wert hängt von dessen Bonität ab. |

---

## 7 · Offene Prüfpunkte vor Veröffentlichung

- Steuerlichen Rahmen (S04) am Volltext der Gesetzesquellen gegenlesen lassen
- Primärquellen im Volltext lesen (BGBl., Eurex, Cboe, CME, ATAS)
- Aktualität der Angaben am Stichtag durch Abgleich mit den Originalquellen bestätigen
- Interessenkonflikte durch Herausgeber bestätigen
- PRIIPs-/UWG-Bezüge und § 63 Abs. 10 WpHG am Original prüfen
- Datenschutzerklärung korrigieren: sessionStorage, Stand-Datum, Log-Speicherdauer, Vorlagenhinweis
- Provenienz je Fakt nach dem Volltextabgleich der Primärquellen bestätigen (siehe C3, C8)
- Allaussagen (S11) und Fazit-Wertungen manuell gegenprüfen (L06b, L62)
- K-Verweise, Fazit-Bezug und Folgetexte manuell gegenprüfen
- Claim A11 (NDX/NQ-0DTE-Dynamik) belegen oder streichen; Claim-Ergebnisse nach L61 durch unabhängige Zweitprüfung bestätigen
- Wettbewerberangaben (Matrix S09, Eurex-GEX) an den Anbieterseiten im Volltext belegen; ATAS-Footprint am Herstellerdokument belegen
- Matrix um Datenquelle, Preismodell, Zielgruppe und Stand ergänzen; Validierungsverfahren (Modul 2) und Spreads, Pricing, Liquidität, Mindestgrößen (Modul 6) belegt ergänzen oder als n. v. kennzeichnen
- Analyse an die Ausgabestruktur des Prompts angleichen (M-DBOM als JSON-LD, Quellen mit Abrufdatum, Primär/Sekundär getrennt)

---

## 8 · QA-Scorecard

> **Automatisch erzeugt** aus den Gate-Zellen von `m300.html` (`qa/sync_module.py`, L49). Nicht von Hand ändern.

| Gate | Status | Begründung |
|---|---|---|
| C1 Disclaimer Anfang/Ende | ✓ | Zweitprüfung: alle sechs Pflichtbestandteile in Hero, Schluss, Analyse Anfang/Ende gelesen; L42-Test |
| C2 Keine Anlageempfehlung (MAR) | ✓ | – |
| C3 Steuer/Recht mit Primärquelle | ◐ | Primärquellen nur per Snippet eingesehen |
| C4 Neutralität / Interessenkonflikte | ◐ | Interessenkonflikte vom Herausgeber noch nicht bestätigt (L10b) |
| C5 Marken beschreibend | ✓ | – |
| C6 UWG-konforme Begriffe | ◐ | Begriffe neutral; Tatsachenangaben über Wettbewerber stützen sich nur auf Snippet-Medienangaben (Konfidenz 0,6–0,65) und sind nach § 6 UWG noch nicht voll nachprüfbar |
| C7 Ausgewogene Risikodarstellung | ✓ | – |
| C8 Regulatorische Bezüge belegt | ◐ | § 80 WpHG über Suchtreffer auf den Gesetzestext belegt; PRIIPs/UWG und § 63 Abs. 10 WpHG UNVERIFIED |
| C9 Datenschutz | ◐ | Modul: 0 Drittanbieter-Abrufe, kein Speicher (L20); verlinkte Datenschutzerklärung offen (L38) |
| Q1 Faktencheck K1–K9 vollständig | ◐ | Claim-Tabelle A01–A15; A11 ohne Beleg ([N. V.]); Ergebnisse nach L61 |
| Q2 Aktualität / Stichtag | ◐ | Kontraktdaten belegt (Abruf 2026-10-11); Originalabgleich offen; ✓ erst nach Messung (L10) |
| Q3 Mathematische Konsistenz | ✓ | – |
| Q4 Provenienz je Fakt | ◐ | Kontraktdaten und Struktur Eurex/Optionsscheine belegt; ✓ erst nach Zweitprüfung (L10) |
| Q5 Quellenqualität | ◐ | Primärquellen identifiziert, nicht im Volltext gelesen |
| Q6 Vollständigkeit | ◐ | Zweitprüfung: Matrix ohne Spalten Datenquelle, Preismodell, Zielgruppe, Stand; Modul 2 ohne Validierungsverfahren; Modul 6 ohne Spreads, Pricing, Liquidität, Mindestgrößen |
| Q7 Widerspruchsfreiheit | ◐ | Claims über k/k_differs an K-Zeilen gebunden (L61); ✓ erst nach Messung (L10) |
| Q8 Glossar | ✓ | Zweitprüfung: alle 15 Pflichtbegriffe vorhanden |
| Q9 Keine Überzeichnung / Halluzination | ◐ | Allaussage S11 mit n. v.-Fall (L06b), Fazit-Wertungen gekennzeichnet (L62); ✓ erst nach Zweitprüfung (L10) |
| Q10 Formatvorgaben | ◐ | Seite nach L41/L41b/L44 geprüft; Analyse weicht von der Ausgabestruktur des Prompts ab (M-DBOM als Tabelle statt JSON-LD, Quellen ohne Abrufdatum und ohne Trennung Primär/Sekundär) |

**Gesamtscore:** 6 × ✓ + 13 × ◐ = 12,5 von 19 Punkten = **65,8 %**.
**Freigabeempfehlung: ÜBERARBEITUNG.**

---

## 9 · Disclaimer, Marken-Hinweis, Interessenkonflikte

**Disclaimer.** Diese Analyse dient ausschließlich der allgemeinen Information und Bildung. Sie stellt keine
Anlageberatung, Anlagevermittlung oder Finanzportfolioverwaltung im Sinne von WpIG, KWG oder WpHG dar.
Sie ist keine Rechtsdienstleistung im Sinne des RDG und keine Hilfeleistung in Steuersachen im Sinne des
StBerG. Sie enthält keine Anlageempfehlung und keine Empfehlung einer Anlagestrategie im Sinne von Art. 3
Abs. 1 Nr. 34 und 35 MAR. Derivate wie Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind
komplexe Produkte mit Hebelwirkung. Sie können zum Totalverlust führen. Bei Futures und Stillhaltergeschäften
sind Verluste über den Kapitaleinsatz hinaus möglich. Diese Produkte sind nur für erfahrene Anleger geeignet,
die Hebel- und Knock-out-Mechanik verstehen und Verluste bis zum Totalverlust tragen können. Verbriefte Derivate tragen zusätzlich das
Emittentenrisiko. Vergangene Marktmuster und Modellausgaben sind kein verlässlicher Indikator für künftige
Entwicklungen. Steuerliche Ausführungen geben den recherchierten Rechtsstand zum 05.10.2026 wieder und
können sich ändern. Für Ihre persönliche Situation wenden Sie sich an einen Steuerberater oder Rechtsanwalt.
Alle Angaben ohne Gewähr.

**Marken-Hinweis.** ATAS, Options X-Ray, OptionsDepth, SpotGamma, HIRO, MenthorQ, Volland, Bookmap,
Interactive Brokers, TWS, Rithmic, CQG, Eurex, Cboe, VIX, OPRA, dxFeed, IQFeed, DAX, EURO STOXX 50, S&P 500, Nasdaq-100,
Gamma Cockpit, ORATS, Morgan Stanley, Sutor, Deutscher Derivate Verband (DDV), Stiftung Warentest und Deutsche Börse sind Marken oder Produktbezeichnungen ihrer jeweiligen Inhaber. Sie werden hier rein
beschreibend genannt. Es besteht keine Verbindung zu den Inhabern und keine Billigung durch sie.

**Interessenkonflikte.** Dem Verfasser sind keine Interessenkonflikte bekannt, insbesondere keine Affiliate-,
Partner- oder Vergütungsbeziehungen zu den genannten Anbietern. Der Herausgeber hat dies vor der
Veröffentlichung zu bestätigen.
