-- ============================================================
-- ACG_MEC_E 子模 define 覆盖：君主特质（ruler personalities）
-- ============================================================
-- 背景（均为本机实测值）：
--   原版  common/defines.lua:857 MAX_EXTRA_PERSONALITIES = 2, FIRST = 10, YEARS = 15
--   ACG1  common/defines/acg_defines.lua:17 = 4（注释“提升到5个”）, FIRST = 5, YEARS = 10
--   Xorme common/defines/xorme_ai_main.lua:1-3 = 3, FIRST = 0, YEARS = 15
--
-- 两边的 define 文件名不同（acg_defines.lua / xorme_ai_main.lua），所以不是“互相覆盖文件”，
-- 而是两段 Lua 赋值先后执行、后执行的那条生效。本文件用 zz_ 前缀命名，目的是排在
-- acg_defines.lua、xorme_ai_main.lua 之后执行，只压掉这 3 个键。
--
-- 只写这 3 个键：Xorme AI 其余 AI define 与 ACG1 其余 define 全部保持原样。
--
-- 生效结果：君主特质总数 = 1（15 岁获得）+ 4 = 最多 5 个
-- 节奏沿用 Xorme：就任后即获得第 2 个特质，其后每 15 年 1 个
--
-- 进游戏自查：开新局看君主特质数量。就任后立刻出现第 2 个特质 => 本文件（FIRST=0）生效；
--             若必须等 5 年才出第 2 个特质 => 生效的是 ACG1（FIRST=5），说明本文件被盖掉，
--             此时在启动器把本子模排到 “Xorme - AI” 之后即可。
-- ============================================================

NDefines.NCountry.MAX_EXTRA_PERSONALITIES = 4
NDefines.NCountry.FIRST_EXTRA_PERSONALITY = 0
NDefines.NCountry.YEARS_PER_EXTRA_PERSONALITY = 15
