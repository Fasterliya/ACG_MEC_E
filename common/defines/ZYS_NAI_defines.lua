NDefines.NAI.ACCEPTABLE_BALANCE_DEFAULT = 0.65  ------ai决战倾向
NDefines.NAI.ACCEPTABLE_BALANCE_FRIEND_IN_COMBAT = 0.55   --------优势高于此值ai就会支援战斗
NDefines.NAI.ACCEPTABLE_BALANCE_MULT_FRIEND_IN_COMBAT = 0.3
NDefines.NAI.ACCEPTABLE_BALANCE_MULT_OFFENSIVE = 0.5 --	除非战斗中的盟友已经补充
NDefines.NAI.ACCEPTABLE_BALANCE_THREAT_WEIGHT = 0.6 --威胁开战的接受权重
NDefines.NAI.INVASION_ARMY_LOOKUP_INTERVAL_ON_FAILURE = 12   ------如果ai找不到入侵的军队，它会在几天内再次尝试
NDefines.NAI.INVADING_MAX_AWAY_RATIO = 0.45   ---------AI不会派遣超过这个比例的军队去入侵，并且会把剩余的军队留在已占领地区或本国待命
NDefines.NAI.REGION_PLANNING_HOMELAND_PRIORIZATION = 25.0  ----在向地区分配军队时，国土优先（仅在实际受到威胁时适用）
NDefines.NAI.MIN_FORCE_LIMIT_SHARE_REGION_ASSIGN = 0.2  ---AI只会将更大的军队分配到一个地区
NDefines.NAI.BORDER_DISTANCE_SCORE_IMPACT = 12   ----------省份距离对省份评价的影响（不明所以）
NDefines.NAI.IMPORANT_PROVINCE_THRESHOLD = 0.03   ---------ai保卫省份的最低发展度占比
NDefines.NAI.ARMY_DISTANCE_SCORE_IMPACT	= 0.5  ---陆军<->省距离对省评价的影响  （看不懂）
NDefines.NAI.PURSUE_DISTANCE = 95.0  ----AI不会追击撤退到更远省份的军队。
--NDefines.NAI.FORCE_COMPOSITION_CHANGE_TECH_LEVEL = 16 --在达到此科技等级时，AI将会使其炮兵的比例翻一番
NDefines.NAI.CONQUEST_INTEREST_DISTANCE = 75  --超出这个范围，AI对征服省份的兴趣就不大了。
NDefines.NAI.ASSIMILATION_INTEREST_AMOUNT_FACTOR = 100.0 -- 剩下的省份数量对征服兴趣的影响
NDefines.NAI.INVADING_BRAVERY = 1.2 --如果（防御者实力）/（入侵者实力）>INVADING_BRAVERY，AI将不会试图进行海上入侵。
--
NDefines.NAI.MAX_TASKS_NEW_REGION_ASSIGN_ALGORITHM = 50 --在新的区域分配算法中使用的最大任务量
NDefines.NAI.MAX_ARMIES_NEW_REGION_ASSIGN_ALGORITHM = 40 --在新的区域分配算法中使用的最大军队数量
--
NDefines.NAI.BASE_CAN_MAKE_CORE_DESIRE_TO_RETURN_PROVINCE = 15
--
NDefines.NAI.NOMINAL_ARMY_SIZE_MULTIPLIER = 1.15
NDefines.NAI.FORT_CAPITAL_DESIRE = 100.0
--
NDefines.NAI.VASSAL_FABRICATE_CLAIMS = 1  -------ai造宣称开关
--
NDefines.NAI.PEACE_HIGH_WAR_EXHAUSTION_FACTOR = 7  ---------高厌战带来的额外投降倾向
NDefines.NAI.PEACE_DESPERATION_FACTOR = 80   --------占地带来的ai和谈意愿
NDefines.NAI.PEACE_WAR_EXHAUSTION_FACTOR = 2.5  ----------厌战带来的和谈意愿
NDefines.NAI.PEACE_EXCESSIVE_DEMANDS_FACTOR = 0.025   --------AI不愿意投降，因为要求的东西比你的战争分数更多（改高了会溢出，10分吃100分的那种）
NDefines.NAI.PEACE_TIME_MONTHS = 24   -------AI在一场战争中顽固的时间
NDefines.NAI.PEACE_WAR_DIRECTION_FACTOR = 0.33   ---------取得优势时ai和谈意愿
NDefines.NAI.PEACE_WARGOAL_FACTOR = 5.0   --------战争目标带来的和谈意愿
NDefines.NAI.PEACE_BASE_RELUCTANCE = 0    ---------ai和谈基础不情愿值
NDefines.NAI.PEACE_ALLY_WAR_EXHAUSTION_MULT = 1.5  -----------盟友强度对和谈意愿的影响
NDefines.NAI.PEACE_HIGH_WAR_EXHAUSTION_THRESHOLD = 4.0  ------高厌战带来的和谈意愿
NDefines.NAI.PEACE_WAR_DIRECTION_WINNING_MULT = 7  -------增加AI对战争方向的重视，如果它是取得胜利的一方。
NDefines.NAI.PEACE_TIME_LATE_FACTOR = 6  -----------战争热情结束后ai的和谈意愿会乘以这个值
NDefines.NAI.PEACE_CALL_FOR_PEACE_FACTOR = 0  -------呼吁和平对ai和谈意愿的影响
NDefines.NAI.PEACE_STALLED_WAR_TIME_FACTOR = 0.5  --------战争持续时间对战争热情的影响
NDefines.NAI.PEACE_TIME_EARLY_FACTOR = 0.75 --在几个月的固执中，时间流逝的影响会成倍增加。
--NDefines.NAI.PEACE_TERMS_BASE_SCORE = 20 --任何和平需求的基础AI得分。
NDefines.NAI.PEACE_ALLY_TIME_MULT = 1.2 --在战争中为盟友增加 PEACE_TIME_FACTOR
NDefines.NAI.PEACE_TERMS_MIN_SCORE = 0.85  --	'AI "不想要 "得到比这更低分数的和平条约（由AI个性修改）
--
NDefines.NAI.PEACE_TERMS_STRATEGY_MULT = 0.75 --AI对战争目标的渴望，如果不符合他们的总体战略，就会成倍地增加。
NDefines.NAI.PEACE_RANDOM_FACTOR = 0 --对AI加权的随机性有多大（作为目标分数的一部分）。
NDefines.NAI.PEACE_TERMS_PROVINCE_ISOLATED_CAPITAL_MULT = 1.01 --如果一个省是首都的话，AI对它的渴望（拿下它的成本会更高一点）
NDefines.NAI.PEACE_TERMS_RETURN_CORES_VASSAL_MULT = 10.0 --AI对回归核心省份的渴望，对他们的附庸来说是成倍增加的。
--
NDefines.NAI.PEACE_TERMS_TRANSFER_VASSAL_MAX_MULT = 1 --	AI最大转移附庸倾向乘于这个。
NDefines.NAI.PEACE_TERMS_CB_MULT = 5  --------ai达成战争目标的倾向
NDefines.NAI.PEACE_TERMS_PROVINCE_WARGOAL_MULT = 10  ----------ai攻击目标地的倾向
NDefines.NAI.PEACE_TERMS_PROVINCE_CORE_MULTT = 15   ----------ai收核倾向
NDefines.NAI.PEACE_TERMS_INDEPENDENCE_BASE_MULT = 150.0 ----------和谈独立倾向
NDefines.NAI.PEACE_TERMS_CHANGE_RELIGION_BASE_MULT = 1.0  --------强迫改教倾向
NDefines.NAI.PEACE_TERMS_ANNEX_BASE_MULT = 200.0  ----全吃倾向
NDefines.NAI.PEACE_TERMS_PILLAGE_CAPITAL_MULT = 0    ----劫掠首都倾向
--NDefines.NAI.PEACE_TERMS_PROVINCE_BASE_MULT = 2.5   ----吃地倾向
NDefines.NAI.PEACE_TERMS_HUMILIATE_BASE_MULT = 1  ----羞辱倾向
NDefines.NAI.PEACE_TERMS_REVOKE_CORES_BASE_MULT = 0.05  ----消核倾向
NDefines.NAI.PEACE_TERMS_REVOKE_REFORM_BASE_MULT = 0.5  -----撤销改革倾向
NDefines.NAI.PEACE_TERMS_RETURN_CORES_BASE_MULT = 1   ------还地倾向
--NDefines.NAI.PEACE_TERMS_RELEASE_VASSALS_BASE_MULT = 1  ---吐狗倾向
NDefines.NAI.PEACE_TERMS_TRANSFER_VASSALS_BASE_MULT = 1.25  -----ntr倾向
--NDefines.NAI.PEACE_TERMS_RELEASE_ANNEXED_BASE_MULT = 0.85  ---吐地倾向
NDefines.NAI.PEACE_TERMS_ANNUL_TREATIES_BASE_MULT = 0.8  ----断条约倾向
NDefines.NAI.PEACE_TERMS_GOLD_BASE_MULT = 0.1  ----AI在和平条约中索取金币的权重修正
NDefines.NAI.PEACE_TERMS_GIVE_UP_CLAIM = 0.01  ---放弃宣称倾向
NDefines.NAI.PEACE_TERMS_GIVE_UP_CLAIM_PERMANENT = 0.05  ----同上
NDefines.NAI.PEACE_TERMS_CONCEDE_DEFEAT_BASE_MULT = 0.01  ------认输倾向
NDefines.NAI.PEACE_TERMS_ENFORCE_REBEL_DEMANDS_BASE_MULT = 1.0  ----强迫向叛军投降倾向
NDefines.NAI.PEACE_TERMS_TRIBUTARY_BASE_MULT = 0.01  ------收狗倾向
NDefines.NAI.PEACE_TERMS_PROVINCE_IMPERIAL_LIBERATION_MULT = 0.5  ---解放伪罗省份
--NDefines.NAI.PEACE_TERMS_PROVINCE_NO_CB_MULT = 0.8   -----如果一个省份没有有效的cb(只在兼并没有应用到核心时使用)，那么AI对该省的渴望就会乘以这个。
NDefines.NAI.PEACE_TERMS_PROVINCE_CORE_MULT = 4  ----ai割核心倾向
NDefines.NAI.PEACE_TERMS_PROVINCE_CLAIM_MULT = 3   ----割宣称倾向
NDefines.NAI.PEACE_TERMS_PROVINCE_NOT_CULTURE_MULT = 0.6  -----割异文化地倾向
--NDefines.NAI.PEACE_TERMS_PROVINCE_VASSAL_MULT = 0.9  ---如果一个省属于他们的附属国，而不是他们自己，那么ai对一个省的渴望就会成倍增加。
--NDefines.NAI.PEACE_TERMS_PROVINCE_REAL_ADJACENT_MULT = 2  ----对于每个拥有的相邻省份，ai对一个省份的渴望会增加这个乘数。
--NDefines.NAI.PEACE_TERMS_PROVINCE_NOT_ADJACENT_MULT = 0.05  ----如果一个省份完全不相邻(包括附属国和其他省份在和平状态下被占领)，那么ai对一个省份的渴望就会成倍增加。
--NDefines.NAI.PEACE_TERMS_PROVINCE_NO_INTEREST_MULT = 0.25  ----如果一个省份不在征服名单上，人工智能对这个省份的渴望就会成倍增加。
NDefines.NAI.PEACE_TERMS_PROVINCE_OVEREXTENSION_MIN_MULT = 1  --------如果有99%的过度扩展(不应用于核心)，AI对一个省份的渴望就会乘以这个。
NDefines.NAI.PEACE_TERMS_PROVINCE_OVEREXTENSION_MAX_MULT = 5  -----------如果省份有0%的过度扩展(不应用于核心)，那么AI对省份的渴望就会乘以这个。
NDefines.NAI.PEACE_TERMS_PROVINCE_ALLY_MULT = 0.75  ----ai希望把(非核心)省份给盟友。
NDefines.NAI.PEACE_TERMS_PROVINCE_IMPORTANT_ALLY_MULT = 2  ----ai希望把自己承诺拥有土地的省份给盟友。
NDefines.NAI.PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.03   ---在共享节点中，每0.1个交易价值，人工智能转移贸易权力的愿望就会乘以这个。
NDefines.NAI.PEACE_TERMS_TRADE_POWER_VALUE_MAX = 0.1  ----最大AI从共享节点价值转移交易权力的愿望。
NDefines.NAI.PEACE_TERMS_TRADE_POWER_NO_TRADE_INTEREST_MULT = 0.0  ---如果ai不是一个商共，转移贸易权力的愿望就会成倍增加
NDefines.NAI.PEACE_TERMS_PROVINCE_HRE_UNJUSTIFIED_MULT = 1  ----ai吃伪罗地的倾向
NDefines.NAI.PEACE_TERMS_MIN_MONTHS_OF_GOLD = 10  ---如果ai没有这么多的钱，他们宁愿承认失败。
NDefines.NAI.PEACE_TERMS_PROVINCE_STRATEGY_THRESHOLD = 5  -----如果该省至少有这个战略优先级，ai在和平协议中会更重视它。
NDefines.NAI.PEACE_TERMS_RETURN_PROVINCE_STRATEGY_MULT = 0.5  ----如果我们对一个省有战略优先权，那么AI把它释放给其他国家的愿望就会乘以这个数量。
NDefines.NAI.PEACE_TERMS_WAR_REPARATIONS_BASE_MULT = 0.01  ---ai要赔款倾向
NDefines.NAI.PEACE_TERMS_WAR_REPARATIONS_MIN_INCOME_RATIO = 0.9  ----AI只希望在其他国家至少自己该数值收入的情况下获得战争赔偿。
--
NDefines.NAI.POWERFUL_ALLY_PENALTY = 100    -------如果ai已经有一个强大的盟友，那么联盟将会受到惩罚。
NDefines.NAI.DIPLOMATIC_ACTION_OFFER_CONDOTTIERI_ONLY_MILITARY_RULERS = 0  ---为1时只有斧头才会派遣雇佣兵
NDefines.NAI.DIPLOMATIC_ACTION_IMPROVE_RELATIONS_VASSALIZE_FACTOR = 200  -----如果AI的态度带有“附属化”的欲望(也适用于皇室婚姻的欲望)，那么AI改善关系的得分就会增加。
NDefines.NAI.DIPLOMATIC_ACTION_IMPROVE_RELATIONS_ALLY_FACTOR = 190  ---如果AI有“盟友”的愿望，那么他们改善关系的得分会因此增加。
NDefines.NAI.DIPLOMATIC_ACTION_IMPROVE_RELATIONS_BEFRIEND_FACTOR = 190  ----如果AI的态度带有“交朋友”的欲望，那么AI改善关系的得分会因此增加。
NDefines.NAI.DIPLOMATIC_ACTION_TAKE_ON_DEBT_POWERBALANCE_FACTOR = 20  ---AI对阻挡力量平衡威胁的目标增加承担外债得分。
NDefines.NAI.DIPLOMATIC_ACTION_FABRICATE_CLAIM_BASE_FACTOR = 100.0  ---只要这个省份是一个征服优先级，AI伪造宣称的得分就会增加。
NDefines.NAI.DIPLOMATIC_ACTION_FABRICATE_CLAIM_STRATEGY_FACTOR = 2.0  -----ai对基于战略征服优先级的造宣称的倾向。
NDefines.NAI.DIPLOMATIC_ACTION_FABRICATE_CLAIM_OTHER_CB_FACTOR = 1   -----如果有一个可以吃掉该地的cb，ai就不会造宣称
NDefines.NAI.DIPLOMATIC_ACTION_FABRICATE_CLAIM_NOT_ADJACENT_FACTOR = 0.25  ---ai造飞地宣称的倾向
NDefines.NAI.DIPLOMATIC_ACTION_TRIBUTARY_ACCEPTANCE_PER_DEVELOPMENT = -1  ---每点发展度对AI成为朝贡国的影响
NDefines.NAI.DIPLOMATIC_ACTION_TRIBUTARY_EMPIRE_FACTOR = 1  ---天朝和部落收朝贡的倾向
NDefines.NAI.DIPLOMATIC_ACTION_SUBSIDIES_POWERBALANCE_FACTOR = 50  ----AI得分给阻碍/对抗力量平衡威胁的国家提供战争援助。
NDefines.NAI.DIPLOMATIC_ACTION_GIFT_POWERBALANCE_FACTOR_AI = 30  ----AI因实力均衡的威胁而向AI国家赠送礼物的意向
NDefines.NAI.DIPLOMATIC_ACTION_GIFT_POWERBALANCE_FACTOR_PLAYER = 25  ---AI因实力均衡的威胁而向玩家国家赠送礼物的意向
NDefines.NAI.DIPLOMATIC_ACTION_GUARANTEE_POWERBALANCE_FACTOR = 30 ----	AI对因实力均衡的威胁收到阻挡而添加独立保证行为的倾向。
NDefines.NAI.DIPLOMATIC_ACTION_VASSALIZE_DEVELOPMENT_FACTOR	= 100  ---AI的附庸国得分随着目标省份的发展而增加。
NDefines.NAI.DIPLOMATIC_ACTION_MILITARY_ACCESS_EXISTING_RELATION_MULT = 20.0  ----如果AI有一个现有的权力成本关系，那么它对军事访问的得分将乘以这个。
NDefines.NAI.DIPLOMATIC_ACTION_MILITARY_ACCESS_ENEMY_REGIMENTS_FACTOR = 2.5  ----每有一个敌人部队在自己没有军事通行权的地方AI得分都会因此而增加。
NDefines.NAI.DIPLOMATIC_ACTION_SUBSIDIES_WAR_WITH_RIVAL_FACTOR = 75  ----ai因向与对手交战的国家提供战争援助而倾向。
NDefines.NAI.DIPLOMATIC_ACTION_ALLIANCE_ACCEPTANCE_MULT = 2  -----人工智能对联盟的打分是基于如果提供给他们，他们是否愿意接受。
NDefines.NAI.DIPLOMATIC_ACTION_WARNING_WARN_FACTOR = 100  ---如果他们有'警告'欲望的态度（乘以共同邻居的数量），AI发布警告的评分会因此而改变。
--
NDefines.NAI.DIPLOMATIC_ACTION_INFLUENCE_NATION_BASE_FACTOR = 25 --影响国家的AI基础得分（需要是盟友或阻止对手/列强的威胁，甚至适用）
NDefines.NAI.DIPLOMATIC_ACTION_INFLUENCE_NATION_ALLY_FACTOR	= 20 --对与我们结盟的国家进行影响国家外交行动的AI额外得分。
NDefines.NAI.DIPLOMATIC_ACTION_OFFER_CONDOTTIERI_DISABLE_VERSUS_PLAYER_ENEMIES = 0 --如果设置为1,AI不会向与玩家作战的国家派遣雇佣军
NDefines.NAI.DIPLOMATIC_ACTION_PERSONALITY_MULT = 3 --如果一个外交行动符合他们的个性（为外交官改善关系等），那么AI会更加重视。
NDefines.NAI.DIPLOMATIC_INTEREST_DISTANCE = 150 --如果边界距离大于这个外交AI对该国的兴趣就会降低。
--
NDefines.NAI.CONVERT_TRIBUTARY_TO_VASSAL_AI_DESIRE_BASE = 40 --AI将朝贡国转化为附庸的基础权重
NDefines.NAI.CONVERT_TRIBUTARY_TO_VASSAL_AI_DESIRE_PREPARING_FOR_WAR_SCORE = 100
NDefines.NAI.CONVERT_TRIBUTARY_TO_VASSAL_AI_DESIRE_WANTS_LAND_SCORE = 50
--
NDefines.NAI.DIPLOMATIC_ACTION_TAKE_ON_DEBT_ALLY_FACTOR = 50 --AI对与我们结盟的国家的外债进行额外的打分
NDefines.NAI.DIPLOMATIC_ACTION_SUBSIDIES_INDEBTED_FACTOR = 40 --AI为给一个负债累累的盟友提供补贴的权重。
--
NDefines.NAI.MAX_BUILDING_COST_INCOME_MONTHS = 50   -----如果有更便宜的替代品，AI将不会为一个花费超过(月收入*该值)的建筑存钱。
NDefines.NAI.MAX_SAVINGS = 240  ---AI将在长期储蓄中保留最多这*他们的月收入。
NDefines.NAI.ADVISOR_PROMOTION_AGE_CUTOFF = 45  ---AI不会升级年龄比该数更大的顾问
--
NDefines.NAI.CORRUPTION_BUDGET_FRACTION = 2  ---人工智能将把每月收入的最大一部分用于根除腐败。
NDefines.NAI.ARMY_BUDGET_FRACTION = 5  ----ai将把这个月收入的最大部分用于军队维护(基于战时成本)。
NDefines.NAI.NAVY_BUDGET_FRACTION = 2   ---ai将把这个月收入的最大一部分用于海军维护(基于战时成本)。
NDefines.NAI.FORT_BUDGET_FRACTION = 1   ---ai将把这个月收入的最大部分花在堡垒上
--
NDefines.NAI.REPAY_LOAN_BASE_AI_DESIRE = 1000.0  -----AI偿还贷款的权重，乘以（MAX（预算-其他贷款，0）*贷款数量）/成本
NDefines.NAIEconomy.LOAN_REPAYMENT_SAVINGS_PRIORITY = 1000.0
--
NDefines.NAI.DANGEROUS_OVEREXTENSION_PERCENTAGE = 5
--
NDefines.NAI.MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER = 5 --ai私掠倾向
--
NDefines.NAI.AGGRESSIVENESS = 25.0  ---ai攻击性
NDefines.NAI.AGGRESSIVENESS_BONUS_EASY_WAR = 35.0  ---如果战争的对象是弱小的或特别讨厌的敌人，就会增加侵略性。
NDefines.NAI.MISSION_PICK_CHANCE = 10000.0  ---如果缺少一个任务，AI每月选择一个任务的几率(100)。
NDefines.NAI.PS_SHORT_TERM_POOL = 150  ----AI最多储存该数值的君主点数在短期支出池
NDefines.NAI.AI_TOTAL_DEV_CULTURE_MULTIPLIER = 20.0  ----	AI对主流文化中拥有大量发展度的重视程度修正。
--
NDefines.NAI.AI_WANT_ACCEPT_CULTURES = 1 --想要接受文化
NDefines.NAI.WANT_TRIBUTARY_LOST_MANDATE = 25.0 --影响天朝与非接壤成立朝贡国的重要性
--
NDefines.NAI.DEFENDER_OF_FAITH_BASE_AI_DESIRE = 0.25  ---ai信仰基础的守护者是欲望
--
NDefines.NAI.EDICT_VALUE_THRESHOLD = 15  ---值越高，AI开启法令的倾向越低
NDefines.NAI.EDICT_VALUE_THRESHOLD_MULTIPLY_DEFICIT = 6  ---当AI财政有亏损时改变上述阈值为多少倍
NDefines.NAI.EDICT_VALUE_THRESHOLD_MULTIPLY_LOW_INCOME = 3  ---	当AI财政收入较低时改变上述阈值为多少倍
--
NDefines.NAI.ASSIMILATION_INTEREST_AMOUNT_FACTOR = 1000.0   ----对同化兴趣的影响，来自剩余省份的征服数量（看不懂）
--
NDefines.NAI.WAR_WARSCORE_TO_JOIN = -100  ----ai参展的最低分
NDefines.NAI.WAR_MIN_WARSCORE_TO_JOIN = -50  ----战争分对ai参战倾向的影响
--
NDefines.NAI.TRANSPORT_FRACTION = 0.2  ---货船最大占比
NDefines.NAI.BIGSHIP_FRACTION = 1   ----AI海军中轻型船只和大型船只的比例
NDefines.NAI.OVER_FORCELIMIT_AVOIDANCE_FACTOR = 65  ----这个数字越高，AI就越不愿意超上限。
NDefines.NAI.ARTILLERY_FRACTION = 0.15   ----AI征召的炮兵相对步兵的比例
NDefines.NAI.MIN_CAV_PERCENTAGE = 0
NDefines.NAI.MAX_CAV_PERCENTAGE = 100 ----ai骑兵比例
NDefines.NAI.REGIMENTS_PER_GENERAL = 24  --AI会想要一个将军，每个团的数量(不会超过免费的领袖池)。
NDefines.NAI.ONLY_INFANTRY_MERCS = 1 --当此值设定为0时，AI将会雇佣骑兵和炮兵
--
NDefines.NAI.CALL_ACCEPTANCE_COALITION_VS_SUBJECT = -30  ---当AI的朝贡国（或者当下未存在的相似机制属国类型）召唤至反包围网战争，而影响到的接受因素惩罚。
----
NDefines.NAI.AI_FORT_PER_DEV_RATIO = 15 --AI大约会在每拥有该数值发展度后会修建一个要塞
NDefines.NAI.FORT_NEXT_TO_FORT_MULT = 1.25 --AI拥有要塞后继续修建要塞的倾向
NDefines.NAI.FORT_ON_BORDER_MULT = 2 --AI在边境上修要塞的倾向
--
NDefines.NAI.HRE_DESIRE_OVERLORD_IS_EMPEROR = 200  ---选弟候支持宗主倾向
NDefines.NAI.HRE_DESIRE_WANTS_TO_ANTAGONISE_EMPEROR = 30 --伪罗诸侯和伪帝对立倾向
NDefines.NAI.HRE_DESIRE_WANTS_TO_WEAKEN_EMPEROR = 50 --伪罗诸侯削弱伪帝倾向
NDefines.NAI.HRE_DESIRE_WANTS_TO_WARN_EMPEROR = 100 --伪罗诸侯警告伪帝倾向
---
NDefines.NAI.PEACE_TERMS_VASSAL_BASE_MULT = 1 --附庸cb ai附庸倾向
NDefines.NAI.REVOLUTION_EMBRACE_MAX_ABSOLUTISM = 20 --ai专制度大于此值时永远不会革命
NDefines.NAI.DEVELOPMENT_CAP_BASE = 50 --	AI不会开发那些发展度超过这个或DEVELOPMENT_CAP_MULT*原始发展程度（以大者为准）的省份。
NDefines.NAI.DEVELOPMENT_CAP_MULT = 1.2
NDefines.NAI.GOVERNING_CAPACITY_OVER_PERCENTAGE_TOLERATED = 0.4 --AI最多会超过行政容量百分之多少
NDefines.NAI.DANGEROUS_OVEREXTENSION_PERCENTAGE = 1.1 --过扩？
--
NDefines.NAI.AI_USES_HISTORICAL_IDEA_GROUPS	= 1 --如果设置为0，ai将在挑选理念组时使用ai_will_do而不是历史理念组
--
NDefines.NAI.ESTATE_MAX_WANTED_INFLUENCE = 94.0
NDefines.NAI.ESTATE_MIN_WANTED_CROWNLAND = 20.0
NDefines.NAI.DANGEROUS_ESTATE_INFLUENCE_BUFFER = 6.0  --AI将控制阶层影响力，最多为ESTATE_DANGER_THRESHOLD减去这个（见ai_territory_modifier）。
--
NDefines.NAI.FOREIGN_MINISTER_IGNORE_DISTANCE_BASE = 7
NDefines.NAI.FOREIGN_MINISTER_BASE_PROVINCE_COUNT = 2
--
NDefines.NAI.INCOME_SAVINGS_FRACTION = 0.275 --	AI将保留这笔盈余用于长期储蓄。
NDefines.NAI.EXTRA_SURPLUS_WHEN_NEEDING_BUILDINGS = 0.2 --	AI的目标是在他们需要建筑物时，至少有这部分收入作为额外的盈余
NDefines.NAI.DESIRED_DEFICIT = 0.1 --AI将尝试把这部分钱花在他们的目标之上，以实现长期储蓄。
NDefines.NAI.DESIRED_SURPLUS = 0.115 --	AI的目标是，当他们没有大量储蓄时，至少要有这部分收入作为盈余。
NDefines.NAI.DEFICIT_SPENDING_MIN_MONTHS = 3.0 --AI至少要有这么多的月度储蓄才愿意进行赤字支出
NDefines.NAI.DEFICIT_SPENDING_MIN_MONTHS_PEACETIME = 24.0 --与DEFICIT_SPENDING_MIN_MONTHS相同，但在和平时期，没有叛军，也没有厌战度
--
NDefines.NAI.DEBASE_THRESHOLD = 700
NDefines.NAI.DRILLING_BUDGET_OF_SURPLUS = 0.01 --	当盈余高于该数值年收入时，AI才会训练部队
NDefines.NAI.DRILLING_DEBT_SURPLUS_RATIO_THRESHOLD = 0.01 --	只有当盈余/债务比率高于上述标准时，AI才会考虑进行训练。
NDefines.NAI.DRILLING_ACCEPTABLE_THREAT_REDUCTION = 300 --		AI遭到威胁时会减少训练的情况
--
NDefines.NAI.ADVISOR_MIN_SKILL_RELUCTANT_FIRE = 3 --	AI将不愿意解雇等级比该数更高的顾问(由于之前雇佣时的高花费）。
NDefines.NAI.RECRUIT_ADVISOR_BASE_AI_DESIRE = 80.0  --AI重新招募顾问的权重，乘以预算/成本
NDefines.NAI.PROMOTE_ADVISOR_BASE_AI_DESIRE = 50.0 --AI晋升顾问的权重，乘以预算/成本
NDefines.NAI.ADVISOR_BUDGET_FRACTION_MAX = 0.6 --AI最多会将月收入的这一部分花在顾问的维护上
NDefines.NAI.ADVISOR_BUDGET_FRACTION_MIN = 0.2 --AI最少会将月收入的这一部分花在顾问的维护上
NDefines.NAI.ADVISOR_BUDGET_FRACTION_MERITOCRACY_MAX = 0.8 --如果AI启用了择优录取制度，AI最多会将月收入的这一部分花在顾问的维护上
NDefines.NAI.ADVISOR_BUDGET_FRACTION_MERITOCRACY_MIN = 0.3 --	如果AI启用了择优录取制度，AI最少会将月收入的这一部分花在顾问的维护上
--
NDefines.NAI.CORRUPTION_BUDGET_FRACTION = 10.0 --AI将最多花费月收入的这一部分用于根除腐败
NDefines.NAI.COLONY_BUDGET_FRACTION = 1.475 --	AI最多会花这个数额的月度金币购买殖民地
--
NDefines.NAI.GREAT_PROJECT_DESIRE_MOVE_FROM_SUBJECT_MODIFIER = 0 --AI偷奇观倾向
NDefines.NAI.GREAT_PROJECT_DESIRE_LEAVE_IN_SUBJECT_MODIFIER = 1
NDefines.NAI.GREAT_PROJECT_DESIRE_UPGRADE_IN_SUBJECT_MODIFIER = 1 --附庸国AI升级奇观的倾向
NDefines.NAI.GREAT_PROJECT_DESIRE_UPGRADE_MODIFIER = 5.5 --AI升级奇观的倾向
NDefines.NAI.GREAT_PROJECT_DESIRE_BUILD_NEW_MODIFIER = 5.0 --	AI建造奇观的倾向
NDefines.NAI.GREAT_PROJECT_DESIRE_CAPITAL_MODIFIER = 0 --AI希望奇观在首都倾向修正
NDefines.NAI.GREAT_PROJECT_DESIRE_CAPITAL_BASE = 0 --AI希望奇观在首都倾向的基础值
NDefines.NAI.GREAT_PROJECT_DESIRE_CAPITAL_AREA_MODIFIER = 0 --	AI希望奇观在首都区域倾向修正
--
NDefines.NAI.UPGRADE_CENTER_OF_TRADE_BASE_AI_DESIRE = 500.0 --AI升级贸易中心的权重，乘以预算/成本。
--
NDefines.NAIEconomy.STATE_MAINTENANCE_FRACTION = 2.0 --州维护分数
NDefines.NAIEconomy.BUDGETING_ADJUSTMENT_STEP = 0.11 --由于盈余/亏损而进行调整时，增加/减少预算员额支出的金额（百分比）
NDefines.NAIEconomy.MILITARY_FOCUS_DEFAULT = 2.85 --军事焦点默认值
NDefines.NAIEconomy.MILITARY_FOCUS_LOWER_BOUND = 3.0 --军事焦点下限
NDefines.NAIEconomy.MILITARY_FOCUS_UPPER_BOUND = 4.5 --军事焦点上限
NDefines.NAIEconomy.MISSIONARY_FRACTION = 0.175 --传教倾向
NDefines.NAIEconomy.ARMY_FRACTION_PEACEFUL = 2.1
NDefines.NAIEconomy.ARMY_FRACTION_MILITARIST = 4.35
NDefines.NAIEconomy.ARMY_FRACTION_MILITARIST = 4.35
NDefines.NAIEconomy.ARMY_FRACTION_MILITARIZE = 2.2
NDefines.NAIEconomy.NAVY_FRACTION_PEACEFUL = 2.0
NDefines.NAIEconomy.NAVY_FRACTION_CAPITALIST = 2.0
NDefines.NAIEconomy.FORT_FRACTION_MILITARIZE = 4.0
NDefines.NAIEconomy.FORT_FRACTION_MILITARIST = 7.0
NDefines.NAIEconomy.FORT_FRACTION_CAPITALIST = 6.0
NDefines.NAIEconomy.REBEL_THREAT_MILITARIZE_THRESHOLD = 1.0
--