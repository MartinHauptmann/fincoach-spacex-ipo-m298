# FinCoach AI · Deep-Dive-Prime-Analyse · Modul M300

**ATAS Options X-Ray · Dealer-Greeks · Eurex-Börsenoptionen vs. verbriefte Derivate · Termingeschäfte im Steuerrecht**

| Feld | Wert |
|---|---|
| Modul | M300 (Platzhalter-ID) |
| Version | 1.7.0 (Entwurf) |
| Stichtag | 2026-10-05 |
| Zielstufe (CAT-Level) | Experte |
| Grundlage | Prompt `prompts/m300-atas-options-xray-deep-dive-prompt.md` v1.4.0; Quelltext vom 2026-10-05 (USER_PROVIDED) |
| Freigabeempfehlung | **ÜBERARBEITUNG** (siehe QA-Scorecard, Abschnitt 8) |

> **Disclaimer (Kurzfassung):** Diese Analyse ist eine allgemeine Information zu Bildungszwecken. Sie ist
> keine Anlageberatung oder Anlagevermittlung im Sinne von WpIG/KWG, keine Rechtsberatung im Sinne des RDG
> und keine Steuerberatung im Sinne des StBerG. Sie enthält keine Anlageempfehlung im Sinne von Art. 3 Abs. 1
> Nr. 35 MAR. Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind Hebelprodukte mit dem
> Risiko des Totalverlusts. Bei Futures und Stillhaltergeschäften (Verkauf von Optionen gegen Prämie) können die Verluste den Kapitaleinsatz
> übersteigen. Diese Produkte sind nur für erfahrene Anleger geeignet, die Hebel- und Knock-out-Mechanik
> verstehen und Verluste bis zum Totalverlust tragen können. Steuerliche Aussagen geben den recherchierten Rechtsstand zum Stichtag wieder und ersetzen
> keine individuelle Prüfung durch Steuerberater oder Rechtsanwalt.

> **Methodischer Vorbehalt:** Die Recherche lief über eine Netzwerkumgebung, die den direkten Abruf der
> meisten Primärquellen gesperrt hat, darunter gesetze-im-internet.de, recht.bund.de, bundesfinanzministerium.de,
> bundesfinanzhof.de, eurex.com, atas.net und die Anbieterseiten. Die Befunde beruhen auf Suchtreffern, die
> auf diese Primärquellen verweisen. Die URLs sind im Quellenverzeichnis aufgeführt. Fundstellen, deren
> Wortlaut nicht vollständig einsehbar war, tragen ein schwächeres Verdict oder **[N. V.]**.
> Vor einer Veröffentlichung sind sie am Original zu prüfen.

> **Aufbau (ab v1.7.0):** Diese Analyse ist eine faktgebundene Kurzfassung. Jede Tatsachenbehauptung nennt
> ihre Fakt-ID aus `provenance/m300.dbom.json`; Verdict und Konfidenz stehen dort. Abschnitt 2, die Module in
> Abschnitt 3 und das Glossar erzeugt `qa/sync_module.py` aus Modulseite und DBOM (L53). Die ausführliche
> Darstellung mit Diagrammen und Rechner steht auf der Modulseite `m300.html`.

---

## 1 · Executive Summary

Kernergebnisse; jede Aussage mit Fakt-ID:

- **Rechtsstand:** § 20 Abs. 6 Satz 5 und 6 EStG a. F. mit der 20.000-€-Grenze hat das JStG 2024 aufgehoben
  (`FACT_JSTG2024_REPEAL`). Dass dies nach § 52 Abs. 28 EStG in allen offenen Fällen gilt, ist nur per Snippet
  belegt (`FACT_P52_ABS28`, ungeprüft, Konfidenz 0,6). Das BMF-Schreiben vom 14.05.2025 setzt die Aufhebung um
  (`FACT_BMF_2025`).
- **Kapitalgesellschaften:** § 15 Abs. 4 Satz 3 EStG gilt über § 8 Abs. 1 KStG auch für sie (`FACT_P15_KSTG`).
- **Market Maker:** Eine gesetzliche Pflicht zum Orderbuch-Hedging besteht nicht (`FACT_MM_NO_HEDGE_DUTY`).
- **Produkt:** Die Suite umfasst zehn Indikatoren auf Basis eines 1-Minuten-CBOE-Feeds, nur für SPX-Optionen
  (`FACT_XRAY_10_IND`, `FACT_XRAY_1MIN_SPX`). Optionen sind in ATAS derzeit nicht handelbar (`FACT_ATAS_NO_OPT_TRADING`).
- **Modell:** Das GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (`FACT_DEALER_CONVENTION`,
  SCENARIO_PROJECTION, Konfidenz 0,5).
- **Wettbewerb:** Intraday-fähige Eurex-GEX bietet keiner der fünf bestimmbaren von sechs verglichenen Anbietern;
  für MenthorQ ist das n. v. (`FACT_NO_EUREX_GEX`, Medienangabe, Konfidenz 0,6).
- **Einschätzung [SZENARIO]:** Der Wert einer Eurex-Erweiterung läge damit in dieser Analyselücke, nicht in einem
  Steuervorteil (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0). Das ist keine Prognose.

---

## 2 · Phase A: Faktenprüfung K1–K12

### 2.1 Prüfprotokoll

<!-- sync:K -->
**K1 · Rechtsstand § 20 Abs. 6 S. 5/6 EStG.** Quelltext: 20.000-€-Grenze gilt „seit 2021“ fort. Das JStG 2024 (BGBl. 2024 I Nr. 387) hat die Sätze 5 und 6 aufgehoben, anwendbar in allen offenen Fällen (§ 52 Abs. 28 EStG, Satznummern ungeprüft); Umsetzung durch BMF-Schreiben vom 14.05.2025. Das Normzitat im Ausgangstext ist zudem falsch: Gemeint ist Satz 5, nicht Satz 6. Belege: (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9), (`FACT_P52_ABS28`, ungeprüft, Konfidenz 0,6), (`FACT_BMF_2025`, belegt, Konfidenz 0,85), (`FACT_TERMIN_2019`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (KRITISCH)

**K2 · BFH VIII B 113/23.** Quelltext: „mehrere Beschlüsse“; Unsicherheit bis zum BVerfG. Belegt ist ein Beschluss über die AdV (Aussetzung der Vollziehung) vom 07.06.2024 (summarische Prüfung, Streitjahr 2021). Durch die Aufhebung ist die Frage für Termingeschäfte erledigt. Anhängig bleibt laut Sekundärquelle (ungeprüft) 2 BvL 3/21 zu Aktienverlusten, ein anderer Sachverhalt. Belege: (`FACT_BFH_ADV`, belegt, Konfidenz 0,85), (`FACT_STOCK_LOSS_S4`, belegt, Konfidenz 0,7), (`FACT_BVERFG_PENDING`, ungeprüft, Konfidenz 0,6). **Ergebnis: ✗** (KRITISCH)

**K3 · Abgrenzung Termingeschäft.** Quelltext: Optionsscheine/Knock-outs steuerlich bevorzugt, Anleger „gedrängt“. Die Einordnung als Nicht-Termingeschäft ist korrekt (BMF seit 03.06.2021). Der Knock-out-Totalverlust fiel nach Auffassung der Finanzverwaltung aber unter Satz 6 a. F. (Sekundärbeleg, ungeprüft). Die Verdrängungsthese trägt heute nicht mehr. Belege: (`FACT_OS_KO_NOT_TERMIN`, belegt, Konfidenz 0,85), (`FACT_KO_SATZ6`, ungeprüft, Konfidenz 0,6), (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9). **Ergebnis: ◐** (WESENTLICH)

**K4 · Kapitalgesellschaft.** Quelltext: „keine Verlustverrechnungsbeschränkung“. Über § 8 Abs. 1 KStG gilt § 15 Abs. 4 Satz 3 EStG: eigener Verlustkreis für Termingeschäfte (BFH I R 25/14). Ausnahmen bestehen nur für Institute und Sicherungsgeschäfte. Belege: (`FACT_P15_KSTG`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (KRITISCH)

**K5 · Hedging-Pflicht Market Maker.** Quelltext: Market Maker „gesetzlich gezwungen“, über das Orderbuch zu hedgen. Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition in Abs. 5) regeln Quotierungs- und Vertragspflichten. Delta-Hedging ist Risikomanagement und kann über viele Kanäle erfolgen. Belege: (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85). **Ergebnis: ✗** (WESENTLICH)

**K6 · GEX-Prämisse.** Quelltext: Dealer-Hedging als feste Mechanik. Die Positionskonvention ist eine Modellannahme. Beim SPX ist sie durch Teilnehmer-markierte Cboe-Daten besser fundiert, bleibt aber anfällig für Spreads, Overwriting und Intraday-Volumen. (Modellannahme; Cboe-Daten: Medienangabe) Belege: (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, Konfidenz 0,5), (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (WESENTLICH)

**K7 · Emittenten-Hedging.** Quelltext: „keine“ Hedging-Spuren im FDAX. Emittenten hedgen dynamisch, auch über Basiswert und Gegengeschäfte. Die Spur ist schwach und nicht zurechenbar, aber nicht null. (Medienangabe) Belege: (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6). **Ergebnis: ◐** (HINWEIS)

**K8 · ATAS-Produktangaben.** Quelltext: 10 Indikatoren, CBOE/OptionsDepth, 60 s, nur SPX. Bestätigt durch Hilfe- und Lernseiten des Herstellers. Ergänzung: Optionen in ATAS derzeit nicht handelbar; Options Board/Strategy Analyzer als Beta. Belege: (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85), (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85), (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8). **Ergebnis: ✓** (HINWEIS)

**K9 · Wettbewerber.** Quelltext: Vergleich SpotGamma, MenthorQ, Volland, Bookmap, TWS. Weitgehend belegt (Hersteller- und Drittquellen); einzelne Felder n. v.; Preise sind Richtwerte. (Medienangaben) Belege: (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65). **Ergebnis: ◐** (HINWEIS)

**K10 · Eurex-Spezifikationen.** Quelltext: FDAX/FESX-Optionsketten, „Hexensabbat“. Gelistet sind Indexoptionen (ODAX 5 €/Pkt., OESX 10 €/Pkt.), keine Optionen auf die Futures. Fachbegriff: Quartalsverfall. End-of-Day-Optionen existieren (OEXP, ODAP); Verfälle an zehn Handelstagen sind nur für OEXP belegt. (OESX-Multiplikator und „keine Optionen auf Futures“: ungeprüft) Belege: (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85), (`FACT_OESX_MULT`, ungeprüft, Konfidenz 0,7), (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85). **Ergebnis: ◐** (HINWEIS)

**K11 · IBKR-Combo-Orders.** Quelltext: native Spread-Engine fehlt. Für ATAS zutreffend, aber zu präzisieren. Die IB-API unterstützt BAG-Combo-Orders (bis 6 Legs, Netto-Limit) bereits. Die Lücke liegt in UI, Risikoprüfung und Positionsführung. Belege: (`FACT_IB_BAG`, belegt, Konfidenz 0,85). **Ergebnis: ◐** (WESENTLICH)

**K12 · Warrant-Fair-Value-Tool.** Quelltext: „verdeckte Marge“, „künstliche Spread-Ausweitung“. Wertende Begriffe mit UWG-Risiko. Neutral: Fair-Value-Differenz, Emittentenaufschlag. Abgleich mit PRIIPs-KID; Emittentenbonität ist ein realer Wert, keine Marge. (Rechtsgrundlagen PRIIPs/UWG: ungeprüft) Belege: (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75). **Ergebnis: ◐** (WESENTLICH)

<!-- /sync:K -->

### 2.2 Korrekturliste zum Quelltext

<!-- sync:KORR -->
| Nr. | Schwere | Prüfpunkt | Ergebnis |
|---|---|---|---|
| K1 | KRITISCH | Rechtsstand § 20 Abs. 6 S. 5/6 EStG: 20.000-€-Grenze gilt „seit 2021“ fort | ✗ |
| K2 | KRITISCH | BFH VIII B 113/23: „mehrere Beschlüsse“; Unsicherheit bis zum BVerfG | ✗ |
| K3 | WESENTLICH | Abgrenzung Termingeschäft: Optionsscheine/Knock-outs steuerlich bevorzugt, Anleger „gedrängt“ | ◐ |
| K4 | KRITISCH | Kapitalgesellschaft: „keine Verlustverrechnungsbeschränkung“ | ✗ |
| K5 | WESENTLICH | Hedging-Pflicht Market Maker: Market Maker „gesetzlich gezwungen“, über das Orderbuch zu hedgen | ✗ |
| K6 | WESENTLICH | GEX-Prämisse: Dealer-Hedging als feste Mechanik | ◐ |
| K7 | HINWEIS | Emittenten-Hedging: „keine“ Hedging-Spuren im FDAX | ◐ |
| K9 | HINWEIS | Wettbewerber: Vergleich SpotGamma, MenthorQ, Volland, Bookmap, TWS | ◐ |
| K10 | HINWEIS | Eurex-Spezifikationen: FDAX/FESX-Optionsketten, „Hexensabbat“ | ◐ |
| K11 | WESENTLICH | IBKR-Combo-Orders: native Spread-Engine fehlt | ◐ |
| K12 | WESENTLICH | Warrant-Fair-Value-Tool: „verdeckte Marge“, „künstliche Spread-Ausweitung“ | ◐ |

<!-- /sync:KORR -->

---

## 3 · Phase B: Module 1–8 (faktgebundene Kurzfassung)

Je Modul die gebundenen Fakten aus der DBOM. Wertungen stehen nur in Modul 8 und sind als Einschätzung markiert.

<!-- sync:MOD -->
#### Modul 1 · Technologische Dekonstruktion der Options X-Ray Suite

- Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile). (`FACT_XRAY_10_IND`, belegt, Konfidenz 0,85)
- Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY. (`FACT_XRAY_1MIN_SPX`, belegt, Konfidenz 0,85)
- OptionsDepth deckt derzeit nur SPX und VIX ab. (`FACT_OPTIONSDEPTH_SCOPE`, belegt, Konfidenz 0,75)
- SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt. (`FACT_CBOE_OPENCLOSE`, Medienangabe, Konfidenz 0,6)
- GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls). (`FACT_DEALER_CONVENTION`, SCENARIO_PROJECTION, Konfidenz 0,5)
- Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES. (`FACT_GEX_EXAMPLE`, SCENARIO_PROJECTION, Konfidenz 1,0)

#### Modul 2 · Datenfeed-Architektur, Latenzprofil und Validierung

- Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung. (`FACT_XRAY_CONNECTIVITY`, belegt, Konfidenz 0,7)
- Start der Options X-Ray Suite am 04.09.2026. (`FACT_XRAY_LAUNCH`, ungeprüft, Konfidenz 0,6)
- OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster. (`FACT_OPRA_CAPACITY`, belegt, Konfidenz 0,7)
- Gemessene OPRA-Bursts über 180 Mio. Nachrichten/s (1-ms-Fenster). (`FACT_OPRA_BURSTS`, Medienangabe, Konfidenz 0,6)
- Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab. (`FACT_CHAIN_SUITE`, belegt, Konfidenz 0,85)

#### Modul 3 · Handels- und Ausführungsmöglichkeiten

- ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed. (`FACT_ATAS_CONNECTIONS`, belegt, Konfidenz 0,85)
- Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan). (`FACT_ATAS_NO_OPT_TRADING`, belegt, Konfidenz 0,8)
- ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026). (`FACT_CROSS_TRADING`, belegt, Konfidenz 0,85)
- IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit. (`FACT_IB_BAG`, belegt, Konfidenz 0,85)
- § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). (`FACT_ALGO_TRADING`, belegt, Konfidenz 0,85)
- Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. (`FACT_MM_NO_HEDGE_DUTY`, belegt, Konfidenz 0,85)

#### Modul 4 · Mikro-Makro-Synergien im praktischen Trading

- Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %. (`FACT_SPX_0DTE_59`, belegt, Konfidenz 0,85)
- Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. (`FACT_MAR_RECO`, belegt, Konfidenz 0,85)

#### Modul 5 · Globaler Wettbewerbsvergleich (Matrix auf der Modulseite, S09)

- Angaben der Wettbewerbsmatrix zu Fokus, Datenfrequenz, Greeks, Abdeckung, Orderflow und Ausführung von SpotGamma, MenthorQ, Volland, Bookmap und IBKR TWS. (`FACT_COMPETITOR_MATRIX`, Medienangabe, Konfidenz 0,65)
- Monatspreise der Anbieter: ATAS Ultra ca. 50–90 €, SpotGamma ca. 67–224 $, MenthorQ 129/349 $, Volland 150–1.000 $, Bookmap 39–99 $. (`FACT_VENDOR_PRICES`, Medienangabe, Konfidenz 0,55)
- Von sechs verglichenen Anbietern ist für fünf bestimmbar, dass keiner intraday-fähige Eurex-GEX anbietet; für MenthorQ n. v. Gamma Cockpit (nicht im Vergleichsfeld) liefert DAX-GEX nur auf Tagesbasis (Beta). (`FACT_NO_EUREX_GEX`, Medienangabe, Konfidenz 0,6)

#### Modul 6 · DACH-Marktspezifika und Rechtsstand

- § 20 Abs. 6 Satz 5 EStG a. F. (Termingeschäfte) und Satz 6 a. F. (Forderungsausfall, wertlose Wirtschaftsgüter), jeweils mit 20.000-€-Grenze, durch das JStG 2024 (BGBl. 2024 I Nr. 387) aufgehoben. (`FACT_JSTG2024_REPEAL`, belegt, Konfidenz 0,9)
- Die Aufhebung von § 20 Abs. 6 Satz 5 und 6 EStG a. F. ist nach § 52 Abs. 28 EStG in allen offenen Fällen anzuwenden. (`FACT_P52_ABS28`, ungeprüft, Konfidenz 0,6)
- BMF-Schreiben vom 14.05.2025 setzt die Aufhebung um; bestehende Verlustvorträge aus Termingeschäften sind danach unbeschränkt verrechenbar. (`FACT_BMF_2025`, belegt, Konfidenz 0,85)
- Einführung der Verlustverrechnungsbeschränkung für Termingeschäfte durch Gesetz vom 21.12.2019 (BGBl. I S. 2875): 10.000 € je Jahr, für Termingeschäfte ab 01.01.2021. (`FACT_TERMIN_2019`, belegt, Konfidenz 0,85)
- JStG 2020 vom 21.12.2020 (BGBl. I S. 3096) erhöht die Grenze auf 20.000 €. (`FACT_TERMIN_2020_RAISE`, Medienangabe, Konfidenz 0,65)
- BFH VIII B 113/23 vom 07.06.2024: Beschluss über die Aussetzung der Vollziehung (§ 69 Abs. 3 FGO; Streitjahr 2021), summarische Zweifel an der Verfassungsmäßigkeit (Art. 3 Abs. 1 GG). (`FACT_BFH_ADV`, belegt, Konfidenz 0,85)
- § 20 Abs. 6 Satz 4 EStG (Aktienverluste nur mit Aktiengewinnen) gilt fort. (`FACT_STOCK_LOSS_S4`, belegt, Konfidenz 0,7)
- Zu § 20 Abs. 6 Satz 4 EStG ist beim BVerfG die Vorlage 2 BvL 3/21 anhängig; eine Entscheidung wurde bis 05.10.2026 nicht gefunden. (`FACT_BVERFG_PENDING`, ungeprüft, Konfidenz 0,6)
- Optionsscheine und Knock-out-Zertifikate sind nach Auffassung der Finanzverwaltung keine Termingeschäfte im Sinne von § 20 Abs. 6 Satz 5 EStG a. F. (`FACT_OS_KO_NOT_TERMIN`, belegt, Konfidenz 0,85)
- Nach Auffassung der Finanzverwaltung (BMF 03.06.2021) fiel der Totalverlust eines Knock-out-Zertifikats als Verlust aus wertlosen Wirtschaftsgütern unter § 20 Abs. 6 Satz 6 EStG a. F. (`FACT_KO_SATZ6`, ungeprüft, Konfidenz 0,6)
- § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016. (`FACT_P15_KSTG`, belegt, Konfidenz 0,85)
- ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet. (`FACT_ODAX_SPECS`, belegt, Konfidenz 0,85)
- OESX: 10 € je Indexpunkt; Optionen auf DAX- bzw. EURO-STOXX-50-Futures wurden nicht gefunden. (`FACT_OESX_MULT`, ungeprüft, Konfidenz 0,7)
- Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. (`FACT_EUREX_OI`, belegt, Konfidenz 0,85)
- Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen. (`FACT_EUREX_DAILY_LAUNCH`, belegt, Konfidenz 0,85)
- ADV seit Produktstart: OEXP ca. 30.900 Kontrakte, ODAP ca. 2.300 Kontrakte. (`FACT_EUREX_DAILY_ADV`, ungeprüft, Konfidenz 0,6)
- Anteile am Börsenumsatz verbriefter Derivate (jeweils am Gesamtumsatz): Hebelprodukte ca. 84 %, darunter Knock-outs ca. 59 % und Optionsscheine ca. 19 %. (`FACT_BSW_SHARES`, ungeprüft, Konfidenz 0,6)
- Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte. (`FACT_ISSUER_HEDGING`, Medienangabe, Konfidenz 0,6)
- Strukturvergleich Eurex-Optionen vs. Optionsscheine/Knock-outs: Rechtsnatur, Kontrahentenrisiko (CCP vs. Emittent), Preisbildung, Volatilität im Preis, Stillhalterfähigkeit. (`FACT_PRODUCT_STRUCTURE`, ungeprüft, Konfidenz 0,5)
- BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen. (`FACT_BAFIN_TURBO`, belegt, Konfidenz 0,85)
- BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023. (`FACT_BAFIN_STUDY`, ungeprüft, Konfidenz 0,7)
- Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG. (`FACT_PRIIPS_UWG`, ungeprüft, Konfidenz 0,75)
- Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG. (`FACT_ANGEMESSENHEIT`, ungeprüft, Konfidenz 0,7)

#### Modul 7 · Strategische Produkt-Roadmap [SZENARIO]

- Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge. (`FACT_ROADMAP`, SCENARIO_PROJECTION, Konfidenz 0,0)

#### Modul 8 · Fazit [Einschätzung]


Belegt sind Produktumfang (Modul 1–3) und Rechtsstand (Modul 6); die GEX-Profile beruhen auf einer Modellannahme (`FACT_DEALER_CONVENTION`). Die strategische These zur Eurex-Erweiterung ist ein Szenario (`FACT_ROADMAP`) und keine Prognose.

<!-- /sync:MOD -->

### 3.9 Modellrechnung [MODELL]

Die Berechnungslogik der Indikatoren ist nicht öffentlich dokumentiert. Die folgenden Formeln sind die
fachübliche Referenzmodellierung und nicht die belegte Implementierung des Herstellers (`FACT_DEALER_CONVENTION`,
`FACT_GEX_EXAMPLE`).

Ausgangspunkt ist das Dollar-Gamma je Strike. Es gibt an, um wie viele Dollar sich das Hedge-Delta der
Dealer bei einer Bewegung des Basiswerts um ein Prozent verändert:

$$
GEX_K \;=\; \sum_{i \in K} s_i \cdot \Gamma_i \cdot OI_i \cdot M \cdot S^2 \cdot 0{,}01
$$

Dabei ist $\Gamma_i$ das Black-Scholes-Gamma der Option $i$ je Indexpunkt, $OI_i$ ihr Open Interest in
Kontrakten, $M$ der Kontraktmultiplikator (SPX: 100) und $S$ der Indexstand. $s_i \in \{+1,-1\}$ ist die
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
Zeit. Ihr Nutzen hängt allerdings vollständig von der Richtigkeit der Positionsannahme $s_i$ ab (K6).

Die Umrechnung in **ES-Äquivalente** macht die Größen für Futures-Händler lesbar. Das Hedge-Delta der Dealer
in Indexeinheiten ist $\sum_i s_i\,\Delta_i\,OI_i\,M_{SPX}$. Geteilt durch den ES-Multiplikator ergibt sich
die Kontraktzahl:

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
| Open Interest | Bestand nicht glattgestellter Kontrakte je Serie. | Wird nach Handelsschluss veröffentlicht (T+1); Basis der GEX-Profile. |
| Implizite Volatilität | Aus dem Optionspreis zurückgerechnete Volatilität. | Fläche über Strike und Laufzeit; Eingang für Vanna-Effekte. |
| Delta-Divergenz | Abweichung zwischen Preisverlauf und kumuliertem Delta. | Schwächeres Umkehrsignal im Short-Gamma-Regime. |
| BAG / Combo-Order | IB-Ordertyp für Spreads mit Netto-Limit. | Schützt vor Legging-Risiko; in ATAS derzeit nicht integriert. (`FACT_IB_BAG`, `FACT_ATAS_NO_OPT_TRADING`) |
| Angemessenheitsprüfung | Abfrage von Kenntnissen und Erfahrungen vor dem Handel. | Für komplexe Produkte vorgeschrieben (Fundstelle in S10, ungeprüft). |
| Optionsschein | Verbriefte Option, rechtlich eine Schuldverschreibung. | Emittentenrisiko; kein öffentliches Open Interest je Strike. |
| 0DTE | Zero Days to Expiration; beim SPX an jedem Wochentag. | Großer Teil des SPX-Volumens (Kennzahl in S01); erzeugt Intraday-Positionen ohne OI-Spur. |
| GEX | Gamma Exposure: aggregiertes Dollar-Gamma der Dealer-Positionen. | $\sum s_i\Gamma_i OI_i M S^2\cdot 0{,}01$; Vorzeichen hängt an der Positionsannahme. |
| GEX-Flip | Preis, an dem das Netto-Gamma das Vorzeichen wechselt. | Grenze zwischen dämpfendem und verstärkendem Hedging-Regime. |
| Call/Put Wall | Strikes mit der höchsten Call- bzw. Put-Gamma-Konzentration. | Modellhafte Widerstands-/Unterstützungszonen; keine Preisgarantie. |
| Charm | Änderung des Deltas pro Zeiteinheit. | $\partial\Delta/\partial t$; stark bei 0DTE und vor Verfall. |
| Vanna | Änderung des Deltas pro Änderung der impliziten Volatilität. | $\partial\Delta/\partial\sigma$; treibt Flows nach IV-Crush/-Spikes. |
| ES-Äquivalent | Hedge-Delta geteilt durch den ES-Multiplikator (50). | SPX-Multiplikator 100 / ES 50 / MES 5; Basis SPX↔ES beachten. |
| OPRA | Options Price Reporting Authority. | Datenraten weit jenseits von Desktop-Kapazitäten (Kennzahlen in S07); ungefiltert nicht verarbeitbar. |
| MBO | Market by Order (Level 3). | Erlaubt Queue-Position, Iceberg- und Sweep-Erkennung. |
| Footprint | Volumen getrennt nach Bid/Ask je Kerze. | Grundlage für Absorption und Delta-Divergenz. |
| Absorption | Aggressives Volumen wird von passiven Orders aufgenommen. | Bestätigungssignal für Wall-Thesen im Long-Gamma-Regime. |
| Sweep | Aggressive Order über mehrere Levels in einem Zug. | Widerlegungssignal für Wall-Thesen; oft Short-Gamma-Beschleunigung. |
| Iceberg | Order mit verdecktem Volumen, die nachgefüllt wird. | Im MBO über wiederholte Ausführungen derselben Order-ID erkennbar. |
| Termingeschäft (steuerlich) | Options-, Futures- oder Swapgeschäft mit Differenzausgleich oder Lieferung; Einkünfte nach § 20 EStG. | Sonderbeschränkung (§ 20 Abs. 6 Satz 5 a. F.) durch JStG 2024 aufgehoben. (`FACT_JSTG2024_REPEAL`) |
| Knock-out-Zertifikat | Verbriefte Schuldverschreibung mit Knock-out-Barriere. | Für Turbos gilt eine BaFin-Allgemeinverfügung (Details in S10). (`FACT_BAFIN_TURBO`) |
| CCP | Central Counterparty, hier Eurex Clearing. | Ersetzt bilaterales Kontrahentenrisiko durch Margin-System. |
| PRIIPs-KID | EU-Basisinformationsblatt (VO (EU) 1286/2014, Fundstelle ungeprüft). | Referenz für Kostenvergleiche verbriefter Derivate. (`FACT_PRIIPS_UWG`) |
| Quartalsverfall | Dritter Freitag der Quartalsmonate. | Umgangssprachlich „Hexensabbat“; OI-Verschiebungen davor relevant. |

<!-- /sync:GLOSSAR -->

---

## 5 · Quellenverzeichnis

Abgerufen 2026-10-05 bis 2026-10-08, überwiegend über Suchtreffer-Snippets (siehe Methodischer Vorbehalt). Das
Verzeichnis ist ein Auszug aus `provenance/m300.dbom.json` (Lehre L13/L14) und wird von dort erzeugt, nicht von
Hand gepflegt. Die S-Nummern sind die Belegverweise in dieser Analyse.

| Nr. | Quelle | Stufe | DBOM-ID | URL |
|---|---|---|---|---|
| S1 | Jahressteuergesetz 2024, BGBl. 2024 I Nr. 387 | Primärquelle | `SRC_BGBL_JSTG2024` | https://www.recht.bund.de/bgbl/1/2024/387/regelungstext.pdf |
| S2 | BT-Drs. 20/13419, 20/13420, 20/12780 (JStG 2024) | Primärquelle | `SRC_BT_DRS` | https://dserver.bundestag.de/btd/20/134/2013420.pdf |
| S3 | Gesetz zur Einführung einer Pflicht zur Mitteilung grenzüberschreitender Steuergestaltungen (BGBl. I 2019 S. 2875) | Primärquelle | `SRC_BZST_2019` | https://www.bzst.de/SharedDocs/Downloads/DE/DAC6/dac6_gesetz_grenzueberschreitender_steuergestaltungen.pdf |
| S4 | BMF-Schreiben Einzelfragen zur Abgeltungsteuer, 14.05.2025 | Primärquelle | `SRC_BMF_2025` | https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Abgeltungsteuer/2025-05-14-einzelfragen-zur-abgeltungsteuer.pdf |
| S5 | BFH, Beschluss v. 07.06.2024, VIII B 113/23 | Primärquelle | `SRC_BFH_VIIIB11323` | https://www.bundesfinanzhof.de/en/entscheidungen/entscheidungen-online/decision-detail/STRE202410113/ |
| S6 | FG Rheinland-Pfalz 1 V 1674/23 (tax-news, Sekundärquelle) | Sekundärquelle | `SRC_FG_RLP` | https://www.tax-news.de/news/fg-rheinland-pfalz-haelt-verfassungsmaessigkeit-der-verlustverrechnungsbeschraenkung-bei-termingeschaeften-fuer-zweifelhaft/ |
| S7 | BMF-Schreiben vom 03.06.2021 (Anhang 19 EStH) | Primärquelle | `SRC_BMF_2021` | https://ao.bundesfinanzministerium.de/esth/2024/C-Anhaenge/Anhang-19/II/anhang-19-II.html |
| S8 | § 20 EStG (EStH 2025) | Primärquelle | `SRC_ESTG_20` | https://esth.bundesfinanzministerium.de/esth/2025/A-Einkommensteuergesetz/II-Einkommen-2-24b/8-Die-einzelnen-Einkunftsarten-13-24b/e-Kapitalvermoegen-20/Paragraf-20/paragraf-20.html |
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
| S23 | SpotGamma (Preise, HIRO) | Herstellerquelle | `SRC_SPOTGAMMA` | https://spotgamma.com/hiro-indicator/ |
| S24 | MenthorQ (Preise, Abdeckung) | Herstellerquelle | `SRC_MENTHORQ` | https://menthorq.com/guide/menthorq-asset-coverage/ |
| S25 | Volland (ORATS-Partnerseite, User Guide) | Sekundärquelle | `SRC_VOLLAND` | https://orats.com/volland |
| S26 | Bookmap (Pakete, Konnektivität) | Herstellerquelle | `SRC_BOOKMAP` | https://bookmap.com/en/packages-comparison |
| S27 | Interactive Brokers · OptionTrader / TWS | Herstellerquelle | `SRC_IBKR` | https://www.interactivebrokers.com/en/software/pdfhighlights/PDF-OptionTrader.php |
| S28 | Gamma Cockpit (DAX-GEX, Beta) | Herstellerquelle | `SRC_GAMMACOCKPIT` | https://gammacockpit.com/ |
| S29 | Eurex · Produktseiten DAX-Optionen (ODAX), Micro-DAX-Optionen (ODXS), EURO STOXX 50 Options | Primärquelle | `SRC_EUREX_SPECS` | https://www.eurex.com/ex-en/markets/idx/dax/DAX-Options-139884 |
| S30 | Eurex Circulars OEXP 047/23 und 117/25 | Primärquelle | `SRC_EUREX_CIRCULARS` | https://www.eurex.com/ex-en/find/circulars/circular-4844340 |
| S31 | Eurex · Whitepaper EURO STOXX 50 Options / Präsentation Daily Options | Primärquelle | `SRC_EUREX_WHITEPAPER` | https://www.eurex.com/resource/blob/3617154/068c57ac37e964429b57ff10fcd78f53/data/presentation-daily-options.pdf |
| S32 | Cboe · Trading Volume December and Full Year 2025 | Primärquelle | `SRC_CBOE_FY2025` | https://ir.cboe.com/news/news-details/2026/Cboe-Global-Markets-Reports-Trading-Volume-for-December-and-Full-Year-2025/default.aspx |
| S33 | OPRA · Capacity Projections Update (Sept. 2025) | Primärquelle | `SRC_OPRA` | https://cdn.opraplan.com/documents/notices/OPRA_Capacity_Projections_Update_0925.pdf |
| S34 | BSW · Börsenumsätze verbriefter Derivate | Primärquelle | `SRC_BSW` | https://www.derbsw.de/de/boersenumsaetze/ |
| S35 | Delegierte VO (EU) 2016/958 (Anlageempfehlungen) | Primärquelle | `SRC_DELVO_958` | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32016R0958 |
| S36 | CMS · Aufhebung der Verlustabzugsbeschränkung (Sekundärquelle) | Sekundärquelle | `SRC_CMS` | https://cms.law/de/deu/legal-updates/Ade-Verlustabzugsbeschraenkung-fuer-Termingeschaefte-Gesetzgeber-bereinigt-Verfassungswidrigkeit |
| S37 | Databento · Processing OPRA in real time (Sekundärquelle) | Sekundärquelle | `SRC_DATABENTO` | https://databento.com/blog/beyond-40-gbps-processing-opra-in-real-time |
| S38 | steuertipps.de · Stand 2 BvL 3/21 (Sekundärquelle) | Sekundärquelle | `SRC_STEUERTIPPS` | https://www.steuertipps.de/altersvorsorge-rente-finanzen/aktienverluste-nur-mit-aktiengewinnen-verrechenbar-verfassungswidrig |
| S39 | Preisseiten ATAS, SpotGamma, MenthorQ, ORATS/Volland, Bookmap (Snippets/Drittquellen; Sekundärquelle) | Sekundärquelle | `SRC_PRICES` | https://atas.net/pricing/ |
| S40 | Handelsblatt · Erhöhung auf 20.000 € durch JStG 2020 (Sekundärquelle) | Sekundärquelle | `SRC_HB_JSTG2020` | https://www.handelsblatt.com/finanzen/steuern-recht/steuern/umstrittene-regelung-groko-bessert-bei-steuerlicher-verlustverrechnung-von-termingeschaeften-nach/26697238.html |
| S41 | BaFin · Studie Turbo-Zertifikate (2025) | Primärquelle | `SRC_BAFIN_STUDY` | https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Fachartikel/2025/Studie_250521_Turbo_Zertifikate.html |
| S42 | MenthorQ · Cboe Market-Maker-Tagged Data erklärt (Sekundärquelle) | Sekundärquelle | `SRC_MENTHORQ_GUIDE` | https://menthorq.com/guide/cboe-market-maker-tagged-data-explained/ |
| S44 | VO (EU) Nr. 1286/2014 (PRIIPs) | Primärquelle | `SRC_PRIIPS` | https://eur-lex.europa.eu/eli/reg/2014/1286/oj |
| S45 | test.de · Studie zu Turbo-Zertifikaten (Sekundärquelle) | Sekundärquelle | `SRC_TESTDE` | https://www.test.de/Studie-zu-Turbo-Zertifikaten-Die-meisten-Anleger-machen-mit-Turbo-Zertifikaten-Verluste-6227752-0/ |
| S46 | Eurex · Daily Options (OEXP/ODAP) | Primärquelle | `SRC_EUREX_DAILY` | https://www.eurex.com/ex-en/markets/idx/daily-opt |
| S47 | § 63 WpHG (Wohlverhaltenspflichten) | Primärquelle | `SRC_WPHG_63` | https://www.gesetze-im-internet.de/wphg/__63.html |
| S48 | Sutor Bank · Formular Angemessenheit nach § 63 Abs. 10 WpHG (Sekundärquelle) | Sekundärquelle | `SRC_SUTOR` | https://www.sutorbank.de/fileadmin/Dateien/Service/Formulare/Investmentsparvertraege/Angaben-zur-Feststellung-der-Angemessenheit.pdf |
| S49 | OptionsDepth (Abdeckung, API) | Herstellerquelle | `SRC_OPTIONSDEPTH` | https://optionsdepth.com/ |
| S50 | Eurex · Statistiken / Extended Market Data Service (Open Interest) | Primärquelle | `SRC_EUREX_STATS` | https://www.eurex.com/ex-en/data/statistics |
| S51 | DZ BANK Steuerinformation Ausgabe 2/2021 (Knock-out-Verluste und § 20 Abs. 6 Satz 6 EStG) | Sekundärquelle | `SRC_DZB_2021` | https://www.pax-bank.de/content/dam/f0395-0/externeinhalte/pdf/verbund/DZB%20Steuerinformation%20Ausgabe%202%202021.pdf |

---

## 6 · M-DBOM (Data Bill of Materials)

Führende Provenienzliste ist **`provenance/m300.dbom.json`** (Lehre L13: eine DBOM für Seite und Analyse). Die
Tabelle ist ein Auszug daraus und wird bei Änderungen neu erzeugt, nicht von Hand gepflegt. Stand: Modul v1.7.0,
46 Fakten, 53 Quellen.

| ID | Verdict | Klasse | Konf. | Bezugszeitraum | Claim |
|---|---|---|---|---|---|
| `FACT_JSTG2024_REPEAL` | CONFIRMED | REGULATORY_FRAMEWORK | 0,9 | Rechtsstand 2026-10-05 (JStG 2024 vom 02.12.2024) | § 20 Abs. 6 Satz 5 EStG a. F. (Termingeschäfte) und Satz 6 a. F. (Forderungsausfall, wertlose Wirtschaftsgüter), jeweils mit 20.000-€-Grenze, durch das JStG 2024 (BGBl. 2024 I Nr. 387) aufgehoben. |
| `FACT_P52_ABS28` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,6 | Rechtsstand 2026-10-05 | Die Aufhebung von § 20 Abs. 6 Satz 5 und 6 EStG a. F. ist nach § 52 Abs. 28 EStG in allen offenen Fällen anzuwenden. |
| `FACT_BMF_2025` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | BMF-Schreiben 14.05.2025 | BMF-Schreiben vom 14.05.2025 setzt die Aufhebung um; bestehende Verlustvorträge aus Termingeschäften sind danach unbeschränkt verrechenbar. |
| `FACT_TERMIN_2019` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Gesetz vom 21.12.2019, Anwendung ab 01.01.2021 | Einführung der Verlustverrechnungsbeschränkung für Termingeschäfte durch Gesetz vom 21.12.2019 (BGBl. I S. 2875): 10.000 € je Jahr, für Termingeschäfte ab 01.01.2021. |
| `FACT_TERMIN_2020_RAISE` | MEDIA_REPORT | REGULATORY_FRAMEWORK | 0,65 | JStG 2020 vom 21.12.2020 | JStG 2020 vom 21.12.2020 (BGBl. I S. 3096) erhöht die Grenze auf 20.000 €. |
| `FACT_BFH_ADV` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Beschluss 07.06.2024 | BFH VIII B 113/23 vom 07.06.2024: Beschluss über die Aussetzung der Vollziehung (§ 69 Abs. 3 FGO; Streitjahr 2021), summarische Zweifel an der Verfassungsmäßigkeit (Art. 3 Abs. 1 GG). |
| `FACT_STOCK_LOSS_S4` | CONFIRMED | REGULATORY_FRAMEWORK | 0,7 | Rechtsstand 2026-10-05 | § 20 Abs. 6 Satz 4 EStG (Aktienverluste nur mit Aktiengewinnen) gilt fort. |
| `FACT_BVERFG_PENDING` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,6 | Stand 05.10.2026 | Zu § 20 Abs. 6 Satz 4 EStG ist beim BVerfG die Vorlage 2 BvL 3/21 anhängig; eine Entscheidung wurde bis 05.10.2026 nicht gefunden. |
| `FACT_OS_KO_NOT_TERMIN` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | BMF 03.06.2021, fortgeführt 14.05.2025 | Optionsscheine und Knock-out-Zertifikate sind nach Auffassung der Finanzverwaltung keine Termingeschäfte im Sinne von § 20 Abs. 6 Satz 5 EStG a. F. |
| `FACT_KO_SATZ6` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,6 | BMF 03.06.2021 bis Aufhebung durch JStG 2024 | Nach Auffassung der Finanzverwaltung (BMF 03.06.2021) fiel der Totalverlust eines Knock-out-Zertifikats als Verlust aus wertlosen Wirtschaftsgütern unter § 20 Abs. 6 Satz 6 EStG a. F. |
| `FACT_P15_KSTG` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis für Termingeschäfte) gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften; Satz 4: Ausnahmen für Institute und Absicherungsgeschäfte; Satz 5: Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b Abs. 2 KStG). Rechtsprechung: BFH I R 25/14 vom 06.07.2016. |
| `FACT_MM_NO_HEDGE_DUTY` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. |
| `FACT_ALGO_TRADING` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). |
| `FACT_MAR_RECO` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. |
| `FACT_PRIIPS_UWG` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,75 | Rechtsstand 2026-10-05 | Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG, die Herabsetzung von Mitbewerbern § 4 Nr. 1 UWG. |
| `FACT_ANGEMESSENHEIT` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,7 | Rechtsstand 2026-10-05 | Angemessenheitsprüfung (Kenntnisse und Erfahrungen) vor dem Handel komplexer Produkte nach § 63 Abs. 10 WpHG. |
| `FACT_BAFIN_TURBO` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Allgemeinverfügung 15.10.2025, in Kraft 16.06.2026 | BaFin-Allgemeinverfügung zu Turbo-/Knock-out-Zertifikaten vom 15.10.2025 (Art. 42 MiFIR, § 15 WpHG), in Kraft seit 16.06.2026: standardisierter Risikohinweis, Wissenstest, Verbot von Kaufanreizen. |
| `FACT_BAFIN_STUDY` | UNVERIFIED | MARKET_DATA | 0,7 | Untersuchungszeitraum 2019–2023 | BaFin-Studie: Rund 74,2 % der Kleinanleger erlitten mit Turbo-Zertifikaten Verluste; Untersuchungszeitraum 2019–2023. |
| `FACT_XRAY_10_IND` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Options X-Ray Suite umfasst zehn Indikatoren (Market State, Expected Move, GEX/Charm/Strike Heatmap, Big Trades, Flow, Flow Delta, Strike Profile, Surface Profile). |
| `FACT_XRAY_1MIN_SPX` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Datenbasis 1-Minuten-CBOE-Feed mit Analytik von OptionsDepth; nur SPX-Optionen, Anzeige auf ES/MES/SPY. |
| `FACT_OPTIONSDEPTH_SCOPE` | CONFIRMED | VENDOR_CLAIM | 0,75 | Herstellerangabe Stand 2026-10-05 | OptionsDepth deckt derzeit nur SPX und VIX ab. |
| `FACT_XRAY_CONNECTIVITY` | CONFIRMED | VENDOR_CLAIM | 0,7 | Changelog Stand 2026-10-05 | Options X-Ray setzt eine Verbindung über Rithmic oder Interactive Brokers voraus; CQG ist in Entwicklung. |
| `FACT_XRAY_LAUNCH` | UNVERIFIED | VENDOR_CLAIM | 0,6 | Changelog Stand 2026-10-05 | Start der Options X-Ray Suite am 04.09.2026. |
| `FACT_ATAS_CONNECTIONS` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über TWS) an, als Datenfeeds dxFeed und IQFeed. |
| `FACT_CHAIN_SUITE` | CONFIRMED | VENDOR_CLAIM | 0,85 | Herstellerdoku Stand 2026-10-05 | Die Options Chain Suite arbeitet mit dem täglichen Open-Interest-Snapshot (EOD) und deckt ES, NQ, CL und GC ab. |
| `FACT_ATAS_NO_OPT_TRADING` | CONFIRMED | VENDOR_CLAIM | 0,8 | Herstellerdoku Stand 2026-10-05 | Optionen sind in ATAS derzeit nicht handelbar; Options Board und Strategy Analyzer als Beta (Ultra-Plan). |
| `FACT_CROSS_TRADING` | CONFIRMED | VENDOR_CLAIM | 0,85 | ATAS 8.0.12 (17.02.2026) | ES/MES-Cross-Trading seit ATAS 8.0.12 (17.02.2026). |
| `FACT_IB_BAG` | CONFIRMED | VENDOR_CLAIM | 0,85 | API-Doku Stand 2026-10-05 | IB TWS API unterstützt Combo-Orders (secType BAG) mit bis zu 6 Legs und Netto-Limit. |
| `FACT_CBOE_OPENCLOSE` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | SPX-Optionen werden nur an der Cboe gehandelt; Cboe stellt nach Teilnehmertyp markierte Open-Close-Daten bereit, auf die sich OptionsDepth stützt. |
| `FACT_SPX_0DTE_59` | CONFIRMED | MARKET_DATA | 0,85 | Gesamtjahr 2025 | Anteil 0DTE am SPX-Optionsvolumen 2025 rund 59 %. |
| `FACT_OPRA_CAPACITY` | CONFIRMED | MARKET_DATA | 0,7 | Projektion Sept. 2025 | OPRA-Kapazitätsprojektion: Spitzenlast je Stream 37,3 Gbps im 1-ms-Fenster. |
| `FACT_OPRA_BURSTS` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | April 2025 | Gemessene OPRA-Bursts über 180 Mio. Nachrichten/s (1-ms-Fenster). |
| `FACT_ODAX_SPECS` | CONFIRMED | MARKET_DATA | 0,85 | Produktseite Stand 2026-10-05 | ODAX: 5 € je Indexpunkt, europäisch, Barausgleich, Basiswert DAX-Index; Micro-DAX-Optionen (ODXS) sind gelistet. |
| `FACT_EUREX_OI` | CONFIRMED | MARKET_DATA | 0,85 | Stand 2026-10-05 | Eurex veröffentlicht das Open Interest je Serie täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. |
| `FACT_PRODUCT_STRUCTURE` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,5 | Stand 2026-10-05 | Strukturvergleich Eurex-Optionen vs. Optionsscheine/Knock-outs: Rechtsnatur, Kontrahentenrisiko (CCP vs. Emittent), Preisbildung, Volatilität im Preis, Stillhalterfähigkeit. |
| `FACT_OESX_MULT` | UNVERIFIED | MARKET_DATA | 0,7 | Stand 2026-10-05 | OESX: 10 € je Indexpunkt; Optionen auf DAX- bzw. EURO-STOXX-50-Futures wurden nicht gefunden. |
| `FACT_EUREX_DAILY_LAUNCH` | CONFIRMED | MARKET_DATA | 0,85 | Eurex-Circulars 2023–2026 | Eurex: OEXP (EURO STOXX 50 End-of-Day Options) seit 28.08.2023, ODAP (DAX End-of-Day Options) seit 13.11.2023; OEXP seit 05.01.2026 mit Verfällen an zehn Handelstagen. |
| `FACT_EUREX_DAILY_ADV` | UNVERIFIED | MARKET_DATA | 0,6 | seit Produktstart, Stand n. v. | ADV seit Produktstart: OEXP ca. 30.900 Kontrakte, ODAP ca. 2.300 Kontrakte. |
| `FACT_BSW_SHARES` | UNVERIFIED | MARKET_DATA | 0,6 | n. v. | Anteile am Börsenumsatz verbriefter Derivate (jeweils am Gesamtumsatz): Hebelprodukte ca. 84 %, darunter Knock-outs ca. 59 % und Optionsscheine ca. 19 %. |
| `FACT_ISSUER_HEDGING` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | Emittenten sichern ihr Nettorisiko laufend dynamisch ab, über den Basiswert oder passende Gegengeschäfte. |
| `FACT_COMPETITOR_MATRIX` | MEDIA_REPORT | MEDIA_REPORT | 0,65 | Stand 2026-10-05 | Angaben der Wettbewerbsmatrix zu Fokus, Datenfrequenz, Greeks, Abdeckung, Orderflow und Ausführung von SpotGamma, MenthorQ, Volland, Bookmap und IBKR TWS. |
| `FACT_VENDOR_PRICES` | MEDIA_REPORT | MEDIA_REPORT | 0,55 | Stand 2026-10-05 | Monatspreise der Anbieter: ATAS Ultra ca. 50–90 €, SpotGamma ca. 67–224 $, MenthorQ 129/349 $, Volland 150–1.000 $, Bookmap 39–99 $. |
| `FACT_NO_EUREX_GEX` | MEDIA_REPORT | MEDIA_REPORT | 0,6 | Stand 2026-10-05 | Von sechs verglichenen Anbietern ist für fünf bestimmbar, dass keiner intraday-fähige Eurex-GEX anbietet; für MenthorQ n. v. Gamma Cockpit (nicht im Vergleichsfeld) liefert DAX-GEX nur auf Tagesbasis (Beta). |
| `FACT_DEALER_CONVENTION` | SCENARIO_PROJECTION | MODEL_ASSUMPTION | 0,5 | – | GEX-Vorzeichen beruht auf einer Annahme über die Dealer-Position (Kunden long Puts / short Calls). |
| `FACT_GEX_EXAMPLE` | SCENARIO_PROJECTION | SCENARIO_PROJECTION | 1,0 | – | Zahlenbeispiel: S=6.500, OI=10.000, Γ=0,002 → GEX 845 Mio. USD je 1 % ≈ 2.600 ES. |
| `FACT_ROADMAP` | SCENARIO_PROJECTION | SCENARIO_PROJECTION | 0,0 | – | Vier Roadmap-Erweiterungen (Multi-Asset, Eurex, Multi-Leg, Warrant-Fair-Value) sind Vorschläge. |

---

## 7 · Offene Prüfpunkte vor Veröffentlichung

- Wortlaut § 52 Abs. 28 EStG und BMF-Randziffern am Original prüfen
- Stand BVerfG 2 BvL 3/21 prüfen
- ATAS-Start (04.09.2026) und Preise prüfen
- Wettbewerbspreise beim Anbieter prüfen
- OESX-Multiplikator auf eurex.com bestätigen
- Bezugszeitraum der BSW-Umsatzstatistik klären
- Primärquellen im Volltext lesen (BGBl., BMF, BFH, Eurex, ATAS)
- Interessenkonflikte durch Herausgeber bestätigen
- PRIIPs-/UWG-Bezüge und § 63 Abs. 10 WpHG am Original prüfen
- Datenschutzerklärung korrigieren: sessionStorage, Stand-Datum, Log-Speicherdauer, Vorlagenhinweis
- Faktgebundene Analyse v1.7.0 (Kennzeichnung je Fakt-ID, L51, L53) durch unabhängige Zweitprüfung bestätigen
- Knock-out-Totalverlust unter § 20 Abs. 6 Satz 6 a. F. im BMF-Schreiben 2021 (Randziffer) prüfen
- Strukturvergleich Eurex vs. Optionsscheine mit Primärquellen (Eurex Clearing, Emittentenbedingungen) belegen
- Bezugszeitraum der OEXP/ODAP-ADV und Volltext der BaFin-Turbo-Studie prüfen
- Gestraffte Analyse v1.7.0 (unbelegte Angaben entfallen, L43, L53) durch unabhängige Zweitprüfung bestätigen
- Analyse v1.7.0 ohne Hand-Konfidenzen und Provenienzkürzel, BMF-Fakt ohne Teilaussage „offene Fälle“ (L48b, L05d) durch unabhängige Zweitprüfung bestätigen

---

## 8 · QA-Scorecard

> **Automatisch erzeugt** aus den Gate-Zellen von `m300.html` (`qa/sync_module.py`, L49). Nicht von Hand ändern.

| Gate | Status | Begründung |
|---|---|---|
| C1 Disclaimer Anfang/Ende | ✓ | Sechste Zweitprüfung: alle sechs Pflichtbestandteile in Hero, Schluss, Analyse Anfang/Ende gelesen; L42-Test |
| C2 Keine Anlageempfehlung (MAR) | ✓ | – |
| C3 Steuer/Recht mit Primärquelle | ◐ | Primärquellen nur per Snippet eingesehen |
| C4 Neutralität / Interessenkonflikte | ◐ | Interessenkonflikte vom Herausgeber noch nicht bestätigt (L10b) |
| C5 Marken beschreibend | ✓ | – |
| C6 UWG-konforme Begriffe | ✓ | – |
| C7 Ausgewogene Risikodarstellung | ✓ | – |
| C8 Regulatorische Bezüge belegt | ◐ | § 80 WpHG über Suchtreffer auf den Gesetzestext belegt; PRIIPs/UWG und § 63 Abs. 10 WpHG UNVERIFIED |
| C9 Datenschutz | ◐ | Modul: 0 Drittanbieter-Abrufe, kein Speicher (L20); verlinkte Datenschutzerklärung offen (L38) |
| Q1 Faktencheck K1–K12 vollständig | ✓ | – |
| Q2 Aktualität / a. F. markiert | ◐ | BVerfG-Stand, ATAS-Start, Preise und Eurex-Daten offen (L10b) |
| Q3 Mathematische Konsistenz | ✓ | – |
| Q4 Provenienz je Fakt | ◐ | v1.7.0: Analyse faktgebunden, Kennzeichnung je Fakt-ID (L51, L53); ✓ erst nach Zweitprüfung (L10) |
| Q5 Quellenqualität | ◐ | Primärquellen identifiziert, nicht im Volltext gelesen |
| Q6 Vollständigkeit | ✓ | – |
| Q7 Widerspruchsfreiheit | ◐ | v1.7.0: Analyse ohne Hand-Konfidenzen, Labels = DBOM (L48b, L05d); ✓ erst nach Zweitprüfung (L10) |
| Q8 Glossar | ✓ | Pflichtbegriffe von der vierten Zweitprüfung bestätigt |
| Q9 Keine Überzeichnung / Halluzination | ◐ | v1.7.0: Analyse auf DBOM-Fakten gestrafft (L43, L53); ✓ erst nach Zweitprüfung (L10) |
| Q10 Formatvorgaben | ✓ | Sechste Zweitprüfung: Erklärungen sachlich korrekt, Version einheitlich; L41/L41b/L44-Tests |

**Gesamtscore:** 10 × ✓ + 9 × ◐ = 14,5 von 19 Punkten = **76,3 %**.
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
Interactive Brokers, TWS, Rithmic, CQG, Eurex, Cboe, OPRA, DAX, EURO STOXX 50, S&P 500, Nasdaq-100 und
Gamma Cockpit sind Marken oder Produktbezeichnungen ihrer jeweiligen Inhaber. Sie werden hier rein
beschreibend genannt. Es besteht keine Verbindung zu den Inhabern und keine Billigung durch sie.

**Interessenkonflikte.** Dem Verfasser sind keine Interessenkonflikte bekannt, insbesondere keine Affiliate-,
Partner- oder Vergütungsbeziehungen zu den genannten Anbietern. Der Herausgeber hat dies vor der
Veröffentlichung zu bestätigen.
