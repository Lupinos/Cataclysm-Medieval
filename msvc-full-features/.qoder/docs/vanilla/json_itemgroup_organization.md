# CDDA item_group 组织概念与目录分布

> 深度调研：~3849 个 item_group 的 9 维组织概念 + 目录→概念映射关系
> 原始数据源 [json_itemgroup_monstergroup.md](json_itemgroup_monstergroup.md)

---

## 一、总览

| 指标 | 数值 |
|------|------|
| 总 group 数 | ~3849 |
| 源文件数 | ~303 个 JSON 文件 |
| 定义位置 | 100% 集中在 `data/json/itemgroups/` |
| 外部引用 | mapgen / monsters / NPC / professions 只引用 ID，不定义 |

---

## 二、9 维组织概念

### 维度 1：房间/家具（Room / Furniture）— mapgen 的第一消费者

**概念**：定义"某个家具/房间位置上会刷出什么物品"。

**消费者**：`mapgen/` 中每个 `"place_items"` 调用。

**关键文件**：`collections_domestic.json`、`SUS/domestic.json`、`SUS/fridges.json`

**代表性 groups**：

```
kitchen, bedroom, livingroom, bathroom, nightstand, fridge,
bed, dresser, coat_rack, shower, dining, cleaning, oven,
pool_table, garden_shed, home_display_case, memorial
```

**Mapgen 引用模式**（house24.json 实测）：
```json
{ "chance": 45, "item": "kitchen",      "x": 11, "y": 11 },
{ "chance": 80, "item": "crate_kitchen","x": 11, "y": 14 },
{ "chance": 45, "item": "bed",          "x": 18, "y": 17 },
{ "chance": 40, "item": "nightstand",   "x": 21, "y": 8  }
```

单个 house 变体可引用 20~30 个此类 group。

> **SUS 与新体系**：`fridge` group 自注释 `"This is a terrible item group and should be phased out. See SUS_fridge for a more modern take"`，表明 SUS 是模块化重构方向，但 `collections_domestic.json` 仍是主要消费方。

---

### 维度 2：服装套装（Clothing Set）— 最庞大的分支

**概念**：按性别、部位、职业、季节/场合四个轴交叉组织。

**关键目录**：`Clothing_Gear/`（7 文件，172+ groups）

**四维交叉矩阵**：

| 轴 | 细分 | 示例 ID |
|---|------|---------|
| **部位/slot** | 上/下/脚/头/手/内衣/包 | `shoes`, `pants`, `shirts`, `jackets`, `hats`, `gloves`, `underwear`, `bags` |
| **性别** | male/female/unisex/child | `clothing_male`, `pants_womens`, `shoes_unisex`, `child_items` |
| **职业/身份** | 军/警/消防/泳/潜水/骑行... | `clothing_military`, `fireman_torso`, `diving_suits`, `clothing_biker` |
| **场合/季节** | 日常/婚礼/冬/夏/制服装 | `winter`, `suits`, `wedding_dresses`, `costumes` |

**嵌套模式**：mapgen 调用 `clothing_male` → 分发到 `pants_male`/`shirts`/`shoes` → 每个再分发到具体 item。

**子目录文件**：

| 文件 | groups | 内容 |
|------|--------|------|
| `clothing.json` | 81 | 军事/职业/平民/泳装/潜水/珠宝子集/幸存者 |
| `costumes.json` | 27 | 万圣节/角色扮演/拉拉队 |
| `gear.json` | 21 | 特警/消防/医疗/战术/平民护甲 |
| `gear_civilian.json` | 14 | 口袋物品/lunchbox/schoolbag |
| `wallets.json` | 20 | 钱包/现金/硬币/银行卡 |
| `jewellery_gems.json` | 7 | 珠宝陈列/gemstones |
| `hazmat_gear.json` | 2 | 防化服/消毒间 |

---

### 维度 3：武器/弹药类别（Weapon / Ammo）— 类型×稀有度×场景三级金字塔

**关键目录**：`Weapons_Mods_Ammo/` + 子目录 `arsenal/`

**金字塔结构**：

```
L1 顶级聚合: ammo, guns_common
  │
L2 类型+稀有度: guns_pistol_common, guns_rifle_rare, ammo_shotgun_common
  │
L3 场景变体: guns_pistol_common_display (展示柜), guns_shotgun_rare_worn (磨损)
  │
L4 预组装: nested_guns.json (枪+弹匣一体)
```

**子目录**：

| 文件 | 内容 |
|------|------|
| `guns.json` | 按类型×稀有度×场景三级分组 |
| `ammo.json` | 弹药按口径分组 |
| `gunmod.json` | 枪支配件 |
| `magazines.json` | 弹匣分组 |
| `nested_guns.json` | 枪+弹匣预组装 |
| `nested_ammo.json` | 弹药+容器预组装 |
| `arsenal/` | 按口径/枪型进一步细分 |
| `weapons_misc.json` | 近战/投掷/特种武器 |

---

### 维度 4：食品饮料（Food）— 按商品类型

**关键文件**：`Food/food.json`、`Food/irradiated.json`

由 `kitchen` 和 `fridge` 等房间 group 大量引用：

```
snacks, condiments, dry_goods, pantry_liquids, alcohol,
softdrinks_canned, frozen_dinner, candy, canned_food...
```

---

### 维度 5：建筑/场所（Location）— 按整栋建筑类型

**关键目录**：`Locations_MapExtras/`

| 文件 | 内容 |
|------|------|
| `mall_item_groups.json` | 商场各摊位 |
| `mansion.json` | 豪宅特有物品 |
| `prison_item_groups.json` | 监狱物品 |
| `private_resort_item_groups.json` | 私人度假村 |
| `locations.json` / `locations_commercial.json` | 通用商业/地点 |

不再以单个房间为单位，而是以**整栋建筑的主题**为单位。

---

### 维度 6：怪物掉落（Monster Drops）— 按生物类别×掉落类型

**关键目录**：`Monsters_Animals_Lairs/`

**双层掉落模型**：

| 层 | 概念 | 示例 |
|----|------|------|
| **身体部位** | 怪物死后直接掉落 | `monparts`(通用), `bug_parts`(昆虫), `vertebrate_parts`(脊椎), `human_parts`(类人) |
| **巢穴/储藏** | 巢穴内部环境战利品 | `ant_food`(蚂蚁囤积), `wasp_lair`(黄蜂巢), `kraken_food`(海怪储藏) |

**其他子维度**：

| 概念 | 示例 |
|------|------|
| 家养动物配饰 | `cow`, `dog_cop`, `dog_clothes` |
| 单一实体/原型 | `vault_wanderer`(完整 NPC 装备), `biollante`(独特怪物) |
| 解剖收获 | `harvest_cbm.json`, `harvest_dissection.json` |

---

### 维度 7：NPC / 职业起始装备

由 `professions.json` 和 NPC 定义直接引用 item_group ID 作为起始装备。

例如 `npc_hacker`、`vault_wanderer`、`traveler` 等 group 被职业/NPC 定义消费。

---

### 维度 8：物品+容器预组装（Container Pre-assembly）

**概念**：解决"物品需要装在合理容器里生成"的问题——CDDA 特有设计。

**命名模式**：`{item_id}_{container_id}_{count}`

```json
"bacon_bag_plastic_2"       ← 2 份培根装在塑料袋
"cereal_box_small_4"        ← 4 份麦片装在小盒子
"coffee_raw_can_food_big_240" ← 240 份咖啡豆装在大食品罐
"loaded_quiver"             ← 箭袋预装箭支
```

类型：`"subtype": "collection"`，使用 `"container-item"` 字段声明容器。

这些 group 通常自动生成，集中在 `collections_domestic.json` 底部和 `nested_ammo.json`。

---

### 维度 9：SUS（Special Use Sets）— 现代化重构层

**概念**：将旧的大杂烩 group 重构为模块化、可直接被家具引用的颗粒。

**关键目录**：`SUS/`

| 文件 | 内容 |
|------|------|
| `domestic.json` | 家庭（SUS_fridge, SUS_bathroom_sink, SUS_junk_drawer） |
| `fridges.json` | 冰箱子集 |
| `combos.json` | 组合表 |
| `gunstore.json` | 枪店 |
| `library.json` | 图书馆 |
| `office.json` | 办公室 |
| `garage.json` | 车库 |
| `lodge.json` | 小屋 |
| `clothes_store.json` | 服装店 |
| `evac_shelter.json` | 避难所 |
| `alien.json` | 外星物品 |

与传统 `collections_domestic.json` 并行存在，逐步推进替换。

---

## 三、目录→概念映射全景

```
data/json/itemgroups/
│
├── 🏠 房间/家具 — collections_domestic.json + SUS/domestic.json
├── 👔 服装套装 — Clothing_Gear/ (7 文件)
├── 🔫 武器弹药 — Weapons_Mods_Ammo/ (8 文件 + arsenal/)
├── 🍖 食品饮料 — Food/ (2 文件)
├── 💊 药品烟酒 — Drugs_Tobacco_Alcohol/
├── 🏛  建筑/场所 — Locations_MapExtras/ (10+ 文件)
├── 👾 怪物掉落 — Monsters_Animals_Lairs/ (4 文件)
├── 🔬 实验室   — Labs/
├── 🌾 农业采集 — Agriculture_Forage_Excavation/
│
├── 📚 零散概念文件 (按主题 vs 按物品类型)
│   ├── main.json          ← 顶级聚合 (ammo, archery, launchers)
│   ├── books.json         ← 书籍分组 (按技能领域)
│   ├── tools.json         ← 工具分组
│   ├── military.json      ← 军事装备
│   ├── bionics.json       ← 生化模块
│   ├── supplies.json      ← 补给品
│   ├── electronics.json   ← 电子产品
│   ├── mail.json          ← 邮件包裹
│   ├── cash_register.json ← 收银台
│   ├── vending_machines.json ← 自动售货机
│   ├── furniture.json     ← 家具本身掉落
│   ├── faction_camps.json ← 阵营营地
│   ├── shops_trades.json  ← 商店交易
│   ├── activities_hobbies.json ← 活动/爱好
│   ├── art_antiques_crafts.json ← 艺术品/古董
│   ├── stashes.json       ← 隐藏储物点
│   ├── collections_trades.json ← 交易/职业收藏
│   ├── vehicles_fuel_related.json ← 车辆/燃料
│   └── ...                ← 其他专业化文件
│
└── 🔧 特殊目录
    ├── SUS/               ← Special Use Sets (现代化重构)
    └── oa_shared_item_groups.json ← 跨 mod 共享组
```

---

## 四、核心设计原则总结

| 原则 | 说明 |
|------|------|
| **概念 ≈ 目录** | 大概念用子目录（Clothing_Gear/），小概念用单文件（books.json） |
| **最终消费者驱动命名** | 命名反映的是"它在哪里被消费"而非"它包含什么" |
| **嵌套金字塔** | 大类聚合→子类分组→场景变体→具体条目，3~5 层常见 |
| **预组装是独立粒度** | 物品×容器×数量＝一个 group，解决"刷出合理包装"问题 |
| **SUS 是现代方向** | 旧的大杂烩逐步重构为模块化、单职责的 group |

---

## 五、对 Medieval Mod 的启示

1. **房间/家具 group 是最高优先级**。村庄建筑有 mapgen，但没有 `kitchen`/`bedroom` 等 group 就永远是空的。
2. **服装按部位分层**——不做 `medieval_peasant_outfit` 大杂烩，分 `pants`/`tunic`/`shoes` 子组，方便 mapgen 灵活引用。
3. **中世纪不需要 SUS 重构**——从零设计直接按模块化模式做。
4. **预组装容器模式直接复用**——`{item}_{container}_{count}` 命名规则纯中世纪可用。
5. **9 个维度大多有中世纪对应**——枪→弓弩，生化→魔法(可选)，收银机→货摊。
