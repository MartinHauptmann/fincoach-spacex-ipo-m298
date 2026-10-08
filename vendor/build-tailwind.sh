#!/bin/sh
# Baut vendor/tailwind.css aus den Modulseiten (Tailwind v3.4, Version fest).
set -e
cd "$(dirname "$0")/.."
npx --yes tailwindcss@3.4.19 -c vendor/tailwind.config.cjs -i vendor/tailwind.input.css -o vendor/tailwind.css --minify
