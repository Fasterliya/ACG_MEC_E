# -*- coding: utf-8 -*-
"""1) 翡萨烈 FSL 君主名补上：坎特蕾拉 / Cantarella（王朝名保持 翡萨烈）
   2) 在 analysis 下开一个「待转码」工作台文件夹，把需要转码的文件全部复制进去 + 清单
"""
import os, re, shutil

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
ENC = 'latin-1'


def patch_lines(path, repl):
    """按行替换：repl 是 (匹配正则, 替换函数) 列表。latin-1 往返，字节保真。"""
    raw = open(path, 'rb').read()
    t = raw.decode(ENC)
    crlf = '\r\n' in t
    lines = t.split('\n')
    n = 0
    for i, line in enumerate(lines):
        core = line.rstrip('\r')
        for pat, fn in repl:
            if re.search(pat, core):
                new = fn(core)
                if new != core:
                    lines[i] = new + ('\r' if line.endswith('\r') else '')
                    n += 1
                break
    out = '\n'.join(lines)
    open(path, 'wb').write(out.encode(ENC))
    return n, crlf


def main():
    log = []

    # --- 1. 正式 history（用户已转码，编码态）：只动 name 这一行 ---
    p = os.path.join(MOD, 'history', 'countries', 'FSL - Fisalia.txt')
    n, _ = patch_lines(p, [(r'^\s*name\s*=', lambda l: re.sub(r'^(\s*)name\s*=.*$', r'\1name = "Cantarella"', l))])
    log.append('history/countries/FSL - Fisalia.txt  name 行替换 %d 处 -> "Cantarella"' % n)

    # --- 2. 正式 common/countries（ASCII）：名字池占位 Regent -> Cantarella ---
    p = os.path.join(MOD, 'common', 'countries', 'Fisalia.txt')
    n, _ = patch_lines(p, [(r'^\s*"Regent #0"', lambda l: l.replace('"Regent #0"', '"Cantarella #0"'))])
    log.append('common/countries/Fisalia.txt  monarch_names Regent -> Cantarella %d 处' % n)

    # --- 3. 明文两份（UTF-8）：摄政 -> 坎特蕾拉 ---
    p = os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'history_countries', 'FSL - Fisalia.txt')
    t = open(p, encoding='utf-8').read()
    t2 = t.replace('name = "摄政"', 'name = "坎特蕾拉"').replace('dynasty = "翡萨烈"', 'dynasty = "翡萨烈"')
    open(p, 'w', encoding='utf-8', newline='\n').write(t2)
    log.append('明文 history_countries/FSL - Fisalia.txt -> 坎特蕾拉 %s' % ('OK' if '坎特蕾拉' in t2 else 'FAIL'))

    p = os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'common_countries', 'Fisalia.txt')
    t = open(p, encoding='utf-8').read()
    t2 = t.replace('"摄政 #0"', '"坎特蕾拉 #0"')
    open(p, 'w', encoding='utf-8', newline='\n').write(t2)
    log.append('明文 common_countries/Fisalia.txt -> 坎特蕾拉 %s' % ('OK' if '坎特蕾拉' in t2 else 'FAIL'))

    # --- 4. 待转码工作台 ---
    stage = os.path.join(MOD, 'analysis', 'to_encode_20261120')
    for d in ('', 'localisation', 'common_countries', 'history_countries'):
        os.makedirs(os.path.join(stage, d), exist_ok=True)

    pairs = []
    src = os.path.join(MOD, 'decode_localisation', 'acg_wuthering_nine_l_english.yml')
    shutil.copy2(src, os.path.join(stage, 'localisation', 'acg_wuthering_nine_l_english.yml'))
    pairs.append(('localisation/acg_wuthering_nine_l_english.yml', 'localisation/acg_wuthering_nine_l_english.yml'))

    cc = os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'common_countries')
    for f in sorted(os.listdir(cc)):
        shutil.copy2(os.path.join(cc, f), os.path.join(stage, 'common_countries', f))
        pairs.append(('common_countries/' + f, 'common/countries/' + f))

    hc = os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'history_countries')
    for f in sorted(os.listdir(hc)):
        shutil.copy2(os.path.join(hc, f), os.path.join(stage, 'history_countries', f))
        pairs.append(('history_countries/' + f, 'history/countries/' + f))

    # 清单
    lines = []
    lines.append('# 待转码清单（2026-11-20）')
    lines.append('')
    lines.append('> 本文件夹里的文件全部是 **UTF-8 无 BOM 明文**，未经项目自定义编码。')
    lines.append('> 转码后按「目标路径」覆盖到正式目录；`localisation/` 那份编码后按原名落地。')
    lines.append('> 本 `_转码清单.md` 不是转码对象，别把它一起过机。')
    lines.append('')
    lines.append('## 合计 %d 个文件' % len(pairs))
    lines.append('')
    lines.append('| # | 本文件夹内路径 | 转码后目标路径 |')
    lines.append('|---|---|---|')
    for i, (a, b) in enumerate(pairs, 1):
        lines.append('| %d | `%s` | `%s` |' % (i, a, b))
    lines.append('')
    lines.append('## 说明')
    lines.append('')
    lines.append('- `localisation/` 那份：198 个 key（九国全部），编码后放 `localisation/acg_wuthering_nine_l_english.yml`。')
    lines.append('  **注意**：`localisation/` 里现在那份是旧的，仍带 `LGN_*`（拉古那已改名 RGU），必须用这份重新覆盖。')
    lines.append('- `common_countries/` 9 份：只有 `monarch_names` / `leader_names` 含中文，其余是颜色、兵种表、理念组。')
    lines.append('- `history_countries/` 9 份：`name` / `dynasty` 含中文；翡萨烈已改为 **坎特蕾拉**，其余为 汐 / 罗斯玛丽 / 爱弥斯 / 暝 / 弗洛洛 / 珂莱塔 / 菲比，浮光林仍是占位「摄政」。')
    lines.append('- 覆盖目标目录的编码约定：UTF-8 → 项目自定义编码；行尾保持 CRLF。')
    open(os.path.join(stage, '_转码清单.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

    log.append('工作台：%s（%d 个待转码文件 + 1 份清单）' % (stage, len(pairs)))
    print('\n'.join(log))
    for a, b in pairs:
        print('  ', a, '->', b)


if __name__ == '__main__':
    main()
