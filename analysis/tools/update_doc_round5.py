# -*- coding: utf-8 -*-
p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()

add = """
### 13.9 理念第三版：去重 + 降档 + 槽位混合

第三轮反馈：同一国家内不要重复同一个修正、数值降一档、不要每个槽都塞两项。

**做法**
1. **同国去重**：传统 2 + 野心 1 + 7 条理念，全部 modifier 在同一国家内唯一。九国 121 个实例，重复数 **0**。
2. **数值降一档**：约降 20%，例：`land_morale 0.15->0.12`、`discipline 0.05->0.04`、`core_creation -0.15->-0.12`、`naval_forcelimit_modifier 0.25->0.20`、`prestige 1.5->1.0`、`global_unrest -2->-1.5`、`governing_capacity 150->80`。
3. **槽位混合**：7 个槽在 1~2 条之间混排，不再全是 2 条（详见下表）。

| 国家 | 修正总数 | 唯一 | 7 槽条数分布 | 传统 | 野心 |
|---|---|---|---|---|---|
| JZH | 14 | 14 | 2,1,2,1,1,2,2 | 2 | 1 |
| RGU | 13 | 13 | 2,1,1,1,2,1,2 | 2 | 1 |
| XJA | 13 | 13 | 1,1,2,2,1,1,2 | 2 | 1 |
| MGZ | 15 | 15 | 2,2,2,2,2,1,1 | 2 | 1 |
| CXT | 14 | 14 | 2,1,2,1,2,2,1 | 2 | 1 |
| FGL | 13 | 13 | 2,1,1,2,1,1,2 | 2 | 1 |
| FSL | 12 | 12 | 1,2,1,2,1,1,1 | 2 | 1 |
| MTL | 13 | 13 | 1,1,1,2,2,2,1 | 2 | 1 |
| YHH | 14 | 14 | 2,2,1,2,1,2,1 | 2 | 1 |

**理念名与描述没动** —— `decode_localisation/acg_wuthering_nine_l_english.yml` 仍是 198 key，**不需要重新转码**。本轮只改了 `common/ideas/*.txt`（纯 ASCII），进游戏即生效。

备份：`analysis/backup_ideas_v3_20261120/`；工具：`analysis/tools/build_ideas_v3.py`；报告：`analysis/_ideas_v3_report.json`。
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
