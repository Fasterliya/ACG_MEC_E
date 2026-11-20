#Requires -Version 5.1
<#
  rebuild_msk_missions.ps1
  Re-lays out missions/MSK_missions.txt into PLAN B (funnel) geometry.
  Only id / position / required_missions are rewritten; trigger & effect
  bodies are copied byte-for-byte from the current file.
  Pure ASCII source (Windows PowerShell 5.1 reads .ps1 as ANSI).
#>
[CmdletBinding()]
param(
    [string]$InPath,
    [string]$OutPath,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $InPath) { $InPath = Join-Path $root 'missions\MSK_missions.txt' }
if (-not $OutPath) { $OutPath = $InPath }

# ---------------------------------------------------------------- layout table
# new = "<slot>_<pos>"; old = source block in the current file ('NEW' = hand-made)
$layout = @(
    @{ slot = 1; pos = 1; new = '1_1';  old = '1_1'; req = @() }
    @{ slot = 1; pos = 2; new = '1_2';  old = '2_2'; req = @('1_1') }
    @{ slot = 1; pos = 3; new = '1_3';  old = '1_3'; req = @('1_2') }
    @{ slot = 1; pos = 4; new = '1_4';  old = '1_4'; req = @('1_3') }
    @{ slot = 1; pos = 5; new = '1_5';  old = '1_5'; req = @('1_4') }
    @{ slot = 1; pos = 6; new = '1_6';  old = '1_6'; req = @('1_5') }
    @{ slot = 1; pos = 7; new = '1_7';  old = '1_7'; req = @('1_6') }
    @{ slot = 1; pos = 8; new = '1_8';  old = '1_8'; req = @('1_7') }

    @{ slot = 2; pos = 2; new = '2_2';  old = '2_8'; req = @('1_1') }
    @{ slot = 2; pos = 3; new = '2_3';  old = '2_9'; req = @('2_2') }
    @{ slot = 2; pos = 4; new = '2_4';  old = '4_6'; req = @('3_3') }
    @{ slot = 2; pos = 5; new = '2_5';  old = '4_7'; req = @('1_4') }
    @{ slot = 2; pos = 7; new = '2_7';  old = '4_8'; req = @('3_6') }

    @{ slot = 3; pos = 1; new = '3_1';  old = '4_1'; req = @() }
    @{ slot = 3; pos = 2; new = '3_2';  old = '4_2'; req = @('3_1') }
    @{ slot = 3; pos = 3; new = '3_3';  old = '3_3'; req = @('3_2') }
    @{ slot = 3; pos = 4; new = '3_4';  old = '3_4'; req = @('3_3') }
    @{ slot = 3; pos = 5; new = '3_5';  old = '3_5'; req = @('3_4') }
    @{ slot = 3; pos = 6; new = '3_6';  old = '3_6'; req = @('3_5') }
    @{ slot = 3; pos = 7; new = '3_7';  old = '2_5'; req = @('1_6') }
    @{ slot = 3; pos = 8; new = '3_8';  old = '2_6'; req = @('3_7') }
    @{ slot = 3; pos = 9; new = '3_9';  old = 'NEW'; req = @('3_8', '1_8', '5_8') }

    @{ slot = 4; pos = 2; new = '4_2';  old = '4_3'; req = @('3_1') }
    @{ slot = 4; pos = 3; new = '4_3';  old = '4_4'; req = @('4_2') }
    @{ slot = 4; pos = 4; new = '4_4';  old = '4_5'; req = @('4_3') }
    @{ slot = 4; pos = 5; new = '4_5';  old = '2_7'; req = @('4_4') }
    @{ slot = 4; pos = 6; new = '4_6';  old = '5_6'; req = @('4_5') }
    @{ slot = 4; pos = 7; new = '4_7';  old = '5_7'; req = @('4_6') }
    @{ slot = 4; pos = 8; new = '4_8';  old = '5_8'; req = @('4_7') }

    @{ slot = 5; pos = 1; new = '5_1';  old = '3_1'; req = @() }
    @{ slot = 5; pos = 2; new = '5_2';  old = '2_3'; req = @('5_1') }
    @{ slot = 5; pos = 3; new = '5_3';  old = '2_4'; req = @('5_2') }
    @{ slot = 5; pos = 4; new = '5_4';  old = '5_1'; req = @('5_3') }
    @{ slot = 5; pos = 5; new = '5_5';  old = '5_2'; req = @('5_4') }
    @{ slot = 5; pos = 6; new = '5_6';  old = '5_3'; req = @('5_5') }
    @{ slot = 5; pos = 7; new = '5_7';  old = '5_4'; req = @('5_6') }
    @{ slot = 5; pos = 8; new = '5_8';  old = '5_5'; req = @('5_7') }
)

$errors = New-Object System.Collections.ArrayList

# ---------------------------------------------------------------- parse blocks
$lines = [System.IO.File]::ReadAllLines($InPath, [System.Text.Encoding]::UTF8)
$blocks = @{}
$i = 0
while ($i -lt $lines.Count) {
    if ($lines[$i] -match '^\s*(MSK_missions_\d+_\d+)\s*=\s*\{\s*$') {
        $id = $matches[1]
        $start = $i
        $depth = 0
        $j = $start
        while ($j -lt $lines.Count) {
            $depth += ([regex]::Matches($lines[$j], '\{')).Count
            $depth -= ([regex]::Matches($lines[$j], '\}')).Count
            if ($depth -le 0) { break }
            $j++
        }
        if ($j -ge $lines.Count) { [void]$errors.Add("unterminated block $id"); break }
        $blocks[$id] = @($lines[$start..$j])
        $i = $j + 1
    } else {
        $i++
    }
}

foreach ($l in $layout) {
    if ($l.old -ne 'NEW' -and -not $blocks.ContainsKey("MSK_missions_$($l.old)")) {
        [void]$errors.Add("missing source block MSK_missions_$($l.old) (for new $($l.new))")
    }
}

# ---------------------------------------------------------------- rewrite block
function Rewrite-Block {
    param($BlockLines, [string]$NewId, [string]$Pos, $Req)

    $hasReq = $false
    foreach ($ln in $BlockLines) { if ($ln -match '^\s*required_missions\s*=') { $hasReq = $true } }

    if ($Req.Count -gt 0) { $refs = ($Req | ForEach-Object { "MSK_missions_$_" }) -join ' ' }

    $out = New-Object System.Collections.ArrayList
    $first = $true
    foreach ($ln in $BlockLines) {
        if ($first) {
            [void]$out.Add("`tMSK_missions_$NewId = {")
            $first = $false
            continue
        }
        if ($ln -match '^\s*position\s*=') {
            [void]$out.Add("`t`tposition = $Pos")
            if ($Req.Count -gt 0 -and -not $hasReq) {
                [void]$out.Add("`t`trequired_missions = { $refs }")
            }
            continue
        }
        if ($ln -match '^\s*required_missions\s*=') {
            if ($Req.Count -gt 0) { [void]$out.Add("`t`trequired_missions = { $refs }") }
            continue
        }
        [void]$out.Add($ln)
    }
    return $out
}

# ---------------------------------------------------------------- new finale
$finale = @(
    "`tMSK_missions_3_9 = {"
    "`t`ticon = mission_empire"
    "`t`tposition = 9"
    "`t`trequired_missions = { MSK_missions_3_8 MSK_missions_1_8 MSK_missions_5_8 }"
    "`t`ttrigger = {"
    "`t`t`tnum_of_cities = 120"
    "`t`t`tprestige = 75"
    "`t`t}"
    "`t`teffect = {"
    "`t`t`tadd_prestige = 50"
    "`t`t`tadd_splendor = 500"
    "`t`t`tadd_stability = 2"
    "`t`t`tadd_army_tradition = 10"
    "`t`t}"
    "`t}"
)

# ---------------------------------------------------------------- emit
$doc = New-Object System.Collections.ArrayList
for ($slot = 1; $slot -le 5; $slot++) {
    [void]$doc.Add("MSK_missions_$slot = {")
    [void]$doc.Add("`tslot = $slot")
    [void]$doc.Add("`tgeneric = no")
    [void]$doc.Add("`tai = yes")
    [void]$doc.Add("`tpotential = {")
    [void]$doc.Add("`t`ttag = MSK")
    [void]$doc.Add("`t}")
    [void]$doc.Add("`thas_country_shield = yes")

    $group = @($layout | Where-Object { $_.slot -eq $slot } | Sort-Object { [int]$_.pos })
    foreach ($l in $group) {
        [void]$doc.Add("`t")
        if ($l.old -eq 'NEW') {
            foreach ($fl in $finale) { [void]$doc.Add($fl) }
        } else {
            $blk = Rewrite-Block -BlockLines $blocks["MSK_missions_$($l.old)"] -NewId $l.new -Pos ([string]$l.pos) -Req $l.req
            foreach ($b in $blk) { [void]$doc.Add($b) }
        }
    }
    if ($slot -lt 5) {
        [void]$doc.Add("}")
        [void]$doc.Add("")
    } else {
        [void]$doc.Add("}")
    }
}

# ---------------------------------------------------------------- validate
$text = $doc -join "`r`n"
$ids = [regex]::Matches($text, '(?m)^\tMSK_missions_(\d+_\d+) = \{') | ForEach-Object { $_.Groups[1].Value }
$dup = $ids | Group-Object | Where-Object { $_.Count -gt 1 }
foreach ($d in $dup) { [void]$errors.Add("duplicate id $($d.Name)") }

foreach ($m in [regex]::Matches($text, '(?m)^\t\trequired_missions = \{ ([^}]*) \}')) {
    foreach ($r in ($m.Groups[1].Value -split '\s+')) {
        if ($r -and -not ($ids -contains ($r -replace '^MSK_missions_', ''))) { [void]$errors.Add("dangling reference $r") }
    }
}

# slot / position / delta-row rule check
$idx = @{}
foreach ($l in $layout) {
    $idx["MSK_missions_$($l.new)"] = @{ slot = [int]$l.slot; pos = [int]$l.pos }
}
foreach ($l in $layout) {
    foreach ($r in $l.req) {
        $a = $idx["MSK_missions_$($l.new)"]
        $b = $idx["MSK_missions_$r"]
        if (-not $b) { continue }
        if ($a.slot -eq $b.slot) {
            if (($a.pos - $b.pos) -lt 1) { [void]$errors.Add("$($l.new): same-column parent $r is not above") }
        } else {
            if (($a.pos - $b.pos) -ne 1) { [void]$errors.Add("$($l.new): cross-column parent $r delta-row=$($a.pos - $b.pos)") }
        }
    }
}

Write-Output ("blocks parsed : " + $blocks.Count)
Write-Output ("missions out  : " + $ids.Count)
Write-Output ("unique ids    : " + ($ids | Sort-Object -Unique).Count)
Write-Output ("text length   : " + $text.Length)

if ($errors.Count -gt 0) {
    Write-Output "[ERRORS]"
    Write-Output ($errors -join "`n")
    exit 1
}

if ($DryRun) {
    Write-Output "[DRY RUN] no file written"
    exit 0
}

$backup = Join-Path (Split-Path -Parent $InPath) 'MSK_missions.txt.bak'
if (-not (Test-Path $backup)) {
    Copy-Item -LiteralPath $InPath -Destination $backup
    Write-Output "backup: $backup"
}

[System.IO.File]::WriteAllText($OutPath, $text, (New-Object System.Text.UTF8Encoding($false)))
Write-Output "written: $OutPath"
Write-Output "[OK] no errors"
