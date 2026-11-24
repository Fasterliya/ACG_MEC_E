# ACG_MEC_E : generate Teyvat / Solaris unit groups
# - 76 unit files under common/units
# - enable lines injected into common/technologies/mil.txt per tech block (block ordinal = tech level)
# ASCII only on purpose: no encoding risk inside generated .txt
$ErrorActionPreference = 'Stop'

$mod      = 'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
$unitDir  = Join-Path $mod 'common\units'
$milPath  = Join-Path $mod 'common\technologies\mil.txt'
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# baseline curve cloned from existing tech_gensokyan units (same total pips, only shifted)
$base = @(
    @{t='infantry';  lvl=1;  man=1; om=0; dm=1; of=0; df=1; os=0; ds=0},
    @{t='infantry';  lvl=5;  man=1; om=0; dm=1; of=1; df=1; os=0; ds=1},
    @{t='infantry';  lvl=9;  man=1; om=1; dm=1; of=1; df=1; os=1; ds=1},
    @{t='infantry';  lvl=12; man=1; om=2; dm=2; of=3; df=2; os=1; ds=1},
    @{t='infantry';  lvl=15; man=1; om=2; dm=3; of=4; df=3; os=1; ds=1},
    @{t='infantry';  lvl=19; man=1; om=3; dm=3; of=3; df=3; os=3; ds=3},
    @{t='infantry';  lvl=26; man=1; om=3; dm=3; of=6; df=6; os=5; ds=4},
    @{t='cavalry';   lvl=1;  man=2; om=1; dm=1; of=0; df=0; os=2; ds=0},
    @{t='cavalry';   lvl=6;  man=2; om=2; dm=2; of=0; df=0; os=2; ds=0},
    @{t='cavalry';   lvl=10; man=2; om=2; dm=2; of=0; df=0; os=3; ds=2},
    @{t='cavalry';   lvl=14; man=2; om=3; dm=3; of=1; df=0; os=3; ds=2},
    @{t='cavalry';   lvl=23; man=2; om=4; dm=3; of=1; df=2; os=5; ds=5},
    @{t='cavalry';   lvl=28; man=2; om=2; dm=4; of=3; df=5; os=5; ds=5},
    @{t='artillery'; lvl=7;  man=2; om=1; dm=1; of=0; df=1; os=0; ds=0},
    @{t='artillery'; lvl=12; man=2; om=1; dm=3; of=2; df=3; os=0; ds=0},
    @{t='artillery'; lvl=16; man=2; om=2; dm=2; of=2; df=3; os=0; ds=1},
    @{t='artillery'; lvl=22; man=2; om=3; dm=3; of=4; df=3; os=1; ds=1},
    @{t='artillery'; lvl=26; man=2; om=3; dm=4; of=5; df=5; os=1; ds=1},
    @{t='artillery'; lvl=29; man=2; om=4; dm=3; of=5; df=5; os=2; ds=2}
)

function Copy-Pips($u) {
    return @{ man=$u.man; om=$u.om; dm=$u.dm; of=$u.of; df=$u.df; os=$u.os; ds=$u.ds }
}

function Get-Total($u) {
    return ($u.om + $u.dm + $u.of + $u.df + $u.os + $u.ds)
}

# early tiers have too few pips for a clean 1-point shift: both doctrines stay identical
$shiftThreshold = 9

# Teyvat assault : push one pip each from defensive fire/shock into offensive fire/shock
function New-TeyvatAssault($u) {
    $n = Copy-Pips $u
    if ((Get-Total $u) -lt $shiftThreshold) { return $n }
    if ($n.df -gt 1) { $n.of++; $n.df-- } elseif ($n.dm -gt 1) { $n.of++; $n.dm-- }
    if ($n.ds -gt 1) { $n.os++; $n.ds-- } elseif ($n.df -gt 1) { $n.os++; $n.df-- }
    return $n
}

# Teyvat guard : mirror image, defensive side gains
function New-TeyvatGuard($u) {
    $n = Copy-Pips $u
    if ((Get-Total $u) -lt $shiftThreshold) { return $n }
    if ($n.of -gt 1) { $n.df++; $n.of-- } elseif ($n.om -gt 1) { $n.df++; $n.om-- }
    if ($n.os -gt 1) { $n.ds++; $n.os-- } elseif ($n.df -gt 1) { $n.ds++; $n.df-- }
    return $n
}

# Solaris resonance : fire-heavy
function New-SolarisFire($u) {
    $n = Copy-Pips $u
    if ((Get-Total $u) -lt $shiftThreshold) { return $n }
    if ($n.ds -gt 1) { $n.of++; $n.ds-- } elseif ($n.dm -gt 1) { $n.of++; $n.dm-- }
    if ($n.os -gt 1) { $n.df++; $n.os-- } elseif ($n.om -gt 1) { $n.df++; $n.om-- }
    return $n
}

# Solaris tide : shock-heavy
function New-SolarisShock($u) {
    $n = Copy-Pips $u
    if ((Get-Total $u) -lt $shiftThreshold) { return $n }
    if ($n.df -gt 1) { $n.os++; $n.df-- } elseif ($n.dm -gt 1) { $n.os++; $n.dm-- }
    if ($n.of -gt 1) { $n.ds++; $n.of-- } elseif ($n.om -gt 1) { $n.ds++; $n.om-- }
    return $n
}

function Write-UnitFile($name, $type, $unitType, $pips, $comment) {
    $lines = @(
        "# $comment",
        "type = $type",
        "unit_type = $unitType",
        "",
        "maneuver = $($pips.man)",
        "offensive_morale = $($pips.om)",
        "defensive_morale = $($pips.dm)",
        "offensive_fire = $($pips.of)",
        "defensive_fire = $($pips.df)",
        "offensive_shock = $($pips.os)",
        "defensive_shock = $($pips.ds)"
    )
    $path = Join-Path $unitDir ($name + '.txt')
    [System.IO.File]::WriteAllText($path, ($lines -join "`n") + "`n", $utf8NoBom)
    return $name
}

# one unit_type group per doctrine family: switching the group IS switching the doctrine,
# every unit inside an unlocked group is available by default (no per-unit trigger)
$doctrine = @(
    @{prefix='acg_tv_assault'; group='acg_teyvat';   fn='New-TeyvatAssault'; label='Teyvat assault doctrine'},
    @{prefix='acg_tv_guard';   group='acg_teyvat';   fn='New-TeyvatGuard';   label='Teyvat guard doctrine'},
    @{prefix='acg_sl_fire';    group='acg_solaris'; fn='New-SolarisFire';   label='Solaris resonance doctrine'},
    @{prefix='acg_sl_shock';   group='acg_solaris';fn='New-SolarisShock';  label='Solaris tide doctrine'}
)

$created = New-Object System.Collections.Generic.List[string]
$perLevel = @{}

foreach ($d in $doctrine) {
    foreach ($u in $base) {
        $pips = & $d.fn $u
        $name = '{0}_{1}_{2:00}' -f $d.prefix, $u.t, $u.lvl
        $comment = "$($d.label) | $($u.t) T$($u.lvl) | ACG_MEC_E"
        Write-UnitFile $name $u.t $d.group $pips $comment | Out-Null
        $created.Add($name)

        if (-not $perLevel.ContainsKey($u.lvl)) { $perLevel[$u.lvl] = New-Object System.Collections.Generic.List[string] }
        $perLevel[$u.lvl].Add($name)
    }
}

# ---------- mil.txt insertion ----------
$lines = [System.IO.File]::ReadAllLines($milPath)
$blockCount = ($lines | Where-Object { $_ -match '^\s*technology\s*=\s*\{' }).Count
$out = New-Object System.Collections.Generic.List[string]
$level = 0
$inserted = 0
foreach ($line in $lines) {
    if ($line -match '^\s*technology\s*=\s*\{') { $level++; $out.Add($line); continue }
    if ($level -gt 0 -and $line -match '^\}') {
        # block 1 is Tech 0 (year 1350), so block ordinal - 1 = technology level
        $techLevel = $level - 1
        if ($perLevel.ContainsKey($techLevel)) {
            foreach ($e in $perLevel[$techLevel]) { $out.Add("`tenable = $e"); $inserted++ }
        }
        $out.Add($line); continue
    }
    $out.Add($line)
}

[System.IO.File]::WriteAllLines($milPath, $out, $utf8NoBom)

"unit files created : $($created.Count)"
"mil.txt tech blocks : $blockCount"
"mil.txt enable rows : $inserted"
"levels touched      : " + (($perLevel.Keys | Sort-Object) -join ',')

