# 中世纪项目文档索引

开始工作时先读相关 **design**；查询当前实现时优先查对应 **process（如有）**，再核对源码、JSON 与测试。启动阅读和索引维护要求见 [AGENTS.md](AGENTS.md)。

## 盔甲文档阅读入口

1. [盔甲总设计](docs/design/design02-盔甲.md)：用途区分、外层主甲与垫衣/锁甲组合、负重及防护原则。
2. [布里根丁与板甲衣细分](docs/design/design02_1-布里根丁与板甲衣细分.md)：防具定位、初始数值区间、重量一致性与原方案评判。
3. [旧盔甲实现记录](docs/archive/technical/medieval_armor.md)：旧分支装备与参数归档，**不代表当前 Medieval 分支已实现**。
4. [护甲穿透调研](docs/vanilla/code_armor_penetration_system.md)：我们整理的原版机制背景参考。

## 当前进度查询

本分支重新基于原版开始，目前没有已跟踪的 `docs/process/` 文档。实际开展实现后，分别查询或创建 `docs/process/json/<对应design同名文件>.md` 和 `docs/process/code/<对应design同名文件>.md`，并在本索引登记。`docs/archive/technical/` 仅供参考，不作为当前完成状态的依据。

## 覆盖与维护

仅收录我们维护的 `docs/` 文档，包括 design、process（如有）、vanilla 调研和技术归档；不收录原版 `doc/`、其他模组或仓库其他目录的文档。链接路径相对于仓库根目录。

文档增删、移动、重命名或简介与正文不符后，在同一次提交中同步更新本索引。

## 中世纪游戏策划（design）

| 文档位置 | 简介 |
| --- | --- |
| [docs/design/design00-清理现代内容.md](docs/design/design00-%E6%B8%85%E7%90%86%E7%8E%B0%E4%BB%A3%E5%86%85%E5%AE%B9.md) | 中世纪转换 mod 设计方案：5层拦截架构、item_group覆写策略、物品注入通道、硬编码限制 |
| [docs/design/design01-世界观.md](docs/design/design01-%E4%B8%96%E7%95%8C%E8%A7%82.md) | 世界观与威胁体系：中世纪背景设定、危险来源、文明等级 |
| [docs/design/design02-盔甲.md](docs/design/design02-%E7%9B%94%E7%94%B2.md) | 盔甲游戏策划：薄垫衣与厚布甲区分、普通层叠穿代价、外层主甲、部位防护和负重取舍。 |
| [docs/design/design02_1-布里根丁与板甲衣细分.md](docs/design/design02_1-%E5%B8%83%E9%87%8C%E6%A0%B9%E4%B8%81%E4%B8%8E%E6%9D%BF%E7%94%B2%E8%A1%A3%E7%BB%86%E5%88%86.md) | 板甲衣、布里根丁与胸背甲：形制定位、厚度/重量/累赘初始区间、锁甲与肢体甲及数据合理性评判。 |
| [docs/design/design03-日常衣物.md](docs/design/design03-%E6%97%A5%E5%B8%B8%E8%A1%A3%E7%89%A9.md) | 低端衣物与日常装备（平民层）：麻、羊毛、基础皮革，覆盖全阶层日常着装 |
| [docs/design/design04-武器.md](docs/design/design04-%E6%AD%A6%E5%99%A8.md) | 武器体系：Oakeshott XV-XVIII型、60+种武器分类、伤害类型×反甲逻辑矩阵 |
| [docs/design/design04_1-quality体系.md](docs/design/design04_1-quality%E4%BD%93%E7%B3%BB.md) | 装备 Quality 体系（设计冻结/非初版）：材料变体走JSON copy-from，Quality作为纯运行时属性，区分武器/盔甲影响 |
| [docs/design/design05-职业.md](docs/design/design05-%E8%81%8C%E4%B8%9A.md) | 开局职业与技能映射：中世纪社会阶层→CDDA profession/skill体系 |
| [docs/design/design06-建筑.md](docs/design/design06-%E5%BB%BA%E7%AD%91.md) | 中世纪聚落与建筑体系：村庄布局、建筑类型、材料与建造逻辑 |
| [docs/design/design07-冒险者工会.md](docs/design/design07-%E5%86%92%E9%99%A9%E8%80%85%E5%B7%A5%E4%BC%9A.md) | 冒险者工会体系：单一工会/多分会架构、声望等级、三层任务池、NPC/服务设计 |
| [docs/design/design08-敌人.md](docs/design/design08-%E6%95%8C%E4%BA%BA.md) | **总决策**：双系统分层（NPC用于人形敌人，Monster+部位HP修复用于野兽/巨怪） |
| [docs/design/design08_1-野怪_强盗.md](docs/design/design08_1-%E9%87%8E%E6%80%AA_%E5%BC%BA%E7%9B%97.md) | NPC 体系（一）—— 强盗：刷新配置、装备池、AI行为 |
| [docs/design/design08_2-野怪_野生动物.md](docs/design/design08_2-%E9%87%8E%E6%80%AA_%E9%87%8E%E7%94%9F%E5%8A%A8%E7%89%A9.md) | ⚠️ 修订为 Monster 路线 —— 14种真实中世纪动物（数值可作 Monster JSON 参考） |
| [docs/design/design08_3-野怪_奇幻.md](docs/design/design08_3-%E9%87%8E%E6%80%AA_%E5%A5%87%E5%B9%BB.md) | ⚠️ 拆分为 NPC/ Monster —— 14种奇幻生物，生态+战利品，标注各自归属系统 |
| [docs/design/design09-战斗系统重置.md](docs/design/design09-%E6%88%98%E6%96%97%E7%B3%BB%E7%BB%9F%E9%87%8D%E7%BD%AE.md) | 战斗系统深度重置：手动技艺选择 + 部位瞄准，双轮UI、n/k技能线性缩放 |
| [docs/design/design09_1-部位血量系统.md](docs/design/design09_1-%E9%83%A8%E4%BD%8D%E8%A1%80%E9%87%8F%E7%B3%BB%E7%BB%9F.md) | 部位血量系统：移除 monster::hp，vital 部位死亡判定 + 塔科夫式伤害扩散 |
| [docs/design/design09_2-怪物部位行动影响.md](docs/design/design09_2-%E6%80%AA%E7%89%A9%E9%83%A8%E4%BD%8D%E8%A1%8C%E5%8A%A8%E5%BD%B1%E5%93%8D.md) | 怪物部位伤害对行动的影响：方案 B 设计与实施计划（未完成） |
| [docs/design/design09_2-远程伤害系统.md](docs/design/design09_2-%E8%BF%9C%E7%A8%8B%E4%BC%A4%E5%AE%B3%E7%B3%BB%E7%BB%9F.md) | 远程伤害系统策划：射击伤害、相关属性与战斗规则。 |
| [docs/design/design09_4-远程部位瞄准.md](docs/design/design09_4-%E8%BF%9C%E7%A8%8B%E9%83%A8%E4%BD%8D%E7%9E%84%E5%87%86.md) | 远程部位瞄准策划：攻击部位选择与命中规则。 |

## 原版机制调研（vanilla）

| 文档位置 | 简介 |
| --- | --- |
| [docs/vanilla/code_armor_penetration_system.md](docs/vanilla/code_armor_penetration_system.md) | 护甲穿透系统：damage_unit→res_pen/res_mult全程链路、Character/Monster护甲吸收、Medieval STR×重量破甲改造 |
| [docs/vanilla/code_bodypart_hp_system.md](docs/vanilla/code_bodypart_hp_system.md) | 部位分血架构：Creature五层部位体系、Monster绕过机制、Character受伤三层模型 |
| [docs/vanilla/code_city_generation_system.md](docs/vanilla/code_city_generation_system.md) | 城市/城镇生成系统：place_cities()入口、build_city_street()递归、建筑池 |
| [docs/vanilla/code_clothing_layer_system.md](docs/vanilla/code_clothing_layer_system.md) | 穿衣分层调研：同层子部位冲突、额外累赘算法、刚性限制、原版防具基准及 to_hit 的适用范围。 |
| [docs/vanilla/code_combat_system.md](docs/vanilla/code_combat_system.md) | 战斗系统：伤害类型、护甲穿透、近战命中/暴击/格挡、远程瞄准/后坐力 |
| [docs/vanilla/code_crafting_system.md](docs/vanilla/code_crafting_system.md) | 制作与技能：双轨制技能系统、配方学习、熟练度、建造蓝图 |
| [docs/vanilla/code_harvest_drop_system.md](docs/vanilla/code_harvest_drop_system.md) | 解剖/屠宰产物系统：harvest_drop_type→harvest→monster三层key引用链、harvest vs dissect差异、C++数据流 |
| [docs/vanilla/code_item_damage_system.md](docs/vanilla/code_item_damage_system.md) | 物品伤害/破损等级系统：底层的整千倍乘与离散折叠算法，剖析 JSON 伤害概率塌陷与强盗装备“整齐划一”的数学机理 |
| [docs/vanilla/code_localization_system.md](docs/vanilla/code_localization_system.md) | 本地化与国际化系统：延迟翻译容器translation、自制MO解析器与哈希查找、自动化JSON文本提取工作流与Mod本地化策略 |
| [docs/vanilla/code_magic_system.md](docs/vanilla/code_magic_system.md) | 魔法系统：法术定义、能量来源、33种法术效果、附魔与触发式法术 |
| [docs/vanilla/code_material_system.md](docs/vanilla/code_material_system.md) | 材料系统：material_type加载/验证流程、damage_type注册机制、stab抗性引擎支持、钢材7级分级与chain变体 |
| [docs/vanilla/code_monster_spawn_system.md](docs/vanilla/code_monster_spawn_system.md) | 怪物刷新系统：MonsterGroupEntry/GetResultFromGroup核心算法、5条刷新通道 |
| [docs/vanilla/code_mutation_bionic_system.md](docs/vanilla/code_mutation_bionic_system.md) | 变异与生化改造：突变类别/阈值、生化模块能量/安装/升级 |
| [docs/vanilla/code_npc_equipment_system.md](docs/vanilla/code_npc_equipment_system.md) | NPC装备系统：三层override机制、17槽位着装链、武器按技能选择、bandit分析 |
| [docs/vanilla/code_nutrition_health_system.md](docs/vanilla/code_nutrition_health_system.md) | 营养与健康：胃/肠道消化、卡路里计算、维生素、饮食限制、代谢率 |
| [docs/vanilla/code_time_system.md](docs/vanilla/code_time_system.md) | 时间系统：时间单位、Speed/Moves/动作消耗关系、游戏主循环、怪物速度 |
| [docs/vanilla/code_weapon_to_hit_system.md](docs/vanilla/code_weapon_to_hit_system.md) | 武器命中与双手系统：grip/surface/length/balance四属性计算m_to_hit、ALWAYS_TWOHAND判定 |
| [docs/vanilla/json_data_system.md](docs/vanilla/json_data_system.md) | JSON数据体系：data/目录结构、加载机制、80+种JSON类型、核心Schema、Mod系统 |
| [docs/vanilla/json_general.md](docs/vanilla/json_general.md) | JSON依赖关系图：80+种JSON类型之间的引用/依赖关系全景 |
| [docs/vanilla/json_itemgroup_monstergroup.md](docs/vanilla/json_itemgroup_monstergroup.md) | item_group与monstergroup分组粒度分析 |
| [docs/vanilla/json_itemgroup_organization.md](docs/vanilla/json_itemgroup_organization.md) | item_group组织概念与目录分布：9维概念体系、概念→目录映射、对Medieval的启示 |
| [docs/vanilla/json_map.md](docs/vanilla/json_map.md) | 地图体系：从世界生成到可见地块的完整管线 |
| [docs/vanilla/json_martial.md](docs/vanilla/json_martial.md) | 战斗系统JSON配置：techniques/martialarts/body_parts/anatomy/limb_scores |
| [docs/vanilla/json_mission.md](docs/vanilla/json_mission.md) | 任务与剧情系统：missiondef/effects_on_condition/talk_topic |
| [docs/vanilla/json_npc.md](docs/vanilla/json_npc.md) | NPC配置体系调研：npc_class、对话、任务、faction等JSON配置 |
| [docs/vanilla/json_technique_deep.md](docs/vanilla/json_technique_deep.md) | Technique 字段深度字典：39 个 JSON key 的 C++ 加载默认值、运行时行为、关键 gotcha |
| [docs/vanilla/monster_wildlife_hp_overview.md](docs/vanilla/monster_wildlife_hp_overview.md) | 原版野生动物HP概览：哺乳动物/鸟类/爬行两栖/鱼类血量分布与Medieval参考标尺 |

## 旧分支技术归档（不代表当前实现）

| 文档位置 | 简介 |
| --- | --- |
| [docs/archive/technical/example_griffin.md](docs/archive/technical/example_griffin.md) | 旧分支技术归档：任务：狮 Griffiin 示例改造；仅供参考。 |
| [docs/archive/technical/medieval_armor.md](docs/archive/technical/medieval_armor.md) | 旧分支技术归档：中世纪盔甲与战术防护体系实现方案；仅供参考。 |
| [docs/archive/technical/medieval_bandit_system.md](docs/archive/technical/medieval_bandit_system.md) | 旧分支技术归档：中世纪野怪与强盗据点/遭遇体系实现方案；仅供参考。 |
| [docs/archive/technical/medieval_clothing.md](docs/archive/technical/medieval_clothing.md) | 旧分支技术归档：中世纪平民与日常衣物体系实现方案；仅供参考。 |
| [docs/archive/technical/medieval_combat_rebalance.md](docs/archive/technical/medieval_combat_rebalance.md) | 旧分支技术归档：中世纪战斗重平衡：实现方案；仅供参考。 |
| [docs/archive/technical/medieval_i18n_workflow.md](docs/archive/technical/medieval_i18n_workflow.md) | 旧分支技术归档：中世纪 Mod 独立本地化自动化工作流 (Medieval i18n Workflow)；仅供参考。 |
| [docs/archive/technical/medieval_professions.md](docs/archive/technical/medieval_professions.md) | 旧分支技术归档：中世纪职业实现方案；仅供参考。 |
| [docs/archive/technical/medieval_settlement.md](docs/archive/technical/medieval_settlement.md) | 旧分支技术归档：中世纪聚落与地图：实现方案；仅供参考。 |
| [docs/archive/technical/medieval_weapons.md](docs/archive/technical/medieval_weapons.md) | 旧分支技术归档：中世纪近战与远程武器体系实现方案；仅供参考。 |
| [docs/archive/technical/modern_content_removal.md](docs/archive/technical/modern_content_removal.md) | 旧分支技术归档：现代内容清除进度；仅供参考。 |
| [docs/archive/technical/monster_bodypart_fix.md](docs/archive/technical/monster_bodypart_fix.md) | 旧分支技术归档：任务：Monster 部位 HP 修复；仅供参考。 |
| [docs/archive/technical/ranged_aimed_part.md](docs/archive/technical/ranged_aimed_part.md) | 旧分支技术归档：任务：射击部位瞄准系统；仅供参考。 |
