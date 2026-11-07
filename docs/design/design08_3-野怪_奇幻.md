# 策划案 008_3：野怪体系（三）—— 奇幻生物

> 分层：**人形 → NPC 系统**（需装备/技能分布/派系），**巨怪/龙 → Monster 系统**（需 harvest/special_attacks）。

---

## 一、龙族（Monster 系统）

### 1. 双足飞龙 Wyvern

| 字段 | 值 |
|------|-----|
| hp | 180 |
| speed | 150 |
| melee_skill | 6 |
| melee_dice | 3 |
| melee_dice_sides | 8 |
| melee_damage | `[{ "type": "cut", "amount": 10 }, { "type": "pierce", "amount": 6 }]` |
| dodge | 3 |
| armor_bash | 4 |
| armor_cut | 6 |
| aggression | 20 |
| morale | 100 |
| anger_triggers | `["PLAYER_CLOSE", "HURT"]` |
| special_attacks | `[{ "type": "bite", "cooldown": 8, "effects": "venom_wyvern" }]` |

> 毒刺（bite）附加 `venom_wyvern`：疼痛+肌肉麻痹。伤害：3d8 bash + 10 cut + 6 pierce。

**生态**：高山峭壁巢穴。昼行。独居。半径 5-10km 领地。

**harvest**：`harvest_wyvern`
- flesh, blood, bone: 标准龙类比例
- skin: `scale_wyvern` (0.06)
- dissect: `wyvern_venom_gland`, `wyvern_wing_membrane`, `wyvern_fang`

---

### 2. 地龙 Drake

| 字段 | 值 |
|------|-----|
| hp | 250 |
| speed | 120 |
| melee_skill | 5 |
| melee_dice | 4 |
| melee_dice_sides | 8 |
| melee_damage | `[{ "type": "cut", "amount": 8 }]` |
| dodge | 1 |
| armor_bash | 6 |
| armor_cut | 8 |
| aggression | 10 |
| morale | 100 |
| anger_triggers | `["PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "bite", "cooldown": 6 }]` |

> 4 腿无翼。4d8 bash + 8 cut。伏击型——`aggression: 10` 不主动寻敌但靠近就咬。

**生态**：干燥荒地/峡谷/火山边缘。晨昏活动。独居。

**harvest**：`harvest_drake`
- flesh, blood, bone
- skin: `scale_drake` (0.07)
- dissect: `drake_fang`, `drake_heart`

---

## 二、合体兽（Monster 系统）

### 3. 狮鹫 Griffin

| 字段 | 值 |
|------|-----|
| hp | 150 |
| speed | 160 |
| melee_skill | 6 |
| melee_dice | 3 |
| melee_dice_sides | 6 |
| melee_damage | `[{ "type": "cut", "amount": 10 }]` |
| dodge | 4 |
| armor_bash | 3 |
| armor_cut | 4 |
| aggression | 15 |
| morale | 90 |
| anger_triggers | `["PLAYER_CLOSE", "PLAYER_WEAK"]` |
| special_attacks | `[{ "type": "leap", "cooldown": 5 }]` |

> 俯冲（leap）首击 ×2。会优先攻击玩家的马/坐骑。

**生态**：高山悬崖。昼行。成对终身。可偷蛋驯养幼崽。

**harvest**：`harvest_griffin`
- flesh (0.25), bone (0.10)
- offal: `feather_griffin` (0.02)
- dissect: `griffin_claw`, `griffin_egg`（巢穴 loot 概率出，不是 dissect 产物）

---

### 4. 蝎尾狮 Manticore

| 字段 | 值 |
|------|-----|
| hp | 160 |
| speed | 140 |
| melee_skill | 6 |
| melee_dice | 3 |
| melee_dice_sides | 6 |
| melee_damage | `[{ "type": "cut", "amount": 8 }, { "type": "pierce", "amount": 4 }]` |
| dodge | 3 |
| armor_bash | 3 |
| armor_cut | 4 |
| aggression | 25 |
| morale | 100 |
| anger_triggers | `["PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "bite", "cooldown": 12, "range": 8, "effects": "venom_manticore", "damage": [{ "type": "pierce", "amount": 6 }] }]` |

> 尾射毒刺 8 格射程，附加 `venom_manticore`（疼痛+麻痹+减速）

**生态**：干旱荒地/峡谷。晨昏。独居。会用毒刺在岩石上刻领地标记。

**harvest**：`harvest_manticore`
- flesh, bone
- skin: `pelt_manticore` (0.02)
- dissect: `manticore_stinger`, `manticore_mane`

---

## 三、大怪物（Monster 系统）

### 5. 树妖 Treant

| 字段 | 值 |
|------|-----|
| hp | 400 |
| speed | 40 |
| melee_skill | 4 |
| melee_dice | 4 |
| melee_dice_sides | 12 |
| melee_damage | `[{ "type": "bash", "amount": 16 }]` |
| dodge | 0 |
| armor_bash | 10 |
| armor_cut | 8 |
| armor_pierce | 6 |
| aggression | -50 |
| morale | 200 |
| anger_triggers | `["PLAYER_CLOSE", "HURT"]` |

> 4d12 bash + 16。一拳碎墙。`speed: 40` 极慢——你跑得过它，但如果你站着不动就死了。

**生态**：古森林核心。几乎不移动。玩家砍树 → 站起来。

**harvest**：`harvest_treant`
- 没有 meat！掉落木材和植物材料
- skin: `bark_treant` (0.10)
- offal: `resin_treant` (0.03)
- dissect: `heartwood_treant`, `leaf_treant`（治疗药材料）

---

### 6. 多头蛇蜥 Hydra

| 字段 | 值 |
|------|-----|
| hp | 350 |
| speed | 80 / 水上 140 |
| melee_skill | 5 |
| melee_dice | 3 |
| melee_dice_sides | 6 |
| melee_damage | `[{ "type": "pierce", "amount": 8 }]` |
| dodge | 2 |
| armor_bash | 4 |
| armor_cut | 6 |
| aggression | 30 |
| morale | 200 |
| anger_triggers | `["PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "bite", "cooldown": 3 }, { "type": "bite", "cooldown": 3 }, { "type": "bite", "cooldown": 3 }]` |
| regenerate | 5（每回合回复 5 HP，火/酸伤害不回复） |

> 三个咬攻击 = 每回合咬三次。再生需在 C++ 中实现（`monster::process_turn` 加火/酸检测）。

**生态**：沼泽深处/地下湖。水里主场（speed 140）。独居。

**harvest**：`harvest_hydra`
- flesh: `meat_hydra` (0.30)
- blood: `blood_hydra` (0.05) — 剧毒
- dissect: `hydra_fang` ×3+, `hydra_venom_gland` ×2

---

## 四、人形怪物（NPC 系统）

> 以下走 NPC 三层架构（npc_class → npc → mapgen/faction），沿用强盗文档的格式。

### 7. 山岭巨人 Hill Giant

**npc_class_giant_hill**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [12, 16] }` |
| bonus_dex | `{ "rng": [-4, -2] }` |
| bonus_int | `{ "rng": [-6, -4] }` |

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [3, 5]` |
| Dodge | `"constant": 0` |

**武器**：`weapon_override: "itemgroup_giant_club"` — 大树干/骨棒  
**护甲**：`worn_override: "itemgroup_giant_rags"` — 翻来的破烂+骨头护甲

**faction**：`giants` — 对玩家 `likes_u: -30`，`kill on sight` 经对话或不对话  
**chat**：`TALK_GIANT_HILL`（可尝试哄骗/贿赂）

**生态**：丘陵洞穴。昼行。独居或成对。巢穴 = 垃圾堆+骨头。

**搜刮**：骨棒（双手钝器，需高 STR）、背包里 3-5 件随机人类物品、巨人牙项链

---

### 8. 独眼巨人 Cyclops

**npc_class_cyclops**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [8, 12] }` |
| bonus_dex | `{ "rng": [-2, 0] }` |

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [2, 4]` |

**武器**：`weapon_override: "itemgroup_cyclops_club"`  
**护甲**：毛皮拼接

**faction**：`giants` — 对玩家 `likes_u: -10`（不主动攻击，保护牛群）  
**chat**：`TALK_CYCLOPS`（极简单——"牛。我的。你走。"）

**生态**：草原/河谷。放牧野牛。极度孤独，可能尝试抓人说话。

**搜刮**：巨木棒、野牛肉干、独眼巨人眼

---

### 9. 沼泽巨人 Bog Giant

**npc_class_giant_bog**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [10, 14] }` |
| bonus_dex | `{ "rng": [-6, -4] }` |

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [4, 6]` |

**behavior**：`AMBUSH` — 站在原地伪装为土丘，`stealth: 10`（站在沼泽里 + 苔藓伪装）  
**faction**：`giants` — `likes_u: -80`，靠近即攻击  
**chat**：`TALK_DONE`（不说话）

**生态**：沼泽深处。几百年不动。玩家踩到身上附近 → 站起来攻击。

**搜刮**：苔藓皮（天然伪装斗篷材料）、泥浆腺（投掷物——减速/致盲）

---

### 10. 食人魔 Ogre

**npc_class_ogre**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [8, 12] }` |
| bonus_dex | `{ "rng": [-2, 0] }` |

| 技能 | 分布 |
|------|------|
| Bashing | `"rng": [3, 5]` |
| Dodge | `"constant": 0` |

**武器**：`weapon_override: "itemgroup_ogre_weapon"` — 大树干/拆下来的门/抢来的锅  
**护甲**：`worn_override: "itemgroup_ogre_armor"` — 破皮甲拼接  
**faction**：`ogres` — `likes_u: -40`，杀无赦  
**chat**：`TALK_DONE`

**生态**：森林边缘/废弃磨坊/桥底。夜行。巢穴 = 垃圾+骨头+抢来的锅。

**搜刮**：食人魔棍、牙项链（12-20 颗牙）、被吞掉的戒指×0-3

---

### 11. 哥布林 Goblin

**npc_class_goblin**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [-4, -2] }` |
| bonus_dex | `{ "rng": [2, 4] }` |

| 技能 | 分布 |
|------|------|
| Cutting | `"rng": [0, 2]` |
| Piercing | `"rng": [1, 2]` |
| Dodge | `"rng": [2, 4]` |
| Stealth | `"rng": [2, 4]` |

**武器**：小刀/短矛/投石索  
**护甲**：破布  
**faction**：`goblin_bands` — 对玩家 `likes_u: -20`，弱小时攻击，强大时逃跑  
**chat**：`TALK_GOBLIN`（恐吓/贿赂/逃跑）

**生态**：洞穴/废墟/下水道。夜行。部落制 20-100。放哨+设陷阱+偷营地。

**搜刮**：哥布林耳（赏金凭证）、破袋子（随机破烂）

---

### 12. 大地精 Hobgoblin

**npc_class_hobgoblin**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [2, 4] }` |
| bonus_dex | `{ "rng": [1, 3] }` |
| bonus_int | `{ "rng": [0, 2] }` |

| 技能 | 分布 |
|------|------|
| Cutting | `"rng": [2, 4]` |
| Piercing | `"rng": [2, 3]` |
| Dodge | `"rng": [1, 2]` |

**武器**：军刀/短矛+盾  
**护甲**：锁子甲/皮甲——比哥布林好一个档次  
**faction**：`hobgoblin_legion` — `likes_u: -40`，列阵迎敌

**生态**：哥布林部落的"军营区"。全天哨兵轮班。会包抄、退却、喊援兵。

**搜刮**：军刀（优质单手剑）、锁子甲、军旗

---

### 13. 狗头人 Kobold

**npc_class_kobold**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [-6, -4] }` |
| bonus_dex | `{ "rng": [3, 5] }` |

| 技能 | 分布 |
|------|------|
| Piercing | `"rng": [1, 2]` |
| Dodge | `"rng": [2, 4]` |

**武器**：投石索/短矛  
**护甲**：蜥蜴鳞片——天生鳞甲（`armor_bash: 1, armor_cut: 2` 来自 mutation `SCALES`）  
**faction**：`kobold_warrens` — `likes_u: -30`（进洞即敌对，洞外无视）

**生态**：地下洞穴/矿井。挖洞+设陷阱。对龙类有宗教崇拜。

**搜刮**：陷阱零件（弹簧/尖刺/绳）、蜡烛帽（光源头饰）、鳞片袋

---

### 14. 牛头人 Minotaur

**npc_class_minotaur**

| 属性偏移 | 值 |
|----------|-----|
| bonus_str | `{ "rng": [8, 12] }` |
| bonus_dex | `{ "rng": [0, 2] }` |

| 技能 | 分布 |
|------|------|
| Cutting | `"rng": [3, 5]` |
| Bashing | `"rng": [2, 4]` |

**武器**：`weapon_override: "itemgroup_minotaur_weapon"` — 巨斧/巨锤  
**护甲**：厚皮（`mutation: THICK_SKIN`）  
**faction**：`minotaur` — `likes_u: -30`，迷宫入侵者格杀勿论  
**chat**：`TALK_DONE`

**生态**：地下迷宫/废弃神庙。全天。记得每条死路。脚步声回荡在通道里。

**搜刮**：牛头人巨斧（专属武器）、牛角（号角材料）、迷宫钥匙

---

## 五、NPC 派系规划

| 派系 | 成员 | 关系 |
|------|------|------|
| `giants` | 山岭巨人、独眼巨人、沼泽巨人 | 各自松散，对玩家默认敌对 |
| `ogres` | 食人魔 | 对一切 kill on sight |
| `goblin_bands` | 哥布林、大地精 | 对玩家弱小时攻击，强大时逃跑；对狗头人奴役 |
| `hobgoblin_legion` | 大地精（主力） | 比哥布林更有序，可能与哥布林结盟 |
| `kobold_warrens` | 狗头人 | 进洞敌对，洞外中立；崇拜龙 |

---

## 六、双系统分层总结

| | Monster 系统 | NPC 系统 |
|---|---|---|
| **生物** | 飞龙、地龙、狮鹫、蝎尾狮、树妖、多头蛇蜥（6种） | 山岭巨人、独眼巨人、沼泽巨人、食人魔、哥布林、大地精、狗头人、牛头人（8种） |
| **为啥** | 不需要装备/对话；需要 harvest+special_attacks | 需要装备/技能分布/派系/（可能）对话 |
| **部位 HP** | 修 `apply_damage` 一行即可 | 原生支持 |
| **产物** | `harvest` + `dissect` 原生 | 需搜刮装备（npc 死亡时走掉落逻辑） |
