---
name: medieval-json-mapgen
description: Generate CDDA mapgen JSON for Medieval mod (overmap_terrain, palette, mapgen with ASCII rows). Handles the full binding chain from overmap symbol to 24x24 tile layout, plus city generation pipeline (city_building + region_overlay). Use when the user asks to create buildings, terrain features, mapgen layouts, overmap definitions, or settlement content.
---

# Medieval Mod JSON Mapgen Generator

Generate CDDA-compliant mapgen data for `E:\Cataclysm-Medieval\data\mods\Medieval\`.

---

## Quick Workflow

```
User request
  ├─ 1. Choose terrain/furniture IDs from [terrain_furniture_reference.md](terrain_furniture_reference.md)
  ├─ 2. Design 24x24 ASCII layout → verify 24 rows x 24 cols
  ├─ 3. Validate door/window placement (MUST replace walls, not insert beside them)
  ├─ 4. Write palette + mapgen JSON → 10_medieval_core/mapgen/<name>.json
  ├─ 5. Write/append overmap_terrain + city_building → 10_medieval_core/overmap/
  ├─ 6. Add to region_overlay pool → 00_cleanup/region_overlay.json
  ├─ 7. Run medieval-json-check → C++ level validation (exit 0 required)
  └─ 8. Test in-game (Map Editor: Debug → M → o → find → Apply)
```

---

## File Locations

| Content | Path |
|---------|------|
| Mapgen + Palette | `10_medieval_core/mapgen/<name>.json` |
| Overmap terrain | `10_medieval_core/overmap/overmap_terrain.json` |
| City building entries | `10_medieval_core/overmap/city_building.json` |
| Road override | `00_cleanup/road_override.json` |
| region_overlay (city pools) | `00_cleanup/region_overlay.json` |
| City toggle | `00_cleanup/game_balance.json` (OVERMAP_PLACE_CITIES: true) |

All paths relative to `E:\Cataclysm-Medieval\data\mods\Medieval\`. `10_medieval_core/` loads recursively.

---

## The Binding Chain

### Single building (standalone / map editor test)

```
overmap_terrain.id  =  mapgen.om_terrain   (same string)
```

### City-placed building (appears automatically in generated cities)

```
city_building.id  →  overmap_terrain._north  →  mapgen.om_terrain
                         │                          │
                  C++ auto-generates          single mapgen rotated
                  _east/_south/_west          0/90/180/270° at runtime
```

**Key**: `oter_type_t::finalize()` auto-creates 4 directional peers from one base definition. `get_mapgen_id()` strips the direction suffix. **1 city_building + 1 overmap_terrain + 1 mapgen = 4 rotated variants. No 4 JSON variants needed.**

---

## Phase 1: Palette Definition

```json
{
  "type": "palette",
  "id": "farmstead_t5_palette",
  "terrain": {
    "_": "t_grass", "#": "t_wall_wattle", "+": "t_door_c",
    "o": "t_window_empty", ".": "t_dirtfloor", ",": "t_dirt",
    "f": "t_splitrail_fence"
  },
  "furniture": {
    "b": "f_straw_bed", "t": "f_table", "c": "f_chair",
    "F": "f_fireplace", "h": "f_hay"
  }
}
```

- Furniture-only characters (like `b`) inherit terrain from `fill_ter`
- Do NOT reference `item_group` — all vanilla item_groups are empty
- Characters needing terrain+furniture must appear in both `terrain` and `furniture` maps

---

## Phase 2: Mapgen Definition

```json
{
  "type": "mapgen", "method": "json",
  "om_terrain": [ "medieval_farmstead_t5" ], "weight": 100,
  "object": {
    "fill_ter": "t_grass",
    "flags": [ "ERASE_ALL_BEFORE_PLACING_TERRAIN" ],
    "rows": [ /* 24 rows x 24 chars each */ ],
    "palettes": [ "farmstead_t5_palette" ]
  }
}
```

- `fill_ter`: default terrain for unmapped tiles (outdoor=t_grass, indoor=t_dirtfloor)
- `ERASE_ALL_BEFORE_PLACING_TERRAIN`: required to clear procedural terrain
- Exactly 24 rows, each exactly 24 chars. Spaces are NOT valid.

---

## Phase 3: Door/Window Placement (MANDATORY CHECK)

**Rule**: Door/window must REPLACE a wall character, not insert beside it. Row stays 24 chars.

**WRONG** (25 chars, door inserted between walls):
```
#######.+##########
```

**CORRECT** (24 chars, door replaces wall):
```
#######+##########
```

**Verification trick**: Write wall-only row first, then substitute:
```
Step 1:  SSSSSSSSSSSSSSSSSSSSSSSS  (24 S's)
Step 2:  SSSSSSS+SSSSSSSSSSSSSSSS  (replace S at col 7 → 24 chars)
```

Checklist for every row with `+`/`o`/`w`:
- Door/window position is where a wall would be
- Row exactly 24 chars
- Wall continuous on both sides

---

## Phase 4: 24x24 Design Tips

### Common characters

| Char | Terrain | Furniture |
|------|---------|-----------|
| `_` | `t_grass` | — |
| `,` | `t_dirt` | — |
| `.` | `t_dirtfloor` | — |
| `f` | `t_splitrail_fence` | — |
| `#` | `t_wall_wattle` | — |
| `+` | `t_door_c` | — |
| `o` | `t_window_empty` | — |
| `b` | — | `f_straw_bed` |
| `t` | — | `f_table` |
| `c` | — | `f_chair` |
| `F` | — | `f_fireplace` |

### Quick picks by building type

| Building | Wall | Floor | Key Furniture |
|----------|------|-------|---------------|
| Farmhouse | `t_wall_wattle` | `t_dirtfloor` | `f_straw_bed`, `f_fireplace`, `f_table` |
| Barn | `t_wall_wood` | `t_dirtfloor` | `f_hay` |
| Log cabin | `t_wall_log` | `t_floor_primitive` | `f_straw_bed`, `f_woodstove` |
| Stone church | `t_rock_wall` | `t_rock_floor` | `f_brazier` |
| Smithy | `t_wall_wood` | `t_dirtfloor` | `f_forge`, `f_anvil` |

Full catalog: [terrain_furniture_reference.md](terrain_furniture_reference.md)

---

## Phase 5: Overmap Terrain + City Building

### overmap_terrain.json
```json
{
  "type": "overmap_terrain",
  "id": [ "medieval_farmstead_t5" ],
  "name": "abandoned farmstead",
  "sym": "+", "color": "brown", "see_cost": 5
}
```
Avoid blacklisted flags: LAB, MAN_MADE, MILITARY, URBAN, FARM, EXODII.

### city_building.json
```json
{
  "type": "city_building",
  "id": "medieval_farmhouse",
  "locations": [ "land" ],
  "overmaps": [
    { "point": [ 0, 0, 0 ], "overmap": "medieval_farmstead_t5_north" }
  ]
}
```
- `overmaps[].overmap` references `_north` variant (C++ generates other 3)
- `locations: ["land"]` required
- `point: [0,0,0]` for single-tile

---

## Phase 6: Region Overlay (City Pools)

Add the city_building ID to `00_cleanup/region_overlay.json`:

| Pool | Placement zone | Weight range |
|------|---------------|--------------|
| `houses` | Throughout city | 500-1000 |
| `shops` | Near center | 200-400 |
| `parks` | Medium distance | 100-300 |

```json
"city": {
  "clear_houses": true, "clear_shops": true, "clear_parks": true,
  "houses": { "medieval_farmhouse": 500 },
  "shops": { "medieval_smithy": 300 },
  "parks": { "medieval_church": 200 }
}
```

**CRITICAL**: `clear_*` flags require C++ patch (see Phase 7). Without them, new buildings are ADDED to vanilla pools (~7% probability), not replacing them.

---

## Phase 7: Road Override

```json
{
  "type": "overmap_terrain",
  "id": "road",
  "copy-from": "road",
  "name": "dirt road",
  "color": "brown",
  "travel_cost_type": "dirt_road"
}
```

- MUST use `copy-from` to preserve `generic_transportation` chain → `land_use_code: "transportation"`
- Without `copy-from`: runtime crash `"invalid overmap terrain id"` (`generic_factory.h:509`)
- `overmap_terrain` does NOT support `"delete"` field (unlike monster/item)
- `--check-mods` does NOT detect missing `land_use_code` — runtime only
- `road`: keep `LINEAR` flag. `road_nesw_manhole`/`city_center`: keep `NO_ROTATE`, add `REQUIRES_PREDECESSOR`

---

## Phase 8: Validation + Testing

### Validation
Run `medieval-json-check` skill → `cataclysm-tiles.exe --check-mods medieval`. Exit 0 required.

### In-game test
1. New world with Medieval mod, CITY_SIZE=2, CITY_SPACING=7
2. For standalone mapgen: Debug → M → o → find ID → Apply
3. Overmap Editor only changes overmap symbol — does NOT trigger mapgen. Use Map Editor.

---

## Phase 9: C++ Patch (clear houses/shuts/parks)

In `src/regional_settings.cpp`, after the `load_building_types` lambda (~line 698):

```cpp
if( cityjo.get_bool( "clear_houses", false ) ) {
    region.city_spec.houses.clear();
}
if( cityjo.get_bool( "clear_shops", false ) ) {
    region.city_spec.shops.clear();
}
if( cityjo.get_bool( "clear_parks", false ) ) {
    region.city_spec.parks.clear();
}
```

`building_bin::clear()` already exists (line 1049). Recompile after modifying.

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Door inserted beside wall | Row length != 24 | Door must REPLACE wall char, not insert |
| Missing `copy-from` on road | `invalid overmap terrain id` crash | Add `"copy-from": "road"` etc. |
| No `clear_*` flags | Modern buildings still appear | Add `clear_houses/shuts/parks: true` + C++ patch |
| `locations` missing on city_building | check-mods error | Add `"locations": ["land"]` |
| `sym` missing on road_nesw_manhole | MAP_GEN error | Add `"sym": "+"` |
| `delete` used on overmap_terrain | JSON error | Not supported for this type |
| Overmap Editor instead of Map Editor | Mapgen not triggered | Use Map Editor (`M` → `o`) |
| item_group in palette | Loot failure | No item groups (all vanilla are empty) |
| CITY_SIZE not set | Giant modern cities | Player must set CITY_SIZE=2 manually |

---

## Additional Resources

- [terrain_furniture_reference.md](terrain_furniture_reference.md) — full terrain/furniture catalog
- [code_city_generation_system.md](../docs/vanilla/code_city_generation_system.md) — C++ city pipeline
- [design06-建筑.md](../docs/design/design06-建筑.md) — building design planning
- [medieval_settlement.md](../docs/process/medieval_settlement.md) — implementation progress
