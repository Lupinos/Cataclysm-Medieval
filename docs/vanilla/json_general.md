# CDDA JSON 依赖关系图

## 一、数据全景：核心 JSON 类型一览

| 层级 | type 值 | 所在目录 | 一句话说明 |
|------|---------|----------|-----------|
| **基础层** | `material` | `materials.json` | 物质材料(铁、棉、凯夫拉等)，被 item/furniture/terrain 引用 |
| **基础层** | `skill` | `skills.json` | 技能定义，被 recipe/profession/monster 引用 |
| **基础层** | `body_part` | `body_parts.json` | 身体部位，被 armor/mutation 引用 |
| **基础层** | `damage_type` | `damage_types.json` | 伤害类型(bash/cut/bullet)，被几乎所有战斗相关类型引用 |
| **基础层** | `flag` | `flags.json` | 全局标志定义，被所有类型引用 |
| **物品层** | `ARMOR/GUN/AMMO/TOOL/COMESTIBLE/BOOK/GENERIC` | `items/` | 各种具体物品定义 |
| **分组层** | `item_group` | `itemgroups/` + 散落各处 | 物品概率池，mapgen/monster_drops 的核心中介 |
| **分组层** | `requirement` | `requirements/` | 配方材料需求的复用模板 |
| **怪物层** | `MONSTER` | `monsters/` | 怪物定义，引用 material/species/harvest/item_group |
| **分组层** | `monstergroup` | `monstergroups/` | 怪物概率池，被 mapgen/overmap 引用 |
| **地形层** | `terrain` | `furniture_and_terrain/terrain-*.json` | 地形定义(墙/地板/门等) |
| **地形层** | `furniture` | `furniture_and_terrain/furniture-*.json` | 家具定义(书架/床/冰箱等) |
| **地图层** | `palette` | `mapgen_palettes/` | 符号→地形/家具/物品的映射模板 |
| **地图层** | `mapgen` | `mapgen/` | 具体地图生成规则(ASCII 矩阵 + 物品放置) |
| **世界层** | `overmap_terrain` | `overmap/overmap_terrain/` | 大地图格子定义 |
| **世界层** | `overmap_special` | `overmap/overmap_special/` | 多格建筑组合(如旅馆 = 多个 overmap_terrain 拼接) |
| **世界层** | `overmap_location` | `overmap/special_locations.json` | 大地图放置条件(forest/field/water等) |
| **配方层** | `recipe` | `recipes/` | 制造配方，引用 item/skill/requirement/tool |
| **配方层** | `construction` | `construction.json` | 建造配方(挖坑/筑墙)，引用 terrain/item/skill |
| **角色层** | `profession` | `hobbies.json` + `professions.json`(item_group) | 职业/爱好，引用 skill/proficiency/item_group |
| **角色层** | `scenario` | `scenarios.json` | 游戏开局场景，引用 start_location/profession |
| **角色层** | `start_location` | `start_locations.json` | 出生点，引用 overmap_terrain |
| **采集层** | `harvest` | `harvest.json` | 采集产出表，被 terrain/monster 引用 |

---

## 二、核心依赖关系图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        基础定义层 (Foundation)                        │
│  material ◄── skill ◄── damage_type ◄── body_part ◄── flag          │
└────────┬────────────────────┬───────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐   ┌──────────────────┐
│    物品层        │   │   怪物层          │
│  ARMOR/GUN/TOOL │   │  MONSTER          │
│  AMMO/COMESTIBLE│   │  ├─ species       │
│  BOOK/GENERIC   │   │  ├─ material      │
│  ├─ material    │   │  ├─ harvest ──────┼──► harvest (产出 item)
│  ├─ flag        │   │  ├─ death_drops ──┼──► item_group
│  ├─ qualities   │   │  └─ special_attacks│
│  └─ techniques  │   └────────┬──────────┘
└───────┬─────────┘            │
        │                      ▼
        │            ┌──────────────────┐
        ├──────────► │   item_group     │ ◄───── monsterdrops (是item_group)
        │            │  (概率分发池)     │
        │            │  ├─ "item": id   │  ← 直接引用 item
        │            │  └─ "group": id  │  ← 嵌套引用其他 item_group
        │            └───────┬──────────┘
        │                    │
        │                    ▼
        │  ┌─────────────────────────────────────────────┐
        │  │              地图生成层 (Mapgen)              │
        │  │                                             │
        │  │  palette ─────► mapgen                      │
        │  │  ├─ terrain      ├─ "rows" (ASCII)          │
        │  │  ├─ furniture    ├─ "place_items" → item_group│
        │  │  └─ items → item_group  ├─ "place_loot"     │
        │  │                  ├─ "place_monster" → monstergroup│
        │  │                  └─ palettes → palette_id   │
        │  └─────────────────────────┬───────────────────┘
        │                            │
        │                            ▼
        │  ┌─────────────────────────────────────────────┐
        │  │              世界层 (Overmap)                 │
        │  │                                             │
        │  │  overmap_terrain ──► overmap_special         │
        │  │       ▲                 ├─ connections       │
        │  │       │                 └─ locations → overmap_location│
        │  │       │                                     │
        │  │  mapgen.om_terrain 绑定 overmap_terrain      │
        │  └─────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│         配方层 (Crafting)          │
│                                   │
│  requirement ◄─── recipe          │
│  ├─ components → item             │    recipe
│  ├─ tools → item                  │    ├─ result → item
│  └─ qualities                     │    ├─ skill_used → skill
│                                   │    ├─ using → requirement
│  construction                     │    ├─ components → item
│  ├─ pre_terrain → terrain         │    ├─ tools → item
│  ├─ post_terrain → terrain        │    └─ book_learn → item(book)
│  └─ components → item             │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│         角色层 (Character)         │
│                                   │
│  scenario                         │
│  ├─ allowed_locs → start_location │
│  └─ missions                      │
│                                   │
│  start_location                   │
│  └─ terrain → overmap_terrain     │
│                                   │
│  profession (含 hobby)            │
│  ├─ skills → skill                │
│  ├─ proficiencies                 │
│  └─ items → item / item_group     │
└───────────────────────────────────┘
```

---

## 三、关键发现：item 的引用方式

### 问题：item 是被直接引用，还是更多通过 item_group 间接引用？

**结论：绝大多数场景通过 item_group 间接引用，直接引用 item id 只在少数明确场景出现。**

| 引用场景 | 引用方式 | 说明 |
|---------|---------|------|
| mapgen `place_items` | `"item": "item_group_id"` | 通过 item_group 名称引用，不是直接的 item id |
| mapgen `place_loot` | `"group": "xxx"` 或 `"item": "item_id"` | 两者皆可，但 group 更常见 |
| palette `items` | `"item": "item_group_id"` | 这里的 "item" 键实际指的是 item_group！ |
| monster `death_drops` | `"groups": [["item_group_id", prob]]` | 通过 item_group 引用 |
| item_group 内部 | `"item": "actual_item_id"` | **真正直接引用 item id 的地方** |
| item_group 内部 | `"group": "other_group_id"` | 嵌套引用其他 item_group |
| recipe `components` | `[["item_id", count]]` | **直接引用 item id** |
| recipe `tools` | `[["item_id", charges]]` | **直接引用 item id** |
| construction `components` | `[["item_id", count]]` | **直接引用 item id** |
| furniture `deconstruct/bash` | `"item": "item_id"` | **直接引用 item id** |

### 核心结论

```
item 的"消费者"大致分两派：

1. 【间接派 - 通过 item_group】(占大多数场景)
   mapgen/palette/monster_drops/profession → item_group → item

2. 【直接派】(配方/建造/拆解场景)
   recipe/construction/furniture.bash → 直接引用 item id
```

---

## 四、item_group 的核心地位

item_group 是 CDDA 数据系统中最重要的**中间层/胶水层**：

```
                ┌── mapgen (地图上刷什么)
                ├── palette (家具里放什么)
item_group ◄────┼── monster death_drops (怪物掉什么)
                ├── profession items (开局带什么)
                └── NPC shop (商人卖什么)

                ┌── "item": "xxx" (直接包含 item)
item_group 内部 ─┤
                └── "group": "xxx" (嵌套其他 item_group)
```

### item_group 的两种子类型

| subtype | 行为 | 类比 |
|---------|------|------|
| `distribution` | 从列表中**随机选一个**（按概率） | 抽奖机 - 抽一次 |
| `collection` | 列表中**每个都独立判定**是否出现 | 购物清单 - 每个可能买 |

### item_group 的嵌套深度

实际数据显示 item_group 会多层嵌套：

```
default_zombie_clothes (collection)
  └─ group: "coats_unisex"
  └─ group: "common_gloves"  
  └─ distribution:
       └─ collection:
            └─ distribution:
                 └─ group: "male_underwear"
            └─ group: "pants_male"
            └─ group: "shirts_unisex"
```

这种设计使得"一个丧尸穿什么衣服"可以非常精细地分层控制性别/季节/职业的差异。

---

## 五、monstergroup 与 item_group 的对称性

| 维度 | item_group | monstergroup |
|------|-----------|--------------|
| 作用 | 定义"物品池" | 定义"怪物池" |
| 被谁引用 | mapgen/palette/death_drops | mapgen/overmap_terrain |
| 内部条目 | `"item": id` / `"group": id` | `"monster": id` / `"group": id` |
| 概率控制 | `prob` | `weight` |
| 嵌套 | 支持 | 支持 |

---

## 六、地图生成的完整引用链

一个地点从"世界生成"到"玩家看到具体物品"的完整链路：

```
overmap_special (如 "Motel")
  └─ 引用多个 overmap_terrain (如 "motel_entrance_north")
       └─ mapgen (om_terrain = "motel_entrance_north")
            ├─ palettes → palette_id
            │    ├─ terrain: 符号 → terrain_id (如 "#" → "t_wall_w")
            │    ├─ furniture: 符号 → furniture_id (如 "@" → "f_bed") 
            │    └─ items: 符号 → item_group_id (如 "d" → "SUS_dresser_mens")
            ├─ place_items / place_loot → item_group_id
            ├─ place_monster → monstergroup_id
            └─ rows: ASCII 地图矩阵
```

**示意：一个银行的生成**
```
overmap_special
  → overmap_terrain "bank"
    → mapgen (bank.json)
      → terrain: "$" = "t_metal_floor", "R" = "t_wall_metal"
      → furniture: "$" = "f_safe_l", "T" = "f_table"
      → place_items: "vault" (item_group) → 金币/珠宝等
      → place_items: "office" (item_group) → 办公用品
```

---

## 七、copy-from 继承机制

CDDA 大量使用 `copy-from` 实现"继承"：

```json
{
  "type": "overmap_terrain",
  "abstract": "generic_city_building",    // 抽象基类
  "sym": "^",
  "see_cost": 5
}

{
  "type": "overmap_terrain",
  "id": "bank",
  "copy-from": "generic_city_building",   // 继承
  "name": "bank",
  "color": "light_gray"
}
```

同样适用于 item、monster、material 等所有类型，形成类似 OOP 的继承树。

---

## 八、总结：依赖方向一图流

```
scenario → start_location → overmap_terrain ← overmap_special
                                    ↑
profession → item_group ──────► mapgen ← palette
     ↓            ↑                ↑        ├─ terrain
   skill     item (物品)      monstergroup  ├─ furniture
                ↑                  ↑        └─ item_group
           material            MONSTER
                              ├─ species
                              ├─ harvest → item
                              └─ death_drops → item_group → item

recipe → item (result)
  ├─ skill
  ├─ requirement → item (components/tools)
  └─ components → item
```

**核心设计哲学：**
1. **item 是最底层的原子单位**，极少被最终消费者直接引用
2. **item_group 是万能胶水**，在 item 和所有"需要物品"的场景之间做概率化桥接
3. **palette 是地图的复用模板**，避免每个 mapgen 重复定义符号映射
4. **monstergroup 对应怪物领域**，与 item_group 形成对称设计
5. **copy-from 提供继承**，减少重复定义
