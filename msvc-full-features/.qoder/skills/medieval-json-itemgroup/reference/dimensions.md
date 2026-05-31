# item_group 9-Dimension Classification

Reference for dimension classification. See [json_itemgroup_organization.md](../../docs/vanilla/json_itemgroup_organization.md) for full vanilla analysis.

---

## Dimension 1: Room/Furniture

**File**: `domestic.json`

**Consumer**: mapgen `place_items` calls.

**Naming**: `{room_name}` or `{furniture_name}` — lowercase, plain words.

```json
"id": "kitchen"       // Everything found in a kitchen
"id": "bedroom"       // Everything found in a bedroom
"id": "nightstand"    // Contents of a nightstand
"id": "garden_shed"   // Contents of a garden shed
```

**Design rule**: Room groups use `subtype: distribution` (pick random items from the pool). Furniture-specific groups can use `subtype: collection` for realism (this shelf ALWAYS has these things).

**Subtype**: `distribution` (room) or `collection` (furniture, SUS-style).

**Medieval examples**: `kitchen_medieval`, `blacksmith_forge`, `tavern_counter`, `farmhouse_bedroom`, `mill_grainroom`.

---

## Dimension 2: Clothing Set

**File**: `clothing.json` (may split into `clothing_civilian.json`, `clothing_military.json`)

**Consumer**: mapgen (placing clothes in wardrobes), NPC generation, monster drops.

**Naming**: `{slot}_{class}` or `clothing_{occupation}`.

```json
"id": "tunic_peasant"       // Peasant tunics only
"id": "pants_merchant"      // Merchant-level pants
"id": "clothing_knight"     // Knight's full wardrobe set
"id": "winter"              // Winter clothing across slots
```

**Design rule**: Group by slot first (pants, tunic, shoes, hat), then by social class/occupation. Use `distribution` for picking one item; use nested `group` references for full outfits.

**Subtype**: `distribution`.

---

## Dimension 3: Weapons/Ammo

**File**: `weapons.json`

**Consumer**: mapgen (armory/market), NPC equipment, profession starting gear.

**Naming**: `weapons_{class}` or `{weapon_type}_{variant}`.

```json
"id": "weapons_swords"      // All swords
"id": "weapons_common"      // Common weapons any household might have
"id": "arrows"              // Arrow types
"id": "bows"                // Bow types
```

**Design rule**: 2-3 level pyramid. Top level aggregates (weapons), mid level by type (swords, axes, bows), bottom level by quality/rarity (fine_swords, peasant_weapons). Use nested `group` references.

**Subtype**: `distribution`.

---

## Dimension 4: Food/Drink

**File**: `food.json`

**Consumer**: kitchen/fridge/tavern room groups (nested reference).

**Naming**: `{food_category}`.

```json
"id": "snacks"        // Snack items
"id": "pantry"        // Pantry staples
"id": "condiments"    // Herbs, spices, sauces
"id": "ale_and_mead"  // Medieval drinks
```

**Design rule**: Category-level groups, designed to be referenced by room groups. Don't create ultra-specific food groups unless the room type demands it.

**Subtype**: `distribution`.

---

## Dimension 5: Location/Building

**File**: `locations.json`

**Consumer**: mapgen for unique/special buildings.

**Naming**: `{location_name}`.

```json
"id": "mansion"           // Mansion-specific loot
"id": "prison"            // Prison-specific items
"id": "monastery"         // Monastery-specific items
```

**Design rule**: Use when a building type needs a unique loot table different from generic room groups. Most buildings should use Dimension 1 room groups instead—only create location groups for significantly different loot profiles.

**Subtype**: `distribution`.

---

## Dimension 6: Monster/NPC Drops

**File**: `monster_drops.json`

**Consumer**: monster definitions `death_drops` field, NPC equipment pools.

**Naming**: `{creature}_parts` or `{creature}_drop`.

```json
"id": "human_parts"       // What a human corpse yields
"id": "bandit_gear"       // Bandit NPC equipment pool
"id": "wolf_parts"        // Wolf corpse yields
"id": "bear_lair"         // Bear lair environmental loot
```

**Design rule**: Two-layer model — `{creature}_parts` for corpse drops (collection, all parts), `{creature}_gear` for equipment pool (distribution, random gear).

**Subtype**: `collection` (parts) or `distribution` (gear).

---

## Dimension 7: NPC/Profession Starting Gear

**File**: `professions.json` (or `npc_gear.json`)

**Consumer**: Profession definitions, NPC class definitions.

**Naming**: `starting_gear_{profession}` or `npc_gear_{role}`.

```json
"id": "starting_gear_blacksmith"     // Blacksmith profession starting items
"id": "npc_gear_town_guard"          // Town guard NPC equipment
```

**Design rule**: `subtype: collection` to give the full starting set. Use nested group references to clothing/weapons groups.

**Subtype**: `collection`.

---

## Dimension 8: Container Pre-assembly

**File**: `domestic.json` (bottom section) or `misc.json`.

**Consumer**: Referenced by any other group that needs items in containers.

**Naming**: `{item_id}_{container_id}_{count}`.

```json
"id": "bread_bag_cloth_4"       // 4 bread in cloth bag
"id": "arrows_quiver_10"        // 10 arrows in quiver
```

**Design rule**: Always `subtype: collection` with `container-item`. Use `"container-item": "null"` on entry items so they spawn loose.

**Subtype**: `collection`.

---

## Dimension 9: Shops/Trade

**File**: `shops.json`

**Consumer**: NPC merchant inventory definitions, shop mapgen.

**Naming**: `{shop_type}_shop` or `market_{type}`.

```json
"id": "blacksmith_shop"      // Blacksmith shop inventory
"id": "market_food"          // Food market stall
"id": "tavern_supplies"      // Tavern supply room
```

**Design rule**: `subtype: distribution`. Larger prob pools than room groups (shops have more stock variety).

**Subtype**: `distribution`.
