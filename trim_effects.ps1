function Trim-Effect($txt) {
    $lines = $txt -split "`r`n"
    $allItems = @()
    $depth = 0; $buf = @()
    foreach ($line in $lines) {
        $t = $line.Trim()
        if ($t -match '\{') { $depth++ }
        if ($t -match '\}') { $depth-- }
        $buf += $line
        if ($depth -le 0 -and $buf.Count -gt 0 -and $t.Length -gt 0) {
            $item = ($buf -join "`r`n").Trim()
            if ($item -notmatch '^$') { $allItems += $item }
            $buf = @()
        }
    }
    if ($buf.Count -gt 0) { $allItems += ($buf -join "`r`n").Trim() }
    $claims = @(); $rewards = @()
    foreach ($it in $allItems) {
        if ($it -match 'add_permanent_claim|add_claim|set_country_flag|set_global_flag') {
            $claims += $it
        } else {
            $rewards += $it
        }
    }
    $modIdx = -1; $splIdx = -1; $presIdx = -1; $stabIdx = -1; $reformIdx = -1
    $capIdx = -1; $yrIdx = -1; $trIdx = -1; $atIdx = -1; $ntIdx = -1
    $mpIdx = -1; $mcIdx = -1; $bldIdx = -1
    for ($i = 0; $i -lt $rewards.Count; $i++) {
        $r = $rewards[$i]
        if ($r -match 'add_country_modifier') { $modIdx = $i }
        elseif ($r -match 'add_splendor') { $splIdx = $i }
        elseif ($r -match 'add_prestige') { $presIdx = $i }
        elseif ($r -match 'add_stability') { $stabIdx = $i }
        elseif ($r -match 'change_government_reform_progress') { $reformIdx = $i }
        elseif ($r -match 'capital_scope') { $capIdx = $i }
        elseif ($r -match 'add_years_of_income') { $yrIdx = $i }
        elseif ($r -match 'add_treasury') { $trIdx = $i }
        elseif ($r -match 'add_army_tradition') { $atIdx = $i }
        elseif ($r -match 'add_navy_tradition') { $ntIdx = $i }
        elseif ($r -match 'add_manpower') { $mpIdx = $i }
        elseif ($r -match 'add_mercantilism') { $mcIdx = $i }
        elseif ($r -match 'add_building') { $bldIdx = $i }
    }
    $kept = @()
    if ($modIdx -ge 0) { $kept += $rewards[$modIdx] }
    if ($splIdx -ge 0) { $kept += $rewards[$splIdx] }
    if ($presIdx -ge 0) { $kept += $rewards[$presIdx] }
    $slots = 5 - $kept.Count
    if ($slots -le 0) { $slots = 0 }
    $prio = @{}
    if ($stabIdx -ge 0) { $prio[$stabIdx] = 90 }
    if ($capIdx -ge 0) { $prio[$capIdx] = 85 }
    if ($reformIdx -ge 0) { $prio[$reformIdx] = 80 }
    if ($yrIdx -ge 0) { $prio[$yrIdx] = 70 }
    if ($mpIdx -ge 0) { $prio[$mpIdx] = 60 }
    if ($atIdx -ge 0) { $prio[$atIdx] = 55 }
    if ($ntIdx -ge 0) { $prio[$ntIdx] = 50 }
    if ($trIdx -ge 0) { $prio[$trIdx] = 40 }
    if ($mcIdx -ge 0) { $prio[$mcIdx] = 30 }
    if ($bldIdx -ge 0) { $prio[$bldIdx] = 20 }
    $sorted = $prio.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First $slots | Sort-Object Key
    foreach ($s in $sorted) { $kept += $rewards[$s.Key] }
    $result = @()
    $result += $claims
    $result += $kept
    return ($result -join "`r`n").Trim()
}

function ProcessFile($filePath) {
    $raw = [System.IO.File]::ReadAllText($filePath)
    $sb = [System.Text.StringBuilder]::new()
    $i = 0
    while ($i -lt $raw.Length) {
        $efIdx = $raw.IndexOf('effect = {', $i)
        if ($efIdx -lt 0) { [void]$sb.Append($raw.Substring($i)); break }
        [void]$sb.Append($raw.Substring($i, $efIdx - $i))
        $brace = 1; $j = $efIdx + 11
        while ($j -lt $raw.Length -and $brace -gt 0) {
            if ($raw[$j] -eq '{') { $brace++ }
            if ($raw[$j] -eq '}') { $brace-- }
            $j++
        }
        $inner = $raw.Substring($efIdx + 10, $j - $efIdx - 11)
        $trimmed = Trim-Effect $inner
        [void]$sb.Append("effect = {`r`n$trimmed`r`n`t}")
        $i = $j
    }
    [System.IO.File]::WriteAllText($filePath, $sb.ToString())
}

$files = @(
    "F:\Paradox Interactive\Europa Universalis IV\mod\1\missions\KSN_missions.txt",
    "F:\Paradox Interactive\Europa Universalis IV\mod\1\missions\HKH_missions.txt"
)
foreach ($f in $files) {
    Write-Output "Processing $f"
    if (Test-Path $f) { ProcessFile $f }
    Write-Output "Done"
}
