# 02 兵种组层调查报告

调查范围：`common/units`、`common/technology.txt`、`common/technologies/mil.txt`、`common/countries`、`common/scripted_effects/ACGR_unit_group_effects.txt`、相关 localisation。
基线数据（`00_baseline.md` 第 3/4/8 条）已核实，不重复。

---

## 1. 三方 units 目录全貌（表格）

### 1.1 目录级统计

| 源 | 路径 | `.txt` 文件数 | `unit_type` 取值集合 | 说明 |
|---|---|---|---|---|
| `WS` | `mod\ACG_MEC_E\common\units` | **72** | `tech_gensokyan` × 72（100%） | 单一兵种组，全为我方幻想乡兵种 |
| `PT` | `Downloads\ACG_MEC_E\ACG_MEC_E\common\units` | **72** | `acgr_g01` × 72（100%） | 文件名与数值与 `WS` 完全一致，仅 `unit_type` 一行被改 |
| `MOD` | `workshop\...\2796854877\common\units` | **1519** | 19 个组名 + 空值 | 36 个 `acgr_gXX` + 原版组重定义 + 无 `unit_type` 的通用炮兵/海军 |

统计命令：`Get-ChildItem -File -Filter *.txt` 计数；`unit_type` 用 `(?m)^\s*unit_type\s*=\s*(\S+)` 逐文件扫描后 `Group-Object`。

### 1.2 `MOD` 1519 个文件按 `unit_type` 分解（精确到个位，合计 1519）

| `unit_type` | 文件数 | 性质 |
|---|---|---|
| `acgr_g01`…`acgr_g36`（36 组） | **974** | 母 mod 新兵种组，命名 `acgr_gXX_<type>_<level>.txt` |
| `muslim` | 245 | 原版组被重写（内含大量角色专属兵种，如 `alice_unit.txt`、`anko_cavalry.txt`） |
| `western` | 51 | 原版组被重写 |
| `acg_american` | 14 | 母 mod 旧自定义组 |
| `eastern` | 3、`chinese` 2、`ottoman` 2 | 零星重写 |
| **（空，无 `unit_type` 字段）** | **228** | 其中 `type = artillery` **57** 个 + 海军类（light_ship/heavy_ship/galley）等 |

`acgr_*` 族的前缀细分（`Get-ChildItem` 按前两段分组）：
`acgr_g12` 49、`acgr_g09` 46、`acgr_g18` 41、`acgr_g36` 38、`acgr_g23` 36、`acgr_g07` 35、`acgr_g07s` 21、`acgr_k01`…`acgr_k07` 共 16–18×7、`acgr_g13` 34、`acgr_g01` 32 …
`acgr_g07s_*` 与 `acgr_k01..k07_*` 的 `unit_type` 全部是 `acgr_g07`（实测 `acgr_k01_cavalry_03.txt:3` → `unit_type = acgr_g07`），属于 g07 的**子模型分支**，不是独立组。

### 1.3 每组规模与等级集合（代表）

| 组 | 单位数 | 等级集合 | type 分布 |
|---|---|---|---|
| `acgr_g01` | 32 | 3,5,9,10,12,14,15,18,19,23,26,28,30 | cavalry 10 / infantry 22 |
| `acgr_g02` | 18 | 3,5,9,10,12,14,15,18,19,23,26,28,30 | cavalry 8 / infantry 10 |
| `acgr_g07` | 173 | 3,5,6,9,10,11,12,14,15,17,18,19,22,23,26,28,30 | cavalry 78 / infantry 95 |
| `acgr_g09` | 46 | 3,5,9,10,12,14,15,18,19,23,26,28,30 | cavalry 17 / infantry 29 |
| `acgr_g18` | 41 | 同上 | cavalry 10 / infantry 31 |
| `acgr_g28` | 17 | 3,5,6,9,10,12,14,15,17,19,23,26,28,30 | cavalry 8 / infantry 9 |
| `acgr_g31` / `acgr_g32` | 18 / 18 | 3,5,9,10,12,14,15,18,19,23,26,28,30 | cavalry 8 / infantry 10 |
| `acgr_g36` | 38 | 同 g01 | cavalry 8 / infantry 30 |

**关键结构事实：36 个 `acgr` 组的 `type` 只有 `infantry` 与 `cavalry`，`artillery` = 0 个**（`$mod | ? type -eq 'artillery'` 计数 = 0）。母 mod 的炮兵体系是 57 个**不带 `unit_type`** 的通用炮兵（`KYG_artillery_8`、`Elzia_Phantasma_ut_29`、`DXD_Juggernaut_Annihilation_Battery` 等），`offensive_fire` 范围 1–6、`defensive_fire` 0–6，对所有科技组/所有 `unit_type` 通用。

### 1.4 `WS` 的 72 个文件结构

| type | 文件数 | 等级（`t` 后数字 = 解锁科技级） | 每级变体数 |
|---|---|---|---|
| infantry | **28** | t1, t5, t9, t12, t15, t19, t26 | 4（`_01`…`_04`） |
| cavalry | **17** | t1, t6, t10, t14, t17, t23, t28 | 2–3 |
| artillery | **27** | t7, t8, t10, t12, t13, t14, t15, t16, t18, t20, t22, t25, t26, t29 | 1–3（含 `_KSN` 河童专属） |

`_KSN` 后缀共 10 个（`artillery_gen_t8/t10/t12/t14/t15/t18/t20/t22/t26_KSN` 等），是河童（Kawashiro Nitori）专属炮兵分支，与 `gen_t*` 同组、同 `unit_type`。

---

## 2. 同名文件冲突矩阵（WS∩MOD / WS∩PT / PT∩MOD）

方法：`Get-ChildItem -File | % Basename` 取三个 Basename 数组做 `-contains` 交集。

| 交集 | 同名文件数 | 结论 |
|---|---|---|
| `WS ∩ MOD` | **0** | 我方兵种与母 mod 兵种**零同名**，不存在"submod 覆盖母 mod"的 units 文件级覆盖 |
| `WS ∩ PT` | **72（全部）** | 伙伴版每个我方 units 文件都被改写（同文件名、改内容） |
| `PT ∩ MOD` | **0** | 伙伴版没有引入任何母 mod 的 units 文件 |
| `WS` 独有（不在 MOD） | 72 | — |
| `PT` 独有（不在 MOD） | 72 | — |

`WS` vs `PT` 逐文件 SHA256 比对：**72/72 全部 DIFF**。

**结论（对整合计划的直接影响）**：units **文件层没有覆盖冲突**。真正的冲突不在文件名，而在两个**整文件级同名资源**上：

| 文件 | WS | MOD | 是否存在覆盖 |
|---|---|---|---|
| `common/technology.txt` | 20 组（含 `tech_gensokyan`） | 55 组（含 36 `acgr_gXX`） | **是，整文件覆盖** |
| `common/technologies/mil.txt` | 883 条 `enable`（含 71 条我方兵种） | 1791 条 `enable`（含 972 条 `acgr`） | **是，整文件覆盖** |

`enable` 集合差异（精确）：
- `MOD` 有、`WS` 无 = **981** 条（其中 `acgr` 972 条）
- `WS` 有、`MOD` 无 = **73** 条（72 个 `gen_t*` 兵种 + 1 条其他）
- `WS` 的 `mil.txt` 中 `acgr` 命中 = **0**

---

## 3. 我方幻想乡兵种清单与数值区间

`common/units/*.txt` 全部 `unit_type = tech_gensokyan`（`infantry_gen_t1_01.txt:4` 等），字段集合固定为：
`type`、`unit_type`、`maneuver`、`offensive_fire`、`defensive_fire`、`offensive_shock`、`defensive_shock`、`offensive_morale`、`defensive_morale`（无其他字段，无顶层单位键——与原版 `common/units/aboriginal_ambusher.txt` 同格式）。

### 3.1 逐级数值区间（min–max，同 type 同 level 的 2–4 个变体）

口径：`of/df/os/ds` = offensive/defensive fire、shock；`om/dm` = offensive/defensive morale；`man` = maneuver。

| type | 等级 | n | of | df | os | ds | om | dm | man |
|---|---|---|---|---|---|---|---|---|---|
| infantry | t1 | 4 | 0–1 | 0–0 | 0–1 | 0–0 | 0–1 | 0–1 | 1 |
| infantry | t5 | 4 | 0–1 | 0–1 | 0–2 | 0–1 | 0–2 | 0–1 | 1 |
| infantry | t9 | 4 | 0–1 | 0–2 | 1–3 | 0–2 | 1–2 | 0–2 | 1 |
| infantry | t12 | 4 | 1–3 | 2–3 | 1–3 | 1–2 | 1–2 | 0–2 | 1 |
| infantry | t15 | 4 | 1–4 | 3–4 | 1–3 | 1–3 | 2–2 | 1–3 | 1 |
| infantry | t19 | 4 | 1–5 | 1–5 | 2–6 | 1–5 | 2–4 | 2–3 | 1 |
| infantry | **t26** | 4 | **5–6** | **4–6** | **5–6** | **4–5** | 3–5 | 3–4 | 1 |
| cavalry | t1 | 3 | 0 | 0 | 0–1 | 0–1 | 1 | 0–1 | 1–2 |
| cavalry | t6 | 3 | 0 | 0 | 2 | 0–2 | 1–2 | 1–2 | 2 |
| cavalry | t10 | 3 | 0 | 0 | 3–4 | 2 | 2–3 | 1–2 | 2 |
| cavalry | t14 | 2 | 1–3 | 0–1 | 3 | 2 | 2–3 | 1–3 | 2 |
| cavalry | t17 | 2 | 1–3 | 1–3 | 3–4 | 3–4 | 2–3 | 2–3 | 2 |
| cavalry | t23 | 2 | 1–4 | 2 | 4–5 | 3–5 | 4 | 3 | 2 |
| cavalry | **t28** | 2 | 3–4 | 3–5 | **5** | **5** | 2–3 | 4 | 2 |
| artillery | t7 | 2 | 0 | 1 | 0 | 0–1 | 1 | 0–1 | 2 |
| artillery | t10 | 3 | 2 | 1–3 | 0 | 0–2 | 0–1 | 0–2 | 2 |
| artillery | t12 | 1 | 2 | 3 | 0 | 0 | 1 | 3 | 2 |
| artillery | t14 | 1 | 2 | 3 | 0 | 1 | 2 | 3 | 2 |
| artillery | t15 | 1 | 2 | 3 | 0 | 2 | 2 | 3 | 2 |
| artillery | t16 | 2 | 2 | 2–3 | 0 | 1–2 | 2 | 1–2 | 2 |
| artillery | t18 | 3 | 3 | 2–4 | 1 | 1–2 | 2 | 1–3 | 2 |
| artillery | t20 | 3 | 3 | 2–4 | 1 | 1–2 | 3 | 1–3 | 2 |
| artillery | t22 | 3 | 4 | 3–4 | 1 | 1–2 | 3–4 | 2–3 | 2 |
| artillery | t25 | 2 | 4 | 3–4 | 1 | 1–2 | 3 | 2–3 | 2 |
| artillery | t26 | 1 | 5 | 5 | 1 | 1 | 3 | 4 | 2 |
| artillery | **t29** | 2 | **5** | 4–5 | 2 | 2–3 | 4 | 2–3 | 2 |

设计倾向（读数）：步兵 = fire/shock 双高但 maneuver 恒 1（正面肉搏型）；骑兵 = shock 主导、fire 迟至 t14 才出现；炮兵 = 早期几乎无 fire，t18 后 fire 才追上，`_KSN` 分支统一比同级 `_01/_02` 高 1 点防御。

### 3.2 72 个兵种完整清单（中文名来自 `decode_localisation/touhou_tech_and_units_l_english.yml`）

**步兵（28）**

| 文件 | 中文名 | 定位向量（of/df/os/ds/om/dm） |
|---|---|---|
| infantry_gen_t1_01 | 鸦 | 0/0/0/0/1/1 |
| infantry_gen_t1_02 | 怨灵 | 0/0/1/0/1/0 |
| infantry_gen_t1_03 | 妖精 | 1/0/0/0/0/1 |
| infantry_gen_t1_04 | 简易人偶 | 1/0/0/0/1/0 |
| infantry_gen_t5_01 | 花田妖精 | 1/1/0/1/0/1 |
| infantry_gen_t5_02 | 幽灵 | 1/0/0/0/2/1 |
| infantry_gen_t5_03 | 僵尸 | 0/0/2/1/1/0 |
| infantry_gen_t5_04 | 先进人偶 | 1/0/1/0/1/1 |
| infantry_gen_t9_01 | 人偶军团 | 1/1/1/1/1/1 |
| infantry_gen_t9_02 | 妖魔 | 0/0/1/1/2/2 |
| infantry_gen_t9_03 | 浪人武士 | 0/0/3/2/1/0 |
| infantry_gen_t9_04 | 魔界妖精 | 0/2/1/0/1/2 |
| infantry_gen_t12_01 | 河童侦察部队 | 3/2/1/1/2/2 |
| infantry_gen_t12_02 | 半灵 | 1/2/3/2/1/2 |
| infantry_gen_t12_03 | 先进人偶军团 | 2/2/2/2/2/1 |
| infantry_gen_t12_04 | 「琪露利亚」妖精 | 3/3/2/1/2/0 |
| infantry_gen_t15_01 | 河童步兵 | 4/3/1/1/2/3 |
| infantry_gen_t15_02 | 埴轮军士 | 1/3/3/3/2/2 |
| infantry_gen_t15_03 | 武装巫女 | 3/3/2/2/2/2 |
| infantry_gen_t15_04 | 老道妖精 | 4/4/2/1/2/1 |
| infantry_gen_t19_01 | 白狼天狗 | 3/3/3/3/3/3 |
| infantry_gen_t19_02 | 阎魔学徒 | 1/1/6/5/3/2 |
| infantry_gen_t19_03 | 年轻魔法使 | 5/5/2/1/2/3 |
| infantry_gen_t19_04 | 受训妖精 | 4/2/3/2/4/3 |
| infantry_gen_t26_01 | 鬼族武士 | 6/6/5/4/3/3 |
| infantry_gen_t26_02 | 贫穷神社巫女 | 5/5/5/5/4/3 |
| infantry_gen_t26_03 | 上海人偶部队 | 5/4/5/4/5/4 |
| infantry_gen_t26_04 | 狂气妖精 | 6/4/6/4/3/4 |

**骑兵（17）**

| 文件 | 中文名 | 定位向量 |
|---|---|---|
| cavalry_gen_t1_01 | 人类骑兵部队 | 0/0/0/1/1/1 |
| cavalry_gen_t1_02 | 送迎犬 | 0/0/1/0/1/1 |
| cavalry_gen_t1_03 | 活动扫帚 | 0/0/1/1/1/0 |
| cavalry_gen_t6_01 | 幽灵骑手 | 0/0/2/0/2/2 |
| cavalry_gen_t6_02 | 大鹫 | 0/0/2/1/2/1 |
| cavalry_gen_t6_03 | 年轻魔法使 | 0/0/2/2/1/1 |
| cavalry_gen_t10_01 | 雷兽 | 0/0/3/2/2/2 |
| cavalry_gen_t10_02 | 天狗新兵 | 0/0/3/2/3/1 |
| cavalry_gen_t10_03 | 老练魔法使 | 0/0/4/2/2/1 |
| cavalry_gen_t14_01 | 轮入道 | 1/0/3/2/3/3 |
| cavalry_gen_t14_02 | 骑乘配置人偶 | 3/1/3/2/2/1 |
| cavalry_gen_t17_01 | 半妖侧卫 | 1/1/4/4/3/3 |
| cavalry_gen_t17_02 | 先进骑乘配置人偶 | 3/3/3/3/2/2 |
| cavalry_gen_t23_01 | 天人云骑手 | 1/2/5/5/4/3 |
| cavalry_gen_t23_02 | 机甲人偶 | 4/2/4/3/4/3 |
| cavalry_gen_t28_01 | 飞空魔女集会 | 3/5/5/5/2/4 |
| cavalry_gen_t28_02 | 鸦天狗狗仔记者 | 4/3/5/5/3/4 |

**炮兵（27）**

| 文件 | 中文名 | 定位向量 |
|---|---|---|
| artillery_gen_t7_01 | 河童火炮 | 0/1/0/0/1/1 |
| artillery_gen_t7_02 | 鸦天狗投石 | 0/1/0/1/1/0 |
| artillery_gen_t8_KSN | 河童工坊特制炮 | 0/2/0/0/1/2 |
| artillery_gen_t10_01 | 妖怪炮台 | 2/2/0/1/0/1 |
| artillery_gen_t10_02 | 鬼族掷岩 | 2/1/0/2/0/0 |
| artillery_gen_t10_KSN | 河童试作炮 | 2/3/0/0/1/2 |
| artillery_gen_t12_KSN | 河童量产炮 | 2/3/0/0/1/3 |
| artillery_gen_t13_01 | 魔导炮 | 2/2/0/1/1/2 |
| artillery_gen_t13_02 | 人偶自爆兵 | 2/2/0/2/1/1 |
| artillery_gen_t14_KSN | 河童机动炮 | 2/3/0/1/2/3 |
| artillery_gen_t15_KSN | 河童精密火炮 | 2/3/0/2/2/3 |
| artillery_gen_t16_01 | 天狗风炮 | 2/3/0/1/2/2 |
| artillery_gen_t16_02 | 河童水雷炮 | 2/2/0/2/2/1 |
| artillery_gen_t18_01 | 鬼族重炮 | 3/3/1/1/2/2 |
| artillery_gen_t18_02 | 月兔火箭筒 | 3/2/1/2/2/1 |
| artillery_gen_t18_KSN | 河童光学瞄准炮 | 3/4/1/1/2/3 |
| artillery_gen_t20_01 | 月都加农 | 3/3/1/1/3/2 |
| artillery_gen_t20_02 | 地狱炎炮 | 3/2/1/2/3/1 |
| artillery_gen_t20_KSN | 河童超电磁炮 | 3/4/1/1/3/3 |
| artillery_gen_t22_01 | 地狱业火炮 | 4/3/1/1/3/3 |
| artillery_gen_t22_02 | 天界制裁炮 | 4/3/1/2/3/2 |
| artillery_gen_t22_KSN | 河童电浆炮 | 4/4/1/1/4/3 |
| artillery_gen_t25_01 | 天界雷炮 | 4/4/1/1/3/3 |
| artillery_gen_t25_02 | 隙间传送炮 | 4/3/1/2/3/2 |
| artillery_gen_t26_KSN | 河童究极科学炮 | 5/5/1/1/3/4 |
| artillery_gen_t29_01 | 八云机关炮 | 5/5/2/2/4/3 |
| artillery_gen_t29_02 | 究极魔炮 | 5/4/2/3/4/2 |

### 3.3 与母 mod `acgr` 同 type 同 level 对比（取该级"最高档"代表值，`of/df/os/ds/om/dm`）

**步兵**

| 等级 | WS（区间） | acgr_g01 | acgr_g02 | acgr_g32 | acgr_g36 | 参照 acgr_g07 |
|---|---|---|---|---|---|---|
| L12 | 1–3/2–3/1–3/1–2/1–2/0–2 | 1/3/1/2/2/2 | 3/3/0/1/2/2 | 4/0/2/1/3/1 | 1/2/3/2/3/4 | 5/3/3/4/4/4 |
| L19 | 1–5/1–5/2–6/1–5/2–4/2–3 | 2/4/1/3/3/3 | 4/4/1/1/3/3 | 6/0/2/3/4/1 | 2/3/4/3/4/5 | 7/5/4/5/5/4 |
| L26 | 5–6/4–6/5–6/4–5/3–5/3–4 | 3/6/1/3/4/5 | 5/6/1/2/4/4 | 7/1/3/3/5/3 | 3/4/5/4/6/7 | 7/7/5/6/6/6 |

**骑兵**

| 等级 | WS（区间） | acgr_g01 | acgr_g02 | acgr_g32 | acgr_g36 | 参照 acgr_g07 |
|---|---|---|---|---|---|---|
| L14 | 1–3/0–1/3/2/2–3/1–3 | 1/0/3/2/2/3 | 2/2/1/2/2/2 | 2/0/3/1/4/1 | 1/1/3/2/2/2 | 2/3/5/4/4/4 |
| L23 | 1–4/2/4–5/3–5/4/3 | 1/2/6/3/4/4 | 3/4/2/3/4/4 | 2/1/4/3/7/3 | 2/2/4/4/4/4 | 2/4/8/7/5/7 |
| L28 | 3–4/3–5/5/5/2–3/4 | 1/3/6/4/4/5 | 4/5/3/3/4/4 | 3/1/5/3/7/4 | 2/3/4/5/4/5 | 3/4/8/7/6/7 |

**读数结论**
1. **我方步兵的冲击段偏强**：L26 的 `os 5–6 / ds 4–5` 只有 `acgr_g07`（5/6）与 `acgr_g28`（6/3）能对位，`g36`（5/4）勉强持平，`g01/g02` 只有 1–2。
2. **我方骑兵整体弱于母 mod 核心组**：L28 `os 5 / ds 5` 对 `g07` 的 `8/7`、`g01` 的 `6/4`、`g32` 的 `5/3`——除 `g02`（3/3）外全被压制。
3. **我方炮兵无可比对象**：36 个 `acgr` 组 `artillery` = 0，只能与母 mod 57 个通用炮兵（`of` 1–6）横向比；我方 t29 的 `5/4–5` 处于通用炮兵中上段（最高 `Elzia_Phantasma_ut_29` 6/6）。
4. 我方数值曲线是"每级 2–4 个变体、按定位分化"，母 mod 是"每级 1 个、按组分化"。两者**设计粒度不同**：并组会把我方的"变体选择"压缩成母 mod 的"单线升级"。

---

## 4. 合作伙伴 units 改动性质判定

### 4.1 命令与结果

```
git -C "C:\Users\HP\Downloads\ACG_MEC_E\ACG_MEC_E" diff --stat -- common/units
→ 72 files changed, 72 insertions(+), 72 deletions(-)
git status --porcelain -- common/units
→ M × 72（无新增、无删除）
```

72 个文件、**每个文件恰好 1 增 1 删**——这是"单行替换"的指纹。

### 4.2 抽样 5 个文件的 diff（全部同一形态）

```
===== infantry_gen_t1_01 =====
-unit_type = tech_gensokyan
+unit_type = acgr_g01
===== artillery_gen_t7_01 =====
-unit_type = tech_gensokyan
+unit_type = acgr_g01
===== cavalry_gen_t6_01 =====
-unit_type = tech_gensokyan
+unit_type = acgr_g01
===== infantry_gen_t26_04 =====
-unit_type = tech_gensokyan
+unit_type = acgr_g01
===== artillery_gen_t12_KSN =====
-unit_type = tech_gensokyan
+unit_type = acgr_g01
```

72 个文件的 `unit_type` **全部**为 `acgr_g01`（100%），无一按题材分流到 g02/g31/g32/g36。

### 4.3 配套改动（这一步决定了改动的真正含义）

| 文件 | PT 的改动 | 证据 |
|---|---|---|
| `common/units/*.txt` × 72 | `unit_type: tech_gensokyan → acgr_g01` | 上面的 diff |
| `history/countries` 39 个我方国 | `technology_group` 改为 `acgr_gXX`，并**新增** `unit_type = acgr_gXX` 行 | `git diff "history/countries/AIU - Aiur.txt"`：`-technology_group = sub_saharan` / `+technology_group = acgr_g09` / `+unit_type = acgr_g09` |
| 39 国的组分配 | `acgr_g01` 32 国、`acgr_g02` 5 国（EIR/RES/KGY/WNT/WNY）、`acgr_g09` 1（AIU）、`acgr_g18` 1（HMC） | 逐文件扫描 `^\s*technology_group\s*=` |
| 245 个未跟踪国家文件（母 mod 新国） | 把 `unit_type=acgr_gXX` 与 `technology_group` **同步**（MOD 原本是 `technology_group = western/muslim/chinese`） | MOD 端 `acgr_g07|muslim` 40、`acgr_g09|western` 39；PT 端 `acgr_g07|acgr_g07` 40、`acgr_g09|acgr_g09` 40 |
| `common/technology.txt` | 换成母 mod 的 55 组，**丢弃 `tech_gensokyan`**（`git diff --stat`：179 增 14 删；`tech_gensokyan` 命中 = 0） | 同基线第 3 条 |
| `common/technologies/mil.txt` | 合并：1865 条 `enable`（含 `acgr` 1006 条 + `gen_t` 72 条），`git diff --stat` = 1065 增 16 删 | 计数命令 |

### 4.4 结论

**"合作伙伴是否把幻想乡兵种整体替换成母 mod 的 acgr 兵种？" → 不是。**

- 伙伴版**没有引入任何母 mod 的 units 文件**（`PT ∩ MOD = 0`），72 个我方兵种的**文件名、中文名、全部 9 项数值一字未改**（数值对比：72/72 文件仅 `unit_type` 一行不同）。
- 他做的是：**把幻想乡 72 个兵种整体"挂靠"到 `acgr_g01` 名下**，同时删掉 `tech_gensokyan` 组、把 39 个我方国家的科技组/兵种组改写成 `acgr_gXX`。
- 性质判定 = **「改成 acgr 命名」+「删掉 tech_gensokyan 组」**，不是「数值重平衡」，也不是「直接覆盖成母 mod 版本」。
- 副作用一（语义丢失）：幻想乡兵种失去了"独立兵种组"这一身份；`localisation` 里的 `tech_gensokyan: "幻想乡"` 成为孤儿条目。
- 副作用二（覆盖不全）：7 个国家被分流到 `g02`/`g09`/`g18`，而 72 个兵种全在 `g01` → **EIR / RES / KGY / WNT / WNY / AIU / HMC 七国看不到任何幻想乡兵种**，用的是母 mod 该组原生模型。
- 副作用三（编号语义错位）：27 个炮兵也全挂 `acgr_g01`，而母 mod 的 `acgr` 组本身不设炮兵（靠通用炮兵）→ g01 会同时拥有"母 mod 32 个步骑 + 我方 72 个单位（含 27 门炮）"的超大兵种池。

---

## 5. `unit_type` 与科技组的绑定机制（证据）

### 5.1 五条独立链路（缺一条对应功能就废）

| 链路 | 文件 | 证据行 |
|---|---|---|
| ① 兵种定义：**文件名即兵种键**，文件内只有无键的 `type`/`unit_type`/9 项数值 | `common/units/*.txt` | 原版 `common\units\aboriginal_ambusher.txt:1-12`（`unit_type = aboriginal_tech` / `type = infantry`，无顶层键）；我方 `common\units\infantry_gen_t1_01.txt:1-12` 同构 |
| ② 科技组：决定研究成本/等级，组名是 `technology.txt` 里 `groups = { }` 的**二级键** | `common/technology.txt` | `MOD` 55 组 / `WS` 20 组（`groups`/`tables` 为一级键，故必须按嵌套深度解析，不能只 grep 行首） |
| ③ 国家兵种组（**与科技组是两个轴**）：`unit_type` 写在 country history | `history/countries/*.txt` | 原版 `history\countries\*.txt` 大量 `unit_type = sub_saharan`；`MOD\history\countries\ABD - Albedo.txt:3-6` = `unit_type = acgr_g14` + `set_country_flag = acgr_unit_group_g14` + `technology_group = western` |
| ④ 等级解锁：`enable = <兵种键>` 必须挂在某个 `mil_tech` 等级下 | `common/technologies/mil.txt` | `MOD` 1791 条（`mil.txt:137-155` 是 `acgr_g01_infantry_03` … `acgr_g09_ctl_cavalry_03` 的 L3 解锁块）；`WS` 883 条（`mil.txt:108-114` = `cavalry_gen_t1_01…infantry_gen_t1_04` 的 L3 解锁块） |
| ⑤ 模型偏好/展示：`historical_units` 列出国家倾向使用的兵种键；`change_unit_type` effect 可运行时切换 | `common/countries/*.txt`、`common/scripted_effects/ACGR_unit_group_effects.txt` | `MOD\common\countries\Alice Margatroid.txt:21-41` = `historical_units = { acgr_g01_infantry_03 … acgr_g01_cavalry_30 }`（带 `# BEGIN/END ACGR_UNIT_GROUPS PREFERRED MODELS` 注释）；`ACGR_unit_group_effects.txt:45` `change_unit_type = acgr_g01` … 逐组一路到 g36 |

### 5.2 我方现状：只依赖 ①②③④ 的"同名对齐"

- `WS` 的 36 个幻想乡国（基线第 4 条）**全部没有 `unit_type` 行**（`history/countries` 42 个文件，`^\s*unit_type\s*=` 命中 **0**）。
- 即：这些国只有 `technology_group = tech_gensokyan`，兵种选择靠"**默认 `unit_type` = 科技组名**"隐式生效。
- 兵种侧 72 个文件全部 `unit_type = tech_gensokyan`；`mil.txt` 用 71 条 `enable = *_gen_t*` 按等级解锁（对齐良好）。

### 5.3 `MOD` 是否有 36 组之外的旧名残留

| 检查项 | 结果 |
|---|---|
| `MOD` 全库出现 `gensokyan` 的文件数（`*.txt`+`*.yml` 递归） | **0** |
| `MOD` units 的 `unit_type` 是否全部落在 55 组内 | **是**（19 个组名 + 空值，无一个野字符串） |
| 旧名 `gen` / `gensokyan` / `tech_gensokyan` 的 `unit_type` | **不存在** |

→ 母 mod **完全没保留**幻想乡旧组，也没有"组名改名遗留"。所以 `WS` 与 `MOD` 在这条链上是**两套互不相交的命名空间**，只能靠"再挂一次"合并。

### 5.4 若 `tech_gensokyan` 组消失会发生什么（按链路逐条推演）

| 链路 | 后果 | 严重度 |
|---|---|---|
| ② `technology.txt` 没有该组 | 36 国 `technology_group = tech_gensokyan` 指向不存在的组 | 高（科技面板/研究成本异常或报错日志） |
| ③/① 国 `<->` 兵种对不上 | 72 个 `unit_type = tech_gensokyan` 的兵种没有任何国家能匹配到（除非显式 `unit_type` 或 `change_unit_type`）→ 兵种**不可见、不可选** | 高 |
| ④ `mil.txt` 的 71 条 `enable = *_gen_t*` | `enable` 指向仍存在的兵种键，但兵种本身不可用 → 空解锁，无报错但无意义 | 中 |
| ⑤ `historical_units` | 我方没有 `common/countries` 文件，无影响 | 低 |
| `discovered_by = tech_gensokyan`（1870 省，基线第 9 条） | 引用不存在的科技组 → 视野判定失效 | 高（属省份层，归 01/03 号报告） |

**PT 的实际处置**：直接把 ③ 的 `technology_group` 改成存在的 `acgr_gXX`，绕过 ② 的缺失——所以他的组合是自洽的（`technology_group` 与 `unit_type` 都指向同一个已存在的 `acgr` 组）。

### 5.5 一个尚未证明的点（如实记入第 8 节）

引擎是否**硬校验**"`unit_type` 字面量必须是 `technology.txt` 的组名"，无法只靠文件层证明：母 mod 把两条链都写成同名，无法区分哪条是必要条件。可确认的是：**两条链同时成立时才安全**，因此整合方案必须两条都补。

---

## 6. 母 mod `acgr` 兵种组 vs 我方兵种 对照表

母 mod 的组名本地化文件 `MOD\localisation\ACGR_unit_groups_l_english.yml` 中文已**字节级损毁**（UTF-8 BOM 后出现 `0x11 0xE2 0x80 0xB0`，任何代码页解不回），故下表定位依据是各组的**兵种注释**（`common/units/acgr_gXX_*.txt` 第 1 行 `# 中文名 | source draft ...`，UTF-8 可读）与 `history/countries` 的国别归属。

| 组 | 题材（注释实证） | 我方等价兵种 | 等价度 |
|---|---|---|---|
| **g01** 妖怪突击队 | 妖怪斥候、天狗游击队、天狗屏护游骑、改良妖怪突击队、结界巡猎队、幻想乡机动禁卫、天狗机动近卫 | `cavalry_gen_t10_02` 天狗新兵、`cavalry_gen_t28_02` 鸦天狗狗仔记者、`infantry_gen_t19_01` 白狼天狗、`cavalry_gen_t1_02` 送迎犬、`infantry_gen_t26_01` 鬼族武士 | **高**（同宗妖怪/天狗体系，4–5 单位题材直接对位；PT 把 32 国划到此组在题材上说得通） |
| **g02** 月兔 | 月兔列装射手、月兔侦察骑、月面屏护龙骑、月都全域机动卫队、月面精密战列 | 仅炮兵 `artillery_gen_t18_02` 月兔火箭筒、`artillery_gen_t20_01` 月都加农 | **低**（我方没有月兔步/骑线；月都题材只在炮兵里出现） |
| **g07** 遗库/联邦 | 联邦遗骑护卫、离网护送骑队、商路遗械突骑、遗库盾卫、地方供能骑卫 | **无** | **无**（我方无"遗库/联邦/商路"设定） |
| **g09** 学院/结界 | 学院枪盾侍从、学院结界步兵、学院骑卫、魔法侍从骑、术式龙骑、使魔护卫骑 | `infantry_gen_t19_03` 年轻魔法使、`infantry_gen_t15_03` 武装巫女、`cavalry_gen_t10_03` 老练魔法使、`cavalry_gen_t17_02` 先进骑乘人偶 | **中**（魔法/结界/使魔题材重叠，但"学院"建制我方没有） |
| **g18** 学园/百鬼夜行 | 学园巡逻队、阿拜多斯三角洲机动队、联合战术机动群、学园近距射击队、百鬼夜行九州铁炮队 | **无**（仅"百鬼夜行"呼应 `infantry_gen_t9_02` 妖魔） | **低/无**（机动车辆/学园建制是另一套世界观） |
| **g28** 妖族 | 妖族战兵、四魂突击兵、妖族混成军、鬼猎骑队、妖星铁骑、四魂龙骑 | `infantry_gen_t26_01` 鬼族武士、`infantry_gen_t19_02` 阎魔学徒、`infantry_gen_t9_02` 妖魔 | **中**（妖/鬼题材对位，但母 mod 走"妖族军团"建制，我方走"妖怪个体单位"） |
| **g31** 人偶/童话 | 人偶守备、童话巨兽骑群、秘仪重装使魔军、龙牙护卫、童话使魔战列 | `infantry_gen_t1_04` 简易人偶、`t5_04` 先进人偶、`t9_01`/`t12_03` 人偶军团、`t26_03` 上海人偶部队、`cavalry_gen_t14_02`/`t17_02` 骑乘人偶、`t23_02` 机甲人偶、`artillery_gen_t13_02` 人偶自爆兵 | **高**（爱丽丝/人偶 9 单位全面对位，母 mod 的 g31 = 童话使魔线，题材吻合） |
| **g32** 红魔馆术士 | 红魔见习术士、红魔初阶术士、红魔咏唱射手、爆裂术式护卫、红魔震慑龙骑 | **无专属线**（只有 `artillery_gen_t13_01` 魔导炮、`artillery_gen_t22_02` 天界制裁炮 擦边） | **低**（我方红魔馆没有独立兵种线） |
| **g36** 乡团自警 | 乡团自警队、乡团列装骑、乡镇火铳民兵、乡镇列阵民兵、地方常备步兵、西欧乡团近卫骑 | `infantry_gen_t1_01` 鸦、`t1_03` 妖精、`t5_01` 花田妖精（人类村落/低阶民兵位） | **中低**（母 mod 是"人类村落自卫队"，我方同级单位是"妖精/妖怪"，种族定位相反） |

### 结论：幻想乡兵种**能不能**并入母 mod 的 `acgr` 体系？

**题材上能并（9 组里 6 组有对位，g01/g31 等价度"高"），工程上必须改的是"粒度"而不是"命名"：**

1. **能并的部分**：`g01`（妖怪/天狗）与 `g31`（人偶）题材几乎一一对应，`g09`/`g28` 部分对应。母 mod 已经按幻想乡派系把题材**拆细**（g01 妖怪、g02 月都、g28 妖族、g31 人偶、g32 红魔、g36 人类村落），这套拆分比"单一 `tech_gensokyan` 组"更贴合世界观。
2. **不能无损并的部分**：
   - **炮兵线 27 个单位无处安放**——`acgr` 组体系里 `artillery` = 0，母 mod 用 57 个无 `unit_type` 的通用炮兵。并入后我方炮兵只能作为某个组的"专属炮兵"（PT 的做法）或改成通用炮兵。
   - **"每级 4 变体"的结构会退化**——母 mod 每组每级 1 个兵种，我方每级 2–4 个。并组后 72 个单位会成为某个组的"超额兵种池"，而不是清晰的升级链。
   - **一个国家的 `unit_type` 是单选**——36 国若改 `acgr_gXX`，就看不到 `tech_gensokyan` 的兵种；要两者都看见，只能把 72 个兵种的 `unit_type` 也改成对应 `acgr_gXX`（= 深度整合），或保留 `tech_gensokyan` 组并让 36 国继续用它（= 平行共存，母 mod 模型对这 36 国不可见）。

---

## 7. 风险与推荐

### 7.1 若直接采用 `PT` 的 units 覆盖

| 风险 | 量化 | 说明 |
|---|---|---|
| 兵种数值/名称丢失 | **0** | 72/72 文件只改 `unit_type` 一行，数值、中文名、文件名全保留 |
| 独立兵种组身份丢失 | `tech_gensokyan` 组消失 | `localisation` 的 `tech_gensokyan: "幻想乡"` 变孤儿；科技面板不再有幻想乡组 |
| 7 国兵种不可见 | **7 / 39 国** | EIR/RES/KGY/WNT/WNY（g02）、AIU（g09）、HMC（g18）看不到 72 个幻想乡兵种 |
| 炮兵语义冲突 | 27 门炮挂 g01 | g01 同时拥有母 mod 32 个单位 + 我方 72 个（含 27 炮），同级重复解锁；且母 mod 通用炮兵 57 门对该国仍可用 → 同级多达 3 门炮可选 |
| 我方"变体选择"被稀释 | 每级 4→(4+1) | 幻想乡国在 g01 里要在"我方 4 变体"与"母 mod 1 标准件"之间选，数值不连续（如 L26 我方 os 5–6 vs g01 os 1） |
| 连带层（非本层结论，仅指向） | 39 国 `technology_group` 被改写；1870 省 `discovered_by = tech_gensokyan` 成孤儿 | 归 01/03 号报告 |

**判定**：`PT` 的 units 改动**本身可采纳**（零数值损失、`mil.txt` 合并干净：1865 条 enable 含 72 条 `gen_t`）。不可直接采纳的是它**顺带**做掉的两件事：删 `tech_gensokyan` 组、把 39 国科技组改写。

### 7.2 若保留 `WS` 的 units（并沿用 `WS` 的 `technology.txt`/`mil.txt`）

| 冲突 | 量化 | 说明 |
|---|---|---|
| 母 mod 36 个 `acgr` 组消失 | 55 → 20 组 | `WS\common\technology.txt` 整文件覆盖母 mod 同名文件 |
| 母 mod 兵种解锁失效 | **981 条** `enable` 丢失（其中 `acgr` 972 条） | `WS\common\technologies\mil.txt` 883 条整文件覆盖母 mod 1791 条 |
| 母 mod 兵种成死数据 | **974 个** `acgr` 兵种文件不可达 | `unit_type = acgr_gXX` 无组、无 `enable`、`historical_units` 指向未解锁兵种 |
| 母 mod 国家无模型 | **303** 个 `history/countries`（`unit_type = acgr_gXX`） | 这些国 `technology_group` 仍是 western/muslim/chinese，`unit_type` 指向被删组 |
| units 同名覆盖 | **0** | 已验证：`WS ∩ MOD = 0`，本层不存在"覆盖掉母 mod 兵种文件" |

### 7.3 推荐路径

**推荐 A2（最小风险 / 兵种零丢失）：平行共存 + 增量合并**

1. `common/technology.txt`：以**母 mod 55 组为底**，只**追加** `tech_gensokyan` 一个组（→ 56 组），绝不整文件回退到 `WS` 版本。
2. `common/technologies/mil.txt`：以**母 mod 1791 条 `enable` 为底**，追加我方 71 条 `enable = *_gen_t*`（= 直接采纳 `PT` 的合并结果，1865 条）。
3. `common/units/*.txt`：**保持 `WS` 原样**（`unit_type = tech_gensokyan`，72 文件不动）。
4. `history/countries` 36 国：保持 `technology_group = tech_gensokyan`（不写 `unit_type`，沿用隐式默认）。
5. 结果：幻想乡 36 国用我方 72 兵种；母 mod 国家用 `acgr` 模型；两套并存，**零覆盖、零丢失**。代价：36 国看不到母 mod 的 `acgr` 模型。

**备选 A1（深度整合 / 采纳母 mod 派系拆分）：**

1. 同样做第 1、2 步（56 组 + 合并 `mil.txt`）。
2. 按第 6 节对照表把 72 个兵种的 `unit_type` **分题材改写**（而不是 PT 的一刀切 `g01`）：
   - 妖怪/天狗/鬼：`infantry_gen_t9_02`、`t19_01`、`t26_01`、`cavalry_gen_t10_02`、`t28_02` → `acgr_g01`
   - 月都/月兔：`artillery_gen_t18_02`、`t20_01` → `acgr_g02`
   - 人偶（含 `_KSN` 以外的爱丽丝线）：`t1_04`、`t5_04`、`t9_01`、`t12_03`、`t26_03`、`cavalry_gen_t14_02`、`t17_02`、`t23_02` → `acgr_g31`
   - 魔法使/术式/魔导：`infantry_gen_t19_03`、`cavalry_gen_t6_03`、`t10_03`、`artillery_gen_t13_01` → `acgr_g32`
   - 妖精/村落民兵/通用：其余步兵 + `_KSN` 炮兵 → `acgr_g36` / `acgr_g01`
3. 39 国 `technology_group` 与 `unit_type` 同步到对应组（不能只改一个）。
4. 补 `common/countries/*.txt` 的 `historical_units`（我方目前**没有** `common/countries` 文件，母 mod 有 284 个带 `historical_units`）。
5. 结果：与母 mod 体系完全同构，模型可在组内并列；代价：`tech_gensokyan` 组退役，1870 省 `discovered_by` 需同步改写。

**明确不推荐**：直接把 `PT` 的 `common/units` + `PT` 的 `common/technology.txt` 一起整体搬过来——那会让 7 国看不到幻想乡兵种，且把"删 `tech_gensokyan`"这个决定一并继承。

---

## 8. 不确定项

1. **`unit_type` 字面量是否为 `technology.txt` 组名的硬校验**：文件层无法证伪。母 mod 两条链同名（`unit_type = acgr_g14` + `technology_group = western` 虽然分离，但 36 组都写进了 `technology.txt`），我方两条链也同名；没有反例可判。→ 保守做法：两条链都补（推荐 A2 已覆盖）。
2. **`acgr` 组的中文显示名不可恢复**：`MOD\localisation\ACGR_unit_groups_l_english.yml` 中文在文件写入时已损坏（第 2 行字节 `EF BB BF` 之后出现 `0x11 E2 80 B0 5E`），GBK/GB18030/Big5/Shift-JIS/1252 全解不回。第 6 节的组题材靠 `common/units` 首行注释（UTF-8 完好）反推，个别组（g18、g28）题名可能与母 mod 原意有偏差。
3. **我方 `localisation` 存在孤儿条目**：`decode_localisation/touhou_tech_and_units_l_english.yml` 里有 `infantry_lcu_t*`（月兔系列，如「月兔列装射手」）、`cavalry_lgk_t*`（「现代化月人骑士」）与 `tech_gensokyan_lunarian`（「现代化月球」）条目，但**三方 `common/units` 目录都没有对应文件**（`_(lcu|lgk)_` 命中 = 0，WS 全库文件名命中 = 0）。可能是历史遗留或未实装的月都兵种计划；本次未追溯其来源。
4. **我方 `mil.txt` 少一条解锁**：72 个单位对应 71 条 `enable`，缺 `cavalry_gen_t10_03`（老练魔法使）→ 该兵种在游戏内**永不出现**（既有缺陷，非本次整合引入）。
5. **母 mod 57 个通用炮兵包含角色专属命名**（`KYG_artillery_8`、`DXD_Juggernaut_Annihilation_Battery`、`Elzia_Phantasma_ut_29`），却都不写 `unit_type` → 等于对所有科技组/所有国开放。这是母 mod 的有意设计还是漏写 `unit_type`，无法从文件层判定；若属漏写，母 mod 的炮兵平衡整体偏强。
6. **`PT` 的 `history/countries` 只有 287 个文件，`MOD` 有 303 个**（差 16）：可能被删/改名/未复制，归 01 号报告（历史层）核实，本层不下结论。
