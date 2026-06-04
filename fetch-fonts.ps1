# ════════════════════════════════════════════════════════════════
#  fetch-fonts.ps1 — Google Fonts DSGVO-konform self-hosten
#  Lädt Inter / Space Grotesk / JetBrains Mono lokal herunter,
#  erzeugt fonts.css und stellt alle HTML-Dateien auf lokale
#  Einbindung um (keine IP-Übermittlung an Google mehr).
#
#  Ausführen:  pwsh "C:\Users\User\AI Financecoach\publish-rente\fetch-fonts.ps1"
#  Danach:     git add -A; git commit -m "fonts: self-hosted"; netlify deploy --prod --dir .
# ════════════════════════════════════════════════════════════════
$ErrorActionPreference = 'Stop'
$base     = $PSScriptRoot
$fontsDir = Join-Path $base 'fonts'
New-Item -ItemType Directory -Force $fontsDir | Out-Null

$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
$families = @(
  'Inter:wght@300;400;500;600;700;800;900',
  'Space+Grotesk:wght@400;500;600;700',
  'JetBrains+Mono:wght@400;500;600'
)

$cssOut = New-Object System.Collections.Generic.List[string]
$counter = @{}

foreach ($fam in $families) {
  $url = "https://fonts.googleapis.com/css2?family=$fam&display=swap"
  Write-Host "→ Lade CSS: $fam"
  $css = (Invoke-WebRequest -Uri $url -UserAgent $ua -UseBasicParsing).Content

  foreach ($b in [regex]::Matches($css, '@font-face\s*\{[^}]*\}')) {
    $blk = $b.Value
    $m = [regex]::Match($blk, 'src:\s*url\((https://[^)]+\.woff2)\)')
    if (-not $m.Success) { continue }
    $fontUrl  = $m.Groups[1].Value
    $famName  = ([regex]::Match($blk, "font-family:\s*'([^']+)'").Groups[1].Value) -replace '\s',''
    $weight   = [regex]::Match($blk, 'font-weight:\s*(\d+)').Groups[1].Value
    $key      = "$famName-$weight"
    if (-not $counter.ContainsKey($key)) { $counter[$key] = 0 }
    $idx      = $counter[$key]++
    $fname    = "$famName-$weight-$idx.woff2"

    Write-Host "   ↓ $fname"
    Invoke-WebRequest -Uri $fontUrl -OutFile (Join-Path $fontsDir $fname) -UseBasicParsing

    $blk = $blk -replace [regex]::Escape($fontUrl), "fonts/$fname"
    $cssOut.Add($blk)
  }
}

# fonts.css schreiben
$header = "/* Self-hosted Fonts — generiert von fetch-fonts.ps1. Keine Google-CDN-Abrufe. */`n"
Set-Content -Path (Join-Path $base 'fonts.css') -Value ($header + ($cssOut -join "`n`n")) -Encoding utf8NoBOM
Write-Host "✓ fonts.css geschrieben ($($cssOut.Count) @font-face-Regeln)"

# HTML-Dateien auf lokale Einbindung umstellen
$linkPattern = '<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">'
foreach ($f in @('index.html','modul.html','impressum.html','datenschutz.html')) {
  $p = Join-Path $base $f
  if (-not (Test-Path $p)) { continue }
  $h = Get-Content $p -Raw
  $h = $h -replace '\s*<link rel="preconnect" href="https://fonts\.googleapis\.com">',''
  $h = $h -replace '\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>',''
  $h = [regex]::Replace($h, $linkPattern, '<link rel="stylesheet" href="fonts.css">')
  Set-Content -Path $p -Value $h -Encoding utf8NoBOM -NoNewline
  Write-Host "✓ umgestellt: $f"
}

Write-Host "`nFERTIG. Nächste Schritte:"
Write-Host '  cd "C:\Users\User\AI Financecoach\publish-rente"'
Write-Host '  git add -A; git commit -m "fonts: Google Fonts self-hosted (DSGVO)"; netlify deploy --prod --dir .'
