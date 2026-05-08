# 时间系统 (Time System)

> Cataclysm-Medieval 的时间系统核心机制分析

## 核心文件

| 文件 | 作用 |
|------|------|
| [`src/calendar.h`](../../../src/calendar.h) | 时间单位定义：`time_duration`, `time_point`, 时间字面量 |
| [`src/creature.h`](../../../src/creature.h) / [`src/creature.cpp`](../../../src/creature.cpp) | 生物基类：`moves`, `get_speed()`, `process_turn()` |
| [`src/character.h`](../../../src/character.h) / [`src/character.cpp`](../../../src/character.cpp) | 玩家速度：`get_speed()`, `run_cost()`, `recalc_speed_bonus()` |
| [`src/monster.h`](../../../src/monster.h) / [`src/monster.cpp`](../../../src/monster.cpp) | 怪物速度与移动 |
| [`src/monmove.cpp`](../../../src/monmove.cpp) | 怪物移动 AI 与 `calc_movecost()` |
| [`src/do_turn.cpp`](../../../src/do_turn.cpp) | 游戏主循环 |
| [`src/game_constants.h`](../../../src/game_constants.h) | 移动相关的全局常量 |
| [`src/move_mode.h`](../../../src/move_mode.h) | 移动模式（步行/跑步/蹲伏/匍匐） |
| [`src/speed_description.h`](../../../src/speed_description.h) | 怪物速度 UI 描述 |

## 时间单位体系

| 单位 | 换算 |
|------|------|
| `1 turn` | = 1 秒 |
| `100 moves` | = 1 turn |
| `1 分钟` | = 60 turns |
| `1 小时` | = 3600 turns |

核心实现位于 `calendar.h`：
- `time_duration` 以整数 `turns_` 存储时间间隔
- `time_point` 以整数 `turns_` 存储时间点
- `from_moves(n)` = `n / 100` — 100 行动点 = 1 回合
- `from_seconds(n)` = `n` — 1 回合 = 1 秒

## Speed → Moves → 动作消耗 链条

### 1. 每回合获得 Moves

`Creature::process_turn()` ([`creature.cpp:243-262`](../../../src/creature.cpp#L243-L262))：

```cpp
void Creature::process_turn() {
    // ... 重置加成、处理效果 ...
    if( !has_effect( effect_ridden ) ) {
        moves += get_speed();  // ← 关键！
    }
}
```

`Creature::get_speed()` ([`creature.cpp:2107-2109`](../../../src/creature.cpp#L2107-L2109))：
```cpp
int Creature::get_speed() const {
    return get_speed_base() + get_speed_bonus();
}
```

默认 `speed_base = 100`（[`creature.cpp:146`](../../../src/creature.cpp#L146)），即每回合获得 100 moves = 1 秒的行动预算。

### 2. 玩家 Speed 计算

`Character::get_speed()` ([`character.cpp:4195-4201`](../../../src/character.cpp#L4195-L4201))：

```cpp
int Character::get_speed() const {
    if( has_flag( json_flag_STEADY ) ) {
        return get_speed_base() + std::max( 0, get_speed_bonus() );  // 惩罚归零
    }
    return Creature::get_speed();  // = speed_base + speed_bonus
}
```

`speed_bonus` 由 `recalc_speed_bonus()` ([`character.cpp:12023-12088`](../../../src/character.cpp#L12023-L12088)) 计算，影响因素包括：

| 因素 | 效果 |
|------|------|
| 负重超限 | `25 × (超重量 / 负重上限)` 惩罚 |
| 敏捷 | 超过阈值后每点敏捷加成（由 `get_speedydex_bonus()` 计算） |
| 疼痛 | `pain^0.7` 惩罚，上限 50 |
| 口渴 (>40) | 阶梯惩罚 |
| 卡路里不足 | 速度惩罚 |
| 状态效果 (effects) | SPEED 修改量 |
| 武术 | 速度加成 |
| 温度/阳光 | 冷血/日光依赖等特性影响 |
| **下限保护** | speed_bonus 最低 `-0.75 × speed_base`，即速度最低为基础速度的 25% |

### 3. 玩家移动消耗 - run_cost()

`Character::run_cost()` ([`character.cpp:10148-10158`](../../../src/character.cpp#L10148-L10158))：
```cpp
int Character::run_cost( int base_cost, bool diag ) const {
    float movecost = static_cast<float>( base_cost );  // 基准 100
    if( diag ) { movecost /= M_SQRT2; }
    run_cost_effects( movecost );  // 应用各种修正
    if( diag ) { movecost *= M_SQRT2; }
    return static_cast<int>( movecost );
}
```

`run_cost_effects()` ([`character.cpp:10161-10324`](../../../src/character.cpp#L10161-L10324)) 中的修正因素：

| 类别 | 示例 |
|------|------|
| 地形障碍 | >105 时应用变异修正、跑酷 (×0.5)，最低到 100 |
| 匍匐/爬行 | `crawl_speed_movecost_mod` |
| 负重/伤口 | `limb_run_cost_mod` |
| 变异 | `movecost_modifier`, `movecost_flatground_modifier` |
| 赤脚 | 无鞋 +16，单只无鞋 +8 |
| 轮滑鞋 | 路面跑步 ×0.5，非路面 ×1.5 |
| 蹼 (Fins) | ×1.5 |
| 紧身衣 | ×1.1 |
| 体力 | `stamina_move_cost_mod` |
| 移动模式 | `move_mode_move_cost_mod`（步行/跑步/蹲伏/匍匐） |
| 倒地 | ×2.5 额外惩罚 |
| 附魔 | 加减法与乘数 |

### 4. 实际移动能力 - speed_rating()

`Character::speed_rating()` ([`character.cpp:10120-10129`](../../../src/character.cpp#L10120-L10129))：

```
每回合可移动格数 ≈ get_speed() / run_cost(100)
```

不跑步时还有体力系数额外调整。

## 游戏主循环

`do_turn()` ([`do_turn.cpp:403-726`](../../../src/do_turn.cpp#L403-L726)) 每回合执行顺序：

```
① calendar::turn += 1_turns          → 时间前进 1 秒（回合开头！）
② 玩家活动处理 (while moves > 0 && activity)
③ 玩家行动循环 (while moves > 0)       → handle_action() 处理输入
④ monmove()                          → 所有怪物 process_turn() + 行动
⑤ NPC 行动
⑥ 玩家 process_turn()                → moves += get_speed()（回合末尾补充）
⑦ 天气、气味、光照更新
```

**关键设计：**
- 时间在回合**开头**就前进 1 秒，与玩家做了多少动作无关
- 玩家在回合**末尾**才获得新 moves（用于下一回合）
- 怪物在④阶段开头获得 moves 并立即行动
- 同一回合内：玩家先动完 → 怪物才动

## 动作消耗与透支

每个动作直接扣 moves，**不检查是否足够**：

```cpp
// 开门: handle_action.cpp:581
player_character.moves -= 100;

// 砸东西: handle_action.cpp:1005
player_character.moves -= move_cost * weary_mult;
```

moves 可以为负数，负数由下回合的 `process_turn()` 补齐：
```
回合 N:   moves = 100 → 扣120 → moves = -20 (回合结束)
回合 N+1: moves = -20 + 100(process_turn) = 80
```

## 敌人（怪物）速度系统

怪物速度来源：JSON 定义的 `mtype->speed`，在构造时设置（[`monster.cpp:248-252`](../../../src/monster.cpp#L248-L252)）：

```cpp
moves = type->speed;
Creature::set_speed_base( type->speed );
```

与玩家完全相同的机制：`process_turn()` → `moves += get_speed()`，然后在 `while(moves > 0)` 中行动。

### 怪物移动消耗 calc_movecost()

[`monmove.cpp:1505-1557`](../../../src/monmove.cpp#L1505-L1557)：

| 移动方式 | 消耗 |
|----------|------|
| 飞行/挖掘 | 固定 100 moves/格 |
| 游泳 | 水中 50，陆地 50×地形 |
| 水下行走 | 水中 250，陆地 50×地形，总消耗 ÷2 |
| 攀爬 | 攀爬面 150，普通 50×地形，总消耗 ÷2 |
| 普通 | `(50×源格地形 + 50×目标格地形) / 2` |

怪物速度描述通过比较 `monster_speed_rating / player_speed_rating` 生成（[`monster.cpp:795-822`](../../../src/monster.cpp#L795-L822)）。

## 长时活动的中断机制

当玩家 moves 耗尽但有活动（activities）在进行时，系统检测到有危险敌人靠近会弹出警告（[`do_turn.cpp:571-577`](../../../src/do_turn.cpp#L571-L577)），调用 `cancel_activity_or_ignore_query()`（[`game.cpp:1425`](../../../src/game.cpp#L1425)）。

这不是实时打断——玩家先完成当前回合所有动作，怪物行动期间检测到危险时，在下一回合之前弹出警告。

## 全局常量

[`game_constants.h`](../../../src/game_constants.h)：
- `MAX_HANDLING_COST = 400`
- `INVENTORY_HANDLING_PENALTY = 100`
- `MAP_HANDLING_PENALTY = 80`
- `VEHICLE_HANDLING_PENALTY = 80`
- `MAX_MOVECOST_MODIFIER = 100.0f`

## 移动模式

[`move_mode.h`](../../../src/move_mode.h) 定义了四种模式，各有不同的 `move_speed_mult`、`stamina_mult`、`sound_mult`：

| 模式 | 说明 |
|------|------|
| PRONE | 匍匐 |
| CROUCHING | 蹲伏 |
| WALKING | 步行 |
| RUNNING | 跑步 |
