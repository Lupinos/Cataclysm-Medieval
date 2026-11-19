import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).with_name("gm_items.py")
CATALOG = [
    {"id": "knife", "variant": "", "name": "stone knife"},
    {"id": "knife", "variant": "plastic", "name": "plastic knife"},
    {"id": "radio", "variant": "", "name": "radio"},
    {"id": "apple", "variant": "", "name": "apple"},
]


class GmItemCatalogTest(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        directory = Path(workspace.name)
        self.catalog = directory / "catalog.json"
        self.catalog.write_text(json.dumps(CATALOG), encoding="utf-8")
        self.review = directory / "review.csv"

    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, str(TOOL), str(self.catalog), *args],
            capture_output=True, text=True, check=False,
        )

    def test_review_enumerates_base_items_and_variants(self):
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = list(csv.DictReader(io.StringIO(result.stdout)))
        self.assertEqual(
            [(r["id"], r["variant"]) for r in rows],
            [(r["id"], r["variant"]) for r in CATALOG],
        )
        self.assertTrue(all(r["decision"] == "" for r in rows))

    def test_check_rejects_unreviewed_variants_and_excluded_items(self):
        self.review.write_text(
            "id,variant,name,decision\nknife,,stone knife,keep\n"
            "radio,,radio,remove\nflint,,flint,keep\n",
            encoding="utf-8",
        )
        result = self.run_tool("--review", str(self.review))
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["present_removed"], [CATALOG[2]])
        self.assertEqual(
            report["present_unreviewed"], [CATALOG[3], CATALOG[1]]
        )
        self.assertEqual(report["missing_kept"],
                         [{"id": "flint", "variant": "", "name": "flint"}])

    def test_check_passes_when_catalog_matches_the_reviewed_keep_set(self):
        self.catalog.write_text(json.dumps(CATALOG[:1]), encoding="utf-8")
        self.review.write_text(
            "id,variant,name,decision\nknife,,stone knife,keep\n"
            "knife,plastic,plastic knife,remove\n",
            encoding="utf-8",
        )
        result = self.run_tool("--review", str(self.review))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_check_counts_each_entry_when_variant_ids_repeat(self):
        new = {"id": "knife", "variant": "", "name": "bronze knife"}
        self.catalog.write_text(
            json.dumps([CATALOG[0], new, new]), encoding="utf-8"
        )
        self.review.write_text(
            "id,variant,name,decision\nknife,,stone knife,keep\n"
            "knife,,bronze knife,remove\n",
            encoding="utf-8",
        )
        result = self.run_tool("--review", str(self.review))
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["present_removed"], [new])
        self.assertEqual(report["present_unreviewed"], [new])
        self.assertEqual(report["missing_kept"], [])


if __name__ == "__main__":
    unittest.main()
