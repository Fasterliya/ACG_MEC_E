# ALC 任务树架构分析 & acg风云设计指南

> 基于 `F:\Paradox Interactive\Europa Universalis IV\mod\Touhou-Universalis-Expanded-CN-\missions` 的深度分析

---

## 一、槽位布局约定

| 槽位 | 用途 | 说明 |
|------|------|------|
| **Slot 1-5** | 通用任务 / 原版任务 | 由 `generic = yes` 的文化组/区域通用任务占据 |
| **Slot 6-10** | 自定义国家任务 | 本模组国家专用任务树所在位置 |
| **Slot 11+** | 扩展（极少用） | 仅在 SHI 等大型国家中使用，一般不需要 |

> 本 mod (ALC) 当前使用 Slot 6-10，每个 slot 承载一个主题列。

---

## 二、任务树三大架构模式

### 模式 A：纯线性链（推荐——简单国家）

```
Slot 6:  [1] → [2] → [3] → [4] → [5] → [6]
Slot 7:  [1] → [2] → [3] → [4] → [5] → [6]
Slot 8:  [1] → [2] → [3] → [4] → [5]
...
```

- **特征**：每个任务只依赖同列上一级
- **适用**：中小型国家、线性扩张路径
- **代表**：`TFR_Missions.txt`、`TH_Generic_Missions.txt`

```
required_missions = { ALC_missions_6_1 }   # 只依赖同列上一级
```

### 模式 B：中心主干 + 分支收敛（中等复杂度）

```
         [中央主干 3_1]
        /              \
   [Slot 2]          [Slot 4]
   [2_1]→[2_2]       [4_1]→[4_2]
        \              /
     [交叉汇聚 3_4] ← 同时需要 2_2 + 3_3 + 4_2
```

- **特征**：首任务为自动完成(`always = yes`)，后续分展，重要节点汇聚
- **适用**：有剧情线的中等国家
- **代表**：`THE_SEJ_missions.txt`

```txt
THE_SEJ_p0_fallen_arrow = {
    trigger = { always = yes }     # 开局自动完成
}
# 后续分支
THE_SEJ_p0_war_branch = {
    required_missions = { THE_SEJ_p0_fallen_arrow }  # 只依赖主干
}
# 最终汇聚
THE_SEJ_p0_reconciliation_festival = {
    required_missions = {
        THE_SEJ_p0_war_branch
        THE_SEJ_p0_religion_branch
        THE_SEJ_p0_noble_branch
    }
}
```

### 模式 C：标志位分支（复杂——多路径选择）

```
Slot 2:  [选择路径]  ← 触发事件，设置 country_flag
              ↓
    ┌─────────┼─────────┐
    ↓         ↓         ↓
[分支A]    [分支B]    [分支C]
(flag=A)  (flag=B)  (flag=C)
    ↓         ↓         ↓
    └─────────┼─────────┘
              ↓
        [最终汇聚]
```

- **特征**：同一 slot 有多个同名任务树组，通过 `potential` 中的 flag 互斥显示
- **适用**：核心大国、有重大历史抉择的国家
- **代表**：`HVR_Missions.txt`

```txt
# 前置选择（所有支线可见）
hvr_mission_branching_slot_1 = {
    slot = 1
    potential = {
        tag = HVR
        NOT = { has_country_flag = hvr_no_education_flag }
        NOT = { has_country_flag = hvr_teach_lesson_flag }
    }
}

# 分支A（只有选了A才可见）
hvr_mission_no_education_slot_1 = {
    slot = 1
    potential = {
        tag = HVR
        has_country_flag = hvr_no_education_flag
    }
}

# 分支B（只有选了B才可见）
hvr_mission_teach_lesson_slot_1 = {
    slot = 1
    potential = {
        tag = HVR
        has_country_flag = hvr_teach_lesson_flag
    }
}
```

---

## 三、开局任务设计（第一个任务）

### 设计原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **先宣称后征服** | 首任务给永久宣称，不要求已拥有 | `army_size_percentage = 0.9 → 给3个area宣称` |
| **低门槛** | 用军事/经济/外交基础状态而非征服作条件 | `mil_tech = 6`, `monthly_income = 25`, `navy_size_percentage = 0.8` |
| **自动完成** | 剧情引导型首任务设为 `always = yes` | `trigger = { always = yes }` |
| **多入口** | 每列首任务互不依赖，玩家自选方向 | 5列5个独立入口 |

### 开局任务条件类型

| 类型 | 条件 | 给什么 |
|------|------|--------|
| 军事储备 | `army_size_percentage >= 0.9` | 永久宣称 x3 地区 |
| 海军储备 | `navy_size_percentage >= 0.8` | 永久宣称 x3 地区 + 海军传统 |
| 经济起步 | `monthly_income >= 25` | 永久buff |
| 科技积累 | `mil_tech >= 6` | 永久buff + 陆军传统 |
| 基础建设 | `num_of_owned_provinces_with = { has_building = fort_15th value = 5 }` | 永久buff |

---

## 四、宣称授予规范

### 标准格式（推荐）

```txt
effect = {
    apulia_area = {
        add_permanent_claim = ROOT
    }
    calabria_area = {
        add_permanent_claim = ROOT
    }
    naples_area = {
        add_permanent_claim = ROOT
    }
}
```

### 进阶格式（带防重复守卫）

```txt
effect = {
    apulia_area = {
        limit = {
            NOT = { is_core = ROOT }
            NOT = { is_permanent_claim = ROOT }
        }
        add_permanent_claim = ROOT
    }
}
```

### 宣称慷慨度递进

| 阶段 | 范围 | 区域大小 |
|------|------|----------|
| 首任务 | 2-3个 **area** | 本地区周边 |
| 中任务 | 1个**全 region** | 大区域（如 iberia_region） |
| 终任务 | buff为主 | 不再给宣称 |

---

## 五、难度梯度设计

| 层级 | 发展度门槛 | 收入门槛 | 征服条件 | 奖励类型 |
|------|-----------|---------|---------|---------|
| **Tier 1** (开局) | 无 | 20-25 | 无（给宣称）| 宣称 + 小额点数 + 小buff |
| **Tier 2** (初期) | 无 | 无 | 占有1个area | 宣称 + 金币300-500 |
| **Tier 3** (中期) | 400-500 | 50-80 | 占有2个area 或 ≥10省在某region | 宣称(全region) + 金币800-1000 |
| **Tier 4** (后期) | 800-1000 | 150-200 | ≥20省在某region | 永久buff + 大量点数 |
| **Tier 5** (终局) | 1000-1500 | 200+ | + is_great_power / is_hegemon | 终局buff + 所有点数 |

---

## 六、HVR 的分支系统详解（acg风云可参考）

HVR 的任务树是 Touhou mod 中最复杂的，使用 **标志位互斥** 实现玩家选择：

### 工作流程

```
1. 开局 → 玩家看到「前置任务列」(branching_slot)
2. 完成 Choose Path → 触发 flavor_hvr.1 事件
3. 玩家在事件中选择 A/B
4. 事件设置 country_flag（如 hvr_teach_lesson_flag）
5. 下一个月的 potential 重评估 → 旧列隐藏，新列显示
```

### 实现细节

- 每个 slot 需要 **3个任务树组**：前置版（默认可见）、A分支版（flag A可见）、B分支版（flag B可见）
- 分支版用 `has_country_flag` 作 `potential` 条件
- 最终任务将所有分支汇聚 → 要求完成来自多个分支的任务

### 何时使用

- 国家有重大「二元选择」（如宗教路线、政体路线）
- 不同路线带来不同的永久buff和数据
- 2-3条分支即可，不宜过多

---

## 七、Touhou Mod 特有机制总结

| 机制 | 实现方式 | acg风云是否可用 |
|------|---------|:---:|
| 自定义图标 | `mission_touhou_*` 图标 | ❌ 幻想乡特有 |
| 天气/sword系统 | `change_variable` + `has_country_flag` 解锁 | ✅ 可用于自定义机制 |
| 大工程集成 | `has_dlc = "Leviathan"` 分支 + `add_great_project_tier` | ✅ 真实地图更适用 |
| Boss击败追踪 | `has_country_flag` (如 `FOM_defeated_mima`) | ✅ 可改为历史事件 |
| 二阶段任务树 | Phase 0 → Phase 1（开篇 → 正式） | ✅ 适合有转折点的国家 |
| 全球寻宝 | `random_list` 随机目标 + 单位检查 | ⚠️ 复杂、可用作最终任务 |
| 自定义顾问/佣兵 | `define_advisor` / `th_unlock_mercenary_company` | ⚠️ 需配套文件 |
| AI通过条件 | `if = { limit = { ai = yes } ... }` 简化AI完成 | ✅ 强烈推荐 |

---

## 八、acg风云任务树设计建议

### 与 Touhou Mod 的关键区别

| Touhou Mod | acg风云 |
|------------|---------|
| 幻想乡地图（自定义area/region） | **真实世界地图**（原版 area/region） |
| 自定义国家tag（HVR, YOF, TFR...） | **ACG主题tag**（需定义） |
| 幻想世界观（妖怪、弹幕、博丽） | **ACG作品世界观**（跨作品设定） |
| 小范围领土 | **可能跨大陆** |

### 推荐架构

对于 acg风云 的中等国家：

```
模式 A（纯线性）为主
  Slot 6: 征服扩张路线（意大利/地中海）
  Slot 7: 海外殖民/探索路线
  Slot 8: 经济/贸易路线
  Slot 9: 军事/科技路线
  Slot 10: 基建/文化路线
```

对于核心大国：

```
模式 B（中心主干+分支）或 模式 C（flag分支）
  中央剧情线作为开篇
  军事/经济/外交三线并行
  重要节点汇聚
```

### 使用真实地图的优势

1. **area/region 名称标准化**：直接使用原版 `italy_region`、`iberia_region` 等
2. **贸易节点**：`genua`、`venice`、`english_channel` 等标准节点名
3. **省份ID**：原版 province_id 可直接引用
4. **大工程**：真实世界有标准大工程（圣彼得大教堂、凡尔赛宫等）
5. **殖民地**：`colonial_colombia` 等标准殖民区域名称

---

## 九、文件模板（标准国家）

```txt
# =========================
# [国家名] 任务树
# Slot 6: 征服路线
# Slot 7: 外交路线
# Slot 8: 经济路线
# Slot 9: 军事路线
# Slot 10: 基建路线
# =========================

TAG_missions_6 = {
    slot = 6
    generic = no
    ai = yes
    potential = {
        tag = TAG
        NOT = { map_setup = map_setup_random }
    }
    has_country_shield = yes

    TAG_mission_6_1 = {
        icon = mission_xxx
        position = 1
        # 首任务：无依赖，给宣称
        trigger = {
            army_size_percentage = 0.9
        }
        effect = {
            area_name_1 = { add_permanent_claim = ROOT }
            area_name_2 = { add_permanent_claim = ROOT }
            add_army_tradition = 15
            add_mil_power = 50
            add_prestige = 10
        }
    }
    TAG_mission_6_2 = {
        icon = mission_xxx
        position = 2
        required_missions = { TAG_mission_6_1 }
        provinces_to_highlight = {
            area = area_name_1
            NOT = { country_or_non_sovereign_subject_holds = ROOT }
        }
        trigger = {
            area_name_1 = {
                type = all
                country_or_non_sovereign_subject_holds = ROOT
            }
        }
        effect = {
            area_name_3 = { add_permanent_claim = ROOT }
            add_treasury = 300
            add_prestige = 15
        }
    }
    # ... 继续到 position 5-6
}
```

---

## 十、快速检查清单

- [ ] 所有首任务无 `required_missions`
- [ ] 每个任务只依赖同列上一级（无跨列依赖，除非有明确设计意图）
- [ ] 首任务不是征服条件，而是给宣称
- [ ] 宣称范围随任务推进逐步扩大（area → region）
- [ ] 所有 `add_permanent_claim` 使用正确的原版 area/region 名称
- [ ] 奖励规模与任务难度匹配
- [ ] `provinces_to_highlight` 正确指向未拥有省份
- [ ] DLC 相关内容用 `has_dlc` 守卫
- [ ] 最终任务有足够重量级的永久buff
