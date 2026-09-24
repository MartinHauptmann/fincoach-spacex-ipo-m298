<#
.SYNOPSIS
  Wendet patches/run-audit-base-aware.patch textbasiert auf scripts/styleguide/run-audit.mjs an
  (robust gegen CRLF/LF; erhaelt die vorhandenen Zeilenenden). Idempotent: bereits gepatcht -> Hinweis, keine Aenderung.
.EXAMPLE
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\patches\apply-run-audit-patch.ps1"
  pwsh "C:\Users\User\fincoach-spacex-ipo-m298\publish\nexus2learn\patches\apply-run-audit-patch.ps1" -DryRun
#>
param(
  [string]$Root = 'C:\Users\User\AI Financecoach',
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$p = Join-Path $Root 'scripts\styleguide\run-audit.mjs'
if (-not (Test-Path $p)) { throw "Nicht gefunden: $p" }
$raw = [System.IO.File]::ReadAllText($p)
$nl = if ($raw -match "`r`n") { "`r`n" } else { "`n" }
$s = $raw.Replace("`r`n", "`n")

if ($s.Contains('faceFamilies') -and $s.Contains('page.request.head(')) { Write-Host "Bereits gepatcht: $p" -ForegroundColor Yellow; exit 0 }

# --- Stelle 1: S-TOKEN-FONT ---
$old1 = @'
    if (!fontLink) F('S-TOKEN-FONT', 'FAIL', 'Pflicht-Schriftfamilien (Inter + Space Grotesk + JetBrains Mono) nicht alle eingebunden.');
'@
$new1 = @'
    // Self-hosted Alternative (Publish-Paket mit CSP ohne Google Fonts): @font-face-Regeln fuer alle drei Familien
    const faceFamilies = new Set();
    for (const sh of document.styleSheets) {
      try { for (const r of sh.cssRules) if (r instanceof CSSFontFaceRule) faceFamilies.add(r.style.fontFamily.replace(/["']/g, '').trim()); } catch (e) {}
    }
    const selfHosted = ['Inter', 'Space Grotesk', 'JetBrains Mono'].every(f => faceFamilies.has(f));
    if (!fontLink && !selfHosted) F('S-TOKEN-FONT', 'FAIL', 'Pflicht-Schriftfamilien (Inter + Space Grotesk + JetBrains Mono) nicht alle eingebunden.');
'@
# --- Stelle 2: S-LINK-INTERN-RESOLVE ---
$old2 = @'
  for (const href of links) {
    const cleaned = href.split('#')[0].split('?')[0];
    if (!cleaned) continue;
    const p = join(REPO, cleaned);
    if (!existsSync(p)) findings.push({ id:'S-LINK-INTERN-RESOLVE', severity:'FAIL', message:`Interner Link auf nicht existierende Datei: ${cleaned}` });
  }
'@
$new2 = @'
  const seen = new Set();
  for (const href of links) {
    const cleaned = href.split('#')[0].split('?')[0];
    if (!cleaned || seen.has(cleaned)) continue;
    seen.add(cleaned);
    let missing;
    if (BASE) {
      // Bei gesetztem --base: relativ zur geladenen Seite per HTTP pruefen
      // (Publish-Fassungen liegen in module/ und verlinken ../index.html usw.)
      try { missing = (await page.request.head(new URL(cleaned, page.url()).href)).status() >= 400; }
      catch (e) { missing = true; }
    } else {
      missing = !existsSync(join(REPO, cleaned));
    }
    if (missing) findings.push({ id:'S-LINK-INTERN-RESOLVE', severity:'FAIL', message:`Interner Link auf nicht existierende Datei: ${cleaned}` });
  }
'@
$old1 = $old1.Replace("`r`n", "`n"); $new1 = $new1.Replace("`r`n", "`n")
$old2 = $old2.Replace("`r`n", "`n"); $new2 = $new2.Replace("`r`n", "`n")

$missing = @()
if (-not $s.Contains($old1)) { $missing += 'S-TOKEN-FONT-Zeile (if (!fontLink) ...)' }
if (-not $s.Contains($old2)) { $missing += 'S-LINK-INTERN-RESOLVE-Schleife (for (const href of links) ...)' }
if ($missing.Count) {
  Write-Host "Anker nicht gefunden: $($missing -join '; ')" -ForegroundColor Red
  Write-Host "Bitte diese Zeilen aus $p schicken:" -ForegroundColor Red
  $lines = $s.Split("`n")
  foreach ($i in 0..($lines.Count-1)) { if ($lines[$i] -match "S-TOKEN-FONT|S-LINK-INTERN-RESOLVE|resolveLocalLinks") { Write-Host ("{0,5}: {1}" -f ($i+1), $lines[$i]) } }
  exit 1
}
$s = $s.Replace($old1, $new1).Replace($old2, $new2)
if ($DryRun) { Write-Host "DryRun: beide Stellen gefunden, wuerde schreiben: $p" -ForegroundColor Cyan; exit 0 }
[System.IO.File]::WriteAllText($p, $s.Replace("`n", $nl), [System.Text.UTF8Encoding]::new($false))
Write-Host "Gepatcht: $p (Zeilenende $(if ($nl -eq "`r`n") {'CRLF'} else {'LF'}))" -ForegroundColor Green
& node --check $p
if ($LASTEXITCODE -eq 0) { Write-Host "Syntax OK (node --check)" -ForegroundColor Green } else { throw "node --check meldet einen Fehler" }
