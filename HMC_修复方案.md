# 蓝兔（HMC）任务树 + on_action 修复方案与实施记录

> 日期：2026-09-28 ｜ 目标 mod：ACG_MEC_E（playset 最后一位）｜ 版本基线：EU4 1.37.5
> 证据基准：`F:\SteamLibrary\steamapps\common\Europa Universalis IV`（原版 1.37.5）＋ 本机 104 个 workshop mod

---

## 一、症状与根因（4 类，全部有证据）

用户确认的症状：任务 `HMC_missions_1_2`（七剑合璧，`set_country_flag = HMC_china_core_unlocked`）**已完成**，
但 ① 打下中国省份不自动加核心、② 每年不出现中国统一动态 buff、③ 任务树存在"奖励重复给同一个"的问题。

| # | 根因 | 证据 | 后果 |
|---|---|---|---|
| **R1** | `on_action` 体内用 `effect = { }` 包装 | 原版 `common/on_actions/00_on_actions.txt` 全篇 **0 处** `effect = {`（`:5810 on_conquest = { on_conquest_effect = yes }`；合法包法只有 `:5166` 的 `hidden_effect = {`）。本机 234 个 on_actions 文件里只有 **9** 个用包装，其中 **8** 个属于本项目（含 `mod\佣兵\ACG_MEC_E\` 副本）；ACG1（2796854877）全部直写 | **整段效果被静默丢弃** → 两条 oa 全哑 |
| **R2** | 效果名 `add_trade_income`、`add_crown_land` 在 EU4 **不存在** | 原版 `common/ events/ decisions/ missions/ history/` 全盘 **0 命中**；Wiki《指令》页亦 0 命中（原版只有 `trade_income_percentage` 这类修正；王领的正规效果是 `change_estate_land_share`，见 `common/buildings/00_buildings.txt:163`） | 任务 `3_3`、`5_5` 的该段奖励**静默白给** |
| **R3** | 4 个修正被重复授予 | 同名 `add_country_modifier` 不叠加，只刷新/替换时长。`HMC_missions.txt`：mythic_warrior ×3、hegemon ×3、qijian_unity ×2、qilin_blessing ×2 | 后完成的任务该段奖励白给；`1_1` 的 25 年版还会把 `4_4` 的永久版**顶掉**（降级覆盖） |
| **R4** | 全树 **0 条跨列连线** | 25 个任务全部只依赖同列上一格 | 游戏里是 5 根互不相干的竖柱 |

### 关键前提：同名 on_action 跨文件是**叠加**、不是覆盖
证据：ACG1 在独立文件里定义原版同名的 `on_battle_won_country` / `on_war_won` / `on_adm_development`
（`common/on_actions/uma_on_actions.txt`），而原版那几块里塞着大段原版机制（`00_on_actions.txt:475` 起）；
若为覆盖语义，ACG1 早就把原版战斗机制砸了。⇒ HMC 的 `on_yearly_pulse` 与 SKR 的可以并存，**不需要合并文件**。
（置信度：高置信推断；实测若仍哑 → 兜底把两者合并进同一文件的一个 `on_yearly_pulse` 块。）

---

## 二、修复内容

### 修复 A：on_action 写法（拆掉 20 处包装层）

| 文件 | on_action 块 | 拆掉的 `effect = {` | 花括号校验 |
|---|---|---|---|
| `common/on_actions/HMC_on_actions.txt` | 2 | 2 | 14/14 |
| `common/on_actions/SKR_on_actions.txt` | 14 | 14 | 111/111 |
| `common/on_actions/NNM_on_actions.txt` | 3 | 3 | 21/21 |
| `common/on_actions/ACG_MEC_HNA_on_actions.txt` | 1 | 1 | 6/6 |
| `common/on_actions/ACG_MEC_EX_on_actions.txt` | 1 | 0（本来就对） | — |

改法：删掉 `effect = {` 与配对 `}`，内容提升一层（逻辑一字未改；脚本做过"内容签名比对"确认无内容增减）。
`HMC_on_actions.txt` 另加了两行**临时验证探针**：

```
on_conquest   → log = "HMC_OA_conquest_fired"
on_yearly_pulse → log = "HMC_OA_yearly_pulse_fired"
```

`log` 写入 `logs/game.log`（Wiki《指令》页明写；原版实例 `common/scripted_effects/02_scripted_effects_preview_missions.txt:21`）。
**验证通过后删掉这两行。**

> 注意区分：`common/government_mechanics/` 里的互动块用 `effect = { }` 是**正确**的
> （原版 `10_hessian_militarization.txt:51`），本次未动。

### 修复 B：任务奖励去重（保留 7 个修正，每个只留一个给点）

| 任务 | 原奖励 | 改后 |
|---|---|---|
| `1_1` 初露锋芒 | `qijian_unity` 25 年 | **保留**（升级路径第一段） |
| `2_2` 讨伐魔教 | `mythic_warrior` 永久 ❌重复 | `add_army_tradition = 20` + `add_treasury = 500` |
| `2_5` 势如破竹 | `mythic_warrior` 永久 | **保留（唯一给点）** |
| `3_3` 商路通达 | `add_trade_income = 100` ❌无效名 | `add_treasury = 750` + `add_mercantilism = 2` |
| `3_4` 祥瑞遍地 | `qilin_blessing` 永久 ❌重复 | `add_years_of_income = 1` + `add_mercantilism = 3` |
| `1_5` 麒麟赐福 | `qilin_blessing` 永久 | **保留（唯一给点）** |
| `4_4` 同仇敌忾 | `qijian_unity` 永久 | **保留**（升级路径第二段：把 25 年版顶成永久版） |
| `4_5` 名震天下 | `hegemon` 永久 ❌重复 | `add_legitimacy = 20` + `add_splendor = 300` |
| `5_2` 登基称帝 | `hegemon` 永久 ❌重复 | `add_legitimacy = 30` + `add_splendor = 300` |
| `5_4` 光复中原 | `mythic_warrior` 永久 ❌重复 | `add_army_tradition = 25` + `add_years_of_income = 1` |
| `5_5` 天下归心 | `hegemon` 永久 + `add_crown_land = 10` ❌无效名 | **保留 hegemon（唯一给点）** + `change_estate_land_share = { estate = all  share = -0.10 }` |

其余任务奖励未动。除 `qijian_unity`（1_1 25 年 → 4_4 永久 = 设计上的升级路径）外，每个修正全局只有 1 个给点。

**效果名全部原版验证**：`add_treasury`(385 处)、`add_army_tradition`(273)、`add_splendor`(72)、`add_prestige`(2028)、
`add_stability`(866)、`add_mercantilism`(`02_anglican_aspects.txt:189`)、`add_years_of_income`(`:190`)、
`add_legitimacy`(`01_scripted_effects_for_simple_bonuses_penalties.txt:82`)、
`change_estate_land_share`(`00_buildings.txt:163-166`「大清真寺产生王领」⇒ share 为负 = 划给王领)。

### 修复 C：任务树结构重排（单根阶梯）

| 列 | 行范围 | 跨列前置 |
|---|---|---|
| 1 七剑之誓 | 1–5 | 根 `HMC_missions_1_1` |
| 2 长虹威名 | 2–6 | `2_1` ← `1_1` |
| 3 麒麟祥瑞 | 3–7 | `3_1` ← `2_1` |
| 4 七侠同袍 | 4–8 | `4_1` ← `3_1` |
| 5 天下归一 | 5–9 | `5_1` ← `4_1` |

同列为 `X_{n+1} ← X_n`。**为什么必须错开**：跨列连线硬规则是 Δ行 = 1，而 `position = 1` 上面没有行，
所以"5 列都从第 1 行开始"在数学上永远挂不上跨列前置。
任务 ID 未改 ⇒ **本地化 key（`<任务名>_title` / `_desc`）零改动**，无需重新编码。
顺带解决 R3 的降级覆盖：加连线后 `1_1` 必然早于 `4_4` 完成。
（原版 `position` 值域 1–23，最长树远大于 9 行，空间充足。）

### 修复 D：BLS / NNM 同类无效效果名

| 文件:行 | 原 | 改后 |
|---|---|---|
| `missions/BLS_missions.txt:147` | `add_trade_income = 50` | `add_treasury = 400` + `add_mercantilism = 1` |
| `missions/BLS_missions.txt:516` | `add_crown_land = 10` | `change_estate_land_share = { estate = all  share = -0.10 }` |
| `common/government_mechanics/NNM_mikazuki_mechanic.txt:173` | `add_crown_land = 5` | `change_estate_land_share = { estate = all  share = -0.05 }` |

---

## 三、自检结果（全部通过）

```
structure: 连线总数=24  其中跨列=4  越界/错误=0   根节点=1 (HMC_missions_1_1)
占位唯一性: OK（25 个 (slot,position) 无重复）
花括号: 7 个改动文件全部平衡（14/14, 111/111, 21/21, 6/6, 148/148, 160/160, 70/70）
on_actions 目录 effect = { 包装残留 = 0
无效效果名残留（排除注释）= 0
编码: 有改动文件全部 UTF-8 无 BOM；on_actions/missions 保持原有换行风格
```

## 四、下一步验证清单（需要你跑一局）

1. 启动游戏（playset 不变，ACG_MEC_E 仍在最后）。
2. 控制台自查：任务 `HMC_missions_1_2` 完成后，打下任意中国省份 → 该省份应**立即变成 HMC 核心**。
3. 看 `F:\Paradox Interactive\Europa Universalis IV\logs\game.log`：
   - 应出现 `HMC_OA_conquest_fired`（征服瞬间）与 `HMC_OA_yearly_pulse_fired`（每年 1 月）；
   - 若两条都没有 → R1 之外的兜底（把两个 `on_yearly_pulse` 合并进同一文件的一个块）。
4. 打开任务界面：应从 `HMC_missions_1_1` 单根展开、5 列阶梯错开、4 条斜线连通。
5. `logs/error.log` 里 HMC / BLS / NNM 相关行数应为 0。
6. 验证通过后删掉 `HMC_on_actions.txt` 里的两行 `log` 探针。

## 五、不确定项（单列，不与已确认内容混）

- `effect = { }` 到底是"未知键报错"还是"静默忽略"，离线无法 100% 证实；但**直写式是原版唯一用法**，改完必然正确。
- "同名修正重复 add 用新 duration 顶掉旧 duration"为 EU4 常规行为（本地资料未明写）⇒ 高置信推断。
- 同名 on_action 跨文件叠加为高置信推断（ACG1 举证）；兜底方案见 §四.3。
- `change_estate_land_share` 的符号语义为高置信推断（依据原版唯一用法：产生王领时 share 为负）。

## 六、回滚

```powershell
cd "F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E"
git checkout -- common/on_actions missions/HMC_missions.txt missions/BLS_missions.txt common/government_mechanics/NNM_mikazuki_mechanic.txt
```

## 七、遗留（未修，待你决定）

- `mod\佣兵\ACG_MEC_E\` 是一整份 ACG_MEC_E 的重复副本（同名 `.mod`、`missions/HMC_missions.txt` 逐字节相同，
  当前 playset 未启用）。建议删掉或改名，避免以后"改了没生效"。
- 项目内可能还有**其它同类无效效果名**（本次只按已确认范围扫了 `add_trade_income` / `add_crown_land`）。
  如需全量审计：把 mod 脚本里所有 `key = ` 左值与原版效果/触发器清单做差集。
- `HMC_missions_1`…`HMC_missions_5` 这 5 个本地化 key 是任务树级标题，原版任务树**没有**树级标题键 ⇒ 当前是死键（无害）。
