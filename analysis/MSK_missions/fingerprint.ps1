#Requires -Version 5.1
# Compute the layout fingerprint (R D C P F X J K W B Lmax) for every plan in plans.json
param([string]$DataPath)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
if (-not $DataPath) { $DataPath = Join-Path $here 'plans.json' }

$data = [System.IO.File]::ReadAllText($DataPath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json

foreach ($plan in $data.plans) {
    $nodes = $plan.nodes
    $nodeById = @{}
    foreach ($n in $nodes) { $nodeById[[string]$n.id] = $n }

    $real = @($nodes | Where-Object { $_.ghost -ne $true })
    $rows = [int]$plan.rows
    $cols = @($nodes | ForEach-Object { [int]$_.slot } | Sort-Object -Unique)

    $roots = 0
    foreach ($n in $real) { if ($null -eq $n.parent -or @($n.parent).Count -eq 0) { $roots++ } }

    $depth = 0
    foreach ($n in $nodes) { if ([int]$n.pos -gt $depth) { $depth = [int]$n.pos } }

    $profile = @()
    for ($r = 1; $r -le $depth; $r++) {
        $profile += @($nodes | Where-Object { [int]$_.pos -eq $r }).Count
    }

    $total = $nodes.Count
    $fill = [Math]::Round(100 * $total / ($cols.Count * $depth), 0)

    $links = 0; $cross = 0
    foreach ($n in $nodes) {
        if ($null -eq $n.parent) { continue }
        foreach ($p in $n.parent) {
            $links++
            if ([int]$nodeById[[string]$p].slot -ne [int]$n.slot) { $cross++ }
        }
    }
    $xr = if ($links -gt 0) { [Math]::Round(100 * $cross / $links, 0) } else { 0 }

    $joins = @($nodes | Where-Object { $null -ne $_.parent -and @($_.parent).Count -ge 2 }).Count

    $lastRow = @($nodes | Where-Object { [int]$_.pos -eq $depth }).Count

    $maxRow = ($profile | Measure-Object -Maximum).Maximum

    $childCount = @{}
    foreach ($n in $nodes) {
        if ($null -eq $n.parent) { continue }
        foreach ($p in $n.parent) {
            $k = [string]$p
            if ($childCount.ContainsKey($k)) { $childCount[$k]++ } else { $childCount[$k] = 1 }
        }
    }
    $branch = @($childCount.Keys | Where-Object { $childCount[$_] -ge 2 }).Count

    # longest chain (longest path by dependency, memo)
    $memo = @{}
    function Get-Chain([string]$id, $map, $memoRef) {
        if ($memoRef.ContainsKey($id)) { return $memoRef[$id] }
        $memoRef[$id] = 1
        $n = $map[$id]
        $best = 1
        if ($null -ne $n.parent) {
            foreach ($p in $n.parent) {
                $v = 1 + (Get-Chain ([string]$p) $map $memoRef)
                if ($v -gt $best) { $best = $v }
            }
        }
        $memoRef[$id] = $best
        return $best
    }
    $lmax = 0
    foreach ($n in $nodes) {
        $v = Get-Chain ([string]$n.id) $nodeById $memo
        if ($v -gt $lmax) { $lmax = $v }
    }

    Write-Output ("plan " + $plan.id + "  :  R=" + $roots + "  D=" + $depth + "  C=" + $cols.Count + "  P=" + ($profile -join '-') + "  F=" + $fill + "%  X=" + $xr + "%  J=" + $joins + "  K=" + $lastRow + "  W=" + $maxRow + "  B=" + $branch + "  Lmax=" + $lmax + "  nodes=" + $total)
}
