<#
.SYNOPSIS
  Gezielter Freigabe-Transfer NUR der PISA-Serie (M479-M482) in das Publish-Paket (nexus2learn-website).
  Macht fuer diese vier Module exakt das, was tools/release-modules.ps1 tut (Link-Rewrite auf ../, Companions
  provenance/ und assets/mNNN/ mitkopieren, module/index.json-Eintraege, Teaser, OG-Bild, Sitemap, Allowlist),
  ohne andere Module anzufassen. Hintergrund: release-modules.ps1 entfernt alle HTMLs in module/, die es nicht
  in Root-Registry + Allowlist findet; der Root kennt acht oeffentliche Module (M449, M465-M478) nicht.
.PARAMETER Repo    Lokaler Klon von fincoach-spacex-ipo-m298 (enthaelt publish\nexus2learn\out)
.PARAMETER Pkg     Publish-Paket = Repo nexus2learn-website (publish-nexus2learn im FinCoach-Root)
.PARAMETER DryRun  Nur anzeigen, nichts schreiben
.EXAMPLE
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\release-pisa.ps1" -DryRun
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\release-pisa.ps1"
#>
param(
  [string]$Repo = 'C:\Users\User\fincoach-spacex-ipo-m298',
  [string]$Pkg  = 'C:\Users\User\AI Financecoach\publish-nexus2learn',
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
$out   = Join-Path $Repo 'publish\nexus2learn\out'
$media = Join-Path $Repo 'publish\nexus2learn\media'
$modDir = Join-Path $Pkg 'module'
$entries = Get-Content (Join-Path $out 'snippets\index-json-entries.json') -Raw -Encoding utf8 | ConvertFrom-Json
foreach ($p in @($out, $media, $modDir, (Join-Path $Pkg 'modules-public.json'), (Join-Path $modDir 'index.json'), (Join-Path $Pkg 'sitemap.xml'))) {
  if (-not (Test-Path $p)) { throw "Nicht gefunden: $p" }
}
$map = [ordered]@{
  'href="modul-matrix.html"' = 'href="../module.html"'
  'href="infe-cat.html"'     = 'href="../infe-cat.html"'
  'href="index.html"'        = 'href="../index.html"'
  'href="datenschutz.html"'  = 'href="../datenschutz.html"'
  'href="impressum.html"'    = 'href="../impressum.html"'
}
$rxAsset = [regex]'(?:src|href)=["'']((?:services|templates|assets|img|images|provenance)/[^"''?#]+)["'']'
$copied = 0; $assets = 0
foreach ($e in $entries) {
  $src = Join-Path $out $e.file
  if (-not (Test-Path $src)) { throw "Modul fehlt im Paket: $src" }
  $html = Get-Content $src -Raw -Encoding utf8
  foreach ($k in $map.Keys) { $html = $html.Replace($k, $map[$k]) }
  if ($html -notmatch 'href="\.\./module\.html"') { throw "Katalog-Ruecklink fehlt in $($e.file)" }
  $dst = Join-Path $modDir $e.file
  Write-Host ("  {0} -> {1}" -f $e.file, $dst) -ForegroundColor Green
  if (-not $DryRun) { [System.IO.File]::WriteAllText($dst, $html, $utf8) }
  $copied++
  # Companions: (a) alles, was die HTML per src/href referenziert, (b) das komplette Datenpaket assets/mNNN/
  # (im M-DBOM als Artefakte gelistet, teils nur eingebettet und nicht verlinkt), (c) provenance/mNNN.dbom.json
  $rels = [System.Collections.Generic.List[string]]::new()
  foreach ($mm in $rxAsset.Matches($html)) { $rels.Add($mm.Groups[1].Value) }
  $idL = $e.id.ToLower()
  $pkgDir = Join-Path $out ("assets\{0}" -f $idL)
  if (Test-Path $pkgDir) {
    foreach ($f in Get-ChildItem $pkgDir -File -Recurse) {
      $rels.Add(("assets/{0}/{1}" -f $idL, $f.FullName.Substring($pkgDir.Length + 1).Replace('\','/')))
    }
  }
  $rels.Add(("provenance/{0}.dbom.json" -f $idL))
  foreach ($rel in ($rels | Sort-Object -Unique)) {
    $aSrc = Join-Path $out $rel
    if (-not (Test-Path $aSrc)) { if ($rel -like 'provenance/*') { throw "DBOM fehlt im Paket: $aSrc" } else { continue } }
    $aDst = Join-Path $modDir $rel
    Write-Host ("     companion {0}" -f $rel) -ForegroundColor DarkGray
    if (-not $DryRun) {
      $aDir = Split-Path $aDst -Parent
      if (-not (Test-Path $aDir)) { New-Item -ItemType Directory -Force -Path $aDir | Out-Null }
      Copy-Item $aSrc $aDst -Force
    }
    $assets++
  }
  # Teaser (Fallback zu generate-teasers.mjs)
  $teaser = Join-Path $media ("{0}.jpg" -f $e.id.ToLower())
  if (Test-Path $teaser) {
    $tDir = Join-Path $modDir 'assets\teaser'
    if (-not $DryRun) { if (-not (Test-Path $tDir)) { New-Item -ItemType Directory -Force -Path $tDir | Out-Null }; Copy-Item $teaser (Join-Path $tDir ("{0}.jpg" -f $e.id.ToLower())) -Force }
    Write-Host ("     teaser   assets/teaser/{0}.jpg" -f $e.id.ToLower()) -ForegroundColor DarkGray
  }
}
# OG-Bild der Serie
$og = Join-Path $media 'pisa-2025-serie-1200x627.png'
if (Test-Path $og) {
  $ogDir = Join-Path $Pkg 'assets\og'
  if (-not $DryRun) { if (-not (Test-Path $ogDir)) { New-Item -ItemType Directory -Force -Path $ogDir | Out-Null }; Copy-Item $og (Join-Path $ogDir 'pisa-2025-serie-1200x627.png') -Force }
  Write-Host "  OG-Bild -> assets/og/pisa-2025-serie-1200x627.png" -ForegroundColor Green
}
# module/index.json: vier Eintraege ersetzen/ergaenzen, nach Nummer sortiert
$idxP = Join-Path $modDir 'index.json'
$idx = @(Get-Content $idxP -Raw -Encoding utf8 | ConvertFrom-Json)
$ids = @($entries | ForEach-Object { $_.id })
$idx = @($idx | Where-Object { $ids -notcontains $_.id })
foreach ($e in $entries) { $idx += [pscustomobject]@{ id=$e.id; number=[int]$e.number; title=$e.title; file=$e.file; released=$true } }
$idx = @($idx | Sort-Object number)
Write-Host ("  index.json: {0} Eintraege, davon frei: {1}" -f $idx.Count, @($idx | Where-Object { $_.released }).Count) -ForegroundColor Green
if (-not $DryRun) { [System.IO.File]::WriteAllText($idxP, ($idx | ConvertTo-Json -Depth 4), $utf8) }
# Allowlist
$allowP = Join-Path $Pkg 'modules-public.json'
$allow = @(Get-Content $allowP -Raw -Encoding utf8 | ConvertFrom-Json | ForEach-Object { "$_".ToUpper().Trim() })
$added = @($ids | Where-Object { $allow -notcontains $_ })
if ($added.Count) { $allow += $added; Write-Host ("  Allowlist +{0}" -f ($added -join ', ')) -ForegroundColor Green }
if (-not $DryRun -and $added.Count) { [System.IO.File]::WriteAllText($allowP, (ConvertTo-Json @($allow)), $utf8) }
# Sitemap
$smP = Join-Path $Pkg 'sitemap.xml'
$sm = Get-Content $smP -Raw -Encoding utf8
$today = (Get-Date).ToString('yyyy-MM-dd'); $lines = ''
foreach ($e in $entries) {
  $loc = "https://www.nexus2learn.com/module/$($e.file)"
  if ($sm -notmatch [regex]::Escape($loc)) { $lines += "  <url><loc>$loc</loc><lastmod>$today</lastmod><priority>0.8</priority></url>`n" }
}
if ($lines) { $sm = $sm.Replace('</urlset>', $lines + '</urlset>'); Write-Host "  Sitemap: 4 Eintraege ergaenzt" -ForegroundColor Green; if (-not $DryRun) { [System.IO.File]::WriteAllText($smP, $sm, $utf8) } }
Write-Host ("OK{0} · Module: {1} · Companions: {2}" -f ($(if ($DryRun) { ' (DryRun, nichts geschrieben)' } else { '' })), $copied, $assets) -ForegroundColor Cyan
Write-Host "Naechster Schritt: Startseiten-Karte (out\snippets\index-html-card.html) optional, dann git add/commit/push im Publish-Paket."
