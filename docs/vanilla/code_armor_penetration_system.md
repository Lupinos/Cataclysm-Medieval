# 护甲穿透系统（0.H 原版）

> 核对基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 初始提交的父提交）。以下描述该基准原版，不代表旧 Medieval 引擎。源码路径均相对此基准。

## 数据与公式

`src/damage.h` 的 `damage_unit` 保存 `type`、`amount`、`res_pen`、`res_mult`、`damage_multiplier`、`unconditional_res_mult`、`unconditional_damage_mult`。普通构造默认固定穿透为 0，其余倍率为 1。

`src/damage.cpp` 的 `resistances::get_effective_resist`：

```text
有效抗性 = max(type_resist(type) - res_pen, 0)
         × res_mult × unconditional_res_mult
```

`res_pen` 是固定穿透；`res_mult` 是剩余抗性倍率，0.75 表示保留 75% 抗性。它不是直接的伤害倍率。

## 近战伤害如何产生穿透

`src/melee.cpp::roll_melee_damage_internal` 的普通近战分支以 `arpen = 0` 开始，徒手身体部位的 `unarmed_arpen` 和武术 `mabuff_arpen_bonus` 可以增加固定穿透。武器的 `item::damage_melee` 提供伤害量，不提供武器重量破甲。

暴击修正如下，`c` 为调用者传入的 `crit_mod`：

| 伤害类型 | 抗性倍率 `armor_mult` | 固定穿透修正 | 伤害倍率修正 |
|---|---|---|---|
| stab | `1 - 0.34*c` | 无 | `1 + skill/10*c` |
| cut | `1 - 0.25*c` | `int(5*c)` | `1 + 0.25*c` |
| bash | `0.5*c` | 无 | `1 + 0.5*c` |

常见 `c=1` 时才分别是 34%、25%+5、50% 的穿透效果。不要把这些常数当作所有暴击的固定结果。技艺还可通过 `ma_technique::armor_penetration` 的 flat arpen 添加伤害单元；远程弹药和法术等有自己的伤害实例来源。

## 伤害承受链路

`Creature::deal_damage`（`src/creature.cpp`）复制伤害实例，调用虚函数 `absorb_hit`，再按伤害类型处理剩余量，并调用目标的 `apply_damage`。因此同一个穿透字段在 Character 和 Monster 上要分别看吸收实现。

### Character：覆盖率与多层装备

`src/character_armor.cpp::Character::absorb_hit` 经过生化防御、附魔、`worn.absorb_damage`、被动防护等阶段。`src/character_attire.cpp::outfit::absorb_damage` 遍历穿戴装备，结合命中部位、覆盖率和材料等判定实际参与吸收的护甲。

单件装备调用 `src/item.cpp::item::mitigate_damage`：

```text
mitigation = resistances(该装备, …).get_effective_resist(du)
du.res_pen = max(du.res_pen - 该装备对此伤害类型的抗性, 0)
du.amount -= mitigation
```

固定穿透会在实际参与吸收的装备层之间消耗。不能简单把所有装备抗性先相加后只扣一次穿透，也不能忽略覆盖率便宣称每层总会吸收。

### Monster：天生护甲、弱点与附加护甲

`src/monster.cpp::monster::absorb_hit` 从怪物抗性构造 `resistances`，选择弱点并修正抗性，对每个伤害单元减去：

```text
min(有效抗性 + get_worn_armor_val(type), 当前 amount)
```

随后弱点还可修正伤害实例。原版 Monster 可以有附加护甲（例如宠物护甲），所以“Monster 不穿任何装备”不准确；它的这一吸收路径也不等同于 Character 的逐件穿戴装备处理。

## 耐久与伤害量

`src/item.cpp::item::damage_adjusted_melee_weapon_damage` 对非按 charges 计数物品使用：

```text
近战伤害量 × (1 - 0.1 × max(0, damage_level - 1))
```

完好和 damage_level 1 没有这项损失，level 2 才开始减 10%。详见 [物品破损系统](code_item_damage_system.md)。

## 与项目设计的边界

旧 Medieval 分支曾加入“力量 × 武器重量”固定破甲，属于项目改造，不是 0.H 原版。该设计的数值与物理解释不作为本文原版结论；重做时应独立确认规则及单位换算。
