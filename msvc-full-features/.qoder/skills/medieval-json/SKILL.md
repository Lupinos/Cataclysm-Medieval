---
name: medieval-json
description: Generate CDDA JSON data for the Medieval total conversion mod, based on design documents or user instructions. Handles ALL CDDA JSON types (ARMOR, GENERIC, TOOL, recipe, profession, MONSTER, item_group, scenario, mutation, etc.). Automatically validates syntax, field completeness, ID uniqueness, and field logic consistency. Use when the user asks to generate JSON, create/modify medieval content, equipment, items, professions, monsters, or any CDDA data.
---

# Medieval Mod JSON Generator

Generate CDDA-compliant JSON for `E:\Cataclysm-Medieval\data\mods\Medieval\`.

**Important**: This skill handles ALL CDDA JSON types. Never assume a type is unsupported — use the tools below to discover any type's schema dynamically.

---

## Quick Decision Tree

```
User request
  │
  ├─ Design doc (.qoder/docs/design/) referenced?
  │   │
  │   ├─ YES ──→ Parse doc → Determine CDDA type(s)
  │   │              ↓
  │   │          Phase 1A: keys.py to discover fields for this type
  │   │              ↓
  │   │          Phase 1B: Map doc data → CDDA fields → Generate JSON
  │   │
  │   └─ NO ───→ Request design doc or user instructions
  │                  ↓
  │              User provides specs → proceed as above
  │
  ├─ Write file directly to Medieval mod dir
  │
  ├─ Validate (L0 syntax → L1 fields → L2 ID uniqueness → L3 field logic)
  │
  └─ Notify user to test in-game
```

---

## Phase 1: CDDA Format Research

### Phase 1A: Discover CDDA Fields for This Type

ALWAYS run `keys.py` first to know which fields exist:

```powershell
">python "E:\Cataclysm-Medieval\tools\json_tools\keys.py" --human type=$TYPE
```

This dynamically discovers the field list for any type — no hardcoded type limitations.

### Phase 1B: Map to CDDA Fields

Parse the design document's tables. Match each design column to a CDDA field discovered by `keys.py`. Use `values.py` when unsure about valid values.

For further reference, find vanilla examples of similar items:

```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\pluck.py" type=$CDDA_TYPE
python "E:\Cataclysm-Medieval\tools\json_tools\values.py" -k $FIELD_NAME --human type=$CDDA_TYPE
```

### Phase 1C: Generate

Follow the mapping. See [reference/cdda_schema.md](reference/cdda_schema.md) for common type-specific patterns (ARMOR layers, weapon techniques, recipe structure, etc.), but treat those as examples, not as the only supported types.

---

## Universal JSON Rules (All Types)

### ID Naming

IDs should be descriptive (e.g., `hood_linen`, `helm_kettle`), no strict prefix requirement.

### Name Format

All display `name.str` must use `med_` prefix for console filter search: `"med_ linen hood"`, `"med_ kettle hat"`.

```json
"name": { "str": "med_ name here" }
```
Never use plain strings for `name`.

### Common Fields (Most Item Types)

```json
{
  "type": "$TYPE",
  "id": "medieval_xxx",
  "name": { "str": "..." },
  "description": "...",
  "weight": "XXX g",
  "volume": "X L",
  "price": XXXX,
  "price_postapoc": XXX,
  "material": ["material_id"],
  "symbol": "X",
  "color": "color_name"
}
```

### Material IDs

```
cotton, wool, leather, fur, steel, iron, wood, bone, bronze, copper, brass, silver, gold
```

Use `values.py -k material` to verify an ID exists before using it.

---

## Phase 2: File Output

### Target Directory

```
E:\Cataclysm-Medieval\data\mods\Medieval\
```

Group related items into subdirectories logically (e.g., `items/armor/`, `items/weapons/`, `professions/`, `monsters/`).

### Direct File Write

Write JSON files directly to the target directory using `Write` tool. No relay scripts needed.

### Output Format

One JSON array per file:
```json
[
  { "type": "$TYPE", "id": "medieval_xxx", ... },
  { "type": "$TYPE", "id": "medieval_yyy", ... }
]
```

---

## Phase 3: Validation

### L0: Syntax (MANDATORY, auto-execute)

```powershell
"E:/Cataclysm-Medieval/tools/format/json_formatter.exe" "<output file>"
```

- Empty output → PASS
- Output contains `Json error:` → FIX → re-validate
- **Never proceed past L0 if it fails**

### L1: Field Completeness (auto-execute)

Compare generated JSON keys against vanilla fields for the same type:

```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\keys.py" --human type=$TYPE
```

Flag any vanilla field that appears in >50% of entries but is MISSING from generated output. Report to user.

### L2: ID Uniqueness (auto-execute)

```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\list_duplicates.py"
```

Also scan Medieval mod directory for existing IDs using `grep_code`.

### L3: Field Logic Consistency (MANDATORY, auto-execute)

**对每个生成的 item 逐一核对以下逻辑检查清单，杜绝字段组合上的低级错误。**

#### ARMOR 专用检查

| # | 检查项 | 规则 |
|---|--------|------|
| A1 | `covers` 与装备部位一致 | 颈部装备(gorget/aventail/standard) → `covers: ["head"]` + `specifically_covers: ["head_throat", "head_nape"]`，**绝不能** `covers: ["torso"]` |
| A2 | `covers` body part 存在 | 核对 `body_parts.json`，确认 covers 的 body part 有效（如 `head`/`torso`/`arm_l`/`arm_r`/`leg_l`/`leg_r` 等） |
| A3 | `specifically_covers` 是其 covers body part 的有效子部位 | 如 `head_throat` 仅属于 `head`，不能出现在 `covers: ["torso"]` 的 section 下 |
| A4 | `encumbrance` vs `encumbrance_modifiers` 互斥 | 同一 armor section 内不能同时出现两者 |
| A5 | 非 head 部位不写 `encumbrance_modifiers` | 仅 head 有 `encumbrance_per_weight` 表，torso/arm/leg 等必须用直接 `encumbrance` |
| A6 | `rigid_layer_only` 只用于 eyes/mouth | 不能用于 head/torso 等主部位 |
| A7 | `*_steel_chain` 材料 thickness 是 1.2 的整数倍 | 有效值: 1.2, 2.4, 3.6... |
| A8 | `layers` 不包含 `BELTED`（ARMOR 类型） | `BELTED` layer 仅限背包/挂颈工具等非服装物品 |

#### 通用物品检查

| # | 检查项 | 规则 |
|---|--------|------|
| G1 | `name.str` 有 `med_` 前缀 | 格式: `"med_ item name"` |
| G2 | `type` 字段存在且正确 | 必须: `ARMOR`, `GENERIC`, `TOOL`, `COMESTIBLE`, 等 |
| G3 | `material` 中所有 ID 在 `materials.json` 中存在 | 检查自建材料是否已定义 |
| G4 | `weight` 单位合理 | 布帽 100-500g, 皮甲 300-1000g, 板甲件 1500-3500g |
| G5 | `price` / `price_postapoc` 成比例 | postapoc 约为 price 的 1/5 ~ 1/10 |

#### 执行方式

生成每个 JSON 文件后，对照上述清单逐项人工核对。发现任何违反立即修正后重新 L0。

### Validation Loop

```
Generate → L0 fail? → Fix → re-check
              ↓ pass
            L1 check → Warnings? → Fix criticals
              ↓
            L2 check → Duplicate? → Rename → re-validate
              ↓
            L3 field logic → Violations? → Fix → re-validate
              ↓
            Notify user
```

---

## Phase 4: Completion

Notify user with:
- List of generated files with full paths
- List of all item/entity IDs created
- Reminder: "Run in-game to test. Verify: appearance, stats, spawn behavior, recipe integration."

---

## Reference: Type-Specific Cheatsheets

These are EXAMPLES for common types. Use `keys.py` to discover any type's fields.

### ARMOR Protection Values

| Armor Class | `protection` | `material_thickness` |
|-------------|-------------|---------------------|
| Cloth/linen | `{"bash":2,"cut":1,"stab":0,"bullet":0}` | 1 |
| Padded/gambeson | `{"bash":5,"cut":4,"stab":2,"bullet":1}` | 3-4 |
| Leather | `{"bash":3,"cut":5,"stab":3,"bullet":1}` | 2-3 |
| Mail | `{"bash":3,"cut":12,"stab":6,"bullet":2}` | 4-5 |
| Brigandine | `{"bash":10,"cut":14,"stab":12,"bullet":4}` | 5-7 |
| Plate | `{"bash":14,"cut":18,"stab":16,"bullet":6}` | 7-10 |

### ARMOR Layers (`specifically_covers`)

| Layer | CDDA value |
|-------|-----------|
| Skin (内衣) | `armor_skin` |
| Normal (正常层) | `armor_normal` |
| Outer (外层) | `armor_outer` |
| Strapped (绑缚) | `armor_strapped` |

### Body Parts (`covers`)

```
head, eyes, mouth, torso, arm_l, arm_r, hand_l, hand_r, leg_l, leg_r, foot_l, foot_r
```

### Encumbrance Guidelines

> 详见规则 0。encumbrance 与 encumbrance_modifiers 互斥，同一个 armor section 只能用其一。

| 装备类型 | encumbrance |
|----------|-------------|
| Underclothes | 1-3 |
| Light clothing | 2-5 |
| Gambeson | 8-15 |
| Mail hauberk | 15-25 |
| Plate components | 10-20 each |

### Weapon Techniques

Common: `WBLOCK_1`, `WBLOCK_2`, `RAPID`, `SWEEP`, `PRECISE`, `BRUTAL`, `STAB`

Full schemas in [reference/cdda_schema.md](reference/cdda_schema.md).

---

## ARMOR Writing Rules (Verified)

> 以下规则经实际测试验证，违反会导致游戏 JSON 加载错误。

### 规则 0: `encumbrance` 与 `encumbrance_modifiers` 互斥（同一 section 内）

**同一个 armor section 内只能使用其一。** 源码 `item_factory.cpp:2903` 用 `if/else if/else` 加载，不会叠加。**同一个 item 内可混合**（主 section 用 modifiers，eyes/mouth 等子 section 用 direct encumbrance）。

```json
// 错误 — 同一 section 内同时存在:
{ "covers": ["head"], "encumbrance": 6, "encumbrance_modifiers": ["WELL_SUPPORTED"] }

// head 主 section：重量驱动
{ "covers": ["head"], "encumbrance_modifiers": ["WELL_SUPPORTED"] }

// eyes/mouth 子 section：直接值
{ "covers": ["eyes"], "encumbrance": 20, "rigid_layer_only": true }
```

#### 可用 modifier 与效果

`calc_encumbrance`（`itype.cpp:340`）从物品重量 × `encumbrance_per_weight` 表计算基础值，再叠加 modifier：

| Modifier | 类型 | 效果 |
|----------|------|------|
| `NONE` | FLAT 0 | 纯重量推导 |
| `WELL_SUPPORTED` | MULT -20 | 重量×0.8 |
| `RESTRICTS_NECK` | FLAT +10 | 重量推导 + 10 |
| `IMBALANCED` | FLAT +10 | 重量推导 + 10 |

计算流程（`itype.cpp:370-389`）：
```
multiplier = 100 + sum(MULT)    // WELL_SUPPORTED → 80
flat = sum(FLAT)                // RESTRICTS_NECK → 10
final = base × multiplier/100 + flat
```

> 如：2500g great helm + `RESTRICTS_NECK + WELL_SUPPORTED` → base≈66 → ×0.8 + 10 → ≈63 head encumbrance。

#### 设计理念：modifier 表达人体工学年代

越古老的装备越缺乏人体工学，反映在 modifier 组合：

| 装备 | Modifier | 设计含义 |
|------|----------|---------|
| 布帽/皮帽（轻量） | `["NONE"]` | 重量可忽略 |
| kettle hat（简单钢盔） | `["NONE"]` | 重量直接传导 |
| sallet/bascinet（中期） | `["WELL_SUPPORTED"]` | 人体工学好，×0.8 |
| great helm（古早） | `["RESTRICTS_NECK", "WELL_SUPPORTED"]` | ×0.8+10 偏移 |
| scrap（粗制） | `["IMBALANCED"]` | +10 偏移 |

> 此分组比原版更清晰——原版 conical helm(1425g) 用了 RESTRICTS_NECK+WELL_SUPPORTED，但更重的 kettle helm(2555g) 只用 NONE。我们按设计年代分配，逻辑更一致。

#### 关键限制

- `calc_encumbrance` 仅对 **head** body part 有效（只有 head 定义了 `encumbrance_per_weight` 查询表）
- **非 head 部位必须用直接 `encumbrance` 值**（torso/arm/leg 等会报错 "Can't find a notable point"）

### 规则 0.5: 颈部装备用 `head` + `head_throat`/`head_nape`

`torso_neck` 在 `body_parts.json` 中标记为 `"secondary": true`。源码 `item_factory.cpp:2006` 强制检查：secondary sub-body-part 只能用于 BELTED 层（背包、挂颈工具等），ARMOR 类型不可用。

颈部装甲的**正确**做法是盖 `head` body part 的 throat/nape 子部位（和原版 aventail 一致）：

```json
// 错误 — 盖 torso 会让防护落在躯干而不是颈部:
{
  "covers": ["torso"],
  "coverage": 95,
  "encumbrance": 5
}

// 正确 — 盖 head 的 throat/nape 子部位:
{
  "covers": ["head"],
  "specifically_covers": ["head_throat", "head_nape"],
  "coverage": 95,
  "encumbrance": 5
}
```

| 颈部装备 | covers | specifically_covers |
|----------|--------|---------------------|
| aventail (锁子甲帘) | `head` | `head_nape`, `head_throat` |
| leather standard (皮护颈) | `head` | `head_throat` |
| gorget (板甲护喉) | `head` | `head_nape`, `head_throat` |

> 参照原版 `lc_chainmail_aventail`（`head_attachments.json`）: `covers: ["head"]`, `specifically_covers: ["head_nape", "head_throat"]`。

### 规则 1: 多材料等级用 `copy-from` + `replace_materials`

遵循原版 brigandine 模式：**一种盔甲的所有钢材等级放同一个文件**。

```json
// 基础定义 (lc_steel，完整字段):
{ "id": "medieval_cuirass_lc", "type": "ARMOR", "material": ["lc_steel", "leather"], "armor": [...] }

// 钢材升级版 (3行搞定):
{ "id": "medieval_cuirass_mc", "copy-from": "medieval_cuirass_lc", "name": {...}, "replace_materials": {"lc_steel": "mc_steel"} }
{ "id": "medieval_cuirass_hc", "copy-from": "medieval_cuirass_lc", "name": {...}, "replace_materials": {"lc_steel": "hc_steel"} }
```

钢材等级链: `budget_steel` → `lc_steel` → `mc_steel` → `hc_steel` → `ch_steel` → `qt_steel`
锁子甲等级链: `budget_steel_chain` → `lc_steel_chain` → `mc_steel_chain` → `hc_steel_chain` → `ch_steel_chain` → `qt_steel_chain`

### 规则 2: Per-Section Material 格式

新版 armor 数据**必须**使用 per-section material 定义（而非旧的顶层 `protection` / `material_thickness`）:

```json
"armor": [
  {
    "material": [
      { "type": "steel", "covered_by_mat": 100, "thickness": 2.0 },
      { "type": "leather", "covered_by_mat": 95, "thickness": 0.5 }
    ],
    "covers": ["torso"],
    "coverage": 95,
    "encumbrance": 18
  }
]
```

- `covered_by_mat`: 该材料覆盖的区域百分比（100=全覆盖，<100=部分覆盖）
- `thickness`: 材料厚度(mm)，引擎以此 × 材料基础 resist 值计算最终防护。**若材料定义了 `sheet_thickness`，`thickness` 必须是其整数倍。**
  - `*_steel_chain` 材料 `sheet_thickness` = 1.2 → 有效厚度: 1.2, 2.4, 3.6...
  - `kevlar_layered` 材料 `sheet_thickness` = 4.4 → 有效厚度: 4.4, 8.8...
  - 普通 `*_steel` 板材无 `sheet_thickness`（默认 0），无限制
  - 如需绕过，可在 material 对象中加 `"ignore_sheet_thickness": true`
- 真实板甲厚度约 1.5-2.0mm，布甲厚度 2-5mm

### 规则 3: 头盔面甲用 `rigid_layer_only`

头盔的 visor/面甲部分必须加 `"rigid_layer_only": true`，只对硬质外层生效:

```json
{
  "material": [{ "type": "steel", "covered_by_mat": 100, "thickness": 1.5 }],
  "covers": ["eyes"],
  "coverage": 95,
  "encumbrance": 20,
  "rigid_layer_only": true
}
```

### 规则 4: 锁子甲材料用 `_chain` 变体

锁子甲必须用 `steel_chain` 系列材料（`soft: true` + `breathability: GOOD`），不能用普通 `steel` 系列。
引擎通过此区分锁子甲（软编）和板甲（硬板）的材料行为。

### 规则 5: 版甲 `sided` 属性

需要左右成对的部件（手套、靴子、臂甲、腿甲），有些原版加了 `"sided": true`。
测试表明该字段非必须（引擎默认处理），但加上了无害。

### 规则 6: VARSIZE 盔甲需加 `FIT` flag

`VARSIZE` 表示"可调整适配"而非"已合身"。`item.cpp:3501` 逻辑：
- 有 `FIT` → 显示 `(fits)`
- 有 `VARSIZE` 无 `FIT` → 显示 `(poor fit)`

所有中世纪 VARSIZE 盔甲应加 `FIT`，确保初始即合身：

```json
"flags": [ "VARSIZE", "STURDY", "OUTER", "FIT" ]
```
