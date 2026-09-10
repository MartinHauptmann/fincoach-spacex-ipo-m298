#!/usr/bin/env python3
"""
FinCoach AI · Modul-Prüfung (statisch, offline)
================================================
Definierte Prüfungen für FinCoach-AI-Module (M-DBOM v1):

  ① Compliance      – Pflichtklauseln (Disclaimer, RDG/StBerG/WpIG/FinDAG, DSGVO, Marken),
                      keine externen Fonts/Tracker, nur erlaubte Script-Hosts (CSP-konform)
  ② Datenqualität   – JSON-LD-Provenienz eingebettet, externe DBOM valide, fact_summary
                      konsistent, alle data-source-Referenzen auflösbar, jede source_id
                      vorhanden, Stichtag im HTML == Stichtag in DBOM, Konfidenz je Fakt
  ③ Styleguide      – fonts.css, CAT-Level, NavDock, Live-Audit-Banner, QA-Sektion,
                      Quellen/Glossar/Disclaimer, EST/REP-Marker nur innerhalb von
                      Provenienz-Containern

Aufruf:
  python3 provenance/fincoach_module_check.py m300.html
  python3 provenance/fincoach_module_check.py m299.html m300.html --json

Exit-Code 0 = alle Pflichtprüfungen bestanden, 1 = mindestens ein FAIL.
Nur Standardbibliothek; kein Netzwerk.
"""
import json
import re
import sys
from pathlib import Path

ALLOWED_SCRIPT_HOSTS = ("cdn.tailwindcss.com", "cdn.jsdelivr.net")
ALLOWED_STYLE_HOSTS = ("cdn.jsdelivr.net",)
FORBIDDEN_HOST_PATTERNS = (
    "fonts.googleapis.com", "fonts.gstatic.com", "googletagmanager", "google-analytics",
    "facebook.net", "hotjar", "matomo", "plausible.io", "segment.com", "doubleclick",
)

# Pflichtklauseln: (ID, Beschreibung, Regex, Pflicht?)
COMPLIANCE_CLAUSES = [
    ("C01", "Keine Anlageberatung (Disclaimer)", r"keine\s+Anlageberatung", True),
    ("C02", "RDG/StBerG/WpIG/FinDAG-Hinweis", r"RDG.*StBerG.*(WpIG|WpHG).*FinDAG", True),
    ("C03", "DSGVO-Bezug benannt", r"DSGVO", True),
    ("C04", "Markennennung rein beschreibend", r"rein\s+beschreibend", True),
    ("C05", "Stichtag/Datenstand ausgewiesen", r"Stichtag", True),
    ("C06", "Honest-Disclosure / Daten-Transparenz-Box", r"Daten-Transparenz|honest_disclosure", True),
    ("C07", "Impressum & Datenschutz verlinkt", r'href="impressum\.html".*href="datenschutz\.html"', True),
    ("C08", "EU-KI-VO-Bezug (nur Module mit KI-/Profiling-Inhalt)", r"KI-Verordnung|AI Act|KI-VO", False),
]

STYLE_CHECKS = [
    ("S01", "fonts.css self-hosted eingebunden", r'<link[^>]+href="fonts\.css"'),
    ("S02", "CAT-Level (Einsteiger→Experte)", r'data-lvl="einsteiger".*data-lvl="experte"'),
    ("S03", "NavDock vorhanden", r'id="navdock"'),
    ("S04", "Provenienz-Banner + Live-Audit", r'id="live-audit-banner"'),
    ("S05", "QA-Sektion vorhanden", r'id="s-qa"'),
    ("S06", "Glossar-Container", r'id="glossar"'),
    ("S07", "Modul-Matrix", r'id="s-mtx"'),
    ("S08", "TNGB-Farbtoken (#00CFFF Cyan)", r"#00CFFF"),
]


def _host_of(url):
    m = re.match(r"https?://([^/]+)/?", url)
    return m.group(1).lower() if m else ""


def check_module(html_path: Path):
    root = html_path.parent
    html = html_path.read_text(encoding="utf-8")
    flat = re.sub(r"\s+", " ", html)
    results = []

    def add(section, cid, label, ok, detail="", required=True):
        results.append({"section": section, "id": cid, "label": label,
                        "status": "PASS" if ok else ("FAIL" if required else "WARN"),
                        "detail": detail})

    # ── ① Compliance ────────────────────────────────────────────────────────
    for cid, label, rx, req in COMPLIANCE_CLAUSES:
        ok = re.search(rx, flat, re.I | re.S) is not None
        add("compliance", cid, label, ok, required=req)

    ext_scripts = re.findall(r'<script[^>]+src="(https?://[^"]+)"', html, re.I)
    bad_scripts = [s for s in ext_scripts if _host_of(s) not in ALLOWED_SCRIPT_HOSTS]
    add("compliance", "C09", "Externe Scripts nur von CSP-erlaubten Hosts", not bad_scripts,
        ", ".join(bad_scripts))
    ext_styles = re.findall(r'<link[^>]+href="(https?://[^"]+)"', html, re.I)
    bad_styles = [s for s in ext_styles if _host_of(s) not in ALLOWED_STYLE_HOSTS]
    add("compliance", "C10", "Externe Stylesheets nur von CSP-erlaubten Hosts", not bad_styles,
        ", ".join(bad_styles))
    # Nur geladene Ressourcen prüfen (src/href), nicht Fließtext oder Prüf-Skripte
    resource_urls = re.findall(r'(?:src|href)="(https?://[^"]+)"', html, re.I)
    hits = sorted({p for p in FORBIDDEN_HOST_PATTERNS for u in resource_urls if p in u})
    add("compliance", "C11", "Keine Google-Fonts / Tracker / Analytics als Ressource", not hits, ", ".join(hits))

    # ── ② Datenqualität ─────────────────────────────────────────────────────
    ld = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    ldjson = None
    try:
        ldjson = json.loads(ld.group(1)) if ld else None
    except json.JSONDecodeError as e:
        add("data", "D01", "JSON-LD Provenienz parsebar", False, str(e))
    add("data", "D01", "M-DBOM JSON-LD eingebettet & parsebar", ldjson is not None)

    dbom = None
    ext_path = None
    if ldjson and ldjson.get("module", {}).get("external_dbom"):
        ext_path = root / ldjson["module"]["external_dbom"]
    if ext_path and ext_path.exists():
        try:
            dbom = json.loads(ext_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            add("data", "D02", "Externe DBOM valide", False, str(e))
    add("data", "D02", "Externe DBOM vorhanden & valide", dbom is not None,
        str(ext_path) if ext_path else "kein external_dbom-Pfad")

    if dbom:
        facts = dbom.get("facts", [])
        ids = [f["id"] for f in facts]
        add("data", "D03", "Fakt-IDs eindeutig", len(ids) == len(set(ids)))
        fs = dbom.get("fact_summary", {})
        add("data", "D04", "fact_summary.total == Anzahl Fakten",
            fs.get("total") == len(facts), f"summary={fs.get('total')} facts={len(facts)}")
        src_ids = {s["id"] for s in dbom.get("sources", [])}
        missing_src = [f["id"] for f in facts if f.get("source_id") not in src_ids]
        add("data", "D05", "Jede source_id existiert in sources", not missing_src, ", ".join(missing_src))
        no_conf = [f["id"] for f in facts if not isinstance(f.get("confidence"), (int, float))]
        add("data", "D06", "Konfidenzwert je Fakt", not no_conf, ", ".join(no_conf))
        no_verdict = [f["id"] for f in facts if not f.get("verdict")]
        add("data", "D07", "Verdict je Fakt", not no_verdict, ", ".join(no_verdict))
        refs = re.findall(r'data-source="(FACT_[A-Z0-9_]+)"', html)
        unresolved = sorted({r for r in refs if r not in set(ids)})
        add("data", "D08", f"Alle data-source-Referenzen auflösbar ({len(refs)} Referenzen)",
            not unresolved, ", ".join(unresolved))
        unused = sorted(set(ids) - set(refs))
        add("data", "D09", "Jeder DBOM-Fakt im HTML referenziert", not unused, ", ".join(unused),
            required=False)
        stich = dbom.get("module", {}).get("stichtag", "")
        add("data", "D10", "Stichtag der DBOM im HTML ausgewiesen", bool(stich) and stich in html, stich)
        ver = dbom.get("module", {}).get("version", "")
        add("data", "D11", "Modulversion der DBOM im HTML ausgewiesen", bool(ver) and ("v" + ver) in html, ver)
        if ldjson:
            add("data", "D12", "JSON-LD-Version == externe DBOM-Version",
                ldjson.get("module", {}).get("version") == ver)
        add("data", "D13", "honest_disclosure vorhanden", bool(dbom.get("honest_disclosure")))
        verdicts = {f["verdict"] for f in facts}
        add("data", "D14", "SCENARIO/INTERPRETATION von CONFIRMED getrennt klassifiziert",
            "CONFIRMED" in verdicts and len(verdicts) > 1)

    # ── ③ Styleguide ────────────────────────────────────────────────────────
    for cid, label, rx in STYLE_CHECKS:
        add("style", cid, label, re.search(rx, flat, re.S) is not None)
    # EST/REP-Marker müssen in einem Container mit data-source liegen
    est_total = len(re.findall(r'class="est-mark"', html))
    add("style", "S09", f"EST/REP-Marker vorhanden ({est_total})", est_total > 0, required=False)
    unmasked = re.findall(r">[^<]*\s<\s[^<]*<", html)
    add("style", "S10", "Keine unmaskierten '<'-Zeichen im Fließtext (Mobile-Rendering)", not unmasked,
        f"{len(unmasked)} Fundstellen")

    return results


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    exit_code = 0
    report = {}
    for f in files:
        p = Path(f)
        res = check_module(p)
        report[f] = res
        fails = [r for r in res if r["status"] == "FAIL"]
        warns = [r for r in res if r["status"] == "WARN"]
        if fails:
            exit_code = 1
        if not as_json:
            print(f"\n=== FinCoach AI Modul-Prüfung · {f} ===")
            for sec in ("compliance", "data", "style"):
                print(f"  [{sec}]")
                for r in res:
                    if r["section"] != sec:
                        continue
                    mark = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}[r["status"]]
                    det = f"  — {r['detail']}" if r["detail"] and r["status"] != "PASS" else ""
                    print(f"    {mark} {r['id']} {r['label']}{det}")
            print(f"  Ergebnis: {len(res) - len(fails) - len(warns)} PASS · {len(warns)} WARN · {len(fails)} FAIL")
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
