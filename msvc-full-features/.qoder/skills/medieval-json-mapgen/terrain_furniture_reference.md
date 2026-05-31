# Medieval-Compatible Terrain & Furniture Reference

> All IDs are from vanilla CDDA (`E:\Cataclysm-Medieval\data\json\furniture_and_terrain\`).
> Modern/inappropriate IDs (drywall, asphalt, electronics, chain-link fences, etc.) are excluded.

---

## WALLS

| ID | Name | Material | Flammable | Best For |
|----|------|----------|-----------|----------|
| `t_wall_wattle` | wattle-and-daub wall | wood/earth | YES | Peasant houses, village buildings |
| `t_wall_wood` | wooden wall | wood | YES | Barns, sheds, workshops |
| `t_wall_log` | log wall | wood | YES | Cabins, frontier buildings |
| `t_palisade` | palisade wall | wood | YES | Defensive walls, forts |
| `t_rock_wall` | stone wall | stone | NO | Churches, castles, city walls |
| `t_brick_wall` | brick wall | brick | NO | Wealthy townhouses, guildhalls |

### Damaged wall variants

| ID | State |
|----|-------|
| `t_wall_wattle_half` | Half-built wattle |
| `t_wall_wattle_broken` | Broken wattle |
| `t_wall_wood_chipped` | Chipped wood |
| `t_wall_wood_broken` | Broken wood |
| `t_wall_log_half` | Half-built log |
| `t_wall_log_chipped` | Chipped log |
| `t_wall_log_broken` | Broken log |
| `t_rock_wall_half` | Half-built stone |

---

## FLOORS (INDOOR)

| ID | Name | Material | Best For |
|----|------|----------|----------|
| `t_dirtfloor` | dirt floor | earth | Peasant houses, barns, cellars |
| `t_dirtfloor_thatchroof` | dirt floor (thatch roof) | earth | Rustic buildings (paired with thatch roof) |
| `t_floor` | floor (interlocking wood) | wood | Wealthier homes, inns |
| `t_floor_primitive` | primitive floor | wood | Cabins, frontier |
| `t_floor_waxed` | waxed floor | wood | Noble residences |
| `t_rock_floor` | rock floor | stone | Churches, castle interiors |
| `t_marble_floor` | marble floor | marble | Cathedrals, palaces |

---

## FLOORS (OUTDOOR)

| ID | Name | Best For |
|----|------|----------|
| `t_grass` | grass | Natural ground cover |
| `t_dirt` | dirt | Packed paths, yards |
| `t_mud` | mud | Wet areas, pig pens |
| `t_clay` | clay | Clay deposits |
| `t_sand` | sand | Riverbanks, shores |
| `t_dirtmound` | upturned dirt | Construction sites, graves |

### Regional pseudo-terrains (replaced at runtime by biome)

| ID | Resolves To |
|----|-------------|
| `t_region_groundcover` | Biome-appropriate ground cover |
| `t_region_groundcover_forest` | Forest floor |
| `t_region_soil` | Biome-appropriate soil |
| `t_region_grass` | Biome-appropriate grass |

---

## DOORS & WINDOWS

| ID | Name | Best For |
|----|------|----------|
| `t_door_c` | closed wood door | All medieval buildings |
| `t_door_frame` | empty door frame | Ruined buildings |
| `t_window` | window (glass pane) | Wealthier buildings |
| `t_window_empty` | empty window | Abandoned/poor buildings |
| `t_window_frame` | window frame (glass shattered) | Ruined buildings |
| `t_palisade_gate` | palisade gate | Forts, walls |
| `t_palisade_gate_o` | open palisade gate | Forts, walls |

---

## FENCES & GATES

| ID | Name | Best For |
|----|------|----------|
| `t_splitrail_fence` | split rail fence | Farmsteads, pastures |
| `t_wattle_fence` | woven wattle fence | Village gardens, pens |
| `t_fence` | picket fence | Residential boundaries |
| `t_fence_rope` | rope fence | Temporary enclosures |
| `t_fence_post` | fence post | Fence corners |
| `t_splitrail_fencegate_c` | closed split rail gate | Farmstead entrance |
| `t_splitrail_fencegate_o` | open split rail gate | Farmstead entrance |
| `t_wattle_fence_posts` | narrow fence posts | Wattle fence posts |

---

## ROOFS

| ID | Name | Best For |
|----|------|----------|
| `t_thatch_roof` | thatched roof | Peasant houses, barns |
| `t_log_sod_roof` | sod roof | Log cabins, earth-bermed |
| `t_wood_roof` | wooden roof | Wood buildings |
| `t_shingle_flat_roof` | shingle flat roof | Townhouses |
| `t_tile_flat_roof` | tile flat roof | Churches, wealthy |
| `t_rock_roof` | rock roof | Stone buildings, castles |
| `t_brick_roof` | brick roof | Brick buildings |

---

## FURNITURE: SLEEPING

| ID | Name | Comfort | Best For |
|----|------|---------|----------|
| `f_straw_bed` | straw bed | Low | Peasants, travelers |
| `f_makeshift_bed` | makeshift bed | Low | Squatters, survival |
| `f_bed` | bed (wood frame + mattress) | Medium | Wealthier homes, inns |
| `f_hay` | bale of hay | Very Low | Barns, livestock (also works as bed) |

---

## FURNITURE: TABLES & CHAIRS

| ID | Name | Best For |
|----|------|----------|
| `f_table` | wooden table | All interiors |
| `f_chair` | wooden chair | All interiors |

---

## FURNITURE: HEAT & LIGHT

| ID | Name | Best For |
|----|------|----------|
| `f_fireplace` | stone fireplace | Houses, inns, halls |
| `f_woodstove` | wood stove | Cabins, wealthier homes |
| `f_brazier` | brazier | Churches, large halls |

---

## FURNITURE: STORAGE

| ID | Name | Best For |
|----|------|----------|
| `f_dresser` | dresser (wooden drawers) | Bedrooms |
| `f_wardrobe` | wardrobe (large cabinet) | Bedrooms, storage |
| `f_bookcase` | bookcase (wooden) | Studies, monasteries |
| `f_crate_c` | sealed wooden crate | Trade goods, storage |
| `f_crate_o` | open wooden crate | Storage, goods display |

---

## FURNITURE: CRAFTING

| ID | Name | Best For |
|----|------|----------|
| `f_forge` | forge | Smithy, metalworking |
| `f_anvil` | anvil | Smithy, metalworking |
| `f_anvil_bronze` | bronze anvil | Primitive smithy |

---

## FURNITURE: OUTDOOR / FARM

| ID | Name | Best For |
|----|------|----------|
| `f_hay` | bale of hay | Barns, fields |
| `f_region_flower` | regional flower (pseudo) | Gardens, meadows |

---

## KNOWN GAPS (not in vanilla CDDA, would need custom definitions)

| Missing | Description |
|---------|-------------|
| Stone oven | Medieval baking oven (use `f_fireplace` as placeholder) |
| Wooden barrel | Standalone barrel furniture (use `f_crate_c` as placeholder) |
| Water trough | Livestock trough |
| Well | Water well |
| Cobblestone floor | Outdoor cobblestone (use `t_rock_floor` as placeholder) |
| Altar / shrine | Religious furniture |
