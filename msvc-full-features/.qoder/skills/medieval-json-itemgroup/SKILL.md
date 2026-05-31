---
name: medieval-json-itemgroup
description: Generate or augment CDDA item_group JSON for the Medieval mod. Covers all 9 organizational dimensions (room/furniture, clothing sets, weapons, food, locations, monster drops, NPC gear, containers, shops). Supports demand-driven creation when mapgen or item skills discover missing groups, and item-to-group lookup via itemgroups.py. Use when item_groups need creation, augmentation, or querying.
---

# Medieval Mod JSON Item Group Generator

Generate CDDA-compliant item_group JSON in `E:\Cataclysm-Medieval\data\mods\Medieval\10_medieval_core\itemgroups\`.

---

## Quick Decision Tree

```
Request
  ├─ "Create item_group for X" → Determine dimension → Compose entries → Write file → Validate
  ├─ "Add Y to item_groups" → itemgroups.py --map → Find target groups → Augment (extend)
  ├─ "Which groups contain Y?" → itemgroups.py --map → Report
  └─ Called by another skill (item/mapgen) → Missing group? → Create. Existing but incomplete? → Augment.
```

---

## Phase 0: Determine Dimension

Classify the group into one of 9 dimensions. This determines naming, file placement, and entry strategy.

| # | Dimension | File | Example IDs | Trigger |
|---|-----------|------|-------------|---------|
| 1 | Room/Furniture | `domestic.json` | `kitchen`, `bedroom`, `nightstand`, `garden_shed` | mapgen creates building |
| 2 | Clothing Set | `clothing.json` / `clothing_{type}.json` | `clothing_male`, `pants_peasant`, `winter` | profession/NPC needs outfit |
| 3 | Weapons/Ammo | `weapons.json` / `ammo.json` | `weapons_swords`, `bows`, `arrows` | weapon items created |
| 4 | Food/Drink | `food.json` | `snacks`, `condiments`, `pantry` | food items created |
| 5 | Location/Building | `locations.json` / `locations_{type}.json` | `mansion`, `prison` | unique building needs loot |
| 6 | Monster Drops | `monster_drops.json` | `human_parts`, `ant_food` | monster/NPC created |
| 7 | NPC/Profession Gear | `npc_gear.json` / `professions.json` | `starting_gear_blacksmith` | profession created |
| 8 | Container Pre-assembly | `domestic.json` bottom | `{item}_{container}_{count}` | item needs container packaging |
| 9 | Shops/Trade | `shops.json` | `blacksmith_shop`, `market_food` | vendor NPC created |

When uncertain, consult [reference/dimensions.md](reference/dimensions.md) for full details.

---

## Phase 1: Item Group JSON Schema

### Minimal Template

```json
[
  {
    "type": "item_group",
    "id": "descriptive_id",
    "subtype": "distribution",
    "entries": [
      { "item": "item_id", "prob": 50 },
      { "item": "item_id_2", "prob": 30, "count": [ 1, 3 ] },
      { "group": "other_group", "prob": 20 }
    ]
  }
]
```

### Subtype Semantics

| Subtype | Meaning | When to Use |
|---------|---------|-------------|
| `distribution` | Pick ONE entry at random (weighted by prob) | Most groups. "This shelf could have X OR Y OR Z." |
| `collection` | Generate ALL entries (prob filters each independently) | Furniture-specific (SUS-style). "This drawer always has forks AND spoons AND knives." |

**Key difference**: `distribution` gives variety (DIFFERENT things each run). `collection` gives completeness (ALL the things that SHOULD be there, every run).

### Entry Types

```json
// Direct item
{ "item": "sword_arming", "prob": 40 }

// Direct item with count
{ "item": "arrow_wood", "prob": 100, "count": [ 10, 30 ] }

// Nested group reference
{ "group": "weapons_swords", "prob": 30 }

// Inline collection (ALL sub-entries generated together)
{ "collection": [ { "item": "hammer" }, { "item": "nail", "count": [ 2, 6 ] } ], "prob": 50 }

// Inline distribution (pick ONE from sub-entries)
{ "distribution": [ { "item": "bear_trap" }, { "item": "rope_30" } ], "prob": 30 }
```

### Container Pre-assembly

```json
{
  "type": "item_group",
  "id": "bread_bag_cloth_4",
  "subtype": "collection",
  "container-item": "bag_cloth",
  "entries": [ { "item": "bread", "container-item": "null", "count": 4 } ]
}
```

`container-item`: wraps the entire group output in this container.
`"container-item": "null"` in entries: item spawns loose inside outer container.

### Nested Guns/Ammo Pattern (reusable for bows/arrows)

```json
// Top-level router
{ "id": "weapons_ranged", "subtype": "distribution",
  "entries": [
    { "group": "bows", "prob": 60 },
    { "group": "crossbows", "prob": 40 }
  ]
}

// Pre-loaded quiver
{ "id": "loaded_quiver", "subtype": "collection",
  "container-item": "quiver",
  "entries": [ { "group": "arrows_hunting", "count": [ 5, 15 ] } ]
}
```

### Augmenting Existing Groups (extend pattern)

When adding to an existing group without replacing it:
```json
{
  "id": "blacksmith_shop",
  "type": "item_group",
  "subtype": "collection",
  "extend": {
    "entries": [
      { "item": "anvil", "prob": 80 },
      { "item": "hammer_blacksmith", "prob": 90 }
    ]
  }
}
```

---

## Phase 2: File Output

Write to `E:\Cataclysm-Medieval\data\mods\Medieval\10_medieval_core\itemgroups\`.

Directory structure follows dimensions:
```
itemgroups/
├── domestic.json       ← Dimension 1: Room/Furniture
├── clothing.json       ← Dimension 2: Clothing sets
├── weapons.json        ← Dimension 3: Weapons/Ammo
├── food.json           ← Dimension 4: Food/Drink
├── locations.json      ← Dimension 5: Location/Building
├── monster_drops.json  ← Dimension 6: Monster/NPC drops
├── professions.json    ← Dimension 7: NPC/Profession starting gear
├── shops.json          ← Dimension 9: Shop/Trade inventories
└── misc.json           ← Uncategorized & container pre-assembly
```

One JSON array per file. Group related IDs together within the file.

---

## Phase 3: Item→Group Lookup

Use the vanilla tool to find which groups already contain an item:

```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\itemgroups.py" --map
```

This recursively traces nested group references and outputs:
```
sword_arming: weapons_swords, blacksmith_shop, knight_starting_gear
```

To find items NOT in any group (orphans):
```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\itemgroups.py" --orphans
```

**Always run --map before augmenting** to avoid duplicating items into groups where they already exist.

---

## Phase 4: Validation

### L0: JSON Syntax

```powershell
"E:\Cataclysm-Medieval\tools\format\json_formatter.exe" <file>
```

Empty output = pass. `Json error:` = fix. **Never proceed past L0 if it fails.**

### L1: ID Uniqueness

Grep the mod for the new group ID to ensure no collisions.

### L2: Semantic Check

| Rule | Check |
|------|-------|
| All `"item"` values reference existing CDDA items | grep mod items for each |
| All `"group"` values reference existing item_groups | grep mod itemgroups |
| `subtype` is `distribution` or `collection` | validate |
| `prob` values are positive integers | validate |
| `count` ranges are `[min, max]` with min ≤ max | validate |

### L3: C++ Ground-Truth Check

```powershell
cd E:\Cataclysm-Medieval
.\cataclysm-tiles.exe --check-mods medieval 2> check_errors.txt
```

| Exit | Action |
|------|--------|
| 0 | Pass → Done |
| 1 | Fix errors → re-validate L0→L3 |

---

## Phase 5: Completion

L3 exit 0 → report: new groups + IDs + "Passed C++ --check-mods. Test in-game."

---

## Design Guidelines

### Prob Design for Distribution Groups

- Anchor common items at `prob: 50-80`
- Uncommon at `prob: 15-30`
- Rare at `prob: 3-10`
- Legendary at `prob: 1-2`
- Probs do NOT need to sum to 100 — they're relative weights

### Collection Groups (SUS-style)

Each entry is a `should this be here?` decision with its own prob:
- Common items: `prob: 80-100`
- Less common: `prob: 40-60`
- Optional: `prob: 10-25`

### Nesting Depth

Keep to 2-3 levels max. Use `group` references for deeper reuse. Don't inline everything.

### Medieval-Specific Conventions

- ID naming: descriptive, lowercase, underscores. No `med_` prefix needed (the mod scope disambiguates).
- Room groups: `{room_type}` or `{room}_{subfeature}` like `blacksmith_shop`, `tavern_counter`
- Clothing groups: `{slot}_{class}` like `tunic_peasant`, `pants_merchant`
- Avoid modern-sounding IDs (`cellphone`, `ammo_pistol`) — these should be in the modern cleanup blacklist.

---

## Cross-Skill Integration

This skill is a **public service** for other medieval skills:

```
medieval-json-item creates new item
  → "This item needs to go into groups: X, Y, Z"
  → Call medieval-json-itemgroup to augment

medieval-json-mapgen creates new building
  → "This building needs furniture groups: A, B, C"
  → Call medieval-json-itemgroup to create missing groups
```

When called by another skill: receive the item/group IDs → determine dimension → create or augment → return the new group IDs.

---

## Additional Resources

- Vanilla org: [json_itemgroup_organization.md](../../docs/vanilla/json_itemgroup_organization.md) — full 9-dimension analysis
- Vanilla grain: [json_itemgroup_monstergroup.md](../../docs/vanilla/json_itemgroup_monstergroup.md) — naming patterns
- Design doc: [design00-清理现代内容.md](../../docs/design/design00-清理现代内容.md) — item_group blacklist strategy
- Dimension reference: [reference/dimensions.md](reference/dimensions.md) — detailed classification guide
