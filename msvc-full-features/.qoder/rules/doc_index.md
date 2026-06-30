---
trigger: always_on
alwaysApply: true
---
# 项目文档索引

> 本文件由自动文档归纳机制维护，记录 `.qoder/docs/` 和 `.qoder/repowiki/` 下所有文档文件的索引。
> 新建或更新文档后，务必同步更新此索引。
> 每次对话开始时，你应该回顾此索引了解已有文档，从中查询需要的信息可以避免重复劳动。

## CDDA 原版系统调研 (docs/vanilla/)

> 记录 CDDA 原版代码的架构、机制与实现细节，不涉及中世纪策划内容。
> 文件名前缀：`json_` = JSON 数据层调研，`code_` = C++ 源码机制调研。

### JSON 数据层调研

| 文档 | 说明 |
|------|------|
| [json_data_system.md](../docs/vanilla/json_data_system.md) | JSON数据体系：data/目录结构、加载机制、80+种JSON类型、核心Schema、Mod系统 |
| [json_general.md](../docs/vanilla/json_general.md) | JSON依赖关系图：80+种JSON类型之间的引用/依赖关系全景 |
| [json_itemgroup_monstergroup.md](../docs/vanilla/json_itemgroup_monstergroup.md) | item_group与monstergroup分组粒度分析 |
| [json_itemgroup_organization.md](../docs/vanilla/json_itemgroup_organization.md) | item_group组织概念与目录分布：9维概念体系、概念→目录映射、对Medieval的启示 |
| [json_map.md](../docs/vanilla/json_map.md) | 地图体系：从世界生成到可见地块的完整管线 |
| [json_npc.md](../docs/vanilla/json_npc.md) | NPC配置体系调研：npc_class、对话、任务、faction等JSON配置 |
| [json_martial.md](../docs/vanilla/json_martial.md) | 战斗系统JSON配置：techniques/martialarts/body_parts/anatomy/limb_scores |
| [json_technique_deep.md](../docs/vanilla/json_technique_deep.md) | Technique 字段深度字典：39 个 JSON key 的 C++ 加载默认值、运行时行为、关键 gotcha |
| [json_mission.md](../docs/vanilla/json_mission.md) | 任务与剧情系统：missiondef/effects_on_condition/talk_topic |

### C++ 机制调研

| 文档 | 说明 |
|------|------|
| [code_time_system.md](../docs/vanilla/code_time_system.md) | 时间系统：时间单位、Speed/Moves/动作消耗关系、游戏主循环、怪物速度 |
| [code_combat_system.md](../docs/vanilla/code_combat_system.md) | 战斗系统：伤害类型、护甲穿透、近战命中/暴击/格挡、远程瞄准/后坐力 |
| [code_magic_system.md](../docs/vanilla/code_magic_system.md) | 魔法系统：法术定义、能量来源、33种法术效果、附魔与触发式法术 |
| [code_mutation_bionic_system.md](../docs/vanilla/code_mutation_bionic_system.md) | 变异与生化改造：突变类别/阈值、生化模块能量/安装/升级 |
| [code_crafting_system.md](../docs/vanilla/code_crafting_system.md) | 制作与技能：双轨制技能系统、配方学习、熟练度、建造蓝图 |
| [code_nutrition_health_system.md](../docs/vanilla/code_nutrition_health_system.md) | 营养与健康：胃/肠道消化、卡路里计算、维生素、饮食限制、代谢率 |
| [code_bodypart_hp_system.md](../docs/vanilla/code_bodypart_hp_system.md) | 部位分血架构：Creature五层部位体系、Monster绕过机制、Character受伤三层模型 |
| [code_monster_spawn_system.md](../docs/vanilla/code_monster_spawn_system.md) | 怪物刷新系统：MonsterGroupEntry/GetResultFromGroup核心算法、5条刷新通道 |
| [code_npc_equipment_system.md](../docs/vanilla/code_npc_equipment_system.md) | NPC装备系统：三层override机制、17槽位着装链、武器按技能选择、bandit分析 |
| [code_city_generation_system.md](../docs/vanilla/code_city_generation_system.md) | 城市/城镇生成系统：place_cities()入口、build_city_street()递归、建筑池 |
| [code_weapon_to_hit_system.md](../docs/vanilla/code_weapon_to_hit_system.md) | 武器命中与双手系统：grip/surface/length/balance四属性计算m_to_hit、ALWAYS_TWOHAND判定 |
| [code_material_system.md](../docs/vanilla/code_material_system.md) | 材料系统：material_type加载/验证流程、damage_type注册机制、stab抗性引擎支持、钢材7级分级与chain变体 |
| [code_armor_penetration_system.md](../docs/vanilla/code_armor_penetration_system.md) | 护甲穿透系统：damage_unit→res_pen/res_mult全程链路、Character/Monster护甲吸收、Medieval STR×重量破甲改造 |
| [code_localization_system.md](../docs/vanilla/code_localization_system.md) | 本地化与国际化系统：延迟翻译容器translation、自制MO解析器与哈希查找、自动化JSON文本提取工作流与Mod本地化策略 |
| [code_item_damage_system.md](../docs/vanilla/code_item_damage_system.md) | 物品伤害/破损等级系统：底层的整千倍乘与离散折叠算法，剖析 JSON 伤害概率塌陷与强盗装备“整齐划一”的数学机理 |
| [code_harvest_drop_system.md](../docs/vanilla/code_harvest_drop_system.md) | 解剖/屠宰产物系统：harvest_drop_type→harvest→monster三层key引用链、harvest vs dissect差异、C++数据流 |
| [monster_wildlife_hp_overview.md](../docs/vanilla/monster_wildlife_hp_overview.md) | 原版野生动物HP概览：哺乳动物/鸟类/爬行两栖/鱼类血量分布与Medieval参考标尺 |


## 中世纪策划案 (docs/design/)

> Medieval Mod 的未来规划与方案设计。编号体系：00 为总纲，01-07 为系统策划，08 为敌人体系。
> 现状调研 → [vanilla/](../docs/vanilla/)，实现进度 → [process/](../docs/process/)。

### 总纲

| 编号 | 文档 | 说明 |
|------|------|------|
| 00 | [design00-清理现代内容.md](../docs/design/design00-清理现代内容.md) | 中世纪转换 mod 设计方案：5层拦截架构、item_group覆写策略、物品注入通道、硬编码限制 |

### 系统策划

| 编号 | 文档 | 说明 |
|------|------|------|
| 01 | [design01-世界观.md](../docs/design/design01-世界观.md) | 世界观与威胁体系：中世纪背景设定、危险来源、文明等级 |
| 02 | [design02-盔甲.md](../docs/design/design02-盔甲.md) | 盔甲体系：14世纪末~15世纪初过渡期，布料→锁子甲→板甲的完整防护链 |
| 02_1 | [design02_1-布里根丁与板甲衣细分.md](../docs/design/design02_1-布里根丁与板甲衣细分.md) | 布里根丁与板甲衣细分及抽象化重构：退化抽象基类模板，细化10件过渡期防具及配套肢体防具 |
| 03 | [design03-日常衣物.md](../docs/design/design03-日常衣物.md) | 低端衣物与日常装备（平民层）：麻、羊毛、基础皮革，覆盖全阶层日常着装 |
| 04 | [design04-武器.md](../docs/design/design04-武器.md) | 武器体系：Oakeshott XV-XVIII型、60+种武器分类、伤害类型×反甲逻辑矩阵 |
| 04_1 | [design04_1-quality体系.md](../docs/design/design04_1-quality体系.md) | 装备 Quality 体系（设计冻结/非初版）：材料变体走JSON copy-from，Quality作为纯运行时属性，区分武器/盔甲影响 |
| 05 | [design05-职业.md](../docs/design/design05-职业.md) | 开局职业与技能映射：中世纪社会阶层→CDDA profession/skill体系 |
| 06 | [design06-建筑.md](../docs/design/design06-建筑.md) | 中世纪聚落与建筑体系：村庄布局、建筑类型、材料与建造逻辑 |
| 07 | [design07-冒险者工会.md](../docs/design/design07-冒险者工会.md) | 冒险者工会体系：单一工会/多分会架构、声望等级、三层任务池、NPC/服务设计 |

### 敌人体系

| 编号 | 文档 | 说明 |
|------|------|------|
| 08 | [design08-敌人.md](../docs/design/design08-敌人.md) | **总决策**：双系统分层（NPC用于人形敌人，Monster+部位HP修复用于野兽/巨怪） |
| 08_1 | [design08_1-野怪_强盗.md](../docs/design/design08_1-野怪_强盗.md) | NPC 体系（一）—— 强盗：刷新配置、装备池、AI行为 |
| 08_2 | [design08_2-野怪_野生动物.md](../docs/design/design08_2-野怪_野生动物.md) | ⚠️ 修订为 Monster 路线 —— 14种真实中世纪动物（数值可作 Monster JSON 参考） |
| 08_3 | [design08_3-野怪_奇幻.md](../docs/design/design08_3-野怪_奇幻.md) | ⚠️ 拆分为 NPC/ Monster —— 14种奇幻生物，生态+战利品，标注各自归属系统 |

### 战斗体系

| 编号 | 文档 | 说明 |
|------|------|------|
| 09 | [design09-战斗系统重置.md](../docs/design/design09-战斗系统重置.md) | 战斗系统深度重置：手动技艺选择 + 部位瞄准，双轮UI、n/k技能线性缩放 |
| 09_1 | [design09_1-部位血量系统.md](../docs/design/design09_1-部位血量系统.md) | 部位血量系统：移除 monster::hp，vital 部位死亡判定 + 塔科夫式伤害扩散 |
| 09_2 | [design09_2-怪物部位行动影响.md](../docs/design/design09_2-怪物部位行动影响.md) | 怪物部位伤害对行动的影响：方案 B 设计与实施计划（未完成） |


## 实现进度 (docs/process/)

> Medieval Mod 各功能模块的实现进度跟踪。任务追踪详见 [core_work.md](core_work.md)。

| 文档 | 说明 |
|------|------|
| [modern_content_removal.md](../docs/process/modern_content_removal.md) | 现代内容清除进度：5层拦截架构执行状态、1156条Recipe/40个Background移除详情 |
| [medieval_professions.md](../docs/process/medieval_professions.md) | 开局职业实现进度：当前3个职业与待实现职业清单 |
| [medieval_armor.md](../docs/process/medieval_armor.md) | 盔甲体系实现进度：13个占位符JSON按部位/层分隔，head→neck→torso×6→arms→hands→legs→feet→cloaks |
| [medieval_clothing.md](../docs/process/medieval_clothing.md) | 日常衣物实现进度：29件平民服装+2种新材料，head/torso/legs/feet/cloaks/hands/accessories 共9文件 |
| [medieval_weapons.md](../docs/process/medieval_weapons.md) | 武器体系实现进度：剑系6+斧系4+锤系5，共15件近战武器，steel单材质等级 |
| [medieval_settlement.md](../docs/process/medieval_settlement.md) | 聚落与地图实现进度：T5农舍测试mapgen、palette体系、overmap_terrain定义 |
| [medieval_combat_rebalance.md](../docs/process/medieval_combat_rebalance.md) | 战斗重平衡进度：STR×武器重量破甲（C++ melee.cpp）、待考虑的后续改造项 |
| [medieval_i18n_workflow.md](../docs/process/medieval_i18n_workflow.md) | 独立本地化工作流：基于规范 PO 的 0 硬编码编译与 AI 翻译增补流程 |
| [medieval_bandit_system.md](../docs/process/medieval_bandit_system.md) | 强盗与遭遇系统进度：8大NPC类型、弹药自适应口袋、剧情收费路匪/乞丐陷阱、8组遭遇 EOC |
| [monster_bodypart_fix.md](../docs/process/monster_bodypart_fix.md) | Monster 部位 HP 修复计划：C++ 改动清单 (~10行) + 新部位/anatomy/测试点 |
| [example_griffin.md](../docs/process/example_griffin.md) | 狮鹫示例改造计划：完整引用链（body_part→anatomy→monster→harvest→item） |
| [ranged_aimed_part.md](../docs/process/ranged_aimed_part.md) | 射击部位瞄准系统：等效面积 BFS + targeting_graph 换 root + `~` 快捷键 |

## 项目工程文档 (repowiki/)

> Qoder 自动生成的项目层面文档，涵盖构建系统、项目结构、工具链等工程性知识。

### 总览

| 文档 | 说明 |
|------|------|
| [项目概述](../repowiki/zh/content/项目概述.md) | 项目背景、技术栈、架构概览 |
| [快速开始](../repowiki/zh/content/快速开始.md) | 环境搭建、编译运行、基本操作 |
| [开发工作流](../repowiki/zh/content/开发工作流.md) | 日常开发流程、分支策略、代码审查 |
| [故障排除](../repowiki/zh/content/故障排除.md) | 常见编译/运行时问题及解决方案 |
| [测试框架](../repowiki/zh/content/测试框架.md) | Catch2测试框架使用、测试编写规范 |
| [部署与分发](../repowiki/zh/content/部署与分发.md) | 打包、发布、CI/CD流程 |

### 项目结构详解

| 文档 | 说明 |
|------|------|
| [项目结构详解](../repowiki/zh/content/项目结构详解/项目结构详解.md) | 工程目录布局、各目录职责 |
| [解决方案组织结构](../repowiki/zh/content/项目结构详解/解决方案组织结构.md) | .sln与.vcxproj组织方式 |
| [项目依赖关系](../repowiki/zh/content/项目结构详解/项目依赖关系.md) | 各子项目间编译依赖 |
| [项目文件配置详解](../repowiki/zh/content/项目结构详解/项目文件配置详解.md) | .vcxproj/.props文件配置说明 |
| [共享配置管理](../repowiki/zh/content/项目结构详解/共享配置管理.md) | Cataclysm-common.props等公共配置 |

### 构建系统架构

| 文档 | 说明 |
|------|------|
| [构建系统架构](../repowiki/zh/content/构建系统架构/构建系统架构.md) | MSBuild + vcpkg 构建体系概述 |
| [MSBuild配置详解](../repowiki/zh/content/构建系统架构/MSBuild配置详解.md) | .props/.targets文件与编译开关 |
| [多平台构建支持](../repowiki/zh/content/构建系统架构/多平台构建支持.md) | Windows/Linux/macOS构建差异 |
| [构建流程详解](../repowiki/zh/content/构建系统架构/构建流程详解.md) | 从源码到可执行文件的完整流程 |
| [静态链接策略](../repowiki/zh/content/构建系统架构/静态链接策略.md) | 静态库链接方案与优化 |

### 依赖管理系统

| 文档 | 说明 |
|------|------|
| [依赖管理系统](../repowiki/zh/content/依赖管理系统/依赖管理系统.md) | vcpkg + 自定义端口管理 |
| [SDL2生态系统集成](../repowiki/zh/content/依赖管理系统/SDL2生态系统集成.md) | SDL2及其扩展库的集成方式 |
| [vcpkg配置详解](../repowiki/zh/content/依赖管理系统/vcpkg配置详解.md) | vcpkg.json与triplet配置 |
| [依赖版本管理](../repowiki/zh/content/依赖管理系统/依赖版本管理.md) | 版本锁定、升级策略 |
| [自定义端口开发](../repowiki/zh/content/依赖管理系统/自定义端口开发.md) | 自维护vcpkg端口开发指南 |

### 核心模块

| 文档 | 说明 |
|------|------|
| [核心模块](../repowiki/zh/content/核心模块/核心模块.md) | 核心模块总览与模块间协作 |
| [图形渲染系统](../repowiki/zh/content/核心模块/图形渲染系统.md) | SDL2渲染管线、Tile绘制 |
| [输入处理系统](../repowiki/zh/content/核心模块/输入处理系统.md) | 键盘/鼠标事件处理链 |
| [音频处理系统](../repowiki/zh/content/核心模块/音频处理系统.md) | SDL2_mixer音效与音乐管理 |

#### 游戏引擎核心

| 文档 | 说明 |
|------|------|
| [游戏引擎核心](../repowiki/zh/content/核心模块/游戏引擎核心/游戏引擎核心.md) | 引擎核心架构与主控流程 |
| [游戏循环系统](../repowiki/zh/content/核心模块/游戏引擎核心/游戏循环系统.md) | 主循环、帧率控制、事件分发 |
| [世界生成系统](../repowiki/zh/content/核心模块/游戏引擎核心/世界生成系统.md) | 地图生成、Overmap、区域生成 |
| [人工智能系统](../repowiki/zh/content/核心模块/游戏引擎核心/人工智能系统.md) | NPC/Monster AI行为树 |
| [天气系统](../repowiki/zh/content/核心模块/游戏引擎核心/天气系统.md) | 天气模拟、季节变化 |
| [战斗机制](../repowiki/zh/content/核心模块/游戏引擎核心/战斗机制.md) | 战斗引擎核心逻辑 |
| [物品管理系统](../repowiki/zh/content/核心模块/游戏引擎核心/物品管理系统.md) | 物品生命周期、库存管理 |

#### 数据管理系统

| 文档 | 说明 |
|------|------|
| [数据管理系统](../repowiki/zh/content/核心模块/数据管理系统/数据管理系统.md) | 数据层架构总览 |
| [JSON数据处理系统](../repowiki/zh/content/核心模块/数据管理系统/JSON数据处理系统.md) | JSON加载、校验、类型系统 |
| [FlatBuffers集成与配置](../repowiki/zh/content/核心模块/数据管理系统/FlatBuffers集成与配置.md) | FlatBuffers用于存档/网络通信 |
| [数据序列化与反序列化](../repowiki/zh/content/核心模块/数据管理系统/数据序列化与反序列化.md) | 序列化框架与版本兼容 |
| [存档与读档系统](../repowiki/zh/content/核心模块/数据管理系统/存档与读档系统.md) | 存档格式、迁移、压缩 |

### 自动化工具链

| 文档 | 说明 |
|------|------|
| [自动化工具链](../repowiki/zh/content/自动化工具链/自动化工具链.md) | 工具链总览与协作关系 |
| [预构建脚本](../repowiki/zh/content/自动化工具链/预构建脚本.md) | 编译前预处理步骤 |
| [代码格式化配置](../repowiki/zh/content/自动化工具链/代码格式化配置.md) | AStyle/clang-format统一风格 |
| [JSON格式化工具](../repowiki/zh/content/自动化工具链/JSON格式化工具.md) | JSON数据格式校验与美化 |
| [分发脚本](../repowiki/zh/content/自动化工具链/分发脚本.md) | 打包发布自动化脚本 |
