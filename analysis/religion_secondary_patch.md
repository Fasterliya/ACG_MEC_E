# new_religion.txt 覆盖 + 兼容宗教（融合信仰）增益补全 —— 施工记录

- 生成时间：2026-11-20
- 源文件：`F:\SteamLibrary\steamapps\workshop\content\236850\2796854877\common\religions\new_religion.txt`（ACG1，1644 行，SHA256 `AE3747E1…C611ADA8`）
- 落地文件：`ACG_MEC_E\common\religions\new_religion.txt`（1662 行，改后 SHA256 见文末）
- 覆盖机制：`ACG_MEC_E\descriptor.mod` 的 `dependencies` 已含 `ACG1`，本 mod 后加载；EU4 对 `common/religions/` 是**整文件同名覆盖**（不是逐块合并），所以本副本会整体顶掉 ACG1 那一份。
- 全库冲突面：workshop 236850 下只有 ACG1 提供 `common/religions/new_religion.txt`，无第三方抢同名文件。

## 1. 改动目标

`country_as_secondary` = 宗教作为**融合信仰 / 兼容宗教**被选中时的国家增益，游戏内文案见原版 `localisation/cossacks_l_english.yml:287`
`SECONDARY_RELIGION_BONUS: "Because $NAME$ is a Syncretic Faith:"`。

只有开了 `can_have_secondary_religion = yes` 的宗教能提供这个机制：

- ACG1：`common/religions/00_religion.txt:2117`（`tengri_pagan_reformed`）
- 本 mod：`common/religions/00_acg_mec_e_teyvat_religion.txt:39 / 77`（`acg_mec_e_seven_archons` / `acg_mec_e_moon_goddess`）

=> 提瓦特国家选融合信仰时，ACG 那 14 个宗教就是被选对象，它们的 `country_as_secondary` 就是玩家实际吃到的词条。

## 2. 逐宗教最终值（14 个，全部 2 条）

| 宗教 | country_as_secondary（改后） | 原值 |
|---|---|---|
| acg | `global_trade_goods_size_modifier = 0.05` / `tolerance_heretic = 1` | `global_unrest = -2` |
| JianNiang | `naval_forcelimit_modifier = 0.1` / `navy_tradition_decay = -0.01` | `local_colonist_placement_chance = 0.05`（省份域键塞在国家域，已换掉） |
| idol_reg | `recover_army_morale_speed = 0.1` / `tolerance_own = 1` | `recover_army_morale_speed = 0.05` |
| Nasalik | `manpower_recovery_speed = 0.1` / `land_forcelimit_modifier = 0.1` | `manpower_recovery_speed = 0.1` |
| MikuProtestant | `siege_ability = 0.1` / `defensiveness = 0.1` | 原样（本来 2 条） |
| MagicalGirl | `core_creation = -0.1` / `diplomatic_annexation_cost = -0.1` | `core_creation = -0.05` |
| Fate_reg | `global_trade_power = 0.15` / `fort_maintenance_modifier = -0.1` | `global_trade_power = 0.1` |
| Gensokyo_reg | `build_cost = -0.1` / `ae_impact = -0.05` | `build_cost = -0.1` |
| ElDorado_religion | `global_institution_spread = 0.2` / `global_tax_modifier = 0.1` | `global_institution_spread = 0.2` |
| Kirara | `global_missionary_strength = 0.02` / `diplomatic_reputation = 1` | `global_heretic_missionary_strength = 0.02` |
| goddess_worship | **新建块** `land_maintenance_modifier = -0.1` / `advisor_cost = -0.15` | 原本没有该块 |
| Elzia_reg | `diplomatic_reputation = 1` / `overextension_impact_modifier = -0.1` | `diplomatic_reputation = 0.5` |
| yurihime | `idea_cost = -0.1` / `technology_cost = -0.05` | `technology_cost = -0.05` |
| Inuyasha_religion | `tolerance_heretic = 1` / `tolerance_heathen = 2` | 原样（本来 2 条） |

强度锚点（原版同字段参照）：`dreamtime` `shock_damage 0.1 + hostile_attrition 2`、`protestant / reformed` `idea_cost -0.1`、`orthodox` `diplomatic_reputation 1 + advisor_pool 1`。

## 3. 结构修复（附属项 A / B）

| 项 | 位置 | 内容 |
|---|---|---|
| A-1 | `Fate_reg` 块尾 | `harmonized_modifier = harmonized_Fate_reg` 原先掉在 `Anime` 组级（块外，原第 1107 行），已移回 `Fate_reg` 块内 |
| A-2 | `Gensokyo_reg` | `harmonized_modifier = harmonized_MikuProtestant`（复制粘贴残留）→ `harmonized_Gensokyo_reg` |
| A-3 | 新文件 | `common/event_modifiers/zz_acg_mec_e_harmonized.txt` 补 3 个原先未定义、但被 `new_religion.txt` 引用的修正：`harmonized_Academycity`（`global_missionary_strength = 0.02`，给 Kirara / Elzia_reg 共用）、`harmonized_Gensokyo_reg`（`development_cost = -0.05`）、`harmonized_yurihime`（`idea_cost = -0.05`）。格式对齐 ACG1 `acg_harmonized_modifiers.txt`：1 条修正 + `religion = yes`（`religion = yes` 在原版 `common/event_modifiers/00_event_modifiers.txt:803` 等处有先例） |
| B | `goddess_worship` | 补 `province = { local_development_cost = -0.05 }`（此前 14 个宗教里只有它没有省份块） |

## 4. 校验记录

| 检查 | 结果 |
|---|---|
| 拷贝哈希（拷贝后未改前） | `AE3747E1…C611ADA8` = 源文件，`identical=True` |
| 大括号配平 | `open = 332`，`close = 332` |
| `validate_script`（country 作用域，覆盖全部新增 24 键 + 新块） | `issues: []`，`nodes: 43`，无 trigger/effect 混用 |
| 改动键原版存在性 | 24 个键全部在 `common/ideas`、`common/buildings`、`common/event_modifiers` 找到实例 |
| `eu4_verify_path` | `ok: true`，`underMod: true`，`underVanilla: false` |
| `eu4_readback` | `found: true`，40069 bytes |
| 未触碰 | `common/religions/00_acg_mec_e_teyvat_religion.txt`、`localisation/`、ACG1 原文件 |

## 5. 游戏内验收步骤

1. 启动器只勾 ACG1 + ACG_MEC_E（+中文 mod），确认 ACG_MEC_E 在 ACG1 之后。
2. 选一个信 `acg_mec_e_seven_archons` 或 `acg_mec_e_moon_goddess` 的国家（两者都有 `can_have_secondary_religion = yes`）。
3. 宗教界面 → 融合信仰（Syncretic Faith）列表 → 逐个点 ACG 的 14 个宗教。
4. 期望：每个宗教的 `Because XXX is a Syncretic Faith:` 段都显示 **2 行**；`goddess_worship` 不再空白。
5. 若某宗教仍是 1 行/空白：查 `error.log`（新修正键拼写）、查是否有别的 mod 在 ACG_MEC_E 之后再覆盖同名 `new_religion.txt`。

## 6. 回滚

- 单文件回滚：删除 `ACG_MEC_E\common\religions\new_religion.txt` → ACG1 原版立刻回来。
- 附属项单独回滚：删除 `ACG_MEC_E\common\event_modifiers\zz_acg_mec_e_harmonized.txt`（会把 3 个 `harmonized_modifier` 打回未定义状态，属已知历史问题）。
- 全量回滚：`analysis\religion_secondary_patch.md` 第 2 节表里"原值"列即反推依据。

## 7. ACG1 更新后的重放

ACG1 一旦更新 `new_religion.txt`，本副本会整体盖住新版内容。重放方式：

```powershell
powershell -NoProfile -File "F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\analysis\apply_religion_patch.ps1"
```

脚本流程：读 ACG1 最新文件 → 15 处精确替换（12 个 `country_as_secondary` + B 项新块 + 3 处结构修复）→ 写回本 mod → 打印每处命中数与最终哈希。任一处未命中即报错退出，不会写出半成品。**实测已跑过：脚本产出的文件与人工改的文件 SHA256 完全一致（幂等）。**

> 注意：`apply_religion_patch.ps1` 是 **UTF-8 with BOM**，供 Windows PowerShell 5.1 正确解析中文（无 BOM 时 5.1 会按 GBK 读，直接语法报错）。改这个脚本时别把 BOM 弄丢。

## 8. 哈希基线

| 文件 | SHA256 |
|---|---|
| ACG1 原文件 | `AE3747E182299C4C3015FDD342CFA018AE75C2A287EF63C0A4363773C611ADA8` |
| 本次改后文件（手工版 = 脚本版） | `EB47DB791D121E5E981F5E6CAFC451F07F03321E9E4D5F6C8B367467AAB04417` |

