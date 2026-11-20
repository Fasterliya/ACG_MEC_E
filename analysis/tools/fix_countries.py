#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""旧主处理：全失地国家删除 capital（无地保留 tag）；首都被抢但有地的国家迁都。
字节安全：全程 latin-1 往返，只触碰 ASCII 数字，不破坏项目自定义编码。"""
import os, re, json, shutil, sys

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
ACG1 = r'F:\SteamLibrary\steamapps\workshop\content\236850\2796854877'
VAN = r'F:\SteamLibrary\steamapps\common\Europa Universalis IV'

REMOVE = ['MAJ', 'MLC', 'PSA', 'BNJ', 'BEU', 'KUT', 'PLB', 'PGR', 'DLI',
          'IND', 'BRS', 'PAH', 'SUL', 'BAN', 'BLM']
RECAP = {'BEI': 4804, 'SUN': 630, 'BLI': 2693, 'HMC': 681}

DIRS = [os.path.join(MOD, 'history', 'countries'),
        os.path.join(ACG1, 'history', 'countries'),
        os.path.join(VAN, 'history', 'countries')]
MODDIR = DIRS[0]


def cidx(d):
    m = {}
    if not os.path.isdir(d):
        return m
    for p in os.listdir(d):
        mm = re.match(r'^([A-Z0-9]{3})\s*-', p)
        if mm:
            m.setdefault(mm.group(1), p)
    return m


def locate(tag):
    for d in DIRS:
        m = cidx(d)
        if tag in m:
            return d, m[tag]
    return None, None


def edit_capital(text, newcap):
    lines = text.split('\n')
    depth = 0
    out = []
    done = False
    removed = 0
    CP = re.compile(r'^([ \t]*)capital[ \t]*=[ \t]*(\d+)([ \t]*(?:#.*)?)$')
    for line in lines:
        d0 = depth
        if d0 == 0:
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
    text2 = '\n'.join(out)
    if not text2.endswith('\n'):
        text2 += '\n'
    return text2, done, removed


def main():
    dry = '--apply' not in sys.argv
    backup = os.path.join(MOD, 'analysis', 'backup_国家_鸣潮九国_20261120')
    os.makedirs(backup, exist_ok=True)
    rep = []
    plan = [(t, None) for t in REMOVE] + list(RECAP.items())
    for tag, newcap in plan:
        d, name = locate(tag)
        if not name:
            rep.append({'tag': tag, 'status': 'MISSING'})
            print('MISSING', tag)
            continue
        src = os.path.join(d, name)
        raw = open(src, 'rb').read()
        text = raw.decode('latin-1')
        text2, done, removed = edit_capital(text, newcap)
        ok = text2.count('{') == text2.count('}')
        rec = {'tag': tag, 'src': src, 'file': name, 'newcap': newcap,
               'replaced': done, 'removed': removed, 'braces_ok': ok,
               'layer': 'MOD' if d == MODDIR else os.path.basename(os.path.dirname(os.path.dirname(d)))}
        dst = os.path.join(MODDIR, name)
        rec['dest'] = dst
        if not dry and ok:
            if os.path.exists(dst):
                shutil.copy2(dst, os.path.join(backup, name))
            open(dst, 'wb').write(text2.encode('latin-1'))
        rep.append(rec)
        print('%-4s %-7s -> cap=%-5s replaced=%s removed=%s braces=%s' %
              (tag, rec['layer'], newcap, done, removed, ok))
    json.dump(rep, open(os.path.join(MOD, 'analysis', '_country_fix_report.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
