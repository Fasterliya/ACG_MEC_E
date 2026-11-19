# 适配调查 — 事实基线（Lead 已核实）

调查时间：2026-11-18
三个数据源：

| 代号 | 路径 | 角色 |
|---|---|---|
| `WS` | `F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E` | 本工作区 = 我方 submod（**已 git 干净**，HEAD `6447ea4`） |
| `PT` | `C:\Users\HP\Downloads\ACG_MEC_E\ACG_MEC_E` | 合作伙伴版本（**git HEAD `008208b`，工作树 3327 处未提交改动**） |
| `MOD` | `F:\SteamLibrary\steamapps\workshop\content\236850\2796854877` | 母 mod ACG1（更新后的新版） |

## 已核实事实

1. `WS` 与 `PT` 同一 git 仓库（`https://github.com/Fasterliya/ACG_MEC_E.git`），`PT` HEAD 落后 `WS` 一个提交（`6447ea4 Update SKR_card_modifiers.txt`）。
2. `WS` 工作树 0 改动；`PT` 工作树 3327 处改动：`M` 2020 / `D` 1 / `??` 1306。
   - 按目录：`history/provinces` 2954、`history/countries` 284、`common/units` 72，其余零散（ideas 2、governments 2、technologies 1、technology.txt 1、missions 2、decisions 2、localisation 1、interface 1、static_modifiers 1、event_modifiers 1、estate_privileges 1、buildings 1、diplomatic_actions 1）。
3. 科技组数量：
   - `MOD` `common/technology.txt` 8335 B，**55 组**：原版 18 + `test_group_2`、`acg_american` + **新增 `acgr_g01`..`acgr_g36`（36 个）**。
   - `WS` 同文件 4612 B，**20 组**：原版 18 + `test_group_2`、`acg_american` + `tech_gensokyan`。→ **整文件覆盖，会抹掉母 mod 的 36 个新组**。
   - `PT` 同文件 7934 B，**55 组**：等于母 mod 的 55 组，**但没有 `tech_gensokyan`**（幻想乡科技组被丢弃，36 个幻想乡国家将失去科技组）。
4. `WS` `history/countries` 仅 **42 个文件**，其中 **36 国** `technology_group = tech_gensokyan`（ALC/EIR/FLD/HKH/HKR/HML/HNA/HNK/HSY/IBK/IRK/KGY/KMJ/KSN/KTY/KZK/MRS/MRY/NMK/OKK/PCL/QLN/RES/RML/SJY/SKR/SKY/SMM/TES/WNT/WNY/YKR/YOM/YSK/YUK/YYK）。
5. `MOD` `history/countries` 中 `technology_group` 只用原版组（western 159、muslim 54、chinese 44、nomad_group 28、eastern 14、indian 2、ottoman 1、acg_american 1、east_african 1），**无任何 `acgr_gXX`，也无 `tech_gensokyan`**。→ 母 mod 的 36 个新组在 country history 层没人引用，引用点待溯源。
6. `MOD` 的 36 个 `acgr_gXX` 组定义体完全一致：`start_level = 3`、`start_cost_modifier = 0`、`nation_designer_trigger = { always = no }`（区别只在组名）。
7. `MOD` `common/units/` 兵种文件按 `acgr_gXX_<type>_<level>.txt` 命名，36 组均有兵种；注释（UTF-8）显示它们是**二次元兵种组**，其中多个明确是东方/幻想乡系：`g01` 妖怪突击队、`g02` 月兔列装射手、`g07` 遗库盾卫、`g09` 学院枪盾侍从/结界步兵、`g18` 学园近距射击队/百鬼夜行九州铁炮队、`g28` 妖族战兵、`g31` 人偶守备、`g32` 红魔见习术士、`g36` 乡团自警队 等。
8. `WS` 的幻想乡兵种以 `gen_t*`（另有 `_KSN` 后缀）命名，全部 `unit_type = tech_gensokyan`（`common/units/*.txt` 命中 40+ 文件）。
9. 省份覆盖规模：`WS` `history/provinces` **1904 个文件**，其中 **1870 个含 `discovered_by = tech_gensokyan`**；`MOD` `history/provinces` **2498 个文件**。
10. `PT` 对省份的典型改动（`1-Uppland.txt`、`10-Jamtland.txt`、`100 - Friesland.txt`）：
    - 删除 `discovered_by = tech_gensokyan`
    - 追加 22 条 `discovered_by = acgr_gXX`（g14/g18/g09/g08/g01/g07/g04/g11/g15/g21/g16/g02/g05/g32/g10/g22/g20/g23/g31/g12/g36/g24/g06，各省集合不一致）
    - 部分省份出现母 mod 新版的内容覆盖，例如 `culture = ShiraiKuroko` → `culture = supperability_magic_culture`（说明他直接拿母 mod 新版省份文件覆盖，我方 submod 的省份定制可能被一并冲掉）
11. `MOD` 省份文件里同一省只写 4 条原版 `discovered_by`（eastern/western/muslim/ottoman），**并未**给 36 个 `acgr_gXX` 写 discovered_by（`1-Uppland.txt` 核实）。→ 母 mod 的 36 组视野能力来自别处，或母 mod 本身就不需要（`acgr_gXX` 可能是"兵种组"而非"科技组视野组"）—— 待核实。

## 三个核心冲突的初步定位

- **冲突 1（科技组视野需逐省定义）**：`WS` 用 1870 省 × `discovered_by = tech_gensokyan` 解决幻想乡视野；母 mod 新增 36 组后若这些组也要视野，则省份 discovered_by 段要同时容纳两套，不能像 `PT` 那样删我方条目。
- **冲突 2（母 mod 改动省份）**：`WS` 的 1904 个省是旧母 mod 快照的覆盖，母 mod 新版已改（可能含 culture/owner/发展度/新省）。需逐省 diff 定位"母 mod 新版改了而我们仍在覆盖旧值"的省。
- **冲突 3（伙伴改动整合）**：`PT` 的 2954/284/72 处改动是"直接拿母 mod 新版文件覆盖"的产物，会同时抹掉我方定制；需区分"母 mod 新内容（必须吸收）"与"我方定制（必须保留）"。
