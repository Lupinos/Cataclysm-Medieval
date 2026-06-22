# 中世纪部位分血改造方案

> Medieval Mod 战斗系统：部位分血、骨折、流血系统的方案设计与最终决策。
> 现状架构分析见 → [bodypart_hp_system.md](../vanilla/bodypart_hp_system.md)

---

## 动机

中世纪战斗需要：
- **不同生物有不同部位**：龙有头/躯干/尾/翼/四肢，人类有12部位，蛇只有头+身
- **玩家瞄准特定部位**：攻击龙头 vs 龙尾应有不同效果
- **部位独立死亡判定**：砍断龙尾不应致命，砍断龙头应致命

CDDA 的 `Creature` 基类已内置完整部位分血框架，但 `monster` 子类用全局 HP 绕过了这套设施。

---

## Monster 部位 HP 修复方案

### Phase 1: C++ 改动（核心）

改动集中在 `src/monster.cpp` 和 `src/monster.h`，约需修改 6 个方法 + 1 个成员变量。

#### 1.1 移除/重算全局 HP 成员

当前 `monster` 有成员变量 `int hp` 和 `int hp_max`。改造后：

**方案 A（推荐）**：保留 `hp_max` 作为"总血量"概念（JSON 的 `"hp"` 字段分配到各部位），移除独立的 `hp` 变量。

**方案 B**：完全移除 `hp` 和 `hp_max`，所有 HP 查询走 `Creature` 基类部位求和。

#### 1.2 重写 `apply_damage`

```
Before:  hp -= dam;  → 判断 hp <= 0
After:   mod_part_hp_cur(bp, -dam);  → 检查致命部位是否归零
```

关键变化：死亡判定从"全局 HP"改为"致命部位 HP"。

```cpp
void monster::apply_damage( Creature *source, bodypart_id bp, int dam, bool ) {
    if( is_dead_state() ) return;
    reset_pathfinding_cd();
    
    mod_part_hp_cur( bp, -dam );  // 改用部位分血
    
    // 死亡判定：致命部位（vital）任一归零即死
    bool vital_dead = false;
    for( auto [id, part] : get_body() ) {
        if( id->is_vital && part.get_hp_cur() <= 0 ) {
            vital_dead = true;
            break;
        }
    }
    if( vital_dead ) {
        set_killer( source );
    } else if( dam > 0 ) {
        process_trigger( mon_trigger::HURT, 1 + dam / 3 );
    }
}
```

#### 1.3-1.8 其余改动

- 重写 `get_hp(bp)` / `get_hp_max(bp)` → 委托给基类
- 重写 `get_hp()` / `get_hp_max()` (无参) → 移除 override，使用 Creature 默认
- 重写 `heal_bp` → `mod_part_hp_cur(bp, dam)`
- 重写 `hp_percentage()` → 基于部位总和
- `monster::die()` 适配
- 验证所有调用点（melee, creature, UI HP 条）

### Phase 2: JSON 改动（mod 层）

- 定义新部位类型（tail, wing 等）
- 定义生物解剖学（anatomy_dragon, anatomy_serpent 等）
- 怪物 JSON 引用解剖学
- 按部位分配 HP 策略（部位比例分配 vs 部位独立设定）

### Phase 3: UI 适配（后续考虑）

- 怪物 HP 条 → 改后自然显示总部位 HP
- 部位 HP 显示（可选）
- 攻击目标选择（可选）
- 断尾等特殊效果（可选）

### 改动总结

| 文件 | 改动点 | 行数估算 |
|------|--------|---------|
| `monster.h` | 移除/调整 `hp`/`hp_max` 成员 | ~5 行 |
| `monster.cpp` | 重写 6 个 HP 相关方法 | ~40 行 |
| `monster.cpp` | `die()` / 相关死亡判定适配 | ~20 行 |
| `data/json/bodyparts/` | 新增部位（tail 等） | 按需 |
| `data/json/anatomy.json` | 新增解剖学定义 | 每个生物 ~10 行 |
| **C++ 总改动** | | **~65 行** |

---

## 最终决策：双系统分层（2026-05-19 修订）

> ~~2026-05-03：全面使用 NPC~~  
> **2026-05-19 修订**：原决策"全员 NPC"被推翻。正确的做法是按生物类型分层——不是全或无。

### 推翻原因

把动物塞进 NPC 存在致命缺陷：

1. **NPC 没有 harvest/dissect 机制**。动物/龙被杀死后无法出肉/皮/骨/器官——这是动物最核心的需求。
2. **NPC 模板有 30+ 个字段，动物只需要其中 5 个**。skills/rng/装备池/出身故事/对话/商人——全是噪音。
3. **Monster 已有很多动物需要的功能**：special_attacks（咬/抓/毒/扑）、anger/fear triggers、简单伤害公式——而 NPC 没有。
4. **Monster 修部位 HP 只需要改 `apply_damage` 一行**，不是 ~65 行。

### 修订后对比

| 维度 | Monster + 部位 HP 修复 | NPC（Character） |
|------|----------------------|---------------------|
| **部位 HP** | 修 `apply_damage` 一行 | ✅ 原生 |
| **骨折/流血** | ❌（动物不需要） | ✅ |
| **harvest/dissect** | ✅ 原生 | ❌ 需从零新写代码 |
| **special_attacks** | ✅ 原生（咬/抓/扑/毒） | ❌（NPC 只有平 A） |
| **装备/技能分布** | ❌ | ✅ |
| **对话/派系** | ❌ | ✅ |
| **C++ 工作量** | ~5 行 | 中等（harvest 需新增） |

### 分层路线

```
需要装备/对话/技能分布？
    │
    ├── 是 → NPC 系统
    │       强盗、哥布林、大地精、巨魔、食人魔、巨人
    │
    └── 否 → Monster 系统（+ 部位 HP 修复）
            狼、熊、鹿、野猪（纯野兽）
            飞龙、地龙、狮鹫、蛇龙、树妖（纯战斗生物）
```

| 生物 | 系统 | 判断依据 |
|------|------|---------|
| 强盗/士兵 | NPC | 需要装备+技能分布+对话+派系 |
| 哥布林 | NPC | 需要部落派系+装备偏好+偷窃行为 |
| 大地精 | NPC | 需要军事化装备+纪律行为 |
| 狗头人 | NPC | 需要陷阱+洞穴派系 |
| 食人魔 | NPC | 需要粗糙装备+简单嗜好 |
| 山岭巨人 | NPC | 需要粗糙装备+投石行为 |
| 独眼巨人 | NPC | 需要放牧行为+可能对话 |
| 沼泽巨人 | NPC | 不需要对话但有区域行为 |
| 牛头人 | NPC | 需要迷宫守护行为+武器 |
| **狼/熊/鹿/野猪** | **Monster** | 纯野兽，不需要装备/对话，需要 harvest |
| **飞龙/地龙/蛇龙** | **Monster** | 不需要装备/对话，需要 harvest + special_attacks |
| **狮鹫/蝎尾狮** | **Monster** | 不需要装备/对话，需要 harvest（可骑性另议） |
| **树妖/多头蛇蜥** | **Monster** | 不需要装备/对话，需要 harvest |

### Monster 部位 HP 修复（全部 C++ 改动）

```cpp
// src/monster.cpp — 当前
void monster::apply_damage(Creature *source, bodypart_id /*bp*/, int dam, ...) {
    if( is_dead_state() ) return;
    hp -= dam;  // ❌ 绕过部位
}

// 改为：
void monster::apply_damage(Creature *source, bodypart_id bp, int dam, ...) {
    if( is_dead_state() ) return;
    mod_part_hp_cur( bp, -dam );  // ✅ 走 Creature 基类部位方法
    // 死亡判定改为检查致命部位归零
}
```

同时修复 `get_hp()` / `get_hp(bp)` / `get_hp_max()` 委托给基类。总改动 ~5 行。

Monster 的 `set_body()` 已经支持通过 `anatomy` JSON 定义部位——修复这三行后，纯 JSON 就能定义不同动物的部位配置。

---

## 相关文档

| 文档 | 关系 |
|------|------|
| [bodypart_hp_system.md](../vanilla/bodypart_hp_system.md) | Creature/Monster 部位分血架构现状调研 |
| [combat_system.md](../vanilla/combat_system.md) | 战斗系统（伤害类型、命中、格挡） |
| [medieval_conversion_design.md](medieval_conversion_design.md) | 中世纪转换整体技术方案 |
