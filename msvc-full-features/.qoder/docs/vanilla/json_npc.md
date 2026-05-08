# 参考文档：CDDA NPC 配置体系调研

> 来源：`cataclysm-dda/json/npcs/` 目录实地分析

---

## 一、目录结构

```
json/npcs/
├── classes.json                    ← 主 npc_class 定义（25.7 KB，约 30 个类）
├── npc.json                        ← 顶层 npc 实例定义（deserter, farmer, cyborg 等）
├── npc_behavior.json               ← NPC AI 行为树定义（需求驱动）
├── factions.json                   ← ★ 所有派系定义 + 派系关系矩阵
├── NC_*.json                       ← 独立 npc_class + 装备 item_group（32 个文件）
├── items_generic.json              ← 通用 NPC 衣物池（内衣、裤子、鞋等）
├── BG_trait_groups.json            ← 出身故事 trait 分组
├── BG_traits.json                  ← 出身故事 trait 定义
├── appearance_trait_groups.json    ← 外观 trait 分组
├── starting_traits.json            ← NPC_starting_traits 通用特质池（collection）
├── expertise_traits.json           ← 专长特质
├── destination_locations.json      ← NPC 目的地位置定义
├── talk_tags.json / talk_tags_chat.json  ← 对话标签替换
├── shop_consumption_rates.json     ← 商人物品消耗率
│
├── Backgrounds/                    ← 65 个 talk_topic 文件（每个一种出身故事）
├── civilians/                      ← 平民对话模板（panic, fighter, officer 等）
├── common_chat/                    ← 通用对话（ALLY, GREET, MISSION, OTHER）
├── computers/                      ← 电脑终端对话（非传统 NPC）
│
│  ★ 派系/场景子目录（35 个）
├── hells_raiders/                  ← ★★ 原版唯一强盗派系（NC_BANDIT_LEADER 等）
├── slaves/                         ← 奴隶系统（被强盗俘虏）
├── holdouts/                       ← 孤立据点 NPC（含敌对牛仔，对话驱动敌对状态）
├── valhalla_cult/                  ← 北欧教派（完整小型派系范例）
├── refugee_center/                 ← 避难中心 NPC（约 25 个命名 NPC）
├── robofac/                        ← Hub01 机械派系 NPC
├── godco/                          ← Godco 教会派系 NPC
├── exodii/                         ← Exodii 跨世界旅者派系
├── old_guard/                      ← 老守卫（联邦政府残余）
├── Kindred/                        ← 具名同伴 NPC（深度角色）
├── isherwood_farm/                 ← Isherwood 农场 NPC
├── isolated_road/                  ← 孤立道路商人
├── island_prison/                  ← 监狱 NPC
├── campus/                         ← 大图书馆学者
├── bunker_shop/                    ← 地堡商人
├── cabin_chemist/                  ← 化学家小屋
├── mine/                           ← 矿场 NPC
├── lumbermill_employees/           ← 伐木场
├── tacoma_ranch/                   ← Tacoma 公社
├── random_encounters/              ← ★ 随机遭遇商队/NPC（EOC 触发）
├── portal_storm/                   ← 门户风暴事件 NPC
├── EOC_talkers/                    ← EOC 事件触发 NPC
├── scrap_trader/                   ← 废料交易者
├── your_followers/                 ← 玩家追随者相关
├── other/                          ← 独立幸存者（枪店、公寓、营地、酿酒等）
├── prisoners/                      ← 囚犯
├── Lighthouse_Family/              ← 灯塔家族
└── ...
```

> **文件总量**：npcs/ 目录下共约 **210+ 个 JSON 文件**，分布在 35 个子目录中。

---

## 二、核心配置类型

### 2.1 `npc_class` —— NPC 职业模板

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `type` | string | 固定 `"npc_class"` | `"npc_class"` |
| `id` | string | 唯一标识 | `"NC_SOLDIER"`, `"NC_FARMER"` |
| `name` | object | 显示名 | `{ "str": "Soldier" }` |
| `job_description` | string | 一句话描述（对话中用） | `"I'm just here for the paycheck."` |
| `common` | bool | 是否可被随机生成 | `true` / `false` |
| `common_spawn_weight` | float | 随机生成权重 | `1.0`（默认） |
| `traits` | array | 引用的 trait_group 或 trait 列表 | 见 §2.2 |
| `skills` | array | 技能分布定义 | 见 §2.3 |
| `bonus_str/dex/int/per` | distribution | 属性偏移 | `{ "rng": [0, 2] }` |
| `bonus_*` (personality) | distribution | 性格偏移 | `bonus_aggression`, `bonus_bravery` 等 |
| `worn_override` | item_group ID | 覆盖穿着物品（显式） | `"NC_VOICE_worn"`（见 NC_MARLOSS_VOICE） |
| `carry_override` | item_group ID | 覆盖携带物品 | `"NC_VOICE_carry"` |
| `weapon_override` | item_group ID | 覆盖武器 | `"NC_VOICE_weapon"` |
| `proficiencies` | array | 熟练度列表 | `[ "prof_gunsmithing_basic" ]` |
| `shopkeeper_item_group` | string | 商人销售物品池 | `"NC_DOCTOR_misc"` |

**装备分配：两种链接机制**

CDDA 用两种方式将 `npc_class` 与装备 `item_group` 关联：

```
方式 A：显式 override（直接在 npc_class 中引用 item_group ID）
  npc_class.worn_override = "NC_VOICE_worn"   ──→  item_group "NC_VOICE_worn"

方式 B：命名约定（npc_class 无 override 时，C++ 按类 ID 自动拼接组件名）
  npc_class id = "NC_SOLDIER"（无 override 字段）
      ↓ C++ 自动查询
  item_group "NC_SOLDIER_pants"     item_group "NC_SOLDIER_shirt"
  item_group "NC_SOLDIER_gloves"    item_group "NC_SOLDIER_coat"
  item_group "NC_SOLDIER_vest"      item_group "NC_SOLDIER_shoes"
  item_group "NC_SOLDIER_masks"     item_group "NC_SOLDIER_eyes"
  item_group "NC_SOLDIER_hat"       item_group "NC_SOLDIER_cutting"
  item_group "NC_SOLDIER_stabbing"  item_group "NC_SOLDIER_pistols"
  item_group "NC_SOLDIER_rifle"     item_group "NC_SOLDIER_misc"  ……
```

> **关键发现**：`NC_SOLDIER.json`、`NC_ARMY.json`、`NC_FARMER.json` 等独立文件**只包含 item_group，不包含 npc_class**。npc_class 定义在 `classes.json` 中。两者通过命名约定（`{CLASS_ID}_{组件}` 格式）由 C++ 自动关联，JSON 中看不到显式引用。

| 模式 | 示例 | 特征 |
|------|------|------|
| **显式 override** | `NC_MARLOSS_VOICE`, `NC_CYBORG`, `NC_TRUE_FOODPERSON` | npc_class 含 `worn_override` 等字段，直接显式引用 item_group |
| **命名约定** | `NC_SOLDIER`, `NC_ARMY`, `NC_FARMER` | npc_class 无 override 字段，C++ 按 `{类ID}_{组件名}` 拼接查询 item_group |

### 2.2 `npc` 实例 —— NPC 部署定义（★ 补充）

`npc_class` 只是"职业模板"，真正放置在世界中的 NPC 还需要一层 `npc` 实例定义：

```json
{
  "type": "npc",
  "id": "thug",                        // 唯一 ID，mapgen 引用它来放置 NPC
  "name_suffix": "Thug",               // 名字后缀（"John the Thug"）
  "class": "NC_THUG",                  // 引用 npc_class（决定技能/装备/属性）
  "attitude": 0,                       // 初始态度
  "mission": 8,                        // 行为模式
  "chat": "TALK_DONE",                 // 对话入口 talk_topic
  "faction": "hells_raiders"           // 所属派系
}
```

| 字段 | 说明 | 常见值 |
|------|------|--------|
| `attitude` | 初始态度 | 0=中立, 1=友好, 8=驻守不动, 10=主动敌对 |
| `mission` | 行为模式 | 0=无任务, 1=拦截/对话, 3=商人, 7=驻守, 8=巡逻 |
| `chat` | 对话入口 | talk_topic ID，`"TALK_DONE"` 表示无对话 |
| `faction` | 派系 | 决定与玩家/其他 NPC 的关系 |
| `name_unique` | 唯一名 | 用于命名 NPC（如 "Apis"） |
| `mission_offered` | 提供任务 | 任务 ID |
| `death_eocs` | 死亡触发 | EOC ID 列表 |

**关键设计**：`npc_class` 与 `npc` 是 **多对多关系** —— 同一个 `NC_THUG` class 可以被多个 npc 实例引用（强盗、疯子、守卫都可以用 NC_THUG 的战斗属性）。

### 2.3 `faction` —— 派系关系系统（★ 补充）

`factions.json` 定义了所有派系及其相互关系：

```json
{
  "type": "faction",
  "id": "hells_raiders",
  "name": "Hell's Raiders",
  "likes_u": -25,                      // 对玩家初始好感
  "respects_u": -25,                   // 对玩家初始尊重
  "size": 100,
  "power": 100,
  "food_supply": 230400,
  "wealth": 45000000,
  "relations": {                        // ★ 与其他派系的关系矩阵
    "hells_raiders": { "watch your back": true, "share my stuff": true, ... },
    "free_merchants": { "kill on sight": true },
    "old_guard": { "kill on sight": true },
    "your_followers": { "kill on sight": true }
  }
}
```

**7 种派系关系标记：**

| 标记 | 含义 | 典型应用 |
|------|------|----------|
| `kill on sight` | 见面就打 | 敌对派系 |
| `watch your back` | 帮你打架 | 盟友 |
| `share my stuff` | 共享物资 | 核心成员 |
| `guard your stuff` | 保护你的东西 | 友好派系 |
| `lets you in` | 允许进入领地 | 非敌对 |
| `defends your space` | 防御你的地盘 | 同盟 |
| `knows your voice` | 认识你（不会误伤） | 有接触的 |

**原版全部派系一览：**

| 派系 ID | 名称 | 对玩家 | 与强盗关系 |
|---------|------|--------|-----------|
| `your_followers` | 追随者 | 友好 | — |
| `old_guard` | 老守卫（联邦残余） | 中立偏好 | kill on sight |
| `free_merchants` | 自由商人 | 友好 | kill on sight |
| `hells_raiders` | 地狱突袭者（强盗） | 敌对 | 内部友好 |
| `slaves` | 奴隶 | 中立 | 被控制 |
| `wasteland_scavengers` | 荒野拾荒者 | 中立 | 无 |
| `valhallists` | 北欧教派 | 微友好 | kill on sight |
| `exodii` | Exodii（跨世界旅者） | 友好 | 无 |
| `robofac` | Hub 01（科技派） | 不信任 | 无 |
| `the_great_library` | 大图书馆 | 友好 | kill on sight |
| `gods_community` | 教会社区 | 友好 | kill on sight |
| `isherwood_family` | Isherwood 农家 | 友好 | kill on sight |
| `no_faction` | 无派系 | 中立 | — |
| `prisoners` | 囚犯 | 中立 | 同盟 |
| `amf` | 叛变者 | 极敌对 | — |

### 2.4 `behavior` —— NPC AI 行为树（★ 补充）

`npc_behavior.json` 定义了 NPC 的需求驱动行为：

```
npc_needs (sequential_until_done)
  ├── npc_homeostasis (fallback) ← 条件: npc_needs_warmth_badly
  │    ├── npc_wear_warmer_clothes
  │    └── npc_get_warm
  │         ├── npc_make_fire
  │         └── npc_take_shelter
  ├── npc_thirst (sequential) ← 条件: npc_needs_water_badly
  │    └── npc_drink_water
  └── npc_hunger (sequential) ← 条件: npc_needs_food_badly
       └── npc_eat_food
```

策略类型：
- `sequential_until_done`：依次执行直到一个成功即停
- `sequential`：依次全部执行
- `fallback`：依次尝试，前者失败则尝试后者

### 2.5 `trait_group` —— 特质分组

```json
{
  "type": "trait_group",
  "id": "BG_survival_story_EVACUEE",
  "subtype": "distribution",       ← "distribution" 选一个，"collection" 全选
  "traits": [
    { "group": "BG_survival_story_UNIVERSAL" },  ← 嵌套引用其他 trait_group
    { "trait": "BGSS_Evacuee_1" },               ← 引用单个 trait
    { "trait": "BGSS_Evacuee_2" },
    ...
  ]
}
```

**npc_class 中 traits 的三种引用方式：**
```json
// 方式 1：引用 trait_group（从池中随机选一个）
"traits": [ { "group": "BG_survival_story_EVACUEE" } ]

// 方式 2：直接指定 trait + 概率
"traits": [ [ "MARLOSS", 100 ], [ "MARLOSS_BLUE", 40 ] ]

// 方式 3：混合
"traits": [
  { "group": "BG_survival_story_SOLDIER" },
  { "group": "NPC_starting_traits" },
  { "group": "Appearance_demographics" }
]
```

### 2.3 技能分布类型

| 分布 | 语法示例 | 效果 |
|------|---------|------|
| `rng` | `{ "rng": [1, 4] }` | 1~4 均匀随机 |
| `one_in` | `{ "one_in": 3 }` | 1/3 概率得 1，否则 0 |
| `dice` | `{ "dice": [4, 2] }` | 4d2（4~8） |
| `sum` | `{ "sum": [{ "dice": [3,2] }, { "constant": -3 }] }` | 各部分相加 |
| `constant` | `{ "constant": 3 }` | 固定值 |
| `mul` | `{ "mul": [{ "one_in": 3 }, { "sum": [ ... ] }] }` | 相乘 |

**实际案例 —— NC_SOLDIER 的技能定义：**
```json
"skills": [
  { "skill": "ALL",  "level": { "sum": [{ "dice": [3, 2] }, { "constant": -3 }] } },
  // ↑ 所有未指定的技能 = 3d2-3（即 0~3）

  { "skill": "dodge",  "bonus": { "rng": [1, 2] } },
  { "skill": "melee",  "bonus": { "rng": [1, 2] } },
  { "skill": "rifle",  "bonus": { "rng": [3, 5] } },
  { "skill": "gun",    "bonus": { "rng": [2, 4] } }
]
// ↑ ALL 是基础值，各技能的 bonus 是额外加值
```

### 2.4 `item_group` —— NPC 装备池

NPC 的装备通过 `item_group` 定义，按部位拆分成多个池：

**示例 —— NC_SOLDIER 的 pants 池：**
```json
{
  "type": "item_group",
  "id": "NC_SOLDIER_pants",
  "subtype": "distribution",                     ← 从中选一件
  "entries": [
    { "item": "pants_army", "prob": 80 },
    { "item": "winter_pants_army", "prob": 20 }
  ]
}
```

**两种 subtype：**

| subtype | 行为 | 适用场景 |
|---------|------|----------|
| `distribution` | 按概率**抽一件** | 上衣、裤子、鞋、手套（穿一件） |
| `collection` | **全部产生**（有概率则按概率） | 内衣、袜子（穿一套） |

**worn_override 的工作方式：**
```
npc_class.worn_override = "NC_SOLDIER_worn"
  ↓
item_group "NC_SOLDIER_worn" (type: collection)
  ├── { "group": "NC_SOLDIER_pants" }     ← 从 pants 池抽一件
  ├── { "group": "NC_SOLDIER_shirt" }     ← 从 shirt 池抽一件
  ├── { "group": "NC_SOLDIER_gloves" }    ← 从 gloves 池抽一件
  ├── { "group": "NC_SOLDIER_coat" }      ← ...
  ├── { "group": "NC_SOLDIER_shoes" }
  ├── { "group": "NC_SOLDIER_hat" }
  ├── { "group": "NC_SOLDIER_vest" }
  └── { "group": "npc_underwear_top_male" }  ← 引用 items_generic.json 中的通用内衣池
```

---

## 三、NPC 完整生成管线（修订）

### 3.1 三层架构

```
┌─────────────────────────────────────────────────────────────────┐
│ 第 1 层：npc_class（职业模板）                                    │
│   定义：技能/属性/特质/装备池/性格                                  │
│   文件：classes.json 或 NC_*.json                                 │
├─────────────────────────────────────────────────────────────────┤
│ 第 2 层：npc（实例定义）                                          │
│   绑定：npc_class + faction + attitude + mission + chat           │
│   文件：npc.json 或各子目录下的 npc.json                           │
├─────────────────────────────────────────────────────────────────┤
│ 第 3 层：mapgen / EOC（放置到世界中）                              │
│   方式：mapgen 的 place_npcs 或 EOC 动态生成                      │
│   文件：mapgen/*.json 或 encounters/*.json                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 单个 NPC 的属性生成流

```
npc_class 定义
    │
    ├→ traits → trait_group 池 → 随机抽取一个背景故事 trait (BGSS_*)
    │          └→ 背景故事 trait 是 talk_topic（决定了 NPC 的对话内容）
    │          └→ NPC_starting_traits → trait_group → 随机起始特质
    │          └→ Appearance_demographics → 随机外观
    │
    ├→ skills → ALL 设置全技能基线
    │        └→ 各技能 bonus 叠加在基线上
    │        └→ 所有数值通过 rng/dice/one_in/constant 随机化
    │
    ├→ stats → 基础属性 + bonus_str/dex/int/per 偏移
    │
    ├→ equipment → worn_override → item_group (collection)
    │           │    ├→ pants 池 (distribution) → 随机抽一条裤子
    │           │    ├→ shirt 池 (distribution) → 随机抽一件上衣
    │           │    ├→ coat 池  (distribution) → 随机抽外套（可能为 null=没穿）
    │           │    └→ ...
    │           └→ weapon_override → 武器 item_group → 随机武器
    │
    └→ personality → bonus_aggression/bravery/collector/altruism 偏移
```

### 3.3 NPC 在世界中的行为决定流

```
npc 实例
    │
    ├→ faction → factions.json 中的关系矩阵
    │           └→ 与玩家派系 "kill on sight" = true → 见面开打
    │           └→ "knows your voice" → 不会误伤
    │
    ├→ attitude → 初始态度（可被对话 effect 动态修改）
    │           └→ 0=中立, 10=敌对, "hostile" effect 可运行时切换
    │
    ├→ mission → 行为模式
    │          └→ 8=巡逻 → 在据点范围内移动
    │          └→ 7=驻守 → 待在原地
    │          └→ 3=商人 → 待在原地+开启交易
    │
    └→ chat → 对话入口
            └→ talk_topic → responses → effect（可触发 hostile、招募等）
```

### 3.4 随机遭遇系统（EOC 驱动）

CDDA 的随机遭遇不通过固定 spawn，而是通过 **EOC（Effect on Condition）** 在运行时注入：

```json
{
  "type": "effect_on_condition",
  "id": "EOC_RandEnc_Roadstop_add",
  "recurrence": 1800,             // 每 1800 秒检查一次
  "global": true,
  "effect": [
    { "set_condition": "random_enc_condition",
      "condition": { "and": [ { "not": { "is_season": "winter" } }, "is_day" ] } },
    { "run_eoc_with": "EOC_RandEnc",
      "variables": {
        "omt": "roadstop_a",      // 目标 overmap terrain
        "map_update": "nest_RandEnc_roadstop_a_add",   // 添加 NPC 的 mapgen
        "map_removal": "nest_RandEnc_roadstop_a_remove", // 移除 NPC 的 mapgen
        "chance": "10",           // 10% 概率触发
        "days_till_spawn": "7"    // 存活 7 天后消失
      }
    }
  ]
}
```

对应的 mapgen update 使用 `place_npcs` 放置 NPC：
```json
{
  "type": "mapgen",
  "update_mapgen_id": "nest_RandEnc_roadstop_a_add",
  "object": {
    "place_npcs": [
      { "class": "FM_caravan_merchant_random", "x": 5, "y": 4 },
      { "class": "FM_caravan_guard_A", "x": 4, "y": 1 }
    ]
  }
}
```

---

## 四、Hell's Raiders —— 原版强盗派系实例分析（★ 补充）

CDDA 原版的唯一强盗派系 `hells_raiders` 是我们中世纪强盗设计的直接对标物：

### 4.1 组织结构

| npc 实例 ID | class | 角色 | attitude | mission |
|-------------|-------|------|----------|---------|
| `thug` | NC_THUG | 近战打手 | 0 | 8（巡逻） |
| `bandit` | NC_SCAVENGER | 枪械打手 | 0 | 8（巡逻） |
| `hells_raiders_boss` | NC_BANDIT_LEADER | 头目 | 0 | 8（巡逻） |
| `hells_raiders_assassin` | NC_BOUNTY_HUNTER | 刺客 | 10（敌对） | 0（无） |
| `bandit_trader` | NC_BANDIT_TRADER | 黑市商人 | 0 | 3（商人） |
| `bandit_quartermaster` | NC_BANDIT_QUARTERMASTER | 军需官 | 0 | 3（商人） |
| `bandit_mechanic` | NC_SCAVENGER | 修车匠 | 0 | 8（巡逻） |

**关键发现**：
- 普通打手 attitude=0（中立），**不是默认敌对**——靠 **faction 的 `"kill on sight": true`** 让他们对玩家开打
- 刺客 attitude=10 是唯一主动敌对的，因为它是 EOC 事件触发的追杀者
- 同一个 NC_SCAVENGER class 被 `bandit` 和 `bandit_mechanic` 复用

### 4.2 NC_THUG class 详解（打手模板）

```json
{
  "id": "NC_THUG",
  "bonus_str": { "rng": [2, 4] },
  "bonus_dex": { "rng": [0, 2] },
  "bonus_aggression": { "rng": [1, 6] },
  "bonus_bravery": { "rng": [0, 5] },
  "traits": [
    { "group": "BG_survival_story_CRIMINAL" },
    { "group": "NPC_starting_traits" },
    { "group": "Appearance_demographics" }
  ],
  "skills": [
    { "skill": "ALL", "level": { "sum": [{ "dice": [3, 2] }, { "constant": -4 }] } },
    { "skill": "dodge", "bonus": { "rng": [1, 3] } },
    { "skill": "melee", "bonus": { "rng": [2, 4] } },
    { "skill": "unarmed", "bonus": { "rng": [1, 3] } },
    { "skill": "bashing", "bonus": { "rng": [1, 5] } },
    { "skill": "stabbing", "bonus": { "rng": [1, 5] } },
    { "skill": "cutting", "bonus": { "rng": [1, 5] } }
  ]
}
```

**武器池**（NC_THUG_bashing）：sledge (10), rebar_spear (20), bat (20), crowbar (20), q_staff (20), bwirebat (20), bat_metal (20)

### 4.3 NC_BANDIT_LEADER class（头目模板）

```json
{
  "id": "NC_BANDIT_LEADER",
  "bonus_str": { "rng": [3, 5] },       // 比打手更强
  "bonus_dex": { "rng": [1, 3] },
  "bonus_int": { "rng": [0, 2] },       // 有点脑子
  "skills": [
    { "skill": "ALL", "level": { "sum": [{ "dice": [3, 2] }, { "constant": -4 }] } },
    { "skill": "dodge", "bonus": { "rng": [2, 4] } },
    { "skill": "melee", "bonus": { "rng": [3, 5] } },     // 明显更高
    { "skill": "bashing", "bonus": { "rng": [2, 6] } },
    { "skill": "stabbing", "bonus": { "rng": [2, 6] } },
    { "skill": "cutting", "bonus": { "rng": [2, 6] } }
  ],
  "traits": [
    { "group": "BG_survival_story_CRIMINAL" },
    { "trait": "NO_BASH" },              // 不破坏家具
    { "trait": "RETURN_TO_START_POS" },  // 回原位
    { "trait": "IGNORE_SOUND" }          // 不被声音引走
  ]
}
```

### 4.4 敌对状态的两种实现方式

| 方式 | 机制 | 典型用例 |
|------|------|----------|
| **派系敌对** | faction.relations 中 `"kill on sight": true` | hells_raiders 对 your_followers |
| **对话触发** | talk_topic response 中 `"effect": "hostile"` | holdouts 牛仔 |

对话驱动敌对示例：
```json
{ "text": "I'd like to see you try.", "topic": "TALK_DONE", "effect": "hostile" }
```

---

## 五、对我们中世纪模组的关键启示（修订）

| 启示 | 说明 |
|------|------|
| **技能不写死是内置机制** | CDDA 的 `npc_class` 原生支持 rng/dice/one_in 分布，我们 008 的设计直接对应 |
| **装备 = item_group 池** | 不需要为每个 bandit 写死装备。每个 npc_class 引用一个 worn group + weapon group，从池中抽 |
| **部位拆分粒度** | CDDA 的 worn group 按 pants/shirt/gloves/coat/shoes/hat/vest 拆成独立 item_group，中世纪按 gambeson/mail/plate/legs/helmet 拆更合适 |
| **`null` 表示"没穿"** | 给穷人池（bandit_weak）大量 null 权重，模拟"有人没头盔、有人没鞋"的穷感 |
| **trait_group 可用于出身** | 可以定义 `BG_bandit_story` 的 trait_group，让每个强盗随机一种出身（逃兵/农民/被流放者），决定对话和态度 |
| **装备池可以嵌套** | `NC_SOLDIER_vest` 池引用了 `military_ballistic_vest` group → 中世纪的 bandit_medium_worn 可以嵌套引用通用的 `mail_parts` 池 |
| **common_spawn_weight** | 控制随机生成概率，bandit_weak: 3.0, bandit_leader: 0.3 |
| ★ **需要 `npc` 实例层** | 光有 npc_class 不够，还需定义 npc 实例来绑定 faction/attitude/mission |
| ★ **需要 `faction` 定义** | 中世纪强盗需要自己的 faction，设定 kill on sight 关系 |
| ★ **敌对可以是动态的** | 不一定所有强盗都 kill on sight，可以用对话触发（"交钱放行"失败→hostile） |
| ★ **EOC 可驱动遭遇** | 随机遭遇/巡逻强盗可以用 EOC 在运行时注入，不需要写死在地图上 |
| ★ **行为 trait 控制 AI** | `RETURN_TO_START_POS`（回原位）、`IGNORE_SOUND`（不被引走）、`NO_BASH`（不破坏） |

---

## 六、文件清单速查（修订）

| 需要修改/创建的文件类型 | CDDA 对应 | 中世纪用途 |
|------------------------|----------|-----------|
| `npc_class` JSON | `classes.json` | 定义 npc_class_bandit_weak 等 |
| ★ `npc` 实例 JSON | `hells_raiders/npc.json` | 定义 bandit_weak_instance 绑定 faction |
| ★ `faction` JSON | `factions.json` | 定义中世纪强盗派系 + 关系矩阵 |
| `item_group`（独立文件） | `NC_SOLDIER.json` | 定义 bandit_weak_worn 等装备池 |
| `trait_group` JSON | `BG_trait_groups.json` | 定义 bandit_story 出身池 |
| `talk_topic` JSON | `Backgrounds/soldier_1.json` | 定义每个强盗的随机对话 |
| `items_generic` | `items_generic.json` | 通用中世纪内衣/平民衣物池 |
| ★ `effect_on_condition` | `encounters/randenc_*.json` | 随机遭遇触发逻辑 |
| ★ `mapgen update` | 同上 | 在地图上放置/移除 NPC |
