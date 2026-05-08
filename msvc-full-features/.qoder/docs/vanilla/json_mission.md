# 参考文档：CDDA 任务与剧情系统调研

> 来源：`cataclysm-dda/json/` 目录实地分析
> 覆盖：missiondef.json / effects_on_condition/ / talk_topic 系统

---

## 一、相关文件索引

```
json/
├── npcs/missiondef.json                    ← ★ 主任务定义（54 KB，100+ 任务）
├── npcs/starting_missions.json             ← 开局角色任务
├── npcs/common_chat/TALK_COMMON_MISSION.json ← ★ 任务对话模板
├── npcs/godco/godco_missions.json          ← GodCo 派系任务链（22+ 链）
├── npcs/valhalla_cult/missions.json        ← Valhalla 教派任务链
├── npcs/cabin_chemist/chemist_missions.json ← 化学家任务链
├── npcs/lumbermill_employees/lumbermill_missions.json ← 伐木场任务
├── npcs/exodii/exodii_merchant_missions.json ← Exodii 商人任务
├── npcs/isolated_road/isolated_road_missions.json ← 孤路遭遇任务
│
├── effects_on_condition/                   ← ★ EOC 事件系统（26 文件，347+ EOC）
│   ├── example_eocs.json                   ← EOC 完整示例（31 EOC）
│   ├── misc_effect_on_condition.json       ← 通用效果（16 EOC）
│   ├── generalized_eocs.json               ← ★ 随机遭遇框架（EOC_RandEnc）
│   ├── scenario_specific_eocs.json         ← 开局事件（16 EOC）
│   ├── weather_eocs.json                   ← 天气事件（4 EOC）
│   ├── dream_eocs.json                     ← 梦境事件（3 EOC）
│   ├── melee_eocs.json                     ← 近战职业系统（28 EOC）
│   ├── npc_eocs/generic_npc_eocs.json      ← ★ NPC 生成 + 暗杀者系统（13 EOC）
│   ├── npc_eocs/godco_npc_eocs.json        ← 派系 NPC 处理（6 EOC）
│   ├── mapgen_eocs/lab_mapgen_eocs.json    ← 实验室区域触发（18 EOC）
│   └── nether_eocs/                        ← 异界风暴系统（122+ EOC）
│       ├── portal_storm_effect_on_condition.json (70 EOC)
│       ├── portal_dependent_effect_on_condition.json (38 EOC)
│       └── vitrification_effect_on_condition.json (9 EOC)
│
└── npcs/Backgrounds/                       ← 65 个 talk_topic 出身故事对话
```

> **核心要点**：CDDA 的剧情系统由三层构成——`talk_topic`（对话交互）、`mission_definition`（任务追踪）、`effect_on_condition`（事件触发）。三者协作形成一个完整的 RPG 任务引擎。

---

## 二、核心配置类型

### 2.1 `mission_definition` —— 任务定义

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | string | 唯一标识 | `"MISSION_GET_BLACK_BOX"` |
| `name` | object | 显示名 | `{ "str": "Find the Black Box" }` |
| `description` | string | 可选详细描述 | — |
| **`goal`** | enum | 完成条件类型 | `MGOAL_FIND_ITEM`, `MGOAL_KILL_MONSTER` 等 20+ 种 |
| `goal_condition` | object | 自定义条件（配合 `MGOAL_CONDITION`） | `{ "days_since_cataclysm": 7 }` |
| **`followup`** | string | ★ 完成后自动触发的下一任务 | `"MISSION_GET_BLACK_BOX_TRANSCRIPT"` |
| `origins` | array | 谁能提供此任务 | `[ "ORIGIN_SECONDARY" ]` |
| `difficulty` | int | 任务难度 | 1~7 |
| `value` | int | 奖励金额 | 50000 |
| **`start`** | object | ★ 任务开始时执行 | 生成怪物/物品/修改地图 |
| **`end`** | object | ★ 任务完成时执行 | 奖励/对话/状态变更 |
| `fail` | object | 任务失败时执行 | NPC 死亡等 |
| `deadline_low/high` | int | 时间限制（小时） | 30 / 48 |
| `urgent` | bool | 标记为紧急 | `true` |
| **`dialogue`** | object | ★ 全套对话文本 | 见 §四— |

#### goal 类型一览（20+ 种）

| 类型 | 含义 | 典型场景 |
|------|------|----------|
| `MGOAL_GO_TO_TYPE` | 到达某类地形 | "去安全屋" |
| `MGOAL_GO_TO` | 到达指定地点 | "找到避难中心" |
| `MGOAL_FIND_ITEM` | 找到指定物品 | "取回黑匣子" |
| `MGOAL_FIND_ANY_ITEM` | 找到任意一件 | "捡一把枪回来" |
| `MGOAL_FIND_ITEM_GROUP` | 找到组内物品 | "带药回来" |
| `MGOAL_FIND_NPC` | 找到指定 NPC | 社交任务 |
| `MGOAL_TALK_TO_NPC` | 与 NPC 对话 | 对话推进剧情 |
| `MGOAL_FIND_MONSTER` | 发现怪物位置 | 侦察任务 |
| `MGOAL_KILL_MONSTER` | 击杀指定怪物 | 杀独特敌人 |
| `MGOAL_KILL_MONSTER_SPEC` | 击杀 N 只某物种 | "杀 300 僵尸" |
| `MGOAL_KILL_MONSTER_TYPE` | 击杀某类型怪 | 类型讨伐 |
| `MGOAL_ASSASSINATE` | 刺杀指定目标 | 阵营冲突 |
| `MGOAL_RECRUIT_NPC` | 招募指定 NPC | 同伴招募 |
| `MGOAL_RECRUIT_NPC_CLASS` | 招募某职业 NPC | 职业招募 |
| `MGOAL_COMPUTER_TOGGLE` | 操作终端 | 黑客任务 |
| `MGOAL_CONDITION` | 自定义条件 | 存活 7 天 |
| `MGOAL_NULL` | 手动完成（对话驱动） | 纯剧情推进 |

#### start / end 效果

```json
"start": {
  "effect": [                              // 任务开始时执行的 effect 列表
    { "u_spawn_item": "keycard", "count": 1 },
    { "npc_add_trait": "NPC_GUARDING" },
    "assign_guard"                         // NPC 驻守
  ],
  "assign_mission_target": {               // 标记目标位置
    "om_terrain": "haz_sar_b_4",           // 目标地形 ID
    "reveal_radius": 1,                    // 地图揭示范围
    "search_range": 240,                   // 搜索半径
    "min_distance": 60                     // 最小距离
  },
  "update_mapgen": {                       // 修改地形/生成敌人
    "place_monster": [
      { "monster": "mon_zombie_brute", "x": 18, "y": 23, "target": true }
    ],
    "place_npcs": [
      { "class": "tracker", "x": 11, "y": 11, "target": true }
    ]
  }
}
```

> **关键能力**：任务 start 可以在目标地点**动态生成怪物、NPC、物品、修改地形**。这意味着"接受任务"本身就改变了世界。

---

### 2.2 `effect_on_condition` —— EOC 事件脚本

> 全量 347+ EOC，分布在 26 个文件中。本节梳理其结构和模式。

#### 完整字段表

| 字段 | 类型 | 说明 | 可选 |
|------|------|------|------|
| `type` | string | 固定 `"effect_on_condition"` | 必填 |
| `id` | string | 唯一标识 | 必填 |
| **`eoc_type`** | enum | 触发模式 | 可选，默认定期轮询 |
| **`required_event`** | string | 事件驱动的具体事件名 | `eoc_type: "EVENT"` 时必填 |
| **`recurrence`** | array | 检查间隔 `[最小值, 最大值]` | 定期轮询时用 |
| **`global`** | bool | 全局后台运行（无视玩家位置） | 可选 |
| **`condition`** | object | ★ 触发条件（逻辑表达式） | 可选 |
| **`effect`** | array | ★ 条件满足时执行的操作列表 | 必填 |
| `false_effect` | array | 条件不满足时执行 | 可选 |
| `deactivate_condition` | object | 满足后永久关闭此 EOC | 可选 |

#### eoc_type — 5 种触发模式

| 模式 | 触发机制 | 适用场景 |
|------|----------|----------|
| （默认）定期轮询 | 按 `recurrence` 间隔反复检查 `condition` | 天气效果、暗杀者巡逻、长期事件 |
| `EVENT` | 游戏引擎发出事件时立刻触发 | 进入区域、击杀、施法、起床 |
| `SCENARIO_SPECIFIC` | 角色创建时触发 | 开局设置（给装备/状态/任务） |
| `NPC_DEATH` | NPC 死亡时触发 | 防止关键 NPC 死亡、触发复仇 |
| `AVATAR_DEATH` | 玩家死亡时触发 | 接管随从、复活机制 |

#### required_event — 可用的事件信号

| 事件名 | 触发时机 |
|--------|----------|
| `avatar_enters_omt` | ★ 玩家踏入某 overmap tile |
| `avatar_moves` | 玩家每次移动 |
| `game_start` | 游戏启动/加载 |
| `character_wakes_up` | 玩家醒来 |
| `character_kills_monster` | 击杀怪物 |
| `character_melee_attacks_character` | 近战攻击 |
| `character_takes_damage` | 受到伤害 |
| `character_gains_effect` | 获得新状态效果 |
| `character_dies` | 玩家（或其他角色）死亡 |
| `activates_mininuke` | 激活迷你核弹 |
| `spellcasting_finish` | 施法完成 |
| `character_finished_activity` | 活动完成 |

#### condition — 可用条件类型

```
时间/日期
  ├── days_since_cataclysm: N        ← 灾难后第 N 天
  ├── is_weather: "thunder"          ← 天气判定
  ├── is_season: 季节
  └── is_day: 是否白天

位置
  ├── u_at_om_location: "ID"         ← 精确在此地形格
  ├── u_near_om_location: "ID", range: N ← 距离此格 N 格内
  ├── u_is_outside: 是否室外
  └── map_in_city: 是否在城区

角色状态
  ├── u_has_trait: 拥有特质
  ├── u_has_effect: 拥有状态效果
  ├── u_has_bionics: 拥有仿生体
  ├── u_has_var: 拥有变量（剧情进度）
  └── u_has_items: 拥有物品

派系关系
  └── faction_like: "派系ID"         ← 获取关系值

概率
  ├── one_in_chance: 1/N
  └── x_in_y_chance: { x, y }

数学
  └── math: [ "表达式" ]             ← 支持变量运算和比较

组合
  ├── and: [ cond1, cond2, ... ]
  ├── or: [ cond1, cond2, ... ]
  └── not: { cond }
```

#### effect — 可用操作清单

| 操作 | 说明 |
|------|------|
| `u_spawn_monster` | 生成怪物（可指定 ID、数量、半径、是否组队） |
| `u_spawn_npc` | 生成 NPC |
| `u_teleport` | 传送玩家（可传至全局坐标） |
| `npc_teleport` | 传送 NPC |
| `u_message` | 弹出消息文本 |
| `sound_effect` | 播放音效 |
| `assign_mission` | 分配任务 |
| `offer_mission` | 提供任务（可拒绝） |
| `remove_active_mission` | 移除任务 |
| `mapgen_update` | 修改地形（烧房、路障、建筑变化） |
| `u_add_effect` | 添加状态效果 |
| `u_lose_effect` | 移除状态效果 |
| `u_add_var` | ★ 设置剧情进度变量 |
| `u_has_var` | 检查变量 |
| `run_eocs` | 串联执行其他 EOC |
| `run_eoc_with` | 带参数执行 EOC |
| `queue_eocs` | 延迟执行 EOC |
| `if/then/else` | 条件分支 |
| `switch/case` | 多路分支 |
| `run_until` | 循环 |

---

### 2.3 任务对话系统（talk_topic × mission）

任务对话通过 9 个标准 talk_topic 衔接：

```
TALK_MISSION_OFFER          → NPC 提议任务（玩家可接受/拒绝）
TALK_MISSION_ACCEPTED       → 接受后 NPC 回应（触发 assign_mission）
TALK_MISSION_REJECTED       → 拒绝后 NPC 回应
TALK_MISSION_INQUIRE        → 询问进度／汇报完成
TALK_MISSION_ADVICE         → 询问提示
TALK_MISSION_SUCCESS        → 完成汇报（触发 mission_success effect）
TALK_MISSION_SUCCESS_LIE    → 欺骗 NPC 已完成的回应
TALK_MISSION_FAILURE        → 汇报失败
TALK_MISSION_LIST           → 列出可用任务
TALK_MISSION_LIST_ASSIGNED  → 列出进行中任务
```

对话条件示例：
```json
"condition": { "mission_goal": "MGOAL_ASSASSINATE" }
"condition": { "and": [ "mission_incomplete", { "mission_goal": "MGOAL_FIND_ITEM" } ] }
"condition": { "and": [ "mission_complete", { "mission_goal": "MGOAL_KILL_MONSTER" } ] }
```

---

## 三、剧情编排模式（从实际数据中提取）

### 3.1 任务链模式（mission chain）

```
MISSION_GET_FLAG
  "followup": "MISSION_GET_BLACK_BOX"               ← 完成后自动推进
    "followup": "MISSION_GET_BLACK_BOX_TRANSCRIPT"
      "followup": "MISSION_EXPLORE_SARCOPHAGUS"

MISSION_CABIN_CHEMIST_GET_60_chem_muriatic_acid
  "followup": "MISSION_CABIN_CHEMIST_GET_500_GAS"
    "followup": "MISSION_CABIN_CHEMIST_SET_TRADE_ROUTE"
```

> `followup` 字段使任务自动链式推进，无需 EOC 额外介入。

### 3.2 区域触发 + 任务分配模式

```json
// EOC 监听玩家踏入某区域
{
  "eoc_type": "EVENT",
  "required_event": "avatar_enters_omt",
  "condition": {
    "u_near_om_location": "skalitz_border", "range": 0
  },
  "effect": [
    { "u_spawn_monster": "mon_cuman_soldier", "real_count": 15 },
    { "u_message": "库曼人来了！快逃！" },
    { "assign_mission": "MISSION_ESCAPE_SKALITZ" }
  ]
}
```

### 3.3 随机遭遇框架（EOC_RandEnc）

```json
// run_eoc_with 传递配置参数
{
  "run_eoc_with": "EOC_RandEnc",
  "variables": {
    "omt": "roadstop_a",                        // 目标地形
    "map_update": "nest_RandEnc_roadstop_add",   // 生成的地图更新
    "map_removal": "nest_RandEnc_roadstop_rem",  // 离开后清理
    "chance": "10"                               // 触发概率 10%
  }
}
```

这个框架可以复用来创建各种随机遭遇——路边强盗、流浪商人、逃难者队伍。

### 3.4 暗杀者波次系统（动态难度）

```json
// 三个 EOC 对应三种威胁等级
EOC_BANDIT_ASSASSIN:    faction_like < -40  → 生成 1 个刺客，每 60~100 天
EOC_BANDIT_ASSASSIN_2:  faction_like < -60  → 生成 2 个刺客，每 40~80 天
EOC_BANDIT_ASSASSIN_3:  faction_like < -90  → 生成 3 个刺客，每 20~60 天
```

> **模式提取**：条件值越极端 → 频率越高 → 数量越多。这为动态难度系统提供了模板。

---

## 四、EOC 系统能力评估

### 4.1 纯 JSON 可实现的剧情功能

| 功能 | 实现机制 | CDDA 已有案例 |
|------|----------|-------------|
| 主线任务链 | `followup` 字段 | ✅ Valhalla Cult 5 步任务链 |
| 区域触发事件 | `required_event: "avatar_enters_omt"` | ✅ Portal Storm 系统 |
| 到达区域后刷怪/改地形 | `mapgen_update` + `place_monster` | ✅ 实验室安保系统 |
| 动态生成敌人波次 | `u_spawn_monster` + group | ✅ 暗杀者系统 |
| 剧情分支 | `if/then/else` + `switch/case` | ✅ 梦境/幻觉系统 |
| 剧情进度追踪 | `u_add_var` / `u_has_var` | ✅ story flag 系统 |
| 开局自定义剧情 | `eoc_type: "SCENARIO_SPECIFIC"` | ✅ 多个 existing 开局 |
| NPC 死亡响应 | `eoc_type: "NPC_DEATH"` | ✅ 派系复仇 |
| 定期巡逻/事件 | `global: true` + `recurrence` | ✅ 暗杀者定期刷新 |
| 天气关联事件 | `is_weather` 条件 | ✅ 雷暴/暴雪效果 |
| 动态对话 | `talk_topic` 条件 | ✅ TALK_COMMON_MISSION |

### 4.2 CDDA 不具备的能力（不在 JSON 中）

| 能力 | 说明 |
|------|------|
| **过场动画/播片** | 不存在。只能用 `u_message` 文字替代 |
| **预设 NPC 移动路径** | NPC 行为由 AI 驱动，无法脚本化精确移动 |
| **非对话的选项 UI** | 只有 talk_topic 对话树能弹出选项，其他场景无法 |
| **时间冻结/暂停** | 事件触发时游戏时间照常流逝 |
| **全局世界状态广播** | 多个 NPC 同时对事件做出独立反应的能力有限 |

---

## 五、总结

1. **CDDA 拥有一套完整的 RPG 任务引擎**——`mission_definition` + `effect_on_condition` + `talk_topic` 三层协同，覆盖了从分支对话、任务追踪、动态遭遇到世界变化的全链条。

2. **EOC 是最灵活的事件系统**——347+ EOC 定义了 5 种触发模式、30+ 种条件类型、20+ 种可执行操作，本质上是纯 JSON 编写的"游戏逻辑脚本"。区域触发、时间驱动、全局后台轮询、事件信号监听，四种模式覆盖了回合制 RPG 中大部分剧情需求。

3. **任务链、条件分支、变量追踪均已成熟**——`followup` 自动推进、`if/then/else`/`switch` 控制分支、`u_add_var` 追踪进度，构成了一套完备的剧情状态机。

4. **核心限制不在机制而在交互**——没有播片、没有精确的 NPC 脚本移动、没有非对话的选项 UI。但**剧情逻辑本身完全可由 JSON 驱动**。
