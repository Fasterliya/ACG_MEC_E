# 七神 / 三月 信仰事件 —— 交付说明

> 设计稿：`analysis/archon_events_edit_v2.html`（用户 2025-11-25 定稿 14 件改稿并入后）
> 交付日期：2026-11-25　EU4 1.37.5

## 一、新增文件（4 个，全部在 mod 内）

| 文件 | 内容 | 规模 |
|---|---|---|
| `events/acg_mec_e_archon_events.txt` | namespace `acg_mec_e_archon_events`，30 个 `country_event`（.1–.30） | 27.6 KB |
| `common/event_modifiers/acg_mec_e_archon_modifiers.txt` | 32 条国家修正 | 186 行 |
| `common/scripted_triggers/acg_mec_e_archon_triggers.txt` | 共用互斥 gate：`acg_mec_e_deity_event_gate` | 19 行 |
| `decode_localisation/acg_mec_e_archon_l_english.yml` | 111 个事件 key + 32 个修正 key = 143 条明文 | 待用户编码 |

未改动任何现有文件（`acg_mec_e_teyvat_religion_events.txt`、决议、personal_deities 均未碰）。

## 二、事件映射

| id | 设计稿 | 神 | 类型 | 标题 |
|---|---|---|---|---|
| .1 | A-1 | 巴巴托斯 | 恩泽 | 风起之时 |
| .2 | A-2 | 巴巴托斯 | 抉择 | 无主之歌 |
| .3 | A-3 | 巴巴托斯 | 仪式 | 高天之琴 |
| .4 | B-1 | 摩拉克斯 | 恩泽 | 契约之神的天平 |
| .5 | B-2 | 摩拉克斯 | 抉择 | 摩拉的重量 |
| .6 | B-3 | 摩拉克斯 | 仪式 | 璃月港的仲裁 |
| .7 | C-1 | 巴尔 | 恩泽 | 永恒之愿 |
| .8 | C-2 | 巴尔 | 抉择 | 锁国令 |
| .9 | C-3 | 巴尔 | 仪式 | 千手百眼 |
| .10 | D-1 | 布耶尔 | 恩泽 | 智慧的馈赠 |
| .11 | D-2 | 布耶尔 | 抉择 | 梦境之试 |
| .12 | D-3 | 布耶尔 | 仪式 | 兰那罗的园圃 |
| .13 | E-1 | 芙卡洛斯 | 恩泽 | 正义的审判 |
| .14 | E-2 | 芙卡洛斯 | 抉择 | 歌剧院的判决 |
| .15 | E-3 | 芙卡洛斯 | 仪式 | 水神的谢幕 |
| .16 | F-1 | 玛薇卡 | 恩泽 | 战意燃起 |
| .17 | F-2 | 玛薇卡 | 抉择 | 竞技场的挑战 |
| .18 | F-3 | 玛薇卡 | 仪式 | 灰烬中的重生 |
| .19 | G-1 | 瓦沙嘉 | 恩泽 | 无神之爱 |
| .20 | G-2 | 瓦沙嘉 | 抉择 | 严寒的考验 |
| .21 | G-3 | 瓦沙嘉 | 抉择 | 愚人众的效忠 |
| .22 | H-1 | 恒月 | 恩泽 | 恒月当空 |
| .23 | H-2 | 恒月 | 抉择 | 月相的裂痕 |
| .24 | H-3 | 恒月 | 仪式 | 月下的誓约 |
| .25 | I-1 | 虹月 | 恩泽 | 虹月市集 |
| .26 | I-2 | 虹月 | 抉择 | 色彩的诱惑 |
| .27 | I-3 | 虹月 | 仪式 | 虹月之潮 |
| .28 | J-1 | 霜月 | 恩泽 | 霜月行军 |
| .29 | J-2 | 霜月 | 抉择 | 寒夜的抉择 |
| .30 | J-3 | 霜月 | 仪式 | 霜月加冕 |

## 三、触发与防重入（与设计稿一致 + 一处纠偏）

```
trigger = {
    religion = acg_mec_e_seven_archons            # 或 acg_mec_e_moon_goddess
    has_personal_deity = acg_mec_e_deity_xxx
    acg_mec_e_deity_event_gate = yes              # scripted trigger
}
mean_time_to_happen = { months = 120 }
immediate = { set_country_flag = acg_mec_e_had_deity_event_flag }
after     = { clr_country_flag = acg_mec_e_had_deity_event_flag }
```

**纠偏**：设计阶段我提过 `set_country_flag = { flag = X days = 30 }` 的自动过期写法，落地时查证该写法不存在 —— `set_country_flag` 的签名是 `<string>`（EU4 文档 `effects.txt:47`），不是 block。故改为 gate 里用 `had_country_flag = { flag days = 30 }` 兜底放行：

```
acg_mec_e_deity_event_gate = {
    OR = {
        NOT = { has_country_flag = acg_mec_e_had_deity_event_flag }
        had_country_flag = { flag = acg_mec_e_had_deity_event_flag days = 30 }
    }
}
```

语义：flag 正常时严格互斥；flag 因 `after` 未执行而挂过 30 天，视为漏清、允许继续判定，避免整包 30 件事件被一个 flag 锁死。

## 四、与设计稿不同的 3 处（技术落地限制）

| 设计稿 | 落地形态 | 原因 |
|---|---|---|
| D-3「行政点数 +25、创新度 +5」 | `add_adm_power = 50` | `add_innovations` 在本机 1.37.5 全目录 grep 0 命中，文档索引也无此 effect，无法发放 |
| I-1「商人 +1」 | 并入 `acg_mec_e_rainbow_market` 修正（12 年，`merchants = 1`） | EU4 无「永久 +1 商人」instant effect，`merchants` 只能是国家修正 |
| F-1「获得 2 年人力」 | 修正 `acg_mec_e_pyro_levy`（730 天，`manpower_recovery_speed = 1.0`） | EU4 无动态乘法，`add_manpower` 只能写死绝对值；两年恢复翻倍与国力无关，等效两年人力 |

其余效果与数值全部照抄设计稿（含 C-2 双纯收益、C-3 50 军点冲击 +15% 等）。

## 五、证据（写码时逐条核对过的）

| 结论 | 证据 |
|---|---|
| `has_personal_deity = <deity>` | `events/Hinduism.txt:22`、`events/Norse.txt:20` |
| 事件 `after = { clr_country_flag }` 可用 | `events/ConsortEvents.txt:3195`、`events/flavorDAN.txt:2673` |
| `set_country_flag` 只吃 string | EU4-Doc `effects.txt:47` 签名 `<string>` |
| `had_country_flag = { flag days }` | `decisions/Religion.txt:613`、`events/MuslimDLC.txt:65` |
| `add_devastation` / `add_prosperity` 为 province 作用域 | `common/scripted_effects/00_scripted_effects.txt:94`；`events/flavorAJU.txt:417` |
| `add_unit_construction = { amount type speed cost }` | `common/scripted_effects/00_scripted_effects.txt:4273-4278` |
| `add_mercantilism` / `add_army_professionalism` / `add_navy_tradition` | `events/flavorAJU.txt:35,466,467`、`events/flavorETH.txt:1917` |
| `merchants` 是国家修正 | EU4-Doc `modifiers.txt:332`（country scope） |

## 六、自动检查结果

- 事件数 30，id 1–30 连续、无重复
- 事件 loc key 引用 111 条 → 明文源 0 缺失
- 修正定义 32 条 = 引用 32 条，无悬空引用、无孤儿定义
- 全 mod 内无同名 key 冲突（`find_definition acg_mec_e_wind_rising` 仅本文件定义）
- `eu4_verify_path`：3 个脚本文件均在 mod 内、未落原版目录
- `eu4_readback`：`acg_mec_e_archon_events.30` 回读命中，namespace 校验通过

## 七、待你处理 / 待验证

1. **`decode_localisation/acg_mec_e_archon_l_english.yml` 需要你编码进 `localisation/`**（143 条）。编码前游戏内显示裸 key。
2. `validate_script` 对 `.21` 的 `add_unit_construction` 报了 2 条 `SCOPE_MISMATCH`（`amount` / `type` 需要 country 作用域）—— 这是校验器把 block 内字段当独立 effect 解析造成的误报：原版 `00_scripted_effects.txt:4273` 就在 province 作用域里这么写。进游戏实测一次「接纳愚人众」是否真的排出 3 队步兵即可确认。
3. `add_prosperity = 100`（.13）对已满繁荣的省份会溢出到上限，无害；但全境拉满繁荣的强度体感极强，建议首测后在 `.13` 里改成 `capital_scope` + 邻近省份。
4. C-2 双选项纯收益、C-3 50 军点换冲击 +15% 等 6 条平衡疑点仍按你原稿保留，未擅自调整。

## 八、测试步骤

```
# 进游戏控制台
religion acg_mec_e_seven_archons
add_personal_deity? （无此指令，改用决议「重择七神」选神）
event acg_mec_e_archon_events.16      # 火：战意燃起
event acg_mec_e_archon_events.21      # 冰：愚人众（验证 3 队步兵）
event acg_mec_e_archon_events.13      # 水：全境繁荣
event acg_mec_e_archon_events.30      # 霜月加冕
```

- 想验 MTTH 真实频率：选神后 `tag` 到该国不点事件，观察 flag `acg_mec_e_had_deity_event_flag` 是否只在弹窗期间存在（`flags` 控制台无此指令，看 `debug_mode` 的省份/国家信息）。
- 想验互斥：连点两个 `event` 指令，第二件应正常弹出（手动触发不吃 gate，gate 只作用于 MTTH 判定）—— 这是预期行为。
