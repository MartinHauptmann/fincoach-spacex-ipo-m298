#!/usr/bin/env python3
"""Regressionsnachweis (L50/L80): wendet Injektionsfälle auf eine Kopie des Repos an und prüft,
dass der zuständige Test anschlägt. Aufruf: python3 qa/run_regression.py qa/regression/m300-bypasses.json"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
cases = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
page = cases["page"]
ignore = shutil.ignore_patterns(".git", "node_modules", "__pycache__")
miss = 0
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp) / "base"
    shutil.copytree(root, base, ignore=ignore)
    for c in cases["cases"]:
        d = Path(tmp) / "case"
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(base, d)
        anchor_ok = True
        for f, old, new in c["edits"]:
            p = d / f
            t = p.read_text(encoding="utf-8")
            if old not in t:
                anchor_ok = False
                break
            p.write_text(t.replace(old, new, 1), encoding="utf-8")
        if not anchor_ok:
            print(f"[ANKER FEHLT] {c['name']}: {old[:50]!r}")
            miss += 1
            continue
        if c.get("sync") or not c.get("nosync") and any(f in (page, f"provenance/{Path(page).stem}.dbom.json") for f, _, _ in c["edits"]):  # L82: Spiegel immer nachziehen
            subprocess.run(["python3", "qa/sync_module.py", page], cwd=d, capture_output=True)
        r = subprocess.run(["python3", "qa/check_module.py", page], cwd=d, capture_output=True, text=True)
        fails = [l for l in r.stdout.splitlines() if l.startswith("✗")]
        if c["expect"] == "NONE":  # Negativkontrolle: legitimer Text darf keinen Blocker auslösen
            if r.returncode == 0:
                print(f"[ok]       {c['name']} (Negativkontrolle)")
            else:
                miss += 1
                print(f"[FEHLALARM] {c['name']}: {[l[2:40] for l in fails][:3]}")
            continue
        if r.returncode and not fails:  # Absturz des Prüfskripts ist kein Erkennen
            miss += 1
            print(f"[ABSTURZ]  {c['name']}: {(r.stderr.strip().splitlines() or ['?'])[-1][:120]}")
            continue
        hit = [l for l in fails if re.match(r"✗ (%s)\b" % c["expect"], l)]
        if r.returncode and hit:
            print(f"[erkannt]  {c['name']} → {hit[0][2:40].strip()}")
        else:
            miss += 1
            print(f"[UMGANGEN] {c['name']} (erwartet {c['expect']}; exit {r.returncode}; {[l[2:30] for l in fails][:3]})")
print(f"\n{len(cases['cases']) - miss}/{len(cases['cases'])} Fälle korrekt (Verstöße vom zuständigen Test erkannt, Negativkontrollen ohne Blocker)")
sys.exit(1 if miss else 0)
