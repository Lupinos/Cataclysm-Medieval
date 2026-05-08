# 策划案 008：野怪 NPC 体系（一）—— 强盗

## 设计前提

**所有野外敌人以 NPC 规格存在**，以 CDDA `npc_class` JSON 格式定义。装备通过 `item_group` 池随机分配，技能通过 `rng` / `one_in` / `dice` 分布定义，而非固定值。

**调查来源**：CDDA 的 `npc_class` 系统支持以下技能随机方式：

| 分布类型 | 语法 | 效果 |
|----------|------|------|
| 范围随机 | `"rng": [min, max]` | 在范围内均匀随机 |
| 概率获得 | `"one_in": N` | 1/N 几率获得该技能 |
| 骰子 | `"dice": [num, sides]` | NdS 掷骰 |
| 叠加 | `"sum": [a, b, ...]` | 多个分布相加 |
| 固定 | `"constant": X` | 定值 |

装备映射：`worn_override` / `weapon_override` / `carry_override` 各引用一个 `item_group` ID，系统每次 spawn 时从池中随机抽取。

---

## 一、装备等级原则——"强盗应该比你穷"

**核心问题**：原 008 第一版中 `bandit_medium` 就穿了 mail hauberk + arming sword——这已经是步兵级别的配置了。在秩序崩溃的世界里，大批量出现这种装备是不合理的。

### 装备稀缺性阶梯

| 装备 | 拥有者 | 理由 |
|------|--------|------|
| 破烂衣物、草叉、棍棒 | 大多数强盗 | 农民转业，捡到什么用什么 |
| Gambeson | 少数强一点的 | 从民兵尸体上扒的 |
| 锁子甲部件（袖子/护颈/半身） | 少数幸运者 | 完整的 hauberk 太贵，但捡到局部是可能的 |
| 完整的 mail hauberk | **几乎不应该出现** | 一套锁子甲够一个村子吃一年 |
| Brigandine / 板甲部件 | 仅头目 | 从骑士/军官尸体上抢的，数量极其有限 |
| 好剑（arming sword 以上） | 仅头目 | 剑比斧贵得多，强盗没有铁匠定制 |

### 贫富梯度

```
bandit_weak ────── 穿得比你还惨。他手里的"武器"你在田里就能找到。
bandit_medium ──── 有一两件像样的东西，但不成套。
bandit_strong ──── 有半套好装备，很可能杀过正经士兵。
bandit_leader ──── 才配得上 mail + 好剑。见面你就知道他是老大。
```

---

## 二、技能分布设计（取代固定值）

> 以下所有技能值使用 `rng` / `one_in` / `dice` 分布，不写死具体数字。

### 2.1 npc_class_bandit_weak

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | `"rng": [0, 1]` | 有人用过刀，有人没碰过 |
| Bashing | `"rng": [0, 2]` | 棍子和连枷是农民工具，部分人很熟 |
| Piercing | `"rng": [0, 1]` | — |
| Dodge | `constant: 0` | 不会躲 |
| Throwing | `"one_in": 3` → 得 1 否则 0 | 1/3 概率会扔石头 |
| Survival | `"rng": [0, 2]` | 农民出身有野外常识 |
| 特殊 | — | — |

### 2.2 npc_class_bandit_medium

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | `"rng": [1, 2]` | 至少用过刀 |
| Bashing | `"rng": [1, 2]` | — |
| Piercing | `"rng": [0, 2]` | 可能用过矛 |
| Dodge | `"rng": [0, 1]` | 少数人有战场经验 |
| Throwing | `"rng": [0, 1]` | — |
| 特殊 | — | — |

### 2.3 npc_class_bandit_strong

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | `"rng": [2, 3]` | 正经打过仗 |
| Bashing | `"rng": [2, 3]` | — |
| Piercing | `"rng": [1, 2]` | — |
| Dodge | `"rng": [1, 2]` | 知道怎么活下来的人 |
| 特殊 | 概率获得 `"one_in": 4` → 退伍士兵特质 | 额外 +1 Cutting/Bashing |

### 2.4 npc_class_bandit_archer

| 技能 | 分布 | 说明 |
|------|------|------|
| Archery | `"rng": [1, 3]` | 从"会拉弦"到"偷猎老手"都有 |
| Cutting | `"rng": [0, 1]` | 近战很弱 |
| Dodge | `"rng": [0, 1]` | — |
| 特殊 | 箭矢数量 `"rng": [5, 20]` | 运气好捡到多 |

### 2.5 npc_class_bandit_marksman

| 技能 | 分布 | 说明 |
|------|------|------|
| Archery | `"rng": [3, 5]` | 逃兵弓箭手或职业偷猎者 |
| Cutting | `"rng": [1, 2]` | 有备用的近战能力 |
| Dodge | `"rng": [1, 2]` | — |
| 特质 | 概率 `"one_in": 3` → 潜行 | 埋伏型 |
| 箭矢 | `"rng": [8, 20]` | 不多但每箭都可能致命 |

### 2.6 npc_class_bandit_leader

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | `"rng": [2, 4]` | 比手下强是活下来的前提 |
| Bashing | `"rng": [2, 3]` | — |
| Piercing | `"rng": [1, 3]` | — |
| Dodge | `"rng": [1, 2]` | — |
| Speech | `"rng": [1, 2]` | 能镇住手下叫"说服力" |
| 独有 | 低概率 `"one_in": 10` → Literacy 1 | 极少数头目能识字 |

---

## 三、装备组（item_group）设计

装备不写死在 NPC 上，而是挂载 item_group ID。每次 spawn 从池中按 weight 随机抽取。

### 3.1 bandit_weak_worn（盔甲衣物池）

```
patched_gambeson (wt: 5)       ← 捡来的旧 gambeson
rough_wool_tunic (wt: 15)      ← 农民标配，几乎不防
linen_shirt (wt: 10)           ← 可能连外衣都没有
torn_wool_cloak (wt: 5)        ← 破斗篷
felt_hat (wt: 5)               ← 有人有帽子
no_helmet (wt: 60)             ← 大多数人没头盔
```

### 3.2 bandit_weak_weapon（武器池）

```
grain_flail (wt: 10)           ← 打谷连枷
wood_axe (wt: 8)               ← 伐木斧
club (wt: 12)                  ← 随手捡的棍子
pitchfork (wt: 5)              ← 干草叉
sling (wt: 3)                  ← 投石索
hand_axe (wt: 3)               ← 手斧（少，因为手斧比棍子"贵"）
rock_pile (wt: 8)              ← 石头也行，别嫌弃
```

### 3.3 bandit_medium_worn（盔甲衣物池）

```
gambeson (wt: 10)              ← 捡来的正经 gambeson（可能破）
leather_jerkin (wt: 8)         ← 硬皮短衣
mail_coif (wt: 2)              ← 捡漏的锁子甲头巾（稀有）
mail_sleeves_partial (wt: 1)   ← 单只锁子甲袖子（极稀有，不成套）
kettle_hat (wt: 3)             ← 锅盔
leather_cap (wt: 5)            ← 皮盔
wool_tunic (wt: 15)            ← 很多人还是穿布
```

> **注意**：不包含完整的 mail hauberk。一件完整锁子甲对一个强盗来说过于奢侈。锁子甲部件（头巾、袖子、半身）是可能出现的，但也是稀有的。

### 3.4 bandit_medium_weapon（武器池）

```
falchion (wt: 5)               ← 平民弯刃刀
hand_axe (wt: 8)               ← 手斧
spear (wt: 10)                 ← 最便宜的军用武器
arming_sword (wt: 2)           ← 捡来的骑士剑（稀有）
mace (wt: 3)                   ← 捡来的权杖
club_spiked (wt: 5)            ← 打上钉子的木棍
seax (wt: 7)                   ← 长战斗刀
```

### 3.5 bandit_strong_worn（盔甲衣物池）

```
gambeson (wt: 15)              ← 普遍有
mail_coif (wt: 5)              ← 锁子甲头巾
brigandine_partial (wt: 3)     ← 捡来的 brigandine 半身——奢侈了
mail_vest (wt: 2)              ← 锁子甲背心（不是全长 hauberk！）
plate_gauntlets (wt: 1)        ← 捡来的铁手套
bascinet_no_visor (wt: 3)      ← 无面罩尖顶盔
kettle_hat (wt: 5)             ← 锅盔（有人还是戴这个）
```

### 3.6 bandit_strong_weapon（武器池）

```
battle_axe (wt: 5)             ← 正经战斧
arming_sword (wt: 5)           ← 骑士剑
war_hammer (wt: 3)             ← 战锤
billhook (wt: 4)               ← 钩镰戟（从民兵尸体上扒的）
longsword (wt: 2)              ← 长剑（很稀有）
morning_star (wt: 3)           ← 钉头锤
```

### 3.7 bandit_archer_worn

```
gambeson_light (wt: 10)        ← 轻量 gambeson
leather_jerkin (wt: 8)         ← 硬皮短衣
wool_tunic (wt: 12)            ← 还是布
coif (wt: 5)                   ← 布头巾
```

### 3.8 bandit_archer_weapon

```
shortbow (wt: 10)              ← 短弓
light_crossbow (wt: 5)         ← 轻弩
sling (wt: 3)                  ← 更穷的弓手
```

### 3.9 bandit_marksman_weapon

```
longbow (wt: 5)                ← 长弓（逃兵弓手）
heavy_crossbow (wt: 5)         ← 重弩（逃兵弩手）
composite_bow (wt: 2)          ← 复合弓（东欧/东方背景）
```

### 3.10 bandit_leader_worn

```
bandit_strong_worn 全部 (wt: 10) ← 等同于 strong 或更好
mail_hauberk (wt: 3)           ← 终于出现了！但仍是稀有
brigandine_full (wt: 2)        ← 完整 brigandine
bascinet_visor (wt: 3)         ← 带面罩的尖顶盔
plate_greaves (wt: 1)          ← 胫甲
```

### 3.11 bandit_leader_weapon

```
longsword (wt: 3)              ← 定制长剑
arming_sword (wt: 4)           ← 配盾组合
pollaxe (wt: 2)                ← 骑士戟（扛着就显身份）
war_hammer (wt: 3)             ← 战锤
estoc (wt: 1)                  ← 穿刺剑（极稀有）
```

---

## 四、兽人强盗（技能分布）

兽人属性偏移不变（Str+4, Int-3, 大型, HP+30%），但技能也用分布替代固定值：

### npc_class_orc_bandit_warrior

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [2, 4]` |
| Cutting | `"rng": [1, 3]` |
| Dodge | `constant: 0` |
| Throwing | `"rng": [1, 2]` |

### npc_class_orc_bandit_archer

| 技能 | 分布 |
|------|------|
| Archery | `"rng": [1, 2]`（力量够、精度低） |
| Bashing | `"rng": [1, 2]`（近战保底） |

### npc_class_orc_bandit_chief

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [3, 5]` |
| Cutting | `"rng": [2, 4]` |
| Dodge | `"rng": [0, 1]` |

兽人装备池同理，从对应 item_group 抽取，但偏重重型武器和粗糙拼装盔甲。

---

## 五、哥布林强盗（技能分布）

哥布林属性偏移（Str-4, Dex+4, 小型, HP-40%, 速度+10%），技能分布：

### npc_class_goblin_cutthroat

| 技能 | 分布 |
|------|------|
| Cutting | `"rng": [1, 2]` |
| Piercing | `"rng": [1, 2]` |
| Dodge | `"rng": [2, 4]`（小型 + 敏捷） |

### npc_class_goblin_slinger

| 技能 | 分布 |
|------|------|
| Throwing | `"rng": [2, 3]` |
| Dodge | `"rng": [2, 4]` |

---

### 7.3 搜刮预期（更新后）

| 强盗 | 你大概能拿到什么 |
|------|------------------|
| weak | 草叉、破布、半块面包。几乎不值得打。 |
| medium | 也许一件 gambeson 或手斧，值一点点钱。 |
| strong | 可能有 brigandine 部件或好武器。这是 loot 的甜点区。 |
| leader | 才配出 mail、好剑、百枚硬币。真正的 reward。 |

---

## 八、派系与实例层设计（★ 新增章节）

> 基于 json-004 补充调研的发现：CDDA 的 NPC 部署是三层结构（npc_class → npc 实例 → mapgen 放置），且敌对关系由 faction 关系矩阵驱动。原版 hells_raiders 就是这么做的。

### 8.1 中世纪强盗派系定义

```json
{
    "type": "faction",
    "id": "bandits",
    "name": "Bandits",
    "likes_u": -30,
    "respects_u": -30,
    "size": 200,
    "power": 30,
    "relations": {
        "bandits": {
            "kill on sight": false,
            "watch your back": true,
            "share my stuff": true,
            "guard your stuff": true,
            "lets you in": true,
            "defends your space": true,
            "knows your voice": true
        },
        "your_followers": { "kill on sight": true },
        "village_militia": { "kill on sight": true },
        "merchant_guild": { "kill on sight": true },
        "royal_guard": { "kill on sight": true }
    },
    "description": "Desperate men who prey upon travelers and villages."
}
```

### 8.2 NPC 实例定义（npc 层）

| npc ID | class | attitude | mission | chat | 说明 |
|--------|-------|----------|---------|------|------|
| `bandit_grunt` | npc_class_bandit_weak | 0 | 8 | TALK_DONE | 杂鱼巡逻，靠 faction kill on sight 开打 |
| `bandit_veteran` | npc_class_bandit_medium | 0 | 8 | TALK_DONE | 老手巡逻 |
| `bandit_elite` | npc_class_bandit_strong | 0 | 8 | TALK_DONE | 精锐 |
| `bandit_archer_patrol` | npc_class_bandit_archer | 0 | 8 | TALK_DONE | 弓手巡逻 |
| `bandit_marksman_ambush` | npc_class_bandit_marksman | 10 | 0 | TALK_DONE | 伏击手（主动敌对） |
| `bandit_chief` | npc_class_bandit_leader | 0 | 7 | TALK_BANDIT_CHIEF | 头目驻守，**可对话** |
| `bandit_roadblock` | npc_class_bandit_medium | 0 | 1 | TALK_BANDIT_TOLL | 拦路收费，**对话驱动敌对** |

### 8.3 对话驱动的交互型强盗

不是所有强盗都见面就打。**路匪拦路收费**是经典场景：

```
玩家遇到 bandit_roadblock（attitude=0, mission=1 拦截）
    │
    ├→ "交 50 银币就让你过" → 玩家付钱 → 放行（attitude 不变）
    ├→ "我是 XXX 领主的人" → 检查 speech 技能 / 声望
    │    ├→ 成功 → 放行
    │    └→ 失败 → "少骗我" → hostile
    ├→ "我什么都没有" → "那留下你的命吧" → hostile
    └→ "你最好让开" → hostile
```

JSON 实现（简化）：
```json
{
    "type": "talk_topic",
    "id": "TALK_BANDIT_TOLL",
    "dynamic_line": "Hold! You want to pass, you pay. 50 silver.",
    "responses": [
        { "text": "[Pay 50 silver]", "topic": "TALK_BANDIT_PAID",
            "condition": { "u_has_items": { "item": "silver_coin", "count": 50 } },
            "effect": { "u_sell_item": "silver_coin", "count": 50 } },
        { "text": "I serve Lord Aldric.", "topic": "TALK_BANDIT_BLUFF",
            "condition": { "u_has_skill": { "skill": "speech", "level": 3 } } },
        { "text": "Move aside or die.", "topic": "TALK_DONE", "effect": "hostile" },
        { "text": "[Leave quietly]", "topic": "TALK_DONE" }
    ]
}
```

### 8.4 NPC 行为 trait 规划

| trait | 用于 | 效果 |
|-------|------|------|
| `RETURN_TO_START_POS` | 头目/商人 | 战斗后回到据点中心 |
| `IGNORE_SOUND` | 头目 | 不被远处声音引走 |
| `NO_BASH` | 所有据点 NPC | 不破坏自己的营地家具 |
| （自定义）`AMBUSH_BEHAVIOR` | 伏击弓手 | 不暴露位置直到目标进入射程 |

### 8.5 兽人/哥布林强盗的派系设计

```json
// 兽人强盗 — 独立派系，与人类强盗也敌对
{
    "type": "faction",
    "id": "orc_raiders",
    "relations": {
        "your_followers": { "kill on sight": true },
        "bandits": { "kill on sight": true },       // 兽人和人类强盗也互相打
        "village_militia": { "kill on sight": true }
    }
}

// 哥布林 — 可能有条件性非敌对（贿赂/恐吓可解除）
{
    "type": "faction",
    "id": "goblin_bands",
    "likes_u": -15,
    "relations": {
        "your_followers": { "kill on sight": true },
        "bandits": { "knows your voice": true },    // 哥布林和人类强盗不打不相识
        "orc_raiders": { "kill on sight": false, "knows your voice": true }
    }
}
```

---

## 九、Spawn Group 与遭遇设计（修订）

### 9.1 据点 Spawn（mapgen 放置）

在据点 mapgen 中直接 place_npcs：
```json
"place_npcs": [
{ "class": "bandit_chief", "x": 12, "y": 12 },
{ "class": "bandit_grunt", "x": 8, "y": 10 },
{ "class": "bandit_grunt", "x": 14, "y": 10 },
{ "class": "bandit_archer_patrol", "x": 10, "y": 5 }
]
```

### 9.2 随机路匪遭遇（EOC 驱动）

```json
{
    "type": "effect_on_condition",
    "id": "EOC_bandit_roadblock_spawn",
    "recurrence": 3600,
    "global": true,
    "effect": [
        { "set_condition": "road_bandit_condition",
            "condition": { "and": [ "is_day", { "days_since_cataclysm": 14 } ] } },
        { "run_eoc_with": "EOC_RandEnc",
            "variables": {
                "omt": "road_crossroads",
                "map_update": "nest_bandit_roadblock_add",
                "chance": "15",
                "days_till_spawn": "5"
            }
        }
    ]
}
```

### 9.3 Group 权重（不变，略修订）

| Group | 主要变化 |
|-------|---------|
| GROUP_BANDIT_CAMP_HUMAN | bandit_weak wt 上调（更多杂鱼），leader wt 下调 |
| GROUP_BANDIT_STRONGHOLD | bandit_strong 上限调低，装备靠随机而不是"保证出好货" |
| GROUP_BANDIT_ROADBLOCK | 1-3 个 medium + 概率 1 个 archer，用于动态遭遇 |

---

## 十、设计注记

### 10.1 为什么不写死技能值

CDDA 的 `npc_class` 原生支持 `rng` / `one_in` / `dice`。写死技能值有两个问题：

1. **同质化**：每个 bandit_medium 都一样，玩家第一次遇到的是老手，第 20 次遇到的还是同一个老手
2. **失去惊喜**：分布意味着你偶尔会遇到一个技能 roll 到 3 的 bandit_weak（"这农民怎么这么能打？"），或者 roll 到 1 的 bandit_strong（"穿着好甲但其实是纸老虎"）

### 10.2 装备池 = 故事

`item_group` 的 weight 本身就是叙事：

- `arming_sword` 在 bandit_weak 池里 weight 0——不存在。农民没有剑。
- `arming_sword` 在 bandit_medium 池里 weight 2——捡来的，稀有。
- `mail_hauberk` 只在 bandit_leader 池里 weight 3——你可能杀了 10 个头目都见不到一件。见到的时候你该兴奋。

### 10.3 搜刮预期

| 强盗 | 你大概能拿到什么 |
|------|------------------|
| weak | 草叉、破布、半块面包。几乎不值得打。 |
| medium | 也许一件 gambeson 或手斧，值一点点钱。 |
| strong | 可能有 brigandine 部件或好武器。这是 loot 的甜点区。 |
| leader | 才配出 mail、好剑、百枚硬币。真正的 reward。 |

### 10.4 派系让世界活起来

CDDA 的经验告诉我们：
- **不是所有敌人都见面就打**。路匪可以先收费再动手，这比无脑 aggro 有趣得多。
- **强盗内部有社会结构**。商人（不打你但卖黑货）、军需官、头目——这让据点不只是刷怪点。
- **不同种族的强盗互相打**。兽人和人类强盗 kill on sight，意味着玩家可以利用他们内斗。

---

> 008 文档修订记录：
> - v1: 初始版本
> - v2: 装备降级 + 技能改为分布
> - v3（本次）：补充三层架构（npc_class → npc 实例 → mapgen）、faction 关系系统、对话驱动敌对、EOC 随机遭遇、行为 trait、多种族派系关系
