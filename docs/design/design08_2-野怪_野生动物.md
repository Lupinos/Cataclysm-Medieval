# 策划案 008_2：野怪体系（二）—— 野生动物

> 使用 **Monster 系统**（+ 部位 HP 修复）。14 种真实中世纪欧洲动物。

## 设计前提

- Monster 的 `set_body()` 已通过 `anatomy` JSON 支持部位定义，修复 `apply_damage` 一行后即有完整部位分血
- 伤害公式：`melee_dice × melee_dice_sides` bash + `melee_damage[]` 额外伤害
- 行为：`anger_triggers` / `fear_triggers` / `aggression` / `morale`
- 产物：`harvest` / `dissect` 原生支持
- 不需要 faction / dialogue / equipment —— 这些是 NPC 的东西

---

## 一、掠食者

### 1. 棕熊 (Brown Bear)

> 别惹。

| 字段 | 值 |
|------|-----|
| hp | 200 |
| speed | 130 |
| melee_skill | 5 |
| melee_dice | 4 |
| melee_dice_sides | 8 |
| melee_damage | `[{ "type": "cut", "amount": 6 }]` |
| dodge | 0 |
| armor_bash | 6 |
| armor_cut | 4 |
| armor_pierce | 2 |
| aggression | -5 |
| morale | 80 |
| anger_triggers | `["HURT", "PLAYER_NEAR_BABY"]` |
| fear_triggers | `["FIRE"]` |

> 伤害：4d8 bash + 6 cut = 4~32 bash + 6 cut。一掌下去你不穿甲就骨折。

**行为**：被动中立。玩家靠近幼崽或攻击后转为敌对。不逃跑。

**harvest**：`harvest_bear_brown`
- flesh: `meat_bear` (mass_ratio 0.40) / `fat_bear` (0.10)
- skin: `pelt_bear_brown` (0.03)
- bone: `bone_large` (0.12)
- offal: `liver_bear` (0.01) / `stomach_large` (scale 1, max 1)

**dissect**：`dissect_bear`
- `bear_claw` / `bear_tooth`

---

### 2. 狼 (Wolf)

> 一只不可怕。五只不一样。

| 字段 | 值 |
|------|-----|
| hp | 50 |
| speed | 150 |
| melee_skill | 5 |
| melee_dice | 2 |
| melee_dice_sides | 4 |
| melee_damage | `[{ "type": "cut", "amount": 4 }]` |
| dodge | 3 |
| armor_bash | 1 |
| armor_cut | 1 |
| aggression | -10 |
| morale | 30 |
| anger_triggers | `["HURT", "PLAYER_WEAK"]` |
| fear_triggers | `["FIRE", "HURT"]` |

> 2d4 bash + 4 cut = 2~8 bash + 4 cut。单只不强，群猎致命。

**monstergroup**：`GROUP_WOLF_PACK` — 2-5只成群，有概率出 alpha（hp+30%, melee_skill+2, morale 60）

**harvest**：`harvest_wolf`
- flesh: `meat_wolf` (0.25) / `fat` (0.02)
- skin: `pelt_wolf` (0.02)
- bone: `bone_medium` (0.08)
- offal: `liver` (0.01)

**dissect**：`dissect_wolf` — `wolf_fang`

---

## 二、大型草食动物

### 3. 野猪 (Wild Boar)

> 森林里最被低估的杀手。

| 字段 | 值 |
|------|-----|
| hp | 120 |
| speed | 120 |
| melee_skill | 4 |
| melee_dice | 3 |
| melee_dice_sides | 6 |
| melee_damage | `[{ "type": "pierce", "amount": 6 }]` |
| dodge | 1 |
| armor_bash | 4 |
| armor_cut | 3 |
| armor_pierce | 4 |
| aggression | -5 |
| morale | 70 |
| anger_triggers | `["HURT", "PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "leap", "cooldown": 10 }]` |

> 3d6 bash + 6 pierce = 3~18 + 6。冲锋（leap）首击 ×1.5。獠牙穿刺 + 厚皮软骨 = 正面很难打死。

**雄猪** aggression: 10, `anger_triggers: ["PLAYER_CLOSE"]`（见人就冲）

**harvest**：`harvest_boar`
- flesh: `meat_pork` (0.35) / `fat_pork` (0.12)
- skin: `pelt_boar` (0.03)
- bone: `bone_medium` (0.08)
- offal: `liver_boar` (0.01)

**dissect**：`dissect_boar` — `boar_tusk` ×2, `boar_bristle`

---

### 4. 欧洲野牛 (European Bison)

> 一吨重的肌肉。见到了绕路。

| 字段 | 值 |
|------|-----|
| hp | 350 |
| speed | 100 |
| melee_skill | 3 |
| melee_dice | 4 |
| melee_dice_sides | 10 |
| melee_damage | `[{ "type": "bash", "amount": 10 }]` |
| dodge | 0 |
| armor_bash | 8 |
| armor_cut | 5 |
| armor_pierce | 3 |
| aggression | 20 |
| morale | 100 |
| anger_triggers | `["PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "leap", "cooldown": 10 }]` |

> 4d10 bash + 10 bash = 4~40 + 10 = 14~50 bash。踩中一个成年男人可以直接踩死。

**harvest**：`harvest_bison`
- flesh: `meat_beef` (0.45) / `fat` (0.08)
- skin: `rawhide_bison` (0.05)
- bone: `bone_large` (0.15)
- offal: `stomach_large` (scale 1, max 1)

---

### 5. 赤鹿 (Red Deer)

> 大型猎物。发情期雄鹿别靠近。

| 字段 | 值 |
|------|-----|
| hp | 80 |
| speed | 140 |
| melee_skill | 3 |
| melee_dice | 2 |
| melee_dice_sides | 4 |
| melee_damage | `[{ "type": "pierce", "amount": 4 }]` |（仅雄鹿）
| dodge | 4 |
| aggression | -20 |
| morale | 20 |
| anger_triggers | `["HURT"]` |
| fear_triggers | `["PLAYER_CLOSE", "SOUND"]` |

> 雄鹿发情期变体 `mon_deer_red_rut`：aggression 30, morale 80, melee_damage +4, anger_triggers 加 `PLAYER_CLOSE`

**harvest**：`harvest_deer`
- flesh: `meat_venison` (0.30)
- skin: `rawhide_deer` (0.02)
- bone: `bone_medium` (0.08)
- offal: `liver` (0.01)

**dissect**：雄鹿 — `deer_antler`

---

### 6. 狍子 (Roe Deer)

> 最常见的猎物。小、快、胆小。

| 字段 | 值 |
|------|-----|
| hp | 35 |
| speed | 170 |
| melee_skill | 0 |
| dodge | 5 |
| aggression | -99 |
| morale | 5 |
| fear_triggers | `["PLAYER_CLOSE", "SOUND"]` |

> 纯逃跑。没有任何攻击能力。

**harvest**：`harvest_deer_small`
- flesh: `meat_venison` (0.20)
- skin: `rawhide_deer` (0.01)

---

## 三、小型兽类

### 7. 赤狐 (Red Fox)

> 偷营地的。

| 字段 | 值 |
|------|-----|
| hp | 15 |
| speed | 140 |
| melee_skill | 2 |
| melee_dice | 1 |
| melee_dice_sides | 3 |
| dodge | 5 |
| aggression | -50 |
| morale | 10 |
| fear_triggers | `["PLAYER_CLOSE", "SOUND"]` |

**harvest**：`harvest_fox`
- skin: `pelt_fox` (0.02)
- flesh: `meat_tiny` (0.10)

---

### 8. 獾 (Badger)

> 小坦克。

| 字段 | 值 |
|------|-----|
| hp | 30 |
| speed | 100 |
| melee_skill | 3 |
| melee_dice | 1 |
| melee_dice_sides | 4 |
| melee_damage | `[{ "type": "cut", "amount": 2 }]` |
| dodge | 3 |
| armor_bash | 3 |
| armor_cut | 2 |
| armor_pierce | 2 |
| aggression | -30 |
| morale | 50 |
| anger_triggers | `["HURT"]` |
| fear_triggers | `["PLAYER_CLOSE"]` |

> 皮厚难杀，伤不小但很能抗。

**harvest**：`harvest_badger`
- flesh: `meat_badger` (0.20) / `fat_badger` (0.05)
- skin: `pelt_badger` (0.02)

---

### 9. 河狸 (Beaver)

> 皮毛之王。极稀有。

| 字段 | 值 |
|------|-----|
| hp | 25 |
| speed | 90 |
| melee_skill | 2 |
| melee_dice | 1 |
| melee_dice_sides | 3 |
| dodge | 2 |
| aggression | -99 |
| morale | 5 |
| fear_triggers | `["PLAYER_CLOSE"]` |

> 低概率生成（spawn_weight: 1），优先出现在河流 map tile。

**harvest**：`harvest_beaver`
- skin: `pelt_beaver` (0.03) — 最值钱的皮毛之一
- flesh: `meat_beaver` (0.15)

**dissect**：`dissect_beaver` — `castoreum_gland`（药材）

---

### 10. 野兔 (Hare)

> 最常见的猎物。

| 字段 | 值 |
|------|-----|
| hp | 8 |
| speed | 180 |
| melee_skill | 0 |
| dodge | 7 |
| aggression | -99 |
| morale | 2 |
| fear_triggers | `["PLAYER_CLOSE"]` |

> 刷新率最高。spawn_weight: 15。

**harvest**：`harvest_hare`
- flesh: `meat_hare` (0.12)
- skin: `pelt_hare` (0.01)

---

## 四、鸟类

### 11. 金雕 (Golden Eagle)

| 字段 | 值 |
|------|-----|
| hp | 20 |
| speed | 160 |
| melee_skill | 4 |
| melee_dice | 1 |
| melee_dice_sides | 6 |
| melee_damage | `[{ "type": "cut", "amount": 4 }]` |
| dodge | 6 |
| aggression | 0 |
| morale | 50 |
| anger_triggers | `["PLAYER_WEAK"]` |
| special_attacks | `[{ "type": "leap", "cooldown": 5 }]` |

> 俯冲（leap）首击 ×2。翼展 2m 但本体重只 5kg——伤害靠速度和抓力，不靠体重。

**harvest**：`harvest_eagle`
- flesh: `meat_bird` (0.10)
- offal: `feather_eagle` (mass_ratio 0.05)

---

### 12. 雕鸮 (Eagle Owl)

| 字段 | 值 |
|------|-----|
| hp | 15 |
| speed | 150 |
| melee_skill | 5 |
| melee_dice | 1 |
| melee_dice_sides | 4 |
| melee_damage | `[{ "type": "cut", "amount": 3 }]` |
| dodge | 6 |
| aggression | -10 |
| morale | 40 |
| anger_triggers | `["PLAYER_WEAK"]` |
| special_attacks | `[{ "type": "leap", "cooldown": 5 }]` |

> 夜行。无声飞行——不会触发声音警报。

**harvest**：同金雕。

---

### 13. 水禽群 (Waterfowl)

| 字段 | 值 |
|------|-----|
| hp | 5 |
| speed | 130 |
| dodge | 4 |
| aggression | -99 |
| morale | 2 |
| fear_triggers | `["PLAYER_CLOSE", "SOUND"]` |

> 群居，2-8只成群。monstergroup: `GROUP_WATERFOWL`

**harvest**：`harvest_waterfowl`
- flesh: `meat_bird` (0.08)
- offal: `feather_duck` (0.03)
- `egg_waterfowl`（春夏季限定, scale 0~3）

---

## 五、爬行类

### 14. 蝰蛇 (Viper)

| 字段 | 值 |
|------|-----|
| hp | 6 |
| speed | 80 |
| melee_skill | 6 |
| melee_dice | 1 |
| melee_dice_sides | 2 |
| dodge | 6 |
| aggression | -20 |
| morale | 80 |
| anger_triggers | `["PLAYER_CLOSE"]` |
| fear_triggers | `["PLAYER_CLOSE"]` |
| special_attacks | `[{ "type": "bite", "cooldown": 5, "effects": [{"id": "venom_viper", "duration": [600, 1200]}] }]` |

> 咬伤附加 `venom_viper`：疼痛 + 肿胀 + 减速 10~20 分钟。不致命但很难受。冬天不生成。

**harvest**：`harvest_viper`
- flesh: `meat_snake` (0.08)

**dissect**：`dissect_viper` — `snake_venom_gland`

---

## 六、地域分布与刷新

| 地形 | AnimalGroup | 内容 |
|------|-----------|------|
| `forest` | `GROUP_FOREST` | 棕熊(2%)、狼(8%)、野猪(10%)、赤鹿(8%)、狍子(15%)、狐(10%)、獾(5%)、野兔(15%)、雕鸮(3%) |
| `forest_thick` | `GROUP_FOREST_DENSE` | 棕熊(5%)、狼(10%)、野猪(15%)、赤鹿(5%)、獾(8%) |
| `swamp_water` | `GROUP_SWAMP` | 河狸(3%)、水禽(20%) |
| `grassland` | `GROUP_PLAINS` | 野牛(5%)、野兔(15%) |
| `mountain` | `GROUP_MOUNTAIN` | 金雕(8%) |
| `night` 追加 | — | 狼权重翻倍、狐权重翻倍、雕鸮权重翻倍 |
| `winter` | — | 蝰蛇权重=0、狼权重×1.5 |
