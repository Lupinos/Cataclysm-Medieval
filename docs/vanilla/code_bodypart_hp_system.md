# 身体部位、HP 与受伤系统（0.H 原版）

> 核对基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 初始提交的父提交）。以下描述该基准原版，不代表旧 Medieval 引擎。源码路径均相对此基准。

## 基础部位数据

`src/bodypart.h` 的 `body_part_type` 是 JSON 蓝图，`bodypart` 是实例。`body_part_type::load` 在 `src/bodypart.cpp` 读取部位定义。

| 字段/概念 | 原版含义 |
|---|---|
| `base_hp` | 初始化部位 HP 的基础值，成员默认 60；Character 后续还会重新计算最大 HP |
| `hit_size` | 选择命中部位的初始权重 |
| `hit_difficulty` | 正命中差值的幂指数；不是直接的命中惩罚 |
| `is_vital` | Character 死亡判定使用的重要部位标记 |
| `main_part` | 主部位关系，例如手的伤害/治疗可能归属到手臂，具体由调用路径决定 |
| `connected_to`、`opposite_part` | 部位连接和对称关系；存在这些关系不等于已经实现通用断肢或伤害扩散 |
| `limb_type` / `limb_types` | 加载为部位类型及权重，不能直接以 C++ 成员名 `limbtypes` 当作 JSON 字段 |

`src/creature.cpp::Creature::set_body` 根据 anatomy 的部位列表创建 `bodypart` 实例。`data/json/anatomy.json` 的 `human_anatomy` 有 12 项，`default_anatomy` 有 torso、head 两项。

## Creature 的 HP 接口

`Creature` 持有 `body`，并提供 `get_part_hp_cur/max`、`set_part_hp_cur/max`、`mod_part_hp_cur/max` 等接口。`Creature::get_hp(bp)` 的默认实现：指定部位则查询该部位；NULL 部位则求所有部位当前 HP 之和。无参 `get_hp()` 调用 NULL 部位版本；`get_hp_max` 类似。

这些基类接口可被 Monster 继承，但“能调用部位接口”不等于 Monster 已经用部位 HP 驱动战斗、治疗和死亡。

## Monster 使用独立全局 HP

`src/monster.cpp`：

- 构造时设置 `default_anatomy` 并 `set_body()`。
- `monster::get_hp(bp)` 与无参 `get_hp()` 均返回全局 `hp`，忽略 bp。
- 两种 `get_hp_max` 均返回 `type->hp`。
- `monster::apply_damage` 忽略传入部位，执行 `hp -= dam`，并处理凶手与受伤触发器。
- `monster::heal_bp` 调用全局 `heal(dam)`。
- `monster::is_dead_state` 判断 `hp <= 0`。

因此原版普通 Monster 没有 Character 那套由各肢体 HP 驱动的致残模型，也没有 Medieval 四足 anatomy、纯部位 HP 或残肢伤害沿连接图扩散。迁移到部位血量需要逐一处理上述虚函数及存档、变形、复活、治疗等调用，不能仅把基类 getter 换进去便视作完成。

## Character 的部位伤与死亡

`src/character.cpp::Character::is_limb_broken` 判断该部位当前 HP 是否为 0。部位 HP 会通过 limb score、角色修正器和各行为自己的限制影响行动与战斗；具体影响要查对应行为，不能一概写成“骨折部位任何装备都不能穿”或“所有受伤均按一个比例缩放”。

`Character::is_dead_state` 遍历主要部位中的 `is_vital` 部位，有任一当前 HP <= 0 即判定死亡；不是检查全身 HP 总和。Creature 的部位 setter/modifier 还对 avatar 从未骨折变为骨折时发送事件，这不表示 NPC 不会受部位 HP 影响。

包扎、消毒、夹板和治疗属于 Character 的具体机制，不会因 Monster 继承了 `bodypart` 字段就自动生效。

## 流血：Monster 确实有，处理方式不同

Character 可按部位绑定 `bleed` effect，伤害效果入口见 `src/character.cpp::Character::on_damage_of_type` 及 `data/json/body_parts.json` 的 `effects_on_hit`。后续流血处理、压迫止血和止血带等见 Character 相关实现。

Monster 也有流血：

- `src/monster.cpp::monster::deal_damage_handle_type` 可依据穿刺、切割等伤害调用 `make_bleed`。
- `monster::make_bleed` 根据 `bleed_rate` 调整持续时间，以 NULL 部位附加 `bleed`；机器人使用 `dripping_mechanical_fluid`。
- `monster::process_one_effect` 对流血生成血迹，并简化为全局 HP 伤害。
- 对应免疫判定检查血液类型与 `bleed_rate`。

准确的区别是：原版 Monster 流血不是 Character 的逐肢体治疗/骨折模型，而不是“Monster 完全没有 bleed effect”。

## 源码入口

- `src/bodypart.h/.cpp`：蓝图、实例和部位字段加载。
- `src/anatomy.cpp`：部位选择和解剖列表。
- `src/creature.cpp`：身体组装、部位 HP 与默认总 HP 接口。
- `src/monster.cpp`：全局 HP、流血与死亡。
- `src/character.cpp`：重要部位死亡、骨折与治疗。
- [战斗系统](code_combat_system.md)：命中部位权重与伤害调用链。
