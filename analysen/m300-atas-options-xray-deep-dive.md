# FinCoach AI · Deep-Dive-Prime-Analyse · Modul M300

**ATAS Options X-Ray · Dealer-Greeks · Eurex-Börsenoptionen vs. verbriefte Derivate · Termingeschäfte im Steuerrecht**

| Feld | Wert |
|---|---|
| Modul | M300 (Platzhalter-ID) |
| Version | 1.0.0 (Entwurf) |
| Stichtag | 2026-10-05 |
| Zielstufe (CAT-Level) | Experte |
| Grundlage | Prompt `prompts/m300-atas-options-xray-deep-dive-prompt.md` v1.0.0; Quelltext vom 2026-10-05 (USER_PROVIDED) |
| Freigabeempfehlung | **ÜBERARBEITUNG** (siehe QA-Scorecard, Abschnitt 8) |

> **Disclaimer (Kurzfassung):** Diese Analyse ist eine allgemeine Information zu Bildungszwecken. Sie ist
> keine Anlageberatung oder Anlagevermittlung im Sinne von WpIG/KWG, keine Rechtsberatung im Sinne des RDG
> und keine Steuerberatung im Sinne des StBerG. Sie enthält keine Anlageempfehlung im Sinne von Art. 3 Abs. 1
> Nr. 35 MAR. Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind Hebelprodukte mit dem
> Risiko des Totalverlusts. Bei Futures und Stillhaltergeschäften können die Verluste den Kapitaleinsatz
> übersteigen. Steuerliche Aussagen geben den recherchierten Rechtsstand zum Stichtag wieder und ersetzen
> keine individuelle Prüfung durch Steuerberater oder Rechtsanwalt.

> **Methodischer Vorbehalt:** Die Recherche lief über eine Netzwerkumgebung, die den direkten Abruf der
> meisten Primärquellen gesperrt hat, darunter gesetze-im-internet.de, recht.bund.de, bundesfinanzministerium.de,
> bundesfinanzhof.de, eurex.com, atas.net und die Anbieterseiten. Die Befunde beruhen auf Suchtreffern, die
> auf diese Primärquellen verweisen. Die URLs sind im Quellenverzeichnis aufgeführt. Fundstellen, deren
> Wortlaut nicht vollständig einsehbar war, sind mit Konfidenz < 0,9 oder **[N. V.]** markiert.
> Vor einer Veröffentlichung sind sie am Original zu prüfen.

---

## 1 · Executive Summary

Der Quelltext beschreibt einen steuerlichen Rahmen, der so nicht mehr gilt. Die Verlustverrechnungsgrenze
von 20.000 € für Termingeschäfte (§ 20 Abs. 6 Satz 5 EStG a. F.) und die parallele Grenze für
Forderungsausfälle (Satz 6 a. F.) hat das **Jahressteuergesetz 2024** (BGBl. 2024 I Nr. 387) aufgehoben.
Nach § 52 Abs. 28 EStG ist das in allen offenen Fällen anzuwenden. Die Finanzverwaltung hat das im
BMF-Schreiben vom 14.05.2025 umgesetzt. Damit entfallen auch die These, Privatanleger würden aus
steuerlichen Gründen in Optionsscheine gedrängt, und die angebliche Rechtsunsicherheit „bis zu einer
Entscheidung des BVerfG“. Weiter gilt nur die Beschränkung für Aktienverluste nach § 20 Abs. 6 Satz 4 EStG.
Sie liegt beim BVerfG unter 2 BvL 3/21. Zweitens trifft die Aussage nicht zu, für eine vermögensverwaltende
Kapitalgesellschaft gebe es keine Verlustbeschränkung bei Termingeschäften. § 15 Abs. 4 Satz 3 EStG gilt
über § 8 Abs. 1 KStG und bildet einen gesonderten Verlustkreis. Drittens sind Market Maker nicht gesetzlich
verpflichtet, über das zentrale Orderbuch zu hedgen. Das Delta-Hedging folgt aus dem Risikomanagement.

Die Produktaussagen zu ATAS halten der Prüfung weitgehend stand. Die Options X-Ray Suite hat zehn
Indikatoren, rechnet auf einem 1-Minuten-Feed der CBOE mit Analytik von OptionsDepth und deckt nur
SPX-Optionen ab, angezeigt auf ES-, MES- und SPY-Charts. Optionen sind in ATAS derzeit nicht handelbar.
Die tragfähige strategische Kernthese lautet daher anders als im Quelltext: Wertvoll ist die Verbindung
von Dealer-Positionierung und Orderflow-Mikrostruktur in einem Arbeitsbereich. Für Europa entsteht der
Bedarf durch die fehlende intraday-fähige Eurex-GEX-Analytik, nicht durch das Steuerrecht.

---

## 2 · Phase A: Fakten- und Rechtsstandsprüfung

### 2.1 Claim-Tabelle

Legende Prüfergebnis: ✓ bestätigt · ◐ teilweise/präzisiert · ✗ falsch/überholt · ? nicht verifizierbar.

| ID | Claim (Kurzform) | Kategorie | Provenienz | Ergebnis | Korrektur / Präzisierung | Quelle | Konf. |
|---|---|---|---|---|---|---|---|
| A01 | Verluste aus Termingeschäften seit 2021 nur bis 20.000 €/Jahr verrechenbar (§ 20 Abs. 6 S. 6 EStG) | Steuer/Recht | CONFIRMED | ✗ | Norm war **Satz 5** (Satz 6 betraf Forderungsausfall). Eingeführt 2019 mit 10.000 €, durch JStG 2020 auf 20.000 € erhöht, durch JStG 2024 aufgehoben (alle offenen Fälle) | S1–S4 | 0,90 |
| A02 | Besteuerung „fiktiver Gewinne“ bei Spreads trotz Nettoverlust | Steuer/Recht | CONFIRMED | ◐ | Für 2021–2024 zutreffend beschrieben (asymmetrische Besteuerung, so auch BFH). Heute in offenen Fällen behoben | S5 | 0,85 |
| A03 | BFH äußerte in „mehreren Beschlüssen“ Zweifel (VIII B 113/23) | Steuer/Recht | CONFIRMED | ◐ | Belegt ist **ein** BFH-Beschluss vom 07.06.2024 im AdV-Verfahren (summarische Prüfung, Streitjahr 2021); Vorinstanz FG Rheinland-Pfalz 1 V 1674/23. Weitere BFH-Beschlüsse nicht gefunden | S5, S6 | 0,85 |
| A04 | Rechtsunsicherheit bleibt bis zur BVerfG-Entscheidung | Steuer/Recht | MEDIA_REPORT | ✗ | Durch die Aufhebung überholt; kein BVerfG-Verfahren speziell zu Termingeschäften gefunden | S1, S4 | 0,80 |
| A05 | Optionsscheine/Knock-outs sind laut Finanzverwaltung keine Termingeschäfte | Steuer/Recht | CONFIRMED | ✓ | Seit BMF 03.06.2021, fortgeführt 19.05.2022 und 14.05.2025. Randziffern [N. V.] | S4, S7 | 0,85 |
| A06 | Optionsschein-Verluste uneingeschränkt mit Aktien-/Zinsgewinnen verrechenbar | Steuer/Recht | CONFIRMED | ◐ | Richtung zutreffend; Aktien*verluste* bleiben nach § 20 Abs. 6 S. 4 auf Aktiengewinne beschränkt. Knock-out-Totalverlust unterlag früher Satz 6 a. F. | S4, S8 | 0,85 |
| A07 | Privatanleger werden in bankemittierte Produkte gedrängt | Markt | USER_PROVIDED | ✗ (heute) | Steuerlich nur 2021–2024 plausibel. Aktuell spricht eher die BaFin-Allgemeinverfügung zu Turbo-Zertifikaten (seit 16.06.2026) für zusätzliche Hürden bei Knock-outs | S9 | 0,75 |
| A08 | Market Maker sind gesetzlich gezwungen, über das zentrale Orderbuch zu hedgen | Mikrostruktur | USER_PROVIDED | ✗ | Keine Rechtspflicht. MiFID II Art. 17 Abs. 3 / § 80 Abs. 4 WpHG regeln Quotierungs-, keine Hedgingpflichten | S10, S11 | 0,85 |
| A09 | Emittenten netten intern, hedgen über OTC-Swaps; keine Orderbuchspuren im FDAX | Mikrostruktur | USER_PROVIDED | ◐ | Netting ist plausibel; Hedging erfolgt aber auch über Basiswert und „passende Gegengeschäfte“. Wirkung im FDAX nicht null, aber nicht zurechenbar | S12 | 0,60 |
| A10 | Für vermögensverwaltende Kapitalgesellschaften gilt keine Verlustverrechnungsbeschränkung | Steuer/Recht | USER_PROVIDED | ✗ | § 15 Abs. 4 S. 3 EStG i. V. m. § 8 Abs. 1 KStG: gesonderter Verlustkreis für Termingeschäfte; Ausnahme nur für Institute/Absicherung (S. 4), Rückausnahme für Aktien-Hedges (S. 5) | S13, S14 | 0,85 |
| A11 | Options X-Ray besteht aus zehn Indikatoren (Market State … Surface Profile) | Produkt | VENDOR_CLAIM | ✓ | Liste stimmt mit Hersteller-Hilfeseiten überein. Start laut Changelog 04.09.2026 (Konf. 0,6) | S15, S16 | 0,85 |
| A12 | Datenbasis CBOE/OptionsDepth, 60-Sekunden-Snapshots | Produkt | VENDOR_CLAIM | ✓ | „1-minute CBOE feed … data and analytics by OptionsDepth“; Neuberechnung jede Minute | S16, S17 | 0,85 |
| A13 | Beschränkung auf den SPX-Komplex | Produkt | VENDOR_CLAIM | ✓ | Nur SPX-Optionen; Anzeige nur auf ES, MES, SPY, US 500. Die separate Options Chain Suite (EOD) deckt ES, NQ, CL, GC ab | S15, S18 | 0,85 |
| A14 | Broker-Konnektivität Rithmic, IB, CQG | Produkt | VENDOR_CLAIM | ◐ | Für ATAS allgemein ✓. Options X-Ray benötigt laut Changelog Rithmic oder IB; CQG „in Entwicklung“ | S19, S17 | 0,70 |
| A15 | ES/MES-Cross-Trading vorhanden | Produkt | VENDOR_CLAIM | ✓ | Seit Version 8.0.12 (17.02.2026), auch NQ/MNQ, YM/MYM, RTY/M2K | S20 | 0,85 |
| A16 | Options Board und Strategy Analyzer in Entwicklung | Produkt | VENDOR_CLAIM | ◐ | Beide als **Beta** verfügbar (ab 8.0.14, Ultra-Plan); Optionshandel in ATAS derzeit nicht möglich | S21, S16 | 0,80 |
| A17 | Fehlende native Multi-Leg-Spread-Routing-Engine | Produkt | VENDOR_CLAIM | ✓ | Zutreffend. Die IB-API unterstützt Combo-Orders (BAG, bis 6 Legs) bereits nativ | S22 | 0,85 |
| A18 | NDX/NQ zeigt überproportionale 0DTE-Dynamik | Markt | USER_PROVIDED | ? | Keine belastbare Quantifizierung gefunden | – | 0,30 |
| A19 | Wettbewerbsfelder (SpotGamma, MenthorQ, Volland, Bookmap, TWS) | Wettbewerb | MEDIA_REPORT | ◐ | Siehe Modul 5; mehrere Felder [N. V.] | S23–S28 | 0,65 |
| A20 | Vier Roadmap-Erweiterungen | Vorschlag | SCENARIO_PROJECTION | – | Bewertung in Modul 7 | – | – |
| A21 | Warrant-Fair-Value-Tool zeigt „verdeckte Marge“ | Vorschlag | SCENARIO_PROJECTION | ◐ | Begriff wertend; neutral: Fair-Value-Differenz/Emittentenaufschlag (K12) | – | – |

### 2.2 Prüfprotokoll K1–K12

**K1 · Rechtsstand § 20 Abs. 6 Satz 5/6 EStG.** Die Verlustverrechnungsbeschränkung für Termingeschäfte geht
auf das Gesetz zur Einführung einer Pflicht zur Mitteilung grenzüberschreitender Steuergestaltungen vom
21.12.2019 zurück (BGBl. I S. 2875). Sie galt für Termingeschäfte ab dem 01.01.2021 und war zunächst auf
10.000 € begrenzt. Das Jahressteuergesetz 2020 vom 21.12.2020 (BGBl. I S. 3096) hob die Grenze auf 20.000 €
an. Das Jahressteuergesetz 2024 vom 02.12.2024 (BGBl. 2024 I Nr. 387, Bundestag 18.10.2024, Bundesrat
22.11.2024) hob die Sätze 5 und 6 in Artikel 3 auf. Nach der Anwendungsregel in § 52 Abs. 28 EStG sind sie
„in allen offenen Fällen nicht mehr anzuwenden“. Die Satznummern 25/26 sind nur per Snippet belegt
(Konfidenz 0,7). Das BMF-Schreiben „Einzelfragen zur Abgeltungsteuer“ vom 14.05.2025
(IV C 1 – S 2252/00075/016/070) setzt das um. Bestehende Verlustvorträge aus Termingeschäften sind
danach in offenen Fällen unbeschränkt verrechenbar. Im Steuerabzugsverfahren der Banken wirkte die
Beschränkung nie unmittelbar. Termingeschäftsverluste wurden bescheinigt und erst in der Veranlagung
berücksichtigt. Nach Kundeninformationen von Instituten gilt im Abzugsverfahren seit 01.01.2025 die volle
Verrechnung (Konfidenz 0,6). **Ergebnis: ✗ im Quelltext; die Regelung ist kein geltendes Recht mehr.**

**K2 · BFH VIII B 113/23.** Es handelt sich um einen Beschluss vom 07.06.2024 im Verfahren über die Aussetzung
der Vollziehung (§ 69 Abs. 3 FGO). Der Senat prüfte nur summarisch und kam zu dem Ergebnis, die Regelung sei
mit Art. 3 Abs. 1 GG voraussichtlich nicht vereinbar. Begründet wurde das mit dem objektiven Nettoprinzip
und der asymmetrischen Besteuerung. Ein Hauptsacheurteil oder eine Vorlage an das BVerfG wurde nicht gefunden.
Die Bezeichnung „mehrere Beschlüsse“ ist nicht belegt, und die Aussage „Rechtsunsicherheit bis zur BVerfG-Entscheidung“ ist durch die Aufhebung überholt. **Ergebnis: ✗** (Beschluss selbst korrekt zitiert).

**K3 · Abgrenzung Termingeschäft.** Die Finanzverwaltung ordnet Optionsscheine (Kapitalforderungen) und
Zertifikate einschließlich Knock-out-Produkten nicht als Termingeschäfte im Sinne von § 20 Abs. 6 Satz 5
a. F. ein. Das gilt seit dem BMF-Schreiben vom 03.06.2021 und ist in den Fassungen von 2022 und 2025
fortgeführt. Beim Knock-out-Ereignis griff bis zur Aufhebung allerdings Satz 6 a. F. (Ausfall oder
Wertloswerden), ebenfalls mit einer Grenze von 20.000 €. Der vom Quelltext behauptete einseitige
Steuervorteil verbriefter Produkte war daher schon unter altem Recht kleiner als dargestellt. Nach der
Aufhebung besteht er nicht mehr. Unverändert gilt nur § 20 Abs. 6 Satz 4 (Aktienverluste). Dazu ist beim
BVerfG die Vorlage 2 BvL 3/21 anhängig. Bescheide ergehen insoweit vorläufig. Eine Entscheidung wurde bis
zum Stichtag nicht gefunden (Konfidenz 0,6). **Ergebnis: ◐** (Einordnung ✓, Verdrängungsthese ✗).

**K4 · Kapitalgesellschaft.** § 15 Abs. 4 Satz 3 EStG schließt aus, dass Verluste aus Termingeschäften mit
anderen Einkünften ausgeglichen werden. Sie sind nur mit Gewinnen aus Termingeschäften verrechenbar
(gesonderter Verlustkreis, ohne betragsmäßige Obergrenze). Über § 8 Abs. 1 KStG gilt das auch für
Kapitalgesellschaften (z. B. BFH I R 25/14 vom 06.07.2016). Satz 4 nimmt Geschäfte von Kredit- und
Finanzdienstleistungsinstituten sowie Absicherungsgeschäfte aus. Satz 5 enthält eine Rückausnahme für die
Absicherung von Aktiengeschäften, deren Gewinne nach § 3 Nr. 40 EStG bzw. § 8b Abs. 2 KStG ganz oder
teilweise steuerfrei sind. Das JStG 2024 hat § 15 Abs. 4 nach den Rechercheergebnissen nicht geändert.
Eine Empfehlung zur Rechtsformwahl lässt sich daraus nicht ableiten und wird hier nicht ausgesprochen.
**Ergebnis: ✗ im Quelltext.**

**K5 · Hedging-Pflicht der Market Maker.** Art. 17 Abs. 3 MiFID II und § 80 Abs. 4 WpHG (Definition der
Market-Making-Strategie in Abs. 5) verpflichten Wertpapierfirmen mit algorithmischer Market-Making-Strategie, kontinuierlich zu quotieren und eine
Vereinbarung mit dem Handelsplatz zu schließen. Eine Pflicht, das resultierende Delta über das
Orderbuch des Basiswerts zu neutralisieren, enthalten diese Normen nicht. Delta-Hedging ist ökonomisch
naheliegend und durch Eigenkapital- und Risikolimits motiviert. Es kann aber über Futures, ETFs,
Kassamarkt, OTC-Derivate oder internes Netting gegenläufiger Bestände erfolgen. **Ergebnis: ✗.** Die
GEX-Logik bleibt als Verhaltensmodell brauchbar. Sie darf aber nicht als rechtlicher Automatismus
dargestellt werden.

**K6 · GEX-Prämisse.** Jede GEX-Berechnung braucht eine Annahme über die Gegenpartei. Die klassische
Konvention lautet „Kunden kaufen Puts und verkaufen Calls, Dealer halten die Gegenposition“. Sie ist eine
**MODEL_ASSUMPTION**. OptionsDepth stützt sich nach eigener Darstellung auf nach Teilnehmertyp markierte
CBOE-Daten (Open-Close-Daten). Das ist für SPX-Optionen, die nur an der Cboe gehandelt werden, eine
deutlich bessere Grundlage als eine reine Tape-Klassifikation (Konfidenz 0,7). Restfehler bleiben trotzdem:
Ein Market Maker im Sinne der Datenmarkierung ist nicht zwingend der Risikoträger mit Hedgebedarf. Kombi-
und Spread-Trades verzerren die Strike-Zuordnung. Overwriting- und Dispersionsprogramme sowie Volumen,
das intraday eröffnet und geschlossen wird, hinterlassen keine Spur im Open Interest. **Ergebnis: ◐.**

**K7 · Emittenten-Hedging bei Optionsscheinen.** Emittenten sichern das Nettorisiko ihrer Bücher laufend
dynamisch ab, über den Basiswert oder über „passende Gegengeschäfte“ (Konfidenz 0,6). Eine Primärquelle,
die das Hedging des Nettodeltas speziell über FDAX oder ODAX belegt, wurde nicht gefunden. Die Aussage
„keine Hedging-Kaskaden im FDAX“ ist daher zu stark. Zutreffend ist: Die Spur ist nach dem Netting klein,
zeitlich verteilt, nicht öffentlich zurechenbar und lässt sich nicht aus Börsendaten rekonstruieren.
**Ergebnis: ◐.**

**K8 · ATAS-Produktangaben.** Die Indikatorliste, die Datenquelle (1-Minuten-CBOE-Feed, Analytik
OptionsDepth), die SPX-Beschränkung und das ES/MES-Cross-Trading sind über Hilfe- und Lernseiten des
Herstellers belegt. Options Board und Strategy Analyzer existieren als Beta. Optionen sind in ATAS nach
Herstellerangabe derzeit nicht handelbar. Der Start der Suite am 04.09.2026 ist nur über einen Snippet
belegt (Konfidenz 0,6). **Ergebnis: ✓ mit Präzisierungen.**

**K9 · Wettbewerber.** Siehe Modul 5. Preise und Frequenzen stammen aus Snippets von Anbieter- und
Drittseiten; mehrere Felder sind [N. V.]. **Ergebnis: ◐.**

**K10 · Eurex-Spezifikationen.** Die Kontraktgrößen sind:

- FDXM 5 €/Pkt. und FDXS 1 €/Pkt. (belegt)
- ODAX 5 €/Pkt., europäisch, Barausgleich, Basiswert DAX-Index (belegt)
- FDAX 25 €/Pkt. sowie FESX und OESX je 10 €/Pkt. (Standardangaben, Konfidenz 0,8)

Optionen auf DAX- oder Euro-Stoxx-50-Futures wurden nicht gefunden. Gelistet sind Indexoptionen
einschließlich Micro-DAX-Optionen (ODXS). Für den kurzfristigen Bereich gibt es zwei Produkte. OEXP
(EURO STOXX 50 End-of-Day Options) startete am 28.08.2023. Seit 05.01.2026 hat OEXP Verfälle an zehn
Handelstagen, seit 06.07.2026 zusätzlich Monatsend-Verfälle. ODAP (DAX End-of-Day Options) startete am
13.11.2023. Der Fachbegriff für den „Hexensabbat“ ist Quartalsverfall: dritter Freitag in März, Juni,
September und Dezember. ODAX und OESX haben zusätzlich Monatsverfälle. Open Interest veröffentlicht
Eurex täglich über die Statistiken und den Extended Market Data Service, nicht über EOBI. **Ergebnis: ◐** (präzisiert: Indexoptionen statt Optionen auf Futures, Quartalsverfall statt „Hexensabbat“).

**K11 · IBKR-Combo-Orders.** Die TWS-API unterstützt Spreads als Kontrakt mit `secType = "BAG"` und bis
zu sechs `ComboLeg`-Elementen. Möglich sind ein Netto-Limitpreis und optional Preise je Leg. Vertical,
Calendar, Diagonal, Straddle und Iron Condor sind damit abbildbar. Die eigentliche Lücke bei ATAS liegt
also nicht im Routing, sondern in der Plattform darüber: Strategie-UI, Pre-Trade-Risikoprüfung,
Preisfindung für das Paket, Schutz vor Legging-Risiko und Positionsführung. **Ergebnis: ◐** (Befund zutreffend, Ursache präzisiert).

**K12 · Warrant-Fair-Value-Tool.** „Verdeckte Marge“ und „künstliche Spread-Ausweitung“ sind wertende,
im Sinne von §§ 4, 6 UWG riskante Begriffe. Neutral sind „Fair-Value-Differenz“, „Emittentenaufschlag“
und „Geld-Brief-Spanne“. Die Kosten des Emittenten sind über das PRIIPs-Basisinformationsblatt und die
Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen. Ein Tool sollte gegen diese
Angaben abgleichen statt gegen eine eigene „Marge“. **Ergebnis: ◐.**

### 2.3 Korrekturliste zum Quelltext

| # | Schweregrad | Korrektur |
|---|---|---|
| 1 | KRITISCH | Die 20.000-€-Grenze ist durch das JStG 2024 aufgehoben (alle offenen Fälle). Normzitat im Quelltext ist zudem falsch (Satz 5, nicht Satz 6). |
| 2 | KRITISCH | Die „Rechtsunsicherheit bis zur BVerfG-Entscheidung“ besteht für Termingeschäfte nicht mehr. Anhängig ist 2 BvL 3/21 zu Aktienverlusten (Satz 4), also ein anderer Sachverhalt. |
| 3 | KRITISCH | Für vermögensverwaltende Kapitalgesellschaften gilt § 15 Abs. 4 Satz 3 EStG (gesonderter Verlustkreis). „Keine Beschränkung“ ist falsch. |
| 4 | WESENTLICH | Es gibt keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging. |
| 5 | WESENTLICH | Die steuerliche Verdrängung in verbriefte Produkte ist heute keine tragfähige Kausalität. Als regulatorischer Faktor ist die BaFin-Allgemeinverfügung zu Turbo-Zertifikaten (in Kraft seit 16.06.2026) zu ergänzen. |
| 6 | WESENTLICH | Wertende Begriffe beim Warrant-Tool sind neutral zu ersetzen (UWG). |
| 7 | WESENTLICH | ATAS ermöglicht derzeit keinen Optionshandel. Options Board und Strategy Analyzer sind Beta. Die IB-API unterstützt Combo-Orders bereits. |
| 8 | HINWEIS | Nur ein BFH-Beschluss ist belegt (AdV, summarisch). |
| 9 | HINWEIS | Emittenten-Hedging hinterlässt eine schwache, nicht zurechenbare Börsenspur, keine „Nullspur“. |
| 10 | HINWEIS | „Hexensabbat“ heißt fachlich Quartalsverfall. Eurex hat mit OEXP und ODAP bereits Optionen mit Tagesverfall. |
| 11 | HINWEIS | Die Options Chain Suite (EOD) deckt bereits ES, NQ, CL und GC ab. Die Multi-Asset-Forderung betrifft nur die Intraday-Analytik von X-Ray. |

---

## 3 · Phase B: Deep-Dive-Analyse

### Modul 1 · Technologische Dekonstruktion der Options X-Ray Suite

Die Suite wandelt die Positionierung im SPX-Optionsmarkt in Informationen um, die auf einem Futures-Chart
verwertbar sind. Die zehn Indikatoren erfüllen dabei drei Funktionen. **Market State**, **Expected Move**
und das **Surface Profile** beschreiben das Regime: Sie sagen, ob der Markt in einem dämpfenden oder
beschleunigenden Gamma-Umfeld liegt und welche Bandbreite die implizite Volatilität einpreist. Market State
trennt nach Herstellerangabe beobachtete Daten sichtbar von Modellausgaben. Diese Unterscheidung ist auch
aus Compliance-Sicht wertvoll. **GEX Heatmap**, **Charm Heatmap**, **Strike Heatmap** und **Strike Profile**
übersetzen die Exponierung je Strike und Verfall in Preiszonen auf der Chartachse. **Big Trades**, **Flow**
und **Flow Delta** schließlich bilden den Strom neuer Abschlüsse ab und sollen zeigen, wie sich die
Positionierung innerhalb des Tages verschiebt. Die genaue Berechnungslogik der Indikatoren ist nicht
öffentlich dokumentiert. Die folgenden Formeln sind deshalb die fachübliche Referenzmodellierung **[MODELL]**
und nicht die belegte Implementierung des Herstellers.

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
hinterherkaufen und fallenden hinterherverkaufen. Sein Hedging verstärkt die Bewegung. Daraus folgt der
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

**Zahlenbeispiel [SZENARIO, hypothetische Werte]:** Angenommen sind ein SPX-Stand $S = 6.500$, ein Strike mit
$OI = 10.000$ Calls, $\Gamma = 0{,}0020$ je Punkt und Dealer long ($s = +1$). Dann gilt
$\Gamma\cdot OI\cdot M = 0{,}002 \cdot 10.000 \cdot 100 = 2.000$ Indexeinheiten Delta je Punkt. Eine
Bewegung von 1 % entspricht $65$ Punkten. Daraus ergibt sich eine Delta-Änderung von $2.000 \cdot 65 =
130.000$ Indexeinheiten, in Dollar $GEX = 2.000 \cdot 6.500^2 \cdot 0{,}01 = 845$ Mio. USD. In
ES-Äquivalenten sind das $130.000 / 50 = 2.600$ ES-Kontrakte oder $26.000$ MES. Probe:
$2.600 \cdot 50 \cdot 6.500 = 845$ Mio. USD. Im Long-Gamma-Fall würden Dealer bei einem Anstieg um 1 %
modellgemäß rund 2.600 ES verkaufen. Ob diese Menge das Orderbuch spürbar bewegt, hängt von der
Markttiefe in diesem Moment ab. Dieses Bindeglied liefert erst die Kombination mit MBO- und
Footprint-Daten (Modul 4).

### Modul 2 · Datenfeed-Architektur, Latenzprofil und Validierung

Mit der Entscheidung für serverseitig berechnete Minuten-Snapshots verlagert ATAS das Rechenproblem vom
Client auf den Datenpartner. Der Vergleich zeigt die Größenordnung: Das gesamte US-Optionstape (OPRA) ist
für Spitzenlasten von mehr als 30 Gbps je Stream ausgelegt. Die Kapazitätsprojektion der OPRA nennt
37,3 Gbps im 1-ms-Fenster. Sekundärquellen berichten 2025 von Bursts mit über 180 Mio. Nachrichten pro
Sekunde. Ein Desktop-Client kann das weder empfangen noch bewerten. Für die Suite genügt zwar die
SPX-Kette, weil SPX-Optionen nur an der Cboe gehandelt werden. Aber auch deren laufende
Greek-Neuberechnung über Tausende Serien, einschließlich IV-Fit und Positionszuordnung, ist serverseitig
besser aufgehoben. Der Minutentakt reduziert die Last auf dem Client auf wenige Kilobyte je Update
**[EST]**.

Der Preis dafür ist Analyse-Latenz. Sie ist sauber von Ausführungs-Slippage zu trennen. Die Ausführung des
Futures erfolgt unabhängig vom Snapshot in Echtzeit über Rithmic oder IB. Der Snapshot bestimmt nur, wie
aktuell die Landkarte ist, auf der die Entscheidung getroffen wird. Bei Makroereignissen (CPI, FOMC, NFP)
bewegt sich der ES innerhalb von Sekunden über mehrere Gamma-Zonen. Das Profil auf dem Chart zeigt dann
bis zu 60 Sekunden lang einen Zustand vor dem Ereignis. In diesem Fenster entstehen drei Fehlerarten. Erstens
verschieben sich Gamma-Walls, weil sich die IV-Fläche ändert (Vanna), obwohl sich das Open Interest nicht
geändert hat. Zweitens löst Volumen, das neue Positionen eröffnet, Hedges aus, die im letzten Snapshot noch
fehlen. Drittens verdeckt die zeitliche Unterabtastung eine kurze Bewegung durch einen Level und zurück
(Aliasing). Praktisch heißt das: In den ersten ein bis zwei Minuten nach einer Veröffentlichung trägt das
Optionsprofil kaum Information. Der Orderflow im Future ist dann führend.

Die **Options Chain Suite** ist dazu das clientseitige Gegenstück auf Tagesbasis. Sie arbeitet mit dem
täglichen Open-Interest-Snapshot und vier Indikatoren (OI Profile, Key Levels einschließlich Max Pain,
Expected Move, GEX Profile) für ES, NQ, CL und GC. Sie ist breiter in der Abdeckung, aber strukturell
blind für 0DTE-Positionen, die innerhalb des Tages eröffnet und geschlossen werden. Diese machten 2025 rund
59 % des SPX-Volumens aus (Cboe).

Zur **Validierung** sind vier Verfahren geeignet. Die Summen je Strike werden mit dem veröffentlichten
Cboe-Open-Interest des Folgetags abgeglichen. Die Stabilität der Walls zwischen aufeinanderfolgenden
Snapshots wird gemessen. Ereignisstudien prüfen, ob sich die realisierte Volatilität im Long- und im
Short-Gamma-Regime unterscheidet. Backtests müssen frei von Look-ahead-Bias sein: Die Daten dürfen erst ab
ihrer tatsächlichen Verfügbarkeit verwendet werden, beim Open Interest also T+1. Ohne veröffentlichte
Validierungsstatistik des Herstellers bleibt die Prognosegüte der Suite **[N. V.]**.

### Modul 3 · Handels- und Ausführungsmöglichkeiten

ATAS bindet als Handelsverbindungen Rithmic, CQG und Interactive Brokers (über eine laufende TWS) an, als
reine Datenfeeds dxFeed und IQFeed. Options X-Ray setzt nach Herstellerangabe eine Verbindung über Rithmic
oder IB voraus. CQG ist dort in Entwicklung. Seit Version 8.0.12 vom 17.02.2026 gibt es **Cross-Trading**:
Analyse und Order-Eingabe finden auf dem ES-Chart statt, die Ausführung erfolgt im MES. Diese Trennung ist
für kleinere Konten nützlich, weil die Liquiditätsinformation des ES mit der Positionsgröße des Micro-Kontrakts
kombiniert wird.

Die Optionsseite ist dagegen bisher reine Analyse. **Options Board** (Strike-Verfall-Matrix mit Kursen,
Greeks und IV-Skew) und **Options Strategy Analyzer** (P&L-, Volatilitäts-, Zeit- und Delta-Hedge-Szenarien)
sind als Beta im Ultra-Plan verfügbar. Optionen selbst lassen sich in ATAS laut Herstellerseite derzeit
nicht handeln. Ein Optionshändler arbeitet also mit zwei Plattformen: Die Struktur wird in ATAS analysiert,
die Ausführung erfolgt in der TWS oder bei einem anderen Broker. Damit entstehen Medienbrüche,
Übertragungsfehler und Zeitverlust. Weil die IB-API Combo-Orders (BAG) mit Netto-Limit bereits nativ
unterstützt (K11), ist der Weg zu einem integrierten Ticket technisch kürzer, als der Quelltext suggeriert.
Der eigentliche Aufwand liegt in Risikoprüfung, Preisfindung und Positionsführung (Modul 7).

### Modul 4 · Mikro-Makro-Synergien im praktischen Trading

> **Compliance-Hinweis:** Die folgenden Konstellationen sind generische, lehrhafte Beschreibungen von
> Marktmechanik. Sie enthalten keine Kursziele, Einstiegsmarken oder Richtungsaussagen zu einem bestimmten
> Instrument und sind keine Handelsempfehlung. Gamma-Levels sind Wahrscheinlichkeitszonen und keine
> Preisgarantien.

Optionsdaten liefern die Landkarte: Wo sitzt Hedge-Bedarf und in welche Richtung wirkt er? Orderflow-Daten
zeigen, ob dieser Bedarf im Moment tatsächlich ausgeführt wird. Erst beides zusammen ergibt ein prüfbares
Bild. In einem **Long-Gamma-Regime** innerhalb des Expected-Move-Korridors legt das Modell nahe, dass
Bewegungen an einer Call- oder Put-Wall eher abgebremst werden. Ob das zutrifft, zeigt der Footprint
an dieser Stelle. **Absorption**, also hohes aggressives Volumen ohne Preisfortschritt, und im MBO-Bild
nachgefüllte Limitorders (Icebergs) bestätigen die These. Ein **Sweep**, der mehrere Preisstufen auf einmal
abräumt, ohne dass die Liquidität zurückkehrt, widerlegt sie. Das Setup ist erst nach dieser Bestätigung
gültig. Es ist ungültig, sobald der Preis die Wall mit anhaltender Delta-Dominanz und ohne Rückkehr der
Liquidität durchbricht.

Im **Short-Gamma-Regime** unterhalb des GEX-Flips kehrt sich die Logik um. Hier interessieren weniger
Umkehrzonen als Beschleunigungszonen. Eine **Delta-Divergenz** (neues Preistief bei schwächerem negativem
kumuliertem Delta) ist in diesem Regime ein schwächeres Signal als im Long-Gamma-Umfeld, weil prozyklisches
Hedging Trends verlängern kann. Ein **Gamma-Squeeze** entsteht, wenn der Preis in eine Zone mit dichtem
Short-Gamma läuft. Jeder Tick erhöht dann den Hedge-Bedarf in Bewegungsrichtung. Für eine Bewegung
$\Delta S$ ist das ungefähr $-\,\text{GEX}_{\text{netto}}\cdot \Delta S/(0{,}01\,S)$ in Dollar Delta. Geht
die Markttiefe gleichzeitig zurück, verstärken sich Bewegung und Hedge-Bedarf gegenseitig. Ein
**Charm-Squeeze** ist leiser: Am Nachmittag vor einem großen Verfall muss Delta zurückgekauft oder
verkauft werden, auch wenn sich der Preis kaum bewegt. Der Flow steigt typischerweise in der letzten
Handelsstunde. Im Footprint erscheint er als einseitiges, gleichmäßig verteiltes Volumen ohne große
Einzelorders **[MODELL]**.

Für alle Konstellationen gelten dieselben Grenzen. Das Profil ist bis zu 60 Sekunden alt (Modul 2). Die
Dealer-Annahme kann falsch sein (K6). Makroereignisse überlagern jede Mikrostruktur. Und das Risiko einer
einzelnen Position bestimmt sich nicht aus Gamma-Levels, sondern aus Positionsgröße und Stop-Disziplin.

### Modul 5 · Globaler Wettbewerbsvergleich

Die Matrix stützt sich auf Anbieterseiten und Drittquellen, die nur über Suchtreffer einsehbar waren (Stand
2026-10-05). Preise sind Richtwerte, vor Verwendung beim Anbieter zu prüfen. Provenienz: V = VENDOR_CLAIM,
M = MEDIA_REPORT. Die Reihenfolge ist keine Rangfolge.

| Merkmal | ATAS (Options X-Ray) | SpotGamma | MenthorQ | Volland | Bookmap | IBKR TWS |
|---|---|---|---|---|---|---|
| Kernfokus | Orderflow-Plattform + Dealer-Positionierung (V) | Dealer-Gamma-Levels, Research (V) | Gamma-Levels, Modelle, Ausbildung (V) | Notional-Greeks des Dealer-Buchs (V) | Orderbuch-Heatmap, Ausführung (V) | Broker-Plattform, Portfoliorisiko (V) |
| Datenfrequenz Optionen | 1 Min. (V) | HIRO/TRACE intraday real-time; Levels vor Eröffnung (V) | EOD + alle 5 Min. intraday (V) | EOD bis alle 5 Min. je Tarif (V) | keine nativen Optionsmetriken (V) | Echtzeit (Kursdaten-Abo) (V) |
| Datenquelle | CBOE via OptionsDepth (V) | [N. V.] | [N. V.] | Trade-Feed, Anbieter [N. V.] | Rithmic, dxFeed, CQG (Futures) (V) | Börsendaten je Abo (V) |
| GEX / Vanna / Charm | ✓ / [N. V.] / ✓ (V) | ✓ / Vanna-Modell / [N. V.] (V) | ✓ / [N. V.] / [N. V.] (V) | ✓ / ✓ / ✓ (V) | nur über Add-ons (V) | nein, nur eigene Positions-Greeks (V) |
| Abdeckung | SPX (intraday); ES, NQ, CL, GC (EOD) (V) | SPX, NDX, ETFs, >3.500 Aktien (V) | ~1.300–1.400 Werte inkl. Futures-Optionen ES, NQ, CL, GC u. a. (V) | Top-200 nach Options-Notional (V) | Futures, Aktien, Krypto (V) | global inkl. Eurex ODAX/OESX (V) |
| Eurex-GEX | nein | nein | [N. V.] | nein | nein | Rohdaten, keine GEX |
| Orderflow / MBO | Footprint, MBO-Bundle (Iceberg, Sweeps, Stop Runs) (V) | nein | nein | nein | Heatmap, MBO via Rithmic (V) | nein |
| Ausführung | Futures ja; Optionen nein (V) | nein | über Partnerplattformen (V) | [N. V.] | ja (V) | ja, vollständig (V) |
| Preis/Monat (Richtwert) | Ultra ca. 50–90 € (M) | ca. 67–224 $ (M) | 129 / 349 $ (M) | 150–1.000 $ (M) | 39–99 $ + Daten (M) | Plattform frei, Datenabos (V) |
| Zielgruppe | aktive Futures-Trader, Semi-Profis | Retail bis Profi | Retail, Ausbildung | fortgeschritten/Profi | Retail bis Profi | Retail bis institutionell |

Aus der Matrix lässt sich Folgendes ableiten. ATAS ist der einzige Anbieter im Vergleichsfeld, der native
Optionsdaten im Minutentakt mit einem nativen MBO- und Footprint-Werkzeugkasten in einer Oberfläche verbindet;
Bookmap hat MBO, aber keine nativen Optionsmetriken. Volland ist der einzige Anbieter mit belegter Abdeckung von
Gamma, Vanna und Charm. Intraday-Flow-Analytik bieten SpotGamma (HIRO/TRACE) und ATAS (Flow, Flow Delta).
MenthorQ deckt Futures-Optionen nativ ab und aktualisiert intraday alle fünf Minuten. Eigene Ausführung bieten
ATAS (nur Futures), Bookmap und die TWS; für Volland ist sie n. v. Die TWS rechnet keine marktweite
Dealer-Positionierung. **Für Eurex-Optionen bietet keiner der fünf bestimmbaren von sechs verglichenen Anbietern
eine intraday-fähige GEX-Analytik (MenthorQ: n. v.).** Als europäisches Angebot wurde nur Gamma Cockpit gefunden: DAX-GEX auf Basis von
ODAX-Daten, nur auf Tagesbasis, als kostenlose Beta (Stand 2026-10-05, [N. V.] zur Lizenzlage).

### Modul 6 · DACH-Marktspezifika: Börsenoptionen vs. verbriefte Derivate

Der deutschsprachige Markt hat eine besondere Struktur. Am Börsenumsatz verbriefter Derivate stellen
Hebelprodukte nach BSW-Statistik rund 84 % (Bezugszeitraum [N. V.]). Darunter entfallen etwa 59 % auf
Knock-outs und 19 % auf klassische Optionsscheine, jeweils bezogen auf den Gesamtumsatz. Gehandelt wird vor allem an der Euwax in
Stuttgart, an der Börse Frankfurt (Zertifikate) und auf gettex. An der Eurex dagegen konzentriert sich das
professionelle Geschäft in Indexoptionen. OESX kommt nach einem Eurex-Whitepaper auf ein ADV von rund
698.000 Kontrakten (Stand November 2025, Konfidenz 0,6). Die Optionen mit Tagesverfall sind noch klein:
OEXP hat seit Start ein ADV von rund 30.900 Kontrakten, ODAP von rund 2.300 (Stand der Quelle [N. V.]). Beide
sind End-of-Day-Optionen mit Verfällen über mehrere Handelstage, also kein reines 0DTE. Der Vergleich mit den
USA, wo 2025 rund 59 % des SPX-Optionsvolumens auf 0DTE entfielen, zeigt daher nur die Größenordnung.

Die beiden Produktwelten unterscheiden sich in den folgenden Merkmalen:

| Merkmal | Eurex-Börsenoptionen (ODAX/OESX) | Optionsscheine / Knock-outs |
|---|---|---|
| Rechtsnatur | standardisierter Terminkontrakt | Inhaberschuldverschreibung des Emittenten |
| Kontrahentenrisiko | zentrale Gegenpartei (Eurex Clearing) | Bonität des Emittenten (Totalausfall bei Insolvenz möglich) |
| Preisbildung | Orderbuch mit mehreren Market Makern | Quote-Making durch den Emittenten |
| Spreads | marktabhängig, in liquiden Serien eng [EST] | vom Emittenten gesetzt, bei Knock-outs oft eng, bei Optionsscheinen IV-abhängig [EST] |
| Volatilität im Preis | marktgebildete IV | Emittenten-IV, kann von der Börsen-IV abweichen |
| Kontraktgröße | ODAX 5 €/Pkt., ODXS kleiner | frei stückelbar über Bezugsverhältnis |
| Stillhalterposition | möglich (Margin) | nicht möglich |
| Zugang Privatanleger | Angemessenheitsprüfung (§ 63 Abs. 10 WpHG, nur über Praxisformulare belegt); Eurex-Zugang nicht bei allen Brokern | breit verfügbar; für Turbos seit 16.06.2026 Wissenstest und Risikohinweis (BaFin-Allgemeinverfügung) |
| Kostenausweis | Gebühren, Ex-ante-Kosten nach MiFID II | PRIIPs-KID mit Emittentenkosten + MiFID-II-Kosten |
| Steuer (Privatvermögen, offene Fälle) | Einkünfte aus Kapitalvermögen; keine Sonderbeschränkung mehr (JStG 2024) | Einkünfte aus Kapitalvermögen; keine Sonderbeschränkung |

Zur **steuerlichen Zeitachse:** Von 2021 bis 2024 benachteiligte § 20 Abs. 6 Satz 5 EStG a. F.
Privatanleger mit börsengehandelten Optionen und Futures tatsächlich. Verluste aus Glattstellungen und
verfallenen Long-Optionen ließen sich nur bis 20.000 € im Jahr verrechnen. Bei Spread-Strategien konnten
dadurch Steuern auf einen wirtschaftlich nicht vorhandenen Gewinn anfallen. Verbriefte Produkte waren von
Satz 5 nicht erfasst. Knock-out-Totalverluste fielen aber unter Satz 6 a. F. Das JStG 2024 hat beide Sätze
für alle offenen Fälle gestrichen. Ob ein Anleger Altjahre korrigieren kann, hängt davon ab, ob seine
Bescheide noch offen sind. Das ist eine Frage des Einzelfalls und vom Steuerberater zu prüfen. Für die
Gegenwart gilt: Die Steuer unterscheidet nicht mehr zwischen beiden Produktwelten. Bestehen bleibt nur die
Beschränkung für Aktienverluste nach Satz 4. Die vom Quelltext beschriebene steuerliche Verzerrung ist
damit Geschichte. Die Marktstruktur mit dominanten Hebelzertifikaten erklärt sich heute eher aus
Gewohnheit, Vertriebswegen, kleiner Stückelung und Brokerangeboten. Für Knock-outs kommen seit Juni 2026
neue Zugangshürden hinzu. Die zugrunde liegende BaFin-Studie ergab für den Untersuchungszeitraum 2019–2023,
dass rund 74,2 % der Kleinanleger mit Turbo-Zertifikaten Verluste erlitten (Studie nicht im Volltext geprüft).

Warum lassen sich die Hedging-Modelle von Options X-Ray nicht auf Optionsscheine übertragen? Der Grund ist
nicht ein „Versagen“, sondern die Beobachtbarkeit. Ein GEX-Modell braucht drei Dinge: offene Positionen je
Strike, eine Annahme über den Risikoträger und einen Markt, in dem dessen Hedge auftritt. Beim Optionsschein
ist die offene Position nur dem Emittenten bekannt. Ein öffentliches Open Interest je Basispreis wie bei
Eurex gibt es nicht. Der Risikoträger ist mit dem Emittenten bekannt, aber er nettet sein Buch, bevor er
hedgt. Gehedgt wird teils über Basiswert und Börsenderivate, teils außerbörslich. Eine Spur im FDAX gibt es
also durchaus (K7). Sie lässt sich aber weder einer Strike-Struktur zuordnen noch vorhersagen. Für
Eurex-Optionen sind alle drei Bedingungen grundsätzlich erfüllbar. Open Interest je Serie wird täglich
veröffentlicht. Nach Teilnehmertyp markierte Open-Close-Daten wie bei der Cboe sind für Eurex allerdings
nicht belegt **[N. V.]**. Die Positionsannahme ist deshalb dort schwächer fundiert als beim SPX.

### Modul 7 · Strategische Produkt-Roadmap [SZENARIO]

Alle vier Vorschläge sind Szenarien. Ihre Umsetzung, ihr Zeitplan und ihr Erfolg sind offen.

| Erweiterung | Nutzen | Datenverfügbarkeit / -kosten | Technische Komplexität | Regulatorische Implikationen | Hauptrisiko |
|---|---|---|---|---|---|
| Multi-Asset (NDX/NQ, CL, GC, Single Stocks) intraday | hoch | abhängig vom Datenpartner; OptionsDepth deckt nach Recherche nur SPX/VIX ab | mittel bis hoch | gering | Datenpartner-Abhängigkeit, schwächere Positionsdaten außerhalb der Cboe |
| Eurex-X-Ray (FDAX/FESX) | hoch (Alleinstellung) | Eurex-Daten lizenzpflichtig; OI täglich; Teilnehmermarkierung [N. V.] | hoch | gering (Datenlizenz) | geringe 0DTE-Liquidität; schwächere Positionsannahme |
| Multi-Leg-Ausführung + Auto-Delta-Hedging | sehr hoch für die Plattformbindung | IB-API vorhanden (BAG) | hoch | hoch bei automatischer Orderauslösung | Haftung, Fehlorders, Aufsichtsrecht |
| Warrant-Fair-Value-Tool (DACH) | mittel (Transparenz) | Emittentenquotes + Eurex-IV + Zins/Dividende | mittel | mittel (UWG, Marken) | Methodenangriffe durch Emittenten, Fehlinterpretation |

**Multi-Asset-Ausbau.** Für ES, NQ, CL und GC hat ATAS mit der Options Chain Suite bereits eine Abdeckung
auf Tagesbasis. Der Ausbau betrifft also die Intraday-Analytik. Der Engpass ist der Datenpartner: Laut
Recherche deckt OptionsDepth nur SPX und VIX ab. Für NDX und Futures-Optionen bräuchte ATAS deshalb einen
zweiten Datenpartner oder eine eigene Pipeline. Außerdem fehlen außerhalb der Cboe vergleichbar markierte
Positionsdaten. Für Einzelaktien mit mehreren Handelsplätzen müssten die Positionen stärker modelliert
werden, was die Aussagekraft mindert. Die Begründung des Quelltexts mit „überproportionaler
NDX-0DTE-Dynamik“ ist nicht belegt (A18). Tragfähig ist sie als Nachfragethese der Futures-Händler im NQ.

**Eurex-Modul.** Es ist strategisch das stärkste Alleinstellungsmerkmal. Für keinen der verglichenen Anbieter
ist intraday-fähige Eurex-GEX belegt (MenthorQ: n. v.). Gamma Cockpit liefert für den DAX nur Tageswerte. Dem stehen drei
Erschwernisse gegenüber. Eurex-Daten über EOBI/EMDI und EMDS sind lizenzpflichtig. Die 0DTE-Segmente sind
um Größenordnungen kleiner als in den USA, sodass Charm-Effekte im Tagesverlauf schwächer sind. Und die
Positionsannahme ist ohne Teilnehmermarkierung schwächer fundiert. Ein glaubwürdiges Modul wäre deshalb
zweistufig: zuerst Tagesprofile auf Basis des Open Interest mit klarer Quartalsverfall-Analyse, intraday
nur nach nachgewiesener Validierung.

**Multi-Leg-Ausführung und automatisiertes Delta-Hedging.** Die Combo-Order ist über die IB-API verfügbar.
ATAS müsste ein Strategie-Ticket bauen, mit Netto-Limitpreis, Risikoprüfung vor der Order (Margin, maximaler
Verlust, Ausübungsrisiko) und Positionsführung über alle Legs. Weit größere Folgen hat das vorgeschlagene
**automatische Delta-Hedging bei GEX-Schwellenwerten**. Löst eine Software Orders selbständig aus, handelt es
sich um algorithmischen Handel. Die Pflichten nach Art. 17 MiFID II bzw. § 80 Abs. 2 WpHG richten sich an
Wertpapierdienstleistungsunternehmen, nicht unmittelbar an Privatanleger. Für ATAS als Anbieter ist zu prüfen,
ob eine Funktion, die Anlageentscheidungen für Kunden trifft, eine erlaubnispflichtige Tätigkeit nach WpIG oder
KWG darstellt, etwa Finanzportfolioverwaltung. Unabhängig davon braucht es Pre-Trade-Limits, einen
Kill-Switch und eine klare Haftungsregel. Ein Hedge auf Basis eines bis zu 60 Sekunden alten Profils
kann in schnellen Märkten prozyklisch wirken (Modul 2). Empfohlen ist **[SZENARIO]** daher ein
halbautomatischer Vorschlag mit manueller Bestätigung statt einer vollautomatischen Auslösung.

**Warrant-Fair-Value-Tool.** Das Tool würde echten Transparenzgewinn bringen, wenn es methodisch sauber
gebaut ist. Es müsste die Emittenten-Quote eines Optionsscheins mit einem theoretischen Wert vergleichen.
Dieser Wert entsteht aus der Volatilitätsfläche der Börsenoptionen (für DAX-Basiswerte aus ODAX, nicht aus
US-Optionen), mit Laufzeit-, Strike- und Bezugsverhältnisanpassung, Zins- und Dividendenannahme, bei
US-Basiswerten mit Quanto-Effekt und mit einem Abschlag für die Emittentenbonität. Das Kontrahentenrisiko
ist ein realer ökonomischer Unterschied und gehört nicht in die „Marge“. Das Ergebnis sollte als
„Fair-Value-Differenz“ mit offener Methodik und Konfidenzband ausgewiesen und mit den Kostenangaben im
PRIIPs-KID abgeglichen werden. Wertende Begriffe und Ranglisten einzelner Emittenten bergen das Risiko
von Abmahnungen nach §§ 4, 6 UWG (K12).

### Modul 8 · Fazit und Synthese

Drei Kernaussagen des Quelltexts **halten der Prüfung stand**:
- Options X-Ray überführt SPX-Optionsdaten in ES-Hedge-Äquivalente und macht damit die Positionierung im
  Optionsmarkt für Orderflow-Händler nutzbar.
- Die Minuten-Snapshots lösen das Skalierungsproblem roher Optionsfeeds um den Preis von Analyse-Latenz bei
  Makroereignissen.
- Für den Optionshandel selbst fehlt eine native Ausführung.

Die Kombination aus Positionierungsdaten und MBO-/Footprint-Analyse in einer Oberfläche bleibt nach
Rechercheergebnis ein echtes Differenzierungsmerkmal gegenüber reinen Analyseanbietern.

**Zu relativieren** sind die mikrostrukturellen Begründungen. Market Maker hedgen aus ökonomischem Kalkül,
nicht aus gesetzlichem Zwang. GEX-Profile beruhen auf einer Positionsannahme, die beim SPX dank markierter
Cboe-Daten vergleichsweise gut, anderswo deutlich schwächer fundiert ist. Optionsscheine erzeugen eine
schwache und nicht zurechenbare Hedgespur, aber nicht gar keine.

**Entfallen** muss die steuerliche Rahmenerzählung. Die 20.000-€-Grenze für Termingeschäfte ist seit dem
JStG 2024 für alle offenen Fälle aufgehoben. Ein Verfahren vor dem BVerfG zu dieser Frage ist nicht zu
erwarten. Kapitalgesellschaften sind über § 15 Abs. 4 Satz 3 EStG nicht frei von einer Verlustbeschränkung
für Termingeschäfte.

Die strategische These für den DACH-Markt muss deshalb neu begründet werden. Der Wert einer Eurex-Erweiterung
liegt nicht darin, eine Steuerbarriere zu umgehen. Er liegt in einer Analyselücke: Für ODAX und OESX ist
im Vergleichsfeld für keinen Anbieter eine intraday-fähige Dealer-Positionierung belegt (MenthorQ: n. v.). Ob ATAS diese Lücke füllen kann,
hängt von Datenlizenzen, Validierung und einer ehrlichen Kommunikation der schwächeren Positionsannahme ab.
Diese Bewertung ist ein Szenario und keine Prognose.

---

## 4 · Glossar

| Begriff | Erklärung |
|---|---|
| 0DTE | Optionen mit Verfall am selben Handelstag („zero days to expiration“) |
| Absorption | Hohes aggressives Volumen, das von passiven Orders aufgenommen wird, ohne dass sich der Preis bewegt |
| Angemessenheitsprüfung | Prüfung von Kenntnissen und Erfahrungen des Kunden vor dem Handel komplexer Produkte (§ 63 Abs. 10 WpHG) |
| BAG / Combo-Order | IB-Ordertyp, der mehrere Optionslegs als ein Paket mit Netto-Limit handelt |
| Call Wall / Put Wall | Strike mit der höchsten Call- bzw. Put-Gamma-Konzentration; modellhaft eine Widerstands- bzw. Unterstützungszone |
| CCP | Zentrale Gegenpartei (hier Eurex Clearing), die zwischen Käufer und Verkäufer tritt |
| Charm | Änderung des Optionsdeltas durch Zeitablauf |
| Delta-Divergenz | Abweichung zwischen Preisentwicklung und kumuliertem Delta (Käufer- minus Verkäuferaggression) |
| EOBI / EMDI / EMDS | Eurex-Marktdatenschnittstellen: Einzelorderbuch / aggregiertes Orderbuch / Settlement- und OI-Daten |
| ES-Äquivalent | Umrechnung eines Options-Hedge-Deltas in eine Anzahl E-mini-S&P-500-Futures |
| Footprint | Chartform mit dem Volumen je Preisstufe, getrennt nach Bid und Ask |
| GEX | Gamma Exposure: aggregiertes Dollar-Gamma der (angenommenen) Dealer-Positionen |
| GEX-Flip | Preisniveau, an dem das Netto-Gamma-Exposure das Vorzeichen wechselt |
| Iceberg | Großorder, von der nur ein Teil im Orderbuch sichtbar ist und die nachgefüllt wird |
| Knock-out-Zertifikat | Hebelzertifikat, das beim Berühren einer Schwelle (fast) wertlos verfällt |
| MBO | Market by Order: Orderbuchdaten auf Ebene einzelner Orders |
| OPRA | Options Price Reporting Authority: konsolidierter US-Optionsdatenfeed |
| Optionsschein | Vom Emittenten begebenes, verbrieftes Optionsrecht (Schuldverschreibung) |
| PRIIPs-KID | EU-Basisinformationsblatt für verpackte Anlageprodukte mit Kosten- und Risikoangaben |
| Quartalsverfall | Gleichzeitiger Verfall von Index-Futures und -Optionen am dritten Freitag im März, Juni, September und Dezember |
| Sweep | Aggressive Order, die mehrere Preisstufen in einem Zug abräumt |
| Termingeschäft (steuerlich) | Geschäft mit Differenzausgleich bzw. vom Basiswert abgeleitetem Wert; steuerlich nach § 20 Abs. 2 S. 1 Nr. 3 EStG |
| Vanna | Änderung des Optionsdeltas bei Änderung der impliziten Volatilität |

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

---

## 6 · M-DBOM (Data Bill of Materials)

Führende Provenienzliste ist **`provenance/m300.dbom.json`** (Lehre L13: eine DBOM für Seite und Analyse). Die
Tabelle ist ein Auszug daraus und wird bei Änderungen neu erzeugt, nicht von Hand gepflegt. Stand: Modul v1.3.0,
44 Fakten, 51 Quellen.

| ID | Verdict | Klasse | Konf. | Bezugszeitraum | Claim |
|---|---|---|---|---|---|
| `FACT_JSTG2024_REPEAL` | CONFIRMED | REGULATORY_FRAMEWORK | 0,9 | Rechtsstand 2026-10-05 (JStG 2024 vom 02.12.2024) | § 20 Abs. 6 Satz 5 und 6 EStG a. F. (20.000-€-Grenze Termingeschäfte / Forderungsausfall) durch JStG 2024 aufgehoben; Anwendung in allen offenen Fällen (§ 52 Abs. 28 EStG). |
| `FACT_BMF_2025` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | BMF-Schreiben 14.05.2025 | BMF-Schreiben vom 14.05.2025 setzt die Aufhebung um; Verlustvorträge aus Termingeschäften in offenen Fällen unbeschränkt verrechenbar. |
| `FACT_TERMIN_2019` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Gesetz vom 21.12.2019, Anwendung ab 01.01.2021 | Einführung der Verlustverrechnungsbeschränkung für Termingeschäfte durch Gesetz vom 21.12.2019 (BGBl. I S. 2875): 10.000 € je Jahr, für Termingeschäfte ab 01.01.2021. |
| `FACT_TERMIN_2020_RAISE` | MEDIA_REPORT | REGULATORY_FRAMEWORK | 0,65 | JStG 2020 vom 21.12.2020 | JStG 2020 vom 21.12.2020 (BGBl. I S. 3096) erhöht die Grenze auf 20.000 €. |
| `FACT_BFH_ADV` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Beschluss 07.06.2024 | BFH VIII B 113/23 vom 07.06.2024: AdV-Beschluss (Streitjahr 2021), summarische Zweifel an der Verfassungsmäßigkeit (Art. 3 Abs. 1 GG). |
| `FACT_STOCK_LOSS_S4` | CONFIRMED | REGULATORY_FRAMEWORK | 0,7 | Rechtsstand 2026-10-05 | § 20 Abs. 6 Satz 4 EStG (Aktienverluste nur mit Aktiengewinnen) gilt fort. |
| `FACT_BVERFG_PENDING` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,6 | Stand 05.10.2026 | Zu § 20 Abs. 6 Satz 4 EStG ist beim BVerfG die Vorlage 2 BvL 3/21 anhängig; eine Entscheidung wurde bis 05.10.2026 nicht gefunden. |
| `FACT_OS_KO_NOT_TERMIN` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | BMF 03.06.2021, fortgeführt 14.05.2025 | Optionsscheine und Knock-out-Zertifikate sind nach Auffassung der Finanzverwaltung keine Termingeschäfte im Sinne von § 20 Abs. 6 Satz 5 EStG a. F. |
| `FACT_P15_KSTG` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 15 Abs. 4 Satz 3–5 EStG gilt über § 8 Abs. 1 KStG auch für Kapitalgesellschaften (gesonderter Verlustkreis für Termingeschäfte); Ausnahmen für Institute und Absicherungsgeschäfte, Rückausnahme für Aktien-Hedges (§ 3 Nr. 40 EStG, § 8b KStG). |
| `FACT_MM_NO_HEDGE_DUTY` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Keine gesetzliche Pflicht der Market Maker zum Orderbuch-Hedging; Art. 17 Abs. 3 MiFID II bzw. § 80 Abs. 4 WpHG (Definition Abs. 5) regeln Quotierungs- und Vertragspflichten. |
| `FACT_ALGO_TRADING` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | § 80 Abs. 2 WpHG verpflichtet Wertpapierdienstleistungsunternehmen, die algorithmischen Handel betreiben, zu Risikokontrollen, Notfallvorkehrungen und Dokumentation (Umsetzung Art. 17 MiFID II). |
| `FACT_MAR_RECO` | CONFIRMED | REGULATORY_FRAMEWORK | 0,85 | Rechtsstand 2026-10-05 | Art. 3 Abs. 1 Nr. 34/35 MAR definieren Anlageempfehlungen und Empfehlungen zu Anlagestrategien; die Delegierte VO (EU) 2016/958 regelt objektive Darstellung und Offenlegung von Interessenkonflikten. |
| `FACT_PRIIPS_UWG` | UNVERIFIED | REGULATORY_FRAMEWORK | 0,75 | Rechtsstand 2026-10-05 | Kosten verbriefter Derivate sind im PRIIPs-Basisinformationsblatt (VO (EU) 1286/2014) und in der Ex-ante-Kosteninformation nach Art. 24 Abs. 4 MiFID II offenzulegen; vergleichende Werbung unterliegt § 6 UWG. |
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
| `FACT_PRODUCT_STRUCTURE` | UNVERIFIED | MARKET_DATA | 0,8 | Stand 2026-10-05 | Strukturvergleich Eurex-Optionen vs. Optionsscheine/Knock-outs: Rechtsnatur, Kontrahentenrisiko (CCP vs. Emittent), Preisbildung, Volatilität im Preis, Stillhalterfähigkeit. |
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
- Zweitprüfung v1.3.0: Faktbindungen K2, K3, K4 und Steuer-Zeitachse korrigieren; FACT_PRODUCT_STRUCTURE mit passender Quelle
- Zweitprüfung v1.3.0: Aufzählung im Wettbewerbsvergleich um IBKR TWS ergänzen und an die Analyse angleichen
- Zweitprüfung v1.3.0: ODAP-Verfälle belegen; Hero-Satz „jede Aussage“ abschwächen
- Fachbegriffe beim ersten Auftreten erklären (AdV, Stillhalter, Strike, Quanto, Bezugsverhältnis, Expected Move)

---

## 8 · QA-Scorecard

> **Hinweis 2026-10-07:** Diese Scorecard gibt den Stand der Erstfassung wieder. Die aktuelle, gemessene Bewertung steht in
> `m300.html` (QA-Sektion) und im Prüfbericht `analysen/m300-qa-report-2026-10-07.md`.

| Gate | Status | Begründung |
|---|---|---|
| C1 Disclaimer | ✓ | Kurzfassung am Anfang, Vollfassung am Ende |
| C2 Keine Anlageempfehlung | ✓ | Setups generisch, ohne Instrument-, Ziel- und Timingangaben; Compliance-Hinweis in Modul 4 |
| C3 Steuer/Recht mit Stichtag und Primärquelle | ◐ | Stichtag und Normen genannt; Primärquellen nur per Snippet eingesehen (Abbruchregel 9 greift) |
| C4 Neutralität / Interessenkonflikte | ✓ | Einheitliche Maßstäbe; Matrix ohne Rangfolge; Interessenkonflikte: keine bekannt (vom Herausgeber zu bestätigen) |
| C5 Marken | ✓ | Rein beschreibend, Marken-Hinweis am Ende |
| C6 UWG | ✓ | Wertende Begriffe ersetzt; keine Emittentenbewertung |
| C7 Risikodarstellung | ✓ | Modell-, Latenz- und Positionsannahmenrisiken in Modul 1, 2, 4 |
| C8 Regulatorische Bezüge | ◐ | Korrekt benannt; PRIIPs/Art. 24 MiFID II/§ 6 UWG nicht neu am Original verifiziert |
| C9 Datenschutz | ✓ | Keine personenbezogenen Daten |
| Q1 Phase A vollständig | ✓ | Claim-Tabelle, K1–K12, Korrekturliste |
| Q2 Aktualität | ✓ | Stichtag je Aussage; a. F. gekennzeichnet |
| Q3 Mathematische Konsistenz | ✓ | Formeln mit Konvention; Zahlenbeispiel mit Probe |
| Q4 Provenienz | ✓ | Tags und Konfidenz in Claim-Tabelle und M-DBOM |
| Q5 Quellenqualität | ◐ | Primärquellen identifiziert, aber nicht im Volltext gelesen |
| Q6 Vollständigkeit | ✓ | Alle acht Module; Matrix mit [N. V.] |
| Q7 Widerspruchsfreiheit | ✓ | Fazit folgt Phase A (K1, K3, K4) |
| Q8 Glossar | ✓ | 23 Begriffe |
| Q9 Keine Halluzinationen | ◐ | Unsichere Fundstellen markiert und in Abschnitt 7 gelistet |
| Q10 Formatvorgaben | ✓ | Fließtext, Tabellen für Quantitatives, LaTeX |

**Gesamtscore:** 15 × ✓ + 4 × ◐ = 15 + 2 = 17 von 19 Punkten = **89,5 %**.
**Freigabeempfehlung: ÜBERARBEITUNG.** Kein Compliance-Gate steht auf ✗, aber C3 und C8 stehen auf ◐, und
der Score liegt unter 90 %. Nach Abarbeitung der Punkte in Abschnitt 7 ist eine Freigabe erreichbar.

---

## 9 · Disclaimer, Marken-Hinweis, Interessenkonflikte

**Disclaimer.** Diese Analyse dient ausschließlich der allgemeinen Information und Bildung. Sie stellt keine
Anlageberatung, Anlagevermittlung oder Finanzportfolioverwaltung im Sinne von WpIG, KWG oder WpHG dar.
Sie ist keine Rechtsdienstleistung im Sinne des RDG und keine Hilfeleistung in Steuersachen im Sinne des
StBerG. Sie enthält keine Anlageempfehlung und keine Empfehlung einer Anlagestrategie im Sinne von Art. 3
Abs. 1 Nr. 34 und 35 MAR. Derivate wie Optionen, Futures, Optionsscheine und Knock-out-Zertifikate sind
komplexe Produkte mit Hebelwirkung. Sie können zum Totalverlust führen. Bei Futures und Stillhaltergeschäften
sind Verluste über den Kapitaleinsatz hinaus möglich. Verbriefte Derivate tragen zusätzlich das
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
