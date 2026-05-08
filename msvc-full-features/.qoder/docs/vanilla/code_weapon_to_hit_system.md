# CDDA 武器命中（to_hit）与双手握持系统

> 调研 `data/json/items/melee/` 中每件武器都携带的 `"grip"/"surface"/"length"/"balance"` 词条，
> 以及 `ALWAYS_TWOHAND` flag 的实际 C++ 作用。

---

## 1. JSON 分布概况

| 文件 | 含 to_hit 的武器数 |
|------|-------------------|
| `swords_and_blades.json` | 93 |
| `bludgeons.json` | 84 |
| `spears_and_polearms.json` | 41 |
| `knives_kitchen.json` | 8 |
| `unarmed_weapons.json` | 8 |
| `misc.json` | 3 |
| `fake.json` | 2 |
| **总计** | **239** |

每个条目中 `grip`/`surface`/`length`/`balance` 始终作为 `to_hit` 对象的四个子字段出现：

```json
"to_hit": { "grip": "solid", "length": "long", "surface": "any", "balance": "neutral" }
```

---

## 2. to_hit 的双重格式

### 旧格式（整数）

```json
"to_hit": 2
```

直接读取为 `m_to_hit` 整数。

### 新格式（对象）

```json
"to_hit": { "grip": "solid", "surface": "any", "length": "long", "balance": "neutral" }
```

通过 `io::acc_data` 结构体加载，调用 `sum_values()` 合并为单一 `m_to_hit` 整数。

**加载逻辑**（[item_factory.cpp](E:\Cataclysm-Medieval\src\item_factory.cpp:4115)）：

```cpp
if( jo.has_int( "to_hit" ) ) {
    assign( jo, "to_hit", def.m_to_hit, strict );          // 旧格式：直接 int
} else if( jo.has_object( "to_hit" ) ) {
    io::acc_data temp;
    bool was_loaded = false;
    mandatory( jo, was_loaded, "to_hit", temp );            // 新格式：acc_data
    def.m_to_hit = temp.sum_values();                       // 合并为 int
}
```

---

## 3. 四个子属性的枚举定义

所有枚举定义在 [item_factory.cpp](E:\Cataclysm-Medieval\src\item_factory.cpp:3805)。

### grip_val（握持质量，4 档）

| JSON 值 | 枚举 | int | 说明 |
|----------|------|-----|------|
| `"bad"` | `BAD` | 0 | 握持困难（如拿刀片） |
| `"none"` | `NONE` | 1 | 无握柄（如石头） |
| `"solid"` | `SOLID` | 2 | 稳固握柄（有护手/包柄） |
| `"weapon"` | `WEAPON` | 3 | 专门武器握柄（默认值） |

### length_val（武器长度，3 档）

| JSON 值 | 枚举 | int | 说明 |
|----------|------|-----|------|
| `"hand"` | `HAND` | 0 | 手掌长度（默认值，匕首级） |
| `"short"` | `SHORT` | 1 | 短武器（手斧/短剑） |
| `"long"` | `LONG` | 2 | 长武器（长剑/矛） |

### surface_val（打击面类型，4 档）

| JSON 值 | 枚举 | int | 说明 |
|----------|------|-----|------|
| `"point"` | `POINT` | 0 | 点状接触（矛尖） |
| `"line"` | `LINE` | 1 | 线状接触（斧刃、刀刃） |
| `"any"` | `ANY` | 2 | 任意面（剑，默认值） |
| `"every"` | `EVERY` | 3 | 全方位（巨型武器、全身打击） |

### balance_val（平衡性，4 档）

| JSON 值 | 枚举 | int | 说明 |
|----------|------|-----|------|
| `"clumsy"` | `CLUMSY` | 0 | 笨拙（巨锤、大木桩） |
| `"uneven"` | `UNEVEN` | 1 | 不均衡（手斧、镰刀） |
| `"neutral"` | `NEUTRAL` | 2 | 均衡（剑，默认值） |
| `"good"` | `GOOD` | 3 | 极佳（细剑、小刀） |

---

## 4. sum_values() 计算规则

```cpp
struct acc_data {
    grip_val grip = grip_val::WEAPON;        // 默认 3
    length_val length = length_val::HAND;    // 默认 0
    surface_val surface = surface_val::ANY;  // 默认 2
    balance_val balance = balance_val::NEUTRAL; // 默认 2

    static constexpr int base_acc = -2;
    static constexpr int grip_offset = -1;
    static constexpr int surface_offset = -2;
    static constexpr int balance_offset = -2;
    static constexpr int acc_offset = base_acc + grip_offset + surface_offset + balance_offset;
    // acc_offset = -2 + (-1) + (-2) + (-2) = -7

    int sum_values() const {
        return acc_offset + (int)grip + (int)length + (int)surface + (int)balance;
    }
};
```

### 举例

| 武器 | grip | length | surface | balance | sum = m_to_hit |
|------|------|--------|---------|---------|----------------|
| 2-by-sword (木剑) | solid(2) | long(2) | any(2) | neutral(2) | -7+2+2+2+2 = **1** |
| 理论最大值 | weapon(3) | long(2) | every(3) | good(3) | -7+3+2+3+3 = **4** |
| 理论最小值 | bad(0) | hand(0) | point(0) | clumsy(0) | -7+0+0+0+0 = **-7** |
| 全默认值 | weapon(3) | hand(0) | any(2) | neutral(2) | -7+3+0+2+2 = **0** |

**结论**：`m_to_hit` 的理论范围是 **-7 ~ +4**。

---

## 5. m_to_hit 在战斗中的实际作用

`m_to_hit` 最终存储在 `itype::m_to_hit`（只有一个 int），被两处战斗代码引用：

### 5.1 命中判定（[melee.cpp:349](E:\Cataclysm-Medieval\src\melee.cpp:349)）

```cpp
float Character::get_hit_weapon( const item &weap ) const
{
    float skill = get_skill_level( weap.melee_skill() );
    return (skill / 3.0f) + (get_skill_level(skill_melee) / 2.0f) + weap.type->m_to_hit;
}
```

`m_to_hit` 作为**直接加值**进入命中率计算，与技能平权叠加。+1 的 `m_to_hit` 约等于 3 级武器专精技能或 2 级近战技能。

### 5.2 暴击判定（[melee.cpp:1083](E:\Cataclysm-Medieval\src\melee.cpp:1083)）

```cpp
if( weap.type->m_to_hit > 0 ) {
    // 正向 m_to_hit → 暴击底限至少 0.5 + 0.1*m_to_hit
    weapon_crit_chance = std::max( weapon_crit_chance, 0.5 + 0.1 * weap.type->m_to_hit );
} else if( weap.type->m_to_hit < 0 ) {
    // 负向 m_to_hit → 从暴击率中扣除
    weapon_crit_chance += 0.1 * weap.type->m_to_hit;
}
```

每点 `m_to_hit` 提供 **10% 暴击率**修正（与 unarmed 技能的 5% 相比更高效）。

---

## 6. ALWAYS_TWOHAND 与双手握持系统

### 6.1 判定函数（[item.cpp:9181](E:\Cataclysm-Medieval\src\item.cpp:9181)）

```cpp
bool item::is_two_handed( const Character &guy ) const
{
    if( has_flag( flag_ALWAYS_TWOHAND ) ) {
        return true;    // 无条件双手
    }
    // 重量判定：重量(g)/113g > 臂力*4 → 也需要双手
    return ( ( weight() / 113_gram ) > guy.get_arm_str() * 4 );
}
```

**双手判定有两条路径**：
1. `ALWAYS_TWOHAND` flag → 无论力量多大都必须双手（如长矛、巨剑）
2. 重量阈值 → 武器太重（> 臂力 × 452g）自动视为双手

**力量阈值速查**：`get_arm_str()` 通常 = STR
| STR | 单手重量上限 |
|-----|------------|
| 8 | ~3.6kg |
| 10 | ~4.5kg |
| 12 | ~5.4kg |
| 14 | ~6.3kg |

### 6.2 握持限制（[character.cpp:7849](E:\Cataclysm-Medieval\src\character.cpp:7849)）

```cpp
if( it.is_two_handed( *this ) && ( !has_two_arms_lifting() ||
     worn_with_flag( flag_RESTRICT_HANDS ) ) ) {
    if( worn_with_flag( flag_RESTRICT_HANDS ) ) {
        return failure( "Something you are wearing hinders the use of both hands." );
    } else if( it.has_flag( flag_ALWAYS_TWOHAND ) ) {
        return failure( "You can't wield the %s with only one arm." );
    } else {
        return failure( "You are too weak to wield the %s with only one arm." );
    }
}
```

三种不同错误消息：
- 穿戴了限手装备（`RESTRICT_HANDS`）
- `ALWAYS_TWOHAND` 且只有单臂
- 武器太重/力量不足

### 6.3 战斗中的额外伤害扩散（[melee.cpp:2329](E:\Cataclysm-Medieval\src\melee.cpp:2329)）

双手武器在**自伤事件**（`HURT_WHEN_WIELDED`、玻璃碎裂等）中会将伤害同时施加到**左手/左臂**：

```cpp
if( weap.is_two_handed( *this ) ) { // Hurt left hand too, if it was big
    deal_damage( nullptr, bodypart_id( "hand_l" ), di );
}
```

### 6.4 触手攻击限制（[melee.cpp:2398](E:\Cataclysm-Medieval\src\melee.cpp:2398)）

手持双手武器时，触手突变（ARM_TENTACLES 系列）额外攻击次数会被削减。

### 6.5 ALWAYS_TWOHAND 在 data/json 中的分布

| 武器类别 | 含 ALWAYS_TWOHAND 的条目数 |
|----------|---------------------------|
| bludgeons.json | 17 |
| spears_and_polearms.json | 10 |
| swords_and_blades.json | 10 |

---

## 7. 相关 flag 体系

| Flag | 作用 |
|------|------|
| `ALWAYS_TWOHAND` | 无条件强制双手（无视力量） |
| `FIRE_TWOHAND` | 射击时强制双手（`ranged.cpp:3989`） |
| `RESTRICT_HANDS` | 穿戴此装备时限制双手使用 |
| `NO_UNWIELD` | 不能手动解除握持（生化武器专用） |
| `BIONIC_WEAPON` | 生化模块武器，不能手动握持 |
| `BELT_CLIP` | 可挂在腰带上 |
| `STR_DRAW` | 力量影响弓的射程（`item.cpp:10671`） |

---

## 8. CDDA 手持物的实际规则

用户提问：「CDDA 手持物应该只允许一个，双手握持有什么意义？」

**CDDA 的手持规则**：

1. **始终只有一个 wielded 槽位**——玩家在任何时刻只能「握持」一件物品。
2. 双手武器的意义不是「占用两个手槽」，而是：
   - **握持门槛**：力量不足或只有单臂时，禁止握持双手武器
   - **穿戴冲突**：穿某些装备（`RESTRICT_HANDS`）时不能使用双手武器
   - **受伤扩散**：一些自伤机制会伤到双手/双臂
   - **触手减益**：触手突变在持双手武器时攻击次数减少
3. 这模拟的是「需要两只手来操作的武器」，而不是双持（CDDA 没有双持）。

---

## 9. 总结

| 概念 | 本质 |
|------|------|
| `grip/surface/length/balance` | **仅在加载时存在**的中间属性，通过 `sum_values()` 合并为单一 `m_to_hit` int 后丢弃原始枚举值 |
| `m_to_hit` | 存储在 `itype` 中，直接影响命中率（直接加值）和暴击率（每点 ±10%） |
| `ALWAYS_TWOHAND` | 强制双手判定，不因力量增长而变单手；主要在握持门槛、自伤扩散、突变减益中生效 |
| 双手 vs 双持 | CDDA **没有双持**，双手武器仅表示「需要两只手一起用」，不影响槽位数量 |
