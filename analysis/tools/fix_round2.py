#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第二轮修正：
A. LGN -> RGU（LGN 与 ACG1 flavorAOG.txt 的 union tag 冲突）
B. 630 -> XJA（全量），680 -> 还原给 HMC（从备份恢复）
C. 4804 / 4802 / 4803 / 640 -> BLS（只改归属+宗教，文化保持），BLS 全部省份宗教 -> acg
D. 国家首都：HMC 681->680；SUN / BEI / SMB 全失地删 capital
"""
import os, re, shutil, sys, glob

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
ACG1 = r'F:\SteamLibrary\steamapps\workshop\content\236850\2796854877'
VAN = r'F:\SteamLibrary\steamapps\common\Europa Universalis IV'
PROV = os.path.join(MOD, 'history', 'provinces')
BK = os.path.join(MOD, 'analysis', 'backup_round2_20261120')
PROV_BK = os.path.join(MOD, 'analysis', 'backup_省份_鸣潮九国_20261120')


def split_braces(text):
    out, i, n, com = [], 0, len(text), False
    while i < n:
        c = text[i]
        if com:
            out.append(c)
            if c == '\n':
                com = False
            i += 1
            continue
        if c == '#':
            com = True
            out.append(c)
            i += 1
            continue
        if c == '{':
            out.append('{\n')
            i += 1
            while i < n and text[i] in ' \t':
                i += 1
            continue
        if c == '}':
            while out and out[-1] in ' \t':
                out.pop()
            if out and out[-1] != '\n':
                out.append('\n')
            out.append('}\n')
            i += 1
            while i < n and text[i] in ' \t':
                i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


DATE_RE = re.compile(r'\d+\.\d+\.\d+\s*=\s*\{')


def strip_empty_date_blocks(text):
    out, i, n = [], 0, len(text)
    while i < n:
        if (i == 0 or text[i - 1] == '\n'):
            m = DATE_RE.match(text, i)
        else:
            m = None
        if not m:
            out.append(text[i])
            i += 1
            continue
        brace = text.find('{', i)
        depth, j = 0, brace
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
            end = text.find('\n', j)
            i = n if end == -1 else end + 1
            continue
        out.append(text[i:j + 1])
        i = j + 1
    return ''.join(out)


def find_prov(pid):
    for f in os.listdir(PROV):
        m = re.match(r'^\s*(\d+)\s*-', f)
        if m and int(m.group(1)) == pid:
            return os.path.join(PROV, f)
    # 回退：按基底层找
    for d in (os.path.join(ACG1, 'history', 'provinces'), os.path.join(VAN, 'history', 'provinces')):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            m = re.match(r'^\s*(\d+)\s*-', f)
            if m and int(m.group(1)) == pid:
                return os.path.join(d, f)
    return None


KEYS = ('owner', 'controller', 'add_core', 'remove_core', 'religion', 'culture')
KEY_RE = re.compile(r'^(\s*)(owner|controller|add_core|remove_core|religion|culture)\s*=\s*([^\s{}#]+)')


def rewrite_province(text, tag, change_culture):
    text = split_braces(text)
    lines = text.split('\n')
    depth = 0
    res = []
    have = {'owner': False, 'controller': False, 'add_core': False, 'religion': False, 'culture': False}
    core_done = False
    stat = {'date': 0}
    for line in lines:
        d0 = depth
        m = KEY_RE.match(line)
        if m and d0 == 0:
            ind, k = m.group(1), m.group(2)
            if k == 'owner':
                res.append('%sowner = %s' % (ind, tag)); have['owner'] = True
            elif k == 'controller':
                res.append('%scontroller = %s' % (ind, tag)); have['controller'] = True
            elif k == 'add_core':
                if not core_done:
                    res.append('%sadd_core = %s' % (ind, tag)); core_done = True; have['add_core'] = True
            elif k == 'remove_core':
                pass
            elif k == 'religion':
                res.append('%sreligion = acg' % ind); have['religion'] = True
            elif k == 'culture':
                if change_culture:
                    res.append('%sculture = acg_wuthering_waves' % ind)
                    have['culture'] = True
                else:
                    res.append(line)
            depth += line.count('{') - line.count('}')
            continue
        if d0 >= 1 and m:
            k = m.group(2)
            if k in ('owner', 'controller', 'add_core', 'remove_core', 'religion') or (change_culture and k == 'culture'):
                stat['date'] += 1
                depth += line.count('{') - line.count('}')
                continue
        res.append(line)
        depth += line.count('{') - line.count('}')
        if depth < 0:
            depth = 0
    text2 = '\n'.join(res)
    add = []
    if not have['owner']:
        add.append('owner = %s' % tag)
    if not have['controller']:
        add.append('controller = %s' % tag)
    if not core_done:
        add.append('add_core = %s' % tag)
    if not have['religion']:
        add.append('religion = acg')
    if change_culture and not have['culture']:
        add.append('culture = acg_wuthering_waves')
    if add:
        ls = text2.split('\n')
        h = 0
        while h < len(ls) and (ls[h].strip() == '' or ls[h].strip().startswith('#')):
            h += 1
        ls[h:h] = add + ['']
        text2 = '\n'.join(ls)
    text2 = strip_empty_date_blocks(text2)
    text2 = re.sub(r'\n{3,}', '\n\n', text2)
    if not text2.endswith('\n'):
        text2 += '\n'
    return text2, stat


# ---------- A. LGN -> RGU ----------
RENAME_FILES = [
    os.path.join(MOD, 'common', 'ideas', 'LGN_ideas.txt'),
    os.path.join(MOD, 'history', 'countries', 'LGN - Ragunna.txt'),
    os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'history_countries', 'LGN - Ragunna.txt'),
]
CONTENT_FILES = [
    os.path.join(MOD, 'common', 'country_tags', 'ACG_MEC_E_country_tag.txt'),
    os.path.join(MOD, 'decode_localisation', 'acg_wuthering_nine_l_english.yml'),
]


def do_rename():
    os.makedirs(BK, exist_ok=True)
    log = []
    for p in RENAME_FILES:
        if not os.path.exists(p):
            log.append('SKIP missing %s' % p)
            continue
        t = open(p, encoding='utf-8').read()
        shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
        t2 = re.sub(r'\bLGN\b', 'RGU', t)
        new = p.replace('LGN', 'RGU')
        open(new, 'w', encoding='utf-8', newline='\n').write(t2)
        os.remove(p)
        log.append('RENAMED %s -> %s' % (os.path.basename(p), os.path.basename(new)))
    for p in CONTENT_FILES:
        if not os.path.exists(p):
            continue
        t = open(p, encoding='utf-8').read()
        t2 = re.sub(r'\bLGN\b', 'RGU', t)
        if t2 != t:
            shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
            open(p, 'w', encoding='utf-8', newline='\n').write(t2)
            log.append('CONTENT %s: %d 处' % (os.path.basename(p), len(re.findall(r'\bLGN\b', t))))
    return log


# ---------- B/C. 省份 ----------
PROV_PLAN = [
    (630, 'XJA', True),    # 卡隆巴 -> 星炬学院（连文化一起转）
    (4804, 'BLS', False),
    (4802, 'BLS', False),
    (4803, 'BLS', False),
    (640, 'BLS', False),
    (636, 'BLS', False),   # BLS 原有 5 省，只改宗教
    (2704, 'BLS', False),
    (2705, 'BLS', False),
    (4805, 'BLS', False),
    (4806, 'BLS', False),
]


def do_provinces(dry):
    os.makedirs(BK, exist_ok=True)
    log = []
    for pid, tag, chc in PROV_PLAN:
        p = find_prov(pid)
        if not p:
            log.append('MISSING %d' % pid)
            continue
        raw = open(p, 'rb').read()
        bom = raw.startswith(b'\xef\xbb\xbf')
        t = raw.decode('utf-8-sig')
        old = re.search(r'(?m)^\s*owner\s*=\s*([A-Za-z0-9_]+)', t)
        old = old.group(1) if old else '-'
        t2, st = rewrite_province(t, tag, chc)
        ok = t2.count('{') == t2.count('}')
        log.append('%s %-5d %-4s->%-4s culture=%s dateRemoved=%d braces=%s' %
                   ('PLAN' if dry else 'WRITE', pid, old, tag,
                    'acg_wuthering_waves' if chc else 'keep', st['date'], ok))
        if not dry and ok:
            dst = os.path.join(PROV, os.path.basename(p))
            if os.path.exists(dst):
                shutil.copy2(dst, os.path.join(BK, os.path.basename(dst)))
            open(dst, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + t2.encode('utf-8'))
    return log


# ---------- B. 680 还原 ----------
def restore_680(dry):
    src = os.path.join(PROV_BK, '680 - Chongqing.txt')
    dst = os.path.join(PROV, '680 - Chongqing.txt')
    if not os.path.exists(src):
        return ['680 备份缺失：%s' % src]
    if not dry:
        shutil.copy2(dst, os.path.join(BK, '680 - Chongqing.before-restore.txt'))
        shutil.copy2(src, dst)
    return ['680 restored from round1 backup -> HMC / acg_hongmao / confucianism']


# ---------- D. 首都 ----------
CP = re.compile(r'^([ \t]*)capital[ \t]*=[ \t]*(\d+)([ \t]*(?:#.*)?)$')
CDIRS = [os.path.join(MOD, 'history', 'countries'),
         os.path.join(ACG1, 'history', 'countries'),
         os.path.join(VAN, 'history', 'countries')]


def locate_country(tag):
    for d in CDIRS:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if re.match(r'^%s\s*-' % tag, f):
                return d, f
    return None, None


def edit_capital(text, newcap):
    lines = text.split('\n')
    depth, out, done, removed = 0, [], False, 0
    for line in lines:
        if depth == 0:
            m = CP.match(line.rstrip('\r'))
            if m:
                cr = '\r' if line.endswith('\r') else ''
                if newcap is None:
                    removed += 1
                    depth += line.count('{') - line.count('}')
                    continue
                if not done:
                    out.append('%scapital = %d%s%s' % (m.group(1), newcap, m.group(3), cr))
                    done = True
                    depth += line.count('{') - line.count('}')
                    continue
                removed += 1
                depth += line.count('{') - line.count('}')
                continue
        out.append(line)
        depth += line.count('{') - line.count('}')
    t = '\n'.join(out)
    if not t.endswith('\n'):
        t += '\n'
    return t, done, removed


def do_capitals(dry):
    log = []
    plan = [('HMC', 680), ('SUN', None), ('BEI', None), ('SMB', None)]
    for tag, cap in plan:
        d, f = locate_country(tag)
        if not f:
            log.append('MISSING country %s' % tag)
            continue
        src = os.path.join(d, f)
        raw = open(src, 'rb').read()
        t = raw.decode('latin-1')
        t2, done, removed = edit_capital(t, cap)
        ok = t2.count('{') == t2.count('}')
        log.append('%s %-4s cap=%-5s replaced=%s removed=%s braces=%s' %
                   ('PLAN' if dry else 'WRITE', tag, cap, done, removed, ok))
        if not dry and ok:
            dst = os.path.join(MOD, 'history', 'countries', f)
            if os.path.exists(dst):
                shutil.copy2(dst, os.path.join(BK, f))
            open(dst, 'wb').write(t2.encode('latin-1'))
    return log


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    print('=== A. LGN -> RGU ===')
    for l in (do_rename() if not dry else ['(dry) rename skipped']):
        print(' ', l)
    print('=== B. 680 还原 ===')
    for l in restore_680(dry):
        print(' ', l)
    print('=== C. 省份 ===')
    for l in do_provinces(dry):
        print(' ', l)
    print('=== D. 首都 ===')
    for l in do_capitals(dry):
        print(' ', l)
