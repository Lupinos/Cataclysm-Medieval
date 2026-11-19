# 原版武器 JSON 字段盘点

对应策划：[04 武器体系及其分案](../design/design04-武器.md)。本篇提供原版武器 JSON 的编写与字段依据，具体装备选型和游戏定位见策划案。

本表由skill中的 `scripts/inventory_weapons.py` 扫描当前工作树生成。它是声明盘点，不是游戏加载后的最终物品数据库。详细语义见[武器编写指南](guide04_weapons_json.md)。

## 统计口径

- 范围：`data/json/**/*.json`，排除 `data/mods`、测试数据与外部mod。
- 选择：近战目录的物品声明；所有GUN/GUNMOD/AMMO/MAGAZINE；显式含近战伤害、投掷伤害、武器类别或武器槽的物品；以及这些条目的copy-from后代。
- 该口径有意包含工具、护甲等可作武器的物品，以及非战斗用途弹药；不把它们都称作独立武器类型。没有显式战斗字段且不在选中父链的普通可投物可能不在本表。
- `id`与`abstract`分别计数；同ID多次声明按声明计数。字段次数仅统计该层显式出现，每个嵌套路径在同一条声明中只计一次；不展开继承，不模拟finalize，不把未出现视为不支持。
- 读取到物品声明9581条，选中4180条：具体声明4112条，abstract声明68条。
- JSON解析失败0个文件；若非零则此表不能视作全量扫描。

## 按主类型

| type | 声明数 |
|---|---:|
| `AMMO` | 734 |
| `ARMOR` | 684 |
| `BIONIC_ITEM` | 124 |
| `BOOK` | 245 |
| `COMESTIBLE` | 12 |
| `GENERIC` | 670 |
| `GUN` | 389 |
| `GUNMOD` | 182 |
| `MAGAZINE` | 373 |
| `PET_ARMOR` | 8 |
| `TOOL` | 678 |
| `TOOL_ARMOR` | 56 |
| `WHEEL` | 25 |

## 近战目录单独统计

仅统计data/json/items/melee的声明，不含目录外工具，不代表按历史形制去重后的数量。

| 文件 | 具体声明 | abstract |
|---|---:|---:|
| [data/json/items/melee/bludgeons.json](../../data/json/items/melee/bludgeons.json) | 92 | 0 |
| [data/json/items/melee/fake.json](../../data/json/items/melee/fake.json) | 2 | 0 |
| [data/json/items/melee/knives_kitchen.json](../../data/json/items/melee/knives_kitchen.json) | 8 | 1 |
| [data/json/items/melee/misc.json](../../data/json/items/melee/misc.json) | 3 | 0 |
| [data/json/items/melee/spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json) | 46 | 0 |
| [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) | 205 | 0 |
| [data/json/items/melee/unarmed_weapons.json](../../data/json/items/melee/unarmed_weapons.json) | 24 | 0 |

## 按文件

| 文件 | 具体声明 | abstract |
|---|---:|---:|
| [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) | 19 | 0 |
| [data/json/items/ammo.json](../../data/json/items/ammo.json) | 96 | 0 |
| [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) | 10 | 0 |
| [data/json/items/ammo/12mm.json](../../data/json/items/ammo/12mm.json) | 1 | 0 |
| [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) | 6 | 1 |
| [data/json/items/ammo/22.json](../../data/json/items/ammo/22.json) | 10 | 0 |
| [data/json/items/ammo/223.json](../../data/json/items/ammo/223.json) | 13 | 0 |
| [data/json/items/ammo/270win.json](../../data/json/items/ammo/270win.json) | 5 | 1 |
| [data/json/items/ammo/300.json](../../data/json/items/ammo/300.json) | 3 | 0 |
| [data/json/items/ammo/3006.json](../../data/json/items/ammo/3006.json) | 12 | 0 |
| [data/json/items/ammo/300blk.json](../../data/json/items/ammo/300blk.json) | 4 | 0 |
| [data/json/items/ammo/303.json](../../data/json/items/ammo/303.json) | 9 | 0 |
| [data/json/items/ammo/308.json](../../data/json/items/ammo/308.json) | 10 | 0 |
| [data/json/items/ammo/30carbine.json](../../data/json/items/ammo/30carbine.json) | 8 | 0 |
| [data/json/items/ammo/32.json](../../data/json/items/ammo/32.json) | 8 | 0 |
| [data/json/items/ammo/338lapua.json](../../data/json/items/ammo/338lapua.json) | 9 | 0 |
| [data/json/items/ammo/357mag.json](../../data/json/items/ammo/357mag.json) | 8 | 0 |
| [data/json/items/ammo/357sig.json](../../data/json/items/ammo/357sig.json) | 8 | 0 |
| [data/json/items/ammo/36paper.json](../../data/json/items/ammo/36paper.json) | 1 | 0 |
| [data/json/items/ammo/38.json](../../data/json/items/ammo/38.json) | 10 | 0 |
| [data/json/items/ammo/380.json](../../data/json/items/ammo/380.json) | 10 | 0 |
| [data/json/items/ammo/38super.json](../../data/json/items/ammo/38super.json) | 8 | 0 |
| [data/json/items/ammo/40.json](../../data/json/items/ammo/40.json) | 8 | 0 |
| [data/json/items/ammo/40x46mm.json](../../data/json/items/ammo/40x46mm.json) | 21 | 1 |
| [data/json/items/ammo/40x53mm.json](../../data/json/items/ammo/40x53mm.json) | 8 | 1 |
| [data/json/items/ammo/410shot.json](../../data/json/items/ammo/410shot.json) | 11 | 0 |
| [data/json/items/ammo/44.json](../../data/json/items/ammo/44.json) | 6 | 0 |
| [data/json/items/ammo/44paper.json](../../data/json/items/ammo/44paper.json) | 1 | 0 |
| [data/json/items/ammo/45.json](../../data/json/items/ammo/45.json) | 10 | 0 |
| [data/json/items/ammo/450bushmaster.json](../../data/json/items/ammo/450bushmaster.json) | 6 | 0 |
| [data/json/items/ammo/454.json](../../data/json/items/ammo/454.json) | 3 | 0 |
| [data/json/items/ammo/4570.json](../../data/json/items/ammo/4570.json) | 7 | 0 |
| [data/json/items/ammo/458wm.json](../../data/json/items/ammo/458wm.json) | 3 | 1 |
| [data/json/items/ammo/45colt.json](../../data/json/items/ammo/45colt.json) | 11 | 1 |
| [data/json/items/ammo/46.json](../../data/json/items/ammo/46.json) | 3 | 0 |
| [data/json/items/ammo/460.json](../../data/json/items/ammo/460.json) | 6 | 0 |
| [data/json/items/ammo/50.json](../../data/json/items/ammo/50.json) | 11 | 0 |
| [data/json/items/ammo/500.json](../../data/json/items/ammo/500.json) | 3 | 0 |
| [data/json/items/ammo/50_beowulf.json](../../data/json/items/ammo/50_beowulf.json) | 6 | 0 |
| [data/json/items/ammo/50ae.json](../../data/json/items/ammo/50ae.json) | 8 | 0 |
| [data/json/items/ammo/545x39.json](../../data/json/items/ammo/545x39.json) | 6 | 0 |
| [data/json/items/ammo/57.json](../../data/json/items/ammo/57.json) | 4 | 0 |
| [data/json/items/ammo/66mm.json](../../data/json/items/ammo/66mm.json) | 2 | 0 |
| [data/json/items/ammo/762.json](../../data/json/items/ammo/762.json) | 6 | 0 |
| [data/json/items/ammo/762R.json](../../data/json/items/ammo/762R.json) | 3 | 0 |
| [data/json/items/ammo/762x25.json](../../data/json/items/ammo/762x25.json) | 6 | 0 |
| [data/json/items/ammo/77mm_jap.json](../../data/json/items/ammo/77mm_jap.json) | 3 | 0 |
| [data/json/items/ammo/84x246mm.json](../../data/json/items/ammo/84x246mm.json) | 3 | 0 |
| [data/json/items/ammo/8x40mm.json](../../data/json/items/ammo/8x40mm.json) | 3 | 0 |
| [data/json/items/ammo/9mm.json](../../data/json/items/ammo/9mm.json) | 12 | 0 |
| [data/json/items/ammo/9x18.json](../../data/json/items/ammo/9x18.json) | 10 | 0 |
| [data/json/items/ammo/atgm.json](../../data/json/items/ammo/atgm.json) | 1 | 0 |
| [data/json/items/ammo/barb.json](../../data/json/items/ammo/barb.json) | 1 | 0 |
| [data/json/items/ammo/blank.json](../../data/json/items/ammo/blank.json) | 1 | 0 |
| [data/json/items/ammo/cannon.json](../../data/json/items/ammo/cannon.json) | 1 | 0 |
| [data/json/items/ammo/chemical_spray.json](../../data/json/items/ammo/chemical_spray.json) | 3 | 0 |
| [data/json/items/ammo/exodii.json](../../data/json/items/ammo/exodii.json) | 13 | 2 |
| [data/json/items/ammo/flintlock.json](../../data/json/items/ammo/flintlock.json) | 2 | 0 |
| [data/json/items/ammo/nail.json](../../data/json/items/ammo/nail.json) | 3 | 0 |
| [data/json/items/ammo/paintball.json](../../data/json/items/ammo/paintball.json) | 1 | 0 |
| [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) | 19 | 1 |
| [data/json/items/ammo/shotpaper.json](../../data/json/items/ammo/shotpaper.json) | 4 | 1 |
| [data/json/items/ammo/signal_flare.json](../../data/json/items/ammo/signal_flare.json) | 1 | 0 |
| [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) | 6 | 0 |
| [data/json/items/ammo/weldgas.json](../../data/json/items/ammo/weldgas.json) | 7 | 0 |
| [data/json/items/appliances.json](../../data/json/items/appliances.json) | 6 | 0 |
| [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) | 11 | 0 |
| [data/json/items/armor/arms_armor.json](../../data/json/items/armor/arms_armor.json) | 34 | 0 |
| [data/json/items/armor/ballistic_armor.json](../../data/json/items/armor/ballistic_armor.json) | 1 | 0 |
| [data/json/items/armor/bespoke_armor/custom_bodysuits.json](../../data/json/items/armor/bespoke_armor/custom_bodysuits.json) | 27 | 0 |
| [data/json/items/armor/bespoke_armor/custom_boots.json](../../data/json/items/armor/bespoke_armor/custom_boots.json) | 21 | 0 |
| [data/json/items/armor/bespoke_armor/custom_headgear.json](../../data/json/items/armor/bespoke_armor/custom_headgear.json) | 21 | 0 |
| [data/json/items/armor/bespoke_armor/cuttingroom.json](../../data/json/items/armor/bespoke_armor/cuttingroom.json) | 21 | 0 |
| [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) | 57 | 0 |
| [data/json/items/armor/brigandine.json](../../data/json/items/armor/brigandine.json) | 75 | 0 |
| [data/json/items/armor/gloves.json](../../data/json/items/armor/gloves.json) | 35 | 0 |
| [data/json/items/armor/hats.json](../../data/json/items/armor/hats.json) | 2 | 0 |
| [data/json/items/armor/helmets.json](../../data/json/items/armor/helmets.json) | 148 | 0 |
| [data/json/items/armor/integrated.json](../../data/json/items/armor/integrated.json) | 6 | 0 |
| [data/json/items/armor/jewelry.json](../../data/json/items/armor/jewelry.json) | 17 | 0 |
| [data/json/items/armor/legs_armor.json](../../data/json/items/armor/legs_armor.json) | 34 | 0 |
| [data/json/items/armor/misc.json](../../data/json/items/armor/misc.json) | 1 | 0 |
| [data/json/items/armor/pets_dog_armor.json](../../data/json/items/armor/pets_dog_armor.json) | 7 | 0 |
| [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) | 16 | 0 |
| [data/json/items/armor/sheath.json](../../data/json/items/armor/sheath.json) | 4 | 0 |
| [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) | 15 | 0 |
| [data/json/items/armor/suits_protection.json](../../data/json/items/armor/suits_protection.json) | 70 | 0 |
| [data/json/items/armor/torso_armor.json](../../data/json/items/armor/torso_armor.json) | 52 | 0 |
| [data/json/items/armor/torso_clothes.json](../../data/json/items/armor/torso_clothes.json) | 2 | 0 |
| [data/json/items/basecamp.json](../../data/json/items/basecamp.json) | 1 | 0 |
| [data/json/items/battery.json](../../data/json/items/battery.json) | 19 | 0 |
| [data/json/items/bionics.json](../../data/json/items/bionics.json) | 121 | 3 |
| [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) | 0 | 26 |
| [data/json/items/book/barter.json](../../data/json/items/book/barter.json) | 1 | 0 |
| [data/json/items/book/chemistry.json](../../data/json/items/book/chemistry.json) | 7 | 0 |
| [data/json/items/book/computer.json](../../data/json/items/book/computer.json) | 3 | 0 |
| [data/json/items/book/cooking.json](../../data/json/items/book/cooking.json) | 17 | 0 |
| [data/json/items/book/dodge.json](../../data/json/items/book/dodge.json) | 2 | 0 |
| [data/json/items/book/electronics.json](../../data/json/items/book/electronics.json) | 6 | 0 |
| [data/json/items/book/fabrication.json](../../data/json/items/book/fabrication.json) | 11 | 0 |
| [data/json/items/book/firstaid.json](../../data/json/items/book/firstaid.json) | 4 | 0 |
| [data/json/items/book/mechanics.json](../../data/json/items/book/mechanics.json) | 4 | 0 |
| [data/json/items/book/misc.json](../../data/json/items/book/misc.json) | 64 | 0 |
| [data/json/items/book/misc_newage.json](../../data/json/items/book/misc_newage.json) | 10 | 0 |
| [data/json/items/book/misc_philosophy.json](../../data/json/items/book/misc_philosophy.json) | 5 | 0 |
| [data/json/items/book/misc_pulp.json](../../data/json/items/book/misc_pulp.json) | 9 | 0 |
| [data/json/items/book/misc_scifi.json](../../data/json/items/book/misc_scifi.json) | 12 | 0 |
| [data/json/items/book/misc_sports.json](../../data/json/items/book/misc_sports.json) | 14 | 0 |
| [data/json/items/book/nonfiction.json](../../data/json/items/book/nonfiction.json) | 22 | 0 |
| [data/json/items/book/speech.json](../../data/json/items/book/speech.json) | 3 | 0 |
| [data/json/items/book/survival.json](../../data/json/items/book/survival.json) | 4 | 0 |
| [data/json/items/book/tailor.json](../../data/json/items/book/tailor.json) | 6 | 0 |
| [data/json/items/book/traps.json](../../data/json/items/book/traps.json) | 2 | 0 |
| [data/json/items/book/young.json](../../data/json/items/book/young.json) | 12 | 0 |
| [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) | 63 | 0 |
| [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) | 0 | 18 |
| [data/json/items/classes/magazine.json](../../data/json/items/classes/magazine.json) | 0 | 1 |
| [data/json/items/comestibles/carnivore.json](../../data/json/items/comestibles/carnivore.json) | 1 | 0 |
| [data/json/items/comestibles/drink.json](../../data/json/items/comestibles/drink.json) | 3 | 0 |
| [data/json/items/comestibles/raw_fruit.json](../../data/json/items/comestibles/raw_fruit.json) | 4 | 0 |
| [data/json/items/comestibles/raw_veggy.json](../../data/json/items/comestibles/raw_veggy.json) | 2 | 0 |
| [data/json/items/comestibles/veggy_dishes.json](../../data/json/items/comestibles/veggy_dishes.json) | 1 | 0 |
| [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) | 40 | 0 |
| [data/json/items/corpses/dead_exodii.json](../../data/json/items/corpses/dead_exodii.json) | 4 | 0 |
| [data/json/items/corpses/dead_yrax.json](../../data/json/items/corpses/dead_yrax.json) | 3 | 0 |
| [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) | 36 | 0 |
| [data/json/items/fake.json](../../data/json/items/fake.json) | 2 | 0 |
| [data/json/items/fluff.json](../../data/json/items/fluff.json) | 4 | 0 |
| [data/json/items/fuel.json](../../data/json/items/fuel.json) | 19 | 0 |
| [data/json/items/generic.json](../../data/json/items/generic.json) | 97 | 0 |
| [data/json/items/generic/bathroom_house.json](../../data/json/items/generic/bathroom_house.json) | 16 | 1 |
| [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) | 64 | 7 |
| [data/json/items/generic/spares.json](../../data/json/items/generic/spares.json) | 4 | 0 |
| [data/json/items/generic/toys_and_sports.json](../../data/json/items/generic/toys_and_sports.json) | 12 | 0 |
| [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) | 11 | 0 |
| [data/json/items/gun/12mm.json](../../data/json/items/gun/12mm.json) | 1 | 0 |
| [data/json/items/gun/20x66mm.json](../../data/json/items/gun/20x66mm.json) | 3 | 0 |
| [data/json/items/gun/22.json](../../data/json/items/gun/22.json) | 10 | 0 |
| [data/json/items/gun/223.json](../../data/json/items/gun/223.json) | 24 | 0 |
| [data/json/items/gun/270win.json](../../data/json/items/gun/270win.json) | 1 | 0 |
| [data/json/items/gun/300.json](../../data/json/items/gun/300.json) | 4 | 0 |
| [data/json/items/gun/3006.json](../../data/json/items/gun/3006.json) | 6 | 0 |
| [data/json/items/gun/300BLK.json](../../data/json/items/gun/300BLK.json) | 3 | 0 |
| [data/json/items/gun/303.json](../../data/json/items/gun/303.json) | 2 | 0 |
| [data/json/items/gun/308.json](../../data/json/items/gun/308.json) | 17 | 0 |
| [data/json/items/gun/30carbine.json](../../data/json/items/gun/30carbine.json) | 2 | 0 |
| [data/json/items/gun/32.json](../../data/json/items/gun/32.json) | 4 | 0 |
| [data/json/items/gun/338lapua.json](../../data/json/items/gun/338lapua.json) | 4 | 0 |
| [data/json/items/gun/357sig.json](../../data/json/items/gun/357sig.json) | 3 | 0 |
| [data/json/items/gun/36paper.json](../../data/json/items/gun/36paper.json) | 1 | 0 |
| [data/json/items/gun/38.json](../../data/json/items/gun/38.json) | 7 | 0 |
| [data/json/items/gun/380.json](../../data/json/items/gun/380.json) | 8 | 0 |
| [data/json/items/gun/38super.json](../../data/json/items/gun/38super.json) | 2 | 0 |
| [data/json/items/gun/40.json](../../data/json/items/gun/40.json) | 10 | 0 |
| [data/json/items/gun/40x46mm.json](../../data/json/items/gun/40x46mm.json) | 6 | 0 |
| [data/json/items/gun/40x53mm.json](../../data/json/items/gun/40x53mm.json) | 1 | 0 |
| [data/json/items/gun/410shot.json](../../data/json/items/gun/410shot.json) | 2 | 0 |
| [data/json/items/gun/44.json](../../data/json/items/gun/44.json) | 5 | 0 |
| [data/json/items/gun/44paper.json](../../data/json/items/gun/44paper.json) | 2 | 0 |
| [data/json/items/gun/45.json](../../data/json/items/gun/45.json) | 14 | 0 |
| [data/json/items/gun/450bushmaster.json](../../data/json/items/gun/450bushmaster.json) | 1 | 0 |
| [data/json/items/gun/454.json](../../data/json/items/gun/454.json) | 2 | 0 |
| [data/json/items/gun/4570.json](../../data/json/items/gun/4570.json) | 3 | 0 |
| [data/json/items/gun/458wm.json](../../data/json/items/gun/458wm.json) | 1 | 0 |
| [data/json/items/gun/45colt.json](../../data/json/items/gun/45colt.json) | 3 | 0 |
| [data/json/items/gun/46.json](../../data/json/items/gun/46.json) | 1 | 0 |
| [data/json/items/gun/460.json](../../data/json/items/gun/460.json) | 1 | 0 |
| [data/json/items/gun/50.json](../../data/json/items/gun/50.json) | 5 | 0 |
| [data/json/items/gun/500.json](../../data/json/items/gun/500.json) | 2 | 0 |
| [data/json/items/gun/545x39.json](../../data/json/items/gun/545x39.json) | 2 | 0 |
| [data/json/items/gun/57.json](../../data/json/items/gun/57.json) | 5 | 0 |
| [data/json/items/gun/66mm.json](../../data/json/items/gun/66mm.json) | 1 | 0 |
| [data/json/items/gun/762.json](../../data/json/items/gun/762.json) | 9 | 0 |
| [data/json/items/gun/762R.json](../../data/json/items/gun/762R.json) | 3 | 0 |
| [data/json/items/gun/762x25.json](../../data/json/items/gun/762x25.json) | 2 | 0 |
| [data/json/items/gun/77mm_jap.json](../../data/json/items/gun/77mm_jap.json) | 2 | 0 |
| [data/json/items/gun/84x246mm.json](../../data/json/items/gun/84x246mm.json) | 3 | 0 |
| [data/json/items/gun/8x40mm.json](../../data/json/items/gun/8x40mm.json) | 6 | 0 |
| [data/json/items/gun/9mm.json](../../data/json/items/gun/9mm.json) | 39 | 0 |
| [data/json/items/gun/9x18.json](../../data/json/items/gun/9x18.json) | 2 | 0 |
| [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) | 4 | 0 |
| [data/json/items/gun/atgm.json](../../data/json/items/gun/atgm.json) | 1 | 0 |
| [data/json/items/gun/bio.json](../../data/json/items/gun/bio.json) | 6 | 0 |
| [data/json/items/gun/blunderbuss.json](../../data/json/items/gun/blunderbuss.json) | 1 | 0 |
| [data/json/items/gun/cannon.json](../../data/json/items/gun/cannon.json) | 1 | 0 |
| [data/json/items/gun/chemical_spray.json](../../data/json/items/gun/chemical_spray.json) | 1 | 0 |
| [data/json/items/gun/combination.json](../../data/json/items/gun/combination.json) | 1 | 0 |
| [data/json/items/gun/exodii.json](../../data/json/items/gun/exodii.json) | 6 | 0 |
| [data/json/items/gun/flammable.json](../../data/json/items/gun/flammable.json) | 2 | 0 |
| [data/json/items/gun/flintlock.json](../../data/json/items/gun/flintlock.json) | 5 | 0 |
| [data/json/items/gun/nail.json](../../data/json/items/gun/nail.json) | 2 | 0 |
| [data/json/items/gun/paintball.json](../../data/json/items/gun/paintball.json) | 1 | 0 |
| [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) | 30 | 0 |
| [data/json/items/gun/shot.json](../../data/json/items/gun/shot.json) | 24 | 0 |
| [data/json/items/gun/signal_flare.json](../../data/json/items/gun/signal_flare.json) | 1 | 0 |
| [data/json/items/gun/ups.json](../../data/json/items/gun/ups.json) | 8 | 0 |
| [data/json/items/gunmod/accessories.json](../../data/json/items/gunmod/accessories.json) | 7 | 0 |
| [data/json/items/gunmod/barrel.json](../../data/json/items/gunmod/barrel.json) | 3 | 0 |
| [data/json/items/gunmod/brass_catcher.json](../../data/json/items/gunmod/brass_catcher.json) | 1 | 0 |
| [data/json/items/gunmod/conversions.json](../../data/json/items/gunmod/conversions.json) | 29 | 0 |
| [data/json/items/gunmod/grip.json](../../data/json/items/gunmod/grip.json) | 3 | 0 |
| [data/json/items/gunmod/laser_gunmods.json](../../data/json/items/gunmod/laser_gunmods.json) | 5 | 0 |
| [data/json/items/gunmod/loading_port.json](../../data/json/items/gunmod/loading_port.json) | 7 | 0 |
| [data/json/items/gunmod/mechanism.json](../../data/json/items/gunmod/mechanism.json) | 9 | 0 |
| [data/json/items/gunmod/mount.json](../../data/json/items/gunmod/mount.json) | 8 | 0 |
| [data/json/items/gunmod/muzzle.json](../../data/json/items/gunmod/muzzle.json) | 12 | 0 |
| [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) | 8 | 0 |
| [data/json/items/gunmod/sights.json](../../data/json/items/gunmod/sights.json) | 18 | 0 |
| [data/json/items/gunmod/sling.json](../../data/json/items/gunmod/sling.json) | 3 | 0 |
| [data/json/items/gunmod/stock.json](../../data/json/items/gunmod/stock.json) | 19 | 0 |
| [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) | 38 | 0 |
| [data/json/items/handloaded_bullets.json](../../data/json/items/handloaded_bullets.json) | 4 | 0 |
| [data/json/items/magazine/10mm.json](../../data/json/items/magazine/10mm.json) | 11 | 0 |
| [data/json/items/magazine/12mm.json](../../data/json/items/magazine/12mm.json) | 1 | 0 |
| [data/json/items/magazine/20x60mm.json](../../data/json/items/magazine/20x60mm.json) | 3 | 0 |
| [data/json/items/magazine/22.json](../../data/json/items/magazine/22.json) | 13 | 0 |
| [data/json/items/magazine/223.json](../../data/json/items/magazine/223.json) | 35 | 0 |
| [data/json/items/magazine/300.json](../../data/json/items/magazine/300.json) | 2 | 0 |
| [data/json/items/magazine/3006.json](../../data/json/items/magazine/3006.json) | 5 | 0 |
| [data/json/items/magazine/303.json](../../data/json/items/magazine/303.json) | 2 | 0 |
| [data/json/items/magazine/308.json](../../data/json/items/magazine/308.json) | 27 | 0 |
| [data/json/items/magazine/30carbine.json](../../data/json/items/magazine/30carbine.json) | 2 | 0 |
| [data/json/items/magazine/32.json](../../data/json/items/magazine/32.json) | 3 | 0 |
| [data/json/items/magazine/338lapua.json](../../data/json/items/magazine/338lapua.json) | 3 | 0 |
| [data/json/items/magazine/357mag.json](../../data/json/items/magazine/357mag.json) | 1 | 0 |
| [data/json/items/magazine/357sig.json](../../data/json/items/magazine/357sig.json) | 2 | 0 |
| [data/json/items/magazine/38.json](../../data/json/items/magazine/38.json) | 3 | 0 |
| [data/json/items/magazine/380.json](../../data/json/items/magazine/380.json) | 8 | 0 |
| [data/json/items/magazine/38super.json](../../data/json/items/magazine/38super.json) | 2 | 0 |
| [data/json/items/magazine/40.json](../../data/json/items/magazine/40.json) | 11 | 0 |
| [data/json/items/magazine/40mm.json](../../data/json/items/magazine/40mm.json) | 1 | 0 |
| [data/json/items/magazine/410shot.json](../../data/json/items/magazine/410shot.json) | 2 | 0 |
| [data/json/items/magazine/44.json](../../data/json/items/magazine/44.json) | 2 | 0 |
| [data/json/items/magazine/45.json](../../data/json/items/magazine/45.json) | 18 | 0 |
| [data/json/items/magazine/450bushmaster.json](../../data/json/items/magazine/450bushmaster.json) | 2 | 0 |
| [data/json/items/magazine/454.json](../../data/json/items/magazine/454.json) | 2 | 0 |
| [data/json/items/magazine/46.json](../../data/json/items/magazine/46.json) | 2 | 0 |
| [data/json/items/magazine/460.json](../../data/json/items/magazine/460.json) | 2 | 0 |
| [data/json/items/magazine/50.json](../../data/json/items/magazine/50.json) | 4 | 0 |
| [data/json/items/magazine/500.json](../../data/json/items/magazine/500.json) | 1 | 0 |
| [data/json/items/magazine/50ae.json](../../data/json/items/magazine/50ae.json) | 1 | 0 |
| [data/json/items/magazine/50beowulf.json](../../data/json/items/magazine/50beowulf.json) | 5 | 0 |
| [data/json/items/magazine/545x39.json](../../data/json/items/magazine/545x39.json) | 3 | 0 |
| [data/json/items/magazine/57.json](../../data/json/items/magazine/57.json) | 4 | 0 |
| [data/json/items/magazine/66mm.json](../../data/json/items/magazine/66mm.json) | 1 | 0 |
| [data/json/items/magazine/762.json](../../data/json/items/magazine/762.json) | 14 | 0 |
| [data/json/items/magazine/762R.json](../../data/json/items/magazine/762R.json) | 3 | 0 |
| [data/json/items/magazine/762x25.json](../../data/json/items/magazine/762x25.json) | 3 | 0 |
| [data/json/items/magazine/77mm_jap.json](../../data/json/items/magazine/77mm_jap.json) | 1 | 0 |
| [data/json/items/magazine/8x40mm.json](../../data/json/items/magazine/8x40mm.json) | 6 | 0 |
| [data/json/items/magazine/9mm.json](../../data/json/items/magazine/9mm.json) | 85 | 0 |
| [data/json/items/magazine/9x18.json](../../data/json/items/magazine/9x18.json) | 1 | 0 |
| [data/json/items/magazine/chemical_spray.json](../../data/json/items/magazine/chemical_spray.json) | 1 | 0 |
| [data/json/items/magazine/exodii.json](../../data/json/items/magazine/exodii.json) | 3 | 0 |
| [data/json/items/magazine/filter.json](../../data/json/items/magazine/filter.json) | 5 | 0 |
| [data/json/items/magazine/liquid.json](../../data/json/items/magazine/liquid.json) | 2 | 0 |
| [data/json/items/magazine/methanol_fuelcell.json](../../data/json/items/magazine/methanol_fuelcell.json) | 4 | 0 |
| [data/json/items/magazine/nail.json](../../data/json/items/magazine/nail.json) | 1 | 0 |
| [data/json/items/magazine/shot.json](../../data/json/items/magazine/shot.json) | 7 | 0 |
| [data/json/items/magazine/weldgas.json](../../data/json/items/magazine/weldgas.json) | 2 | 0 |
| [data/json/items/melee/bludgeons.json](../../data/json/items/melee/bludgeons.json) | 92 | 0 |
| [data/json/items/melee/fake.json](../../data/json/items/melee/fake.json) | 2 | 0 |
| [data/json/items/melee/knives_kitchen.json](../../data/json/items/melee/knives_kitchen.json) | 8 | 1 |
| [data/json/items/melee/misc.json](../../data/json/items/melee/misc.json) | 3 | 0 |
| [data/json/items/melee/spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json) | 46 | 0 |
| [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) | 205 | 0 |
| [data/json/items/melee/unarmed_weapons.json](../../data/json/items/melee/unarmed_weapons.json) | 24 | 0 |
| [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) | 31 | 0 |
| [data/json/items/ranged/crossbows.json](../../data/json/items/ranged/crossbows.json) | 19 | 0 |
| [data/json/items/ranged/energy.json](../../data/json/items/ranged/energy.json) | 2 | 0 |
| [data/json/items/ranged/launchers.json](../../data/json/items/ranged/launchers.json) | 3 | 0 |
| [data/json/items/ranged/pneumatic.json](../../data/json/items/ranged/pneumatic.json) | 2 | 0 |
| [data/json/items/ranged/slings.json](../../data/json/items/ranged/slings.json) | 4 | 0 |
| [data/json/items/ranged/spearguns.json](../../data/json/items/ranged/spearguns.json) | 7 | 0 |
| [data/json/items/ranged/throwing.json](../../data/json/items/ranged/throwing.json) | 11 | 0 |
| [data/json/items/relics/altered_items.json](../../data/json/items/relics/altered_items.json) | 2 | 0 |
| [data/json/items/resources/alien.json](../../data/json/items/resources/alien.json) | 3 | 0 |
| [data/json/items/resources/chemicals.json](../../data/json/items/resources/chemicals.json) | 7 | 0 |
| [data/json/items/resources/fasteners.json](../../data/json/items/resources/fasteners.json) | 9 | 0 |
| [data/json/items/resources/glass.json](../../data/json/items/resources/glass.json) | 5 | 0 |
| [data/json/items/resources/home_improvement.json](../../data/json/items/resources/home_improvement.json) | 4 | 0 |
| [data/json/items/resources/metal.json](../../data/json/items/resources/metal.json) | 67 | 0 |
| [data/json/items/resources/misc.json](../../data/json/items/resources/misc.json) | 10 | 0 |
| [data/json/items/resources/plastic.json](../../data/json/items/resources/plastic.json) | 3 | 0 |
| [data/json/items/resources/stone.json](../../data/json/items/resources/stone.json) | 7 | 0 |
| [data/json/items/resources/tailoring.json](../../data/json/items/resources/tailoring.json) | 3 | 0 |
| [data/json/items/resources/wood.json](../../data/json/items/resources/wood.json) | 17 | 0 |
| [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) | 7 | 0 |
| [data/json/items/tool/container.json](../../data/json/items/tool/container.json) | 1 | 0 |
| [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) | 48 | 0 |
| [data/json/items/tool/deployable.json](../../data/json/items/tool/deployable.json) | 16 | 0 |
| [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) | 18 | 0 |
| [data/json/items/tool/entry_tools.json](../../data/json/items/tool/entry_tools.json) | 4 | 0 |
| [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) | 50 | 0 |
| [data/json/items/tool/firefighting.json](../../data/json/items/tool/firefighting.json) | 10 | 0 |
| [data/json/items/tool/fishing.json](../../data/json/items/tool/fishing.json) | 10 | 0 |
| [data/json/items/tool/handloading.json](../../data/json/items/tool/handloading.json) | 3 | 0 |
| [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) | 2 | 0 |
| [data/json/items/tool/knives.json](../../data/json/items/tool/knives.json) | 8 | 0 |
| [data/json/items/tool/landscaping.json](../../data/json/items/tool/landscaping.json) | 20 | 0 |
| [data/json/items/tool/lighting.json](../../data/json/items/tool/lighting.json) | 23 | 1 |
| [data/json/items/tool/masonry.json](../../data/json/items/tool/masonry.json) | 5 | 0 |
| [data/json/items/tool/med.json](../../data/json/items/tool/med.json) | 6 | 0 |
| [data/json/items/tool/metalworking.json](../../data/json/items/tool/metalworking.json) | 22 | 0 |
| [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) | 31 | 0 |
| [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) | 14 | 0 |
| [data/json/items/tool/pets.json](../../data/json/items/tool/pets.json) | 9 | 0 |
| [data/json/items/tool/radio_tools.json](../../data/json/items/tool/radio_tools.json) | 3 | 0 |
| [data/json/items/tool/raincatchers.json](../../data/json/items/tool/raincatchers.json) | 2 | 0 |
| [data/json/items/tool/science.json](../../data/json/items/tool/science.json) | 53 | 0 |
| [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) | 7 | 0 |
| [data/json/items/tool/smoking.json](../../data/json/items/tool/smoking.json) | 2 | 0 |
| [data/json/items/tool/stationery.json](../../data/json/items/tool/stationery.json) | 3 | 0 |
| [data/json/items/tool/stoneworking.json](../../data/json/items/tool/stoneworking.json) | 5 | 0 |
| [data/json/items/tool/tailoring.json](../../data/json/items/tool/tailoring.json) | 6 | 0 |
| [data/json/items/tool/toiletries.json](../../data/json/items/tool/toiletries.json) | 8 | 0 |
| [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) | 8 | 0 |
| [data/json/items/tool/woodworking.json](../../data/json/items/tool/woodworking.json) | 21 | 0 |
| [data/json/items/tool/workshop.json](../../data/json/items/tool/workshop.json) | 65 | 0 |
| [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) | 27 | 0 |
| [data/json/items/vehicle/animals.json](../../data/json/items/vehicle/animals.json) | 2 | 0 |
| [data/json/items/vehicle/armor.json](../../data/json/items/vehicle/armor.json) | 2 | 0 |
| [data/json/items/vehicle/battery.json](../../data/json/items/vehicle/battery.json) | 9 | 0 |
| [data/json/items/vehicle/boat.json](../../data/json/items/vehicle/boat.json) | 9 | 0 |
| [data/json/items/vehicle/cargo.json](../../data/json/items/vehicle/cargo.json) | 5 | 0 |
| [data/json/items/vehicle/controls.json](../../data/json/items/vehicle/controls.json) | 7 | 0 |
| [data/json/items/vehicle/farming.json](../../data/json/items/vehicle/farming.json) | 6 | 0 |
| [data/json/items/vehicle/frames.json](../../data/json/items/vehicle/frames.json) | 9 | 0 |
| [data/json/items/vehicle/fuel_storage.json](../../data/json/items/vehicle/fuel_storage.json) | 1 | 0 |
| [data/json/items/vehicle/lights.json](../../data/json/items/vehicle/lights.json) | 6 | 0 |
| [data/json/items/vehicle/manual.json](../../data/json/items/vehicle/manual.json) | 2 | 0 |
| [data/json/items/vehicle/mills.json](../../data/json/items/vehicle/mills.json) | 4 | 0 |
| [data/json/items/vehicle/motors.json](../../data/json/items/vehicle/motors.json) | 6 | 0 |
| [data/json/items/vehicle/noise.json](../../data/json/items/vehicle/noise.json) | 2 | 0 |
| [data/json/items/vehicle/plating.json](../../data/json/items/vehicle/plating.json) | 10 | 0 |
| [data/json/items/vehicle/rams.json](../../data/json/items/vehicle/rams.json) | 1 | 0 |
| [data/json/items/vehicle/seating.json](../../data/json/items/vehicle/seating.json) | 3 | 0 |
| [data/json/items/vehicle/solar.json](../../data/json/items/vehicle/solar.json) | 12 | 0 |
| [data/json/items/vehicle/tables.json](../../data/json/items/vehicle/tables.json) | 4 | 0 |
| [data/json/items/vehicle/utilities.json](../../data/json/items/vehicle/utilities.json) | 19 | 0 |
| [data/json/items/vehicle/wheel.json](../../data/json/items/vehicle/wheel.json) | 46 | 0 |
| [data/json/mapgen/crater.json](../../data/json/mapgen/crater.json) | 1 | 0 |
| [data/json/monster_special_attacks/monster_gun.json](../../data/json/monster_special_attacks/monster_gun.json) | 14 | 0 |
| [data/json/npcs/exodii/exodii_merchant_definitions.json](../../data/json/npcs/exodii/exodii_merchant_definitions.json) | 1 | 0 |
| [data/json/npcs/refugee_center/surface_refugees/NPC_Boris_Borichenko.json](../../data/json/npcs/refugee_center/surface_refugees/NPC_Boris_Borichenko.json) | 1 | 0 |
| [data/json/npcs/refugee_center/surface_refugees/NPC_Dana_Nunez.json](../../data/json/npcs/refugee_center/surface_refugees/NPC_Dana_Nunez.json) | 1 | 0 |
| [data/json/obsoletion/obsolete-0.G-items.json](../../data/json/obsoletion/obsolete-0.G-items.json) | 5 | 0 |
| [data/json/obsoletion/obsolete_items.json](../../data/json/obsoletion/obsolete_items.json) | 37 | 0 |

## 顶层字段：显式使用

| 字段 | 声明数 | 一个原版实例 |
|---|---:|---|
| `//` | 536 | `art_dagger` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `//0` | 6 | `charcoal` · [data/json/items/ammo.json](../../data/json/items/ammo.json) |
| `//1` | 29 | `duct_tape` · [data/json/items/ammo.json](../../data/json/items/ammo.json) |
| `//2` | 52 | `270win_fmj` · [data/json/items/ammo/270win.json](../../data/json/items/ammo/270win.json) |
| `//3` | 6 | `dragonskin` · [data/json/items/armor/ballistic_armor.json](../../data/json/items/armor/ballistic_armor.json) |
| `//4` | 1 | `cac2powder` · [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) |
| `//bashing` | 1 | `novel_samurai` · [data/json/items/book/misc.json](../../data/json/items/book/misc.json) |
| `//dual genre` | 2 | `book_fict_hard_sports_uni` · [data/json/items/book/misc_sports.json](../../data/json/items/book/misc_sports.json) |
| `//durability_modifier` | 6 | `dias` · [data/json/items/gunmod/mechanism.json](../../data/json/items/gunmod/mechanism.json) |
| `//genre` | 1 | `book_fict_soft_pulp_ddive` · [data/json/items/book/misc_pulp.json](../../data/json/items/book/misc_pulp.json) |
| `//isbn13` | 32 | `novel_samurai` · [data/json/items/book/misc.json](../../data/json/items/book/misc.json) |
| `//note` | 1 | `book_fict_hard_scifi_fifth` · [data/json/items/book/misc_scifi.json](../../data/json/items/book/misc_scifi.json) |
| `//range` | 3 | `ruger_1022` · [data/json/items/gun/22.json](../../data/json/items/gun/22.json) |
| `//volume` | 1 | `crossbow` · [data/json/items/ranged/crossbows.json](../../data/json/items/ranged/crossbows.json) |
| `abstract` | 68 | `20x66_abstract` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `acceptable_ammo` | 1 | `arredondo_chute` · [data/json/items/gunmod/loading_port.json](../../data/json/items/gunmod/loading_port.json) |
| `add_mod` | 32 | `retool_ar15_223rem` · [data/json/items/gunmod/conversions.json](../../data/json/items/gunmod/conversions.json) |
| `aim_speed_modifier` | 12 | `rail_laser_sight` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `ammo` | 435 | `power_armor_basic` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `ammo_data` | 1 | `water` · [data/json/items/comestibles/drink.json](../../data/json/items/comestibles/drink.json) |
| `ammo_effects` | 38 | `flamethrower_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `ammo_modifier` | 24 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `ammo_to_fire` | 2 | `flamethrower_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `ammo_type` | 679 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `armor` | 270 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `armor_data` | 22 | `magazine_belt` · [data/json/items/classes/magazine.json](../../data/json/items/classes/magazine.json) |
| `ascii_picture` | 245 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `barrel_length` | 281 | `sw_610` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `barrel_volume` | 69 | `rm120c` · [data/json/items/gun/20x66mm.json](../../data/json/items/gun/20x66mm.json) |
| `blacklist_mod` | 14 | `barrel_ported` · [data/json/items/gunmod/barrel.json](../../data/json/items/gunmod/barrel.json) |
| `blacklist_slot` | 1 | `rail_bayonet_lug` · [data/json/items/gunmod/mount.json](../../data/json/items/gunmod/mount.json) |
| `blackpowder_tolerance` | 85 | `sw_610` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `built_in_mods` | 42 | `hk_mp5_10_semi` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `calories` | 7 | `pineapple` · [data/json/items/comestibles/raw_fruit.json](../../data/json/items/comestibles/raw_fruit.json) |
| `capacity` | 45 | `light_minus_battery_cell` · [data/json/items/battery.json](../../data/json/items/battery.json) |
| `casing` | 67 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `category` | 1065 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `chapters` | 31 | `book_nonf_hard_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `charged_qualities` | 14 | `hair_dryer` · [data/json/items/generic/bathroom_house.json](../../data/json/items/generic/bathroom_house.json) |
| `charges` | 2 | `blood_acid_plant` · [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) |
| `charges_per_use` | 122 | `small_propane_tank` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `clip_size` | 132 | `sw_610` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `color` | 2450 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `comestible_type` | 7 | `blood_acid_plant` · [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) |
| `consume_chance` | 11 | `llink` · [data/json/items/gunmod/mechanism.json](../../data/json/items/gunmod/mechanism.json) |
| `consume_divisor` | 11 | `llink` · [data/json/items/gunmod/mechanism.json](../../data/json/items/gunmod/mechanism.json) |
| `container` | 82 | `gas_chloramine` · [data/json/items/ammo/chemical_spray.json](../../data/json/items/ammo/chemical_spray.json) |
| `cooling_value` | 5 | `emp_gun` · [data/json/items/gun/ups.json](../../data/json/items/gun/ups.json) |
| `copy-from` | 1996 | `art_helm` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `count` | 266 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `countdown_action` | 24 | `dynamite_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `countdown_interval` | 2 | `grenade_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `critical_multiplier` | 5 | `arrow_field_point_fletched` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `damage` | 174 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage_modifier` | 13 | `robofac_gun_smg` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `default_ammo` | 2 | `belt223` · [data/json/items/magazine/223.json](../../data/json/items/magazine/223.json) |
| `default_mods` | 39 | `rm228` · [data/json/items/gun/20x66mm.json](../../data/json/items/gun/20x66mm.json) |
| `delete` | 261 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `description` | 3831 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `diameter` | 22 | `yoke_harness` · [data/json/items/vehicle/animals.json](../../data/json/items/vehicle/animals.json) |
| `difficulty` | 121 | `bio_adrenaline` · [data/json/items/bionics.json](../../data/json/items/bionics.json) |
| `dispersion` | 423 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `dispersion_modifier` | 38 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `drop` | 4 | `20x66_flare` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `drop_action` | 1 | `blood_acid_plant` · [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) |
| `durability` | 315 | `sw_610` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `effects` | 172 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `emits` | 3 | `throw_extinguisher_act` · [data/json/items/tool/firefighting.json](../../data/json/items/tool/firefighting.json) |
| `energy_drain` | 17 | `hk_g80` · [data/json/items/gun/12mm.json](../../data/json/items/gun/12mm.json) |
| `energy_drain_multiplier` | 4 | `upstest` · [data/json/items/gunmod/barrel.json](../../data/json/items/gunmod/barrel.json) |
| `environmental_protection` | 106 | `lsurvivor_jumpsuit` · [data/json/items/armor/bespoke_armor/custom_bodysuits.json](../../data/json/items/armor/bespoke_armor/custom_bodysuits.json) |
| `environmental_protection_with_filter` | 4 | `scuba_tank` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `expand_snippets` | 1 | `nice_mug` · [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) |
| `explode_in_fire` | 27 | `sling-ready_small_homemade_grenade` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `explosion` | 26 | `sling-ready_small_homemade_grenade` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `extend` | 633 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `faults` | 74 | `bionic_general` · [data/json/items/bionics.json](../../data/json/items/bionics.json) |
| `field_of_view` | 15 | `rail_laser_sight` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `flags` | 1751 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `fuel_efficiency` | 2 | `power_armor_generator` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `fun` | 79 | `book_nonf_hard_dodge_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `gun_data` | 15 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gunmod_data` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `handling` | 5 | `gun_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `handling_modifier` | 53 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `heat_per_shot` | 5 | `emp_gun` · [data/json/items/gun/ups.json](../../data/json/items/gun/ups.json) |
| `id` | 4112 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `initial_charges` | 16 | `power_cord` · [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) |
| `install_time` | 129 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `insulation` | 4 | `minifridge` · [data/json/items/vehicle/utilities.json](../../data/json/items/vehicle/utilities.json) |
| `integral_longest_side` | 52 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `integral_volume` | 86 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `integral_weight` | 60 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `intelligence` | 89 | `book_nonf_hard_dodge_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `is_upgrade` | 1 | `bionic_general` · [data/json/items/bionics.json](../../data/json/items/bionics.json) |
| `linkage` | 4 | `belt223` · [data/json/items/magazine/223.json](../../data/json/items/magazine/223.json) |
| `location` | 130 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `longest_side` | 1220 | `art_rod` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `looks_like` | 1405 | `matchhead_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `loudness` | 90 | `410shot_slug` · [data/json/items/ammo/410shot.json](../../data/json/items/ammo/410shot.json) |
| `loudness_modifier` | 23 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `magazine_adaptor` | 16 | `retool_ar15_223rem` · [data/json/items/gunmod/conversions.json](../../data/json/items/gunmod/conversions.json) |
| `magazines` | 1 | `rm88_battle_rifle` · [data/json/items/gun/8x40mm.json](../../data/json/items/gun/8x40mm.json) |
| `material` | 2550 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `material_thickness` | 188 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `max_charges` | 17 | `power_cord` · [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) |
| `max_level` | 63 | `textbook_business` · [data/json/items/book/barter.json](../../data/json/items/book/barter.json) |
| `max_pet_vol` | 1 | `kevlar_harness` · [data/json/items/armor/pets_dog_armor.json](../../data/json/items/armor/pets_dog_armor.json) |
| `melee_damage` | 1757 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `milling` | 3 | `large_bone` · [data/json/items/comestibles/carnivore.json](../../data/json/items/comestibles/carnivore.json) |
| `min_cycle_recoil` | 146 | `glock_29` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `min_pet_vol` | 3 | `kevlar_harness` · [data/json/items/armor/pets_dog_armor.json](../../data/json/items/armor/pets_dog_armor.json) |
| `min_skills` | 112 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `min_strength` | 17 | `selfbow` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `mod_targets` | 154 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `mode_modifier` | 18 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `modes` | 100 | `launcher_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `name` | 4180 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `non_functional` | 1 | `helmet_riding` · [data/json/items/armor/helmets.json](../../data/json/items/armor/helmets.json) |
| `overheat_threshold` | 5 | `emp_gun` · [data/json/items/gun/ups.json](../../data/json/items/gun/ups.json) |
| `overwrite_min_cycle_recoil` | 10 | `robofac_gun_ar` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `pet_bodytype` | 1 | `kevlar_harness` · [data/json/items/armor/pets_dog_armor.json](../../data/json/items/armor/pets_dog_armor.json) |
| `phase` | 50 | `gas_chloramine` · [data/json/items/ammo/chemical_spray.json](../../data/json/items/ammo/chemical_spray.json) |
| `pocket_data` | 992 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_mods` | 24 | `retool_ar15_223rem` · [data/json/items/gunmod/conversions.json](../../data/json/items/gunmod/conversions.json) |
| `power_armor` | 8 | `power_armor_basic` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `power_draw` | 38 | `power_armor_basic_on` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `price` | 2691 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `price_postapoc` | 2635 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `proficiencies` | 23 | `adv_chemistry` · [data/json/items/book/chemistry.json](../../data/json/items/book/chemistry.json) |
| `projectile_count` | 19 | `20x66_shot` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `properties` | 2 | `chicken_cage` · [data/json/items/tool/pets.json](../../data/json/items/tool/pets.json) |
| `proportional` | 737 | `10mmP` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `qualities` | 413 | `art_dagger` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `quench` | 7 | `water` · [data/json/items/comestibles/drink.json](../../data/json/items/comestibles/drink.json) |
| `range` | 248 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `range_modifier` | 6 | `robofac_gun_smg` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `range_multiplier` | 3 | `beam_scatterer` · [data/json/items/gunmod/laser_gunmods.json](../../data/json/items/gunmod/laser_gunmods.json) |
| `ranged_damage` | 121 | `gun_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `recoil` | 91 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relative` | 261 | `10mm_jhp` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relic_data` | 12 | `integrated_claws` · [data/json/items/armor/integrated.json](../../data/json/items/armor/integrated.json) |
| `reload` | 88 | `flamethrower_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `reload_noise` | 5 | `flamethrower_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `reload_noise_volume` | 99 | `gun_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `reload_time` | 77 | `robofac60` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `repairs_like` | 2 | `helmet_army_outdated` · [data/json/items/armor/helmets.json](../../data/json/items/armor/helmets.json) |
| `repairs_with` | 31 | `sabaton_metal_sheets` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `replace_materials` | 236 | `mc_sabaton` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `required_level` | 59 | `textbook_business` · [data/json/items/book/barter.json](../../data/json/items/book/barter.json) |
| `revert_msg` | 1 | `lightstrip` · [data/json/items/tool/lighting.json](../../data/json/items/tool/lighting.json) |
| `revert_to` | 52 | `power_armor_basic_on` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `sealed` | 17 | `gas_chloramine` · [data/json/items/ammo/chemical_spray.json](../../data/json/items/ammo/chemical_spray.json) |
| `shot_damage` | 19 | `20x66_shot` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `shot_spread` | 18 | `20x66_shot` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `shot_spread_multiplier_modifier` | 2 | `robofac_gun_shotgun` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `show_stats` | 5 | `barb_paralysis` · [data/json/items/ammo/barb.json](../../data/json/items/ammo/barb.json) |
| `sided` | 18 | `quiver` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `sight_dispersion` | 43 | `pistol_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `skill` | 201 | `book_nonf_hard_cook_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `smoking_result` | 4 | `pineapple` · [data/json/items/comestibles/raw_fruit.json](../../data/json/items/comestibles/raw_fruit.json) |
| `snippet_category` | 14 | `philosophy_book` · [data/json/items/book/misc_philosophy.json](../../data/json/items/book/misc_philosophy.json) |
| `solar_efficiency` | 1 | `solarpack_on` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `spoils_in` | 7 | `pineapple` · [data/json/items/comestibles/raw_fruit.json](../../data/json/items/comestibles/raw_fruit.json) |
| `stack_size` | 121 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `sub` | 7 | `survivor_mess_kit` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `symbol` | 2379 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `techniques` | 283 | `art_dagger` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `thrown_damage` | 14 | `javelin` · [data/json/items/melee/spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json) |
| `tick_action` | 35 | `combatsaw_on` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `time` | 128 | `book_nonf_hard_dodge_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `to_hit` | 1488 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `turns_per_charge` | 13 | `combatsaw_on` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `type` | 4180 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action` | 511 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `valid_mod_locations` | 255 | `launcher_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `valid_mods` | 9 | `survivor_jumpsuit` · [data/json/items/armor/bespoke_armor/custom_bodysuits.json](../../data/json/items/armor/bespoke_armor/custom_bodysuits.json) |
| `variant_type` | 161 | `heels` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `variants` | 174 | `moisturizer` · [data/json/items/ammo.json](../../data/json/items/ammo.json) |
| `vitamins` | 8 | `large_bone` · [data/json/items/comestibles/carnivore.json](../../data/json/items/comestibles/carnivore.json) |
| `volume` | 2626 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `warmth` | 180 | `xlkevlar` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `weapon_category` | 304 | `art_dagger` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `weight` | 2780 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `weight_capacity_bonus` | 2 | `utility_exoskeleton_on` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `weight_multiplier` | 2 | `light_grip` · [data/json/items/gunmod/grip.json](../../data/json/items/gunmod/grip.json) |
| `width` | 21 | `yoke_harness` · [data/json/items/vehicle/animals.json](../../data/json/items/vehicle/animals.json) |

## 战斗及关联对象的嵌套路径

动态ID键（如伤害类型、flag或EOC变量）可能是数据键，不是独立schema字段；具体语义回到加载器核查。数组写作`[]`。

| 路径 | 声明数 | 一个原版实例 |
|---|---:|---|
| `ammo_data.ammo_type` | 1 | `water` · [data/json/items/comestibles/drink.json](../../data/json/items/comestibles/drink.json) |
| `damage.amount` | 147 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage.armor_penetration` | 105 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage.barrels` | 31 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage.barrels[].amount` | 31 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage.barrels[].barrel_length` | 31 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage.constant_damage_multiplier` | 22 | `arrow_fire_hardened_fletched` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `damage.damage_type` | 174 | `10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `damage_modifier.amount` | 13 | `robofac_gun_smg` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `damage_modifier.damage_type` | 13 | `robofac_gun_smg` · [data/json/items/gun/robofac_gun.json](../../data/json/items/gun/robofac_gun.json) |
| `delete.ammo_type` | 1 | `blood_acid_plant` · [data/json/items/chemicals_and_resources.json](../../data/json/items/chemicals_and_resources.json) |
| `delete.effects` | 181 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `delete.flags` | 253 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `delete.qualities` | 2 | `kettle` · [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) |
| `extend.effects` | 240 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `extend.flags` | 392 | `20x66_exp` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `extend.price` | 1 | `estoc_fake` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `extend.price_postapoc` | 1 | `estoc_fake` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `extend.qualities` | 4 | `pan` · [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) |
| `extend.techniques` | 1 | `survivor_machete` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `gun_data.ammo` | 15 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.barrel_length` | 13 | `combination_gun_shotgun` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gun_data.blackpowder_tolerance` | 3 | `m203` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gun_data.clip_size` | 14 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.dispersion` | 15 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.durability` | 15 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.min_cycle_recoil` | 2 | `ts12_aux_shotgun` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gun_data.range` | 4 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.ranged_damage` | 6 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.ranged_damage.amount` | 6 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.ranged_damage.damage_type` | 6 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gun_data.reload` | 6 | `ksg_aux_shotgun` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gun_data.skill` | 15 | `gun_crossbow` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `gunmod_data.blacklist_mod` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gunmod_data.install_time` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gunmod_data.location` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gunmod_data.mod_targets` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `gunmod_data.mode_modifier` | 7 | `makeshift_bayonet` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `material[].portion` | 67 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `material[].type` | 67 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `melee_damage.bash` | 1680 | `art_sphere` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `melee_damage.cut` | 248 | `art_urchin` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `melee_damage.stab` | 134 | `art_dagger` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `pocket_data[].//` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].//1` | 1 | `candlestick` · [data/json/items/generic.json](../../data/json/items/generic.json) |
| `pocket_data[].//2` | 1 | `ceramic_cup` · [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) |
| `pocket_data[].ablative` | 18 | `boots_h20survivor` · [data/json/items/armor/bespoke_armor/custom_boots.json](../../data/json/items/armor/bespoke_armor/custom_boots.json) |
| `pocket_data[].activity_noise` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].activity_noise.chance` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].activity_noise.volume` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].airtight` | 18 | `small_propane_tank` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].allowed_speedloaders` | 33 | `sw_610` · [data/json/items/gun/10mm.json](../../data/json/items/gun/10mm.json) |
| `pocket_data[].ammo_restriction` | 569 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.10mm` | 13 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.123ln` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.12mm` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.20x66mm` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.22` | 18 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.223` | 44 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.270win` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.273x110` | 2 | `brogyeki` · [data/json/items/gun/exodii.json](../../data/json/items/gun/exodii.json) |
| `pocket_data[].ammo_restriction.273x44` | 3 | `brogyeki` · [data/json/items/gun/exodii.json](../../data/json/items/gun/exodii.json) |
| `pocket_data[].ammo_restriction.273x44RG` | 1 | `brogyeki` · [data/json/items/gun/exodii.json](../../data/json/items/gun/exodii.json) |
| `pocket_data[].ammo_restriction.300` | 7 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.3006` | 10 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.300blk` | 23 | `stanag10` · [data/json/items/magazine/223.json](../../data/json/items/magazine/223.json) |
| `pocket_data[].ammo_restriction.303` | 3 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.308` | 26 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.30carbine` | 2 | `m1carbinebigmag` · [data/json/items/magazine/30carbine.json](../../data/json/items/magazine/30carbine.json) |
| `pocket_data[].ammo_restriction.32` | 7 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.338lapua` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.357mag` | 7 | `cop_38` · [data/json/items/gun/38.json](../../data/json/items/gun/38.json) |
| `pocket_data[].ammo_restriction.357sig` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.36paper` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.38` | 11 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.380` | 9 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.38super` | 2 | `af2011a1mag` · [data/json/items/magazine/38super.json](../../data/json/items/magazine/38super.json) |
| `pocket_data[].ammo_restriction.40` | 16 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.40x46mm` | 13 | `launcher_simple` · [data/json/items/gun/40x46mm.json](../../data/json/items/gun/40x46mm.json) |
| `pocket_data[].ammo_restriction.40x53mm` | 1 | `belt40mm` · [data/json/items/magazine/40mm.json](../../data/json/items/magazine/40mm.json) |
| `pocket_data[].ammo_restriction.410shot` | 9 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.44` | 7 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.44paper` | 3 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.45` | 21 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.450` | 3 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.454` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.4570` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.458wm` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.45colt` | 8 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.46` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.460` | 3 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.50` | 7 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.500` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.50ae` | 1 | `deaglemag_50` · [data/json/items/magazine/50ae.json](../../data/json/items/magazine/50ae.json) |
| `pocket_data[].ammo_restriction.50beowulf` | 6 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.545x39` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.57` | 6 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.5x50` | 2 | `5x50_100_mag` · [data/json/obsoletion/obsolete_items.json](../../data/json/obsoletion/obsolete_items.json) |
| `pocket_data[].ammo_restriction.66mm` | 1 | `LAW` · [data/json/items/ranged/launchers.json](../../data/json/items/ranged/launchers.json) |
| `pocket_data[].ammo_restriction.762` | 16 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.762R` | 6 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.762x25` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.77mm_arisaka` | 3 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.84x246mm` | 1 | `m3_carlgustav` · [data/json/items/gun/84x246mm.json](../../data/json/items/gun/84x246mm.json) |
| `pocket_data[].ammo_restriction.8x40mm` | 7 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.9mm` | 89 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.9x18` | 4 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.BB` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.RPG-7` | 1 | `RPG` · [data/json/obsoletion/obsolete_items.json](../../data/json/obsoletion/obsolete_items.json) |
| `pocket_data[].ammo_restriction.airgun_pellet` | 1 | `varmint_airgun` · [data/json/items/ranged/pneumatic.json](../../data/json/items/ranged/pneumatic.json) |
| `pocket_data[].ammo_restriction.ampoule` | 1 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.arrow` | 17 | `quiver` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.atgm` | 1 | `atgm_launcher` · [data/json/items/gun/atgm.json](../../data/json/items/gun/atgm.json) |
| `pocket_data[].ammo_restriction.barb` | 1 | `barb_launcher` · [data/json/monster_special_attacks/monster_gun.json](../../data/json/monster_special_attacks/monster_gun.json) |
| `pocket_data[].ammo_restriction.battery` | 31 | `light_minus_battery_cell` · [data/json/items/battery.json](../../data/json/items/battery.json) |
| `pocket_data[].ammo_restriction.blunderbuss` | 1 | `blunderbuss` · [data/json/items/gun/blunderbuss.json](../../data/json/items/gun/blunderbuss.json) |
| `pocket_data[].ammo_restriction.bolt` | 13 | `quiver` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.butane` | 1 | `butane_tank` · [data/json/items/tool/science.json](../../data/json/items/tool/science.json) |
| `pocket_data[].ammo_restriction.cannon` | 1 | `cannon_3in_ordnance` · [data/json/items/gun/cannon.json](../../data/json/items/gun/cannon.json) |
| `pocket_data[].ammo_restriction.charcoal` | 8 | `fake_forge` · [data/json/items/basecamp.json](../../data/json/items/basecamp.json) |
| `pocket_data[].ammo_restriction.chemical_spray` | 1 | `pressurized_tank_chem` · [data/json/items/magazine/chemical_spray.json](../../data/json/items/magazine/chemical_spray.json) |
| `pocket_data[].ammo_restriction.coal` | 5 | `fake_forge` · [data/json/items/basecamp.json](../../data/json/items/basecamp.json) |
| `pocket_data[].ammo_restriction.conc_alcohol` | 2 | `popcan_stove` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `pocket_data[].ammo_restriction.crude_lamp_oil` | 1 | `oil_lamp_clay` · [data/json/items/tool/lighting.json](../../data/json/items/tool/lighting.json) |
| `pocket_data[].ammo_restriction.diesel` | 1 | `power_armor_generator` · [data/json/items/armor/power_armor.json](../../data/json/items/armor/power_armor.json) |
| `pocket_data[].ammo_restriction.esbit` | 1 | `esbit_stove` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `pocket_data[].ammo_restriction.extinguishing_agent` | 2 | `extinguisher` · [data/json/items/tool/firefighting.json](../../data/json/items/tool/firefighting.json) |
| `pocket_data[].ammo_restriction.fishspear` | 4 | `airspeargun` · [data/json/items/ranged/spearguns.json](../../data/json/items/ranged/spearguns.json) |
| `pocket_data[].ammo_restriction.flammable` | 3 | `pressurized_tank` · [data/json/items/magazine/liquid.json](../../data/json/items/magazine/liquid.json) |
| `pocket_data[].ammo_restriction.flintlock` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.gasfilter_m` | 1 | `gasfilter_med` · [data/json/items/magazine/filter.json](../../data/json/items/magazine/filter.json) |
| `pocket_data[].ammo_restriction.gasfilter_s` | 1 | `gasfilter_sm` · [data/json/items/magazine/filter.json](../../data/json/items/magazine/filter.json) |
| `pocket_data[].ammo_restriction.gasoline` | 10 | `louverture` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `pocket_data[].ammo_restriction.homebrew_rocket` | 1 | `surv_rocket_launcher` · [data/json/items/ranged/launchers.json](../../data/json/items/ranged/launchers.json) |
| `pocket_data[].ammo_restriction.hydrogen` | 1 | `hydrogen_tank` · [data/json/items/tool/science.json](../../data/json/items/tool/science.json) |
| `pocket_data[].ammo_restriction.lamp_oil` | 5 | `oil_cooker` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `pocket_data[].ammo_restriction.m235` | 1 | `m74_clip` · [data/json/items/magazine/66mm.json](../../data/json/items/magazine/66mm.json) |
| `pocket_data[].ammo_restriction.methanol_fuelcell` | 4 | `5l_methanol_tank` · [data/json/items/magazine/methanol_fuelcell.json](../../data/json/items/magazine/methanol_fuelcell.json) |
| `pocket_data[].ammo_restriction.nail` | 2 | `nailgun` · [data/json/items/gun/nail.json](../../data/json/items/gun/nail.json) |
| `pocket_data[].ammo_restriction.nitrogen` | 1 | `nitrogen_tank` · [data/json/items/tool/science.json](../../data/json/items/tool/science.json) |
| `pocket_data[].ammo_restriction.nitrox` | 4 | `scuba_tank` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `pocket_data[].ammo_restriction.oxygen` | 3 | `smoxygen_tank` · [data/json/items/tool/med.json](../../data/json/items/tool/med.json) |
| `pocket_data[].ammo_restriction.paintball` | 2 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.paper` | 1 | `book_binder` · [data/json/items/generic.json](../../data/json/items/generic.json) |
| `pocket_data[].ammo_restriction.pebble` | 5 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.plasma` | 2 | `plasma_gun` · [data/json/items/ranged/energy.json](../../data/json/items/ranged/energy.json) |
| `pocket_data[].ammo_restriction.plutonium` | 1 | `minireactor` · [data/json/items/vehicle/utilities.json](../../data/json/items/vehicle/utilities.json) |
| `pocket_data[].ammo_restriction.powder_blank` | 1 | `pulverizer` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `pocket_data[].ammo_restriction.propane` | 5 | `small_propane_tank` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].ammo_restriction.rebreather_filter` | 2 | `rebreather_cartridge_air` · [data/json/items/magazine/filter.json](../../data/json/items/magazine/filter.json) |
| `pocket_data[].ammo_restriction.rebreather_o2_regenerator` | 1 | `rebreather_cartridge_regen` · [data/json/items/magazine/filter.json](../../data/json/items/magazine/filter.json) |
| `pocket_data[].ammo_restriction.rock` | 2 | `staff_sling` · [data/json/items/ranged/slings.json](../../data/json/items/ranged/slings.json) |
| `pocket_data[].ammo_restriction.shot` | 42 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.shotpaper` | 1 | `lemat_revolver_shotgun` · [data/json/items/gunmod/underbarrel.json](../../data/json/items/gunmod/underbarrel.json) |
| `pocket_data[].ammo_restriction.signal_flare` | 1 | `flaregun` · [data/json/items/gun/signal_flare.json](../../data/json/items/gun/signal_flare.json) |
| `pocket_data[].ammo_restriction.soap` | 1 | `survivor_shavingkit` · [data/json/items/tool/toiletries.json](../../data/json/items/tool/toiletries.json) |
| `pocket_data[].ammo_restriction.stimpack_ammo` | 1 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].ammo_restriction.strange_arrow` | 1 | `greatbow_meteor` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `pocket_data[].ammo_restriction.water` | 1 | `watercannon` · [data/json/items/ranged/launchers.json](../../data/json/items/ranged/launchers.json) |
| `pocket_data[].ammo_restriction.weldgas` | 2 | `tinyweldtank` · [data/json/items/magazine/weldgas.json](../../data/json/items/magazine/weldgas.json) |
| `pocket_data[].default_magazine` | 72 | `toothbrush_electric` · [data/json/items/generic/bathroom_house.json](../../data/json/items/generic/bathroom_house.json) |
| `pocket_data[].description` | 34 | `lsurvivor_jumpsuit` · [data/json/items/armor/bespoke_armor/custom_bodysuits.json](../../data/json/items/armor/bespoke_armor/custom_bodysuits.json) |
| `pocket_data[].extra_encumbrance` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].flag_restriction` | 106 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].holster` | 17 | `quiver_takedown_bow` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].inherits_flags` | 5 | `hat_hard` · [data/json/items/armor/hats.json](../../data/json/items/armor/hats.json) |
| `pocket_data[].item_restriction` | 195 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].magazine_well` | 99 | `baldric` · [data/json/items/armor/sheath.json](../../data/json/items/armor/sheath.json) |
| `pocket_data[].max_contains_volume` | 167 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].max_contains_weight` | 167 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].max_item_length` | 53 | `quiver_takedown_bow` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].max_item_volume` | 13 | `2lcanteen` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].min_item_length` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].min_item_volume` | 1 | `quiver_takedown_bow` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].moves` | 82 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].open_container` | 39 | `can_drink` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].pocket_type` | 937 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].rigid` | 647 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].ripoff` | 1 | `boxpack` · [data/json/items/armor/storage.json](../../data/json/items/armor/storage.json) |
| `pocket_data[].sealed_data` | 4 | `can_drink` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].sealed_data.spoil_multiplier` | 4 | `can_drink` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `pocket_data[].transparent` | 10 | `belt_loop_small` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].volume_encumber_modifier` | 29 | `ammo_pouch` · [data/json/items/armor/ammo_pouch.json](../../data/json/items/armor/ammo_pouch.json) |
| `pocket_data[].watertight` | 138 | `autoclave` · [data/json/items/appliances.json](../../data/json/items/appliances.json) |
| `pocket_data[].weight_multiplier` | 1 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `proportional.damage` | 224 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.damage.amount` | 224 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.damage.armor_penetration` | 82 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.damage.damage_type` | 224 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.dispersion` | 228 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.encumbrance` | 4 | `boots_acidchitin` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `proportional.longest_side` | 2 | `ground_solar_panel` · [data/json/items/vehicle/solar.json](../../data/json/items/vehicle/solar.json) |
| `proportional.loudness` | 1 | `shot_dragon` · [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) |
| `proportional.loudness_modifier` | 1 | `riv_suppressor` · [data/json/items/gunmod/muzzle.json](../../data/json/items/gunmod/muzzle.json) |
| `proportional.melee_damage` | 45 | `carbine_flintlock` · [data/json/items/gun/flintlock.json](../../data/json/items/gun/flintlock.json) |
| `proportional.melee_damage.bash` | 43 | `carbine_flintlock` · [data/json/items/gun/flintlock.json](../../data/json/items/gun/flintlock.json) |
| `proportional.melee_damage.cut` | 27 | `battleaxe_fake` · [data/json/items/melee/bludgeons.json](../../data/json/items/melee/bludgeons.json) |
| `proportional.melee_damage.stab` | 12 | `lucern_hammerfake` · [data/json/items/melee/bludgeons.json](../../data/json/items/melee/bludgeons.json) |
| `proportional.price` | 630 | `bp_10mm_fmj` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.price_postapoc` | 139 | `bp_303` · [data/json/items/ammo/303.json](../../data/json/items/ammo/303.json) |
| `proportional.quench` | 1 | `water_mineral` · [data/json/items/comestibles/drink.json](../../data/json/items/comestibles/drink.json) |
| `proportional.range` | 6 | `22_cb` · [data/json/items/ammo/22.json](../../data/json/items/ammo/22.json) |
| `proportional.recoil` | 101 | `10mmP` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `proportional.reload` | 5 | `pistol_revolver` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `proportional.shot_spread` | 3 | `40x46mm_hornets_nest_410_scrap` · [data/json/items/ammo/40x46mm.json](../../data/json/items/ammo/40x46mm.json) |
| `proportional.sight_dispersion` | 1 | `offset_sights` · [data/json/items/gunmod/rail.json](../../data/json/items/gunmod/rail.json) |
| `proportional.volume` | 345 | `xs_armguard_scrap` · [data/json/items/armor/arms_armor.json](../../data/json/items/armor/arms_armor.json) |
| `proportional.warmth` | 4 | `boots_acidchitin` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `proportional.weight` | 349 | `xs_armguard_scrap` · [data/json/items/armor/arms_armor.json](../../data/json/items/armor/arms_armor.json) |
| `ranged_damage.amount` | 119 | `gun_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `ranged_damage.armor_penetration` | 9 | `bio_emp_gun` · [data/json/items/gun/bio.json](../../data/json/items/gun/bio.json) |
| `ranged_damage.damage_type` | 119 | `gun_base` · [data/json/items/classes/gun.json](../../data/json/items/classes/gun.json) |
| `ranged_damage[].amount` | 2 | `acid_spray` · [data/json/monster_special_attacks/monster_gun.json](../../data/json/monster_special_attacks/monster_gun.json) |
| `ranged_damage[].armor_multiplier` | 1 | `acid_spray` · [data/json/monster_special_attacks/monster_gun.json](../../data/json/monster_special_attacks/monster_gun.json) |
| `ranged_damage[].damage_type` | 2 | `acid_spray` · [data/json/monster_special_attacks/monster_gun.json](../../data/json/monster_special_attacks/monster_gun.json) |
| `relative.barrel_volume` | 1 | `obrez` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `relative.chapters` | 46 | `book_fict_soft_pulp_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `relative.damage` | 60 | `10mm_jhp` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relative.damage.amount` | 60 | `10mm_jhp` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relative.damage.armor_penetration` | 57 | `10mm_jhp` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relative.damage.damage_type` | 60 | `10mm_jhp` · [data/json/items/ammo/10mm.json](../../data/json/items/ammo/10mm.json) |
| `relative.dispersion` | 32 | `556` · [data/json/items/ammo/223.json](../../data/json/items/ammo/223.json) |
| `relative.durability` | 1 | `m1911-460` · [data/json/items/gun/460.json](../../data/json/items/gun/460.json) |
| `relative.fun` | 36 | `book_fict_soft_pulp_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `relative.intelligence` | 41 | `book_fict_soft_pulp_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `relative.melee_damage` | 93 | `boots_acidchitin` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `relative.melee_damage.bash` | 7 | `boots_acidchitin` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `relative.melee_damage.cut` | 68 | `survivor_machete` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `relative.melee_damage.stab` | 19 | `lc_knife_rambo` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `relative.price` | 13 | `57mm_ss` · [data/json/items/ammo/57.json](../../data/json/items/ammo/57.json) |
| `relative.price_postapoc` | 16 | `book_fict_soft_pulp_tpl` · [data/json/items/book/abstract.json](../../data/json/items/book/abstract.json) |
| `relative.qualities` | 73 | `pan` · [data/json/items/generic/dining_kitchen.json](../../data/json/items/generic/dining_kitchen.json) |
| `relative.range` | 15 | `450_penetrator` · [data/json/items/ammo/450bushmaster.json](../../data/json/items/ammo/450bushmaster.json) |
| `relative.ranged_damage` | 4 | `obrez` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `relative.ranged_damage.amount` | 4 | `obrez` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `relative.ranged_damage.damage_type` | 4 | `obrez` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `relative.recoil` | 8 | `45_super` · [data/json/items/ammo/45.json](../../data/json/items/ammo/45.json) |
| `relative.shot_damage` | 1 | `shot_flechette` · [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) |
| `relative.shot_damage.amount` | 1 | `shot_flechette` · [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) |
| `relative.shot_damage.damage_type` | 1 | `shot_flechette` · [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) |
| `relative.shot_spread` | 1 | `shot_flechette` · [data/json/items/ammo/shot.json](../../data/json/items/ammo/shot.json) |
| `relative.time` | 1 | `book_nonf_hard_dodge_tlwd` · [data/json/items/book/dodge.json](../../data/json/items/book/dodge.json) |
| `relative.volume` | 6 | `book_newage_horoscopes` · [data/json/items/book/misc_newage.json](../../data/json/items/book/misc_newage.json) |
| `relative.weight` | 15 | `paperback_romance_circuses` · [data/json/items/book/misc.json](../../data/json/items/book/misc.json) |
| `replace_materials.lc_steel` | 102 | `mc_sabaton` · [data/json/items/armor/boots.json](../../data/json/items/armor/boots.json) |
| `replace_materials.lc_steel_chain` | 44 | `mc_demi_gaunt` · [data/json/items/armor/gloves.json](../../data/json/items/armor/gloves.json) |
| `replace_materials.leather` | 65 | `lc_cavalry_sabre` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `replace_materials.mc_steel` | 122 | `knife_rambo` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `replace_materials.steel` | 12 | `survivor_machete_qt` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `replace_materials.wood` | 3 | `survivor_machete_qt` · [data/json/items/melee/swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json) |
| `shot_damage.amount` | 19 | `20x66_shot` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `shot_damage.armor_penetration` | 1 | `blun_flechette` · [data/json/items/handloaded_bullets.json](../../data/json/items/handloaded_bullets.json) |
| `shot_damage.damage_type` | 19 | `20x66_shot` · [data/json/items/ammo/20x66mm.json](../../data/json/items/ammo/20x66mm.json) |
| `thrown_damage[].amount` | 14 | `javelin` · [data/json/items/melee/spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json) |
| `thrown_damage[].damage_type` | 14 | `javelin` · [data/json/items/melee/spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json) |
| `tick_action.description_frequency` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.fun` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.fun_bonus` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.npc_descriptions` | 4 | `acoustic_guitar` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.player_descriptions` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.speed_penalty` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.type` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action.volume` | 14 | `banjo` · [data/json/items/tool/musical_instruments.json](../../data/json/items/tool/musical_instruments.json) |
| `tick_action[].sound_id` | 1 | `firecracker_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `tick_action[].sound_message` | 1 | `firecracker_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `tick_action[].sound_variant` | 1 | `firecracker_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `tick_action[].sound_volume` | 1 | `firecracker_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `tick_action[].type` | 1 | `firecracker_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `to_hit.balance` | 338 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `to_hit.grip` | 338 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `to_hit.length` | 338 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `to_hit.surface` | 338 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.//` | 17 | `aquarium_medium_drying` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `use_action.active` | 44 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.allow_under_player` | 3 | `cot` · [data/json/items/tool/deployable.json](../../data/json/items/tool/deployable.json) |
| `use_action.allow_underwater` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.ammo_scale` | 17 | `armor_nomad_plate_on` · [data/json/items/armor/suits_protection.json](../../data/json/items/armor/suits_protection.json) |
| `use_action.base` | 2 | `folding_solar_panel` · [data/json/items/vehicle/solar.json](../../data/json/items/vehicle/solar.json) |
| `use_action.broken_type` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.bury` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.bury.done_message` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.bury.moves` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.bury.practice` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.bury.trap` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.bury_question` | 2 | `beartrap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.cable_length` | 9 | `dehydrator` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `use_action.can_extend` | 3 | `jumper_cable` · [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) |
| `use_action.charge_rate` | 9 | `dehydrator` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `use_action.container` | 4 | `eggs_ferment` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `use_action.description` | 1 | `nre_recorder` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action.description_frequency` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.difficulty` | 36 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.done_message` | 14 | `glass_shard` · [data/json/items/resources/glass.json](../../data/json/items/resources/glass.json) |
| `use_action.door_closed` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.door_opened` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.effect_on_conditions` | 2 | `bot_yrax_trifacet` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.efficiency` | 2 | `hd_tow_cable` · [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) |
| `use_action.floor` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.floor_center` | 2 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.friendly_msg` | 31 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.fun` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.fun_bonus` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.furn_type` | 17 | `household_water_heater` · [data/json/items/generic.json](../../data/json/items/generic.json) |
| `use_action.holster_msg` | 5 | `baldric` · [data/json/items/armor/sheath.json](../../data/json/items/armor/sheath.json) |
| `use_action.holster_prompt` | 5 | `baldric` · [data/json/items/armor/sheath.json](../../data/json/items/armor/sheath.json) |
| `use_action.hostile_msg` | 31 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.level` | 1 | `louverture` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `use_action.max_weight` | 2 | `livestock_scale` · [data/json/items/tool/pets.json](../../data/json/items/tool/pets.json) |
| `use_action.menu_text` | 174 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.message` | 21 | `dynamite_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `use_action.monster_id` | 36 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.moves` | 86 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.moves_slow` | 1 | `binoculars` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `use_action.msg` | 202 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.mundane` | 1 | `louverture` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `use_action.name` | 20 | `dynamite_act` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `use_action.need_charges` | 19 | `armor_nomad_plate` · [data/json/items/armor/suits_protection.json](../../data/json/items/armor/suits_protection.json) |
| `use_action.need_charges_msg` | 18 | `armor_nomad_plate` · [data/json/items/armor/suits_protection.json](../../data/json/items/armor/suits_protection.json) |
| `use_action.need_fire` | 19 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.need_sunlight` | 1 | `binoculars` · [data/json/items/tool_armor.json](../../data/json/items/tool_armor.json) |
| `use_action.need_wielding` | 26 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.no_fail` | 1 | `louverture` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `use_action.noise` | 2 | `airhorn` · [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) |
| `use_action.noise_id` | 2 | `airhorn` · [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) |
| `use_action.noise_message` | 2 | `airhorn` · [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) |
| `use_action.noise_variant` | 2 | `airhorn` · [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) |
| `use_action.not_ready_msg` | 9 | `aquarium_medium_drying` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `use_action.npc_descriptions` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.outer_layer_trap` | 1 | `blade_trap` · [data/json/items/tool/traps.json](../../data/json/items/tool/traps.json) |
| `use_action.place_randomly` | 13 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.player_descriptions` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.practice` | 14 | `glass_shard` · [data/json/items/resources/glass.json](../../data/json/items/resources/glass.json) |
| `use_action.qualities_needed` | 3 | `compbow` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `use_action.qualities_needed.SCREW_FINE` | 3 | `compbow` · [data/json/items/ranged/archery.json](../../data/json/items/ranged/archery.json) |
| `use_action.radius` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action.skills` | 35 | `bot_EMP_hack` · [data/json/items/corpses/inactive_bots.json](../../data/json/items/corpses/inactive_bots.json) |
| `use_action.speed_penalty` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.spell_id` | 1 | `louverture` · [data/json/items/gun/artisan_guns.json](../../data/json/items/gun/artisan_guns.json) |
| `use_action.target` | 202 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.target_ammo` | 1 | `LAW_Packed` · [data/json/items/tool/explosives.json](../../data/json/items/tool/explosives.json) |
| `use_action.target_charges` | 6 | `sling-ready_molotov` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.target_timer` | 27 | `sling-ready_grenade` · [data/json/items/ammo/sling-ready_grenade.json](../../data/json/items/ammo/sling-ready_grenade.json) |
| `use_action.targets` | 5 | `power_cord` · [data/json/items/tool/cables.json](../../data/json/items/tool/cables.json) |
| `use_action.transform_age` | 9 | `aquarium_medium_drying` · [data/json/items/containers/containers.json](../../data/json/items/containers/containers.json) |
| `use_action.trap` | 14 | `glass_shard` · [data/json/items/resources/glass.json](../../data/json/items/resources/glass.json) |
| `use_action.type` | 326 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.use_message` | 2 | `airhorn` · [data/json/items/tool/misc.json](../../data/json/items/tool/misc.json) |
| `use_action.volume` | 1 | `art_harp` · [data/json/artifact/artifact_item_types.json](../../data/json/artifact/artifact_item_types.json) |
| `use_action.wall` | 4 | `large_tent_kit` · [data/json/items/tool/shelters.json](../../data/json/items/tool/shelters.json) |
| `use_action[].//need_charges_msg` | 2 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].active` | 6 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].ammo_scale` | 12 | `laptop_screen_lit` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].cable_length` | 47 | `hair_dryer` · [data/json/items/generic/bathroom_house.json](../../data/json/items/generic/bathroom_house.json) |
| `use_action[].charge_rate` | 47 | `hair_dryer` · [data/json/items/generic/bathroom_house.json](../../data/json/items/generic/bathroom_house.json) |
| `use_action[].cost_scaling` | 9 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].description` | 2 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].effect_on_conditions` | 2 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].furn_type` | 1 | `mannequin` · [data/json/items/generic/toys_and_sports.json](../../data/json/items/generic/toys_and_sports.json) |
| `use_action[].item_action_type` | 9 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].materials` | 9 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].menu_text` | 16 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].move_cost` | 9 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].moves` | 7 | `propane_cooker` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `use_action[].moves_slow` | 2 | `propane_cooker` · [data/json/items/tool/cooking.json](../../data/json/items/tool/cooking.json) |
| `use_action[].msg` | 14 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].need_charges` | 4 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].need_charges_msg` | 4 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].size` | 1 | `dragonskin` · [data/json/items/armor/ballistic_armor.json](../../data/json/items/armor/ballistic_armor.json) |
| `use_action[].skill` | 9 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].target` | 15 | `laptop` · [data/json/items/tool/electronics.json](../../data/json/items/tool/electronics.json) |
| `use_action[].tool_quality` | 5 | `integrated_welder` · [data/json/items/tool/integrated.json](../../data/json/items/tool/integrated.json) |
| `use_action[].type` | 74 | `dragonskin` · [data/json/items/armor/ballistic_armor.json](../../data/json/items/armor/ballistic_armor.json) |

## 显式flags取值

| 值 | 声明数 |
|---|---:|
| `ABLATIVE_CHAINMAIL_TORSO` | 5 |
| `ACT_IN_FIRE` | 3 |
| `ACT_ON_RANGED_HIT` | 1 |
| `ALARMCLOCK` | 1 |
| `ALLOWS_BODY_BLOCK` | 108 |
| `ALLOWS_NATURAL_ATTACKS` | 20 |
| `ALLOWS_REMOTE_USE` | 82 |
| `ALLOWS_TAIL` | 3 |
| `ALLOWS_TALONS` | 1 |
| `ALWAYS_TWOHAND` | 47 |
| `BACKBLAST` | 4 |
| `BAROMETER` | 1 |
| `BATTERY_HEAVY` | 5 |
| `BATTERY_LIGHT` | 5 |
| `BATTERY_MEDIUM` | 5 |
| `BATTERY_ULTRA_LIGHT` | 3 |
| `BELTED` | 75 |
| `BELT_CLIP` | 96 |
| `BIONIC_WEAPON` | 7 |
| `BIONIC_WEAPON_MELEE` | 2 |
| `BIPOD` | 4 |
| `BLOCK_WHILE_WORN` | 17 |
| `BOMB` | 43 |
| `BRASS_CATCHER` | 1 |
| `BURNOUT` | 2 |
| `CABLE_SPOOL` | 5 |
| `CAMERA_PRO` | 2 |
| `CANT_WEAR` | 3 |
| `CASELESS_ROUNDS` | 1 |
| `CBM` | 1 |
| `CHARGEDIM` | 6 |
| `CHOKE` | 2 |
| `COLLAPSED_STOCK` | 1 |
| `COLLAPSE_CONTENTS` | 30 |
| `COMBAT_TOGGLEABLE` | 9 |
| `CONDUCTIVE` | 41 |
| `CONSUMABLE` | 11 |
| `CORROSIVE` | 1 |
| `CRUTCHES` | 4 |
| `DANGEROUS` | 14 |
| `DEAF` | 1 |
| `DEBUG_ONLY` | 1 |
| `DETERGENT` | 2 |
| `DIG_TOOL` | 4 |
| `DISABLE_SIGHTS` | 14 |
| `DROP_ACTION_ONLY_IF_LIQUID` | 1 |
| `DURABLE_MELEE` | 154 |
| `EASY_CLEAN` | 48 |
| `EATEN_COLD` | 3 |
| `EDIBLE_FROZEN` | 1 |
| `ELECTRIC_IMMUNE` | 6 |
| `ELECTRONIC` | 48 |
| `FANCY` | 7 |
| `FIRE` | 6 |
| `FIRESTARTER` | 9 |
| `FIREWOOD` | 16 |
| `FIRE_TWOHAND` | 14 |
| `FLAMING` | 2 |
| `FLOTATION` | 3 |
| `FOLDED_STOCK` | 3 |
| `FRAGILE` | 3 |
| `FRAGILE_MELEE` | 71 |
| `FREEZERBURN` | 1 |
| `GASFILTER_MED` | 1 |
| `GASFILTER_SM` | 1 |
| `GAS_TANK` | 4 |
| `GRENADE` | 12 |
| `HOOD` | 8 |
| `HURT_WHEN_WIELDED` | 6 |
| `HYGROMETER` | 1 |
| `INEDIBLE` | 3 |
| `INSPIRATIONAL` | 2 |
| `INSTALL_DIFFICULT` | 10 |
| `INTEGRATED` | 8 |
| `IRREMOVABLE` | 32 |
| `IRREPLACEABLE_CONSUMABLE` | 72 |
| `IS_ARMOR` | 2 |
| `IS_PET_ARMOR` | 1 |
| `IS_UPS` | 4 |
| `JAVELIN` | 4 |
| `LASER_SIGHT` | 3 |
| `LEAK_ALWAYS` | 2 |
| `LEAK_DAM` | 16 |
| `LIGHT_10` | 4 |
| `LIGHT_15` | 5 |
| `LIGHT_2` | 2 |
| `LIGHT_200` | 1 |
| `LIGHT_240` | 2 |
| `LIGHT_300` | 2 |
| `LIGHT_4` | 1 |
| `LIGHT_450` | 2 |
| `LIGHT_500` | 1 |
| `LIGHT_60` | 1 |
| `MAG_BELT` | 2 |
| `MAG_BULKY` | 44 |
| `MAG_COMPACT` | 226 |
| `MAG_DESTROY` | 2 |
| `MAG_EJECT` | 2 |
| `MECH_BAT` | 1 |
| `MESSY` | 9 |
| `METHANOL_TANK` | 4 |
| `MISSION_ITEM` | 1 |
| `MOP` | 2 |
| `MOUNTED_GUN` | 8 |
| `NEEDS_NO_LUBE` | 7 |
| `NEEDS_UNFOLD` | 3 |
| `NEVER_JAMS` | 96 |
| `NOGIB` | 3 |
| `NONCONDUCTIVE` | 146 |
| `NON_FOULING` | 20 |
| `NORMAL` | 5 |
| `NO_DROP` | 9 |
| `NO_INGEST` | 1 |
| `NO_RELOAD` | 56 |
| `NO_REPAIR` | 59 |
| `NO_SALVAGE` | 94 |
| `NO_TURRET` | 20 |
| `NO_UNLOAD` | 70 |
| `NO_UNWIELD` | 3 |
| `NO_WEAR_EFFECT` | 6 |
| `NPC_ACTIVATE` | 12 |
| `NPC_THROWN` | 12 |
| `NPC_THROW_NOW` | 1 |
| `OBSOLETE` | 5 |
| `ONLY_ONE` | 15 |
| `OUTER` | 77 |
| `OVERHEATS` | 3 |
| `OVERSIZE` | 48 |
| `PADDED` | 36 |
| `PALS_LARGE` | 3 |
| `PALS_MEDIUM` | 2 |
| `PALS_SMALL` | 2 |
| `PAPER_SHAPED` | 1 |
| `PARTIAL_DEAF` | 3 |
| `PERSONAL` | 2 |
| `POCKETS` | 15 |
| `POLEARM` | 21 |
| `POWERARMOR_COMPATIBLE` | 3 |
| `POWERED` | 8 |
| `PRIMITIVE_RANGED_WEAPON` | 27 |
| `PSEUDO` | 3 |
| `PUMP_ACTION` | 2 |
| `PUMP_RAIL_COMPATIBLE` | 8 |
| `RADIOACTIVE` | 18 |
| `RADIOSIGNAL_2` | 2 |
| `RADIO_ACTIVATION` | 2 |
| `RADIO_INVOKE_PROC` | 31 |
| `RADIO_MODABLE` | 29 |
| `RAINPROOF` | 12 |
| `RAIN_PROTECT` | 2 |
| `RAW` | 2 |
| `REACH3` | 6 |
| `REACH_ATTACK` | 49 |
| `REBREATHER_CART` | 3 |
| `RECHARGE` | 11 |
| `REDUCED_BASHING` | 1 |
| `RELOAD_AND_SHOOT` | 17 |
| `RELOAD_EJECT` | 37 |
| `RELOAD_ONE` | 44 |
| `REMOVED_STOCK` | 1 |
| `REQUIRES_BALANCE` | 1 |
| `RESTRICT_HANDS` | 6 |
| `ROBOFAC_ROBOT_MEDIUM` | 2 |
| `ROBOFAC_ROBOT_SMALL` | 2 |
| `ROLLER_QUAD` | 1 |
| `SHEATH_AXE` | 23 |
| `SHEATH_BOW` | 10 |
| `SHEATH_GOLF` | 1 |
| `SHEATH_KNIFE` | 58 |
| `SHEATH_SPEAR` | 63 |
| `SHEATH_SWORD` | 44 |
| `SINGLE_USE` | 60 |
| `SKINTIGHT` | 11 |
| `SLEEP_IGNORE` | 6 |
| `SLOWS_MOVEMENT` | 2 |
| `SLOW_WIELD` | 5 |
| `SMOKABLE` | 4 |
| `SOFT` | 2 |
| `SOLARPACK` | 1 |
| `SOLARPACK_ON` | 1 |
| `SPAWN_ACTIVE` | 3 |
| `SPEAR` | 47 |
| `SPEEDLOADER` | 15 |
| `SPEEDLOADER_CLIP` | 3 |
| `STR_RELOAD` | 1 |
| `STURDY` | 157 |
| `SUN_GLASSES` | 10 |
| `SWIM_GOGGLES` | 1 |
| `TACK` | 1 |
| `TANGLE` | 2 |
| `TARDIS` | 1 |
| `THERMOMETER` | 4 |
| `TINDER` | 3 |
| `TOW_CABLE` | 1 |
| `TRADER_AVOID` | 164 |
| `TWO_WAY_RADIO` | 2 |
| `UNBREAKABLE` | 8 |
| `UNBREAKABLE_MELEE` | 14 |
| `UNDERSIZE` | 21 |
| `UNDERWATER_GUN` | 4 |
| `UNRECOVERABLE` | 12 |
| `USES_BIONIC_POWER` | 4 |
| `USES_NEARBY_AMMO` | 1 |
| `USE_UPS` | 18 |
| `VARSIZE` | 118 |
| `WATCH` | 6 |
| `WATERPROOF` | 75 |
| `WATERPROOF_GUN` | 32 |
| `WATER_BREAK` | 82 |
| `WATER_BREAK_ACTIVE` | 3 |
| `WATER_DISSOLVE` | 1 |
| `WATER_EXTINGUISH` | 4 |
| `WATER_FRIENDLY` | 74 |
| `WHIP` | 2 |
| `WIND_EXTINGUISH` | 1 |
| `WONT_TRAIN_MARKSMANSHIP` | 2 |
| `ZERO_WEIGHT` | 12 |
| `ZOOM` | 10 |

## 显式techniques取值

| 值 | 声明数 |
|---|---:|
| `BRUTAL` | 43 |
| `DEF_DISARM` | 7 |
| `IMPALE` | 8 |
| `PRECISE` | 20 |
| `RAPID` | 56 |
| `SPIN` | 3 |
| `SWEEP` | 70 |
| `SWEETSPOT` | 1 |
| `WBLOCK_1` | 198 |
| `WBLOCK_2` | 52 |
| `WBLOCK_3` | 1 |
| `WIDE` | 29 |
| `WRAP` | 2 |

## 显式weapon_category取值

| 值 | 声明数 |
|---|---:|
| `AUTOMATIC_PISTOLS` | 39 |
| `AUTOMATIC_RIFLES` | 9 |
| `BATONS` | 20 |
| `BIONIC_SWORDS` | 1 |
| `BIONIC_WEAPONRY` | 2 |
| `BSHORT_SWORDS` | 1 |
| `CLAWS` | 2 |
| `FENCING_WEAPONRY` | 14 |
| `FLAILS` | 2 |
| `GREAT_AXES` | 11 |
| `GREAT_HAMMERS` | 7 |
| `GREAT_SWORDS` | 7 |
| `HAND_AXES` | 5 |
| `HOOKING_WEAPONRY` | 33 |
| `KNIVES` | 25 |
| `LONG_SWORDS` | 3 |
| `LONG_THRUSTING_SWORDS` | 3 |
| `MACES` | 18 |
| `MEDIUM_SWORDS` | 17 |
| `POLEARMS` | 46 |
| `QUARTERSTAVES` | 17 |
| `SHIVS` | 49 |
| `SHORT_SWORDS` | 11 |
| `SPEARS` | 24 |

## 源码读取入口字段索引

以下从当前源码指定入口提取实际读取调用。函数与行号可用于回查；原样调用中的最后参数可能是下界或reader，不自动解释为默认值。分支是否运行、继承和finalize仍以主文解释与源码为准。此索引补足原版JSON未显式使用的受支持字段。

| 入口 | 字段 | 读取调用及源码 |
|---|---|---|
| `void Item_factory::load_basic_info` | `category` | `assign( jo, "category", def.category_force, strict );` · [src/item_factory.cpp:4086](../../src/item_factory.cpp#L4086) |
| `void Item_factory::load_basic_info` | `weight` | `assign( jo, "weight", def.weight, strict, 0_gram );` · [src/item_factory.cpp:4087](../../src/item_factory.cpp#L4087) |
| `void Item_factory::load_basic_info` | `integral_weight` | `assign( jo, "integral_weight", def.integral_weight, strict, 0_gram );` · [src/item_factory.cpp:4088](../../src/item_factory.cpp#L4088) |
| `void Item_factory::load_basic_info` | `volume` | `assign( jo, "volume", def.volume );` · [src/item_factory.cpp:4089](../../src/item_factory.cpp#L4089) |
| `void Item_factory::load_basic_info` | `longest_side` | `assign( jo, "longest_side", def.longest_side );` · [src/item_factory.cpp:4090](../../src/item_factory.cpp#L4090) |
| `void Item_factory::load_basic_info` | `price` | `assign( jo, "price", def.price, false, 0_cent );` · [src/item_factory.cpp:4091](../../src/item_factory.cpp#L4091) |
| `void Item_factory::load_basic_info` | `price_postapoc` | `assign( jo, "price_postapoc", def.price_post, false, 0_cent );` · [src/item_factory.cpp:4092](../../src/item_factory.cpp#L4092) |
| `void Item_factory::load_basic_info` | `stackable` | `assign( jo, "stackable", def.stackable_, strict );` · [src/item_factory.cpp:4093](../../src/item_factory.cpp#L4093) |
| `void Item_factory::load_basic_info` | `integral_volume` | `assign( jo, "integral_volume", def.integral_volume );` · [src/item_factory.cpp:4094](../../src/item_factory.cpp#L4094) |
| `void Item_factory::load_basic_info` | `integral_longest_side` | `assign( jo, "integral_longest_side", def.integral_longest_side, false, 0_mm );` · [src/item_factory.cpp:4095](../../src/item_factory.cpp#L4095) |
| `void Item_factory::load_basic_info` | `melee_damage` | `jo.get_object( "melee_damage" ) );` · [src/item_factory.cpp:4097](../../src/item_factory.cpp#L4097) |
| `void Item_factory::load_basic_info` | `proportional` | `jo.get_object( "proportional" );` · [src/item_factory.cpp:4101](../../src/item_factory.cpp#L4101) |
| `void Item_factory::load_basic_info` | `melee_damage` | `jprop.get_object( "melee_damage" ) );` · [src/item_factory.cpp:4104](../../src/item_factory.cpp#L4104) |
| `void Item_factory::load_basic_info` | `relative` | `jo.get_object( "relative" );` · [src/item_factory.cpp:4109](../../src/item_factory.cpp#L4109) |
| `void Item_factory::load_basic_info` | `melee_damage` | `jrel.get_object( "melee_damage" ) );` · [src/item_factory.cpp:4112](../../src/item_factory.cpp#L4112) |
| `void Item_factory::load_basic_info` | `to_hit` | `assign( jo, "to_hit", def.m_to_hit, strict );` · [src/item_factory.cpp:4116](../../src/item_factory.cpp#L4116) |
| `void Item_factory::load_basic_info` | `to_hit` | `mandatory( jo, was_loaded, "to_hit", temp );` · [src/item_factory.cpp:4120](../../src/item_factory.cpp#L4120) |
| `void Item_factory::load_basic_info` | `variant_type` | `optional( jo, false, "variant_type", def.variant_kind, itype_variant_kind::generic );` · [src/item_factory.cpp:4123](../../src/item_factory.cpp#L4123) |
| `void Item_factory::load_basic_info` | `variants` | `optional( jo, false, "variants", def.variants );` · [src/item_factory.cpp:4124](../../src/item_factory.cpp#L4124) |
| `void Item_factory::load_basic_info` | `container` | `assign( jo, "container", def.default_container );` · [src/item_factory.cpp:4125](../../src/item_factory.cpp#L4125) |
| `void Item_factory::load_basic_info` | `sealed` | `assign( jo, "sealed", def.default_container_sealed );` · [src/item_factory.cpp:4126](../../src/item_factory.cpp#L4126) |
| `void Item_factory::load_basic_info` | `min_strength` | `assign( jo, "min_strength", def.min_str );` · [src/item_factory.cpp:4127](../../src/item_factory.cpp#L4127) |
| `void Item_factory::load_basic_info` | `min_dexterity` | `assign( jo, "min_dexterity", def.min_dex );` · [src/item_factory.cpp:4128](../../src/item_factory.cpp#L4128) |
| `void Item_factory::load_basic_info` | `min_intelligence` | `assign( jo, "min_intelligence", def.min_int );` · [src/item_factory.cpp:4129](../../src/item_factory.cpp#L4129) |
| `void Item_factory::load_basic_info` | `min_perception` | `assign( jo, "min_perception", def.min_per );` · [src/item_factory.cpp:4130](../../src/item_factory.cpp#L4130) |
| `void Item_factory::load_basic_info` | `emits` | `assign( jo, "emits", def.emits );` · [src/item_factory.cpp:4131](../../src/item_factory.cpp#L4131) |
| `void Item_factory::load_basic_info` | `explode_in_fire` | `assign( jo, "explode_in_fire", def.explode_in_fire );` · [src/item_factory.cpp:4132](../../src/item_factory.cpp#L4132) |
| `void Item_factory::load_basic_info` | `insulation` | `assign( jo, "insulation", def.insulation_factor );` · [src/item_factory.cpp:4133](../../src/item_factory.cpp#L4133) |
| `void Item_factory::load_basic_info` | `solar_efficiency` | `assign( jo, "solar_efficiency", def.solar_efficiency );` · [src/item_factory.cpp:4134](../../src/item_factory.cpp#L4134) |
| `void Item_factory::load_basic_info` | `ascii_picture` | `assign( jo, "ascii_picture", def.picture_id );` · [src/item_factory.cpp:4135](../../src/item_factory.cpp#L4135) |
| `void Item_factory::load_basic_info` | `repairs_with` | `assign( jo, "repairs_with", def.repairs_with );` · [src/item_factory.cpp:4136](../../src/item_factory.cpp#L4136) |
| `void Item_factory::load_basic_info` | `thrown_damage` | `jo.get_array( "thrown_damage" ) );` · [src/item_factory.cpp:4139](../../src/item_factory.cpp#L4139) |
| `void Item_factory::load_basic_info` | `repairs_like` | `jo.read( "repairs_like", def.repairs_like );` · [src/item_factory.cpp:4148](../../src/item_factory.cpp#L4148) |
| `void Item_factory::load_basic_info` | `weapon_category` | `optional( jo, true, "weapon_category", def.weapon_category, auto_flags_reader<weapon_category_id> {} );` · [src/item_factory.cpp:4151](../../src/item_factory.cpp#L4151) |
| `void Item_factory::load_basic_info` | `degradation_multiplier` | `optional( jo, false, "degradation_multiplier", degrade_mult, 1.0f );` · [src/item_factory.cpp:4154](../../src/item_factory.cpp#L4154) |
| `void Item_factory::load_basic_info` | `name` | `jo.read( "name", def.name ) ) {` · [src/item_factory.cpp:4167](../../src/item_factory.cpp#L4167) |
| `void Item_factory::load_basic_info` | `description` | `jo.read( "description", def.description );` · [src/item_factory.cpp:4172](../../src/item_factory.cpp#L4172) |
| `void Item_factory::load_basic_info` | `symbol` | `jo.get_string( "symbol" );` · [src/item_factory.cpp:4176](../../src/item_factory.cpp#L4176) |
| `void Item_factory::load_basic_info` | `color` | `jo.get_string( "color" ) );` · [src/item_factory.cpp:4180](../../src/item_factory.cpp#L4180) |
| `void Item_factory::load_basic_info` | `material` | `jo.get_array( "material" ).test_object() ) {` · [src/item_factory.cpp:4193](../../src/item_factory.cpp#L4193) |
| `void Item_factory::load_basic_info` | `material` | `jo.get_array( "material" ) ) {` · [src/item_factory.cpp:4194](../../src/item_factory.cpp#L4194) |
| `void Item_factory::load_basic_info` | `type` | `mat.get_string( "type" ) ), mat.get_int( "portion", 1 ) );` · [src/item_factory.cpp:4195](../../src/item_factory.cpp#L4195) |
| `void Item_factory::load_basic_info` | `type` | `mat.get_string( "type" ) );` · [src/item_factory.cpp:4197](../../src/item_factory.cpp#L4197) |
| `void Item_factory::load_basic_info` | `material` | `jo.get_tags( "material" ) ) {` · [src/item_factory.cpp:4202](../../src/item_factory.cpp#L4202) |
| `void Item_factory::load_basic_info` | `phase` | `jo.get_enum_value<phase_id>( "phase" );` · [src/item_factory.cpp:4219](../../src/item_factory.cpp#L4219) |
| `void Item_factory::load_basic_info` | `magazines` | `jo.get_array( "magazines" ) ) {` · [src/item_factory.cpp:4226](../../src/item_factory.cpp#L4226) |
| `void Item_factory::load_basic_info` | `nanofab_template_group` | `jo.get_string( "nanofab_template_group" ) );` · [src/item_factory.cpp:4240](../../src/item_factory.cpp#L4240) |
| `void Item_factory::load_basic_info` | `template_requirements` | `jo.get_string( "template_requirements" ) );` · [src/item_factory.cpp:4244](../../src/item_factory.cpp#L4244) |
| `void Item_factory::load_basic_info` | `min_skills` | `jo.get_array( "min_skills" );` · [src/item_factory.cpp:4247](../../src/item_factory.cpp#L4247) |
| `void Item_factory::load_basic_info` | `explosion` | `jo.get_object( "explosion" );` · [src/item_factory.cpp:4260](../../src/item_factory.cpp#L4260) |
| `void Item_factory::load_basic_info` | `memory_card` | `jo.get_object( "memory_card" ) );` · [src/item_factory.cpp:4266](../../src/item_factory.cpp#L4266) |
| `void Item_factory::load_basic_info` | `variables` | `assign( jo, "variables", def.item_variables );` · [src/item_factory.cpp:4269](../../src/item_factory.cpp#L4269) |
| `void Item_factory::load_basic_info` | `flags` | `assign( jo, "flags", def.item_tags );` · [src/item_factory.cpp:4270](../../src/item_factory.cpp#L4270) |
| `void Item_factory::load_basic_info` | `source_monster` | `assign( jo, "source_monster", def.source_monster );` · [src/item_factory.cpp:4272](../../src/item_factory.cpp#L4272) |
| `void Item_factory::load_basic_info` | `faults` | `assign( jo, "faults", def.faults );` · [src/item_factory.cpp:4274](../../src/item_factory.cpp#L4274) |
| `void Item_factory::load_basic_info` | `extend` | `jo.get_object( "extend" );` · [src/item_factory.cpp:4281](../../src/item_factory.cpp#L4281) |
| `void Item_factory::load_basic_info` | `delete` | `jo.get_object( "delete" );` · [src/item_factory.cpp:4286](../../src/item_factory.cpp#L4286) |
| `void Item_factory::load_basic_info` | `relative` | `jo.get_object( "relative" );` · [src/item_factory.cpp:4291](../../src/item_factory.cpp#L4291) |
| `void Item_factory::load_basic_info` | `properties` | `optional( jo, def.was_loaded, "properties", def.properties );` · [src/item_factory.cpp:4302](../../src/item_factory.cpp#L4302) |
| `void Item_factory::load_basic_info` | `extend` | `jo.get_object( "extend" );` · [src/item_factory.cpp:4309](../../src/item_factory.cpp#L4309) |
| `void Item_factory::load_basic_info` | `delete` | `jo.get_object( "delete" );` · [src/item_factory.cpp:4314](../../src/item_factory.cpp#L4314) |
| `void Item_factory::load_basic_info` | `countdown_interval` | `assign( jo, "countdown_interval", def.countdown_interval );` · [src/item_factory.cpp:4323](../../src/item_factory.cpp#L4323) |
| `void Item_factory::load_basic_info` | `revert_to` | `assign( jo, "revert_to", def.revert_to, strict );` · [src/item_factory.cpp:4324](../../src/item_factory.cpp#L4324) |
| `void Item_factory::load_basic_info` | `countdown_action` | `jo.get_string( "countdown_action" ) );` · [src/item_factory.cpp:4327](../../src/item_factory.cpp#L4327) |
| `void Item_factory::load_basic_info` | `countdown_action` | `jo.get_object( "countdown_action" );` · [src/item_factory.cpp:4330](../../src/item_factory.cpp#L4330) |
| `void Item_factory::load_basic_info` | `drop_action` | `jo.get_string( "drop_action" ) );` · [src/item_factory.cpp:4338](../../src/item_factory.cpp#L4338) |
| `void Item_factory::load_basic_info` | `drop_action` | `jo.get_object( "drop_action" );` · [src/item_factory.cpp:4341](../../src/item_factory.cpp#L4341) |
| `void Item_factory::load_basic_info` | `looks_like` | `jo.read( "looks_like", def.looks_like );` · [src/item_factory.cpp:4348](../../src/item_factory.cpp#L4348) |
| `void Item_factory::load_basic_info` | `conditional_names` | `jo.get_array( "conditional_names" ) ) {` · [src/item_factory.cpp:4352](../../src/item_factory.cpp#L4352) |
| `void Item_factory::load_basic_info` | `type` | `curr.get_enum_value<condition_type>( "type" );` · [src/item_factory.cpp:4354](../../src/item_factory.cpp#L4354) |
| `void Item_factory::load_basic_info` | `condition` | `curr.get_string( "condition" );` · [src/item_factory.cpp:4355](../../src/item_factory.cpp#L4355) |
| `void Item_factory::load_basic_info` | `value` | `curr.get_string( "value", "" );` · [src/item_factory.cpp:4357](../../src/item_factory.cpp#L4357) |
| `void Item_factory::load_basic_info` | `name` | `curr.read( "name", cname.name ) ) {` · [src/item_factory.cpp:4358](../../src/item_factory.cpp#L4358) |
| `void Item_factory::load_basic_info` | `armor_data` | `assign( jo, "armor_data", def.armor, src == "dda" );` · [src/item_factory.cpp:4365](../../src/item_factory.cpp#L4365) |
| `void Item_factory::load_basic_info` | `pet_armor_data` | `assign( jo, "pet_armor_data", def.pet_armor, src == "dda" );` · [src/item_factory.cpp:4366](../../src/item_factory.cpp#L4366) |
| `void Item_factory::load_basic_info` | `book_data` | `assign( jo, "book_data", def.book, src == "dda" );` · [src/item_factory.cpp:4367](../../src/item_factory.cpp#L4367) |
| `void Item_factory::load_basic_info` | `ammo_data` | `assign( jo, "ammo_data", def.ammo, src == "dda" );` · [src/item_factory.cpp:4370](../../src/item_factory.cpp#L4370) |
| `void Item_factory::load_basic_info` | `seed_data` | `assign( jo, "seed_data", def.seed, src == "dda" );` · [src/item_factory.cpp:4371](../../src/item_factory.cpp#L4371) |
| `void Item_factory::load_basic_info` | `brewable` | `assign( jo, "brewable", def.brewable, src == "dda" );` · [src/item_factory.cpp:4372](../../src/item_factory.cpp#L4372) |
| `void Item_factory::load_basic_info` | `milling` | `assign( jo, "milling", def.milling_data, src == "dda" );` · [src/item_factory.cpp:4374](../../src/item_factory.cpp#L4374) |
| `void Item_factory::load_basic_info` | `gunmod_data` | `jo.get_object( "gunmod_data" );` · [src/item_factory.cpp:4380](../../src/item_factory.cpp#L4380) |
| `void Item_factory::load_basic_info` | `abstract` | `jo.read( "abstract", def.id, true );` · [src/item_factory.cpp:4386](../../src/item_factory.cpp#L4386) |
| `void Item_factory::load_basic_info` | `id` | `jo.read( "id", def.id, true );` · [src/item_factory.cpp:4388](../../src/item_factory.cpp#L4388) |
| `void Item_factory::load_basic_info` | `pocket_data` | `assign( jo, "pocket_data", def.pockets );` · [src/item_factory.cpp:4391](../../src/item_factory.cpp#L4391) |
| `void Item_factory::load_basic_info` | `snippet_category` | `jo.get_array( "snippet_category" ) );` · [src/item_factory.cpp:4419](../../src/item_factory.cpp#L4419) |
| `void Item_factory::load_basic_info` | `snippet_category` | `jo.get_string( "snippet_category", "" );` · [src/item_factory.cpp:4421](../../src/item_factory.cpp#L4421) |
| `void Item_factory::load_basic_info` | `expand_snippets` | `optional( jo, def.was_loaded, "expand_snippets", def.expand_snippets, false );` · [src/item_factory.cpp:4424](../../src/item_factory.cpp#L4424) |
| `void Item_factory::load_basic_info` | `replace_materials` | `jo.get_object( "replace_materials" );` · [src/item_factory.cpp:4427](../../src/item_factory.cpp#L4427) |
| `void Item_factory::load` | `skill` | `assign( jo, "skill", slot.skill_used, strict );` · [src/item_factory.cpp:2743](../../src/item_factory.cpp#L2743) |
| `void Item_factory::load` | `ammo` | `assign( jo, "ammo", slot.ammo, strict );` · [src/item_factory.cpp:2744](../../src/item_factory.cpp#L2744) |
| `void Item_factory::load` | `range` | `assign( jo, "range", slot.range, strict );` · [src/item_factory.cpp:2745](../../src/item_factory.cpp#L2745) |
| `void Item_factory::load` | `ranged_damage` | `assign( jo, "ranged_damage", slot.damage, strict, damage_instance( damage_type_id::NULL_ID(), -20, -20, -20, -20 ) );` · [src/item_factory.cpp:2747](../../src/item_factory.cpp#L2747) |
| `void Item_factory::load` | `dispersion` | `assign( jo, "dispersion", slot.dispersion, strict );` · [src/item_factory.cpp:2749](../../src/item_factory.cpp#L2749) |
| `void Item_factory::load` | `sight_dispersion` | `assign( jo, "sight_dispersion", slot.sight_dispersion, strict, 0, static_cast<int>( MAX_RECOIL ) );` · [src/item_factory.cpp:2750](../../src/item_factory.cpp#L2750) |
| `void Item_factory::load` | `recoil` | `assign( jo, "recoil", slot.recoil, strict, 0 );` · [src/item_factory.cpp:2751](../../src/item_factory.cpp#L2751) |
| `void Item_factory::load` | `handling` | `assign( jo, "handling", slot.handling, strict );` · [src/item_factory.cpp:2752](../../src/item_factory.cpp#L2752) |
| `void Item_factory::load` | `durability` | `assign( jo, "durability", slot.durability, strict, 0, 10 );` · [src/item_factory.cpp:2753](../../src/item_factory.cpp#L2753) |
| `void Item_factory::load` | `loudness` | `assign( jo, "loudness", slot.loudness, strict );` · [src/item_factory.cpp:2754](../../src/item_factory.cpp#L2754) |
| `void Item_factory::load` | `clip_size` | `assign( jo, "clip_size", slot.clip, strict, 0 );` · [src/item_factory.cpp:2755](../../src/item_factory.cpp#L2755) |
| `void Item_factory::load` | `reload` | `assign( jo, "reload", slot.reload_time, strict, 0 );` · [src/item_factory.cpp:2756](../../src/item_factory.cpp#L2756) |
| `void Item_factory::load` | `reload_noise` | `assign( jo, "reload_noise", slot.reload_noise, strict );` · [src/item_factory.cpp:2757](../../src/item_factory.cpp#L2757) |
| `void Item_factory::load` | `reload_noise_volume` | `assign( jo, "reload_noise_volume", slot.reload_noise_volume, strict, 0 );` · [src/item_factory.cpp:2758](../../src/item_factory.cpp#L2758) |
| `void Item_factory::load` | `barrel_volume` | `assign( jo, "barrel_volume", slot.barrel_volume, strict, 0_ml );` · [src/item_factory.cpp:2759](../../src/item_factory.cpp#L2759) |
| `void Item_factory::load` | `barrel_length` | `assign( jo, "barrel_length", slot.barrel_length, strict, 0_mm );` · [src/item_factory.cpp:2760](../../src/item_factory.cpp#L2760) |
| `void Item_factory::load` | `built_in_mods` | `assign( jo, "built_in_mods", slot.built_in_mods, strict );` · [src/item_factory.cpp:2761](../../src/item_factory.cpp#L2761) |
| `void Item_factory::load` | `default_mods` | `assign( jo, "default_mods", slot.default_mods, strict );` · [src/item_factory.cpp:2762](../../src/item_factory.cpp#L2762) |
| `void Item_factory::load` | `energy_drain` | `assign( jo, "energy_drain", slot.energy_drain, strict, 0_kJ );` · [src/item_factory.cpp:2763](../../src/item_factory.cpp#L2763) |
| `void Item_factory::load` | `blackpowder_tolerance` | `assign( jo, "blackpowder_tolerance", slot.blackpowder_tolerance, strict, 0 );` · [src/item_factory.cpp:2764](../../src/item_factory.cpp#L2764) |
| `void Item_factory::load` | `min_cycle_recoil` | `assign( jo, "min_cycle_recoil", slot.min_cycle_recoil, strict, 0 );` · [src/item_factory.cpp:2765](../../src/item_factory.cpp#L2765) |
| `void Item_factory::load` | `ammo_effects` | `assign( jo, "ammo_effects", slot.ammo_effects, strict );` · [src/item_factory.cpp:2766](../../src/item_factory.cpp#L2766) |
| `void Item_factory::load` | `ammo_to_fire` | `assign( jo, "ammo_to_fire", slot.ammo_to_fire, strict, 0 );` · [src/item_factory.cpp:2767](../../src/item_factory.cpp#L2767) |
| `void Item_factory::load` | `heat_per_shot` | `assign( jo, "heat_per_shot", slot.heat_per_shot, strict, 0.0 );` · [src/item_factory.cpp:2768](../../src/item_factory.cpp#L2768) |
| `void Item_factory::load` | `cooling_value` | `assign( jo, "cooling_value", slot.cooling_value, strict, 0.0 );` · [src/item_factory.cpp:2769](../../src/item_factory.cpp#L2769) |
| `void Item_factory::load` | `overheat_threshold` | `assign( jo, "overheat_threshold", slot.overheat_threshold, strict, -1.0 );` · [src/item_factory.cpp:2770](../../src/item_factory.cpp#L2770) |
| `void Item_factory::load` | `valid_mod_locations` | `jo.get_array( "valid_mod_locations" ) ) {` · [src/item_factory.cpp:2774](../../src/item_factory.cpp#L2774) |
| `void Item_factory::load` | `modes` | `assign( jo, "modes", slot.modes );` · [src/item_factory.cpp:2780](../../src/item_factory.cpp#L2780) |
| `void Item_factory::load` | `hurt_part_when_fired` | `assign( jo, "hurt_part_when_fired", slot.hurt_part_when_fired );` · [src/item_factory.cpp:2781](../../src/item_factory.cpp#L2781) |
| `void Item_factory::load` | `damage_modifier` | `assign( jo, "damage_modifier", slot.damage, strict, damage_instance( damage_type_id::NULL_ID(), -20, -20, -20, -20 ) );` · [src/item_factory.cpp:3414](../../src/item_factory.cpp#L3414) |
| `void Item_factory::load` | `loudness_modifier` | `assign( jo, "loudness_modifier", slot.loudness );` · [src/item_factory.cpp:3416](../../src/item_factory.cpp#L3416) |
| `void Item_factory::load` | `location` | `assign( jo, "location", slot.location );` · [src/item_factory.cpp:3417](../../src/item_factory.cpp#L3417) |
| `void Item_factory::load` | `dispersion_modifier` | `assign( jo, "dispersion_modifier", slot.dispersion );` · [src/item_factory.cpp:3418](../../src/item_factory.cpp#L3418) |
| `void Item_factory::load` | `field_of_view` | `assign( jo, "field_of_view", slot.field_of_view );` · [src/item_factory.cpp:3419](../../src/item_factory.cpp#L3419) |
| `void Item_factory::load` | `sight_dispersion` | `assign( jo, "sight_dispersion", slot.sight_dispersion );` · [src/item_factory.cpp:3420](../../src/item_factory.cpp#L3420) |
| `void Item_factory::load` | `aim_speed_modifier` | `assign( jo, "aim_speed_modifier", slot.aim_speed_modifier );` · [src/item_factory.cpp:3421](../../src/item_factory.cpp#L3421) |
| `void Item_factory::load` | `aim_speed` | `assign( jo, "aim_speed", slot.aim_speed, strict, -1 );` · [src/item_factory.cpp:3422](../../src/item_factory.cpp#L3422) |
| `void Item_factory::load` | `handling_modifier` | `assign( jo, "handling_modifier", slot.handling, strict );` · [src/item_factory.cpp:3423](../../src/item_factory.cpp#L3423) |
| `void Item_factory::load` | `range_modifier` | `assign( jo, "range_modifier", slot.range );` · [src/item_factory.cpp:3424](../../src/item_factory.cpp#L3424) |
| `void Item_factory::load` | `range_multiplier` | `assign( jo, "range_multiplier", slot.range_multiplier );` · [src/item_factory.cpp:3425](../../src/item_factory.cpp#L3425) |
| `void Item_factory::load` | `consume_chance` | `assign( jo, "consume_chance", slot.consume_chance );` · [src/item_factory.cpp:3426](../../src/item_factory.cpp#L3426) |
| `void Item_factory::load` | `consume_divisor` | `assign( jo, "consume_divisor", slot.consume_divisor );` · [src/item_factory.cpp:3427](../../src/item_factory.cpp#L3427) |
| `void Item_factory::load` | `shot_spread_multiplier_modifier` | `assign( jo, "shot_spread_multiplier_modifier", slot.shot_spread_multiplier_modifier );` · [src/item_factory.cpp:3428](../../src/item_factory.cpp#L3428) |
| `void Item_factory::load` | `ammo_effects` | `assign( jo, "ammo_effects", slot.ammo_effects, strict );` · [src/item_factory.cpp:3429](../../src/item_factory.cpp#L3429) |
| `void Item_factory::load` | `energy_drain_multiplier` | `assign( jo, "energy_drain_multiplier", slot.energy_drain_multiplier );` · [src/item_factory.cpp:3430](../../src/item_factory.cpp#L3430) |
| `void Item_factory::load` | `energy_drain_modifier` | `assign( jo, "energy_drain_modifier", slot.energy_drain_modifier );` · [src/item_factory.cpp:3431](../../src/item_factory.cpp#L3431) |
| `void Item_factory::load` | `ammo_to_fire_multiplier` | `assign( jo, "ammo_to_fire_multiplier", slot.ammo_to_fire_multiplier );` · [src/item_factory.cpp:3432](../../src/item_factory.cpp#L3432) |
| `void Item_factory::load` | `ammo_to_fire_modifier` | `assign( jo, "ammo_to_fire_modifier", slot.ammo_to_fire_modifier );` · [src/item_factory.cpp:3433](../../src/item_factory.cpp#L3433) |
| `void Item_factory::load` | `weight_multiplier` | `assign( jo, "weight_multiplier", slot.weight_multiplier );` · [src/item_factory.cpp:3434](../../src/item_factory.cpp#L3434) |
| `void Item_factory::load` | `overwrite_min_cycle_recoil` | `assign( jo, "overwrite_min_cycle_recoil", slot.overwrite_min_cycle_recoil );` · [src/item_factory.cpp:3435](../../src/item_factory.cpp#L3435) |
| `void Item_factory::load` | `overheat_threshold_modifier` | `assign( jo, "overheat_threshold_modifier", slot.overheat_threshold_modifier );` · [src/item_factory.cpp:3436](../../src/item_factory.cpp#L3436) |
| `void Item_factory::load` | `overheat_threshold_multiplier` | `assign( jo, "overheat_threshold_multiplier", slot.overheat_threshold_multiplier );` · [src/item_factory.cpp:3437](../../src/item_factory.cpp#L3437) |
| `void Item_factory::load` | `cooling_value_modifier` | `assign( jo, "cooling_value_modifier", slot.cooling_value_modifier );` · [src/item_factory.cpp:3438](../../src/item_factory.cpp#L3438) |
| `void Item_factory::load` | `cooling_value_multiplier` | `assign( jo, "cooling_value_multiplier", slot.cooling_value_multiplier );` · [src/item_factory.cpp:3439](../../src/item_factory.cpp#L3439) |
| `void Item_factory::load` | `heat_per_shot_modifier` | `assign( jo, "heat_per_shot_modifier", slot.heat_per_shot_modifier );` · [src/item_factory.cpp:3440](../../src/item_factory.cpp#L3440) |
| `void Item_factory::load` | `heat_per_shot_multiplier` | `assign( jo, "heat_per_shot_multiplier", slot.heat_per_shot_multiplier );` · [src/item_factory.cpp:3441](../../src/item_factory.cpp#L3441) |
| `void Item_factory::load` | `install_time` | `jo.get_int( "install_time" );` · [src/item_factory.cpp:3452](../../src/item_factory.cpp#L3452) |
| `void Item_factory::load` | `mod_targets` | `jo.get_tags( "mod_targets" ) ) {` · [src/item_factory.cpp:3461](../../src/item_factory.cpp#L3461) |
| `void Item_factory::load` | `mode_modifier` | `assign( jo, "mode_modifier", slot.mode_modifier );` · [src/item_factory.cpp:3466](../../src/item_factory.cpp#L3466) |
| `void Item_factory::load` | `reload_modifier` | `assign( jo, "reload_modifier", slot.reload_modifier );` · [src/item_factory.cpp:3467](../../src/item_factory.cpp#L3467) |
| `void Item_factory::load` | `min_str_required_mod` | `assign( jo, "min_str_required_mod", slot.min_str_required_mod );` · [src/item_factory.cpp:3468](../../src/item_factory.cpp#L3468) |
| `void Item_factory::load` | `add_mod` | `jo.get_array( "add_mod" ) ) {` · [src/item_factory.cpp:3471](../../src/item_factory.cpp#L3471) |
| `void Item_factory::load` | `blacklist_mod` | `assign( jo, "blacklist_mod", slot.blacklist_mod );` · [src/item_factory.cpp:3475](../../src/item_factory.cpp#L3475) |
| `void Item_factory::load` | `blacklist_slot` | `assign( jo, "blacklist_slot", slot.blacklist_slot );` · [src/item_factory.cpp:3476](../../src/item_factory.cpp#L3476) |
| `void Item_factory::load` | `barrel_length` | `assign( jo, "barrel_length", slot.barrel_length );` · [src/item_factory.cpp:3477](../../src/item_factory.cpp#L3477) |
| `void Item_factory::load` | `ammo_modifier` | `jo.get_array( "ammo_modifier" ) ) {` · [src/item_factory.cpp:3121](../../src/item_factory.cpp#L3121) |
| `void Item_factory::load` | `ammo_modifier` | `jo.get_string( "ammo_modifier" ) ) );` · [src/item_factory.cpp:3125](../../src/item_factory.cpp#L3125) |
| `void Item_factory::load` | `capacity_multiplier` | `assign( jo, "capacity_multiplier", slot.capacity_multiplier, strict );` · [src/item_factory.cpp:3127](../../src/item_factory.cpp#L3127) |
| `void Item_factory::load` | `acceptable_ammo` | `jo.get_tags( "acceptable_ammo" ) ) {` · [src/item_factory.cpp:3131](../../src/item_factory.cpp#L3131) |
| `void Item_factory::load` | `magazine_adaptor` | `jo.get_array( "magazine_adaptor" );` · [src/item_factory.cpp:3136](../../src/item_factory.cpp#L3136) |
| `void Item_factory::load` | `pocket_mods` | `jo.get_array( "pocket_mods" );` · [src/item_factory.cpp:3148](../../src/item_factory.cpp#L3148) |
| `void Item_factory::load` | `pocket_mods` | `optional( jo, false, "pocket_mods", slot.add_pockets );` · [src/item_factory.cpp:3150](../../src/item_factory.cpp#L3150) |
| `void Item_factory::load` | `ammo` | `assign( jo, "ammo", slot.ammo_id, strict );` · [src/item_factory.cpp:3068](../../src/item_factory.cpp#L3068) |
| `void Item_factory::load` | `max_charges` | `assign( jo, "max_charges", slot.max_charges, strict, 0 );` · [src/item_factory.cpp:3069](../../src/item_factory.cpp#L3069) |
| `void Item_factory::load` | `initial_charges` | `assign( jo, "initial_charges", slot.def_charges, strict, 0 );` · [src/item_factory.cpp:3070](../../src/item_factory.cpp#L3070) |
| `void Item_factory::load` | `charges_per_use` | `assign( jo, "charges_per_use", slot.charges_per_use, strict, 0 );` · [src/item_factory.cpp:3071](../../src/item_factory.cpp#L3071) |
| `void Item_factory::load` | `charge_factor` | `assign( jo, "charge_factor", slot.charge_factor, strict, 1 );` · [src/item_factory.cpp:3072](../../src/item_factory.cpp#L3072) |
| `void Item_factory::load` | `turns_per_charge` | `assign( jo, "turns_per_charge", slot.turns_per_charge, strict, 0 );` · [src/item_factory.cpp:3073](../../src/item_factory.cpp#L3073) |
| `void Item_factory::load` | `fuel_efficiency` | `assign( jo, "fuel_efficiency", slot.fuel_efficiency, strict, -1.0f );` · [src/item_factory.cpp:3074](../../src/item_factory.cpp#L3074) |
| `void Item_factory::load` | `power_draw` | `assign( jo, "power_draw", slot.power_draw, strict, 0_W );` · [src/item_factory.cpp:3075](../../src/item_factory.cpp#L3075) |
| `void Item_factory::load` | `revert_msg` | `assign( jo, "revert_msg", slot.revert_msg, strict );` · [src/item_factory.cpp:3076](../../src/item_factory.cpp#L3076) |
| `void Item_factory::load` | `sub` | `assign( jo, "sub", slot.subtype, strict );` · [src/item_factory.cpp:3077](../../src/item_factory.cpp#L3077) |
| `void Item_factory::load` | `rand_charges` | `jo.get_array( "rand_charges" ) ) {` · [src/item_factory.cpp:3089](../../src/item_factory.cpp#L3089) |
| `void Item_factory::load` | `ammo_type` | `assign( jo, "ammo_type", slot.type, strict );` · [src/item_factory.cpp:3493](../../src/item_factory.cpp#L3493) |
| `void Item_factory::load` | `capacity` | `assign( jo, "capacity", slot.capacity, strict, 0 );` · [src/item_factory.cpp:3494](../../src/item_factory.cpp#L3494) |
| `void Item_factory::load` | `count` | `assign( jo, "count", slot.count, strict, 0 );` · [src/item_factory.cpp:3495](../../src/item_factory.cpp#L3495) |
| `void Item_factory::load` | `default_ammo` | `assign( jo, "default_ammo", slot.default_ammo, strict );` · [src/item_factory.cpp:3496](../../src/item_factory.cpp#L3496) |
| `void Item_factory::load` | `reload_time` | `assign( jo, "reload_time", slot.reload_time, strict, 0 );` · [src/item_factory.cpp:3497](../../src/item_factory.cpp#L3497) |
| `void Item_factory::load` | `linkage` | `assign( jo, "linkage", slot.linkage, strict );` · [src/item_factory.cpp:3498](../../src/item_factory.cpp#L3498) |
| `void islot_ammo::load` | `ammo_type` | `mandatory( jo, was_loaded, "ammo_type", type );` · [src/item_factory.cpp:2614](../../src/item_factory.cpp#L2614) |
| `void islot_ammo::load` | `casing` | `optional( jo, was_loaded, "casing", casing, std::nullopt );` · [src/item_factory.cpp:2615](../../src/item_factory.cpp#L2615) |
| `void islot_ammo::load` | `drop` | `optional( jo, was_loaded, "drop", drop, itype_id::NULL_ID() );` · [src/item_factory.cpp:2616](../../src/item_factory.cpp#L2616) |
| `void islot_ammo::load` | `drop_chance` | `assign( jo, "drop_chance", drop_chance, strict, 0.0f, 1.0f );` · [src/item_factory.cpp:2617](../../src/item_factory.cpp#L2617) |
| `void islot_ammo::load` | `drop_active` | `optional( jo, was_loaded, "drop_active", drop_active, true );` · [src/item_factory.cpp:2618](../../src/item_factory.cpp#L2618) |
| `void islot_ammo::load` | `projectile_count` | `optional( jo, was_loaded, "projectile_count", count, 1 );` · [src/item_factory.cpp:2619](../../src/item_factory.cpp#L2619) |
| `void islot_ammo::load` | `shot_spread` | `optional( jo, was_loaded, "shot_spread", shot_spread, 0 );` · [src/item_factory.cpp:2620](../../src/item_factory.cpp#L2620) |
| `void islot_ammo::load` | `shot_damage` | `assign( jo, "shot_damage", shot_damage, strict );` · [src/item_factory.cpp:2621](../../src/item_factory.cpp#L2621) |
| `void islot_ammo::load` | `damage` | `assign( jo, "damage", damage, strict );` · [src/item_factory.cpp:2623](../../src/item_factory.cpp#L2623) |
| `void islot_ammo::load` | `range` | `assign( jo, "range", range, strict, 0 );` · [src/item_factory.cpp:2624](../../src/item_factory.cpp#L2624) |
| `void islot_ammo::load` | `range_multiplier` | `assign( jo, "range_multiplier", range_multiplier, strict, 1.0f );` · [src/item_factory.cpp:2625](../../src/item_factory.cpp#L2625) |
| `void islot_ammo::load` | `dispersion` | `assign( jo, "dispersion", dispersion, strict, 0 );` · [src/item_factory.cpp:2626](../../src/item_factory.cpp#L2626) |
| `void islot_ammo::load` | `recoil` | `assign( jo, "recoil", recoil, strict, 0 );` · [src/item_factory.cpp:2627](../../src/item_factory.cpp#L2627) |
| `void islot_ammo::load` | `count` | `assign( jo, "count", def_charges, strict, 1 );` · [src/item_factory.cpp:2628](../../src/item_factory.cpp#L2628) |
| `void islot_ammo::load` | `loudness` | `assign( jo, "loudness", loudness, strict, 0 );` · [src/item_factory.cpp:2629](../../src/item_factory.cpp#L2629) |
| `void islot_ammo::load` | `effects` | `assign( jo, "effects", ammo_effects, strict );` · [src/item_factory.cpp:2630](../../src/item_factory.cpp#L2630) |
| `void islot_ammo::load` | `critical_multiplier` | `assign( jo, "critical_multiplier", critical_multiplier, strict, 1.0f );` · [src/item_factory.cpp:2631](../../src/item_factory.cpp#L2631) |
| `void islot_ammo::load` | `show_stats` | `optional( jo, was_loaded, "show_stats", force_stat_display, false );` · [src/item_factory.cpp:2632](../../src/item_factory.cpp#L2632) |
| `void acc_data::load` | `grip` | `optional( jo, was_loaded, "grip", grip, grip_val::WEAPON );` · [src/item_factory.cpp:3987](../../src/item_factory.cpp#L3987) |
| `void acc_data::load` | `length` | `optional( jo, was_loaded, "length", length, length_val::HAND );` · [src/item_factory.cpp:3988](../../src/item_factory.cpp#L3988) |
| `void acc_data::load` | `surface` | `optional( jo, was_loaded, "surface", surface, surface_val::ANY );` · [src/item_factory.cpp:3989](../../src/item_factory.cpp#L3989) |
| `void acc_data::load` | `balance` | `optional( jo, was_loaded, "balance", balance, balance_val::NEUTRAL );` · [src/item_factory.cpp:3990](../../src/item_factory.cpp#L3990) |
| `void itype_variant_data::load` | `id` | `mandatory( jo, false, "id", id );` · [src/item_factory.cpp:2727](../../src/item_factory.cpp#L2727) |
| `void itype_variant_data::load` | `name` | `mandatory( jo, false, "name", alt_name );` · [src/item_factory.cpp:2728](../../src/item_factory.cpp#L2728) |
| `void itype_variant_data::load` | `description` | `mandatory( jo, false, "description", alt_description );` · [src/item_factory.cpp:2729](../../src/item_factory.cpp#L2729) |
| `void itype_variant_data::load` | `symbol` | `optional( jo, false, "symbol", alt_sym, std::nullopt );` · [src/item_factory.cpp:2730](../../src/item_factory.cpp#L2730) |
| `void itype_variant_data::load` | `color` | `jo.get_string( "color" ) );` · [src/item_factory.cpp:2732](../../src/item_factory.cpp#L2732) |
| `void itype_variant_data::load` | `ascii_picture` | `optional( jo, false, "ascii_picture", art );` · [src/item_factory.cpp:2734](../../src/item_factory.cpp#L2734) |
| `void itype_variant_data::load` | `weight` | `optional( jo, false, "weight", weight, 1 );` · [src/item_factory.cpp:2735](../../src/item_factory.cpp#L2735) |
| `void itype_variant_data::load` | `append` | `optional( jo, false, "append", append );` · [src/item_factory.cpp:2736](../../src/item_factory.cpp#L2736) |
| `void itype_variant_data::load` | `expand_snippets` | `optional( jo, false, "expand_snippets", expand_snippets );` · [src/item_factory.cpp:2737](../../src/item_factory.cpp#L2737) |
| `static damage_unit load_damage_unit` | `damage_type` | `curr.get_string( "damage_type" ) );` · [src/damage.cpp:657](../../src/damage.cpp#L657) |
| `static damage_unit load_damage_unit` | `amount` | `curr.get_float( "amount", 0 );` · [src/damage.cpp:659](../../src/damage.cpp#L659) |
| `static damage_unit load_damage_unit` | `armor_penetration` | `curr.get_float( "armor_penetration", 0 );` · [src/damage.cpp:660](../../src/damage.cpp#L660) |
| `static damage_unit load_damage_unit` | `armor_multiplier` | `curr.get_float( "armor_multiplier", 1.0f );` · [src/damage.cpp:661](../../src/damage.cpp#L661) |
| `static damage_unit load_damage_unit` | `damage_multiplier` | `curr.get_float( "damage_multiplier", 1.0f );` · [src/damage.cpp:662](../../src/damage.cpp#L662) |
| `static damage_unit load_damage_unit` | `constant_armor_multiplier` | `curr.get_float( "constant_armor_multiplier", 1.0f );` · [src/damage.cpp:664](../../src/damage.cpp#L664) |
| `static damage_unit load_damage_unit` | `constant_damage_multiplier` | `curr.get_float( "constant_damage_multiplier", 1.0f );` · [src/damage.cpp:665](../../src/damage.cpp#L665) |
| `static damage_unit load_damage_unit` | `barrels` | `optional( curr, false, "barrels", du.barrels );` · [src/damage.cpp:670](../../src/damage.cpp#L670) |
| `void damage_type::load` | `name` | `mandatory( jo, was_loaded, "name", name );` · [src/damage.cpp:111](../../src/damage.cpp#L111) |
| `void damage_type::load` | `skill` | `optional( jo, was_loaded, "skill", skill, skill_id::NULL_ID() );` · [src/damage.cpp:112](../../src/damage.cpp#L112) |
| `void damage_type::load` | `physical` | `optional( jo, was_loaded, "physical", physical );` · [src/damage.cpp:113](../../src/damage.cpp#L113) |
| `void damage_type::load` | `melee_only` | `optional( jo, was_loaded, "melee_only", melee_only );` · [src/damage.cpp:114](../../src/damage.cpp#L114) |
| `void damage_type::load` | `edged` | `optional( jo, was_loaded, "edged", edged );` · [src/damage.cpp:115](../../src/damage.cpp#L115) |
| `void damage_type::load` | `environmental` | `optional( jo, was_loaded, "environmental", env );` · [src/damage.cpp:116](../../src/damage.cpp#L116) |
| `void damage_type::load` | `material_required` | `optional( jo, was_loaded, "material_required", material_required );` · [src/damage.cpp:117](../../src/damage.cpp#L117) |
| `void damage_type::load` | `mon_difficulty` | `optional( jo, was_loaded, "mon_difficulty", mon_difficulty );` · [src/damage.cpp:118](../../src/damage.cpp#L118) |
| `void damage_type::load` | `no_resist` | `optional( jo, was_loaded, "no_resist", no_resist );` · [src/damage.cpp:119](../../src/damage.cpp#L119) |
| `void damage_type::load` | `immune_flags` | `jo.get_object( "immune_flags" );` · [src/damage.cpp:121](../../src/damage.cpp#L121) |
| `void damage_type::load` | `monster` | `jsobj.get_array( "monster" ) ) {` · [src/damage.cpp:124](../../src/damage.cpp#L124) |
| `void damage_type::load` | `character` | `jsobj.get_array( "character" ) ) {` · [src/damage.cpp:130](../../src/damage.cpp#L130) |
| `void damage_type::load` | `magic_color` | `optional( jo, was_loaded, "magic_color", color_str, "black" );` · [src/damage.cpp:138](../../src/damage.cpp#L138) |
| `void damage_type::load` | `derived_from` | `jo.get_array( "derived_from" );` · [src/damage.cpp:143](../../src/damage.cpp#L143) |
| `void damage_type::load` | `onhit_eocs` | `jo.get_array( "onhit_eocs" ) ) {` · [src/damage.cpp:147](../../src/damage.cpp#L147) |
| `void damage_type::load` | `ondamage_eocs` | `jo.get_array( "ondamage_eocs" ) ) {` · [src/damage.cpp:151](../../src/damage.cpp#L151) |
| `void ma_technique::load` | `name` | `mandatory( jo, was_loaded, "name", name );` · [src/martialarts.cpp:213](../../src/martialarts.cpp#L213) |
| `void ma_technique::load` | `description` | `optional( jo, was_loaded, "description", description, translation() );` · [src/martialarts.cpp:214](../../src/martialarts.cpp#L214) |
| `void ma_technique::load` | `messages` | `jo.get_array( "messages" );` · [src/martialarts.cpp:217](../../src/martialarts.cpp#L217) |
| `void ma_technique::load` | `crit_tec` | `optional( jo, was_loaded, "crit_tec", crit_tec, false );` · [src/martialarts.cpp:222](../../src/martialarts.cpp#L222) |
| `void ma_technique::load` | `crit_ok` | `optional( jo, was_loaded, "crit_ok", crit_ok, false );` · [src/martialarts.cpp:223](../../src/martialarts.cpp#L223) |
| `void ma_technique::load` | `attack_override` | `optional( jo, was_loaded, "attack_override", attack_override, false );` · [src/martialarts.cpp:224](../../src/martialarts.cpp#L224) |
| `void ma_technique::load` | `wall_adjacent` | `optional( jo, was_loaded, "wall_adjacent", wall_adjacent, false );` · [src/martialarts.cpp:225](../../src/martialarts.cpp#L225) |
| `void ma_technique::load` | `reach_tec` | `optional( jo, was_loaded, "reach_tec", reach_tec, false );` · [src/martialarts.cpp:226](../../src/martialarts.cpp#L226) |
| `void ma_technique::load` | `reach_ok` | `optional( jo, was_loaded, "reach_ok", reach_ok, false );` · [src/martialarts.cpp:227](../../src/martialarts.cpp#L227) |
| `void ma_technique::load` | `needs_ammo` | `optional( jo, was_loaded, "needs_ammo", needs_ammo, false );` · [src/martialarts.cpp:229](../../src/martialarts.cpp#L229) |
| `void ma_technique::load` | `defensive` | `optional( jo, was_loaded, "defensive", defensive, false );` · [src/martialarts.cpp:231](../../src/martialarts.cpp#L231) |
| `void ma_technique::load` | `disarms` | `optional( jo, was_loaded, "disarms", disarms, false );` · [src/martialarts.cpp:232](../../src/martialarts.cpp#L232) |
| `void ma_technique::load` | `take_weapon` | `optional( jo, was_loaded, "take_weapon", take_weapon, false );` · [src/martialarts.cpp:233](../../src/martialarts.cpp#L233) |
| `void ma_technique::load` | `side_switch` | `optional( jo, was_loaded, "side_switch", side_switch, false );` · [src/martialarts.cpp:234](../../src/martialarts.cpp#L234) |
| `void ma_technique::load` | `dummy` | `optional( jo, was_loaded, "dummy", dummy, false );` · [src/martialarts.cpp:235](../../src/martialarts.cpp#L235) |
| `void ma_technique::load` | `dodge_counter` | `optional( jo, was_loaded, "dodge_counter", dodge_counter, false );` · [src/martialarts.cpp:236](../../src/martialarts.cpp#L236) |
| `void ma_technique::load` | `block_counter` | `optional( jo, was_loaded, "block_counter", block_counter, false );` · [src/martialarts.cpp:237](../../src/martialarts.cpp#L237) |
| `void ma_technique::load` | `miss_recovery` | `optional( jo, was_loaded, "miss_recovery", miss_recovery, false );` · [src/martialarts.cpp:238](../../src/martialarts.cpp#L238) |
| `void ma_technique::load` | `grab_break` | `optional( jo, was_loaded, "grab_break", grab_break, false );` · [src/martialarts.cpp:239](../../src/martialarts.cpp#L239) |
| `void ma_technique::load` | `weighting` | `optional( jo, was_loaded, "weighting", weighting, 1 );` · [src/martialarts.cpp:241](../../src/martialarts.cpp#L241) |
| `void ma_technique::load` | `repeat_min` | `optional( jo, was_loaded, "repeat_min", repeat_min, 1 );` · [src/martialarts.cpp:243](../../src/martialarts.cpp#L243) |
| `void ma_technique::load` | `repeat_max` | `optional( jo, was_loaded, "repeat_max", repeat_max, 1 );` · [src/martialarts.cpp:244](../../src/martialarts.cpp#L244) |
| `void ma_technique::load` | `down_dur` | `optional( jo, was_loaded, "down_dur", down_dur, 0 );` · [src/martialarts.cpp:245](../../src/martialarts.cpp#L245) |
| `void ma_technique::load` | `stun_dur` | `optional( jo, was_loaded, "stun_dur", stun_dur, 0 );` · [src/martialarts.cpp:246](../../src/martialarts.cpp#L246) |
| `void ma_technique::load` | `knockback_dist` | `optional( jo, was_loaded, "knockback_dist", knockback_dist, 0 );` · [src/martialarts.cpp:247](../../src/martialarts.cpp#L247) |
| `void ma_technique::load` | `knockback_spread` | `optional( jo, was_loaded, "knockback_spread", knockback_spread, 0 );` · [src/martialarts.cpp:248](../../src/martialarts.cpp#L248) |
| `void ma_technique::load` | `knockback_follow` | `optional( jo, was_loaded, "knockback_follow", knockback_follow, false );` · [src/martialarts.cpp:249](../../src/martialarts.cpp#L249) |
| `void ma_technique::load` | `aoe` | `optional( jo, was_loaded, "aoe", aoe, "" );` · [src/martialarts.cpp:251](../../src/martialarts.cpp#L251) |
| `void ma_technique::load` | `flags` | `optional( jo, was_loaded, "flags", flags, auto_flags_reader<> {} );` · [src/martialarts.cpp:252](../../src/martialarts.cpp#L252) |
| `void ma_technique::load` | `tech_effects` | `optional( jo, was_loaded, "tech_effects", tech_effects, tech_effect_reader{} );` · [src/martialarts.cpp:253](../../src/martialarts.cpp#L253) |
| `void ma_technique::load` | `attack_vectors` | `optional( jo, was_loaded, "attack_vectors", attack_vectors, {} );` · [src/martialarts.cpp:255](../../src/martialarts.cpp#L255) |
| `void ma_technique::load` | `attack_vectors_random` | `optional( jo, was_loaded, "attack_vectors_random", attack_vectors_random, {} );` · [src/martialarts.cpp:256](../../src/martialarts.cpp#L256) |
| `void ma_technique::load` | `eocs` | `jo.get_array( "eocs" ) ) {` · [src/martialarts.cpp:258](../../src/martialarts.cpp#L258) |
| `void ma_technique::load` | `condition_desc` | `optional( jo, was_loaded, "condition_desc", condition_desc );` · [src/martialarts.cpp:264](../../src/martialarts.cpp#L264) |
| `void ma_requirements::load` | `unarmed_allowed` | `optional( jo, was_loaded, "unarmed_allowed", unarmed_allowed, false );` · [src/martialarts.cpp:184](../../src/martialarts.cpp#L184) |
| `void ma_requirements::load` | `melee_allowed` | `optional( jo, was_loaded, "melee_allowed", melee_allowed, false );` · [src/martialarts.cpp:185](../../src/martialarts.cpp#L185) |
| `void ma_requirements::load` | `unarmed_weapons_allowed` | `optional( jo, was_loaded, "unarmed_weapons_allowed", unarmed_weapons_allowed, true );` · [src/martialarts.cpp:186](../../src/martialarts.cpp#L186) |
| `void ma_requirements::load` | `weapon_categories_allowed` | `mandatory( jo, was_loaded, "weapon_categories_allowed", tmp_id );` · [src/martialarts.cpp:189](../../src/martialarts.cpp#L189) |
| `void ma_requirements::load` | `weapon_categories_allowed` | `optional( jo, was_loaded, "weapon_categories_allowed", weapon_categories_allowed );` · [src/martialarts.cpp:192](../../src/martialarts.cpp#L192) |
| `void ma_requirements::load` | `strictly_unarmed` | `optional( jo, was_loaded, "strictly_unarmed", strictly_unarmed, false );` · [src/martialarts.cpp:194](../../src/martialarts.cpp#L194) |
| `void ma_requirements::load` | `wall_adjacent` | `optional( jo, was_loaded, "wall_adjacent", wall_adjacent, false );` · [src/martialarts.cpp:195](../../src/martialarts.cpp#L195) |
| `void ma_requirements::load` | `required_buffs_all` | `optional( jo, was_loaded, "required_buffs_all", req_buffs_all, string_id_reader<::ma_buff> {} );` · [src/martialarts.cpp:197](../../src/martialarts.cpp#L197) |
| `void ma_requirements::load` | `required_buffs_any` | `optional( jo, was_loaded, "required_buffs_any", req_buffs_any, string_id_reader<::ma_buff> {} );` · [src/martialarts.cpp:198](../../src/martialarts.cpp#L198) |
| `void ma_requirements::load` | `forbidden_buffs_all` | `optional( jo, was_loaded, "forbidden_buffs_all", forbid_buffs_all, string_id_reader<::ma_buff> {} );` · [src/martialarts.cpp:199](../../src/martialarts.cpp#L199) |
| `void ma_requirements::load` | `forbidden_buffs_any` | `optional( jo, was_loaded, "forbidden_buffs_any", forbid_buffs_any, string_id_reader<::ma_buff> {} );` · [src/martialarts.cpp:200](../../src/martialarts.cpp#L200) |
| `void ma_requirements::load` | `req_flags` | `optional( jo, was_loaded, "req_flags", req_flags, string_id_reader<::json_flag> {} );` · [src/martialarts.cpp:202](../../src/martialarts.cpp#L202) |
| `void ma_requirements::load` | `required_char_flags` | `optional( jo, was_loaded, "required_char_flags", req_char_flags );` · [src/martialarts.cpp:203](../../src/martialarts.cpp#L203) |
| `void ma_requirements::load` | `required_char_flags_all` | `optional( jo, was_loaded, "required_char_flags_all", req_char_flags_all );` · [src/martialarts.cpp:204](../../src/martialarts.cpp#L204) |
| `void ma_requirements::load` | `forbidden_char_flags` | `optional( jo, was_loaded, "forbidden_char_flags", forbidden_char_flags );` · [src/martialarts.cpp:205](../../src/martialarts.cpp#L205) |
| `void ma_requirements::load` | `skill_requirements` | `optional( jo, was_loaded, "skill_requirements", min_skill, ma_skill_reader {} );` · [src/martialarts.cpp:207](../../src/martialarts.cpp#L207) |
| `void ma_requirements::load` | `weapon_damage_requirements` | `optional( jo, was_loaded, "weapon_damage_requirements", min_damage, ma_weapon_damage_reader {} );` · [src/martialarts.cpp:208](../../src/martialarts.cpp#L208) |
| `tech_effect_data load_tech_effect_data` | `id` | `e.get_string( "id" ) ), e.get_int( "duration", 0 ),` · [src/martialarts.cpp:160](../../src/martialarts.cpp#L160) |
| `tech_effect_data load_tech_effect_data` | `permanent` | `e.get_bool( "permanent", false ), e.get_bool( "on_damage", true ),` · [src/martialarts.cpp:161](../../src/martialarts.cpp#L161) |
| `tech_effect_data load_tech_effect_data` | `chance` | `e.get_int( "chance", 100 ), e.get_string( "message", "" ),` · [src/martialarts.cpp:162](../../src/martialarts.cpp#L162) |
| `tech_effect_data load_tech_effect_data` | `req_flag` | `e.get_string( "req_flag", "NULL" ) ) );` · [src/martialarts.cpp:163](../../src/martialarts.cpp#L163) |
| `void pocket_data::load` | `pocket_type` | `optional( jo, was_loaded, "pocket_type", type, pocket_type::CONTAINER );` · [src/item_pocket.cpp:122](../../src/item_pocket.cpp#L122) |
| `void pocket_data::load` | `ammo_restriction` | `optional( jo, was_loaded, "ammo_restriction", ammo_restriction );` · [src/item_pocket.cpp:123](../../src/item_pocket.cpp#L123) |
| `void pocket_data::load` | `flag_restriction` | `optional( jo, was_loaded, "flag_restriction", flag_restrictions );` · [src/item_pocket.cpp:124](../../src/item_pocket.cpp#L124) |
| `void pocket_data::load` | `item_restriction` | `optional( jo, was_loaded, "item_restriction", item_id_restriction );` · [src/item_pocket.cpp:125](../../src/item_pocket.cpp#L125) |
| `void pocket_data::load` | `material_restriction` | `optional( jo, was_loaded, "material_restriction", material_restriction );` · [src/item_pocket.cpp:126](../../src/item_pocket.cpp#L126) |
| `void pocket_data::load` | `allowed_speedloaders` | `optional( jo, was_loaded, "allowed_speedloaders", allowed_speedloaders );` · [src/item_pocket.cpp:127](../../src/item_pocket.cpp#L127) |
| `void pocket_data::load` | `default_magazine` | `optional( jo, was_loaded, "default_magazine", default_magazine );` · [src/item_pocket.cpp:128](../../src/item_pocket.cpp#L128) |
| `void pocket_data::load` | `description` | `optional( jo, was_loaded, "description", description );` · [src/item_pocket.cpp:129](../../src/item_pocket.cpp#L129) |
| `void pocket_data::load` | `name` | `optional( jo, was_loaded, "name", pocket_name );` · [src/item_pocket.cpp:130](../../src/item_pocket.cpp#L130) |
| `void pocket_data::load` | `item_restriction` | `mandatory( jo, was_loaded, "item_restriction", item_restriction );` · [src/item_pocket.cpp:142](../../src/item_pocket.cpp#L142) |
| `void pocket_data::load` | `min_item_volume` | `optional( jo, was_loaded, "min_item_volume", min_item_volume, volume_reader(), 0_ml );` · [src/item_pocket.cpp:148](../../src/item_pocket.cpp#L148) |
| `void pocket_data::load` | `max_item_volume` | `optional( jo, was_loaded, "max_item_volume", temp, volume_reader(), temp );` · [src/item_pocket.cpp:150](../../src/item_pocket.cpp#L150) |
| `void pocket_data::load` | `max_contains_volume` | `optional( jo, was_loaded, "max_contains_volume", volume_capacity, volume_reader(), max_volume_for_container );` · [src/item_pocket.cpp:154](../../src/item_pocket.cpp#L154) |
| `void pocket_data::load` | `max_contains_weight` | `optional( jo, was_loaded, "max_contains_weight", max_contains_weight, mass_reader(), max_weight_for_container );` · [src/item_pocket.cpp:156](../../src/item_pocket.cpp#L156) |
| `void pocket_data::load` | `max_item_length` | `optional( jo, was_loaded, "max_item_length", max_item_length, units::default_length_from_volume( volume_capacity ) * M_SQRT2 );` · [src/item_pocket.cpp:158](../../src/item_pocket.cpp#L158) |
| `void pocket_data::load` | `min_item_length` | `optional( jo, was_loaded, "min_item_length", min_item_length );` · [src/item_pocket.cpp:160](../../src/item_pocket.cpp#L160) |
| `void pocket_data::load` | `extra_encumbrance` | `optional( jo, was_loaded, "extra_encumbrance", extra_encumbrance, 0 );` · [src/item_pocket.cpp:161](../../src/item_pocket.cpp#L161) |
| `void pocket_data::load` | `volume_encumber_modifier` | `optional( jo, was_loaded, "volume_encumber_modifier", volume_encumber_modifier, 1 );` · [src/item_pocket.cpp:162](../../src/item_pocket.cpp#L162) |
| `void pocket_data::load` | `ripoff` | `optional( jo, was_loaded, "ripoff", ripoff, 0 );` · [src/item_pocket.cpp:163](../../src/item_pocket.cpp#L163) |
| `void pocket_data::load` | `activity_noise` | `optional( jo, was_loaded, "activity_noise", activity_noise );` · [src/item_pocket.cpp:164](../../src/item_pocket.cpp#L164) |
| `void pocket_data::load` | `spoil_multiplier` | `optional( jo, was_loaded, "spoil_multiplier", spoil_multiplier, 1.0f );` · [src/item_pocket.cpp:166](../../src/item_pocket.cpp#L166) |
| `void pocket_data::load` | `weight_multiplier` | `optional( jo, was_loaded, "weight_multiplier", weight_multiplier, 1.0f );` · [src/item_pocket.cpp:167](../../src/item_pocket.cpp#L167) |
| `void pocket_data::load` | `volume_multiplier` | `optional( jo, was_loaded, "volume_multiplier", volume_multiplier, 1.0f );` · [src/item_pocket.cpp:168](../../src/item_pocket.cpp#L168) |
| `void pocket_data::load` | `magazine_well` | `optional( jo, was_loaded, "magazine_well", magazine_well, volume_reader(), 0_ml );` · [src/item_pocket.cpp:169](../../src/item_pocket.cpp#L169) |
| `void pocket_data::load` | `moves` | `optional( jo, was_loaded, "moves", moves, 100 );` · [src/item_pocket.cpp:170](../../src/item_pocket.cpp#L170) |
| `void pocket_data::load` | `fire_protection` | `optional( jo, was_loaded, "fire_protection", fire_protection, false );` · [src/item_pocket.cpp:171](../../src/item_pocket.cpp#L171) |
| `void pocket_data::load` | `watertight` | `optional( jo, was_loaded, "watertight", watertight, false );` · [src/item_pocket.cpp:172](../../src/item_pocket.cpp#L172) |
| `void pocket_data::load` | `airtight` | `optional( jo, was_loaded, "airtight", airtight, false );` · [src/item_pocket.cpp:173](../../src/item_pocket.cpp#L173) |
| `void pocket_data::load` | `open_container` | `optional( jo, was_loaded, "open_container", open_container, false );` · [src/item_pocket.cpp:174](../../src/item_pocket.cpp#L174) |
| `void pocket_data::load` | `transparent` | `optional( jo, was_loaded, "transparent", transparent, false );` · [src/item_pocket.cpp:175](../../src/item_pocket.cpp#L175) |
| `void pocket_data::load` | `rigid` | `optional( jo, was_loaded, "rigid", rigid, false );` · [src/item_pocket.cpp:176](../../src/item_pocket.cpp#L176) |
| `void pocket_data::load` | `forbidden` | `optional( jo, was_loaded, "forbidden", forbidden, false );` · [src/item_pocket.cpp:177](../../src/item_pocket.cpp#L177) |
| `void pocket_data::load` | `holster` | `optional( jo, was_loaded, "holster", holster );` · [src/item_pocket.cpp:178](../../src/item_pocket.cpp#L178) |
| `void pocket_data::load` | `ablative` | `optional( jo, was_loaded, "ablative", ablative );` · [src/item_pocket.cpp:179](../../src/item_pocket.cpp#L179) |
| `void pocket_data::load` | `inherits_flags` | `optional( jo, was_loaded, "inherits_flags", inherits_flags );` · [src/item_pocket.cpp:180](../../src/item_pocket.cpp#L180) |
| `void pocket_data::load` | `sealed_data` | `optional( jo, was_loaded, "sealed_data", sealed_data );` · [src/item_pocket.cpp:185](../../src/item_pocket.cpp#L185) |
| `void ammo_effect::load` | `trigger_chance` | `optional( jo, was_loaded, "trigger_chance", trigger_chance, 1 );` · [src/ammo_effect.cpp:65](../../src/ammo_effect.cpp#L65) |
| `void ammo_effect::load` | `aoe` | `jo.get_object( "aoe" );` · [src/ammo_effect.cpp:68](../../src/ammo_effect.cpp#L68) |
| `void ammo_effect::load` | `field_type` | `optional( joa, was_loaded, "field_type", aoe_field_type_name, "fd_null" );` · [src/ammo_effect.cpp:69](../../src/ammo_effect.cpp#L69) |
| `void ammo_effect::load` | `intensity_min` | `optional( joa, was_loaded, "intensity_min", aoe_intensity_min, 0 );` · [src/ammo_effect.cpp:70](../../src/ammo_effect.cpp#L70) |
| `void ammo_effect::load` | `intensity_max` | `optional( joa, was_loaded, "intensity_max", aoe_intensity_max, 0 );` · [src/ammo_effect.cpp:71](../../src/ammo_effect.cpp#L71) |
| `void ammo_effect::load` | `radius` | `optional( joa, was_loaded, "radius", aoe_radius, 1 );` · [src/ammo_effect.cpp:72](../../src/ammo_effect.cpp#L72) |
| `void ammo_effect::load` | `radius_z` | `optional( joa, was_loaded, "radius_z", aoe_radius_z, 0 );` · [src/ammo_effect.cpp:73](../../src/ammo_effect.cpp#L73) |
| `void ammo_effect::load` | `chance` | `optional( joa, was_loaded, "chance", aoe_chance, 100 );` · [src/ammo_effect.cpp:74](../../src/ammo_effect.cpp#L74) |
| `void ammo_effect::load` | `size` | `optional( joa, was_loaded, "size", aoe_size, 0 );` · [src/ammo_effect.cpp:75](../../src/ammo_effect.cpp#L75) |
| `void ammo_effect::load` | `check_passable` | `optional( joa, was_loaded, "check_passable", aoe_check_passable, false );` · [src/ammo_effect.cpp:76](../../src/ammo_effect.cpp#L76) |
| `void ammo_effect::load` | `check_sees` | `optional( joa, was_loaded, "check_sees", aoe_check_sees, false );` · [src/ammo_effect.cpp:77](../../src/ammo_effect.cpp#L77) |
| `void ammo_effect::load` | `check_sees_radius` | `optional( joa, was_loaded, "check_sees_radius", aoe_check_sees_radius, 0 );` · [src/ammo_effect.cpp:78](../../src/ammo_effect.cpp#L78) |
| `void ammo_effect::load` | `trail` | `jo.get_object( "trail" );` · [src/ammo_effect.cpp:81](../../src/ammo_effect.cpp#L81) |
| `void ammo_effect::load` | `field_type` | `optional( joa, was_loaded, "field_type", trail_field_type_name, "fd_null" );` · [src/ammo_effect.cpp:82](../../src/ammo_effect.cpp#L82) |
| `void ammo_effect::load` | `intensity_min` | `optional( joa, was_loaded, "intensity_min", trail_intensity_min, 0 );` · [src/ammo_effect.cpp:83](../../src/ammo_effect.cpp#L83) |
| `void ammo_effect::load` | `intensity_max` | `optional( joa, was_loaded, "intensity_max", trail_intensity_max, 0 );` · [src/ammo_effect.cpp:84](../../src/ammo_effect.cpp#L84) |
| `void ammo_effect::load` | `chance` | `optional( joa, was_loaded, "chance", trail_chance, 100 );` · [src/ammo_effect.cpp:85](../../src/ammo_effect.cpp#L85) |
| `void ammo_effect::load` | `explosion` | `jo.get_object( "explosion" );` · [src/ammo_effect.cpp:88](../../src/ammo_effect.cpp#L88) |
| `void ammo_effect::load` | `do_flashbang` | `optional( jo, was_loaded, "do_flashbang", do_flashbang, false );` · [src/ammo_effect.cpp:91](../../src/ammo_effect.cpp#L91) |
| `void ammo_effect::load` | `do_emp_blast` | `optional( jo, was_loaded, "do_emp_blast", do_emp_blast, false );` · [src/ammo_effect.cpp:92](../../src/ammo_effect.cpp#L92) |
| `void ammo_effect::load` | `foamcrete_build` | `optional( jo, was_loaded, "foamcrete_build", foamcrete_build, false );` · [src/ammo_effect.cpp:93](../../src/ammo_effect.cpp#L93) |
| `void iuse_transform::load` | `target` | `obj.read( "target", target, true );` · [src/iuse_actor.cpp:167](../../src/iuse_actor.cpp#L167) |
| `void iuse_transform::load` | `msg` | `obj.read( "msg", msg_transform );` · [src/iuse_actor.cpp:169](../../src/iuse_actor.cpp#L169) |
| `void iuse_transform::load` | `variant_type` | `obj.read( "variant_type", variant_type );` · [src/iuse_actor.cpp:170](../../src/iuse_actor.cpp#L170) |
| `void iuse_transform::load` | `container` | `obj.read( "container", container );` · [src/iuse_actor.cpp:171](../../src/iuse_actor.cpp#L171) |
| `void iuse_transform::load` | `sealed` | `obj.read( "sealed", sealed );` · [src/iuse_actor.cpp:172](../../src/iuse_actor.cpp#L172) |
| `void iuse_transform::load` | `target_charges` | `obj.read( "target_charges", ammo_qty );` · [src/iuse_actor.cpp:177](../../src/iuse_actor.cpp#L177) |
| `void iuse_transform::load` | `rand_target_charges` | `obj.get_array( "rand_target_charges" ) ) {` · [src/iuse_actor.cpp:179](../../src/iuse_actor.cpp#L179) |
| `void iuse_transform::load` | `target_ammo` | `obj.read( "target_ammo", ammo_type );` · [src/iuse_actor.cpp:187](../../src/iuse_actor.cpp#L187) |
| `void iuse_transform::load` | `target_timer` | `obj.read( "target_timer", target_timer );` · [src/iuse_actor.cpp:189](../../src/iuse_actor.cpp#L189) |
| `void iuse_transform::load` | `active` | `obj.read( "active", active );` · [src/iuse_actor.cpp:195](../../src/iuse_actor.cpp#L195) |
| `void iuse_transform::load` | `moves` | `obj.read( "moves", moves );` · [src/iuse_actor.cpp:197](../../src/iuse_actor.cpp#L197) |
| `void iuse_transform::load` | `need_fire` | `obj.read( "need_fire", need_fire );` · [src/iuse_actor.cpp:202](../../src/iuse_actor.cpp#L202) |
| `void iuse_transform::load` | `need_charges_msg` | `obj.read( "need_charges_msg", need_charges_msg ) ) {` · [src/iuse_actor.cpp:204](../../src/iuse_actor.cpp#L204) |
| `void iuse_transform::load` | `need_charges` | `obj.read( "need_charges", need_charges );` · [src/iuse_actor.cpp:208](../../src/iuse_actor.cpp#L208) |
| `void iuse_transform::load` | `need_fire_msg` | `obj.read( "need_fire_msg", need_fire_msg ) ) {` · [src/iuse_actor.cpp:210](../../src/iuse_actor.cpp#L210) |
| `void iuse_transform::load` | `need_worn` | `obj.read( "need_worn", need_worn );` · [src/iuse_actor.cpp:214](../../src/iuse_actor.cpp#L214) |
| `void iuse_transform::load` | `need_wielding` | `obj.read( "need_wielding", need_wielding );` · [src/iuse_actor.cpp:215](../../src/iuse_actor.cpp#L215) |
| `void iuse_transform::load` | `need_empty` | `obj.read( "need_empty", need_empty );` · [src/iuse_actor.cpp:217](../../src/iuse_actor.cpp#L217) |
| `void iuse_transform::load` | `qualities_needed` | `obj.read( "qualities_needed", qualities_needed );` · [src/iuse_actor.cpp:219](../../src/iuse_actor.cpp#L219) |
| `void iuse_transform::load` | `menu_text` | `obj.read( "menu_text", menu_text );` · [src/iuse_actor.cpp:221](../../src/iuse_actor.cpp#L221) |
| `void holster_actor::load` | `holster_prompt` | `obj.read( "holster_prompt", holster_prompt );` · [src/iuse_actor.cpp:2464](../../src/iuse_actor.cpp#L2464) |
| `void holster_actor::load` | `holster_msg` | `obj.read( "holster_msg", holster_msg );` · [src/iuse_actor.cpp:2465](../../src/iuse_actor.cpp#L2465) |
| `explosion_data load_explosion_data` | `power` | `jo.read( "power", ret.power );` · [src/explosion.cpp:108](../../src/explosion.cpp#L108) |
| `explosion_data load_explosion_data` | `distance_factor` | `jo.get_float( "distance_factor", 0.75f );` · [src/explosion.cpp:110](../../src/explosion.cpp#L110) |
| `explosion_data load_explosion_data` | `max_noise` | `jo.get_int( "max_noise", 90000000 );` · [src/explosion.cpp:111](../../src/explosion.cpp#L111) |
| `explosion_data load_explosion_data` | `fire` | `jo.get_bool( "fire", false );` · [src/explosion.cpp:112](../../src/explosion.cpp#L112) |
| `explosion_data load_explosion_data` | `shrapnel` | `jo.get_int( "shrapnel" );` · [src/explosion.cpp:114](../../src/explosion.cpp#L114) |
| `explosion_data load_explosion_data` | `shrapnel` | `jo.get_object( "shrapnel" );` · [src/explosion.cpp:118](../../src/explosion.cpp#L118) |
| `shrapnel_data load_shrapnel_data` | `casing_mass` | `jo.read( "casing_mass", ret.casing_mass );` · [src/explosion.cpp:129](../../src/explosion.cpp#L129) |
| `shrapnel_data load_shrapnel_data` | `fragment_mass` | `jo.get_float( "fragment_mass", 0.08 );` · [src/explosion.cpp:131](../../src/explosion.cpp#L131) |
| `shrapnel_data load_shrapnel_data` | `recovery` | `jo.get_int( "recovery", 0 );` · [src/explosion.cpp:132](../../src/explosion.cpp#L132) |
| `shrapnel_data load_shrapnel_data` | `drop` | `jo.get_string( "drop", "null" ) );` · [src/explosion.cpp:133](../../src/explosion.cpp#L133) |
| `void ammunition_type::load_ammunition_type` | `id` | `jsobj.get_string( "id" ) ) ];` · [src/ammo.cpp:30](../../src/ammo.cpp#L30) |
| `void ammunition_type::load_ammunition_type` | `name` | `jsobj.read( "name", res.name_ );` · [src/ammo.cpp:31](../../src/ammo.cpp#L31) |
| `void ammunition_type::load_ammunition_type` | `default` | `jsobj.read( "default", res.default_ammotype_, true );` · [src/ammo.cpp:32](../../src/ammo.cpp#L32) |
| `void bonus_container::load` | `stat` | `qualifiers.get_string( "stat" ) );` · [src/bonuses.cpp:121](../../src/bonuses.cpp#L121) |
| `void bonus_container::load` | `type` | `qualifiers.read( "type", dt );` · [src/bonuses.cpp:128](../../src/bonuses.cpp#L128) |
| `effect_scaling::effect_scaling` | `scaling-stat` | `obj.get_string( "scaling-stat" ) );` · [src/bonuses.cpp:104](../../src/bonuses.cpp#L104) |
| `effect_scaling::effect_scaling` | `scale` | `obj.get_float( "scale" );` · [src/bonuses.cpp:109](../../src/bonuses.cpp#L109) |
