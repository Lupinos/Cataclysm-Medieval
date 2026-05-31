---
name: medieval-json-check
description: Run C++-level JSON semantic validation via --check-mods. Captures errors through stderr to a clean per-run file. Use to verify Medieval mod JSON correctness after generation, or to diagnose existing JSON errors with categorized fix guidance.
---

# Medieval JSON Check (C++ Level Validation)

Runs `cataclysm-tiles.exe --check-mods` to validate Medieval mod JSON through the **full C++ loading pipeline** — the same path the game uses when loading a world. This catches errors that JSON syntax checkers cannot: missing dependencies, invalid ID references, CDDA text style violations, plural form generation failures, and inter-type consistency issues.

**Exe path**: `E:\Cataclysm-Medieval\cataclysm-tiles.exe`
**Validation scope**: Loads core data + Medieval mod data → runs ~60 `finalize_loaded_data()` steps + ~45 `check_consistency`/`check_definitions` checks

---

## Phase 1: Run Check

### Command

```powershell
cd E:\Cataclysm-Medieval
.\cataclysm-tiles.exe --check-mods medieval 2> check_errors.txt
echo "Exit: $?"
```

- Exit **0**: All checks passed, mod is clean
- Exit **1**: Errors found → proceed to Phase 2
- The `2>` redirect captures stderr (where `DebugLog` errors now go after `src/debug.cpp` modification) into `check_errors.txt`
- `check_errors.txt` is **overwritten** on each run (unlike `config/debug.log` which is append-only and can be 1MB+)

### What gets validated

| Check level | Source | What it catches |
|-------------|--------|----------------|
| JSON data loading | `DynamicDataLoader` | All 80+ CDDA JSON types parsed through their C++ load handlers |
| `finalize_data()` | ~60 finalize steps | Cross-JSON linking (recipes→items, spawns→monsters, etc.) |
| `check_consistency()` | ~45 consistency checks | Missing dependencies, orphan IDs, invalid references |
| `check_definitions()` | type-specific | Plural forms, material thickness, armor body parts |
| Text style | `text_style_check_reader.cpp:55` | Double-space rule after sentence-ending periods (`.  ` required) |
| Translation/plural | `translation.cpp:250` | Plural form auto-generation failures (needs explicit `str_pl` or `str_sp`) |

---

## Phase 2: Error Analysis

When exit 1, read `check_errors.txt` and categorize every error. Present findings to the user in a structured report.

### Error Type Priority

Errors should be grouped by type and prioritized:

| Priority | Error type | Source file | Why important |
|----------|-----------|-------------|---------------|
| **CRITICAL** | Missing dependencies/mods | `game.cpp:518-520` | Mod will not load at all |
| **CRITICAL** | Invalid type/data errors | `debug.cpp` via `realDebugmsg` | JSON fundamentally corrupt in C++ view |
| **HIGH** | Armor body part errors | `item_factory.cpp:2006` | Secondary body parts (e.g., `torso_neck`) rejected for ARMOR type |
| **HIGH** | Material thickness violations | material system | `sheet_thickness` not an integer multiple |
| **HIGH** | Armor `encumbrance_modifiers` on non-head | `itype.cpp:370-389` | Non-head body parts lack `encumbrance_per_weight` table |
| **MEDIUM** | Plural form failures | `translation.cpp:250` | Item name won't pluralize correctly in-game ("a pair of XXXs") |
| **LOW** | Text style (single vs double space) | `text_style_check_reader.cpp:55` | CDDA convention (`.  ` after sentence-end period); cosmetic but flagged as error |
| **LOW** | Unknown JSON types (silently skipped) | `DynamicDataLoader` | Unknown types silently skipped — no error but data silently lost |

### Error Report Template

```
## Check Result for Medieval Mod

**Exit code**: 1 (XX errors found)

### CRITICAL (X errors)
- [source:line] Description → Fix: ...

### HIGH (X errors)  
- [source:line] Description → Fix: ...

### MEDIUM (X errors)
- [source:line] Plural form for "item_name" → Fix: add "str_pl" or "str_sp" to name object

### LOW (X errors)
- [source:line] Text style: need double space after ". " → Fix: add one space
```

---

## Phase 3: Fix Guidance

For each error category, provide the user with a fix strategy. Ask the user whether to auto-fix LOW/MEDIUM issues.

### Auto-fixable (ask user first)

| Error | Fix method |
|-------|-----------|
| Plural form missing `str_pl`/`str_sp` | Add `"str_pl": "item_names"` or `"str_sp": "item_name"` to name object |
| Text style single-sentence-space | Add ` ` after each `. ` before the next word in description |
| Missing `str` in name field | Wrap name in `{ "str": "..." }` instead of bare string |

### Manual review needed

| Error | Required action |
|-------|----------------|
| Missing dependencies | Add missing mod to `dependencies` in modinfo.json, or create missing JSON entities |
| Armor body part violations | Change `covers` to valid body part for ARMOR type |
| Material thickness not integer multiple | Adjust `thickness` to match material's `sheet_thickness` × N, or add `"ignore_sheet_thickness": true` |
| Any C++-level load failure | Requires understanding of what the C++ loader expects; consult [json_data_system.md](../../docs/vanilla/json_data_system.md) |

---

## Phase 4: Retry Loop

After fixes are applied, re-run Phase 1. Loop until exit 0.

```
Run check → Exit 1? → Analyze errors → Fix → Run check → Exit 1? → ... → Exit 0 ✓
```

**IMPORTANT**: Always present a summary of what was fixed and what the final exit code is.

---

## Tips

### Common errors in Medieval mod

Based on known error patterns:

1. **Plural forms**: Items named with `"name": { "str": "med_ xxx" }` without `str_pl` will fail if CDDA can't auto-detect the plural form. Add `"str_pl": "med_ xxxs"`.

2. **Text style**: All `description` strings must use double space after sentence-ending `.` (e.g., `"First sentence.  Second sentence."`).

3. **Unknown JSON types**: Custom types not registered in the C++ type list are silently skipped. The data is lost — not reported as an error. Use only standard CDDA JSON types.

4. **`torso_neck` in ARMOR**: Cannot use `torso_neck` (it's `secondary: true`). Neck armor must use `covers: ["head"]` + `specifically_covers: ["head_throat", "head_nape"]`.

### check_errors.txt vs debug.log

| Property | `check_errors.txt` (stderr capture) | `config/debug.log` |
|----------|--------------------------------------|---------------------|
| Per-run | ✓ Clean per run | ✗ Append-only, cumulative |
| Size | ~30KB for Medieval mod errors | Can exceed 1MB |
| Generated by | `2> check_errors.txt` on command | Automatically by game engine |
| Includes previous runs | Never | Yes (accumulated history) |
| Read format | `Read` tool on the file | `Read` tool on the file |

**Always use `check_errors.txt` for development iteration.**
