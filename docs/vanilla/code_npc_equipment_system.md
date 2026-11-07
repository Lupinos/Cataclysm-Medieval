# NPC 装备系统

> 调查日期：2026-05-04 — 为理解强盗装备指定机制而调研。

---

## 1. 概述

NPC 的装备（着装、武器、物品栏）完全由 `item_group` 系统驱动。每个 `npc_class` 通过以下机制决定装备：

```
npc_class (JSON)
  ├── worn_override    → item_group_id  ─→ 全身着装（替代 17 槽位系统）
  ├── carry_override   → item_group_id  ─→ 物品栏（替代默认 misc 系统）
  ├── weapon_override  → item_group_id  ─→ 武器（替代技能匹配系统）
  │
  └── 默认机制（无 override 时）：
        ├── 着装: <class>_<slot> → npc_<slot> 回退链（17个槽位）
        ├── 武器: <class>_<skill> → npc_<skill> 回退链（按最佳战斗技能）
        └── 物品栏: <class>_misc → npc_misc 回退链 + 弹药逻辑
```

---

## 2. 三层 Override（顶层控制）

定义在 [npc_class.h](file:///E:/Cataclysm-Medieval/src/npc_class.h) L108-110：

```cpp
item_group_id worn_override;     // 不为空时，完全替代 17 槽位着装系统
item_group_id carry_override;    // 不为空时，完全替代默认物品栏系统
item_group_id weapon_override;   // 不为空时，完全替代技能匹配武器系统
```

JSON 加载在 [npc_class.cpp](file:///E:/Cataclysm-Medieval/src/npc_class.cpp) L303-305：

```cpp
optional( jo, was_loaded, "worn_override", worn_override );
optional( jo, was_loaded, "carry_override", carry_override );
optional( jo, was_loaded, "weapon_override", weapon_override );
```

校验在 [npc_class.cpp](file:///E:/Cataclysm-Medieval/src/npc_class.cpp) L150-159 —— 如果 override 不为空但 `item_group` 不存在，发出 debugmsg。

**使用场景**：大多数有特殊外观的 NPC 用 override（如 GODCO 守卫、Exodii 商人等），普通随机 NPC 则不用 override。

---

## 3. 默认着装系统（17 槽位链）

代码入口：[npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L818-857 `starting_clothes()`

### 3.1 核心函数

```cpp
// 三参数版本: "<class>_<what>" → 回退到 fallback
static item random_item_from( const npc_class_id &type, const std::string &what,
                              const item_group_id &fallback )
{
    item result = item_group::item_from( item_group_id( type.str() + "_" + what ), calendar::turn );
    if( result.is_null() ) {
        result = item_group::item_from( fallback, calendar::turn );
    }
    return result;
}

// 两参数版本: "<class>_<what>" → 回退到 "npc_<what>"
static item random_item_from( const npc_class_id &type, const std::string &what )
{
    return random_item_from( type, what, item_group_id( "npc_" + what ) );
}

// 性别感知版本: "<class>_<what>_<gender>" → "<class>_<what>" → "npc_<what>_<gender>"
static item get_clothing_item( const npc_class_id &type, const std::string &what, bool male )
{
    // 1. 先查 class 的性别版本: <class>_pants_male / <class>_pants_female
    // 2. 回退到 class 的通用版本: <class>_pants
    // 3. 最后回退到 npc 的性别版本: npc_pants_male / npc_pants_female
}
```

### 3.2 17 个装备槽位

```cpp
void starting_clothes( npc &who, const npc_class_id &type, bool male )
{
    if( worn_override ) {
        ret = item_group::items_from( type->worn_override );  // 一次性搞定
    } else {
        // ★ 以下是 17 个槽位，各自独立查找 item_group：
        ret.push_back( get_clothing_item( type, "pants", male ) );           // 1. 裤子（性别）
        ret.push_back( get_clothing_item( type, "shirt", male ) );           // 2. 上衣（性别）
        ret.push_back( get_clothing_item( type, "underwear_top", male ) );   // 3. 内衣上（性别）
        ret.push_back( get_clothing_item( type, "underwear_bottom", male ) );// 4. 内衣下（性别）
        ret.push_back( get_clothing_item( type, "underwear_feet", male ) );  // 5. 袜子（性别）
        ret.push_back( get_clothing_item( type, "shoes", male ) );           // 6. 鞋子（性别）
        ret.push_back( random_item_from( type, "gloves" ) );                 // 7. 手套
        ret.push_back( random_item_from( type, "coat" ) );                   // 8. 外套
        ret.push_back( random_item_from( type, "vest" ) );                   // 9. 背心
        ret.push_back( random_item_from( type, "masks" ) );                  // 10. 面具
        ret.push_back( random_item_from( type, "glasses", Item_spawn_data_npc_eyes ) ); // 11. 眼镜
        ret.push_back( random_item_from( type, "hat" ) );                    // 12. 帽子
        ret.push_back( random_item_from( type, "scarf" ) );                  // 13. 围巾
        ret.push_back( random_item_from( type, "storage" ) );                // 14. 背包/存储
        ret.push_back( random_item_from( type, "holster" ) );                // 15. 枪套
        ret.push_back( random_item_from( type, "belt" ) );                   // 16. 腰带
        ret.push_back( random_item_from( type, "wrist" ) );                  // 17. 手腕
    }
}
```

### 3.3 性别分化

有 6 个槽位是性别感知的（`get_clothing_item`）：`pants`, `shirt`, `underwear_top`, `underwear_bottom`, `underwear_feet`, `shoes`。

查找链（以男性 pants 为例）：
1. `<class>_pants_male` （如 `NC_SCAVENGER_pants_male`）
2. `<class>_pants` （如 `NC_SCAVENGER_pants`）
3. `npc_pants_male` （通用回退）

### 3.4 默认 `npc_*` 物品组

定义在 `data/json/npcs/items_generic.json`（1149行），涵盖所有 17 槽位的回退：

| 物品组 | 示例内容 |
|--------|---------|
| `npc_pants_male` | jeans, pants, pants_leather, shorts, pants_cargo... |
| `npc_shirt_male` | tshirt, polo_shirt, dress_shirt, longshirt, sweater... |
| `npc_shoes_male` | boots, boots_combat, boots_hiking, sneakers, dress_shoes... |
| `npc_gloves` | null(60%), gloves_leather, gloves_fingerless... |
| `npc_coat` | null(20%), hoodie, jacket_light, jacket_leather, trenchcoat... |
| `npc_masks` | null(80%), mask_dust, bandana, mask_filter... |
| `npc_hat` | null(20%), hat_ball, hat_cotton, hat_knit, helmet_bike... |
| ... | (所有 17 个槽位都有对应回退组) |

---

## 4. 武器选择系统

代码入口：[npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L1059-1119 `starting_weapon()`

```cpp
void npc::starting_weapon( const npc_class_id &type )
{
    // 优先：weapon_override
    if( type->weapon_override ) {
        set_wielded_item( item_group::item_from( type->weapon_override ) );
        return;
    }

    // 否则：按最佳战斗技能选择武器
    const skill_id best = best_combat_skill( combat_skills::WEAPONS_ONLY ).first;
    
    if( best == skill_stabbing ) → random_item_from(type, "stabbing", Item_spawn_data_survivor_stabbing)
    if( best == skill_bashing )  → random_item_from(type, "bashing", Item_spawn_data_survivor_bashing)
    if( best == skill_cutting )  → random_item_from(type, "cutting", Item_spawn_data_survivor_cutting)
    if( best == skill_throw )    → random_item_from(type, "throw")
    if( best == skill_archery )  → random_item_from(type, "archery")
    if( best == skill_pistol )   → random_item_from(type, "pistol", Item_spawn_data_guns_pistol_common)
    if( best == skill_shotgun )  → random_item_from(type, "shotgun", Item_spawn_data_guns_shotgun_common)
    if( best == skill_smg )      → random_item_from(type, "smg", Item_spawn_data_guns_smg_common)
    if( best == skill_rifle )    → random_item_from(type, "rifle", Item_spawn_data_guns_rifle_common)
}
```

武器查找链（以 pistol 为例）：
1. `<class>_pistol` （如 `NC_SCAVENGER_pistols`）
2. `npc_pistol` （通用回退）
3. `Item_spawn_data_guns_pistol_common` （硬编码回退常量）

---

## 5. 物品栏系统

代码入口：[npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L859-918 `starting_inv()`

```cpp
void starting_inv( npc &who, const npc_class_id &type )
{
    if( carry_override ) {
        *who.inv += item_group::items_from( type->carry_override );
        return;
    }
    // 弹药补充逻辑（如果武器是枪）
    // 特殊类处理（如 NC_ARSONIST → molotov）
    // 随机 misc 物品（qty = 2~6 或 5~15）:
    //   → random_item_from(type, "misc") → 回退到 "npc_misc"
}
```

---

## 6. 强盗 ("bandit") 装备分析

### 6.1 NPC 模板定义

`data/json/npcs/hells_raiders/npc.json`：

```json
{
    "type": "npc",
    "id": "bandit",
    "class": "NC_SCAVENGER",     // ← 使用 Scavenger 职业！
    "attitude": 0,
    "mission": 8,
    "faction": "hells_raiders"
}
```

**关键发现**：原版 "bandit" NPC 没有自己的专属 `npc_class`，而是复用了通用的 `NC_SCAVENGER`！

### 6.2 NC_SCAVENGER class 定义

`data/json/npcs/classes.json` L305-318：

```json
{
    "type": "npc_class",
    "id": "NC_SCAVENGER",
    "name": "Scavenger",
    "skills": [
        { "skill": "gun", "bonus": { "rng": [2,4] } },
        { "skill": "pistol", "bonus": { "rng": [2,5] } },
        { "skill": "rifle", "bonus": { "rng": [0,3] } },
        { "skill": "archery", "bonus": { "rng": [0,3] } }
    ]
    // ★ 没有 worn_override / carry_override / weapon_override！
}
```

### 6.3 NC_SCAVENGER 的专属 item_group

`data/json/npcs/NC_SCAVENGER.json` 只定义了 5 个物品组：

| item_group | 类型 | 用途 |
|-----------|------|------|
| `NC_SCAVENGER_gloves` | 着装槽位 | leather/working/fingerless gloves（30% null） |
| `NC_SCAVENGER_archery` | 武器 | shortbow, crossbow |
| `NC_SCAVENGER_pistols` | 武器 | usp_45, sw_619, m9, ruger_redhawk, makarov |
| `NC_SCAVENGER_rifle` | 武器 | browning_blr, remington_700, m1a, m1903 |
| `NC_SCAVENGER_misc` | 物品栏 | 饮料/零食/罐头 |

**其他所有槽位（14/17）均回退到通用的 `npc_*` 物品组！**

### 6.4 bandit 完整装备链

以男性 bandit 为例：

```
装备流程:
  worn_override? → NO (NC_SCAVENGER 未定义)
    ↓
  17槽位各自查找:
    pants → "NC_SCAVENGER_pants_male"? → NO
          → "NC_SCAVENGER_pants"? → NO
          → "npc_pants_male" → ✅ (jeans/pants/pants_leather...)
    
    shirt → "npc_shirt_male" → ✅ (tshirt/polo_shirt/sweater...)
    shoes → "npc_shoes_male" → ✅ (boots/sneakers...)
    gloves → "NC_SCAVENGER_gloves" → ✅ (已定义！)
    coat → "npc_coat" → ✅
    ... (其他均回退到 npc_*)

武器流程:
  weapon_override? → NO
    ↓
  best_combat_skill? → pistol (bonus 2-5，最高)
    ↓
  "NC_SCAVENGER_pistol"? → ❌ (不存在)
    ↓
  "npc_pistol"? → (通用)
    ↓
  Item_spawn_data_guns_pistol_common → ✅

物品栏:
  carry_override? → NO
    ↓
  random_item_from(type, "misc") → "NC_SCAVENGER_misc" → ✅
```

### 6.5 结论

**原版强盗的装备完全是随机的现代幸存者风格**：
- 裤子：现代牛仔裤/工装裤（来自 `npc_pants_male`）
- 上衣：T恤/衬衫/毛衣（来自 `npc_shirt_male`）
- 鞋子：现代靴子/运动鞋（来自 `npc_shoes_male`）
- 武器：现代手枪（来自 `NC_SCAVENGER_pistols`）
- 特殊槽位（手套）：NC_SCAVENGER 专属皮革/工作手套

**没有任何 bandit 专属的 item_group。** 强盗复用了幸存者（Scavenger）的装备组，只因为 faction 和姓名不同而被称为"bandit"。

---

## 7. 各 NPC 子类的装备指定模式

| 模式 | 代表 NPC | 说明 |
|------|---------|------|
| **override 全家桶** | GODCO 守卫、Exodii 商人 | `worn_override` + `carry_override` + `weapon_override` 全部定义，完全自定义装备 |
| **override 单独** | NC_APIS | 用 `EMPTY_GROUP` 清空所有装备 |
| **部分槽位覆盖** | NC_THUG | 只定义 `NC_THUG_bashing`（武器），着装使用默认 npc_* |
| **完全默认** | **NC_SCAVENGER (bandit)** | 只定义 5 个槽位的 item_group，其余全部回退 |

---

## 8. 中世纪强盗装备方案

> 中世纪 NPC/强盗装备改造的策划案已移至 → [../design/medieval_npc_equipment_design.md](../design/medieval_npc_equipment_design.md)

---

## 9. 关键文件索引

| 文件 | 内容 |
|------|------|
| [npc_class.h](file:///E:/Cataclysm-Medieval/src/npc_class.h) L108-110 | worn_override/carry_override/weapon_override 字段定义 |
| [npc_class.cpp](file:///E:/Cataclysm-Medieval/src/npc_class.cpp) L150-159, L303-305 | override 校验和 JSON 加载 |
| [npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L779-857 | random_item_from(), get_clothing_item(), starting_clothes() |
| [npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L859-918 | starting_inv() |
| [npc.cpp](file:///E:/Cataclysm-Medieval/src/npc.cpp) L1059-1119 | starting_weapon() |
| [items_generic.json](file:///E:/Cataclysm-Medieval/data/json/npcs/items_generic.json) | 17 槽位的通用 npc_* 回退物品组 |
| [classes.json](file:///E:/Cataclysm-Medieval/data/json/npcs/classes.json) L305-318 | NC_SCAVENGER 定义 |
| [NC_SCAVENGER.json](file:///E:/Cataclysm-Medieval/data/json/npcs/NC_SCAVENGER.json) | NC_SCAVENGER 专属 item_group（5个） |
| [hells_raiders/npc.json](file:///E:/Cataclysm-Medieval/data/json/npcs/hells_raiders/npc.json) | bandit NPC 模板（class=NC_SCAVENGER） |
| [hells_raiders/classes.json](file:///E:/Cataclysm-Medieval/data/json/npcs/hells_raiders/classes.json) | NC_BANDIT_TRADER/NC_BANDIT_QUARTERMASTER/NC_BANDIT_LEADER |
