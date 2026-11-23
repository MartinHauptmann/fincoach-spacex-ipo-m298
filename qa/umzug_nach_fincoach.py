#!/usr/bin/env python3
"""Umzug M300 (Staging, fincoach-spacex-ipo-m298) -> M525 (fincoach-ai). Einmaliger, reproduzierbarer Schritt.

Aufruf:  python3 qa/umzug_nach_fincoach.py <ziel-checkout-von-fincoach-ai>

Was passiert (nur Dateien im Ziel, kein Commit):
  * Seite, M-DBOM, Analysen, Prompt, qa/ (Skripte, Lehren, Regression), Skill, Agent werden kopiert.
  * Alle Verweise werden mit EINER Abbildung umbenannt (T), auch in den Regressionsfällen,
    damit Anker in Fällen und Seite zueinander passen.
  * Seitenkopf: selbst gehostete Bibliotheken -> FinCoach-Konvention (CDN in der Quelle,
    Umschreibung auf /vendor erst beim Website-Release durch release-single-module.mjs).
    Tailwind-Konfiguration ist in beiden Repos identisch (vendor/tailwind.config.cjs = Inline-Config).
  * Für das Render-Audit ohne CDN-Zugang entsteht qa/vendor-offline/ (für --vendor).
Inhaltlich ändert sich nichts außer Modulnummer und Bibliotheks-Einbindung.
"""
import re, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
DST = Path(sys.argv[1]).resolve()
PAGE = "modul-m525-atas-options-xray.html"
WEB_VENDOR = Path("/home/user/nexus2learn-website/vendor")  # KaTeX 0.16.11 wie live

PAIRS = [("m300.html", PAGE), ("M300", "M525"), ("m300", "m525")]


def T(s: str) -> str:
    for a, b in PAIRS:
        s = s.replace(a, b)
    return s


HEAD_OLD = ('<link rel="stylesheet" href="fonts.css"/>\n'
            '<link rel="stylesheet" href="vendor/tailwind.css"/>\n'
            '<link rel="stylesheet" href="vendor/katex/katex.min.css"/>\n'
            '<script src="vendor/katex/katex.min.js"></script>\n'
            '<script src="vendor/katex/auto-render.min.js"></script>\n'
            '<script src="vendor/chartjs/chart.umd.min.js"></script>\n')
HEAD_NEW = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet"/>\n'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous"/>\n'
            '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>\n'
            '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>\n'
            '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>\n'
            '<script src="https://cdn.tailwindcss.com"></script>\n'
            '<script>\n'
            'tailwind.config = { theme: { extend: {\n'
            "  colors: { tngb: { bg:'#0A0F1A', card:'#121A2E', cyan:'#00CFFF', emerald:'#00CC7A', magenta:'#E6399A', orange:'#FF6B00', lavender:'#9933FF', gold:'#DFAF0F', indigo:'#4472C4', coral:'#E040A0', muted:'#64748B', border:'#1E293B' } },\n"
            "  fontFamily: { sans:['Inter','system-ui','sans-serif'], head:['Space Grotesk','sans-serif'], mono:['JetBrains Mono','monospace'] }\n"
            '}}}\n'
            '</script>\n')


def put(rel_src: str, rel_dst: str, text_fn=T):
    s, d = SRC / rel_src, DST / rel_dst
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text(text_fn(s.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"  {rel_src:58} -> {rel_dst}")


def page_fn(s: str) -> str:
    assert s.count(HEAD_OLD) == 1, "Seitenkopf nicht wie erwartet"
    return T(s.replace(HEAD_OLD, HEAD_NEW))


def case_fn(s: str) -> str:
    # Anker auf den alten Kopf bleiben bewusst unverändert (sie melden danach ANKER FEHLT und werden einzeln umgeschrieben)
    return T(s)


print(f"Umzug {SRC} -> {DST}")
put("m300.html", PAGE, page_fn)
put("provenance/m300.dbom.json", "provenance/m525.dbom.json")
for f in sorted((SRC / "analysen").glob("m300-*.md")):
    put(f"analysen/{f.name}", f"analysen/{T(f.name)}")
for f in sorted((SRC / "prompts").glob("m300-*.md")):
    put(f"prompts/{f.name}", f"prompts/{T(f.name)}")
for f in ["qa/check_module.py", "qa/sync_module.py", "qa/render_audit.cjs", "qa/run_regression.py", "qa/LESSONS.md", "qa/fachbegriffe.json"]:
    put(f, f)
for f in sorted((SRC / "qa/regression").glob("m300-*.json")):
    put(f"qa/regression/{f.name}", f"qa/regression/{T(f.name)}", case_fn)
for f in sorted((SRC / ".claude/skills/fincoach-module-qa").rglob("*")):
    if f.is_file():
        r = f.relative_to(SRC).as_posix()
        put(r, r)
put(".claude/agents/fincoach-qa-reviewer.md", ".claude/agents/fincoach-qa-reviewer.md")

# Offline-Bibliotheken für render_audit --vendor (gleiche Versionen wie die Quelle lädt bzw. live ausgeliefert wird)
vo = DST / "qa/vendor-offline"
vo.mkdir(parents=True, exist_ok=True)
shutil.copyfile(WEB_VENDOR / "katex-0.16.11.min.js", vo / "katex.min.js")
shutil.copyfile(WEB_VENDOR / "katex-0.16.11.min.css", vo / "katex.min.css")
shutil.copyfile(WEB_VENDOR / "katex-auto-render-0.16.11.min.js", vo / "auto-render.min.js")
shutil.copyfile(SRC / "vendor/chartjs/chart.umd.min.js", vo / "chart.umd.js")
shutil.copyfile(SRC / "vendor/tailwind.css", vo / "tw.css")
for lic, name in [("vendor/LICENSE-tailwindcss", "LICENSE-tailwindcss"), ("vendor/chartjs/LICENSE.md", "LICENSE-chartjs.md"),
                  ("vendor/katex/LICENSE", "LICENSE-katex")]:
    shutil.copyfile(SRC / lic, vo / name)
cfg = (SRC / "vendor/tailwind.config.cjs").read_text(encoding="utf-8").replace(
    "content: ['./m300.html', './impressum.html', './datenschutz.html']", f"content: ['./{PAGE}']")
(vo / "tailwind.config.cjs").write_text(cfg, encoding="utf-8")
shutil.copyfile(SRC / "vendor/tailwind.input.css", vo / "tailwind.input.css")
(vo / "build-tailwind.sh").write_text(
    "#!/bin/sh\n# Baut qa/vendor-offline/tw.css (nur für render_audit --vendor; live lädt die Seite Tailwind per CDN bzw. /vendor).\n"
    "set -e\ncd \"$(dirname \"$0\")/../..\"\n"
    "npx --yes tailwindcss@3.4.19 -c qa/vendor-offline/tailwind.config.cjs -i qa/vendor-offline/tailwind.input.css -o qa/vendor-offline/tw.css --minify\n",
    encoding="utf-8")
print("  qa/vendor-offline/ (KaTeX 0.16.11, Chart.js 4.4.4, tw.css, Lizenzen, Build-Skript)")
