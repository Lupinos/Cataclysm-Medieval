# CDDA 材料系统调研

> 核验基点：CDDA `0.H-branch`，提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 改造前的维护分支快照，并非最初的 0.H 发布标签）。下述源码路径均以该提交为准。

> 调研日期：2026-05-06
> 调研范围：`src/material.cpp` / `src/material.h` / `src/damage.cpp` / `src/damage.h` / `data/json/materials.json` / `data/json/damage_types.json`

## 一、material_type 核心结构

文件：material.h、material.cpp

### 关键属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `_resistances` | `resistances` | 伤害抗性映射表（任意 damage_type → float） |
| `_res_was_loaded` | `vector<string>` | 记录 JSON 中显式定义了哪些 resist 键名 |
| `_chip_resist` | `int` | 抗碎性，影响物品耐久和维修损耗 |
| `_density` | `float` | 密度（g/cm³），影响物品重量 |
| `_breathability` | `breathability_rating` | 透气性等级（IMPERMEABLE→SECOND_SKIN） |
| `_wind_resist` | `optional<int>` | 防风率（0-100） |
| `_soft` | `bool` | 是否为软质材料（如锁子甲、布料） |
| `_repair_difficulty` | `int` | 维修难度（0-10） |
| `_sheet_thickness` | `optional<float>` | 材料片厚度（mm），影响覆盖层计算 |

### 关键方法

```cpp
// 查询某伤害类型的抗性
float material_type::resist( const damage_type_id &dmg_type ) const;

// 判断记录的 resist 键中是否显式列出该伤害类型（copy-from 可保留父定义的键记录）
bool material_type::has_dedicated_resist( const damage_type_id &dmg_type ) const;
```

## 二、材料加载流程

### 2.1 load() — JSON 解析入口 (material.cpp:81)

```
material_type::load(JsonObject)
  ├── _name — 必需
  ├── "resist" → load_resistances_instance(jo)
  │   └── 记录所有 JSON 键名到 _res_was_loaded
  ├── "conductive" — 可选；"chip_resist"、"density" — 必需
  ├── _sheet_thickness, _repair_difficulty, _wind_resist — 可选
  ├── _breathability — 可选（默认 IMPERMEABLE）
  ├── _soft, _uncomfortable, _edible, _rotting — 可选（默认 false）
  ├── burn_data — 燃烧数据
  └── burn_products — 燃烧产物
```

### 2.2 finalize_all() — 全局后处理 (material.cpp:145)

```cpp
void material_type::finalize_all() {
    material_data.finalize();
    for (const material_type &mtype : material_data.get_all()) {
        finalize_damage_map(mt._resistances.resist_vals);
    }
}
```

材料此处以默认 `force_derive=false` 调用 `finalize_damage_map`：按 `all` / `physical` / `non_physical` 及默认值补齐伤害类型，不在此处自动执行 `derived_from`。`src/item.cpp` 的 `_general_resist` 等护甲查询会在材料未专门定义该抗性时使用派生类型与倍率。怪物护甲的 finalize 路径则可强制派生。

### 2.3 check() — 验证阶段 (material.cpp:154)

两项关键验证：

1. **抵抗类型有效性**（:179-183）：
   ```cpp
   for (const auto &dt : _resistances.resist_vals) {
       if (!dt.first.is_valid()) {
           debugmsg("Invalid resistance type \"%s\" for material %s", dt.first.c_str(), id.c_str());
       }
   }
   ```
   任意注册的 damage_type_id 都可以被材料引用。

2. **必需抗性缺失检查**（:185-191）：
   ```cpp
   for (const damage_type &dt : damage_type::get_all()) {
       if (dt.material_required && !type_defined) {
           debugmsg("material %s is missing required resistance for \"%s\"", id.c_str(), dt.id.c_str());
       }
   }
   ```
   只有当 `damage_type.material_required == true` 时，才强制要求材料必须定义该抗性。

## 三、伤害类型系统

文件：damage_types.json

### 已注册类型及材料要求

| ID | 名称 | physical | material_required | 派生关系 | 说明 |
|----|------|----------|-------------------|----------|------|
| `bash` | bash | true | **true** | — | 钝击 |
| `cut` | cut | true | **true** | — | 砍伤 |
| `stab` | pierce | true | **false** | derived_from cut×0.8 | 穿刺（具体派生取决于调用路径） |
| `bullet` | ballistic | true | **true** | — | 弹道 |
| `acid` | acid | false | **true** | derived_from cut×0.5 | 腐蚀 |
| `heat` | fire | false | **true** | — | 火焰 |
| `electric` | electric | false | false | — | 电击 |
| `cold` | cold | false | false | — | 冰冻 |
| `biological` | biological | false | false | — | 生物（no_resist） |
| `pure` | pure | false | false | — | 真伤（no_resist） |

### stab 的特殊地位

- **已注册为 damage_type**，在 C++ 中可通过 `damage_type_id("stab")` 引用
- **material_required = false**：材料可以不定义 stab 抗性
- **derived_from: ["cut", 0.8]**：声明穿刺由 cut×0.8 派生；怪物护甲后处理和物品护甲查询均有使用途径，不能仅限定为 monster
- **可在材料层显式定义**：如 `kevlar` 定义了 `"stab": 5`。引擎正常读取并参与防护计算
- 对 Character/NPC 的战斗系统，stab 伤害独立于 cut，`character_armor.cpp` 中有专门的 ARMOR_STAB/ITEM_ARMOR_STAB 附魔支持

## 四、load_resistances_instance()

文件：damage.cpp:816

```cpp
resistances load_resistances_instance( const JsonObject &jo,
                                       const std::set<std::string> &ignored_keys ) {
    resistances ret;
    ret.resist_vals = load_damage_map( jo, ignored_keys );
    return ret;
}
```

`load_damage_map` 将 JSON 对象的每个键值对转换为 `damage_type_id → float` 映射。**不检查键名有效性**（该检查在 material_type::check() 中完成），纯粹按需加载。

多处复用此函数：
- 材料抗性（material.cpp:88）
- 身体部位护甲（bodypart.cpp:451）
- 生化模块保护（bionics.cpp:441）
- 怪物护甲（monstergenerator.cpp:722）
- 变异防护（mutation_data.cpp:610）

## 五、钢材分级体系

CDDA 原版定义了 7 种板材材料 + 6 种锁子甲变体，按 SAE 碳含量标准分级：

| 等级 | 板材 | 锁子甲 | 含碳量 | bash | cut | bullet | repair |
|------|------|--------|--------|------|-----|--------|--------|
| 铸铁 | `iron` | — | >2% | 4 | 4 | 2 | 2 |
| 杂钢 | `budget_steel` | `budget_steel_chain` | 混杂 | 6 | 6 | 2 | 2 |
| 低碳钢 | `lc_steel` | `lc_steel_chain` | 0.1% | 6 | 6 | 4.5 | 3 |
| 中碳钢 | `mc_steel` | `mc_steel_chain` | 0.5% | 7 | 7 | 4.5 | 4 |
| 高碳钢 | `hc_steel` | `hc_steel_chain` | 0.85% | 10 | 10 | 6.5 | 5 |
| 渗碳钢 | `ch_steel` | `ch_steel_chain` | 表层硬化 | 10 | 10 | 6.5 | 6 |
| 淬火钢 | `qt_steel` | `qt_steel_chain` | 回火处理 | 11 | 11 | 7.5 | 7 |

### chain 变体机制

锁子甲材料通过 `soft: true` + `breathability: GOOD` + `sheet_thickness: 1.2` 区别于板甲硬质材料。`soft` 参与物品柔软性判定（例如空容器体积、长度）；不能据此推断存在一套独立的“软甲穿透模型”。护甲仍需检查材料抗性、厚度和覆盖率等实际计算。chain 变体的 `repair_difficulty` 统一为 2（锁子甲比板甲容易修）。

## 六、对中世纪 Mod 的影响

1. **stab 可显式定义**：是否独立设置 `"stab": N` 是项目数值设计；原版不要求所有材料显式列出 stab
2. **钢材分级可直接复用**：从 `lc_steel`（熟铁级）到 `qt_steel`（淬火级）可作游戏材料数据参考；这些 ID 与数值本身不证明其历史对应关系
3. **chain 变体可作锁甲数据参考**：只需在 mod 中通过 `copy-from` 调整具体数值即可
4. **缺少的材料需要 mod 新增**：`linen`（亚麻）、`hardened_leather`（硬化皮）在原版中不存在

## 源码核对入口

`src/material.cpp` 的 `load`、`finalize_all`、`check`；`src/damage.cpp` 的 `finalize_damage_map`（注意 `force_derive` 参数）；`src/item.cpp` 的 `_general_resist`、`is_soft`；原始数值见 `data/json/materials.json` 与 `data/json/damage_types.json`。末节是项目取用建议，不是原版强制规则。
