#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""鸣潮九国：批量生成 tag 注册 / 国家定义 / 国家历史 / 理念 / 本地化明文 / 旗帜。
约定：正式路径下的脚本一律 ASCII（可直接进游戏）；中文只落在 decode_localisation/（BLS 模式）。"""
import os, re, json, shutil

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
SRC_FLAGS = r'F:\SITU\东方风云设计理念\政府改革\ACG风云立绘\新国家'
BK = os.path.join(MOD, 'analysis', 'backup_新建国家_鸣潮九国_20261120')

UNITS = ['chinese_longspear', 'japanese_archer', 'chinese_footsoldier', 'japanese_samurai',
         'east_asian_spearmen', 'asian_arquebusier', 'asian_mass_infantry', 'asian_musketeer',
         'reformed_asian_musketeer', 'reformed_asian_cavalry', 'eastern_militia', 'indian_elephant',
         'steppe_riders', 'steppe_lancers', 'steppe_musketeers', 'steppe_cavalry',
         'eastern_knights', 'eastern_carabinier', 'eastern_uhlan', 'eastern_skirmisher']

N = [
 dict(tag='JZH', cn='今州', en='Jinzhou', flag='今州', color=(60, 200, 170), rev=(40, 170, 145),
      rank=2, cap=2710, mon='Xi', mon_cn='汐', dyn='Jin', dyn_cn='今',
      groups=['defensive_ideas', 'offensive_ideas', 'quality_ideas', 'administrative_ideas',
              'humanist_ideas', 'economic_ideas', 'trade_ideas', 'quantity_ideas'],
      start=[('land_morale', 0.10), ('defensiveness', 0.15)],
      bonus=[('infantry_power', 0.10)],
      ideas=[('玉京守望', [('production_efficiency', 0.10)]),
             ('今州铁壁', [('defensiveness', 0.20)]),
             ('鸣钟之律', [('stability_cost_modifier', -0.10)]),
             ('龙泉军工', [('build_cost', -0.10)]),
             ('潮汐军阵', [('discipline', 0.03)]),
             ('边地屯垦', [('manpower_recovery_speed', 0.10)]),
             ('岁主遗训', [('global_manpower_modifier', 0.10)])],
      adj='今州的', sname=['Jinzhou', 'Chaoyin'], lname=['Jiyan', 'Yangyang', 'Chixia', 'Sanhua']),
 dict(tag='LGN', cn='拉古那', en='Ragunna', flag='拉古那', color=(230, 150, 60), rev=(200, 120, 40),
      rank=2, cap=622, mon='Rosemary', mon_cn='罗斯玛丽', dyn='Fisalia', dyn_cn='翡萨烈',
      groups=['trade_ideas', 'diplomatic_ideas', 'economic_ideas', 'defensive_ideas',
              'quality_ideas', 'administrative_ideas', 'influence_ideas', 'quantity_ideas'],
      start=[('trade_efficiency', 0.10), ('global_trade_power', 0.10)],
      bonus=[('diplomatic_reputation', 1)],
      ideas=[('狂欢之港', [('production_efficiency', 0.10)]),
             ('商路辐辏', [('trade_efficiency', 0.10)]),
             ('群岛船团', [('global_ship_trade_power', 0.15)]),
             ('假面舞会', [('prestige', 0.5)]),
             ('剧院之城', [('build_cost', -0.10)]),
             ('金穗税制', [('global_tax_modifier', 0.05)]),
             ('远洋护航', [('naval_morale', 0.10)])],
      adj='拉古那的', sname=['Ragunna', 'Carnival'], lname=['Rosa', 'Lumi', 'Enzo', 'Vera']),
 dict(tag='XJA', cn='星炬学院', en='Xingju-Academy', flag='星炬学院', color=(170, 130, 230), rev=(140, 100, 200),
      rank=1, cap=2687, mon='Aemis', mon_cn='爱弥斯', dyn='Snowfox', dyn_cn='大雪绒',
      groups=['innovative_ideas', 'economic_ideas', 'administrative_ideas', 'humanist_ideas',
              'diplomatic_ideas', 'defensive_ideas', 'quality_ideas', 'trade_ideas'],
      start=[('technology_cost', -0.05), ('development_cost', -0.05)],
      bonus=[('all_power_cost', -0.05)],
      ideas=[('星炬讲堂', [('technology_cost', -0.05)]),
             ('共鸣研究', [('development_cost', -0.05)]),
             ('学院工坊', [('build_cost', -0.10)]),
             ('学术声望', [('prestige', 0.5)]),
             ('交换学者', [('diplomatic_reputation', 1)]),
             ('学园产业', [('global_tax_modifier', 0.05)]),
             ('护院卫队', [('land_morale', 0.05)])],
      adj='星炬学院的', sname=['Xingju', 'Torchlight'], lname=['Aemis', 'Ling', 'Baird', 'Nova']),
 dict(tag='MGZ', cn='梦州', en='Mengzhou', flag='梦州', color=(220, 130, 190), rev=(190, 100, 165),
      rank=2, cap=639, mon='Ming', mon_cn='暝', dyn='Suo', dyn_cn='锁',
      groups=['humanist_ideas', 'religious_ideas', 'administrative_ideas', 'economic_ideas',
              'defensive_ideas', 'offensive_ideas', 'trade_ideas', 'quantity_ideas'],
      start=[('stability_cost_modifier', -0.10), ('global_unrest', -1)],
      bonus=[('tolerance_own', 1)],
      ideas=[('梦泽烟波', [('prestige', 0.5)]),
             ('州府编户', [('global_tax_modifier', 0.05)]),
             ('织造之邦', [('production_efficiency', 0.10)]),
             ('锁氏亲军', [('land_morale', 0.05)]),
             ('泽国堤防', [('defensiveness', 0.15)]),
             ('归化之策', [('core_creation', -0.10)]),
             ('梦州声望', [('diplomatic_reputation', 1)])],
      adj='梦州的', sname=['Mengzhou', 'Misty'], lname=['Ming', 'Suo', 'Yan', 'Bai']),
 dict(tag='CXT', cn='残星会', en='Fractsidus', flag='残星会', color=(150, 40, 60), rev=(110, 25, 45),
      rank=1, cap=627, mon='Phrolova', mon_cn='弗洛洛', dyn='Fractsidus', dyn_cn='残星',
      groups=['espionage_ideas', 'offensive_ideas', 'quality_ideas', 'defensive_ideas',
              'administrative_ideas', 'influence_ideas', 'economic_ideas', 'quantity_ideas'],
      start=[('spy_offence', 0.15), ('land_morale', 0.05)],
      bonus=[('discipline', 0.03)],
      ideas=[('残星锐士', [('infantry_power', 0.10)]),
             ('暗潮渗透', [('siege_ability', 0.10)]),
             ('星屑回响', [('manpower_recovery_speed', 0.10)]),
             ('不惜代价', [('war_exhaustion', -0.05)]),
             ('铁腕统御', [('global_unrest', -1)]),
             ('疆域清算', [('core_creation', -0.10)]),
             ('残星征召', [('global_manpower_modifier', 0.10)])],
      adj='残星会的', sname=['Fractsidus', 'Duskstar'], lname=['Phrolova', 'Scar', 'Nyx', 'Rin']),
 dict(tag='FGL', cn='浮光林', en='Fuguanglin', flag='浮光林', color=(90, 170, 90), rev=(65, 140, 70),
      rank=1, cap=628, mon='Regent', mon_cn='摄政', dyn='Fuguang', dyn_cn='浮光',
      groups=['defensive_ideas', 'quantity_ideas', 'economic_ideas', 'administrative_ideas',
              'humanist_ideas', 'offensive_ideas', 'trade_ideas', 'religious_ideas'],
      start=[('global_manpower_modifier', 0.10), ('max_hostile_attrition', 1)],
      bonus=[('manpower_recovery_speed', 0.10)],
      ideas=[('林间伏兵', [('defensiveness', 0.20)]),
             ('守林游猎', [('land_morale', 0.05)]),
             ('木寨工事', [('build_cost', -0.10)]),
             ('浮光木产', [('production_efficiency', 0.10)]),
             ('林贡之制', [('global_tax_modifier', 0.05)]),
             ('山林征召', [('land_forcelimit_modifier', 0.10)]),
             ('林誓之约', [('stability_cost_modifier', -0.10)])],
      adj='浮光林的', sname=['Fuguang', 'Glowwood'], lname=['Lin', 'Ye', 'Mu', 'Qing']),
 dict(tag='FSL', cn='翡萨烈', en='Fisalia', flag='翡萨烈', color=(40, 90, 160), rev=(25, 70, 135),
      rank=2, cap=2681, mon='Regent', mon_cn='摄政', dyn='Fisalia', dyn_cn='翡萨烈',
      groups=['naval_ideas', 'trade_ideas', 'exploration_ideas', 'economic_ideas',
              'defensive_ideas', 'quality_ideas', 'diplomatic_ideas', 'administrative_ideas'],
      start=[('naval_morale', 0.10), ('global_ship_trade_power', 0.10)],
      bonus=[('naval_forcelimit_modifier', 0.20)],
      ideas=[('重舰传统', [('heavy_ship_power', 0.10)]),
             ('海峡操练', [('recover_navy_morale_speed', 0.10)]),
             ('水手世家', [('sailors_recovery_speed', 0.10)]),
             ('香料航路', [('trade_efficiency', 0.10)]),
             ('远洋传承', [('navy_tradition_decay', -0.01)]),
             ('群岛商权', [('global_trade_power', 0.10)]),
             ('港务税关', [('global_tax_modifier', 0.05)])],
      adj='翡萨烈的', sname=['Fisalia', 'Deepjade'], lname=['Fisalia', 'Maren', 'Corin', 'Tide']),
 dict(tag='MTL', cn='莫塔里', en='Montelli', flag='莫塔里', color=(140, 60, 90), rev=(110, 40, 70),
      rank=2, cap=2673, mon='Carlotta', mon_cn='珂莱塔', dyn='Montelli', dyn_cn='莫塔里',
      groups=['economic_ideas', 'trade_ideas', 'diplomatic_ideas', 'administrative_ideas',
              'defensive_ideas', 'quality_ideas', 'humanist_ideas', 'influence_ideas'],
      start=[('global_tax_modifier', 0.05), ('production_efficiency', 0.10)],
      bonus=[('trade_efficiency', 0.10)],
      ideas=[('家族金库', [('build_cost', -0.10)]),
             ('商会网络', [('global_trade_power', 0.10)]),
             ('城邦营造', [('development_cost', -0.05)]),
             ('名门声望', [('prestige', 0.5)]),
             ('契约精神', [('stability_cost_modifier', -0.10)]),
             ('私兵护卫', [('land_morale', 0.05)]),
             ('外交联姻', [('diplomatic_reputation', 1)])],
      adj='莫塔里的', sname=['Montelli', 'Goldmark'], lname=['Carlotta', 'Montelli', 'Enzo', 'Livia']),
 dict(tag='YHH', cn='隐海修会', en='OrderOfTheDeep', flag='隐海修会', color=(120, 200, 210), rev=(90, 175, 190),
      rank=3, cap=596, mon='Phoebe', mon_cn='菲比', dyn='Order', dyn_cn='隐海修会',
      groups=['religious_ideas', 'humanist_ideas', 'administrative_ideas', 'defensive_ideas',
              'economic_ideas', 'influence_ideas', 'quality_ideas', 'trade_ideas'],
      start=[('tolerance_own', 1), ('stability_cost_modifier', -0.10)],
      bonus=[('prestige', 1.0)],
      ideas=[('深海圣所', [('global_tax_modifier', 0.05)]),
             ('修会戒律', [('global_unrest', -1)]),
             ('海疆归化', [('core_creation', -0.10)]),
             ('圣殿卫队', [('land_morale', 0.05)]),
             ('教区治理', [('governing_capacity', 50)]),
             ('布道四方', [('diplomatic_reputation', 1)]),
             ('虔诚之刃', [('discipline', 0.03)])],
      adj='隐海修会的', sname=['Order', 'Deepsea'], lname=['Phoebe', 'Maren', 'Silas', 'Nia']),
]


def w(path, text, bom=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        shutil.copy2(path, os.path.join(BK, os.path.basename(path)))
    data = text.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    with open(path, 'wb') as f:
        f.write(data)


def countries_file(n):
    us = '\n'.join('\t' + u for u in UNITS)
    gr = '\n'.join('\t' + g for g in n['groups'])
    mn = '\n'.join('\t"%s #0" = %d' % (x, 60) for x in [n['mon']] + n['lname'])
    ln = ' '.join(n['lname'])
    sn = ' '.join('"%s"' % s for s in n['sname'])
    return f"""#{n['en']} (Wuthering Waves) - {n['cn']}

graphical_culture = acggfx

color = {{ {n['color'][0]} {n['color'][1]} {n['color'][2]} }}

random_nation_chance = 0

historical_score = 0

revolutionary_colors = {{ {n['rev'][0]} {n['rev'][1]} {n['rev'][2]} }}

historical_idea_groups = {{
{gr}
}}

historical_units = {{
{us}
}}

monarch_names = {{
{mn}
}}

leader_names = {{
	{ln}
}}

ship_names = {{
	{sn}
}}
"""


def history_file(n):
    return f"""# {n['en']} - {n['cn']}
government = acg_monarchy
add_government_reform = acg_universal_government_reform_1
government_rank = {n['rank']}
primary_culture = acg_wuthering_waves
religion = acg
technology_group = chinese
capital = {n['cap']}

1444.11.11 = {{
	monarch = {{
		name = "{n['mon']}"
		dynasty = "{n['dyn']}"
		birth_date = 1400.1.1
		death_date = 1821.12.31
		adm = 4
		dip = 5
		mil = 4
		female = yes
	}}
	add_ruler_personality = immortal_personality
	add_ruler_personality = scholar_personality
	add_ruler_personality = calm_personality
}}
"""


def ideas_file(n):
    def mods(lst, ind='\t\t'):
        return '\n'.join('%s%s = %s' % (ind, k, v) for k, v in lst)
    body = []
    for i, (cn, ml) in enumerate(n['ideas'], 1):
        body.append('\t%s_idea_%d = {\n%s\n\t}' % (n['tag'], i, mods(ml)))
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
""" % (n['tag'], mods(n['start']), mods(n['bonus']), n['tag'], '\n'.join(body))


def loc_file(n):
    out = ['l_english:', '']
    out.append(' %s: "%s"' % (n['tag'], n['cn']))
    out.append(' %s_ADJ: "%s"' % (n['tag'], n['adj']))
    out.append(' %s_ADJ2: "%s"' % (n['tag'], n['adj']))
    out.append(' %s_ideas: "%s理念"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_start: "%s传统"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_start_desc: "%s立国之初便已凝结的传统。"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_bonus: "%s野心"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_bonus_desc: "%s理念浑然一体之时，便是其真正野心显形之日。"' % (n['tag'], n['cn']))
    for i, (cn, ml) in enumerate(n['ideas'], 1):
        out.append(' %s_idea_%d: "%s"' % (n['tag'], i, cn))
        out.append(' %s_idea_%d_desc: "%s。这一条被后世写入%s的国史。"' % (n['tag'], i, cn, n['cn']))
    return '\n'.join(out) + '\n'


def country_plain_history(n):
    return f"""# {n['en']} - {n['cn']}
government = acg_monarchy
add_government_reform = acg_universal_government_reform_1
government_rank = {n['rank']}
primary_culture = acg_wuthering_waves
religion = acg
technology_group = chinese
capital = {n['cap']}

1444.11.11 = {{
	monarch = {{
		name = "{n['mon_cn']}"
		dynasty = "{n['dyn_cn']}"
		birth_date = 1400.1.1
		death_date = 1821.12.31
		adm = 4
		dip = 5
		mil = 4
		female = yes
	}}
	add_ruler_personality = immortal_personality
	add_ruler_personality = scholar_personality
	add_ruler_personality = calm_personality
}}
"""


def countries_plain(n):
    """common/countries 的中文明文版（人名池换成中文，其余同正式版）。"""
    us = '\n'.join('\t' + u for u in UNITS)
    gr = '\n'.join('\t' + g for g in n['groups'])
    mn = '\n'.join('\t"%s #0" = %d' % (x, 60) for x in [n['mon_cn']] + n['lname'])
    ln = ' '.join(n['lname'])
    sn = ' '.join('"%s"' % s for s in n['sname'])
    return f"""#{n['en']} (Wuthering Waves) - {n['cn']}

graphical_culture = acggfx

color = {{ {n['color'][0]} {n['color'][1]} {n['color'][2]} }}

random_nation_chance = 0

historical_score = 0

revolutionary_colors = {{ {n['rev'][0]} {n['rev'][1]} {n['rev'][2]} }}

historical_idea_groups = {{
{gr}
}}

historical_units = {{
{us}
}}

monarch_names = {{
{mn}
}}

leader_names = {{
	{ln}
}}

ship_names = {{
	{sn}
}}
"""


def main():
    os.makedirs(BK, exist_ok=True)
    log = []

    # P1 tag 注册（追加）
    tag_path = os.path.join(MOD, 'common', 'country_tags', 'ACG_MEC_E_country_tag.txt')
    cur = open(tag_path, encoding='utf-8').read()
    add = ''
    for n in N:
        line = '%s = "countries/%s.txt" #%s' % (n['tag'], n['en'], n['cn'])
        if n['tag'] + ' =' not in cur:
            add += line + '\n'
    if add:
        shutil.copy2(tag_path, os.path.join(BK, 'ACG_MEC_E_country_tag.txt'))
        if not cur.endswith('\n'):
            cur += '\n'
        open(tag_path, 'w', encoding='utf-8', newline='\n').write(cur + add)
        log.append('tag: +%d' % add.count('\n'))

    for n in N:
        w(os.path.join(MOD, 'common', 'countries', n['en'] + '.txt'), countries_file(n))
        w(os.path.join(MOD, 'history', 'countries', '%s - %s.txt' % (n['tag'], n['en'])), history_file(n))
        w(os.path.join(MOD, 'common', 'ideas', '%s_ideas.txt' % n['tag']), ideas_file(n))
        w(os.path.join(MOD, 'decode_localisation', '%s_l_english.yml' % n['tag']), loc_file(n))
        w(os.path.join(MOD, 'decode_localisation', 'history', n['en'] + '.txt'), countries_plain(n))
        w(os.path.join(MOD, 'decode_localisation', 'history', '%s - %s.txt' % (n['tag'], n['en'])),
          country_plain_history(n))
        log.append('%s ok' % n['tag'])

    print('\n'.join(log))


if __name__ == '__main__':
    main()
