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
    r"\d[\d.,]*\s?-?(?:%|Gbps|Mio\.|Mrd\.|€|\$|Kontrakte|Legs)"   # Zahl mit Einheit
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
          r"|rechtswidrig\w*|gleichheitswidrig\w*|verst(?:ieß|ößt|oßen|oße) gegen")  # L52/L47b  # L52: normalisiert, Synonyme
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
                "Hebel": r"Hebel", "Knock-out": r"Knock-out", "nur erfahrene Anleger": r"nur\s+für\s+erfahrene\s+Anleger"}
    NEG = re.compile(r"\b(ohne|kein\w*|nicht|ausgeschlossen|nie)\b|(?<![a-zäöü])un(?=erfahren)", re.I)  # L42b: Verneinung im ganzen Teilsatz

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
                    if fid in facts and abs(float(v.replace(",", ".")) - facts[fid]["confidence"]) > 1e-9]
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
        # L46/L52b · Leitphrasen abgetrennter Fakten: kleinstes Element mit der Leitphrase (normalisiert) bindet den Fakt allein
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
        report("L46 Leitphrasen gebunden", BLOCKER, not l46 and any(f.get("markers") for f in F), "; ".join(sorted(set(l46))[:4]) if l46 else ("alle Leitphrasen an ihren Fakt gebunden" if any(f.get("markers") for f in F) else "keine markers in der DBOM"))
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
        for row in (re.findall(r'\["K\d+",.*?\]', js_ks.group(1)) if js_ks else []):
            if re.search(r"\b(belegt|bestätigt)\b", re.sub(r'"(?:ok|part|no)"', "", row)) and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in re.findall(r"FACT_[A-Z0-9_]+", row)):
                l57.append(row[2:6].strip('",'))
        if md:
            for para in re.split(r"\n\s*\n|\n(?=[-|] )", re.split(r"\n## 5 · ", md)[0]):
                txt = re.sub(r"\(`FACT_[A-Z0-9_]+`, (?:belegt|Medienangabe|ungeprüft|SCENARIO_PROJECTION)[^)]*\)|Legende:[^\n]*|Schwächster Beleg|\| belegt \|", "", para)
                if re.search(r"\b(belegt|bestätigt)\b", txt) and not any(facts.get(i, {}).get("verdict") == "CONFIRMED" for i in re.findall(r"FACT_[A-Z0-9_]+", para)):
                    l57.append("Analyse: " + re.sub(r"\s+", " ", txt)[:40] + "…")
        report("L57 „belegt“ nur mit CONFIRMED", BLOCKER, not l57, "; ".join(l57[:4]) if l57 else "„belegt/bestätigt“ nur bei gebundenem CONFIRMED-Fakt")
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
            for m in re.finditer(r"Konf(?:\.|idenz)\s*(\d+(?:[.,]\d+)?)", body):  # L48b/L48c: auch „Konf.“, ganze Zahlen, Dezimalpunkt
                par = body[body.rfind("(", 0, m.start()):m.start()]
                ids = re.findall(r"`(FACT_[A-Z0-9_]+)`", par)
                if not ids:
                    l48.append(f"Z. {body[:m.start()].count(chr(10)) + 1}: ohne Fakt-ID")
                elif ids[-1] in facts and abs(float(m.group(1).replace(",", ".")) - facts[ids[-1]]["confidence"]) > 1e-9:
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
            want = build_blocks(html, dbom)
            l53b = [f"Block {b} weicht von der Erzeugung ab" for b, m in blocks.items() if m and m.group(1) != want.get(b)]
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
                   "2 Claim-Tabelle": r"Claim-Tabelle\n\n<!-- sync:CLAIMS -->", "2 K1–K12": r"Prüfprotokoll K1–K12", "2 Korrekturliste": r"Korrekturliste",
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
            inner = element_inner(html, m)
            need = "|".join(BADGE[facts[i]["verdict"]] for i in ids)
            if not re.search(need, inner):
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
        seen = re.findall(r"(?i)\b(?:v|(?:modul)?version\s?)(\d+\.\d+\.\d+)\b", visible) + re.findall(r'"version": "(\d+\.\d+\.\d+)", "stichtag"', html)  # L52/L44b
        tb = md.split("\n---", 1)[0] if md else ""  # L44b: jede Versionsangabe im Titelblock außer der Prompt-Grundlage
        mv = (re.findall(r"\b(\d+\.\d+\.\d+)\b", "\n".join(ln for ln in tb.splitlines() if not ln.startswith("| Grundlage"))) + re.findall(r"\bModul v(\d+\.\d+\.\d+)", md)) if md else []  # „Version x.y.z“ in der Analyse = Herstellerversionen (z. B. ATAS 8.0.12), daher nur Kopfzeile/„Modul v“
        bad_v = sorted(set(x for x in seen + mv if x != v))
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
        report("L03b Freigabestatus", BLOCKER, badge in html.upper(), f"Regel ergibt {badge}")
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
