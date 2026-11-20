# -*- coding: utf-8 -*-
p = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E\新建国家计划_鸣潮九国.md'
t = open(p, encoding='utf-8').read()

old_todo = """1. **转码**：
   - `decode_localisation/history_wuwa9/common_countries/` 9 份明文 → 编码后覆盖到 `common/countries/`
   - `decode_localisation/history_wuwa9/history_countries/` 9 份明文 → 编码后覆盖到 `history/countries/`
   - `decode_localisation/acg_wuthering_nine_l_english.yml` **一份**（198 key，九国全在里面）→ 编码成 `localisation/acg_wuthering_nine_l_english.yml`"""
new_todo = """1. **转码**：全部待转码文件已复制到 **`analysis/to_encode_20261120/`**（19 份 + `_转码清单.md`），直接在那一处统一处理：
   - `common_countries/` 9 份 → 编码后覆盖到 `common/countries/`
   - `history_countries/` 9 份 → 编码后覆盖到 `history/countries/`
   - `localisation/acg_wuthering_nine_l_english.yml` **一份**（198 key）→ 编码成 `localisation/acg_wuthering_nine_l_english.yml`（覆盖旧的那份，旧份仍带 LGN key）"""
if old_todo in t:
    t = t.replace(old_todo, new_todo)
    print('todo updated')

add = """
### 13.5 翡萨烈君主名补齐（2026-11-20）

用户补正：FSL 翡萨烈的君主是 **坎特蕾拉（Cantarella）**，上一轮留的是占位「摄政」。

| 文件 | 处理 | 现值 |
|---|---|---|
| `history/countries/FSL - Fisalia.txt`（编码态） | 仅替换 `name` 行，其余字节未动 | `name = "Cantarella"`（ASCII，转码前即可用） |
| `common/countries/Fisalia.txt`（ASCII） | `monarch_names` 首项 | `"Cantarella #0"` |
| `decode_localisation/history_wuwa9/history_countries/FSL - Fisalia.txt` | 明文本 | `name = "坎特蕾拉"` |
| `decode_localisation/history_wuwa9/common_countries/Fisalia.txt` | 明文本 | `"坎特蕾拉 #0"` |

王朝名保持 `翡萨烈`（`Fisalia`）不变。

### 13.6 待转码工作台（analysis/to_encode_20261120）

为了统一转码，把 19 份需要编码的文件复制进 `analysis/to_encode_20261120/`，并附 `_转码清单.md`（含「本文件夹 → 目标路径」对照表）：

| 子目录 | 份数 | 转码后目标 |
|---|---|---|
| `localisation/` | 1（`acg_wuthering_nine_l_english.yml`，198 key） | `localisation/` |
| `common_countries/` | 9 | `common/countries/` |
| `history_countries/` | 9 | `history/countries/` |

源文件仍在 `decode_localisation/` 原位；工作台是副本，改完源文件后要重新同步一次。

**仍未定**：浮光林 FGL 的君主名还是占位「摄政 / 浮光」。
"""

t = t.rstrip() + '\n' + add
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('ok bytes=', len(t.encode('utf-8')))
