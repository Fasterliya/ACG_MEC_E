# 如何给一个政体改革挂「立绘进度条」（EU4 1.37.5 实测写法）

> 本包示范对象：ACG_MEC_E 里稗田阿求的政体改革「稗田家史笔」（`ACG_MEC_HNA_chronicle_reform`）。
> 目标效果：进游戏后在**政府界面**看到一张 300×162 的立绘**当作进度条**用——暗版铺底，随 power 增长从左往右被亮版覆盖。

---

## 0. 包里有什么

| 文件 | 作用 |
|---|---|
| `common/government_mechanics/ACG_MEC_HNA_mechanic.txt` | ① mechanic 定义 + 唯一一条 power（数值口径：max=100、每月 +1） |
| `interface/government_mechanics/ACG_MEC_HNA_mechanic.gfx` | ② 贴图绑定：`progressbartype`（满图/空图）+ 外框 `spriteType` |
| `interface/government_mechanics/ACG_MEC_HNA_mechanic.gui` | ③ 界面：窗口 + `government_power_bar` 控件 + 透明外框控件 |
| `gfx/interface/government_mechanics/ACG_MEC_HNA/*.dds` | ④ 三张贴图：满图（进度）、空图（底）、外框（当前全透明占位） |
| `common/government_reforms/ACG_MEC_HNA_reforms.txt` | ⑤ 授权：改革里加 `government_abilities = { <mechanic_id> }`（**旧文件，只有末尾 3 行是新增**） |
| `decode_localisation/ACG_MEC_HNA_l_english.yml` | ⑥ 本地化 6 个 key（**旧文件，只有末尾是新增**，值留空待填） |
| `02_changes_since_last_commit.diff` | 上面两个旧文件的**精确改动面**（git diff，便于对照最小改动） |

---

## 1. 原理（一句话讲清）

EU4 的 `common/government_mechanics/*.txt` 里，一个 mechanic 可以带 1..n 条 **power**（进度条）。给这条 power 写上 `gui = <窗口名>`，窗口里放一个**名字必须叫 `government_power_bar`** 的控件，引擎就会把这条 power 的百分比灌进这个控件；控件背后是一个 `progressbartype`，它**按 x 坐标在两张贴图之间切**：

```hlsl
// gfx/FX/progress.shader:95
return v.vTexCoord0.x <= CurrentState ? tex2D( TextureOne, … ) : tex2D( TextureTwo, … );
```

- `textureFile1`（TextureOne）= **已完成进度**那一段 → 放「满图（亮版）」
- `textureFile2`（TextureTwo）= **尚未进度**那一段 → 放「空图（暗版）」
- 顺带：`color / colortwo` 只在 `PixelColor` 分支用（`progress.shader:99-105`），**不会给贴图染色**；混合是 `SRC_ALPHA/INV_SRC_ALPHA + AlphaTest`（`:127-133`），所以**全透明外框不会挡住立绘**。

---

## 2. 五步照抄

### ① 放图

```
gfx/interface/government_mechanics/<你的目录>/
    xxx_full.dds     ← 亮版（进度段）
    xxx_empty.dds    ← 暗版（底）
    xxx_frame.dds    ← 外框（可以先做成同尺寸全透明占位）
```

规格：**300×162、32bpp 未压缩 BGRA 的 DDS**（带 mip 链无害，`progress.shader` 里 `MipFilter = None`，不会采样 mip）。
外框图可以直接用同尺寸全透明图（本包 `ACG_MEC_HNA_chronicle_frame.dds` 就是：复用源图 128 字节 DDS 头 + 像素数据全 0），以后想加边框直接覆盖这个文件即可，不用改任何脚本。

### ② 贴图绑定 `.gfx`（`interface/government_mechanics/xxx.gfx`）

```
spriteTypes = {

	progressbartype = {
		name = "GFX_xxx_bar"
		color = { 1.0 1.0 1.0 }
		colortwo = { 1.0 1.0 1.0 }
		textureFile1 = "gfx/interface/government_mechanics/<你的目录>/xxx_full.dds"
		textureFile2 = "gfx/interface/government_mechanics/<你的目录>/xxx_empty.dds"
		size = { x = 300 y = 162 }
		effectFile = "gfx/FX/progress.lua"
	}

	spriteType = {
		name = "GFX_xxx_frame"
		texturefile = "gfx/interface/government_mechanics/<你的目录>/xxx_frame.dds"
		loadType = "INGAME"
		transparencecheck = yes
	}
}
```

蓝本：原版 `interface/government_mechanics/government_mechanics.gfx:1`（`spriteTypes` 包裹）、`:184-199`（外框 + 大图进度条，奥斯曼腐败条 274×110）。

### ③ 界面 `.gui`（`interface/government_mechanics/xxx.gui`）

```
guiTypes = {
	windowType = {
		name = "xxx_gov_mech"
		backGround = ""
		position = { x = 0 y = 0 }
		size = { x = 300 y = 162 }
		moveable = 0
		dontRender = ""
		horizontalBorder = ""

		iconType = {                     # ← 名字必须是 government_power_bar
			name = "government_power_bar"
			spriteType = "GFX_xxx_bar"
			position = { x = 0 y = 0 }
		}

		iconType = {
			name = "xxx_frame"           # 外框控件名可自取
			spriteType = "GFX_xxx_frame"
			position = { x = 0 y = 0 }
			alwaystransparent = yes
		}
	}
}
```

蓝本：`ottoman_decadence.gui:1-25`、`divine_authority.gui:2-29`。**引擎只认 `government_power_bar` 这个名字**，改成别的名字 → 条永远不会动。

### ④ mechanic + power（`common/government_mechanics/xxx_mechanic.txt`）

```
xxx_mechanic = {
	available = {
		always = yes          # 想卡 DLC 就写 has_dlc = "..."；卡国家请在改革里卡
	}

	powers = {
		xxx_power = {
			gui = xxx_gov_mech          # ← 指向 ③ 的 windowType 名
			min = 0
			max = 100
			default = 0
			reset_on_new_ruler = no
			base_monthly_growth = 1     # 每月 +1（先占位，之后可换真数值）
			increases_with_global = no
			is_good = yes
		}
	}
}
```

字段全表见原版自带说明 `common/government_mechanics/readme.txt`（`:8-13`、`:38`）；
要让它产生效果，在 power 里加 `scaled_modifier / range_modifier / reverse_scaled_modifier`（`readme.txt:16-35`），
要从脚本加/减数值用 `add_government_power / set_government_power`（`readme.txt:47-49`）：

```
add_government_power = {
	mechanic_type = xxx_mechanic
	power_type   = xxx_power
	value        = 10
}
```

### ⑤ 授权 + 本地化

**授权**（关键的一步，写在**政体改革**文件里，不是在 mechanic 文件里）：

```
# common/government_reforms/<你的改革>.txt
your_reform = {
	...
	government_abilities = {
		xxx_mechanic
	}
}
```

依据：`common/government_mechanics/readme.txt:1`「The ID of the government mechanic which is used by the **government_abilities** in the gov reform files」；原版 71 处实例，如 `common/government_reforms/01_government_reforms_monarchies.txt:1039`。
好处：**换掉改革 = 自动失去 mechanic = 条自动消失**，不需要额外的 flag 维护。

**本地化** 6 个 key（少一个悬停就会显示原始 key）：

| key | 显示在哪 |
|---|---|
| `<power_id>` | 条名 |
| `<power_id>_desc` | 条说明（悬停正文） |
| `monthly_<power_id>` | 「每月变化」类修正名 |
| `<power_id>_gain_modifier` | 「增益」类修正名 |
| `ability_<mechanic_id>` | mechanic 名（原版口径） |
| `<mechanic_id>` | mechanic id 本身（可选） |

原版证据：`localisation/domination_l_english.yml:2576-2578`、`localisation/winds_of_change_l_english.yml:3907-3911`。

---

## 3. 三个坑（都踩过，附日志证据）

1. **`.gfx` 必须用 `spriteTypes = { … }` 包裹。**
   直接把 `spriteType = {` 写在文件开头 → `error.log` 报
   `Parsing Error. File: "interface/…/xxx.gfx", Error: Unexpected token: spriteType, near line: 1`
   → **里面的贴图一个都不会加载**（本次排错时在旧文件上真实撞到）。
2. **`on_action` 体里直接写效果，不要套 `effect = { … }`。**
   正确形态见原版 `common/on_actions/00_on_actions.txt:475-500`（`on_battle_won_country` 里直接写 `xxx_effect = yes`、`if = { limit = {…} … }`）；
   套了外壳会报 `Unknown effect type. Key: effect: effect`，**整个钩子静默失效**且不报错中断（本次也在日志里抓到）。
3. **贴图路径必须真实存在。** 否则每次启动往 `error.log` 刷
   `Texture Handler encountered missing texture file: …` / `Couldn't find texture file: …`（一行一张，几万行刷屏）。

---

## 4. 验证清单

1. 看日志：`…\Europa Universalis IV\logs\error.log`（游戏每次启动会重建这个文件）。
   搜自己的文件名 → 没有 `Parsing Error` / `missing texture` 才算加载成功。
2. 进游戏 → 该国持有该改革 → **政府界面**应出现立绘条。
   - 开局是空的（只有暗版）；`base_monthly_growth = 1` 时每月 +1，100 个月满。
   - 若是读旧存档、条没出现：把政体改革切走再切回来（让 `government_abilities` 重新授予一次）。
3. 悬停条显示原始 key 而不是文字 → 本地化文件没生效（本包 `decode_localisation/` 里是明文源，需要按本项目的编码流程转成 `localisation/` 下的文件）。

---

## 5. 本写法的最小改动面（给评审用）

新增 6 个文件 + 改 2 个已存在文件（只在**文件末尾追加**）：

- `common/government_reforms/ACG_MEC_HNA_reforms.txt`：末尾加 `government_abilities = { ACG_MEC_HNA_chronicle_mechanic }`
- `decode_localisation/ACG_MEC_HNA_l_english.yml`：末尾加 6 个本地化 key

精确 diff 见包内 `02_changes_since_last_commit.diff`。
