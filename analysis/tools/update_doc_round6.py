# -*- coding: utf-8 -*-
p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()

add = """
### 13.10 备份清理（2026-11-20）

中间快照已全部删除（共 9 项 / 120 个文件 / 547.7 KB），`analysis/` 体积 2.33 MB → 1.79 MB：

| 已删除 | 文件数 |
|---|---|
| `analysis/backup_省份_鸣潮九国_20261120/` | 62 |
| `analysis/backup_round2_20261120/` | 25 |
| `analysis/backup_ideas_v2_20261120/` | 10 |
| `analysis/backup_ideas_v3_20261120/` | 9 |
| `analysis/backup_新建国家_鸣潮九国_20261120/` | 10 |
| `analysis/backup_国家_鸣潮九国_20261120/` | 1 |
| `analysis/mod_only.txt` / `ws_only.txt` / `overlap_ws_mod.txt`（全库扫描快照） | 3 |

**保留**（美术素材与工作必需）：
- `analysis/_flag_preview/`（九面旗 PNG + 拼图 + 现有旗对照）
- `analysis/teyvat_icons/`、`analysis/reference/`（图标与科技组条带）
- `analysis/tools/`（15 个脚本，可重放全部改动）
- `analysis/to_encode_20261120/`（待转码 19 份 + 清单）
- `analysis/ui/`（分地台弹窗）
- 5 份 JSON 报告 + 既有分析文档/CSV

> ⚠️ 上文 §12、§13 中提到的 `analysis/backup_*` 路径已随本次清理消失。若要回滚某一处改动：省份基底可从 `ACG1\\history\\provinces` 或原版 `history\\provinces` 取同名文件重建；国家历史同理；具体改动逻辑用 `analysis/tools/` 里的脚本重放（`apply_provinces.py` / `fix_countries.py` / `build_nations.py` / `fix_round2b.py` / `build_ideas_v3.py`）。
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok')
