# 全仓库文档索引

开始工作时先读相关 **design**；查询当前实现时优先查对应 **process（如有）**，再核对源码、JSON 与测试。启动阅读和索引维护要求见 [AGENTS.md](AGENTS.md)。

## 盔甲文档阅读入口

1. [盔甲总设计](docs/design/design02-盔甲.md)：时代背景、防具分类、材料与分层防护。
2. [布里根丁与板甲衣细分](docs/design/design02_1-布里根丁与板甲衣细分.md)：过渡期防具变体与设计方案。
3. [旧盔甲实现记录](docs/archive/technical/medieval_armor.md)：旧分支装备与参数归档，**不代表当前 Medieval 分支已实现**。
4. [原版护甲穿透调研](docs/vanilla/code_armor_penetration_system.md) 与 [护甲平衡指南](doc/ARMOR_BALANCE_AND_DESIGN.md)：机制背景参考。

## 当前进度查询

本分支重新基于原版开始，目前没有已跟踪的 `docs/process/` 文档。实际开展实现后，分别查询或创建 `docs/process/json/<对应design同名文件>.md` 和 `docs/process/code/<对应design同名文件>.md`，并在本索引登记。`docs/archive/technical/` 仅供参考，不作为当前完成状态的依据。

## 覆盖与维护

逐项收录仓库中的 `.md`、`.rst`、`.adoc` 文档，`doc/`、`docs/` 中的 `.txt` 说明，以及各目录 `README.txt`、`LICENSE.txt`。源码、JSON 数据、翻译、词典、素材清单与构建配置不逐项收录。链接路径相对于仓库根目录。

文档增删、移动、重命名或简介与正文不符后，在同一次提交中同步更新本索引。

## 仓库入口与协作规范

| 文档位置 | 简介 |
| --- | --- |
| [.github/pull_request_template.md](.github/pull_request_template.md) | 提交 Pull Request 时使用的说明模板。 |
| [AGENTS.md](AGENTS.md) | 协作约定：最小改动、文档分类、design 优先、process 查询与索引维护。 |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | 社区行为准则、参与规范与归属声明。 |
| [INDEX.md](INDEX.md) | 全仓库文档主索引，包含位置、简介、盔甲阅读入口及当前进度文档位置。 |
| [ISSUES.md](ISSUES.md) | Issues：How to create new issues properly、Rule zero、Bug reports |
| [LICENSE.txt](LICENSE.txt) | 代码与随附组件的许可条款及版权声明。 |
| [README.md](README.md) | Cataclysm: Dark Days Ahead：Downloads、Packaging status、Compile |
| [lang/notes/README_all_translators.md](lang/notes/README_all_translators.md) | Instructions for Cataclysm-DDA translators：Translation file format、Translation file header、Format strings and newlines |

## 中世纪游戏策划（design）

| 文档位置 | 简介 |
| --- | --- |
| [docs/design/design00-清理现代内容.md](docs/design/design00-%E6%B8%85%E7%90%86%E7%8E%B0%E4%BB%A3%E5%86%85%E5%AE%B9.md) | 中世纪转换 mod 设计方案：5层拦截架构、item_group覆写策略、物品注入通道、硬编码限制 |
| [docs/design/design01-世界观.md](docs/design/design01-%E4%B8%96%E7%95%8C%E8%A7%82.md) | 世界观与威胁体系：中世纪背景设定、危险来源、文明等级 |
| [docs/design/design02-盔甲.md](docs/design/design02-%E7%9B%94%E7%94%B2.md) | 盔甲体系：14世纪末~15世纪初过渡期，布料→锁子甲→板甲的完整防护链 |
| [docs/design/design02_1-布里根丁与板甲衣细分.md](docs/design/design02_1-%E5%B8%83%E9%87%8C%E6%A0%B9%E4%B8%81%E4%B8%8E%E6%9D%BF%E7%94%B2%E8%A1%A3%E7%BB%86%E5%88%86.md) | 布里根丁与板甲衣细分及抽象化重构：退化抽象基类模板，细化10件过渡期防具及配套肢体防具 |
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

## 原版开发与机制文档（doc）

| 文档位置 | 简介 |
| --- | --- |
| [doc/ARMOR_BALANCE_AND_DESIGN.md](doc/ARMOR_BALANCE_AND_DESIGN.md) | CDDA 原版护甲机制与平衡指南：防护、覆盖、材料、累赘及防具设计。 |
| [doc/ARTIFACTS.md](doc/ARTIFACTS.md) | Artifacts：Introduction、Generation、charge_types |
| [doc/ASCII_ART.md](doc/ASCII_ART.md) | Making ASCII art for CDDA：ASCII art Editors、Installing REXPaint、Drawing |
| [doc/BASECAMP.md](doc/BASECAMP.md) | Basecamp：Recommended reading、Adding alternate basecamp upgrade paths、recipe JSONs |
| [doc/Blank_Building_Template.txt](doc/Blank_Building_Template.txt) | 空白建筑地图绘制模板。 |
| [doc/CHANGELOG_GUIDELINES.md](doc/CHANGELOG_GUIDELINES.md) | Changelog Guidelines：该主题的说明与参考。 |
| [doc/CLIMBING.md](doc/CLIMBING.md) | Climbing Aids：example definition、`id`、`type` |
| [doc/CODE_STYLE.md](doc/CODE_STYLE.md) | Code Style Guide：Code Example、Code Guidelines |
| [doc/COLOR.md](doc/COLOR.md) | Colors：Color string format、Examples of color strings、Color code |
| [doc/COMPILING/COMPILER_SUPPORT.md](doc/COMPILING/COMPILER_SUPPORT.md) | Compilers Supported：Mingw and Mingw-w64、MSYS2、XCode |
| [doc/COMPILING/COMPILING-CMAKE-VCPKG.md](doc/COMPILING/COMPILING-CMAKE-VCPKG.md) | Compiling CMAKE VCPKG：Disclaimer、1 Prerequisites、2 Configure |
| [doc/COMPILING/COMPILING-CMAKE.md](doc/COMPILING/COMPILING-CMAKE.md) | Compiling CMAKE：Disclaimer、Prerequisites、Build Environment |
| [doc/COMPILING/COMPILING-CYGWIN.md](doc/COMPILING/COMPILING-CYGWIN.md) | Compilation guide for 64 bit Windows (using Cygwin)：Prerequisites:、Installation:、Configuration: |
| [doc/COMPILING/COMPILING-DEVCONTAINER.md](doc/COMPILING/COMPILING-DEVCONTAINER.md) | Compilation guide for devcontainers in Visual Studio Code：Prerequisites:、Installation:、Cross-compiling from Linux to Windows |
| [doc/COMPILING/COMPILING-FLATPAK.md](doc/COMPILING/COMPILING-FLATPAK.md) | Compiling Flatpak：该主题的说明与参考。 |
| [doc/COMPILING/COMPILING-MSYS.md](doc/COMPILING/COMPILING-MSYS.md) | Compilation guide for 64-bit Windows (using MSYS2)：Prerequisites:、Installation:、Configuration: |
| [doc/COMPILING/COMPILING-VS-VCPKG.md](doc/COMPILING/COMPILING-VS-VCPKG.md) | Compilation guide for Windows (using Visual Studio and vcpkg)：Prerequisites:、Installation and configuration:、cd to the appropriate folder first |
| [doc/COMPILING/COMPILING.md](doc/COMPILING/COMPILING.md) | Compiling：General Linux Guide、Compiler、Tools |
| [doc/CONSRTUCTION_BALANCE.md](doc/CONSRTUCTION_BALANCE.md) | Construction Balance：该主题的说明与参考。 |
| [doc/CONTRIBUTING.md](doc/CONTRIBUTING.md) | Contribute：Using a good text editor、All PRs must have a "Summary" section、Contributing via GitHub |
| [doc/DEVELOPER_FAQ.md](doc/DEVELOPER_FAQ.md) | Developer FAQ：Adding stuff、Adding a monster、Adding structures to the map |
| [doc/DEVELOPER_TOOLING.md](doc/DEVELOPER_TOOLING.md) | Developer Tooling：Pre-commit hook、Code style (astyle)、JSON style |
| [doc/EFFECTS_JSON.md](doc/EFFECTS_JSON.md) | Effects：How to give effects in-game?、Comestibles、Creature attacks |
| [doc/EFFECT_ON_CONDITION.md](doc/EFFECT_ON_CONDITION.md) | Effect On Condition：Fields、Alpha and Beta Talkers、Typical Alpha and Beta Talkers by cases |
| [doc/EXAMINE.md](doc/EXAMINE.md) | Terrain/Furniture Examination Actions：Hardcoded Examine Actions、Examine Actors、`appliance_convert` |
| [doc/FACTIONS.md](doc/FACTIONS.md) | NPC factions：Scale of faction values、Faction relations |
| [doc/FREQUENTLY_MADE_SUGGESTIONS.md](doc/FREQUENTLY_MADE_SUGGESTIONS.md) | Frequently Made Suggestions：Project Management、Game Features、Performance |
| [doc/GAME_BALANCE.md](doc/GAME_BALANCE.md) | Game Balance：Stat system scaling:、Skill system scaling:、Monster melee skill scaling: |
| [doc/GUIDE_COMESTIBLES.md](doc/GUIDE_COMESTIBLES.md) | Guide to add Comestibles：List of special comestibles:、List of normal comestibles, in order of priority:、Liquid |
| [doc/HOW_YOU_CAN_HELP.md](doc/HOW_YOU_CAN_HELP.md) | How You Can Help：Other ways to help、Issue labels、Languages |
| [doc/IN_REPO_MODS.md](doc/IN_REPO_MODS.md) | Getting Mods Into The Repository：Why have in-repo mods?、What kind of mods can be in the CleverRaven repository?、What is necessary for a mod to be included in the repository? |
| [doc/ITEM_SPAWN.md](doc/ITEM_SPAWN.md) | Item spawn system：Collection or Distribution、Format、Entries array |
| [doc/JSON_FLAGS.md](doc/JSON_FLAGS.md) | JSON Flags：Notes、Inheritance、TODO |
| [doc/JSON_INFO.md](doc/JSON_INFO.md) | JSON INFO：Introduction、Overall structure、Common properties |
| [doc/JSON_INHERITANCE.md](doc/JSON_INHERITANCE.md) | JSON Inheritance：Examples、Support、Guidelines |
| [doc/JSON_LOADING_ORDER.md](doc/JSON_LOADING_ORDER.md) | JSON Loading Order：Same-depth loading order |
| [doc/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md](doc/JSON_Mapping_Guides/Guide_for_beginning_mapgen.md) | Guide for basic mapgen：该主题的说明与参考。 |
| [doc/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md](doc/JSON_Mapping_Guides/Guide_for_intermediate_mapgen.md) | Guide For Intermediate Mapgen：该主题的说明与参考。 |
| [doc/JSON_Mapping_Guides/JSON_ROOF_MAPGEN.md](doc/JSON_Mapping_Guides/JSON_ROOF_MAPGEN.md) | Adding Json Roof Guide：Making the Roof Map、Linking the main floor and the roof、Overmap Specials |
| [doc/JSON_STYLE.md](doc/JSON_STYLE.md) | JSON Style Guide：JSON Example、Formatting tool、Using git to filter JSON files with uncommitted changes (provided there are no spaces in the file or directory names). |
| [doc/JSON_TOOLS.md](doc/JSON_TOOLS.md) | JSON tools：Keys and Values、Examples、Examples and use cases |
| [doc/LORE.md](doc/LORE.md) | Faction Lore：The Blob、Lore owner: ?、The Blob Questions |
| [doc/Lore/design-balance.md](doc/Lore/design-balance.md) | Design - Overview of game balance principles：Balance around general game concepts、Overall combat balance、Sound |
| [doc/Lore/design-doc.md](doc/Lore/design-doc.md) | Design - Design Doc Overview：About this Page、How to Understand the Design Docs、Design Overview |
| [doc/Lore/design-gameplay.md](doc/Lore/design-gameplay.md) | Design - Gameplay：Gameplay Table of Contents、Objectives、Game Stages and Timeline |
| [doc/Lore/design-user-experience.md](doc/Lore/design-user-experience.md) | Design - User Experience：User Experience Table of Contents、Overview、Deployment |
| [doc/Lore/lore-background.md](doc/Lore/lore-background.md) | Lore - Background Story：Summary、Timeline |
| [doc/Lore/lore-factions.md](doc/Lore/lore-factions.md) | Lore - CDDA Faction Lore and Design Document：CDDA Faction Lore and Design Goals: Deep Dive、CDDA-Earth Native Human Factions、Free Merchants |
| [doc/Lore/lore.md](doc/Lore/lore.md) | Lore - Setting：Supporting Documents、Story、Style and Structure |
| [doc/Lore/technology.md](doc/Lore/technology.md) | Lore - Technology in the Cataclysm：Summary、Civilian Tech、Cybernetics |
| [doc/MAGIC.md](doc/MAGIC.md) | Magic, Spells, and Enchantments：Spells、The template spell、Mandatory fields |
| [doc/MANUAL_OF_STYLE.md](doc/MANUAL_OF_STYLE.md) | Manual Of Style：该主题的说明与参考。 |
| [doc/MAPGEN.md](doc/MAPGEN.md) | MAPGEN：How buildings and terrain are generated、Adding mapgen entries、Methods |
| [doc/MARTIALART_JSON.md](doc/MARTIALART_JSON.md) | Martial arts and Techniques：Martial arts、Techniques、Attack vectors |
| [doc/MISSIONS_JSON.md](doc/MISSIONS_JSON.md) | Creating missions：type、id、name |
| [doc/MODDING.md](doc/MODDING.md) | Modding guide：Other guides、The basics、Creating a barebones mod |
| [doc/MONSTERS.md](doc/MONSTERS.md) | MONSTERS：Monster properties、"name"、"description" |
| [doc/MONSTER_SPECIAL_ATTACKS.md](doc/MONSTER_SPECIAL_ATTACKS.md) | How to add special attacks to monsters：Monster special attacks、TODO、Adding `special_attacks` to monsters |
| [doc/MOVE_MODE.md](doc/MOVE_MODE.md) | Movement Modes：definition、`type`、`id` |
| [doc/MUTATIONS.md](doc/MUTATIONS.md) | Mutations：System info、Mutagens and primers、Thresholds |
| [doc/NPCs.md](doc/NPCs.md) | NPCs：Creating new NPCs、NPC Class definition、Shopkeeper NPC configuration |
| [doc/OVERMAP.md](doc/OVERMAP.md) | Overmap Generation：Overview、Overmap generation、Terminology and Types |
| [doc/PLAYER_ACTIVITY.md](doc/PLAYER_ACTIVITY.md) | Activities：Adding new activities、JSON Properties、Termination |
| [doc/POINTS_COORDINATES.md](doc/POINTS_COORDINATES.md) | Points, tripoints, and coordinate systems：Axes、Coordinate systems、Vertical coordinates |
| [doc/PORTAL_STORM_BALANCE_AND_DESIGN.md](doc/PORTAL_STORM_BALANCE_AND_DESIGN.md) | Portal Storm Design：Ideas、Reminders、Long Term Desires |
| [doc/POSTAPOC_PRICE_GUIDE.md](doc/POSTAPOC_PRICE_GUIDE.md) | Post-apocalypse Price Guide：Pricing philosophy |
| [doc/PRACTICE_RECIPES.md](doc/PRACTICE_RECIPES.md) | Practice Recipes：JSON fields、Example |
| [doc/PROFICIENCY.md](doc/PROFICIENCY.md) | Proficiencies：Skills and proficiencies、Proficiency trees or graphs、Effects of gaining proficiency |
| [doc/PROFICIENCY_LIST.md](doc/PROFICIENCY_LIST.md) | Proficiencies List：Magiclysm proficiencies |
| [doc/REGION_SETTINGS.md](doc/REGION_SETTINGS.md) | Region Settings：Fields、Example、Region Terrain / Furniture |
| [doc/RELEASE_DIFF.md](doc/RELEASE_DIFF.md) | Release Diff：该主题的说明与参考。 |
| [doc/SOUNDPACKS.md](doc/SOUNDPACKS.md) | Soundpacks：soundpack.txt format、JSON format、Sound effects |
| [doc/STEEL_CRAFTING.md](doc/STEEL_CRAFTING.md) | Making and working with steel grades：Defining Steel Grades、Slag、Budget Steel |
| [doc/TER_FURN_TRANSFORM.md](doc/TER_FURN_TRANSFORM.md) | Terrain and Furniture Transforms：该主题的说明与参考。 |
| [doc/TESTING.md](doc/TESTING.md) | Testing Cataclysm：Guidelines、Writing test cases、Requiring or Checking |
| [doc/TESTING_YOUR_CHANGES.md](doc/TESTING_YOUR_CHANGES.md) | Testing your changes and making sure they work as expected：Style、Applying your changes locally、Using the debug menu |
| [doc/TILESET.md](doc/TILESET.md) | TILESETS：Terminology、JSON Schema、Tile entry |
| [doc/TRANSLATING.md](doc/TRANSLATING.md) | Translating Cataclysm: DDA：Translators、Getting Started、Glossary |
| [doc/TRANSLATING_MOD.md](doc/TRANSLATING_MOD.md) | Translating MOD：In Cataclysm DDA root directory |
| [doc/USER_INTERFACE_AND_ACCESSIBILITY.md](doc/USER_INTERFACE_AND_ACCESSIBILITY.md) | User Interface / Accessibility：SDL version requirement of the tiles build、Compatibility with screen readers |
| [doc/VEHICLES_JSON.md](doc/VEHICLES_JSON.md) | Vehicle prototypes：Vehicle prototypes、Part order、Parts list |
| [doc/VITAMIN.md](doc/VITAMIN.md) | Vitamins：definition、`id`、`type` |
| [doc/WEATHER_TYPE.md](doc/WEATHER_TYPE.md) | Weather Types：`weather_type` properties |
| [doc/WIDGETS.md](doc/WIDGETS.md) | Widgets：Sidebar Modification、Widgets、Required fields |
| [doc/melee_weapons/MELEE_BALANCE_SPREADSHEET.md](doc/melee_weapons/MELEE_BALANCE_SPREADSHEET.md) | Melee Balance Spreadsheet：Overview、Raw、Filter |
| [doc/unicode_chars_palette.txt](doc/unicode_chars_palette.txt) | 地图及界面绘制可用的 Unicode 字符参考。 |

## 模组与数据说明

| 文档位置 | 简介 |
| --- | --- |
| [data/json/LOADING_ORDER.md](data/json/LOADING_ORDER.md) | JSON Loading Order：Same-depth loading order |
| [data/json/mapgen/lab/README.md](data/json/mapgen/lab/README.md) | Lab JSON Quick Guide：Quick Guide for new lab areas:、Quick Guide for new lab dead-ends:、Quick Guide for new lab rooms: |
| [data/json/npcs/godco/NECC_INFO.md](data/json/npcs/godco/NECC_INFO.md) | NPCs：该主题的说明与参考。 |
| [data/json/npcs/refugee_center/FREE_MERCHANTS_INFO.md](data/json/npcs/refugee_center/FREE_MERCHANTS_INFO.md) | Shops：该主题的说明与参考。 |
| [data/mods/Aftershock/README.md](data/mods/Aftershock/README.md) | Design Document：Areas seeking contributors、Size as of 0.F Stable :  31,084 Lines、Here be dragons! |
| [data/mods/Aftershock/crafting_system.md](data/mods/Aftershock/crafting_system.md) | Scrap Crafting System：Overview、Current Scrap Categories、Scrap Tiers Briefly Explained |
| [data/mods/Aftershock/items/armor/exosuit/exosuit_guide.md](data/mods/Aftershock/items/armor/exosuit/exosuit_guide.md) | Exosuit Guide：Getting started、Background、Frame |
| [data/mods/Aftershock/suit_operating_time.md](data/mods/Aftershock/suit_operating_time.md) | Powered Armor Balance：Operating time |
| [data/mods/Backrooms/README.md](data/mods/Backrooms/README.md) | Backrooms CDDA：Warning: You MUST choose the scenario "Backrooms" when creating a character!、Questions、What's the current state of the mod? |
| [data/mods/BlazeIndustries/README.txt](data/mods/BlazeIndustries/README.txt) | README：该主题的说明与参考。 |
| [data/mods/BombasticPerks/docs/contributing.md](data/mods/BombasticPerks/docs/contributing.md) | Contributing to Bombastic Perks：Rules for all content、Naming Convention、Adding |
| [data/mods/BombasticPerks/docs/expanding_with_mods.md](data/mods/BombasticPerks/docs/expanding_with_mods.md) | Expanding Bombastic Perks With Mods：Adding the perk |
| [data/mods/DinoMod/DESIGN.md](data/mods/DinoMod/DESIGN.md) | Design Document SPOILERS AHEAD：What belongs in DinoMod?、Realism vs. Fun、Adding, replacing, removing |
| [data/mods/DinoMod/README.md](data/mods/DinoMod/README.md) | DinoMod：Takeaway Features |
| [data/mods/Graphical_Overmap/readme.txt](data/mods/Graphical_Overmap/readme.txt) | readme：该主题的说明与参考。 |
| [data/mods/MA/README.md](data/mods/MA/README.md) | MA：Implemented Features、Plannned Features、Notes |
| [data/mods/Magiclysm/lore.md](data/mods/Magiclysm/lore.md) | History：Classes、Class Characteristics |
| [data/mods/Magiclysm/magic_balance.md](data/mods/Magiclysm/magic_balance.md) | Spells：Difficulty、Max Level、Attack Stats |
| [data/mods/Megafauna/readme.md](data/mods/Megafauna/readme.md) | readme：该主题的说明与参考。 |
| [data/mods/MindOverMatter/NewPowerGuide.md](data/mods/MindOverMatter/NewPowerGuide.md) | Adding New Powers：Maintaining the Theme、Intelligence Bonuses、Path Capabilities |
| [data/mods/MindOverMatter/PowerDescriptionSpoilers.md](data/mods/MindOverMatter/PowerDescriptionSpoilers.md) | Power Descriptions：Biokinesis、Overcome Pain (C)、Physical Enhancement (C) |
| [data/mods/MindOverMatter/README.md](data/mods/MindOverMatter/README.md) | Mind Over Matter：该主题的说明与参考。 |
| [data/mods/MindOverMatter/lore_spoilers.md](data/mods/MindOverMatter/lore_spoilers.md) | LORE：PROJECT PHAVIAN、HUMAN ASCENSION |
| [data/mods/No_Hope/README.md](data/mods/No_Hope/README.md) | No Hope：List of features |
| [data/mods/Sky_Island/README.md](data/mods/Sky_Island/README.md) | Sky Islands：Warning:、Overview、You Can't Go Back |
| [data/mods/TEST_DATA/README.md](data/mods/TEST_DATA/README.md) | Test Data pseudo-mod：该主题的说明与参考。 |
| [data/mods/Xedra_Evolved/README.md](data/mods/Xedra_Evolved/README.md) | Agents of Change：Lore、I want to believe、Chapter 1 Hail Arcadia |
| [data/mods/alt_map_key/readme.txt](data/mods/alt_map_key/readme.txt) | readme：该主题的说明与参考。 |
| [data/mods/classic_zombies/design-doc.md](data/mods/classic_zombies/design-doc.md) | The DDotDDD - Dark Days of the Dead Design Document：Mission Statement、Gameplay、Desired changes to monster stats |
| [data/mods/classic_zombies/place_names.md](data/mods/classic_zombies/place_names.md) | place names：该主题的说明与参考。 |
| [data/mods/innawood/readme.md](data/mods/innawood/readme.md) | Goal：Changes |

## 工具说明

| 文档位置 | 简介 |
| --- | --- |
| [tools/llama/README.md](tools/llama/README.md) | Using llama to accelerate your build：Troubleshooting |
