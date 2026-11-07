# 任务：狮 Griffiin 示例改造

## 目标

作为 Monster 部位 HP 修复后的第一个完整示例，验证双系统分层 + 新部位 + 新 anatomy + harvest/dissect 全链路。

## 依赖

- `monster_bodypart_fix.md`（C++ 修复必须先完成）
- `design08_3-野怪_奇幻.md` 狮鹫设计

---

## 改造内容

### 1. 新建 body part（`data/json/body_parts.json`）

```json
{ "id": "wing_l", "type": "body_part",
  "name": "left wing", "name_multiple": "wings",
  "base_hp": 40, "hit_size": 18, "hit_difficulty": 1.2,
  "main_part": "wing_l", "connected_to": "torso", "opposite_part": "wing_r",
  "is_limb": true, "is_vital": false,
  "limb_types": [["wing", 1.0]],
  "flags": ["LIMB_UPPER"],
  "encumbrance_text": "wing damaged",
  "smash_message": "You smash the %s with a sweeping blow."
},
{ "id": "wing_r", "type": "body_part", /* 对称 */ }
```

> 狮鹫不需要 neck/tail 新部位——head 足够粗，用 torso 作为脖子击中的路由即可。

### 2. 新建 anatomy（`data/json/anatomy.json`）

```json
{
  "id": "anatomy_griffin",
  "type": "anatomy",
  "parts": [
    "head", "torso",
    "arm_l", "arm_r", "hand_l", "hand_r",
    "leg_l", "leg_r", "foot_l", "foot_r",
    "wing_l", "wing_r"
  ]
}
```

> 12 部位：复用 human_anatomy 的 10 个 + 新增 2 个翅膀。

### 3. 新建 monster（`data/json/monsters/griffin.json`）

```json
{
  "type": "MONSTER",
  "id": "mon_griffin",
  "name": "Griffin",
  "anatomy": "anatomy_griffin",
  "bodytype": "bird",
  "species": ["MAMMAL"],
  "volume": "200000 ml",
  "weight": "200000 g",
  "hp": 150,
  "speed": 160,
  "melee_skill": 6,
  "melee_dice": 3,
  "melee_dice_sides": 6,
  "melee_damage": [{ "damage_type": "cut", "amount": 10 }],
  "dodge": 4,
  "armor_bash": 3,
  "armor_cut": 4,
  "aggression": 15,
  "morale": 90,
  "anger_triggers": ["PLAYER_CLOSE", "PLAYER_WEAK"],
  "special_attacks": [
    { "type": "leap", "cooldown": 5 }
  ],
  "harvest": "harvest_griffin",
  "dissect": "dissect_griffin",
  "vision_day": 50,
  "vision_night": 15,
  "path_settings": { "max_dist": 20 }
}
```

> `hp: 150` — C++ 修复后，150 会被分配到 12 个部位。每个部位 `base_hp + str_mod` 后约 40~60 HP，总 HP 约 500+。

### 4. 新建 harvest 产物（`data/json/harvest.json`）

```json
{
  "type": "harvest",
  "id": "harvest_griffin",
  "entries": [
    { "drop": "meat_wild",    "type": "flesh", "mass_ratio": 0.25 },
    { "drop": "bone_medium",  "type": "bone",  "mass_ratio": 0.10 },
    { "drop": "sinew",        "type": "bone",  "mass_ratio": 0.005 },
    { "drop": "feather_gold", "type": "skin",  "mass_ratio": 0.02 },
    { "drop": "fat",          "type": "flesh", "mass_ratio": 0.04 }
  ]
},
{
  "type": "harvest",
  "id": "dissect_griffin",
  "entries": [
    { "drop": "griffin_claw",  "type": "bone" },
    { "drop": "griffin_feather_gold", "type": "skin" }
  ]
}
```

### 5. 新建刷新组（`data/json/monstergroups.json`）

```json
{
  "type": "monstergroup",
  "name": "GROUP_MOUNTAIN_APEX",
  "monsters": [
    { "monster": "mon_griffin", "weight": 1, "cost_multiplier": 10 }
  ]
}
```

> weight=1 = 极稀有。`cost_multiplier: 10` = 生成一次占 10 个怪物的 spawn 配额——确保不会挤满。

### 6. 物品定义（`data/json/items/medieval/monster_parts.json`）

```json
{ "type": "GENERIC", "id": "griffin_claw",
  "name": "griffin claw", "description": "A razor-sharp talon from a griffin." },
{ "type": "GENERIC", "id": "griffin_feather_gold",
  "name": "golden griffin feather", "description": "A brilliant golden feather." }
```

---

## 完整引用链

```
body_parts.json
  wing_l / wing_r  ← anatomy_griffin.parts[] ← mon_griffin.anatomy
                                              ← mon_griffin.harvest → harvest_griffin
                                              ← mon_griffin.dissect → dissect_griffin
                                                                  → item.id (griffin_claw)
```

---

## 测试点

1. 狮鹫生成后 `get_all_body_parts()` 返回 12 个部位（含 wing_l/r）
2. 击中左翼 → 左翼 HP 扣减，头和躯干不受损
3. 左翼 HP=0 → 不死亡（is_vital=false），可能减速/不能飞
4. 头/躯干 HP=0 → 死亡（is_vital=true）
5. 死亡后 butcher → harvest_griffin 产物（肉/骨/羽毛）
6. 死亡后 dissect → 尸体口袋有 griffin_claw + griffin_feather_gold
