# 01 科技组层调查报告

调查员：tech-groups ｜ 时间：2026-11-18 ｜ 只读三源，未修改任何被调查文件
基线引用：`analysis/00_baseline.md`（已核实项不重复核）

数据源：
- `WS` = `F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E`
- `PT` = `C:\Users\HP\Downloads\ACG_MEC_E\ACG_MEC_E`
- `MOD` = `F:\SteamLibrary\steamapps\workshop\content\236850\2796854877`
- 参照系：原版 1.37.5 = `F:\SteamLibrary\steamapps\common\Europa Universalis IV`（下称 `VAN`）

---

## 0. 本层最重要的一条结论（先看这个）

**`acgr_g01..g36` 在母 mod 里的角色是「兵种组（unit_type）」，不是「科技组（technology_group）」。**

- `MOD` 全库 5898 个 txt 里，`technology_group = acgr_g*` 命中 **0 处**；`unit_type = acgr_g*` 命中 **280 个国家 + 972 个兵种文件**。
- `MOD` 的 36 个幻想乡国家已经被母 mod 迁走：`MOD/history/countries/ALC - Alice Margatroid.txt:2` = `unit_type = acgr_g01`，`:10` = `technology_group = western`。即母 mod 作者**已经放弃了 `tech_gensokyan`**，改用「westen/muslim 科技组 + acgr 兵种组」。
- 因此 `WS` 覆盖 `common/technology.txt` 造成的真实破坏不是"少了 36 个可选科技组"，而是**抹掉了 36 个兵种组的注册表**，导致 `MOD` 侧 280 个国家的 `unit_type = acgr_gXX`（`MOD/history/countries/ABY - Abydos.txt:2`）与 972 个兵种文件的 `unit_type` 全部指向未定义组；同时 `WS/common/technologies/mil.txt`（1475 行、0 条 acgr，`WS/common/technologies/mil.txt`）覆盖母 mod 的 2417 行版本，把 **855 条 `enable = acgr_gXX_*`** 全数抹掉。

机制证据见 §5。

---

## 1. 三方组清单对比（表格）

文件尺寸/行数：

| 源 | 路径 | 字节 | 行 | CRLF |
|---|---|---|---|---|
| `WS` | `common/technology.txt` | 4612 | 236 | 有 |
| `PT` | `common/technology.txt` | 7934 | 400 | 无（LF） |
| `MOD` | `common/technology.txt` | 8335 | 401 | 有 |

组数：`WS` 20 ／ `PT` 55 ／ `MOD` 55。

| # | 组名 | 归属 | `WS` | `PT` | `MOD` | 证据（行号） |
|---|---|---|---|---|---|---|
| 1–17 | `western` `eastern` `ottoman` `muslim` `indian` `east_african` `central_african` `chinese` `nomad_group` `sub_saharan` `north_american` `mesoamerican` `south_american` `andean` `aboriginal_tech` `polynesian_tech` `high_american` | 原版 | ✔ | ✔ | ✔ | WS:10–188 / MOD:10–188 / VAN
| 18 | `test_group_2` | 原版 | ✔ | ✔ | ✔ | WS:189–195 / MOD:189–195
| 19 | `acg_american` | 母 mod | ✔ | ✔ | ✔ | WS:196–212 / MOD:196–212
| 20 | `tech_gensokyan` | **我方独有** | ✔ | ✘ | ✘ | WS:213–229
| 21–56 | `acgr_g01` … `acgr_g36`（36 个） | **母 mod 新增** | ✘ | ✔ | ✔ | MOD:214–393（`# BEGIN ACGR_UNIT_GROUPS REGISTERED UNIT FAMILIES` MOD:213，`# END` MOD:394）；PT 同内容

- `WS` 相对 `MOD` **缺 36 组**：`acgr_g01..acgr_g36` 全部缺失（整文件覆盖所致）。
- `PT` 相对 `MOD` **完全一致**：`Compare-Object` 逐行 0 差异；字节差 8335−7934 = 401 = 401 个 CRLF→LF 的换行符差，**内容零差异**（`.gitattributes`/`core.autocrlf` 检出归一化，非人工编辑）。
- `PT` 相对 `WS`：`git -C PT diff -- common/technology.txt` 显示唯一改动 = 删掉 `tech_gensokyan` 块（−30 行）+ 加 36 个 acgr 块与 2 条注释（+182 行），`193 +++/30 ---`。**合作伙伴是直接拿母 mod 的新文件覆盖，不是手工合并**；`tech_gensokyan` 是被顺带删除的。

---

## 2. 组定义体 diff（哪些组定义不同）

### 2.1 原版 18 组 + `acg_american`：三方一致，`WS` 未改

- 取 `WS` 与 `MOD` 两个文件的**前 209 行**（到 `acg_american` 结束）做 SHA256：两侧同为 `FC0AD297…B016B6`，`identical=True`。→ 18 原版组 + `acg_american` 的 `start_level`/`start_cost_modifier`/`nation_designer_*`/`is_primitive` 全部逐字节相同。
- `PT` 与 `MOD` 行级完全一致（§1），故 `test_group_2`、`acg_american` 在 `PT` 也与 `WS` 相同 → **任务 6 的答案是「一致，`WS` 没改过这两个组」**。
- 定点核对：`test_group_2` = `start_level 1 / start_cost_modifier 0 / nation_designer_cost{value=1000}`（WS:189–195 = MOD:189–195）；`acg_american` = `start_level 3 / start_cost_modifier 0 / nation_designer_trigger{continent OR} / nation_designer_cost{75}`（WS:196–212 = MOD:196–212）。

### 2.2 `tech_gensokyan`（仅 `WS`）

`WS/common/technology.txt:213–229`：

```
tech_gensokyan = {
    start_level = 3
    start_cost_modifier = 0
    nation_designer_cost = { trigger = { capital_scope = { OR = { continent = new_world … oceania } } } value = 75 }
}
```

关键字段与 `western`（WS:10–26）**数值完全相同**（3 / 0 / 75），差别只是 `nation_designer_cost` 带了"新世界"触发器。→ 幻想乡国家的科技成本档位等值于西方组，**没有平衡偏差**。

### 2.3 36 个 `acgr_gXX`（仅 `MOD`/`PT`）

每个组的定义体**完全相同**（基线第 6 条已核实，本次复核 `MOD:214–218` / `269–273` / `389–393` 一致）：

```
acgr_gXX = { start_level = 3
             start_cost_modifier = 0
             nation_designer_trigger = { always = no } }
```

两点值得注意：
1. `nation_designer_trigger = { always = no }` → 这 36 组在国家设计器里**不可选**，是"内部注册用"的痕迹，佐证它们是被当作 `unit_type` 的命名空间占位注册，而不是给玩家选的科技组。
2. 36 组都没有 `nation_designer_unit_type` 字段（对比 `WS:98 / 103 / 151 / 174` 的 `nation_designer_unit_type = sub_saharan / south_american / high_american`）→ 组内不预设兵种，兵种一律由国家 history 的 `unit_type =` 指定。

### 2.4 `tables` 段三方一致

`WS:232–236` = `MOD:397–401` = `PT` 同段：`adm_tech/dip_tech/mil_tech` 三条映射未改。

---

## 3. `acgr_gXX` 引用溯源（表格：引用类型 / 文件数 / 代表证据）

统计口径：严格正则 `acgr_g\d\d`（已排除 `acgr_genertic.*`、`acgr_gorakubu_*`、`Acgr_government` 等前缀误命中）。

| 引用类型 | `MOD` | `WS` | `PT` | 代表证据 |
|---|---|---|---|---|
| `common/technology.txt` 组定义 | 36 组 | **0** | 36 组 | `MOD/common/technology.txt:214`（g01）…`:389`（g36） |
| `history/countries` `unit_type = acgr_gXX` | **280 文件 / 280 行** | 0 | **284 文件 / 284 行** | `MOD/history/countries/ABY - Abydos.txt:2`；`MOD/history/countries/ALC - Alice Margatroid.txt:2`；`PT/history/countries/ABD - Albedo.txt:2` |
| `history/countries` `technology_group = acgr_gXX` | **0** | 0 | **284 文件 / 284 行** | `PT/history/countries/ABY - Abydos.txt:9`；`PT/history/countries/ABD - Albedo.txt:10` |
| `history/countries` `set_country_flag = acgr_unit_group_gXX` | 280 行 | 0 | 280 行 | `MOD/history/countries/ALC - Alice Margatroid.txt:3` |
| `common/countries/*.txt` `historical_units = { acgr_gXX_* }` | **284 文件 / 4953 行** | 0 | 0（未覆盖母 mod 的文件，沿用母 mod 内容） | `MOD/common/countries/Abydos.txt:22–43`（`# BEGIN ACGR_UNIT_GROUPS PREFERRED MODELS`） |
| `common/units/*.txt` `unit_type = acgr_gXX` | **972 文件 / 974 行** | 0 | **72 文件 / 72 行（全部 = `acgr_g01`，疑为偷懒/占位）** | `MOD/common/units/acgr_g01_cavalry_03.txt:3`；`PT/common/units/artillery_gen_t10_01.txt:4` |
| `common/technologies/mil.txt` `enable = acgr_gXX_*` | **855 行 / 1 文件** | 0 | 855 行 / 1 文件 | `MOD/common/technologies/mil.txt:136–234`（MIL 3 块）等 17 个块，见 §5 |
| `common/scripted_effects` | **1 文件 / 37 行**（36 条 `change_unit_type` + 108 行 flag 操作） | 0 | 0（该文件由母 mod 提供，PT 不重复覆盖） | `MOD/common/scripted_effects/ACGR_unit_group_effects.txt:42–49`（`acgr_use_g01_unit_group_effect`）、`:3–40`（清旗标） |
| `common/scripted_triggers` | **0** | 0 | 0 | 仅 `acgr_gorakubu_*` 前缀误命中（`MOD/common/scripted_triggers/acgr_calculation_triggers.txt:1,5,44`） |
| `common/governments/` | **0** | 0 | 0 | 全库无命中 |
| `common/government_reforms/` | **0** | 0 | 0 | 仅 `Acgr_government` 类名误命中（`MOD/common/government_reforms/republics_base.txt:1`） |
| `common/ideas/` | **0** | 0 | 0 | 全库无命中 |
| `events/` | **0** | 0 | 0 | 仅 `acgr_genertic.*` / `acgr_gorakubu_*`（`MOD/events/ACGR_genertic_mission_events.txt:1`） |
| `missions/` | **0** | 0 | 0 | 仅 `MOD/missions/ACGR_missions.txt:134`（`acgr_genertic.1`） |
| `decisions/` | **0** | 0 | 0 | 仅 `MOD/decisions/yureyuri_decisions.txt:322`（`acgr_gorakubu_*`） |
| `history/provinces` `discovered_by = acgr_gXX` | **0** | 0 | **2945 文件 / 42905 行** | `PT/history/provinces/1-Uppland.txt:22–27`（4 条原版 + 23 条 acgr） |
| **全库合计（严格口径）** | **7134 行 / 约 1585 文件** | **0** | **约 44000 行 / 3302 文件** | — |

### 3.1 母 mod 是否存在"动态切换科技组"

**没有。** `set_technology_group|change_technology_group` 在 `MOD` 全库命中 60 处，值**全部是原版组**，0 处指向 `acgr_gXX` 或 `tech_gensokyan`：

- `MOD/common/government_mechanics/20_egyptian_westernization.txt:599` → `change_technology_group = western`
- `MOD/common/government_reforms/04_government_reforms_tribes.txt:676,684,692,…,945` → `muslim/eastern/north_american/andean/mesoamerican/aboriginal_tech/chinese`
- `history/countries` 层直接用 `technology_group =` 静态赋值（`MOD/history/countries/ABY - Abydos.txt:9`）

母 mod 的动态切换发生在**兵种组**上，用的是另一个效果：

- `MOD/common/scripted_effects/ACGR_unit_group_effects.txt:45` `change_unit_type = acgr_g01`（…`:360` = g36，共 36 条）
- 调用范式：`acgr_use_gXX_unit_group_effect = { if = { limit = { NOT = { has_country_flag = acgr_unit_group_gXX } } change_unit_type = acgr_gXX ; acgr_clear_unit_group_flags_effect = yes ; set_country_flag = … } }`（`:42–49`）
- `has_country_flag = acgr_unit_group_gXX` 全库 72 行（6 个效应各 12 处判定/清除）；`set_country_flag …` 共 388 行（280 国家 history + 108 效应内）。

**结论**：谁也没在运行时切科技组；科技组是 1444 年书写死的。所谓"36 组新科技组"实际是兵种组的静态注册表 + 国家 history 的静态 `unit_type`，加上一个效果层面的兵种组切换器。

---

## 4. `tech_gensokyan` 引用面（表格）

### 4.1 `WS` 全库（2131 个 txt 文件，全量扫描）

| 引用位置 | 行数 | 文件数 | 代表证据 |
|---|---|---|---|
| `history/provinces/*.txt` `discovered_by = tech_gensokyan` | **1870** | **1870** | （基线第 9 条已核实） |
| `common/units/*.txt` `unit_type = tech_gensokyan` | **72** | **72** | `WS/common/units/infantry_gen_t1_01.txt:4`、`cavalry_gen_t1_01.txt:4`、`artillery_gen_t7_01.txt:4` |
| `history/countries/*.txt` `technology_group = tech_gensokyan` | **36** | **36** | `WS/history/countries/ALC - Alice Margatroid.txt:6` … `YYK - Saigyouji Yuyuko.txt:6` |
| `common/technology.txt` 组定义 | **1** | **1** | `WS/common/technology.txt:213` |
| `common/scripted_effects|scripted_triggers|events|decisions|missions|ideas|governments|government_reforms` | **0** | 0 | 全库无命中 |
| **合计** | **1979** | 1979 | — |

补充：`WS/history/countries` 42 个文件中，6 个不是 `tech_gensokyan`——`AIU`（sub_saharan）、`BLS`/`HMC`/`QNG`（chinese）、`NNM`（western）、`TMY`（western）；其中 `AIU/BLS/HMC/QNG` **在母 mod 里不存在**（我方独占国家，不能删）。`WS/decode_localisation/history/` 下还有 4 个同内容副本（同上 4 国），也不含 `tech_gensokyan`。

### 4.2 `PT` 全库（3431 个 txt 文件，全量扫描）

**`tech_gensokyan` 命中 = 0 行 / 0 文件。**

→ **幻想乡科技组体系在合作伙伴版里被整体、彻底废弃**：组定义没了（§1）、`technology_group` 赋值全改成 `acgr_gXX`（284 文件）、`unit_type` 也跟着改成 `acgr_gXX`（284 文件）、兵种文件的 `unit_type` 被批量改成 `acgr_g01`（72/72 文件）、1870 省 `discovered_by` 被删并替换成 `acgr_gXX` 子集（2945 文件 / 42905 行）。

这是一次**破坏性迁移**，不是"补上母 mod 新内容"。

---

## 5. 科技表与兵种组绑定机制（证据）

### 5.1 绑定关系分三层定义

| 层 | 字段 | 作用 | 证据 |
|---|---|---|---|
| 兵种 → 组 | `common/units/*.txt` 内 `unit_type = <组名>` | 该兵种实例归属哪个兵种组 | `MOD/common/units/acgr_g01_cavalry_03.txt:2–3`（`type = cavalry` / `unit_type = acgr_g01`）；`WS/common/units/infantry_gen_t1_01.txt:3–4`（`unit_type = tech_gensokyan`）；`VAN/common/units/aboriginal_infantry.txt:3–4`（`unit_type = aboriginal_tech`） |
| 国家 → 组 | `history/countries/*.txt` 的 `unit_type = <组名>` | 该国用哪套兵种（**与 `technology_group` 解耦**） | `MOD/history/countries/ABY - Abydos.txt:2`（`unit_type = acgr_g18`）+ `:9`（`technology_group = muslim`）→ 两个值不同；原版同型写法 `VAN/history/countries/ADA - Adal.txt:3–4`（`technology_group = east_african` / `unit_type = sub_saharan`） |
| 组 → 科技等级 | `common/technologies/mil.txt` 每个 `technology = { … enable = <兵种名> }` | 某兵种在第几级军事科技解锁（**全局一张表，不按组分表**） | `MOD/common/technologies/mil.txt:136`（`# BEGIN ACGR_UNIT_GROUPS MIL 3`）`:137 enable = acgr_g01_infantry_03` … `:234`（`# END`） |

**所以「兵种组 ↔ 科技等级」的确切定义位置 = `common/technologies/mil.txt` 各 `technology{}` 块内的 `enable =` 行**；「兵种 ↔ 兵种组」在 `common/units/*.txt` 的 `unit_type`；「国家 ↔ 兵种组」在 `history/countries` 的 `unit_type`。

### 5.2 母 mod 没有"按组分表"，也没有新增等级

- `technology = {` 块数：VAN 33 / MOD 33 / PT 33 / WS 33 —— **同一套 0–32 级，谁都没加等级**。
- `MOD` 只是在既有等级内插入 17 个 acgr 兵种解锁块（`mil.txt` 行号：136–234、303–359、402–428、517–578、632–684、704–707、750–810、888–944、991–1055、1106–1121、1165–1201、1254–1308、1394–1402、1465–1565、1682–1769、1837–1948、2271–2376；对应 MIL 3/5/6/9/10/11/12/14/15/17/18/19/22/23/26/28/30），共 **855 条 `enable = acgr_gXX_*`**。
- `MOD/common/technologies/mil.txt` = 2417 行 / 1791 条 `enable`（其中 855 acgr + 一批 `acgr_k01..k07` 旁支 + `miku_future_knights_*` / `Slave_warriors` / `Jin_Yiwei` / `Yuling_Army`）。
- 除 855 条 acgr 的 `enable` 外，**`mil.txt` 不含任何把组名当科技表键的写法**（无 `acgr_gXX = { … }` 子块）。

### 5.3 为什么兵种组必须写进 `common/technology.txt`（机制原因）

原版严格校验：`VAN/common/units/*.txt` 里出现的 14 个 distinct `unit_type` 值 **100% 都等于原版的科技组名**，一个例外都没有：

```
vanilla unit_type distinct = 14   （aboriginal_tech, andean, central_african, chinese, east_african,
                                   eastern, high_american, indian, mesoamerican, muslim, nomad_group,
                                   north_american, polynesian_tech, south_american, sub_saharan, western 的子集）
unit_type NOT in technology.txt groups = （空）
```

`MOD` 侧同样自洽：42 个 distinct `unit_type` 全部能在 `MOD/common/technology.txt` 的 55 个组名里找到（0 例外）。

→ **`unit_type` 与 `technology_group` 共用同一套「组名」命名空间**，所以母 mod 要新增兵种组，必须先把它注册成 technology 组（这就是 36 个"空壳科技组"存在的原因：`start_level 3` / `cost 0` / `nation_designer_trigger always no`）。

**推论（未验证引擎源码，标注为推断）**：`WS` 覆盖 `technology.txt` 抹掉 36 个组名后，`unit_type = acgr_gXX` 会解析失败（母 mod 的 280 国 + 972 兵种文件受影响），而 855 条 `enable = acgr_gXX_*` 也失去宿主。

### 5.4 视野 / sight 也是同一套命名空间

`discovered_by = <组名>`（省份文件）同样吃这套组名：
- `MOD` 省份 **0 处** acgr（`history/provinces` 全库 0 命中），母 mod 做法是让幻想乡国家用 `western`（29 国）/`muslim`（7 国）科技组，直接复用原版 4 条 `discovered_by` → **母 mod 完全不需要改省份视野**。
- `PT` 反过来：把 36 国 `technology_group` 改成 `acgr_gXX`，就必须给每个省补 `discovered_by = acgr_gXX`（`PT/history/provinces/1-Uppland.txt:15–18` 原版 4 条 + `:22–27` 起的 acgr 子集；2945 文件 / 42905 行，平均 14.6 条/省，且各省集合不一致）。

---

## 6. 幻想乡科技组归宿：方案 A/B/C 对比与推荐

补充事实（三方案共同前提）：

- `MOD` 已把 36 个幻想乡国家的 `technology_group` 写成 `western`(29 国：ALC,EIR,FLD,HKR,HML,HNA,HNK,HSY,IBK,IRK,KGY,KMJ,KZK,MRS,NMK,OKK,PCL,QLN,RES,RML,SJY,SKR,SKY,SMM,TES,YKR,YOM,YUK,YYK) / `muslim`(7 国：HKH,KSN,KTY,MRY,WNT,WNY,YSK)，并写入 `unit_type`：g01 ×30、g02 ×5（EIR/KGY/RES/WNT/WNY）、g09 ×1（SKR）。
- 兵种组语义（读母 mod 兵种注释 UTF-8）：`g01` = 妖怪/天狗/幻想乡机动禁卫（32 兵种文件，34 国）；`g02` = 月兔/月都系（18 兵种，5 国）；`g09` = 使魔/魔法学院系（46 兵种，39 国）。
- `WS` 与 `MOD` 的 36 个国家 history 文件 diff：**30 国仅差 6 行**（母 mod 多 4 行 acgr 块 + `technology_group` 值不同）；**2 国实质分歧**：`SKR`（母 mod 改名为 `SKR - Kinomoto Sakura`，并改 `government_rank 1→2`、`primary_culture cards_magic_culture→channeling_magic_culture`、`SKR_clow_card_reform→acg_universal_government_reform_1`、ruler 属性/寿命，共 23 行差）与 `NMK`（`Touhou_Republic_government_reform→Fujiwara_Mokou_government_reform`，8 行差）。

### 方案 A：`WS` 保留 `tech_gensokyan` + 并入 36 个 `acgr_gXX`（56 组）

| 项 | 内容 |
|---|---|
| 要改的文件 | ① `WS/common/technology.txt` → 用 `MOD` 版（55 组）末尾追加 `tech_gensokyan` 块，得 56 组；② `WS/common/technologies/mil.txt` → 用 `MOD` 版（2417 行/1791 enable）末尾/对应等级插入我方 71 条 `enable = *_gen_t*`（可直接照抄 `PT/common/technologies/mil.txt`，那已经是"母 mod + 74 条我方 enable、0 条母 mod 内容丢失"的正确合并结果） |
| 要改的引用点 | **0 处引用改写**：36 country 文件、72 兵种文件、1870 省文件全不动 |
| 额外必须补的一致性 | 母 mod 的 `common/countries/{36}.txt` 含 `historical_units = { acgr_g01_* }`（`MOD/common/countries/Abydos.txt:22–43`），而我国 `unit_type` 仍是 `tech_gensokyan` → 二选一：(a) 36 个国家 history 各加 1 行 `unit_type = acgr_gXX`（+36 行，兵种模型走母 mod，我方 gen_t* 变成死资源）；(b) 自建 36 个 `common/countries/*.txt`，`historical_units` 写我方 `*_gen_t*`（+36 文件、约 180 行） |
| 保留的收益 | 我方 gen_t* 兵种数值/命名体系全留；幻想乡仍是独立科技组（自定义空间最大） |
| 与母 mod 未来更新的冲突 | **中**：`technology.txt` + `mil.txt` 两个"整文件覆盖"必须每次母 mod 更新后重跑合并。可控（母 mod 用 `# BEGIN/END ACGR_UNIT_GROUPS` 标记块，合并可脚本化；`mil.txt` 我方 enable 与 acgr 块不重叠，出冲突概率低） |
| 遗留负担 | 1870 省 `discovered_by = tech_gensokyan` 必须继续维护（且与省份层"母 mod 新版省份覆盖"冲突纠缠，见 00_baseline 冲突 1/2） |

### 方案 B：废弃 `tech_gensokyan`，改用母 mod 已写好的 `acgr_gXX`（**推荐**）

| 项 | 内容 |
|---|---|
| 要改的文件 | ① **删** `WS/common/technology.txt`（母 mod 的 55 组直接生效）；② **删** `WS/common/technologies/mil.txt`（或换成母 mod 原版：我方 71 条 gen enable 在 B 下已无宿主）；③ **删** `WS/history/countries` 里 30 个"仅差 6 行"的国家覆盖文件（母 mod 版更好：带 `unit_type` 与 acgr 块）；④ `SKR`、`NMK` 两个文件**手工合并**（保留我方 `SKR_clow_card_reform`/`Touhou_Republic_government_reform` 等自研内容，同时补母 mod 的 `unit_type`+`set_country_flag` 两行）；⑤ `AIU/BLS/HMC/QNG`（母 mod 无此 4 国）**保留不动**；⑥ 72 个 `*_gen_t*` 兵种文件转为死资源（可留可删） |
| 要改的引用点 | 36 个国家 history 的 `technology_group` 由 `tech_gensokyan` → 母 mod 的 `western/muslim`（其中 30 国直接删覆盖文件即可，等于 0 手工改写；`SKR`/`NMK` 各 1 行 + 各 2 行 acgr 块） |
| 附带大收益 | **1870 个省的 `discovered_by = tech_gensokyan` 全部作废**（我方国家改用 western/muslim，直接命中原版 `discovered_by`）→ 这 1870 个省份覆盖文件从"科技组层必需"降级为"仅承载省份定制"，**00_baseline 冲突 1 在本层被消解**，并大幅缩小冲突 2 的处理面 |
| 与母 mod 未来更新的冲突 | **最低**：我们不再持有 `technology.txt`/`mil.txt`/36 国 history/兵种文件，母 mod 怎么改都不会打架；只需在母 mod 更新时复核 `SKR`/`NMK` 两个手工合并点 |
| 代价 | 失去我方 gen_t* 兵种数值体系（改用母 mod 的 g01/g02/g09 三套）；7 国（HKH/KSN/KTY/MRY/WNT/WNY/YSK）变 `muslim`（`start_cost_modifier 0.40` vs 原 0）——`start_cost_modifier` 在现代版本的精确作用存疑，见 §7 |

**B'（B 的保守变体，值得并行评估）**：科技组跟母 mod 走（`western`/`muslim`），但**保留我方兵种**——36 国 history 各加 1 行 `unit_type = tech_gensokyan`，`technology.txt` 只追加 `tech_gensokyan` 一组（仍要 56 组合并文件）。兵种文件 72 个、mil enable 71 条全部保留；省份 1870 条仍可作废。代价是母 mod 的 `historical_units`（acgr_g01_*）与我方 `unit_type` 不匹配，需自建 36 个 `common/countries` 覆盖（否则兵种模型/名称走母 mod 而数值走我方，观感错位）。

### 方案 C：直接把 `tech_gensokyan` 改名为某个 `acgr_gXX`（兵种文件不动）

| 项 | 内容 |
|---|---|
| 要改的文件 | ① `common/technology.txt`：不能简单改名——母 mod 的 `acgr_g01` 已存在，必须写成"合并版 55 组、把 `acgr_g01` 定义体改成 `tech_gensokyan` 的体"（或按国家分流到 g01/g02/g09 三组，则需 3 个组体都被改写）；② 36 个国家 history 的 `technology_group`；③ 72 个兵种文件的 `unit_type`；④ **1870 个省文件的 `discovered_by`**（否则全国失明） |
| 要改的引用点 | **约 1979 行**（1 + 36 + 72 + 1870），是本方案最大成本项 |
| 与母 mod 未来更新的冲突 | **高**：把 `acgr_g01` 的定义体改成我方体，等于劫持母 mod 34 国共用的 g01 组（`MOD` 侧 g01 有 34 国），母 mod 一改 g01 的 `start_level`/`nation_designer_*` 就打架；且我方 30 国塞进 g01 后，兵种树与母 mod 的一次改名强绑定。**同时与母 mod 已写好的 `technology_group = western` 直接矛盾**（下一版更新会把我们覆盖回去） |
| 结论 | 反向操作，不建议 |

### 推荐

**推荐 B（必要时 B'）**，理由按权重：

1. **与母 mod 的设计意图一致**：母 mod 已经把 `tech_gensokyan` 删干净并迁到 `western/muslim` + `acgr_g01/g02/g09`，我们的 submod 逆向保留它，等于每版都要和母 mod 抢 36 个国家 history 文件。
2. **消解 00_baseline 冲突 1**：1870 省 `discovered_by` 从"必须维护"变成"可退役"，是本层能给出的最大结构性减负。
3. **改动最省**：手工工作量 = 2 个文件（SKR/NMK）合并 + 4 个我方独占国保留；其余全是"删覆盖"。
4. 若策划要求保住 gen_t* 兵种数值，则走 B'：多 36 行 `unit_type` + 36 个 `common/countries` 覆盖 + 56 组合并版 `technology.txt`，仍比 A 轻（A 还要长期背 1870 省视野），比 C 轻得多。

对 `PT` 的处置建议（供 Lead 决策）：**`PT` 的科技组层不可直接采纳**——它把 284 国 `technology_group` 改成 `acgr_gXX`（`PT/history/countries/ABY - Abydos.txt:9`），并为此重写 2945 个省份、42905 行 `discovered_by`，且各省 acgr 子集不一致（`1-Uppland.txt` 23 条，别省不同），会造成"某幻想乡国家看不见某省"的视野漏洞；同时 72 个我方兵种文件被批量改成 `unit_type = acgr_g01`（`PT/common/units/artillery_gen_t10_01.txt:4`），与文件名/编制语义完全脱节。唯一值得吸收的是 `PT/common/technologies/mil.txt`——它确实是"母 mod 2417 行 + 我方 74 条 enable、0 条母 mod 内容丢失"的正确合并产物，可作为方案 A 的现成参考件。

---

## 7. 不确定项

1. **`unit_type` 指向未注册组时的引擎行为**：本文按"原版 42/42 `unit_type` 值都在 `technology.txt` 组名集合内"推断"未注册 = 解析失败/回退默认"。缺什么证据：EU4 引擎源码或 `error.log` 实测样本（需要在 `WS + MOD` 当前组合下实际启动一盘游戏并抓 `logs/error.log` 的 `unit_type` 报错）。**这是判定 `WS` 当前状态破坏程度的关键，建议在整合后跑一次启动日志验证。**
2. **`historical_units` 与 `unit_type` 不匹配的后果**：`MOD/common/countries/Abydos.txt:22–43` 列了 18 个 `acgr_g18_*`，若国家 `unit_type = tech_gensokyan`（方案 A/B'），这些条目是被忽略、还是报错、还是照旧套模型？缺证据：同上，需 `error.log` 或实机观察军团模型/名称。
3. **`start_cost_modifier` 在当前版本的精确作用**：`muslim = 0.40` vs `acgr_gXX = 0` 的实际差异，我只确认了字段值与三方一致性，未确认 1.37 引擎是否仍用它算科技点（现代版本科技成本趋于统一，该字段可能只影响国家设计器/开局等级）。缺证据：EU4 wiki 该字段页 + 原版 `defines` 核对。
4. **`discovered_by` 是否对未使用组有副作用**：方案 B 下保留 1870 条 `discovered_by = tech_gensokyan`（若省份层决定不删）时，只要 `tech_gensokyan` 组仍被注册（56 组版），这些行是惰性的；若组被彻底删除，这些行是否报错未知。缺证据：同 1。
5. **`MOD` 对 36 国科技组的语义选择是否稳定**：29 国 `western` / 7 国 `muslim` 的划分依据（月都系 vs 幻想乡系？）只能从 tag 名单反推，未见母 mod 注释说明。缺证据：母 mod 更新日志/作者说明。
6. **`acgr_g07` 的旁支归并**：`acgr_k01..k07`（117 文件）与 `acgr_g07s`（21 文件）的文件名前缀与声明组不一致，实际 `unit_type` 全写 `acgr_g07`（138 处 mismatch）。这不影响本层结论（36 组注册表完整），但说明母 mod 内部命名有历史包袱，若方案 B 要"逐国挑组"需按 `unit_type` 实值而非文件名判定。
