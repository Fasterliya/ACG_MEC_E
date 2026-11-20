# apply_religion_patch.ps1
# 作用：把 ACG_MEC_E 的「兼容宗教（融合信仰）增益补全」补丁，重放到 ACG1 最新的 new_religion.txt 上。
# 用法：pwsh -File apply_religion_patch.ps1
# 特性：每次都以 ACG1 原始文件为源重新生成（幂等）；每处替换必须命中恰好 1 次，否则报错退出且不写盘。

param(
	[string]$Source = 'F:\SteamLibrary\steamapps\workshop\content\236850\2796854877\common\religions\new_religion.txt',
	[string]$Target = 'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\common\religions\new_religion.txt'
)

$ErrorActionPreference = 'Stop'
$T = "`t"

# 每项：Name / Old / New（Old 必须在源文件中恰好出现 1 次）
$pairs = @(
	# ---------- 1. acg ----------
	@{
		Name = 'acg: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_unrest = -2`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_trade_goods_size_modifier = 0.05`n$T$T$T" + "tolerance_heretic = 1`n$T$T}"
	},
	# ---------- 2. JianNiang ----------
	@{
		Name = 'JianNiang: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "local_colonist_placement_chance = 0.05`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "naval_forcelimit_modifier = 0.1`n$T$T$T" + "navy_tradition_decay = -0.01`n$T$T}"
	},
	# ---------- 3. idol_reg ----------
	@{
		Name = 'idol_reg: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "recover_army_morale_speed = 0.05`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "recover_army_morale_speed = 0.1`n$T$T$T" + "tolerance_own = 1`n$T$T}"
	},
	# ---------- 4. Nasalik ----------
	@{
		Name = 'Nasalik: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "manpower_recovery_speed = 0.1`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "manpower_recovery_speed = 0.1`n$T$T$T" + "land_forcelimit_modifier = 0.1`n$T$T}"
	},
	# ---------- 5. MagicalGirl ----------
	@{
		Name = 'MagicalGirl: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "core_creation = -0.05`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "core_creation = -0.1`n$T$T$T" + "diplomatic_annexation_cost = -0.1`n$T$T}"
	},
	# ---------- 6. Fate_reg ----------
	@{
		Name = 'Fate_reg: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_trade_power = 0.1`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_trade_power = 0.15`n$T$T$T" + "fort_maintenance_modifier = -0.1`n$T$T}"
	},
	# ---------- 7. Gensokyo_reg ----------
	@{
		Name = 'Gensokyo_reg: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "build_cost = -0.1`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "build_cost = -0.1`n$T$T$T" + "ae_impact = -0.05`n$T$T}"
	},
	# ---------- 8. ElDorado_religion ----------
	@{
		Name = 'ElDorado_religion: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_institution_spread = 0.2`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_institution_spread = 0.2`n$T$T$T" + "global_tax_modifier = 0.1`n$T$T}"
	},
	# ---------- 9. Kirara ----------
	@{
		Name = 'Kirara: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_heretic_missionary_strength = 0.02`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "global_missionary_strength = 0.02`n$T$T$T" + "diplomatic_reputation = 1`n$T$T}"
	},
	# ---------- 10. goddess_worship：新增 country_as_secondary + province ----------
	@{
		Name = 'goddess_worship: 新建 country_as_secondary + province'
		Old  = "$T$T" + "country = {`n$T$T$T" + "land_maintenance_modifier = -0.05`n$T$T$T" + "advisor_cost = -0.1`n$T$T}"
		New  = "$T$T" + "country = {`n$T$T$T" + "land_maintenance_modifier = -0.05`n$T$T$T" + "advisor_cost = -0.1`n$T$T}`n" +
		        "$T$T" + "country_as_secondary = {`n$T$T$T" + "land_maintenance_modifier = -0.1`n$T$T$T" + "advisor_cost = -0.15`n$T$T}`n" +
		        "$T$T" + "province = {`n$T$T$T" + "local_development_cost = -0.05`n$T$T}"
	},
	# ---------- 11. Elzia_reg ----------
	@{
		Name = 'Elzia_reg: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "diplomatic_reputation = 0.5`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "diplomatic_reputation = 1`n$T$T$T" + "overextension_impact_modifier = -0.1`n$T$T}"
	},
	# ---------- 12. yurihime ----------
	@{
		Name = 'yurihime: country_as_secondary'
		Old  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "technology_cost = -0.05`n$T$T}"
		New  = "$T$T" + "country_as_secondary = {`n$T$T$T" + "idea_cost = -0.1`n$T$T$T" + "technology_cost = -0.05`n$T$T}"
	},
	# ---------- A-1. Fate_reg 的 harmonized_modifier 从组级移回块内 ----------
	@{
		Name = 'A-1 Fate_reg: harmonized_modifier 位置修正'
		Old  = "$T$T" + "aspects_name = Fate_reg_ASPECTS`n$T}`n$T" + "harmonized_modifier = harmonized_Fate_reg`n$T" + "Gensokyo_reg = {"
		New  = "$T$T" + "aspects_name = Fate_reg_ASPECTS`n$T$T" + "harmonized_modifier = harmonized_Fate_reg`n$T}`n$T" + "Gensokyo_reg = {"
	},
	# ---------- A-2. Gensokyo_reg 的 harmonized_modifier 误指 ----------
	@{
		Name = 'A-2 Gensokyo_reg: harmonized_modifier 改指'
		Old  = "$T$T" + "aspects_name = Gensokyo_reg_ASPECTS`n$T$T" + "harmonized_modifier = harmonized_MikuProtestant"
		New  = "$T$T" + "aspects_name = Gensokyo_reg_ASPECTS`n$T$T" + "harmonized_modifier = harmonized_Gensokyo_reg"
	},
	# ---------- A-3. yurihime 的注释同步 ----------
	@{
		Name = 'A-3 yurihime: harmonized 注释同步'
		Old  = "harmonized_modifier = harmonized_yurihime     #无定义需补全"
		New  = "harmonized_modifier = harmonized_yurihime$T$T# 定义见 common/event_modifiers/zz_acg_mec_e_harmonized.txt"
	}
)

if (-not (Test-Path -LiteralPath $Source)) { throw "源文件不存在：$Source" }

$text = [System.IO.File]::ReadAllText($Source)
$text = $text -replace "`r`n", "`n"
$before = $text.Length

$applied = 0
foreach ($p in $pairs) {
	$count = ([regex]::Matches($text, [regex]::Escape($p.Old))).Count
	if ($count -ne 1) {
		throw ("替换点未命中：{0}（命中 {1} 次，期望 1 次）。ACG1 结构可能已变更，先人工核对。" -f $p.Name, $count)
	}
	$text = $text.Replace($p.Old, $p.New)
	$applied++
	Write-Host ("[OK] {0}" -f $p.Name)
}

# 配平自检
$open  = ([regex]::Matches($text, '\{')).Count
$close = ([regex]::Matches($text, '\}')).Count
if ($open -ne $close) { throw ("大括号不配平：{0} vs {1}" -f $open, $close) }

# 统一 CRLF 写回，UTF-8 无 BOM
$text = $text -replace "`n", "`r`n"
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Target, $text, $utf8)

Write-Host ""
Write-Host ("替换点：{0}/{1}" -f $applied, $pairs.Count)
Write-Host ("字符数：{0} -> {1}" -f $before, ($text.Length - ($text.Length - $before)))
Write-Host ("大括号：{0} / {1}" -f $open, $close)
Write-Host ("final = {0}" -f (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash)
Write-Host ("目标：{0}" -f $Target)
