# 城市/城镇生成系统

> 调查日期：2026-05-04 — 为制作中世纪村庄/城镇做准备。

---

## 1. 总体架构

城市生成是 overmap 生成流程中的一个环节，完全由 **C++ 硬编码**，几乎没有 JSON 侧的可配置性（建筑类型除外）。

```
overmap::generate()
  ├── calculate_urbanity() / calculate_forestosity()
  ├── place_rivers()
  ├── place_lakes() / place_oceans()
  ├── place_forests() / place_swamps()
  ├── place_cities()          ← 城市核心入口
  │     ├── 决定城市数量/大小
  │     ├── 放置十字路口种子 (oter_road_nesw)
  │     └── build_city_street() ×4方向  ← 递归展开
  │           ├── 铺设道路 (overmap_connection "local_road")
  │           ├── 分岔子道路 (左右随机)
  │           └── place_building()  ← 沿路放置建筑
  │                 └── pick_random_building_to_place()
  │                       ├── 店铺 (pick_shop)
  │                       ├── 公园 (pick_park)
  │                       └── 住宅 (pick_house)
  ├── place_roads()           ← 城市间道路连接
  ├── place_specials()        ← 独立特殊地点(实验室、军事基地等，非城市建筑)
  └── place_mongroups()       ← 城市怪物群生成
```

## 2. 核心数据结构

### 2.1 `city` 结构体 (`src/city.h`)

```cpp
struct city {
    city_id id;              // JSON 定义的固定城市 ID（可选）
    point_abs_om pos_om;     // 所在 overmap 的绝对坐标
    point_om_omt pos;        // 城市中心在 overmap 内的 OMT 坐标
    int population = 0;      // 原始人口
    int size = -1;           // 城市半径 (OMT 单位，约等于街道长度)
    std::string name;        // 城市名称
};
```

- `size` 是城市半径，决定街道延伸多远，也决定建筑数量
- `size = 1` 只是一个十字路口，没有建筑

### 2.2 `city_settings` 结构体 (`src/regional_settings.h`)

```cpp
struct city_settings {
    int shop_radius = 30;    // 距市中心多远开始放店铺（归一化 0-100）
    int shop_sigma = 20;     // 正态分布 σ
    int park_radius = 30;    // 距市中心多远开始放公园
    int park_sigma = 70;     // 正态分布 σ（默认更大，让公园扩散到全城）

    building_bin houses;     // 住宅建筑池 (weighted_int_list<overmap_special_id>)
    building_bin shops;      // 商店建筑池
    building_bin parks;      // 公园/空地池
};
```

### 2.3 `city_building` JSON 类型

定义可放置在城市场地上的建筑模板（实际存为 `overmap_special`，加载时通过 `city_building` 类型区分）：

```json
{
  "type": "city_building",
  "id": "bungalow01",
  "locations": [ "land" ],
  "overmaps": [
    { "point": [ 0, 0, 0 ], "overmap": "bungalow01_1_north" },
    { "point": [ 0, 0, 1 ], "overmap": "bungalow01_roof_north" }
  ]
}
```

关键特征：
- **1 个 `city_building` = 1 OMT 宽**（大多数情况），紧贴道路放置
- 可能有多层（z-level 0, 1, 屋顶）
- 文件位置：`data/json/overmap/multitile_city_buildings.json`（5247行，含数百种建筑模板）

## 3. `place_cities()` 详细流程

位置：`src/overmap.cpp` 行 5419-5538

### 3.1 参数来源

| 参数 | 来源 | 说明 |
|------|------|------|
| `op_city_size` | 游戏选项 `CITY_SIZE` | 基础城市尺寸（默认 4） |
| `op_city_spacing` | 游戏选项 `CITY_SPACING` | 城市间距（默认 4，对应 6% 覆盖率） |
| `max_urbanity` | 游戏选项 `OVERMAP_MAXIMUM_URBANITY` | 最大城市密度倍数 |
| `urbanity` | 本次 overmap 计算值 | 基于预期城市化和邻居 overmap 的城市数量 |
| `forestosity` | 本次 overmap 计算值 | 森林覆盖率，越多森林 → 城市越少越大间距 |

### 3.2 城市数量计算

```
city_map_coverage_ratio = 1 / 2^op_city_spacing
omts_per_city = (op_city_size × 2 + 1) × (max_city_size × 2 + 1) × 3/4
num_cities = round(omts_per_overmap × city_map_coverage_ratio / omts_per_city)
```

间距与覆盖率对照表（OMAPX=OMAPY=180）：

| spacing | 覆盖率 | size=4 城市数 | size=8 城市数 |
|---------|--------|--------------|--------------|
| 0       | ~99%   | 506          | 126          |
| 2       | 25%    | 126          | 31           |
| 4 (默认)| 6%     | 31           | 7            |
| 6       | 1%     | 7            | 1            |

### 3.3 两种城市定位模式

**模式 A：随机城市（默认）**
- 触发条件：没有 JSON 定义的 `city` 条目（`city::get_all().empty()`）
- 随机选 `num_cities` 个位置，验证是否在默认地形上（`settings->default_oter`）
- 城市大小随机：33% tiny(×1/3), 33% small(×2/3), 17% large(×3/2), 17% huge(×2)
- 最小 size=2

**模式 B：JSON 预定义城市**
- 触发条件：JSON 中存在 `"type": "city"` 条目
- 按 JSON 中指定的 `pos` 和 `size` 放置
- 不再随机生成额外城市

### 3.4 城市展开

每个城市从十字路口开始，向 4 个方向递归调用 `build_city_street()`：

```cpp
do {
    build_city_street(local_road, tmp.pos, tmp.size, cur_dir, tmp);
} while ((cur_dir = turn_right(cur_dir)) != start_dir);
```

## 4. `build_city_street()` — 街道递归铺设

位置：`src/overmap.cpp` 行 5588-5665

```
build_city_street(connection, pos, cs, dir, town)
  cs = 剩余步数 (初始 = city.size)
  │
  ├── lay_out_street() → 规划街道路径
  ├── build_connection() → 铺设 "local_road" 道路 (OMT级别)
  │
  ├── [沿路径每步]: 
  │     ├── c >= 2 时，随机分岔：
  │     │     left = cs - rng(1,3)
  │     │     right = cs - rng(1,3)
  │     │     → build_city_street(left, turn_left)   // 递归左岔
  │     │     → build_city_street(right, turn_right)  // 递归右岔
  │     │
  │     ├── 3/4 概率 (BUILDINGCHANCE=4) 放置左侧建筑
  │     └── 3/4 概率 放置右侧建筑
  │
  └── [到达终点时]: cs >= 2 时随机拐弯继续延伸
```

关键参数：
- `BUILDINGCHANCE = 4`（`overmap.cpp:150`）→ 每个路边位置 75%(=1-1/4) 概率放置建筑
- `block_width` 交替在 2 和 rng(3,5) 之间切换
- 分岔长度随机减少 1-3 步，模拟自然街道长短不一

## 5. `place_building()` — 建筑选择与放置

位置：`src/overmap.cpp` 行 5570-5586

```cpp
void overmap::place_building(tripoint_om_omt p, direction dir, city &town) {
    building_pos = p + displace(dir);  // 道路旁边一格
    town_dist = (distance_to_center * 100) / max(town.size, 1);  // 归一化 0-100
    
    for (10次重试) {
        building = pick_random_building_to_place(town_dist);
        if (can_place_special(building, ...)) {
            place_special(building, ...);
            break;
        }
    }
}
```

### 5.1 `pick_random_building_to_place()` — 建筑类型选择

基于到市中心的归一化距离（0-100）决定放什么：

```
shop_normal = normal_roll(shop_radius, shop_sigma)  // 默认 μ=30, σ=20
park_normal = normal_roll(park_radius, park_sigma)   // 默认 μ=30, σ=70

if (shop_normal > town_dist) → pick_shop()     // 市中心附近 → 商店
else if (park_normal > town_dist) → pick_park() // 中等距离 → 公园
else → pick_house()                              // 远距离 → 住宅
```

正态分布效果：
- **商店**集中在市中心（μ=30, σ=20）
- **公园**分布更均匀（μ=30, σ=70）
- **住宅**占据城市外围

### 5.2 建筑池来源

建筑池定义在 `regional_settings` JSON 中（`data/json/regional_map_settings.json` 行 830-1060+）：

```json
"city_spec": {
  "shop_radius": 30,
  "park_radius": 20,
  "houses": {
    "2storyModern01": 500,     // 权重 500
    "bungalow01": 300,         // 权重 300
    ...
  },
  "parks": {
    "park": 400,
    "pool": 100,
    ...
  },
  "shops": {
    "s_gas": 500,
    "s_grocery": 600,
    ...
  }
}
```

注意：
- 这些 `city_building` 在加载阶段被转换为 `overmap_special`，加入对应的 `building_bin`
- Mod 可以通过 `region_overlay` 或直接覆盖 `regional_map_settings` 来修改建筑池

## 6. 道路系统

### 6.1 城市内部道路

- 使用 `overmap_connection` 类型 `"local_road"`
- 城市内所有街道都是 `local_road` 连接
- 在 `overmap.cpp:137` 硬编码引用：
  ```cpp
  static const overmap_connection_id overmap_connection_local_road("local_road");
  ```

### 6.2 城市间道路 (`place_roads()`)

位置：`src/overmap.cpp` 行 5091-5162

- 收集所有城市中心点 → `road_points`
- 使用 `connect_closest_points()` 连接 → 铺设 `local_road`
- 同样受 `CITY_SIZE` 控制（size≤0 则不生成道路）

## 7. 怪物群 (`place_mongroups()`)

城市生成后，最后的 `place_mongroups()` 阶段（`overmap.cpp` 行 5364-5407）：

```
对每个城市:
  mongroup radius = city_size * 2.5    (OMT 单位)
  mongroup population = city_size * 80  (怪物总数)
  → 城市越大，郊区怪物群越多
```

这是城市僵尸密度高的根本原因：怪物群在城市生成阶段就已经嵌入 overmap 数据结构。

---

## 8. 中世纪化方案

> 中世纪村庄/城镇改造的策划案已移至 → [../design/medieval_city_design.md](../design/medieval_city_design.md)

---

## 9. 关键文件索引

| 文件 | 内容 |
|------|------|
| `src/city.h` | `city` 结构体定义 |
| `src/city.cpp` | `city` JSON 加载/工厂 |
| `src/overmap.cpp:5419-5538` | `place_cities()` — 城市入口 |
| `src/overmap.cpp:5540-5568` | `pick_random_building_to_place()` — 建筑类型选择 |
| `src/overmap.cpp:5570-5586` | `place_building()` — 单建筑放置 |
| `src/overmap.cpp:5588-5665` | `build_city_street()` — 街道递归铺设 |
| `src/overmap.cpp:5091-5162` | `place_roads()` — 城市间道路 |
| `src/overmap.cpp:5364-5407` | `place_mongroups()` — 城市怪物群 |
| `src/overmap.cpp:3359-3465` | `overmap::generate()` — 总生成流程 |
| `src/regional_settings.h:41-80` | `city_settings` / `building_bin` 结构体 |
| `src/regional_settings.h:262-286` | `regional_settings` 完整结构 |
| `src/overmap_connection.h` | `overmap_connection` 道路连接系统 |
| `data/json/regional_map_settings.json` | JSON 端城市配置（houses/shops/parks 池） |
| `data/json/overmap/multitile_city_buildings.json` | 所有城市建筑模板 (5247行) |
