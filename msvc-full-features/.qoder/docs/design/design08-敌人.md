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

## 改造方案（Monster 路线 — 已放弃）

> ⚠️ 此方案经完整评估后已放弃。保留作为技术参考，Medieval Mod 走 NPC 路线。

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

## 最终决策：放弃 Monster，全面使用 NPC 系统

> 2026-05-03：经过完整的部位分血 + 受伤系统评估，决定 **Medieval Mod 不使用 monster 系统**。

### 决策对比

| 维度 | Monster + 部位分血改造 | NPC 系统（Character） |
|------|----------------------|---------------------|
| **部位 HP** | 需 C++ 改造（~65 行） | ✅ 原生 12 部位分血 |
| **解剖学自定义** | 需 C++ 改造 + JSON | ✅ 纯 JSON（`anatomy` 系统） |
| **骨折** | 需要从零实现 | ✅ 原生 `is_limb_broken` |
| **流血** | 需要从零实现 | ✅ 原生 `effect_bleed` |
| **包扎/消毒/夹板** | 需要从零实现 | ✅ 原生支持 |
| **部位伤残影响** | 需要从零实现 | ✅ 骨折影响奔跑/攻击/穿戴/施法 |
| **护甲按部位** | 需额外实现 | ✅ 原生 per-part armor |
| **NPC AI 行为** | 需额外实现 | ✅ 原生 AI（战斗/逃跑/对话） |
| **JSON 工作量** | 大（全新怪物体系） | 中（改造 NPC 模板） |
| **C++ 工作量** | 大（~65 行基础 + 无数附加） | **零** |

### 路线选择

**主路线：NPC（Character）系统**
- 所有"敌对生物"实际是 NPC，继承全套 Character 能力
- 纯 JSON 即可定义不同生物的部位配置、HP、护甲
- 利用 `anatomy` 系统定义不同生物的部位数量和类型
- 利用 NPC faction/ai 系统控制行为

**备选路线：重新实现的平行类**
- 如果未来 NPC 系统在性能或行为上有无法接受的限制
- 可以考虑 fork 出 Character 的核心部位/受伤逻辑到新的 `combatant` 基类
- 但这是远期选项，优先用 NPC 验证玩法可行性

---

## 相关文档

| 文档 | 关系 |
|------|------|
| [bodypart_hp_system.md](../vanilla/bodypart_hp_system.md) | Creature/Monster 部位分血架构现状调研 |
| [combat_system.md](../vanilla/combat_system.md) | 战斗系统（伤害类型、命中、格挡） |
| [medieval_conversion_design.md](medieval_conversion_design.md) | 中世纪转换整体技术方案 |
