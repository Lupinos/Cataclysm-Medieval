# 护甲穿透系统 (Armor Penetration System)

> CDDA 原版护甲穿透机制的完整流程：从伤害生成到护甲减免
> Medieval 改造点：在 `roll_melee_damage_internal` 引入 STR × 武器重量破甲

---

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/damage.h` / `src/damage.cpp` | `damage_unit` 结构体、`resistances` 抗性计算、`load_damage_map` |
| `src/melee.cpp` | 近战伤害生成：`roll_melee_damage_internal`（arpen 初始化位置）|
| `src/creature.cpp` | `deal_damage` 主入口、调用 `absorb_hit` |
| `src/monster.cpp` | `monster::absorb_hit` — 怪物护甲吸收 |
| `src/character_armor.cpp` | `Character::absorb_hit` — 角色护甲吸收 |
| `src/character_attire.cpp` | `outfit::absorb_damage` — 穿戴装备遍历吸收 |
| `src/item.cpp` | `item::mitigate_damage` — 单件护甲减免，消耗 `res_pen` |
| `src/weakpoint.cpp` | 弱点系统修正 `resistances` |

---

## 一、damage_unit：穿透数据的载体

### 结构体定义 (`damage.h:109-127`)

```cpp
struct damage_unit {
    damage_type_id type;
    float amount;                     // 原始伤害量
    float res_pen;                    // 固定护甲穿透（flat AP）
    float res_mult;                   // 百分比护甲穿透倍率（<1 = 穿透）
    float damage_multiplier;          // 伤害倍率
    float unconditional_res_mult;     // 无条件抗性倍率
    float unconditional_damage_mult;  // 无条件伤害倍率
};
```

构造函数 (`damage.h:121-124`)：
```cpp
damage_unit(dt, amt, arpen=0.0f, arpen_mult=1.0f, dmg_mult=1.0f,
            unc_arpen_mult=1.0f, unc_dmg_mult=1.0f);
//              res_pen  res_mult
```

---

## 二、全程链路

### 步骤 1：伤害生成 — `roll_melee_damage_internal` (`melee.cpp:1225-1432`)

```cpp
int arpen = 0;           // ← 武器本身不提供固定穿甲
float armor_mult = 1.0f; // ← 默认不减抗

// 来源 1：徒手身体部位
arpen += bp->unarmed_arpen(dt);

// 来源 2：武侠 buff
arpen += u.mabuff_arpen_bonus(dt);

// 来源 3（Medieval 新增）：武器重量 × 力量
// 见第五节

// 暴击时修改 armor_mult（百分比穿甲）
if (crit) {
    if (dt == stab)   armor_mult = 1.0 - 0.34 * crit_mod;         // 34% 穿甲
    if (dt == cut)   { armor_mult = 1.0 - 0.25 * crit_mod; arpen += 5; }  // 25%+5
    if (dt == bash)   armor_mult = 0.5 * crit_mod;                // 50% 穿甲
}

di.add_damage(dt, dmg, arpen, armor_mult, dmg_mul);
```

### 步骤 2：有效抗性计算 (`damage.cpp:620-623`)

```cpp
float resistances::get_effective_resist(const damage_unit &du) const {
    return std::max(type_resist(du.type) - du.res_pen,  // 先扣固定穿透
                    0.0f) * du.res_mult                 // 再乘百分比
           * du.unconditional_res_mult;                  // 无条件倍率
}
```

**公式**：`有效抗性 = max(护甲值 - res_pen, 0) × res_mult × unconditional_res_mult`

### 步骤 3：伤害承受 — `Creature::deal_damage` (`creature.cpp:1187-1230`)

```cpp
damage_instance d = dam;                         // 拷贝
const weakpoint *wp = absorb_hit(attack, bp, d); // 护甲吸收 → 修改 d
for (auto &it : d.damage_units) {
    deal_damage_handle_type(..., it, bp, cur_damage, total_pain);
}
apply_damage(source, bp, total_damage);
```

### 步骤 4a：Character 护甲吸收 (`character_armor.cpp:160-230`)

```cpp
Character::absorb_hit(...) {
    for (damage_unit &elem : dam.damage_units) {
        armor_enchantment_adjust(*this, elem);     // 附魔修正
        worn.absorb_damage(*this, elem, bp, ...);  // 遍历穿戴装备
        passive_absorb_hit(bp, elem);              // 变异/生化护甲
        post_absorbed_damage_enchantment_adjust(*this, elem);
    }
}
```

单件护甲吸收 — `item::mitigate_damage` (`item.cpp:9157-9167`)：
```cpp
void item::mitigate_damage(damage_unit &du, ...) const {
    resistances res = resistances(*this, false, roll, bp);
    float mitigation = res.get_effective_resist(du);  // 套用公式
    du.res_pen -= res.type_resist(du.type);           // 消耗固定穿甲
    du.res_pen = std::max(0.0f, du.res_pen);
    du.amount -= mitigation;
}
```

关键：**穿透值会逐层消耗**。如果第一层锁子甲消耗了 6 点 `res_pen`，内层板甲面对的 `res_pen` 就减少了 6 点。

### 步骤 4b：Monster 护甲吸收 (`monster.cpp:1828-1848`)

```cpp
monster::absorb_hit(...) {
    resistances r = resistances(*this);      // 怪物天生护甲
    const weakpoint *wp = type->weakpoints.select_weakpoint(attack);
    wp->apply_to(r);                          // 弱点修正抗性
    for (damage_unit &elem : dam) {
        elem.amount -= std::min(r.get_effective_resist(elem)
                                + get_worn_armor_val(elem.type), elem.amount);
    }
    wp->apply_to(dam, attack.is_crit);
}
```

Monster 不穿装备，没有逐层消耗穿透的概念。一次性计算 `get_effective_resist` + 穿戴护甲值。

---

## 三、穿甲参数来源总览

| 参数 | 近战武器 | 徒手 | 暴击 | 武术 buff |
|------|---------|------|------|----------|
| `res_pen`（固定穿甲） | ✗ 原版无 / ✓ Medieval 重量破甲 | ✓ `bp->unarmed_arpen` | ✓ cut 暴击 +5 | ✓ `mabuff_arpen_bonus` |
| `res_mult`（百分比穿甲） | ✗ | ✗ | ✓ stab:0.66 / cut:0.75 / bash:0.5 | ✗ |

---

## 四、武器伤害 `damage_melee` 不包含穿甲

`item::damage_melee()` (`item.cpp:7532-7567`) 只返回 JSON `melee_damage` 手写值 × 耐久惩罚（每级 -10%），**不涉及任何护甲穿透参数**。

```cpp
int item::damage_melee(damage_type_id dt) const {
    int res = type->melee[dt];                  // JSON 手写值
    res = damage_adjusted_melee_weapon_damage(res); // 耐久惩罚
    return std::max(res, 0);
}
```

---

## 五、Medieval 改造：STR × 武器重量破甲

### 插入位置

`roll_melee_damage_internal` (`melee.cpp:1350-1362`)，在徒手 arpen 计算之后、暴击 arpen 修正之前。

### 实现逻辑

```cpp
if( !unarmed && !weap.is_null() ) {
    const float weapon_mass_kg = weap.weight() / 1_kilogram;
    const float str_factor = u.get_arm_str() / 10.0f;   // STR 10 = 1.0x
    if( dt == damage_bash ) {
        arpen += static_cast<int>( weapon_mass_kg * str_factor );
    } else if( dt == damage_stab || dt == damage_cut ) {
        arpen += static_cast<int>( weapon_mass_kg * str_factor * 0.5f );
    }
}
```

### 设计理由

- **物理直觉**：重量 × 力量 = 冲击力，更重的武器配上更强的手臂能更有效地击穿/砸碎护甲
- **钝器优先**：bash 伤害获得全额加成（锤/斧背/棍的动量直接转化为破甲力）
- **利器折半**：stab/cut 破甲更依赖刃口几何和材料硬度，重量帮助有限（一把轻 rapier 照样能刺穿锁子甲）
- **徒手不参与**：徒手已有独立的 `unarmed_arpen` 体系

### 参数预期

| STR | 武器重量 | bash arpen | stab/cut arpen |
|-----|---------|-----------|----------------|
| 8 | 1kg 单手斧 | +0 | +0 |
| 10 | 2kg 长剑 | +2 | +1 |
| 14 | 3kg 巨剑 | +4 | +2 |
| 16 | 4kg 战锤 | +6 | +3 |

---

## 六、与暴击穿甲的对比

| 穿甲来源 | 类型 | 触发条件 | 典型值 |
|---------|------|---------|-------|
| 重量破甲（新增） | `res_pen` 固定 | 每次攻击 | 0-6 点（视 STR + 重量）|
| stab 暴击 | `res_mult` 百分比 | 暴击 | 34% |
| cut 暴击 | `res_mult` + `res_pen` | 暴击 | 25% + 5 点 |
| bash 暴击 | `res_mult` 百分比 | 暴击 | 50% |
| 武术 buff | `res_pen` 固定 | 激活武术 | 配置值 |

重量破甲提供**每次攻击的持续优势**，暴击提供**偶尔的大幅穿透**，两者正交叠加。

---

## 七、可能的进一步扩展方向

| 方向 | 说明 |
|------|------|
| JSON 可配置乘数 | 让 `melee_damage` 支持 `arpen` 字段，允许匕首等高穿刺武器获得 JSON 级固定穿甲 |
| 材料影响破甲 | 高碳钢武器 vs 低碳钢武器，`res_mult` 差异 |
| 武器速度权衡 | 破甲高的武器攻速更慢，作为平衡 |
| Monster 端扩展 | Monster 使用 NPC 体系后，武器重量同样影响其破甲 |
