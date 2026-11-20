# -*- coding: utf-8 -*-
"""理念第三版：同一国家内修正不重复 / 数值降一档 / 槽位条数混合（1-3 条，不再全二）
理念名与描述不变 —— loc 明文不受影响，不用重转。"""
import os, re, shutil, json

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
BK = os.path.join(MOD, 'analysis', 'backup_ideas_v3_20261120')

N = [
 ('JZH', [('land_morale', 0.12), ('defensiveness', 0.15)], [('infantry_power', 0.08)],
  [('玉京守望', [('production_efficiency', 0.12), ('build_cost', -0.08)]),
   ('今州铁壁', [('max_hostile_attrition', 1)]),
   ('鸣钟之律', [('stability_cost_modifier', -0.12), ('global_unrest', -1)]),
   ('龙泉军工', [('artillery_power', 0.08)]),
   ('潮汐军阵', [('discipline', 0.04)]),
   ('边地屯垦', [('manpower_recovery_speed', 0.12), ('global_manpower_modifier', 0.10)]),
   ('岁主遗训', [('land_forcelimit_modifier', 0.12), ('core_creation', -0.08)])]),

 ('RGU', [('trade_efficiency', 0.12), ('global_trade_power', 0.12)], [('diplomatic_reputation', 1)],
  [('狂欢之港', [('production_efficiency', 0.12), ('global_tax_modifier', 0.08)]),
   ('商路辐辏', [('global_ship_trade_power', 0.15)]),
   ('群岛船团', [('naval_forcelimit_modifier', 0.15)]),
   ('假面舞会', [('prestige', 0.8)]),
   ('剧院之城', [('build_cost', -0.12), ('development_cost', -0.08)]),
   ('金穗税制', [('governing_capacity', 80)]),
   ('远洋护航', [('naval_morale', 0.12), ('heavy_ship_power', 0.10)])]),

 ('XJA', [('technology_cost', -0.08), ('development_cost', -0.08)], [('all_power_cost', -0.04)],
  [('星炬讲堂', [('institution_spread', 0.12)]),
   ('共鸣研究', [('build_cost', -0.08)]),
   ('学院工坊', [('production_efficiency', 0.10), ('global_tax_modifier', 0.08)]),
   ('学术声望', [('prestige', 0.8), ('diplomatic_reputation', 1)]),
   ('交换学者', [('global_trade_power', 0.10)]),
   ('学园产业', [('trade_efficiency', 0.08)]),
   ('护院卫队', [('land_morale', 0.08), ('discipline', 0.03)])]),

 ('MGZ', [('stability_cost_modifier', -0.12), ('global_unrest', -1)], [('tolerance_own', 1)],
  [('梦泽烟波', [('prestige', 0.8), ('diplomatic_reputation', 1)]),
   ('州府编户', [('global_tax_modifier', 0.12), ('governing_capacity', 80)]),
   ('织造之邦', [('production_efficiency', 0.12), ('trade_efficiency', 0.08)]),
   ('锁氏亲军', [('land_morale', 0.08), ('infantry_power', 0.08)]),
   ('泽国堤防', [('defensiveness', 0.15), ('max_hostile_attrition', 1)]),
   ('归化之策', [('core_creation', -0.12)]),
   ('梦州声望', [('manpower_recovery_speed', 0.10)])]),

 ('CXT', [('spy_offence', 0.20), ('land_morale', 0.08)], [('discipline', 0.04)],
  [('残星锐士', [('infantry_power', 0.12), ('cavalry_power', 0.08)]),
   ('暗潮渗透', [('siege_ability', 0.12)]),
   ('星屑回响', [('manpower_recovery_speed', 0.12), ('global_manpower_modifier', 0.08)]),
   ('不惜代价', [('war_exhaustion', -0.08)]),
   ('铁腕统御', [('global_unrest', -1.5), ('stability_cost_modifier', -0.08)]),
   ('疆域清算', [('core_creation', -0.12), ('prestige', 0.5)]),
   ('残星征召', [('land_forcelimit_modifier', 0.12)])]),

 ('FGL', [('global_manpower_modifier', 0.12), ('max_hostile_attrition', 1)], [('manpower_recovery_speed', 0.12)],
  [('林间伏兵', [('defensiveness', 0.18), ('land_morale', 0.08)]),
   ('守林游猎', [('infantry_power', 0.08)]),
   ('木寨工事', [('build_cost', -0.12)]),
   ('浮光木产', [('production_efficiency', 0.12), ('global_tax_modifier', 0.08)]),
   ('林贡之制', [('governing_capacity', 60)]),
   ('山林征召', [('land_forcelimit_modifier', 0.15)]),
   ('林誓之约', [('stability_cost_modifier', -0.12), ('global_unrest', -1)])]),

 ('FSL', [('naval_morale', 0.12), ('global_ship_trade_power', 0.12)], [('naval_forcelimit_modifier', 0.20)],
  [('重舰传统', [('heavy_ship_power', 0.12)]),
   ('海峡操练', [('recover_navy_morale_speed', 0.12), ('naval_combat_ability', 0.12)]),
   ('水手世家', [('sailors_recovery_speed', 0.12)]),
   ('香料航路', [('trade_efficiency', 0.12), ('global_trade_power', 0.10)]),
   ('远洋传承', [('navy_tradition_decay', -0.015)]),
   ('群岛商权', [('global_tax_modifier', 0.08)]),
   ('港务税关', [('production_efficiency', 0.10)])]),

 ('MTL', [('global_tax_modifier', 0.08), ('production_efficiency', 0.12)], [('trade_efficiency', 0.12)],
  [('家族金库', [('build_cost', -0.12)]),
   ('商会网络', [('global_trade_power', 0.15)]),
   ('城邦营造', [('development_cost', -0.08)]),
   ('名门声望', [('prestige', 0.8), ('diplomatic_reputation', 1)]),
   ('契约精神', [('stability_cost_modifier', -0.12), ('global_unrest', -1)]),
   ('私兵护卫', [('land_morale', 0.08), ('land_forcelimit_modifier', 0.08)]),
   ('外交联姻', [('governing_capacity', 60)])]),

 ('YHH', [('tolerance_own', 1), ('stability_cost_modifier', -0.12)], [('prestige', 1.0)],
  [('深海圣所', [('global_tax_modifier', 0.08), ('governing_capacity', 80)]),
   ('修会戒律', [('global_unrest', -1.5), ('land_morale', 0.08)]),
   ('海疆归化', [('core_creation', -0.12)]),
   ('圣殿卫队', [('discipline', 0.04), ('infantry_power', 0.08)]),
   ('教区治理', [('manpower_recovery_speed', 0.10)]),
   ('布道四方', [('diplomatic_reputation', 1), ('global_manpower_modifier', 0.08)]),
   ('虔诚之刃', [('cavalry_power', 0.08)])]),
]


def fmt(v):
    s = ('%.4f' % v).rstrip('0').rstrip('.')
    return s if s != '-0' else '0'


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


def main():
    os.makedirs(BK, exist_ok=True)
    rows = []
    for tag, start, bonus, ideas in N:
        p = os.path.join(MOD, 'common', 'ideas', '%s_ideas.txt' % tag)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
        open(p, 'w', encoding='utf-8', newline='\n').write(text(tag, start, bonus, ideas))
        allmods = [k for k, _ in start] + [k for k, _ in bonus] + [k for _, ml in ideas for k, _ in ml]
        dup = sorted({k for k in allmods if allmods.count(k) > 1})
        per = [len(ml) for _, ml in ideas]
        rows.append({'tag': tag, 'mods': len(allmods), 'uniq': len(set(allmods)),
                     'dup': dup, 'per_slot': per, 'start': len(start), 'bonus': len(bonus)})
        print('%-4s 修正=%-3d 唯一=%-3d 重复=%s 槽位=%s 传统=%d 野心=%d' %
              (tag, len(allmods), len(set(allmods)), dup or '无', per, len(start), len(bonus)))
    json.dump(rows, open(os.path.join(MOD, 'analysis', '_ideas_v3_report.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
