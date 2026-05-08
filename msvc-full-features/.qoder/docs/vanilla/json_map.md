# CDDA 地图体系：从世界生成到可见地块的完整管线

## 一、总览：地图的四个尺度层级

```
┌──────────────────────────────────────────────────────────────────────┐
│  尺度1: Overmap (180x180 格, 每格 = 24x24 地块)                       │
│  "世界地图" - 玩家按 m 键看到的大地图                                   │
│  每一格 = 1个 overmap_terrain                                         │
├──────────────────────────────────────────────────────────────────────┤
│  尺度2: Mapgen (24x24 地块)                                           │
│  "一个建筑/一块地" - 一个 overmap_terrain 对应的实际地图内容              │
│  由 ASCII 矩阵 + palette 定义                                         │
├──────────────────────────────────────────────────────────────────────┤
│  尺度3: Tile (单个地块, 1x1)                                          │
│  "一块砖" - 由 terrain + furniture 两层叠加构成                         │
│  terrain: 地板/墙壁/水  |  furniture: 桌子/床/书架                      │
├──────────────────────────────────────────────────────────────────────┤
│  尺度4: Content (地块上的内容)                                         │
│  物品(items) + 怪物(monsters) + 载具(vehicles) + NPC                   │
└──────────────────────────────────────────────────────────────────────┘
```

**换算关系：**
- 1 个 overmap 格 = 24x24 = 576 个地块 (tile)
- 1 个 overmap (完整大地图) = 180x180 个 overmap 格 = ~18.7 百万个地块
- Z轴：从 -10 到 +10 共 21 层

---

## 二、尺度1: Overmap 世界地图层

### 2.1 世界地图是怎么铺出来的

```
region_settings (区域设定)
  │
  ├── 1. 自然地形噪声填充
  │     地图大部分面积是由 Perlin 噪声 + 阈值 生成的自然地形：
  │     noise < 0.2  → field (空地)
  │     noise 0.2~0.25 → forest (森林)
  │     noise > 0.25 → forest_thick (密林)
  │     特殊区域: 河流/湖泊/沼泽/海洋 (用单独的噪声设定)
  │
  ├── 2. 城市生成
  │     在世界地图上放置 N 个城市中心
  │     城市有 size 参数，决定建筑分布密度
  │     城市内部用 city_building 和 overmap_special 填充
  │
  ├── 3. 道路网络连接
  │     overmap_connection 定义道路如何铺设：
  │     城市之间用 local_road 连接
  │     穿越不同地形有不同 cost (森林贵, 空地便宜)
  │
  ├── 4. 特殊建筑放置 (overmap_special)
  │     按 occurrences / city_distance / locations 条件散落
  │     如：军事基地(远离城市)、加油站(沿路)、实验室(地下)
  │
  └── 5. Map Extras 叠加
        在已有地形上随机叠加事件：
        坠毁直升机、毒品交易现场、路障、陨石坑等
```

### 2.2 关键数据类型

| 类型 | 文件位置 | 作用 |
|------|---------|------|
| `region_settings` | `regional_map_settings.json` | 全局参数：噪声阈值、树种分布、城市密度等 |
| `overmap_terrain` | `overmap/overmap_terrain/` | 大地图上每一格的定义（名称/符号/颜色/标志） |
| `overmap_special` | `overmap/overmap_special/` | 多格建筑组合（旅馆/核电站/实验室） |
| `city_building` | `overmap/multitile_city_buildings.json` | 城市内建筑（多层住宅/商店） |
| `overmap_connection` | `overmap/overmap_connections.json` | 道路/下水道/地铁的铺设规则 |
| `overmap_location` | `overmap/special_locations.json` | 放置条件（land/water/forest等） |
| `map_extra` | `overmap/map_extras.json` | 随机事件叠加层 |

### 2.3 overmap_terrain 的结构

```json
{
  "type": "overmap_terrain",
  "id": "s_gas",                    // 唯一标识，mapgen 通过这个绑定
  "name": "gas station",            // 玩家看到的名称
  "sym": "G",                       // 大地图上显示的字符
  "color": "light_blue",            // 大地图上的颜色
  "see_cost": 5,                    // 远处能否看到（数值越低越容易发现）
  "extras": "build",                // 可叠加的 map_extra 类别
  "mondensity": 2,                  // 怪物密度
  "flags": ["SIDEWALK", "SOURCE_FUEL"]  // 标志（有人行道/有燃料）
}
```

### 2.4 overmap_special 的结构（多格建筑）

```json
{
  "type": "overmap_special",
  "id": "Motel",
  "overmaps": [
    { "point": [0, 0, 0], "overmap": "motel_entrance_north" },   // 地面层
    { "point": [1, 0, 0], "overmap": "motel_1_north" },          // 地面层右侧
    { "point": [0, 0, 1], "overmap": "motel_entrance_roof_north" } // 屋顶层
  ],
  "connections": [
    { "point": [2, 0, 0], "terrain": "road", "connection": "local_road" }
  ],
  "locations": ["land"],            // 只放在陆地上
  "city_distance": [8, 30],         // 距城市 8~30 格
  "occurrences": [1, 2]             // 整个地图上出现 1~2 次
}
```

### 2.5 city_building 的结构（城市建筑）

与 overmap_special 类似，但专门在城市内部生成：

```json
{
  "type": "city_building",
  "id": "2storyModern01",
  "locations": ["land"],
  "overmaps": [
    { "point": [0, 0, -1], "overmap": "2storyModern01_basement_north" },
    { "point": [0, 0, 0], "overmap": "2storyModern01_first_north" },
    { "point": [0, 0, 1], "overmap": "2storyModern01_second_north" },
    { "point": [0, 0, 2], "overmap": "2storyModern01_roof_north" }
  ]
}
```

**注意 Z 轴：** point 的第三个值是 Z 坐标：
- `-1` = 地下室
- `0` = 地面层
- `1` = 二楼
- `2` = 屋顶

---

## 三、尺度2: Mapgen 地图生成层

### 3.1 mapgen 是什么

每一个 `overmap_terrain` 必须有对应的 `mapgen` 定义，告诉游戏"这一格 24x24 的地块具体长什么样"。

```json
{
  "type": "mapgen",
  "method": "json",
  "om_terrain": "house_01",        // 绑定到哪个 overmap_terrain
  "weight": 100,                   // 如果有多个 mapgen 绑同一个 om_terrain，按权重随机选
  "object": { ... }                // 实际的地图数据
}
```

### 3.2 mapgen object 的核心结构

```json
"object": {
  "fill_ter": "t_floor",           // 整个 24x24 的默认地形填充

  "rows": [                        // 24行 x 24列 的 ASCII 矩阵
    ".%.``````p..............",      // 每个字符 = 1个地块
    ".%#~~~~~~##o##*##oo##...",      // '#' = 墙, 'o' = 窗, '.' = 室外地面
    ...                             // 共 24 行
  ],

  "palettes": ["domestic_general_and_variant_palette"],  // 引用调色板

  "terrain": {                     // 本地符号→地形映射（覆盖 palette）
    "%": ["t_region_shrub", "t_region_shrub_fruit"],
    "#": "t_wall_wood",
    "~": "t_thconc_floor"
  },

  "furniture": {                   // 本地符号→家具映射
    "!": "f_region_flower"
  },

  "place_items": [...],            // 在坐标范围放置 item_group
  "place_loot": [...],             // 放置物品/物品组
  "place_monsters": [...],         // 放置 monstergroup
  "place_vehicles": [...],         // 放置车辆
  "place_nested": [...]            // 放置嵌套子地图
}
```

### 3.3 palette 调色板系统

palette 是 mapgen 的**复用引擎**——同样的符号映射可以被上百个 house 共用：

```json
{
  "type": "palette",
  "id": "standard_domestic_palette",

  "parameters": {                  // 参数化！每次使用可以不同
    "interior_wall_type": {
      "type": "ter_str_id",
      "default": {
        "distribution": [          // 随机选一种内墙颜色
          ["t_wall_w", 6],         // 白墙概率最高
          ["t_wall_b", 1],         // 蓝墙
          ["t_wall_p", 1],         // 粉墙
          ["t_wall_y", 1]          // 黄墙
        ]
      }
    }
  },

  "terrain": {                     // 符号→地形映射
    ".": "t_floor",
    "#": "t_wall_w",
    "+": "t_door_c",
    "o": "t_window_domestic"
  },

  "furniture": {                   // 符号→家具映射
    "@": "f_bed",
    "R": "f_bookcase",
    "F": "f_fridge"
  },

  "items": {                       // 符号→物品映射 (引用 item_group!)
    "F": { "item": "SUS_fridge", "chance": 80 },
    "R": { "item": "bedroom", "chance": 20 }
  },

  "toilets": { "t": {} },         // 符号→马桶（特殊处理，自带水）
  "liquids": { ... }              // 符号→液体
}
```

**palette 的继承与变体：**
```
domestic_general_and_variant_palette
  └── 按概率分发到：
      ├── standard_domestic_palette (95% 正常住宅)
      ├── standard_domestic_abandoned_palette (2.8% 废弃住宅)
      ├── house_survivor_palette (1.8% 幸存者住宅)
      └── house_hoarder_palette (0.4% 囤积者住宅)
```

这意味着同一套 house mapgen，仅通过 palette 切换就能产出 4 种完全不同风格的住宅！

### 3.4 嵌套地图 (Nested Mapgen)

小尺寸的可复用模块，可被嵌入到主 mapgen 中：

```json
// 定义一个 4x4 的卧室模块
{
  "type": "mapgen",
  "method": "json",
  "nested_mapgen_id": "bedroom_4x4_adult_1_N",
  "object": {
    "mapgensize": [4, 4],         // 不是 24x24，而是 4x4！
    "rotation": [0, 3],           // 可随机旋转 0~3 次（0°/90°/180°/270°）
    "rows": [
      "LEEL",
      " EE ",
      "y   ",
      "O   "
    ],
    "palettes": ["house_w_nest_palette"]
  }
}
```

**在主 mapgen 中嵌入：**
```json
"place_nested": [
  {
    "chunks": [
      ["roof_6x6_garden_4", 15],
      ["shed_6x6_junk", 15],
      ["firepit_5x5_1", 15],
      ["playset_4x4_1", 15]
    ],
    "x": [4, 13],                  // 放置区域 x 范围
    "y": 17                        // 放置区域 y 坐标
  }
]
```

**作用：** 让后院可以随机出现花园/棚屋/火坑/游乐设施等，每次游玩不同。

### 3.5 同一个 om_terrain 的多变体

```json
// 变体1: 正常住宅 (weight 100)
{ "type": "mapgen", "om_terrain": "house_01", "weight": 100, "object": { ... } }

// 变体2: 废弃住宅 (weight 20)  
{ "type": "mapgen", "om_terrain": "house_01", "weight": 20, "object": { ... } }
```

游戏生成时按 weight 比例随机选择 → 同一个"house_01"地块，有 83% 概率是正常住宅，17% 概率是废弃版本。

---

## 四、尺度3: Terrain + Furniture 地块层

### 4.1 每个地块 = terrain + furniture 的叠加

```
一个地块的视觉 = terrain（底层） + furniture（表层）

例: 厨房地板上放着冰箱
  terrain: t_linoleum_white (白色油布地面)
  furniture: f_fridge (冰箱)

例: 草地上的篝火
  terrain: t_grass (草地)
  furniture: f_campfire (篝火)

例: 单纯的墙壁
  terrain: t_wall_w (白墙)
  furniture: (无)
```

### 4.2 terrain 的属性

```json
{
  "type": "terrain",
  "id": "t_wall_w",
  "name": "white wall",
  "symbol": "|",                   // 在游戏中显示的字符
  "color": "white",                // 字符颜色
  "move_cost": 0,                  // 0 = 不可通过
  "flags": ["FLAMMABLE", "NOITEM", "SUPPORTS_ROOF", "WALL", "CONNECT_WITH_WALL"],
  "bash": { "str_min": 40, "str_max": 100, ... },  // 被砸毁需要的力量
  "deconstruct": { "ter_set": "t_floor", "items": [...] }  // 拆解产物
}
```

### 4.3 furniture 的属性

```json
{
  "type": "furniture",
  "id": "f_bookcase",
  "name": "bookcase",
  "symbol": "{",
  "color": "brown",
  "move_cost_mod": -1,             // -1 = 不可通过
  "coverage": 80,                  // 提供 80% 掩体
  "max_volume": "2000 L",          // 可存储 2000L 物品
  "flags": ["FLAMMABLE", "PLACE_ITEM", "ORGANIC"],
  "deconstruct": { "items": [{"item": "2x4", "count": 12}, ...] },
  "bash": { ... }
}
```

### 4.4 region_terrain：区域化随机地形

CDDA 的一大特色是 **`t_region_*` 和 `f_region_*`** —— 伪地形/伪家具 ID：

```json
// 这不是一个具体地形，而是一个"概率池"
"t_region_tree_forest": {
  "t_tree": 18,
  "t_tree_hickory": 18,
  "t_tree_pine": 9,
  "t_tree_maple": 7,
  "t_tree_birch": 7,
  ...
}
```

在 mapgen 中写 `"t_region_tree_forest"` → 游戏实际放置时会按权重随机选一种真实树木。

**好处：** 同一个森林 mapgen 每次生成的树种组合都不同，而且不同 region（例如沙漠 mod）可以覆盖这些定义来改变植被。

---

## 五、尺度4: 内容放置层

### 5.1 物品放置

```json
// 方式1: place_items (在坐标区域放 item_group)
"place_items": [
  { "item": "office", "x": [4, 9], "y": 8, "chance": 30 }
]

// 方式2: place_loot (更灵活)
"place_loot": [
  { "group": "cash_register_random", "x": 21, "y": 13 },
  { "item": "television", "x": 7, "y": 10, "chance": 100 }
]

// 方式3: palette 中的 items 映射（最常用）
"items": {
  "F": { "item": "SUS_fridge", "chance": 80 },
  "d": { "item": "SUS_dresser_mens", "chance": 50 }
}
```

### 5.2 怪物放置

```json
"place_monsters": [
  { "monster": "GROUP_ZOMBIE", "x": [3, 20], "y": [3, 20] }
]
```

或在 overmap_terrain 级别通过 `mondensity` 全局控制。

### 5.3 车辆放置

```json
"place_vehicles": [
  { "vehicle": "car", "x": 12, "y": 5, "chance": 50, "rotation": 90 }
]
```

---

## 六、完整流程：从 0 构建一个"加油站"

### 场景：玩家在大地图上看到一个加油站，走进去看到具体内容

**第1步：世界生成时**

```
region_settings 
  → 在城市边缘沿路放置 overmap_special
  → overmap_special "Gas_Station" 选中了一个合适位置
  → 在大地图上填入 overmap_terrain "s_gas"
```

**第2步：overmap_terrain 定义**

```json
// 玩家在大地图上看到:  符号 "G"  颜色 light_blue  名字 "gas station"
{
  "id": "s_gas",
  "name": "gas station",
  "sym": "G",
  "color": "light_blue",
  "mondensity": 2,
  "flags": ["SOURCE_FUEL", "SOURCE_VEHICLES"]
}
```

**第3步：玩家接近/进入时，触发 mapgen**

```json
{
  "type": "mapgen",
  "om_terrain": "s_gas",          // 绑定到 s_gas
  "weight": 100,
  "object": {
    "fill_ter": "t_pavement",      // 24x24 全铺水泥地
    "rows": [
      "ssssssssssssssssssssssss",
      "s####o##+##o####........",  // # = 墙, o = 窗, + = 门
      "s#FJ.........C#........",  // F = 冰箱, J = 柜台, C = 椅子
      ...
    ],
    "terrain": { "#": "t_wall_w", "+": "t_door_glass_c", ... },
    "furniture": { "F": "f_glass_fridge", "J": "f_counter", ... },
    "items": {
      "F": { "item": "fridgesnacks", "chance": 80 },
      "J": { "item": "behindcounter", "chance": 70 }
    },
    "place_vehicles": [
      { "vehicle": "fuel_pump", "x": 15, "y": 12 }
    ]
  }
}
```

**第4步：游戏解析 mapgen → 生成 576 个具体地块**

```
对每个字符位置 (x, y):
  1. 查 terrain 映射 → 确定 terrain (如 "#" → t_wall_w)
  2. 查 furniture 映射 → 确定 furniture (如 "F" → f_glass_fridge)
  3. 查 items 映射 → 从 item_group "fridgesnacks" 按概率生成物品
  4. 处理 region 替换 → "t_region_shrub" → 具体灌木种类
  5. 放置 vehicles / monsters / nested chunks
```

**第5步：玩家最终看到**

```
在屏幕上看到一个 24x24 的地图片段：
- 灰色方块 = 水泥地面
- 白色竖线 = 墙壁
- 绿色字符 = 灌木
- 棕色花括号 = 货架(内有商品)
- 蓝色方块 = 冰箱(内有饮料)
- 'Z' = 丧尸(由 mondensity 或 place_monsters 生成)
```

---

## 七、自然地形的特殊生成：forest_mapgen_settings

森林/沼泽/河流等自然地形不使用 ASCII 矩阵，而是用**程序化组件系统**：

```json
"forest_mapgen_settings": {
  "forest": {
    "groundcover": { "t_region_groundcover_forest": 1 },  // 底层铺设
    "components": {
      "trees": {
        "sequence": 0,           // 先放树
        "chance": 12,            // 每格 1/12 概率放树
        "types": { "t_region_tree_forest": 128, "t_tree_young": 32 }
      },
      "shrubs_and_flowers": {
        "sequence": 1,           // 再放灌木
        "chance": 10,
        "types": { "t_region_shrub_forest": 120, "f_region_forest": 10 }
      },
      "clutter": {
        "sequence": 2,           // 最后放杂物
        "chance": 80,
        "types": { "t_trunk": 128, "f_boulder_small": 128, "t_pit": 1 }
      }
    }
  }
}
```

**生成流程：**
```
1. 整个 24x24 铺上 groundcover (森林地面)
2. 遍历每格，1/12 概率放一棵树 (从 region_tree 池随机选种)
3. 再遍历，1/10 概率放灌木/花
4. 再遍历，1/80 概率放树桩/石头等杂物
```

---

## 八、Z轴与多层建筑

### 8.1 Z轴的组织方式

```
Z = +10  (最高天空)
Z = +2   屋顶
Z = +1   二楼
Z = 0    地面 (主要游玩层)
Z = -1   地下室 / 下水道
Z = -2   地铁 / 实验室上层
Z = -5   实验室深处
Z = -10  (最深地下)
```

### 8.2 多层建筑在 overmap 上的表达

```json
// 一栋2层现代住宅在 overmap 上占据:
{
  "overmaps": [
    { "point": [0, 0, -1], "overmap": "house_basement_north" },  // Z-1 地下室
    { "point": [0, 0, 0],  "overmap": "house_first_north" },     // Z0  一楼
    { "point": [0, 0, 1],  "overmap": "house_second_north" },    // Z1  二楼
    { "point": [0, 0, 2],  "overmap": "house_roof_north" }       // Z2  屋顶
  ]
}
```

每一层都有独立的 mapgen (独立的 24x24 ASCII 图)，通过楼梯/梯子连接。

---

## 九、Map Extras: 事后叠加层

在正常地图生成完成后，可以叠加随机事件：

```json
{
  "type": "map_extra",
  "id": "mx_crater",
  "name": "Crater",
  "generator": { "generator_method": "update_mapgen", "generator_id": "mx_crater" },
  "min_max_zlevel": [0, 0]
}
```

**工作方式：**
1. 正常 mapgen 先生成完整地图
2. `update_mapgen` 在其上"覆写"部分内容（如炸出一个坑）
3. 不替换整个地图，只修改局部

**常见 map_extras：** 坠毁直升机、毒品交易、路障、集体坟墓、军事检查站等。

---

## 十、完整管线图

```
┌─────────────────────────────────────────────────────────────────┐
│                    世界生成阶段                                    │
│                                                                 │
│  region_settings                                                │
│    ├── Perlin噪声 → 自然地形铺设 (field/forest/river)              │
│    ├── 城市放置 → city_building 填充                              │
│    ├── overmap_special 散布 → 特殊建筑放置                        │
│    ├── overmap_connection → 道路/地铁连接                         │
│    └── map_extras 概率标记 → 随机事件位置                         │
│                                                                 │
│  结果: 一张完整的 180x180 x 21层 的 overmap_terrain 网格           │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    地图实例化阶段 (玩家接近时)                      │
│                                                                 │
│  overmap_terrain id                                             │
│    │                                                            │
│    ├── [建筑地形] → 查找 mapgen (om_terrain = id)                 │
│    │     ├── 按 weight 选一个 mapgen                             │
│    │     ├── 解析 ASCII rows                                     │
│    │     ├── 应用 palette (符号→terrain/furniture/items)           │
│    │     ├── 执行 place_nested (嵌入子模块)                       │
│    │     ├── 执行 place_items / place_loot                       │
│    │     ├── 执行 place_monsters / place_vehicles                │
│    │     └── 如有 map_extra → 执行 update_mapgen 覆写             │
│    │                                                            │
│    └── [自然地形] → 使用 forest_mapgen_settings 程序化生成          │
│          ├── 铺 groundcover                                      │
│          ├── 按概率放 trees                                       │
│          ├── 按概率放 shrubs                                      │
│          └── 按概率放 clutter                                     │
│                                                                 │
│  结果: 576 个具体的 (terrain + furniture + items + monsters)       │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    渲染阶段 (玩家看到)                             │
│                                                                 │
│  对每个地块 (x, y, z):                                           │
│    显示 terrain.symbol (底层)                                     │
│    覆盖 furniture.symbol (如有)                                   │
│    覆盖 item 图标 (如有物品在地上)                                  │
│    覆盖 monster 图标 (如有怪物)                                    │
│    覆盖 vehicle part 图标 (如有载具)                               │
│                                                                 │
│  结果: 玩家看到一个有意义的、充满细节的游戏画面                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 十一、关键设计模式总结

| 模式 | 机制 | 效果 |
|------|------|------|
| **palette 复用** | 100+ 个 house mapgen 共用 domestic_palette | 减少重复，统一风格 |
| **palette 变体** | palette 内部按概率分发到不同子 palette | 同一布局产出废弃/正常/幸存者版本 |
| **参数化 palette** | `parameters` + `distribution` | 墙色/围栏类型每栋房子随机不同 |
| **region 替换** | `t_region_tree` 等伪 ID | 同一 mapgen 在不同生态区产出不同植被 |
| **weight 多变体** | 同 om_terrain 多个 mapgen | 同一"类型"的建筑有多种完全不同的布局 |
| **nested 模块化** | 4x4~6x6 的小 mapgen 嵌入 | 后院/卧室/屋顶花园随机组合 |
| **Z轴叠层** | city_building 的 point z 坐标 | 多层建筑，地下室到屋顶完整 |
| **map_extras 覆写** | update_mapgen 事后修改 | 在已生成的地图上叠加随机事件 |
| **程序化自然** | forest_mapgen_settings | 不需手绘，自动生成自然感森林 |
