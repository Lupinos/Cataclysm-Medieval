# 部位分血与受伤系统 (Bodypart HP & Injury System)

> CDDA 中 Creature/Monster 的部位分血架构与受伤机制现状调研。

---

## 现有架构分析

### layer 1: 部位蓝图 — `body_part_type`

文件：[`src/bodypart.h:176-375`](file://E:\Cataclysm-Medieval\src\bodypart.h#L176-L375)，[`src/bodypart.cpp:284+`](file://E:\Cataclysm-Medieval\src\bodypart.cpp#L284)

JSON 驱动（`bodypart.json`），通过 `generic_factory` 加载。关键字段：

| 字段 | 说明 |
|------|------|
| `base_hp` | 该部位的默认 HP（默认 60） |
| `hit_size` | 近战命中时的目标大小 |
| `hit_difficulty` | 命中难度（高=精准攻击更易命中此部位） |
| `is_vital` | 部位归零是否导致死亡 |
| `is_limb` | 是否为肢体系部位 |
| `main_part` | 伤害归属的"主部位" |
| `limbtypes` | 部位类型（head/torso/arm/leg/tail/wing/...） |
| `connected_to` | 连接关系（用于断肢判定） |
| `opposite_part` | 对称部位（如左臂→右臂） |

完全可 mod——新部位（如 `tail`、`wing_l`）可通过 JSON 定义。

### layer 2: 部位实例 — `bodypart` class

文件：[`src/bodypart.h:431-520`](file://E:\Cataclysm-Medieval\src\bodypart.h#L431-L520)

```cpp
class bodypart {
    int hp_cur = 0;    // 当前 HP
    int hp_max = 0;    // 最大 HP
    bodypart_str_id id;
    // ... 其他状态
public:
    explicit bodypart( bodypart_str_id id ) : 
        id( id ), hp_cur( id->base_hp ), hp_max( id->base_hp ) {}
    
    int get_hp_cur() const;
    int get_hp_max() const;
    void set_hp_cur( int set );
    void mod_hp_cur( int mod );
    // ...
};
```

每个部位实例拥有独立的 `hp_cur` 和 `hp_max`，初始值来自 `body_part_type::base_hp`。

### layer 3: 身体组装 — `Creature::set_body()`

文件：[`src/creature.cpp:2141-2147`](file://E:\Cataclysm-Medieval\src\creature.cpp#L2141-L2147)

```cpp
void Creature::set_body() {
    body.clear();
    for( const bodypart_id &bp : get_anatomy()->get_bodyparts() ) {
        body.emplace( bp.id(), bodypart( bp.id() ) );
    }
}
```

根据 creature 的 `anatomy`（JSON 中定义的部位列表），为每个部位创建一个 `bodypart` 实例。
- `default_anatomy` → 2 个部位 (torso, head)
- `human_anatomy` → 12 个部位

### layer 4: 部位 HP 查询 — `Creature` 基类方法

文件：[`src/creature.cpp:2246-2376`](file://E:\Cataclysm-Medieval\src\creature.cpp#L2246-L2376)

```cpp
int Creature::get_part_hp_cur( const bodypart_id &id ) const {
    return get_part_helper( *this, id, &bodypart::get_hp_cur );
}
int Creature::get_part_hp_max( const bodypart_id &id ) const {
    return get_part_helper( *this, id, &bodypart::get_hp_max );
}
void Creature::set_part_hp_cur( const bodypart_id &id, int set ) {
    set_part_helper( *this, id, &bodypart::set_hp_cur, set );
}
void Creature::mod_part_hp_cur( const bodypart_id &id, int mod ) {
    set_part_helper( *this, id, &bodypart::mod_hp_cur, mod );
}
```

`get_part_helper` 在 `body` map 中按 `bodypart_str_id` 查找对应的 `bodypart` 实例，查询/修改其 HP。

**这些方法对 monster 同样有效**——它们是 `Creature` 的 non-virtual 方法，monster 继承后直接可用。

### layer 5: 总 HP — `Creature::get_hp()` (无参)

文件：[`src/creature.cpp:2716-2725`](file://E:\Cataclysm-Medieval\src\creature.cpp#L2716-L2725)

```cpp
int Creature::get_hp() const {
    int hp_total = 0;
    for( const auto &elem : get_body() ) {
        hp_total += elem.second.get_hp_cur();
    }
    return hp_total;
}
```

遍历所有部位求和。这是 Creature 基类的默认实现。

---

## Monster 如何绕过部位系统

### monster 的 override 逐行分析

| 方法 | 位置 | 当前行为 | 基类已提供的正确实现 |
|------|------|---------|---------------------|
| `get_hp(bp)` | [monster.cpp:3627](file://E:\Cataclysm-Medieval\src\monster.cpp#L3627-L3629) | `return hp`（全局） | `get_part_hp_cur(bp)` |
| `get_hp_max(bp)` | monster.cpp | `return hp_max`（全局） | `get_part_hp_max(bp)` |
| `apply_damage(src, bp, dam)` | [monster.cpp:2118-2136](file://E:\Cataclysm-Medieval\src\monster.cpp#L2118-L2136) | `hp -= dam`，bp 参数被注释掉 | `mod_part_hp_cur(bp, -dam)` |
| `heal_bp(bp, dam)` | [monster.cpp:2144-2147](file://E:\Cataclysm-Medieval\src\monster.cpp#L2144-L2147) | `heal(dam)`（全局） | `mod_part_hp_cur(bp, dam)` |
| `get_hp()` (无参) | monster.cpp | 返回全局 `hp` | Creature 基类默认实现已遍历求和 |
| `get_hp_max()` (无参) | monster.cpp | 返回全局 `hp_max` | Creature 基类默认实现已遍历求和 |

### `monster::apply_damage` 完整代码

```cpp
void monster::apply_damage( Creature *source, bodypart_id /*bp*/, int dam,
                            const bool /*bypass_med*/ ) {
    if( is_dead_state() ) return;
    reset_pathfinding_cd();
    hp -= dam;           // ← 无视 bp，直接减全局 HP
    if( hp < 1 ) {
        set_killer( source );
    } else if( dam > 0 ) {
        process_trigger( mon_trigger::HURT, 1 + dam / 3 );
        if( source && !aggro_character && !source->is_monster() && !source->is_fake() )
            aggro_character = true;
    }
}
```

---

## Monster 缺失的"受伤"概念

部位分血只是"受伤"的最底层。CDDA 中 **Character（玩家/NPC）** 有三层完整的受伤系统，而 monster 全部缺失。

### 受伤三层模型

| 层级 | 机制 | Character 实现 | Monster 现状 |
|------|------|---------------|-------------|
| **L1: 部位 HP** | `hp_cur` 按部位独立扣减 | ✅ `mod_part_hp_cur(bp, -dam)` | ❌ 全局 `hp -= dam` |
| **L2: 骨折** | `hp_cur ≤ 0` → 部位功能丧失 | ✅ `is_limb_broken(bp)` 影响行动/攻击/穿戴 | ❌ 不存在 — `hp≤0` 直接死亡 |
| **L3: 流血** | `effect_bleed` 按部位绑定，随时间恶化 | ✅ 自动止血判定、手动按压、止血带 | ❌ 不存在 |
| **辅助: 包扎** | `damage_bandaged` 字段存储 | ✅ NPC/玩家可用绷带治疗 | ❌ 字段存在但无用 |
| **辅助: 消毒** | `damage_disinfected` 字段存储 | ✅ 防感染 | ❌ 字段存在但无用 |
| **辅助: 夹板** | `flag_SPLINT` 装备标记 | ✅ 骨折部位需要夹板才能恢复 | ❌ 概念不存在 |

### 骨折系统 (L2)

定义：[`character.cpp:2140`](file://E:Cataclysm-Medieval\src\character.cpp#L2140) — **仅 Character 类有此方法**

```cpp
bool Character::is_limb_broken( const bodypart_id &limb ) const {
    return get_part_hp_cur( limb ) == 0;
}
```

骨折后果（遍布 character 代码）：
- **不能奔跑** — [`can_run()`](file://E:\Cataclysm-Medieval\src\character.cpp#L2145) 检查腿/脚骨折
- **攻击惩罚** — 手臂骨折徒手攻击 ×0.1
- **穿戴限制** — 骨折部位不能穿装备（除非有夹板）
- **施法受限** — 骨折手臂影响施法
- **活动限制** — 手部骨折不能精细操作
- **自动恢复** — 夹板 + 时间 = 逐步恢复

注意 `Creature::set_part_hp_cur` 和 `mod_part_hp_cur` 中的骨折检测：
```cpp
// creature.cpp:2313
bool was_broken = is_avatar() && as_character()->is_limb_broken( id );
```
只对玩家（avatar）触发骨折事件，NPC 骨折是静默的（但影响存在）。

### 流血系统 (L3)

基于 `effect` 系统，`effect_bleed` 按**身体部位**绑定：
```cpp
add_effect( effect_bleed, duration, bodypart_id, ... );
has_effect( effect_bleed, bodypart_id );
```

Character 的流血处理链（[`character.cpp:12899-12998`](file://E:\Cataclysm-Medieval\src\character.cpp#L12899)）：
1. 每回合自动评估止血能力
2. 优先处理最严重的流血部位
3. 空手可手动按压止血
4. 止血带可强制止血
5. 骨折部位止血困难（惩罚）

### Monster 有 effect 系统但不用来受伤

Monster 确实调用了 `add_effect`/`has_effect`（`monster.cpp:280-1133`），但仅限于**全局状态**：

| Monster Effect | 用途 |
|---------------|------|
| `effect_leashed` | 被缰绳拴住 |
| `effect_monster_saddled` | 有鞍具 |
| `effect_monster_armor` | 有护甲 |
| `effect_ridden` | 被骑乘中 |
| `effect_beartrap` | 被捕兽夹夹住 |
| `effect_stunned` | 眩晕 |
| `effect_downed` | 倒地 |
| `effect_critter_well_fed` | 吃饱了 |

**没有任何 `effect_bleed` 或按部位绑定的受伤效果。**

---

## 关键文件索引

| 文件 | 内容 |
|------|------|
| `src/bodypart.h` | `body_part_type` 部位蓝图 + `bodypart` 部位实例 |
| `src/bodypart.cpp` | 部位 JSON 加载、`body_part_type::load()` |
| `src/creature.cpp:2141-2147` | `Creature::set_body()` 身体组装 |
| `src/creature.cpp:2246-2376` | `Creature::get_part_hp_cur/max` 等部位 HP 查询 |
| `src/creature.cpp:2716-2725` | `Creature::get_hp()` 无参总 HP |
| `src/monster.cpp:2118-2136` | `monster::apply_damage()` — 绕过 bp 参数 |
| `src/monster.cpp:3627-3629` | `monster::get_hp(bp)` — 返回全局 hp |
| `src/character.cpp:2140` | `Character::is_limb_broken()` — 骨折判定 |
| `src/character.cpp:12899-12998` | 流血处理链 |

---

## 相关文档

| 文档 | 关系 |
|------|------|
| [combat_system.md](combat_system.md) | 战斗系统（伤害类型、命中、格挡） |
| [../design/medieval_bodypart_hp_design.md](../design/medieval_bodypart_hp_design.md) | Medieval Mod 部位分血改造方案（策划案） |
