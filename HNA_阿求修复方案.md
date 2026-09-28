# 稗田阿求（HNA）修复记录：战斗成长口径 + 升级后专属特质丢失

> 日期：2026-09-28 ｜ 版本基线：EU4 1.37.5 ｜ 证据基准：本机原版 + 104 个 workshop mod 全库扫描

---

## 一、问题一：战斗成长不是 2% 随机（事实查证结论）

**结论：没有随机、没有百分比。规则是「陆战获胜 + 阿求在役 + 90 天冷却 + 每次 +1 成长点」。**

完整链路（逐行核对）：

| 环节 | 位置 | 内容 |
|---|---|---|
| 钩子 | `common/on_actions/ACG_MEC_HNA_on_actions.txt` `on_battle_won_country` | 三重门：`tag = HNA` + `has_reform = ACG_MEC_HNA_chronicle_reform` + `has_leader = "Hieda no Akyuu"` |
| 冷却 | `common/scripted_effects/ACG_MEC_HNA_effects.txt` `HNA_akyuu_battle_growth_effect` | `had_country_flag = { flag = HNA_akyuu_battle_cd days = 90 }` 到期才清 flag |
| 发放 | 同上 | `NOT = { has_country_flag = HNA_akyuu_battle_cd }` 且未达 peak → `+1` |

- 全 HNA 脚本 grep `random_list|chance|random =|2%` 只命中 `ai_chance`（事件 AI 选项权重），与本机制无关。
- 「像小概率」的来源大概是量级：90 天冷却 ⇒ 最多 ~4 点/年，而 tier 16 需要 320 点 ⇒ **纯靠打仗约 80 年**；实际成长点主要来自任务树（11 处 `HNA_akyuu_grant_growth_effect`）与成书事件（15 处）。
- ⚠️ **本次之前它从未运行过**：`ACG_MEC_HNA_on_actions.txt` 整块被 `effect = { }` 包着（与 HMC/SKR/NNM 同一个根因，已于 2026-09-28 修复），on_action 体内用 `effect = { }` 会让整段效果被静默丢弃。

> 关于"特质是不是战斗随机给的"：也不是。`common/leader_personalities/ACG_MEC_HNA_lp.txt` 两个特质都写了 `allow = { always = no }`，永远不会随机获得，只能由脚本 `trait =` 指派。原版同款设计：`common/leader_personalities/00_core.txt` 有 4 个 `always = no` 特质，其中 3 个（`dragon_tiger_general_personality`、`great_explorer_personality`、`bestevaer_personality`）正是靠脚本 `trait =` 指派的。

---

## 二、问题二：升级后将领专属特质丢失（根因与修法）

### 症状（用户实测）
- **tier 0（召出阿求）**：特质 `akyuu_chronicler_personality` 正常显示 ✅
- **tier 1 及以上（任意一次升级）**：四维已按新等级提高，但将领面板上**连特质那一行都没有** ❌

### 根因
`HNA_akyuu_rebuild_general_effect` 原本是「同一个执行块里先 `kill_leader` 再 `define_general`」：

```eu4
if = { limit = { has_leader = "Hieda no Akyuu" } kill_leader = { type = "Hieda no Akyuu" } }
if = { limit = { tier >= 16 } define_general = { ... trait = akyuu_chronicler_peak_personality } }
```

- **tier 0 时 `has_leader` 为假**（召出决议的 potential 就要求 `NOT = { has_leader = ... }`）⇒ 没有 kill，`define_general` 是干净创建 ⇒ 特质正常。
- **升级时 `has_leader` 为真** ⇒ 同帧内先 kill 再 define ⇒ **EU4 照常写入四维，却把 `trait =`（leader personality）整个吞掉**。

### 证据链
| 证据 | 内容 |
|---|---|
| 原版 1.37.5 | 共 **26** 个「带 `trait =` 的 `define_general`」块，**没有任何一个紧邻 `kill_leader`** —— 全部是干净创建（`events/flavorAIMARA.txt:161-168`、`missions/DH_Timurid_Missions.txt:229+` 等） |
| 全库扫描 | 108,526 个 mod 脚本文件里，"kill + define" 紧邻的只有 Touhou 系 mod 与 ACG1 少数几处；而 **ACG1 的规范写法是把 `kill_leader` 放事件 `immediate`、`define_general` 放事件 `option`**（`events/ACG_advise_2_events.txt:975-996`）——刻意分成两个执行时机 |
| 语法排除 | `define_general` 内 `trait =` ✅ 合法；`kill_leader = { type = "名" }` ✅ 合法（原版 `disaster_ambrosian_republic.txt:446`）；`has_leader = "名"` ✅ 合法（原版 40 处）；两个特质的修正键全部原版存在（`fire_damage`/`shock_damage`/`movement_speed`/`siege_ability`/`recover_army_morale_speed`/`land_morale`） |
| 症状对照 | 若为「特质定义没加载」→ 连 tier 0 也不会有；若为「同帧 kill 吞特质」→ 恰好只有升级路径丢失 ✅ 与实测一致 |

### 修法：两段式（kill 与 define 分到两个执行时机）

**入口效果自动分岔**（`HNA_akyuu_rebuild_general_effect`）：

```eu4
HNA_akyuu_rebuild_general_effect = {
	if = {
		limit = { has_leader = "Hieda no Akyuu" }        # 在役：必须先撤下
		kill_leader = { type = "Hieda no Akyuu" }
		set_country_flag = HNA_akyuu_rebuild_pending     # 预约重建
	}
	else = {
		HNA_akyuu_define_general_effect = yes            # 不在役：干净创建（原本就正常）
	}
}
```

**载波分工**（把 define 挪到"下一个执行时机"，全部复用已存在的弹窗，零新增弹窗/零新增本地化 key）：

| 路径 | 载波 | 说明 |
|---|---|---|
| 升级 tier 1–15 | `events.1` 突破选项 | 原本每次突破就弹，直接复用 |
| 升级 tier 16（四维圆满） | `events.30` 四维圆满选项 | tier 16 那一级**不排突破事件**，改由圆满事件承载 |
| 整军决议 | `events.60`（新增事件，**复用 `.40` 的本地化 key**） | 该决议原本不弹事件，需要载体 |
| 兜底 | `on_monthly_pulse` | 弹窗一直没人点时，下个月自动补建，最多缺席一个月 |

**召出 / 再召两条决议完全未改**：两条的 potential 都要求她不在役 ⇒ 走 `else` 分支干净创建 ⇒ 本来就是好的，不动。

**幂等保护**：`HNA_akyuu_define_general_effect` 第一行就是 `clr_country_flag = HNA_akyuu_rebuild_pending`，所有载波调用点都带 `if = { limit = { has_country_flag = ... } }` 守卫 ⇒ 多个弹窗/兜底重复触发时只有第一个真正执行，不会出现同名双将领。

---

## 三、改动文件

| 文件 | 改动 |
|---|---|
| `common/scripted_effects/ACG_MEC_HNA_effects.txt` | 入口效果拆成「在役撤下 / 不在役直建」分岔；原 17 个等级分支表迁到新的 `HNA_akyuu_define_general_effect`（只 define、不 kill） |
| `events/ACG_MEC_HNA_events.txt` | `.1` 与 `.30` 选项内加重建守卫调用；新增 `.60` 整军重建载波（复用 `.40` 文本）；文件头补 v7 变更说明 |
| `decisions/ACG_MEC_HNA_decisions.txt` | 整军决议追加 `country_event = { id = ACG_MEC_HNA_events.60 days = 1 }`；再召决议的注释同步 |
| `common/on_actions/ACG_MEC_HNA_on_actions.txt` | 新增 `on_monthly_pulse` 兜底（预约未处理时自动补建） |

**本地化：零改动**（新事件 `.60` 复用 `.40` 的 `title` / `desc` / `option name`，新 flag 不需要文本）。

## 四、自检结果

```
花括号: effects 206/206、on_actions 13/13、events 98/98、decisions 47/47  全部平衡
define_general 块 = 17（tier 16 + 15..1 + tier 0），17 个全部带 trait =  ✓
kill_leader 与 define_general 已不在同一执行块 ✓
重建预约 flag：1 处 set（入口）、1 处 clear（define 首行）、4 处守卫调用 ✓
```

## 五、验证清单（需跑一局）

1. HNA 开局 → 决议「召稗田阿求出任将领」→ 面板应有特质「稗田阿求」✅（应与修复前一致）。
2. 攒到 20 成长点触发 tier 1 → 等 1 天出现「突破」弹窗 → **点选项后**看将领面板：四维应为 7/7/8/6，且**特质仍在**。
3. 决议「为阿求整军」→ 1 天后出现弹窗 → 点选项 → 特质仍在。
4. 升到 tier 16 → 「四维圆满」弹窗 → 点选项 → 特质应换成「幻想乡史笔」（`akyuu_chronicler_peak_personality`）。
5. 故意不点弹窗 → 下个月月初阿求应被自动补回（兜底生效）。
6. `logging`：`logs/error.log` 内 HNA 相关行应为 0。

## 六、不确定项（单列）

- 「同帧 kill+define 会吞掉 personality」的确切内部机制未在离线环境证实，**结论来自症状对照 + 原版/全库写法统计**；若换到下一执行时机仍丢，则说明该特质另有问题，需再查（下一步会把 `log` 探针加进 define 分支）。
- 兜底依赖 `on_monthly_pulse`（原版 `common/on_actions/00_on_actions.txt:2046` 该块为空，但 on_action 名存在）。主路径不依赖它，它只是在弹窗无人点击时保底。
- 升到 tier 16 时若「四维圆满」事件因 `HNA_akyuu_peak_flag` 已置位而不触发，则当次重建只靠兜底（最多一个月）。

## 七、回滚

```powershell
cd "F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E"
git checkout -- common/scripted_effects/ACG_MEC_HNA_effects.txt events/ACG_MEC_HNA_events.txt decisions/ACG_MEC_HNA_decisions.txt common/on_actions/ACG_MEC_HNA_on_actions.txt
```

---

# v8 追加（2026/9/28）：成书事件奖励 —— 永久 buff 不再重复白给

## 问题
v6 去掉 `fire_only_once` 后 `.10`–`.14` 可重复刷，但其中 **10 个选项发的是永久修正**
（`duration = -1`）。同名修正重复发放只会刷新时长 ⇒ 玩家再次看到同一选项时，必须自己回忆
"这个永久 buff 我是不是已经拿过了"，否则就是白点一次。

## 修法（选项**保留可见**，只把「发修正」那一段包进守卫）
```eu4
option = {   #发展向
	name = "ACG_MEC_HNA_events.10.a"
	if = {
		limit = { NOT = { has_country_modifier = ACG_MEC_HNA_reward_dev_1 } }
		add_country_modifier = { name = ACG_MEC_HNA_reward_dev_1 duration = -1 }
	}
	# 额外奖励：无论是否首次都照发 ⇒ 旧选项永远不是空奖励
	add_treasury = 200
	add_prestige = 10
	HNA_akyuu_grant_growth_effect = { amount = 4 }
}
```

## 额外奖励表（10 个永久修正选项，全部每次点击都发）

| 选项 | 守卫的修正 | 额外奖励 |
|---|---|---|
| `.10.a` 发展向 | `reward_dev_1` | treasury 200 + prestige 10 |
| `.10.c` 军事向 | `reward_army_1` | army_tradition 10 + splendor 100 |
| `.11.a` 建筑向 | `reward_build_1` | treasury 300 + mercantilism 2 |
| `.11.c` 军事向 | `reward_army_2` | army_tradition 10 + splendor 100 |
| `.12.b` 军事向 | `reward_army_2`（与 .11.c 同一个） | army_tradition 10 + splendor 100 |
| `.12.c` 内政向 | `reward_adm_1` | adm 100 + splendor 100 |
| `.13.a` 军事向 | `reward_army_3` | army_tradition 15 + splendor 150 |
| `.13.c` 内政向 | `reward_adm_1`（与 .12.c 同一个） | adm 450（原 300 + 新 150）+ splendor 150 |
| `.14.b` 永久向 | `chronicle_permanent` | splendor 200 + stability 1 |
| `.14.c` 魔法向 | `reward_magic_tech` | Mana 200 + Magic_exp 100 |

**两个限时修正选项按需求不加守卫**：`.11.b`（`reward_magic_mana` 3650 天）、
`.12.a`（`reward_magic_exp` 5475 天）—— 重复领取会**刷新时长**，本身不是白给。
**三个不发修正的选项不变**：`.10.b` / `.13.b` / `.14.a`。

## 自检
```
花括号 133/133 平衡；BOM=False；LF
12 个发修正的选项：10 个永久 → 全部带守卫且 limit 里的名字与发放名逐字一致 ✔
                    2 个限时 → 无守卫（按需求）✔
额外奖励用到的效果名原版全部存在：add_treasury(385) add_prestige(2028)
  add_army_tradition(273) add_splendor(72) add_mercantilism(378) add_adm_power(1285)
  add_stability(866) add_mil_power(881) change_variable(215)
```

## 同类漏网（未修，等你决定）
以下两个事件**各自只有一个选项、且发永久修正**，玩家若已从别处拿到，点下去等于空奖励：

| 事件 | 发的修正 | 可能已被谁发过 |
|---|---|---|
| `.30` 四维圆满 | `ACG_MEC_HNA_chronicle_permanent` | `.14.b`（可重复刷） |
| `.40` 阿求出任将领 | `ACG_MEC_HNA_reward_dev_1` | `.10.a`、任务 2_1 / 2_2 |

两者都是 `fire_only_once = yes`，所以只会在第一次遇到；修法与本节完全一致（加守卫 + 补 `else` 兜底奖励）。

