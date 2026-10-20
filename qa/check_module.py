#!/usr/bin/env python3
"""FinCoach-AI · statische Modul-Prüfung (Gate vor jeder Veröffentlichung).

Aufruf:  python3 qa/check_module.py m300.html [provenance/m300.dbom.json]
Exit-Code 0 = alle BLOCKER bestanden, 1 = mindestens ein BLOCKER verletzt.

Jede Regel trägt die L-Nummer aus dem Fehlerkatalog qa/LESSONS.md.
Neuer Fehler → neue L-Nummer → neue Regel hier → Regressionsnachweis.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_module import build_blocks  # noqa: E402  L53b: dieselbe Erzeugung wie sync_module

BLOCKER, WARN = "BLOCKER", "WARN"
results = []
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "path", "rect", "line", "circle"}
# L12: Angaben, die eine Provenienz brauchen
FACT_PATTERN = re.compile(
    r"\d[\d.,]*\s?-?(?:%|Gbps|Mio\.|Mrd\.|€|\$|USD|US-\$|EUR\b|Kontrakte|Legs)"   # Zahl mit Einheit (L80: USD/EUR)
    r"|\d[\d.,]*\s?-?(?:s\b|Sek\.|Sekunden\w*|Min\.|Minuten\w*|Std\.|Stunden\w*|ms\b)"   # L82: Zeitangaben
    r"|\b(?:eine[rn]?|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|fünfzehn|zwanzig|dreißig|sechzig)(?: bis \w+)? (?:Sekunden|Minuten|Stunden)\b"
    r"|\b\d{2}\.\d{2}\.\d{4}\b"                                  # Datum
    r"|§\s?\d+|\bArt\.\s?\d+|\bBGBl\b|\b[IVX]+ [A-Z] \d+/\d+\b"  # Fundstelle / Aktenzeichen
)
# L28/L37: Überbehauptungen zum Prüfstatus
OVERCLAIM = r"[Aa]lle Fakten sind|geprüfte[rn]? Deep-Dive|vollständig belegt|(?<!nicht )(?<!un)verifiziert(?![^<]{0,30}nicht)|prüfen jede Aussage"
# L36: Aktenzeichen (BFH/BVerfG) und Normteile ohne §, die im gebundenen Fakt stehen müssen
AZ_NORM = (r"\b(?:[IVX]+ [A-Z]{1,2}|\d BvL|\d BvR) \d+/\d{2}\b"      # Aktenzeichen BFH/BVerfG
           r"|\b(?:Satz|Sätze|S\.)\s?\d+\b|\bAbs\.\s?\d+\b|\bNr\.\s?\d+\b")  # L36b: Normteile ohne §


def norm_txt(x):
    """L52: Markup entfernen, Entities auflösen, Leerraum zusammenfassen, Kleinschreibung."""
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", x))).strip().casefold()


def nz(x):
    """Vergleichsform: ohne Leerraum, „S.“/„Sätze“ = „Satz“."""
    return re.sub(r"\s+", "", re.sub(r"\bS\.(?=\s?\d)|\bSätze\b", "Satz", x))
FACT_PATTERN = re.compile(FACT_PATTERN.pattern + "|" + AZ_NORM)  # L36b
# L43/L50: belegpflichtige Angaben in der Analyse
MD_TOK = (r"\b\d{2}\.\d{2}\.\d{4}\b|§\s?\d+[a-z]?(?:\s?Abs\.\s?\d+)?|\b(?:[IVX]+ [A-Z]{1,2}|\d BvL|\d BvR|\d{1,2} [A-Z]{1,2}) \d+/\d{2}\b"
          r"|\bArt(?:ikel|\.)\s?\d+|\bIV [A-Z] \d+ – S \d+|\d[\d.,]*\s?-?(?:€|%|USD|\$|Gbps|Mio\.|Mrd\.|Kontrakte|Legs)|\b\d+\.\d+\.\d+\b|\b(?:19|20)\d{2}\b|\bSatznummern? \d+"
          r"|\b(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\b|\bFG [A-ZÄÖÜ][\wäöü-]+")  # L52
# L47: starke rechtliche Bewertungen müssen wörtlich im Claim stehen
STRONG = (r"voraussichtlich (?:nicht )?(?:mit [^.]{0,40}?)?vereinbar|nicht mit [^.]{0,40}?vereinbar|unvereinbar|verfassungswidrig\w*|\bnichtig\w*"
          r"|rechtswidrig\w*|gleichheits\w*widrig\w*|grundgesetzwidrig\w*|verst(?:ieß|ößt|oßen|oße) gegen")  # L52/L47b  # L52: normalisiert, Synonyme
SCOPE = re.compile(r"^(s0[1-9]|s1[01]|s-fz)$")  # Inhaltssektionen


def element_inner(html, m):
    """Inhalt eines Elements bis zum passenden Schluss-Tag (verschachtelt gezählt)."""
    tag = m.group(1)
    depth, pos = 1, m.end()
    pat = re.compile(r"<(/?)" + tag + r"\b[^>]*>")
    while depth:
        n = pat.search(html, pos)
        if not n:
            return html[m.end():]
        depth += -1 if n.group(1) else 1
        pos = n.end()
    return html[m.end():n.start()]


HIDDEN = r'<(\w+)\b[^>]*(?:\bhidden\b|data-publish="hidden"|display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0(?![.\d])|font-size\s*:\s*0(?![.\d])|sr-only|aria-hidden="true")[^>]*>.*?</\1>'


def visible_part(inner):
    """L82: Kommentare und unsichtbare Elemente zählen nicht als Kennzeichen."""
    inner = re.sub(r"<!--.*?-->", "", inner, flags=re.S)
    prev = None
    while prev != inner:
        prev, inner = inner, re.sub(HIDDEN, " ", inner, flags=re.S | re.I)
    return inner


def report(rule, level, ok, msg):
    results.append((rule, level, ok, msg))


class Tree(HTMLParser):
    """Einmaliger Durchlauf: Elternkette je Textknoten, Verweise, Gate-Zellen, Hero."""

    def __init__(self):
        super().__init__()
        self.stack, self.texts, self.refs, self.qa_rows, self.boxes = [], [], [], [], []
        self.sec = None
        self._row = None
        self._cell = None
        self.hero_graphic = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "section":
            self.sec = a.get("id", "")
        if "data-source" in a and a["data-source"].startswith("FACT_"):
            for fid in a["data-source"].split():
                self.refs.append((fid, cls))
        if re.search(r"\b(caveat-box|info-box)\b", cls):
            self.boxes.append(cls)
        if self.sec == "s01" and tag == "svg" and a.get("role") == "img":
            self.hero_graphic = True
        if self.sec == "s01" and tag == "img" and a.get("alt"):
            self.hero_graphic = True
        if self.sec == "s-qa" and tag == "tr":
            self._row = []
        if self.sec == "s-qa" and tag == "td" and self._row is not None:
            self._cell = {"cls": cls, "text": ""}
        if tag in VOID:
            return
        bound = any(k in a for k in ("data-source", "data-est", "data-def")) or tag in ("script", "style", "svg")
        node = {"tag": tag, "bound": bound, "src": a.get("data-source"), "def": a.get("data-def"), "est": False, "texts": []}
        if "est-mark" in cls and self.stack:
            self.stack[-1]["est"] = True
        self.stack.append(node)

    def handle_endtag(self, tag):
        if tag == "td" and self._cell is not None and self._row is not None:
            self._row.append(self._cell)
            self._cell = None
        if tag == "tr" and self._row is not None:
            if len(self._row) >= 2 and re.match(r"^[CQ]\d+\s", self._row[0]["text"].strip()):
                self.qa_rows.append((self._row[0]["text"].strip(), self._row[1]["cls"]))
            self._row = None
        while self.stack:
            n = self.stack.pop()
            if n["tag"] == tag:
                if not n["est"]:
                    self.texts.extend(n["texts"])
                break

    def handle_data(self, data):
        if self._cell is not None:
            self._cell["text"] += data
        if not self.stack or not data.strip():
            return
        chain_bound = any(n["bound"] for n in self.stack)
        src = next((n["src"] for n in reversed(self.stack) if n["src"]), None)
        dfn = next((n["def"] for n in reversed(self.stack) if n.get("def")), None)
        code = any(n["tag"] in ("script", "style") for n in self.stack)
        self.stack[-1]["texts"].append({"sec": self.sec, "text": data, "bound": chain_bound, "src": src, "def": dfn, "code": code})


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    page = Path(sys.argv[1])
    html = page.read_text(encoding="utf-8")
    mod = re.search(r"m(\d{3})", page.name)
    dbom_path = Path(sys.argv[2]) if len(sys.argv) > 2 else page.parent / "provenance" / f"m{mod.group(1)}.dbom.json"
    dbom = json.loads(dbom_path.read_text(encoding="utf-8")) if dbom_path.exists() else None
    md_dir = page.parent / "analysen"
    mds = sorted(md_dir.glob(f"m{mod.group(1)}-*deep-dive*.md")) if md_dir.exists() else []
    md = mds[0].read_text(encoding="utf-8") if mds else ""

    t = Tree()
    t.feed(html)

    # ---------- Styleguide / Darstellung
    m = re.search(r"\bbody\s*\{([^}]*)\}", html)
    body = (m.group(1) if m else "").replace(" ", "")
    report("L01 body-Basis", BLOCKER, "color:#E2E8F0" in body and "Inter" in body, "body{} mit color:#E2E8F0 und Inter")
    if "new Chart(" in html:
        report("L02 Chart.defaults.color", BLOCKER, "Chart.defaults.color='#94A3B8'" in html.replace('"', "'"), "Chart.defaults.color='#94A3B8'")
    report("L22 Hero-Grafik", BLOCKER, t.hero_graphic, "S01 enthält <svg role=img> bzw. <img alt>" if t.hero_graphic else "keine zugängliche Hero-Grafik in S01")
    narrow = [c for c in t.boxes if re.search(r"\bmax-w-", c)]
    report("L23 Hinweisboxen volle Breite", BLOCKER, not narrow, f"{len(t.boxes)} caveat-/info-box ohne max-w-*" if not narrow else f"{len(narrow)} Boxen mit max-w-*")
    ext = re.findall(r'<(?:script|link)\b[^>]*?(?:src|href)="(https?://[^"]+)"', html)
    report("L20 externe Ressourcen", BLOCKER, not ext, "alle Bibliotheken selbst gehostet" if not ext else "extern: " + ", ".join(sorted({re.sub(r"^https?://([^/]+).*", r"\1", u) for u in ext})))

    # ---------- Compliance
    hero = re.search(r'<section id="s01".*?</section>', html, re.S)
    hero_txt = hero.group(0) if hero else ""
    report("L04 Hero-Disclaimer", BLOCKER, bool(re.search(r"keine Anlage-?,? ?(Rechts|Anlageberatung)", hero_txt, re.I)) and "Totalverlust" in hero_txt,
           "Beratungsausschluss und Totalverlusthinweis im Hero")
    # L42 · C1-Pflichtbestandteile in jedem Disclaimer (Hero, Schluss, Analyse Anfang/Ende)
    C1_PARTS = {"Beratungsausschluss": r"keine (?:Anlage-?,? ?(?:Rechts|Steuer)|Anlageberatung)", "allgemeine Information": r"Information|Bildung", "Totalverlust": r"Totalverlust",
                "Hebel": r"Hebel(?!frei|los)", "Knock-out": r"Knock-out", "nur erfahrene Anleger": r"nur\s+für\s+erfahrene\s+Anleger"}
    NEG = re.compile(r"\b(ohne|kein\w*|nicht|ausgeschlossen|nie|unmöglich|niemals)\b|(?<![a-zäöü])un(?=erfahren)", re.I)  # L42b: Verneinung im ganzen Teilsatz

    def c1_has(rx, txt):
        txt = re.sub(r"\s+", " ", txt)
        for m in re.finditer(r"(?<![A-Za-zäöü])(?:" + rx + ")", txt, re.I):
            a = max(txt.rfind(c, 0, m.start()) for c in ".;:,!?"); b = min([i for i in (txt.find(c, m.end()) for c in ".;:,!?") if i > -1] or [len(txt)])
            clause = re.sub(r"nicht ausgeschlossen", "möglich", txt[a + 1:b], flags=re.I)  # L42c: doppelte Verneinung = positiv
            if rx.startswith("keine") or not NEG.search(clause):
                return True
        return False
    hd = re.search(r'<(\w+)[^>]*data-qa="hero-disclaimer"[^>]*>', html)
    closing = re.findall(r'<div class="caveat-box[^"]*">\s*<h3[^>]*>Disclaimer.*?</div>', html, re.S)
    discl = {"Hero": element_inner(html, hd) if hd else "", "Schluss": closing[-1] if closing else ""}
    if md:
        k1 = re.search(r"> \*\*Disclaimer \(Kurzfassung\):\*\*.*?(?=\n\n)", md, re.S)
        k9 = re.search(r"\*\*Disclaimer\.\*\*.*?(?=\n\n)", md, re.S)
        discl.update({"Analyse Anfang": re.sub(r"\n> ?", " ", k1.group(0)) if k1 else "", "Analyse Ende": re.sub(r"\n", " ", k9.group(0)) if k9 else ""})
    c1_miss = [f"{w}: {p}" for w, txt in discl.items() for p, rx in C1_PARTS.items() if not c1_has(rx, re.sub(r"<[^>]+>", "", txt))]
    c1_miss += [f"{w}: positive Beratungsaussage" for w, txt in discl.items() if re.search(r"(?<!kein)\b(?:ist|sind|stellt)\b[^.]{0,20}\b(?:eine )?Anlageberatung\b(?! ?(?:dar)?[^.]{0,5}keine)", re.sub(r"<[^>]+>", "", txt)) and not re.search(r"keine[^.]{0,40}Anlageberatung", re.sub(r"<[^>]+>", "", txt))]
    report("L42 C1-Pflichtbestandteile", BLOCKER, not c1_miss, "fehlt: " + ", ".join(c1_miss[:6]) if c1_miss else f"{len(discl)} Disclaimer vollständig")

    # ---------- Provenienz
    js_ks = re.search(r"const KS=\[(.*?)\n\];", html, re.S)
    js_reg = re.search(r"const REG=\{(.*?)\n\};", html, re.S)
    js_refs = set(re.findall(r"FACT_[A-Z0-9_]+", (js_ks.group(1) if js_ks else "") + (js_reg.group(1) if js_reg else "")))
    ref_ids = {r[0] for r in t.refs} | js_refs
    if dbom:
        facts = {f["id"]: f for f in dbom.get("facts", [])}
        srcs = {s["id"]: s for s in dbom.get("sources", [])}
        F = list(facts.values())
        missing = sorted(ref_ids - facts.keys())
        report("L08a Verweise aufgelöst", BLOCKER, not missing, "fehlend: " + ", ".join(missing) if missing else f"{len(ref_ids)} Verweise ok")
        unbound = sorted(facts.keys() - ref_ids)
        report("L08b Fakten gebunden", BLOCKER, not unbound, "ungebunden: " + ", ".join(unbound) if unbound else "alle Fakten gebunden")
        allowed = {"CONFIRMED", "MEDIA_REPORT", "UNVERIFIED", "SCENARIO_PROJECTION"}
        badv = [f["id"] for f in F if f["verdict"] not in allowed]
        report("L05c Verdict zulässig", BLOCKER, not badv, "unzulässig: " + ", ".join(badv) if badv else "alle zulässig")
        bad = [f["id"] for f in F if f["verdict"] == "CONFIRMED" and (f["class"] in ("MEDIA_REPORT", "MODEL_ASSUMPTION", "SCENARIO_PROJECTION") or f["confidence"] < 0.7)]
        report("L05 Verdict-Klasse", BLOCKER, not bad, "CONFIRMED trotz Medien/Modell/Konf.<0,7: " + ", ".join(bad) if bad else "konsistent")
        wrong_kpi = sorted({fid for fid, cls in t.refs if "confirmed-kpi" in cls and facts.get(fid, {}).get("verdict") != "CONFIRMED"})
        report("L05b KPI-Stil", BLOCKER, not wrong_kpi, "confirmed-kpi auf nicht bestätigtem Fakt: " + ", ".join(wrong_kpi) if wrong_kpi else "konsistent")
        noper = [f["id"] for f in F if f["verdict"] == "CONFIRMED" and not re.search(r"\b(19|20)\d\d\b", f.get("period", ""))]
        report("L16 Bezugszeitraum", BLOCKER, not noper, "CONFIRMED ohne datierten period: " + ", ".join(noper) if noper else "alle CONFIRMED mit datiertem period")
        weak = [f["id"] for f in F if f["verdict"] == "CONFIRMED" and srcs.get(f["source_id"], {}).get("tier") not in ("primary", "vendor")]
        weak += [f["id"] for f in F if f["verdict"] == "CONFIRMED" and any(srcs.get(a, {}).get("tier") == "secondary" for a in f.get("additional_sources", []))]
        report("L19 schwächster Teilbeleg", BLOCKER, not weak, "CONFIRMED mit Sekundär-Hauptbeleg/Teilbeleg: " + ", ".join(sorted(set(weak))) if weak else "konsistent")
        used = {s for f in F for s in [f.get("source_id"), *f.get("supporting_sources", []), *f.get("additional_sources", [])] if s}
        unused, dangling = sorted(srcs.keys() - used), sorted(used - srcs.keys())
        report("L14 Quellen ↔ Fakten", BLOCKER, not unused and not dangling,
               " ".join(x for x in [("ungenutzt: " + ", ".join(unused)) if unused else "", ("fehlend: " + ", ".join(dangling)) if dangling else ""] if x) or f"{len(srcs)} Quellen, alle genutzt")
        cnt = {"total": len(F), "confirmed": sum(f["verdict"] == "CONFIRMED" for f in F), "media": sum(f["verdict"] == "MEDIA_REPORT" for f in F),
               "unverified": sum(f["verdict"] == "UNVERIFIED" for f in F), "scenario": sum(f["verdict"] == "SCENARIO_PROJECTION" for f in F),
               "vendor": sum(f["class"] == "VENDOR_CLAIM" for f in F), "sources": len(srcs)}
        shown = re.findall(r'data-dbom-count="(\w+)"[^>]*>(\d+)<', html)
        diffs = [f"{k}: Text {v} ≠ DBOM {cnt[k]}" for k, v in shown if k in cnt and int(v) != cnt[k]]
        report("L07 Zählungen", BLOCKER, bool(shown) and not diffs, "; ".join(diffs) if diffs else ("alle Zählungen = DBOM" if shown else "keine data-dbom-count-Bindung"))
        hard = re.findall(r"(?<!von )\b\d+ (?:belegt|belegte Fakten|Herstellerangaben)\b", re.sub(r'<span data-dbom-count="\w+">\d+</span>', "", html))
        report("L07b keine Hardcodes", WARN, not hard, "fest geschrieben: " + ", ".join(hard) if hard else "keine")
        ld = re.search(r'"fact_summary":\s*\{([^}]*)\}', html)
        if ld:
            nums = {k: int(v) for k, v in re.findall(r'"(\w+)":\s*(\d+)', ld.group(1))}
            d2 = [f"{k}: {v}≠{dbom['fact_summary'].get(k)}" for k, v in nums.items() if dbom["fact_summary"].get(k) != v]
            report("L07c JSON-LD", BLOCKER, not d2, "; ".join(d2) if d2 else "JSON-LD = DBOM")
        # L21 · Konfidenz-Spannen aus der DBOM
        rng = {}
        for f in F:
            if f["confidence"] is not None:
                rng.setdefault(f["class"], []).append(f["confidence"])
        rd = []
        for k, lo, hi in re.findall(r'data-dbom-range="(\w+)">([\d,]+)–([\d,]+)<', html):
            if k in rng and (float(lo.replace(",", ".")), float(hi.replace(",", "."))) != (min(rng[k]), max(rng[k])):
                rd.append(f"{k}: Text {lo}–{hi} ≠ DBOM {min(rng[k])}–{max(rng[k])}")
        has_ranges = "data-dbom-range" in html
        report("L21 Konfidenz-Spannen", BLOCKER, has_ranges and not rd, "; ".join(rd) if rd else ("Spannen = DBOM" if has_ranges else "Spannen nicht an DBOM gebunden"))
        # L17 · Zahl im gebundenen Element steht im gebundenen Fakt
        miss = []
        for x in t.texts:
            if not x["src"]:
                continue
            hay = " ".join(str(facts[s].get(k, "")) for s in x["src"].split() if s in facts for k in ("claim", "period", "caveat"))
            for num in re.findall(r"\d[\d.,]*(?=\s?(?:%|Gbps|Mio\.|Mrd\.|€|\$|Kontrakte|Legs))", x["text"]):
                if num.rstrip(".,") not in hay:
                    miss.append(f"{x['src'].split()[0]}: {num}")
        report("L17 Zahl ∈ Fakt", BLOCKER, not miss, ("nicht im gebundenen Fakt: " + ", ".join(sorted(set(miss))[:8])) if miss else "alle gebundenen Zahlen im Fakt")
        # L18 · Quantor-Nenner: Seite = DBOM-Basis = Analyse
        basis = {f["id"]: f["basis"] for f in F if "basis" in f}
        pg = [(int(a), int(b)) for a, b in re.findall(r">(\d+) von (\d+)<", html)]
        words = {"zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7}
        an = {words[w] for w in re.findall(r"(?:keinem|keiner|alle) der (zwei|drei|vier|fünf|sechs|sieben)\b[^.]{0,80}?Anbieter", md)}
        det = {b["determinable"] for b in basis.values()}
        # L33: ein Abgleich besteht nie über eine leere Menge, wenn eine DBOM-Basis existiert
        ok18 = bool(det) and bool(pg) and (bool(an) or not md) and {n for _, n in pg} <= det and an <= det
        report("L18 Quantor-Nenner", BLOCKER, ok18, f"Seite {sorted({n for _, n in pg})} · Analyse {sorted(an)} · DBOM-Basis {sorted(det)}")

        # L21b · Konfidenz-Pills aus der DBOM
        conf_bad = [f"{fid}: {v}" for fid, v in re.findall(r'data-dbom-conf="(\w+)">([\d,]+)<', html)
                    if fid in facts and (facts[fid]["confidence"] is None or abs(float(v.replace(",", ".")) - facts[fid]["confidence"]) > 1e-9)]
        hand_conf = re.findall(r'class="dbom-conf">Konf\. [\d.,]+<', html)
        report("L21b Konfidenz-Pills", BLOCKER, not conf_bad and not hand_conf, "; ".join(conf_bad + hand_conf) or "alle Pills an DBOM gebunden")
        # L26 · Fakt mit offenem Pflichtpunkt ist nicht CONFIRMED
        open_facts = {fid for li in re.findall(r"<li[^>]*data-open[^>]*>", html) for m in re.findall(r'data-source="([^"]+)"', li) for fid in m.split()}
        oc = sorted(f for f in open_facts if facts.get(f, {}).get("verdict") == "CONFIRMED")
        report("L26 Offen ⇒ nicht CONFIRMED", BLOCKER, not oc, "CONFIRMED trotz Offen-Punkt: " + ", ".join(oc) if oc else f"{len(open_facts)} Fakten in der Offen-Liste, keiner CONFIRMED")
        # L26b · Offen-Punkte, die eine Fundstelle aus einem Fakt nennen, binden diesen Fakt
        l26b = []
        for li in re.finditer(r"<li([^>]*data-open[^>]*)>(.*?)</li>", html, re.S):
            ids = set(re.findall(r"FACT_[A-Z0-9_]+", li.group(0)))  # L50: Bindung auch in innerem Markup
            for tk in re.findall(r"§\s?\d+[a-z]?\s?Abs\.\s?\d+|" + AZ_NORM, re.sub(r"<[^>]+>", "", li.group(2))):
                hit = {f["id"] for f in F if nz(tk) in nz(f["claim"])}
                if hit and not hit & ids:
                    l26b.append(f"„{tk}“ → {', '.join(sorted(hit))}")
        report("L26b Offen-Punkt mit Fundstelle gebunden", BLOCKER, not l26b, "ungebunden: " + "; ".join(l26b[:4]) if l26b else "Fundstellen in Offen-Punkten an ihre Fakten gebunden")
        # L43 · Analyse: Daten, Paragraphen und Aktenzeichen vor Abschnitt 5 stehen in einem DBOM-Fakt
        if md:
            hay_all = nz(" ".join(str(f.get(k, "")) for f in F for k in ("claim", "period", "caveat")))
            body = re.split(r"\n## 5 · ", md)[0]
            body = "\n" * body[:body.find("\n## 1 ")].count("\n") + body[body.find("\n## 1 "):]  # Titelblock (Version, Prompt) ausgenommen, Zeilen bleiben
            body = re.sub(r"\$\$.*?\$\$|\$[^$]+?\$", lambda m: "\n" * m.group(0).count("\n"), body, flags=re.S)  # Formeln (Modell) ausgenommen, Zeilen bleiben
            md_miss = []
            fz = lambda x: nz(x).replace("-€", "€").replace("€-", "€")
            pos = 0
            for para in re.split(r"(\n\s*\n|\n(?=[-|] ))", body):  # L56: Token im Fakt desselben Absatzes bzw. derselben Zeile
                ids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", para) if i in facts]
                hay = fz(" ".join(str(facts[i].get(k, "")) for i in ids for k in ("claim", "period", "caveat"))) if ids else fz(hay_all)
                for m in re.finditer(MD_TOK, para):
                    if fz(m.group(0)) not in hay:
                        md_miss.append(f"Z. {body[:pos + m.start()].count(chr(10)) + 1}: {m.group(0)}")
                pos += len(para)
            report("L43 Analyse-Angaben ∈ DBOM", BLOCKER, not md_miss, "ohne Fakt: " + ", ".join(md_miss[:8]) + (f" (+{len(md_miss) - 8})" if len(md_miss) > 8 else "") if md_miss else "alle Daten und Fundstellen der Analyse in der DBOM")
        # L46/L52b · Leitphrasen abgetrennter Fakten (keine abgetrennten Fakten = keine Leitphrasen; L33: leere Basis, kein leerer Test): kleinstes Element mit der Leitphrase (normalisiert) bindet den Fakt allein
        l46 = []
        scan = re.sub(r'<section id="s-qa".*?</section>|<(script|style)\b.*?</\1>', "", html, flags=re.S)
        elems = [(m, norm_txt(element_inner(scan, m))) for m in re.finditer(r"<(p|li|td|th|div|span|h\d|strong|em|a|abbr|dfn)\b[^>]*>", scan)]
        for f in F:
            for mk in (norm_txt(x) for x in f.get("markers", [])):
                hits = [(m, txt) for m, txt in elems if mk in txt]
                for m, txt in hits:
                    inner = [n for n, t2 in hits if n.start() > m.start() and n.end() <= m.start() + len(element_inner(scan, m)) + len(m.group(0)) and mk in t2]
                    if inner:
                        continue  # nicht das kleinste Element
                    src = re.search(r'data-source="([^"]+)"', m.group(0))
                    if not src or src.group(1).split() != [f["id"]]:
                        l46.append(f"„{mk}“ nicht allein an {f['id']}: {txt[:40]}…")
                for blob in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else []) + ([b for _, b in re.findall(r"\n\s*(\w+):\{(.*?)\}(?:,|$)", js_reg.group(1))] if js_reg else []):
                    if mk in norm_txt(blob) and (f["id"] not in blob or (f["verdict"] != "CONFIRMED" and not re.search(r"ungeprüft|medienangabe|modell", norm_txt(blob)))):
                        l46.append(f"JS „{mk}“ ohne {f['id']}")
        report("L46 Leitphrasen gebunden", BLOCKER, not l46, "; ".join(sorted(set(l46))[:4]) if l46 else ("alle Leitphrasen an ihren Fakt gebunden" if any(f.get("markers") for f in F) else "keine abgetrennten Fakten mit Leitphrasen in der DBOM"))
        # L51 · Leitphrasen in der Analyse: Absatz/Zeile nennt den Fakt (normalisiert, L52b)
        l51 = []
        if md:
            for para in re.split(r"\n\s*\n|\n(?=[-|] )", re.split(r"\n## 5 · ", md)[0]):
                for f in F:
                    for mk in f.get("markers", []):
                        if norm_txt(mk) in norm_txt(re.sub(r"[*_`]", "", para)) and f["id"] not in para:
                            l51.append(f"„{mk}“ ohne {f['id']}: {re.sub(chr(10), ' ', para)[:50]}…")
        report("L51 Leitphrasen in der Analyse", BLOCKER, not l51, "; ".join(l51[:3]) if l51 else "alle Leitphrasen der Analyse nennen ihren Fakt")
        # L57 · „belegt/bestätigt“ nur mit gebundenem CONFIRMED-Fakt (Seite: gebundene Texte und K-Tabelle; Analyse: Absätze)
        l57 = []
        for x in t.texts:
            if x["src"] and not x.get("code") and re.search(r"\b(belegt|bestätigt)\w*", x["text"]) and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in x["src"].split()):
                l57.append(f"{x['sec']}: {x['text'].strip()[:40]}…")
        for x in t.texts:  # L53c: auch ungebundene Texte (außer Zählzeile, Legende, QA-Sektion)
            if not x["src"] and not x.get("code") and x["sec"] not in (None, "s-qa", "s01", "s03") and re.search(r"\b(belegt|bestätigt)\w*", x["text"]):
                l57.append(f"{x['sec']} (ungebunden): {x['text'].strip()[:40]}…")
        for row in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else []):
            if re.search(r"\b(belegt|bestätigt)\b", re.sub(r'"(?:ok|part|no)"', "", row)) and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in re.findall(r"FACT_[A-Z0-9_]+", row)):
                l57.append(row[2:6].strip('",'))
        if md:
            for para in re.split(r"\n\s*\n|\n(?=[-|] )", re.split(r"\n## 5 · ", md)[0]):
                txt = re.sub(r"\(`FACT_[A-Z0-9_]+`, (?:belegt|Medienangabe|ungeprüft|SCENARIO_PROJECTION)[^)]*\)|Legende:[^\n]*|Schwächster Beleg|\| belegt \|", "", para)
                if re.search(r"\b(belegt|bestätigt)\b", txt) and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in re.findall(r"FACT_[A-Z0-9_]+", para)):
                    l57.append("Analyse: " + re.sub(r"\s+", " ", txt)[:40] + "…")
        report("L57 „belegt“ nur mit CONFIRMED", BLOCKER, not l57, "; ".join(l57[:4]) if l57 else "„belegt/bestätigt“ nur bei gebundenem CONFIRMED-Fakt")
        # L61 · Claim-Ergebnis passt zu den Belegen: ✓/✗ nur mit CONFIRMED-Beleg; = Ergebnis der zugeordneten K-Zeile; [N. V.] mit Offen-Punkt
        kres = {k[0]: k[3] for k in (json.loads(r) for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else []))}
        open_txt = " ".join(re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<li[^>]*data-open[^>]*>(.*?)</li>", html, re.S))
        l61 = []
        for c in dbom.get("source_claims", []):
            if c["result"] in ("ok", "no") and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in c["facts"]):
                l61.append(f"{c['id']}: {c['result']} ohne CONFIRMED-Beleg")
            if c.get("k") and kres.get(c["k"]) != c["result"]:
                l61.append(f"{c['id']} ≠ {c['k']}")
            if c["result"] in ("part", "scen") and not c["facts"]:
                l61.append(f"{c['id']}: {c['result']} ohne Belege")
            kshare = [k for k, row in ((json.loads(r)[0], json.loads(r)) for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else [])) if set(row[6].split()) & set(c["facts"])]
            if kshare and not c.get("k") and not c.get("k_differs"):
                l61.append(f"{c['id']}: teilt Belege mit {kshare[0]}, aber ohne k/k_differs")  # L69
            kd = c.get("k_differs", "")
            kd_words = {w for w in re.findall(r"[a-zäöüß]{5,}", kd.casefold())} - {"bewertet", "teilaspekt", "daher", "abweichend", "nicht", "passt", "anders"}
            if kd and (len(kd.strip()) < 25 or not (set(re.findall(r"\bK\d+\b", kd)) & (set(kshare) or set(kres)))
                       or not any(w[:6] in c["claim"].casefold() for w in kd_words)):  # L80: Sachgrund nennt einen Gegenstand des Claims
                l61.append(f"{c['id']}: k_differs ohne Begründung mit Bezug auf {'/'.join(kshare) or 'eine K-Zeile mit gemeinsamen Belegen'}")  # L80
            if c["result"] == "nv" and c["id"] not in open_txt:
                l61.append(f"{c['id']}: [N. V.] ohne Offen-Punkt")
            l61 += [f"{c['id']}: unbekannte ID {i}" for i in c["facts"] if i not in facts]
        report("L61 Claim-Ergebnis = Belege", BLOCKER, bool(dbom.get("source_claims")) and not l61, "; ".join(l61[:4]) if l61 else f"{len(dbom.get('source_claims', []))} Claims konsistent")
        # L62 · Fazit: jeder Punkt als Einschätzung (Badge) oder ausdrücklich als Faktwiedergabe (data-assessment="fact"); SCENARIO im Konjunktiv
        fzs = re.search(r'<section id="s-fz".*?</section>', html, re.S)
        l62 = []
        WERT = (r"besser|schwächer|merkmal|differenzier|lösen|mehrwert|empf(?:ohl|ehl|iehl)|sinnvoll|überleg|ideal|wertvoll|leider|beste|optimal|attraktiv"
                r"|überzeug|deutlich|vorteil|nachteil|stärke|schwäche|\bschwach|\bstark|\bklar(?:er|e|es)?\b|\bgut\b|schlecht|hervorragend|enttäusch|bedauer"
                r"|unverzichtbar|erfreulich|unschlagbar|beeindruck|überragend|herausragend|ärgerlich|gelungen|mangelhaft|lohnend|lohnt")  # L70/L80
        no_claims = {c["id"] for c in dbom.get("source_claims", []) if c["result"] == "no"} | {k for k, v in kres.items() if v == "no"}
        fz_html = re.sub(r"<!--.*?-->", "", fzs.group(0), flags=re.S) if fzs else ""
        for li in re.findall(r"<li\b[^>]*>.*?</li>", fz_html, re.S):
            badge = 'dbom-class-badge">EINSCHÄTZUNG<' in li
            refuted = (re.search(r'data-claim="([AK]\d+)"', li) or [None, None])[1] in no_claims  # gibt einen widerlegten Claim wieder
            if not badge and not refuted and re.search(WERT, norm_txt(li)):
                l62.append("Wertung ohne EINSCHÄTZUNG: " + re.sub(r"<[^>]+>", "", li)[:40])  # L70/L80: data-claim ersetzt das Badge nicht
            if not badge and 'data-assessment="fact"' not in li:
                l62.append("Fazit-Punkt ohne Einordnung: " + re.sub(r"<[^>]+>", "", li)[:40])
        scen = {f["id"] for f in F if f["verdict"] == "SCENARIO_PROJECTION"}
        for m in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html):
            ids = m.group(2).split()
            if ids and set(ids) <= scen and m.group(1) in ("span", "p", "div", "li"):
                for sent in re.split(r"(?<=[.!?])\s+", norm_txt(re.sub(r"<span class=\"dbom-class-badge\">(?:SCENARIO|MODELL)</span>", " §badge§ ", re.sub(r"<(table|label|h[1-6]|caption|canvas|figcaption|thead)\b.*?</\1>", " ", element_inner(html, m), flags=re.S)))):  # L80: Fließtext satzweise, jedes Verb
                    if "§badge§" in sent and len(sent.split()) <= 7:
                        continue  # kurze Beschriftung mit SCENARIO-/MODELL-Badge („Bewertung von Vorschlägen, keine Prognose.“)
                    if len(sent.split()) >= 4 and not re.search(r"\b(läge|lägen|träfe|träfen|wäre|wären|könnte|könnten|würde|würden|käme|kämen|hätte|hätten|ließe|dürfte|müsste)\b|szenario|hypothetisch|angenommen|illustrativ|denkbar", sent):
                        l62.append("SCENARIO im Indikativ: " + sent[:40])
        # L80: Text außerhalb der <li> (Info-Boxen) satzweise; Empfehlungen seitenweit satzweise
        def sentences(h):
            h = re.sub(r'<span class="dbom-class-badge">(\w+)</span>', r" §\1§ ", h)
            return [x.strip() for x in re.split(r"(?<=[.!?])\s+", norm_txt(h)) if x.strip()]
        for sent in sentences(re.sub(r"<li\b.*?</li>|<h[1-6]\b.*?</h[1-6]>", " ", fz_html, flags=re.S)):
            if re.search(WERT, sent) and not re.search(r"§(einschätzung|scenario)§", sent):
                l62.append("Wertung ohne EINSCHÄTZUNG: " + sent[:40])
        body_wo = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->", "", html, flags=re.S)
        for sent in sentences(body_wo):  # L80: Produktpläne von ATAS nur als Szenario
            if re.search(r"\batas (?:führt\b.*\bein\b|plant|kündigt|wird (?:\S+ ){0,4}(?:einführen|anbieten|integrieren|bringen))", sent) and not re.search(r"§(scenario|einschätzung)§|\b(?:würde|könnte|käme|wäre)\b", sent):
                l62.append("Produktplan als Tatsache: " + sent[:40])
        for sent in sentences(body_wo):
            if re.search(r"(?<!anlage)empf(?:ohl|ehl|iehl)\w*|\bratsam\b|sollten (?:anleger|privatanleger|sie|trader)|\bwer\b[^.]*\bsollte\b|\bsollte[n]? (?:man|anleger|trader|privatanleger)\b|bessere wahl|vorzuziehen|klar besser|\bbesser geeignet", sent) \
                    and not re.search(r"§(einschätzung|scenario)§|kein\w* (?:\S+ ){0,2}\S*empf|nicht (?:\S+ )?empf", sent):  # L80: auch „Empfehlung“, seitenweit
                l62.append("Empfehlung/Wertung ohne SCENARIO/EINSCHÄTZUNG: " + sent[:40])
        # L66 · Fazit-Punkte unter „Relativiert/Entfällt“ verweisen auf einen Claim oder K-Punkt
        for box in re.findall(r"<h3[^>]*>[^<]*(?:Relativiert|Entfällt)[^<]*</h3><ul[^>]*>(.*?)</ul>", fzs.group(0) if fzs else "", re.S):
            for li in re.findall(r"<li\b[^>]*>", box):
                cl = re.search(r'data-claim="([AK]\d+)"', li)
                ok_ids = {c["id"] for c in dbom.get("source_claims", [])} | set(kres)
                if not cl or cl.group(1) not in ok_ids:
                    l62.append("Fazit-Punkt ohne gültigen data-claim (L66)")
                    continue
                lis = set((re.search(r'data-source="([^"]*)"', li) or [None, ""])[1].split())
                cf = set(next((c["facts"] for c in dbom.get("source_claims", []) if c["id"] == cl.group(1)), []))
                cf |= set(next((json.loads(r)[6].split() for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else []) if json.loads(r)[0] == cl.group(1)), []))
                if not lis & cf:
                    l62.append(f"Fazit-Punkt: data-claim {cl.group(1)} teilt keinen Beleg mit dem Punkt (L66/L80)")
        report("L62 Fazit eingeordnet, SCENARIO im Konjunktiv", BLOCKER, bool(fzs) and not l62, "; ".join(l62[:3]) if l62 else "alle Fazit-Punkte eingeordnet; Szenarien im Konjunktiv")
        js_gl = re.search(r"const GLOSSAR=\[(.*?)\n\];", html, re.S)
        # L63 · Konstanten eines Fakts (values) stimmen überall und sind gebunden (auch Formeln, Labels, data-def, Glossar)
        l63 = []
        for f in F:
            for sym, val in f.get("values", {}).items():
                rx = re.compile(r"(?:M_\{(?:\\text\{)?%s\}?\}\s*=\s*|\b%s(?:-\w*[Mm]ultiplikator)?\)?\s*(?:\(|=|:)?\s*)(\d+)\b(?!\s?%%|[.,]\d)|Multiplikator\s*\(?(\d+)\)?\s*\(%s\)"
                                r"|\b%s\b[^\d<>.;]{0,30}?(\d+)\s?(?:USD|US-?\$|\$|€)" % (sym, sym, sym, sym))  # L71/L80: KaTeX \text, Einheit nach bis zu 30 Zeichen
                for m in rx.finditer(scan):
                    num = m.group(1) or m.group(2) or m.group(3)
                    if num != val:
                        l63.append(f"{sym} = {num} ≠ {val}")
                    else:
                        before = scan[:m.start()]
                        opened = [o for o in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', before) if f["id"] in o.group(2).split()]
                        if not any(m.start() < o.end() + len(element_inner(scan, o)) for o in opened):
                            l63.append(f"{sym} {val} nicht an {f['id']} gebunden")
                for row in (re.findall(r'^\s*\[".*\]', js_gl.group(1), re.M) if js_gl else []):
                    for m in rx.finditer(row):
                        if (m.group(1) or m.group(2) or m.group(3)) != val or f["id"] not in row:
                            l63.append(f"Glossar {sym} {m.group(1) or m.group(2) or m.group(3)}")
                if md:
                    l63 += [f"Analyse {sym} = {m.group(1) or m.group(2) or m.group(3)}" for m in rx.finditer(md) if (m.group(1) or m.group(2) or m.group(3)) != val]
            for sym, val in f.get("values", {}).items():
                rxk = re.compile(r"\b%s\b[^\d<>.;]{0,30}?(\d+)\s?(?:USD|US-?\$|\$|€)|\b%s\s*(?:\(|=)\s*(\d+)\b" % (sym, sym))
                for row in (re.findall(r'^\s*\["K\d+",.*\]', js_ks.group(1), re.M) if js_ks else []):
                    for m in rxk.finditer(row):
                        if (m.group(1) or m.group(2)) != val:
                            l63.append(f"K-Tabelle {sym} {m.group(1) or m.group(2)} ≠ {val}")
            # L80: Rechner-Vorgaben in an den Fakt gebundenen Labels
            for lab in re.finditer(r'<label\b[^>]*data-source="([^"]*)"[^>]*>(.*?)</label>', html, re.S):
                if f["id"] in lab.group(1).split():
                    syms = [y for y in f.get("values", {}) if re.search(r"\b%s\b" % y, re.sub(r"<input\b[^>]*>", "", lab.group(2)))]
                    inp = re.search(r'<input\b[^>]*\bvalue="([^"]*)"', lab.group(2))
                    if len(syms) == 1 and inp and inp.group(1) != f["values"][syms[0]]:
                        l63.append(f"Rechner {syms[0]} value={inp.group(1)} ≠ {f['values'][syms[0]]}")
                    iid = re.search(r'<input\b[^>]*\bid="([^"]+)"', lab.group(2))
                    if len(syms) == 1 and iid:  # L80: JS-Ersatzwert num('id')||N
                        for fb in re.findall(r"num\('%s'\)\s*\|\|\s*(\d+)" % re.escape(iid.group(1)), html):
                            if fb != f["values"][syms[0]]:
                                l63.append(f"Rechner-Ersatzwert {syms[0]} {fb} ≠ {f['values'][syms[0]]}")
        report("L63 Faktkonstanten gebunden", BLOCKER, not l63, "; ".join(sorted(set(l63))[:4]) if l63 else "alle Faktkonstanten stimmen und sind gebunden")
        # L27b · Glossar: Einträge mit nicht bestätigtem Fakt tragen das Badge des schwächsten Verdicts
        BADGE1 = {"MEDIA_REPORT": "MEDIEN", "UNVERIFIED": "UNGEPRÜFT", "SCENARIO_PROJECTION": "SCENARIO"}
        RANK = {"CONFIRMED": 3, "MEDIA_REPORT": 2, "UNVERIFIED": 1, "SCENARIO_PROJECTION": 0}
        l27b = []
        for r in (re.findall(r'^\s*(\[".*\])\s*,?\s*$', js_gl.group(1), re.M) if js_gl else []):
            g = json.loads(r)
            ids = g[4].split() if len(g) > 4 else []
            weak = min((facts[i]["verdict"] for i in ids if i in facts), key=RANK.get, default="CONFIRMED")
            want = BADGE1.get(weak, "")
            if (g[5] if len(g) > 5 else "") != want:
                l27b.append(f"{g[0]}: Badge „{g[5] if len(g) > 5 else ''}“ ≠ „{want}“")
        # L27c · ungebundene Glossar-Einträge enthalten keine Tatsachenmerkmale (Institution, Norm, Rechtsnatur, Risikoaussage)
        l27c = []
        for r in (re.findall(r'^\s*(\[".*\])\s*,?\s*$', js_gl.group(1), re.M) if js_gl else []):
            g = json.loads(r)
            if not (len(g) > 4 and g[4].strip()):
                hit = re.search(r"§|\b(eurex|cboe|cme|bafin|esma|wphg|estg|kstg|kwg|mar|mifid\w*|priips|emir|nasdaq|xetra|nyse|ice|börse\w*|emittent\w*|rechtlich\w*|gesetz\w*"
                                r"|vorgeschrieben|\w*pflicht\w*|veröffentlich\w*|bonität|kontrahent\w*|schuldverschreibung|ccp|atas|ib|tws|anbiete\w*|bieten|lizen\w*|\d{4})\b", norm_txt(" ".join(g[1:4])))  # L80
                if hit:
                    l27c.append(f"{g[0]}: „{hit.group(0)}“ ohne Fakt")
        report("L27c Glossar-Tatsachen gebunden", BLOCKER, bool(js_gl) and not l27c, "; ".join(l27c[:4]) if l27c else "ungebundene Glossar-Einträge ohne Tatsachenmerkmale")
        rend27 = "g[5]" in html and "dbom-class-badge" in html[html.find("function renderGlossar"):html.find("function renderGlossar") + 600]
        report("L27b Glossar-Badges", BLOCKER, not l27b and rend27, "; ".join(l27b[:4]) if l27b else ("Renderer ohne Badge" if not rend27 else "Glossar-Badges = schwächstes Verdict"))
        # L06b/L72 · Alleinstellungs-Aussagen nur mit Vergleichsbasis im selben Satz (auch K-Tabelle)
        l06b = []
        UNIQ_NOUN = r"(?:\S+ ){0,2}(?:Anbieter\w*|Werkzeug\w*|Tool\w*|Plattform\w*|Lösung\w*|Produkt\w*|Software|Wettbewerber\w*|Börse\w*|Dienst\w*|Indikator\w*|Suite|Feed\w*|Broker\w*)"
        ALLEIN = (r"Alleinstellung|einzigartig|\beinzige[rnsm]? " + UNIQ_NOUN + r"|\beinzig (?:ATAS|bei|mit)\b|\bals einzige\w*|exklusiv\w*|\bnur (?:ATAS|wir|ein\w* (?:Anbieter|Werkzeug|Tool|Plattform))\b"
                  r"|\bkein(?:e[rn]?)? (?:andere[rn]? )?(?:Wettbewerber|Anbieter|Konkurrent)\w*|\bniemand sonst\b|\bsonst (?:niemand|keiner|kein Anbieter)\b")  # L72/L80
        uniq_ok = {f["id"] for f in F if re.search(r"\bnur (?:an|bei|von|über) (?:der|dem|den)\b|\beinzig|\bkeiner\b", f["claim"], re.I)}  # L82: Alleinstellung, die der Claim selbst trägt
        js_strs = [m.group(1) for sc in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S) for m in re.finditer(r'"((?:[^"\\]|\\.){12,})"|`([^`]{12,})`|\'((?:[^\'\\]|\\.){12,})\'', sc) if m.group(1)]
        js_strs += [m.group(2) or m.group(3) for sc in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S) for m in re.finditer(r'"((?:[^"\\]|\\.){12,})"|`([^`]{12,})`|\'((?:[^\'\\]|\\.){12,})\'', sc) if not m.group(1)]
        for js in js_strs:  # L80: Glossar, Modale und andere JS-Texte ohne Bindung
            for sent in re.split(r"(?<=[.;!?])\s", norm_txt(js)):
                if re.search(ALLEIN, sent, re.I):  # in JS-Texten gibt es keine Bindung an einen Fakt → nie zulässig
                    l06b.append(f"JS: {sent.strip()[:40]}…")
        texts06 = [(x["sec"], x["text"], x["src"]) for x in t.texts if not x.get("code") and x["sec"] != "s-qa"]
        texts06 += [("KS", r, "FACT") for r in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else [])]
        for sec, txt, src in texts06:
            for sent in re.split(r"(?<=[.;!?])\s", txt):
                if re.search(ALLEIN, sent, re.I) and not (src and (re.search(r"Vergleichsfeld|bestimmbar|n\. v\.", sent) or set(src.split()) & uniq_ok)):  # L80/L82
                    l06b.append(f"{sec}: {sent.strip()[:40]}…")
        body06 = re.sub(r'<section id="s-qa".*?</section>', " ", body_wo, flags=re.S)
        for m in list(re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', body06))[::-1]:
            if set(m.group(2).split()) & uniq_ok:
                body06 = body06[:m.end()] + re.sub(ALLEIN, "§claim§", element_inner(body06, m), flags=re.I) + body06[m.end() + len(element_inner(body06, m)):]
        for sent in sentences(body06):  # L80: seitenweit satzweise (nicht nur Textknoten)
            if re.search(ALLEIN, sent, re.I) and not re.search(r"vergleichsfeld|bestimmbar|n\. v\.", sent):
                l06b.append(f"Seite: {sent[:40]}…")
        report("L06b Alleinstellung mit Basis", BLOCKER, not l06b, "; ".join(l06b[:3]) if l06b else "Alleinstellungsaussagen mit Vergleichsbasis im selben Satz")
        # L60 · Eigenständigkeit: keine Verweise auf andere Module oder frühere Fassungen
        own = f"M{mod.group(1)}"
        dtxt = json.dumps({k: v for k, v in dbom.items() if k != "audit_trail"}, ensure_ascii=False)
        l60 = []
        prm = sorted((page.parent / "prompts").glob(f"m{mod.group(1)}-*.md")) if (page.parent / "prompts").exists() else []
        ptxt = prm[0].read_text(encoding="utf-8") if prm else ""
        ver = dbom["module"]["version"]
        HIST = (r"Vormodul\w*|Vorversion\w*|Vorgänger\w*|Schwestermodul\w*|Begleitmodul\w*|Erstfassung\w*|Ursprungsfassung\w*|Vorfassung\w*"
                r"|(?:frühere|vorige|vorherige|letzte|bisherige|alte|ältere)[nrs]? (?:Fassung|Version|Modul|Release|Ausgabe)\w*"
                r"|(?:gegenüber|im Vergleich zu[rm]?|seit) (?:der |dem )?(?:Version |Release |Fassung |v)\s?\d[\d.]*|\bRelease \d|Fortsetzung von|Nachfolger\w*")  # L80
        for name, txt in (("Seite", re.sub(r"<(style)\b.*?</\1>", "", html, flags=re.S)), ("Analyse", md), ("DBOM", dtxt), ("Prompt", ptxt)):  # L68: JS eingeschlossen
            l60 += [f"{name}: {x}" for x in sorted(set(re.sub(r"[\s-]", "", y) for y in re.findall(r"\bM[\s-]?\d{3}\b", txt)) - {own})]  # L80: „M-299“
            l60 += [f"{name}: {x}" for x in sorted(set(re.findall(r"\bModul\s\d{3}\b|\bm\d{3}\b", txt)) - {f"Modul {mod.group(1)}", f"m{mod.group(1)}"})]  # L80
            l60 += [f"{name}: Link {x}" for x in sorted(set(re.findall(r'href=["\'](?:\./)?([\w./-]+\.html)', txt)) - {page.name, "impressum.html", "datenschutz.html", "index.html"})]  # L80: jede andere lokale Seite
            if name != "Prompt":  # der Prompt formuliert die Regel selbst („keine früheren Fassungen“)
                vcl = set(re.findall(r"\b\d+\.\d+\.\d+\b", " ".join(f["claim"] for f in F)))  # Herstellerversionen aus Claims
                l60 += [f"{name}: „{x}“" for x in re.findall(HIST, txt, re.I) if not set(re.findall(r"\d+\.\d+\.\d+", x)) & vcl]
                pver = set(re.findall(r"Prompt-Version:\*\* (\d+\.\d+\.\d+)", ptxt))
                vcl = set(re.findall(r"\b\d+\.\d+\.\d+\b", " ".join(f["claim"] for f in F)))  # Herstellerversionen aus Claims
                l60 += [f"{name}: Version {x}" for x in sorted(set(re.findall(r"\b(?:v|Version |Release )(\d+(?:\.\d+){1,2})\b", txt)) - {ver} - pver - vcl)]  # L80: fremde Versionsnummern
        # L68b · Gate-Tooltips und Offen-Liste beschreiben den Zielzustand, nicht den Bearbeitungsverlauf
        qa_sec = re.search(r'<section id="s-qa".*?</section>', html, re.S)
        qa_txt = " ".join(re.findall(r'title="([^"]*)"', qa_sec.group(0)) + re.findall(r"<li[^>]*data-open[^>]*>(.*?)</li>", qa_sec.group(0), re.S)) if qa_sec else ""
        l60 += [f"QA: „{x}“" for x in re.findall(r"\b(?:entfernt|angeglichen|überarbeitete?[nm]?|korrigiert|bereinigt|gestrichen|nach dem Review|nach der Zweitprüfung|in der Zweitprüfung geändert|neu gefasst|ergänzt|nachgetragen|aktualisiert|geändert|ersetzt)\b", qa_txt, re.I)]
        report("L60 Eigenständigkeit", BLOCKER, not l60, "; ".join(l60[:4]) if l60 else "keine Verweise auf andere Module oder frühere Fassungen")
        # L65 · K-Bereiche und K-Verweise passen zur Zahl der K-Zeilen (Seite, Analyse, Prompt)
        nk = len(kres)
        l65 = []
        ncl = len(dbom.get("source_claims", []))
        ZW = {w: i for i, w in enumerate("null eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf dreizehn vierzehn fünfzehn sechzehn siebzehn achtzehn neunzehn zwanzig".split())}
        ZW.update({"ein": 1, "eine": 1})
        for name, txt in (("Seite", re.sub(r"<(style)\b.*?</\1>", "", html, flags=re.S)), ("Analyse", md), ("Prompt", ptxt), ("DBOM", dtxt)):  # L80: auch DBOM-Freitext
            tn = re.sub(r"(?i)(?<!strike )\bK(?:\s|&nbsp;|&#160;|-)(?=\d)", "K", __import__("html").unescape(txt).replace("—", "–").replace("‑", "-")).upper()  # Attribute bleiben erhalten; „Strike K 50“ ist kein K-Verweis  # L80: „K 10“, Geviertstrich
            l65 += [f"{name}: K1–K{n}" for n in re.findall(r"\bK1\s?[–-]\s?K?(\d+)|\bK1 BIS K?(\d+)", tn) for n in [n[0] or n[1]] if int(n) != nk]  # L80: „K1–10“
            l65 += [f"{name}: K{n}" for n in set(re.findall(r"\bK(\d{1,2})\b", tn)) if int(n) > nk]
            l65 += [f"{name}: A01–A{n}" for n in re.findall(r"\bA0?1\s?[–-]\s?A?(\d+)", tn) if int(n) != ncl]  # L65b/L80: „A1–A20“
            l65 += [f"{name}: A{n}" for n in set(re.findall(r"\bA(\d{2})\b|\bCLAIM A(\d+)\b", tn)) for n in [n[0] or n[1]] if int(n) > ncl]  # L80: Einzelverweise
            l65 += [f"{name}: „{x} {w}“" for x, w in re.findall(r"\b(\d+) (kernaussagen|k-punkte|prüfpunkte des ausgangstexts)", norm_txt(txt)) if int(x) != nk]  # L80: Ziffer
            l65 += [f"{name}: „{w} {x}“" for w, x in re.findall(r"\b([a-zäöüß]+) (kernaussagen|k-punkte|prüfpunkte des ausgangstexts)", norm_txt(txt)) if w in ZW and ZW[w] != nk]  # L80: Zahlwörter
        if prm:
            pdefs = re.findall(r"^K(\d+)\s{1,2}[A-ZÄÖÜ]", prm[0].read_text(encoding="utf-8"), re.M)
            if len(pdefs) != nk:
                l65.append(f"Prompt definiert {len(pdefs)} K-Punkte, Seite {nk}")
        report("L65 K-Verweise konsistent", BLOCKER, nk > 0 and not l65, "; ".join(sorted(set(l65))[:4]) if l65 else f"K1–K{nk} überall konsistent")
        # L66 · Datenherkunft nennt nur Stellen, die in den Quellen vorkommen
        dh = re.search(r'Datenherkunft</div><p[^>]*>([^<]*)</p>', html)
        srcs_txt = norm_txt(" ".join(x["title"] + " " + x.get("url", "") for x in dbom["sources"]))
        AUTH = ["BMF", "BFH", "BVerfG", "BaFin", "Eurex", "Cboe", "CME", "OPRA", "BGBl", "ESMA", "BSW", "DDV", "Deutsche Börse"]
        l66 = [a for a in AUTH if dh and re.search(r"\b" + re.escape(a) + r"\b", dh.group(1)) and norm_txt(a) not in srcs_txt]
        GENERIC = {"gesetzestexte", "herstellerdokumentation", "suchtreffer", "primärquelle", "primärquellen", "volltextabruf", "gesperrt", "medien", "medien-",
                   "sekundärquellen", "medienangabe", "gekennzeichnet", "sowie", "überwiegend", "herausgeber", "original", "recherchiert", "bafin-turbo-studie", "medienbericht", "primär-", "herstellerquellen", "medienangaben", "sekundärquelle", "quantor", "herstellerangaben", "die", "der", "das", "und", "sind", "als", "auf", "über"}
        if dh:  # L80: jedes groß geschriebene Wort ist generisch oder kommt in den Quellen vor
            l66 += [w for w in re.findall(r"\b[A-ZÄÖÜ][\wäöüß-]+", dh.group(1)) if w.casefold() not in GENERIC and w.casefold().rstrip("-") not in srcs_txt and w not in l66]
        report("L66 Datenherkunft = Quellen", BLOCKER, bool(dh) and not l66, "nicht in den Quellen: " + ", ".join(l66) if l66 else ("Datenherkunft durch Quellen gedeckt" if dh else "keine Datenherkunft"))
        # L74 · Footer-Datum = letzte Änderung im audit_trail; Schweregrade im Prompt = K-Tabelle
        last = max((e["date"] for e in dbom.get("audit_trail", [])), default="")
        fd = re.findall(r"M%s · v[\d.]+ · (\d{4}-\d{2}-\d{2})" % mod.group(1), html)
        l74 = [f"Footer {x} ≠ {last}" for x in fd if x != last]
        if prm:
            SEVM = {"crit": "KRITISCH", "major": "WESENTLICH", "hint": "HINWEIS"}
            ksev = {json.loads(r)[0]: SEVM.get(json.loads(r)[4]) for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else [])}
            for kk, sev in re.findall(r"^\|\s*\**(K\d+(?:\s?/\s?K\d+)*)\**\s*\|.*\|\s*[*_]*(KRITISCH|WESENTLICH|HINWEIS)[*_]*\s*\|\s*$", ptxt, re.M):  # L80: Markup, alle K
                for ks_ in re.findall(r"K\d+", kk):
                    if ksev.get(ks_) and ksev[ks_] != sev:
                        l74.append(f"Prompt {ks_} {sev} ≠ Seite {ksev[ks_]}")
            pg = re.search(r"\*\*Geändert:\*\* (\d{4}-\d{2}-\d{2})", ptxt)
            if pg and pg.group(1) != last:
                l74.append(f"Prompt geändert {pg.group(1)} ≠ {last}")  # L80
        report("L74 Datum und Schweregrade synchron", BLOCKER, bool(fd) and not l74, "; ".join(l74[:3]) if l74 else f"Footer {last}, Schweregrade = K-Tabelle")
        # L75 · jede nicht bestätigte Angabe (außer Szenario) ist bewusst behalten: keep_reason
        l75 = [f["id"] for f in F if f["verdict"] in ("UNVERIFIED", "MEDIA_REPORT")
               and not (len(f.get("keep_reason", "").strip()) >= 25 and re.search(r"\b(?:K\d+|Modul \d|[CQ]\d+|S\d{2}|Fazit)\b", f.get("keep_reason", "")))]  # L80: Begründung mit Bezug
        krows = {json.loads(r)[0]: json.loads(r)[6].split() for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else [])}
        mods = {i + 1: m_.get("facts", []) for i, m_ in enumerate(dbom.get("analysis_modules", []))}
        for f in F:  # L80: genannte K-Zeilen und Module verwenden den Fakt tatsächlich
            kr = f.get("keep_reason", "")
            l75 += [f"{f['id']}: {k} nutzt den Fakt nicht" for k in re.findall(r"\bK\d+\b", kr) if f["id"] not in krows.get(k, [])]
            for grp in re.findall(r"\bModul ((?:\d+/?)+)", kr):
                if not any(f["id"] in mods.get(int(n), []) for n in grp.split("/") if n):
                    l75.append(f"{f['id']}: Modul {grp} nutzt den Fakt nicht")
        report("L75 nicht bestätigte Angaben begründet", BLOCKER, not l75, "ohne tragfähiges keep_reason (≥ 25 Zeichen, Bezug K/Modul/Gate/Fazit): " + ", ".join(l75) if l75 else f"{sum(f['verdict'] in ('UNVERIFIED', 'MEDIA_REPORT') for f in F)} nicht bestätigte Fakten mit Begründung")
        # L76 · Zahlen, Daten und Rechtsfolge-Wörter in gebundenen Elementen stehen im Claim der gebundenen Fakten
        def iso(x):
            return re.sub(r"\b(\d{2})\.(\d{2})\.(\d{4})\b", r"\3-\2-\1", x)
        l76 = []
        for m in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html):
            ids = m.group(2).split()
            if not ids or not set(ids) <= set(facts):
                continue  # JS-Vorlagen (${…}) prüft L27/L27b
            inner = element_inner(html, m)
            inner = re.sub(r'<span\b[^>]*data-dbom-conf[^>]*>.*?</span>|<(script|style)\b.*?</\1>', " ", inner, flags=re.S)
            for n in list(re.finditer(r'<(\w+)\b[^>]*data-source="[^"]+"[^>]*>', inner))[::-1]:  # verschachtelt gebundene Elemente prüft ihr eigener Durchlauf
                inner = inner[:n.start()] + " " + inner[n.end() + len(element_inner(inner, n)):]
            txt = iso(__import__("html").unescape(re.sub(r"<[^>]+>", " ", inner)))
            txt = re.sub(r"\\\(.*?\\\)", " ", txt)  # Formeln (KaTeX) prüft L63
            if "data-claim=" in m.group(0):
                txt = re.sub(r"„[^“]*“", " ", txt)  # wörtlich zitierte (widerlegte) Ausgangsthese
            if re.fullmatch(r"\W*\d[\d.,]*\W*", txt.strip() or "x"):
                l76.append(f"{ids[0]}: Bindung nur an eine Zahl ohne Kontext")  # L80: Bindungswäsche
            for w, n in ZW.items():  # L80: Zahlwörter im Element wie Ziffern prüfen
                if n > 1:
                    txt = re.sub(r"\b%s\b" % w, str(n), txt, flags=re.I)
            hay = iso(" ".join(str(facts[i].get(k, "")) for i in ids for k in ("claim", "period", "caveat", "values", "basis")))
            for w, n in ZW.items():  # Zahlwörter im Claim („zehn Indikatoren“) zählen als Ziffer
                if n > 1 and re.search(r"\b%s\b" % w, hay, re.I):
                    hay += f" {n} "
            NUM = r"(?<![\w.,/])(?<!\d-)\d+(?:[.,]\d+)*(?:-\d{2}-\d{2})?(?![\w])"
            hay_n = set(re.findall(NUM, hay))
            for num in re.findall(NUM, re.sub(r"S&P 500|Nasdaq-100|EURO STOXX 50|DAX 40|E-mini-S&P-500", " ", txt)):
                if num not in hay_n:
                    l76.append(f"{ids[0]}: {num}")
            for num, unit in re.findall(r"(?<![\w.,])(\d+(?:[.,]\d+)*)\s?(Mio\.|Mrd\.|€|Euro|EUR|USD|%)", txt):  # L80: Betrag nur mit derselben Einheit im Claim
                if not re.search(r"(?<![\d.,])%s\s?%s" % (re.escape(num), re.escape(unit)), hay):
                    l76.append(f"{ids[0]}: {num} {unit}")
            LEGAL = r"grenze|betrag|begrenz|beschränk|höchst|unbegrenzt|unbeschränkt|rücktrag|vortrag|ausgeschlossen|bußgeld|geldbuße|sanktion|strafbar"
            for w in re.findall(r"\w*(?:%s)\w*" % LEGAL, txt, re.I):
                core = re.search(r"(?:%s)\w*" % LEGAL, w.lower()).group(0)  # lower statt casefold: „ß“ bleibt erhalten
                if w.lower() not in hay.lower() and not (core in hay.lower() and len(w) - len(core) <= 8 and not re.search(r"höchst|verlust", w.lower()[:len(w) - len(core)])):
                    l76.append(f"{ids[0]}: „{w}“")  # L80: ganzes Wort, kein Präfix-Trick
            for para in re.findall(r"§\s?\d+[a-z]\b", txt):
                if re.sub(r"\s", "", para) not in re.sub(r"\s", "", hay):
                    l76.append(f"{ids[0]}: {para}")  # L80: § 15b
        for m in re.finditer(r'\{f:\[([^\]]*)\],t:"((?:[^"\\]|\\.)*)",b:"((?:[^"\\]|\\.)*)"', html):  # L80: JS-Modale
            ids = re.findall(r"FACT_[A-Z0-9_]+", m.group(1))
            hay = iso(" ".join(str(facts[i].get(k, "")) for i in ids if i in facts for k in ("claim", "period", "caveat", "values")))
            for d_ in re.findall(r"\d{4}-\d{2}-\d{2}", iso(m.group(2) + " " + m.group(3))):
                if d_ not in hay:
                    l76.append(f"Modal {ids[0] if ids else '?'}: {d_}")
        # L76b · Claims verweisen nicht auf die Seite; Matrixzellen nur mit Zahlen aus dem Claim-Abschnitt ihres Anbieters
        l76 += [f"{f['id']}: Claim verweist auf die Seite" for f in F if re.search(r"(?i)matrix\b|\btabelle\b|modulseite|dieser seite", f["claim"])]
        for tb in re.finditer(r'<table\b[^>]*data-source="([^"]+)"[^>]*>(.*?)</table>', html, re.S):
            hdr = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th\b[^>]*>(.*?)</th>", tb.group(2), re.S)]
            segs = {h: " ".join(seg for i in tb.group(1).split() if i in facts for seg in facts[i]["claim"].split(";") if h and h.split()[0] in seg) for h in hdr}
            for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", tb.group(2), re.S):  # L18b: auch Zeilen mit Attributen
                for j, cell in enumerate(re.findall(r"<td\b([^>]*)>(.*?)</td>", row, re.S)):
                    if j and j < len(hdr) and "data-source" not in cell[0] and segs.get(hdr[j]):  # L82/L76c: auch Textzellen
                        ct = re.sub(r"n\. v\.|[✓–/+;,()]", " ", __import__("html").unescape(re.sub(r"<[^>]+>", " ", cell[1])))
                        for w in re.findall(r"[A-Za-zÄÖÜäöüß][\wÄÖÜäöüß-]{2,}", ct):
                            if w.casefold() not in segs[hdr[j]].casefold() and w.casefold() not in ("und", "nur", "via", "inkl") \
                                    and not (w.casefold() == "nein" and re.search(r"\bkeine?\b", segs[hdr[j]], re.I)):  # „nein“ = „keine …“ im Claim
                                l76.append(f"Matrix {hdr[j]}: „{w}“ nicht im Claim-Abschnitt des Anbieters")
                        for num in re.findall(r"(?<![\w.,])\d+(?:[.,]\d+)*(?![\w])", re.sub(r"<[^>]+>", " ", cell[1])):
                            if num not in re.findall(r"(?<![\w.,])\d+(?:[.,]\d+)*(?![\w])", segs[hdr[j]]):
                                l76.append(f"Matrix {hdr[j]}: {num} nicht im Claim-Abschnitt des Anbieters")
        report("L76 gebundene Angaben ∈ Claim", BLOCKER, not l76, "nicht im Claim: " + "; ".join(sorted(set(l76))[:40]) if l76 else "Zahlen, Daten und Rechtsfolgen gebundener Elemente stehen im Claim")
        # L77 · Fakt-IDs in DBOM-Freitexten und Analyse existieren
        l77 = sorted({x for x in re.findall(r"\bFACT_[A-Z0-9_]+\b", json.dumps({k: v for k, v in dbom.items() if k != "audit_trail"}, ensure_ascii=False) + " " + md + " " + html + " " + ptxt) if x not in facts})  # audit_trail ist Verlauf; L80: auch Seite und Prompt
        report("L77 Fakt-IDs existieren", BLOCKER, not l77, "unbekannt: " + ", ".join(l77[:6]) if l77 else "alle genannten Fakt-IDs existieren")
        # L78 · Bezugszeitraum ≤ Stichtag; späterer Abruf ausdrücklich; Abrufzeitraum umfasst den spätesten Abruf
        st = dbom["module"].get("stichtag", "")
        l78, abruf = [], []
        for f in F:
            for m in re.finditer(r"\d{4}-\d{2}-\d{2}", iso(f.get("period", ""))):
                if re.search(r"\b(?:abgerufen|abruf)\b", iso(f["period"])[max(0, m.start() - 25):m.start()], re.I):  # L80: „abrufbar“ zählt nicht
                    abruf.append(m.group(0))
                elif st and m.group(0) > st:
                    l78.append(f"{f['id']}: Bezugszeitraum {m.group(0)} nach Stichtag {st}")
            if st and not re.search(r"\b(?:abgerufen|abruf)\b", f.get("period", ""), re.I):  # L80: Jahreszahlen im Bezugszeitraum
                l78 += [f"{f['id']}: Bezugsjahr {y} nach Stichtag" for y in re.findall(r"(?<![\d-])(20\d{2})(?![\d-])", f.get("period", "")) if y > st[:4]]
            for d_ in re.findall(r"\d{4}-\d{2}-\d{2}", iso(f["claim"])):  # L80: Daten im Claim
                if st and d_ > st:
                    l78.append(f"{f['id']}: Claim-Datum {d_} nach Stichtag {st}")
        late = max(abruf, default=st)
        for name, txt in (("DBOM", dbom.get("honest_disclosure", "")), ("Analyse", md)):
            for m in re.finditer(r"(?:abgerufen|recherche)\D{0,40}?\d{4}-\d{2}-\d{2}\s?(?:bis|–|-)\s?(\d{4}-\d{2}-\d{2})", iso(txt), re.I):  # L80: auch Gedankenstrich
                if m.group(1) < late:
                    l78.append(f"{name}: Abruf bis {m.group(1)} < {late}")
        report("L78 Stichtag und Abruf", BLOCKER, not l78, "; ".join(l78[:4]) if l78 else f"Bezugszeiträume ≤ {st}; Abruf bis {late} ausgewiesen")
        # L79 · nur an Herstellerangaben gebundene Elemente tragen das VENDOR-Kennzeichen
        vend = {f["id"] for f in F if f["class"] == "VENDOR_CLAIM"}
        l79 = []
        for m in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html):
            ids = set(m.group(2).split())
            if ids and ids <= vend and not re.search(r">\s*VENDOR\s*<", visible_part(element_inner(html, m))):  # L80/L82: Kommentar/unsichtbar zählt nicht
                l79.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", element_inner(html, m))).strip()[:30])
        report("L79 VENDOR-Kennzeichen", BLOCKER, not l79, "ohne VENDOR: " + "; ".join(l79[:4]) if l79 else "alle Herstellerangaben gekennzeichnet")
        # L26c · Offen-Punkte zu Kontraktdaten binden die betroffenen Fakten; diese nennen den offenen Abgleich im caveat
        l26c = []
        syms = {y for f in F for y in f.get("values", {})}
        for li in re.findall(r"<li\b[^>]*data-open[^>]*>.*?</li>", html, re.S):
            t26 = re.sub(r"<[^>]+>", " ", li)
            if re.search(r"multiplikator|kontraktdaten|kontraktwert|kontraktgröße|spezifikation|verfallstermin|\b(?:%s)\b" % "|".join(map(re.escape, syms or {"§§"})), t26, re.I):  # L80
                ids = (re.search(r'data-source="([^"]*)"', li) or [None, ""])[1].split()
                if not ids:  # gebunden greift L26: ein Fakt mit eigenem Offen-Punkt ist nicht CONFIRMED
                    l26c.append("Offen-Punkt nennt Kontraktdaten ohne data-source: " + t26.strip()[:40])
        # L19b · Quellenstufe „vendor“ nur für Hersteller des beschriebenen Produkts, nie als Beleg für Rechts- oder Marktstruktur
        stier = {x["id"]: x.get("tier") for x in dbom["sources"]}
        l19b = sorted({f"{f['id']} ← {sid}" for f in F if f["class"] == "REGULATORY_FRAMEWORK" for sid in [f["source_id"]] + f.get("supporting_sources", []) if stier.get(sid) == "vendor"})
        report("L19b Quellenstufe vendor", BLOCKER, not l19b, "vendor-Quelle stützt Rechtsrahmen: " + ", ".join(l19b[:4]) if l19b else "keine vendor-Quelle als Beleg für den Rechtsrahmen")
        # L26d · ein Fakt, dessen caveat oder keep_reason einen offenen Abgleich nennt, ist nicht CONFIRMED
        l26d = [f["id"] for f in F if f["verdict"] == "CONFIRMED" and re.search(r"\boffen\b|gegenlesen|offen-punkt|zu prüfen|ungeprüft|nicht geprüft|noch prüfen|steht aus|ausstehend|unsicher|unklar|zweifel|vorläufig|zu verifizieren|noch nicht|pending|to be (?:verified|checked)|unverified|tbd\b", f.get("caveat", "") + " " + f.get("keep_reason", ""), re.I)]
        report("L26d CONFIRMED ohne offenen Abgleich", BLOCKER, not l26d, "CONFIRMED trotz offenem Abgleich im caveat: " + ", ".join(l26d) if l26d else "kein CONFIRMED-Fakt nennt einen offenen Abgleich")
        # L82 · Belegstufe je Fakt: evidence ∈ {snippet, fulltext, secondary, derived, model}; SCENARIO ⇔ model; Snippet-Belege halten C3/Q2/Q4/Q5 auf ◐
        l82 = [f"{f['id']}: evidence „{f.get('evidence')}“" for f in F if f.get("evidence") not in ("snippet", "fulltext", "secondary", "derived", "model")]
        l82 += [f"{f['id']}: SCENARIO ⇔ model verletzt" for f in F if (f["verdict"] == "SCENARIO_PROJECTION") != (f.get("evidence") == "model")]
        if any(f["verdict"] == "CONFIRMED" and f.get("evidence") == "snippet" for f in F):
            gates = {g: c for c, g in re.findall(r'<td class="check-(\w+)"[^>]*data-gate="(\w+)"', html)}
            l82 += [f"Gate {g} ✓ trotz Snippet-Belegen" for g in ("C3", "Q2", "Q4", "Q5") if gates.get(g) == "pass"]
            l82 += [] if 'data-dbom-count="snippet"' in html else ["Seite zeigt die Zahl der Snippet-Belege nicht"]
            l82 += [] if re.search(r"evidence", dbom.get("honest_disclosure", "")) else ["honest_disclosure ohne Definition der Belegstufe"]
        report("L82 Belegstufe je Fakt", BLOCKER, not l82, "; ".join(l82[:4]) if l82 else "evidence je Fakt gesetzt, Snippet-Belege offen ausgewiesen")
        # L26e · Offen-Punkt, der eine Sektion nennt, bindet deren Fakten (sonst gilt er als faktspezifisch ohne Bindung)
        l26e = [re.sub(r"<[^>]+>", " ", li).strip()[:40] for li in re.findall(r"<li\b[^>]*data-open[^>]*>.*?</li>", html, re.S)
                if re.search(r"\bS\d{2}\b", re.sub(r"<[^>]+>", " ", li)) and "data-source=" not in li.split(">", 1)[0]]
        report("L26e Offen-Punkt mit Sektion gebunden", BLOCKER, not l26e, "ohne data-source: " + "; ".join(l26e[:3]) if l26e else "Offen-Punkte mit Sektionsbezug gebunden")
        # L27d · Glossar-Einträge mit Fakt: Zahlen, Daten und Rechtsfolgen stehen im Claim
        l27d = []
        for r in (re.findall(r'^\s*(\[".*\])\s*,?\s*$', js_gl.group(1), re.M) if js_gl else []):
            g = json.loads(r)
            ids = [i for i in (g[4].split() if len(g) > 4 else []) if i in facts]
            if not ids:
                continue
            gt = iso(re.sub(r"\\\(.*?\\\)|\bS\d{2}\b", " ", " ".join(g[1:4])))
            hay = iso(" ".join(str(facts[i].get(k, "")) for i in ids for k in ("claim", "period", "caveat", "values", "basis")))
            hn = set(re.findall(r"(?<![\w.,/])(?<!\d-)\d+(?:[.,]\d+)*(?:-\d{2}-\d{2})?(?![\w])", hay))
            l27d += [f"{g[0]}: {n}" for n in re.findall(r"(?<![\w.,/])(?<!\d-)\d+(?:[.,]\d+)*(?:-\d{2}-\d{2})?(?![\w])", gt) if n not in hn]
            l27d += [f"{g[0]}: „{w}“" for w in re.findall(r"\w*(?:schuldverschreibung|grenze|beschränk|rücktrag|vortrag|ausgeschlossen|bußgeld|pflicht)\w*", gt, re.I) if w.lower() not in hay.lower()]
        report("L27d Glossar-Fakten im Claim", BLOCKER, not l27d, "nicht im Claim: " + "; ".join(l27d[:4]) if l27d else "Glossar-Angaben mit Fakt stehen im Claim")
        # L27e · kein Verdict-Kennzeichen schwächer als das schwächste Verdict der Fakten im innersten gebundenen Element
        WEAK = {"UNGEPRÜFT": "UNVERIFIED", "MEDIEN": "MEDIA_REPORT", "SCENARIO": "SCENARIO_PROJECTION"}
        l27e = []
        for b in re.finditer(r'<span class="dbom-class-badge">(UNGEPRÜFT|MEDIEN|SCENARIO)</span>', html):
            opened = [o for o in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html[:b.start()]) if b.start() < o.end() + len(element_inner(html, o))]
            if opened:
                ids = [i for i in opened[-1].group(2).split() if i in facts]
                if ids and not any(facts[i]["verdict"] == WEAK[b.group(1)] for i in ids):
                    l27e.append(f"{b.group(1)} an {' '.join(ids)}")
        report("L27e Kennzeichen = Verdict", BLOCKER, not l27e, "zu schwaches Kennzeichen: " + "; ".join(l27e[:4]) if l27e else "Kennzeichen entsprechen den Verdicts")
        # L82b · Volltext-Belege ohne Snippet-Reste; ohne Snippet-Belege kein Snippet-Status im Präsens
        l82b = [f"{f['id']}: caveat/keep_reason nennt Snippet" for f in F if f.get("evidence") == "fulltext" and re.search(r"snippet|suchtreffer", f.get("caveat", "") + " " + f.get("keep_reason", ""), re.I)]
        if not any(f.get("evidence") == "snippet" for f in F):
            for name, txt in (("honest_disclosure", dbom.get("honest_disclosure", "")), ("Analyse", md), ("Seite", re.sub(r"<[^>]+>", " ", html))):
                l82b += [f"{name}: „{x[:40]}“" for x in re.findall(r"[^.]*\b(?:stützen|beruhen|stützt|beruht) sich (?:\S+ ){0,4}auf (?:Suchtreffer|Snippet)[^.]*", txt)]
                l82b += [f"{name}: „{x}“" for x in re.findall(r"(?:steht|stehen) (?:\S+ ){0,4}(?:Snippet|Volltextabgleich)\S*(?: \S+){0,3} aus|Volltextabgleich steht aus", txt)]
        report("L82b Belegstufe ohne Reste", BLOCKER, not l82b, "; ".join(l82b[:4]) if l82b else "keine Snippet-Reste bei Volltext-Belegen")
        # L76d · Einschränkungen (qualifier) des Fakts erscheinen in jedem gebundenen Element, das den Gegenstand nennt
        l76d = []
        for m in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html):
            txt = re.sub(r"<[^>]+>", " ", element_inner(html, m))
            for i in m.group(2).split():
                q = facts.get(i, {}).get("qualifier")
                if q and re.search(q["subject"], txt) and not any(re.search(t_, txt, re.I) for t_ in q["terms"]):
                    l76d.append(f"{i}: „{q['subject']}“ ohne {'/'.join(q['terms'])}")
        for r in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else []):
            row = json.loads(r)
            for i in row[6].split():
                q = facts.get(i, {}).get("qualifier")
                if q and re.search(q["subject"], row[5]) and not any(re.search(t_, row[5], re.I) for t_ in q["terms"]):
                    l76d.append(f"{row[0]}/{i}: ohne {'/'.join(q['terms'])}")
        report("L76d Einschränkungen sichtbar", BLOCKER, not l76d, "; ".join(sorted(set(l76d))[:4]) if l76d else "Einschränkungen (Beta, Erprobung …) überall genannt")
        # L84 · jede Marke aus dem Inventar, die auf Seite, in Tooltips oder Quelltiteln vorkommt, steht im Markenhinweis
        marks = json.loads((Path(__file__).parent / "fachbegriffe.json").read_text(encoding="utf-8")).get("marks", [])
        notice = re.search(r"<strong>Marken:</strong>(.*?)</p>", html, re.S)
        corpus = html + " " + json.dumps(dbom, ensure_ascii=False)
        l84 = [mk for mk in marks if re.search(r"(?<![\w-])%s(?![\w])" % re.escape(mk), corpus.replace(notice.group(0), "") if notice else corpus) and not (notice and re.search(r"(?<![\w-])%s(?![\w])" % re.escape(mk), notice.group(1)))]
        report("L84 Markenhinweis vollständig", BLOCKER, bool(notice) and bool(marks) and not l84, "fehlt im Markenhinweis: " + ", ".join(l84[:6]) if l84 else (f"{len(marks)} Inventar-Marken geprüft" if notice else "kein Markenhinweis"))
        # L82c · Freigabeumfang passt zum caveat; Mehrzahl von Berichten nur mit ≥ 2 Quellen
        l82c = []
        for f in F:
            sc = f.get("verified", {}).get("scope", "")
            if re.search(r"\boriginal\b", sc, re.I) and re.search(r"selbst nicht (?:\S+ ){0,3}eingesehen|quelle (?:\S+ ){0,3}nicht eingesehen|nicht im volltext", f.get("caveat", ""), re.I):  # andere Dokumente (z. B. Emissionsbedingungen) zählen nicht
                l82c.append(f"{f['id']}: Umfang „{sc}“ ≠ caveat")
            nsrc = len({f["source_id"], *f.get("supporting_sources", []), *f.get("additional_sources", [])})
            if nsrc < 2 and re.search(r"mehrere[nr]? |übereinstimmend", f.get("caveat", "") + " " + f.get("claim", ""), re.I):
                l82c.append(f"{f['id']}: Mehrzahl mit {nsrc} Quelle")
        for m in re.finditer(r'\{f:\[([^\]]*)\],t:"(?:[^"\\]|\\.)*",b:"((?:[^"\\]|\\.)*)"', html):
            ids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", m.group(1)) if i in facts]
            media = [i for i in ids if facts[i]["verdict"] == "MEDIA_REPORT"] or ids  # die Mehrzahl muss der Medienfakt selbst tragen
            nmin = min((len({facts[i]["source_id"], *facts[i].get("supporting_sources", [])}) for i in media), default=0)
            if nmin < 2 and re.search(r"übereinstimmend|mehreren (?:Medien)?bericht", m.group(2), re.I):
                l82c.append(f"Modal {ids[0] if ids else '?'}: Mehrzahl ohne zweite Quelle")
        report("L82c Freigabeumfang = caveat", BLOCKER, not l82c, "; ".join(l82c[:4]) if l82c else "Freigabeumfang und Quellenzahl stimmen mit den caveats überein")
        # L76e · ein Claim mit Beta/Erprobung/in Entwicklung trägt einen qualifier
        l76e = [f["id"] for f in F if re.search(r"\bBeta\b|Erprobung|in Entwicklung", f["claim"]) and not f.get("qualifier")]
        report("L76e Einschränkung als qualifier", BLOCKER, not l76e, "ohne qualifier: " + ", ".join(l76e) if l76e else "alle Einschränkungen als qualifier geführt")
        # L85 · Vergleichstabelle: gleiche Quellenstufe ⇒ gleiches Verdict (Neutralität, C4)
        stier = {x["id"]: x.get("tier") for x in dbom["sources"]}
        l85 = []
        for tb in re.finditer(r'<table\b[^>]*data-source="([^"]+)"', html):
            ids = [i for i in tb.group(1).split() if i in facts]
            byt = {}
            for i in ids:
                byt.setdefault(stier.get(facts[i]["source_id"]), set()).add(facts[i]["verdict"])
            l85 += [f"Stufe {t_}: {', '.join(sorted(v))}" for t_, v in byt.items() if len(v) > 1]
        report("L85 Vergleich mit gleichen Maßstäben", BLOCKER, not l85, "; ".join(l85[:3]) if l85 else "gleiche Quellenstufe, gleiches Verdict in Vergleichstabellen")
        # L19c · Rechtsrahmen-Fakten stützen sich auf eine Primärquelle (Sekundärquellen nur ergänzend)
        l19c = [f["id"] for f in F if f["class"] == "REGULATORY_FRAMEWORK" and stier.get(f["source_id"]) != "primary"]
        report("L19c Recht mit Primärquelle", BLOCKER, not l19c, "Hauptquelle nicht primär: " + ", ".join(l19c) if l19c else "Rechtsrahmen-Fakten mit Primärquelle")
        # L27f · pauschales Verdict-Wort im Text nur, wenn alle gebundenen Fakten dieses Verdict tragen (sonst je Fakt nennen)
        VW = {"Medienangaben": "MEDIA_REPORT", "ungeprüft": "UNVERIFIED"}
        l27f = []
        rows27 = [(r[0], r[5], r[6]) for r in (json.loads(x) for x in (re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', js_ks.group(1), re.M) if js_ks else []))]
        rows27 += [(g[0], " ".join(g[1:4]), g[4] if len(g) > 4 else "") for g in (json.loads(x) for x in (re.findall(r'^\s*(\[".*\])\s*,?\s*$', js_gl.group(1), re.M) if js_gl else []))]
        for name, txt, ids_ in rows27:
            ids = [i for i in ids_.split() if i in facts]
            for w, vd in VW.items():
                for m in re.finditer(r"(?<!: )\b%s\b" % w, txt):
                    if ids and any(facts[i]["verdict"] != vd for i in ids):
                        l27f.append(f"{name}: „{w}“, aber {', '.join(i for i in ids if facts[i]['verdict'] != vd)[:60]} nicht {vd}")
        report("L27f Verdict-Wörter = Verdicts", BLOCKER, not l27f, "; ".join(l27f[:3]) if l27f else "pauschale Verdict-Wörter nur bei einheitlichem Verdict")
        # L86 · Szenarien ohne Prognose-Konfidenz: confidence null, keine Spanne, kein Pill, Live-Audit ohne Wert
        l86 = [f"{f['id']}: confidence {f['confidence']}" for f in F if f["verdict"] == "SCENARIO_PROJECTION" and f.get("confidence") is not None]
        scen_only = {f["class"] for f in F} - {f["class"] for f in F if f["verdict"] != "SCENARIO_PROJECTION"}
        l86 += [f"Spanne {c}" for c in re.findall(r'data-dbom-range="(\w+)"', html) if c in scen_only]
        l86 += [f"Pill {i}" for i in re.findall(r'data-dbom-conf="(\w+)"', html) if i in facts and facts[i]["verdict"] == "SCENARIO_PROJECTION"]
        if "info.confidence!=null" not in html.replace(" ", ""):
            l86.append("Live-Audit zeigt Konfidenz ohne Prüfung auf null")
        report("L86 Szenarien ohne Konfidenz", BLOCKER, not l86, "; ".join(l86[:4]) if l86 else "Szenarien ohne Prognose-Konfidenz in DBOM und Anzeige")
        # L85b · L85 über alle Bindungen einer Vergleichstabelle (Tabelle, Zeilen, Zellen); Quantor-Fakten mit Basis ausgenommen
        l85b = []
        for tb in re.finditer(r'<table\b[^>]*data-source="([^"]+)"[^>]*>(.*?)</table>', html, re.S):
            ids = set(tb.group(1).split()) | {i for grp in re.findall(r'data-source="([^"]+)"', tb.group(2)) for i in grp.split()}
            byt = {}
            for i in ids:
                if i in facts and not facts[i].get("basis"):
                    byt.setdefault(stier.get(facts[i]["source_id"]), {}).setdefault(facts[i]["verdict"], []).append(i)
            l85b += [f"Stufe {t_}: " + "; ".join(f"{v}: {', '.join(sorted(x))[:50]}" for v, x in vs.items()) for t_, vs in byt.items() if len(vs) > 1]
        report("L85b Vergleich über alle Bindungen", BLOCKER, not l85b, "; ".join(l85b[:2]) if l85b else "alle Bindungen der Vergleichstabellen mit gleichen Maßstäben")
        # L27g · Kennzeichen je Gegenstand (gehärtet nach der 18. Zweitprüfung): Kennzeichen und Verdict-Wörter
        # MEDIEN/UNGEPRÜFT stehen in der Teilaussage (seit Satz-/Teilsatzbeginn bzw. vorigem Kennzeichen) des Fakts mit
        # diesem Verdict und nennen keinen Gegenstand anderen Verdicts; jede Teilaussage über einen Medien-Fakt trägt
        # ihr Kennzeichen (außer n. v.); ein Kennzeichen ohne eigene Aussage ist unzulässig. Attribute am span zählen nicht.
        class _BM:  # Kennzeichen als beliebiges Element (span, em, …), Text ohne inneres Markup, &nbsp;/&shy; aufgelöst
            def __init__(s_, m_, t_):
                s_.m, s_.t = m_, t_
            def start(s_):
                return s_.m.start()
            def end(s_):
                return s_.m.end()
            def group(s_, k=0):
                return s_.t if k else s_.m.group(0)

        class _BadgeRx:
            def __init__(s_, cls):
                s_.rx = re.compile(r'<(\w+)\b[^>]*\bclass="[^"]*\b(?:%s)\b[^"]*"[^>]*>(.*?)</\1>' % cls, re.S)
            def finditer(s_, src):
                out = []
                for m_ in s_.rx.finditer(src):
                    t_ = __import__("html").unescape(re.sub(r"<[^>]+>", "", m_.group(2))).replace("\xad", "").replace("\xa0", " ").strip()
                    if re.fullmatch(r"[A-ZÄÖÜ]+", t_):
                        out.append(_BM(m_, t_))
                return out
            def findall(s_, src):
                return [b.group(1) for b in s_.finditer(src)]
            def search(s_, src):
                return s_.finditer(src)
            def sub(s_, rep_, src):
                return s_.rx.sub(rep_, src)

        BADGE = _BadgeRx(r"dbom-class-badge|badge b-\w+")
        VB = {"MEDIEN": "MEDIA_REPORT", "UNGEPRÜFT": "UNVERIFIED"}
        VW = {"medienangabe": "MEDIA_REPORT", "medienangaben": "MEDIA_REPORT", "ungeprüft": "UNVERIFIED"}
        SENT = re.compile(r"(?<=[.;:!?])\s+(?=[A-ZÄÖÜ„(])|;\s*|\s*[¶·]\s*")

        def _names(claim):
            toks = {t.strip("–,:;.()„“") for t in claim.split()}
            parts = {p_ for t in toks for p_ in [t] + re.split(r"[-/]", t)}
            return {claim.split()[0].strip("–,:")} | {p_ for p_ in parts if len(re.findall(r"[A-ZÄÖÜ]", p_)) >= 2}

        def _txt(x):  # Zellen-, Absatz- und Zeilengrenzen trennen Teilaussagen (¶)
            x = re.sub(r"</(?:td|th|li|p|caption|h[1-6])>|<br\s*/?>", " ¶ ", x)
            x = re.sub(r"\s+", " ", __import__("html").unescape(re.sub(r"<[^>]+>", " ", x))).replace("n. v.", "n.v.")
            x = re.sub(r"\([^()]*\)", lambda k: k.group(0).replace(";", ","), x)  # „;“ in Klammern trennt nicht
            i_ = x.rfind("(")
            return x[:i_] + x[i_:].replace(";", ",") if i_ > x.rfind(")") else x  # auch in noch offener Klammer

        DS = re.compile(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>')
        l27g = []

        def _bound0(pos, src=None):
            src = src if src is not None else vh
            return [i for m_ in DS.finditer(src[:pos]) if m_.end() + len(element_inner(src, m_)) > pos for i in m_.group(2).split() if i in facts]
        for m in DS.finditer(html):
            ids = [i for i in m.group(2).split() if i in facts]
            if not ids:
                continue
            inner = visible_part(element_inner(html, m))
            if BADGE.search(inner) and not re.sub(r"\b(?:%s)\b" % "|".join(BADGE.findall(inner)), "", _txt(BADGE.sub(" ", inner))).strip(" .,;:()"):
                l27g.append(f"{ids[0]}: Kennzeichen ohne Aussage")
            if len({facts[i]["verdict"] for i in ids}) < 2:
                continue
            nested = [(n.start(), n.end() + len(element_inner(inner, n))) for n in DS.finditer(inner)]
            marks = [(b.start(), b.end(), VB.get(b.group(1))) for b in BADGE.finditer(inner)]  # jedes Kennzeichen beendet einen Abschnitt
            marks += [(w.start(), w.end(), VW[w.group(1).lower()]) for w in re.finditer(r"\b(Medienangaben?|ungeprüft)\b", inner, re.I)
                      if not re.search(r"<[^>]*$", inner[:w.start()])]
            prev, lastseg, lastw = 0, "", False
            for a, e, verd in sorted(marks):
                seg = SENT.split(_txt(inner[prev:a]))[-1]
                if not re.sub(r"[\W_]", "", seg) and prev and lastw:
                    seg = lastseg  # Kennzeichen direkt nach Verdict-Wort: gleiche Teilaussage
                lastseg, prev, lastw = seg, e, not inner[a:e].startswith("<")
                if not verd or any(s0 <= a < e0 for s0, e0 in nested):
                    continue
                own = set().union(*[_names(facts[i]["claim"]) for i in ids if facts[i]["verdict"] == verd])
                oth = set().union(*[_names(facts[i]["claim"]) for i in ids if facts[i]["verdict"] != verd])
                if not any(n in seg for n in own - oth) or any(n in seg for n in oth - own):
                    l27g.append(f"{' '.join(ids)[:40]}: {inner[a:e][-12:]} ohne eindeutigen Bezug („{seg[-30:]}“)")
            if m.group(1) in ("table", "tr", "td", "thead", "tbody"):
                continue
            hb = inner
            for s0, e0 in sorted(nested, reverse=True):
                hb = hb[:s0] + " " + hb[e0:]
            for unit in SENT.split(_txt(hb)):
                for verd, word in (("MEDIA_REPORT", "MEDIEN"), ("UNVERIFIED", "UNGEPRÜFT")):
                    own = set().union(*[_names(facts[i]["claim"]) for i in ids if facts[i]["verdict"] == verd])
                    oth = set().union(*[_names(facts[i]["claim"]) for i in ids if facts[i]["verdict"] != verd])
                    if own and any(n in unit for n in own - oth) and "n.v." not in unit and word not in unit and not re.search(r"(?i)medienangabe|ungeprüft", unit):
                        l27g.append(f"{' '.join(ids)[:40]}: Teilaussage ohne {word} („{unit[:30]}“)")
        # L27g (global) · auch außerhalb gebundener Elemente: ein MEDIEN/UNGEPRÜFT-Kennzeichen oder Verdict-Wort nennt in seiner
        # Teilaussage keinen Anbieter eines belegten Fakts (Claim-Anfang) und kein „Herstellerangabe“, außer ein gebundener
        # Fakt dieses Verdicts nennt ihn selbst.
        owner = {}
        for f_ in F:
            if f_["class"] == "VENDOR_CLAIM" or f_["verdict"] != "CONFIRMED":  # Anbieterangaben
                owner.setdefault(f_["claim"].split()[0].strip("–,:"), set()).add(f_["verdict"])
        vh = visible_part(html)
        vh = re.sub(r"<(script|style|head)\b.*?</\1>", lambda x: " " * len(x.group(0)), vh, flags=re.S | re.I)
        gmarks = [(b.start(), b.end(), VB.get(b.group(1)), "b") for b in BADGE.finditer(vh)]
        gmarks += [(w.start(), w.end(), VW[w.group(1).lower()], "w") for w in re.finditer(r"\b(Medienangaben?|ungeprüft)\b", vh, re.I) if not re.search(r"<[^>]*$", vh[:w.start()])]
        prev = 0
        lastseg, lastkind = "", ""
        for a, e, verd, kind in sorted(gmarks):
            blk_start = max(vh.rfind(t_, 0, a) for t_ in ("<p", "<li", "<td", "<th", "<caption", "<div", "<h"))
            seg = SENT.split(_txt(vh[max(prev, blk_start):a]))[-1]
            if not re.sub(r"[\W_]", "", seg) and prev > blk_start and lastkind == "w":
                seg = lastseg  # Kennzeichen direkt nach Verdict-Wort: gleiche Teilaussage
            lastseg, lastkind, prev = seg, kind, e
            if not verd:
                continue
            allowed = " ".join(facts[i]["claim"] for i in _bound0(a) if facts[i]["verdict"] == verd)
            bad = [n for n, vs in owner.items() if verd not in vs and len(n) > 2 and re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", seg) and n not in allowed]
            if kind == "b" and re.search(r"(?i)herstellerangabe", seg) and verd == "MEDIA_REPORT":
                bad.append("Herstellerangabe")
            if bad:
                l27g.append(f"{verd[:5]}-Kennzeichen über {', '.join(bad[:3])} („{seg[-30:]}“)")
        report("L27g Kennzeichen je Gegenstand", BLOCKER, not l27g, "; ".join(l27g[:3]) if l27g else "Kennzeichen je Teilaussage, keine pauschalen Kennzeichen über gemischten Verdicts")
        # L27h · Legende nennt jedes sichtbar verwendete Kennzeichen als Kennzeichen; Modellannahmen tragen MODELL, nie SCENARIO
        vis_html = visible_part(html)
        leg = re.search(r'data-qa="kennzeichen-legende"[^>]*>(.*?)</p>', vis_html, re.S)  # sichtbare Legende (S12)
        CBADGE = _BadgeRx(r"dbom-class-badge|badge b-v")  # Daten-Kennzeichen, nicht Schweregrade
        used = set(CBADGE.findall(vis_html))
        legb = set(CBADGE.findall(leg.group(1))) if leg else set()
        l27h = [f"Legende ohne {u}" for u in sorted(used - legb - {"RAHMEN", "MARKT"})]
        for m in DS.finditer(html):
            ids = [i for i in m.group(2).split() if i in facts]
            cls = {facts[i]["class"] for i in ids}
            if "MODEL_ASSUMPTION" not in cls:
                continue
            inner = visible_part(element_inner(html, m))
            if cls == {"MODEL_ASSUMPTION"} and "SCENARIO" in BADGE.findall(inner):
                l27h.append(f"{ids[0]}: SCENARIO statt MODELL")
            elif len(cls) > 1:
                prev = 0
                for b in BADGE.finditer(inner):
                    seg = SENT.split(_txt(inner[prev:b.start()]))[-1]
                    prev = b.end()
                    want = {"SCENARIO": "SCENARIO_PROJECTION", "MODELL": "MODEL_ASSUMPTION"}.get(b.group(1))
                    if want and not any(n in seg for n in set().union(*[_names(facts[i]["claim"]) for i in ids if facts[i]["class"] == want])):
                        l27h.append(f"{' '.join(ids)[:40]}: {b.group(1)} ohne Bezug („{seg[-25:]}“)")
        report("L27h Legende und Klassen-Kennzeichen", BLOCKER, bool(leg) and not l27h, "; ".join(l27h[:3]) if l27h else "Legende vollständig, Modellannahmen einheitlich MODELL")
        # L87 · n. v.-Gegenstände (DBOM not_evaluated): jede Einheit (Glossar-Stufe, Tabellenzelle, Modal-Satz, Fließtext-Satz,
        # Analyse-Satz/-Zelle) zum Gegenstand nennt „n. v.“ direkt beim Gegenstand bzw. bei „Ausgestaltung“ oder ist an
        # einen Fakt gebunden, der den Gegenstand nennt und mit dem sie ein Fachwort teilt. Aufzählungen von
        # Produktklassen (Risikohinweis) sind ausgenommen. Groß-/Kleinschreibung egal.
        l87 = []
        ds_spans = [(m.start(), m.end() + len(element_inner(html, m)), m.group(2).split()) for m in DS.finditer(html)]

        def _bound(pos):
            return [i for s0, e0, ids_ in ds_spans if s0 <= pos < e0 for i in ids_ if i in facts]

        for ne in dbom.get("not_evaluated", []):
            SUBJ = re.compile(r"(?i)(?<![\w-])(?:[A-Za-zÄÖÜäöü]+-)?(?:%s)(?![\w-]*studie)[\w-]*" % ne["subject"])  # „Long-Turbo“ ja, „BaFin-Turbo-Studie“ nein
            MARK = re.compile(r"(?i)(?:%s)[\w-]*|ausgestaltung" % ne["subject"])

            def _ok(unit, ids_, about=False):
                u = unit.replace("n. v.", "n.v.")
                hits = list(SUBJ.finditer(u))
                if not hits and not about:
                    return True
                for f_ in ids_:
                    cl = facts[f_]["claim"]
                    if re.search(ne["subject"], cl, re.I):
                        shared = [w for w in re.findall(r"[A-Za-zÄÖÜäöüß][\wÄÖÜäöüß-]{5,}", u) if not SUBJ.fullmatch(w) and w.lower() in cl.lower()]
                        if shared:
                            return True
                if u.strip().startswith("n.v."):
                    return True
                for h in hits:
                    pre = u[max(0, h.start() - 40):h.start()]
                    if re.search(r"(?:\w-?\s*,\s*|\w-?\s+(?:und|oder)\s+|/)$", pre) and re.search(r"(?i)\b(?:optionen|futures|optionsscheine|derivate|hebel-)", u) \
                            and re.search(r"(?i)totalverlust|risiko|mechanik|hebelprodukt|hebelwirkung", u):
                        continue  # Risikohinweis über Produktklassen
                    rest = re.sub(r"^(?:\s*(?:,|und|oder|/)\s*" + SUBJ.pattern[4:] + r")*", "", u[h.end():], flags=re.I)  # „Knock-outs und Turbos: n. v.“
                    if re.search(r"(?i)(?:studie|allgemeinverfügung|bericht|untersuchung)\s+(?:zu|über)\s+(?:den\s+)?$", pre):
                        continue  # Gegenstand nur als Bezug einer Quelle („Studie zu Turbo-Zertifikaten“)
                    if not re.match(r"[\s:,]*(?:(?:ist|sind)\s+(?:die\s+)?(?:\w+\s+){0,3}?)?(?:hier\s+)?(?:n\.v\.|nicht ausgewertet)", rest) and \
                       not re.search(r"(?i)ausgestaltung\s+(?:hier\s+)?(?:n\.v\.|nicht ausgewertet)", u):
                        return False
                if about and not hits:
                    return bool(re.search(r"(?i)ausgestaltung\s+(?:hier\s+)?(?:n\.v\.|nicht ausgewertet)", u))
                return True

            for r in (re.findall(r'^\s*(\[".*\])\s*,?\s*$', js_gl.group(1), re.M) if js_gl else []):
                g = json.loads(r)
                gids = [i for i in (g[4].split() if len(g) > 4 else []) if i in facts]
                for k, stage in enumerate(g[1:4], 1):
                    if not all(_ok(u_, gids, about=bool(SUBJ.search(g[0]))) for u_ in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ„(])", stage.replace("n. v.", "n.v.")) if u_.strip()):
                        l87.append(f"Glossar {g[0]} Stufe {k}")
            for mm in re.finditer(r'\{f:\[([^\]]*)\],t:"((?:[^"\\]|\\.)*)",b:"((?:[^"\\]|\\.)*)"', html):
                mids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", mm.group(1)) if i in facts]
                for unit in SENT.split(mm.group(3)):
                    if not _ok(unit, mids):
                        l87.append(f"Modal {mm.group(2)[:20]}: „{unit[:25]}“")
            hb = re.sub(r"<(script|style|head|th|button)\b.*?</\1>", lambda x: " " * len(x.group(0)), html, flags=re.S | re.I)
            for tb in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, re.S):
                hdr = [_txt(h) for h in re.findall(r"<th\b[^>]*>(.*?)</th>", tb.group(1), re.S)]
                for row in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", tb.group(1), re.S):
                    for j, tdm in enumerate(re.finditer(r"<td\b[^>]*>(.*?)</td>", row.group(1), re.S)):
                        about = j < len(hdr) and bool(SUBJ.search(hdr[j]))
                        if not _ok(_txt(visible_part(tdm.group(1))), _bound(tb.start(1) + row.start(1) + tdm.start()), about=about):
                            l87.append(f"Zelle „{_txt(tdm.group(1))[:30]}“")
            hb = re.sub(r"<table\b.*?</table>", lambda x: " " * len(x.group(0)), hb, flags=re.S)
            for blk in re.finditer(r"<(p|li|div|h[1-6]|span|dd|figcaption|caption)\b[^>]*>((?:(?!<(?:p|li|div|h[1-6]|ul|ol|table)\b).)*?)</\1>", hb, re.S):
                for unit in SENT.split(_txt(visible_part(blk.group(2)))):
                    if SUBJ.search(unit) and not _ok(unit, _bound(blk.start(2))):
                        l87.append(f"Text „{unit[:30]}“")
            if md:
                for line_ in md.splitlines():
                    if line_.startswith("|") and not re.match(r"\|\s*-", line_):
                        cells = [c_.strip() for c_ in line_.strip("|").split("|")]
                        about = bool(SUBJ.search(cells[0])) if cells else False
                        rids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", line_) if i in facts] + \
                               [f_["id"] for f_ in F if f_.get("source_id") in re.findall(r"SRC_[A-Z0-9_]+", line_)]  # Bindung je Zeile
                        for c_ in cells[1:]:
                            if not _ok(c_, rids, about=about):
                                l87.append(f"Analyse-Zelle „{c_[:30]}“")
                for para_ in re.split(r"\n\s*\n", re.sub(r"^\|.*$", "", md, flags=re.M)):
                    para_ = re.sub(r"^>\s?", "", para_, flags=re.M).replace("\n", " ")
                    for unit in SENT.split(para_.replace("n. v.", "n.v.")):
                        if SUBJ.search(unit) and not _ok(unit, re.findall(r"FACT_[A-Z0-9_]+", para_)):
                            l87.append(f"Analyse „{unit[:30]}“")
        report("L87 n. v.-Gegenstände durchgängig", BLOCKER, not l87, "; ".join(list(dict.fromkeys(l87))[:4]) if l87 else "n. v.-Gegenstände in Glossar, Tabellen, Modalen, Fließtext und Analyse durchgängig")
        # L82e · Belegstufe passt zum Prüfumfang: „fulltext“ nur, wenn verified.scope ein Original ohne Einschränkung nennt
        def _exc(f):
            sc = f.get("verified", {}).get("scope", "")
            return bool(f.get("verified")) and ("Original" not in sc or re.search(r"(?i)nicht (?:im volltext )?eingesehen|medienbericht", sc + " " + f.get("caveat", "")))
        exc = [f for f in F if _exc(f) and f["verdict"] != "SCENARIO_PROJECTION" and f.get("evidence") != "derived"]
        l82e = [f"{f['id']}: evidence fulltext bei Prüfumfang „{f['verified'].get('scope', '')[:30]}“" for f in exc if f.get("evidence") == "fulltext"]
        # L82f · Hauptquelle der Stufe secondary ⇒ Belegstufe secondary (nicht fulltext)
        l82e += [f"{f['id']}: Sekundärquelle, aber evidence {f.get('evidence')}" for f in F if stier.get(f["source_id"]) == "secondary" and f.get("evidence") not in ("secondary", "model")]
        # L82d · Ausnahmen im Prüfumfang stehen in jedem Satz, der Vollständigkeit am Original oder auf Stufe Volltext behauptet
        UNIV = re.compile(r"(?i)\b(?:alle|sämtliche|jede[nrs]?|ausnahmslos|vollständig|die)\b[^.;]{0,80}?\b(?:Belege?|Quellen?|Fakten|Fakt|Angaben)\b[^.;]{0,80}?(?:(?:am|im) Original|Volltext|fulltext)"
                          r"|\b(?:sämtlich|vollständig|ausnahmslos|alles)\b[^.;]{0,30}?(?:am|im) Original"
                          r"|(?:(?:am|im) Original|Volltext|fulltext)[^.;]{0,40}?\b(?:alle|sämtliche|jede[nrs]?)\b[^.;]{0,40}?\b(?:Belege?|Quellen?|Fakten)\b")
        l82d = []
        if exc:
            tit = " ".join(re.findall(r'\btitle="([^"]*)"', html))
            for name, txt in (("Seite", _txt(visible_part(html)) + " " + tit), ("Analyse", (md or "").replace("\n> ", " ").replace("\n", " ")), ("honest_disclosure", dbom.get("honest_disclosure", ""))):
                for sent in re.split(r"(?<=[.;])\s", txt.replace("n. v.", "n.v.")):
                    if not UNIV.search(sent):
                        continue
                    for f in exc:
                        nm = f["claim"].split()[0].strip(":,")
                        named = f["id"] in sent or all(p_ in sent for p_ in re.split(r"-", nm) if len(p_) > 2) or \
                            (f["verdict"] == "MEDIA_REPORT" and re.search(r"(?i)medienangabe|sekundärquelle", sent)) or \
                            any(len(p_) > 4 and p_ in sent for p_ in re.split(r"[-:]", nm))  # Name, ID, Kategorie oder Namensteil
                        if not (named and re.search(r"(?i)außer|ausgenommen|ausnahme|bis auf|nur am medienbericht|am medienbericht", sent)) or re.search(r"(?i)\bkeine? ausnahme", sent):
                            l82d.append(f"{name}: „{sent.strip()[:40]}“")
        report("L82d Ausnahmen im Freigabeumfang genannt", BLOCKER, not l82d, "; ".join(l82d[:3]) if l82d else "Ausnahmen des Prüfumfangs in jedem Vollständigkeitssatz genannt")
        report("L82e Belegstufe passt zum Prüfumfang", BLOCKER, not l82e, "; ".join(l82e[:3]) if l82e else f"{len(exc)} Fakt(e) mit eingeschränktem Prüfumfang, keiner mit evidence fulltext")
        vendors = {f_["claim"].split()[0].strip("–,:") for f_ in F if f_["class"] == "VENDOR_CLAIM" or "VENDOR" in f_.get("class", "")} | {"ATAS", "IBKR", "TWS"}

        def _is_cmp(hdr):  # Vergleichstabelle: Kopf „Merkmal/Kriterium“ oder mindestens zwei Anbieter in den Spaltenköpfen
            return bool(hdr) and (hdr[0] in ("Merkmal", "Kriterium") or sum(any(w in vendors for w in h.split()) for h in hdr[1:]) >= 2)

        # L18b · Quantor-Basis aus Anbieterfakten: jeder als bestimmbar gezählte Anbieter hat einen Fakt mit Aussage zum Gegenstand
        l18b = []
        for f in F:
            b_ = f.get("basis")
            if not b_:
                continue
            df = b_.get("determinable_from")
            if df is None:
                l18b.append(f"{f['id']}: basis ohne determinable_from")
                continue
            if len(df) != b_["determinable"] or b_["compared"] != b_["determinable"] + len(b_.get("not_verifiable", [])):
                l18b.append(f"{f['id']}: Basis {b_['compared']}/{b_['determinable']} passt nicht zu {len(df)} bestimmbaren + {len(b_.get('not_verifiable', []))} n. v.")
            for v_, fid in df.items():
                if fid not in facts or not re.search(b_.get("subject", "$^"), facts[fid]["claim"]) or v_ in b_.get("not_verifiable", []):
                    l18b.append(f"{f['id']}: {v_} ohne Aussage zum Gegenstand in {fid}")
            # Text: in Klammern als bestimmbar genannte Anbieter stehen in determinable_from
            keys = " ".join(df)
            for name, txt in (("Seite", _txt(visible_part(html))), ("Analyse", md or "")):
                for lst in re.findall(r"bestimmbar\w*[^().;·]{0,60}\(([^)]*)\)", txt):
                    for v_ in re.split(r",\s*|\s+und\s+", lst):
                        v_ = v_.strip()
                        if v_ and re.match(r"[A-Z]", v_) and not any(w in keys for w in v_.split()):
                            l18b.append(f"{name}: „{v_}“ als bestimmbar genannt, nicht in determinable_from")
            # Sätze mit „bestimmbar“: jeder nicht bestimmbare Anbieter steht in einem Abschnitt mit „n. v.“
            for name, txt in (("Seite", _txt(visible_part(html))), ("Analyse", (md or "").replace("\n", " "))):
                for sent in re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ„])", txt.replace("n. v.", "n.v.")):
                    if "bestimmbar" not in sent:
                        continue
                    for v_ in b_.get("not_verifiable", []):
                        for occ in re.finditer(r"(?<![\w-])" + re.escape(v_) + r"(?![\w-])", sent):
                            chunk = re.split(r"[–;¶·]|(?<!n\.v)\.(?!\w)", sent[occ.start():])[0]
                            if "n.v." not in chunk:
                                l18b.append(f"{name}: {v_} im Bestimmbar-Satz ohne n. v. („{sent[max(0, occ.start() - 15):occ.start() + 20]}“)")
            # Anbieterfakten in determinable_from: der Claim-Abschnitt zum Gegenstand trägt kein n. v.
            for v_, fid in df.items():
                if fid in facts:
                    for seg_ in re.split(r"[·;]", facts[fid]["claim"]):
                        if re.search(b_.get("subject", "$^"), seg_) and "n. v." in seg_:
                            l18b.append(f"{f['id']}: {v_} als bestimmbar gezählt, aber {fid} sagt „{seg_.strip()[:30]}“")
            # Vergleichstabellen: Zeile zum Gegenstand (Merkmal trifft basis.subject): Ja/Nein-Zellen nur für bestimmbare Anbieter
            for tb in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, re.S):
                hdr = [_txt(h).replace("¶", "").strip() for h in re.findall(r"<th\b[^>]*>(.*?)</th>", tb.group(1), re.S)]
                if not _is_cmp(hdr):
                    continue
                for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", tb.group(1), re.S):
                    cells = [_txt(c_).replace("¶", "").strip() for c_ in re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S)]
                    rowids = set(re.findall(r"FACT_[A-Z0-9_]+", row))
                    if not cells or not (re.search(b_.get("subject", "$^").split("|")[0], cells[0]) or set(df.values()) <= rowids):
                        continue
                    for j, c_ in enumerate(cells[1:], 1):
                        if j < len(hdr) and not c_.startswith("n.v.") and not any(w in keys for w in hdr[j].split()):
                            l18b.append(f"Zeile {cells[0][:15]}: {hdr[j]} „{c_[:15]}“ ohne Fakt mit Aussage zum Gegenstand")
        report("L18b Quantor-Basis aus Anbieterfakten", BLOCKER, not l18b, "; ".join(l18b[:3]) if l18b else "jede Quantor-Basis aus Anbieterfakten abgeleitet")
        # L12c · Vergleichstabellen (erste Spalte „Merkmal“): jede Datenzelle ist an einen Fakt gebunden (td/tr/table) oder ganz n. v.
        l12c = []
        for tb in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, re.S):
            ths = [_txt(h).replace("¶", "").strip() for h in re.findall(r"<th\b[^>]*>(.*?)</th>", tb.group(1), re.S)]
            if not _is_cmp(ths):
                continue
            for row in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", tb.group(1), re.S):
                for j, cm in enumerate(re.finditer(r"<td\b[^>]*>(.*?)</td>", row.group(1), re.S)):
                    if j and _txt(cm.group(1)).replace("¶", "").strip(" .") != "n.v" and not _bound(tb.start(1) + row.start(1) + cm.start()):
                        l12c.append(f"„{_txt(cm.group(1))[:30]}“")
        report("L12c Vergleichszellen gebunden", BLOCKER, not l12c, "ungebunden: " + "; ".join(l12c[:4]) if l12c else "alle Datenzellen der Vergleichstabellen gebunden oder n. v.")
        report("L26c Offen-Punkt bindet Fakten", BLOCKER, not l26c, "; ".join(l26c[:3]) if l26c else "Offen-Punkte zu Kontraktdaten gebunden (L26 greift)")
        # L64/L67 · nur geltendes Recht: normalisiert, inkl. JS-Inhalte, Attribute und Prompt
        OLD_LAW = (r"\ba\.\s?f\.|alte[nr]? fassung|\baufgehoben\b|aufhebung|altjahre|altf[aä]ll|offene[nr]? fälle|§\s?52 abs\.\s?28|bis zur abschaffung"
                   r"|(?:vor|seit) dem jstg|bis 2024|\bbverfg\b|aussetzung der vollziehung|\badv\b(?=[- ](?:verfahren|antrag|beschluss|gewährt))|rückwirk|steuer-zeitachse|zeitachse (?:der|des) (?:rechts|steuer|besteuer)"
                   r"|\b(?:frühere|vormalige|ehemalige|bisherige|alte)\w* \S*(?:grenze|beschränkung|begrenzung|regel\w*|rechtslage|fassung)"  # L80
                   r"|\b(?:vormals|ehemals|einst)\b|\bfrüher\b(?! als)|abgeschafft|entfiel\b|weggefallen|\bgalt\b"  # L80; „früher als“ = Komparativ
                   r"|\b\d{1,3}[. \u00a0]?000\s?-?(?:€|euro|eur)\b|(?:€|\beur|\beuro)\s?\d{1,3}[. \u00a0]?000\b|\b\d{1,3}\.?000-euro|\b\d+\s?t€"  # L80: Beträge
                   r"|\bbis (?:zum |einschließlich )?(?:vz |veranlagungszeitraum )?20(?:1\d|2[0-4])\b|\bwar(?:en)? (?:\S+ ){0,6}(?:beschränkt|begrenzt)\b"  # L80: Präteritum, VZ
                   r"|(?:beschränkung|grenze|begrenzung)\w*(?: \S+){0,7} (?:gestrichen|entfällt|entfallen|weggefallen)|(?:gestrichen|aufgehoben) (?:\S+ ){0,3}\S*(?:beschränkung|grenze)"
                   r"|\bzuvor (?:geltend|gültig)\w*|\bnicht mehr (?:begrenzt|beschränkt)")  # L80 (Holdout r12)
        attrs = " ".join(re.findall(r'(?:title|aria-label|alt)="([^"]*)"', html))
        page_all = re.sub(r"<(style)\b.*?</\1>", "", html, flags=re.S) + " " + attrs
        PROMPT_OLD = (r"\ba\.\s?f\.|altjahre|§\s?52 abs\.\s?28|\badv\b|\b\d{1,3}\.?000\s?-?(?:€|euro|eur)\b|\b\d+\s?t€|satz [56] a\."
                      r"|§\s?20 abs\.\s?6 satz [56]\b|\b(?:vormals|ehemals)\b|\bfrüher\b(?! als)|abgeschafft|entfiel\b|rückwirkend|\baufgehoben\b|bverfg-vorlage|\bbis (?:vz )?20(?:1\d|2[0-4])\b")  # L80
        l64 = []
        md_nosrc = "\n".join(ln for ln in md.splitlines() if not re.match(r"\|\s*S\d+\s*\|", ln)) if md else ""  # L80: ganze Analyse außer Quellenzeilen
        for name, txt, rx in (("Seite", page_all, OLD_LAW), ("Analyse", md_nosrc, OLD_LAW),
                              ("DBOM", json.dumps({k: v for k, v in dbom.items() if k not in ("audit_trail", "sources")}, ensure_ascii=False), OLD_LAW),
                              ("Prompt", prm[0].read_text(encoding="utf-8") if prm else "", PROMPT_OLD)):
            l64 += [f"{name}: „{x}“" for x in sorted(set(re.findall(rx, norm_txt(txt))))]
        report("L64 nur geltendes Recht", BLOCKER, not l64, "; ".join(l64[:5]) if l64 else "keine Darstellung früherer Rechtslagen (normalisiert, inkl. JS, Attribute, Prompt)")
        # L47 · starke rechtliche Bewertung nur, wenn ein Claim sie wörtlich trägt
        claims_nz = nz(" ".join(f["claim"] for f in F))
        page_txt = re.sub(r"<[^>]+>", " ", re.sub(r"<style\b.*?</style>", "", html, flags=re.S))
        md_body = re.split(r"\n## 5 · ", md)[0] if md else ""  # Quellenverzeichnis (Titel, URLs) ausgenommen
        claims_cf = norm_txt(" ".join(f["claim"] for f in F))
        l47 = [m.group(0) for src in (page_txt, md_body) for m in re.finditer(STRONG, norm_txt(src)) if m.group(0) not in claims_cf]
        report("L47 Modalität = Claim", BLOCKER, not l47, "ohne Claim: " + ", ".join(sorted(set(l47))[:5]) if l47 else "keine stärkere Rechtsbewertung als im Claim")
        if md:
            # L48 · Konfidenzen in der Analyse nur mit Fakt-ID und = DBOM
            l48 = []
            VL = {"belegt": "CONFIRMED", "medienangabe": "MEDIA_REPORT", "ungeprüft": "UNVERIFIED", "scenario_projection": "SCENARIO_PROJECTION"}
            for m in re.finditer(r"\(`(FACT_[A-Z0-9_]+)`, (belegt|Medienangabe|ungeprüft|SCENARIO_PROJECTION)", body):  # L05d: Verdict-Label = DBOM
                if m.group(1) in facts and facts[m.group(1)]["verdict"] != VL[m.group(2).casefold()]:
                    l48.append(f"{m.group(1)}: Label {m.group(2)} ≠ {facts[m.group(1)]['verdict']}")
            if re.search(r"\((?:V|M|P|S)\)", body):
                l48.append("Provenienzkürzel (V)/(M)/(P)/(S) statt Fakt-ID")
            for m in re.finditer(r"Konf(?:\.|idenz)(?:\s*:|\s+von|\s+bei)?\s*(\d+(?:[.,]\d+)?)", body):  # L48b/L48c: auch „Konf.“, ganze Zahlen, Dezimalpunkt
                par = body[body.rfind("(", 0, m.start()):m.start()]
                ids = re.findall(r"`(FACT_[A-Z0-9_]+)`", par)
                if not ids:
                    l48.append(f"Z. {body[:m.start()].count(chr(10)) + 1}: ohne Fakt-ID")
                elif ids[-1] in facts and (facts[ids[-1]]["confidence"] is None or abs(float(m.group(1).replace(",", ".")) - facts[ids[-1]]["confidence"]) > 1e-9):
                    l48.append(f"{ids[-1]}: {m.group(1)} ≠ DBOM")
            report("L48 Analyse-Konfidenzen", BLOCKER, not l48, "; ".join(l48[:5]) if l48 else "alle Konfidenzen mit Fakt-ID und = DBOM")
            # L53 · Analyse = faktgebundene Kurzfassung: Sync-Blöcke vorhanden; Handtext mit Angaben nennt eine Fakt-ID
            blocks = {b: re.search(r"<!-- sync:%s -->\n(.*?)<!-- /sync:%s -->" % (b, b), md, re.S) for b in ("CLAIMS", "K", "KORR", "MOD", "GLOSSAR")}
            nk = len(re.findall(r'^\s*\["K\d+",', js_ks.group(1), re.M)) if js_ks else 0
            l53 = [f"Block {b} fehlt/leer" for b, m in blocks.items() if not m or not m.group(1).strip()]
            if blocks["K"] and len(re.findall(r"^\*\*K\d+ ·", blocks["K"].group(1), re.M)) != nk:
                l53.append("K-Block ≠ KS")
            hand = re.sub(r"<!-- sync:(\w+) -->.*?<!-- /sync:\1 -->", "", body, flags=re.S)
            hand = re.sub(r"\$\$.*?\$\$|\$[^$]+?\$", "", hand, flags=re.S)
            for para in re.split(r"\n\s*\n|\n(?=- )", hand):
                if re.search(MD_TOK, para) and "FACT_" not in para and not para.lstrip().startswith(("#", ">", "|")):
                    l53.append("ohne Fakt-ID: " + re.sub(r"\s+", " ", para)[:60] + "…")
            # L53b · Blöcke byte-genau = Neuerzeugung; jede Fakt-ID der Analyse existiert in der DBOM
            try:
                want = build_blocks(html, dbom)
                l53b = [f"Block {b} weicht von der Erzeugung ab" for b, m in blocks.items() if m and m.group(1) != want.get(b)]
            except (ValueError, KeyError) as e:  # L53c: Erzeugung bricht bei inkonsistenten Daten ab
                l53b = [f"Erzeugung nicht möglich: {e}"]
            l53b += [f"unbekannte Fakt-ID {i}" for i in sorted(set(re.findall(r"FACT_[A-Z0-9_]+", md)) - set(facts))]
            report("L53b Sync-Blöcke = Erzeugung", BLOCKER, not l53b, "; ".join(l53b[:4]) if l53b else f"{len(blocks)} Blöcke byte-gleich, alle Fakt-IDs in der DBOM")
            # L54 · keine Beleggrad-Aussagen in Handtext der DBOM; Modul 8 aus dem Fazit der Seite
            l54 = [m["title"] for m in dbom.get("analysis_modules", []) if re.search(r"\b(belegt|gesichert|bestätigt|verifiziert)\b", m.get("note", ""), re.I)]
            if not any(m.get("source") == "s-fz" for m in dbom.get("analysis_modules", [])):
                l54.append("Modul 8 nicht aus S-FZ erzeugt")
            report("L54 Beleggrad nur aus Verdicts", BLOCKER, not l54, "; ".join(l54) if l54 else "keine Beleggrad-Notizen, Modul 8 aus dem Fazit der Seite")
            # L58 · Sektionsnummern der Seite in der Analyse nur als „Modulseite Sxx“
            l58 = re.findall(r"(?<!Modulseite )\b(?:S\d{2}|S-FZ)\b", body)
            report("L58 Seitenverweise eindeutig", BLOCKER, not l58, "ohne „Modulseite“: " + ", ".join(sorted(set(l58))) if l58 else "Seitenverweise als „Modulseite Sxx“")
            # L59 · Pflichtabschnitte der Ausgabestruktur (Prompt Abschnitt 7) und Executive Summary ≤ 250 Wörter
            REQ = {"0 Titelblock": r"^\| Version \|", "0 Kurz-Disclaimer": r"\*\*Disclaimer \(Kurzfassung\):\*\*", "1 Executive Summary": r"^## 1 · Executive Summary",
                   "2 Claim-Tabelle": r"Claim-Tabelle\n\n<!-- sync:CLAIMS -->", "2 K-Prüfprotokoll": r"Prüfprotokoll K1–K\d+", "2 Korrekturliste": r"Korrekturliste",
                   "3 Module 1–7": r"#### Modul 1 ·[\s\S]*#### Modul 7 ·", "4 Modul 8": r"#### Modul 8 ·", "5 Glossar": r"^## 4 · Glossar",
                   "6 Quellen": r"^## 5 · Quellenverzeichnis", "7 M-DBOM": r"^## 6 · M-DBOM", "8 Scorecard": r"^## 8 · QA-Scorecard", "9 Disclaimer": r"^## 9 · Disclaimer"}
            l59 = [k for k, rx in REQ.items() if not re.search(rx, md, re.M)]
            es = re.search(r"## 1 · Executive Summary\n(.*?)\n---", md, re.S)
            words = len(re.findall(r"\w+", re.sub(r"`FACT_[A-Z0-9_]+`", "", es.group(1)))) if es else 0
            if words > 250:
                l59.append(f"Executive Summary {words} Wörter > 250")
            report("L59 Ausgabestruktur", BLOCKER, not l59, "fehlt: " + ", ".join(l59) if l59 else f"alle Pflichtabschnitte vorhanden, Executive Summary {words} Wörter")
            report("L53 Analyse faktgebunden", BLOCKER, not l53, "; ".join(l53[:3]) if l53 else f"Sync-Blöcke vollständig ({nk} K), Handtext mit Angaben faktgebunden")
            # L49 · Analyse-Scorecard = Seite (per Sync erzeugt)
            m8 = re.search(r"## 8 · QA-Scorecard\n(.*?)\n---", md, re.S)
            sc = re.findall(r"= \*\*([\d,]+) %\*\*", m8.group(1)) if m8 else []
            pg = re.findall(r"data-qa-score>([\d,]+)<", html)
            sym = {"check-pass": "✓", "check-part": "◐", "check-fail": "✗"}
            rows8 = {g: (st, why) for g, st, why in re.findall(r"^\| ([CQ]\d+) [^|]*\| ([✓◐✗]) \| (.*) \|$", m8.group(1), re.M)} if m8 else {}
            tips = {lab.split()[0]: (re.search(r'title="([^"]*)"', rest) or [None, ""])[1] for lab, rest in re.findall(r'<tr><td>([CQ]\d+ [^<]*)</td><td class="check-\w+"([^>]*)>', html)}
            import html as _h
            rowdiff = [g for g, c in ((lab.split()[0], c) for lab, c in t.qa_rows) if rows8.get(g, ("", ""))[0] != sym.get(c.split()[0] if c else "", "?")
                       or rows8.get(g, ("", ""))[1] != (_h.unescape(tips.get(g, "")) or "–")]  # L49b: auch Begründung
            sc = sc if not rowdiff else sc + ["Zeilen " + ",".join(rowdiff)]
            report("L49 Analyse-Scorecard", BLOCKER, bool(sc) and bool(pg) and set(sc) == {pg[0]} and "Automatisch erzeugt" in m8.group(1),
                   f"Analyse {', '.join(sc) or '–'} % · Seite {pg[0] if pg else '–'} %" + ("" if m8 and "Automatisch erzeugt" in m8.group(1) else " · nicht per Sync erzeugt"))
        # L40 · Rückweg zu L10b: jeder UNVERIFIED-Fakt hat einen Offen-Punkt
        uv_open = sorted(f["id"] for f in F if f["verdict"] == "UNVERIFIED" and f["id"] not in open_facts)
        report("L40 UNVERIFIED ⇒ Offen-Punkt", BLOCKER, not uv_open, "ohne Offen-Punkt: " + ", ".join(uv_open) if uv_open else f"alle {sum(f['verdict'] == 'UNVERIFIED' for f in F)} UNVERIFIED-Fakten in der Offen-Liste")
        # L39 · Quelle passt zum Beleggrad: interne Quellen höchstens UNVERIFIED (Konf. ≤ 0,6) oder SCENARIO_PROJECTION
        tier = {x["id"]: x.get("tier") for x in dbom["sources"]}
        bad39 = [f"{f['id']} ({f['verdict']}, {f['confidence']})" for f in F if tier.get(f["source_id"]) == "internal"
                 and not (f["verdict"] == "SCENARIO_PROJECTION" or (f["verdict"] == "UNVERIFIED" and f["confidence"] <= 0.6))]
        report("L39 interne Quelle ⇒ schwaches Verdict", BLOCKER, not bad39, "zu stark belegt: " + ", ".join(bad39) if bad39 else "interne Quellen nur mit UNVERIFIED ≤ 0,6 oder SCENARIO_PROJECTION")
        # L37 · DBOM-Freitexte: keine Überbehauptungen, kein abweichender Score (Verlauf im audit_trail ausgenommen)
        dtext = json.dumps({k: v for k, v in dbom.items() if k != "audit_trail"}, ensure_ascii=False)
        over_d = re.findall(OVERCLAIM, dtext)
        page_pct = re.findall(r"data-qa-score>([\d,]+)<", html)
        sc_d = [x for x in re.findall(r"Score\D{0,30}?(\d+[,.]\d) ?%", dtext) if x.replace(".", ",") not in page_pct]
        report("L37 DBOM-Freitexte", BLOCKER, not over_d and not sc_d, "; ".join(([f"Überbehauptung: {', '.join(sorted(set(over_d)))}"] if over_d else []) + ([f"Score {', '.join(sc_d)} ≠ Seite"] if sc_d else [])) or "keine Überbehauptung, kein abweichender Score")
        # L27 · sichtbares Verdict-Badge, wenn alle gebundenen Fakten nicht CONFIRMED sind
        BADGE = {"MEDIA_REPORT": "MEDIEN", "UNVERIFIED": "UNGEPRÜFT", "SCENARIO_PROJECTION": "SCENARIO|MODELL"}
        nobadge = []
        for m in re.finditer(r'<(\w+)\b[^>]*data-source="([^"]+)"[^>]*>', html):
            ids = [i for i in m.group(2).split() if i in facts]
            if not ids or any(facts[i]["verdict"] == "CONFIRMED" for i in ids) or "data-open" in m.group(0):
                continue
            inner = visible_part(element_inner(html, m))  # L80/L82: Kommentar oder unsichtbares Element ist kein Kennzeichen
            need = "|".join(BADGE[facts[i]["verdict"]] for i in ids)
            if not re.search(r">\s*(?:%s)\s*<" % need, inner):
                nobadge.append(ids[0])
        for row in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else []):
            ids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", row) if i in facts]
            if any(facts[i]["verdict"] != "CONFIRMED" for i in ids) and not re.search(r"Medienangabe|ungeprüft|Modellannahme", row):
                nobadge.append(row[2:6].strip('",'))
        report("L27 Verdict-Badge", BLOCKER, not nobadge, "ohne Badge: " + ", ".join(sorted(set(nobadge))[:8]) if nobadge else "alle nicht bestätigten Bindungen gekennzeichnet")
        # L25 · Fundstellen und Zahlen in K-Tabelle/Modal stehen im gebundenen Fakt
        norm = nz
        tok = re.compile(r"§\s?\d+[a-z]?(?:\s?Abs\.\s?\d+)?|\bArt\.\s?\d+|\b\d{4}\b|\d[\d.,]*\s?(?:%|€|\$)|" + AZ_NORM)
        js_miss = []
        for blob in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else []) + ([b for _, b in re.findall(r"\n\s*(\w+):\{(.*?)\}(?:,|$)", js_reg.group(1))] if js_reg else []):
            ids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", blob) if i in facts]
            hay = norm(" ".join(str(facts[i].get(k, "")) for i in ids for k in ("claim", "period", "caveat")))
            text = re.sub(r'FACT_[A-Z0-9_]+|u:"[^"]*"|https?://\S+', "", blob)
            for tk in tok.findall(text):
                if norm(tk) not in hay:
                    js_miss.append(f"{(ids or ['?'])[0]}: {tk}")
        report("L25 Fundstellen in JS-Inhalten", BLOCKER, not js_miss, ("nicht im Fakt: " + ", ".join(sorted(set(js_miss))[:8]) + (f" (+{len(set(js_miss)) - 8})" if len(set(js_miss)) > 8 else "")) if js_miss else "alle Fundstellen/Zahlen der K-Tabelle und des Modals im Fakt")
        # L36 · Aktenzeichen und Normteile in statischen Sektionen stehen im gebundenen Fakt
        az_miss = []
        for x in t.texts:
            if x["src"] and SCOPE.match(x["sec"] or ""):
                hay = norm(" ".join(str(facts[s].get(k, "")) for s in x["src"].split() if s in facts for k in ("claim", "period", "caveat")))
                az_miss += [f"{x['src'].split()[0]}: {m}" for m in re.findall(AZ_NORM, x["text"]) if norm(m) not in hay]
        js_az = [m for m in js_miss if re.search(AZ_NORM, m)]
        report("L36 Aktenzeichen/Normteil ∈ Fakt", BLOCKER, not az_miss and not js_az,
               ("nicht im gebundenen Fakt: " + ", ".join(sorted(set(az_miss + js_az))[:8])) if az_miss or js_az else "alle Aktenzeichen und Normteile im gebundenen Fakt")
        # L36b · data-def befreit keine Fundstellen: Paragraph/Aktenzeichen/Normteil in data-def braucht data-source
        def_az = [f"{x['sec']}: {m.group(0)}" for x in t.texts if x.get("def") and not x["src"] and SCOPE.match(x["sec"] or "")
                  for m in re.finditer(r"§\s?\d+|" + AZ_NORM, x["text"])]
        report("L36b Fundstellen in data-def", BLOCKER, not def_az, "ohne Faktbindung: " + ", ".join(def_az[:6]) if def_az else "keine ungebundenen Fundstellen in Definitionen")
        # L41a · Glossar: Fundstellen in data-def-Einträgen brauchen eine Faktbindung (L29 erweitert)
        js_gl = re.search(r"const GLOSSAR=\[(.*?)\n\];", html, re.S)
        gl_miss = []
        for row in (re.findall(r'^\s*\[(".*?)\],?$', js_gl.group(1), re.M) if js_gl else []):
            ids = [i for i in re.findall(r"FACT_[A-Z0-9_]+", row) if i in facts]
            hay = norm(" ".join(str(facts[i].get(k, "")) for i in ids for k in ("claim", "period", "caveat")))
            txt = re.sub(r'FACT_[A-Z0-9_]+|\\\\\(.*?\\\\\)', "", row)
            for tk in re.findall(r"§\s?\d+[a-z]?(?:\s?Abs\.\s?\d+)?|\bArt\.\s?\d+|\bVO\b[^\"]{0,12}?\d+/\d{4}|" + AZ_NORM, txt):
                if norm(tk) not in hay:
                    gl_miss.append(f"{row[1:row.index(chr(34), 1)]}: {tk}")
        rend = bool(re.search(r'data-def="Glossar"[^>]{0,40}data-source="\$\{g\[4\]\}"', html))
        need_r = bool(js_gl) and "FACT_" in js_gl.group(1)
        report("L41a Glossar-Fundstellen gebunden", BLOCKER, not gl_miss and (rend or not need_r), ("ungebunden: " + ", ".join(gl_miss[:6])) if gl_miss else ("Glossar-Renderer setzt data-source" if rend else ("Glossar-Renderer ohne data-source" if need_r else "keine Fundstellen im Glossar")) if js_gl else "kein Glossar")

    # ---------- L12 · Rückwärtsbindung (statisch) und JS-Tabellen
    unb = [f"{x['sec']}: {mm.group(0).strip()}" for x in t.texts if SCOPE.match(x["sec"] or "") and not x["bound"] for mm in FACT_PATTERN.finditer(x["text"])]
    ks_rows = re.findall(r'\["K\d+",.*?\]\s*(?:,|$)', js_ks.group(1), re.M) if js_ks else []
    ks_nofact = [r[2:5].strip('",') for r in ks_rows if "FACT_" not in r]
    reg_entries = re.findall(r"\n\s*(\w+):\{(.*?)\}(?:,|$)", js_reg.group(1)) if js_reg else []
    reg_nofact = [k for k, body in reg_entries if "FACT_" not in body]
    detail = unb[:8] + [f"K-Tabelle {k}" for k in ks_nofact] + [f"REG {k}" for k in reg_nofact]
    report("L12 Rückwärtsbindung", BLOCKER, not detail, ("ungebunden: " + ", ".join(detail[:10]) + (f" (+{len(detail) - 10})" if len(detail) > 10 else "")) if detail else "alle Fakt-Angaben in Sektionen, K-Tabelle und Modal gebunden")

    # ---------- Analyse ↔ Seite
    if md:
        md_k = {k: r for k, r in re.findall(r"\*\*(K\d+) ·.*?\*\*Ergebnis: ([✓◐✗])", md, re.S)}
        sym = {"ok": "✓", "part": "◐", "no": "✗"}
        page_k = {k: sym.get(r, "?") for k, r in re.findall(r'\["(K\d+)","[^"]*","[^"]*","(ok|part|no)"', html)}
        diff = [f"{k}: Seite {page_k.get(k)} ≠ Analyse {md_k.get(k)}" for k in sorted(set(md_k) | set(page_k), key=lambda x: int(x[1:])) if md_k.get(k) != page_k.get(k)]
        report("L13 Phase A Seite = Analyse", BLOCKER, not diff and bool(md_k), "; ".join(diff) if diff else f"{len(md_k)} Ergebnisse identisch")
        lead = f"provenance/m{mod.group(1)}.dbom.json" in md and '"facts": [' not in md
        report("L13b eine führende DBOM", BLOCKER, lead, "Analyse verweist auf externe DBOM" if lead else "Analyse führt eigene Faktenliste")
        if dbom:
            refs = {s.get("ref") for s in dbom["sources"]}
            cited = set(re.findall(r"\bS[1-9]\d*\b", md))  # S04 = Sektion, S4 = Quelle
            listed = set(re.findall(r"^\| (S\d+) \|", md, re.M))
            miss = sorted(cited - refs, key=lambda x: int(x[1:]))
            report("L13c Quellen Analyse = DBOM", BLOCKER, not miss and listed == (refs - {"–"}),
                   ("zitiert, aber nicht in DBOM: " + ", ".join(miss)) if miss else ("Quellenliste der Analyse = dbom.sources" if listed == (refs - {"–"}) else f"Quellenliste der Analyse weicht ab ({len(listed)} vs. {len(refs - {'–'})})"))

    # ---------- L44 · eine Version in Titel, Kopf, JSON-LD, DBOM und Analyse
    if dbom:
        v = dbom["module"]["version"]
        visible = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", "", html, flags=re.S))  # L50: ganze Seite, nur sichtbarer Text
        seen = re.findall(r"(?i)\b(?:v|(?:modul)?version\s?:?\s?|fassung:?\s?)(\d+\.\d+\.\d+)\b", visible) + re.findall(r'"version": "(\d+\.\d+\.\d+)", "stichtag"', html)  # L52/L44b
        tb = md.split("\n---", 1)[0] if md else ""  # L44b: jede Versionsangabe im Titelblock außer der Prompt-Grundlage
        mv = (re.findall(r"\b(\d+\.\d+\.\d+)\b", "\n".join(ln for ln in tb.splitlines() if not ln.startswith("| Grundlage"))) + re.findall(r"\bModul v(\d+\.\d+\.\d+)", md)) if md else []  # „Version x.y.z“ in der Analyse = Herstellerversionen (z. B. ATAS 8.0.12), daher nur Kopfzeile/„Modul v“
        vclaims = set(re.findall(r"\b\d+\.\d+\.\d+\b", " ".join(f["claim"] for f in dbom["facts"])))  # L80: Herstellerversionen (z. B. ATAS 8.0.12)
        bad_v = sorted(set(x for x in seen + mv if x != v and x not in vclaims))
        report("L44 Version einheitlich", BLOCKER, bool(seen) and not bad_v and (bool(mv) or not md), f"DBOM {v}; abweichend: {', '.join(bad_v)}" if bad_v else (f"überall {v}" if mv or not md else "Analyse ohne Versionszeile"))

    # ---------- L28 · keine Überbehauptungen in Methodik/Transparenz
    over = re.findall(OVERCLAIM, re.sub(r"<script.*?</script>", "", html, flags=re.S))
    report("L28 Überbehauptungen", BLOCKER, not over, "gefunden: " + ", ".join(sorted(set(over))) if over else "keine")
    # ---------- L29 · data-def nur auf Blattelementen
    blk = [m.group(1) for m in re.finditer(r'<(\w+)\b[^>]*data-def="[^"]*"[^>]*>(.*?)</\1>', html, re.S) if re.search(r"<(div|p|section|table|ul|ol|figure|svg)\b", m.group(2))]
    report("L29 data-def nur Blatt", BLOCKER, not blk, f"{len(blk)} data-def-Container mit Blockinhalt" if blk else "data-def nur auf Blattelementen")
    # ---------- L31 · Barrierefreiheit (statisch)
    canv = re.findall(r"<canvas\b[^>]*>", html)
    bad_c = [c for c in canv if 'role="img"' not in c or "aria-label" not in c]
    report("L31 Canvas zugänglich", BLOCKER, not bad_c, f"{len(bad_c)} canvas ohne role=img/aria-label" if bad_c else f"{len(canv)} canvas mit role=img und aria-label")
    report("L31b reduzierte Bewegung", BLOCKER, "prefers-reduced-motion" in html or "scroll-fade" not in html, "prefers-reduced-motion berücksichtigt" if "prefers-reduced-motion" in html else "Einblend-Animation ohne prefers-reduced-motion")
    # ---------- L32 · Lizenzen und Versionen der selbst gehosteten Dateien
    root = page.parent
    if "fonts.css" in html:
        ofl = sorted(p.name for p in (root / "fonts").glob("LICENSE-*-OFL.txt"))
        report("L32 Schriftlizenzen", BLOCKER, len(ofl) >= 3, f"{len(ofl)} OFL-Lizenzdateien in fonts/")
    kx = root / "vendor/katex/katex.min.js"
    if "vendor/katex" in html and kx.exists():
        v = re.search(r'version:"(\d+)\.(\d+)\.(\d+)"', kx.read_text(encoding="utf-8", errors="ignore"))
        ver = tuple(map(int, v.groups())) if v else (0, 0, 0)
        report("L32b KaTeX ≥ 0.16.10", BLOCKER, ver >= (0, 16, 10), "KaTeX " + ".".join(map(str, ver)))
    # ---------- L34 · Offen-Liste Seite = Analyse
    if md:
        po = [re.sub(r"\s+", " ", t).strip() for t in re.findall(r"<li[^>]*data-open[^>]*>([^<]*)</li>", html)]
        sec7 = re.search(r"## 7 · Offene Prüfpunkte vor Veröffentlichung\n\n((?:- .*\n)+)", md)
        mo = [x[2:].strip() for x in sec7.group(1).splitlines()] if sec7 else []
        report("L34 Offen-Liste Seite = Analyse", BLOCKER, bool(po) and po == mo, f"{len(po)} Punkte identisch" if po == mo and po else f"Seite {len(po)} · Analyse {len(mo)} Punkte, abweichend")

    # ---------- QA-Sektion
    pts = sum(1 if "check-pass" in cls else 0.5 if "check-part" in cls else 0 for _, cls in t.qa_rows)
    n = len(t.qa_rows)
    if n:
        pct = round(pts / n * 100, 1)
        shown = re.findall(r"data-qa-score>([\d,]+)<", html)
        report("L03 QA-Score", BLOCKER, bool(shown) and all(float(s.replace(",", ".")) == pct for s in shown), f"Zellen {pts}/{n} = {pct} %; Text: {', '.join(shown) or 'nicht gebunden'}")
        fails = [lab for lab, cls in t.qa_rows if "check-pass" not in cls]
        badge = "FREIGABE" if not [l for l in fails if l.startswith("C")] and pct >= 90 else "ÜBERARBEITUNG"
        # L03b/L03c/L03d · Freigabestatus exakt: DBOM-Status ist die Quelle; jede Statusangabe auf Seite und in der Analyse stimmt überein,
        # FREIGABE nur, wenn die Regel (alle C ✓, Score ≥ 90 %) erfüllt ist
        st_db = {"UEBERARBEITUNG": "ÜBERARBEITUNG"}.get(dbom["module"].get("release_status", ""), dbom["module"].get("release_status", "")) if dbom else ""
        found = [("Seite", x.upper()) for x in re.findall(r"Freigabe(?:status)?:\s*(Überarbeitung|Freigabe)\b", html, re.I)]
        found += [("JSON-LD", {"UEBERARBEITUNG": "ÜBERARBEITUNG"}.get(x, x)) for x in re.findall(r'"release_status": "(\w+)"', html)]
        found += [("Analyse", x or y) for x, y in re.findall(r"\*\*Freigabeempfehlung:\s*(ÜBERARBEITUNG|FREIGABE)|Freigabeempfehlung \|\s*\*\*(ÜBERARBEITUNG|FREIGABE)", md)] if md else []
        l03 = [f"{w}: {x} ≠ {st_db}" for w, x in found if x != st_db]
        entw = re.findall(r"\bEntwurf\b", html) + (re.findall(r"\(Entwurf\)", md) if md else [])
        if st_db == "FREIGABE" and entw:
            l03.append("Status FREIGABE, aber „Entwurf“ steht noch")
        if st_db != "FREIGABE" and not re.search(r"(?<!kein )(?<!keine )\bEntwurf\w*", _txt(visible_part((re.search(r"<footer\b.*?</footer>", html, re.S) or [""])[0]))):  # L03d: sichtbar
            l03.append("Footer ohne „Entwurf“ trotz Status " + st_db)
        if st_db == "FREIGABE" and badge != "FREIGABE":
            l03.append("Status FREIGABE, Regel ergibt ÜBERARBEITUNG")
        report("L03b Freigabestatus", BLOCKER, bool(st_db) and len(found) >= 3 and not l03, "; ".join(l03[:4]) if l03 else f"Status {st_db} an {len(found)} Stellen einheitlich; Regel ergibt {badge}")
    open_gates = set(re.findall(r'<li[^>]*data-gate="([CQ]\d+)"', html))
    passed = {lab.split()[0] for lab, cls in t.qa_rows if "check-pass" in cls}
    clash = sorted(open_gates & passed)
    report("L10b ✓ trotz Offen-Punkt", BLOCKER, not clash, "✓ trotz offenem Punkt: " + ", ".join(clash) if clash else f"{len(open_gates)} Gates mit Offen-Punkten, keines auf ✓")
    # L40 · jedes nicht bestandene Gate hat einen Offen-Punkt als Abschlusskriterium
    no_crit = sorted({lab.split()[0] for lab, cls in t.qa_rows if "check-pass" not in cls} - open_gates, key=lambda g: (g[0], int(g[1:])))
    report("L40 ◐/✗ ⇒ Offen-Punkt", BLOCKER, bool(t.qa_rows) and not no_crit, ("ohne Abschlusskriterium: " + ", ".join(no_crit)) if no_crit else ("keine Gate-Tabelle" if not t.qa_rows else f"{len([1 for _, c in t.qa_rows if 'check-pass' not in c])} nicht bestandene Gates mit Offen-Punkt"))
    qa_sec = re.search(r'<section id="s-qa".*?</section>', html, re.S)
    hand = re.findall(r"\d+ (?:Elemente|Treffer)", qa_sec.group(0)) if qa_sec else []
    report("L15 QA-Messwerte", WARN, not hand, "handgeschrieben: " + ", ".join(hand) if hand else "keine handgeschriebenen Messwerte")

    w = max(len(r[0]) for r in results)
    blockers = 0
    for rule, level, ok, msg in results:
        if not ok and level == BLOCKER:
            blockers += 1
        print(f"{'✓' if ok else ('✗' if level == BLOCKER else '!')} {rule.ljust(w)}  [{level}] {msg}")
    print(f"\n{page.name}: {blockers} BLOCKER verletzt" if blockers else f"\n{page.name}: alle BLOCKER bestanden")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
