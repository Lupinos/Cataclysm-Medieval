# 战斗系统（0.H 原版）

> 核对基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 初始提交的父提交）。以下描述该基准原版，不代表旧 Medieval 引擎。源码路径均相对此基准。

## 近战命中链

入口主要在 `src/melee.cpp::Character::melee_attack`、`melee_attack_abstract`；命中检测调用目标 `Creature::deal_melee_attack`，伤害与命中部位继续进入 `deal_melee_hit`、`deal_damage`。

`Character::get_hit_base`（`src/character.cpp`）返回 `DEX / 4.0`，不直接包含 PER。`Character::get_hit_weapon`（`src/melee.cpp`）为：

```text
对应武器技能/3 + melee技能/2 + itype::m_to_hit
```

CQB 生化模块可对这里使用的武器技能设下限。随后加上武术命中 buff；未矫正远视减 2，倒地减 8，否则蹲伏减 2，再乘 `character_modifier_melee_attack_roll_mod`（角色修正器，不应直接称作附魔倍率）。

`melee::melee_hit_range` 从均值 `accuracy*5`、标准差 25 的正态分布抽取命中投骰。约 95% 的值在均值 ±50 内，但不是硬上下限。

`Creature::deal_melee_attack` 使用：

```text
hit_spread = hitroll - dodge_roll() - size_melee_penalty()
```

IMMOBILE 目标另加 40。体型 penalty 依次为 tiny 30、small 15、medium 0、large -10、huge -20。`Character::melee_attack_abstract` 的主攻击以 `hit_spread >= 0` 作为命中。`Creature::deal_melee_attack` 的 on_dodge 回调条件却含 `<= 0`，存在零值边界不一致；不能用回调条件倒推主攻击必然 miss。

## 闪避

`Character::get_dodge` 先检查能否尝试闪避，再在基类值上应用陷阱、轮滑鞋、速度、体力、reaction limb score、`limb_dodge_mod` 和身体大小比等修正，最低为 0。

`Character::dodge_roll` 通常返回 `get_dodge()*5`。EVASION 附魔可提前返回极高值。HARDTOHIT 分支源码是 `max(get_dodge(), get_dodge())*5`，但普通 `get_dodge` 本身不是随机投骰，不能仅凭“调用两次”称作两个独立随机骰取优。

怪物有自己的命中/闪避实现，不能把 Character 的技能和体力公式直接套到 Monster。

### 闪避乘数的具体顺序

`Character::get_dodge` 的修正依源码顺序为：

1. beartrap/lightsnare/heavysnare 任一命中：除以 2。
2. ROLLER_INLINE/QUAD/ONE：有 PROF_SKATER 时除以 2，否则除以 5。
3. speed < 100 时乘 speed/100；高于 100 不通过这一项额外增加。
4. 乘 `get_stamina_dodge_modifier()`；其值为 `1 - logarithmic_range(0.1*最大体力, 0.9*最大体力, 当前体力)`。
5. 乘 reaction limb score，再乘角色修正器 `limb_dodge_mod`。
6. 除以当前 anatomy 相对 human_anatomy 的 size ratio，最后最低为 0。

`data/json/character_modifiers.json` 中 limb_dodge_mod 的 limb_score_op 是乘法 `x`，配置含 balance 权重 1.5、move_speed、footing；不能把它直接读成这三个分数的加法。

## 暴击：三个分项与最终概率

`Character::scored_crit` 使用一次新的 `hit_roll()` 调用 `crit_chance`，因此不是直接重用前面命中判定的投骰。`crit_chance` 先算三个限制在 [0,1] 内的分项：

- W：默认 0.5；纯徒手为 `0.5 + 0.05*unarmed`；正武器 to_hit 将 W 提高到至少 `0.5+0.1*to_hit`，负值则直接加 `0.1*to_hit`。
- S：`0.25 + 0.01*DEX + 0.02*PER`。
- K：`0.25 + 0.025*(武器技能 + melee/2.5)`，CQB 在此也可影响武器技能。

令 T = W*S*K，B 为武术暴击 buff 修正（百分值除以 100）：

```text
若本次 roll_hit > 1.5*target_dodge：
    P = T + 0.5*(W*S + S*K + W*K - 3*T) + B
否则：
    P = T + B
```

代码最后用 `rng_float(0,1) < P`。所谓“双重暴击”项带有 0.5 系数，不能简化为“任意两项成功就全额算暴击”；武器 to_hit 的每点 0.1 只改 W，不是最终暴击率每点提高十个百分点。

## 命中部位

`Creature::deal_melee_hit` 可由调用者指定部位，未指定才调用 `select_body_part`。`Creature::select_body_part` 还会调整能否攻击高处的标志，再委托 `src/anatomy.cpp::anatomy::select_body_part`。

每个候选部位初始权重为 `hit_size`；按 min/max hit_size 过滤。不能攻击高处时，带 `LIMB_UPPER` flag 的部位被剔除，`LIMB_LOWER` 的权重乘 3；这是 flag 判断，不是按“头/手/腿”名称硬编码。正命中差值 h 时：

```text
weight(bp) = adjusted_hit_size(bp) * h ** hit_difficulty(bp)
概率(bp) = weight(bp) / 所有候选部位权重之和
```

这是一条幂函数，不是“指数级增长”；h 增大时高 `hit_difficulty` 部位的相对权重上升。实际权重还受候选 anatomy 和上述过滤影响。

`data/json/body_parts.json` 中的人类主要值：torso 36/1.0，head 4/1.2，单臂 13/0.95，单腿 13/0.9，单手 1.5/1.1，单脚 2/0.8，eyes、mouth 各 0.5/1.15（格式为 hit_size / hit_difficulty）。不要把它们直接当成固定命中百分比。

### 仅按人类 anatomy 权重推算的例子

下表假设完整 human_anatomy、可攻击高处、没有 min/max 筛选，仅代入上述权重公式；arm/leg/hand/foot 为**单侧**概率。它是公式计算，不是完整战斗命中率。

| h | torso | head | arm | leg | hand | foot | eyes | mouth |
|---|---|---|---|---|---|---|---|---|
| 5 | 37.76% | 5.79% | 12.58% | 11.61% | 1.85% | 1.52% | 0.67% | 0.67% |
| 30 | 39.03% | 8.56% | 11.89% | 10.03% | 2.28% | 1.10% | 0.90% | 0.90% |
| 80 | 39.34% | 10.50% | 11.41% | 9.17% | 2.54% | 0.91% | 1.05% | 1.05% |

头部相对躯干的权重比为 `(4/36)*h**0.2`，所以它随精度增加而上升，不能只看 hit_difficulty 就忽略 hit_size 基数。

## 伤害、护甲与技艺

`Character::roll_damage` 按伤害类型生成伤害实例；普通近战类型进入 `roll_melee_damage_internal`，包含力量、技能、武术、变异和暴击修正。技艺随后还可修改伤害和行动消耗。`Creature::deal_damage` 调用目标的虚函数 `absorb_hit` 后才扣实际 HP。

- Character 的穿戴护甲有覆盖率、材料和多层吸收。
- Monster 使用天生抗性、弱点和附加护甲，其 HP 为全局值。
- 原版没有 Medieval 的力量乘武器重量固定破甲，也没有怪物残肢溢出伤害沿 anatomy 扩散。

完整穿透字段与公式见 [护甲穿透](code_armor_penetration_system.md)；技艺筛选和执行见 [Technique 字段](json_technique_deep.md)；HP 与受伤见 [部位系统](code_bodypart_hp_system.md)。

### 已确认的姿态、距离与肢体伤害修正

`Character::melee_attack_abstract` 生成伤害实例后依次检查：

| 条件 | 伤害修正 |
|---|---|
| HAND 攻击且 working_arm_count < 1 | ×0.1，并取消已选技艺 |
| reach_range > 1、非 reach_attacking 且带 POLEARM flag | ×0.7；不能泛化到所有矛或所有长柄武器 |
| 倒地 | ×0.3 |
| 否则蹲伏 | ×0.8 |

随后才执行已选技艺的 `perform_technique` 等处理。

### 技能伤害倍率

`roll_melee_damage_internal` 对 stab 的技能倍率：skill <= 5 为 `0.66+0.1*skill`，否则 `0.86+0.06*skill`；其他普通近战类型 skill < 5 为 `0.8+0.08*skill`，否则 `0.96+0.04*skill`。bash 还有力量随机加值、低技能伤害 cap 和武术倍率；这些倍率不能当作完整伤害公式。

### 体力消耗

`get_base_melee_stamina_cost` 返回 `min(-50, get_standard_stamina_cost(weap))`。`get_total_melee_stamina_cost` 则直接使用标准消耗（**不是先夹过的 base 值**）：

```text
total_stam = min(-50, standard_stamina_cost + round(melee_skill) - stance_malus)
stance_malus = 倒地50，否则蹲伏20，否则0
```

实际攻击又可加 deft 等修正，再按至少消耗 50 的限制调用 `mod_stamina`。负数表示扣减。

## 格挡与武器损耗

`Character::block_hit`（`src/melee.cpp`）还受可格挡状态、次数、武器/身体格挡能力与 limb score 等限制，不是仅比较一个技能随机数。`melee::blocking_ability` 的 WBLOCK_3/2/1、BLOCK_WHILE_WORN 基础值分别是 10/6/4/2，后续吸收不能仅凭该值推断。

`Character::handle_melee_wear` 处理武器磨损，受武器抗崩裂能力、技能、敏捷与 FRAGILE_MELEE/DURABLE_MELEE/UNBREAKABLE_MELEE 等影响。UNBREAKABLE_MELEE 在此路径避免磨损，不等同于所有损坏入口都无敌。

普通磨损的 `stat_factor = DEX/2 + melee_skill + 64/max(arm_STR,4)`，再乘材料 chip_resistance 并除以 wear_multiplier，转换成整数 damage_chance；DURABLE_MELEE 将这个参数乘 4。代码通过 `one_in(damage_chance)` 判定是否继续损坏，参数不是“损坏概率乘 4”。FRAGILE_MELEE 会根据组件选取薄弱材料并在破坏后处理组件，不是简单对每件组件独立判定同样的磨损。

## 远程与弱点的边界

`src/ranged.cpp`、`src/ballistics.cpp` 管理射击、投掷、散布、弹道与命中；`recoil` 是瞄准状态的一部分，射击增加的后坐力由武器和角色计算，不能一概写成“每次射击后立即达到 MAX_RECOIL”。MAX_RECOIL 是最大瞄准偏差/重置相关的上限常量。

`src/weakpoint.cpp` 的怪物弱点能调整抗性和伤害，并可触发效果。弱点不是普通 anatomy 部位 HP 的同义词，命中弱点也不表示原版 Monster 有独立肢体血量。
