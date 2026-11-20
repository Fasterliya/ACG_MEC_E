#Requires -Version 5.1
<#
  gen_svg.ps1 - render MSK mission-tree layout proposals from plans.json
  Pure ASCII source (Windows PowerShell 5.1 reads .ps1 as ANSI):
  every non-ASCII string is loaded from plans.json as UTF-8.
#>
[CmdletBinding()]
param(
    [string]$DataPath,
    [string]$OutDir
)

$ErrorActionPreference = 'Stop'

$here = $PSScriptRoot
if (-not $here) { $here = Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $DataPath) { $DataPath = Join-Path $here 'plans.json' }
if (-not $OutDir) { $OutDir = Join-Path $here '' }

$raw = [System.IO.File]::ReadAllText($DataPath, [System.Text.Encoding]::UTF8)
$data = $raw | ConvertFrom-Json

$S = $data.strings

$colStep = 196
$rowStep = 104
$nodeW = 172
$nodeH = 62
$left = 52
$legendH = 96

function Esc([string]$s) {
    if ([string]::IsNullOrEmpty($s)) { return '' }
    return $s.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;').Replace('"', '&quot;')
}

function WrapText([string]$s, [int]$per) {
    $out = New-Object System.Collections.ArrayList
    if ([string]::IsNullOrEmpty($s)) { return $out }
    for ($i = 0; $i -lt $s.Length; $i += $per) {
        $len = [Math]::Min($per, $s.Length - $i)
        [void]$out.Add($s.Substring($i, $len))
    }
    return $out
}

$lineKeys = @()
foreach ($p in $data.lines.PSObject.Properties) { $lineKeys += $p.Name }

function LineColor($lineName) {
    $c = $data.lines.$lineName
    if ($null -eq $c) { return '#8a93a3' }
    return $c.color
}
function LineName($lineName) {
    $c = $data.lines.$lineName
    if ($null -eq $c) { return $lineName }
    return $c.name
}

$report = New-Object System.Collections.ArrayList
$svgDocs = @{}
$violations = New-Object System.Collections.ArrayList

foreach ($plan in $data.plans) {

    $rows = [int]$plan.rows
    $W = $left * 2 + 4 * $colStep + $nodeW

    $noteLines = WrapText $plan.note 78
    $nodeTop = 108 + ($noteLines.Count * 21)
    $H = $nodeTop + ($rows - 1) * $rowStep + $nodeH + $legendH

    $map = @{}
    foreach ($n in $plan.nodes) { $map[[string]$n.id] = $n }

    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
    [void]$sb.AppendLine("<svg xmlns=""http://www.w3.org/2000/svg"" viewBox=""0 0 $W $H"" width=""$W"" height=""$H"" font-family=""Microsoft YaHei, PingFang SC, Segoe UI, Arial, sans-serif"">")

    [void]$sb.AppendLine('<defs>')
    [void]$sb.AppendLine('<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#161a23"/><stop offset="0.55" stop-color="#101419"/><stop offset="1" stop-color="#0a0d12"/></linearGradient>')
    foreach ($k in $lineKeys) {
        $c = LineColor $k
        [void]$sb.AppendLine("<marker id=""arr-$k"" viewBox=""0 0 8 8"" refX=""7"" refY=""4"" markerWidth=""5.5"" markerHeight=""5.5"" orient=""auto""><path d=""M0,0 L8,4 L0,8 z"" fill=""$c""/></marker>")
    }
    [void]$sb.AppendLine('</defs>')

    [void]$sb.AppendLine("<rect x=""0"" y=""0"" width=""$W"" height=""$H"" fill=""url(#bg)""/>")
    [void]$sb.AppendLine("<rect x=""16"" y=""14"" width=""$($W-32)"" height=""$($H-28)"" rx=""14"" fill=""none"" stroke=""#2a3040"" stroke-width=""1.2""/>")

    [void]$sb.AppendLine("<text x=""$left"" y=""58"" font-size=""26"" font-weight=""700"" fill=""#f2eee3"">$(Esc $plan.name)</text>")
    $ty = 84
    foreach ($ln in $noteLines) {
        [void]$sb.AppendLine("<text x=""$left"" y=""$ty"" font-size=""12.5"" fill=""#8b95a6"">$(Esc $ln)</text>")
        $ty += 21
    }

    [void]$sb.AppendLine('<g class="links" fill="none">')
    foreach ($n in $plan.nodes) {
        if ($null -eq $n.parent) { continue }
        $cx = $left + ([int]$n.slot - 1) * $colStep + ($nodeW / 2)
        $cy = $nodeTop + ([int]$n.pos - 1) * $rowStep
        foreach ($parRef in $n.parent) {
            $p = $map[[string]$parRef]
            if ($null -eq $p) { continue }
            $ps = [int]$p.slot; $pp = [int]$p.pos
            $ns = [int]$n.slot; $np = [int]$n.pos
            if ($ps -eq $ns -and ($np - $pp) -lt 1) { [void]$violations.Add("$($plan.id): $($n.id) same-column row must increase") }
            if ($ps -ne $ns -and ($np - $pp) -ne 1) { [void]$violations.Add("$($plan.id): $($n.id) cross-column delta-row=$($np-$pp) must be 1") }
            $px = $left + ($ps - 1) * $colStep + ($nodeW / 2)
            $py = $nodeTop + ($pp - 1) * $rowStep + $nodeH
            $col = LineColor $n.line
            if ($ps -eq $ns) {
                [void]$sb.AppendLine("<path d=""M $px $py L $cx $cy"" stroke=""$col"" stroke-opacity=""0.55"" stroke-width=""2"" marker-end=""url(#arr-$($n.line))""/>")
            } else {
                $my = [Math]::Round(($py + $cy) / 2, 1)
                [void]$sb.AppendLine("<path d=""M $px $py C $px $my, $cx $my, $cx $cy"" stroke=""$col"" stroke-opacity=""0.6"" stroke-width=""2"" stroke-dasharray=""7 5"" marker-end=""url(#arr-$($n.line))""/>")
            }
        }
    }
    [void]$sb.AppendLine('</g>')

    foreach ($n in $plan.nodes) {
        $x = $left + ([int]$n.slot - 1) * $colStep
        $y = $nodeTop + ([int]$n.pos - 1) * $rowStep
        $col = LineColor $n.line
        $isGhost = ($n.ghost -eq $true)
        $isFinal = ($n.line -eq 'final')

        [void]$sb.AppendLine('<g>')
        if ($isFinal) {
            [void]$sb.AppendLine("<rect x=""$($x-6)"" y=""$($y-6)"" width=""$($nodeW+12)"" height=""$($nodeH+12)"" rx=""13"" fill=""$col"" fill-opacity=""0.10"" stroke=""$col"" stroke-opacity=""0.35"" stroke-width=""1""/>")
        }
        [void]$sb.AppendLine("<rect x=""$x"" y=""$y"" width=""$nodeW"" height=""$nodeH"" rx=""9"" fill=""#12161e"" fill-opacity=""0.95""/>")
        [void]$sb.AppendLine("<rect x=""$x"" y=""$y"" width=""$nodeW"" height=""$nodeH"" rx=""9"" fill=""$col"" fill-opacity=""0.11""/>")

        if ($isGhost) {
            [void]$sb.AppendLine("<rect x=""$x"" y=""$y"" width=""$nodeW"" height=""$nodeH"" rx=""9"" fill=""none"" stroke=""$col"" stroke-opacity=""0.55"" stroke-width=""1.4"" stroke-dasharray=""6 4""/>")
        } else {
            [void]$sb.AppendLine("<rect x=""$x"" y=""$y"" width=""$nodeW"" height=""$nodeH"" rx=""9"" fill=""none"" stroke=""$col"" stroke-opacity=""0.6"" stroke-width=""1.5""/>")
        }

        [void]$sb.AppendLine("<rect x=""$x"" y=""$($y+9)"" width=""4"" height=""$($nodeH-18)"" rx=""2"" fill=""$col""/>")

        if ($isGhost) { $titleFill = '#6d7787' } else { $titleFill = '#eceae3' }
        if ($n.label.Length -ge 9) { $titleSize = 12.8 } elseif ($n.label.Length -ge 7) { $titleSize = 13.6 } else { $titleSize = 14.5 }
        [void]$sb.AppendLine("<text x=""$($x+16)"" y=""$($y+27)"" font-size=""$titleSize"" fill=""$titleFill"">$(Esc $n.label)</text>")

        if ($isGhost) {
            if ($n.keyLabel) { $keyTxt = $n.keyLabel } else { $keyTxt = ($S.keyPending -f $n.key) }
        }
        elseif ($n.key -eq 'NEW') { $keyTxt = $S.keyNew }
        else { $keyTxt = ($S.keyMoved -f $n.key) }
        [void]$sb.AppendLine("<text x=""$($x+16)"" y=""$($y+47)"" font-size=""11"" fill=""#7b8598"">$(Esc $keyTxt)</text>")

        $slotTxt = ($S.slotRow -f $n.slot, $n.pos)
        [void]$sb.AppendLine("<text x=""$($x+$nodeW-12)"" y=""$($y+51)"" font-size=""9.5"" text-anchor=""end"" fill=""$col"" fill-opacity=""0.8"">$(Esc $slotTxt)</text>")

        [void]$sb.AppendLine('</g>')
    }

    $ly = $H - 62
    $lx = $left
    $usedLines = @()
    foreach ($k in $lineKeys) {
        foreach ($n in $plan.nodes) { if ($n.line -eq $k) { $usedLines += $k; break } }
    }
    foreach ($k in $usedLines) {
        $c = LineColor $k
        $nm = LineName $k
        [void]$sb.AppendLine("<rect x=""$lx"" y=""$($ly-9)"" width=""14"" height=""14"" rx=""3"" fill=""$c"" fill-opacity=""0.85""/>")
        [void]$sb.AppendLine("<text x=""$($lx+21)"" y=""$($ly+3)"" font-size=""12"" fill=""#9aa4b4"">$(Esc $nm)</text>")
        $lx += 21 + ($nm.Length * 12) + 34
    }
    [void]$sb.AppendLine("<text x=""$left"" y=""$($H-30)"" font-size=""11.5"" fill=""#5f6879"">$(Esc $S.legendNote)</text>")

    [void]$sb.AppendLine('</svg>')

    $svgText = $sb.ToString()
    $svgDocs[$plan.id] = $svgText
    $file = Join-Path $OutDir ("plan_" + $plan.id.ToLower() + ".svg")
    [System.IO.File]::WriteAllText($file, $svgText, (New-Object System.Text.UTF8Encoding($false)))
    [void]$report.Add("wrote $file")
}

$hb = New-Object System.Text.StringBuilder
[void]$hb.AppendLine('<!DOCTYPE html>')
[void]$hb.AppendLine('<html lang="zh-CN"><head><meta charset="utf-8">')
[void]$hb.AppendLine("<title>$(Esc $S.htmlTitle)</title>")
[void]$hb.AppendLine('<style>')
[void]$hb.AppendLine('*{box-sizing:border-box}')
[void]$hb.AppendLine('body{margin:0;background:#0a0d12;color:#e8e5dd;font-family:"Microsoft YaHei","PingFang SC",Segoe UI,sans-serif}')
[void]$hb.AppendLine('.bar{position:sticky;top:0;z-index:9;display:flex;gap:8px;align-items:center;padding:10px 16px;background:rgba(10,13,18,.92);border-bottom:1px solid #222836;flex-wrap:wrap}')
[void]$hb.AppendLine('.bar h1{font-size:15px;margin:0 14px 0 0;font-weight:700;letter-spacing:.5px;color:#f2eee3}')
[void]$hb.AppendLine('button.tab{background:#161b24;color:#c6cee0;border:1px solid #2b3342;border-radius:8px;padding:7px 14px;font-size:13px;cursor:pointer;font-family:inherit}')
[void]$hb.AppendLine('button.tab.on{background:#233047;color:#fff;border-color:#4a6da8}')
[void]$hb.AppendLine('button.pick{background:#1d2b1f;color:#bfe6c6;border:1px solid #2f5a38;border-radius:8px;padding:7px 16px;font-size:13px;cursor:pointer;margin-left:auto;font-family:inherit}')
[void]$hb.AppendLine('button.pick.on{background:#2d6b3d;color:#fff;border-color:#4fbf6a}')
[void]$hb.AppendLine('.wrap{padding:10px 14px 40px}')
[void]$hb.AppendLine('section.plan{display:none}')
[void]$hb.AppendLine('section.plan.show{display:block}')
[void]$hb.AppendLine('svg{width:100%;height:auto;max-height:82vh;display:block;margin:0 auto}')
[void]$hb.AppendLine('.hint{font-size:12px;color:#7d8590;padding:8px 16px 0;line-height:1.6}')
[void]$hb.AppendLine('</style></head><body>')
[void]$hb.AppendLine("<div class=""bar""><h1>$(Esc $S.htmlTitle)</h1>")
foreach ($plan in $data.plans) {
    if ($plan.id -eq 'A') { $on = ' on' } else { $on = '' }
    [void]$hb.AppendLine("<button class=""tab$on"" data-plan=""$($plan.id)"" onclick=""show('$($plan.id)')"">$(Esc $plan.name)</button>")
}
[void]$hb.AppendLine("<button class=""pick"" id=""pickbtn"" onclick=""pick()"">$(Esc $S.pickBtn)</button>")
[void]$hb.AppendLine('</div>')
[void]$hb.AppendLine("<div class=""hint"">$(Esc $S.htmlHint)</div>")
[void]$hb.AppendLine('<div class="wrap">')
foreach ($plan in $data.plans) {
    if ($plan.id -eq 'A') { $cls = 'plan show' } else { $cls = 'plan' }
    [void]$hb.AppendLine("<section class=""$cls"" id=""plan-$($plan.id)"" data-plan=""$($plan.id)"">")
    [void]$hb.AppendLine($svgDocs[$plan.id])
    [void]$hb.AppendLine('</section>')
}
[void]$hb.AppendLine('</div>')
[void]$hb.AppendLine('<script>')
[void]$hb.AppendLine('var current="A";')
[void]$hb.AppendLine('var doneTpl=' + '"' + $S.pickDone + '"' + ';')
[void]$hb.AppendLine('function show(p){current=p;document.querySelectorAll("section.plan").forEach(function(s){s.classList.toggle("show",s.dataset.plan===p)});document.querySelectorAll("button.tab").forEach(function(b){b.classList.toggle("on",b.dataset.plan===p)});}')
[void]$hb.AppendLine('function pick(){var b=document.getElementById("pickbtn");b.classList.add("on");b.textContent=doneTpl.replace("{0}",current);if(window.dshHTML&&window.dshHTML.send){window.dshHTML.send("pick_plan",{plan:current})}}')
[void]$hb.AppendLine('</script></body></html>')

$htmlFile = Join-Path $OutDir 'index.html'
[System.IO.File]::WriteAllText($htmlFile, $hb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
[void]$report.Add("wrote $htmlFile")

Write-Output ($report -join "`n")
if ($violations.Count -gt 0) {
    Write-Output ""
    Write-Output "[VIOLATIONS]"
    Write-Output ($violations -join "`n")
} else {
    Write-Output ""
    Write-Output "[VIOLATIONS] none - all links satisfy slot/position rules"
}
