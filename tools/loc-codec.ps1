# loc-codec.ps1 - ACG_MEC_E localisation codec (ASCII-only source; no BOM needed)
#
# localisation/*.yml in this mod use a custom CJK encoding; decode_localisation/*.yml are
# the readable UTF-8 masters. This tool converts both ways.
#
# Reverse-engineered structure (validated against every decode/encoded pair, see -Analyze):
#   CJK char (U+XXXX) -> 3 code units: [flag][lo'][hi']
#     lo = cp & 0xFF ; hi = (cp >> 8) & 0xFF
#     flag = 0x10 | (lo shifted ? 1 : 0) | (hi shifted ? 2 : 0)
#     lo' = lo + 0x0E when shifted ; hi' = hi - 0x09 when shifted
#     each byte is written as its CP1252 character (0x80-0x9F -> C1 range)
#   ASCII (<0x80) and SECTION SIGN 0xA7 pass through as a single unit.
#
# The shipped encoder uses a per-character table harvested from the existing corpus
# (see -Analyze for counts). It NEVER guesses: unknown characters abort the encode.
#
# Usage:
#   pwsh -File tools\loc-codec.ps1 -Analyze
#   pwsh -File tools\loc-codec.ps1 -Check   -Only SKR_l_english.yml
#   pwsh -File tools\loc-codec.ps1 -Encode  -Only SKR_l_english.yml
#   pwsh -File tools\loc-codec.ps1 -Decode  -Only SKR_l_english.yml
#   pwsh -File tools\loc-codec.ps1 -DumpTable tools\loc_table.json

[CmdletBinding()]
param(
    [string]$ModRoot = 'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E',
    [string]$Only,
    [string]$DumpTable,
    [switch]$Analyze,
    [switch]$Check,
    [switch]$Encode,
    [switch]$Decode
)

$ErrorActionPreference = 'Stop'

# ---------- CP1252 maps ----------
$cp1252 = [System.Text.Encoding]::GetEncoding(1252)
$ByteToChar = @{}
$CharToByte = @{}
for ($i = 0; $i -lt 256; $i++) {
    $ch = [int][char]$cp1252.GetString([byte[]]@($i))
    $ByteToChar[$i] = $ch
    if (-not $CharToByte.ContainsKey($ch)) { $CharToByte[$ch] = $i }
}

function Get-Pairs {
    $srcDir = Join-Path $ModRoot 'decode_localisation'
    $encDir = Join-Path $ModRoot 'localisation'
    $pairs = @()
    foreach ($src in Get-ChildItem $srcDir -Filter '*.yml' -File) {
        $enc = Join-Path $encDir $src.Name
        if (Test-Path $enc) { $pairs += [pscustomobject]@{ Name = $src.Name; Src = $src.FullName; Enc = $enc } }
    }
    return $pairs
}

function Get-Body([string]$line) {
    $m = [regex]::Match($line, '^(.*?: ")(.*)("\s*)$')
    if ($m.Success) { return $m.Groups[2].Value }
    return $null
}

function Test-Expandable([string]$s, [string]$e) {
    $cjk = ($s.ToCharArray() | Where-Object { [int][char]$_ -gt 127 -and [int][char]$_ -ne 0xA7 }).Count
    return (($s.Length - $cjk + 3 * $cjk) -eq $e.Length)
}

function Get-Observations {
    $charMap = @{}
    $loShift = @{}; $loNo = @{}; $hiShift = @{}; $hiNo = @{}
    $conflicts = @(); $badLines = @(); $lineCount = 0
    foreach ($p in Get-Pairs) {
        $la = Get-Content $p.Src -Encoding UTF8
        $lb = Get-Content $p.Enc -Encoding UTF8
        $n = [Math]::Min($la.Count, $lb.Count)
        for ($i = 0; $i -lt $n; $i++) {
            $s = Get-Body $la[$i]; $e = Get-Body $lb[$i]
            if ($null -eq $s -or $null -eq $e) { continue }
            if (-not (Test-Expandable $s $e)) { $badLines += ('{0}:{1}' -f $p.Name, ($i + 1)); continue }
            $lineCount++
            $pos = 0; $ok = $true
            foreach ($ch in $s.ToCharArray()) {
                $code = [int][char]$ch
                if ($code -lt 128 -or $code -eq 0xA7) { if ($e[$pos] -ne $ch) { $ok = $false; break }; $pos++; continue }
                $triple = $e.Substring($pos, 3); $pos += 3
                if ($charMap.ContainsKey($code)) { if ($charMap[$code] -ne $triple) { $conflicts += ('U+{0:X4}' -f $code) } }
                else { $charMap[$code] = $triple }
                $lo = $code -band 0xFF; $hi = ($code -shr 8) -band 0xFF
                $f = [int][char]$triple[0]
                if (($f -band 1) -ne 0) { $loShift[$lo] = $true } else { $loNo[$lo] = $true }
                if (($f -band 2) -ne 0) { $hiShift[$hi] = $true } else { $hiNo[$hi] = $true }
            }
            if (-not $ok) { $badLines += ('{0}:{1}[ascii]' -f $p.Name, ($i + 1)) }
        }
    }
    return [pscustomobject]@{
        CharMap = $charMap; LoShift = $loShift; LoNo = $loNo; HiShift = $hiShift; HiNo = $hiNo
        Conflicts = $conflicts; BadLines = $badLines; LineCount = $lineCount
    }
}

$script:MissingChars = New-Object System.Collections.Generic.HashSet[string]

function Encode-Text([string]$text, $obs) {
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $text.ToCharArray()) {
        $code = [int][char]$ch
        if ($code -lt 128 -or $code -eq 0xA7) { [void]$sb.Append($ch); continue }
        if ($obs.CharMap.ContainsKey($code)) { [void]$sb.Append($obs.CharMap[$code]) }
        else { [void]$script:MissingChars.Add(('{0}(U+{1:X4})' -f $ch, $code)); [void]$sb.Append('???') }
    }
    return $sb.ToString()
}

function Encode-TextByRule([string]$text, $obs) {
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $text.ToCharArray()) {
        $code = [int][char]$ch
        if ($code -lt 128 -or $code -eq 0xA7) { [void]$sb.Append($ch); continue }
        $lo = $code -band 0xFF; $hi = ($code -shr 8) -band 0xFF
        $flag = 0x10
        if ($obs.LoShift.ContainsKey($lo)) { $lo = ($lo + 0x0E) -band 0xFF; $flag = $flag -bor 1 }
        if ($obs.HiShift.ContainsKey($hi)) { $hi = ($hi - 0x09) -band 0xFF; $flag = $flag -bor 2 }
        [void]$sb.Append([char]$flag).Append([char]$ByteToChar[$lo]).Append([char]$ByteToChar[$hi])
    }
    return $sb.ToString()
}

function Decode-Text([string]$text) {
    $sb = New-Object System.Text.StringBuilder
    $i = 0
    while ($i -lt $text.Length) {
        $code = [int][char]$text[$i]
        if ($code -lt 128 -or $code -eq 0xA7) { [void]$sb.Append($text[$i]); $i++; continue }
        if ($i + 2 -ge $text.Length) { break }
        $flag = $code
        $lo = $CharToByte[[int][char]$text[$i + 1]]
        $hi = $CharToByte[[int][char]$text[$i + 2]]
        if (($flag -band 1) -ne 0) { $lo = ($lo - 0x0E) -band 0xFF }
        if (($flag -band 2) -ne 0) { $hi = ($hi + 0x09) -band 0xFF }
        [void]$sb.Append([char]($lo -bor ($hi -shl 8)))
        $i += 3
    }
    return $sb.ToString()
}

function Test-Coverage([string]$text, $obs, [string]$where) {
    $missing = @()
    foreach ($ch in $text.ToCharArray()) {
        $code = [int][char]$ch
        if ($code -lt 128 -or $code -eq 0xA7) { continue }
        if (-not $obs.CharMap.ContainsKey($code)) { $missing += ('{0}(U+{1:X4})' -f $ch, $code) }
    }
    if ($missing.Count -gt 0) {
        Write-Output ('  [MISSING] {0} -> {1}' -f $where, (($missing | Select-Object -Unique) -join ' '))
        return $false
    }
    return $true
}

$obs = Get-Observations

if ($Analyze) {
    Write-Output ('sample lines (structurally OK) = {0}' -f $obs.LineCount)
    Write-Output ('structurally odd lines         = {0} {1}' -f $obs.BadLines.Count, $(if ($obs.BadLines.Count) { '(' + (($obs.BadLines | Select-Object -First 6) -join ', ') + ')' }))
    Write-Output ('distinct CJK chars mapped      = {0}' -f $obs.CharMap.Count)
    Write-Output ('char map conflicts             = {0} {1}' -f $obs.Conflicts.Count, $(if ($obs.Conflicts.Count) { '(' + (($obs.Conflicts | Select-Object -First 10) -join ', ') + ')' }))
    $loOnly = $obs.LoShift.Keys | Where-Object { -not $obs.LoNo.ContainsKey($_) } | Sort-Object
    $hiOnly = $obs.HiShift.Keys | Where-Object { -not $obs.HiNo.ContainsKey($_) } | Sort-Object
    Write-Output ('lo bytes needing shift ({0}): {1}' -f $loOnly.Count, (($loOnly | ForEach-Object { '{0:X2}' -f $_ }) -join ' '))
    Write-Output ('hi bytes needing shift ({0}): {1}' -f $hiOnly.Count, (($hiOnly | ForEach-Object { '{0:X2}' -f $_ }) -join ' '))
    $mismatch = 0; $tested = 0; $samples = @()
    foreach ($p in Get-Pairs) {
        $la = Get-Content $p.Src -Encoding UTF8
        $lb = Get-Content $p.Enc -Encoding UTF8
        $n = [Math]::Min($la.Count, $lb.Count)
        for ($i = 0; $i -lt $n; $i++) {
            $s = Get-Body $la[$i]; $e = Get-Body $lb[$i]
            if ($null -eq $s -or $null -eq $e) { continue }
            $tested++
            if ((Encode-TextByRule $s $obs) -ne $e) {
                $mismatch++
                if ($samples.Count -lt 6) { $samples += ('{0}:{1}' -f $p.Name, ($i + 1)) }
            }
        }
    }
    Write-Output ('rule replay: {0} lines tested, {1} mismatched {2}' -f $tested, $mismatch, $(if ($samples.Count) { '(' + ($samples -join ', ') + ')' }))
    Write-Output 'table roundtrip (decode encoded file, compare with master):'
    foreach ($p in Get-Pairs) {
        $encLines = Get-Content $p.Enc -Encoding UTF8
        $srcLines = Get-Content $p.Src -Encoding UTF8
        $diff = 0
        $n = [Math]::Min($encLines.Count, $srcLines.Count)
        for ($i = 0; $i -lt $n; $i++) { if ((Decode-Text $encLines[$i]) -ne $srcLines[$i]) { $diff++ } }
        if ($encLines.Count -ne $srcLines.Count) { $diff++ }
        Write-Output ('  {0,-46} diff lines = {1}' -f $p.Name, $diff)
    }
    return
}

if ($DumpTable) {
    $obj = @{}
    foreach ($k in $obs.CharMap.Keys) { $obj[('{0:X4}' -f $k)] = $obs.CharMap[$k] }
    [System.IO.File]::WriteAllText($DumpTable, ($obj | ConvertTo-Json -Depth 3), (New-Object System.Text.UTF8Encoding($false)))
    Write-Output ('table dumped: {0} ({1} entries)' -f $DumpTable, $obj.Count)
    return
}

$targets = if ($Only) { @($Only) } else { (Get-Pairs).Name }

if ($Check) {
    $fail = 0
    foreach ($name in $targets) {
        $src = Join-Path (Join-Path $ModRoot 'decode_localisation') $name
        if (-not (Test-Path $src)) { Write-Output ('missing master: {0}' -f $src); $fail++; continue }
        $lines = Get-Content $src -Encoding UTF8
        $bad = 0
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if (-not (Test-Coverage $lines[$i] $obs ('{0}:{1}' -f $name, ($i + 1)))) { $bad++ }
        }
        if ($bad -eq 0) { Write-Output ('  [OK] {0}' -f $name) } else { $fail++ }
    }
    if ($fail -gt 0) { Write-Output ('CHECK FAILED: {0} file(s)' -f $fail); exit 1 } else { Write-Output 'CHECK PASSED'; exit 0 }
}

if ($Encode) {
    $missing = New-Object System.Collections.Generic.HashSet[string]
    $plan = @()
    foreach ($name in $targets) {
        $src = Join-Path (Join-Path $ModRoot 'decode_localisation') $name
        if (-not (Test-Path $src)) { Write-Output ('missing master: {0}' -f $src); exit 1 }
        $lines = Get-Content $src -Encoding UTF8
        $out = New-Object System.Collections.Generic.List[string]
        foreach ($line in $lines) { $out.Add((Encode-Text $line $obs)) }
        foreach ($m in $script:MissingChars) { [void]$missing.Add($m) }
        $plan += [pscustomobject]@{ Name = $name; Lines = $out }
    }
    if ($missing.Count -gt 0) {
        Write-Output 'ENCODE ABORTED - characters not present in the harvested table:'
        foreach ($m in ($missing | Sort-Object)) { Write-Output ('  {0}' -f $m) }
        Write-Output 'Reword using characters already used elsewhere in the mod, or extend the table.'
        exit 2
    }
    $utf8Bom = New-Object System.Text.UTF8Encoding($true)
    foreach ($item in $plan) {
        $dst = Join-Path (Join-Path $ModRoot 'localisation') $item.Name
        [System.IO.File]::WriteAllText($dst, (($item.Lines -join "`r`n") + "`r`n"), $utf8Bom)
        Write-Output ('encoded: {0} -> {1}' -f $item.Name, $dst)
    }
    exit 0
}

if ($Decode) {
    foreach ($name in $targets) {
        $enc = Join-Path (Join-Path $ModRoot 'localisation') $name
        if (-not (Test-Path $enc)) { Write-Output ('missing file: {0}' -f $enc); exit 1 }
        $text = Get-Content $enc -Encoding UTF8 -Raw
        Write-Output ('=== {0} ===' -f $name)
        Write-Output (Decode-Text $text)
    }
    exit 0
}

Write-Output 'specify one of -Analyze / -Check / -Encode / -Decode / -DumpTable'
