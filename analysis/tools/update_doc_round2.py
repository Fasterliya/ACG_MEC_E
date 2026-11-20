# -*- coding: utf-8 -*-
import re

p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()
t = t.replace('LGN', 'RGU')
t = t.replace('| XJA 星炬学院 | 2687 | 624, 625, 680, 2687, 2688, 4790, 4791 | 7 |',
              '| XJA 星炬学院 | 2687 | 624, 625, 630, 2687, 2688, 4790, 4791 | 7 |')

add = """
---

## 13. 第二轮修正记录（2026-11-20）

### 13.1 Tag 变更：LGN -> RGU

`LGN` 与母 mod `ACG1` 冲突 —— 证据：`ACG1\\events\\flavorAOG.txt:277` 用 `break_union = LGN` / `create_union = LGN`（把 LGN 当联合 tag），`ACG1\\localisation\\Acg_countries_l_english.yml:216` 已有 `LGN:` / `LGN_ADJ:` 的本地化。它是 ACG1 里一个没有 country_tags 定义的"孤儿 tag"，占用同名会被 AOG 事件与本地化互相污染。

已整体改名 **LGN -> RGU**（全库 0 命中的候选），涉及：
- `common/country_tags/ACG_MEC_E_country_tag.txt`
- `common/ideas/RGU_ideas.txt`（文件名 + `RGU_ideas` / `RGU_idea_1..7` / `tag = RGU`）
- `history/countries/RGU - Ragunna.txt`
- `decode_localisation/history_wuwa9/history_countries/RGU - Ragunna.txt`
- `decode_localisation/acg_wuthering_nine_l_english.yml`（22 个 key + 1 处分组注释）
- 拉古那 7 个省文件（621/622/623/2678/2679/2680/4818）

**注意**：`localisation/acg_wuthering_nine_l_english.yml` 里已经转码的 `LGN_*` 旧 key 还在，需要按新明文重新转码一次（旧 key 不报错，只是没被引用，界面会回落成原始 key）。

### 13.2 省份调整

| 省 | 操作 | 结果 |
|---|---|---|
| 630 Kalapa | SUN -> **XJA**（连文化一起转 `acg_wuthering_waves`） | 星炬学院补齐 7 省 |
| 680 Chongqing | **还原给 HMC**（从第一轮备份整份恢复） | `acg_hongmao` / `confucianism` / `add_core = HMC` |
| 4804 Kuching | BEI -> **BLS** | 文化保持 `bornean`，宗教 `acg` |
| 4802 / 4803 / 640 | SMB -> **BLS** | 文化保持 `bornean`，宗教 `acg` |
| 636 / 2704 / 2705 / 4805 / 4806 | BLS 原有 5 省 | 宗教统一改 `acg` |

**BLS 现有 9 省**：636, 640, 2704, 2705, 4802, 4803, 4804, 4805, 4806 —— 全部 `religion = acg`（已核）。

### 13.3 旧主连锁变化

| Tag | 变化 | 处理 |
|---|---|---|
| HMC 虹猫 | 收回 680 重庆，现有 5 省（680/681/2171/2172/4211） | `capital` 从 681 改回 **680** |
| SUN 巽他 | 唯一省 630 划给 XJA -> 无地 | 删 `capital` |
| BEI 文莱 | 唯一省 4804 划给 BLS -> 无地 | 删 `capital` |
| SMB 三发 | 3 省（4802/4803/640）全划给 BLS -> 无地 | 删 `capital` |

至此全失地国家共 **18 个**：MAJ / MLC / PSA / BNJ / BEU / KUT / PLB / PGR / DLI / IND / BRS / PAH / SUL / BAN / BLM / SUN / BEI / SMB。

### 13.4 校验

- 九国省数：JZH 10 / **RGU 7** / XJA 7 / MGZ 8 / CXT 5 / FGL 7 / FSL 5 / MTL 5 / YHH 11 = 65
- 全库（除 `localisation/` 成品、备份、文档）已无 `LGN` 残留
- 10 个省文件括号平衡、顶层 `owner` 唯一、日期块归属/宗教残留全清
- 备份：`analysis/backup_round2_20261120/`
- 工具：`analysis/tools/fix_round2.py`（结构）、`fix_round2b.py`（LGN->RGU 正确改名 + 复用前者）
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok bytes=', len(t.encode('utf-8')))
