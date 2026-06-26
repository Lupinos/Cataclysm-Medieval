---
trigger: always_on
alwaysApply: true
---

# Cataclysm-Medieval：核心工作计划

> 宏观任务追踪，只列出已做和将做的事情。
> 技术方案 → [design00-清理现代内容.md](../docs/design/design00-清理现代内容.md)
> 实现进度 → [modern_content_removal.md](../docs/process/modern_content_removal.md)

---

## 目标

将 CDDA 改造为**中世纪风格**的生存游戏。通过独立 mod 覆写核心数据，不动 `data/json/` 原始文件。

当前阶段：屏蔽掉几乎所有现代内容。后续方向（写实/奇幻）待定。

---

## 调研已完成

- [x] JSON 数据体系 → [json_data_system.md](../docs/vanilla/json_data_system.md)
- [x] Total Conversion 技术方案 → [design00-清理现代内容.md](../docs/design/design00-清理现代内容.md)
- [x] 城市/城镇生成系统 → [code_city_generation_system.md](../docs/vanilla/code_city_generation_system.md)
- [x] 怪物刷新系统 → [code_monster_spawn_system.md](../docs/vanilla/code_monster_spawn_system.md)
- [x] NPC 装备系统 → [code_npc_equipment_system.md](../docs/vanilla/code_npc_equipment_system.md)

- [x] 护甲穿透系统 → [code_armor_penetration_system.md](../docs/vanilla/code_armor_penetration_system.md)

## 实现已完成

- [x] Mod 骨架（modinfo.json + 目录结构）
- [x] EXTERNAL_OPTION：关闭城市/道路
- [x] region_overlay 地图黑名单
- [x] 场景覆盖 + 起始位置修复
- [x] 现代 Background 移除（40 个）
- [x] 现代 Recipe 标记 obsolete（1156 条）
- [x] MONSTER_WHITELIST（WILDLIFE + NULL）
- [x] 覆写 item_group（140 组置空，10 文件）
- [x] 覆写 professions（1个裸体职业 + SCENARIO_BLACKLIST屏蔽所有其他）

## 短线任务：屏蔽现代内容（当前阶段）

> 完成「世界只剩荒野」后，中世纪内容才能从干净的基底上生长。

1. [x] 配置 MONSTER_WHITELIST
2. [x] 覆写 item_group（140 组置空，10 文件）
3. [x] 覆写 professions（1个裸体职业 + 1个场景白名单）

---

## 长线方向：中世纪内容重建

> 短线任务完成后，以下方向逐步展开。每个方向对应各自的调研文档。

### 定居点重建 — [code_city_generation_system.md](../docs/vanilla/code_city_generation_system.md)

- 方案 A（优先）：纯数据驱动 — 中世纪 `regional_settings` + `city_building` 池 + 减小 CITY_SIZE
- 方案 B（远期）：C++ 改动 — 非正交弯曲道路、村庄/城镇类型区分、城墙建筑、中世纪 NPC 替代僵尸密度

### NPC 式怪物体系 — [code_bodypart_hp_system.md](../docs/vanilla/code_bodypart_hp_system.md)

- **决策（2026-05-19 修订）**：~~全面使用 NPC~~ → **双系统分层**
  - **NPC**：人形敌人（强盗、哥布林、巨人等）— 需要装备/技能分布/派系/对话
  - **Monster + 部位 HP 修复**：野兽/巨怪（狼、熊、龙、狮鹫等）— 需要 harvest/dissect/special_attacks
  - Monster 部位 HP 修复仅需改 `apply_damage` 一行 + `get_hp()`/`get_hp_max()` 委托基类
- 纯 JSON 定义不同生物的 `anatomy`（龙/蛇/人类各有不同部位配置）

### 战斗系统深度重构 — [code_bodypart_hp_system.md](../docs/vanilla/code_bodypart_hp_system.md) + [code_combat_system.md](../docs/vanilla/code_combat_system.md) + [code_armor_penetration_system.md](../docs/vanilla/code_armor_penetration_system.md)

- [x] **STR × 武器重量破甲** — `roll_melee_damage_internal` (melee.cpp:1350-1362)：`arpen += weapon_mass_kg × arm_str/10`，bash 全额，stab/cut 折半
- 部位瞄准：玩家可主动选择攻击目标部位
- 骨折/流血/包扎/夹板：Character 原生机制直接复用于所有敌对生物
- 不同生物不同致死判定：砍断龙头致命，砍断龙尾不致命

### 刷新系统适配 — [code_monster_spawn_system.md](../docs/vanilla/code_monster_spawn_system.md)

- NPC 替代 monster 后，刷新通道需从 mongroup 迁移到 NPC spawn 机制
- 精确小队组合（如 2 剑士 + 1 弓箭手 + 1 队长）— 当前 GetResultFromGroup 不支持

### 中世纪制作与经济 — [code_crafting_system.md](../docs/vanilla/code_crafting_system.md)

- 完整中世纪配方链：锻造、炼金、纺织、酿造、制皮
- 中世纪职业树及起始装备体系

### 奇幻方向（可选） — [code_magic_system.md](../docs/vanilla/code_magic_system.md)

- 如果走奇幻路线，需要魔法的 NPC 施法能力
- 法术效果与中世纪世界观融合
