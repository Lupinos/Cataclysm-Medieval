"""Typed references in the CDDA data used by the wilderness baseline."""

from typing import NamedTuple, Optional, Tuple, Union


ITEM_TYPES = frozenset(
    "AMMO ARMOR BATTERY BIONIC_ITEM BOOK COMESTIBLE ENGINE GENERIC GUN GUNMOD "
    "MAGAZINE PET_ARMOR TOOL TOOLMOD TOOL_ARMOR WHEEL".split()
)
RECIPE_TYPES = frozenset(("recipe", "practice", "nested_category"))
NAME_IDS = frozenset(("monstergroup", "MONSTER_FACTION", "EXTERNAL_OPTION"))
FieldPath = Tuple[Union[str, int], ...]


class Link(NamedTuple):
    namespace: str
    id: Optional[str]
    relation: str
    path: FieldPath


def namespace(type_name):
    if type_name in ITEM_TYPES:
        return "item"
    if type_name in RECIPE_TYPES:
        return "recipe"
    if type_name == "city_building":
        return "overmap_special"
    return type_name


def pointer(path):
    """JSON Pointer relative to a file or a declaration."""
    return "".join(
        "/" + str(part).replace("~", "~0").replace("/", "~1") for part in path
    )


def identities(obj):
    """Return the registry, identity field, and declared IDs."""
    type_name = obj["type"]
    registry = namespace(type_name)
    if type_name == "mapgen":
        for field, registry in (
            ("om_terrain", "mapgen"),
            ("nested_mapgen_id", "nested_mapgen"),
            ("update_mapgen_id", "update_mapgen"),
        ):
            if field in obj:
                return registry, field, tuple(string_ids(obj[field]))
        return type_name, "", ()
    if "abstract" in obj:
        return registry, "abstract", tuple(string_ids(obj["abstract"]))
    if type_name in ("recipe", "uncraft") and "result" in obj:
        result = obj["result"]
        if type_name == "recipe":
            for field in ("variant", "id_suffix"):
                if obj.get(field):
                    result += "_" + obj[field]
        return registry, "result", (result,)
    if type_name in NAME_IDS:
        return registry, "name", tuple(string_ids(obj.get("name")))
    field = "id" if "id" in obj else "ident"
    return registry, field, tuple(string_ids(obj.get(field)))


def string_ids(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for entry in value:
            yield from string_ids(entry)


def children(value):
    if isinstance(value, dict):
        return value.items()
    if isinstance(value, list):
        return enumerate(value)
    return ()


def fields(value, pattern, path=()):
    """Match fields using * for a list entry or a dictionary value."""
    if not pattern:
        yield value, path
        return
    key, *rest = pattern
    if key == "*":
        for index, entry in children(value):
            yield from fields(entry, rest, path + (index,))
    elif isinstance(value, dict) and key in value:
        yield from fields(value[key], rest, path + (key,))


def choices(value, path, target, relation):
    if isinstance(value, str):
        yield Link(target, value, relation, path)
    elif isinstance(value, list):
        # Weighted pairs store the ID first, then its numeric weight.
        if len(value) == 2 and isinstance(value[1], (int, float)):
            yield from choices(value[0], path + (0,), target, relation)
        else:
            for index, entry in enumerate(value):
                yield from choices(entry, path + (index,), target, relation)
    elif isinstance(value, dict):
        for member in ("distribution", "fallback", "default"):
            if member in value:
                yield from choices(
                    value[member], path + (member,), target, relation
                )
        for case, entry in children(value.get("cases")):
            yield from choices(entry, path + ("cases", case), target, relation)
        if not set(value).issubset({"distribution", "fallback", "default"}):
            yield Link(target, None, relation, path)


def read_fields(obj, rules, path=()):
    for target, relation, patterns in rules:
        for pattern in patterns.split():
            for value, location in fields(obj, pattern.split("/"), path):
                yield from choices(value, location, target, relation)


def keyed_refs(obj, patterns, target, relation, path=()):
    for pattern in patterns.split():
        for value, location in fields(obj, pattern.split("/"), path):
            if isinstance(value, dict):
                for key in value:
                    if not key.startswith("//"):
                        yield Link(target, key, relation, location + (key,))


def item_group(value, path, default="item_group"):
    if isinstance(value, str):
        yield Link(default, value, "spawns", path)
    elif isinstance(value, list):
        for index, entry in enumerate(value):
            loc = path + (index,)
            if isinstance(entry, list) and entry:
                yield from item_group(entry[0], loc + (0,), default)
            else:
                yield from item_group(entry, loc, default)
    elif isinstance(value, dict):
        yield from read_fields(
            value,
            (
                ("item", "spawns", "item"),
                ("item_group", "spawns", "group"),
                (
                    "item",
                    "contains",
                    "container-item contents-item entry-wrapper ammo-item",
                ),
                (
                    "item_group",
                    "contains",
                    "container-group contents-group ammo-group",
                ),
            ),
            path,
        )
        for key, target in (
            ("items", "item"),
            ("groups", "item_group"),
            ("entries", "item"),
            ("distribution", "item"),
            ("collection", "item"),
            ("extend", default),
        ):
            if key in value:
                yield from item_group(value[key], path + (key,), target)


def requirements(obj, path=()):
    for key, relation, target in (
        ("components", "component", "item"),
        ("tools", "tool", "item"),
        ("qualities", "uses", "tool_quality"),
    ):
        for group_index, group in children(obj.get(key)):
            # Requirements are an AND of groups, each containing alternatives.
            # A single alternative can also be written without nesting.
            loc = path + (key, group_index)
            if isinstance(group, dict) and key == "qualities":
                alternatives = [(group, loc)]
            elif (
                isinstance(group, list) and group and isinstance(group[0], str)
            ):
                alternatives = [(group, loc)]
            else:
                alternatives = [(v, loc + (i,)) for i, v in children(group)]
            for entry, entry_path in alternatives:
                if isinstance(entry, list) and entry:
                    registry = "requirement" if "LIST" in entry[2:] else target
                    yield from choices(
                        entry[0], entry_path + (0,), registry, relation
                    )
                elif key == "qualities" and isinstance(entry, dict):
                    yield from read_fields(
                        entry, (("tool_quality", "uses", "id"),), entry_path
                    )
    using = obj.get("using")
    if isinstance(using, str):
        yield Link("requirement", using, "uses", path + ("using",))
    elif isinstance(using, list):
        for index, entry in enumerate(using):
            if isinstance(entry, list) and entry:
                yield from choices(
                    entry[0], path + ("using", index, 0), "requirement", "uses"
                )


PLACEMENTS = (
    # Palette field, coordinate field, subfield, target registry.
    ("item", "place_item", "item", "item"),
    ("liquids", "place_liquids", "liquid", "item"),
    ("vendingmachines", "place_vendingmachines", "item_group", "item_group"),
    ("npcs", "place_npcs", "class", "npc"),
    ("monsters", "place_monsters", "monster", "monstergroup"),
    ("monster", "place_monster", "monster", "MONSTER"),
    ("monster", "place_monster", "group", "monstergroup"),
    ("vehicles", "place_vehicles", "vehicle", "vehicle_group"),
    ("terrain", "place_terrain", "ter", "terrain"),
    ("furniture", "place_furniture", "furn", "furniture"),
    ("traps", "place_traps", "trap", "trap"),
    ("nested", "place_nested", "chunks", "nested_mapgen"),
    ("nested", "place_nested", "else_chunks", "nested_mapgen"),
)


def placement_pieces(value, path):
    if isinstance(value, list) and value and isinstance(value[0], dict):
        yield from ((v, path + (i,)) for i, v in enumerate(value))
    else:
        yield value, path


def placements(obj, path=()):
    yield from read_fields(
        obj,
        (
            ("palette", "uses", "palettes"),
            ("terrain", "uses", "fill_ter"),
            (
                "overmap_terrain",
                "uses",
                "predecessor_mapgen fallback_predecessor_mapgen",
            ),
            ("item", "spawns", "add/*/item place_loot/*/item"),
            ("item_group", "spawns", "place_loot/*/group"),
        ),
        path,
    )
    for symbol, coordinate, key, target in PLACEMENTS:
        for pattern in (
            f"{symbol}/*",
            f"mapping/*/{symbol}",
            f"{coordinate}/*",
        ):
            for value, loc in fields(obj, pattern.split("/"), path):
                for piece, pos in placement_pieces(value, loc):
                    if isinstance(piece, dict) and key in piece:
                        yield from choices(
                            piece[key], pos + (key,), target, "spawns"
                        )
                    elif coordinate in (
                        "place_terrain",
                        "place_furniture",
                        "place_traps",
                    ):
                        yield from choices(piece, pos, target, "uses")
    for pattern in ("place_items/*", "items/*", "mapping/*/items"):
        for value, loc in fields(obj, pattern.split("/"), path):
            for piece, pos in placement_pieces(value, loc):
                if isinstance(piece, dict) and "item" in piece:
                    yield from item_group(piece["item"], pos + ("item",))


REGION_FIELDS = (
    (
        "overmap_terrain",
        "spawns",
        "default_oter forest_mapgen_settings/*/terrains",
    ),
    ("terrain", "spawns", "default_groundcover"),
    ("item_group", "spawns", "forest_mapgen_settings/*/item_group"),
)


def region_references(obj):
    yield from read_fields(obj, REGION_FIELDS)
    for patterns, registry in (
        (
            "city/houses city/shops city/parks "
            "forest_trail_settings/trailheads",
            "overmap_special",
        ),
        ("map_extras/*/extras", "map_extra"),
        (
            "region_terrain_and_furniture/terrain/* "
            "forest_mapgen_settings/*/groundcover",
            "terrain",
        ),
        ("region_terrain_and_furniture/furniture/*", "furniture"),
    ):
        yield from keyed_refs(obj, patterns, registry, "spawns")


RULES = {
    "item": (
        ("material", "uses", "armor/*/material/*/type"),
        (
            "item",
            "contains",
            "container default_ammo pocket_data/*/item_restriction",
        ),
        (
            "item",
            "transforms",
            "revert_to smoked_result smoking_result seed_data/fruit "
            "seed_data/byproducts milling/into",
        ),
        ("item", "uses", "sub magazine_adaptor/*/*"),
        ("ammunition_type", "uses", "ammo"),
        ("technique", "uses", "techniques"),
        ("vitamin", "uses", "vitamins"),
    ),
    "recipe": (
        ("item", "produces", "result byproducts"),
        ("item", "contains", "container"),
        ("item_group", "produces", "byproduct_group"),
        ("skill", "uses", "skill_used"),
        ("recipe", "uses", "nested_category_data"),
        ("proficiency", "uses", "proficiencies/*/proficiency"),
    ),
    "uncraft": (("item", "uses", "result"),),
    "ammunition_type": (("item", "uses", "default"),),
    "material": (("item", "uses", "repaired_with salvaged_into"),),
    "MONSTER": (
        ("harvest", "produces", "harvest dissect"),
        (
            "MONSTER",
            "transforms",
            "upgrades/into zombify_into burn_into "
            "fungalize_into reproduction/baby_monster",
        ),
        ("monstergroup", "transforms", "upgrades/into_group"),
        ("MONSTER_FACTION", "uses", "default_faction"),
        ("SPECIES", "uses", "species"),
        (
            "item",
            "produces",
            "revert_to_itype reproduction/baby_egg "
            "biosignature/biosig_item mech_battery mech_weapon",
        ),
    ),
    "monstergroup": (
        ("MONSTER", "spawns", "default monsters/*/monster"),
        ("monstergroup", "spawns", "monsters/*/group"),
    ),
    "terrain": (
        (
            "terrain",
            "transforms",
            "open close rotates_to transforms_into roof "
            "bash/ter_set bash/ter_set_bashed_from_above deconstruct/ter_set",
        ),
        ("harvest", "produces", "harvest_by_season/*/id"),
        ("trap", "uses", "trap"),
    ),
    "furniture": (
        (
            "furniture",
            "transforms",
            "open close rotates_to bash/furn_set "
            "deconstruct/furn_set plant_data/transform plant_data/base",
        ),
        ("harvest", "produces", "harvest_by_season/*/id"),
        ("item", "uses", "crafting_pseudo_item deployed_item"),
    ),
    "overmap_special": (
        ("overmap_terrain", "spawns", "overmaps/*/overmap"),
        ("monstergroup", "spawns", "spawns/group"),
        ("overmap_location", "uses", "locations"),
    ),
    "overmap_terrain": (
        ("monstergroup", "spawns", "spawns/group"),
        ("effect_on_condition", "effect", "entry_eoc exit_eoc"),
    ),
    "scenario": (
        ("start_location", "uses", "allowed_locs"),
        ("profession", "uses", "professions"),
        ("achievement", "uses", "requirement"),
        ("mutation", "uses", "forced_traits forbidden_traits"),
        ("monstergroup", "spawns", "surround_groups/*/group"),
        ("mission_definition", "uses", "missions"),
        ("vehicle", "spawns", "vehicle"),
    ),
    "profession": (
        ("MONSTER", "spawns", "pets/*/name"),
        ("vehicle", "spawns", "vehicle"),
        ("recipe", "uses", "recipes"),
        ("mission_definition", "uses", "missions"),
        ("achievement", "uses", "requirement"),
    ),
    "npc": (
        ("npc_class", "uses", "class"),
        ("faction", "uses", "faction"),
        ("talk_topic", "uses", "chat"),
        ("mission_definition", "uses", "mission_offered"),
    ),
    "npc_class": (
        (
            "item_group",
            "spawns",
            "worn_override carry_override weapon_override",
        ),
        ("item_group", "spawns", "shopkeeper_item_group/*/group"),
    ),
    "mission_definition": (("item", "uses", "item"),),
    "construction": (("construction_group", "uses", "group"),),
    "vehicle": (
        ("vehicle_part", "uses", "parts/*/part parts/*/parts/*/part"),
        ("item", "spawns", "items/*/items"),
        ("item_group", "spawns", "items/*/item_groups"),
    ),
    "vehicle_group": (("vehicle", "spawns", "vehicles"),),
    "vehicle_part": (("item", "uses", "item"),),
    "MIGRATION": (("item", "migrates_to", "replace contents/*/id"),),
    "ITEM_BLACKLIST": (("item", "filters", "items"),),
    "SCENARIO_BLACKLIST": (("scenario", "filters", "scenarios"),),
    "MONSTER_BLACKLIST": (("MONSTER", "filters", "monsters"),),
    "MONSTER_WHITELIST": (("MONSTER", "filters", "monsters"),),
}


def effects(value, path=()):
    if isinstance(value, dict):
        for key in (
            "u_spawn_item",
            "npc_spawn_item",
            "u_buy_item",
            "u_sell_item",
            "u_consume_item",
            "npc_consume_item",
        ):
            if key in value:
                target = (
                    "item_group" if value.get("use_item_group") else "item"
                )
                yield from choices(value[key], path + (key,), target, "effect")
                if "container" in value:
                    yield from choices(
                        value["container"],
                        path + ("container",),
                        "item",
                        "contains",
                    )
        yield from read_fields(
            value,
            (
                ("effect_on_condition", "effect", "run_eocs"),
                ("update_mapgen", "effect", "mapgen_update"),
            ),
            path,
        )
    for key, entry in children(value):
        if isinstance(entry, (list, dict)) and not str(key).startswith("//"):
            yield from effects(entry, path + (key,))


def references(obj, registry, harvest_types):
    type_name = obj["type"]
    if "copy-from" in obj:
        yield from choices(
            obj["copy-from"], ("copy-from",), registry, "inherits"
        )
    # Obsolete recipes still load their base, then skip the remaining fields.
    if registry in ("recipe", "uncraft") and obj.get("obsolete") is True:
        return
    if "looks_like" in obj:
        yield from choices(
            obj["looks_like"], ("looks_like",), registry, "appearance"
        )
    yield from read_fields(obj, RULES.get(registry, ()))
    if type_name == "mapgen" and isinstance(obj.get("object"), dict):
        yield from placements(obj["object"], ("object",))
    if type_name == "palette":
        yield from placements(obj)
    if type_name == "item_group":
        yield from item_group(obj, ())
    if type_name in (
        "recipe",
        "uncraft",
        "practice",
        "construction",
        "requirement",
    ):
        yield from requirements(obj)
    if isinstance(obj.get("extend"), dict):
        yield from read_fields(
            obj["extend"], RULES.get(registry, ()), ("extend",)
        )
    for key in ("bash", "deconstruct"):
        if type_name in ("terrain", "furniture") and isinstance(
            obj.get(key), dict
        ):
            yield from item_group(obj[key].get("items"), (key, "items"))
    if type_name == "construction":
        for key in ("pre_terrain", "post_terrain"):
            value = obj.get(key)
            if isinstance(value, str) and value:
                target = "furniture" if value.startswith("f_") else "terrain"
                yield Link(target, value, "uses", (key,))
    if type_name in ("region_settings", "region_overlay"):
        yield from region_references(obj)
    if type_name == "start_location":
        for value, loc in fields(obj, ("terrain", "*")):
            if isinstance(value, dict):
                if value.get("om_terrain_match_type") in (
                    "PREFIX",
                    "CONTAINS",
                ):
                    yield Link("overmap_terrain", None, "uses", loc)
                    continue
                value, loc = value.get("om_terrain"), loc + ("om_terrain",)
            yield from choices(value, loc, "overmap_terrain", "uses")
    if type_name == "map_extra" and isinstance(obj.get("generator"), dict):
        generator = obj["generator"]
        method = generator.get("generator_method")
        if method in ("mapgen", "update_mapgen"):
            yield from choices(
                generator.get("generator_id"),
                ("generator", "generator_id"),
                method,
                "spawns",
            )
    if type_name == "vehicle":
        for value, loc in fields(obj, ("parts", "*", "parts", "*")):
            if isinstance(value, str):
                yield Link("vehicle_part", value, "uses", loc)
            elif isinstance(value, dict):
                yield from read_fields(
                    value,
                    (("item", "contains", "ammo_types fuel tools"),),
                    loc,
                )
    if registry in ("item", "MONSTER"):
        for value, path in fields(obj, ("material",)):
            if isinstance(value, dict):
                for key in value:
                    yield Link("material", key, "uses", path + (key,))
            else:
                yield from choices(value, path, "material", "uses")
    if type_name == "MONSTER":
        yield from item_group(obj.get("death_drops"), ("death_drops",))
        if isinstance(obj.get("starting_ammo"), dict):
            for key in obj["starting_ammo"]:
                yield Link("item", key, "contains", ("starting_ammo", key))
    if type_name == "harvest":
        for entry, loc in fields(obj, ("entries", "*")):
            if not isinstance(entry, dict):
                continue
            drop_type = entry.get("type")
            target = "item_group" if harvest_types.get(drop_type) else "item"
            yield from choices(
                entry.get("drop"), loc + ("drop",), target, "produces"
            )
            yield from choices(
                drop_type, loc + ("type",), "harvest_drop_type", "uses"
            )
    if type_name == "profession":
        for value, loc in fields(obj, ("items", "*")):
            yield from item_group(value, loc, "item")
    if type_name == "npc_class" and isinstance(
        obj.get("shopkeeper_item_group"), str
    ):
        yield Link(
            "item_group",
            obj["shopkeeper_item_group"],
            "spawns",
            ("shopkeeper_item_group",),
        )
    if registry == "recipe" and "book_learn" in obj:
        books = obj["book_learn"]
        if isinstance(books, dict):
            for key in books:
                yield Link("item", key, "uses", ("book_learn", key))
        else:
            yield from choices(books, ("book_learn",), "item", "uses")
    actions = obj.get("use_action")
    for index, action in enumerate(
        actions if isinstance(actions, list) else [actions]
    ):
        if isinstance(action, dict) and action.get("type") in (
            "transform",
            "delayed_transform",
            "auto_transform",
        ):
            loc = (
                ("use_action", index)
                if isinstance(actions, list)
                else ("use_action",)
            )
            yield from read_fields(
                action,
                (
                    ("item", "transforms", "target container"),
                    ("item_group", "spawns", "target_group"),
                ),
                loc,
            )
    if type_name in (
        "effect_on_condition",
        "talk_topic",
        "mission_definition",
    ):
        yield from effects(obj)
    for key in ("use_action", "result_eocs", "eoc", "examine_action"):
        if key in obj:
            yield from effects(obj[key], (key,))
