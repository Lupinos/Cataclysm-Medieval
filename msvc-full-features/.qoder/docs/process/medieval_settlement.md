# 中世纪聚落与地图：实现进度

> 对应策划案：[design06-建筑.md](../design/design06-建筑.md)
> 原版调研：[json_map.md](../vanilla/json_map.md)、[code_city_generation_system.md](../vanilla/code_city_generation_system.md)

---

## 当前阶段：启用城市系统 + 中世纪建筑池

在「世界只剩荒野」的基础上，通过 CDDA 原生 `place_cities()` 管线生成中世纪村庄。
技术路线：`city_building` 定义建筑 → `region_overlay` 覆写 `city_spec` 建筑池 → `CITY_SIZE=2` 控制规模。

### 已完成

- [x] **第一阶段测试**：T5 独户农舍 (`medieval_farmstead_t5`)
- [x] **第二阶段测试**：T3 村庄核心建筑（4 个单格 mapgen）
- [x] **第三阶段：村庄管线打通（city_building）** ★NEW
  - **关键发现**：C++ 的 `oter_type_t::finalize()` 自动生成 `_north/_east/_south/_west` 4 个方向变体，`get_mapgen_id()` 去掉方向后缀指向同一份 mapgen，mapgen.cpp 物理旋转 0/90/180/270 度——**不需要为每个建筑定义 4 份 overmap_terrain 或 4 份 mapgen**。
  - 文件：`10_medieval_core/overmap/city_building.json` — 5 个 `city_building` 条目（farmhouse/manor/church/smithy/mill），单格 `point: [0,0,0]`+`locations: ["land"]`
  - 文件：`00_cleanup/road_override.json` — 使用 `copy-from` 继承原版 `road`/`road_nesw_manhole`/`city_center` 的 `generic_transportation` 链（保留 `land_use_code: "transportation"`），覆写为棕色土路（`travel_cost_type: dirt_road`）。`road` 保留 `LINEAR` 标志（C++ 自动生成方向变体）
  - 文件：`00_cleanup/game_balance.json` — `OVERMAP_PLACE_CITIES` 改为 `true`
  - 文件：`00_cleanup/region_overlay.json` — 新增 `city` 块，`clear_houses`/`clear_shops`/`clear_parks` 清空原版建筑池后，houses=农舍×500, shops=铁匠铺×300+磨坊×300, parks=庄园×200+教堂×200
  - **JSON 验证通过** (`--check-mods medieval` exit 0)
  - **已修复**：`road_nesw_manhole`/`city_center` 缺少 `sym` 字段导致 MAP_GEN 错误
  - **已修复**：运行时 `invalid overmap terrain id "city_center"` (`generic_factory.h:509`)。根因：直接覆写 `overmap_terrain` 而未使用 `copy-from`，丢失了 `generic_transportation` 提供的 `land_use_code: "transportation"`。修复：全部 3 个条目添加 `copy-from` 继承原版定义
  - **教训**：`overmap_terrain` 不支持 `delete` 语法（不同于 `monster`/`item`），`extras` 字段暂无法移除（后续可定义空 extras）
  - **教训**：`--check-mods` 不检测 `land_use_code` 缺失，只有游戏运行时才会报 `invalid overmap terrain id`
  - **已修复**：游戏内生成了大量现代建筑（城市仍是现代风格）。根因：`apply_region_overlay` 对 `houses`/`shops`/`parks` 池是**累加**而非替换——5 个中世纪建筑（权重 1500）被添加到 340+ 现代建筑（权重 35000+）旁，中世纪概率 ~4%。
    - **C++ 修复**：`src/regional_settings.cpp:707-715` — 在 `apply_region_overlay` 中新增 `clear_houses`/`clear_shops`/`clear_parks` 三个 JSON boolean 开关，调用 `building_bin::clear()` 清空后再加载新条目
    - **JSON 修复**：`region_overlay.json` 的 `city` 块增加 `"clear_houses": true, "clear_shops": true, "clear_parks": true`
    - **重新编译并验证通过** (`--check-mods medieval` exit 0)
  - **已修复**：道路 tile 仍显示为沥青/人行道/黄线（现代路面）。根因：`road_override.json` 只覆写了 overmap_terrain 层（战略大地图图标），但 tile 级地形由 `road_palette` 控制——该 palette 把 `.`→`t_pavement`、`_`→`t_sidewalk`、`*`→`t_pavement_y`（黄线），且有 `f_street_light`（路灯）、`f_traffic_light`（交通灯）、`f_bench`（长椅）、`f_trashcan`（垃圾桶）、`f_bike_rack`（自行车架）等现代家具。
    - **修复**：`00_cleanup/road_palette_override.json` 覆写三个 palette：
      - `road_palette`：所有路面/人行道/黄线/水泥字符 → `t_dirt`，清除现代家具
      - `bridge_ground_palette`：桥面字符 → `t_dirt`
      - `bridge_road_palette`：架空桥面字符 → `t_dirt`
      - 同时覆写 `24x24_road_curved_layby` nested mapgen（移除原版的现代 terrain/furniture/items 本地覆写）
    - **重要发现**：`road_nested.json` 中所有人行道、路灯、交通灯、人行横道、路边垃圾嵌套 mapgen **全部引用 `road_palette`**——只覆写一个 palette 即可改变所有道路子元素
    - **验证通过** (`--check-mods medieval` exit 0)

- [x] **第四阶段：荒野据点与强盗营地管线打通（overmap_special）** ★NEW
  - **实现逻辑**：定义独立 hostile faction (`med_bandits`) -> 三级 bandit NPC types / classes (`NC_MED_BANDIT_*`) -> 6组装备worn/weapon items-group -> 24x24 single-tile mapgen (`medieval_bandit_camp`) with place_npcs -> overmap_special wilderness spawn setup.
  - 文件：`10_medieval_core/npcs/factions.json` — `med_bandits` faction
  - 文件：`10_medieval_core/npcs/classes.json` — 3 个 npc_class
  - 文件：`10_medieval_core/npcs/npc.json` — 3 个 npc 实例
  - 文件：`10_medieval_core/npcs/bandit_equipment.json` — 6 个 item_group
  - 文件：`10_medieval_core/mapgen/bandit_camp.json` — 1 个 24x24 single-tile mapgen, using `f_firering` campfire palette
  - 文件：`10_medieval_core/overmap/overmap_terrain.json` — `medieval_bandit_camp` terrain registration
  - 文件：`10_medieval_core/overmap/overmap_special.json` — `medieval_bandit_camp` special, spawning in wilderness.
  - **已解决**：`generic_factory.h` compile runtime validation error: `invalid furniture id "f_campfire"`. Fixed by replacing with `f_firering` (stone fire ring).
  - **验证通过** (`--check-mods medieval` exit 0, compiles perfectly with no warnings/errors).

- [x] **第五阶段：5x5 特大城堡要塞聚落实装（overmap_special）** ★NEW
  - **实现逻辑**：为了展现一个壮丽的中世纪堡垒城镇，在 `overmap_terrain.json` 注册 25 个独立网格 ID，并在 `overmap_special.json` 注册 5x5 连体 Special。在 `mapgen/fortified_town.json` 完整绘制 25 格 ASCII 图。
  - **核心区域**：
    - NW/NE/SW/SE：转角 watchtower 哨塔（含 log 墙、木梯、宝箱）。
    - N/S Gate：滑轨大门（palisade gate + pulley），门内侧各部署 2 名 Town Guard 站岗。
    - Smithy（[1,1]）：石木结构，含 forge 熔炉、anvil 铁砧。
    - Keep（[2,1]）：10x14 石制领主城堡（rock wall + rock floor），含壁炉、藏宝箱、长桌椅、主卧。
    - Barracks（[3,1]）：民兵营房，含训练假人、武器架、草垫床。
    - Church（[1,2]）：Chapel 教堂，内设 altar/benches，户外带 dirtmound 墓地。
    - Market（[2,2]）：核心石井广场，环绕木制商人货摊。
    - Tavern（[3,2]）：酒馆旅店（wood floor），含 bar counter 吧台、灶台、木桌椅。
    - Stables（[2,3]）：隔间马厩（splitrail fence + haypile）与 granary 谷仓。
    - Crops（[3,3]）：大型庄稼菜园。
  - 文件：`10_medieval_core/overmap/overmap_terrain.json` — 注册 25 个要塞 ID
  - 文件：`10_medieval_core/overmap/overmap_special.json` — 注册 `medieval_fortified_town` Special
  - 文件：`10_medieval_core/mapgen/fortified_town.json` — 编写 25 格 ASCII mapgen 连体定义
  - **验证通过** (`--check-mods medieval` exit 0, 编译零警告，语法与语义完全正确)。

### 待做

- [x] 验证 mapgen 在游戏中正确渲染
- [x] 创建 `medieval-json-mapgen` Skill
- [x] T3 村庄布局设计 + city_building 定义 + region_overlay 建筑池
- [ ] 游戏内实际测试村庄生成（需设 CITY_SIZE=2, CITY_SPACING=7）
- [ ] 测试多格建筑（T4 农庄 / 2-4 格）
- [ ] 建立中世纪 palette 库（提取公共 palette 而非每个建筑手写）
- [ ] 补充村庄建筑：谷仓、水井、牛栏/羊圈
- [ ] 覆写 `road` 的 map_extra（现代道路垃圾）
- [ ] T2 市镇与 T1 大城（远期）


---

## 经验教训：门窗定位错误

### 问题描述

生成 mapgen 时，门窗字符（`+`、`w`、`o`）被放在墙体**旁边**而不是**替换**墙体，导致：
- 门窗出现在墙体内部（浮空）
- 行长度超出 24 字符（因为额外添加了字符）

### 根因

设计 ASCII 行时，先写了完整的墙体行 `SSSSSSSSSSSSSSSSSSSS`，然后在某位置**插入**了门 `+`，而不是**替换**该位置的 `S`。

### 正确做法

**先写墙体模板，再替换：**
```
1. 写完整墙体行：  SSSSSSSSSSSSSSSSSSSS  (20个S)
2. 确定门位置：    第7个S要变成门
3. 替换（非插入）： SSSSSS+SSSSSSSSSSSSS  (6S + 1门 + 13S = 20字符)
```

### 验证方法

- **行长度检查**：含门窗的行必须与纯墙体行长度相同（24字符）
- **墙体连续性**：门窗两侧应该紧邻墙体字符（如 `S+S`），不应有空隙（如 `S.+S`）
- **位置对齐**：上下行的墙体字符应在同一列对齐

### 已固化到 Skill

`medieval-json-mapgen` Skill 的 **Phase 5** 现在是「门窗定位验证（强制）」，包含：
- 错误/正确示例对比
- 4步验证流程
- 5项检查清单
- 快速验证技巧（先写模板再替换）

---

## 经验教训：家具下方的地形

### 问题描述

铁匠铺的铁砧 `f_anvil`（字符 `a`）下方显示为草地 `t_grass`，而不是室内的泥土地板 `t_dirtfloor`。

### 根因

在 palette 中，家具字符（如 `a`）只在 `furniture` 部分定义，没有在 `terrain` 部分定义。CDDA mapgen 的规则是：
- 如果字符只在 `furniture` 中定义 → 该位置的 terrain 来自 `fill_ter`（本例中是 `t_grass`）
- 如果字符同时在 `terrain` 和 `furniture` 中定义 → terrain 覆盖 `fill_ter`，furniture 放在上面

### 正确做法

**家具字符需要在 palette 的 `terrain` 和 `furniture` 两部分都定义：**
```json
"terrain": {
  ".": "t_dirtfloor",
  "a": "t_dirtfloor"    // 铁砧位置的地形也应该是泥土地板
},
"furniture": {
  "a": "f_anvil"        // 铁砧家具放在泥土地板上
}
```

### 适用场景

所有室内家具都需要这样处理：
- 锻造炉 `f_forge`、铁砧 `f_anvil` → `t_dirtfloor`
- 桌子 `f_table`、椅子 `f_chair` → `t_dirtfloor` 或 `t_floor`
- 床 `f_straw_bed` → `t_dirtfloor` 或 `t_floor`
- 壁炉 `f_fireplace` → `t_dirtfloor` 或 `t_rock_floor`

### 已固化到 Skill

`medieval-json-mapgen` Skill 的 **Phase 3**（Palette 定义）新增了「家具地形覆盖」说明，强调室内家具字符必须在 `terrain` 中显式定义，否则会继承 `fill_ter`（通常是户外地形）。

---

## 文件结构

```
10_medieval_core/
├── mapgen/
│   ├── farmstead_t5.json          # T5 独户农舍
│   ├── manor_house_t3.json        # T3 领主庄园宅邸
│   ├── parish_church_t3.json      # T3 教区教堂+墓地
│   ├── smithy_t3.json             # T3 铁匠铺
│   ├── mill_t3.json               # T3 磨坊
│   └── bandit_camp.json           # 强盗营地 mapgen
├── overmap/
│   ├── overmap_terrain.json       # 中世纪 overmap_terrain 定义（含强盗营地）
│   ├── overmap_special.json       # 强盗营地 overmap_special
│   └── city_building.json         # city_building 条目（5 个）
└── npcs/
    ├── factions.json              # 强盗 faction
    ├── classes.json               # 强盗 npc_class
    ├── npc.json                   # 强盗 npc 实例
    └── bandit_equipment.json      # 强盗 worn/weapon item_groups

00_cleanup/
├── game_balance.json               # EXTERNAL_OPTION（OVERMAP_PLACE_CITIES=true）
├── region_overlay.json             # region_overlay + city 建筑池
├── road_override.json              # 覆写 road/city_center 为土路（overmap 层）
└── road_palette_override.json      # 覆写 road/bridge palette（tile 层），去掉沥青/现代家具
```

## 测试方式

通过 CDDA **Map Editor 的 mapgen 预览功能**测试：
1. Debug Menu → `M`（Map editor）
2. 按小写 `o`（Edit overmap/mapgen）
3. 在 "Mapgen stamp" 列表中找目标 terrain ID → ENTER
4. 实时预览 → 选 "Apply" 写入游戏世界

> 注意：Overmap Editor 的 "Place Overmap Terrain" 只改大地图符号，不触发 mapgen。测试 mapgen 必须用 Map Editor。
>
> 完整流程已标准化为 `medieval-json-mapgen` Skill。

---

## 已知未使用的 CDDA 中世纪材质

> 调研自 `data/json/furniture_and_terrain/`，以下地形/家具已存在但尚需在后续 mapgen 中使用：

| 类型 | ID | 说明 |
|------|-----|------|
| 墙体 | `t_wall_log` | 原木墙，适合森林小屋 |
| 墙体 | `t_palisade` | 木栅墙，适合防御工事 |
| 屋顶 | `t_thatch_roof` | 茅草屋顶 |
| 屋顶 | `t_shingle_flat_roof` | 木瓦平顶 |
| 屋顶 | `t_tile_flat_roof` | 瓦片平顶 |
| 地面 | `t_floor` | 木地板（相对富裕） |
| 地面 | `t_floor_primitive` | 原始木地板 |
| 家具 | `f_makeshift_bed` | 临时床 |
| 家具 | `f_woodstove` | 木炉（富裕） |
| 家具 | `f_bookcase` | 书架 |
| 家具 | `f_dresser` | 衣柜 |
| 家具 | `f_wardrobe` | 大衣柜 |
| 家具 | `f_crate_c` / `f_crate_o` | 木箱 |
| 水体 | `t_dirtmound` | 土堆（用于墓地等） |
