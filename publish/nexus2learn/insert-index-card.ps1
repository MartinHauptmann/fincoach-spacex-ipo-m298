<#
.SYNOPSIS
  Fuegt die PISA-Startseiten-Karte (out\snippets\index-html-card.html, Teil vor "Optional: Hero-Pill") als erste Karte
  in das Karten-Grid der Sektion "AKTUELL · FINCOACH AI ANALYSEN" von publish-nexus2learn\index.html ein.
  Idempotent (bereits vorhanden -> Hinweis), erhaelt Zeilenenden, schreibt UTF-8 ohne BOM.
.EXAMPLE
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\insert-index-card.ps1" -DryRun
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\insert-index-card.ps1"
#>
param(
  [string]$Repo = 'C:\Users\User\fincoach-spacex-ipo-m298',
  [string]$Pkg  = 'C:\Users\User\AI Financecoach\publish-nexus2learn',
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$idx  = Join-Path $Pkg 'index.html'
$snip = Join-Path $Repo 'publish\nexus2learn\out\snippets\index-html-card.html'
foreach ($p in @($idx, $snip)) { if (-not (Test-Path $p)) { throw "Nicht gefunden: $p" } }
$raw = [System.IO.File]::ReadAllText($idx)
$nl = if ($raw -match "`r`n") { "`r`n" } else { "`n" }
$s = $raw.Replace("`r`n", "`n")
if ($s.Contains('BILDUNG &amp; DATENKOMPETENZ &middot; M479')) { Write-Host "Karte bereits vorhanden: $idx" -ForegroundColor Yellow; exit 0 }

$card = ([System.IO.File]::ReadAllText($snip)).Replace("`r`n", "`n").Split('<!-- Optional: Hero-Pill -->')[0]
$lines = $card.Trim("`n").Split("`n") | Where-Object { -not ($_.StartsWith('<!--') -or $_.StartsWith('     Karte ist')) }
$card = ($lines | ForEach-Object { if ($_.Length) { '    ' + $_ } else { $_ } }) -join "`n"

$anchor = "  <div class=`"grid md:grid-cols-3 gap-4`">`n    <a href=`"module/modul-m478-warren-buffett-investment-dashboard.html`" class=`"card p-6 block"
$n = ([regex]::Matches($s, [regex]::Escape($anchor))).Count
if ($n -ne 1) {
  Write-Host "Anker (Karten-Grid vor der M478-Karte) $n-mal gefunden, erwartet 1. index.html hat sich geaendert - bitte melden." -ForegroundColor Red
  exit 1
}
$s = $s.Replace($anchor, "  <div class=`"grid md:grid-cols-3 gap-4`">`n" + $card + "`n    <a href=`"module/modul-m478-warren-buffett-investment-dashboard.html`" class=`"card p-6 block")
if ($DryRun) { Write-Host "DryRun: Anker gefunden, Karte (11 Zeilen) wuerde vor M478 eingefuegt in $idx" -ForegroundColor Cyan; exit 0 }
[System.IO.File]::WriteAllText($idx, $s.Replace("`n", $nl), [System.Text.UTF8Encoding]::new($false))
Write-Host "Eingefuegt: $idx (Zeilenende $(if ($nl -eq "`r`n") {'CRLF'} else {'LF'}))" -ForegroundColor Green
