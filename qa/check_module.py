#!/usr/bin/env python3
"""FinCoach-AI · statische Modul-Prüfung (Gate vor jeder Veröffentlichung).

Aufruf:  python3 qa/check_module.py m300.html [provenance/m300.dbom.json]
Exit-Code 0 = alle BLOCKER bestanden, 1 = mindestens ein BLOCKER verletzt.

Jede Regel verweist auf einen Eintrag im Fehlerkatalog qa/LESSONS.md (L-Nummer).
Neue Fehler → neue L-Nummer → neue Regel hier. So wird aus jedem Fehler ein Test.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCKER, WARN = "BLOCKER", "WARN"
results = []


def report(rule, level, ok, msg):
    results.append((rule, level, ok, msg))


class Collector(HTMLParser):
    """Sammelt data-source-Verweise, KPI-Karten und Gate-Zellen."""

    def __init__(self):
        super().__init__()
        self.refs = []           # (fact_id, classes)
        self.qa_rows = []        # (label, status_class)
        self._in_qa = False
        self._row = None
        self._cell = None
        self._depth_qa = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "data-source" in a and a["data-source"].startswith("FACT_"):
            self.refs.append((a["data-source"], a.get("class", "")))
        if tag == "section" and a.get("id") == "s-qa":
            self._in_qa = True
        if self._in_qa and tag == "tr":
            self._row = {"cells": []}
        if self._in_qa and tag == "td" and self._row is not None:
            self._cell = {"cls": a.get("class", ""), "text": ""}

    def handle_endtag(self, tag):
        if tag == "td" and self._cell is not None and self._row is not None:
            self._row["cells"].append(self._cell)
            self._cell = None
        if tag == "tr" and self._row is not None:
            c = self._row["cells"]
            if len(c) >= 2 and re.match(r"^[CQ]\d+\s", c[0]["text"].strip()):
                self.qa_rows.append((c[0]["text"].strip(), c[1]["cls"]))
            self._row = None
        if tag == "section" and self._in_qa:
            self._in_qa = False

    def handle_data(self, data):
        if self._cell is not None:
            self._cell["text"] += data


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    page = Path(sys.argv[1])
    html = page.read_text(encoding="utf-8")
    mod = re.search(r"m(\d{3})", page.name)
    dbom_path = Path(sys.argv[2]) if len(sys.argv) > 2 else page.parent / "provenance" / f"m{mod.group(1)}.dbom.json"
    dbom = json.loads(dbom_path.read_text(encoding="utf-8")) if dbom_path.exists() else None

    # L01 · Styleguide-Basis muss auf body stehen (Einbettung überschreibt sonst Farbe/Schrift)
    m = re.search(r"\bbody\s*\{([^}]*)\}", html)
    body = m.group(1) if m else ""
    report("L01 body-Basis", BLOCKER,
           "color:#E2E8F0" in body.replace(" ", "") and "Inter" in body,
           "body{} setzt color:#E2E8F0 und font-family Inter" if body else "keine body{}-Regel gefunden")

    # L02 · Chart.js-Standardtextfarbe = Styleguide-Diagrammfarbe
    if "chart.js" in html.lower() or "new Chart(" in html:
        report("L02 Chart.defaults.color", BLOCKER, "Chart.defaults.color='#94A3B8'" in html.replace('"', "'"),
               "Chart.defaults.color='#94A3B8' gesetzt")

    # L04 · Kurz-Disclaimer im Hero (erste Section) – Gate C1 gilt für jede Ausgabeform
    hero = re.search(r'<section id="s01".*?</section>', html, re.S)
    hero_txt = hero.group(0) if hero else ""
    report("L04 Hero-Disclaimer", BLOCKER,
           bool(re.search(r"keine Anlage-?,? ?(Rechts|Anlageberatung)", hero_txt, re.I)) and "Totalverlust" in hero_txt,
           "Hero enthält Beratungsausschluss und Totalverlusthinweis")

    c = Collector()
    c.feed(html)
    ref_ids = {r[0] for r in c.refs}

    if dbom:
        facts = {f["id"]: f for f in dbom.get("facts", [])}
        # L08a · jeder Verweis existiert in der DBOM
        missing = sorted(ref_ids - facts.keys())
        report("L08a Verweise aufgelöst", BLOCKER, not missing, "fehlend: " + ", ".join(missing) if missing else f"{len(ref_ids)} Verweise ok")
        # L08b · jeder DBOM-Fakt ist an mindestens ein Seitenelement gebunden
        unbound = sorted(facts.keys() - ref_ids)
        report("L08b Fakten gebunden", BLOCKER, not unbound, "ungebunden: " + ", ".join(unbound) if unbound else "alle Fakten gebunden")
        # L05 · Verdict passt zu Klasse und Konfidenz
        bad = [f["id"] for f in facts.values() if f["verdict"] == "CONFIRMED"
               and (f["class"] in ("MEDIA_REPORT", "MODEL_ASSUMPTION", "SCENARIO_PROJECTION") or f["confidence"] < 0.7)]
        report("L05 Verdict-Klasse", BLOCKER, not bad, "CONFIRMED trotz Medien/Modell/Konf.<0,7: " + ", ".join(bad) if bad else "konsistent")
        # L05c · nur zulässige Verdicts
        allowed = {"CONFIRMED", "MEDIA_REPORT", "UNVERIFIED", "SCENARIO_PROJECTION"}
        badv = [f["id"] for f in facts.values() if f["verdict"] not in allowed]
        report("L05c Verdict zulässig", BLOCKER, not badv, "unzulässig: " + ", ".join(badv) if badv else "alle Verdicts zulässig")
        # L16 · CONFIRMED braucht Bezugszeitraum
        noper = [f["id"] for f in facts.values() if f["verdict"] == "CONFIRMED" and not f.get("period")]
        report("L16 Bezugszeitraum", BLOCKER, not noper, "CONFIRMED ohne period: " + ", ".join(noper) if noper else "alle CONFIRMED mit period")
        # L05b · grün umrandete KPI (confirmed-kpi) nur für CONFIRMED-Fakten
        wrong_kpi = [fid for fid, cls in c.refs if "confirmed-kpi" in cls and facts.get(fid, {}).get("verdict") != "CONFIRMED"]
        report("L05b KPI-Stil", BLOCKER, not wrong_kpi, "confirmed-kpi auf nicht bestätigtem Fakt: " + ", ".join(wrong_kpi) if wrong_kpi else "KPI-Stile konsistent")
        # L07 · Zahlen im Text = Zahlen aus der DBOM (data-dbom-count)
        F = list(facts.values())
        cnt = {"total": len(F), "confirmed": sum(f["verdict"] == "CONFIRMED" for f in F),
               "media": sum(f["verdict"] == "MEDIA_REPORT" for f in F),
               "unverified": sum(f["verdict"] == "UNVERIFIED" for f in F),
               "scenario": sum(f["verdict"] == "SCENARIO_PROJECTION" for f in F),
               "vendor": sum(f["class"] == "VENDOR_CLAIM" for f in F)}
        diffs = [f"{k}: Text {v} ≠ DBOM {cnt[k]}" for k, v in re.findall(r'data-dbom-count="(\w+)"[^>]*>(\d+)<', html) if k in cnt and int(v) != cnt[k]]
        bound = "data-dbom-count" in html
        report("L07 Zählungen", BLOCKER, bound and not diffs, "; ".join(diffs) if diffs else ("alle Zählungen = DBOM" if bound else "Zählungen nicht an DBOM gebunden (data-dbom-count fehlt)"))
        # L07b · keine fest geschriebenen Faktenzahlen außerhalb data-dbom-count
        hard = re.findall(r"(?<!von )\b\d+ (?:belegt|belegte Fakten|Herstellerangaben)\b", re.sub(r'<span data-dbom-count="\w+">\d+</span>', "", html))
        report("L07b keine Hardcodes", WARN, not hard, "fest geschrieben: " + ", ".join(hard) if hard else "keine")
        # L07c · JSON-LD fact_summary = externe DBOM
        ld = re.search(r'"fact_summary":\s*\{([^}]*)\}', html)
        if ld:
            nums = dict((k, int(v)) for k, v in re.findall(r'"(\w+)":\s*(\d+)', ld.group(1)))
            exp = dbom["fact_summary"]
            d2 = [f"{k}: {v}≠{exp.get(k)}" for k, v in nums.items() if exp.get(k) != v]
            report("L07c JSON-LD", BLOCKER, not d2, "; ".join(d2) if d2 else "JSON-LD = DBOM")

    # L06 · KPI-Aussagen „0 von N“ / „alle N“ nur, wenn die Quelle kein n. v. enthält
    for mm in re.finditer(r'>(0|\d+) von (\d+)<', html):
        ctx = html[max(0, mm.start() - 600): mm.end() + 600]
        ok = "n. v." in ctx or "belegt" in ctx
        report("L06 Quantor-KPI", WARN, ok, f"„{mm.group(1)} von {mm.group(2)}“: " + ("Belegstatus/n. v. ausgewiesen" if ok else "n. v.-Fälle und Belegstatus im KPI ausweisen"))

    # L03 · QA-Score im Text = Score aus Gate-Zellen
    pts = sum(1 if "check-pass" in cls else 0.5 if "check-part" in cls else 0 for _, cls in c.qa_rows)
    n = len(c.qa_rows)
    if n:
        pct = round(pts / n * 100, 1)
        shown = re.findall(r"data-qa-score>([\d,]+)<", html)
        ok = all(float(s.replace(",", ".")) == pct for s in shown) and shown
        report("L03 QA-Score", BLOCKER, bool(ok), f"Zellen: {pts}/{n} = {pct} %; Text: {', '.join(shown) or 'nicht gebunden'}")
        fails = [lab for lab, cls in c.qa_rows if "check-pass" not in cls]
        release_ok = not [l for l in fails if l.startswith("C")] and pct >= 90
        badge = "FREIGABE" if release_ok else "ÜBERARBEITUNG"
        report("L03b Freigabestatus", BLOCKER, badge in html.upper() or (badge == "ÜBERARBEITUNG" and "ÜBERARBEITUNG" in html),
               f"Regel ergibt {badge}")

    # L10b · kein ✓ für ein Gate, zu dem ein offener Pflichtpunkt existiert (data-gate auf <li> und Gate-Zelle)
    open_gates = set(re.findall(r'<li[^>]*data-gate="([CQ]\d+)"', html))
    passed_gates = {lab.split()[0] for lab, cls in c.qa_rows if "check-pass" in cls}
    clash = sorted(open_gates & passed_gates)
    report("L10b ✓ trotz Offen-Punkt", BLOCKER, not clash, "✓ trotz offenem Punkt: " + ", ".join(clash) if clash else f"{len(open_gates)} Gates mit Offen-Punkten, keines auf ✓")

    if dbom:
        # L14 · Quellen: jede DBOM-Quelle von ≥ 1 Fakt genutzt, jeder Fakt mit existierender Quelle
        src_ids = {x["id"] for x in dbom.get("sources", [])}
        used = {s for f in dbom.get("facts", []) for s in [f.get("source_id"), *f.get("additional_sources", [])] if s}
        unused, dangling = sorted(src_ids - used), sorted(used - src_ids)
        report("L14 Quellen ↔ Fakten", BLOCKER, not unused and not dangling,
               (f"ungenutzt: {', '.join(unused)}" if unused else "") + (f" fehlend: {', '.join(dangling)}" if dangling else "") or "konsistent")

    # L12 · Rückwärtsbindung: Zahlen mit Einheit in S01–S11 brauchen in der Elternkette data-source,
    #       data-est/data-def oder ein EST-Zeichen im selben Element
    class NumScan(HTMLParser):
        def __init__(self):
            super().__init__(); self.stack = []; self.hits = []; self.sec = None
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == "section": self.sec = a.get("id", "")
            if tag in ("br", "img", "input", "meta", "link", "hr"): return
            node = {"tag": tag, "bound": any(k in a for k in ("data-source", "data-est", "data-def")), "texts": [], "est": False}
            if "est-mark" in (a.get("class") or "") and self.stack: self.stack[-1]["est"] = True
            self.stack.append(node)
        def handle_endtag(self, tag):
            while self.stack:
                n = self.stack.pop()
                if n["tag"] == tag:
                    if not n["est"]:
                        for t in n["texts"]: self.hits.append(t)
                    elif self.stack: pass
                    break
        def handle_data(self, data):
            if not self.stack or not re.match(r"s(0[1-9]|1[01])$", self.sec or ""): return
            if any(n["bound"] for n in self.stack): return
            for m in re.findall(r"\d[\d.,]*\s?(?:%|Gbps|Mio\.|Mrd\.|€|\$|Kontrakte)", data):
                self.stack[-1]["texts"].append(f"{self.sec}: {m.strip()}")
    ns = NumScan(); ns.feed(html)
    report("L12 Rückwärtsbindung", BLOCKER, not ns.hits, ("ungebunden: " + ", ".join(ns.hits[:8])) if ns.hits else "alle Zahlenangaben mit Einheit gebunden")

    # L13 · Phase-A-Ergebnisse Seite = Analyse; eine führende DBOM
    md_path = page.parent / "analysen"
    mds = list(md_path.glob(f"m{mod.group(1)}-*deep-dive*.md")) if md_path.exists() else []
    if mds:
        md = mds[0].read_text(encoding="utf-8")
        md_k = {k: r for k, r in re.findall(r"\*\*(K\d+) ·.*?\*\*Ergebnis: ([✓◐✗])", md, re.S)}
        sym = {"ok": "✓", "part": "◐", "no": "✗"}
        page_k = {k: sym.get(r, "?") for k, r in re.findall(r'\["(K\d+)","[^"]*","[^"]*","(ok|part|no)"', html)}
        diff = [f"{k}: Seite {page_k.get(k)} ≠ Analyse {md_k.get(k)}" for k in sorted(set(md_k) | set(page_k), key=lambda x: int(x[1:])) if md_k.get(k) != page_k.get(k)]
        report("L13 Phase A Seite = Analyse", BLOCKER, not diff and bool(md_k), "; ".join(diff) if diff else f"{len(md_k)} Ergebnisse identisch")
        lead = f"provenance/m{mod.group(1)}.dbom.json" in md and '"facts": [' not in md
        report("L13b eine führende DBOM", BLOCKER, lead, "Analyse verweist auf externe DBOM, keine eigene Faktenliste" if lead else "Analyse führt eigene Faktenliste oder verweist nicht auf die externe DBOM")

    # L15 · keine handgeschriebenen Messwerte in der QA-Sektion
    qa_sec = re.search(r'<section id="s-qa".*?</section>', html, re.S)
    hand = re.findall(r"\d+ (?:Elemente|Treffer)", qa_sec.group(0)) if qa_sec else []
    report("L15 QA-Messwerte", WARN, not hand, "handgeschrieben: " + ", ".join(hand) if hand else "keine handgeschriebenen Messwerte")

    w = max(len(r[0]) for r in results)
    blockers = 0
    for rule, level, ok, msg in results:
        mark = "✓" if ok else ("✗" if level == BLOCKER else "!")
        if not ok and level == BLOCKER:
            blockers += 1
        print(f"{mark} {rule.ljust(w)}  [{level}] {msg}")
    print(f"\n{page.name}: {blockers} BLOCKER verletzt" if blockers else f"\n{page.name}: alle BLOCKER bestanden")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
