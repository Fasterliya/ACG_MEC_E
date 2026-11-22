# 挪德卡莱 NDK 任务树：结构与施工方案

> 目标国家：`NDK`（挪德卡莱 / Nod-Krai），已在 `common/country_tags/ACG_MEC_E_country_tag.txt:6` 注册。
> 本文只定**结构与方案**，不含最终写码。门禁 B 通过后按第 9 节 SOP 落盘。
> 证据基准：本机原版 1.37.5（`F:\SteamLibrary\steamapps\common\Europa Universalis IV`）+ 本项目现有 missions 写法。

---

## 1. 现状勘定（已实测，不是推测）

### 1.1 国家基底

| 项 | 值 | 证据 |
|---|---|---|
| tag | `NDK` | `common/country_tags/ACG_MEC_E_country_tag.txt:6` |
| 首都 | `313 Soroka` | `decode_localisation/countries/NDK - Nod-Krai.txt:9` |
| 政体 / 等级 | `acg_monarchy` / `government_rank = 1`（公国） | 同上 `:2-5` |
| 文化 / 宗教 / 科技组 | `acg_nodkrai` / `acg` / `eastern` | 同上 `:6-8` |
| 君主 | 基里尔（adm4/dip5/mil4，immortal + scholar + bold_fighter） | 同上 `:11-25` |
| 理念 | `NDK_ideas`：部族议会 / 边贸要道 / 雪原游击 / 猎手传统 / 熔炉与铁砧 / 月之民 / 极寒生存 | `decode_localisation/NDK_l_english.yml:6-24` |

**任务树主题必须长在这 7 条理念上**，不要另起一套世界观 —— 理念已经是这个国家的性格说明书。

### 1.2 领土与地理锚点（写 trigger 的硬依据）

9 个省份，正好卡满 3 个 area：

| area | 省份 | 数量 |
|---|---|---|
| `pomor_area` | 1776 Karelia、313 Soroka、1958 Kargopol、4258 Onega | 4 / 4 全占 |
| `arkhangelsk_area` | 4122 Shenkursk、4256 Solvychegodsk、1955 Kholmogory、4257 Mezen | 4 / 4 全占 |
| `laponia_area` | 1777 Kola | 1（该 area 只取 1 省） |

- 证据：`map/area.txt` 解析结果；region 归属 `russia_region`（`map/region.txt`）。
- 贸易节点：**`white_sea`**，成员含 313 / 1776 / 1958 / 4258 / 1955 / 4122 / 4256 / 4257 / 1777（`common/tradenodes/00_tradenodes.txt:1914` 的 members 行）。

⇒ 设计含义：**前期任务全是"经营白海"，中期是"吃掉这两个 area 的残余 + 伸手拉普兰"，后期才是"南下诺夫哥罗德 / 出波罗的海"。** 不要给 NDK 一上来就写"征服莫斯科"，它只有 9 省 1 级政体。

### 1.3 项目现有任务树写法（照抄这套壳，不发明新壳）

`missions/BLS_missions.txt:1-9`（每个国家 5 个顶层块，一个块 = 一列）：

```
BLS_missions_1 = {
	slot = 1
	generic = no
	ai = yes
	potential = {
		tag = BLS
		NOT = { map_setup = map_setup_random }
	}
	has_country_shield = yes
	...
}
```

- 节点命名 = `<TAG>_missions_<列>_<行>`，例：`BLS_missions_1_3` 在 `slot = 1` 块内、`position = 3`。
- 节点必备字段：`icon` / `position` / `trigger` / `effect`；非根节点加 `required_missions = { 上级 }`。
- 奖励语汇池（全部在本项目已跑通）：`add_prestige` `add_splendor` `add_adm_power` `add_dip_power` `add_mil_power` `add_treasury` `add_stability` `add_mercantilism` `add_country_modifier` `change_government_reform_progress` `define_advisor` `capital_scope = { add_base_tax ... }` `add_permanent_claim`。
- 顺手记一笔前人踩的坑（`BLS_missions.txt:147` / `:518`）：`add_trade_income` 与 `add_crown_land` **都是不存在的效果名，写了静默白给**；王领要用 `change_estate_land_share = { estate = all share = -0.10 }`。

---

## 2. 三个结构方案（推荐 A）

| 方案 | 结构 | 节点数 | 优点 | 缺点 |
|---|---|---|---|---|
| **A（推荐）** | 5 列 × 5 行，每列一条独立竖梯 | 25 | 零越界（全同列 Δ行≥1）、与 BLS/HMC/PLP 现有树完全同构、可分段施工、单列坏了不影响别列 | 视觉上 5 个根，没有"一棵树"的收束感 |
| B | 阶梯错位 + 跨列收束（主列 slot3，其余列每级 `Δ行=1` 挂到主列） | 21–25 | 有主线感，一个玩家能读懂的"主线 → 分岔" | 行号必须严格遵守 D.3 错位骨架，写错一行整棵塌成竖柱；返工成本高 |
| C（MVP） | 3 列 × 5 行 | 15 | 两小时能跑通，先验收再扩 | 覆盖不到"月之民"与"南方答复"两条最有味道的线 |

**推荐 A**，理由：这个 mod 的 14 个任务树文件里 11 个是 A 形态（`BLS_missions.txt`、`HMC`、`PLP`、`ALC`…），玩家视觉预期已经定型；而且 A 形态可以**按列交付**——先交 1/3/4 三列（内政、月之民、军事），玩家当天就能玩，2/5 两列后补。

---

## 3. 方案 A：五列主题

| slot | 列名（树级 loc） | 主题 | 挂在哪条理念上 | 节奏 |
|---|---|---|---|---|
| 1 | 极北立国 | 生存 → 议会 → 工业 → 港口 → 界碑 | 极寒生存 / 部族议会 / 熔炉与铁砧 | 全期，第 5 格是"立国"节点 |
| 2 | 边贸要道 | 税卡 → 走私路 → 毛皮 → 商路特权 → 白海霸权 | 边贸要道 | 中前期发力，第 5 格吃满 `white_sea` |
| 3 | 月之民（主线） | 守夜誓言 → 月历 → 圣所 → 月辉之律 → 月下国度 | 月之民 | 慢热，条件偏"稳定/威望/发展"，第 5 格给国家身份级永久修正 |
| 4 | 雪原游击 | 猎手 → 伏击 → 边军 → 极北军团 → 不可逾越的冬天 | 雪原游击 / 猎手传统 | 军事线，条件全是军队规模/传统/要塞 |
| 5 | 南方的答复 | 诺夫哥罗德遗产 → 卡累利阿与拉普兰 → 白海全岸 → 波罗的海之窗 → 北方帝国 | 无（对外线） | 全期最重的征服线，放在最后解锁 |

---

## 4. 节点表（可直接照此写码）

`slot` = 列，`position` = 行（**别写反**，见 `index/domains.md` §D.1）。全部节点 `required_missions` 只指向**同列上一行**，因此 100% 落在"关系 A｜同列 Δ行≥1"，零越界。

### slot 1 — 极北立国

| 节点 | pos | icon（已验存在） | trigger（要点） | effect（要点） |
|---|---|---|---|---|
| `NDK_missions_1_1` 第一堆火 | 1 | `mission_develop_the_capital` | `total_development = 30` | 首都 +1/+1/+1、`add_prestige = 10`、`add_treasury = 100` |
| `NDK_missions_1_2` 部族议会 | 2 | `mission_noble_council` | `stability = 1`、`total_development = 60` | `add_stability = 1`、`define_advisor = { type = statesman skill = 2 }`、`change_government_reform_progress = 25`、`add_splendor = 50` |
| `NDK_missions_1_3` 熔炉与铁砧 | 3 | `mission_iron_and_copper` | `monthly_income = 25`、`num_of_owned_provinces_with = { value = 2 has_fort_building_trigger = yes }` | `add_country_modifier = { name = NDK_forge_modifier duration = 9125 }`、`add_adm_power = 100` |
| `NDK_missions_1_4` 白海港口 | 4 | `mission_found_arkhangelsk` | `num_of_total_ports = 5`、`naval_forcelimit = 15` | `NDK_white_sea_harbor_modifier`（-1）、`add_dip_power = 150`、`add_splendor = 100` |
| `NDK_missions_1_5` 立起界碑 | 5 | `mission_empire` | `government_rank = 2`、`total_development = 120` | `NDK_border_stone_modifier`（-1）、`add_stability = 1`、首都 +2/+2/+2、`add_splendor = 200` |

### slot 2 — 边贸要道

| 节点 | pos | icon | trigger | effect |
|---|---|---|---|---|
| `NDK_missions_2_1` 雪原上的税卡 | 1 | `mission_market_place_with_asian_traders` | `monthly_income = 15` | `NDK_toll_gate_modifier`（9125）、`add_treasury = 150` |
| `NDK_missions_2_2` 不问来路的货 | 2 | `mission_the_grand_bazaar` | `white_sea = { trade_share = { country = ROOT share = 20 } }` | `NDK_smuggler_road_modifier`（9125）、`add_dip_power = 100` |
| `NDK_missions_2_3` 毛皮与盐 | 3 | `mission_control_fur_trade` | `white_sea = { trade_share = { country = ROOT share = 35 } }` | `NDK_fur_monopoly_modifier`（-1）、`add_treasury = 300`、`add_splendor = 100` |
| `NDK_missions_2_4` 白海商路特权 | 4 | `mission_great_trading_houses` | `num_of_light_ship = 10`、`trade_efficiency = 0.15` | `NDK_trade_charter_modifier`（9125）、`add_dip_power = 200`、`add_mercantilism = 1` |
| `NDK_missions_2_5` 白海的主人 | 5 | `mission_dominate_home_trade_node` | `white_sea = { trade_share = { country = ROOT share = 60 } }`、`monthly_income = 60` | `NDK_white_sea_hegemon_modifier`（-1）、`add_treasury = 1000`、`add_splendor = 300` |

### slot 3 — 月之民（主线）

| 节点 | pos | icon | trigger | effect |
|---|---|---|---|---|
| `NDK_missions_3_1` 守夜者的誓言 | 1 | `mission_hands_praying` | `prestige = 25` | `NDK_nightwatch_oath_modifier`（9125）、`add_prestige = 10` |
| `NDK_missions_3_2` 月历 | 2 | `mission_norse_faith` | `stability = 2` | `NDK_moon_calendar_modifier`（-1，小）、`add_adm_power = 100`、`add_splendor = 50` |
| `NDK_missions_3_3` 月下圣所 | 3 | `mission_temple_patronage` | `stability = 2`、`prestige = 50` | `NDK_moonlight_sanctum_modifier`（9125）、首都 +2/+0/+1、`add_splendor = 100` |
| `NDK_missions_3_4` 月辉之律 | 4 | `mission_religious` | `total_development = 150`、`legitimacy = 90` | `NDK_moonlit_law_modifier`（-1）、`add_stability = 1`、`change_government_reform_progress = 50` |
| `NDK_missions_3_5` 月下的国度 | 5 | `mission_lion_of_the_empire` | `total_development = 250`、`stability = 3` | `NDK_moonlit_realm_modifier`（-1，国家身份级）、`add_stability = 2`、`add_splendor = 400` |

### slot 4 — 雪原游击

| 节点 | pos | icon | trigger | effect |
|---|---|---|---|---|
| `NDK_missions_4_1` 猎手传统 | 1 | `mission_hunting` | `army_size = 10` | `NDK_hunter_tradition_modifier`（9125）、`add_mil_power = 100` |
| `NDK_missions_4_2` 雪里的伏击 | 2 | `mission_the_sami` | `army_tradition = 20` | `NDK_snow_ambush_modifier`（9125）、`add_army_tradition = 10` |
| `NDK_missions_4_3` 边军 | 3 | `mission_castle_construction` | `num_of_owned_provinces_with = { value = 2 has_fort_building_trigger = yes }` | `NDK_border_host_modifier`（-1）、`add_mil_power = 150` |
| `NDK_missions_4_4` 极北军团 | 4 | `mission_new_army` | `army_size = 40`、`num_of_artillery = 10` | `NDK_arctic_legion_modifier`（9125）、`add_mil_power = 200`、`define_general = { ... }` |
| `NDK_missions_4_5` 不可逾越的冬天 | 5 | `mission_build_up_to_force_limit` | `army_tradition = 40`、`army_size = 60` | `NDK_invincible_winter_modifier`（-1）、`add_stability = 1`、`add_splendor = 300` |

### slot 5 — 南方的答复

| 节点 | pos | icon | trigger | effect |
|---|---|---|---|---|
| `NDK_missions_5_1` 诺夫哥罗德的遗产 | 1 | `mission_novgorod_the_great` | `controls = 310` | `NDK_novgorod_legacy_modifier`（9125）、`add_prestige = 20`、`add_adm_power = 100` |
| `NDK_missions_5_2` 卡累利阿与拉普兰 | 2 | `mission_karels_heritage` | `karelia_area = { type = all country_or_non_sovereign_subject_holds = ROOT }`、`laponia_area = { type = all country_or_non_sovereign_subject_holds = ROOT }` | 对 `pomor_area` / `arkhangelsk_area` 未核心者 `add_permanent_claim = ROOT`、`add_mil_power = 150` |
| `NDK_missions_5_3` 白海全岸 | 3 | `mission_protect_white_sea_trade` | `pomor_area` 与 `arkhangelsk_area` 均 `type = all ... holds = ROOT` | `russia_region` 边境 area 抛 `add_permanent_claim`、`add_splendor = 150`、`add_mil_power = 200` |
| `NDK_missions_5_4` 波罗的海之窗 | 4 | `mission_baltic_empire` | `num_of_total_ports = 12`、`naval_forcelimit = 40` | `NDK_baltic_window_modifier`（9125）、`add_dip_power = 200` |
| `NDK_missions_5_5` 北方帝国 | 5 | `mission_lion_of_the_north` | `government_rank = 3`、`total_development = 500` | `NDK_northern_empire_modifier`（-1）、`add_stability = 2`、`add_splendor = 500`、首都 +3/+3/+3 |

> `army_tradition` / `legitimacy` / `num_of_light_ship` / `num_of_artillery` / `controls` / `government_rank` / `is_great_power` 这几个是**待逐条回原版复核**项，见第 7 节。

---

## 5. 箭头与空间自查（写完必跑这一节）

按 `index/domains.md` §D.2 的硬规则：

| 检查项 | 本方案 |
|---|---|
| `slot` 语义 = 列，`position` 语义 = 行 | 已按此排布，未写反 |
| 跨列依赖必须 `Δ行 = 1` | **本方案 0 条跨列依赖**，天然满足 |
| `Δ行 ≤ 0` 越界 | 0 条（所有 `required_missions` 均指向同列 `position - 1`） |
| `Δ行 ≥ 2` 的同列连接 | 0 条，全部严格 +1（想省地方可以合并成 +2，但别和跨列混用） |
| `slot` 取值 | 只用 1–5。原版 1.37.5 全库只有 1–5；本 mod 的 `HKH/KSN/SKR` 用了 6–10，属**未验证**写法，NDK 不跟 |
| 每列根节点 | `position = 1`，无 `required_missions`，共 5 个根（欧盟原版常态，如 `01_Generic_European_Missions.txt` 多根） |

若之后要升级成方案 B（跨列收束），只允许在"`position` 比目标高 1"的位置挂，推荐骨架：主线 slot3 占 1–5，slot2 占 2–6，slot4 占 2–6，slot1 占 1–5，slot5 占 3–7。

---

## 6. 奖励与经济曲线（对齐 BLS 档位，不超模）

三档，全部照 `BLS_missions.txt` 的强度抄：

| 档位 | 位置 | 修正时长 | 点数 | 钱 / 辉煌 | 其他 |
|---|---|---|---|---|---|
| 早期 | pos 1–2 | `9125`（25 年） | 100 | treasury 100–200 / splendor 25–50 | — |
| 中期 | pos 3–4 | `9125`，纯内政小修正可 `-1` | 100–200 | 300 / 100–150 | `add_stability = 1`、首都 dev、改革进度 25–50 |
| 终局 | pos 5 | `-1` 永久 | 200+ | 1000 / 200–500 | `add_stability = 2`、首都 +3/+3/+3、`change_government_reform_progress = 100+` |

25 任务总量级：treasury ≈ 4000–5000、splendor ≈ 2500–3000、永久修正 11 条。与 BLS（25 任务 / treasury 1400+ / 永久修正 12 条）基本同档 —— **挪德卡莱是 9 省小国，修正要给得"精"不要给得"肥"**：贸易/防御/人力向，别给 `discipline` 大礼包。

`NDK_*_modifier` 全部只允许用下面这批**本项目已验证的 modifier 键**（`BLS_mission_modifiers.txt:1-93` 实证）：

`defensiveness` `fort_maintenance_modifier` `global_unrest` `stability_cost_modifier` `administrative_efficiency` `trade_efficiency` `global_trade_power` `production_efficiency` `global_trade_goods_size_modifier` `mercantilism_cost` `trade_income_percentage` `interest` `naval_morale` `sailors_recovery_speed` `global_ship_recruit_speed` `heavy_ship_power` `navy_tradition_decay` `naval_forcelimit_modifier` `global_sailors_modifier` `global_ship_trade_power` `discipline` `land_morale` `land_forcelimit_modifier` `global_manpower_modifier` `core_creation` `governing_capacity_modifier` `governing_capacity` `prestige` `diplomatic_reputation` `all_power_cost` `prestige_decay` `legitimacy`

> 想加 `hostile_attrition` / `army_tradition` / `manpower_recovery_speed` 之类的，必须先 `query_script_doc` 确认 1.37.5 存在，再进文件。

---

## 7. 待复核 / 风险清单（写码前逐条销账）

| # | 项 | 现状 | 处理 |
|---|---|---|---|
| 1 | `white_sea = { trade_share = { country = ROOT share = N } }` （用贸易节点名当作用域） | 内层写法有原版实证：`00_Generic_missions.txt:296-301` 用 `home_trade_node` 包 `trade_share`；外层直挂节点名的形式**未见原版实例** | 首版落地后进游戏点开 NDK 任务栏实测；不通就退回 `home_trade_node` + `white_sea = { ... }` 二选一实测 |
| 2 | `num_of_light_ship` | 原版 missions 有实证 `99_Hansa_Missions.txt:1809` | 可用 |
| 3 | `num_of_artillery` | 脚本文档命中（`triggers.txt:442`，country 作用域） | 可用；另在 missions 里抽一条原版实例再确认 |
| 4 | `army_size` / `controls` | 原版实证：`00_Generic_missions.txt:109`、`DOM_Russia_Missions.txt:2389` | 可用 |
| 5 | `army_tradition` / `legitimacy` | 未复核 | 写码时 `query_script_doc` 各查一次，不通换 `prestige` / `stability` |
| 6 | `has_fort_building_trigger` | 本项目实证 `BLS_missions.txt:59` | 可用 |
| 7 | `slot = 6..10` | 本 mod 存在但原版 0 例 | NDK 不用，只用 1–5 |
| 8 | 树级 loc 键 `NDK_missions_1` | 项目里 BLS 写了（`BLS_l_english.yml:49-53`），Wiki 说树无标题键 | 按项目惯例照写，无害 |
| 9 | 任务图标 sprite | 25 个 icon 全部在本机 967 个 `mission_*` sprite 里逐条命中 | 不需要新增 gfx |
| 10 | 本地化 | `localisation/` 由你手动编码，AI 只写 `decode_localisation/` | 见第 8 节 |

---

## 8. 本地化清单（AI 只写 `decode_localisation/`）

- 文件：**追加**到 `decode_localisation/NDK_l_english.yml`（已存在，现有 24 行，`l_english:` 开头 + 行首 1 空格缩进）。
- 键量：5 个树级键 + 25 × 2（`_title` / `_desc`）+ 11 个 modifier 键 = **66 个键**。
- 命名：`NDK_missions_<列>_<行>_title` / `_desc`（**不是**裸节点名，漏 `_title` 界面空白）。
- 文案口径（建议）：
  - `_title`：4–8 字，冷、硬、像界碑上的刻字（例：「第一堆火」「不问来路的货」「不可逾越的冬天」）。
  - `_desc`：60–110 字，第三人称史书体 + 一句挪德卡莱视角的冷幽默；不写"你将获得"这类攻略腔。
  - 颜色只在关键数字上用 `§Y` / `§G`，不整段刷色。
- 收尾我会附一张 **key → 中文全文** 对照表给你编码，你直接抄。

---

## 9. 施工 SOP（顺序不可换）

1. **写修正**：新建 `common/event_modifiers/NDK_mission_modifiers.txt`，11 条 `NDK_*_modifier`（只用第 6 节白名单键）。
2. **写任务**：新建 `missions/NDK_missions.txt`，5 个顶层块，25 节点，SOP 顺序按列（1 → 3 → 4 → 2 → 5，先交能玩的三列）。
3. **静态校验**：每列写完跑 `validate_script`（作用域 + trigger/effect 混用）；trigger 里出现 effect、effect 里出现 trigger 一律打回。
4. **loc 校验**：`check_loc_keys` 确认 66 个键全部有对应用户编码后的条目（AI 侧先保证 `decode_localisation` 齐全）。
5. **路径校验**：`eu4_verify_path` → 必须 `underMod = true`（严禁落进原版或 workshop 目录）。
6. **回读校验**：`eu4_readback` 确认 `NDK_missions_1_1` … `NDK_missions_5_5` 全部 `found = true`。
7. **游戏内验收**（第 10 节）。
8. **你编码 loc** → 进游戏复看文本是否溢出按钮宽度。

---

## 10. 验收标准（做到这些才算完成）

1. 进入 NDK，任务栏出现 **5 列 × 5 格**，无空格、无"未知任务"占位、无空白文本。
2. 每列第 1 格可点（`required_missions` 为空），第 2–5 格灰锁，且**锁链只向上连一格**（不出现斜拉到别列、不出现同行横线）。
3. 完成 `NDK_missions_2_5` 后，`white_sea` 节点份额 ≥ 60 的判定确实触发（用控制台 `trade node` 面板核对份额数字）。
4. 所有 `NDK_*_modifier` 在鼠标悬停时显示中文名与数值，不是裸 key。
5. `error.log` 无 `Unknown modifier` / `Invalid trigger` / `missing localisation` 记录。

---

## 11. 下一步

本文件只到"结构与方案"。等你确认下面三件事后再动文件：
1. 走方案 A（5×5=25）还是先交 MVP（3 列 15 个）？
2. 「月之民」这条线是走**宗教/文化向**（稳定、威望、传教、月历制度）还是**修正叠加向**（永久修正滚雪球）？
3. 第 5 列是否允许把 **诺夫哥罗德 / 卡累利阿** 写成征服目标（会与 RWF 赤冬、SVZ 至冬的地盘逻辑产生摩擦，需要确认要不要避开 SVZ 首都 33）？
