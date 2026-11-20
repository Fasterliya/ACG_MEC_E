# -*- coding: utf-8 -*-
p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()

add = """
### 13.7 国旗补漏：LGN.tga -> RGU.tga

`gfx/flags/LGN.tga` 是改名 LGN->RGU 时漏掉的唯一一处（脚本只换了文本，没换二进制文件名）。
已重命名为 **`gfx/flags/RGU.tga`**，回读规格：128×128 / 24bpp / 未压缩 / 49196 B，与其余 8 面一致，也与 `BLS.tga` 同规格。

### 13.8 理念强化（九国全改）

原版九国理念「传统 2 + 野心 1 + 7×1 = 10 条修正」，单条理念只有 1 条，太贫瘠。现全部重写为 **传统 2 + 野心 1 + 7×2 = 17 条修正/国**，数值向 `BLS_ideas.txt` 的强度看齐。

| 国家 | 传统（2 条） | 野心（1 条） |
|---|---|---|
| JZH 今州 | land_morale 0.15 / defensiveness 0.20 | infantry_power 0.10 |
| RGU 拉古那 | trade_efficiency 0.15 / global_trade_power 0.15 | diplomatic_reputation 2 |
| XJA 星炬学院 | technology_cost -0.10 / development_cost -0.10 | all_power_cost -0.05 |
| MGZ 梦州 | stability_cost_modifier -0.15 / global_unrest -1 | tolerance_own 1 |
| CXT 残星会 | spy_offence 0.25 / land_morale 0.10 | discipline 0.05 |
| FGL 浮光林 | global_manpower_modifier 0.15 / max_hostile_attrition 1 | manpower_recovery_speed 0.15 |
| FSL 翡萨烈 | naval_morale 0.15 / global_ship_trade_power 0.15 | naval_forcelimit_modifier 0.25 |
| MTL 莫塔里 | global_tax_modifier 0.10 / production_efficiency 0.15 | trade_efficiency 0.15 |
| YHH 隐海修会 | tolerance_own 1 / stability_cost_modifier -0.15 | prestige 1.5 |

示例（CXT 残星会，7 条各 2 修正）：
`infantry_power 0.15 + discipline 0.05` / `siege_ability 0.15 + spy_offence 0.20` / `manpower_recovery_speed 0.15 + global_manpower_modifier 0.10` / `war_exhaustion -0.10 + land_morale 0.10` / `global_unrest -2 + stability_cost_modifier -0.10` / `core_creation -0.15 + prestige 0.5` / `global_manpower_modifier 0.15 + land_forcelimit_modifier 0.15`

校验：
- 九国共 **153 条 modifier 实例**，全部落在已验证白名单内（无拼错键名）
- 9 个 ideas 文件括号平衡
- loc key 仍是 **198**（key 名不变，只有理念名与 `_desc` 文案重写，63 条描述全部换成有实感的史书体）
- `common/ideas/*.txt` 是纯 ASCII，**不需要转码**；需要重转的只有 `localisation` 那份明文（因为文本变了）

备份：`analysis/backup_ideas_v2_20261120/`；工具：`analysis/tools/build_ideas_v2.py`。
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
