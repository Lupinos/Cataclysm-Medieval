# 参考文档：CDDA 任务与剧情系统调研

> 原版基准：CDDA 0.H 维护分支提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 项目初始化前）。下列路径、字段与流程以该提交为准，不代表后续 Medieval 改造。
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
| **`goal`** | enum | 完成条件类型 | `MGOAL_FIND_ITEM`, `MGOAL_KILL_MONSTER` 等 |
| `goal_condition` | object | 自定义条件（配合 `MGOAL_CONDITION`） | `{ "days_since_cataclysm": 7 }` |
| **`followup`** | string | 清理已交付任务时为 NPC 保留下一条可提供任务，不自动接取 | `"MISSION_GET_BLACK_BOX_TRANSCRIPT"` |
| `origins` | array | 谁能提供此任务 | `[ "ORIGIN_SECONDARY" ]` |
| `difficulty` | int | 任务难度 | 1~7 |
| `value` | int | 任务价值，非自动现金支付 | 50000 |
| **`start`** | object | ★ 任务开始时执行 | 生成怪物/物品/修改地图 |
| **`end`** | object | ★ 任务完成时执行 | 奖励/对话/状态变更 |
| `fail` | object | 任务失败时执行 | NPC 死亡等 |
| `deadline_low/high` | int | 时间限制；无单位数字按天解析，亦接受带单位时长 | "30 hours" / "48 hours" |
| `urgent` | bool | 标记为紧急 | `true` |
| **`dialogue`** | object | ★ 全套对话文本 | 见 §四— |

#### goal 类型一览（以src/mission.h为准）

| 类型 | 含义 | 典型场景 |
|------|------|----------|
| `MGOAL_GO_TO_TYPE` | 到达某类地形 | "去安全屋" |
| `MGOAL_GO_TO` | 到达指定地点 | "找到避难中心" |
| `MGOAL_FIND_ITEM` | 找到指定物品 | "取回黑匣子" |
| `MGOAL_FIND_ANY_ITEM` | 找到带本任务 ID 标记的物品 | 取回任务物品 |
| `MGOAL_FIND_ITEM_GROUP` | 找到组内物品 | "带药回来" |
| `MGOAL_FIND_NPC` | 找到指定 NPC | 社交任务 |
| `MGOAL_TALK_TO_NPC` | 与 NPC 对话 | 对话推进剧情 |
| `MGOAL_FIND_MONSTER` | 寻找并带回任务指定的友好怪物 | 寻找任务生物 |
| `MGOAL_KILL_MONSTER` | 击杀指定怪物 | 杀独特敌人 |
| `MGOAL_KILL_MONSTER_SPEC` | 击杀 N 只某物种 | "杀 300 僵尸" |
| `MGOAL_KILL_MONSTER_TYPE` | 击杀某类型怪 | 类型讨伐 |
| `MGOAL_ASSASSINATE` | 刺杀指定目标 | 阵营冲突 |
| `MGOAL_RECRUIT_NPC` | 招募指定 NPC | 同伴招募 |
| `MGOAL_RECRUIT_NPC_CLASS` | 招募某职业 NPC | 职业招募 |
| `MGOAL_COMPUTER_TOGGLE` | 操作终端 | 黑客任务 |
| `MGOAL_CONDITION` | 自定义条件 | 存活 7 天 |
| `MGOAL_NULL` | 空目标；成功逻辑看 mission::is_complete | 纯剧情推进 |

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

### 2.2 effect_on_condition：触发、队列与上下文

源码依据：src/effect_on_condition.h 的 eoc_type，src/effect_on_condition.cpp 的 load、load_new_character、process_effect_on_conditions、process_reactivate。

| eoc_type | 入口 |
|---|---|
| ACTIVATION | 被其他效果显式调用；无 recurrence 且无显式类型时的默认 |
| RECURRING | 按 recurrence 排队；设置 recurrence 会推导为此类型 |
| SCENARIO_SPECIFIC | 场景/角色初始化 |
| NPC_DEATH | NPC 死亡 |
| AVATAR_DEATH | 玩家死亡 |
| PREVENT_DEATH | 尝试阻止玩家死亡 |
| OM_MOVE | 大地图移动 |
| EVENT | 订阅 required_event 指定事件 |

不是默认定期轮询，也不只有5种。recurrence 用时长/变量解析器，不限数组；纯数字按 turns，带单位字符串显式给出时长。condition 选择 effect / false_effect。deactivate_condition 可将 recurring EOC 暂停到 inactive 集合，后续有重新激活检查，不是永久关闭。global 与 run_for_npcs 控制队列及玩家/NPC执行范围，不表示全世界远处 NPC 都按完整地图与AI模拟。

EVENT 的合法事件以 src/event.h / event.cpp 为准，如 avatar_enters_omt、character_kills_monster、character_takes_damage、spellcasting_finish。不要把概念性的“活动结束/获得状态”等名称直接当作存在的钩子。

条件与效果分别由 src/condition.cpp 与 src/npctalk.cpp 等解析：可以检查特质/物品/位置/时间、存取变量、调用或排队 EOC、生成物品/生物、地图更新、分配任务或交互。u_has_var 是条件而非效果。if/then/else、switch/case 等概念化伪代码必须转换成真实解析器接受的字段与结构。

NPC生成的 u_spawn_npc 和 mapgen place_npcs 均引用 npc 模板 ID，不是 npc_class。真实/幻觉数量均默认0，需显式给出。具体上下文中的 u/npc 指谁也需要沿调用者核实。

---

### 2.3 任务对话系统（talk_topic × mission）

任务对话通过标准 talk_topic 衔接：

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
  "followup": "MISSION_GET_BLACK_BOX"               ← 交付后提供后续任务
    "followup": "MISSION_GET_BLACK_BOX_TRANSCRIPT"
      "followup": "MISSION_EXPLORE_SARCOPHAGUS"

MISSION_CABIN_CHEMIST_GET_60_chem_muriatic_acid
  "followup": "MISSION_CABIN_CHEMIST_GET_500_GAS"
    "followup": "MISSION_CABIN_CHEMIST_SET_TRADE_ROUTE"
```

> talk_function::clear_mission（src/npctalk_funcs.cpp）预留 followup 并加入 NPC 可提供任务列表，不是完成时自动接取。

### 3.2 区域触发与任务

EVENT EOC 可以监听实际支持的事件，检查位置并分配任务/调用地图更新。原文库曼人、Skalitz等是 Medieval 设计示意而非0.H原版ID，不能原样执行。事件名和上下文以src/event.h及事件发送点为准。

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
EOC_BANDIT_ASSASSIN:    -60 < faction_like < -40 → 生成1个刺客，间隔60~100天
EOC_BANDIT_ASSASSIN_2:  -90 < faction_like < -60 → 生成2个刺客，间隔60~100天
EOC_BANDIT_ASSASSIN_3:  faction_like < -90 → 生成3个刺客，间隔60~100天
```

> **模式提取**：三档频率相同，数量增加；还分别限制灾难后天数、累计刺客数、天气和附近安全地点，并非好感越低刷新越快。依据 generic_npc_eocs.json。

---

## 四、复用边界与源码索引

任务链、条件对话、区域/时间触发、动态放置和地图更新可以复用；不能据此断言全部剧情都能纯JSON实现。原文“无非对话选项UI”“事件触发时游戏时间照常流逝”等绝对结论不成立：游戏是回合制，EOC/对话效果也包含交互和活动控制入口。精确走位、镜头/过场和多人同步演出需核对实际API，不能以调研代替验收。

- mission_type::load（src/missiondef.cpp）规定任务字段、阶段对象parse_funcs结构、NPC来源任务的必需dialogue文本。start/end示意并非任意EOC字段都能直接混用。
- mission_goal（src/mission.h）还包括 MGOAL_KILL_MONSTERS、MGOAL_KILL_NEMESIS；目标完成、交付和奖励属于不同阶段。
- talk_function::clear_mission（src/npctalk_funcs.cpp）决定后续任务提供，不能把followup等同自动接取。
- EOC_RandEnc是数据层约定，omt/map_update/map_removal/chance等变量由generalized_eocs.json实际读取；不能从名字反推单位、寿命或引擎内建行为。
- 文中 JSON 若有注释、占位ID或省略号，是配置模式示意，不是完整可运行定义。对象/文件数量是原调研快照，不是稳定接口。
