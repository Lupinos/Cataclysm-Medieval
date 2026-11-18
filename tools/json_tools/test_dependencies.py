import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dependencies import Change, apply_changes


TOOL = Path(__file__).with_name("dependencies.py")


class DependencyToolTest(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        self.data = self.root / "data"
        self.data.mkdir()

    def write(self, name, value):
        path = self.data / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def run_tool(self, *args, ok=True):
        self.assertTrue(
            TOOL.is_file(), "Dependency tool has not been implemented"
        )
        result = subprocess.run(
            [sys.executable, str(TOOL), *args, "--root", "data", "--json"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if ok:
            self.assertEqual(
                result.returncode, 0, result.stderr + result.stdout
            )
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_counts_declarations_ids_types_and_anonymous_entries(self):
        self.write(
            "base.json",
            [
                {"type": "GENERIC", "id": "stone"},
                {"type": "material", "id": "stone"},
                {"type": "ARMOR", "abstract": "padded"},
                {"type": "overmap_terrain", "id": ["river", "bank"]},
                {"type": "SCENARIO_BLACKLIST", "scenarios": []},
            ],
        )
        self.write("overlay.json", {"type": "GENERIC", "id": "stone"})
        counts = self.run_tool("stats")
        self.assertEqual(counts["files"], 2)
        self.assertEqual(counts["declarations"], 6)
        self.assertEqual(counts["unique_ids"], 5)
        self.assertEqual(counts["anonymous"], 1)
        self.assertEqual(counts["abstracts"], 1)
        self.assertEqual(counts["by_type"]["GENERIC"], 2)
        self.assertEqual(
            self.run_tool("stats", "--type", "item")["declarations"], 3
        )

    def test_query_tracks_typed_links_and_dependency_paths(self):
        self.write(
            "nature.json",
            [
                {"type": "material", "id": "apple"},
                {"type": "COMESTIBLE", "id": "apple", "material": ["apple"]},
                {
                    "type": "harvest",
                    "id": "fall_fruit",
                    "entries": [{"drop": "apple"}],
                },
                {
                    "type": "terrain",
                    "id": "orchard_tree",
                    "harvest_by_season": [
                        {"id": "fall_fruit", "seasons": ["autumn"]}
                    ],
                },
                {
                    "type": "item_group",
                    "id": "apple",
                    "entries": [{"item": "apple"}],
                },
                {
                    "type": "mapgen",
                    "om_terrain": "forest",
                    "object": {
                        "place_items": [{"item": "apple"}, {"item": "missing"}]
                    },
                },
                {"type": "GENERIC", "id": "sign", "description": "apple"},
            ],
        )
        result = self.run_tool("query", "item:apple", "--depth", "2")
        self.assertEqual(
            result["definitions"][0]["location"], "@data/nature.json#/1"
        )
        self.assertEqual(
            [r["target"] for r in result["uses"]], ["material:apple"]
        )
        paths = {tuple(r["path"]) for r in result["used_by"]}
        self.assertIn(
            ("item:apple", "harvest:fall_fruit", "terrain:orchard_tree"), paths
        )
        self.assertIn(
            ("item:apple", "item_group:apple", "mapgen:forest"), paths
        )
        self.assertNotIn(("item:apple", "item:sign"), paths)
        result = self.run_tool("query", "mapgen:forest")
        self.assertTrue(
            any(
                r["target"] == "item_group:missing" and not r["targets"]
                for r in result["uses"]
            )
        )
        result = self.run_tool("query", "apple", ok=False)
        self.assertIn("ambiguous", result.stderr)

    def test_recipe_id_and_list_requirements(self):
        self.write(
            "craft.json",
            [
                {"type": "GENERIC", "id": "plank"},
                {"type": "GENERIC", "id": "saw"},
                {
                    "type": "requirement",
                    "id": "wood",
                    "components": [[["plank", 2]]],
                },
                {
                    "type": "recipe",
                    "result": "plank",
                    "id_suffix": "sawn",
                    "tools": [[["saw", -1]]],
                    "components": [[["wood", 1, "LIST"]]],
                },
            ],
        )
        result = self.run_tool("query", "recipe:plank_sawn")
        self.assertEqual(
            {r["target"] for r in result["uses"]},
            {"item:plank", "item:saw", "requirement:wood"},
        )

    def test_delete_previews_then_removes_only_requested_objects(self):
        path = self.data / "items.json"
        before = (
            b'[\r\n  { "type": "GENERIC", "id": "keep", "//": "keep me" },\r\n'
            b'  { "type": "GENERIC", "id": "drop" },\r\n'
            b'  { "type": "material", "id": "drop" }\r\n]\r\n'
        )
        path.write_bytes(before)
        group = self.write(
            "group.json",
            {
                "type": "item_group",
                "id": "example",
                "items": [["drop", 1]],
            },
        )
        preview = self.run_tool("delete", "item:drop")
        self.assertFalse(preview["applied"])
        self.assertEqual(preview["references"][0]["field"], "/items/0/0")
        self.run_tool("delete", "item:drop", "--apply", ok=False)
        self.assertEqual(path.read_bytes(), before)
        result = self.run_tool(
            "delete", "item:drop", "item_group:example", "--apply"
        )
        self.assertTrue(result["applied"])
        self.assertEqual(result["declarations_removed"], 2)
        self.assertEqual(
            path.read_bytes(),
            before.replace(b'  { "type": "GENERIC", "id": "drop" },\r\n', b""),
        )
        self.assertEqual(json.loads(group.read_bytes()), [])

    def test_deleting_one_of_many_ids_preserves_the_other_ids(self):
        path = self.write(
            "terrain.json",
            [
                {"type": "overmap_terrain", "id": ["a", "b", "c"]},
                {"type": "mapgen", "om_terrain": [["a", "b"], ["c", "d"]]},
            ],
        )
        original = path.read_bytes()
        self.run_tool("delete", "mapgen:b", "--apply", ok=False)
        self.assertEqual(path.read_bytes(), original)
        result = self.run_tool("delete", "overmap_terrain:b", "--apply")
        self.assertEqual(result["declarations_removed"], 0)
        self.assertEqual(json.loads(path.read_bytes())[0]["id"], ["a", "c"])
        self.run_tool("delete", "@data/terrain.json#/1", "--apply", ok=False)
        result = self.run_tool(
            "delete", "@data/terrain.json#/1", "--apply", "--allow-dangling"
        )
        self.assertEqual(result["declarations_removed"], 1)

    def test_multiple_declarations_require_an_explicit_location(self):
        self.write("base.json", {"type": "GENERIC", "id": "duplicate"})
        path = self.write(
            "nested/mod.json",
            {
                "type": "TOOL",
                "id": "duplicate",
                "copy-from": "duplicate",
            },
        )
        result = self.run_tool("query", "item:duplicate")
        self.assertEqual(len(result["definitions"]), 2)
        self.assertEqual(result["uses"][0]["targets"], ["@data/base.json#"])
        self.run_tool("delete", "item:duplicate", "--apply", ok=False)
        self.run_tool("delete", "@data/base.json#", "--apply", ok=False)
        self.run_tool("delete", "@data/nested/mod.json#", "--apply")
        self.assertEqual(json.loads(path.read_bytes()), [])

    def test_invalid_batch_target_leaves_all_files_untouched(self):
        path = self.write("a.json", {"type": "GENERIC", "id": "exists"})
        before = path.read_bytes()
        self.run_tool(
            "delete", "item:exists", "item:unknown", "--apply", ok=False
        )
        self.assertEqual(path.read_bytes(), before)

    def test_write_failure_restores_earlier_files_in_the_batch(self):
        first = self.write("a.json", {"type": "GENERIC", "id": "first"})
        second = self.write("b.json", {"type": "GENERIC", "id": "second"})
        changes = [Change(p, p.read_bytes(), b"[]\n") for p in (first, second)]
        real_replace = os.replace

        def replace(source, target):
            if target == second:
                raise PermissionError("simulated second-file failure")
            real_replace(source, target)

        with patch("dependencies.os.replace", side_effect=replace):
            with self.assertRaises(PermissionError):
                apply_changes(changes)
        for change in changes:
            self.assertEqual(change.path.read_bytes(), change.before)
        self.assertEqual(set(self.data.iterdir()), {first, second})

    def test_mapgen_world_and_vehicle_links_include_engine_generated_ids(self):
        self.write(
            "world.json",
            [
                {"type": "overmap_terrain", "id": "cabin"},
                {
                    "type": "city_building",
                    "id": "stay",
                    "overmaps": [{"overmap": "cabin_north"}],
                },
                {
                    "type": "region_settings",
                    "id": "default",
                    "city": {"houses": {"stay": 5}},
                    "map_extras": {"forest": {"extras": {"wreck": 1}}},
                },
                {
                    "type": "map_extra",
                    "id": "wreck",
                    "generator": {
                        "generator_method": "mapgen",
                        "generator_id": "cabin",
                    },
                },
                {
                    "type": "mapgen",
                    "om_terrain": "cabin",
                    "object": {"place_vehicles": [{"vehicle": "cart"}]},
                },
                {
                    "type": "vehicle",
                    "id": "cart",
                    "parts": [{"parts": ["axle#2"]}],
                },
                {"type": "vehicle_part", "id": "axle"},
            ],
        )
        result = self.run_tool("query", "vehicle_part:axle", "--depth", "5")
        paths = {tuple(row["path"]) for row in result["used_by"]}
        self.assertIn(
            (
                "vehicle_part:axle",
                "vehicle:cart",
                "mapgen:cabin",
                "overmap_terrain:cabin",
                "overmap_special:stay",
                "region_settings:default",
            ),
            paths,
        )
        self.assertIn(
            (
                "vehicle_part:axle",
                "vehicle:cart",
                "mapgen:cabin",
                "map_extra:wreck",
                "region_settings:default",
            ),
            paths,
        )

    def test_plain_bash_drop_field_references_an_item_group(self):
        self.write(
            "world.json",
            [
                {"type": "item_group", "id": "sticks"},
                {"type": "GENERIC", "id": "sticks"},
                {
                    "type": "terrain",
                    "id": "t_tree",
                    "bash": {"items": "sticks"},
                },
            ],
        )
        result = self.run_tool("query", "terrain:t_tree")
        self.assertEqual(
            [r["target"] for r in result["uses"]], ["item_group:sticks"]
        )

    def test_cpp_literals_are_reported_and_can_block_deletion(self):
        path = self.write("items.json", {"type": "GENERIC", "id": "test_item"})
        before = path.read_bytes()
        code = self.root / "src"
        code.mkdir()
        (code / "example.cpp").write_text(
            '// itype_id("test_item");\n'
            'const itype_id example{ "test_item" };\n',
            encoding="utf-8",
        )
        result = self.run_tool("query", "item:test_item", "--code-root", "src")
        self.assertEqual(
            [(ref["file"], ref["line"]) for ref in result["code"]],
            [("src/example.cpp", 2)],
        )
        self.run_tool(
            "delete",
            "item:test_item",
            "--code-root",
            "src",
            "--apply",
            ok=False,
        )
        self.assertEqual(path.read_bytes(), before)
        self.run_tool(
            "delete",
            "item:test_item",
            "--code-root",
            "src",
            "--apply",
            "--allow-dangling",
        )
        self.assertEqual(json.loads(path.read_bytes()), [])


if __name__ == "__main__":
    unittest.main()
