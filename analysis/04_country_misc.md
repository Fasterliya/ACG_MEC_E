# 04 国家 history 与杂项改动调查报告

调查范围：`WS`（本工作区）/ `PT`（合作伙伴工作树）/ `MOD`（母 mod ACG1 新版）。
只读三源，未读取任何 `localisation/` 内容。

---

## 1. 国家 history 三方对比

### 1.0 规模基线（本次实测，含 TAG 去重）

| 源 | `history/countries` 文件数 | 去重后 TAG 数 | `history/provinces` 文件数 | `common/countries` 文件数 |
|---|---|---|---|---|
| `WS` | 42 | 42 | 1904 | 3 |
| `PT` | 287 | 284（3 组重名文件，见 §3.5） | 2960 | 3（+1 未跟踪） |
| `MOD` | 303 | 303（无重名） | 2498 | 288 |

**结论：母 mod 的 `history/countries` 是 303 个文件。**

### 1.1 机制前提核实：`unit_type` 与 `technology_group` 的真实关系（Lead 问题的答案）

Lead 的假设「`unit_type` 一旦存在就优先于 `technology_group`，二者不能同时生效」**不成立，二者是正交的，同时生效**。证据链：

1. 本地 wiki 镜像 `历史修改.html:331-333`（国家历史基本格式）：
   ```
   technology_group = <group>      # 确定科技组和兵种组，默认是相同的
   unit_type = <group>             # 当科技组和兵种组不同时，单独设定兵种组
   ```
   wiki 原文明确二者**可以并存**，`unit_type` 只覆盖「兵种组」这一维。
2. `单位修改.html:327`：`unit_type = <technology group>  # 可选。设定该单位将会出现在某个特定科技组` → 兵种组在文件层面就是科技组名。
3. `Effects.html` 关于 `change_unit_type <type>`：「将兵种组改为指定类型……兵种组对应于科技组 /Europa Universalis IV/common/technology.txt」。
4. **原版实证**：`原版/history/countries/ABB - Dongola.txt:7-8` 同时写了
   ```
   technology_group = east_african
   unit_type = sub_saharan
   ```
   原版共有 **89 处** `unit_type`，取值 `sub_saharan`(73)/`south_american`(14)/`eastern`(1)/`western`(1)，全部是「科技组 ≠ 兵种组」的场景。所以 `technology_group` 决定科技成本/等级树，`unit_type` 决定用哪套兵种，**互不覆盖**。

**因此正确的取舍不是「二选一」，而是三个可分离的维度**：
- `technology_group`：科技树 / 科技成本 / `discovered_by` 视野判定
- `unit_type`：兵种数值与模型
- 国家 flag `acgr_unit_group_gNN`：**只作标记，母 mod 里 0 个调用点**（下文）

### 1.2 母 mod 的兵种组机制（真正的新架构）

`MOD` 的做法是把「兵种组」从科技组剥离：

| 证据 | 内容 |
|---|---|
| `MOD/history/countries/HKR - Hakurei Reimu.txt:1-10` | `# BEGIN ACGR_UNIT_GROUPS INITIAL ARMY` / `unit_type = acgr_g01` / `set_country_flag = acgr_unit_group_g01` / … / `technology_group = western` |
| `MOD/history/countries` 统计 | **303 个文件里 280 个**带 `# BEGIN ACGR_UNIT_GROUPS` 头（另 23 个是原版 TAG 覆写，见 §1.4） |
| `MOD/common/countries/Alice Margatroid.txt:21-42` | `# BEGIN ACGR_UNIT_GROUPS PREFERRED MODELS` + `historical_units = { acgr_g01_infantry_03 … acgr_g01_cavalry_30 }`（每国 18 条模型偏好，全库 4953 处 `acgr_g` 命中） |
| `MOD/common/scripted_effects/ACGR_unit_group_effects.txt:42-49` | `acgr_use_g01_unit_group_effect = { if = { limit = { NOT = { has_country_flag = acgr_unit_group_g01 } } change_unit_type = acgr_g01 … } }`，共 g01~g36 三十六段 |
| **全库调用点统计** | `acgr_use_gNN_unit_group_effect` 在**除定义文件外的调用点 = 0**。→ 这套 effect 是死代码，实际生效的只有 history 里的 `unit_type` |
| `MOD/common/scripted_effects/ACGR_unit_group_effects.txt:662-670` | `acgr_change_legacy_unit_type_effect = { if = { limit = { acgr_has_unit_assignment_trigger = yes } acgr_reapply_unit_group_effect = yes } else = { change_unit_type = $LEGACY_UNIT_TYPE$ } }` — 科技组变更后把兵种组重挂回去 |
| `MOD/common/scripted_effects/00_scripted_effects.txt:6639-6657` | `adopt_technology_group_from_target`：16 个原版组逐条 `change_technology_group = X` + `acgr_change_legacy_unit_type_effect = { LEGACY_UNIT_TYPE = X }` |
| `MOD/decisions/KGYdecision.txt:298-307` | KGY 决议：`acgr_change_legacy_unit_type_effect = { LEGACY_UNIT_TYPE = western }` + `change_technology_group = western`，**并对 `every_subject_country` 同样处理** |

母 mod 的设计意图很清楚：`technology_group` 保持原版组（科技成本/等级树/视野走原版），兵种走 `unit_type = acgr_gNN`（36 套二次元兵种美术与数值）。

**`WS` 的隐患**：`WS` 全库 `change_technology_group` 命中 **0 次**，但母 mod 的 `KGYdecision.txt` 会对 KGY 及其全部附庸执行 `change_technology_group = western`。一旦触发，这 36 国中的 KGY 系会被强行拉出 `tech_gensokyan`，且因 `acgr_has_unit_assignment_trigger` 为否（我方无 flag），兵种被 `change_unit_type = western` 兜底 → **科技组与兵种组双重脱离我方体系**。这是既有风险，不是合作方引入的。

### 1.3 42 国逐国对比表

差异字段分类：`U`=ACGR 兵种组段（`unit_type` + `set_country_flag`）；`T`=`technology_group`；`R`=`add_government_reform`；`K`=`government_rank`；`C`=`primary_culture`；`P`=`capital`；`M`=monarch 段；`F`=`historical_friend`；`X`=其它（`add_army_professionalism`/`national_focus`）。

| TAG | MOD 有? | 差异行数 | WS `technology_group` | MOD `technology_group` | MOD `unit_type` | 差异字段 |
|---|---|---|---|---|---|---|
| AIU | ✗ | — | `sub_saharan` | — | — | 母 mod 无此 TAG |
| ALC | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| BLS | ✗ | — | `chinese` | — | — | 母 mod 无此 TAG |
| EIR | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g02` | U,T |
| FLD | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| HKH | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g01` | U,T |
| HKR | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| HMC | ✗ | — | `chinese` | — | — | 母 mod 无此 TAG |
| HML | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| HNA | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| HNK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| HSY | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| IBK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| IRK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| KGY | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g02` | U,T |
| KMJ | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| KSN | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g01` | U,T |
| KTY | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g01` | U,T |
| KZK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| MRS | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| MRY | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g01` | U,T |
| NMK | ✓ | 8 | `tech_gensokyan` | `western` | `acgr_g01` | U,T,R |
| NNM | ✓ | 6 | `western` | `western` | `acgr_g08` | U,R |
| OKK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| PCL | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| QLN | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| QNG | ✗ | — | `chinese` | — | — | 母 mod 无此 TAG |
| RES | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g02` | U,T |
| RML | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| SJY | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| SKR | ✓ | 23 | `tech_gensokyan` | `western` | `acgr_g09` | U,T,R,K,C,M,F |
| SKY | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| SMM | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| TES | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| TMY | ✓ | 20 | `western` | `western` | `acgr_g09` | U,C,P,M,F,X |
| WNT | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g02` | U,T |
| WNY | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g02` | U,T |
| YKR | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| YOM | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| YSK | ✓ | 6 | `tech_gensokyan` | `muslim` | `acgr_g01` | U,T |
| YUK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |
| YYK | ✓ | 6 | `tech_gensokyan` | `western` | `acgr_g01` | U,T |

**统计口径**：
- `WS` 独有国家（母 mod 无此 TAG）= **4 个**：`AIU`、`BLS`、`HMC`、`QNG`。
- 母 mod 有而 `WS` 未覆盖 = **265 个 TAG**（303 − 38）。
- 双方都有且内容有差异 = **38 / 38**（100% 全有差异）。其中 **34 国差异只有 6 行**（4 行 ACGR 兵种组段 + 2 行科技组），说明 `WS` 的这 34 个国家文件**就是旧版母 mod 文件把 `technology_group` 换成 `tech_gensokyan` 的产物**，没有其它定制。
- 真正有额外定制的只有 4 国：

| TAG | `WS` 定制内容（相对母 mod 新版） |
|---|---|
| `NMK` | `add_government_reform = Touhou_Republic_government_reform`（母 mod 为 `Fujiwara_Mokou_government_reform`） |
| `NNM` | `add_government_reform = NNM_mikazuki_government_reform`（母 mod 为 `Magical_girl_government_reform`） |
| `SKR` | `add_government_reform = SKR_clow_card_reform`（母 mod 为 `acg_universal_government_reform_1`）；`government_rank 1`（母 mod 为 2）；`primary_culture = cards_magic_culture`（母 mod 为 `channeling_magic_culture`）；`historical_friend = TMY`（母 mod 删除）；monarch `birth_date 1428.4.1 / dip 5 / female = yes`（母 mod 为 `1428.11.11 / death_date 1821.12.31 / dip 4` + 3 条 `add_ruler_personality`） |
| `TMY` | `primary_culture = cards_magic_culture`（母 mod `channeling_magic_culture`）；`capital = 265`（母 mod **4726**）；`historical_friend = SKR`（母 mod 删除）；monarch `1428.9.3 / dip 5 / mil 3 / kind_hearted_personality`（母 mod 为 `1428.11.11 / death 1821.12.31 / dip 2 / mil 6`）；母 mod 新增 `add_army_professionalism = 0.04`、`national_focus = MIL` |

`cards_magic_culture` 与 `channeling_magic_culture` 在母 mod 新版里**同时存在**（`MOD/common/cultures/hre_cultures.txt:744` 与 `:365`），所以 `WS` 的引用不是死引用，只是母 mod 已把 SKR/TMY 改派到新文化。

### 1.4 母 mod 那 23 个不带 ACGR 头的国家文件

`MOD/history/countries` 里 23 个文件没有 `# BEGIN ACGR_UNIT_GROUPS`，全部是**原版 TAG 覆写**：
`ENG, ETH, GEN, LIT, MAM, MNG, MTS, PAL, PAP, POL, POR, PRA, PRO, RIB, RYA, SAX, SIL, SWE, TIM, TRA, TRE, TRI, TUR`。
`PT` 一个都没拿（`MOD 有 PT 无` 恰好等于这 23 个）。

因为 `WS`/`PT` 是叠在母 mod 上的 submod，**没拿 = 自动继承母 mod 的这 23 个文件**，功能无损。这反过来证明一个关键架构事实：**submod 不覆盖就自动继承母 mod，所以「母 mod 有的文件」绝大多数根本不需要复制进 `WS`**（见 §5 的重要推论）。

---

## 2. 首都/领土一致性交叉验证

### 2.1 `WS` 内部：国家 `capital` vs `WS/history/provinces` 的 `owner`

方法：解析 `WS` 1862 个数字命名省份文件的首个 `owner`（1637 个有 owner），与 42 国 `capital` 交叉。

| TAG | capital | `WS` 该省 owner | 判定 |
|---|---|---|---|
| `EIR` | 101 | **KTY** | 不一致 |
| `IBK` | 1247 | **IRK** | 不一致 |

**其余 40 个 TAG 全部一致，没有任何 capital 指向不存在或无 owner 的省。**

**但这两个不一致不是 `WS` 引入的**：母 mod 新版自己也是
- `MOD/history/countries/EIR*.txt` `capital = 101`，而 `MOD/history/provinces/101 - Genoa.txt` `owner = KTY`；
- `MOD/history/countries/IBK*.txt` `capital = 1247`，而 `MOD/history/provinces/1247 - Corsica.txt` `owner = IRK`。

`WS` 的 `101 - Genoa.txt:3` 与 `1247 - Corsica.txt:3` 与母 mod 完全一致（`owner = KTY` / `owner = IRK`）→ **这是母 mod 自带的 capital/owner 矛盾，我方向下继承**。EU4 对这种配置的表现是国家开局首都不属于自己（通常会导致该国 0 省或首都强制迁移）。属于需要在整合时一并修的低风险项，不是冲突。

### 2.2 `WS` 42 国首都在母 mod 新版里的归属

| TAG | capital | 母 mod 新版归属 | 结论 |
|---|---|---|---|
| `AIU` | 2274 | **母 mod 无该省文件**（原版有 2274；`WS` 覆盖之并置 `owner = AIU`） | 不丢，我方覆盖继续生效 |
| `BLS` | 636 | **母 mod 无该省文件**（同上） | 不丢 |
| `HMC` | 680 | `680 - Chongqing.txt` `owner = **SHJ**`（山海经） | **失去首都** |
| `QNG` | 1816 | `1816 - Beijing.txt` `owner = **QIN**`（秦） | **失去首都** |
| `EIR` | 101 | `owner = KTY` | 母 mod 同源矛盾（§2.1） |
| `IBK` | 1247 | `owner = IRK` | 母 mod 同源矛盾（§2.1） |
| 其余 36 国 | — | 各省 owner 与 TAG 完全一致 | 站得住 |

**净结论：36 个幻想乡国家在母 mod 新版省份里「全部站得住」；出问题的是 4 个 `WS` 独有国中的 `HMC`（重庆）与 `QNG`（北京），因为它们不是母 mod 的国家，母 mod 新版把这两省派给了 SHJ 与 QIN。**
→ 只要 `WS` 保留 `680 - Chongqing.txt`、`1816 - Beijing.txt` 两个省份覆盖（把 owner 写回 HMC/QNG），这两个国家就不会丢首都。这属于省份层待办，不是国家 history 层能修的。

---

## 3. 合作伙伴 284 国改动性质 + `tech_gensokyan`→`acgr` 映射

### 3.1 改动规模与拆分

```
git -C PT status --porcelain -- history/countries
  M  = 39
  ?? = 245
  合计 = 284
```

| 类别 | 数量 | 内容 |
|---|---|---|
| `M`（已跟踪被改） | 39 | `WS` 的 42 个文件里被改 39 个（未改的 3 个：`NNM - Nanami Yachiyo.txt`、`TMY - Tomoyo Daidouji.txt`、`QNG - Qing.txt`，`git diff` 无内容差异，仅行尾/BOM 变动） |
| `??`（新增未跟踪） | 245 | 全部来自母 mod 新版的国家文件（`MOD` 同名文件 245 / 245 命中） |

### 3.2 操作模式判定（抽样 10 个 `??` + 4 个 `M` 看全文 diff）

**`??` 新文件：100% 是「拿母 mod 新版国家文件，然后把 `technology_group` 改成与 `unit_type` 相同的 `acgr_gNN`」**。抽样 10 个（ABD/ABY/ACV/AGA/AKE/AKR/AMR/AOB/AOG/AQO）**每一个的 diff 都只有 2 行**：

```
=> technology_group = western      # 母 mod 原值
<= technology_group = acgr_g14     # 合作方改成与 unit_type 相同的组
```
（`=>` 为母 mod 侧、`<=` 为 `PT` 侧。）即 245 个文件 = 母 mod 原样 + 单行 `technology_group` 替换。

**`M` 文件：同样是「母 mod 新版内容 + 科技组替换」**。以 `ALC` 为例（`git -C PT diff` 全文）：

```diff
@@ -0,0 +1,4 @@
+# BEGIN ACGR_UNIT_GROUPS INITIAL ARMY
+unit_type = acgr_g01
+set_country_flag = acgr_unit_group_g01
+# END ACGR_UNIT_GROUPS
@@ -6 +10 @@ religion = Gensokyo_reg
-technology_group = tech_gensokyan
+technology_group = acgr_g01
```

`AIU`（母 mod 无此 TAG，合作方自行分配）：

```diff
-technology_group = sub_saharan
+technology_group = acgr_g09
+unit_type = acgr_g09
```

**判定：操作模式是「拿母 mod 新版国家文件覆盖，再把科技组改成 acgr 系」——即整体放弃 `tech_gensokyan`，不是在我方文件上做适配。**

### 3.3 关键问题：`tech_gensokyan` 是否被改成 `acgr_gXX`？——**是，全量改掉**

`PT/history/countries` 全目录 `technology_group` 取值分布（287 文件）：

- `technology_group = acgr_gNN`：**284 个文件**
- `technology_group = tech_gensokyan`：**0 个文件**
- 非 acgr 的 3 个：`western` ×2（`TMY - Tomoyo Daiji`/`TMY - Tomoyo`）、`chinese` ×1（`QNG - Qing`）

对照 `MOD` 同目录：只用原版组（`western` 159 / `muslim` 54 / `chinese` 44 / `nomad_group` 28 / `eastern` 14 / `indian` 2 / `ottoman` 1 / `acg_american` 1 / `east_african` 1），**`acgr_gXX` 命中 0**。

→ **合作方把母 mod 的 `unit_type = acgr_gNN` 误当成 `technology_group` 抄了一遍，并顺手删掉了我方的 `tech_gensokyan`。** 这是本次整合里最典型的「语义误读」型错误：母 mod 刻意保留原版 `technology_group`，`acgr_gNN` 只是兵种组。

### 3.4 映射表：原 `tech_gensokyan` → `PT` 的 `technology_group`

| TAG | 母 mod `unit_type` | `PT/technology_group` | `PT/unit_type` | 与母 mod `unit_type` 一致? |
|---|---|---|---|---|
| ALC | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| EIR | acgr_g02 | acgr_g02 | acgr_g02 | ✓ |
| FLD | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HKH | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HKR | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HML | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HNA | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HNK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| HSY | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| IBK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| IRK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| KGY | acgr_g02 | acgr_g02 | acgr_g02 | ✓ |
| KMJ | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| KSN | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| KTY | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| KZK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| MRS | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| MRY | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| NMK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| OKK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| PCL | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| QLN | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| RES | acgr_g02 | acgr_g02 | acgr_g02 | ✓ |
| RML | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| SJY | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| **SKR** | **acgr_g09** | acgr_g09（`SKR - Kinomoto Sakura.txt`）／**acgr_g01**（`SKR - Sakura Kinomoto.txt`） | 同左 | **✗ 两文件冲突** |
| SKY | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| SMM | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| TES | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| WNT | acgr_g02 | acgr_g02 | acgr_g02 | ✓ |
| WNY | acgr_g02 | acgr_g02 | acgr_g02 | ✓ |
| YKR | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| YOM | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| YSK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| YUK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |
| YYK | acgr_g01 | acgr_g01 | acgr_g01 | ✓ |

附（非 `tech_gensokyan` 但被 `PT` 一并改掉的）：
`NNM` `western`→`acgr_g08`；`TMY` 保持 `western`（未改，但母 mod 的 `unit_type = acgr_g09` 未复制进这份文件）；`AIU` `sub_saharan`→`acgr_g09`；`BLS` `chinese`→`acgr_g01`；`HMC` `chinese`→`acgr_g18`；`QNG` 保持 `chinese`。

**36 国里 24 国都是 `acgr_g01`**（妖怪系），只有 `EIR/KGY/RES/WNT/WNY` = `acgr_g02`（月兔系）、`SKR` = `acgr_g09` → 母 mod 的「差异化兵种组」实际上非常集中，这一点会直接影响 §3.6 的建议。

### 3.5 `PT` 的重复 TAG 文件（严重隐患）

`PT/history/countries` 有 3 组同 TAG 双份文件：

| TAG | 旧名（tracked） | 新名（未跟踪，来自母 mod） | 两份内容行差 |
|---|---|---|---|
| `SKR` | `SKR - Sakura Kinomoto.txt`（tech=`acgr_g01`） | `SKR - Kinomoto Sakura.txt`（tech=`acgr_g09`） | 24 |
| `TMY` | `TMY - Tomoyo Daidouji.txt`（tech=`western`，无 unit_type） | `TMY - Tomoyo.txt`（tech=`acgr_g09`，unit_type=`acgr_g09`） | 22 |
| `NNM` | `NNM - Nanami Yachiyo.txt`（tech=`western`，无 unit_type） | `NNM - Nanami Yachiyo .txt`（tech=`acgr_g08`，unit_type=`acgr_g08`） | 8 |

同 TAG 两份国家 history 会按加载顺序叠加覆盖，非重叠键会被「合并」成互相矛盾的配置（例如 SKR 两处 `technology_group` 取值不同、`add_government_reform` 不同、`government_rank` 不同）。**整合时必须二选一，不能沿用 `PT` 目录结构。**

### 3.6 `PT` 的 1 个 `D`（删除）文件

```
 D "history/provinces/2046 - Nasirabad.txt"
```

原因可查：母 mod 新版把该省份文件改名成了 **`2046 - Nasirabad.txt.txt`（双 `.txt` 扩展名，母 mod 侧的命名 bug）**。

| 源 | `2046 - Nasirabad.txt` | `2046 - Nasirabad.txt.txt` |
|---|---|---|
| `WS` | 有 | 有 |
| `PT` | **已删** | 有 |
| `MOD` | 无 | 有 |

`PT` 的删除动作是**正确的**（否则同省两份定义会互相覆盖），但它把母 mod 的双扩展名 bug 一起继承了。`0` 风险的连带问题：`WS` 自己现在同时有 `2046 - Nasirabad.txt` 与 `2046 - Nasirabad.txt.txt` 两份，**这是 `WS` 现状里的一个重复定义坑**（不属于本次 284 改动，但建议顺手清掉）。

---

## 4. 杂项改动逐个定性

判定方法：先把三份文件归一化（`CRLF/CR`→`LF`、去 BOM）再做行级比较，避免行尾差异污染结论。表中「`PT`=`MOD`」表示归一化后 0 行差异。

| # | 文件 | `PT` vs `MOD` | `PT` vs `WS` | 改了什么 | 风险 | 建议 |
|---|---|---|---|---|---|---|
| 1 | `common/diplomatic_actions/00_diplomatic_actions.txt` | **0（完全等于母 mod 新版）** | 142 | 整文件采用母 mod 新版，我方 `#ACG_MEC` 定制块被清除：`tooltip = ACG_MEC_E_cannot_deaclare`、`is_year = 1464` 起禁结盟条件、`ab_Magic_Gem` 魔力宝石相关 `add_country_modifier` / `Developing_productivity_reform_modifier_1→2` 等 | **高**。禁用结盟的窗口（1464+）与魔力宝石修正整段消失，玩法直接变形 | **必须回退**，并在母 mod 新版基础上重新并入我方块（母 mod 新增的 `imperial_realm_war_action` 要保留） |
| 2 | `common/estate_privileges/kirara_privileges.txt` | **0** | 38 | 采用母 mod 新版：`max_absolutism -10→-25`、`build_time 0.15→0.3`、`stability_cost_modifier 0.1→0.3`、`global_manpower_modifier 0.15→0.3` 等 12 处数值上调，并新增 2 处 `kirara_start_variable_cycles_effect = yes`（该 effect 定义在 `MOD/common/scripted_effects/kirara_lifecycle_effects.txt:1281`，母 mod 内共 13 处调用，`WS` 无定义 0 调用） | **中**。是母 mod 的重平衡，方向合理；但我方原本的数值体系会被替换 | **保留 `PT`（=母 mod）**，仅需确认我方是否曾有意采用更宽松的数值；无结构性损失（`WS`/`MOD` 各 300 个特权定义，无独有项） |
| 3 | `common/event_modifiers/SKR_card_modifiers.txt` | 母 mod **无此文件** | **0（与 `WS` HEAD 完全相同）** | 只有一处：`skr_clear_card_dawn` 的 `discipline = 0.5` → `technology_cost = -0.10`。这正是 `WS` HEAD 提交 `6447ea4 Update SKR_card_modifiers.txt` 的内容 | **无**。`PT` HEAD 落后一个提交，所以这处改动在 `PT` 里表现为「工作树改动」，实际与 `WS` 已提交内容等价 | **保留**（等价，无冲突） |
| 4 | `common/governments/reform_levels_monarchy.txt` | **0** | 10 | 整文件采用母 mod 新版，删除 `###ACG MEC E` 段 **8 条改革注册**：`NNM_mikazuki_government_reform`、`SKR_clow_card_reform`、`SKR_sakura_card_reform`、`SKR_clear_card_reform`、`BLS_black_shore_reform`、`HMC_qijian_reform`、`PLP_purple_heart_reform`、`YYK_netherworld_reform`；保留母 mod 新增的 `contact_with_miku_reform_mikuver` | **极高**。这 8 条改革**在母 mod 里根本不存在**（`MOD` 全库命中 0），被我方引用的次数：`BLS_black_shore_reform`/`HMC_qijian_reform` 各 8 次、其余各 5 次（`PT` 里同样还残留 7/4 次引用）。注册被删后 `add_government_reform = SKR_clow_card_reform` 变成对未注册改革的引用 → 我方 7 国（NNM/SKR/BLS/HMC/PLP/YYK）的政体改革全部失效 | **必须回退我方版本**，再把母 mod 新增的 `contact_with_miku_reform_mikuver` 补进去 |
| 5 | `common/governments/reform_levels_republic.txt` | **0** | 5 | 整文件采用母 mod 新版，丢失我方 2 条：`ACG_MEC_HNA_chronicle_reform`（`WS` 全库引用 17 次，`PT` 仍残留 16 次）、`idol_republic` 的 `acg_universal_government_reform_1` | **高**。`ACG_MEC_HNA_chronicle_reform` 在母 mod 中同样 0 命中 → 被删注册即失效，HNA 的编年史政体链断掉 | **必须回退我方版本** + 并入母 mod 新增的 `Fujiwara_Mokou_government_reform`、`NMK_solitary_dweller`、`NMK_Eternal_Flame`、`NMK_Beyond_life_and_death` |
| 6 | `common/ideas/00_basic_ideas.txt` | **0** | 1133 | 整文件采用母 mod 新版。结构性定义名两边几乎完全一致（`WS` 602 个花括号定义 / `MOD` 544 个，去重后 `WS` 无真实独有项），差异全部落在**数值与条件行**上 | **中-高**。母 mod 新版整体重写了基础理念数值；我方在该文件上的调参被一次性抹掉。因为旧母 mod 版本不可得，**无法用三方 diff 把我方定制与旧版母 mod 内容分开** | **保留 `PT`（=母 mod 新版）** 作为基线，若我方确实调过基础理念数值需人工重放；不要整体回退 `WS`（会把基础理念拉回旧母 mod 版本） |
| 7 | `common/ideas/new_countries_ideas.txt` | 42 | 374 | `PT` = 母 mod 新版 **+ 我方 `TMY_ideas` 完整块**（`MOD` 里没有该块：`MOD` 全库 `TMY_ideas` 命中 0）。我方 `TMY_ideas` 含 `Costume_designer`/`Video_documentation`/`Daidouji_fortune`/`Sakuras_guardian`/`Melody_of_hearts`/`Sakura_and_tomoyo`/`Eternal_friendship` 七条理念 | **低**。这是 `PT` 里少见的「正确合并」样本 | **保留 `PT`**（我方 `TMY_ideas` 保住了）。注意母 mod 新版新增 33 个定义（`MUS_ideas`、`CHN_ideas`、`CTL_ideas` 等）必须吸收，`PT` 已吸收 |
| 8 | `common/static_modifiers/acg_modifiers.txt` | 8 | 26 | `PT` = 母 mod 新版结构 + **保留我方佣兵数值**（`merc_maintenance_modifier = 0` / `mercenary_cost = 0` / `mercenary_discipline = 0` / `mercenary_manpower = 0`），而母 mod 新版已改成 `0.5 / 0.25 / 0.05 / -0.5`；`WS` 与 `PT` 的这 4 个值完全相同 | **低**。方向正确的合并（保留我方平衡 + 吸收母 mod 新条目） | **保留 `PT`**。但需最终拍板：佣兵到底是「零成本（我方）」还是「贵 50%（母 mod 新版）」 |
| 9 | `common/technologies/mil.txt` | 107 | 1051 | ① 采用母 mod 新版（含 1006 处 `acgr_` 内容）；② **把我方 72 条 `enable = *_gen_t*` 兵种解锁行插进母 mod 的全局 `technology` 块**（行 143~2055，保留原科技等级分布）；③ 配合 §3 把 72 个 `gen_t` 兵种文件的 `unit_type` 从 `tech_gensokyan` 改成 `acgr_g01` | **中**。这套改法让 72 个幻想乡兵种全部归入 `acgr_g01` 一个组，其余 35 组拿不到任何 `gen_t` 兵种；且 `tech_gensokyan` 组已从 `technology.txt` 删除，我方「幻想乡统一兵种组」体系被彻底拆解 | **部分保留**：`enable` 行的等级分布可参考，但 `unit_type` 归并到 `acgr_g01` 必须回退（见 §6 建议） |
| 10 | `common/technology.txt` | **0** | 193 | 整文件采用母 mod 新版：**55 组**（原版 18 + `test_group_2` + `acg_american` + `acgr_g01..g36`），**`tech_gensokyan` 被删除** | **极高**。`tech_gensokyan` 一消失，`WS` 的 36 国 `technology_group`、1870 省的 `discovered_by = tech_gensokyan`、72 个 `gen_t` 兵种的 `unit_type` 全部变成悬空引用 | **必须保留 `WS` 版本 + 补进母 mod 的 36 个 `acgr_gXX` 定义**（合并成 56 组），不能整文件覆盖 |
| 11 | `common/buildings/only_buildings.txt` | **0（新文件）** | 不存在 | `PT` 新增未跟踪文件，内容与母 mod 完全一致 | **无风险** | **按「submod 自动继承母 mod」原则不必纳入**；若要锁定母 mod 版本再纳入 |
| 12 | `interface/assets/zz_acggfx_units.gfx` | 母 mod **无此文件**（`MOD/interface/assets/` 为空目录） | 不存在 | `PT` 新增未跟踪文件，7.8 KB，定义 `pdxmesh = { name = "acggfx_generic_01_type1/type2" … }`，动画绑定 `polearm_twohanded_*` / `cavalry_rider_*` | **低-中**：全库共 10 处引用 `acggfx_generic_01_type`，但 **`PT`/`MOD`/`WS` 的 `gfx/models/Units/` 里 `acggfx*` mesh 文件数均为 0** → 这是**死引用 gfx**（对应 .mesh 不存在，只是模型缺失不崩游戏） | **不纳入**。属母 mod 旧版遗留或 `PT` 自建残留，无对应美术资源 |
| 13 | `decisions/dome_decisions.txt` | 母 mod **无此文件** | 不存在 | `PT` 新增未跟踪文件（合作伙伴自建决议，DOME=圆顶/穹顶系） | 需人工审阅内容后定性 | 先**不纳入**，等 YG 确认是否为本次要交付的新内容 |
| 14 | `decisions/IYS_decisions.txt` | **0** | 6 | 整文件采用母 mod 新版：我方把 `army_professionalism 0.50→0.8`、`army_tradition 50→95`、`else 分支 army_tradition 80→95` 的加严门槛被抹掉 | **中**。IYS（犬夜叉）决议的成本被我方收紧，恢复母 mod 值等于决议变容易 | 若我方门槛是有意设计 → **回退我方数值**；否则保留 |
| 15 | `missions/ACGR_missions.txt` | **0** | 2363 | **这是最危险的一条**：`WS` 的该文件 **838 行全部被 `#` 注释（有效行 0）**，即我方**故意停用母 mod 的 ACG 通用任务树**；`PT` 直接拿母 mod 新版覆盖（1588 行，有效行 1548），**把我方「停用」决定否定掉了** | **极高**。ACG 通用任务会给所有 anime 国家（`acgr_is_anime_country_trigger`）挂上整套任务树，与我方 36 国的专属任务叠加冲突 | **必须回退为「整文件注释」态**，然后按母 mod 新版内容重新同步后再整体注释（保持「内容最新、状态停用」） |
| 16 | `missions/IYS_missions.txt` | **0** | 4 | 整文件采用母 mod 新版：我方 3 处调整被抹——`IYS_modifier_1` 的 `duration 18250→7300`、`IYS_missions_3` 的 `change_mil = 1` 后新增 `kirara_check_sek_aid_effect = yes` 调用、`IYS_missions_10` 尾部空行 | **中**。`kirara_check_sek_aid_effect` 是母 mod 的 kirara 生命周期效果调用，被我方接进 IYS 任务奖励；现在丢失 | 若该接入是我方有意（把 sek aid 检查挂到 IYS 任务）→ **回退我方 3 处**；`duration 7300` 同理 |
| 17 | `localisation/DOME_l_english.yml` | 母 mod 无 | 不存在 | `PT` 新增未跟踪文件，437 B / 5 行 | 按项目纪律 | **仅记录：有改动、文件名 `localisation/DOME_l_english.yml`、437 B / 5 行、未读内容** |

**必须保留（`PT` 方向正确）**：#3、#7、#8。
**必须回退（`PT` 造成回归）**：#1、#4、#5、#10、#15，以及 #16/#14 的我方数值段。
**必须审核后再定**：#6、#9、#11、#12、#13、#17。

---

## 5. 1306 个新增文件盘点

`git -C PT status --porcelain` 里 `??` 条目 1306 条，展开后仍是 1306 个文件（两个目录条目 `common/buildings/`、`interface/assets/` 各含 1 个文件）。

### 5.1 按目录聚合

| 一级目录 | 数量 | 二级明细 |
|---|---|---|
| `history/` | **1302** | `history/provinces` **1057**、`history/countries` **245** |
| `common/` | 1 | `common/buildings/only_buildings.txt` |
| `decisions/` | 1 | `decisions/dome_decisions.txt` |
| `interface/` | 1 | `interface/assets/zz_acggfx_units.gfx` |
| `localisation/` | 1 | `localisation/DOME_l_english.yml` |
| `events/` | **0** | 无 |
| `missions/` | **0** | 无 |
| `gfx/` | **0** | 无 |

### 5.2 代表文件 20 个

`history/provinces`（1057，代表 10 个）：
`history/provinces/1 - Stockholm.txt`、`…/10 - Jamtland.txt`、`…/100 - Friesland.txt`、`…/101 - Genoa.txt`、`…/957 - Delaware.txt`、`…/2554 - Nanticoke.txt`、`…/1820 - …`、`…/2265 - …`（其余为 1057 个母 mod 新版省文件，`MOD` 同名率 100%，唯 957/2554 除外）

`history/countries`（245，代表 8 个）：
`history/countries/ABD - Albedo.txt`、`ABY - Abydos.txt`、`AGA - Asagiri Aya.txt`、`AKE - Akemi Homura.txt`、`AOG - Ainz Ooal Gown.txt`、`IYS -  Inuyasha.txt`、`SKR - Kinomoto Sakura.txt`、`TMY - Tomoyo.txt`

其余（4 个）：`common/buildings/only_buildings.txt`、`decisions/dome_decisions.txt`、`interface/assets/zz_acggfx_units.gfx`、`localisation/DOME_l_english.yml`

### 5.3 性质判定（判据：同名文件在 `MOD` 是否存在）

| 类别 | 数量 | 明细 |
|---|---|---|
| **`MOD` 有同名文件** → 属「母 mod 新版带来的新文件」 | **1301** | `history/provinces` 1055、`history/countries` 245、`common/buildings` 1 |
| **`MOD` 无同名文件** → 合作伙伴自建 / 从别处拷入 | **5** | `decisions/dome_decisions.txt`、`interface/assets/zz_acggfx_units.gfx`、`localisation/DOME_l_english.yml`、`history/provinces/957 - Delaware.txt`、`history/provinces/2554 - Nanticoke.txt` |

对 5 个例外进一步溯源：
- `957 - Delaware.txt`、`2554 - Nanticoke.txt`：**原版游戏有、母 mod 没有、我方没有**，`PT` 版本被大幅裁剪（`PT` 19 行 vs 原版 66 行；`PT` 16 行 vs 原版 41 行）→ 这是**合作伙伴从原版拷来并删减**的省份文件。作为 submod 覆盖原版 = 用残缺版本替换完整版，**没有任何收益，只会在原版后续更新时掩盖变化**。
- `dome_decisions.txt`、`DOME_l_english.yml`：`DOME` 前缀成套，合作伙伴新内容。
- `zz_acggfx_units.gfx`：见 §4 #12，死引用 gfx。

### 5.4 重要架构推论（建议 Lead 写进整合策略）

因为 `WS`/`PT` 是**叠在母 mod 上的 submod**，§1.4 已用 23 个原版 TAG 覆写文件证明：**不覆盖 = 自动继承母 mod**。所以这 1301 个 `MOD` 同名文件**没有必要复制进 `WS`**：

- 复制进去 → 内容等于母 mod（无收益）＋ 一旦我们改一行，就永久锁定该文件在旧版母 mod 内容上（有维护债）；
- 不复制 → 始终跟随母 mod 最新版；
- 而 `PT` 的实际结果正是复制后的反面教材：245 个国家文件全部被塞进错误的 `technology_group`，1057 个省文件被塞进 `discovered_by = acgr_gXX`（Baseline 已核实）+ 删除我方 `discovered_by = tech_gensokyan`。

**建议：1301 个母 mod 同名文件一律不纳入 `WS`；只保留我们确实要改的那 42 个国家文件（以及确实要改的省份文件）。** 5 个例外里 3 个（`957`/`2554`/`zz_acggfx_units.gfx`）建议丢弃，2 个（`dome_decisions.txt` / `DOME_l_english.yml`）待 YG 确认。

---

## 6. 母 mod 更新对国家的实质影响

### 6.1 母 mod 新增国家 TAG

- `MOD/history/countries` **303 个文件 / 303 个 TAG，无重复**；`MOD/common/country_tags/ACG_country_tag.txt` 291 行。
- `WS` 覆盖 **42** 个 TAG；其中 4 个（`AIU`/`BLS`/`HMC`/`QNG`）**母 mod 根本没有**，由 `WS/common/country_tags/ACG_MEC_E_country_tag.txt`（3 行：BLS/HMC/AIU）＋ 母 mod 提供其余。
- 母 mod 有而 `WS` 未覆盖 = **265 个 TAG**。代表 TAG：
  `ABD`(Albedo)、`ABY`(Abydos)、`AGA`(Asagiri Aya)、`AKE`(Akemi Homura)、`AOG`(Ainz Ooal Gown)、`AQO`(Aqours)、`ATR`(Altria Pendragon)、`BTR`(Gotou Hitori)、`CHN`(Kafuu Chino)、`EMT`(Emilia)、`FRR`(Frieren)、`HKY`(Hyakkiyako)、`IYS`(Inuyasha)、`KSR`(Kirima Syaro)、`MKM`(Mitsukasa Ayase)、`QIN`(Qin)、`SHI`(Shirai Kuroko)、`SHJ`(Shanhaijing)、`TRG`(Trinity)、`U01`~`U22`(赛马娘 22 国) 等。
- **无法用现有三源判定「哪 265 个是本版新增、哪 265 个是旧版就有但我方没覆盖」**——旧母 mod 快照不存在。可用的间接证据：`PT` 复制了其中 245 个，且复制的这 245 个在 `MOD` 全部存在（100% 命中），跳过的 23 个全是原版 TAG 覆写文件（§1.4）→ 说明 `PT` 是按「带 ACGR 兵种组＝二次元国」这条线整批复制的，与「新旧」无关。

### 6.2 母 mod 是否改了 `technology_group` 的分配逻辑？——**改了，但改的是「兵种组分配」，不是科技组**

| 层 | 母 mod 新版做法 | 证据 |
|---|---|---|
| 国家 history | `technology_group` 保持原版组；新增 `unit_type = acgr_gNN` + `set_country_flag = acgr_unit_group_gNN`（280/303 国） | `MOD/history/countries/HKR - Hakurei Reimu.txt:1-10` |
| 模型偏好 | `common/countries/*.txt` 新增 `historical_units = { acgr_gNN_* }`（每国 18 条） | `MOD/common/countries/Alice Margatroid.txt:21-42` |
| 兵种定义 | `common/units/` 按 `acgr_gXX_<type>_<level>.txt` 命名，36 组齐备 | `MOD/common/units/` |
| 科技组定义 | `common/technology.txt` 新增 `acgr_g01..g36`（36 组，定义体完全一致：`start_level = 3`、`start_cost_modifier = 0`、`nation_designer_trigger = { always = no }`） | `MOD/common/technology.txt`（55 组） |
| 兵种解锁 | `common/technologies/mil.txt` 内 `acgr_` 命中 1006 处 | `MOD/common/technologies/mil.txt` |
| **科技组切换钩子** | `adopt_technology_group_from_target`（16 个原版组逐一 `change_technology_group` + `acgr_change_legacy_unit_type_effect`） | `MOD/common/scripted_effects/00_scripted_effects.txt:6639-6657` |
| **国家层面的强制改科技组** | `KGYdecision.txt` 把 KGY 及其全部附庸 `change_technology_group = western` | `MOD/decisions/KGYdecision.txt:298-307` |
| `common/` + `events/` 全库 `technology_group` 引用 | **357 处**：`decisions` 146、`government_reforms` 97、`missions` 30、`scripted_effects` 17、`institutions` 16、`cb_types` 13、`events` 10、`estates` 8、`wargoal_types` 6、`ideas` 5、`ruler_personalities` 3、`subject_types` 2、`on_actions` 2、`insults` 1、`government_mechanics` 1 | 本次统计 |

**对 `WS` 的实质影响**：母 mod 的这些 `change_technology_group` 调用**全部只认原版组名**，没有一个分支处理 `tech_gensokyan`。所以只要 `WS` 保留 `tech_gensokyan`，这些母 mod 脚本一旦作用到我方 36 国（最典型是 KGY 决议），就会把我方国家**单向**拉出我方科技组，且没有回程路径。

### 6.3 `WS` 的 36 个幻想乡国家在母 mod 新版省份里的存续（详见 §2.2）

| 结论 | 数量 | TAG |
|---|---|---|
| 首都/领土在母 mod 新版**完全站得住** | 36 | 全部 36 个 `tech_gensokyan` 国 |
| **失去首都**（母 mod 把该省派给别人） | 2 | `HMC`（680 Chongqing → SHJ）、`QNG`（1816 Beijing → QIN） |
| 母 mod 同源 capital/owner 矛盾（非本次引入） | 2 | `EIR`（101 → KTY）、`IBK`（1247 → IRK） |
| 母 mod 无该省文件、由我方覆盖生效 | 2 | `AIU`（2274）、`BLS`（636） |

### 6.4 36 国逐国建议（Lead 问题 4）

**先定框架**（依据 §1.1 的三维可分离性）：

- **方案 A（建议默认）**：`technology_group = tech_gensokyan`，**不写** `unit_type` → 兵种沿用我方 72 个 `gen_t`（≈36 国统一幻想乡兵种组），科技树走我方。代价：放弃母 mod 的 `acgr_gNN` 兵种美术。
- **方案 B**：`technology_group = tech_gensokyan` + `unit_type = acgr_gNN`（母 mod 分配）→ **我方科技树 + 母 mod 兵种**，两者正交可并存（原版 `ABB`/`Dongola.txt:7-8` 即此写法）。代价：我方 72 个 `gen_t` 对这 36 国变死资源。
- **方案 C（`PT` 做法）**：`technology_group = acgr_gNN`，废弃 `tech_gensokyan`。**不建议**：会连带废掉 1870 省的 `discovered_by = tech_gensokyan`，且 `acgr_gNN` 科技组 `start_level = 3` 会让 36 国开局科技等级跳到 3。

**逐国建议表**（母 mod 分配的 `unit_type` 已核实，见 §1.3）：

| TAG | 母 mod `unit_type` | 建议 | 理由 |
|---|---|---|---|
| ALC | `acgr_g01` | **A** | 34 国里 24 国同为 `g01`，改用 `unit_type` 并无差异化收益，反废我方兵种 |
| EIR | `acgr_g02` | **A**（可选 B） | `g02`=月兔列装射手，与设定契合；若要月兔专属兵种可走 B |
| FLD | `acgr_g01` | **A** | 同上 |
| HKH | `acgr_g01` | **A** | 同上 |
| HKR | `acgr_g01` | **A** | 同上 |
| HML | `acgr_g01` | **A** | 同上 |
| HNA | `acgr_g01` | **A** | 同上 |
| HNK | `acgr_g01` | **A** | 同上 |
| HSY | `acgr_g01` | **A** | 同上 |
| IBK | `acgr_g01` | **A** | 同上 |
| IRK | `acgr_g01` | **A** | 同上 |
| KGY | `acgr_g02` | **A**（可选 B） | 月之都系，`g02` 契合；**优先处理 §6.2 的 KGY 决议强制转 western** |
| KMJ | `acgr_g01` | **A** | — |
| KSN | `acgr_g01` | **A** | — |
| KTY | `acgr_g01` | **A** | — |
| KZK | `acgr_g01` | **A** | — |
| MRS | `acgr_g01` | **A** | — |
| MRY | `acgr_g01` | **A** | — |
| NMK | `acgr_g01` | **A** | 同时需修 `add_government_reform`（母 mod 新增了 `Fujiwara_Mokou_government_reform`，我方用 `Touhou_Republic_government_reform`，二选一） |
| OKK | `acgr_g01` | **A** | — |
| PCL | `acgr_g01` | **A** | — |
| QLN | `acgr_g01` | **A** | — |
| RES | `acgr_g02` | **A**（可选 B） | 月兔系 |
| RML | `acgr_g01` | **A** | — |
| SJY | `acgr_g01` | **A** | — |
| SKR | `acgr_g09` | **A** + 保留我方整份 | `g09`=学院枪盾侍从/结界步兵，设定契合但收益不抵我方定制（我方有 `SKR_clow_card_reform`、`cards_magic_culture`、`historical_friend TMY`、monarch 全套、`government_rank 1`）；**且必须删掉 `PT` 的重复文件** |
| SKY | `acgr_g01` | **A** | — |
| SMM | `acgr_g01` | **A** | — |
| TES | `acgr_g01` | **A** | — |
| WNT | `acgr_g02` | **A**（可选 B） | 月兔系 |
| WNY | `acgr_g02` | **A**（可选 B） | 月兔系 |
| YKR | `acgr_g01` | **A** | — |
| YOM | `acgr_g01` | **A** | — |
| YSK | `acgr_g01` | **A** | — |
| YUK | `acgr_g01` | **A** | — |
| YYK | `acgr_g01` | **A** | — |

**非 `tech_gensokyan` 的 6 国**：

| TAG | 我方现状 | 母 mod `unit_type` | 建议 |
|---|---|---|---|
| `NNM` | `western`，无 `unit_type` | `acgr_g08` | **采用母 mod 的 `unit_type = acgr_g08`**（我方对她没有兵种定制，改用二次元兵种纯赚）；改革用我方 `NNM_mikazuki_government_reform` |
| `TMY` | `western`，无 `unit_type` | `acgr_g09` | **采用母 mod 的 `unit_type = acgr_g09`**；`capital` 建议改母 mod 的 `4726`（`265 - Brno` 属 TMY 但 Brno 是捷克地，母 mod 已迁都，且 `265` 在新版 `owner = TMY` 仍成立，二者都可，需 YG 拍板）；culture 建议跟随母 mod 改 `channeling_magic_culture` |
| `AIU` | `sub_saharan`，无 `unit_type` | 母 mod 无此 TAG | **保留我方** `sub_saharan`；可选 `unit_type = acgr_g09`（学院系）——但这是纯自定义，无母 mod 依据 |
| `BLS` | `chinese`，无 `unit_type` | 母 mod 无此 TAG | **保留我方** `chinese`；可选 `unit_type = acgr_g01`（`PT` 的选择，无母 mod 依据） |
| `HMC` | `chinese`，无 `unit_type` | 母 mod 无此 TAG | **保留我方** `chinese`；可选 `unit_type = acgr_g18`（学园近距射击/百鬼夜行九州铁炮，`PT` 的选择，无母 mod 依据） |
| `QNG` | `chinese`，无 `unit_type` | 母 mod 无此 TAG | **保留我方** `chinese`；**必须修首都 1816（母 mod 派给 QIN）** |

### 6.5 `MOD/history/countries` 带 `# BEGIN ACGR_UNIT_GROUPS` 的数量（Lead 问题 5）

- `MOD/history/countries`：**303 个文件中 280 个**带该注释头（另 23 个是原版 TAG 覆写，§1.4）。
- `WS` 覆盖的 42 国里，**38 个**在母 mod 中已被挂上这套兵种组（36 个 `tech_gensokyan` 国 + `NNM` + `TMY`）；未挂的 4 个正是 `AIU`/`BLS`/`HMC`/`QNG`（母 mod 无此 TAG）。
- 修正 Lead 口中的「35 国」→ 实测是 **38 国**（36 gensokyan + NNM + TMY）。

---

## 7. 不确定项

1. **无法区分「我方定制」与「旧母 mod 内容」**：`00_basic_ideas.txt`（1133 行差）、`mil.txt`（1051 行差）、`00_diplomatic_actions.txt`（142 行差）、`kirara_privileges.txt`（38 行差）这四类文件中，`WS` 的内容是「旧母 mod 快照 + 我方改动」的混合物，而旧母 mod 版本不可得（Steam 创意工坊只保留最新版）。因此只能给出「整文件级别的取舍建议」，无法逐行判定哪一行是我方设计意图。**若要精确合并，需要 YG 提供旧版母 mod 副本或其 workshop 历史版本。**
2. **`PT` 的 `AIU`/`BLS`/`HMC` 三个 `acgr` 分配（g09/g01/g18）来源不明**：母 mod 没有任何依据（无此 3 TAG），也未见 `PT` 的其它文件解释这些选择的理由。可能是合作伙伴按兵种组名称（妖怪/学院/学园铁炮）人工挑的，也可能是脚本随机。**无法确认是否有意为之。**
3. **`PT/history/provinces/957 - Delaware.txt`、`2554 - Nanticoke.txt` 的用途不明**：原版有、母 mod 与我方都没有，`PT` 版本被裁剪到 19/16 行（原版 66/41 行）。裁剪掉了哪些字段未逐行核对（属省份调查员职责）。**来源与目的待确认。**
4. **`decisions/dome_decisions.txt` 的内容性质未评估**：`PT` 新增未跟踪文件，未做内容审阅（不在本次 16 个指定文件清单内）。**需 YG 或后续调查员定性。**
5. **`interface/assets/zz_acggfx_units.gfx` 的模型资源缺失是否为母 mod 的已知问题**：`MOD`/`PT`/`WS` 三方的 `gfx/models/Units/acggfx*` 均为 0 个文件，但全库有 10 处引用 `acggfx_generic_01_type1/type2`。无法判断是母 mod 打包遗漏还是该 gfx 已废弃。**建议实际启动游戏看 error.log 是否报 missing mesh。**
6. **`WS` 自身的 `2046 - Nasirabad.txt` 与 `2046 - Nasirabad.txt.txt` 双份共存**（§3.6）是既有问题，未逐行确认两份内容是否一致，也未确认游戏实际加载哪一份。
7. **`missions/ACGR_missions.txt` 的「整文件注释」是不是我方既定设计**：`WS` 838 行全注释、0 有效行，`git log` 显示该文件仅有 1 个提交（`80ef332`）。从形态看极可能是刻意停用，但**没有 commit message 佐证**。整合前需 YG 一句话确认，因为它决定了 §4 #15 的处置方向。
8. **`PT` 那 39 个 `M` 国家文件里有 3 个（`TMY - Tomoyo Daidouji.txt`、`NNM - Nanami Yachiyo.txt`、`QNG - Qing.txt`）在 `git status` 里显示 `M` 但 `git diff` 无内容差异**（推测仅行尾 CRLF/BOM 变动），未进一步验证字节级差异。
9. **`technology_group` 与 `unit_type` 的并存结论是基于 wiki 1.23 时代文档 + 原版 1.37.5 实例推断**，未做游戏内实测（例如「`technology_group = tech_gensokyan` + `unit_type = acgr_g01` 时，兵种列表是否完全按 `acgr_g01` 走、科技惩罚是否完全按 `tech_gensokyan` 走」）。**若要上方案 B，建议先用一个测试国实际跑一局验证。**
