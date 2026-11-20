# -*- coding: utf-8 -*-
p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()

add = """
### 13.11 理念第四版：数值只走 5% 网格

要求：不许出现 8%、2%、4% 这类尾数，只允许 5 的倍数（5 / 7.5 / 10 / 15 / 20 …）。

**全量数值集合**（去重后只有这 11 个）：
`-1` `-0.10` `-0.05` `0.05` `0.10` `0.15` `0.20` `0.50` `1.00` `50` `100`
—— 换算成百分比即：-100% / -10% / -5% / 5% / 10% / 15% / 20% / 50% / 100% / 50 / 100。逐个校验 `值×100` 均为 5 的整数倍，**全部通过**。

| 国家 | 修正总数 | 唯一 | 重复 | 7 槽条数 | 传统 | 野心 |
|---|---|---|---|---|---|---|
| JZH | 14 | 14 | 0 | 2,1,2,1,1,2,2 | 2 | 1 |
| RGU | 13 | 13 | 0 | 2,1,1,1,2,1,2 | 2 | 1 |
| XJA | 13 | 13 | 0 | 1,1,2,2,1,1,2 | 2 | 1 |
| MGZ | 15 | 15 | 0 | 2,2,2,2,2,1,1 | 2 | 1 |
| CXT | 14 | 14 | 0 | 2,1,2,1,2,2,1 | 2 | 1 |
| FGL | 13 | 13 | 0 | 2,1,1,2,1,1,2 | 2 | 1 |
| FSL | 12 | 12 | 0 | 1,2,1,2,1,1,1 | 2 | 1 |
| MTL | 13 | 13 | 0 | 1,1,1,2,2,2,1 | 2 | 1 |
| YHH | 14 | 14 | 0 | 2,2,1,2,1,2,1 | 2 | 1 |

非百分比类修正保持整数点：`tolerance_own 1`、`diplomatic_reputation 1`、`global_unrest -1`、`max_hostile_attrition 1`、`governing_capacity 50/100`、`prestige 0.5/1.0`、`navy_tradition_decay -0.05`。

**理念名与描述仍无改动** —— loc 明文依旧 198 key，**不需要重新转码**；本轮只改 `common/ideas/*.txt`（纯 ASCII）。

备份：`analysis/backup_ideas_v4_20261120/`；工具：`analysis/tools/build_ideas_v4.py`；报告：`analysis/_ideas_v4_report.json`。
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
