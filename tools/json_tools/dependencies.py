#!/usr/bin/env python3
"""Count, query, and remove CDDA JSON declarations."""

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from itertools import islice
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import NamedTuple, Optional

from dependency_rules import (
    Link,
    fields,
    identities,
    namespace,
    placements,
    pointer,
    references,
    string_ids,
)


REPO = Path(__file__).resolve().parents[2]
DEFAULT_ROOTS = [REPO / "data/core", REPO / "data/json"]
DECODER = json.JSONDecoder()
SPACE = re.compile(r"[ \t\r\n]*")
STATIC_SCOPE = (
    "References come from supported fields and typed C++ literals. "
    "Other fields and runtime-generated references require review. "
    "Declarations follow the selected roots and file loading order."
)

CPP_TYPES = {
    "item": "item",
    "itype_id": "item",
    "item_group_id": "item_group",
    "mtype_id": "MONSTER",
    "mongroup_id": "monstergroup",
    "material_id": "material",
    "ter_str_id": "terrain",
    "furn_str_id": "furniture",
    "recipe_id": "recipe",
    "requirement_id": "requirement",
    "oter_str_id": "overmap_terrain",
    "overmap_special_id": "overmap_special",
    "nested_mapgen_id": "nested_mapgen",
    "update_mapgen_id": "update_mapgen",
    "palette_id": "palette",
    "vproto_id": "vehicle",
    "vgroup_id": "vehicle_group",
    "vpart_id": "vehicle_part",
    "efftype_id": "effect_type",
    "effect_on_condition_id": "effect_on_condition",
    "skill_id": "skill",
    "trait_id": "mutation",
    "trap_str_id": "trap",
    "harvest_id": "harvest",
    "profession_id": "profession",
    "scenario_id": "scenario",
    "mission_type_id": "mission_definition",
    "npc_template_id": "npc",
    "npc_class_id": "npc_class",
    "map_extra_id": "map_extra",
}
# Skip comments and ordinary strings before looking for a typed literal.
CPP_TOKEN = re.compile(
    r"//[^\n]*|/\*.*?\*/"
    r"|\b(?P<type>" + "|".join(CPP_TYPES) + r")\s*"
    r'(?:[A-Za-z_]\w*\s*)?[({]\s*(?P<literal>"(?:\\.|[^"\\\r\n])*")'
    r'|"(?:\\.|[^"\\])*"',
    re.DOTALL,
)

ROTATED_TERRAIN = ("_north", "_east", "_south", "_west")
LINEAR_TERRAIN = (
    "_isolated",
    "_end_south",
    "_end_west",
    "_ne",
    "_end_north",
    "_ns",
    "_es",
    "_nes",
    "_end_east",
    "_wn",
    "_ew",
    "_new",
    "_sw",
    "_nsw",
    "_esw",
    "_nesw",
)
LINEAR_MAPGEN = ("_straight", "_curved", "_end", "_tee", "_four_way")


class ToolError(Exception):
    pass


class Symbol(NamedTuple):
    namespace: str
    id: str

    def __str__(self):
        return f"{self.namespace}:{self.id}"


def display(path):
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def source_files(roots, extensions):
    seen = set()
    for root in roots:
        root = root.absolute()
        if root.is_dir():
            files = sorted(
                (
                    p
                    for p in root.rglob("*")
                    if p.suffix in extensions and p.is_file()
                ),
                key=lambda p: (len(p.parts), p.as_posix()),
            )
        elif root.is_file() and root.suffix in extensions:
            files = [root]
        else:
            raise ToolError(f"Invalid source path: {display(root)}")
        for path in files:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield path


def skip_space(text, pos):
    return SPACE.match(text, pos).end()


def array_entries(text, start):
    """Read the contents and offsets of a JSON array."""
    pos = skip_space(text, start + 1)
    entries = []
    if not text.startswith("]", pos):
        while True:
            value, end = DECODER.raw_decode(text, pos)
            entries.append((pos, end, value))
            pos = skip_space(text, end)
            if not text.startswith(",", pos):
                break
            pos = skip_space(text, pos + 1)
    if not text.startswith("]", pos):
        raise json.JSONDecodeError("Expected ',' or ']'", text, pos)
    return entries, pos + 1


@dataclass
class Declaration:
    file: Path
    index: Optional[int]
    start: int
    end: int
    line: int
    data: dict
    order: int
    type: str
    identity_field: str
    registry: str
    symbols: tuple
    aliases: tuple

    @property
    def location(self):
        suffix = f"/{self.index}" if self.index is not None else ""
        return f"@{display(self.file)}#{suffix}"

    @property
    def label(self):
        return ", ".join(map(str, self.symbols)) or self.type

    @property
    def abstract(self):
        return self.identity_field == "abstract"

    def describe(self):
        return {
            "type": self.type,
            "ids": list(map(str, self.symbols)),
            "aliases": list(map(str, self.aliases)),
            "abstract": self.abstract,
            "location": self.location,
            "line": self.line,
            "order": self.order,
        }


@dataclass
class JsonFile:
    path: Path
    text: str
    records: list = field(default_factory=list)
    array: Optional[tuple] = None


def load_file(path, order):
    text = path.read_bytes().decode("utf-8")
    start = skip_space(text, int(text.startswith("\ufeff")))
    document = JsonFile(path, text)
    if text.startswith("[", start):
        entries, end = array_entries(text, start)
        document.array = (start, end)
    else:
        value, end = DECODER.raw_decode(text, start)
        entries = [(start, end, value)]
    if skip_space(text, end) != len(text):
        raise json.JSONDecodeError("Extra data", text, end)
    newlines = [m.start() for m in re.finditer("\n", text)]
    for i, (start, end, obj) in enumerate(entries):
        line = bisect_right(newlines, start) + 1
        if not isinstance(obj, dict) or not isinstance(obj.get("type"), str):
            raise ToolError(
                f"{display(path)}:{line}: expected a typed JSON object"
            )
        registry, member, ids = identities(obj)
        alias = obj.get("alias", [])
        if isinstance(alias, str):
            alias = [alias]
        aliases = (
            tuple(
                Symbol(registry, name)
                for name in alias
                if isinstance(name, str)
            )
            if isinstance(alias, list) and ids
            else ()
        )
        document.records.append(
            Declaration(
                path,
                i if document.array is not None else None,
                start,
                end,
                line,
                obj,
                order + i,
                obj["type"],
                member,
                registry,
                tuple(dict.fromkeys(Symbol(registry, name) for name in ids)),
                aliases,
            )
        )
    return document


class Edge(NamedTuple):
    source: int
    link: Link

    @property
    def target(self):
        if self.link.id is not None:
            return Symbol(self.link.namespace, self.link.id)
        return None


class Index:
    def __init__(self, roots):
        self.files = {}
        self.records = []
        self.symbols = defaultdict(list)
        self.names = defaultdict(set)
        self.locations = {}
        for path in source_files(roots, {".json"}):
            try:
                doc = load_file(path, len(self.records))
            except (ValueError, TypeError) as exc:
                raise ToolError(f"{display(path)}: {exc}") from exc
            self.files[path] = doc
            self.records.extend(doc.records)
            for record in doc.records:
                self.locations[record.location] = record.order
                for key in dict.fromkeys(record.symbols + record.aliases):
                    self.symbols[key].append(record.order)
                    self.names[key.id].add(key)
        if not self.files:
            raise ToolError("No JSON files found in the selected roots")
        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)
        self.terrain_variants = {}
        self.mapgen_suffixes = {}

    def build_graph(self):
        harvest_types = {
            key.id: self.records[orders[-1]].data.get("group", False)
            for key, orders in self.symbols.items()
            if key.namespace == "harvest_drop_type"
        }
        self.index_terrain_variants()
        for record in self.records:
            links = list(
                references(record.data, record.registry, harvest_types)
            )
            links.extend(self.implicit_references(record))
            for link in dict.fromkeys(links):
                edge = Edge(record.order, self.normalize_link(link))
                self.outgoing[record.order].append(edge)
                if edge.target is not None:
                    self.incoming[edge.target].append(edge)

    def index_terrain_variants(self):
        flags_at = {}
        for record in self.records:
            if record.registry != "overmap_terrain":
                continue
            obj = record.data
            inherited = flags_at.get(obj.get("copy-from"), set())
            flags = (
                set(string_ids(obj.get("flags")))
                if "flags" in obj
                else inherited
            )
            edits = (
                set(string_ids(obj.get(key, {}).get("flags")))
                for key in ("extend", "delete")
            )
            added, removed = edits
            flags = (flags | added) - removed
            for symbol in record.symbols:
                flags_at[symbol.id] = flags
                if record.abstract:
                    continue
                if "LINEAR" in flags:
                    variants, mapgens = LINEAR_TERRAIN, LINEAR_MAPGEN
                else:
                    variants = () if "NO_ROTATE" in flags else ROTATED_TERRAIN
                    mapgens = ("",)
                self.mapgen_suffixes[record.order] = mapgens
                for suffix in variants:
                    self.terrain_variants[symbol.id + suffix] = symbol.id

    def implicit_references(self, record):
        if record.registry == "overmap_terrain":
            for suffix in self.mapgen_suffixes.get(record.order, ()):
                for symbol in record.symbols:
                    target = Symbol("mapgen", symbol.id + suffix)
                    if target in self.symbols:
                        yield Link(
                            *target, "generates", (record.identity_field,)
                        )
                for value, loc in fields(
                    record.data, ("mapgen" + suffix, "*", "object")
                ):
                    yield from placements(value, loc)
        elif record.registry == "vehicle_group":
            # A vehicle prototype is added to the group with the same ID.
            for symbol in record.symbols:
                key = Symbol("vehicle", symbol.id)
                if key in self.symbols:
                    yield Link(*key, "spawns", ("id",))

    def reference_key(self, key):
        if key.namespace == "vehicle_part":
            return Symbol(key.namespace, key.id.rsplit("#", 1)[0])
        if key in self.symbols:
            return key
        if key.namespace == "overmap_terrain":
            variant_base = self.terrain_variants.get(key.id)
            if variant_base is not None:
                return Symbol(key.namespace, variant_base)
        if key.namespace == "vehicle_group":
            vehicle = Symbol("vehicle", key.id)
            if vehicle in self.symbols:
                return vehicle
        return key

    def normalize_link(self, link):
        if link.id is None:
            return link
        key = self.reference_key(Symbol(link.namespace, link.id))
        return Link(*key, link.relation, link.path)

    def select(self, selector):
        if selector.startswith("@"):
            location = selector
            if location not in self.locations:
                name, sep, index = location[1:].rpartition("#")
                if sep:
                    location = f"@{display(Path(name).absolute())}#{index}"
            if location in self.locations:
                return None, [self.locations[location]]
        elif ":" in selector:
            typ, name = selector.split(":", 1)
            key = Symbol(namespace(typ), name)
            orders = self.symbols.get(key, ())
            if typ != key.namespace:
                orders = [i for i in orders if self.records[i].type == typ]
            if orders:
                return key, orders
        else:
            keys = self.names.get(selector, ())
            if len(keys) == 1:
                key = next(iter(keys))
                return key, self.symbols[key]
            if keys:
                candidates = ", ".join(sorted(map(str, keys)))
                raise ToolError(f"ID {selector!r} is ambiguous: {candidates}")
        raise ToolError(f"No declaration matches {selector!r}")

    def resolve(self, edge):
        candidates = self.symbols.get(edge.target, ())
        if edge.link.relation != "inherits":
            return [i for i in candidates if not self.records[i].abstract]
        earlier = [i for i in candidates if i < edge.source]
        if earlier and edge.link.namespace == "item_group":
            return earlier
        if earlier:
            # Item_factory and generic_factory look up concrete bases before
            # abstract ones. Finalization can also resolve a base loaded later.
            concrete = [i for i in earlier if not self.records[i].abstract]
            return [(concrete or earlier)[-1]]
        return [i for i in candidates if i != edge.source]

    def describe_edge(self, edge):
        source = self.records[edge.source]
        return {
            "from": source.label,
            "source": source.location,
            "target": str(edge.target) if edge.target is not None else None,
            "namespace": edge.link.namespace,
            "field": pointer(edge.link.path),
            "relation": edge.link.relation,
            "targets": [self.records[i].location for i in self.resolve(edge)],
        }

    def selected_keys(self, key, orders):
        keys = set()
        for i in orders:
            record = self.records[i]
            if key is None:
                keys.update(record.symbols)
            else:
                keys.add(key)
            sole_id = len(record.symbols) == 1 and key in record.symbols
            if key is None or sole_id:
                keys.update(record.aliases)
        return keys

    def walk(self, key, orders, depth, reverse=False):
        active = deque(
            (i, (str(key) if key is not None else self.records[i].label,))
            for i in orders
        )
        visited = set(orders)
        emitted = set()
        root_keys = self.selected_keys(key, orders)
        while active:
            index, path = active.popleft()
            record = self.records[index]
            if reverse:
                keys = (
                    root_keys
                    if len(path) == 1
                    else record.symbols + record.aliases
                )
                edges = (
                    edge
                    for symbol in sorted(set(keys))
                    for edge in self.incoming.get(symbol, ())
                    if index in self.resolve(edge)
                )
            else:
                edges = self.outgoing.get(index, ())
            for edge in edges:
                next_nodes = [edge.source] if reverse else self.resolve(edge)
                if edge not in emitted:
                    emitted.add(edge)
                    step = (
                        self.records[edge.source].label
                        if reverse
                        else str(edge.target)
                        if edge.target is not None
                        else f"<dynamic {edge.link.namespace}>"
                    )
                    yield dict(self.describe_edge(edge), path=path + (step,))
                if len(path) < depth:
                    for i in next_nodes:
                        if i not in visited:
                            visited.add(i)
                            active.append((i, path + (self.records[i].label,)))


def code_references(index, roots, keys):
    if not keys:
        return []
    name_set = {key.id for key in keys}
    terrains = {key.id for key in keys if key.namespace == "overmap_terrain"}
    name_set.update(
        k for k, v in index.terrain_variants.items() if v in terrains
    )
    quoted_names = [json.dumps(name, ensure_ascii=False) for name in name_set]
    found = []
    files = source_files(roots, {".cpp", ".cc", ".cxx", ".h", ".hpp"})
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(quoted_names) <= 32 and not any(
            name in text for name in quoted_names
        ):
            continue
        for token in CPP_TOKEN.finditer(text):
            if token["type"] is None:
                continue
            try:
                name = json.loads(token["literal"])
            except ValueError:
                continue
            key = index.reference_key(Symbol(CPP_TYPES[token["type"]], name))
            if key in keys:
                found.append(
                    {
                        "target": str(key),
                        "file": display(path),
                        "line": text.count("\n", 0, token.start()) + 1,
                    }
                )
    return found


def filter_records(index, types):
    if not types:
        return index.records
    return [r for r in index.records if r.type in types or r.registry in types]


def counts(index, records):
    return {
        "files": len(index.files),
        "matched_files": len({r.file for r in records}),
        "declarations": len(records),
        "unique_ids": len({key for r in records for key in r.symbols}),
        "anonymous": sum(not r.symbols for r in records),
        "abstracts": sum(r.abstract for r in records),
        "by_type": dict(sorted(Counter(r.type for r in records).items())),
    }


def target_removals(index, selectors):
    removals = {}
    for selector in selectors:
        key, orders = index.select(selector)
        if len(orders) != 1:
            locations = ", ".join(index.records[i].location for i in orders)
            raise ToolError(
                f"Multiple declarations for {selector!r}: {locations}"
            )
        i = orders[0]
        record = index.records[i]
        if key is not None and key not in record.symbols:
            raise ToolError(
                f"{selector!r} is an alias. Select {record.label}."
            )
        keys = record.symbols if key is None else [key]
        removals.setdefault(i, set()).update(keys)
    for i, keys in removals.items():
        record = index.records[i]
        if keys == set(record.symbols):
            removals[i] = None
        elif record.identity_field != "id" or not isinstance(
            record.data["id"], list
        ):
            raise ToolError(
                f"{record.location} declares {record.label}. Select every ID "
                "or the declaration location to delete it as a unit."
            )
        elif record.aliases or not all(
            isinstance(v, str) for v in record.data["id"]
        ):
            raise ToolError(
                f"Cannot split compound IDs in {record.location}. "
                "Select the entire declaration by location."
            )
    return removals


def deletion_impact(index, removals):
    target_orders = defaultdict(set)
    for i, keys in removals.items():
        record = index.records[i]
        for key in record.symbols + record.aliases if keys is None else keys:
            target_orders[key].add(i)
    impact = []
    still_defined = []
    for key in sorted(target_orders):
        removed = target_orders[key]
        remaining = sorted(set(index.symbols[key]) - removed)
        if remaining:
            still_defined.append(
                {
                    "id": str(key),
                    "locations": [
                        index.records[i].location for i in remaining
                    ],
                }
            )
        for edge in index.incoming.get(key, ()):
            if edge.source in removals and removals[edge.source] is None:
                continue
            providers = set(index.resolve(edge))
            if providers & removed and (
                edge.link.relation == "inherits" or not providers - removed
            ):
                impact.append(index.describe_edge(edge))
    return impact, set(target_orders), still_defined


def deletion_spans(entries, deleted, bounds):
    """Drop contiguous runs together with the appropriate array separator."""
    if len(deleted) == len(entries):
        start, end = bounds
        return [(start + 1, end - 1)]
    spans = []
    i = 0
    while i < len(entries):
        if i not in deleted:
            i += 1
            continue
        first = i
        while i in deleted:
            i += 1
        if i < len(entries):
            spans.append((entries[first][0], entries[i][0]))
        else:
            spans.append((entries[first - 1][1], entries[i - 1][1]))
    return spans


def member_start(text, record, desired):
    pos = skip_space(text, record.start + 1)
    found = None
    while text[pos] != "}":
        key, end = DECODER.raw_decode(text, pos)
        value_start = skip_space(text, skip_space(text, end) + 1)
        _, end = DECODER.raw_decode(text, value_start)
        if key == desired:
            if found is not None:
                raise ToolError(
                    f"Repeated {desired!r} member at {record.location}"
                )
            found = value_start
        pos = skip_space(text, end)
        if text[pos] != ",":
            break
        pos = skip_space(text, pos + 1)
    return found


class Change(NamedTuple):
    path: Path
    before: bytes
    after: bytes


def deletion_changes(index, removals):
    by_file = defaultdict(dict)
    for i, keys in removals.items():
        record = index.records[i]
        by_file[record.file][record.index] = keys
    changes = []
    for path, edits in by_file.items():
        doc = index.files[path]
        if path.is_symlink():
            raise ToolError(
                f"Select the real file instead of a symlink: {display(path)}"
            )
        deleted = {i for i, keys in edits.items() if keys is None}
        spans = []
        if deleted:
            if doc.array is None:
                entry = doc.records[0]
                spans.append((entry.start, entry.end, "[]"))
            else:
                entries = [(r.start, r.end) for r in doc.records]
                spans.extend(
                    (a, b, "")
                    for a, b in deletion_spans(
                        entries,
                        deleted,
                        doc.array,
                    )
                )
        for i, keys in edits.items():
            if keys is None:
                continue
            record = doc.records[i if i is not None else 0]
            start = member_start(doc.text, record, "id")
            entries, end = array_entries(doc.text, start)
            selected = {k.id for k in keys}
            ids = {
                j for j, (_, _, name) in enumerate(entries) if name in selected
            }
            spans.extend(
                (a, b, "")
                for a, b in deletion_spans(
                    entries,
                    ids,
                    (start, end),
                )
            )
        updated = doc.text
        for start, end, replacement in sorted(spans, reverse=True):
            updated = updated[:start] + replacement + updated[end:]
        before = doc.text.encode("utf-8")
        after = updated.encode("utf-8")
        json.loads(after)
        changes.append(Change(path, before, after))
    return changes


def stage(path, content):
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=".dependencies-", delete=False
    ) as output:
        staged = Path(output.name)
        try:
            output.write(content)
            output.close()
            staged.chmod(stat.S_IMODE(path.stat().st_mode))
        except BaseException:
            output.close()
            staged.unlink(missing_ok=True)
            raise
    return staged


def apply_changes(changes):
    staged = []
    written = []
    recover = []
    temporary = []
    try:
        for change in changes:
            if change.path.read_bytes() != change.before:
                raise ToolError(
                    f"File changed during scan: {display(change.path)}"
                )
            pending = stage(change.path, change.after)
            temporary.append(pending)
            backup = stage(change.path, change.before)
            temporary.append(backup)
            staged.append((change, pending, backup))
        for change, pending, backup in staged:
            if change.path.read_bytes() != change.before:
                raise ToolError(
                    f"File changed before writing: {display(change.path)}"
                )
            os.replace(pending, change.path)
            written.append((change, backup))
    except (OSError, ToolError, KeyboardInterrupt) as exc:
        for change, backup in reversed(written):
            try:
                if change.path.read_bytes() != change.after:
                    raise ToolError("File changed while applying the batch")
                os.replace(backup, change.path)
            except (OSError, ToolError):
                recover.append(backup)
        if recover:
            paths = ", ".join(display(path) for path in recover)
            raise ToolError(f"{exc}. Original files saved at {paths}") from exc
        raise
    finally:
        for path in temporary:
            if path not in recover:
                path.unlink(missing_ok=True)


def limit_rows(rows, limit):
    if not limit:
        return list(rows), False
    preview = list(islice(rows, limit + 1))
    return preview[:limit], len(preview) > limit


def query(index, args, code_roots):
    key, orders = index.select(args.selector)
    result = {
        "definitions": [index.records[i].describe() for i in orders],
        "uses": [],
        "used_by": [],
        "truncated": [],
        "code": code_references(
            index, code_roots, index.selected_keys(key, orders)
        ),
        "direction": args.direction,
    }
    for label, reverse in (("uses", False), ("used_by", True)):
        if args.direction in ("both", label):
            rows = index.walk(key, orders, args.depth, reverse=reverse)
            result[label], truncated = limit_rows(rows, args.limit)
            if truncated:
                result["truncated"].append(label)
    return result


def delete(index, args, code_roots):
    removals = target_removals(index, args.selectors)
    impact, keys, still_defined = deletion_impact(index, removals)
    code = code_references(index, code_roots, keys)
    changes = deletion_changes(index, removals)
    blocked = any(ref["relation"] != "appearance" for ref in impact) or bool(
        code
    )
    applied = args.apply and (args.allow_dangling or not blocked)
    if applied:
        apply_changes(changes)
    return {
        "applied": applied,
        "blocked": blocked,
        "declarations_removed": sum(
            part is None for part in removals.values()
        ),
        "ids_selected": len(keys),
        "selections": [
            dict(
                index.records[i].describe(),
                remove_ids=sorted(map(str, part))
                if part is not None
                else None,
            )
            for i, part in removals.items()
        ],
        "files": [display(change.path) for change in changes],
        "references": impact,
        "code": code,
        "still_defined": still_defined,
    }


def print_reference(ref):
    target = ref["target"] or f"<dynamic {ref['namespace']}>"
    if not ref["targets"] and ref["target"]:
        target += " [definition outside index or missing]"
    text = f"{ref['from']} -> {target} [{ref['relation']}]"
    print(f"  {text} at {ref['source']} {ref['field']}")
    if len(ref.get("path", ())) > 2:
        print(f"    Path: {' -> '.join(ref['path'])}")
    for location in ref["targets"]:
        print(f"    Target: {location}")


def print_declaration(row):
    label = ", ".join(row["ids"]) or "(no ID)"
    extra = " (abstract)" if row["abstract"] else ""
    print(
        f"  {label} [{row['type']}]{extra} "
        f"{row['location']} (line {row['line']})"
    )
    if row["aliases"]:
        print(f"    Aliases: {', '.join(row['aliases'])}")


def print_result(command, result):
    if command == "stats":
        print(
            f"Files scanned: {result['files']}. "
            f"Matched: {result['matched_files']}."
        )
        print(
            f"Declarations: {result['declarations']}. "
            f"Unique IDs: {result['unique_ids']}."
        )
        print(
            f"Abstracts: {result['abstracts']}. "
            f"Anonymous: {result['anonymous']}."
        )
        for typ, count in result["by_type"].items():
            print(f"{count:>6}  {typ}")
        return
    if command == "list":
        for row in result["definitions"]:
            print_declaration(row)
        print(f"{result['count']} matching declarations.")
        if result["truncated"]:
            print("Use --limit 0 for all results.")
        return
    if command == "query":
        print("Declarations in scan order")
        for row in result["definitions"]:
            print_declaration(row)
        for name, label in (("uses", "Depends on"), ("used_by", "Used by")):
            if result["direction"] not in ("both", name):
                continue
            print(f"{label}:")
            for ref in result[name]:
                print_reference(ref)
            if not result[name]:
                print("  None found in the index.")
            if name in result["truncated"]:
                print("  Use --limit 0 for all results.")
    else:
        label = "Applied" if result["applied"] else "Preview"
        print(
            f"{label}: {result['declarations_removed']} whole declarations, "
            f"{result['ids_selected']} IDs, {len(result['files'])} files."
        )
        for row in result["selections"]:
            print_declaration(row)
            if row["remove_ids"] is not None:
                print(f"    Remove IDs: {', '.join(row['remove_ids'])}")
        for entry in result["still_defined"]:
            locations = ", ".join(entry["locations"])
            print(f"{entry['id']} remains defined at {locations}")
        for ref in result["references"]:
            print_reference(ref)
        if result["blocked"] and not result["applied"]:
            print(
                "References remain. Review them before applying the batch."
            )
        elif not result["applied"]:
            print("Run again with --apply to write the changes.")
    for ref in result["code"]:
        print(f"  C++ literal {ref['target']} at {ref['file']}:{ref['line']}")
    print(STATIC_SCOPE)


def nonnegative(text):
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return value


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--root",
        action="append",
        type=Path,
        help="JSON file or directory. Repeat in load order. "
        "Defaults to the repository's data/core and data/json.",
    )
    shared.add_argument("--json", action="store_true", help="Output JSON.")
    commands = parser.add_subparsers(dest="command", required=True)
    stats = commands.add_parser(
        "stats",
        parents=[shared],
        help="Count JSON declarations and unique IDs.",
    )
    inventory = commands.add_parser(
        "list", parents=[shared], help="List IDs and declaration locations."
    )
    for command in (stats, inventory):
        command.add_argument(
            "--type",
            action="append",
            help="Filter by JSON type or registry, e.g. item.",
        )
    inventory.add_argument(
        "--limit",
        type=nonnegative,
        default=50,
        help="Limit displayed definitions (0 for all).",
    )
    query_parser = commands.add_parser(
        "query", parents=[shared], help="Show dependencies and uses."
    )
    delete_parser = commands.add_parser(
        "delete", parents=[shared], help="Preview or apply a deletion batch."
    )
    for command in (query_parser, delete_parser):
        command.add_argument(
            "--code-root",
            action="append",
            type=Path,
            help="Scan C++ literals in this file or directory. "
            "Repository src is scanned with the default roots.",
        )
    selector = (
        "ID, registry:ID, or @path.json#/index (@path.json# for an object)"
    )
    query_parser.add_argument("selector", help=selector)
    query_parser.add_argument(
        "--depth",
        type=nonnegative,
        default=1,
        help="Number of edges to follow (default: 1).",
    )
    query_parser.add_argument(
        "--direction", choices=("both", "uses", "used_by"), default="both"
    )
    query_parser.add_argument(
        "--limit",
        type=nonnegative,
        default=50,
        help="Limit each direction's results (0 for all).",
    )
    delete_parser.add_argument(
        "selectors", metavar="selector", nargs="+", help=selector
    )
    delete_parser.add_argument(
        "--apply", action="store_true", help="Write the selected deletions."
    )
    delete_parser.add_argument(
        "--allow-dangling",
        action="store_true",
        help="Apply despite references to review.",
    )
    args = parser.parse_args(argv)
    if args.command == "query" and args.depth < 1:
        parser.error("--depth must be at least 1")
    return args


def main(argv=None):
    args = parse_args(argv)
    roots = args.root or DEFAULT_ROOTS
    try:
        index = Index(roots)
        if args.command in ("stats", "list"):
            records = filter_records(index, args.type)
            if args.command == "stats":
                result = counts(index, records)
            else:
                rows, truncated = limit_rows(
                    (r.describe() for r in records), args.limit
                )
                result = {
                    "definitions": rows,
                    "count": len(records),
                    "truncated": truncated,
                }
        else:
            code_roots = args.code_root or (
                [] if args.root else [REPO / "src"]
            )
            index.build_graph()
            if args.command == "query":
                result = query(index, args, code_roots)
            else:
                result = delete(index, args, code_roots)
            result["scope"] = STATIC_SCOPE
            result["code_roots"] = [display(p.absolute()) for p in code_roots]
        result["roots"] = [display(p.absolute()) for p in roots]
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_result(args.command, result)
        if args.command == "delete" and args.apply and not result["applied"]:
            print(
                "Deletion blocked by references. Review the report above.",
                file=sys.stderr,
            )
            return 1
    except (ToolError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
