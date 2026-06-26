# JSON 数据体系

> Cataclysm-DDA 游戏的所有数据内容均由 JSON 定义。本文档描述 `data/` 目录下的 JSON 数据组织方式、类型体系、加载规则和关键约定。

---

## 1. 目录总览

```
data/
├── core/            # 核心配置（游戏平衡参数、世界选项滑块、提示语、天气、伤害指示）
├── json/            # ★ 主数据目录（所有游戏内容 JSON，见 §2）
├── mods/            # 模组系统（51+ 个 mod，见 §5）
├── raw/             # 底层原始数据（键位绑定、颜色主题/模板、推箱子关卡）
├── cache/           # 缓存数据
├── credits/         # 鸣谢名单
├── font/            # 字体数据 + fontdata.json
├── help/            # 帮助文本
├── motd/            # 每日提示（Message of the Day）
├── names/           # 名称生成数据（人名等）
├── sound/           # 音效
└── title/           # 标题画面数据
```

---

## 2. `data/json/` 主数据目录（100+ 文件/子目录）

### 2.1 加载顺序机制

**广度优先（BFS）**：文件按目录层级加载，同层按字典序。

```
data/json/                  ← 第 1 层（最早加载）
  skills.json               ← A-Z 排序
  materials.json
  ...
  items/                    ← 第 2 层（之后加载）
    generic.json
    ammo/
    armor/
  recipes/                  ← 第 2 层
    recipe_food.json
    ...
  monsters/                 ← 第 2 层
    zed-classic.json
    ...
```

**关键规则**：`data/json/xxx.json` **总是** 先于 `data/json/subdir/xxx.json` 加载。因此：

- 依赖项应放在较浅层级（如 `skills.json` 在根级，`professions/` 在子目录）
- 同深度的文件按字典序加载（仅 ASCII 保证字母序，UTF-8 按 codepoint 排序）

### 2.2 JSON 类型完整目录

以下是 `data/json/` 中所有 JSON 顶层 `"type"` 类型及其所在文件/目录（按文件系统组织）：

| 分类 | 文件/目录 | 主要 type |
|------|----------|-----------|
| **技能** | `skills.json` | `skill` |
| **材料** | `materials.json` (103KB) | `material` |
| **物品** | `items/` (42 子目录) | `GENERIC`, `AMMO`, `GUN`, `TOOL`, `ARMOR`, `COMESTIBLE`, `BOOK`, `BIONIC_ITEM`, `MAGAZINE`, `TOOLMOD`, `GUNMOD`, `PET_ARMOR`, `ENGINE`, `WHEEL`, `BATTERY` 等 |
| **怪物** | `monsters/` (59 文件) | `MONSTER` |
| **怪物组** | `monstergroups/` (24 文件) | `monstergroup` |
| **怪物掉落** | `monsterdrops/` (23 文件) | `item_group` |
| **怪物特殊攻击** | `monster_special_attacks/` (8 文件) | `monster_attack` |
| **怪物弱点** | `monster_weakpoints/` (14 文件) | `weakpoint_set` |
| **怪物阵营** | `monster_factions.json` | `monster_faction` |
| **配方** | `recipes/` (24 文件, 最大 `recipe_food.json` 350KB) | `recipe` |
| **拆卸** | `uncraft/` (14 文件) | `uncraft` |
| **建造** | `construction.json` (310KB) | `construction` |
| **建造分类** | `construction_category.json` | `construction_category` |
| **建造分组** | `construction_group.json` | `construction_group` |
| **拆除** | `deconstruction.json` | `construction`（同 type） |
| **职业** | `professions.json` (287KB) | `profession`, `item_group`, `profession_item_substitutions` |
| **场景** | `scenarios.json` | `scenario` |
| **起始地点** | `start_locations.json` | `start_location` |
| **任务** | `starting_missions.json` | `mission_definition` |
| **突变** | `mutations/` (11 文件) | `mutation`, `mutation_category` |
| **生化模块** | `bionics.json` (74KB) | `bionic` |
| **生化法术** | `bionic_spells.json` | `bionic` |
| **法术/魔法** | `artifact/` (6 文件) | `spell_type`, `fake_spell` 等 |
| **附魔** | `enchantments.json` | `enchantment` |
| **效果** | `effects.json` (161KB) | `effect_type` |
| **效果条件** | `effects_on_condition/` (16 文件) | `effect_on_condition` |
| **梦** | `dreams.json` | `dream` |
| **地形/家具** | `furniture_and_terrain/` (58 文件) | `terrain`, `furniture` |
| **地图生成** | `mapgen/` (303 文件!) | `mapgen`, `update_mapgen` |
| **地图调色板** | `mapgen_palettes/` (94 文件) | `palette` |
| **大地图** | `overmap/` (8 文件) | `overmap_terrain`, `overmap_special`, `city_building`, `overmap_connection`, `region_overlay` |
| **区域设置** | `regional_map_settings.json` | `region_settings` |
| **天气** | `weather_type.json` | `weather_type` |
| **弹药效果** | `ammo_effects.json` | `ammo_effect` |
| **伤害类型** | `damage_types.json` | `damage_type` |
| **武术** | `martialarts.json` + `martialarts_fictional.json` | `martial_art` |
| **技法** | `techniques.json` (134KB) | `technique` |
| **攀爬** | `climbing.json` | `climb` |
| **NPC** | `npcs/` (85 文件) | `npc`, `npc_class`, `talk_topic`, `mission_definition`, `item_group`, `faction`, `computer_action` 等 |
| **对话** | `speech.json` (78KB) | `speech` |
| **对话标签** | `npcs/talk_tags.json` | 对话条件/效果标签 |
| **载具** | `vehicles/` (15 文件) | `vehicle` |
| **载具部件** | `vehicleparts/` (25 文件) | `vehicle_part` |
| **载具组** | `vehicle_groups.json` | `vehicle_group` |
| **物品组** | `itemgroups/` (41 文件) | `item_group` |
| **收获** | `harvest.json` (119KB) | `harvest` |
| **解剖收获** | `harvest_dissect.json` | `harvest` |
| **屠宰需求** | `butchery_requirements.json` | `butchery_requirement` |
| **成就** | `achievements.json` | `achievement` |
| **行为准则** | `conducts.json` | `conduct` |
| **统计** | `statistics.json` (89KB) | `statistic` |
| **计分** | `scores.json` | `score` |
| **特质/背景** | `npcs/` + `mutations/` | `mutation`（玩家特质）, `npc`（NPC 背景） |
| **爱好** | `hobbies.json` | `hobby` |
| **熟练度** | `proficiencies/` (17 文件) | `proficiency` |
| **工具品质** | `tool_qualities.json` | `tool_quality` |
| **需求** | `requirements/` (13 文件) | `requirement` |
| **配方分组** | `recipes/` | `recipe_category` |
| **片段** | `snippets/` (40 文件) | `snippet` |
| **旗帜** | `flags.json` (60KB) | `json_flag` |
| **区域** | `zones.json` | 区域定义 |
| **战场类型** | `field_type.json` (58KB) | `field_type` |
| **发射器** | `emit.json` | `emit` |
| **气味** | `scent_types.json` | `scent_type` |
| **士气** | `morale_types.json` | `morale_type` |
| **情绪表情** | `mood_faces.json` | `mood_face` |
| **陷阱** | `traps.json` | `trap` |
| **门** | `gates.json` | `gate` |
| **连接组** | `connect_groups.json` | 连接组定义 |
| **躯体部位** | `body_parts.json` | `body_part` |
| **躯体图表** | `bodypart_graphs/` (9 文件) | `body_graph` |
| **肢体评分** | `limb_scores.json` | `limb_score` |
| **解剖** | `anatomy.json` | 解剖定义 |
| **角色修正** | `character_modifiers.json` | `character_mod` |
| **移动模式** | `move_modes.json` | `move_mode` |
| **速度描述** | `speed_descriptions.json` | `speed_description` |
| **旋转符号** | `rotatable_symbols.json` | `rotatable_symbol` |
| **技能显示** | `skillDisplayType.json` | `skill_display_type` |
| **武器类别** | `weapon_categories.json` | `weapon_category` |
| **弹药类型** | `items/ammo_types.json` | `ammunition_type` |
| **物品分类** | `item_category.json` | `item_category` |
| **物品动作** | `item_actions.json` | `item_action` |
| **服装修改** | `clothing_mods.json` | `clothing_mod` |
| **战利品区域** | `loot_zones.json` | 战利品区域 |
| **玩家活动** | `player_activities.json` | `activity_type` |
| **维生素** | `vitamin.json` | `vitamin` |
| **疾病** | `disease.json` | 疾病 |
| **成瘾** | `addictions.json` | 成瘾 |
| **物种** | `species.json` | `SPECIES` |
| **道路载具** | `road_vehicles.json` | 道路载具生成 |
| **故障** | `faults/` (6 文件) | `fault` |
| **遭遇** | `encounters/` (2 文件) | 随机遭遇 |
| **技能符文** | `ascii_art/` (5 文件) | ASCII 美术 |
| **迁移/淘汰** | `obsoletion/` (22 文件) | 淘汰和迁移数据 |
| **UI** | `ui/` (57 文件) | UI 配置 |
| **艺术** | `screenshots/` | 截图相关 |
| **默认黑名单** | `default_blacklist.json` | 黑名单 |
| **虚假物品** | `items/fake.json` | 系统伪物品 |

### 2.3 按数据量的关键文件

| 文件 | 大小 | 内容 |
|------|------|------|
| `construction.json` | 310KB | ~9000 个建造配方 |
| `professions.json` | 287KB | 职业定义 + 物品组 |
| `recipes/recipe_food.json` | 350KB | 食物配方 |
| `recipes/nested.json` | 255KB | 嵌套配方 |
| `recipes/recipe_deconstruction.json` | 230KB | 拆卸配方 |
| `effects.json` | 161KB | 状态效果定义 |
| `materials.json` | 103KB | 材料属性 |
| `items/generic.json` | 132KB | 通用物品 |
| `items/tool_armor.json` | 151KB | 工具/护甲 |
| `monsters/insect_spider.json` | 153KB | 昆虫/蜘蛛怪物 |
| `monsters/mammal.json` | 118KB | 哺乳动物 |
| `mapgen/` | 303 文件 | 地图生成（规模最大） |

---

## 3. 核心 JSON Schema

### 3.1 通用继承机制

Cataclysm JSON 有强大的数据复用机制：

```json
// copy-from：完全继承另一个对象，覆盖指定字段
{
  "type": "MONSTER",
  "id": "mon_zombie_cop",
  "copy-from": "mon_zombie",         // 继承 mon_zombie 所有属性
  "name": { "str": "zombie cop" },   // 覆盖 name
  "armor": { "bash": 6, "cut": 6 }    // 覆盖 armor
}

// proportional：按比例缩放数值
{
  "proportional": { "weight": 1.25 }  // weight 乘以 1.25
}

// relative：加减数值
{
  "relative": { "melee_damage": { "bash": 2 } }  // bash 伤害 +2
}

// abstract：抽象模板（不直接生成实体）
{
  "abstract": "generic_polymer_resin",  // 其他材料可 copy-from
  "type": "material",
  ...
}
```

### 3.2 Monster（怪物）

**文件**：`monsters/` 下 59 个分类文件
**type**：`"MONSTER"`

```json
{
  "id": "mon_zombie",
  "type": "MONSTER",
  "name": { "str": "zombie" },
  "description": "A human body, swaying as it moves...",
  
  // 基础属性
  "default_faction": "zombie",
  "bodytype": "human",
  "species": [ "ZOMBIE", "HUMAN" ],
  "volume": "62500 ml",
  "weight": "81500 g",
  "hp": 80,
  "speed": 70,              // 移动速度
  "material": [ "flesh" ],
  "symbol": "Z",
  "color": "light_green",
  
  // AI
  "aggression": 100,
  "morale": 100,
  "vision_day": 30,
  "vision_night": 3,
  
  // 战斗
  "melee_skill": 4,
  "melee_dice": 2,
  "melee_dice_sides": 3,
  "melee_damage": [ { "damage_type": "cut", "amount": 0 } ],
  "dodge": 1,
  "armor": { "bash": 2, "cut": 1, "electric": 2 },
  
  // 特殊攻击
  "special_attacks": [
    { "id": "grab" },
    { "id": "bite_humanoid", "cooldown": 5 },
    { "id": "scratch_humanoid" }
  ],
  "grab_strength": 20,
  
  // 弱点/精通
  "weakpoint_sets": [ "wps_humanoid_body" ],
  "families": [ "prof_intro_biology", "prof_physiology", "prof_wp_zombie" ],
  
  // 进化
  "upgrades": { "half_life": 30, "into_group": "GROUP_ZOMBIE_UPGRADE" },
  "burn_into": "mon_zombie_scorched",
  "fungalize_into": "mon_zombie_fungus",
  
  // 掉落/收获
  "death_drops": "default_zombie_death_drops",
  "harvest": "zombie_humanoid",
  
  // 行为标志
  "flags": [ "SEES", "HEARS", "STUMBLES", "WARM", "BASHES", 
             "POISON", "NO_BREATHE", "REVIVES", "FILTHY" ]
}
```

**怪物分类文件组织**：
- `zed-*.json`：僵尸变种（经典、酸性、电力、爆炸、儿童、士兵等 20+ 种）
- `mammal.json`、`bird.json`、`fish.json`、`insect_spider.json`：现实动物
- `nether.json`：异界生物
- `fungus.json`、`triffid.json`：真菌/植物敌人
- `robofac_robots.json`、`turrets.json`、`defense_bot.json`：机械敌人
- `feral_humans.json`：野生人类
- `mutant.json`：变异生物

### 3.3 Item（物品）

**文件**：`items/` 下 42 个子目录
**主要 type**：`GENERIC`, `AMMO`, `GUN`, `TOOL`, `ARMOR`, `COMESTIBLE`, `BOOK`, `BIONIC_ITEM`, `MAGAZINE`, `CONTAINER`, `TOOLMOD`, `GUNMOD`

```json
// GENERIC - 通用物品
{
  "type": "GENERIC",
  "id": "superglue",
  "name": { "str_sp": "superglue" },
  "description": "A tube of strong glue...",
  "category": "spare_parts",
  "weight": "8 g",
  "volume": "10 ml",
  "price": 1800,
  "material": [ "plastic" ],
  "symbol": ",",
  "color": "white"
}

// COMESTIBLE - 食物/药品
{
  "type": "COMESTIBLE",
  "id": "mutant_bug_hydrogen_sacs",
  "comestible_type": "FOOD",
  "spoils_in": "8 hours",
  "fun": -25,
  ...
}

// TOOL - 工具（含电池/容器槽位）
{
  "type": "TOOL",
  "id": "usb_drive",
  "pocket_data": [
    { "pocket_type": "SOFTWARE", "max_contains_volume": "1 L" },
    { "pocket_type": "EBOOK", "rigid": true, ... }
  ],
  "to_hit": { "grip": "bad", "length": "hand", "surface": "any", "balance": "clumsy" }
}
```

**物品子目录组织**：
| 子目录 | 内容 |
|--------|------|
| `ammo/` | 弹药（63 文件，按口径分类） |
| `armor/` | 护甲（40 文件） |
| `book/` | 书籍（42 文件） |
| `comestibles/` | 食物/药品（34 文件） |
| `containers/` | 容器（4 文件） |
| `corpses/` | 尸体物品（4 文件） |
| `generic/` | 通用杂项（13 文件） |
| `gun/` | 枪械（63 文件，按口径/类型分类） |
| `gunmod/` | 枪械改装（15 文件） |
| `magazine/` | 弹匣（48 文件） |
| `melee/` | 近战武器（7 文件） |
| `ranged/` | 远程武器（8 文件） |
| `resources/` | 资源/材料物品（12 文件） |
| `tool/` | 工具（36 文件） |
| `vehicle/` | 载具零件（27 文件） |

### 3.4 Recipe（配方）

**文件**：`recipes/` 下 24 文件
**type**：`"recipe"`

```json
{
  "type": "recipe",
  "activity_level": "LIGHT_EXERCISE",
  "result": "cake2",
  "category": "CC_FOOD",
  "subcategory": "CSC_FOOD_BREAD",
  "skill_used": "cooking",
  "difficulty": 6,
  "time": "2 h",
  "charges": 12,
  
  "book_learn": [
    [ "cookbook_daintydishes", 6 ],
    [ "baking_book", 2 ]
  ],
  
  "qualities": [ { "id": "OVEN", "level": 2 } ],
  "tools": [ [ [ "surface_heat", 35, "LIST" ] ] ],
  
  "proficiencies": [
    { "proficiency": "prof_food_prep" },
    { "proficiency": "prof_baking" }
  ],
  
  "components": [
    [ [ "flour_any", 16, "LIST" ] ],
    [ [ "salt", 2 ] ],
    [ [ "sugar_standard", 2, "LIST" ] ],
    [ [ "chocolate", 3 ] ],
    [ [ "any_butter_or_oil", 10, "LIST" ] ],
    [ [ "eggs_any_shape", 4, "LIST" ] ],
    [ [ "water_clean", 1 ] ]
  ]
}
```

**配方中的关键字段**：
- `activity_level`：`NO_EXERCISE` / `LIGHT_EXERCISE` / `MODERATE_EXERCISE` / `BRISK_EXERCISE`
- `components`：双层嵌套数组，外层 = 需求组（OR），内层 = 替代选项（也用 OR）
- `"LIST"` 后缀：引用预定义物品列表（便于扩展）
- `batch_time_factors`：批量制作时间缩放 [百分比, 数量]
- `byproducts`：副产物

**配方文件组织**：
| 文件 | 大小 | 内容 |
|------|------|------|
| `recipe_food.json` | 350KB | 食物烹饪 |
| `recipe_deconstruction.json` | 230KB | 物品拆卸 |
| `recipe_others.json` | 112KB | 杂项制作 |
| `recipe_medsandchemicals.json` | 92KB | 药品/化学品 |
| `recipe_vehicle.json` | 47KB | 载具相关 |
| `recipe_ammo.json` | 32KB | 弹药制作 |
| `nested.json` | 255KB | 嵌套配方模板 |

### 3.5 Skill（技能）

**文件**：`skills.json`
**type**：`"skill"`

技能分四大类：
- **近战** (`display_melee`)：`melee`, `unarmed`, `bashing`, `cutting`, `stabbing`, `dodge`
- **远程** (`display_ranged`)：`gun`, `archery`, `pistol`, `rifle`, `shotgun`, `smg`, `launcher`, `throw`
- **制造** (`display_crafting`)：`fabrication`, `cooking`, `tailor`, `survival`, `electronics`, `chemistry`
- **交互** (`display_interaction`)：`speech`, `computer`, `firstaid`, `mechanics`, `traps`, `driving`, `swimming`

```json
{
  "type": "skill",
  "id": "melee",
  "name": { "str": "melee" },
  "description": "Your skill and finesse in personal combat...",
  "tags": [ "combat_skill" ],
  "time_to_attack": {
    "min_time": 50,           // 最小攻击时间
    "base_time": 200,         // 基础攻击时间
    "time_reduction_per_level": 20  // 每级减少的攻击时间
  },
  "display_category": "display_melee",
  "sort_rank": 1000
}
```

### 3.6 Material（材料）

**文件**：`materials.json` (103KB, 3099 行)
**type**：`"material"`

定义约 200+ 种材料，每项包含物理属性：

```json
{
  "type": "material",
  "id": "steel",
  "name": "Steel",
  "density": 7.8,
  "specific_heat_liquid": 0.5,
  "specific_heat_solid": 0.5,
  "latent_heat": 273,
  "conductive": true,
  "chip_resist": 15,           // 抗破损
  "dmg_adj": [ "marked", "dented", "smashed", "shattered" ],
  "bash_dmg_verb": "dented",
  "cut_dmg_verb": "scratched",
  "resist": {                   // 护甲值
    "bash": 6,
    "cut": 8,
    "acid": 7,
    "heat": 3,
    "bullet": 4
  },
  "burn_data": [                // 燃烧行为
    { "fuel": 0, "smoke": 0, "burn": 0 },
    { "fuel": 0, "smoke": 0, "burn": 0 },
    { "fuel": 0, "smoke": 0, "burn": 0 }
  ],
  "repair_difficulty": 5
}
```

材料类别涵盖：金属、塑料、织物、有机物（骨/肉/壳）、石材、液体、伪燃料等。

### 3.7 Effect（状态效果）

**文件**：`effects.json` (161KB, 4620 行)
**type**：`"effect_type"`

定义所有角色/NPC/怪物身上的 BUFF/DEBUFF：

```json
{
  "type": "effect_type",
  "id": "poison",
  "name": [ "Poisoned" ],
  "desc": [ "You have been poisoned!" ],
  "rating": "bad",
  "resist_traits": [ "POISRESIST" ],
  "base_mods": {
    "per_mod": [ -2, -1 ],
    "dex_mod": [ -1, -1 ],
    "str_mod": [ -2, 0 ],
    "pain_min": [ 1 ],
    "pain_chance": [ 150, 900 ],
    "hurt_min": [ 1 ],
    "hurt_chance": [ 450, 2700 ]
  },
  "show_in_info": true
}
```

### 3.8 Profession（职业）

**文件**：`professions.json` (287KB)
**type**：`"profession"`

```json
{
  "type": "profession",
  "id": "unemployed",
  "name": "Survivor",
  "description": "Some would say that there's nothing particularly notable about you...",
  "points": 0,
  "items": {
    "both": { "entries": [
      { "item": "jeans" },
      { "item": "longshirt" },
      { "group": "charged_smart_phone" },    // 引用物品组
      { "group": "charged_matches" }
    ]},
    "male": { "entries": [ { "item": "boxer_shorts" } ] },
    "female": { "entries": [ { "item": "bra" }, { "item": "panties" } ] }
  }
}
```

- `points`：职业消耗的创建点数
- `items`：按性别分组的起始装备
- 可包含 `skills`、`proficiencies`、`traits`、`flags`

### 3.9 Construction（建造）

**文件**：`construction.json` (310KB, ~9000 行)
**type**：`"construction"`

```json
{
  "type": "construction",
  "id": "constr_door_curtain",
  "group": "build_door_curtain",
  "category": "CONSTRUCT",
  "required_skills": [ [ "tailor", 1 ] ],
  "time": "30 m",
  "qualities": [ [ { "id": "HAMMER", "level": 2 } ] ],
  "components": [
    [ [ "nail", 4 ], [ "pointy_stick", 2 ], [ "spike", 2 ] ],
    [ [ "sheet", 2 ] ],
    [ [ "stick", 1 ] ],
    [ [ "withered", 12 ], [ "straw_pile", 12 ], [ "string_36", 1 ] ]
  ],
  "pre_special": "check_empty",
  "post_terrain": "t_door_curtain_c"
}
```

类别包括：`CONSTRUCT`（建造）、`REPAIR`（修理）、`REINFORCE`（加固）、`DIG`（挖掘）、`FARM_WOOD`（伐木）、`WINDOWS`（窗户）、`FURN`（家具）等。

### 3.10 Mapgen（地图生成）

**文件**：`mapgen/` (303 文件！)
**type**：`"mapgen"`, `"update_mapgen"`

这是整个 JSON 数据体系中规模最大的子目录，包含每个可生成地点的布局定义。文件命名规律：
- `house/`：152 个房屋变体
- `fema/`：36 个 FEMA 营地变体
- `lab/`：13 个实验室变体
- `microlab/`：15 个微型实验室
- 其余按地点命名：`hospital.json`, `school_1.json`, `stadium_football.json` (128KB!), `mansion.json` (102KB!), 等

**配套的调色板**：`mapgen_palettes/` (94 文件) 定义可复用的地形/家具组合。

### 3.11 其他重要类型简述

| Type | 说明 |
|------|------|
| `terrain` | 地形：地板、墙壁、水、门、窗等 |
| `furniture` | 家具：可交互的物件（工作台、床、容器等） |
| `vehicle` / `vehicle_part` | 载具定义与部件属性 |
| `item_group` | 物品组（战利品表），支持嵌套和概率 |
| `monstergroup` | 怪物生成组 |
| `ammunition_type` | 弹药类型（口径） |
| `mutation` | 变异/特质/背景（三合一） |
| `bionic` | 生化模块 |
| `martial_art` | 武术流派 |
| `technique` | 战斗技法 |
| `npc_class` | NPC 职业模板 |
| `talk_topic` | 对话主题 |
| `mission_definition` | 任务定义 |
| `faction` | 阵营定义 |
| `fault` | 载具故障类型 |
| `field_type` | 场地效应类型（火、酸、烟等） |
| `weather_type` | 天气类型 |
| `overmap_terrain` / `overmap_special` | 大地图地块/特殊地点 |
| `snippet` | 文本片段（用于动态描述生成） |
| `harvest` | 收获定义（解剖掉落） |
| `proficiency` | 熟练度（子技能系统） |
| `tool_quality` | 工具品质（如 HAMMER 1-3） |
| `enchantment` | 附魔效果 |
| `spell_type` | 法术类型 |
| `vitamin` | 维生素定义 |
| `dream` | 梦境文本 |
| `clothing_mod` | 服装修改 |
| `achievement` / `conduct` / `score` | 成就/行为准则/计分 |

---

## 4. 关键约定

### 4.1 `copy-from` 继承链

贯穿整个数据体系的核心模式，用于减少重复：

```
generic_polymer_resin (abstract)
  ├── thermo_resin (copy-from: generic_polymer_resin)
  ├── epoxy (copy-from: generic_polymer_resin)
  ├── fiberglass (copy-from: generic_polymer_resin)
  │     └── carbonfiber (copy-from: fiberglass)
  └── ...
```

### 4.2 `"LIST"` 机制

在配方组件中使用 `"LIST"` 后缀引用预定义的物品列表：
```json
"components": [
  [ [ "flour_any", 16, "LIST" ] ],     // 任何面粉类物品
  [ [ "any_butter_or_oil", 10, "LIST" ] ]  // 任何油脂
]
```

### 4.3 伪物品（Pseudo Items）

以 `PSEUDO` flag 标记的物品仅用于系统内部逻辑，不应出现在游戏中：
- `"animal"`, `"muscle"`, `"wind"`, `"sunlight"`, `"metabolism"`：燃料类型
- `"fire"`, `"apparatus"`：制作所需的抽象工具
- `"null"`：空手

### 4.4 度量单位

JSON 数据中使用带单位的字符串：
- 体积：`"250 ml"`, `"1 L"`, `"30 L"`
- 重量：`"8 g"`, `"81500 g"`, `"1 kg"`
- 时间：`"5 m"`, `"2 h"`, `"9 s"`
- 能量：`"1000 kJ"`, `"15600 kJ"`
- 长度：`"122 cm"`, `"28 cm"`

### 4.5 双轨命名

物品/怪物名称支持单复数分离：
```json
"name": { "str": "chunk of chitin", "str_pl": "chunks of chitin" }
"name": { "str_sp": "superglue" }  // 不可数名词（同形）
```

---

## 5. Mod 系统

### 5.1 Mod 目录结构

`data/mods/` 下有 51 个 mod，每个 mod 是一个子目录：

```
data/mods/
├── default.json              # 开发者推荐合集
├── replacements.json         # 全局替换规则
├── Magiclysm/                # ★ 最大的内容 mod
│   ├── modinfo.json          # MOD_INFO + 额外类型定义
│   ├── items/ (53 文件)      # 物品
│   ├── monsters/ (20 文件)   # 怪物
│   ├── Spells/ (20 文件)     # 法术
│   ├── recipes/ (19 文件)    # 配方
│   ├── enchantments/ (24 文件)
│   ├── mutations/ (9 文件)
│   ├── npc/ (15 文件)
│   ├── worldgen/ (27 文件)   # 世界生成覆盖
│   ├── professions.json
│   ├── scenarios.json
│   ├── materials.json
│   └── ...
├── Aftershock/               # 科幻内容 mod
├── Xedra_Evolved/            # 超自然内容 mod
├── MindOverMatter/           # 灵能 mod
├── DinoMod/                  # 恐龙 mod
├── CrazyCataclysm/           # 疯狂模式
├── No_Hope/                  # 高难度 mod
├── innawood/                 # 纯荒野 mod
├── Sky_Island/               # 天空岛 mod
├── TEST_DATA/                # 测试数据 (61 文件!)
├── ... (共 51 个)
```

### 5.2 modinfo.json

```json
{
  "type": "MOD_INFO",
  "id": "magiclysm",
  "name": "Magiclysm",
  "authors": [ "KorGgenT", "GuardianDll" ],
  "description": "Cataclysm but with magic spells!",
  "category": "content",
  "dependencies": [ "dda" ]
}
```

- `dependencies`：前置 mod
- `category`：分类（`content`, `balance`, `total_conversion` 等）
- 同一 JSON 文件中还可以定义该 mod 独有的 type（如 Magiclysm 定义了 `spellcraft` 技能）

### 5.3 Mod 覆盖机制

Mod 可以：
- 新增 JSON 对象（新物品、新怪物、新配方等）
- 通过 `copy-from` + 覆盖字段修改已有对象
- 通过 `migration_and_obsoletion.json` 淘汰/迁移物品
- 通过 `mod_interactions/` 处理与其他 mod 的交互

### 5.4 Mod 验证与调试流程 ★NEW

#### 5.4.1 C++ 级别静态校验命令
通过执行游戏可执行文件，可以对 JSON 数据的语法、类型字段、依赖一致性进行验证。

*   **`--jsonverify` 限制**：此参数仅运行 `game::load_static_data()`，其只会加载少数全局静态配置 JSON（如 `auto_pickup`, `auto_notes`, `safemode`），并**不会**加载核心游戏数据 `data/json/` 或任何 Mod。
*   **`--check-mods <mod_id>` 核心校验**：必须使用此参数（如 `--check-mods dda` 校验原版，`--check-mods medieval` 校验中世纪 Mod）才能执行全量 JSON 数据的读取、解析、合并与语义 Finalize 校验。所有的 JSON 语法错误与语义引用警告均在此命令中触发。

由于默认的编译产物 `cataclysm-tiles.exe` 采用的是 Windows GUI 子系统，在终端直接运行它会立即返回，并且不会自动将其标准输出/错误打印在控制台上。

*   **最佳实践（PowerShell 监测脚本）**：
    在 `msvc-full-features/` 目录下提供了一个 `check_with_wait.ps1` 脚本。它通过删除旧日志、启动进程、重定向输出并强制睡眠 15 秒（如果进程未结束则继续等待）来安全地收集校验结果。
    ```powershell
    # 校验原版 DDA 核心数据并等待输出：
    powershell -ExecutionPolicy Bypass -File .\check_with_wait.ps1 -Mode dda

    # 校验中世纪 Mod 核心数据并等待输出：
    powershell -ExecutionPolicy Bypass -File .\check_with_wait.ps1 -Mode medieval
    ```
    输出结果会在进程退出后被统一读取并打印在终端，包含：Standard Output、Standard Error、以及 `config/debug.log` 内容。

#### 5.4.2 路径防冲突机制 (Duplicate Load Gotcha)
在 Windows 环境下运行静态校验时，默认会载入基准数据目录下的模组以及用户数据目录下的模组。若当前工作目录与数据目录配置重叠，会导致 mod 被加载两次，触发 `there is already a mod with ident xxx` 的二级解析冲突。
*   **根因**：`PATH_INFO::moddir()` 与 `PATH_INFO::user_moddir_path()` 指向了同一个物理路径。
*   **防范方案**：在校验时**显式指定**不同路径的 `--basepath` 和 `--userdir`。例如，使 `--userdir` 指向一个没有 `mods` 文件夹的空父目录，强制使二者隔离，即可恢复正常加载校验。

#### 5.4.3 校验常见 Lint 与 Gotchas
1.  **空格格式校验**：CDDA 翻译文案与职业描述中，每个句子结束符号（如 `.`、`?`、`!`）后必须紧跟 **两个半角空格** (`.  `)，否则会触发 Lint 语义校验错误。
2.  **大地图 OMT 属性匹配**：`overmap_terrain` 的 flags 必须严格匹配游戏引擎内部定义的枚举。例如，`SOURCE_WATER` 在高版本中不再有效，应当替换为 `SOURCE_DRINK`。
3.  **Mapgen 矩阵宽度守恒**：在手绘 mapgen rows ASCII 矩阵时，若设定了 24x24 大小，所有行的字符串长度必须精确为 24 字符。添加门窗等特殊字符时需用其**替换**对应位置的墙壁或地面字符，而非插入，以防止行宽溢出到 25 字符。

---

## 6. 其他数据目录

### 6.1 `data/core/`

| 文件 | 说明 |
|------|------|
| `game_balance.json` (15KB) | 核心游戏平衡参数（`EXTERNAL_OPTION`），含 ~80+ 项：饱食/饮水/疲劳速率、体力系统、城市丧尸生成、超地图生成阈值、车辆生成状态等 |
| `world_option_sliders.json` | 世界选项滑块定义 |
| `tips.json` | 加载画面提示语 |
| `damage_indicators.json` | 伤害指示器配置 |
| `sentinels.json` | 哨兵/守卫定义 |
| `weather.json` | 天气基础配置 |
| `traps.json` | 陷阱（核心补充） |

### 6.2 `data/raw/`

| 文件 | 说明 |
|------|------|
| `keybindings.json` (147KB) | ⬆ 完整的键位绑定定义 |
| `colors.json` + `color_themes/` (25 文件) | 颜色主题 |
| `color_templates/` | 颜色模板 |
| `sokoban.txt` | 推箱子谜题关卡 |

### 6.3 `data/motd/`, `data/credits/`, `data/names/`, `data/help/`, `data/font/`

- `motd/`：每日提示（23 个文本文件）
- `credits/`：鸣谢名单（20 个文件）
- `names/`：名称生成数据（人名等）
- `help/`：游戏内帮助文本
- `font/`：字体位图数据 + `fontdata.json`

---

## 7. 数据统计

| 维度 | 数量 |
|------|------|
| `data/json/` 直接 JSON 文件 | ~100 个 |
| `data/json/mapgen/` | 303 个地图文件 |
| `data/json/mapgen_palettes/` | 94 个调色板 |
| `data/json/monsters/` | 59 个怪物文件 |
| `data/json/items/` | 42 个子目录 |
| `data/json/npcs/` | 85 个 NPC 文件 |
| `data/json/furniture_and_terrain/` | 58 个地形/家具文件 |
| `data/mods/` | 51 个 mod |
| 最大单文件 | `recipe_food.json` (350KB, 10512 行) |
| 最大目录 | `mapgen/` (303 文件) |
| JSON type 种类 | ~80+ 种 |

---

## 8. 相关文档

- [时间系统](time_system.md)：时间单位、Speed/Moves 关系
- [战斗系统](combat_system.md)：伤害类型、护甲穿透、命中机制
- [魔法系统](magic_system.md)：法术定义、能量来源、33种法术效果
- [变异与生化改造](mutation_bionic_system.md)：突变类别/阈值、生化模块
- [制作与技能](crafting_system.md)：双轨制技能系统、配方学习、熟练度
- [营养与健康](nutrition_health_system.md)：消化系统、卡路里、维生素
