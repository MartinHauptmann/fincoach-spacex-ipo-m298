#!/usr/bin/env python3
"""FinCoach-AI · abgeleitete Werte synchronisieren (L03, L07, L13, L21, L34).

Aufruf:  python3 qa/sync_module.py m300.html
Schreibt alle Werte, die aus der DBOM oder den Gate-Zellen folgen, in Seite und Analyse:
  - Seite: data-dbom-count, JSON-LD fact_summary, data-dbom-range, data-dbom-conf, data-qa-score/-points
  - Analyse: Abschnitt 5 (Quellen), Abschnitt 6 (Fakten), Abschnitt 7 (Offen-Liste = Seite)
Nie von Hand nachziehen – immer dieses Skript laufen lassen, danach check_module.py.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

TIER = {"primary": "Primärquelle", "vendor": "Herstellerquelle", "secondary": "Sekundärquelle"}


def de(x, nd=None):
    s = f"{x:.{nd}f}" if nd is not None else str(x)
    return s.replace(".", ",")


def main():
    page = Path(sys.argv[1])
    mod = re.search(r"m(\d{3})", page.name).group(1)
    dbom_p = page.parent / "provenance" / f"m{mod}.dbom.json"
    d = json.loads(dbom_p.read_text(encoding="utf-8"))
    F = d["facts"]
    fs = {"total": len(F), "confirmed_primary": sum(f["verdict"] == "CONFIRMED" for f in F),
          "media_report": sum(f["verdict"] == "MEDIA_REPORT" for f in F), "unverified": sum(f["verdict"] == "UNVERIFIED" for f in F),
          "scenario_projection": sum(f["verdict"] == "SCENARIO_PROJECTION" for f in F), "vendor_claim": sum(f["class"] == "VENDOR_CLAIM" for f in F)}
    d["fact_summary"] = {**fs, "by_class": dict(sorted(Counter(f["class"] for f in F).items()))}
    dbom_p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    cnt = {"total": fs["total"], "confirmed": fs["confirmed_primary"], "media": fs["media_report"], "unverified": fs["unverified"],
           "scenario": fs["scenario_projection"], "vendor": fs["vendor_claim"], "sources": len(d["sources"])}
    facts = {f["id"]: f for f in F}

    s = page.read_text(encoding="utf-8")
    s = re.sub(r'(<span data-dbom-count="(\w+)">)\d+(</span>)', lambda m: m.group(1) + str(cnt.get(m.group(2), 0)) + m.group(3), s)
    s = re.sub(r'"fact_summary": \{[^}]*\}', '"fact_summary": { ' + ", ".join(f'"{k}": {v}' for k, v in fs.items()) + " }", s, count=1)
    rng = {}
    for f in F:
        rng.setdefault(f["class"], []).append(f["confidence"])
    s = re.sub(r'(<span data-dbom-range="(\w+)">)[^<]*(</span>)', lambda m: m.group(1) + f"{de(min(rng[m.group(2)]))}–{de(max(rng[m.group(2)]))}" + m.group(3), s)
    s = re.sub(r'(<span data-dbom-conf="(\w+)">)[^<]*(</span>)', lambda m: m.group(1) + de(facts[m.group(2)]["confidence"], 2) + m.group(3), s)
    s = re.sub(r'"version": "[\d.]+", "stichtag"', f'"version": "{d["module"]["version"]}", "stichtag"', s, count=1)
    # QA-Score aus den Gate-Zellen
    qa = re.search(r'<section id="s-qa".*?</section>', s, re.S).group(0)
    cells = re.findall(r"<tr><td>([CQ]\d+) [^<]*</td><td class=\"(check-\w+)\"", qa)
    pts = sum(1 if c == "check-pass" else 0.5 if c == "check-part" else 0 for _, c in cells)
    pct = round(pts / len(cells) * 100, 1)
    s = re.sub(r"(<span data-qa-score>)[^<]*(</span>)", lambda m: m.group(1) + de(pct, 1) + m.group(2), s)
    s = re.sub(r"(<span data-qa-points>)[^<]*(</span>)", lambda m: m.group(1) + (de(pts, 1) if pts % 1 else str(int(pts))) + m.group(2), s)
    s = re.sub(r'(QA-Score )[\d,]+( %)', lambda m: m.group(1) + de(pct, 1) + m.group(2), s)
    page.write_text(s, encoding="utf-8")
    open_items = re.findall(r"<li[^>]*data-open[^>]*>([^<]*)</li>", s)

    # Analyse
    mds = sorted((page.parent / "analysen").glob(f"m{mod}-*deep-dive*.md"))
    if mds:
        md = mds[0].read_text(encoding="utf-8")
        rows = sorted((x for x in d["sources"] if x.get("ref", "–") != "–"), key=lambda x: int(x["ref"][1:]))
        tbl = "\n".join(f"| {x['ref']} | {x['title']} | {TIER.get(x['tier'], x['tier'])} | `{x['id']}` | {x['url']} |" for x in rows)
        md = re.sub(r"(\| Nr\. \| Quelle \| Stufe \| DBOM-ID \| URL \|\n\|---\|---\|---\|---\|---\|\n)(?:\|.*\|\n)+", lambda m: m.group(1) + tbl + "\n", md)
        frows = "\n".join(f"| `{f['id']}` | {f['verdict']} | {f['class']} | {de(f['confidence'])} | {f.get('period', '–')} | {f['claim']} |" for f in F)
        md = re.sub(r"(\| ID \| Verdict \| Klasse \| Konf\. \| Bezugszeitraum \| Claim \|\n\|---\|---\|---\|---\|---\|---\|\n)(?:\|.*\|\n)+", lambda m: m.group(1) + frows + "\n", md)
        md = re.sub(r"^\| Version \| [\d.]+", f"| Version | {d['module']['version']}", md, count=1, flags=re.M)  # L44
        md = re.sub(r"Stand: Modul v[\d.]+,\n\d+ Fakten, \d+ Quellen\.", f"Stand: Modul v{d['module']['version']},\n{len(F)} Fakten, {len(d['sources'])} Quellen.", md)
        md = re.sub(r"(## 7 · Offene Prüfpunkte vor Veröffentlichung\n\n)(?:- .*\n)+", lambda m: m.group(1) + "".join(f"- {t}\n" for t in open_items), md)
        mds[0].write_text(md, encoding="utf-8")
    print(f"synchronisiert: {cnt} · QA {de(pct, 1)} % ({pts}/{len(cells)}) · Offen-Liste {len(open_items)} Punkte")


if __name__ == "__main__":
    main()
