# 中世纪战斗重平衡：实现进度

> 对 CDDA 战斗系统进行中世纪适配的 C++ 级改动跟踪
> 调研文档：[code_combat_system.md](../vanilla/code_combat_system.md) | [code_armor_penetration_system.md](../vanilla/code_armor_penetration_system.md) | [code_weapon_to_hit_system.md](../vanilla/code_weapon_to_hit_system.md)

---

## 已完成的改造

### 1. STR × 武器重量破甲

- [x] **实现**：`roll_melee_damage_internal` (`melee.cpp:1350-1362`) 中新增
- [x] **逻辑**：`arpen += weapon_mass_kg × (arm_str / 10)`
  - bash 伤害：全额加成
  - stab/cut 伤害：折半（×0.5）
  - 仅对持武器攻击生效（徒手走独立的 `unarmed_arpen` 体系）
- [x] **调研**：[code_armor_penetration_system.md](../vanilla/code_armor_penetration_system.md)

---

### 2. 战斗系统深度重置策划案

- [x] **策划**：[design09-战斗系统重置.md](../design/design09-战斗系统重置.md) 已完成
- [ ] **实现**：待开始
- **核心内容**：
  - 精确攻击快捷键（类似 `f` 射击逻辑）：选择敌人 → 技艺菜单 → 部位菜单
  - Tab/移动撞敌保持原版自动攻击不变
  - 技艺选择 UI：仅显示当前可用技艺，过滤条件/技能/武器/攻击肢体
  - 部位选择 UI：技艺白名单限制 + 预估命中率显示
  - 数值公式：`n = 3 + skill×1.2`（部位权重放大）, `k = 30 - skill×2.5`（命中惩罚）
  - C++ 改造点：`melee.cpp` 新入口、`anatomy.cpp` 瞄准参数、`martialarts.h` JSON 扩展

---

## 待考虑的改造

| 项目 | 说明 | 优先级 |
|------|------|--------|
| 精确攻击实现 (design09) | 详见策划案，涉及 UI + 核心逻辑 + JSON 扩展 | **高** |
| JSON `melee_damage` 支持 `arpen` 字段 | 允许匕首/rapier 等轻武器获得 JSON 级固定穿甲，弥补重量破甲的盲区 | 中 |
| 材料影响破甲倍率 | 高碳钢武器 vs 低碳钢，`res_mult` 差异 | 低 |
| 武器破甲与攻速权衡 | 破甲高的武器攻速惩罚更大 | 低 |
| Quality 系统的 C++ 基础 | `item::item_vars` 存储 quality，`damage_melee` 末尾乘系数 | 远期 |
| Monster→NPC 迁移后武器破甲 | Monster 使用 NPC Character 体系后，自动享受重量破甲 | 远期 |
