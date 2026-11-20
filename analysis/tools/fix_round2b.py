#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""第二轮修正（续）：LGN -> RGU 的正确改名 + 省份/首都调整。
注意：history/countries 与 common/countries 已被用户转码成项目自定义编码，
这些文件只能重命名 / 做 ASCII 字节级改动，不能按 UTF-8 读写。"""
import os, re, sys, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_round2 as F

MOD = F.MOD
BK = F.BK


def fix_utf8(p, dry):
    if not os.path.exists(p):
        return 'skip missing %s' % os.path.basename(p)
    t = open(p, encoding='utf-8').read()
    if 'LGN' not in t:
        return 'no LGN in %s' % os.path.basename(p)
    t2 = t.replace('LGN', 'RGU')
    n = t.count('LGN')
    if not dry:
        shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
        open(p, 'w', encoding='utf-8', newline='\n').write(t2)
    return '%-46s LGN x%d -> RGU' % (os.path.basename(p), n)


def rename_only(p, dry):
    new = p.replace('LGN', 'RGU')
    if p == new or not os.path.exists(p):
        return 'skip %s' % os.path.basename(p)
    if not dry:
        if not os.path.exists(new):
            os.rename(p, new)
        else:
            os.remove(p)
    return 'rename %s -> %s' % (os.path.basename(p), os.path.basename(new))


def do_rename(dry):
    log = []
    # 1) 理念：内容 key（LGN_ideas / LGN_idea_N）
    for name in ('RGU_ideas.txt', 'LGN_ideas.txt'):
        p = os.path.join(MOD, 'common', 'ideas', name)
        if os.path.exists(p):
            log.append(fix_utf8(p, dry))
    p = os.path.join(MOD, 'common', 'ideas', 'LGN_ideas.txt')
    if os.path.exists(p):
        log.append(rename_only(p, dry))
    # 2) 正式国家历史（编码态）：只重命名
    log.append(rename_only(os.path.join(MOD, 'history', 'countries', 'LGN - Ragunna.txt'), dry))
    # 3) 明文国家历史（UTF-8）：替换 + 重命名
    p = os.path.join(MOD, 'decode_localisation', 'history_wuwa9', 'history_countries', 'LGN - Ragunna.txt')
    log.append(fix_utf8(p, dry))
    log.append(rename_only(p, dry))
    # 4) tag 注册
    log.append(fix_utf8(os.path.join(MOD, 'common', 'country_tags', 'ACG_MEC_E_country_tag.txt'), dry))
    # 5) 本地化明文
    log.append(fix_utf8(os.path.join(MOD, 'decode_localisation', 'acg_wuthering_nine_l_english.yml'), dry))
    # 6) 拉古那 7 个省文件（UTF-8）
    for f in os.listdir(F.PROV):
        m = re.match(r'^\s*(\d+)\s*-', f)
        if m and int(m.group(1)) in (621, 622, 623, 2678, 2679, 2680, 4818):
            log.append(fix_utf8(os.path.join(F.PROV, f), dry))
    return log


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    os.makedirs(BK, exist_ok=True)
    print('=== A. LGN -> RGU ===')
    for l in do_rename(dry):
        print(' ', l)
    print('=== B. 680 还原 ===')
    for l in F.restore_680(dry):
        print(' ', l)
    print('=== C. 省份 ===')
    for l in F.do_provinces(dry):
        print(' ', l)
    print('=== D. 首都 ===')
    for l in F.do_capitals(dry):
        print(' ', l)
