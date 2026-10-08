# Selbst gehostete Bibliotheken (L20)

Keine Abrufe von Drittanbieter-CDNs: keine IP-Übertragung an Dritte und kein Einwilligungsbedarf für diese Ressourcen.

| Datei | Bibliothek | Version | Lizenz |
|---|---|---|---|
| `chartjs/chart.umd.min.js` | Chart.js | 4.4.4 | MIT (`chartjs/LICENSE.md`) |
| `katex/katex.min.js`, `katex/auto-render.min.js`, `katex/katex.min.css`, `katex/fonts/*.woff2` | KaTeX | 0.16.47 | MIT (`katex/LICENSE`) |
| `tailwind.css` | Tailwind CSS (statisch gebaut) | 3.4.19 | MIT (`LICENSE-tailwindcss`) |

Tailwind neu bauen: `sh vendor/build-tailwind.sh` (Konfiguration `vendor/tailwind.config.cjs`).

## Schriften (`fonts/`)

Inter, Space Grotesk und JetBrains Mono stehen unter der SIL Open Font License 1.1. Die Lizenztexte liegen in
`fonts/LICENSE-*-OFL.txt` (Pflicht bei Weitergabe, L32).

## Versionspflege (L32)

KaTeX wurde am 2026-10-08 von 0.16.9 auf 0.16.47 angehoben. Grund: Für Versionen vor 0.16.10 gibt es GitHub-Advisories
vom März 2024. Vor jedem Release die Versionen dieser Tabelle gegen die Sicherheitshinweise der Projekte prüfen.
