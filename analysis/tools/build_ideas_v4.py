# -*- coding: utf-8 -*-
"""理念第四版：所有百分比修正只允许 5% 网格（5/7.5/10/15/20/25…），禁止 8%、2%、4% 这类尾数。
理念名与描述不动 —— loc 明文不受影响。"""
import os, re, shutil, json

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
BK = os.path.join(MOD, 'analysis', 'backup_ideas_v4_20261120')

N = [
 ('JZH', [('land_morale', 0.10), ('defensiveness', 0.15)], [('infantry_power', 0.10)],
  [('玉京守望', [('production_efficiency', 0.10), ('build_cost', -0.10)]),
   ('今州铁壁', [('max_hostile_attrition', 1)]),
   ('鸣钟之律', [('stability_cost_modifier', -0.10), ('global_unrest', -1)]),
   ('龙泉军工', [('artillery_power', 0.10)]),
   ('潮汐军阵', [('discipline', 0.05)]),
   ('边地屯垦', [('manpower_recovery_speed', 0.10), ('global_manpower_modifier', 0.10)]),
   ('岁主遗训', [('land_forcelimit_modifier', 0.10), ('core_creation', -0.10)])]),

 ('RGU', [('trade_efficiency', 0.10), ('global_trade_power', 0.10)], [('diplomatic_reputation', 1)],
  [('狂欢之港', [('production_efficiency', 0.10), ('global_tax_modifier', 0.10)]),
   ('商路辐辏', [('global_ship_trade_power', 0.15)]),
   ('群岛船团', [('naval_forcelimit_modifier', 0.15)]),
   ('假面舞会', [('prestige', 0.5)]),
   ('剧院之城', [('build_cost', -0.10), ('development_cost', -0.10)]),
   ('金穗税制', [('governing_capacity', 100)]),
   ('远洋护航', [('naval_morale', 0.10), ('heavy_ship_power', 0.10)])]),

 ('XJA', [('technology_cost', -0.10), ('development_cost', -0.10)], [('all_power_cost', -0.05)],
  [('星炬讲堂', [('institution_spread', 0.10)]),
   ('共鸣研究', [('build_cost', -0.10)]),
   ('学院工坊', [('production_efficiency', 0.10), ('global_tax_modifier', 0.10)]),
   ('学术声望', [('prestige', 0.5), ('diplomatic_reputation', 1)]),
   ('交换学者', [('global_trade_power', 0.10)]),
   ('学园产业', [('trade_efficiency', 0.10)]),
   ('护院卫队', [('land_morale', 0.10), ('discipline', 0.05)])]),

 ('MGZ', [('stability_cost_modifier', -0.10), ('global_unrest', -1)], [('tolerance_own', 1)],
  [('梦泽烟波', [('prestige', 0.5), ('diplomatic_reputation', 1)]),
   ('州府编户', [('global_tax_modifier', 0.10), ('governing_capacity', 100)]),
   ('织造之邦', [('production_efficiency', 0.10), ('trade_efficiency', 0.10)]),
   ('锁氏亲军', [('land_morale', 0.10), ('infantry_power', 0.10)]),
   ('泽国堤防', [('defensiveness', 0.15), ('max_hostile_attrition', 1)]),
   ('归化之策', [('core_creation', -0.10)]),
   ('梦州声望', [('manpower_recovery_speed', 0.10)])]),

 ('CXT', [('spy_offence', 0.20), ('land_morale', 0.10)], [('discipline', 0.05)],
  [('残星锐士', [('infantry_power', 0.10), ('cavalry_power', 0.10)]),
   ('暗潮渗透', [('siege_ability', 0.10)]),
   ('星屑回响', [('manpower_recovery_speed', 0.10), ('global_manpower_modifier', 0.10)]),
   ('不惜代价', [('war_exhaustion', -0.10)]),
   ('铁腕统御', [('global_unrest', -1), ('stability_cost_modifier', -0.10)]),
   ('疆域清算', [('core_creation', -0.10), ('prestige', 0.5)]),
   ('残星征召', [('land_forcelimit_modifier', 0.10)])]),

 ('FGL', [('global_manpower_modifier', 0.10), ('max_hostile_attrition', 1)], [('manpower_recovery_speed', 0.10)],
  [('林间伏兵', [('defensiveness', 0.15), ('land_morale', 0.10)]),
   ('守林游猎', [('infantry_power', 0.10)]),
   ('木寨工事', [('build_cost', -0.10)]),
   ('浮光木产', [('production_efficiency', 0.10), ('global_tax_modifier', 0.10)]),
   ('林贡之制', [('governing_capacity', 50)]),
   ('山林征召', [('land_forcelimit_modifier', 0.15)]),
   ('林誓之约', [('stability_cost_modifier', -0.10), ('global_unrest', -1)])]),

 ('FSL', [('naval_morale', 0.10), ('global_ship_trade_power', 0.10)], [('naval_forcelimit_modifier', 0.20)],
  [('重舰传统', [('heavy_ship_power', 0.10)]),
   ('海峡操练', [('recover_navy_morale_speed', 0.10), ('naval_combat_ability', 0.10)]),
   ('水手世家', [('sailors_recovery_speed', 0.10)]),
   ('香料航路', [('trade_efficiency', 0.10), ('global_trade_power', 0.10)]),
   ('远洋传承', [('navy_tradition_decay', -0.05)]),
   ('群岛商权', [('global_tax_modifier', 0.10)]),
   ('港务税关', [('production_efficiency', 0.10)])]),

 ('MTL', [('global_tax_modifier', 0.10), ('production_efficiency', 0.10)], [('trade_efficiency', 0.10)],
  [('家族金库', [('build_cost', -0.10)]),
   ('商会网络', [('global_trade_power', 0.15)]),
   ('城邦营造', [('development_cost', -0.10)]),
   ('名门声望', [('prestige', 0.5), ('diplomatic_reputation', 1)]),
   ('契约精神', [('stability_cost_modifier', -0.10), ('global_unrest', -1)]),
   ('私兵护卫', [('land_morale', 0.10), ('land_forcelimit_modifier', 0.10)]),
   ('外交联姻', [('governing_capacity', 50)])]),

 ('YHH', [('tolerance_own', 1), ('stability_cost_modifier', -0.10)], [('prestige', 1.0)],
  [('深海圣所', [('global_tax_modifier', 0.10), ('governing_capacity', 100)]),
   ('修会戒律', [('global_unrest', -1), ('land_morale', 0.10)]),
   ('海疆归化', [('core_creation', -0.10)]),
   ('圣殿卫队', [('discipline', 0.05), ('infantry_power', 0.10)]),
   ('教区治理', [('manpower_recovery_speed', 0.10)]),
   ('布道四方', [('diplomatic_reputation', 1), ('global_manpower_modifier', 0.10)]),
   ('虔诚之刃', [('cavalry_power', 0.10)])]),
]


def fmt(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def text(tag, start, bonus, ideas):
    def blk(lst):
        return '\n'.join('\t\t%s = %s' % (k, fmt(v)) for k, v in lst)
    body = '\n'.join('\t%s_idea_%d = {\n%s\n\t}' % (tag, i, blk(ml)) for i, (nm, ml) in enumerate(ideas, 1))
    return """%s_ideas = {
	start = {
%s
	}
	bonus = {
%s
	}
	trigger = {
		tag = %s
	}
	free = yes
%s
}
""" % (tag, blk(start), blk(bonus), tag, body)


def grid_ok(v):
    """value*100 必须是 5 的整数倍（5% 网格）。"""
    x = round(v * 100, 6)
    return abs(x - round(x)) < 1e-6 and round(x) % 5 == 0


def main():
    os.makedirs(BK, exist_ok=True)
    bad_values = []
    rows = []
    for tag, start, bonus, ideas in N:
        p = os.path.join(MOD, 'common', 'ideas', '%s_ideas.txt' % tag)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
        open(p, 'w', encoding='utf-8', newline='\n').write(text(tag, start, bonus, ideas))

        allmods = [k for k, _ in start] + [k for k, _ in bonus] + [k for _, ml in ideas for k, _ in ml]
        vals = [v for _, v in start] + [v for _, v in bonus] + [v for _, ml in ideas for _, v in ml]
        dup = sorted({k for k in allmods if allmods.count(k) > 1})
        offgrid = [v for v in vals if not grid_ok(v)]
        if offgrid:
            bad_values.append((tag, offgrid))
        rows.append({'tag': tag, 'mods': len(allmods), 'uniq': len(set(allmods)),
                     'dup': dup, 'per_slot': [len(ml) for _, ml in ideas], 'offgrid': offgrid})
        print('%-4s 修正=%-3d 唯一=%-3d 重复=%-4s 槽位=%s 非5%%网格=%s' %
              (tag, len(allmods), len(set(allmods)), dup or '无',
               [len(ml) for _, ml in ideas], offgrid or '无'))
    json.dump(rows, open(os.path.join(MOD, 'analysis', '_ideas_v4_report.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('\n全部数值合规' if not bad_values else '\n违规: %s' % bad_values)


if __name__ == '__main__':
    main()
