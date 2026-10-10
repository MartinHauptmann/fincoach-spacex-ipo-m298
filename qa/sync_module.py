#!/usr/bin/env python3
"""FinCoach-AI · abgeleitete Werte synchronisieren (L03, L07, L13, L21, L34).

Aufruf:  python3 qa/sync_module.py m300.html
Schreibt alle Werte, die aus der DBOM oder den Gate-Zellen folgen, in Seite und Analyse:
  - Seite: data-dbom-count, JSON-LD fact_summary, data-dbom-range, data-dbom-conf, data-qa-score/-points
  - Analyse: Abschnitt 5 (Quellen), Abschnitt 6 (Fakten), Abschnitt 7 (Offen-Liste = Seite)
Nie von Hand nachziehen – immer dieses Skript laufen lassen, danach check_module.py.
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

TIER = {"primary": "Primärquelle", "vendor": "Herstellerquelle", "secondary": "Sekundärquelle"}


def de(x, nd=None):
    s = f"{x:.{nd}f}" if nd is not None else str(x)
    return s.replace(".", ",")

VLAB = {"CONFIRMED": "belegt", "MEDIA_REPORT": "Medienangabe", "UNVERIFIED": "ungeprüft", "SCENARIO_PROJECTION": "SCENARIO_PROJECTION"}
RES = {"ok": "✓", "part": "◐", "no": "✗", "nv": "[N. V.]", "scen": "Szenario"}
SEV = {"crit": "KRITISCH", "major": "WESENTLICH", "hint": "HINWEIS"}
RANK = {"CONFIRMED": 3, "MEDIA_REPORT": 2, "UNVERIFIED": 1, "SCENARIO_PROJECTION": 0}


def plain(x):
    """Seitentext → Markdown: Markup weg, Entities auflösen, KaTeX → $, Sektionsnummern als Modulseite (L58)."""
    x = re.sub(r'<span class="dbom-class-badge">[^<]*</span>', "", x)  # Badges: Kennzeichnung trägt das Fakt-Label
    x = html.unescape(re.sub(r"<[^>]+>", "", x)).replace("\\(", "$").replace("\\)", "$")
    return re.sub(r"\b(S\d{2}|S-FZ)\b", r"Modulseite \1", x)


def build_blocks(page_html, d):
    """L53/L53b/L54/L59: Inhalt der <!-- sync:… -->-Blöcke der Analyse aus Seite und DBOM."""
    facts = {f["id"]: f for f in d["facts"]}

    def flab(fid):
        f = facts[fid]
        return f"(`{fid}`, {VLAB[f['verdict']]}, Konfidenz {de(f['confidence'])})"
    out = {}
    # Claim-Tabelle (L59): Aussagen des Quelltexts, Belege und schwächster Beleg (L19) aus der DBOM
    rows = []
    for c in d.get("source_claims", []):
        fl = [i for i in c["facts"] if i in facts]
        weakest = VLAB[min((facts[i]["verdict"] for i in fl), key=RANK.get)] if fl else "–"
        rows.append(f"| {c['id']} | Quelltext: {c['claim']} | {c['category']} | {RES[c['result']]} | {', '.join(flab(i) for i in fl) or '[N. V.]'} | {weakest} |")
    out["CLAIMS"] = ("Legende: ✓ bestätigt · ◐ präzisiert · ✗ falsch/überholt · [N. V.] nicht verifizierbar. Die Aussagen in Spalte 2 "
                     "zitieren den Quelltext (USER_PROVIDED) und sind keine Tatsachenbehauptungen dieser Analyse.\n\n"
                     "| ID | Aussage | Kategorie | Ergebnis | Belege | Schwächster Beleg |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n")
    ks_js = re.search(r"const KS=\[(.*?)\n\];", page_html, re.S)
    ks = [json.loads(r) for r in re.findall(r'^\s*(\["K\d+",.*\])\s*,?\s*$', ks_js.group(1), re.M)] if ks_js else []
    out["K"] = "".join(f"**{k[0]} · {plain(k[1])}.** Quelltext: {plain(k[2])}. {plain(k[5])} Belege: {', '.join(flab(i) for i in k[6].split())}. **Ergebnis: {RES[k[3]]}** ({SEV.get(k[4], k[4])})\n\n" for k in ks)
    out["KORR"] = "| Nr. | Schwere | Prüfpunkt | Ergebnis |\n|---|---|---|---|\n" + "".join(f"| {k[0]} | {SEV.get(k[4], k[4])} | {plain(k[1])}: {plain(k[2])} | {RES[k[3]]} |\n" for k in ks if k[3] != "ok") + "\n"
    # Module 1–7 aus analysis_modules; Modul 8 aus dem Fazit (S-FZ) der Seite (L54)
    mods = ""
    for m in d.get("analysis_modules", []):
        mods += f"#### {m['title']}\n\n"
        if m.get("source") == "s-fz":
            fz = re.search(r'<section id="s-fz".*?</section>', page_html, re.S)
            for box in re.findall(r'<h3[^>]*>(.*?)</h3><ul[^>]*>(.*?)</ul>', fz.group(0) if fz else "", re.S):
                mods += f"**{plain(box[0])}**\n\n" + "".join(
                    f"- {plain(t).strip()} " + " ".join(flab(i) for i in ids.split() if i in facts) + "\n"
                    for ids, t in re.findall(r'<li data-source="([^"]+)">(.*?)</li>', box[1], re.S)) + "\n"
            th = re.search(r'<div class="info-box[^"]*">(.*?)</div>', fz.group(0) if fz else "", re.S)
            if th:
                ids = sorted(set(re.findall(r"FACT_[A-Z0-9_]+", th.group(1))) | {"FACT_ROADMAP"})
                mods += f"**Strategische These [SZENARIO]:** {plain(re.sub(r'<strong.*?</strong>', '', th.group(1))).strip()} " + " ".join(flab(i) for i in ids if i in facts) + "\n\n"
        else:
            mods += "".join(f"- {plain(facts[i]['claim'])} {flab(i)}\n" for i in m["facts"]) + "\n"
    out["MOD"] = mods
    gl_js = re.search(r"const GLOSSAR=\[(.*?)\n\];", page_html, re.S)
    gl = [json.loads(r) for r in re.findall(r'^\s*(\[".*\])\s*,?\s*$', gl_js.group(1), re.M)] if gl_js else []
    out["GLOSSAR"] = "| Begriff | Definition (Fortgeschritten) | Einordnung (Experte) |\n|---|---|---|\n" + "".join(
        f"| {plain(g[0])} | {plain(g[2])} | {plain(g[3])}{' ' + ' '.join(flab(i) for i in g[4].split() if i in facts) if len(g) > 4 else ''} |\n" for g in gl) + "\n"
    return out


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
        # L53/L53b: erzeugte Blöcke (Claim-Tabelle, Phase A, Module, Glossar) – dieselbe Funktion nutzt check_module
        for name, content in build_blocks(s, d).items():
            md = re.sub(r"(<!-- sync:%s -->\n).*?(<!-- /sync:%s -->)" % (name, name), lambda m: m.group(1) + content + m.group(2), md, count=1, flags=re.S)
        # L48: Konfidenzen im Fließtext stehen mit Fakt-ID und kommen aus der DBOM
        md = re.sub(r"(`(FACT_[A-Z0-9_]+)`[^)`]*?Konf(?:\.|idenz) )(\d+(?:[.,]\d+)?)", lambda m: m.group(1) + de(facts[m.group(2)]["confidence"]) if m.group(2) in facts else m.group(0), md)
        # L49: QA-Scorecard der Analyse aus den Gate-Zellen der Seite
        rows_qa = [(lab, c, (re.search(r'title="([^"]*)"', rest) or [None, ""])[1])
                   for lab, c, rest in re.findall(r'<tr><td>([CQ]\d+ [^<]*)</td><td class="(check-\w+)"([^>]*)>', qa)]
        sym = {"check-pass": "✓", "check-part": "◐", "check-fail": "✗"}
        tbl8 = "\n".join(f"| {lab} | {sym[c]} | {html.unescape(t) or '–'} |" for lab, c, t in rows_qa)
        c_ok = all(c == "check-pass" for lab, c, _ in rows_qa if lab.startswith("C"))
        rel = "FREIGABE" if c_ok and pct >= 90 else "ÜBERARBEITUNG"
        n_ok = sum(c == "check-pass" for _, c, _ in rows_qa); n_part = sum(c == "check-part" for _, c, _ in rows_qa)
        sec8 = ("> **Automatisch erzeugt** aus den Gate-Zellen von `m%s.html` (`qa/sync_module.py`, L49). Nicht von Hand ändern.\n\n"
                "| Gate | Status | Begründung |\n|---|---|---|\n%s\n\n"
                "**Gesamtscore:** %d × ✓ + %d × ◐ = %s von %d Punkten = **%s %%**.\n**Freigabeempfehlung: %s.**\n") % (
                    mod, tbl8, n_ok, n_part, de(pts, 1) if pts % 1 else str(int(pts)), len(cells), de(pct, 1), rel)
        md = re.sub(r"(## 8 · QA-Scorecard\n\n).*?(?=\n---\n)", lambda m: m.group(1) + sec8, md, count=1, flags=re.S)
        mds[0].write_text(md, encoding="utf-8")
    print(f"synchronisiert: {cnt} · QA {de(pct, 1)} % ({pts}/{len(cells)}) · Offen-Liste {len(open_items)} Punkte")


if __name__ == "__main__":
    main()
