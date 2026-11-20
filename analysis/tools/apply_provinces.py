#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""鸣潮九国 —— 省份 history 批量改造（基底 -> MOD 层，顶层重写归属/文化/宗教/核心，清日期块残留）"""
import os, re, json, shutil, sys

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
ACG1 = r'F:\SteamLibrary\steamapps\workshop\content\236850\2796854877'
VAN = r'F:\SteamLibrary\steamapps\common\Europa Universalis IV'

NEW_CULTURE = 'acg_wuthering_waves'
NEW_RELIGION = 'acg'

TARGETS = {
    'JZH': [637, 651, 655, 2703, 2709, 2710, 2711, 4354, 4356, 4799],
    'LGN': [621, 622, 623, 2678, 2679, 2680, 4818],
    'XJA': [624, 625, 680, 2687, 2688, 4790, 4791],
    'MGZ': [638, 639, 2706, 2707, 2708, 2712, 4800, 4801],
    'CXT': [627, 631, 2690, 2691, 4794],
    'FGL': [626, 628, 629, 2689, 2692, 4792, 4793],
    'FSL': [619, 2681, 2682, 4811, 4817],
    'MTL': [617, 2673, 2674, 2685, 4809],
    'YHH': [595, 596, 597, 598, 618, 2392, 2675, 2686, 4810, 4814, 4815],
}
CAPS = {'JZH': 2710, 'LGN': 622, 'XJA': 2687, 'MGZ': 639, 'CXT': 627,
        'FGL': 628, 'FSL': 2681, 'MTL': 2673, 'YHH': 596}

PROV_DIRS = {
    'MOD': os.path.join(MOD, 'history', 'provinces'),
    'ACG1': os.path.join(ACG1, 'history', 'provinces'),
    'VAN': os.path.join(VAN, 'history', 'provinces'),
}


def index_dir(d):
    m = {}
    if not os.path.isdir(d):
        return m
    for p in os.listdir(d):
        if not p.lower().endswith('.txt'):
            continue
        mm = re.match(r'^\s*(\d+)\s*-', p)
        if mm:
            m.setdefault(int(mm.group(1)), os.path.join(d, p))
    return m


IDX = {k: index_dir(v) for k, v in PROV_DIRS.items()}


def locate(pid):
    """返回 (层名, 路径)；MOD 优先。"""
    for k in ('MOD', 'ACG1', 'VAN'):
        if pid in IDX[k]:
            return k, IDX[k][pid]
    return None, None


KEY_RE = re.compile(r'^(\s*)(owner|controller|culture|religion|add_core|remove_core)\s*=\s*([^\s{}#]+)')
DATE_RE = re.compile(r'\d+\.\d+\.\d+\s*=\s*\{')


def strip_empty_date_blocks(text):
    """删除内容为空（只剩空白）的日期块，支持嵌套花括号。"""
    out = []
    i = 0
    n = len(text)
    while i < n:
        m = DATE_RE.match(text, i) if (i == 0 or text[i - 1] == '\n') else None
        if not m:
            out.append(text[i])
            i += 1
            continue
        # 找到块起始 '{'
        brace = text.find('{', i)
        depth = 0
        j = brace
        while j < n:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        inner = text[brace + 1:j]
        if inner.strip() == '':
            # 吞掉整行到行尾
            end = text.find('\n', j)
            end = n if end == -1 else end + 1
            i = end
            continue
        out.append(text[i:j + 1])
        i = j + 1
    return ''.join(out)


def split_braces(text):
    """把 { 和 } 前后强制断行，让块内的键都落在独立行上（注释区不动，换行不影响语法）。"""
    out = []
    i, n = 0, len(text)
    in_comment = False
    while i < n:
        c = text[i]
        if in_comment:
            out.append(c)
            if c == '\n':
                in_comment = False
            i += 1
            continue
        if c == '#':
            in_comment = True
            out.append(c)
            i += 1
            continue
        if c == '{':
            out.append('{')
            out.append('\n')
            i += 1
            while i < n and text[i] in ' \t':
                i += 1
            continue
        if c == '}':
            while out and out[-1] in ' \t':
                out.pop()
            if out and out[-1] != '\n':
                out.append('\n')
            out.append('}')
            out.append('\n')
            i += 1
            while i < n and text[i] in ' \t':
                i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def transform(text, tag, pid):
    text = split_braces(text)
    lines = text.split('\n')
    depth = 0
    res = []
    stats = {'owner_lines': 0, 'controller_lines': 0, 'culture_lines': 0,
             'religion_lines': 0, 'core_lines': 0, 'date_removed': 0}
    have = {'owner': False, 'controller': False, 'culture': False, 'religion': False}
    add_core_written = False

    for raw in lines:
        line = raw
        stripped = line.strip()
        d0 = depth

        # 先按当前深度判断
        m = KEY_RE.match(line)
        if m and d0 == 0:
            ind, key, val = m.group(1), m.group(2), m.group(3)
            if key == 'owner':
                res.append(f'{ind}owner = {tag}')
                have['owner'] = True
                stats['owner_lines'] += 1
            elif key == 'controller':
                res.append(f'{ind}controller = {tag}')
                have['controller'] = True
                stats['controller_lines'] += 1
            elif key == 'culture':
                res.append(f'{ind}culture = {NEW_CULTURE}')
                have['culture'] = True
                stats['culture_lines'] += 1
            elif key == 'religion':
                res.append(f'{ind}religion = {NEW_RELIGION}')
                have['religion'] = True
                stats['religion_lines'] += 1
            elif key == 'add_core':
                if not add_core_written:
                    res.append(f'{ind}add_core = {tag}')
                    add_core_written = True
                    stats['core_lines'] += 1
                else:
                    stats['core_lines'] += 1
            elif key == 'remove_core':
                stats['core_lines'] += 1  # 丢弃
            depth += line.count('{') - line.count('}')
            continue

        if d0 >= 1 and m:
            # 日期块内的归属/文化/宗教变更：全部丢弃
            stats['date_removed'] += 1
            depth += line.count('{') - line.count('}')
            continue

        # hre
        if d0 == 0 and re.match(r'^\s*hre\s*=\s*yes', line):
            res.append(re.sub(r'yes', 'no', line, count=1))

        res.append(line)
        depth += line.count('{') - line.count('}')
        if depth < 0:
            depth = 0

    text2 = '\n'.join(res)

    # 缺的顶层键补上
    add = []
    if not have['owner']:
        add.append(f'owner = {tag}')
    if not have['controller']:
        add.append(f'controller = {tag}')
    if not add_core_written:
        add.append(f'add_core = {tag}')
    if not have['culture']:
        add.append(f'culture = {NEW_CULTURE}')
    if not have['religion']:
        add.append(f'religion = {NEW_RELIGION}')

    if add:
        ls = text2.split('\n')
        head = 0
        while head < len(ls) and (ls[head].strip() == '' or ls[head].strip().startswith('#')):
            head += 1
        block = add + ['']
        ls[head:head] = block
        text2 = '\n'.join(ls)

    text2 = strip_empty_date_blocks(text2)
    # 折叠 3 个以上空行
    text2 = re.sub(r'\n{3,}', '\n\n', text2)
    if not text2.endswith('\n'):
        text2 += '\n'
    return text2, stats


def braces_ok(t):
    return t.count('{') == t.count('}')


def main():
    dry = '--apply' not in sys.argv
    backup = os.path.join(MOD, 'analysis', 'backup_省份_鸣潮九国_20261120')
    os.makedirs(backup, exist_ok=True)
    report = []
    for tag, ids in TARGETS.items():
        for pid in ids:
            layer, src = locate(pid)
            if not src:
                report.append({'id': pid, 'tag': tag, 'status': 'MISSING'})
                continue
            raw = open(src, 'rb').read()
            bom = raw.startswith(b'\xef\xbb\xbf')
            text = raw.decode('utf-8-sig')
            old_owner = ''
            m = re.search(r'(?m)^\s*owner\s*=\s*([A-Za-z0-9_]+)', text)
            if m:
                old_owner = m.group(1)
            new_text, stats = transform(text, tag, pid)
            ok = braces_ok(new_text)
            dst = os.path.join(PROV_DIRS['MOD'], os.path.basename(src))
            if layer != 'MOD':
                # 从基底复制文件名到 MOD 层
                pass
            rec = {'id': pid, 'tag': tag, 'layer': layer, 'file': os.path.basename(src),
                   'old_owner': old_owner, 'braces_ok': ok, 'stats': stats,
                   'capital': CAPS.get(tag) == pid}
            if not dry and ok:
                # 备份
                if os.path.exists(dst):
                    shutil.copy2(dst, os.path.join(backup, os.path.basename(dst)))
                with open(dst, 'wb') as f:
                    if bom:
                        f.write(b'\xef\xbb\xbf')
                    f.write(new_text.encode('utf-8'))
                rec['written'] = dst
            report.append(rec)

    json.dump(report, open(os.path.join(MOD, 'analysis', '_prov_apply_report.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    bad = [r for r in report if r.get('braces_ok') is False or r.get('status') == 'MISSING']
    print('total=%d bad=%d dry=%s' % (len(report), len(bad), dry))
    for r in bad:
        print('  BAD', r)
    for r in report:
        if 'stats' in r and (r['stats']['date_removed'] or r['old_owner']):
            print('  %-5d %-4s %-4s -> %s  dateRemoved=%d core=%d' %
                  (r['id'], r['tag'], r['old_owner'] or '-', r['tag'],
                   r['stats']['date_removed'], r['stats']['core_lines']))


if __name__ == '__main__':
    main()
