# 提瓦特宗教组施工计划

- 项目：ACG_MEC_E（ACG佣兵拓展）
- 目标版本：EU4 1.37.5 / 母 Mod ACG1（ugc_2796854877）
- 文档状态：待批准（v2：键值前缀、2 条/3 条修正、2 决议 2 事件、冰神定名瓦沙嘉）
- 最后更新：2026-11-19

---

## 一、范围

| 项 | 内容 |
|---|---|
| 新宗教组 | `acg_mec_e_teyvat_group`（提瓦特） |
| 新宗教 | `acg_mec_e_seven_archons`（七神信仰）、`acg_mec_e_moon_goddess`（月神信仰） |
| 机制 | 两个宗教都开 `personal_deity = yes`（印度教/诺斯同款主神系统） |
| 主神 | 七神 7 位、三月 3 位，共 10 位，各自可选其一 |
| 主神强度 | 七神每位 **2 条**修正、三月每位 **3 条**修正（慷慨档） |
| 换神交互 | **2 个决议 + 2 个事件**（决议开面板，事件里点选项选神） |
| 宗教图标 | **不新增**，复用现有帧占位（34 / 35） |
| 主神图标 | 新增 10 帧，由你提供的 PNG 裁剪生成 |
| 键值前缀 | 全部加 `acg_mec_e_`，避免与母 Mod、原版撞名 |

---

## 二、实测底牌（实测数据，非推测）

| 项目 | 结果 |
|---|---|
| 贴图格式 | 全部 **未压缩 A8R8G8B8（RGBA8）**，非 DXT5 |
| 原版 `hindu_deities_strip.dds` | 492×41，12 帧（单帧 41×41），mips 1，pitch 1968 |
| 母 Mod `hindu_deities_strip.dds` | **738×41，18 帧**（单帧 41×41），mips 10，pitch 121032 —— 母 Mod 已扩出 6 帧（sprite 13–18） |
| 母 Mod sprite 定义 | `countryreligionview.gfx` 写 12 帧、`newcountryreligionview.gfx` 写 18 帧（同名跨文件定义，后加载者生效） |
| 母 Mod `icon_religion.dds` | 3072×64，48 帧（单帧 64×64），mips 12 |
| 母 Mod `icon_religion_small.dds` | 1536×32，48 帧（单帧 32×32） |
| Pillow 能力 | 可读上述 dds，**不可写 dds** → 需手写 128 字节头 |
| 主神帧号占用 | 1–6 Hindu、7–12 诺斯、13–18 母 Mod 预留 → 本次用 **19–28** |
| 换神脚本入口 | `change_personal_deity = <deity>`（country 作用域，直接在事件 option 内写）；判定 `has_personal_deity = <deity>` |
| 事件 option 支持 `trigger` | 原版有 1644 处实例，可用来隐藏「当前已信奉」的选项 |
| 主神机制 DLC 门槛 | 原版主神事件要求 `has_dlc = "Wealth of Nations"` |
| 源图 | 7 元素 128×128 RGBA；三月 763×763 RGBA；`七元素.png` 带「豆包AI生成」水印，不参与裁切 |

---

## 三、命名规范

统一前缀 `acg_mec_e_`，不允许裸名。

| 类型 | 规则 | 示例 |
|---|---|---|
| 宗教组 | `acg_mec_e_<name>_group` | `acg_mec_e_teyvat_group` |
| 宗教 | `acg_mec_e_<name>` | `acg_mec_e_seven_archons` |
| 主神 | `acg_mec_e_deity_<name>` | `acg_mec_e_deity_morax` |
| 国家修正 | `acg_mec_e_<name>_modifier` | `acg_mec_e_rechoose_deity_cd` |
| 决议 | `acg_mec_e_<name>` | `acg_mec_e_rechoose_seven_archon` |
| 事件命名空间 | `acg_mec_e_teyvat_religion` | `acg_mec_e_teyvat_religion.1` |
| 贴图 | `acg_mec_e_<name>.dds` | `acg_mec_e_deities_strip.dds` |
| 本地化 | 与脚本 key 完全一致 | `acg_mec_e_seven_archons_rebels_demand` |

宗教级派生 key（必须成套）：

```
<religion>_rebels_demand
<religion>_rebels_demand_desc
<religion>_rebels_title
<religion>_rebels_name
<religion>_rebels_desc
<religion>_rebels_army
```

---

## 四、宗教组定义

文件：`common/religions/00_acg_mec_e_teyvat_religion.txt`（新建独立文件，不复制 `00_religion.txt`）

```
acg_mec_e_teyvat_group = {
	defender_of_faith = yes
	flags_with_emblem_percentage = 33
	flag_emblem_index_range = { 1 57 }
	crusade_name = HOLY_WAR

	acg_mec_e_seven_archons = {
		color = { 210 180 90 }
		icon = 34
		allowed_conversion = { acg_mec_e_moon_goddess }

		country = {
			tolerance_heretic = 2
			global_unrest = -1
			land_morale = 0.05
		}
		country_as_secondary = {
			idea_cost = -0.05
			global_institution_spread = 0.05
		}
		province = {
			local_missionary_strength = -0.02
		}

		heretic = { ACG_MEC_E_SEVEN_HERETIC ACG_MEC_E_ABYSS_ORDER }
		personal_deity = yes

		on_convert = {
			change_religion = acg_mec_e_seven_archons
			add_prestige = -50
		}
	}

	acg_mec_e_moon_goddess = {
		color = { 120 140 220 }
		icon = 35
		allowed_conversion = { acg_mec_e_seven_archons }

		country = {
			tolerance_own = 2
			advisor_pool = 1
			spy_offence = 0.15
			prestige = 0.5
		}
		country_as_secondary = {
			diplomatic_reputation = 1
			global_unrest = -1
		}
		province = {
			local_missionary_strength = 0.02
		}

		heretic = { ACG_MEC_E_MOON_HERETIC }
		personal_deity = yes

		on_convert = {
			change_religion = acg_mec_e_moon_goddess
			add_prestige = -50
		}
	}
}
```

> `icon = 34 / 35` 为母 Mod 已存在的图标帧（`acg`、`JianNiang`），宗教图标本轮不新增，先占位。

### 4.1 `heretic` 字段是什么

`heretic = { A B C }` 写的是**该宗教内部的异端派别名池**，不是新宗教、不是可选项、不参与宗教转换。

它的实际用途：

| 用途 | 说明 |
|---|---|
| 异端叛军命名 | 省份爆发异端叛军时，从池里取名字生成叛军类型名与提示文本 |
| 宗教界面文本 | 宗教详情里"异端"一栏的显示内容 |
| 相关事件/修正 | 异端派别出现、宗教迫害等事件引用这些名字 |
| 硬性要求 | 每位宗教至少要有一个，缺省会造成显示与日志异常 |

池里每个大写串都是本地化 key，必须给中文，否则界面显示裸 key。

本方案取值：

| key | 中文 | 设定含义 |
|---|---|---|
| `ACG_MEC_E_SEVEN_HERETIC` | 无信者 | 拒绝承认七神、也不投深渊的世俗派别 |
| `ACG_MEC_E_ABYSS_ORDER` | 深渊教团 | 崇拜深渊、与七神为敌的教团 |
| `ACG_MEC_E_MOON_HERETIC` | 伪月信徒 | 自称侍奉三月、实为篡改月相的教派 |

---

## 五、十个主神

文件：`common/personal_deities/00_acg_mec_e_deities.txt`

### 5.1 七神（每位 2 条）

| # | sprite | key | 神 | 元素 | 修正 |
|---|---|---|---|---|---|
| 1 | 19 | `acg_mec_e_deity_barbatos` | 巴巴托斯 | 风 | `land_morale = 0.10`、`land_attrition = -0.15` |
| 2 | 20 | `acg_mec_e_deity_morax` | 摩拉克斯 | 岩 | `defensiveness = 0.25`、`fort_maintenance_modifier = -0.15` |
| 3 | 21 | `acg_mec_e_deity_baal` | 巴尔 | 雷 | `discipline = 0.05`、`shock_damage = 0.10` |
| 4 | 22 | `acg_mec_e_deity_buer` | 布耶尔 | 草 | `development_cost = -0.10`、`global_institution_spread = 0.10` |
| 5 | 23 | `acg_mec_e_deity_focalors` | 芙卡洛斯 | 水 | `trade_efficiency = 0.10`、`global_tax_modifier = 0.05` |
| 6 | 24 | `acg_mec_e_deity_mavuika` | 玛薇卡 | 火 | `fire_damage = 0.10`、`manpower_recovery_speed = 0.15` |
| 7 | 25 | `acg_mec_e_deity_washajia` | 瓦沙嘉 | 冰 | `global_unrest = -2`、`defensiveness = 0.15` |

### 5.2 三月（每位 3 条）

| # | sprite | key | 神 | 修正 |
|---|---|---|---|---|
| 8 | 26 | `acg_mec_e_deity_hengyue` | 恒月 | `tolerance_own = 2`、`prestige = 1`、`stability_cost_modifier = -0.10` |
| 9 | 27 | `acg_mec_e_deity_hongyue` | 虹月 | `global_tax_modifier = 0.10`、`production_efficiency = 0.10`、`trade_efficiency = 0.10` |
| 10 | 28 | `acg_mec_e_deity_shuangyue` | 霜月 | `discipline = 0.05`、`defensiveness = 0.20`、`manpower_recovery_speed = 0.15` |

### 5.3 代码形态

```
acg_mec_e_deity_morax = {
	sprite = 20
	potential = { religion = acg_mec_e_seven_archons }
	trigger = {}

	defensiveness = 0.25
	fort_maintenance_modifier = -0.15

	effect = {}
	removed_effect = {}
	ai_will_do = {
		factor = 1
		modifier = { factor = 2 personality = ai_militarist }
		modifier = { factor = 0.5 personality = ai_diplomat }
	}
}
```

- 修正写在条目顶层（country 作用域），全国生效；
- `potential` 决定归属宗教，七神的神不会出现在月神国家的列表里；
- `sprite` 必须用新帧（19–28）；
- `effect` / `removed_effect` 留空，留作后续事件钩子。

---

## 六、换神：2 个决议 + 2 个事件

流程：**决议（检查冷却、触发事件）→ 事件（列出可选的神，点一个即切换）**。

### 6.1 决议

文件：`decisions/acg_mec_e_teyvat_religion_decisions.txt`

```
acg_mec_e_rechoose_seven_archon = {
	potential = { religion = acg_mec_e_seven_archons }
	allow = {
		NOT = { has_regency = yes }
		NOT = { has_country_modifier = acg_mec_e_rechoose_deity_cd }
	}
	effect = {
		country_event = { id = acg_mec_e_teyvat_religion.1 }
	}
	ai_will_do = { factor = 0 }
}

acg_mec_e_rechoose_moon = {
	potential = { religion = acg_mec_e_moon_goddess }
	allow = {
		NOT = { has_regency = yes }
		NOT = { has_country_modifier = acg_mec_e_rechoose_deity_cd }
	}
	effect = {
		country_event = { id = acg_mec_e_teyvat_religion.2 }
	}
	ai_will_do = { factor = 0 }
}
```

### 6.2 事件

文件：`events/acg_mec_e_teyvat_religion_events.txt`

```
namespace = acg_mec_e_teyvat_religion

country_event = {
	id = acg_mec_e_teyvat_religion.1
	title = acg_mec_e_teyvat_religion.1.t
	desc = acg_mec_e_teyvat_religion.1.d
	picture = PRAYING_eventPicture
	is_triggered_only = yes

	immediate = {
		add_country_modifier = { name = acg_mec_e_rechoose_deity_cd duration = 7300 }
		reduce_legitimacy_large_effect = yes
	}

	option = {	# 巴巴托斯
		name = acg_mec_e_teyvat_religion.1.a
		trigger = { NOT = { has_personal_deity = acg_mec_e_deity_barbatos } }
		change_personal_deity = acg_mec_e_deity_barbatos
	}

	option = {	# 摩拉克斯
		name = acg_mec_e_teyvat_religion.1.b
		trigger = { NOT = { has_personal_deity = acg_mec_e_deity_morax } }
		change_personal_deity = acg_mec_e_deity_morax
	}

	# 其余 5 位同构（baal / buer / focalors / mavuika / washajia，
	# 选项 key 依次为 .1.c ~ .1.g）
}
```

```
country_event = {
	id = acg_mec_e_teyvat_religion.2
	title = acg_mec_e_teyvat_religion.2.t
	desc = acg_mec_e_teyvat_religion.2.d
	picture = PRAYING_eventPicture
	is_triggered_only = yes

	immediate = {
		add_country_modifier = { name = acg_mec_e_rechoose_deity_cd duration = 7300 }
		reduce_legitimacy_large_effect = yes
	}

	option = {	# 恒月
		name = acg_mec_e_teyvat_religion.2.a
		trigger = { NOT = { has_personal_deity = acg_mec_e_deity_hengyue } }
		change_personal_deity = acg_mec_e_deity_hengyue
	}

	option = {	# 虹月
		name = acg_mec_e_teyvat_religion.2.b
		trigger = { NOT = { has_personal_deity = acg_mec_e_deity_hongyue } }
		change_personal_deity = acg_mec_e_deity_hongyue
	}

	option = {	# 霜月
		name = acg_mec_e_teyvat_religion.2.c
		trigger = { NOT = { has_personal_deity = acg_mec_e_deity_shuangyue } }
		change_personal_deity = acg_mec_e_deity_shuangyue
	}
}
```

要点：

- 冷却与正统性放在 `immediate`，玩家点任何选项都会生效一次；
- 每个 option 带 `trigger`，当前已信奉的那位不会显示（原版 1644 处实例证明该写法可用）；
- 首次选神仍由宗教面板自带按钮完成，决议只负责「换」；
- 冷却 20 年（7300 天），事件触发即计冷却，避免反复开关。

---

## 七、本地化清单

文件：`decode_localisation/acg_teyvat_l_english.yml`（**追加进已有文件**，明文，由你手动编码进 `localisation/`）

| key | 内容 |
|---|---|
| `acg_mec_e_teyvat_group` | 提瓦特 |
| `acg_mec_e_seven_archons` | 七神信仰 |
| `acg_mec_e_moon_goddess` | 月神信仰 |
| `ACG_MEC_E_SEVEN_HERETIC` | 无信者 |
| `ACG_MEC_E_ABYSS_ORDER` | 深渊教团 |
| `ACG_MEC_E_MOON_HERETIC` | 伪月信徒 |
| `acg_mec_e_deity_barbatos` / `_morax` / `_baal` / `_buer` / `_focalors` / `_mavuika` / `_washajia` | 巴巴托斯 / 摩拉克斯 / 巴尔 / 布耶尔 / 芙卡洛斯 / 玛薇卡 / 瓦沙嘉 |
| `acg_mec_e_deity_hengyue` / `_hongyue` / `_shuangyue` | 恒月 / 虹月 / 霜月 |
| 每位神配 `desc_<key>` | 一句神谕式描述 |
| `acg_mec_e_rechoose_seven_archon` / `acg_mec_e_rechoose_moon` | 重择神明 / 重择月相 |
| `acg_mec_e_teyvat_religion.1.t` / `.1.d` | 事件标题与描述（七神） |
| `acg_mec_e_teyvat_religion.2.t` / `.2.d` | 事件标题与描述（三月） |
| `acg_mec_e_teyvat_religion.1.a` ~ `.1.g` | 七个选项名 |
| `acg_mec_e_teyvat_religion.2.a` ~ `.2.c` | 三个选项名 |
| 两套 `*_rebels_demand` / `_demand_desc` / `_title` / `_name` / `_desc` / `_army` | 各 6 条，共 12 条 |

---

## 八、图标流水线

### 8.1 只扩主神条

| 项 | 值 |
|---|---|
| 基底 | 母 Mod `gfx/interface/hindu_deities_strip.dds`（738×41，18 帧） |
| 输出 | `gfx/interface/hindu_deities_strip.dds`（**同名覆盖**原版/母 Mod 路径，**1148×41，28 帧**） |
| 单帧 | 41×41（保持不变） |
| 新增帧位 | 19–28 |
| 格式 | 未压缩 A8R8G8B8，header 以母 Mod 文件为模板，仅替换宽高/pitch/帧数 |
| mipmap | 按母 Mod 风格生成 2 倍递减链 |

### 8.2 裁切规则

1. 取 alpha > 4 的包围盒，去掉四周空白；
2. 以最长边做正方形外扩，居中，不拉伸；
3. LANCZOS 缩放到 41×41；
4. 边缘 alpha 做 1px 收边，避免白边；
5. 输出到 `analysis/teyvat_icons/` 供预览，同时拼进帧图。

源图对应：

| sprite | 源文件 |
|---|---|
| 19 巴巴托斯（风） | `七元素切图_128\透明底_增强+\风.png` |
| 20 摩拉克斯（岩） | `...\岩.png` |
| 21 巴尔（雷） | `...\雷.png` |
| 22 布耶尔（草） | `...\草.png` |
| 23 芙卡洛斯（水） | `...\水.png` |
| 24 玛薇卡（火） | `...\火.png` |
| 25 瓦沙嘉（冰） | `...\冰.png` |
| 26 恒月 | `恒月.png` |
| 27 虹月 | `虹月.png` |
| 28 霜月 | `霜月.png` |

### 8.3 sprite 定义

新建 `interface/zzz_acg_mec_e_religion.gfx`，只重定义一条：

```
spriteType = {
	name = "GFX_hindu_deities_strip"
	texturefile = "gfx//interface//hindu_deities_strip.dds"
	noOfFrames = 28
}
```

母 Mod 里这条 sprite 已被定义两次（12 帧 / 18 帧），说明同名跨文件定义允许；本文件用 `zzz_` 前缀保证字母序最后加载。

**回退方案**：若进游戏发现帧仍按 18 切（图标串位），改为复制母 Mod 的 `newcountryreligionview.gfx` 到本 Mod 并只把 `noOfFrames = 18` 改为 `28`。

### 8.4 校验

1. 写完 dds 用 Pillow 回读，确认尺寸 = 1148×41；
2. 逐帧与裁切后的 41×41 PNG 做像素差，阈值 2/255；
3. 导出带网格和帧号的预览图，人工确认后再进游戏。

---

## 九、文件清单

| # | 路径 | 动作 |
|---|---|---|
| 1 | `common/religions/00_acg_mec_e_teyvat_religion.txt` | 新建 |
| 2 | `common/personal_deities/00_acg_mec_e_deities.txt` | 新建（目录不存在则建） |
| 3 | `decisions/acg_mec_e_teyvat_religion_decisions.txt` | 新建（2 条决议） |
| 4 | `events/acg_mec_e_teyvat_religion_events.txt` | 新建（2 个事件） |
| 5 | `decode_localisation/acg_teyvat_l_english.yml` | 追加（沿用已有文件） |
| 6 | `gfx/interface/hindu_deities_strip.dds` | 生成（同名覆盖，1148×41） |
| 7 | `interface/zzz_acg_mec_e_religion.gfx` | 新建 |
| 8 | `analysis/teyvat_icons/*.png` | 生成的 41×41 预览图 |
| 9 | `analysis/tools/build_teyvat_strip.py` | 可复跑脚本（裁图 + 拼帧 + 校验） |

不改动：`localisation/`（由你编码）、母 Mod 任何文件、原版任何文件。

---

## 十、执行顺序

1. 建目录与 Python 脚本；
2. 裁 10 张 41×41 PNG → 出预览图；
3. 拼帧 → 写 `acg_mec_e_deities_strip.dds` → 回读校验 → 出帧图预览；
4. 写宗教 / 主神 / 决议 / 事件 / 本地化五个文本文件；
5. `validate_script` 校验脚本 → `eu4_verify_path` 校验路径 → `eu4_readback` 回读；
6. 交付清单，你进游戏用 `religion acg_mec_e_seven_archons` 验主神列表。

---

## 十一、验收标准

| 检查点 | 通过标准 |
|---|---|
| 宗教面板 | 出现「提瓦特」组，两个宗教可切换 |
| 主神列表 | 七神国显示 7 位、月神国显示 3 位，图标与名字对应正确 |
| 主神生效 | 选中后国家修正面板出现对应 2 条 / 3 条 |
| 换神链路 | 决议 → 事件 → 选项三步可走；选项不显示当前已信奉的神 |
| 换神代价 | 20 年冷却生效、正统性扣减正确 |
| 异端 | 叛军名与宗教界面显示中文，无裸 key |
| 图标 | 10 帧无串图、无白边、无错位 |
| 日志 | `error.log` 无宗教/主神/事件相关报错 |

---

## 十二、风险与回退

| 风险 | 处理 |
|---|---|
| gfx 加载顺序导致帧数不生效 | 先做加载实验；失败则整份覆盖母 Mod 的 `newcountryreligionview.gfx` |
| 主神机制无 UI（缺 Wealth of Nations） | 需你确认 DLC；无 DLC 则改用 aspects 方案 |
| 帧号越界（19–28 超过 18） | 必须扩图，回读校验尺寸与帧宽 |
| 宗教图标占位（34/35）与母 Mod 图标重复 | 可接受；后续出图再换 |
| 事件选项全被 trigger 隐藏 | 确保选项覆盖全部 7/3 位神，且不写死当前神 |
| 子 Mod 与母 Mod 同时改主神条 | 只改本 Mod 的贴图与 sprite，母 Mod 文件不动 |

---

## 十三、待你确认

1. 本计划是否照此执行；
2. 确认已安装 Wealth of Nations（主神系统 DLC 门槛）；
3. 事件文案与神谕描述由我写中文（如你想要特定口吻，说一声）。
