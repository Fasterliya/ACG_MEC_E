# -*- coding: utf-8 -*-
"""九国理念强化（每条 2-3 条修正，传统 2 条、野心 1 条）+ 本地化明文重写 + LGN.tga -> RGU.tga"""
import os, re, shutil

MOD = r'F:\Paradox Interactive\Europa Universalis IV\mod\ACG_MEC_E'
BK = os.path.join(MOD, 'analysis', 'backup_ideas_v2_20261120')

# (国家, 理念: [(名称, [(modifier, 值)...], 描述)...])
N = [
 dict(tag='JZH', cn='今州',
      start=[('land_morale', 0.15), ('defensiveness', 0.20)],
      bonus=[('infantry_power', 0.10)],
      ideas=[
        ('玉京守望', [('production_efficiency', 0.15), ('build_cost', -0.10)],
         '玉京的城墙下，工匠与农人各自守着一截工事。今州的秩序从不是靠一个人撑起来的。'),
        ('今州铁壁', [('defensiveness', 0.25), ('max_hostile_attrition', 2)],
         '凡入今州者，都要先过城门。城墙一寸寸夯起来，也一寸寸记住了倒在这里的人。'),
        ('鸣钟之律', [('stability_cost_modifier', -0.15), ('global_unrest', -1)],
         '钟声一响，市集开、城门闭、兵甲归位。今州人用一口钟管住了整座城的脾气。'),
        ('龙泉军工', [('build_cost', -0.15), ('artillery_power', 0.10)],
         '龙泉的炉火昼夜不熄。从这里出去的刀、甲、铳，从不将就。'),
        ('潮汐军阵', [('discipline', 0.05), ('land_morale', 0.10)],
         '今州的兵在潮水边练兵。潮起则进，潮落则守，敌人的节奏由海来定。'),
        ('边地屯垦', [('manpower_recovery_speed', 0.15), ('global_manpower_modifier', 0.15)],
         '边地不只有戍卒，还有犁。仓廪满了，才轮得到谈守边。'),
        ('岁主遗训', [('land_forcelimit_modifier', 0.15), ('core_creation', -0.10)],
         '岁主留下的话只有一句：地可以失，人不能散。今州历代的征召令，都从这句里来。'),
      ]),
 dict(tag='RGU', cn='拉古那',
      start=[('trade_efficiency', 0.15), ('global_trade_power', 0.15)],
      bonus=[('diplomatic_reputation', 2)],
      ideas=[
        ('狂欢之港', [('production_efficiency', 0.15), ('global_tax_modifier', 0.10)],
         '港口的锣鼓一年到头不歇。拉古那人把生意做成了节日，又把节日做成了生意。'),
        ('商路辐辏', [('trade_efficiency', 0.15), ('global_ship_trade_power', 0.20)],
         '从海峡到内海，每一条航路的终点都是拉古那的码头。'),
        ('群岛船团', [('global_ship_trade_power', 0.20), ('naval_forcelimit_modifier', 0.20)],
         '拉古那的船从不单独出海。船团一起走，货一起卖，遇上风浪一起沉——所以从不沉。'),
        ('假面舞会', [('prestige', 1.0), ('diplomatic_reputation', 1)],
         '面具之下才能说真话。拉古那的盟约，多半是在舞池边谈成的。'),
        ('剧院之城', [('build_cost', -0.15), ('development_cost', -0.10)],
         '拉古那的剧院比军械库大。这里的名声，是一场场戏攒出来的。'),
        ('金穗税制', [('global_tax_modifier', 0.10), ('production_efficiency', 0.10)],
         '税单写得比账本还细。商人不恨它，因为它算得清。'),
        ('远洋护航', [('naval_morale', 0.15), ('heavy_ship_power', 0.15)],
         '自家的船自家护。拉古那的护航队从不等别人来救命。'),
      ]),
 dict(tag='XJA', cn='星炬学院',
      start=[('technology_cost', -0.10), ('development_cost', -0.10)],
      bonus=[('all_power_cost', -0.05)],
      ideas=[
        ('星炬讲堂', [('technology_cost', -0.10), ('institution_spread', 0.15)],
         '讲堂的灯整夜亮着。学院相信，答案总在下一次试验里。'),
        ('共鸣研究', [('development_cost', -0.10), ('build_cost', -0.10)],
         '把声音拆开再拼回去——学院用这种方式理解世界，也用来改进它的机器。'),
        ('学院工坊', [('production_efficiency', 0.10), ('global_tax_modifier', 0.10)],
         '图纸画到第三稿才准开工。慢，但一次就对。'),
        ('学术声望', [('prestige', 1.0), ('diplomatic_reputation', 1)],
         '别的国家送子弟来求学，带来的不只是学费，还有敬意。'),
        ('交换学者', [('technology_cost', -0.05), ('prestige', 0.5)],
         '学院的门对所有人开，只要他带得动一个问题。'),
        ('学园产业', [('global_tax_modifier', 0.10), ('trade_efficiency', 0.10)],
         '实验室旁边就是作坊。学问落地成货，货换回经费，经费再养学问。'),
        ('护院卫队', [('land_morale', 0.10), ('discipline', 0.05)],
         '学院不养大军，但护院的人个个知道自己守的是什么。'),
      ]),
 dict(tag='MGZ', cn='梦州',
      start=[('stability_cost_modifier', -0.15), ('global_unrest', -1)],
      bonus=[('tolerance_own', 1)],
      ideas=[
        ('梦泽烟波', [('prestige', 1.0), ('diplomatic_reputation', 1)],
         '梦州的名声像雾，看不清，却到处都在。'),
        ('州府编户', [('global_tax_modifier', 0.15), ('governing_capacity', 100)],
         '州府的册子上写着每一户、每一亩。梦州靠这个把水乡管成了国。'),
        ('织造之邦', [('production_efficiency', 0.15), ('trade_efficiency', 0.10)],
         '梦州的织机声比更鼓还密。一匹锦，换一年太平。'),
        ('锁氏亲军', [('land_morale', 0.10), ('infantry_power', 0.10)],
         '锁氏的亲军不从外姓里招。他们守的不是国，是家门。'),
        ('泽国堤防', [('defensiveness', 0.20), ('max_hostile_attrition', 1)],
         '堤一决，半个梦州就没了。所以修堤的钱，谁也不敢省。'),
        ('归化之策', [('core_creation', -0.15), ('tolerance_own', 1)],
         '梦州不急着改别人的风俗，先让人吃饱，再谈别的。'),
        ('梦州声望', [('diplomatic_reputation', 2), ('prestige', 0.5)],
         '梦州的使节走到哪里，都有人愿意先听他说完。'),
      ]),
 dict(tag='CXT', cn='残星会',
      start=[('spy_offence', 0.25), ('land_morale', 0.10)],
      bonus=[('discipline', 0.05)],
      ideas=[
        ('残星锐士', [('infantry_power', 0.15), ('discipline', 0.05)],
         '残星会挑人只看一件事：敢不敢在最前面站住。'),
        ('暗潮渗透', [('siege_ability', 0.15), ('spy_offence', 0.20)],
         '城还没围上，城门已经在里面开了。残星会向来这么打仗。'),
        ('星屑回响', [('manpower_recovery_speed', 0.15), ('global_manpower_modifier', 0.10)],
         '残星会从不浪费一具尸体，也不浪费一个活人。'),
        ('不惜代价', [('war_exhaustion', -0.10), ('land_morale', 0.10)],
         '残星会的军令里没有「撤退」，只有「值不值」。'),
        ('铁腕统御', [('global_unrest', -2), ('stability_cost_modifier', -0.10)],
         '恐惧是最省钱的税。残星会算得很清楚。'),
        ('疆域清算', [('core_creation', -0.15), ('prestige', 0.5)],
         '打下来的地要清得干净，残星会从来不留旧账。'),
        ('残星征召', [('global_manpower_modifier', 0.15), ('land_forcelimit_modifier', 0.15)],
         '残星会征兵不问出身，只问能活几天。'),
      ]),
 dict(tag='FGL', cn='浮光林',
      start=[('global_manpower_modifier', 0.15), ('max_hostile_attrition', 1)],
      bonus=[('manpower_recovery_speed', 0.15)],
      ideas=[
        ('林间伏兵', [('defensiveness', 0.25), ('land_morale', 0.10)],
         '浮光林的兵不列阵，他们趴着。等敌人走进林子，仗就打完了。'),
        ('守林游猎', [('infantry_power', 0.10), ('land_morale', 0.05)],
         '在林子里，猎人和兵的差别只在于猎什么。'),
        ('木寨工事', [('build_cost', -0.15), ('defensiveness', 0.10)],
         '浮光林不修石城，只修木寨。木头会烂，但修得比石头快。'),
        ('浮光木产', [('production_efficiency', 0.15), ('global_tax_modifier', 0.10)],
         '林子里出的东西不多，但每一样别人都缺。'),
        ('林贡之制', [('global_tax_modifier', 0.10), ('governing_capacity', 50)],
         '林贡收得不重，但从不间断。浮光林靠这个养住了整片山。'),
        ('山林征召', [('land_forcelimit_modifier', 0.20), ('global_manpower_modifier', 0.10)],
         '号角一响，猎户放下弓就来。他们本来就住在战场上。'),
        ('林誓之约', [('stability_cost_modifier', -0.15), ('global_unrest', -1)],
         '浮光林的人不立契，只立誓。誓一立，几代人都认。'),
      ]),
 dict(tag='FSL', cn='翡萨烈',
      start=[('naval_morale', 0.15), ('global_ship_trade_power', 0.15)],
      bonus=[('naval_forcelimit_modifier', 0.25)],
      ideas=[
        ('重舰传统', [('heavy_ship_power', 0.15), ('naval_morale', 0.10)],
         '翡萨烈的船厂只造大船。小船护不住航道，也护不住脸面。'),
        ('海峡操练', [('recover_navy_morale_speed', 0.15), ('naval_combat_ability', 0.15)],
         '海峡里的每一道暗流，翡萨烈的舵手都背得下来。'),
        ('水手世家', [('sailors_recovery_speed', 0.15), ('naval_forcelimit_modifier', 0.15)],
         '翡萨烈的水手是生下来的，不是招来的。'),
        ('香料航路', [('trade_efficiency', 0.15), ('global_trade_power', 0.15)],
         '从产地到港口，翡萨烈人自己走完全程，不让中间人碰一手。'),
        ('远洋传承', [('navy_tradition_decay', -0.02), ('naval_morale', 0.10)],
         '老船长退了也不下船，坐在船尾教下一辈看星。'),
        ('群岛商权', [('global_ship_trade_power', 0.20), ('global_tax_modifier', 0.10)],
         '翡萨烈的商旗插在每一个能停船的礁上。'),
        ('港务税关', [('global_tax_modifier', 0.15), ('production_efficiency', 0.10)],
         '港口收的每一文钱，都记着它从哪条船上来。'),
      ]),
 dict(tag='MTL', cn='莫塔里',
      start=[('global_tax_modifier', 0.10), ('production_efficiency', 0.15)],
      bonus=[('trade_efficiency', 0.15)],
      ideas=[
        ('家族金库', [('build_cost', -0.15), ('global_tax_modifier', 0.10)],
         '莫塔里的金库不在地窖里，在账本上。'),
        ('商会网络', [('global_trade_power', 0.20), ('trade_efficiency', 0.10)],
         '莫塔里的商会横跨数国，货没到，消息先到。'),
        ('城邦营造', [('development_cost', -0.10), ('build_cost', -0.10)],
         '城是一砖一瓦买下来的，所以每一块都算得清。'),
        ('名门声望', [('prestige', 1.0), ('diplomatic_reputation', 1)],
         '莫塔里的名字本身就是抵押品，比任何契约都硬。'),
        ('契约精神', [('stability_cost_modifier', -0.15), ('global_unrest', -1)],
         '签了就是签了。莫塔里从不毁约——毁约比赔钱贵。'),
        ('私兵护卫', [('land_morale', 0.10), ('land_forcelimit_modifier', 0.10)],
         '商队自己带枪。护得住货，才谈得上做买卖。'),
        ('外交联姻', [('diplomatic_reputation', 2), ('prestige', 0.5)],
         '莫塔里的婚事都是生意，而且是做成了的生意。'),
      ]),
 dict(tag='YHH', cn='隐海修会',
      start=[('tolerance_own', 1), ('stability_cost_modifier', -0.15)],
      bonus=[('prestige', 1.5)],
      ideas=[
        ('深海圣所', [('global_tax_modifier', 0.10), ('governing_capacity', 100)],
         '修会的圣所建在潮水边。信徒说，海听得见誓言。'),
        ('修会戒律', [('global_unrest', -2), ('land_morale', 0.10)],
         '修会的规矩不多，但破一条就再没有第二次机会。'),
        ('海疆归化', [('core_creation', -0.15), ('tolerance_own', 1)],
         '修会不烧神庙，只把新神像摆在旧神像旁边。过两代，人就忘了区别。'),
        ('圣殿卫队', [('discipline', 0.05), ('infantry_power', 0.10)],
         '圣殿卫队守的不是墙，是门。门开了，墙就没意义了。'),
        ('教区治理', [('governing_capacity', 150), ('global_tax_modifier', 0.05)],
         '每一个渔村都有一个执事。修会的手，比任何官府都长。'),
        ('布道四方', [('diplomatic_reputation', 2), ('prestige', 0.5)],
         '修会的船队走到哪里，经就念到哪里。'),
        ('虔诚之刃', [('discipline', 0.05), ('land_morale', 0.10)],
         '修会的剑上刻着祷词。他们说，砍下去的时候神听得见。'),
      ]),
]


def ideas_text(n):
    def blk(lst):
        return '\n'.join('\t\t%s = %s' % (k, v) for k, v in lst)
    body = []
    for i, (nm, ml, ds) in enumerate(n['ideas'], 1):
        body.append('\t%s_idea_%d = {\n%s\n\t}' % (n['tag'], i, blk(ml)))
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
""" % (n['tag'], blk(n['start']), blk(n['bonus']), n['tag'], '\n'.join(body))


def loc_block(n):
    out = []
    out.append(' %s: "%s"' % (n['tag'], n['cn']))
    out.append(' %s_ADJ: "%s的"' % (n['tag'], n['cn']))
    out.append(' %s_ADJ2: "%s的"' % (n['tag'], n['cn']))
    out.append(' %s_ideas: "%s理念"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_start: "%s传统"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_start_desc: "%s立国之初便已凝结的传承。"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_bonus: "%s野心"' % (n['tag'], n['cn']))
    out.append(' %s_ideas_bonus_desc: "%s理念浑然一体之时，便是其真正野心显形之日。"' % (n['tag'], n['cn']))
    for i, (nm, ml, ds) in enumerate(n['ideas'], 1):
        out.append(' %s_idea_%d: "%s"' % (n['tag'], i, nm))
        out.append(' %s_idea_%d_desc: "%s"' % (n['tag'], i, ds))
    return out


def main():
    os.makedirs(BK, exist_ok=True)
    log = []
    for n in N:
        p = os.path.join(MOD, 'common', 'ideas', '%s_ideas.txt' % n['tag'])
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(BK, os.path.basename(p)))
        open(p, 'w', encoding='utf-8', newline='\n').write(ideas_text(n))
        log.append('%s ideas 重写' % n['tag'])

    # 本地化明文（整份重建）
    lines = ['l_english:', '']
    for n in N:
        lines.append(' # ===== %s %s =====' % (n['tag'], n['cn']))
        lines.append('')
        lines.extend(loc_block(n))
        lines.append('')
    lp = os.path.join(MOD, 'decode_localisation', 'acg_wuthering_nine_l_english.yml')
    shutil.copy2(lp, os.path.join(BK, 'acg_wuthering_nine_l_english.yml'))
    open(lp, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines).rstrip() + '\n')
    log.append('loc 明文重建')

    # LGN.tga -> RGU.tga
    src = os.path.join(MOD, 'gfx', 'flags', 'LGN.tga')
    dst = os.path.join(MOD, 'gfx', 'flags', 'RGU.tga')
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(src)
        else:
            os.rename(src, dst)
        log.append('gfx/flags/LGN.tga -> RGU.tga')

    # 同步工作台
    stage = os.path.join(MOD, 'analysis', 'to_encode_20261120')
    if os.path.isdir(stage):
        shutil.copy2(lp, os.path.join(stage, 'localisation', 'acg_wuthering_nine_l_english.yml'))
        log.append('工作台 loc 副本同步')

    print('\n'.join(log))


if __name__ == '__main__':
    main()
