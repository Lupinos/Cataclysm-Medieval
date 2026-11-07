# CDDA item_group 与 monstergroup 分组粒度分析

## 一、数量概览

| 类型 | 定义数量 | 分布文件数 | 平均每文件 |
|------|---------|-----------|-----------|
| **item_group** | ~3849 个 | 303 个文件 | ~12.7 个/文件 |
| **monstergroup** | ~449 个 | 42 个文件 | ~10.7 个/文件 |

**比例关系：item_group 数量是 monstergroup 的 8.6 倍。**

这反映了 CDDA 中"物品种类远多于怪物种类"的基本事实——物品需要更精细的分类组合。

---

## 二、item_group 的分组粒度

### 2.1 目录组织结构（按领域分文件夹）

```
itemgroups/
├── Clothing_Gear/          ← 服装装备 (clothing, gear, wallets, costumes...)
├── Weapons_Mods_Ammo/      ← 武器弹药 (guns, ammo, gunmod, magazines, arsenal/)
├── Food/                   ← 食品饮料 (food, irradiated)
├── Drugs_Tobacco_Alcohol/  ← 药品烟酒
├── Agriculture_Forage/     ← 农业采集
├── Labs/                   ← 实验室专属
├── Locations_MapExtras/    ← 按地点分的物品组
├── Monsters_Animals_Lairs/ ← 怪物/动物巢穴掉落
├── Weapons_Mods_Ammo/arsenal/ ← 军火库（按口径/枪型细分）
├── SUS/                    ← 特殊用途物品组
└── *.json (散落)           ← books, tools, military, misc...
```

### 2.2 命名粒度分析

item_group 的命名体现了**多层级**的粒度设计：

| 粒度层级 | 命名模式 | 示例 | 典型条目数 |
|---------|---------|------|-----------|
| **大类聚合** | `guns_common` / `ammo` | guns_common, guns_rare, ammo | 5~8个子group引用 |
| **中类-按武器类型** | `guns_{type}_{rarity}` | guns_pistol_common, guns_rifle_milspec | 10~50个item |
| **中类-按场景** | `guns_{type}_{context}` | guns_pistol_common_display, guns_shotgun_rare_worn | 10~20个item |
| **小类-按地点/家具** | 地点名/家具名 | kitchen, fridge, bedroom, nightstand | 10~40个item |
| **小类-按职业** | `clothing_{occupation}` | clothing_military, clothing_biker, clothing_hunting | 5~20个item |
| **微类-具体组合** | 具体描述 | earrings_gold, pendant_necklaces_silver | 10~16个item |
| **容器预组装** | `{item}_{container}_{count}` | bacon_bag_plastic_2, cereal_box_small_4 | 1~2个item |

### 2.3 典型分组案例

**大类（聚合层）- 供 mapgen 直接引用：**
```
guns_common
  ├── group: guns_pistol_common    (prob: 10)
  ├── group: guns_rifle_common     (prob: 8)
  ├── group: guns_shotgun_common   (prob: 6)
  └── group: guns_smg_common       (prob: 2)
```

**中类（场景化）- 体现"在哪里找到"的差异：**
```
guns_pistol_common         ← 一般刷新（如枪店货架）
guns_pistol_common_display ← 展示柜中（全新、可能有弹匣）
guns_pistol_common_everyday_carry ← 随身携带（有磨损、已装弹）
```

**小类（家居场景）- 极度贴近现实：**
```
kitchen (106个条目的大集合)
  ├── 刀叉碗碟
  ├── 调料瓶
  ├── 食品包装
  ├── 厨房电器
  └── 清洁用品

nightstand
  ├── 手电筒
  ├── 手机
  ├── 书
  ├── 药片
  └── 眼镜
```

**微类（物品+容器预组装）：**
```
bacon_bag_plastic_2        ← 2份培根装在塑料袋里
cereal_box_small_4         ← 4份麦片装在小盒子里
coffee_raw_can_food_big_240 ← 240份咖啡豆装在大食品罐里
```
这类 group 解决了"物品需要装在合理容器里生成"的问题。

### 2.4 item_group 分域统计

| 领域 | 文件/目录 | 估计 group 数 | 说明 |
|------|----------|-------------|------|
| 服装装备 | Clothing_Gear/ | ~500+ | 按性别/场合/材质/风格极度细分 |
| 武器弹药 | Weapons_Mods_Ammo/ | ~600+ | 按口径/稀有度/场景/嵌套枪+弹匣 |
| 食品 | Food/ | ~200+ | 按保鲜/料理/饮料/零食等 |
| 家居场景 | collections_domestic | ~100+ | kitchen/bedroom/livingroom 等 |
| 地点商业 | Locations_MapExtras/ | ~300+ | 按建筑类型(mall/prison/mansion) |
| 怪物掉落 | monsterdrops/ + Monsters_Animals/ | ~300+ | 按怪物类型(zombie/cop/soldier) |
| 药品 | Drugs_Tobacco_Alcohol/ | ~80+ | 处方药/毒品/烟草/酒类 |
| NPC/职业 | professions.json + npcs/ | ~200+ | 职业初始装备、NPC商人库存 |
| 书籍 | books.json | ~50+ | 按技能领域分类 |
| 杂项 | misc/tools/military | ~300+ | 工具/军事/活动 |

---

## 三、monstergroup 的分组粒度

### 3.1 文件组织

```
monstergroups/
├── zombies.json           ← 67个组，最大的文件
├── eggs.json              ← 118个（各种孵化组）
├── amphibian.json         ← 32个
├── bugs.json              ← 23个
├── wilderness.json        ← 21个
├── mammal.json            ← 21个
├── zombie_upgrades.json   ← 18个（进化路径）
├── lab.json               ← 16个
├── nether.json            ← 14个
├── military.json          ← 12个
├── misc.json              ← 26个
├── robots.json            ← 7个
├── zanimal_upgrades.json  ← 7个
├── mutant_upgrades.json   ← 6个
├── mi-go.json             ← 5个
├── resort.json            ← 5个
├── triffid.json           ← 4个
├── fungi.json             ← 4个
├── fish.json              ← 3个
├── blob.json              ← 2个
├── kraken.json            ← 2个
└── exodii.json            ← 2个
```

### 3.2 命名粒度分析

| 粒度层级 | 命名模式 | 示例 |
|---------|---------|------|
| **按建筑/地点** | `GROUP_{LOCATION}` | GROUP_HOUSE, GROUP_HOSPITAL, GROUP_MALL, GROUP_SCHOOL |
| **按区域变体** | `GROUP_{LOC}_{VARIANT}` | GROUP_PARK_SCENIC, GROUP_PARK_PLAYGROUND, GROUP_PARK_DOG |
| **按生态环境** | `GROUP_{BIOME}` | GROUP_FOREST, GROUP_SWAMP, GROUP_RIVER, GROUP_CAVE |
| **按生物分类** | `GROUP_{CREATURE_TYPE}` | GROUP_FISH, GROUP_TRIFFID, GROUP_FUNGI |
| **按功能** | `GROUP_{ROLE}` | GROUP_TURRET, GROUP_ROBOT, GROUP_FERAL |
| **按进化** | `GROUP_{MON}_UPGRADE` | GROUP_ZOMBIE_DOG_UPGRADE, GROUP_ZOMBEAR_UPGRADE |
| **按难度区** | `GROUP_{LOC}_{SUBZONE}` | GROUP_HOSPITAL, GROUP_HOSPITAL_INCUBATOR |

### 3.3 典型分组案例

**建筑类（最常见模式）：**
```
GROUP_HOUSE (住宅)
  ├── mon_zombie (基础, weight 500)
  ├── mon_zombie_tough (weight 75)
  ├── mon_zombie_fat (weight 50)
  ├── mon_zombie_rot (weight 50)
  ├── mon_zombie_child (weight 100)
  ├── GROUP_FERAL (嵌套引用, weight 115)
  └── ... 共约15-20种

GROUP_HOSPITAL (医院)
  ├── mon_zombie (weight 400)
  ├── mon_zombie_tough (weight 100)
  ├── mon_zombie_fat (weight 100)
  ├── mon_zombie_scientist (weight 50)
  ├── mon_zombie_nurse (weight 50)
  └── ... 更多特殊医院怪物
```

**生态类（按栖息地）：**
```
GROUP_FOREST
  ├── mon_null (weight 200, 表示"什么都不刷")
  ├── GROUP_WILDERNESS_FOREST_MAMMAL (嵌套)
  ├── GROUP_WILDERNESS_FOREST_BIRD (嵌套)
  ├── GROUP_WILDERNESS_FOREST_INSECT (嵌套)
  └── GROUP_WILDERNESS_FOREST_ZOMBIE (嵌套)
```

**进化链：**
```
GROUP_ZOMBIE_DOG_UPGRADE
  ├── mon_zombie_dog_tough (weight 30)
  ├── mon_zombie_dog_brute (weight 10)
  └── mon_zombie_dog_acid (weight 5)
```

---

## 四、粒度对比与设计哲学

### 4.1 核心对比

| 维度 | item_group | monstergroup |
|------|-----------|--------------|
| 总数量 | ~3849 | ~449 |
| 粒度最细到 | 单个物品+容器组合 | 单个建筑子区域 |
| 嵌套深度 | 3~5层常见 | 1~2层为主 |
| 命名风格 | 小写+下划线，语义化 | GROUP_大写，按地点/角色 |
| "空条目"概念 | 不存在 | `mon_null`（什么都不刷） |
| 条目数典型值 | 5~50 个 item | 5~20 个 monster |
| 概率字段 | `prob` (0~100) | `weight` (相对权重) |

### 4.2 设计哲学总结

**item_group 的分组逻辑：**
```
"现实中这个东西通常和什么东西放在一起？"

nightstand → 手电/手机/书/药  (床头柜上通常有什么)
kitchen    → 刀叉/调料/电器    (厨房通常有什么)
cop_armory → 枪/弹药/防弹衣    (警察武器库通常有什么)
```

**monstergroup 的分组逻辑：**
```
"这个地点通常有什么生物？"

GROUP_HOUSE     → 普通丧尸为主 + 少量变异
GROUP_HOSPITAL  → 普通丧尸 + 医护丧尸 + 特殊变异
GROUP_FOREST    → 动物 + 虫子 + 偶尔丧尸
GROUP_LAB       → 实验体 + 机器人 + 少量科学家丧尸
```

### 4.3 粒度的"金字塔"结构

```
item_group 粒度金字塔:

        ┌─────────┐
        │ ammo    │  ← 最大聚合（弹药总池）
        │ guns    │
        └────┬────┘
             │
     ┌───────┴────────┐
     │guns_pistol_rare│  ← 中间层（类型+稀有度）
     │guns_rifle_common│
     └───────┬────────┘
             │
  ┌──────────┴───────────┐
  │guns_pistol_rare_display│  ← 场景层（在哪里出现）
  │guns_pistol_rare_worn   │
  └──────────┬───────────┘
             │
     ┌───────┴────────┐
     │earrings_gold   │  ← 最细粒度（具体变体）
     │bacon_bag_2     │
     └────────────────┘

monstergroup 粒度金字塔:

        ┌──────────────┐
        │ GROUP_ZOMBIE │  ← 通用城市丧尸池
        └──────┬───────┘
               │
     ┌─────────┴──────────┐
     │ GROUP_HOUSE        │  ← 按建筑分
     │ GROUP_HOSPITAL     │
     │ GROUP_MALL         │
     └─────────┬──────────┘
               │
     ┌─────────┴──────────────┐
     │GROUP_HOSPITAL_INCUBATOR│  ← 建筑内子区域
     │GROUP_MANSION_POOL      │
     └────────────────────────┘
```

---

## 五、关键洞察

1. **item_group 的粒度远比 monstergroup 精细** —— 因为物品要模拟"容器包装""磨损状态""是否装弹"等维度，而怪物只需要"在不在这里"

2. **item_group 大量使用嵌套** —— 一个 `default_zombie_clothes` 可以嵌套 5 层来精确模拟"一个丧尸穿什么"；monstergroup 则少有超过 2 层嵌套

3. **item_group 的"预组装"是独特设计** —— `bacon_bag_plastic_2` 这类 group 只有 1 个条目，其存在目的是"让物品以合理的容器+数量组合出现"

4. **monstergroup 用 `mon_null` 控制密度** —— weight 为 200~500 的 `mon_null` 意味着"大部分时候什么都不刷"，这是怪物稀疏感的来源

5. **两者共享的设计模式**：按"场景/地点"命名是最核心的组织原则，因为最终消费者(mapgen)就是按地点工作的
