# 现代内容清除进度

> `data/mods/Medieval/` — 中世纪 Total Conversion mod 的现代内容屏蔽实现进度。
> 架构设计与技术原理见 [../design/medieval_conversion_design.md](../design/medieval_conversion_design.md)。

---

## 1. Mod 基本信息

| 字段 | 值 |
|------|-----|
| ID | `medieval` |
| 类别 | `total_conversion` |
| 依赖 | `dda` |
| 路径 | `data/mods/Medieval/` |

---

## 2. 当前文件结构

```
data/mods/Medieval/
├── modinfo.json           # MOD_INFO 元信息
├── game_balance.json      # EXTERNAL_OPTION：关闭城市/道路生成
├── region_overlay.json    # 地图特征标志黑名单
├── monster_whitelist.json # MONSTER_WHITELIST：只保留野生动物
├── start_locations.json   # 自然地形起始位置（覆盖 field/forest/river）
├── scenarios.json         # SCENARIO_BLACKLIST(1个) + medieval_peasant 场景
├── professions.json       # 6个职业：4个常规 + medieval_test_master、medieval_test_novice
├── hobbies.json           # 现代 Background 移除：40个现代 hobby 的 subtype 覆写
├── recipes_obsolete.json  # 现代 Recipe 移除：1156条 result 标记为 obsolete
├── itemgroups/            # 现代 item_group 置空覆写（9个文件，140个组）
│   ├── guns.json          # 48个枪械组 → null
│   ├── clothing.json      # 22个衣物组 → null
│   ├── tools.json         # 2个工具组 → null
│   ├── electronics.json   # 3个电子组 → null
│   ├── military_science.json # 军事+科技组 → null
│   ├── books.json         # 12个书籍组 → null
│   ├── food.json          # 34个现代食品组 → null
│   ├── medic.json         # 21个药品组 → null
│   ├── trash.json         # 3个现代垃圾组 → null
│   └── misc.json          # 9个杂项组（allclothes/everyday/grave） → null
└── (recipes/ 目录保留用于未来中世纪配方)
```

---

## 3. 执行顺序 [测试标记-已执行]

按设计方案的 5 层拦截架构自上而下执行：

```
✅ 第1步：modinfo.json + EXTERNAL_OPTION   (关闭城市/道路)
✅ 第2步：region_overlay 地图黑名单         (屏蔽现代建筑)
✅ 第3步：MONSTER_WHITELIST               (只保留野生动物)
✅ 第4步：SCENARIO_BLACKLIST + 场景覆盖     (只留野外场景)
    ↑ 以上4步完成，世界只剩荒野 ↑
✅ 第5步：检查启动报错 → 修复缺失引用(起始位置修复)
✅ 第6步：逐类覆写 item_group（140个，10个文件）
✅ 第7步：现代 Recipe 标记 obsolete（1156条）
✅ 第8步：覆写 professions（6个中世纪职业含2个测试职业，所有其他原版场景/职业被SCENARIO_BLACKLIST屏蔽）
```

---

## 4. 各层实现详情

### Layer 5: EXTERNAL_OPTION (`game_balance.json`)

关闭内容：
- `OVERMAP_PLACE_CITIES` = false — 不生成城市
- `OVERMAP_PLACE_ROADS` = false — 不生成道路

### Layer 4: region_overlay (`region_overlay.json`)

地图特征黑名单：
- `LAB`, `MAN_MADE`, `MILITARY`, `URBAN`, `FARM`, `EXODII`

覆盖区域：`"all"`（全局生效）

**副作用（已修复）**：黑名单屏蔽 MAN_MADE 后，`campsite` 和 `campground` overmap_special 不再生成，导致场景的 `sloc_campsite`/`sloc_campground` 起始位置无效。

### 起始位置修复 (`start_locations.json`)

覆盖/重新定义了 3 个纯自然地形起始位置，确保不受 MAN_MADE 黑名单影响：

| sloc ID | terrain | 说明 |
|---------|---------|------|
| `sloc_field` | `field`, `forest` | 野外空地 |
| `sloc_forest` | `forest`, `forest_thick` | 森林深处 |
| `sloc_river` | `river`, `forest_water` | 河边 |

### 场景覆写 (`scenarios.json`)

**已完成。** 通过 `SCENARIO_BLACKLIST` whitelist 只保留 1 个场景，不再使用 `copy-from` 继承原版。

| 场景 | 起始位置 | 职业 | 说明 |
|------|---------|------|------|
| `medieval_peasant` | forest, field, river | `naked_peasant` / `medieval_wandering_swordsman` / `medieval_novice_bowman` / `medieval_town_guard` / `medieval_test_master` / `medieval_test_novice` | 干净的中世纪开局，无任何现代痕迹 |

- `SCENARIO_BLACKLIST` 白名单只含 `medieval_peasant`，屏蔽所有其他原版场景
- 场景 flags: `LONE_START`（无NPC同伴）
- 无 `copy-from`，完全独立定义

### 现代 Background 移除 (`hobbies.json`)

**已完成。** 通过 `copy-from` 覆盖机制，将 40 个现代 hobby 的 `subtype` 字段设为 `"none"`。

**原理**：CDDA 没有 BACKGROUND_BLACKLIST 机制。`set_hobbies()` 函数通过 `profession::is_hobby()` 过滤（检查 `_subtype == "hobby"`），返回所有 subtype 为 "hobby" 的 profession 条目。在 mod JSON 中用 `copy-from` 覆盖现代 hobby，将其 subtype 设为 "none"（不再是 "hobby"），即可从 Background 页面（`set_hobbies()`）移除。

**被移除的 40 个现代背景分类**：

| 类别 | 数量 | 示例 ID |
|------|:---:|---------|
| 机动车辆 | 6 | boating_license, driving_license, hobby_heli_pilot, car_fan, racing, car_rebuilding |
| 科技/电子 | 6 | computer_literate, high_school_graduate, mundane_survival, vid_games, amateur_electronics, ham_radio_operator |
| 枪械/射击 | 8 | paintball, plinking, skeet_shooting, shooter_beginner, shooter, trap_shooting, handloading, gunsmithing |
| 现代运动(球类) | 11 | baseball_*, basketball_*, football_*, golfing |
| 轮滑/骑行 | 6 | skating, roller_derby, hockey, cyclist_* |
| 现代工艺/家装 | 3 | home_improvement, diy_crafts, diy_crafts_expert |

**保留的 50 个中世纪兼容背景**：射箭(3级)、烹饪(6个)、武术/格斗(12个)、生存/钓鱼/园艺/背包、缝纫/陶艺/木工/锻造、游泳(3级)、急救、炼金、冥想、读书、公共演讲等。

### Layer 3: MONSTER_WHITELIST (`monster_whitelist.json`)

**已完成。** 使用 `mode: "EXCLUSIVE"`，白名单 `WILDLIFE` + `NULL` 两个 category。

**覆盖范围**：
- `WILDLIFE` — 所有自然野生动物（鹿、熊、狼、鸟、蛇、蛙等）
- `NULL` — 无分类变种两栖/爬行动物（巨型变种蛙/蟾蜍/蛇等，仅出现在 `reptile_amphibian.json`）

**被屏蔽**：
- `CLASSIC` category — 全部僵尸、丧尸动物、变异体等现代末日怪物
- 所有未分类且不在白名单内的怪物

**原理**：EXCLUSIVE 模式下，任何不在 whitelist categories/monsters/species 中的怪物全部被 `monster_is_blacklisted()` 返回 true，`FinalizeMonsterGroups()` 阶段从所有 monster group 中剔除。

### Layer 2: item_group 覆写

**已完成（140 个组，10 个 JSON 文件）。** 全部置空（`"item": "null"`），不新增任何中世纪物品。

参照 innawood 模组确定需要覆写的 item_group ID，排除 NC_*/npc_*（NPC装备，属于 professions 阶段）、profession 包、monster drops（由 MONSTER_WHITELIST 控制）、自然组（field/forest/trash_forest/cave_minerals，中世纪兼容）。

**已置空明细（9 类 + 杂项）：**

| 文件 | 数量 | 说明 |
|------|:---:|------|
| guns.json | 48 | archery, guns_pistol_*, guns_smg_*, guns_rifle_*, guns_shotgun_*, guns_launcher_*, guns_common/rare/milspec/improvised, longguns_cop*, sidearms_cop*, guns_cop/swat/survival |
| clothing.json | 22 | clothing_biker/glasses/hunting/watch, coats_unisex, common_gloves, underwear_*, hatstore_hats, jackets, large/small_bags, pants*, scarfs_unisex, shirts*, shoes_unisex |
| electronics.json | 3 | electronics, radio, robots |
| military_science.json | 2 | military, science |
| tools.json | 2 | archeology_tools, tools_common_small |
| books.json | 12 | book_gunmags, book_gunref, book_mag_*, book_martial, book_military, book_school, book_survival |
| food.json | 34 | candy*, cannedfood*, chips*, fast_food, frozen_dinner, MRE/mre_*, preserved_food, snacks*, toasterpastry* |
| medic.json | 21 | antibiotics*, aspirin*, bandages_box, drugdealer, drugs_*, medical_sample_*, pills_sleep* |
| trash.json | 3 | trash_cart, trash_domestic, trash_junkyard |
| misc.json | 9 | allclothes, allclothes_damaged, everyday_corpse*, everyday_gear, grave |

**保留未置空**的自然/中世纪兼容组：
- field, forest — 自然地形物品（石头/树枝等）
- trash_forest — 森林垃圾（树皮/坚果等）
- cave_minerals — 洞穴矿物（铜/锡/铁矿石）
- forage_spring/summer/autumn/winter — 采集物（草药/浆果/蘑菇等）

**策略**：只置空，不新增。中世纪物品的注入留在后续「中世纪内容重建」阶段处理。

### 现代 Recipe 移除 (`recipes_obsolete.json`)

**已完成（1156 条，覆盖 40+ 文件）。** 使用 `"obsolete": true` 标记现代物品的 recipe。格式参照 Generic_Guns mod：`{ "type": "recipe", "result": "item_id", "obsolete": true }`。

**原理**：`recipe::load()` 遇 obsolete=true 跳过所有字段加载。`string_id<recipe>::obj()` 返回 null，`recipe_subset::in_category()` 和 `search()` 均过滤 obsolete，`item_factory::finalize()` 跳过注册。

**已覆盖类别**：

| 类别 | 来源 | 说明 |
|------|------|------|
| 弹药重装 | `ammo/*.json` (9文件) | bp_*, reloaded_, matchhead_* |
| 弹药组件 | `ammo/components.json` | 底火/火药/弹壳 (保留 pebble/clay/marble) |
| 枪械弹匣 | `weapon/magazines.json` | 各类 magazine/clip |
| 爆炸物 | `weapon/explosive.json` | dynamite, grenade, pipebomb, C4 |
| 武器模组 | `weapon/mods.json` | 瞄准镜/消音器/握把 (保留弓类附件) |
| 枪械配方 | `weapon/ranged.json` | pistol/rifle/shotgun/smg (保留弓/弩/投掷) |
| 电子零件/工具 | `electronics/*.json`, `tools/tools_electronic.json` | circuit board, solder, soldering iron |
| 机器人 | `other/bots.json` | 22种机器人 |
| 突变剂 | `chem/mutagens.json` | 28种突变剂 + purifier |
| 现代药物 | `chem/drugs.json`, `recipe_medsandchemicals.json` | caffeine, meth, aspirin, antibiotics |
| 化学制品 | `chem/*.json` | 现代溶剂/塑料/石化产品 (保留中世纪炼金) |
| 电器 | `recipe_appliance.json` | fridge, freezer, dishwasher |
| 现代电力 | `other/power_supplies.json` | 电池/太阳能/发电机 (保留水车/风车) |
| 现代灯光 | `tools/lights.json` | flashlight/electric lantern (保留油灯/蜡烛) |
| 车辆零件 | `recipe_vehicle.json`, `other/vehicle.json` | 引擎/轮胎/电池 (保留挽具/船帆/桨) |
| 技能练习 | `practice/` (4文件) | computers/electronics/devices/mechanics |
| 现代防护服 | `armor/suit.json`, `armor/head.json` 等 | gas_mask, hazmat, wetsuit, nomex, thermal |
| Survivor装备 | `armor/*.json` (9文件) | boots_*survivor, gloves_*survivor, hood_*survivor |
| 现代战术装备 | `armor/storage.json` | molle, chestrig, tacvest, police_belt |
| 现代医疗 | `other/medical.json` | quikclot, pur_tablets, anesthetic_kit |
| 现代材料 | `other/materials.json` | plastic, nylon, kevlar, rubber, aluminum, zinc |

**保留的中世纪核心物品**（未被标记 obsolete）：
- 冷兵器：sword, axe, mace, spear, dagger, poleaxe, halberd, flail
- 弓弩/投掷：bow, crossbow, sling, javelin, throwing_*
- 盔甲：plate, chainmail, brigandine, gambeson, leather, lamellar
- 基本工具：hammer, saw, chisel, shovel, hoe, sickle, scythe, plow, anvil, forge
- 基本容器：barrel, bucket, clay_pot, waterskin, wooden_box, metal_tank
- 基本材料：wood, stone, clay, leather, fur, bone, iron, steel, bronze
- 纺织：loom, spindle, needle, thread, cloth, leather, fur, wool, linen, silk
- 中世纪化学：saltpetre, charcoal, lye, soap, quicklime, slaked_lime, black_powder
- 油灯/蜡烛：candle, oil_lamp, tallow, beeswax
- 水/风车：water_mill, wind_mill

### Layer 1: 职业/配方/制造覆写

**recipe 部分已完成（1156 条，见上方 recipes_obsolete.json）。**

### 职业覆写 (`professions.json`)

**已完成。** 只定义 1 个职业，通过 SCENARIO_BLACKLIST + 场景限定职业列表，使所有其他职业不可选。

| 职业 | 点数 | 物品 | 技能 | 说明 |
|------|:---:|------|:---:|------|
| `naked_peasant` | 0 | loincloth（男性）/ chestwrap（女性） | 无 | 赤身流浪者，一切从零开始 |

**策略**：SCENARIO_BLACKLIST 白名单只有 1 个场景 → 该场景只允许 1 个职业 → 所有其他职业/场景在角色创建界面不可见。无需逐一覆写/删除原版职业定义。

---

## 5. 相关文档

| 文档 | 关系 |
|------|------|
| [../design/medieval_conversion_design.md](../design/medieval_conversion_design.md) | 本 mod 依据的技术方案，含 5 层架构原理 |
| [../vanilla/json_data_system.md](../vanilla/json_data_system.md) | JSON 覆写机制与 Mod 系统基础 |
| [../vanilla/city_generation_system.md](../vanilla/city_generation_system.md) | EXTERNAL_OPTION 关闭城市后 overmap 层面的效果 |
| [../vanilla/monster_spawn_system.md](../vanilla/monster_spawn_system.md) | MONSTER_WHITELIST 生效的底层怪物组机制 |
