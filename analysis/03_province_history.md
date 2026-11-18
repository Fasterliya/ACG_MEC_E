# 03 省份 history 层调查报告

调查人：division `province-history`　调查时间：2026-11-18
数据源（只读）：
- `WS` = `F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\history\provinces`（1904 文件）
- `PT` = `C:\Users\HP\Downloads\ACG_MEC_E\ACG_MEC_E\history\provinces`（2960 文件，工作树未提交）
- `MOD` = `F:\SteamLibrary\steamapps\workshop\content\236850\2796854877\history\provinces`（2498 文件）
- 校验参照：vanilla `F:\SteamLibrary\steamapps\common\Europa Universalis IV\history\provinces`（3923 文件）

方法：全部 1900+ 文件由 PowerShell 脚本聚合（解析后按「键值 token 多重集」比较，注释与空白差异不进差异集），未逐个 read。附件：`analysis/03_prov_id_diff.csv`（3131 行）。

---

## 1. 省份 ID 集合对比

归一化规则：取文件名前导数字 `^(\d+)`，三种命名格式并存，必须按 ID 比，不能按文件名比。
- 无空格：`1-Uppland.txt`、`6-Skane.txt`
- 单空格+短横：`10-Jamtland.txt`
- 短横+空格：`100 - Friesland.txt`（另有双空格个例：`2390 -  Chaiya.txt`、`4805 - East  Sibu.txt`）

| 集合 | 文件数 | 归一化 ID 数 | 说明 |
|---|---|---|---|
| `WS` | 1904 | **1903** | 有 1 个重复 ID：`2046 - Nasirabad.txt` 与 `2046 - Nasirabad.txt.txt`（后者双扩展名，是脏文件） |
| `MOD` | 2498 | **2498** | 全部为 `id - name` 形式；**是「母 mod 改过的省」子集，不是全量** |
| `PT` | 2960 | **2960** | ≈ vanilla 3923 的 75%，等于「母 mod 新版 + 旧版 + 我方定制」混装 |

ID 集合关系（按 ID）：

| 关系 | 数量 | 整合含义 |
|---|---|---|
| `WS` ∩ `MOD` | **1270** | 真正需要逐省三方合并的战场 |
| `MOD` 独有 | **1228** | 母 mod 改过、我方未覆盖 → 母 mod 内容**本来就自动生效**，整合不需要动 |
| `WS` 独有 | **633** | 母 mod 没改这些省，我方文件 = vanilla/旧母 mod 拷贝 + 我方增量，冲突风险低 |
| `PT` ∩ `MOD` | 2325 | PT 覆盖了 2325 个母 mod 也覆盖的省 |
| `PT` ∩ `WS` | 1896 | PT 相对 WS 多出 1057 个 WS 完全没有的省文件（`??` 未跟踪新增） |

- `WS` ID 范围 1–4845；`MOD` 1–4941；交集缺口分布均匀，不存在「整段区间没有交集」的情况。
- 633 个 `WS` 独有 ID 在 vanilla 中**全部存在**（633/633），说明它们是「旧母 mod 覆盖过、新版母 mod 放弃覆盖」的省，而不是母 mod 新省。
- `MOD` 的 1228 个独有 ID 举例：367 The Azores、480 Kulunda、482 Bahamas、565 Bhutan、661 Dali、669 Fuzhou……（完整清单见 CSV 中 `diff_class = MOD_ONLY` 行）

CSV `analysis/03_prov_id_diff.csv` 列：`prov_id, in_WS, in_MOD, diff_class`；`diff_class` 取值 `D1/D2/D3/D4/WS_ONLY/MOD_ONLY`（交集的 `D` 值为该省主分类，见第 2 节）。

---

## 2. 交集差异分类统计（D1–D5）

对 1270 个交集省逐省比较 `WS` 与 `MOD`，按下列规则打标（可重叠）：

| 类 | 判定 | 命中省数 |
|---|---|---|
| **D1** | `discovered_by` 集合差异 | **1241** |
| **D2** | 顶层 `owner`/`controller`/`add_core`/`culture`/`religion` 差异 | **49** |
| **D3** | `base_tax`/`base_production`/`base_manpower`/`trade_goods`/`center_of_trade`/`extra_cost`/建筑/`hre`/`is_city` 差异 | **17** |
| **D4** | 带日期历史条目（`1445.1.1 = { ... }` 等）差异 | **205** |
| **D5** | 归一化后完全一致（仅注释/空白差异） | **0** |
| DX | 其他顶层键差异（仅 67/70，`revolt = { }` 写法差异等） | 2 |

主分类（优先级 D2 > D4 > D3 > D1）：**D1 1017 / D4 190 / D2 49 / D3 14**。

**Lead 要的两个关键数字（交集 1270 内）**：

- **纯 discovered_by 增量（除 `discovered_by = tech_gensokyan` 外与 MOD 完全一致）＝ 1015 个**
  合并动作 = 只加一行，零裁决。
- **还有其他差异（真三方冲突，需逐省裁决）＝ 255 个**
  （其中 `MOD` 侧确有新增内容的 **253** 个；另 2 个是 366/368，`MOD` 删除了整段殖民时间线而 `WS` 保留）

### D1 代表省（1241 省，几乎全是 `WS` 多一行 `tech_gensokyan`）

- `WS\history\provinces\1-Uppland.txt:19` `discovered_by = tech_gensokyan`，MOD 同文件无此行
- `WS\history\provinces\100 - Friesland.txt:19` 同上（MOD 版本 19 行后直接是空行）
- `WS\history\provinces\4117 - Bezhetsk.txt:18` 同上

仅 2 个省出现 **`MOD` 多出的 discovered_by**：1477 Coast of Iceland、1480 Denmark Strait，母 mod 新版给它们加了 `discovered_by = acg_american`：
```
1477: WS[...western,eastern,tech_gensokyan]  MOD[...western,eastern,acg_american]
1480: WS[...western,tech_gensokyan]           MOD[...western,acg_american]
```

### D2 代表省（49 省，全部是「母 mod 新版把 tag/文化体系重组」）

类型分布（按 owner 变化方向分组）：

| 变化 | 省数 | 省 ID |
|---|---|---|
| `qng → qin` | 22 | 690,691,695,696,704,726,1816,2112,2113,2136,2137,2138,2139,2140,2141,2142,2143,2144,4194,4195,4196,4652 |
| `fra → jda` | 13 | 173,174,183,185,186,194,196,200,2753,4112,4390,4391,4695 |
| 仅文化改名 `ShiraiKuroko → supperability_magic_culture` | 5 | 99,100,1931,4381,4382 |
| `hmc → lsw` | 3 | 681,2171,2172 |
| `hmc → shj` | 2 | 680,4211 |
| `hts ↔ frr` 互换 | 3 | 67(→hts),70(→frr),4713(→frr) |
| 仅 `add_core fra→jda` | 1 | 1879 |

代表 diff：

```diff
# 680 - Chongqing.txt   WS:3 vs MOD:3
-owner = HMC
-controller = HMC
-add_core = HMC
-culture = acg_hongmao
-religion = confucianism
+owner = SHJ
+controller = SHJ
+add_core = SHJ
+add_core = MNG
+culture = Shanhaijing
+religion = acg
```

```diff
# 183 - Ile-de-France.txt
-owner = FRA            +owner = JDA
-controller = FRA       +controller = JDA
-culture = cosmopolitan_french  +culture = jeanne
```

```diff
# 99 - Gelre.txt:3
-culture = ShiraiKuroko
+culture = supperability_magic_culture
```

**重要**：D2 里没有一例是「幻想乡 36 国 owner 被母 mod 换成别人」。母 mod 自带幻想乡势力（KTY/RES/YKR/FLD/INX/KYM/SHI/HTS/FRR 全部在 `MOD/common/country_tags/ACG_country_tag.txt` 中有定义，例如 101 Genoa 在 `MOD` 里就是 `owner = KTY`、`culture = Sanae`、`religion = Gensokyo_reg`）。**幻想乡国家不是 WS 的私有定制，是母 mod 自带，我方 province 层并没有"抢地"**。

### D3 代表省（17 省，几乎全是贸易品被换成幻想资源）

- `67 - Nurnberg.txt`：WS `trade_goods = paper` → MOD `garage_kit`（同时 base_manpower 3→7、extra_cost 16→删除、owner frr→hts）
- `4117 - Bezhetsk.txt:10`：`trade_goods = naval_supplies` → `Withered_bamboo`
- `518 - Chittor.txt`：`grain` → `magic_crystal`
- 其他：356 `livestock→sky_flower`、529 `cloth→iron_wood`、1226 `livestock→grease_ore`、1233 `livestock→magic_crystal`、1948 `silk→mithril`、2339/4793/4818 `grain→iron_wood`、2390 `fish→grease_ore`、2393 `fish→withered_bamboo`、2799 `livestock→mithril`、4391 `wine→mercury_flower`、4459 `grain→magic_crystal`、4713 `garage_kit→paper`

结论：`MOD` 的贸易品表已经整体幻想化，`WS` 还停在原版贸易品名——这类低风险，跟随 `MOD` 即可（见 7.2）。

### D4 代表省（205 省；494 个日期块内容变化 + 8 个 WS 独占块）

块内变更键频次：`controller 327 / owner 159 / add_core 130 / remove_core 96 / discovered_by 8 / trade_goods 1 / add_claim 1 / revolt 1`——**D4 的 96% 是 `FRA → JDA` 这类 tag 替换**，不是新增历史内容。`MOD` 侧**没有新增任何日期块**（`MOD_ONLY` 块 = 0），只有内容改写。

```diff
# 100 - Friesland.txt:45 (WS) / :44 (MOD)
-1810.7.10 = {	owner = FRA
-	controller = FRA
-	add_core = FRA
+1810.7.10 = {	owner = JDA
+	controller = JDA
+	add_core = JDA
 } # Annexed by France
```

```diff
# 43 - Danzig.txt  1807.5.24
-controller = fra     +controller = jda
# 1743 - Cambray.txt  1665.9.17
-add_claim = fra      +add_claim = jda
```

```
# 101 - Genoa.txt 1499.1.1 / 1527.1.1 / 1805.6.10 全块 FRA→JDA（11 行替换）
```

`WS` 独占的 8 个日期块只在 2 个省：

| 省 | 块 | 含义 |
|---|---|---|
| 366 - The Canarias.txt（WS:16 起） | 1402.1.1 / 1478.1.1 / 1516.1.23 / 1713.4.11 | `MOD` **删除了整段卡斯蒂利亚殖民时间线**（该省在 MOD 版里只剩地形与发展度、无主） |
| 368 - Madeira.txt | 1419.1.1 / 1420.1.1 / 1425.1.1 / 1497.1.1 | 同上，葡萄牙殖民时间线被删 |

这 2 个省是「母 mod 主动清空历史」的孤例，属于第 7 节要人工裁决的项。

---

## 3. 高风险省清单（逐省合并对象）

定义：`D2` 或 `D4` 有差异 = **239 省**（D2 49 + D4 190）。

其中 **57 个省的 owner 属于幻想乡 36 国**（玩家可玩的幻想乡势力领土），全部是 D4（tag 替换），需优先核对：

```
101 102 103 104 105 107 109 115 116 117 118 119 120 121 122 123 126 127 130 142
165 201 202 204 205 1247 1862 1867 1871 1875 1933 1934 2976 2978 2979 2980
2981 2983 2984 2985 2986 2991 2992 4696 4719 4720 4721 4727 4728 4731 4732
4733 4734 4735 4738 4739 4740
```

**D4 类 190 省（按主分类）**：
```
18 43 44 45 50 52 54 55 56 57 71 74 75 77 78 80 84 85 86 87 88 89 101 102
103 104 105 107 109 115 116 117 118 119 120 121 122 123 126 127 130 136 137
142 165 167 168 169 170 171 172 177 178 179 180 182 184 190 195 197 199 201
202 203 204 205 212 227 228 229 230 231 232 271 272 276 292 293 295 358 361
362 363 366 368 454 770 771 1247 1743 1758 1759 1760 1761 1775 1826 1851
1857 1862 1867 1871 1874 1875 1876 1878 1880 1933 1934 1936 2215 2218 2316
2964 2969 2971 2972 2973 2975 2976 2978 2979 2980 2981 2983 2984 2985 2986
2987 2988 2991 2992 2993 4111 4115 4141 4150 4171 4243 4245 4246 4252 4316
4317 4329 4330 4331 4338 4384 4385 4386 4387 4388 4389 4441 4534 4535 4544
4556 4696 4697 4698 4714 4717 4718 4719 4720 4721 4727 4728 4731 4732 4733
4734 4735 4738 4739 4740 4741 4748 4752 4753 4754 4765 4767 4768 4771 4773
4776 4777 4787
```

**D2 类 49 省**：
```
67 70 99 100 173 174 183 185 186 194 196 200 680 681 690 691 695 696 704 726
1816 1879 1931 2112 2113 2136 2137 2138 2139 2140 2141 2142 2143 2144 2171
2172 2753 4112 4194 4195 4196 4211 4381 4382 4390 4391 4652 4695 4713
```

---

## 4. 母 mod 新版改动量化

**推断依据（必须标注）**：没有旧版母 mod 可比。判据 = 「`WS` 与 `MOD` 在同省上有差异，且 `MOD` 侧的内容不含 `tech_gensokyan`／`acg_*`／幻想乡文化痕迹」。`WS` 的 province 层除 `discovered_by = tech_gensokyan` 外几乎没有私有内容（见下），因此 **`MOD` 相对 `WS` 多出的 token ≈ 母 mod 新版改动量**。

### 4.1 MOD 侧多出的内容（835 个键值 token，分布在 253 个省）

| 键 | token 数 | 说明 |
|---|---|---|
| `controller` | 269 | 母 mod 重做主控 |
| `owner` | 217 | 母 mod 重做归属 |
| `add_core` | 126 | 核心调整 |
| `remove_core` | 76 | |
| `revolt` | 49 | 起义块写法（`{ }`→`{}`） |
| `culture` | 48 | 文化体系重组（`jeand→jeanne`、`acg_hongmao→shanhaijing`、`shiraikuroko→supperability_magic_culture`） |
| `trade_goods` | 18 | 贸易品幻想化 |
| `discovered_by` | 13 | 仅 acg_american 等 |
| `religion` | 5 | `confucianism→acg`/`idol_reg` |
| `capital` 3 / `latent_trade_goods` 2 / `base_production` 2 / `base_manpower` 1 / `revolt_risk` 1 / `add_claim` 1 / `size`, `type` 各 1 | 11 | 零散；`capital` 的 3 个是 `681/2171/2172` 的乱码回写（见 8.9） |

按省分档：`1-2 token` 108 省、`3-5 token` 110 省、`6-10 token` 32 省、`11+ token` 3 省（67 Nurnberg、70 Wurttemberg、4713 Urach——hts/frr 互换三件套）。

### 4.2 反向：WS 侧多出 2110 个 token，其中 `discovered_by` 占 1268

`WS` 独有 token 的键分布：`discovered_by 1268 / controller 270 / owner 219 / add_core 127 / remove_core 77 / culture 50 / revolt 49 / trade_goods 20 / __date 8 / religion 7 / capital 5 / add_claim 2 / is_city 2 / base_production 2 / base_manpower 1 / extra_cost 1`。

`WS` 与 `MOD` 的 controller/owner/add_core 数量几乎相等（270 vs 269、219 vs 217、127 vs 126）——这些是**同一批行的不同值**（`FRA` vs `JDA`），不是「我方额外写了内容」。**结论：`WS` 省份层的私有内容 ≈ 只有 `discovered_by = tech_gensokyan` 一件事**（该行在 1268 个交集省里出现；其余 1870−1268=602 个 gensokyan 省落在 633 个 WS 独有省里）。

### 4.3 五个代表省的完整 diff

**① 西欧 `100 - Friesland.txt`（D1+D2+D4）**
```diff
 # 100 Friesland - Principal cities: Leeuwarden & Harlingen
-culture = ShiraiKuroko          +culture = supperability_magic_culture
 religion = acg / add_core = SHI / owner = SHI / controller = SHI   （不变）
 discovered_by = western/eastern/muslim/ottoman                     （不变）
-discovered_by = tech_gensokyan                                     （MOD 无此行）
-1810.7.10 = { owner = FRA controller = FRA add_core = FRA }
+1810.7.10 = { owner = JDA controller = JDA add_core = JDA }
-1813.11.30 = { ... remove_core = FRA }
+1813.11.30 = { ... remove_core = JDA }
```

**② 东欧 `4117 - Bezhetsk.txt`（D1+D3）**
```diff
 base_tax = 2 / base_production = 2 / base_manpower = 1 / hre = no   （不变）
-trade_goods = naval_supplies      +trade_goods = Withered_bamboo
 discovered_by = eastern/western/nomad_group                        （不变）
-discovered_by = tech_gensokyan
 1450.1.1 = { discovered_by = SIB }                                 （不变）
```

**③ 东亚 `680 - Chongqing.txt`（D2，无 D1）**——见第 2 节 D2 片段：`HMC/acg_hongmao/confucianism` → `SHJ/Shanhaijing/acg`，并多出 `add_core = MNG`。该省在 `WS` 里**没有** `discovered_by = tech_gensokyan`，说明我方当初就没给它加视野。

**④ 幻想乡核心省 `101 - Genoa.txt`（D1+D4）**
```diff
 owner = KTY / culture = Sanae / religion = Gensokyo_reg / center_of_trade = 3   （双方一致！）
-discovered_by = tech_gensokyan                                     （MOD 无）
 1499.1.1 = { owner = FRA → JDA ... }      （5 个块共 11 行 FRA→JDA）
 1805.6.10 = { owner = FRA ... } → JDA
```
注意：`MOD` 的 101 名字是 `101 - Liguria.txt`，`WS` 是 `101 - Genoa.txt`——只有文件名差，内容同源。

**⑤ 非洲/大西洋 `366 - The Canarias.txt`（D4，MOD 删除时间线）**
```diff
 culture = berber / trade_goods = unknown / native_size = 5 ...   （不变）
-1402.1.1 = { discovered_by = western/muslim/ottoman/CAS; owner = CAS; religion = catholic; culture = castillian; trade_goods = sugar } # Castilian control
-1478.1.1 = { capital = "Las Palmas" }
-1516.1.23 = { controller = SPA owner = SPA add_core = SPA }
-1713.4.11 = { remove_core = CAS }
```
母 mod 新版**主动清空**了加那利/马德拉的殖民史（该省在 MOD 版变成无主土著地）。

---

## 5. `discovered_by` 机制核实结论

### 5.1 事实统计

| 项 | `WS` | `MOD` | `PT` |
|---|---|---|---|
| `discovered_by = tech_gensokyan` | **1870 文件 / 1870 行** | 0 | **0**（全删） |
| `discovered_by = acgr_gXX` | 0 | **0 文件 / 0 行** | **2945 文件 / 42905 行** |
| 原版四组（muslim/ottoman/western/eastern） | 1761/1751/1100/1091 行 | 1167/1165/862/851 行 | 1758/1748/1094/1089 行（保留） |
| 其他科技组 | indian 762、chinese 482、nomad_group 848、acg_american 1 | indian 427、chinese 445、nomad_group 844、acg_american 781、north_american 473、south_american 269、mesoamerican 123、andean 88、east_african 180、polynesian_tech 9、aboriginal_tech 16 | 增 acg_american 781、chinese 735、indian 806 |
| TAG 型 discovered_by | SPA 39、POR 460、GBR 130… | SPA 646、POR 371、GBR 333、JDA 194、QNG 46… | 同 MOD + acgr |

- **`MOD` 的省份文件从来没有给 `acgr_gXX` 写过 `discovered_by`（0 次 / 0 文件）**，Lead 的抽查结论在全库成立。
- `WS` 的 1870 个 gensokyan 省：618 落在 633 个 WS 独有省，1268 落在交集省（个别省如 680/681 中国省没写）。按 ID 段抽样看覆盖面无地域偏好：欧洲 1–500、印度 503–570、东亚 661–739、东南亚 617–660、非洲 788–1250、海区 1250–1480、美洲 1477–1480 均有；`WS` 里 `continent`/`region` 不写在 province 文件，只能按 ID 段判断。
- `PT` 每省 acgr 行数：42905 / 2945 ≈ **14.6 条/省**，但集合不一致（g18 2922 省、g23 2141、g01/g02/g04 各 1860、g11 1842、g07 1755、g14/g15/g16 各 1118、g03/g17/g26/g28/g30/g33 各 724 …），说明他按「区域→兵种组」手工挑了一批，不是 36 组全写。
- `PT` **没有删掉原版四组**（muslim 1758 ≈ WS 1761，仅差个别覆盖省），只删了 `tech_gensokyan` 1870 行。

### 5.2 36 组 acgr 到底是什么（关键判据）

| 检查点 | 结果 |
|---|---|
| `MOD/history/provinces` 里 `discovered_by = acgr_` | **0 次 / 0 文件** |
| `MOD` 全库 `acgr_gNN` 命中 | 1541 文件 / 7134 行：`common/*` 6854 行（`common/technology.txt:214` 起 36 组定义 + `common/units/acgr_gNN_*.txt` 兵种），`history/*` **280 行** |
| `MOD/history/countries`（303 文件）里的 acgr | **280 个文件**，全部形如 `ABD - Albedo.txt:2: unit_type = acgr_g14` |
| `MOD` 全库 `technology_group = acgr` | **0 命中**（history/countries、common/countries、common/governments、common/scripted_effects、events 全部无） |
| `MOD/common/technology.txt` | 55 组，`acgr_g01..g36` 定义体一致（`start_level = 3`、`start_cost_modifier = 0`、`nation_designer_trigger = { always = no }`） |

**结论（明确回答任务书问题）**：

1. 36 个 `acgr_gXX` 是**兵种组**（`unit_type = acgr_gXX`，280 国使用），不是任何国家的 `technology_group`。EU4 的 `discovered_by` 生效对象是「科技组 + TAG」，**视野按 `technology_group` 判定**。既然全库 0 个国家把 `acgr_gXX` 设为 `technology_group`，**省份层给它们写 `discovered_by` 永远不会生效**。
2. 母 mod 自己 0 次写 `acgr` 的 `discovered_by`，这是作者的设计选择，不是我方遗漏。
3. **判定：36 组不是「休眠组」（它们被 280 国用作兵种），但在「视野」维度上是「非视野组」，省份层不需要、也不应该写 `discovered_by = acgr_gXX`。**
4. `PT` 的 42905 条 `discovered_by = acgr_gXX` = **语法可接受但永远不生效的冗余**，副作用是每省 +15 行、文件体积膨胀（`PT` 的 `history/provinces` 工作树比 `WS` 多出约 40 MB 级插入），并挤掉了真正生效的 `tech_gensokyan`。

---

## 6. 合作伙伴（`PT`）改动性质判定

### 6.1 总量

```
git -C PT diff --stat -- history/provinces
 1897 files changed, 39582 insertions(+), 3130 deletions(-)
git -C PT status --porcelain  →  3327 行： M 2020 / D 1 / ?? 1306
  history/provinces 拆分： M 1896 / D 1 / ?? 1057
  ?? 中 history 相关 1302（provinces 1057 + countries 245）
```

- 唯一的 `D`：`history/provinces/2046 - Nasirabad.txt`（就是 `WS` 里那个双扩展名脏文件的另一半，他删掉了 `.txt` 版本）
- `??` 1057 个省文件 = 母 mod/vanilla 全量里 `WS` 没有的部分（例：`1000 - Cree.txt`、`1001 - Sault.txt`…），他直接把整份文件拷进来
- `??` 另有 245 个国家历史文件（`history/countries/ABD - Albedo.txt` 等），不在本报告范围

### 6.2 操作模式判定：**「整份覆盖 + 追加 acgr」**，比例 99.8%

判定方法（比抽样更硬的判据）：把 `PT` 工作树文件里所有 `discovered_by = acgr_*` 行剔除后，与 `MOD` 同 ID 文件归一化比较。

| 判定 | 省数 | 比例 |
|---|---|---|
| 剔除 acgr 行后与 `MOD` **完全一致** → 整份覆盖 | **2320 / 2325** | **99.8%** |
| 仍有其他差异（手工合并或用了更旧母 mod 版） | 5（680、681、2171、2172、4211） | 0.2% |

补充判据：`PT` 相对 `WS` 改了 `owner/controller/culture/religion` 的省共 **50 个**，其中 **50/50 的新值与 `MOD` 完全一致**（culture 48 省、owner 40 省、controller 40 省、religion 5 省），无一个省的新值来自别处。

### 6.3 抽样 8 省的 `git diff` 指标

| 省 | +行 | −行 | 新增 acgr | 删 gensokyan | 非 discovered_by 增/删 | 判定 |
|---|---|---|---|---|---|---|
| `1-Uppland.txt` | 23 | 1 | 23 | 1 | 0 / 0 | 纯追加 |
| `6-Skane.txt` | 23 | 1 | 23 | 1 | 0 / 0 | 纯追加 |
| `2356 - Shymkent.txt` | 10 | 1 | 9 | 1 | 0 / 0 | 纯追加 |
| `100 - Friesland.txt` | 28 | 6 | 23 | 1 | 5 / 5（culture,controller,add_core,remove_core） | **整份覆盖** |
| `183 - Ile-de-France.txt` | 32 | 10 | 23 | 1 | 9 / 9（owner,controller,culture,add_core） | **整份覆盖** |
| `101 - Genoa.txt` | 34 | 12 | 23 | 1 | 11 / 11（owner,controller,add_core,remove_core） | **整份覆盖** |
| `4117 - Bezhetsk.txt` | 24 | 2 | 23 | 1 | 1 / 1（trade_goods） | **整份覆盖** |
| `680 - Chongqing.txt` | 26 | 10 | 16 | 0 | 8 / 8（owner,controller,add_core,culture,religion） | **整份覆盖**（该省 WS 本来没 gensokyan） |

`100 - Friesland.txt` 的实际 diff（`git diff` 摘录）：
```diff
-culture = ShiraiKuroko
+culture = supperability_magic_culture
-discovered_by = tech_gensokyan
+discovered_by = acgr_g14 / g18 / g09 / g08 / g01 / g07 / g04 / g11 / g15 / g21 / g16 / g02 / g05 / g32 / g10 / g22 / g20 / g23 / g31 / g12 / g36 / g24 / g06（23 行）
-1810.7.10 = { owner = FRA controller = FRA add_core = FRA }
+1810.7.10 = { owner = JDA controller = JDA add_core = JDA }
```

**为什么 1642 个文件看起来是「纯追加」**：`MOD` 只覆盖 2498 个省。凡是 `MOD` 没有的省（如 `6-Skane`），`PT` 拿不到新版文件，只能在原文件上追加 acgr；凡是 `MOD` 有的省，他就整份覆盖。全量统计：1897 个改动文件里，**1642 个无任何非 discovered_by 增删**（纯追加），**252 个双向覆盖**，255 个含删除。

### 6.4 后果分析：我方定制丢失多少？

**结论修正（与任务书预设不同）**：`PT` 的整份覆盖**造成的实际定制损失远小于预期**，因为 `WS` 省份层几乎没有私有内容（见 4.2）。

| 检查项 | 结果 |
|---|---|
| `WS` 的 12 个真正私有定制省（636、1156、2272–2277、2704、2705、4805、4806；owner = `BLS`/`AIU`，culture = `acg_wuthering_waves`/`acg_aiur`，与 vanilla 不同） | **`PT` 全部保留**（`MOD` 没有这些省 → 他只能追加，覆盖不到） |
| `WS` 里 owner ∈ 幻想乡 36 国的省 | 146 个，`MOD` 覆盖其中 **146/146**；`PT` 也都有 146/146。因为 `MOD` 版本来就是幻想乡归属，**覆盖不丢 owner** |
| 真正丢失的 | **1870 行 `discovered_by = tech_gensokyan` 全被删** → 幻想乡 36 国的开局视野全部失效（这是致命的） |
| 次生影响 | 50 个省的 culture/religion 被换成 `MOD` 新值（`ShiraiKuroko→supperability_magic_culture` 等）——这是**应该跟随**的改名，不是损失；57 个幻想乡省的日期块 FRA→JDA，同样是应跟随 |

一句话：**`PT` 的覆盖方向是对的，唯一致命错误是「把 `tech_gensokyan` 当垃圾删了，换成永不生效的 acgr」**。

---

## 7. 整合策略建议（方案，不含代码）

### 7.1 总体判定

以 **`MOD` 新版省份文件为基底**，只做三件事：
1. 给需要视野的省追加 `discovered_by = tech_gensokyan`（一行）；
2. 保留 `WS` 独有的 633 个省（母 mod 没改，其中 621 个 = vanilla + gensokyan，12 个含我方私有定制）；
3. 删除 `WS` 里 `MOD` 已有新版的所有旧快照覆盖（1270 个交集省中的 1015 个纯增量省直接换成 `MOD` 文件 + 加一行）。

> 依据：`WS` 省份层的私有内容只有 `discovered_by = tech_gensokyan`（1268 个交集省）与 12 个 WS 独有省的 owner/culture；其余差异全是旧母 mod 快照，跟随新版即可。

### 7.2 分项处理

**A. 母 mod 新增/改过的省（`MOD` 独有 1228 个）**
- **不补文件**。这些省我方没有覆盖，母 mod 新版内容自动生效，补一份反而会锁死版本。
- 唯一要检查的是「我方是否需要对它们加 `tech_gensokyan`」。判定标准：该省在 `WS` 的 gensokyan 覆盖范围内吗？现覆盖 1870 省。若产品需求是「幻想乡 36 国开局看到全世界」，则要给全部 2498 个 `MOD` 省都补；若维持现状（1870），则只需保证 `MOD` 有的 1270 省里那些原来有 gensokyan 的省（1268 个）继续有。

**B. 633 个 `WS` 独有省**
- 全部**保留原文件**，不做任何改动。它们是 `MOD` 不覆盖的省（母 mod 没改），删掉就丢 vanilla 定制（12 个省）和 gensokyan（626 个省），没有任何收益。
- 顺手清理 `2046 - Nasirabad.txt.txt`（双扩展名脏文件，与 `2046 - Nasirabad.txt` 重复 ID）。
- 这 633 个省里有 12 个是真私有定制（BLS/AIU 势力），建议加注释标记 `# WS custom`，方便下次母 mod 更新时识别。

**C. 239 个高风险省（D2 49 / D4 190）逐省合并规则**
1. **基底用 `MOD` 文件**（吸收 `qng→qin`、`fra→jda`、`hmc→shj/lsw`、`shiraikuroko→supperability`、贸易品幻想化、`acg_american` 视野）。
2. **只追加** `discovered_by = tech_gensokyan`。
3. **唯一需要人工裁决的 3 处**：
   - `67 / 70 / 4713`：`hts ↔ frr` 互换（`MOD` 把 Nurnberg 给 HTS、Wurttemberg 给 FRR）。若我方有剧情依赖（例如某国初始领土），按剧情定，否则跟随 `MOD`。
   - `366 / 368`：`MOD` 删除了加那利/马德拉的殖民时间线。若我方希望保留「卡斯蒂利亚殖民加那利」的历史，就保留 `WS` 的 1402/1419 块（但要注意 `WS` 的块里含 `discovered_by = tech_gensokyan`，属于把视野写进了日期块，需要拆出来放顶层）。
   - `680 / 681 / 2171 / 2172 / 4211`：`PT` 在这 5 个省上没跟 `MOD`（保留了自己的写法）。这 5 个是中国势力省（HMC/SHJ），需要和 `history/countries` 的中国板块一起裁决。
4. **D3 的 17 个省**（贸易品）：**无条件跟随 `MOD`**。`MOD` 的贸易品表已幻想化，`WS` 的 `naval_supplies`/`grain`/`cloth` 等是原版遗留。

**D. `discovered_by` 段最终形态（模板）**

推荐写法（顶层，紧跟原版四组之后，一行一条，不写 acgr）：

```
discovered_by = western
discovered_by = eastern
discovered_by = muslim
discovered_by = ottoman
discovered_by = tech_gensokyan      # 我方：幻想乡 36 国开局视野
```

带 `acg_american` 的省（母 mod 新版新增）：
```
discovered_by = western
discovered_by = eastern
discovered_by = muslim
discovered_by = ottoman
discovered_by = acg_american        # 母 mod 新版
discovered_by = tech_gensokyan      # 我方
```

**不写**：
```
discovered_by = acgr_g01 … acgr_g36   # 永不生效，禁止保留
```

注意两个坑：
- `366 The Canarias` 的 `discovered_by = tech_gensokyan` 现在写在 `1402.1.1` 日期块**内部**（`WS:21`），不在顶层。若按 B/C 规则以 `MOD` 为基底，这行会随整块被删——需要单独把它提到顶层。
- `1477 / 1480` 两个海区：`MOD` 用 `acg_american` 替换了 `western/eastern`，合并时两组都要留（`WS` 原有的 western/eastern + MOD 的 acg_american + gensokyan）。

**E. 是否给 36 个 acgr 组补 `discovered_by`**

**不补**。依据（第 5 节）：
- 母 mod 自己 0 次写；
- 36 组只被 280 国用作 `unit_type`，全库 `technology_group = acgr` 命中 0；
- `discovered_by` 按 `technology_group` 生效，写了也不生效。

若后续决定把这 36 组真的升格为科技组（`technology_group = acgr_gXX`），那必须在**同一批提交**里同时做三件事：改 `history/countries` 的 280 国 `technology_group`、给 2498 个省的 `discovered_by` 补 36 行、把 `WS` 的 `tech_gensokyan` 政体一起纳入。单独补省份层毫无意义。

### 7.3 与 `PT` 的对接

- 可以**直接采用 `PT` 的覆盖结果作为新基底**（2320/2325 与 `MOD` 一致，质量合格），只需补 3 件事：
  1. 在 2498（或 1270）个省重新加 `discovered_by = tech_gensokyan`；
  2. 删掉全部 42905 条 `discovered_by = acgr_gXX`；
  3. 处理 5 个例外省（680/681/2171/2172/4211）与 366/368。
- 不要接受 `PT` 的 `common/technology.txt`（丢了 `tech_gensokyan`）、`history/countries`（36 国科技组被换掉）——见基线对应章节。

---

## 8. 不确定项

1. **口径差异**：结构分类（D1 单独=1017）与 token 分类（纯增量=1015）差 2 个省，是 `366/368` 在两种判据下的边界情况（`MOD` 删块 → 结构上算 D4，token 上算「`MOD` 没新增」）。报告采用 **1015 / 255**。
2. **`ShiraiKuroko` 文化疑似无定义**：`99/100/1931/4381/4382` 五个省的 `culture = ShiraiKuroko`（`WS\history\provinces\100 - Friesland.txt:3`），但 vanilla、`MOD`、`WS` 三处 `common/cultures` 都搜不到该文化定义（`MOD` 只有 `supperability_magic_culture`，其 `male_names` 里含 `"Kuroko"`）。若属实，这 5 省当前文化是空引用。**需要 cultures 层同学校验**（`MOD\common\cultures\hre_cultures.txt:170` 一带）。
3. **`WS` 的 36 国 vs `MOD` 的 280 国是否同一批**：`MOD/history/countries` 有 280 个文件写 `unit_type = acgr_gXX`（`ALC - Alice Margatroid.txt:2` 等），`WS` 有 36 国写 `technology_group = tech_gensokyan`。若两者重叠，`WS` 覆盖会同时丢掉 `unit_type`（兵种表）——属 `history/countries` 层结论，本报告不下判断。
4. **`WS` 是否真的只需要 1870 省视野**：`WS` 有 1870 个省写了 gensokyan，但 `MOD` 有 2498 个省、vanilla 有 3923 个省。未覆盖的 628/2053 个省幻想乡国家看不到。这可能是设计（只给旧覆盖范围），也可能是历史遗留，需产品确认。
5. **`PT` 的 5 个例外省**（680/681/2171/2172/4211）：只能确认「与 `MOD` 不同」，无法确认他是故意保留还是用了更旧的母 mod 版本（没有旧母 mod 可比）。
6. **`PT` 的 `??` 1057 个省文件的来源**：均为 `MOD`/vanilla 有的省，但无法逐一证明是从哪一版拷贝（`MOD` 2498 vs vanilla 3923 的并集）。
7. **`WS` 的 633 独有省中 621 个 = vanilla + gensokyan**：仍可能有极小概率的 vanilla 版本差（`WS` 基于 1.37.x，本机 vanilla 也是 1.37.5，未逐行验证版本号）。
8. **与队友 `analysis/prov_conflict_class.csv`（355 行）的口径差**：该表按「任意字段集合差 + 行数差」统计，包含 `discovered_by` 本身与行数漂移，所以是 355；本报告是「剔除纯 `tech_gensokyan` 增量后的真冲突省」= 255（另 1015 纯增量）。两者不矛盾，引用时请注明口径。同理 `analysis/ws_only.txt`、`mod_only.txt`、`overlap_ws_mod.txt` 是**全仓库文件**清单（含 `descriptor.mod`、`common/technology.txt` 等），不是省份清单，不能与本报告的 1270/1228/633 直接对照。
9. **`MOD` 有 3 个省的 `capital` 是坏编码**：`681 - Yichang.txt`、`2171 - Xiangyang.txt`、`2172 - Jingzhou.txt` 的 `capital = "..."` 用 GB18030 解码仍是乱码（如 681 只剩 `"淩f"`），注释里保留 `# Yichang`。`WS` 对应值是正常英文名。整合时建议回填 `WS` 的值或正确中文名——这是母 mod 新版的编码事故，不是我方问题。
10. **`MOD` 的 province 文件编码不统一**：多数为 UTF-8，个别含中文（如 681）已被损坏；做自动合并脚本时按字节读写、不要整体转码，否则会二次破坏。

---

### 附：关键数字速查

```
WS 1904 文件 / 1903 ID（1 个重复 ID + 1 个 .txt.txt 脏文件）
MOD 2498 ID（只含它改过的省）
PT 2960 ID
WS∩MOD 1270 | MOD 独有 1228 | WS 独有 633
纯 discovered_by 增量 1015 | 真三方冲突 255 | 高风险(D2∪D4) 239
D2 49（qng→qin 22 / fra→jda 13 / culture 改名 5 / hmc→shj|lsw 5 / hts↔frr 3 / 其他 1）
D4 205（494 个块内容变化，96% 是 FRA→JDA；MOD 未新增任何块；WS 独占块仅 366/368 共 8 个）
D3 17（全部贸易品幻想化）
MOD 新版改动量 835 token / 253 省（controller 269 / owner 217 / add_core 126 / culture 48）
discovered_by：WS gensokyan 1870 | MOD acgr 0 | MOD 的 36 组是 unit_type（280 国）非 technology_group
PT：1897 文件 / +39582 −3130 | 2320/2325 整份覆盖 | 删 gensokyan 1870 | 加 acgr 42905 | 50 省值=MOD
```
