# 战斗系统 (Combat System)

> CDDA 原版近战命中、闪避、暴击、伤害与命中部位的完整机制
> 护甲穿透详见 [code_armor_penetration_system.md](code_armor_penetration_system.md)

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/damage.h` / `src/damage.cpp` | 伤害类型、伤害实例、抗性系统 |
| `src/melee.cpp` / `src/melee.h` | 近战攻击：命中、伤害、格挡、特技 |
| `src/ranged.cpp` / `src/ranged.h` | 远程攻击：瞄准、后坐力、弹道 |
| `src/creature.cpp` / `src/creature.h` | 伤害承受、致命判定、deal_melee_attack |
| `src/character.cpp` / `src/character.h` | 玩家伤害修正、附魔加成、dodge |
| `src/character_armor.cpp` | Character 护甲吸收 (absorb_hit) |
| `src/character_attire.cpp` | 穿戴装备遍历吸收 (outfit::absorb_damage) |
| `src/anatomy.cpp` / `src/anatomy.h` | 部位命中选择 (select_body_part) |
| `src/monster.cpp` / `src/monster.h` | 怪物护甲与伤害 |
| `src/weakpoint.cpp` / `src/weakpoint.h` | 弱点系统 |
| `src/bodypart.cpp` / `src/bodypart.h` | 身体部位与受伤 |
| `data/json/body_parts.json` | 部位定义：hit_size / hit_difficulty |

---

## 一、伤害类型体系

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

游戏中常见的伤害类型：**bash**（钝击）、**cut**（切割）、**stab**（穿刺）、**bullet**（子弹）、**heat/cold/electric**（元素）、**acid/biological**（生化）、**pure**（纯粹 — 完全无视抗性）。

---

## 二、近战攻击流程

### 2.1 命中值生成 — hit_roll()

`Character::hit_roll()` ([melee.cpp:365](file:///e:/Cataclysm-Medieval/src/melee.cpp#L365-L386))：

```
accuracy = get_hit_base()                    // DEX/PER 基础
         + get_hit_weapon(weap)              // 武器命中
         + mabuff_tohit_bonus()              // 武术 buff
         - 远视惩罚（-2）
         - 姿态惩罚（倒地 -8 / 蹲伏 -2）
         × melee_attack_roll_mod             // 附魔倍率

hit_roll = normal_roll( accuracy × 5, σ=25 ) // 正态随机！
```

**关键：不是固定值。** `melee::melee_hit_range()` ([melee.cpp:2966](file:///e:/Cataclysm-Medieval/src/melee.cpp#L2966-L2968)) 使用 `normal_roll(mean, stddev=25)` 对 accuracy 放大 5 倍后做正态分布随机投骰。标准差 25 意味着每次 hit_roll 约有 ±50 的波动范围。

**`get_hit_weapon()`** ([melee.cpp:335](file:///e:/Cataclysm-Medieval/src/melee.cpp#L335-L349))：

```
武器命中 = 武器技能 / 3 + 近战技能(melee) / 2 + m_to_hit
```

`m_to_hit` 是 JSON `to_hit: { grip, surface, length, balance }` 的 `sum_values()` 结果，范围 -7 ~ +4。

影响因素汇总：

| 来源 | 效果 |
|------|------|
| DEX/PER | `get_hit_base()` 基础值 |
| 武器技能 | 每 3 级 +1 |
| 近战技能 (melee) | 每 2 级 +1 |
| 武器 m_to_hit | 直接加值（-7 ~ +4） |
| CQB 生化模块 | 武器技能保底 5 级 |
| 附魔修正 | `melee_attack_roll_mod` 倍率 |
| 姿态惩罚 | 倒地 -8，蹲伏 -2 |
| 远视（未矫正） | -2 |
| **正态随机** | normal_roll(accuracy×5, σ=25)，波动约 ±50 |

---

### 2.2 闪避值 — dodge_roll()

`Character::dodge_roll()` ([melee.cpp:1199](file:///e:/Cataclysm-Medieval/src/melee.cpp#L1199-L1212))：

```cpp
float Character::dodge_roll() const {
    // 附魔闪避：概率性无敌帧
    if( rng(0, 99) < evasion * 100.0 ) return 999999.0f;
    // HARDTOHIT flag → 两个随机骰取优
    if( has_flag( json_flag_HARDTOHIT ) ) return max(get_dodge(), get_dodge()) * 5;
    return get_dodge() * 5;
}
```

**`get_dodge()` 修正链** ([melee.cpp:1148](file:///e:/Cataclysm-Medieval/src/melee.cpp#L1148-L1197))：

```
get_dodge = 基础闪避
          ÷ 2           (如果被陷阱困住)
          ÷ 2~5         (轮滑鞋惩罚)
          × speed/100   (speed < 100 时线性衰减)
          × stamina_logistic    (体力 logistic 衰减，低于10%体力时趋近0)
          × limb_score_reaction (肢体反应分数 — 手受伤/残废则降低)
          × limb_dodge_mod      (balance×1.5 + move_speed + footing — 腿受伤则降低)
          ÷ anatomy_size_ratio  (体型修正)
```

**三个关键修正项：**

| 修正项 | 来源 | 说明 |
|--------|------|------|
| `limb_score_reaction` | 各身体部位的 "reaction" score | 手部受伤/残废 → reaction 下降 → dodge 降低 |
| `limb_dodge_mod` | `character_modifiers.json` `limb_dodge_mod` | balance×1.5 + move_speed + footing 综合，腿受伤 → 降 dodge |
| `stamina_logistic` | `get_stamina_dodge_modifier()` ([character.cpp:1222](file:///e:/Cataclysm-Medieval/src/character.cpp#L1222-L1229)) | 1.0 - logarithmic_range(10%, 90%, current_stamina)，体力越少 dodge 越低 |

---

### 2.3 命中判定 — deal_melee_attack()

`Creature::deal_melee_attack()` ([creature.cpp:738](file:///e:/Cataclysm-Medieval/src/creature.cpp#L738-L766))：

```
hit_spread = hit_roll - dodge_roll - size_melee_penalty
```

- `hit_spread > 0` → **命中**
- `hit_spread ≤ 0` → **未命中**，触发 `on_dodge`

**`size_melee_penalty()`** ([creature.cpp:671](file:///e:/Cataclysm-Medieval/src/creature.cpp#L671-L690)) — 被减数，正数更难命中：

| 体型 | 值 | 效果 |
|------|---|------|
| tiny | +30 | 极小目标，非常难打中 |
| small | +15 | 小目标 |
| medium | 0 | 人类体型 |
| large | -10 | 大体型，容易打中 |
| huge | -20 | 巨兽，极易打中 |

---

### 2.4 暴击判定

`Character::crit_chance()` ([melee.cpp:1070](file:///e:/Cataclysm-Medieval/src/melee.cpp#L1070-L1141)) 使用**三重独立概率**：

| 概率来源 | 公式 | 典型值（新手/专家） |
|---------|------|-------------------|
| 武器暴击 | 0.5 + 0.1×m_to_hit（徒手 0.5+0.05×unarmed） | 50% / 60% |
| 属性暴击 | 0.25 + 0.01×DEX + 0.02×PER | 49% (8/8) / 55% (10/10) |
| 技能暴击 | 0.25 + (weapon_skill + melee/2.5) × 0.025 | 25% (0级) / 60% (10级) |

判定逻辑：

- **三重全中**（概率 = weapon × stat × skill）→ 无条件暴击
- **hit_roll > dodge_roll × 1.5** → 额外触发二重暴击（任意两重中即可），概率大幅提高

最终暴击概率 = 无条件暴击概率 + 条件暴击概率 + 武术 buff 暴击修正。

暴击时伤害倍率见下文 `roll_melee_damage_internal` 中的 `crit` 分支。

---

### 2.5 伤害生成

详见 [code_armor_penetration_system.md](code_armor_penetration_system.md) 完整链路。

速览：

| 步骤 | 函数 | 文件 |
|------|------|------|
| 伤害投骰 | `roll_melee_damage_internal` | melee.cpp:1225 |
| 附魔修正 | `modify_damage_dealt_with_enchantments` | melee.cpp:489 |
| 护甲吸收 | `Character::absorb_hit` → `outfit::absorb_damage` → `item::mitigate_damage` | character_armor.cpp / attire.cpp / item.cpp |
| 有效抗性 | `resistances::get_effective_resist` = max(resist - res_pen, 0) × res_mult | damage.cpp:620 |

**伤害倍率修正**：

- 长柄武器打贴身：×0.7
- 倒地攻击：×0.3
- 蹲伏攻击：×0.8
- 手臂残废徒手：×0.1

---

### 2.6 体力消耗

```
基础体力消耗 = min(-50, 武器标准体力消耗)
总消耗 = min(-50, 基础消耗 + 近战技能 - 姿态惩罚)
```

近战技能越高体力消耗越少；倒地 +50 惩罚，蹲伏 +20 惩罚。

---

## 三、命中部位选择

### 3.1 入口

`Creature::deal_melee_hit()` ([creature.cpp:792](file:///e:/Cataclysm-Medieval/src/creature.cpp#L792-L793))：

```cpp
bodypart_id bp_hit = select_body_part(-1, -1, source->can_attack_high(), hit_spread);
```

传入 `hit_spread`（命中差值），委托给 `anatomy::select_body_part()`。

### 3.2 核心算法

`anatomy::select_body_part()` ([anatomy.cpp:198](file:///e:/Cataclysm-Medieval/src/anatomy.cpp#L198-L246))：

```
对每个身体部位 bp：

  ① 初始权重 = bp.hit_size

  ② 如果 !can_attack_high（攻击者倒地）：
       - 上肢（头/手/胳膊）→ 直接丢弃
       - 下肢（腿/脚）→ 权重 × 3

  ③ 如果 hit_spread > 0：
       最终权重 = 初始权重 × hit_spread ^ hit_difficulty

  ④ 加权随机抽取
```

### 3.3 JSON 数据（人类解剖，body_parts.json）

| 部位 | `hit_size` | `hit_difficulty` | 说明 |
|------|-----------|-----------------|------|
| torso | 36 | 1.0 | 最大，基准难度 |
| arm_l / arm_r | 13 | 0.95 | 中等大小，稍难命中 |
| leg_l / leg_r | 13 | 0.9 | 中等，稍易命中 |
| head | 4 | **1.2** | 小且最难命中 |
| foot_l / foot_r | 2 | 0.8 | 小但容易蹭到 |
| hand_l / hand_r | 1.5 | 1.1 | 很小，较难命中 |
| eyes / mouth | 0.5 | 1.15 | 极小，很难命中 |

### 3.4 数学直觉

`hit_difficulty` 控制精度对命中该部位概率的**指数放大效应**：

- `hit_difficulty < 1`（腿 0.9、脚 0.8）→ hit_spread 增长时权重增长**慢**
- `hit_difficulty = 1`（torso）→ 权重与 hit_spread 线性增长
- `hit_difficulty > 1`（头 1.2、手 1.1）→ 权重**指数级**增长，高精度大幅提高命中率

### 3.5 实例：hit_spread 对分布的影响

| hit_spread | torso | head | arm (单) | leg (单) | hand (单) | foot (单) |
|------------|-------|------|----------|----------|-----------|-----------|
| 5（勉强命中） | 38% | 6% | 13% | 12% | 2% | 1.5% |
| 30（正常命中） | 37% | 8% | 11% | 9.5% | 2% | 1% |
| 80（精准命中） | 33% | 9% | 10% | 8% | 2% | 0.8% |

**结论**：hit_spread 越高，头部等小部位概率上升（6%→9%），但变化幅度有限——torso 的巨大 `hit_size=36` 基数始终主导分布。要显著提高头部命中率，需要极大的 hit_spread 差值（200+）。

---

## 四、格挡系统

`Character::block_hit()` (`melee.cpp:2034+`)：

- 每回合有 `blocks_left` 格挡次数
- 格挡反应检测：`近战技能 × 20 × limb_score_reaction / 100 ≥ 随机值`
- 格挡等级（`melee::blocking_ability()`）：
  - WBLOCK_3 → +10
  - WBLOCK_2 → +6
  - WBLOCK_1 → +4
  - BLOCK_WHILE_WORN → +2
- 格挡可吸收物理伤害（`mabuff_block_bonus()`）

---

## 五、远程攻击

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

- `recoil` 值越高越不准（单位：MoA，分角）
- 每次射击后后坐力达到 `MAX_RECOIL`
- 花行动点瞄准可降低后坐力
- `MIN_RECOIL_IMPROVEMENT = 0.01` MoA — 低于此值不再改进

---

## 六、弱点系统 (Weakpoint)

相关文件：`src/weakpoint.cpp` / `src/weakpoint.h`

怪物可以有弱点部位，命中弱点时：
- 伤害倍率增加
- 可能触发额外效果

---

## 七、武器耐久度

`Character::handle_melee_wear()` (`melee.cpp:201-333`)：

- 每次攻击都有概率损伤武器
- 概率取决于：敏捷、近战技能、武器材料 (`chip_resistance()`)
- **FRAGILE_MELEE** 标记：劣质武器，按组件逐一判定损坏
- **DURABLE_MELEE** 标记：耐打（损坏概率 ×4 生存率）
- **UNBREAKABLE_MELEE** 标记：永不损坏
