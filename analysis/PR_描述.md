# ACG_MEC_E 适配母 mod ACGR 0.5 —— 兵种组体系重构

> 分支：`integrate/acgr-0.5` ｜ 基线：`main@6447ea4` ｜ 本次提交：`dcfa988`
> 变更规模：353 文件 / +20,304 / -840

---

## 一、背景

母 mod `ACG1`（workshop `2796854877`）在 0.5 版本做了一次**兵种体系重构**，不是普通内容更新：

1. 新增 36 个兵种组 `acgr_g01..g36`，注册进 `common/technology.txt`（每组 `start_level 3` / `start_cost_modifier 0` / `nation_designer_trigger = { always = no }`）。
2. 把「兵种组」从 `technology_group` 里**独立**出来，改用国家级 `unit_type = acgr_gXX` + `set_country_flag = acgr_unit_group_gXX` 标记；`technology_group` 一律退回原版组（western 29 国 / muslim 7 国 / 其余原版组）。
3. 兵种定义改为 `common/units/acgr_gXX_<type>_<level>.txt`，按等级解锁写进 `common/technologies/mil.txt` 的 `enable =`（855 条 acgr）。
4. 国家模型偏好写进 `common/countries/*.txt` 的 `historical_units`（4,953 处 acgr 引用）。
5. 重做版图：`QNG(清)→QIN(秦)` 22 省、`FRA→JDA(贞德)` 13 省、`HMC→LSH/SHJ`、`HTS↔FRR` 互换、文化 `ShiraiKuroko → supperability_magic_culture`。

本 submod 是**整文件覆盖**型（2,222 个文件里 1,319 个与母 mod 同名），母 mod 对这 1,319 个文件的更新在本 submod 生效时会**全部失效**。本次适配的目标就是把这 1,319 个覆盖点改成「以母 mod 为底本 + 追加我方增量」。

---

## 二、本分支做了什么

### 1. `common/technology.txt` —— 56 组

以母 mod 版（55 组）为底本，在 `# END ACGR_UNIT_GROUPS` 之前插入我方 `tech_gensokyan` 块（带 `# BEGIN/END ACG_MEC_E` 边界注释，方便母 mod 下次更新时定位）。

> 为什么必须合并：原版 14 个 `unit_type` 取值全部落在 `common/technology.txt` 的组名集合内（0 例外）——**兵种组必须先注册成科技组，`unit_type` 才会被引擎识别**。只保留我方 20 组会让母 mod 的 972 个 acgr 兵种 + 280 国 `unit_type` 指向未注册组；反过来说，我方 `tech_gensokyan` 若被抹掉，36 个幻想乡国家的科技组同样悬空。

### 2. `common/technologies/mil.txt` —— 1,865 条 enable

采用合作方（PT）版本：母 mod 2,417 行 + 我方 74 条 `enable`，**0 条母 mod 内容丢失**。这是本轮唯一直接取用其成果的文件。

校验：`enable` 1,865 条（acgr 972 / `gen_t` 72），对账 `WS + 母 mod + 原版` 共 1,920 个单位后**悬空 enable = 0**。

### 3. `history/countries` —— 38 国以母 mod 为底本合并

- 36 个幻想乡国家：保留 `technology_group = tech_gensokyan`，**删除**母 mod 新加的 `# BEGIN ACGR_UNIT_GROUPS` 段（4 行：`unit_type` / `set_country_flag` 与两行边界注释），其余字段全部照母 mod。
- 34 国只差 6 行（4 行 ACGR 段 + 科技组取值），属机械合并。
- 4 国做字段级合并：

| 国 | 采用值 | 说明 |
|---|---|---|
| NMK | 母 mod 的 `Fujiwara_Mokou_government_reform` | 母 mod 新版改用的角色专属改革（弃我方 `Touhou_Republic_government_reform`，两者定义都在） |
| NNM | 我方 `NNM_mikazuki_government_reform` | 我方独有定义，母 mod 全库无 |
| SKR | 我方 `SKR_clow_card_reform` + `cards_magic_culture` + rank 1 + 友邦 TMY + 选帝侯；吸收母 mod 的 `death_date` 与 5 条君主特质 | 专属改革与外交关系是定制 |
| TMY | 我方 `cards_magic_culture` + 首都 265 + 友邦 SKR；吸收母 mod 的 `add_army_professionalism 0.04` / `national_focus = MIL` / `death_date` | 265 与 4726 双方 owner 均为 TMY，两个首都都安全 |

- 我方独有国 AIU / BLS / HMC / QNG 整份保留（`sub_saharan` / `chinese`，均为原版组）。
- 清理 NNM / SKR / TMY 的旧名重复文件（避免同 TAG 双份随机生效）。

### 4. `history/provinces` —— 1,270 省三方合并

| 批次 | 省数 | 处理 |
|---|---|---|
| 纯 `discovered_by` 增量 | 1,015 | 取母 mod 版 + 追加 `discovered_by = tech_gensokyan` |
| 实质冲突（D2/D4） | 228 | 取母 mod 版 + 追加视野（含 `FRA→JDA` 13 省、`HTS↔FRR` 3 省、文化改名 5 省） |
| **全字段保留我方** | **27** | QNG 22 省（`qng→qin` 母 mod 判给秦，我方保留清）+ HMC 5 省（虹猫为 submod 独有 TAG，母 mod 无） |
| 母 mod 独有省 | 1,228 | 无需操作（submod 不覆盖即继承） |
| 我方独有省 | 633 | 原样保留（含 12 个 BLS/AIU 私有省） |

海省补视界：1475 / 1476（母 mod 版为空文件，按原版补 `western` / `eastern`）、1477 / 1480（母 mod 只有 `acg_american`）。

校验：**1,897 个省文件**含 `discovered_by = tech_gensokyan`；AIU 的 7 省用 `sub_saharan`（非幻想乡，正确）。

### 5. 杂项

| 文件 | 动作 |
|---|---|
| `missions/ACGR_missions.txt` | 回退为 **838 行全注释**（本 submod 故意停用 ACG 通用任务树，有效行 0） |
| `common/governments/reform_levels_monarchy.txt` | 保留我方 9 条改革注册 + 补母 mod 的 `contact_with_miku_reform_mikuver` |
| `common/governments/reform_levels_republic.txt` | 保留我方 `ACG_MEC_HNA_chronicle_reform` + 补母 mod 4 条（`Fujiwara_Mokou_government_reform` / `NMK_solitary_dweller` / `NMK_Eternal_Flame` / `NMK_Beyond_life_and_death`） |

---

## 三、设计取舍（为什么不用母 mod 的 acgr 兵种）

母 mod 已给 36 国分配 `unit_type`：g01 × 30（妖怪突击/天狗骑射系）、g02 × 5（月兔系 EIR/KGY/RES/WNT/WNY）、g09 × 1（SKR 樱系）。本 submod 仍选择保留自己的 72 个 `gen_t*` 兵种，理由：

1. **acgr 36 组里 `artillery = 0`** —— 母 mod 靠 57 门无 `unit_type` 的通用炮兵。我方 27 门炮（占 72 兵种的 37%）在母 mod 体系里没有落点，并入等于直接丢失。
2. 母 mod 把 36 国兵种切成 g01 / g02 / g09 三套，月兔系与樱系失去与本 submod 主体一致的差异化。
3. `unit_type` 与 `technology_group` 是**正交的两个轴**（`wiki 历史修改` + 原版 `ABB - Dongola.txt:7-8` 的 `technology_group = east_african` + `unit_type = sub_saharan`）。不写 `unit_type` 时兵种由 `technology_group` 推导，因此保留 `tech_gensokyan` 即可稳定使用 `gen_t*`。
4. 取舍代价：36 国用不到母 mod 的 acgr 兵种数值/外观；母 mod 每次更新需重跑 `technology.txt` + `mil.txt` 两处合并（约 20 分钟，已有固定插入锚点注释）。

---

## 四、尚未完成（下一轮）

| 项 | 内容 |
|---|---|
| `common/diplomatic_actions/00_diplomatic_actions.txt` | 我方 91 行定制（禁结盟 / 魔力宝石）在，但母 mod 新增的 50 行（NMK 破产/孤立机制、`kirara_queue_global_war_check_effect`）尚未按 action 块补入 |
| `common/ideas/00_basic_ideas.txt` | 我方 2,155 行 vs 母 mod 2,019 行，1,120 行差异待分块判定 |
| `common/ideas/new_countries_ideas.txt` | 380 行差异（PT 版这处合并正确，可参考） |
| `common/estate_privileges/kirara_privileges.txt` / `common/static_modifiers/acg_modifiers.txt` | 38 行 / 34 行差异 |
| `decisions/IYS_decisions.txt` / `missions/IYS_missions.txt` | 6 行 / 4 行（我方门槛 0.8/95、`duration 7300`、`kirara_check_sek_aid_effect` 调用） |
| 游戏内验证 | 1444 开局 → `logs/error.log` 无 unknown unit_type / unknown technology group → 36 国冒烟（HKR / EIR / SKR）→ 首都交叉校验 |

---

## 五、验证数据

| 校验项 | 期望 | 实测 |
|---|---|---|
| `technology.txt` 组数 | 56 | **56** ✓ |
| `mil.txt` enable 条数 | 1,865 | **1,865** ✓ |
| enable 悬空（对账 WS+母 mod+原版） | 0 | **0** ✓ |
| 用 `tech_gensokyan` 的国家 | 36 | **36** ✓ |
| 残留 `unit_type`（国家层） | 0 | **0** ✓ |
| 含 `discovered_by = tech_gensokyan` 的省 | 1,897 | **1,897** ✓ |
| `ACGR_missions.txt` 有效行 | 0 | **0** ✓ |
| 同 TAG 重复国家文件 | 0 | **0** ✓ |

---

## 六、已知风险

- `culture = ShiraiKuroko`（5 省）在 vanilla / 母 mod / submod 三处 `common/cultures` 均无定义，本次已随母 mod 改为 `supperability_magic_culture`。
- 母 mod 的 681 / 2171 / 2172 `capital` 为坏编码乱码，合并时按可读名回填，仍需游戏内确认显示。
- `MOD/decisions/KGYdecision.txt:298-307` 会对 KGY 及全部附庸执行 `change_technology_group = western`，本 submod 为 0 处反向效果 —— 既有风险，非本次引入。
- 旧版母 mod 不可得，故 `00_basic_ideas` / `diplomatic_actions` / `kirara_privileges` 无法把「我方定制」与「旧母 mod 内容」完全分离，只能按块判断。
