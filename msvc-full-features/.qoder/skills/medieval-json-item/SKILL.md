---
name: medieval-json-item
description: Generate CDDA JSON data for Medieval mod items (ARMOR, GENERIC, TOOL, COMESTIBLE, etc.). Automatically validates syntax, field completeness, ID uniqueness, and field logic consistency. Use when the user asks to generate equipment, weapons, tools, consumables, or any CDDA item data.
---

# Medieval Mod JSON Item Generator

Generate CDDA-compliant item JSON for `E:\Cataclysm-Medieval\data\mods\Medieval\`.

---

## Quick Decision Tree

```
User request
  ├─ Design doc? → Parse doc → Determine CDDA type(s)
  │               → keys.py to discover fields
  │               → Map design data → CDDA fields → Generate JSON
  └─ No doc? → Request specs from user → proceed as above
  │
  ├─ Write file to Medieval mod dir
  ├─ Validate: L0 syntax → L1 fields → L2 ID uniqueness → L3 field logic
  ├─ L4: C++ Ground-Truth Check (MANDATORY — invoke medieval-json-check)
  │   └─ Exit 0 → Done ✓
  │   └─ Exit 1 → Fix errors → loop L0→L4 on changed files until clean
  └─ Notify user with final result
```

---

## Phase 1: Research & Generate

Always run `keys.py` first to discover available fields for the type, then map design data to CDDA fields:

```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\keys.py" --human type=$TYPE
```

Reference tools: `values.py -k $FIELD --human type=$TYPE` (valid values), `pluck.py type=$TYPE` (vanilla examples). See [reference/cdda_schema.md](reference/cdda_schema.md) for type-specific patterns.

---

## Universal JSON Rules

### ID Naming

Descriptive, no strict prefix: `hood_linen`, `helm_kettle`.

### Name Format & Plural Forms (CRITICAL)

`name` **must always be an object**, never a plain string. All display names use `med_` prefix.

The C++ loader auto-generates plural forms for simple nouns, but fails for pairs/plurals. **Declare plural forms explicitly for every item.**

| 物品 | 写法 | 例子 |
|------|------|------|
| 天然单数（单复数不同） | `"str"` + `"str_pl"` | `"str": "med_ cuirass", "str_pl": "med_ cuirasses"` |
| 天然复数（成对/集合） | `"str_sp"` only | `"str_sp": "med_ leather boots"` |

**天然复数关键词** (只用 `str_sp`): boots, shoes, sabatons, pattens, footwraps, turnshoes, gloves, mittens, gauntlets, handwraps, wristwraps, hose, chausses, braies, leggings, leg wraps, pants, greaves, vambraces, pauldrons — 及任何以 `-s` 结尾的复数名。

```json
// 正确
"name": { "str": "med_ cuirass", "str_pl": "med_ cuirasses" }
"name": { "str_sp": "med_ leather boots" }

// 错误 — str_sp + str 共存 → C++ loader 拒绝
"name": { "str": "med_ leather boots", "str_sp": "med_ leather boots" }

// 错误 — 天然复数缺 str_sp → auto-generation 报 warning
"name": { "str": "med_ wool mittens" }
```

### Common Fields Template

```json
{
  "type": "$TYPE", "id": "descriptive_id",
  "name": { "str": "med_ ..." },
  "description": "...",
  "weight": "XXX g", "volume": "X L",
  "price": XXXX, "price_postapoc": XXX,
  "material": ["material_id"],
  "symbol": "X", "color": "color_name"
}
```

Materials: `cotton, wool, leather, fur, steel, iron, wood, bone, bronze, copper, brass, silver, gold`. Verify with `values.py -k material`.

---

## Phase 2: File Output

Write directly to `E:\Cataclysm-Medieval\data\mods\Medieval\`. Group by subdirectory (`items/armor/`, `items/weapons/`). One JSON array per file.

---

## Phase 3: Validation

### L0-L2 Quick Reference

| Level | Tool | Rule |
|-------|------|------|
| L0 Syntax | `json_formatter.exe <file>` | Empty output = pass. `Json error:` = fix. **Never proceed past L0 if it fails.** |
| L1 Fields | `keys.py --human type=$TYPE` | Flag fields in >50% of vanilla but missing from output. |
| L2 ID | `list_duplicates.py` + grep_code | No duplicate IDs across mod. |

### L3: Field Logic Checklist (MANDATORY)

对照以下清单逐一核对每个生成的 item。

#### ARMOR 专用

| # | 检查项 | 规则 |
|---|--------|------|
| A1 | `covers` vs 部位 | 颈部 → `covers: ["head"]` + `specifically_covers: ["head_throat","head_nape"]`，不可 `covers: ["torso"]` |
| A2 | body part 有效 | covers 的 body part 在 `body_parts.json` 中存在 |
| A3 | 子部位归属 | `specifically_covers` 必须是其 covers body part 的有效子部位 |
| A4 | encumbrance 互斥 | 同一 section 内 `encumbrance` 与 `encumbrance_modifiers` 不可共存 |
| A5 | modifiers 仅 head | 非 head 部位必须用直接 `encumbrance` |
| A6 | rigid_layer_only | 仅 eyes/mouth，不可用于 head/torso 主部位 |
| A7 | chain thickness | `*_steel_chain` 厚度 = 1.2×N: 1.2, 2.4, 3.6... |
| A8 | BELTED layer | ARMOR 不可用 `BELTED` layer |

#### 通用

| # | 检查项 | 规则 |
|---|--------|------|
| G1 | name 前缀 | `med_` |
| G2 | type 字段 | ARMOR/GENERIC/TOOL/COMESTIBLE 等 |
| G3 | material IDs | 均在 `materials.json` 中已定义 |
| G4 | weight 范围 | 布帽 100-500g, 皮甲 300-1000g, 板甲件 1500-3500g |
| G5 | price 比例 | postapoc ≈ price/5 ~ price/10 |

违反任何规则 → 立即修正 → 重新 L0。

### L4: C++ Ground-Truth Check (MANDATORY)

This is the same pipeline the game uses when loading a world. L0-L3 catch rest errors only; L4 exercises real type handlers and the full ~45-step `check_consistency` chain.

```
cd E:\Cataclysm-Medieval
.\cataclysm-tiles.exe --check-mods medieval 2> check_errors.txt
```

| Exit | Action |
|------|--------|
| 0 | All passed → notify user |
| 1 | Fix errors → loop L0→L4 on changed files until exit 0 |

Report unfixable errors to user with file locations. **Never skip L4.** Unknown JSON types are silently skipped at L0 — only C++ check verifies all data actually loaded.

---

## Phase 4: Completion

L4 exit 0 → report files/IDs + "JSON passed full C++ pipeline (~45 check_consistency steps). Test in-game." L4 exit 1, unfixable → report errors + locations → ask user for direction.

---

## Reference: Type-Specific Cheatsheets

Use `keys.py` to discover any type's fields. See [reference/cdda_schema.md](reference/cdda_schema.md) for full schemas.

### ARMOR Protection Values

| Class | protection | thickness |
|-------|-----------|-----------|
| Cloth/linen | `{"bash":2,"cut":1,"stab":0,"bullet":0}` | 1 |
| Padded/gambeson | `{"bash":5,"cut":4,"stab":2,"bullet":1}` | 3-4 |
| Leather | `{"bash":3,"cut":5,"stab":3,"bullet":1}` | 2-3 |
| Mail | `{"bash":3,"cut":12,"stab":6,"bullet":2}` | 4-5 |
| Brigandine | `{"bash":10,"cut":14,"stab":12,"bullet":4}` | 5-7 |
| Plate | `{"bash":14,"cut":18,"stab":16,"bullet":6}` | 7-10 |

### Other Quick Reference

Layers: `armor_skin` / `armor_normal` / `armor_outer` / `armor_strapped`
Body parts: `head, eyes, mouth, torso, arm_l, arm_r, hand_l, hand_r, leg_l, leg_r, foot_l, foot_r`
Encumbrance: underclothes 1-3, light clothing 2-5, gambeson 8-15, mail hauberk 15-25, plate 10-20 each
Weapon techniques: `WBLOCK_1, WBLOCK_2, RAPID, SWEEP, PRECISE, BRUTAL, STAB`

---

## ARMOR Writing Rules (Verified)

### Rule 0: encumbrance modifiers (head only)

同一 section 内 `encumbrance` 与 `encumbrance_modifiers` 互斥。同一 item 内不同 section 可混合。

| Modifier | 效果 | 适用场景 |
|----------|------|---------|
| `NONE` | 纯重量推导 | 轻布帽/皮帽、kettle hat |
| `WELL_SUPPORTED` | ×0.8 | sallet/bascinet（中期人体工学盔） |
| `RESTRICTS_NECK` | +10 | great helm（古早大型盔） |
| `IMBALANCED` | +10 | scrap/粗制 |

仅 **head** body part 有 `encumbrance_per_weight` 查询表，可使用 modifiers。非 head 部位（torso/arm/leg）必须用直接 `encumbrance`。

```json
// head 主 section：重量驱动
{ "covers": ["head"], "encumbrance_modifiers": ["WELL_SUPPORTED"] }
// eyes/mouth 子 section：直接值
{ "covers": ["eyes"], "encumbrance": 20, "rigid_layer_only": true }
```

### Rule 0.5: 颈部装甲用 head + head_throat/head_nape

颈部装甲盖 `head`（非 `torso`），`specifically_covers` 用 `head_throat`/`head_nape`：

| 装备 | covers | specifically_covers |
|------|--------|---------------------|
| aventail (锁子甲帘) | `head` | `head_nape`, `head_throat` |
| leather standard (皮护颈) | `head` | `head_throat` |
| gorget (板甲护喉) | `head` | `head_nape`, `head_throat` |

### Rule 1: 钢材等级用 copy-from + replace_materials

同一盔甲的所有钢材等级放在同一个文件，基础定义写完整字段，升级版用 copy-from：

```json
{ "id": "cuirass_lc", "type": "ARMOR", "material": ["lc_steel", "leather"], "armor": [...] }
{ "id": "cuirass_mc", "copy-from": "cuirass_lc", "name": {...}, "replace_materials": {"lc_steel": "mc_steel"} }
{ "id": "cuirass_hc", "copy-from": "cuirass_lc", "name": {...}, "replace_materials": {"lc_steel": "hc_steel"} }
```

等级链: `budget_steel → lc_steel → mc_steel → hc_steel → ch_steel → qt_steel`
锁子甲链: `budget_steel_chain → lc_steel_chain → mc_steel_chain → hc_steel_chain → ch_steel_chain → qt_steel_chain`

### Rule 2: Per-section material 格式

必须使用 per-section material 定义（非旧的顶层 `protection`/`material_thickness`）：

```json
"armor": [{
  "material": [
    { "type": "steel", "covered_by_mat": 100, "thickness": 2.0 },
    { "type": "leather", "covered_by_mat": 95, "thickness": 0.5 }
  ],
  "covers": ["torso"], "coverage": 95, "encumbrance": 18
}]
```

- `covered_by_mat`: 材料覆盖百分比（100=全覆盖）
- `thickness`: 若材料定义了 `sheet_thickness`（如 `*_steel_chain`=1.2），必须是其整数倍。普通 `*_steel` 无限制。真实板甲 1.5-2.0mm，布甲 2-5mm。

### Rule 3: 头盔面甲用 rigid_layer_only

```json
{ "material": [{"type":"steel","covered_by_mat":100,"thickness":1.5}], "covers":["eyes"], "coverage":95, "encumbrance":20, "rigid_layer_only":true }
```

### Rule 4: 锁子甲用 _chain 材料

锁子甲必须用 `steel_chain` 系列（`soft:true`），不可用普通 `steel`。

### Rule 5: VARSIZE + FIT

`VARSIZE` = 可调整，非"已合身"。所有中世纪 VARSIZE 盔甲必须同步加 `FIT`：

```json
"flags": [ "VARSIZE", "STURDY", "OUTER", "FIT" ]
```
