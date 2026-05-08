# 战斗系统 (Combat System)

> Cataclysm-Medieval 的伤害、护甲穿透、近战与远程战斗机制

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/damage.h` / `src/damage.cpp` | 伤害类型、伤害实例、抗性系统 |
| `src/melee.cpp` / `src/melee.h` | 近战攻击：命中、伤害、格挡、特技 |
| `src/ranged.cpp` / `src/ranged.h` | 远程攻击：瞄准、后坐力、弹道 |
| `src/ballistics.cpp` / `src/ballistics.h` | 弹道计算 |
| `src/creature.cpp` / `src/creature.h` | 伤害承受、致命判定 |
| `src/character.cpp` / `src/character.h` | 玩家伤害修正、附魔加成 |
| `src/monster.cpp` / `src/monster.h` | 怪物护甲与伤害 |
| `src/weakpoint.cpp` / `src/weakpoint.h` | 弱点系统 |
| `src/bodypart.cpp` / `src/bodypart.h` | 身体部位与受伤 |

---

## 伤害类型体系

### damage_type 结构 (`damage.h:27-59`)

每个伤害类型是一个 JSON 定义的数据：

| 属性 | 说明 |
|------|------|
| `id` | 伤害类型 ID（如 `bash`, `cut`, `stab`, `bullet`, `heat` 等） |
| `skill` | 关联技能（用于训练） |
| `physical` | 是否为物理伤害 |
| `no_resist` | 是否忽略抗性（如 `pure` 类型） |
| `edged` | 是否为利器伤害（影响处决等） |
| `melee_only` | 仅近战可用 |
| `onhit_eocs` | 命中时触发的效果链 |
| `immune_flags` | 玩家免疫标记 |
| `mon_immune_flags` | 怪物免疫标记 |

游戏中常见的伤害类型：
- **bash**（钝击）— 棍棒、拳头、坠落
- **cut**（切割）— 刀剑、利爪
- **stab**（穿刺）— 长矛、刺剑
- **bullet**（子弹）— 枪械
- **heat**（热）、**cold**（冷）、**electric**（电）
- **acid**（酸）、**biological**（生物）
- **pure**（纯粹）— 完全无视抗性

---

## 伤害实例结构

### damage_unit — 单个伤害原子 (`damage.h:109-127`)

```cpp
struct damage_unit {
    damage_type_id type;        // 伤害类型
    float amount;               // 伤害量
    float res_pen;              // 护甲穿透值（固定减抗）
    float res_mult;             // 护甲穿透倍率（百分比穿抗）
    float damage_multiplier;    // 伤害倍率
    float unconditional_res_mult;   // 无条件抗性倍率
    float unconditional_damage_mult; // 无条件伤害倍率
};
```

**护甲穿透公式（推测）：**
```
有效抗性 = max(0, 护甲抗性 - res_pen) × res_mult
最终伤害 = amount × damage_multiplier × (1 - 有效抗性减免)
```

- `res_pen` 是**固定穿透**，直接从目标抗性值中扣除
- `res_mult` 是**百分比穿透**，将剩余抗性乘以倍率（<1 则进一步穿透）
- `unconditional_res_mult` 和 `unconditional_damage_mult` 不受其他因素影响

### damage_instance — 复合伤害 (`damage.h:131-174`)

一次攻击可以包含多个 damage_unit，例如一把带刺的长矛可能同时造成 stab + bash 伤害。核心方法：
- `total_damage()` — 总伤害
- `mult_damage(multiplier, pre_armor)` — 伤害倍率调整
- `add_damage()` — 添加伤害（同类型会归一化）

### resistances — 抗性 (`damage.h:203-228`)

```cpp
struct resistances {
    std::unordered_map<damage_type_id, float> resist_vals;
    float get_effective_resist(const damage_unit &du) const;
};
```

抗性可以从**穿戴的护甲**、**怪物天生护甲**、**变异护甲**来。`get_effective_resist()` 将 damage_unit 的穿透值纳入计算。

---

## 近战攻击流程

### 1. 命中判定 — hit_roll()

`Character::hit_roll()` (`melee.cpp:365-386`)：

```
命中值 = (武器技能/3 + 近战技能/2 + 武器命中加成) × 攻击投骰修正
         ± h典远视/俯卧/蹲伏惩罚
```

影响因素：
- **武器技能**（对应伤害类型的技能，如 bashing/cutting/stabbing）
- **近战技能** (melee)
- **武器 m_to_hit** （武器自带命中）
- **CQB 生化模块**（近战技能保底 5 级）
- **附魔修正** (melee_attack_roll_mod)
- **姿态惩罚**：倒地 -8，蹲伏 -2
- **远视**（未矫正）-2

### 2. 暴击判定 — scored_crit()

与目标的闪避值对比，超过阈值则暴击。暴击时伤害乘暴击倍率。

### 3. 伤害生成 — roll_all_damage()

`Character::roll_all_damage()` (`melee.cpp:429-440`)：
对所有伤害类型（遍历每个 `damage_type`），分别投骰生成伤害值。

### 4. 附魔修正 — modify_damage_dealt_with_enchantments()

`Character::modify_damage_dealt_with_enchantments()` (`melee.cpp:489-546`)：
对每种伤害类型分别应用 `ITEM_DAMAGE_XXX` 附魔和 `MELEE_DAMAGE` 附魔。

### 5. 伤害倍率修正

- **长柄武器打贴身**：×0.7
- **倒地攻击**：×0.3
- **蹲伏攻击**：×0.8
- **手臂残废徒手**：×0.1

### 6. 目标防御 — deal_melee_hit()

分为三级防御：
1. **闪避 (Dodge)** — 速度/敏捷决定
2. **格挡 (Block)** — 盾牌或武器格挡，吸收伤害
3. **护甲 (Armor)** — 各部位护甲减免对应伤害类型

---

## 格挡系统

`Character::block_hit()` (`melee.cpp:2034+`)：

- 每回合有 `blocks_left` 格挡次数
- 需要反应检测：`近战技能 × 20 × 肢体反应分数 / 100 ≥ 随机值`
- 格挡等级（`melee::blocking_ability()`）：
  - WBLOCK_3 → +10
  - WBLOCK_2 → +6
  - WBLOCK_1 → +4
  - BLOCK_WHILE_WORN → +2
- 格挡可吸收物理伤害（`mabuff_block_bonus()`）

---

## 远程攻击

`target_handler` 命名空间 (`ranged.h:26-53`) 定义了多种瞄准模式：

| 模式 | 说明 |
|------|------|
| `mode_fire` | 标准射击（可花行动点瞄准） |
| `mode_throw` | 投掷物品 |
| `mode_reach` | 长距离近战攻击 |
| `mode_turret_manual` | 手动操作车载炮塔 |
| `mode_turrets` | 车辆控制系统操作炮塔 |
| `mode_spell` | 法术施放 |
| `mode_select_only` | 仅选择目标（不发射） |

### 后坐力与瞄准

- `recoil` 值越高越不准（单位：MoA，分角）
- 每次射击后后坐力达到 `MAX_RECOIL`
- 花行动点瞄准可降低后坐力
- `MIN_RECOIL_IMPROVEMENT = 0.01` MoA — 低于此值不再改进

---

## 弱点系统 (Weakpoint)

相关文件：`src/weakpoint.cpp` / `src/weakpoint.h`

怪物可以有弱点部位，命中弱点时：
- 伤害倍率增加
- 可能触发额外效果

---

## 武器耐久度

`Character::handle_melee_wear()` (`melee.cpp:201-333`)：

- 每次攻击都有概率损伤武器
- 概率取决于：敏捷、近战技能、武器材料 (`chip_resistance()`)
- **FRAGILE_MELEE** 标记：劣质武器，按组件逐一判定损坏
- **DURABLE_MELEE** 标记：耐打（损坏概率 ×4 生存率）
- **UNBREAKABLE_MELEE** 标记：永不损坏

---

## 体力消耗

`Character::get_base_melee_stamina_cost()` / `get_total_melee_stamina_cost()` (`melee.cpp:940-952`)：

```
基础体力消耗 = min(-50, 武器标准体力消耗)
总消耗 = min(-50, 基础消耗 + 近战技能 - 姿态惩罚)
```
- 近战技能越高，体力消耗越少
- 倒地 +50 惩罚，蹲伏 +20 惩罚
