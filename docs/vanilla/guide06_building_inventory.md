# 原版建筑 JSON 全量字段盘点

对应策划：[06 聚居地的类型及其分案](../design/design06-建筑.md)。本篇提供具体建筑及地块的原版 JSON 依据，建筑选型与空间关系见策划案。

语义入口：[建筑mapgen指南](guide06_building_json.md)、[全部放置字段](guide06_building_placement.md)、[地形与家具](guide06_building_terrain_furniture.md)。本表扫描当前工作树data/json全部JSON，包含目录外生成器；不扫描data/mods，不把mapgen变体、模块或地形声明数解释为建筑种类数。

## 一、统计口径与声明数量

- 扫描JSON文件：2767；解析失败：0。
- 将obsoletion目录单列；盘点为显式声明，不模拟游戏加载后的继承、迁移、权重选择或实际可达性。
- 同字段路径在同一声明中只计一次；数组用[]归一化；符号字典、参数名和switch分支键用{key}归一化。保留具体上下文，不将内联物品组或封装物品内部字段误认成符号键。
- 实例链接指向原版文件；括号中的声明序号从0开始，用于定位同文件的条目。字段类型是原版实际出现的JSON类型，不是加载器允许类型的完整集合；源码支持但未使用的入口见正文。原版存在未消费的repear拼写，参见[放置字段](guide06_building_placement.md)的内联数据与非功能字段说明；不将其视为合法repeat别名。

| 声明类型 | 非obsoletion | obsoletion |
|---|---:|---:|
| mapgen | 5650 | 17 |
| palette | 425 | 0 |
| terrain | 1001 | 0 |
| furniture | 594 | 0 |
| embedded_mapgen | 20 | 0 |

| mapgen分支 | 声明数 |
|---|---:|
| om_terrain | 2628 |
| nested_mapgen_id | 2274 |
| update_mapgen_id | 748 |

20条非废弃内嵌mapgen均使用builtin与name，作为引用原版C++生成器的入口；普通json生成器、nested、update都纳入下方mapgen字段统计。

## 二、声明分布

| 类型 | 所在一级目录 | 声明数 |
|---|---|---:|
| embedded_mapgen | overmap | 20 |
| furniture | furniture_and_terrain | 594 |
| mapgen | effects_on_condition | 3 |
| mapgen | encounters | 8 |
| mapgen | mapgen | 5545 |
| mapgen | mapgen_palettes | 12 |
| mapgen | monsters | 8 |
| mapgen | npcs | 74 |
| palette | mapgen | 230 |
| palette | mapgen_palettes | 195 |
| terrain | furniture_and_terrain | 1001 |

## 3、mapgen全部显式字段路径

归一化字段路径458种。

| 字段路径 | 声明数 | 实际类型 | 原版实例（声明序号） |
|---|---:|---|---|
| `mapgen.method` | 5650 | string | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.nested_mapgen_id` | 2274 | string | [crates_supplies_mechanics](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_nested_maps.json)（0） |
| `mapgen.object` | 5650 | object | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.add` | 5 | array | [多绑定/拼图](../../data/json/mapgen/cs_car_dealership.json)（0） |
| `mapgen.object.add[].chance` | 5 | int | [多绑定/拼图](../../data/json/mapgen/cs_car_dealership.json)（0） |
| `mapgen.object.add[].item` | 5 | string | [多绑定/拼图](../../data/json/mapgen/cs_car_dealership.json)（0） |
| `mapgen.object.add[].x` | 5 | array, int | [多绑定/拼图](../../data/json/mapgen/cs_car_dealership.json)（0） |
| `mapgen.object.add[].y` | 5 | array, int | [多绑定/拼图](../../data/json/mapgen/cs_car_dealership.json)（0） |
| `mapgen.object.computers` | 73 | object | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}` | 73 | object | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.access_denied` | 9 | string | [多绑定/拼图](../../data/json/mapgen/bank.json)（2） |
| `mapgen.object.computers.{key}.chat_topics` | 2 | array | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_central_hallway.json)（3） |
| `mapgen.object.computers.{key}.eocs` | 2 | array | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_central_hallway.json)（3） |
| `mapgen.object.computers.{key}.failures` | 67 | array | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.failures[].action` | 67 | string | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.name` | 73 | string | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.options` | 71 | array | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.options[].action` | 71 | string | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.options[].name` | 71 | string | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.computers.{key}.options[].security` | 38 | int | [多绑定/拼图](../../data/json/mapgen/irradiator_1.json)（6） |
| `mapgen.object.computers.{key}.security` | 63 | int | [多绑定/拼图](../../data/json/mapgen/bank.json)（0） |
| `mapgen.object.faction_owner` | 141 | array | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.faction_owner[].id` | 141 | string | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.faction_owner[].x` | 141 | array | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.faction_owner[].y` | 141 | array | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.fallback_predecessor_mapgen` | 22 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（2） |
| `mapgen.object.fields` | 23 | object | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.fields.{key}` | 23 | object | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.fields.{key}.age` | 16 | int | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.fields.{key}.field` | 23 | string | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.fields.{key}.intensity` | 22 | array, int | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.fill_ter` | 2401 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.flags` | 1049 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（10） |
| `mapgen.object.furniture` | 1305 | object | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（10） |
| `mapgen.object.furniture.{key}` | 1242 | array, string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（10） |
| `mapgen.object.gaspumps` | 15 | object | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z-1.json)（0） |
| `mapgen.object.gaspumps.{key}` | 11 | object | [多绑定/拼图](../../data/json/mapgen/airport/s_airport_private.json)（0） |
| `mapgen.object.gaspumps.{key}.amount` | 5 | array | [多绑定/拼图](../../data/json/mapgen/helipad.json)（0） |
| `mapgen.object.gaspumps.{key}.fuel` | 8 | string | [多绑定/拼图](../../data/json/mapgen/gas_stations/s_gas.json)（0） |
| `mapgen.object.item` | 105 | object | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.item.{key}` | 105 | array, object | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.item.{key}.amount` | 14 | array, int | [多绑定/拼图](../../data/json/mapgen/cave.json)（11） |
| `mapgen.object.item.{key}.chance` | 60 | int | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.item.{key}.custom-flags` | 3 | array | [FEMA_le](../../data/json/mapgen/fema/FEMA_le_03.json)（0） |
| `mapgen.object.item.{key}.faction` | 1 | string | [tacoma_commune_makeshift_bed](../../data/json/npcs/tacoma_ranch/mission_mapgen_tacoma_commune.json)（9） |
| `mapgen.object.item.{key}.item` | 81 | string | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.item.{key}.repeat` | 21 | array, int | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.item.{key}[].amount` | 3 | array, int | [sub_f_ash](../../data/json/mapgen/lab/lab_rooms.json)（56） |
| `mapgen.object.item.{key}[].chance` | 28 | int | [多绑定/拼图](../../data/json/mapgen/farm.json)（4） |
| `mapgen.object.item.{key}[].charges` | 2 | array, int | [3x3_shed_trail_supplies_N](../../data/json/mapgen/nested/farm_nested.json)（21） |
| `mapgen.object.item.{key}[].item` | 33 | object, string | [多绑定/拼图](../../data/json/mapgen/farm.json)（4） |
| `mapgen.object.item.{key}[].item.cases` | 2 | object | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.item.{key}[].item.cases.{key}` | 2 | string | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.item.{key}[].item.switch` | 2 | object | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.item.{key}[].item.switch.fallback` | 2 | string | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.item.{key}[].item.switch.param` | 2 | string | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.item.{key}[].repeat` | 6 | array, int | [lab_mutagen_8x8_vault_east](../../data/json/mapgen/lab/lab_modular/lab_nests_modular/lab_nested_mutagen.json)（7） |
| `mapgen.object.items` | 1018 | object | [abandonedwarehouse_1](../../data/json/mapgen/abandoned_warehouse.json)（3） |
| `mapgen.object.items.{key}` | 1018 | array, object | [abandonedwarehouse_1](../../data/json/mapgen/abandoned_warehouse.json)（3） |
| `mapgen.object.items.{key}.chance` | 736 | int | [abandonedwarehouse_1](../../data/json/mapgen/abandoned_warehouse.json)（3） |
| `mapgen.object.items.{key}.item` | 742 | object, string | [abandonedwarehouse_1](../../data/json/mapgen/abandoned_warehouse.json)（3） |
| `mapgen.object.items.{key}.item.entries` | 16 | array | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.item.entries[].count` | 4 | array | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.item.entries[].group` | 15 | string | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.item.entries[].item` | 4 | string | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.item.entries[].prob` | 4 | int | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.item.subtype` | 16 | string | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（0） |
| `mapgen.object.items.{key}.repeat` | 449 | array, int | [abandonedwarehouse_1](../../data/json/mapgen/abandoned_warehouse.json)（3） |
| `mapgen.object.items.{key}[].ammo` | 8 | int | [room_6x6_guns_N](../../data/json/mapgen/nested/basement_nested.json)（45） |
| `mapgen.object.items.{key}[].chance` | 558 | int | [abandonedwarehouse_2](../../data/json/mapgen/abandoned_warehouse.json)（5） |
| `mapgen.object.items.{key}[].faction` | 1 | string | [4x4_planksandtools](../../data/json/mapgen/nested/shelter_nested.json)（8） |
| `mapgen.object.items.{key}[].item` | 558 | object, string | [abandonedwarehouse_2](../../data/json/mapgen/abandoned_warehouse.json)（5） |
| `mapgen.object.items.{key}[].item.entries` | 5 | array | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].item.entries[].charges` | 3 | array | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].item.entries[].count` | 3 | array | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].item.entries[].group` | 2 | string | [多绑定/拼图](../../data/json/mapgen/private_resort.json)（2） |
| `mapgen.object.items.{key}[].item.entries[].item` | 3 | string | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].item.entries[].prob` | 5 | int | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].item.subtype` | 5 | string | [多绑定/拼图](../../data/json/mapgen/mine/mine_amigara.json)（0） |
| `mapgen.object.items.{key}[].magazine` | 8 | int | [room_6x6_guns_N](../../data/json/mapgen/nested/basement_nested.json)（45） |
| `mapgen.object.items.{key}[].repeat` | 360 | array, int | [多绑定/拼图](../../data/json/mapgen/airliner.json)（0） |
| `mapgen.object.liquids` | 83 | object | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z0.json)（0） |
| `mapgen.object.liquids.{key}` | 83 | array, object | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z0.json)（0） |
| `mapgen.object.liquids.{key}.amount` | 80 | array | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z0.json)（0） |
| `mapgen.object.liquids.{key}.liquid` | 80 | string | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z0.json)（0） |
| `mapgen.object.liquids.{key}[].amount` | 4 | array | [多绑定/拼图](../../data/json/mapgen/hazardous_waste_sarcophagus.json)（1） |
| `mapgen.object.liquids.{key}[].chance` | 4 | int | [多绑定/拼图](../../data/json/mapgen/hazardous_waste_sarcophagus.json)（1） |
| `mapgen.object.liquids.{key}[].liquid` | 4 | string | [多绑定/拼图](../../data/json/mapgen/hazardous_waste_sarcophagus.json)（1） |
| `mapgen.object.mapgensize` | 2274 | array | [crates_supplies_mechanics](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_nested_maps.json)（0） |
| `mapgen.object.mapping` | 89 | object | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}` | 89 | object | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}.fields` | 1 | object | [lab_security_3x3_EW](../../data/json/mapgen/lab/lab_modular/lab_nests_modular/lab_nested_security.json)（4） |
| `mapgen.object.mapping.{key}.fields.field` | 1 | string | [lab_security_3x3_EW](../../data/json/mapgen/lab/lab_modular/lab_nests_modular/lab_nested_security.json)（4） |
| `mapgen.object.mapping.{key}.furniture` | 31 | array, string | [多绑定/拼图](../../data/json/mapgen/cabin.json)（16） |
| `mapgen.object.mapping.{key}.item` | 18 | array, object | [多绑定/拼图](../../data/json/mapgen/cabin.json)（17） |
| `mapgen.object.mapping.{key}.item.amount` | 1 | array | [lab_security_3x3_EW](../../data/json/mapgen/lab/lab_modular/lab_nests_modular/lab_nested_security.json)（4） |
| `mapgen.object.mapping.{key}.item.chance` | 1 | int | [多绑定/拼图](../../data/json/mapgen/cabin.json)（17） |
| `mapgen.object.mapping.{key}.item.item` | 4 | string | [多绑定/拼图](../../data/json/mapgen/cabin.json)（17） |
| `mapgen.object.mapping.{key}.item[].amount` | 1 | array, int | [多绑定/拼图](../../data/json/mapgen/lab/lab_escape.json)（0） |
| `mapgen.object.mapping.{key}.item[].chance` | 11 | int | [lab_finale_4x4](../../data/json/mapgen/lab/lab_floorplans_finale1level.json)（24） |
| `mapgen.object.mapping.{key}.item[].item` | 14 | string | [多绑定/拼图](../../data/json/mapgen/lab/lab_escape.json)（0） |
| `mapgen.object.mapping.{key}.items` | 60 | array, object | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}.items.chance` | 5 | int | [多绑定/拼图](../../data/json/mapgen/basement/basement_lab_stairs.json)（0） |
| `mapgen.object.mapping.{key}.items.item` | 5 | string | [多绑定/拼图](../../data/json/mapgen/basement/basement_lab_stairs.json)（0） |
| `mapgen.object.mapping.{key}.items[].chance` | 56 | int | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}.items[].item` | 56 | string | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}.items[].repeat` | 11 | array, int | [多绑定/拼图](../../data/json/mapgen/basement/basement_game.json)（4） |
| `mapgen.object.mapping.{key}.liquids` | 13 | object | [exodii_generic_tank](../../data/json/mapgen/exodii/exodii_nested_singletile.json)（13） |
| `mapgen.object.mapping.{key}.liquids.amount` | 13 | array | [exodii_generic_tank](../../data/json/mapgen/exodii/exodii_nested_singletile.json)（13） |
| `mapgen.object.mapping.{key}.liquids.liquid` | 13 | string | [exodii_generic_tank](../../data/json/mapgen/exodii/exodii_nested_singletile.json)（13） |
| `mapgen.object.mapping.{key}.terrain` | 3 | string | [多绑定/拼图](../../data/json/mapgen/cabin.json)（17） |
| `mapgen.object.mapping.{key}.traps` | 3 | array | [smallscrapyard_ocu](../../data/json/mapgen/fortified_scrap_yard/fortified_scrap_yard.json)（0） |
| `mapgen.object.monster` | 122 | object | [多绑定/拼图](../../data/json/mapgen/airliner.json)（0） |
| `mapgen.object.monster.{key}` | 122 | array, object | [多绑定/拼图](../../data/json/mapgen/airliner.json)（0） |
| `mapgen.object.monster.{key}.chance` | 46 | int | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.monster.{key}.friendly` | 1 | bool | [mine_finale](../../data/json/mapgen/mine/mine_generic.json)（7） |
| `mapgen.object.monster.{key}.group` | 6 | string | [多绑定/拼图](../../data/json/mapgen/bugs/beehive.json)（0） |
| `mapgen.object.monster.{key}.monster` | 114 | array, object, string | [多绑定/拼图](../../data/json/mapgen/airliner.json)（0） |
| `mapgen.object.monster.{key}.monster.cases` | 2 | object | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.monster.{key}.monster.cases.{key}` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.monster.{key}.monster.switch` | 2 | object | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.monster.{key}.monster.switch.fallback` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.monster.{key}.monster.switch.param` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.monster.{key}.name` | 1 | string | [多绑定/拼图](../../data/json/mapgen/farm_dairy_2.json)（0） |
| `mapgen.object.monster.{key}.pack_size` | 1 | array | [mx_basement_spider](../../data/json/mapgen/map_extras/spider.json)（3） |
| `mapgen.object.monster.{key}.spawn_data` | 9 | object | [多绑定/拼图](../../data/json/mapgen/gas_stations/gas_station_bunker.json)（2） |
| `mapgen.object.monster.{key}.spawn_data.ammo` | 9 | array | [多绑定/拼图](../../data/json/mapgen/gas_stations/gas_station_bunker.json)（2） |
| `mapgen.object.monster.{key}.spawn_data.ammo[].ammo_id` | 9 | string | [多绑定/拼图](../../data/json/mapgen/gas_stations/gas_station_bunker.json)（2） |
| `mapgen.object.monster.{key}.spawn_data.ammo[].qty` | 9 | array | [多绑定/拼图](../../data/json/mapgen/gas_stations/gas_station_bunker.json)（2） |
| `mapgen.object.monster.{key}[].chance` | 3 | int | [多绑定/拼图](../../data/json/mapgen/cave.json)（8） |
| `mapgen.object.monster.{key}[].monster` | 3 | string | [多绑定/拼图](../../data/json/mapgen/cave.json)（8） |
| `mapgen.object.monsters` | 23 | object | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.monsters.{key}` | 23 | array, object | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.monsters.{key}.chance` | 21 | int | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.monsters.{key}.density` | 18 | int, number | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.monsters.{key}.monster` | 22 | string | [多绑定/拼图](../../data/json/mapgen/cave.json)（2） |
| `mapgen.object.monsters.{key}[].chance` | 2 | int | [多绑定/拼图](../../data/json/mapgen/fema/FEMA.json)（0） |
| `mapgen.object.monsters.{key}[].density` | 2 | number | [多绑定/拼图](../../data/json/mapgen/fema/FEMA.json)（0） |
| `mapgen.object.monsters.{key}[].monster` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fema/FEMA.json)（0） |
| `mapgen.object.nested` | 233 | object | [多绑定/拼图](../../data/json/mapgen/apartment_con_new.json)（5） |
| `mapgen.object.nested.{key}` | 233 | array, object | [多绑定/拼图](../../data/json/mapgen/apartment_con_new.json)（5） |
| `mapgen.object.nested.{key}.chunks` | 232 | array | [多绑定/拼图](../../data/json/mapgen/apartment_con_new.json)（5） |
| `mapgen.object.nested.{key}.chunks[].cases` | 2 | object | [24x24_bandits_block_horizontal_traps](../../data/json/mapgen/map_extras/bandits_block.json)（5） |
| `mapgen.object.nested.{key}.chunks[].cases.{key}` | 2 | string | [24x24_bandits_block_horizontal_traps](../../data/json/mapgen/map_extras/bandits_block.json)（5） |
| `mapgen.object.nested.{key}.chunks[].switch` | 2 | object | [24x24_bandits_block_horizontal_traps](../../data/json/mapgen/map_extras/bandits_block.json)（5） |
| `mapgen.object.nested.{key}.chunks[].switch.fallback` | 2 | string | [24x24_bandits_block_horizontal_traps](../../data/json/mapgen/map_extras/bandits_block.json)（5） |
| `mapgen.object.nested.{key}.chunks[].switch.param` | 2 | string | [24x24_bandits_block_horizontal_traps](../../data/json/mapgen/map_extras/bandits_block.json)（5） |
| `mapgen.object.nested.{key}[].chunks` | 1 | array | [mx_house_wasp](../../data/json/mapgen/map_extras/house_wasp.json)（0） |
| `mapgen.object.npcs` | 15 | object | [24x24_bandits_block_horizontal_felled_trees](../../data/json/mapgen/map_extras/bandits_block.json)（3） |
| `mapgen.object.npcs.{key}` | 15 | object | [24x24_bandits_block_horizontal_felled_trees](../../data/json/mapgen/map_extras/bandits_block.json)（3） |
| `mapgen.object.npcs.{key}.class` | 15 | string | [24x24_bandits_block_horizontal_felled_trees](../../data/json/mapgen/map_extras/bandits_block.json)（3） |
| `mapgen.object.palettes` | 3525 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.palettes[].distribution` | 27 | array | [多绑定/拼图](../../data/json/mapgen/cabin.json)（0） |
| `mapgen.object.palettes[].param` | 170 | string | [fbmc_pottery_cottage_blacksmith_construction_nested](../../data/json/mapgen/basecamps/base/fbmc_pottery_cottage/fbmc_pottery_cottage_blacksmith.json)（0） |
| `mapgen.object.parameters` | 199 | object | [多绑定/拼图](../../data/json/mapgen/barber_shop.json)（0） |
| `mapgen.object.parameters.{key}` | 199 | object | [多绑定/拼图](../../data/json/mapgen/barber_shop.json)（0） |
| `mapgen.object.parameters.{key}.default` | 199 | object | [多绑定/拼图](../../data/json/mapgen/barber_shop.json)（0） |
| `mapgen.object.parameters.{key}.default.distribution` | 199 | array | [多绑定/拼图](../../data/json/mapgen/barber_shop.json)（0） |
| `mapgen.object.parameters.{key}.scope` | 176 | string | [fbmc_pottery_cottage_blacksmith_construction_nested](../../data/json/mapgen/basecamps/base/fbmc_pottery_cottage/fbmc_pottery_cottage_blacksmith.json)（0） |
| `mapgen.object.parameters.{key}.type` | 199 | string | [多绑定/拼图](../../data/json/mapgen/barber_shop.json)（0） |
| `mapgen.object.place_computers` | 9 | array | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_computers[].chat_topics` | 9 | array | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_computers[].eocs` | 9 | array | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_computers[].name` | 9 | string | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_computers[].x` | 9 | int | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_computers[].y` | 9 | int | [prepper_1_computer](../../data/json/mapgen/nested/lmoe_nested.json)（3） |
| `mapgen.object.place_corpses` | 4 | array | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_corpses[].age` | 1 | int | [1x1_dead_wolf](../../data/json/mapgen/map_extras/mayhem.json)（10） |
| `mapgen.object.place_corpses[].group` | 4 | string | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_corpses[].x` | 4 | array, int | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_corpses[].y` | 4 | array, int | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_fields` | 69 | array | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_fields[].age` | 15 | int | [多绑定/拼图](../../data/json/mapgen/farm_dairy_2.json)（2） |
| `mapgen.object.place_fields[].field` | 69 | string | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_fields[].intensity` | 28 | array, int | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_fields[].repeat` | 40 | array, int | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_fields[].x` | 69 | array, int | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_fields[].y` | 69 | array, int | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.object.place_furniture` | 42 | array | [fbmc_firestation1_kitchen3](../../data/json/mapgen/basecamps/base/modular_firestation_1/modular_firestation1.json)（10） |
| `mapgen.object.place_furniture[].furn` | 42 | string | [fbmc_firestation1_kitchen3](../../data/json/mapgen/basecamps/base/modular_firestation_1/modular_firestation1.json)（10） |
| `mapgen.object.place_furniture[].repeat` | 1 | array | [多绑定/拼图](../../data/json/mapgen/survivor_forest_camp.json)（0） |
| `mapgen.object.place_furniture[].x` | 42 | array, int | [fbmc_firestation1_kitchen3](../../data/json/mapgen/basecamps/base/modular_firestation_1/modular_firestation1.json)（10） |
| `mapgen.object.place_furniture[].y` | 42 | array, int | [fbmc_firestation1_kitchen3](../../data/json/mapgen/basecamps/base/modular_firestation_1/modular_firestation1.json)（10） |
| `mapgen.object.place_graffiti` | 11 | array | [headshop_graffiti_snippet](../../data/json/mapgen/headshop.json)（3） |
| `mapgen.object.place_graffiti[].snippet` | 5 | string | [headshop_graffiti_snippet](../../data/json/mapgen/headshop.json)（3） |
| `mapgen.object.place_graffiti[].text` | 6 | string | [多绑定/拼图](../../data/json/mapgen/irradiator_1.json)（6） |
| `mapgen.object.place_graffiti[].x` | 11 | int | [headshop_graffiti_snippet](../../data/json/mapgen/headshop.json)（3） |
| `mapgen.object.place_graffiti[].y` | 11 | int | [headshop_graffiti_snippet](../../data/json/mapgen/headshop.json)（3） |
| `mapgen.object.place_item` | 180 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_item[].amount` | 17 | array, int | [多绑定/拼图](../../data/json/mapgen/basement/basement_meth.json)（0） |
| `mapgen.object.place_item[].chance` | 82 | int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_item[].custom-flags` | 1 | array | [crater_bomb](../../data/json/mapgen/map_extras/crater.json)（0） |
| `mapgen.object.place_item[].faction` | 5 | string | [tacoma_commune_bar_16_done](../../data/json/npcs/tacoma_ranch/mission_mapgen_tacoma_commune.json)（13） |
| `mapgen.object.place_item[].item` | 180 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_item[].repeat` | 68 | array, int | [多绑定/拼图](../../data/json/mapgen/bunker.json)（1） |
| `mapgen.object.place_item[].x` | 180 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_item[].y` | 180 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_items` | 426 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_items[].chance` | 423 | int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_items[].faction` | 1 | string | [tacoma_commune_bar_16_done](../../data/json/npcs/tacoma_ranch/mission_mapgen_tacoma_commune.json)（13） |
| `mapgen.object.place_items[].item` | 423 | object, string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_items[].item.entries` | 4 | array | [cannabis_extraction_equipment_nested_1x1](../../data/json/mapgen/basement/basement_weed.json)（1） |
| `mapgen.object.place_items[].item.entries[].charges` | 1 | array | [mine_minerals_equipment](../../data/json/mapgen/nested/mine_nested.json)（14） |
| `mapgen.object.place_items[].item.entries[].count` | 1 | array | [mine_minerals_equipment](../../data/json/mapgen/nested/mine_nested.json)（14） |
| `mapgen.object.place_items[].item.entries[].damage` | 1 | int | [mine_minerals_equipment](../../data/json/mapgen/nested/mine_nested.json)（14） |
| `mapgen.object.place_items[].item.entries[].group` | 4 | string | [cannabis_extraction_equipment_nested_1x1](../../data/json/mapgen/basement/basement_weed.json)（1） |
| `mapgen.object.place_items[].item.entries[].item` | 1 | string | [mine_minerals_equipment](../../data/json/mapgen/nested/mine_nested.json)（14） |
| `mapgen.object.place_items[].item.entries[].prob` | 4 | int | [cannabis_extraction_equipment_nested_1x1](../../data/json/mapgen/basement/basement_weed.json)（1） |
| `mapgen.object.place_items[].item.subtype` | 4 | string | [cannabis_extraction_equipment_nested_1x1](../../data/json/mapgen/basement/basement_weed.json)（1） |
| `mapgen.object.place_items[].repeat` | 283 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_items[].x` | 423 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_items[].y` | 423 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.place_liquids` | 42 | array | [多绑定/拼图](../../data/json/mapgen/basement/basement_survival.json)（2） |
| `mapgen.object.place_liquids[].amount` | 34 | array, int | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_liquids[].chance` | 6 | int | [多绑定/拼图](../../data/json/mapgen/farm_supply.json)（2） |
| `mapgen.object.place_liquids[].liquid` | 42 | string | [多绑定/拼图](../../data/json/mapgen/basement/basement_survival.json)（2） |
| `mapgen.object.place_liquids[].repeat` | 8 | array, int | [多绑定/拼图](../../data/json/mapgen/basement/basement_survival.json)（2） |
| `mapgen.object.place_liquids[].x` | 42 | array, int | [多绑定/拼图](../../data/json/mapgen/basement/basement_survival.json)（2） |
| `mapgen.object.place_liquids[].y` | 42 | array, int | [多绑定/拼图](../../data/json/mapgen/basement/basement_survival.json)（2） |
| `mapgen.object.place_loot` | 673 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].ammo` | 35 | int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].chance` | 493 | int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].group` | 293 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].item` | 481 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].magazine` | 29 | int | [多绑定/拼图](../../data/json/mapgen/basement/basement_guns.json)（0） |
| `mapgen.object.place_loot[].repeat` | 202 | array, int | [多绑定/拼图](../../data/json/mapgen/airliner.json)（0） |
| `mapgen.object.place_loot[].variant` | 2 | string | [多绑定/拼图](../../data/json/mapgen/military/mil_base/mil_base_z0.json)（2） |
| `mapgen.object.place_loot[].x` | 673 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_loot[].y` | 673 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（13） |
| `mapgen.object.place_monster` | 484 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.place_monster[].chance` | 277 | int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.place_monster[].group` | 302 | object, string | [多绑定/拼图](../../data/json/mapgen/airport/s_airport_private.json)（0） |
| `mapgen.object.place_monster[].group.cases` | 9 | object | [fort_zombie](../../data/json/mapgen/fort.json)（0） |
| `mapgen.object.place_monster[].group.cases.{key}` | 9 | string | [fort_zombie](../../data/json/mapgen/fort.json)（0） |
| `mapgen.object.place_monster[].group.switch` | 9 | object | [fort_zombie](../../data/json/mapgen/fort.json)（0） |
| `mapgen.object.place_monster[].group.switch.fallback` | 9 | string | [fort_zombie](../../data/json/mapgen/fort.json)（0） |
| `mapgen.object.place_monster[].group.switch.param` | 9 | string | [fort_zombie](../../data/json/mapgen/fort.json)（0） |
| `mapgen.object.place_monster[].monster` | 196 | array, string | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.place_monster[].name` | 3 | string | [多绑定/拼图](../../data/json/mapgen/farm_dairy_2.json)（1） |
| `mapgen.object.place_monster[].one_or_none` | 1 | bool | [lab_room_7x7_crossdoors](../../data/json/mapgen/lab/lab_rooms.json)（47） |
| `mapgen.object.place_monster[].pack_size` | 39 | array | [多绑定/拼图](../../data/json/mapgen/cabin.json)（21） |
| `mapgen.object.place_monster[].repeat` | 316 | array, int | [多绑定/拼图](../../data/json/mapgen/airport/s_airport_private.json)（0） |
| `mapgen.object.place_monster[].spawn_data` | 11 | object | [多绑定/拼图](../../data/json/mapgen/cabin.json)（21） |
| `mapgen.object.place_monster[].spawn_data.ammo` | 1 | array | [lab_barracks_turret](../../data/json/mapgen/lab/lab_floorplans_1side.json)（3） |
| `mapgen.object.place_monster[].spawn_data.ammo[].ammo_id` | 1 | string | [lab_barracks_turret](../../data/json/mapgen/lab/lab_floorplans_1side.json)（3） |
| `mapgen.object.place_monster[].spawn_data.ammo[].qty` | 1 | array | [lab_barracks_turret](../../data/json/mapgen/lab/lab_floorplans_1side.json)（3） |
| `mapgen.object.place_monster[].spawn_data.patrol` | 10 | array | [多绑定/拼图](../../data/json/mapgen/cabin.json)（21） |
| `mapgen.object.place_monster[].spawn_data.patrol[].x` | 10 | array, int | [多绑定/拼图](../../data/json/mapgen/cabin.json)（21） |
| `mapgen.object.place_monster[].spawn_data.patrol[].y` | 10 | array, int | [多绑定/拼图](../../data/json/mapgen/cabin.json)（21） |
| `mapgen.object.place_monster[].x` | 484 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.place_monster[].y` | 484 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.place_monsters` | 397 | array | [多绑定/拼图](../../data/json/mapgen/abandoned_textile_mill/abandoned_textile_mill_a.json)（0） |
| `mapgen.object.place_monsters[].chance` | 158 | int | [abstorefront_2](../../data/json/mapgen/abstorefront.json)（6） |
| `mapgen.object.place_monsters[].density` | 235 | int, number | [多绑定/拼图](../../data/json/mapgen/abandoned_textile_mill/abandoned_textile_mill_a.json)（0） |
| `mapgen.object.place_monsters[].monster` | 397 | string | [多绑定/拼图](../../data/json/mapgen/abandoned_textile_mill/abandoned_textile_mill_a.json)（0） |
| `mapgen.object.place_monsters[].repeat` | 100 | array, int | [abstorefront_2](../../data/json/mapgen/abstorefront.json)（6） |
| `mapgen.object.place_monsters[].x` | 397 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned_textile_mill/abandoned_textile_mill_a.json)（0） |
| `mapgen.object.place_monsters[].y` | 397 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned_textile_mill/abandoned_textile_mill_a.json)（0） |
| `mapgen.object.place_nested` | 1139 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.place_nested[].chunks` | 1133 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.place_nested[].chunks[].cases` | 7 | object | [多绑定/拼图](../../data/json/mapgen/microlab/microlab_firebreak.json)（0） |
| `mapgen.object.place_nested[].chunks[].cases.{key}` | 7 | string | [多绑定/拼图](../../data/json/mapgen/microlab/microlab_firebreak.json)（0） |
| `mapgen.object.place_nested[].chunks[].switch` | 7 | object | [多绑定/拼图](../../data/json/mapgen/microlab/microlab_firebreak.json)（0） |
| `mapgen.object.place_nested[].chunks[].switch.fallback` | 7 | string | [多绑定/拼图](../../data/json/mapgen/microlab/microlab_firebreak.json)（0） |
| `mapgen.object.place_nested[].chunks[].switch.param` | 7 | string | [多绑定/拼图](../../data/json/mapgen/microlab/microlab_firebreak.json)（0） |
| `mapgen.object.place_nested[].else_chunks` | 36 | array | [多绑定/拼图](../../data/json/mapgen/farm_horse.json)（13） |
| `mapgen.object.place_nested[].flags` | 5 | object | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.east` | 4 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.north` | 4 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.north_east` | 5 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.north_west` | 5 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.south` | 4 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.south_east` | 5 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.south_west` | 5 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags.west` | 4 | array | [road_straight](../../data/json/mapgen/road.json)（3） |
| `mapgen.object.place_nested[].flags_any` | 15 | object | [24x24_marked_crosswalk_and_lights](../../data/json/mapgen/nested/road_nested.json)（0） |
| `mapgen.object.place_nested[].flags_any.east` | 13 | array | [24x24_marked_crosswalks](../../data/json/mapgen/nested/road_nested.json)（5） |
| `mapgen.object.place_nested[].flags_any.north` | 10 | array | [24x24_marked_crosswalks](../../data/json/mapgen/nested/road_nested.json)（5） |
| `mapgen.object.place_nested[].flags_any.north_east` | 13 | array | [24x24_marked_crosswalks](../../data/json/mapgen/nested/road_nested.json)（5） |
| `mapgen.object.place_nested[].flags_any.north_west` | 13 | array | [24x24_marked_crosswalk_and_lights](../../data/json/mapgen/nested/road_nested.json)（0） |
| `mapgen.object.place_nested[].flags_any.south` | 10 | array | [24x24_marked_crosswalks](../../data/json/mapgen/nested/road_nested.json)（5） |
| `mapgen.object.place_nested[].flags_any.south_east` | 14 | array | [24x24_marked_crosswalks](../../data/json/mapgen/nested/road_nested.json)（5） |
| `mapgen.object.place_nested[].flags_any.south_west` | 14 | array | [24x24_marked_crosswalk_and_lights](../../data/json/mapgen/nested/road_nested.json)（0） |
| `mapgen.object.place_nested[].flags_any.west` | 13 | array | [24x24_marked_crosswalk_and_lights](../../data/json/mapgen/nested/road_nested.json)（0） |
| `mapgen.object.place_nested[].joins` | 6 | object | [ants_four_way](../../data/json/mapgen/bugs/ants.json)（11） |
| `mapgen.object.place_nested[].joins.above` | 5 | string | [ants_four_way](../../data/json/mapgen/bugs/ants.json)（11） |
| `mapgen.object.place_nested[].joins.below` | 1 | string | [mine_tunnel_end](../../data/json/mapgen/mine/mine_generic.json)（1） |
| `mapgen.object.place_nested[].joins.west` | 1 | string | [多绑定/拼图](../../data/json/mapgen/mine/mine_shaft.json)（1） |
| `mapgen.object.place_nested[].neighbors` | 90 | object | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（9） |
| `mapgen.object.place_nested[].neighbors.above` | 30 | array, string | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（9） |
| `mapgen.object.place_nested[].neighbors.east` | 34 | array, string | [crater](../../data/json/mapgen/crater.json)（5） |
| `mapgen.object.place_nested[].neighbors.east[].om_terrain` | 9 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].neighbors.east[].om_terrain_match_type` | 9 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].neighbors.north` | 27 | array, string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north[].om_terrain` | 7 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north[].om_terrain_match_type` | 7 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_east` | 26 | array, string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_east[].om_terrain` | 4 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_east[].om_terrain_match_type` | 4 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_west` | 26 | array, string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_west[].om_terrain` | 4 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.north_west[].om_terrain_match_type` | 4 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（4） |
| `mapgen.object.place_nested[].neighbors.south` | 29 | array, string | [crater](../../data/json/mapgen/crater.json)（5） |
| `mapgen.object.place_nested[].neighbors.south[].om_terrain` | 10 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].neighbors.south[].om_terrain_match_type` | 10 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].neighbors.south_east` | 27 | array, string | [crater](../../data/json/mapgen/crater.json)（5） |
| `mapgen.object.place_nested[].neighbors.south_east[].om_terrain` | 5 | string | [24x24_road_end_straight](../../data/json/mapgen/road.json)（1） |
| `mapgen.object.place_nested[].neighbors.south_east[].om_terrain_match_type` | 5 | string | [24x24_road_end_straight](../../data/json/mapgen/road.json)（1） |
| `mapgen.object.place_nested[].neighbors.south_west` | 26 | array, string | [crater](../../data/json/mapgen/crater.json)（5） |
| `mapgen.object.place_nested[].neighbors.south_west[].om_terrain` | 4 | string | [24x24_road_end_straight](../../data/json/mapgen/road.json)（1） |
| `mapgen.object.place_nested[].neighbors.south_west[].om_terrain_match_type` | 4 | string | [24x24_road_end_straight](../../data/json/mapgen/road.json)（1） |
| `mapgen.object.place_nested[].neighbors.west` | 33 | array, string | [crater](../../data/json/mapgen/crater.json)（5） |
| `mapgen.object.place_nested[].neighbors.west[].om_terrain` | 6 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].neighbors.west[].om_terrain_match_type` | 6 | string | [mx_bandits_block](../../data/json/mapgen/map_extras/bandits_block.json)（0） |
| `mapgen.object.place_nested[].predecessors` | 4 | array | [1x1_predecessor_groundcover](../../data/json/mapgen/nested/forest_trail_nested.json)（2） |
| `mapgen.object.place_nested[].repeat` | 39 | array, int | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（0） |
| `mapgen.object.place_nested[].x` | 1139 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.place_nested[].y` | 1139 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.place_npcs` | 98 | array | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_npcs[].class` | 98 | string | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_npcs[].unique_id` | 3 | string | [nest_RandEnc_RC_JohnBailey_add](../../data/json/encounters/randenc_refugee_center.json)（6） |
| `mapgen.object.place_npcs[].x` | 98 | array, int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_npcs[].y` | 98 | array, int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_rubble` | 17 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（1） |
| `mapgen.object.place_rubble[].items` | 4 | bool | [多绑定/拼图](../../data/json/mapgen/cabin.json)（2） |
| `mapgen.object.place_rubble[].repeat` | 9 | array | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（4） |
| `mapgen.object.place_rubble[].rubble_type` | 2 | string | [destroyed_furniture](../../data/json/mapgen/nested/aux_nested.json)（29） |
| `mapgen.object.place_rubble[].x` | 17 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（1） |
| `mapgen.object.place_rubble[].y` | 17 | array, int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（1） |
| `mapgen.object.place_signs` | 127 | array | [cemetery_small](../../data/json/mapgen/cemetery_small.json)（1） |
| `mapgen.object.place_signs[].signage` | 115 | string | [cemetery_small](../../data/json/mapgen/cemetery_small.json)（1） |
| `mapgen.object.place_signs[].snippet` | 16 | string | [lab_security_z-1](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（3） |
| `mapgen.object.place_signs[].x` | 127 | array, int | [cemetery_small](../../data/json/mapgen/cemetery_small.json)（1） |
| `mapgen.object.place_signs[].y` | 127 | array, int | [cemetery_small](../../data/json/mapgen/cemetery_small.json)（1） |
| `mapgen.object.place_ter_furn_transforms` | 15 | array | [1x1_remove_window](../../data/json/mapgen/map_extras/house_wasp.json)（2） |
| `mapgen.object.place_ter_furn_transforms[].transform` | 15 | string | [1x1_remove_window](../../data/json/mapgen/map_extras/house_wasp.json)（2） |
| `mapgen.object.place_ter_furn_transforms[].x` | 15 | int | [1x1_remove_window](../../data/json/mapgen/map_extras/house_wasp.json)（2） |
| `mapgen.object.place_ter_furn_transforms[].y` | 15 | int | [1x1_remove_window](../../data/json/mapgen/map_extras/house_wasp.json)（2） |
| `mapgen.object.place_terrain` | 54 | array | [lab_north_wall](../../data/json/mapgen/lab/lab_common.json)（4） |
| `mapgen.object.place_terrain[].ter` | 54 | string | [lab_north_wall](../../data/json/mapgen/lab/lab_common.json)（4） |
| `mapgen.object.place_terrain[].x` | 54 | int | [lab_north_wall](../../data/json/mapgen/lab/lab_common.json)（4） |
| `mapgen.object.place_terrain[].y` | 54 | int | [lab_north_wall](../../data/json/mapgen/lab/lab_common.json)（4） |
| `mapgen.object.place_toilets` | 17 | array | [house_03](../../data/json/mapgen/house/house03.json)（2） |
| `mapgen.object.place_toilets[].x` | 17 | int | [house_03](../../data/json/mapgen/house/house03.json)（2） |
| `mapgen.object.place_toilets[].y` | 17 | int | [house_03](../../data/json/mapgen/house/house03.json)（2） |
| `mapgen.object.place_traps` | 35 | array | [house_detatched9](../../data/json/mapgen/house/house_detatched9.json)（0） |
| `mapgen.object.place_traps[].repeat` | 15 | array, int | [多绑定/拼图](../../data/json/mapgen/lab/lab_modular/lab_1x1_security.json)（0） |
| `mapgen.object.place_traps[].trap` | 35 | string | [house_detatched9](../../data/json/mapgen/house/house_detatched9.json)（0） |
| `mapgen.object.place_traps[].x` | 35 | array, int | [house_detatched9](../../data/json/mapgen/house/house_detatched9.json)（0） |
| `mapgen.object.place_traps[].y` | 35 | array, int | [house_detatched9](../../data/json/mapgen/house/house_detatched9.json)（0） |
| `mapgen.object.place_variables` | 1 | array | [多绑定/拼图](../../data/json/mapgen/refugee_center/refugee_center.json)（3） |
| `mapgen.object.place_variables[].name` | 1 | string | [多绑定/拼图](../../data/json/mapgen/refugee_center/refugee_center.json)（3） |
| `mapgen.object.place_variables[].x` | 1 | int | [多绑定/拼图](../../data/json/mapgen/refugee_center/refugee_center.json)（3） |
| `mapgen.object.place_variables[].y` | 1 | int | [多绑定/拼图](../../data/json/mapgen/refugee_center/refugee_center.json)（3） |
| `mapgen.object.place_vehicles` | 483 | array | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].chance` | 483 | int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].faction` | 3 | string | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].fuel` | 78 | int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].repeat` | 27 | array, int | [多绑定/拼图](../../data/json/mapgen/city_blocks/urban_13_dense_house_apt_house.json)（0） |
| `mapgen.object.place_vehicles[].rotation` | 356 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_vehicles[].status` | 250 | int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（11） |
| `mapgen.object.place_vehicles[].vehicle` | 483 | string | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].x` | 483 | array, int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vehicles[].y` | 483 | array, int | [nest_RandEnc_roadstop_a_add](../../data/json/encounters/randenc_caravans.json)（1） |
| `mapgen.object.place_vendingmachines` | 9 | array | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（1） |
| `mapgen.object.place_vendingmachines[].item_group` | 8 | string | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（1） |
| `mapgen.object.place_vendingmachines[].lootable` | 9 | bool | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（1） |
| `mapgen.object.place_vendingmachines[].x` | 9 | array, int | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（1） |
| `mapgen.object.place_vendingmachines[].y` | 9 | int | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（1） |
| `mapgen.object.place_zones` | 50 | array | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.place_zones[].faction` | 50 | string | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.place_zones[].filter` | 10 | string | [多绑定/拼图](../../data/json/mapgen/bunker_shop.json)（1） |
| `mapgen.object.place_zones[].repeat` | 1 | array | [godco_permanent_trader_predatory](../../data/json/mapgen/godco/nested.json)（15） |
| `mapgen.object.place_zones[].type` | 50 | string | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.place_zones[].x` | 50 | array, int | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.place_zones[].y` | 50 | array, int | [多绑定/拼图](../../data/json/mapgen/animalshelter.json)（8） |
| `mapgen.object.predecessor_mapgen` | 134 | string | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（0） |
| `mapgen.object.remove_all` | 10 | object | [多绑定/拼图](../../data/json/mapgen/farm_tiles.json)（26） |
| `mapgen.object.remove_all.{key}` | 10 | object | [多绑定/拼图](../../data/json/mapgen/farm_tiles.json)（26） |
| `mapgen.object.remove_npcs` | 10 | array | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_npcs[].class` | 10 | string | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_npcs[].unique_id` | 1 | string | [nest_RandEnc_RC_JohnBailey_remove](../../data/json/encounters/randenc_refugee_center.json)（7） |
| `mapgen.object.remove_npcs[].x` | 10 | int | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_npcs[].y` | 10 | int | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_vehicles` | 4 | array | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_vehicles[].vehicles` | 4 | array | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_vehicles[].x` | 4 | array | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.remove_vehicles[].y` | 4 | array | [nest_RandEnc_roadstop_a_remove](../../data/json/encounters/randenc_caravans.json)（2） |
| `mapgen.object.rotation` | 1040 | array, int | [abandonedwarehouse](../../data/json/mapgen/abandoned_warehouse.json)（1） |
| `mapgen.object.rows` | 4455 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.rubble` | 3 | object | [多绑定/拼图](../../data/json/mapgen/house/urban_2_house_dd.json)（0） |
| `mapgen.object.rubble.{key}` | 3 | object | [多绑定/拼图](../../data/json/mapgen/house/urban_2_house_dd.json)（0） |
| `mapgen.object.rubble.{key}.rubble_type` | 3 | string | [多绑定/拼图](../../data/json/mapgen/house/urban_2_house_dd.json)（0） |
| `mapgen.object.sealed_item` | 68 | object | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.sealed_item.{key}` | 68 | object | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.sealed_item.{key}.chance` | 19 | int | [多绑定/拼图](../../data/json/mapgen/cs_gardening_allotment.json)（1） |
| `mapgen.object.sealed_item.{key}.furniture` | 68 | string | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.sealed_item.{key}.item` | 55 | object | [多绑定/拼图](../../data/json/mapgen/basement/basement_weed.json)（2） |
| `mapgen.object.sealed_item.{key}.item.chance` | 3 | int | [多绑定/拼图](../../data/json/mapgen/farm_dairy_2.json)（0） |
| `mapgen.object.sealed_item.{key}.item.item` | 55 | string | [多绑定/拼图](../../data/json/mapgen/basement/basement_weed.json)（2） |
| `mapgen.object.sealed_item.{key}.items` | 13 | object | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.sealed_item.{key}.items.chance` | 13 | int | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.sealed_item.{key}.items.item` | 13 | string | [desolatebarn](../../data/json/mapgen/abandoned_barn.json)（2） |
| `mapgen.object.set` | 374 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].amount` | 15 | array, int | [多绑定/拼图](../../data/json/mapgen/hazardous_waste_sarcophagus.json)（0） |
| `mapgen.object.set[].chance` | 8 | int | [dumpsite](../../data/json/mapgen/dumpsite.json)（1） |
| `mapgen.object.set[].id` | 344 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].line` | 76 | string | [fbmh_trench_north](../../data/json/mapgen/basecamps/base/modular_hub/version_1/modular_field_defenses.json)（0） |
| `mapgen.object.set[].point` | 270 | string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].repeat` | 43 | array | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].square` | 54 | string | [多绑定/拼图](../../data/json/mapgen/hazardous_waste_sarcophagus.json)（0） |
| `mapgen.object.set[].x` | 374 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].x2` | 128 | int | [fbmh_trench_north](../../data/json/mapgen/basecamps/base/modular_hub/version_1/modular_field_defenses.json)（0） |
| `mapgen.object.set[].y` | 374 | array, int | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.set[].y2` | 128 | int | [fbmh_trench_north](../../data/json/mapgen/basecamps/base/modular_hub/version_1/modular_field_defenses.json)（0） |
| `mapgen.object.signs` | 14 | object | [多绑定/拼图](../../data/json/mapgen/aircraft_carrier/aircraft_carrier_z-1.json)（0） |
| `mapgen.object.signs.{key}` | 10 | object | [多绑定/拼图](../../data/json/mapgen/cemetery_4square.json)（2） |
| `mapgen.object.signs.{key}.furniture` | 1 | string | [多绑定/拼图](../../data/json/mapgen/missile_silo.json)（0） |
| `mapgen.object.signs.{key}.signage` | 10 | string | [多绑定/拼图](../../data/json/mapgen/cemetery_4square.json)（2） |
| `mapgen.object.ter_furn_transforms` | 2 | object | [mx_clearcut](../../data/json/mapgen/map_extras/clearcut.json)（0） |
| `mapgen.object.ter_furn_transforms.{key}` | 2 | object | [mx_clearcut](../../data/json/mapgen/map_extras/clearcut.json)（0） |
| `mapgen.object.ter_furn_transforms.{key}.transform` | 2 | string | [mx_clearcut](../../data/json/mapgen/map_extras/clearcut.json)（0） |
| `mapgen.object.terrain` | 2267 | object | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.terrain.{key}` | 2209 | array, object, string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.object.terrain.{key}.cases` | 2 | object | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.terrain.{key}.cases.{key}` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.terrain.{key}.fallback` | 24 | string | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（0） |
| `mapgen.object.terrain.{key}.param` | 25 | string | [多绑定/拼图](../../data/json/mapgen/apartment_complex/apartment_complex_other.json)（0） |
| `mapgen.object.terrain.{key}.switch` | 2 | object | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.terrain.{key}.switch.fallback` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.terrain.{key}.switch.param` | 2 | string | [多绑定/拼图](../../data/json/mapgen/fort.json)（1） |
| `mapgen.object.toilets` | 200 | object | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（10） |
| `mapgen.object.toilets.{key}` | 200 | object | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（10） |
| `mapgen.object.translate_ter` | 4 | array | [LMOE_unlock_door](../../data/json/npcs/Backgrounds/prepper_1.json)（50） |
| `mapgen.object.translate_ter[].from` | 4 | string | [LMOE_unlock_door](../../data/json/npcs/Backgrounds/prepper_1.json)（50） |
| `mapgen.object.translate_ter[].to` | 4 | string | [LMOE_unlock_door](../../data/json/npcs/Backgrounds/prepper_1.json)（50） |
| `mapgen.object.translate_ter[].x` | 4 | array, int | [LMOE_unlock_door](../../data/json/npcs/Backgrounds/prepper_1.json)（50） |
| `mapgen.object.translate_ter[].y` | 4 | array, int | [LMOE_unlock_door](../../data/json/npcs/Backgrounds/prepper_1.json)（50） |
| `mapgen.object.traps` | 31 | object | [多绑定/拼图](../../data/json/mapgen/bugs/spider_pit.json)（0） |
| `mapgen.object.traps.{key}` | 31 | array, object, string | [多绑定/拼图](../../data/json/mapgen/bugs/spider_pit.json)（0） |
| `mapgen.object.traps.{key}.trap` | 2 | string | [mx_Trapdoor_spider_den](../../data/json/mapgen/map_extras/trapdoor_spider_den.json)（0） |
| `mapgen.object.vehicles` | 60 | object | [多绑定/拼图](../../data/json/mapgen/boxing.json)（0） |
| `mapgen.object.vehicles.{key}` | 60 | object | [多绑定/拼图](../../data/json/mapgen/boxing.json)（0） |
| `mapgen.object.vehicles.{key}.chance` | 60 | int | [多绑定/拼图](../../data/json/mapgen/boxing.json)（0） |
| `mapgen.object.vehicles.{key}.fuel` | 6 | int | [多绑定/拼图](../../data/json/mapgen/cave.json)（12） |
| `mapgen.object.vehicles.{key}.rotation` | 40 | int | [多绑定/拼图](../../data/json/mapgen/boxing.json)（0） |
| `mapgen.object.vehicles.{key}.status` | 21 | int | [多绑定/拼图](../../data/json/mapgen/bunker.json)（2） |
| `mapgen.object.vehicles.{key}.vehicle` | 60 | string | [多绑定/拼图](../../data/json/mapgen/boxing.json)（0） |
| `mapgen.object.vendingmachines` | 49 | object | [多绑定/拼图](../../data/json/mapgen/bowling_alley.json)（0） |
| `mapgen.object.vendingmachines.{key}` | 49 | object | [多绑定/拼图](../../data/json/mapgen/bowling_alley.json)（0） |
| `mapgen.object.vendingmachines.{key}.item_group` | 47 | string | [多绑定/拼图](../../data/json/mapgen/bowling_alley.json)（0） |
| `mapgen.object.vendingmachines.{key}.lootable` | 44 | bool | [多绑定/拼图](../../data/json/mapgen/bowling_alley.json)（0） |
| `mapgen.om_terrain` | 2628 | array, string | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.type` | 5650 | string | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.update_mapgen_id` | 748 | string | [SCENARIO_BLOOD](../../data/json/effects_on_condition/scenario_specific_eocs.json)（14） |
| `mapgen.weight` | 1625 | int, object | [多绑定/拼图](../../data/json/mapgen/abandoned01.json)（7） |
| `mapgen.weight.default` | 4 | int | [多绑定/拼图](../../data/json/mapgen/bridges.json)（2） |
| `mapgen.weight.global_val` | 4 | string | [多绑定/拼图](../../data/json/mapgen/bridges.json)（2） |

## 4、palette全部显式字段路径

归一化字段路径164种。

| 字段路径 | 声明数 | 实际类型 | 原版实例（声明序号） |
|---|---:|---|---|
| `palette.computers` | 7 | object | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}` | 7 | object | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.access_denied` | 1 | string | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.failures` | 5 | array | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.failures[].action` | 5 | string | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.name` | 7 | string | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.options` | 7 | array | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.options[].action` | 7 | string | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.options[].name` | 7 | string | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.options[].security` | 3 | int | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.computers.{key}.security` | 5 | int | [lab_loot_bionic_vault](../../data/json/mapgen/lab/lab_floorplan_cross.json)（16） |
| `palette.fields` | 2 | object | [nether_monster_palette](../../data/json/mapgen_palettes/nether_monster_palette.json)（0） |
| `palette.fields.{key}` | 2 | object | [nether_monster_palette](../../data/json/mapgen_palettes/nether_monster_palette.json)（0） |
| `palette.fields.{key}.age` | 1 | int | [nuclear_plant_palette](../../data/json/mapgen_palettes/nuclear_plant_palette.json)（0） |
| `palette.fields.{key}.field` | 2 | string | [nether_monster_palette](../../data/json/mapgen_palettes/nether_monster_palette.json)（0） |
| `palette.fields.{key}.intensity` | 2 | int | [nether_monster_palette](../../data/json/mapgen_palettes/nether_monster_palette.json)（0） |
| `palette.furniture` | 358 | object | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.furniture.{key}` | 299 | array, object, string | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.furniture.{key}.cases` | 3 | object | [apt_complex_ground](../../data/json/mapgen_palettes/apartment_complex.json)（1） |
| `palette.furniture.{key}.cases.{key}` | 3 | string | [apt_complex_ground](../../data/json/mapgen_palettes/apartment_complex.json)（1） |
| `palette.furniture.{key}.fallback` | 6 | string | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.furniture.{key}.param` | 6 | string | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.furniture.{key}.switch` | 3 | object | [apt_complex_ground](../../data/json/mapgen_palettes/apartment_complex.json)（1） |
| `palette.furniture.{key}.switch.fallback` | 3 | string | [apt_complex_ground](../../data/json/mapgen_palettes/apartment_complex.json)（1） |
| `palette.furniture.{key}.switch.param` | 3 | string | [apt_complex_ground](../../data/json/mapgen_palettes/apartment_complex.json)（1） |
| `palette.gaspumps` | 2 | object | [speedway_palette](../../data/json/mapgen/speedway.json)（0） |
| `palette.gaspumps.{key}` | 2 | object | [speedway_palette](../../data/json/mapgen/speedway.json)（0） |
| `palette.gaspumps.{key}.fuel` | 1 | string | [speedway_palette](../../data/json/mapgen/speedway.json)（0） |
| `palette.id` | 425 | string | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.item` | 24 | object | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}` | 24 | array, object | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}.chance` | 13 | int | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}.item` | 22 | string | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}.repeat` | 8 | array | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}[].chance` | 8 | int | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}[].charges` | 1 | array | [police_dept](../../data/json/mapgen_palettes/police_dept_palette.json)（0） |
| `palette.item.{key}[].item` | 8 | string | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.item.{key}[].repeat` | 6 | array | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.items` | 124 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.items.{key}` | 124 | array, object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.items.{key}.chance` | 113 | int | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.items.{key}.item` | 113 | object, string | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.items.{key}.item.entries` | 4 | array | [gun_store_palette](../../data/json/mapgen_palettes/gunstore.json)（0） |
| `palette.items.{key}.item.entries[].collection` | 3 | array | [mil_surplus_intact](../../data/json/mapgen_palettes/mil_surplus.json)（1） |
| `palette.items.{key}.item.entries[].collection[].count` | 3 | array | [mil_surplus_intact](../../data/json/mapgen_palettes/mil_surplus.json)（1） |
| `palette.items.{key}.item.entries[].collection[].item` | 3 | string | [mil_surplus_intact](../../data/json/mapgen_palettes/mil_surplus.json)（1） |
| `palette.items.{key}.item.entries[].count` | 3 | array | [mil_surplus_intact](../../data/json/mapgen_palettes/mil_surplus.json)（1） |
| `palette.items.{key}.item.entries[].group` | 4 | string | [gun_store_palette](../../data/json/mapgen_palettes/gunstore.json)（0） |
| `palette.items.{key}.item.entries[].item` | 3 | string | [mil_surplus_intact](../../data/json/mapgen_palettes/mil_surplus.json)（1） |
| `palette.items.{key}.item.entries[].prob` | 4 | int | [gun_store_palette](../../data/json/mapgen_palettes/gunstore.json)（0） |
| `palette.items.{key}.item.entries[].variant` | 2 | string | [mil_surplus_looted](../../data/json/mapgen_palettes/mil_surplus.json)（2） |
| `palette.items.{key}.item.subtype` | 4 | string | [gun_store_palette](../../data/json/mapgen_palettes/gunstore.json)（0） |
| `palette.items.{key}.repeat` | 86 | array, int | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.items.{key}[].ammo` | 4 | int | [basement_empty](../../data/json/mapgen_palettes/basement.json)（3） |
| `palette.items.{key}[].chance` | 81 | int | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.items.{key}[].custom-flags` | 1 | array | [aircraft_carrier_palette](../../data/json/mapgen_palettes/aircraft_carrier_palette.json)（0） |
| `palette.items.{key}[].item` | 81 | object, string | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.items.{key}[].item.entries` | 1 | array | [p_resort_palette_main_floor](../../data/json/mapgen_palettes/private_resort.json)（1） |
| `palette.items.{key}[].item.entries[].group` | 1 | string | [p_resort_palette_main_floor](../../data/json/mapgen_palettes/private_resort.json)（1） |
| `palette.items.{key}[].item.entries[].prob` | 1 | int | [p_resort_palette_main_floor](../../data/json/mapgen_palettes/private_resort.json)（1） |
| `palette.items.{key}[].item.subtype` | 1 | string | [p_resort_palette_main_floor](../../data/json/mapgen_palettes/private_resort.json)（1） |
| `palette.items.{key}[].magazine` | 4 | int | [basement_empty](../../data/json/mapgen_palettes/basement.json)（3） |
| `palette.items.{key}[].repear` | 2 | array | [standard_domestic_untidy_palette](../../data/json/mapgen_palettes/house_general_palette.json)（10） |
| `palette.items.{key}[].repeat` | 67 | array, int | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.liquids` | 19 | object | [basement_utility_nest_palette](../../data/json/mapgen/nested/basement_nested.json)（7） |
| `palette.liquids.{key}` | 19 | object | [basement_utility_nest_palette](../../data/json/mapgen/nested/basement_nested.json)（7） |
| `palette.liquids.{key}.amount` | 19 | array | [basement_utility_nest_palette](../../data/json/mapgen/nested/basement_nested.json)（7） |
| `palette.liquids.{key}.liquid` | 19 | string | [basement_utility_nest_palette](../../data/json/mapgen/nested/basement_nested.json)（7） |
| `palette.mapping` | 12 | object | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.mapping.{key}` | 12 | object | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.mapping.{key}.furniture` | 3 | array, string | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.item` | 8 | array, object | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.mapping.{key}.item.chance` | 5 | int | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.mapping.{key}.item.item` | 5 | string | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.mapping.{key}.item.repeat` | 2 | array | [fort_palette](../../data/json/mapgen_palettes/fort_palette.json)（1） |
| `palette.mapping.{key}.item[].chance` | 3 | int | [lab_loot_research](../../data/json/mapgen/lab/lab_common.json)（1） |
| `palette.mapping.{key}.item[].item` | 3 | string | [lab_loot_research](../../data/json/mapgen/lab/lab_common.json)（1） |
| `palette.mapping.{key}.items` | 7 | array, object | [lab_loot_research](../../data/json/mapgen/lab/lab_common.json)（1） |
| `palette.mapping.{key}.items.chance` | 3 | int | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.items.item` | 3 | string | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.items.repeat` | 2 | array | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.items[].chance` | 5 | int | [lab_loot_research](../../data/json/mapgen/lab/lab_common.json)（1） |
| `palette.mapping.{key}.items[].item` | 5 | string | [lab_loot_research](../../data/json/mapgen/lab/lab_common.json)（1） |
| `palette.mapping.{key}.items[].repeat` | 2 | array, int | [lab_loot_home_office](../../data/json/mapgen/lab/lab_common.json)（2） |
| `palette.mapping.{key}.liquids` | 1 | object | [exodii_palette](../../data/json/mapgen_palettes/exodii/homebase.json)（0） |
| `palette.mapping.{key}.liquids.amount` | 1 | array | [exodii_palette](../../data/json/mapgen_palettes/exodii/homebase.json)（0） |
| `palette.mapping.{key}.liquids.liquid` | 1 | string | [exodii_palette](../../data/json/mapgen_palettes/exodii/homebase.json)（0） |
| `palette.mapping.{key}.terrain` | 2 | object, string | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.terrain.fallback` | 1 | string | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.terrain.param` | 1 | string | [motel_twd_palette](../../data/json/mapgen/motel.json)（16） |
| `palette.mapping.{key}.toilets` | 1 | object | [fort_palette](../../data/json/mapgen_palettes/fort_palette.json)（1） |
| `palette.mapping.{key}.traps` | 2 | array, string | [homeless_palette](../../data/json/mapgen/homeless_shelter.json)（0） |
| `palette.monster` | 25 | object | [car_theater_full](../../data/json/mapgen/drive-in_theater.json)（6） |
| `palette.monster.{key}` | 25 | array, object | [car_theater_full](../../data/json/mapgen/drive-in_theater.json)（6） |
| `palette.monster.{key}.chance` | 22 | int | [car_theater_full](../../data/json/mapgen/drive-in_theater.json)（6） |
| `palette.monster.{key}.group` | 10 | string | [car_theater_full](../../data/json/mapgen/drive-in_theater.json)（6） |
| `palette.monster.{key}.monster` | 16 | string | [cave_palette](../../data/json/mapgen/nested/cave_nested.json)（0） |
| `palette.monster.{key}.pack_size` | 1 | array | [nuclear_plant_palette](../../data/json/mapgen_palettes/nuclear_plant_palette.json)（0） |
| `palette.monster.{key}.spawn_data` | 1 | object | [lab_security_palette](../../data/json/mapgen_palettes/lab/lab_modular_palette.json)（3） |
| `palette.monster.{key}.spawn_data.ammo` | 1 | array | [lab_security_palette](../../data/json/mapgen_palettes/lab/lab_modular_palette.json)（3） |
| `palette.monster.{key}.spawn_data.ammo[].ammo_id` | 1 | string | [lab_security_palette](../../data/json/mapgen_palettes/lab/lab_modular_palette.json)（3） |
| `palette.monster.{key}.spawn_data.ammo[].qty` | 1 | array | [lab_security_palette](../../data/json/mapgen_palettes/lab/lab_modular_palette.json)（3） |
| `palette.monster.{key}[].chance` | 3 | int | [microlab_meat](../../data/json/mapgen_palettes/microlab.json)（2） |
| `palette.monster.{key}[].group` | 1 | string | [microlab_meat](../../data/json/mapgen_palettes/microlab.json)（2） |
| `palette.monster.{key}[].monster` | 3 | string | [microlab_meat](../../data/json/mapgen_palettes/microlab.json)（2） |
| `palette.monsters` | 2 | object | [paddock](../../data/json/mapgen_palettes/farm_horse.json)（1） |
| `palette.monsters.{key}` | 2 | object | [paddock](../../data/json/mapgen_palettes/farm_horse.json)（1） |
| `palette.monsters.{key}.chance` | 1 | int | [paddock](../../data/json/mapgen_palettes/farm_horse.json)（1） |
| `palette.monsters.{key}.density` | 2 | number | [paddock](../../data/json/mapgen_palettes/farm_horse.json)（1） |
| `palette.monsters.{key}.monster` | 2 | string | [paddock](../../data/json/mapgen_palettes/farm_horse.json)（1） |
| `palette.nested` | 49 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.nested.{key}` | 49 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.nested.{key}.chunks` | 49 | array | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.npcs` | 1 | object | [shelter_survivor](../../data/json/mapgen_palettes/shelter.json)（3） |
| `palette.npcs.{key}` | 1 | object | [shelter_survivor](../../data/json/mapgen_palettes/shelter.json)（3） |
| `palette.npcs.{key}.class` | 1 | string | [shelter_survivor](../../data/json/mapgen_palettes/shelter.json)（3） |
| `palette.palettes` | 25 | array | [car_theater_full](../../data/json/mapgen/drive-in_theater.json)（6） |
| `palette.palettes[].distribution` | 2 | array | [convention_palette](../../data/json/mapgen_palettes/convention_center_palette.json)（0） |
| `palette.palettes[].param` | 4 | string | [restaurant_palette](../../data/json/mapgen/restaurant.json)（3） |
| `palette.parameters` | 30 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.parameters.{key}` | 30 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.parameters.{key}.default` | 30 | object | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.parameters.{key}.default.distribution` | 30 | array | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.parameters.{key}.scope` | 3 | string | [domestic_general_and_variant_palette](../../data/json/mapgen_palettes/house_general_palette.json)（0） |
| `palette.parameters.{key}.type` | 30 | string | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.remove_all` | 6 | object | [microlab_distorted_chunk](../../data/json/mapgen/microlab/microlab_distorted/microlab_distorted_chunks.json)（0） |
| `palette.remove_all.{key}` | 6 | object | [microlab_distorted_chunk](../../data/json/mapgen/microlab/microlab_distorted/microlab_distorted_chunks.json)（0） |
| `palette.sealed_item` | 9 | object | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.sealed_item.{key}` | 9 | object | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.sealed_item.{key}.chance` | 3 | int | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.sealed_item.{key}.furniture` | 9 | string | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.sealed_item.{key}.item` | 9 | object | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.sealed_item.{key}.item.item` | 9 | string | [godco_camp](../../data/json/mapgen_palettes/church_retreat.json)（0） |
| `palette.signs` | 3 | object | [road_palette](../../data/json/mapgen_palettes/road.json)（0） |
| `palette.signs.{key}` | 3 | object | [road_palette](../../data/json/mapgen_palettes/road.json)（0） |
| `palette.signs.{key}.furniture` | 1 | string | [road_palette](../../data/json/mapgen_palettes/road.json)（0） |
| `palette.signs.{key}.signage` | 3 | string | [road_palette](../../data/json/mapgen_palettes/road.json)（0） |
| `palette.terrain` | 388 | object | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.terrain.{key}` | 368 | array, object, string | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.terrain.{key}.cases` | 5 | object | [derelict_palette](../../data/json/mapgen/derelict_property.json)（0） |
| `palette.terrain.{key}.cases.{key}` | 5 | string | [derelict_palette](../../data/json/mapgen/derelict_property.json)（0） |
| `palette.terrain.{key}.fallback` | 21 | string | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.terrain.{key}.param` | 22 | string | [abwarehouse_palette](../../data/json/mapgen/abandoned_warehouse.json)（0） |
| `palette.terrain.{key}.switch` | 5 | object | [derelict_palette](../../data/json/mapgen/derelict_property.json)（0） |
| `palette.terrain.{key}.switch.fallback` | 5 | string | [derelict_palette](../../data/json/mapgen/derelict_property.json)（0） |
| `palette.terrain.{key}.switch.param` | 5 | string | [derelict_palette](../../data/json/mapgen/derelict_property.json)（0） |
| `palette.terrain.{key}[][].fallback` | 1 | string | [cabin_palette_abandoned](../../data/json/mapgen_palettes/cabin.json)（1） |
| `palette.terrain.{key}[][].param` | 1 | string | [cabin_palette_abandoned](../../data/json/mapgen_palettes/cabin.json)（1） |
| `palette.toilets` | 99 | object | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.toilets.{key}` | 99 | object | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.toilets.{key}.amount` | 1 | array | [FEMA_camp](../../data/json/mapgen_palettes/fema.json)（0） |
| `palette.traps` | 4 | object | [homelesscamp_palette](../../data/json/mapgen/homeless_camp.json)（0） |
| `palette.traps.{key}` | 4 | array, string | [homelesscamp_palette](../../data/json/mapgen/homeless_camp.json)（0） |
| `palette.type` | 425 | string | [shoppingplaza](../../data/json/mapgen/abandoned_shopping_plaza.json)（0） |
| `palette.vehicles` | 21 | object | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.vehicles.{key}` | 21 | object | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.vehicles.{key}.chance` | 21 | int | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.vehicles.{key}.rotation` | 19 | array, int | [dive_shop_palette](../../data/json/mapgen/dive_shop.json)（2） |
| `palette.vehicles.{key}.status` | 1 | int | [aircraft_carrier_palette](../../data/json/mapgen_palettes/aircraft_carrier_palette.json)（0） |
| `palette.vehicles.{key}.vehicle` | 21 | string | [abstorefront_palette](../../data/json/mapgen/abstorefront.json)（0） |
| `palette.vendingmachines` | 36 | object | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.vendingmachines.{key}` | 36 | object | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.vendingmachines.{key}.item_group` | 33 | string | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |
| `palette.vendingmachines.{key}.lootable` | 23 | bool | [dispensary_palette](../../data/json/mapgen/dispensary.json)（0） |

## 5、terrain全部显式字段路径

归一化字段路径143种。

| 字段路径 | 声明数 | 实际类型 | 原版实例（声明序号） |
|---|---:|---|---|
| `terrain.alias` | 91 | array, string | [t_fence](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（15） |
| `terrain.allowed_template_ids` | 1 | array | [t_nanofab](../../data/json/furniture_and_terrain/terrain-manufactured.json)（24） |
| `terrain.bash` | 790 | object | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.bash_below` | 62 | bool | [t_brick_floor](../../data/json/furniture_and_terrain/terrain-floors-indoor.json)（7） |
| `terrain.bash.explosive` | 13 | int | [t_gas_pump_smashed](../../data/json/furniture_and_terrain/terrain-manufactured.json)（3） |
| `terrain.bash.items` | 701 | array, string | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.items[].charges` | 153 | array | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.items[].count` | 686 | array, int | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.items[].group` | 2 | string | [t_soil](../../data/json/furniture_and_terrain/terrain-walls.json)（112） |
| `terrain.bash.items[].item` | 685 | string | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.items[].prob` | 121 | int | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.bash.sound` | 764 | string | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.sound_fail` | 689 | string | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.sound_fail_vol` | 134 | int | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.bash.sound_vol` | 134 | int | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.bash.str_max` | 790 | int | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.str_max_blocked` | 59 | int | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.bash.str_min` | 790 | int | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.str_min_blocked` | 59 | int | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.bash.str_min_supported` | 102 | int | [t_thconc_floor_flesh](../../data/json/furniture_and_terrain/terrain-flesh.json)（0） |
| `terrain.bash.ter_set` | 790 | string | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.bash.ter_set_bashed_from_above` | 2 | string | [t_soil](../../data/json/furniture_and_terrain/terrain-walls.json)（112） |
| `terrain.boltcut` | 5 | object | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.byproducts` | 5 | array | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.byproducts[].count` | 5 | int | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.byproducts[].item` | 5 | string | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.duration` | 5 | string | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.result` | 5 | string | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.boltcut.sound` | 5 | string | [t_chaingate_l](../../data/json/furniture_and_terrain/terrain-fences-gates.json)（3） |
| `terrain.close` | 85 | string | [t_bullettrailer_swall_door_o](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（13） |
| `terrain.color` | 1001 | array, string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.comfort` | 7 | int | [t_floor](../../data/json/furniture_and_terrain/terrain-floors-indoor.json)（23） |
| `terrain.connect_groups` | 181 | array, string | [t_pavement_bg_dp](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（8） |
| `terrain.connects_to` | 193 | array, string | [t_pavement_bg_dp](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（8） |
| `terrain.copy-from` | 91 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.coverage` | 435 | int | [t_bullettrailer_inner_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（23） |
| `terrain.curtain_transform` | 45 | string | [t_window_domestic](../../data/json/furniture_and_terrain/terrain-windows.json)（2） |
| `terrain.deconstruct` | 253 | object | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.deconstruct.deconstruct_above` | 2 | bool | [t_wood_stairs_up_half](../../data/json/furniture_and_terrain/terrain-zlevel-transitions.json)（1） |
| `terrain.deconstruct.items` | 253 | array | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.deconstruct.items[].charges` | 168 | array, int | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.deconstruct.items[].count` | 215 | array, int | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.deconstruct.items[].item` | 253 | string | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.deconstruct.items[].prob` | 1 | int | [t_conveyor](../../data/json/furniture_and_terrain/terrain-manufactured.json)（41） |
| `terrain.deconstruct.ter_set` | 253 | string | [t_dock](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（1） |
| `terrain.description` | 984 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.emissions` | 7 | array | [t_strconc_floor_glimmer](../../data/json/furniture_and_terrain/terrain-floors-indoor.json)（15） |
| `terrain.examine_action` | 262 | object, string | [t_dock_deep_pile](../../data/json/furniture_and_terrain/terrain-bridges-docks.json)（2） |
| `terrain.examine_action.allow_hacking` | 13 | bool | [t_card_science_visitor](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（17） |
| `terrain.examine_action.consume_card` | 13 | bool | [t_card_science_visitor](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（17） |
| `terrain.examine_action.despawn_monsters` | 13 | bool | [t_card_science_visitor](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（17） |
| `terrain.examine_action.effect_on_conditions` | 7 | array | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.examine_action.effect_on_conditions[].condition` | 3 | object | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].condition.and` | 1 | array | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].condition.and[].u_has_items` | 1 | object | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].condition.and[].u_has_items.count` | 1 | int | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].condition.and[].u_has_items.item` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].condition.and[].u_has_mission` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].condition.u_has_trait` | 2 | string | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].effect` | 4 | array | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.examine_action.effect_on_conditions[].effect[].adjustment` | 1 | int | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].context` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].count` | 1 | int | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].finish_mission` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].popup` | 4 | bool | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.examine_action.effect_on_conditions[].effect[].success` | 1 | bool | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].type` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_adjust_var` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_consume_item` | 1 | string | [t_pit_BEM_human_sample](../../data/json/furniture_and_terrain/terrain-traps.json)（9） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_location_variable` | 2 | object | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_location_variable.u_val` | 2 | string | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_message` | 4 | string | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_teleport` | 2 | object | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].effect[].u_teleport.u_val` | 2 | string | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].effect[].z_adjust` | 2 | int | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].false_effect` | 3 | object | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].false_effect.popup` | 3 | bool | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].false_effect.u_message` | 3 | string | [t_elevator_control_robofac_up](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（34） |
| `terrain.examine_action.effect_on_conditions[].id` | 4 | string | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.examine_action.flags` | 17 | array | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.query` | 13 | bool | [t_card_science_visitor](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（17） |
| `terrain.examine_action.query_msg` | 17 | string | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.radius` | 13 | int | [t_card_science_visitor](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（17） |
| `terrain.examine_action.redundant_msg` | 17 | string | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.success_msg` | 17 | string | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.terrain_changes` | 17 | object | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.terrain_changes.{key}` | 17 | string | [t_card_science](../../data/json/furniture_and_terrain/terrain-mechanisms.json)（13） |
| `terrain.examine_action.type` | 24 | string | [t_fault](../../data/json/furniture_and_terrain/terrain-floors-outdoors.json)（10） |
| `terrain.flags` | 970 | array | [t_bullettrailer_nwall_westcorner](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（1） |
| `terrain.floor_bedding_warmth` | 3 | int | [t_pit_straw](../../data/json/furniture_and_terrain/terrain-manufactured.json)（48） |
| `terrain.hacksaw` | 37 | object | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.byproducts` | 37 | array | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.byproducts[].count` | 37 | array, int | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.byproducts[].item` | 37 | string | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.duration` | 37 | string | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.message` | 37 | string | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.hacksaw.result` | 37 | string | [t_door_bar_c](../../data/json/furniture_and_terrain/terrain-doors.json)（84） |
| `terrain.harvest_by_season` | 41 | array | [t_tree_walnut](../../data/json/furniture_and_terrain/terrain-flora.json)（0） |
| `terrain.harvest_by_season[].id` | 41 | string | [t_tree_walnut](../../data/json/furniture_and_terrain/terrain-flora.json)（0） |
| `terrain.harvest_by_season[].seasons` | 41 | array | [t_tree_walnut](../../data/json/furniture_and_terrain/terrain-flora.json)（0） |
| `terrain.heat_radiation` | 2 | int | [t_lava](../../data/json/furniture_and_terrain/terrain-liquids.json)（20） |
| `terrain.id` | 1001 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.light_emitted` | 11 | int | [t_thconc_y_olight](../../data/json/furniture_and_terrain/terrain-floors-indoor.json)（4） |
| `terrain.lockpick_message` | 9 | string | [t_door_locked_interior](../../data/json/furniture_and_terrain/terrain-doors.json)（47） |
| `terrain.lockpick_result` | 9 | string | [t_door_locked_interior](../../data/json/furniture_and_terrain/terrain-doors.json)（47） |
| `terrain.looks_like` | 678 | string | [t_bullettrailer_nwall_window](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（3） |
| `terrain.max_volume` | 1 | string | [t_recycler](../../data/json/furniture_and_terrain/terrain-manufactured.json)（0） |
| `terrain.move_cost` | 957 | int | [t_bullettrailer_swall_door_o](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（13） |
| `terrain.name` | 984 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.open` | 90 | string | [t_bullettrailer_swall_door](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（12） |
| `terrain.oxytorch` | 33 | object | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.oxytorch.byproducts` | 33 | array | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.oxytorch.byproducts[].count` | 33 | array, int | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.oxytorch.byproducts[].item` | 33 | string | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.oxytorch.duration` | 33 | string | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.oxytorch.result` | 33 | string | [t_door_metal_c](../../data/json/furniture_and_terrain/terrain-doors.json)（68） |
| `terrain.prying` | 24 | object | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.prying.byproducts` | 10 | array | [t_door_boarded](../../data/json/furniture_and_terrain/terrain-doors.json)（62） |
| `terrain.prying.byproducts[].count` | 10 | int | [t_door_boarded](../../data/json/furniture_and_terrain/terrain-doors.json)（62） |
| `terrain.prying.byproducts[].item` | 10 | string | [t_door_boarded](../../data/json/furniture_and_terrain/terrain-doors.json)（62） |
| `terrain.prying.duration` | 9 | string | [t_door_boarded](../../data/json/furniture_and_terrain/terrain-doors.json)（62） |
| `terrain.prying.message` | 24 | string | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.prying.prying_data` | 24 | object | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.prying.prying_data.alarm` | 2 | bool | [t_door_elocked_alarm](../../data/json/furniture_and_terrain/terrain-doors.json)（11） |
| `terrain.prying.prying_data.breakable` | 3 | bool | [t_window_domestic](../../data/json/furniture_and_terrain/terrain-windows.json)（2） |
| `terrain.prying.prying_data.difficulty` | 13 | int | [t_door_elocked](../../data/json/furniture_and_terrain/terrain-doors.json)（9） |
| `terrain.prying.prying_data.failure` | 13 | string | [t_door_elocked](../../data/json/furniture_and_terrain/terrain-doors.json)（9） |
| `terrain.prying.prying_data.noisy` | 12 | bool | [t_door_elocked](../../data/json/furniture_and_terrain/terrain-doors.json)（9） |
| `terrain.prying.prying_data.prying_level` | 13 | int | [t_door_elocked](../../data/json/furniture_and_terrain/terrain-doors.json)（9） |
| `terrain.prying.prying_data.prying_nails` | 9 | bool | [t_door_boarded](../../data/json/furniture_and_terrain/terrain-doors.json)（62） |
| `terrain.prying.result` | 24 | string | [t_door_c](../../data/json/furniture_and_terrain/terrain-doors.json)（8） |
| `terrain.roof` | 385 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.rotates_to` | 4 | string | [t_wall_glass](../../data/json/furniture_and_terrain/terrain-walls.json)（99） |
| `terrain.shoot` | 86 | object | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.shoot.chance_to_hit` | 21 | int | [t_door_white_b](../../data/json/furniture_and_terrain/terrain-doors.json)（21） |
| `terrain.shoot.destroy_damage` | 86 | array | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.shoot.no_laser_destroy` | 35 | bool | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.shoot.reduce_damage` | 86 | array | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.shoot.reduce_damage_laser` | 86 | array | [t_laminated_door_glass_c](../../data/json/furniture_and_terrain/terrain-doors.json)（0） |
| `terrain.symbol` | 1001 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |
| `terrain.transforms_into` | 89 | string | [t_tree_walnut](../../data/json/furniture_and_terrain/terrain-flora.json)（0） |
| `terrain.trap` | 13 | string | [t_strconc_floor_glimmer](../../data/json/furniture_and_terrain/terrain-floors-indoor.json)（15） |
| `terrain.type` | 1001 | string | [t_bullettrailer_brownfloor](../../data/json/furniture_and_terrain/special_use/bullet_trailer.json)（0） |

## 6、furniture全部显式字段路径

归一化字段路径137种。

| 字段路径 | 声明数 | 实际类型 | 原版实例（声明序号） |
|---|---:|---|---|
| `furniture.alias` | 2 | array, string | [f_punching_bag](../../data/json/furniture_and_terrain/furniture-recreation.json)（12） |
| `furniture.bash` | 544 | object | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.collapse_radius` | 8 | int | [f_large_canvas_wall](../../data/json/furniture_and_terrain/furniture-terrains.json)（12） |
| `furniture.bash.explosive` | 12 | int | [f_exodii_generator_1](../../data/json/furniture_and_terrain/furniture-alien.json)（17） |
| `furniture.bash.furn_set` | 74 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.items` | 481 | array | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.items[].charges` | 168 | array, int | [f_scrap_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（9） |
| `furniture.bash.items[].container-item` | 2 | string | [f_active_backup_generator](../../data/json/furniture_and_terrain/furniture-industrial.json)（14） |
| `furniture.bash.items[].count` | 476 | array, int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.items[].damage` | 12 | array | [f_gravelbag_half](../../data/json/furniture_and_terrain/furniture-barriers.json)（1） |
| `furniture.bash.items[].group` | 8 | string | [f_gravelbag_half](../../data/json/furniture_and_terrain/furniture-barriers.json)（1） |
| `furniture.bash.items[].item` | 480 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.items[].prob` | 59 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.items[].variant` | 1 | string | [f_battlefield_cross](../../data/json/furniture_and_terrain/furniture-graves.json)（5） |
| `furniture.bash.sound` | 521 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.sound_fail` | 542 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.sound_fail_vol` | 11 | int | [f_shower](../../data/json/furniture_and_terrain/furniture-plumbing.json)（1） |
| `furniture.bash.sound_vol` | 46 | int | [f_bigmirror](../../data/json/furniture_and_terrain/furniture-decorative.json)（0） |
| `furniture.bash.str_max` | 543 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.str_min` | 543 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.bash.tent_centers` | 19 | array | [f_canvas_wall](../../data/json/furniture_and_terrain/furniture-terrains.json)（11） |
| `furniture.bgcolor` | 69 | array, string | [f_air_conditioner](../../data/json/furniture_and_terrain/furniture-appliances.json)（0） |
| `furniture.bonus_fire_warmth_feet` | 17 | int | [f_bench](../../data/json/furniture_and_terrain/furniture-seats.json)（0） |
| `furniture.close` | 9 | string | [f_curtain_open](../../data/json/furniture_and_terrain/furniture-medical.json)（22） |
| `furniture.color` | 525 | array, string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.comfort` | 43 | int | [f_leaves_pile](../../data/json/furniture_and_terrain/furniture-flora.json)（20） |
| `furniture.connect_groups` | 24 | string | [f_hedge_short](../../data/json/furniture_and_terrain/furniture-flora.json)（31） |
| `furniture.connects_to` | 24 | string | [f_hedge_short](../../data/json/furniture_and_terrain/furniture-flora.json)（31） |
| `furniture.copy-from` | 19 | string | [f_gas_oven_microwave_combo](../../data/json/furniture_and_terrain/furniture-appliances.json)（11） |
| `furniture.coverage` | 410 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.crafting_pseudo_item` | 67 | string | [f_oven](../../data/json/furniture_and_terrain/furniture-appliances.json)（9） |
| `furniture.deconstruct` | 339 | object | [f_alien_pod_resin](../../data/json/furniture_and_terrain/furniture-alien.json)（7） |
| `furniture.deconstruct.furn_set` | 43 | string | [f_gas_oven_microwave_combo](../../data/json/furniture_and_terrain/furniture-appliances.json)（11） |
| `furniture.deconstruct.items` | 339 | array | [f_alien_pod_resin](../../data/json/furniture_and_terrain/furniture-alien.json)（7） |
| `furniture.deconstruct.items[].charges` | 107 | array, int | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.deconstruct.items[].container-item` | 1 | string | [f_pallet_cement](../../data/json/furniture_and_terrain/furniture-pallet.json)（2） |
| `furniture.deconstruct.items[].count` | 334 | array, int | [f_alien_pod_resin](../../data/json/furniture_and_terrain/furniture-alien.json)（7） |
| `furniture.deconstruct.items[].damage` | 1 | array | [f_battlefield_cross](../../data/json/furniture_and_terrain/furniture-graves.json)（5） |
| `furniture.deconstruct.items[].group` | 8 | string | [f_gravelbag_half](../../data/json/furniture_and_terrain/furniture-barriers.json)（1） |
| `furniture.deconstruct.items[].item` | 330 | string | [f_alien_pod_resin](../../data/json/furniture_and_terrain/furniture-alien.json)（7） |
| `furniture.deconstruct.items[].prob` | 10 | int | [f_indoor_plant](../../data/json/furniture_and_terrain/furniture-domestic_plants.json)（0） |
| `furniture.deconstruct.items[].variant` | 1 | string | [f_battlefield_cross](../../data/json/furniture_and_terrain/furniture-graves.json)（5） |
| `furniture.deployed_item` | 33 | string | [f_mannequin](../../data/json/furniture_and_terrain/furniture-decorative.json)（6） |
| `furniture.description` | 592 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.emissions` | 18 | array | [f_alien_anemone](../../data/json/furniture_and_terrain/furniture-alien.json)（1） |
| `furniture.examine_action` | 217 | object, string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions` | 8 | array | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].condition` | 2 | object | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].condition.and` | 1 | array | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].compare_int` | 1 | array | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].compare_int[].const` | 1 | int | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].compare_int[].u_val` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].compare_int[].var_name` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].not` | 1 | object | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].not.u_has_item` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.and[].u_has_item` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.compare_int` | 1 | array | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.compare_int[].const` | 1 | int | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.compare_int[].u_val` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.compare_int[].var_name` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].condition.not` | 1 | object | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].condition.not.u_has_mission` | 1 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].condition.u_has_mission` | 1 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].effect` | 5 | array | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].effect[].arithmetic` | 1 | array | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].effect[].arithmetic[].const` | 1 | int | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].effect[].arithmetic[].u_val` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].effect[].arithmetic[].var_name` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].effect[].assign_mission` | 1 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].effect[].open_dialogue` | 1 | object | [f_impaled_officer](../../data/json/furniture_and_terrain/furniture-alien.json)（28） |
| `furniture.examine_action.effect_on_conditions[].effect[].open_dialogue.topic` | 1 | string | [f_impaled_officer](../../data/json/furniture_and_terrain/furniture-alien.json)（28） |
| `furniture.examine_action.effect_on_conditions[].effect[].popup` | 1 | bool | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].effect[].u_consume_item` | 1 | string | [f_exodii_locator_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（25） |
| `furniture.examine_action.effect_on_conditions[].effect[].u_message` | 3 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.effect_on_conditions[].effect[].weighted_list_eocs` | 1 | array | [f_nm_nether_lily](../../data/json/furniture_and_terrain/furniture_nether_monster.json)（2） |
| `furniture.examine_action.effect_on_conditions[].effect[].weighted_list_eocs[][].effect` | 1 | object | [f_nm_nether_lily](../../data/json/furniture_and_terrain/furniture_nether_monster.json)（2） |
| `furniture.examine_action.effect_on_conditions[].effect[].weighted_list_eocs[][].effect.popup` | 1 | bool | [f_nm_nether_lily](../../data/json/furniture_and_terrain/furniture_nether_monster.json)（2） |
| `furniture.examine_action.effect_on_conditions[].effect[].weighted_list_eocs[][].effect.u_message` | 1 | string | [f_nm_nether_lily](../../data/json/furniture_and_terrain/furniture_nether_monster.json)（2） |
| `furniture.examine_action.effect_on_conditions[].effect[].weighted_list_eocs[][].id` | 1 | string | [f_nm_nether_lily](../../data/json/furniture_and_terrain/furniture_nether_monster.json)（2） |
| `furniture.examine_action.effect_on_conditions[].id` | 5 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.examine_action.furn_set` | 24 | string | [f_dishwasher](../../data/json/furniture_and_terrain/furniture-appliances.json)（2） |
| `furniture.examine_action.item` | 24 | string | [f_dishwasher](../../data/json/furniture_and_terrain/furniture-appliances.json)（2） |
| `furniture.examine_action.type` | 32 | string | [f_exodii_signpost](../../data/json/furniture_and_terrain/furniture-alien.json)（10） |
| `furniture.flags` | 567 | array | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.floor_bedding_warmth` | 39 | int | [f_leaves_pile](../../data/json/furniture_and_terrain/furniture-flora.json)（20） |
| `furniture.hacksaw` | 1 | object | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.hacksaw.byproducts` | 1 | array | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.hacksaw.byproducts[].count` | 1 | array, int | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.hacksaw.byproducts[].item` | 1 | string | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.hacksaw.duration` | 1 | string | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.hacksaw.message` | 1 | string | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.harvest_by_season` | 27 | array | [f_dandelion](../../data/json/furniture_and_terrain/furniture-flora.json)（1） |
| `furniture.harvest_by_season[].id` | 27 | string | [f_dandelion](../../data/json/furniture_and_terrain/furniture-flora.json)（1） |
| `furniture.harvest_by_season[].seasons` | 27 | array | [f_dandelion](../../data/json/furniture_and_terrain/furniture-flora.json)（1） |
| `furniture.id` | 594 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.keg_capacity` | 9 | int | [f_bathtub](../../data/json/furniture_and_terrain/furniture-plumbing.json)（0） |
| `furniture.light_emitted` | 8 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.lockpick_message` | 5 | string | [f_gunsafe_ml](../../data/json/furniture_and_terrain/furniture-storage.json)（12） |
| `furniture.lockpick_result` | 5 | string | [f_gunsafe_ml](../../data/json/furniture_and_terrain/furniture-storage.json)（12） |
| `furniture.looks_like` | 302 | string | [f_scrap_antenna](../../data/json/furniture_and_terrain/furniture-alien.json)（9） |
| `furniture.max_volume` | 89 | string | [f_exodii_botrack](../../data/json/furniture_and_terrain/furniture-alien.json)（11） |
| `furniture.move_cost_mod` | 579 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.name` | 584 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.open` | 10 | string | [f_curtain](../../data/json/furniture_and_terrain/furniture-medical.json)（21） |
| `furniture.oxytorch` | 5 | object | [f_gunsafe_ml](../../data/json/furniture_and_terrain/furniture-storage.json)（12） |
| `furniture.oxytorch.byproducts` | 1 | array | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.oxytorch.byproducts[].count` | 1 | array | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.oxytorch.byproducts[].item` | 1 | string | [f_rack](../../data/json/furniture_and_terrain/furniture-storage.json)（18） |
| `furniture.oxytorch.duration` | 5 | string | [f_gunsafe_ml](../../data/json/furniture_and_terrain/furniture-storage.json)（12） |
| `furniture.oxytorch.result` | 4 | string | [f_gunsafe_ml](../../data/json/furniture_and_terrain/furniture-storage.json)（12） |
| `furniture.plant_data` | 17 | object | [f_plant_harvest](../../data/json/furniture_and_terrain/furniture-domestic_plants.json)（2） |
| `furniture.plant_data.base` | 16 | string | [f_plant_harvest](../../data/json/furniture_and_terrain/furniture-domestic_plants.json)（2） |
| `furniture.plant_data.transform` | 17 | string | [f_plant_harvest](../../data/json/furniture_and_terrain/furniture-domestic_plants.json)（2） |
| `furniture.prying` | 3 | object | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.byproducts` | 1 | array | [f_metal_crate_c](../../data/json/furniture_and_terrain/furniture-storage.json)（52） |
| `furniture.prying.byproducts[].count` | 1 | int | [f_metal_crate_c](../../data/json/furniture_and_terrain/furniture-storage.json)（52） |
| `furniture.prying.byproducts[].item` | 1 | string | [f_metal_crate_c](../../data/json/furniture_and_terrain/furniture-storage.json)（52） |
| `furniture.prying.message` | 3 | string | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.prying_data` | 3 | object | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.prying_data.difficulty` | 3 | int | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.prying_data.failure` | 3 | string | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.prying_data.noisy` | 3 | bool | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.prying_data.prying_level` | 3 | int | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.prying.result` | 3 | string | [f_coffin_c](../../data/json/furniture_and_terrain/furniture-storage.json)（2） |
| `furniture.required_str` | 575 | int | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.rotates_to` | 26 | string | [f_sink](../../data/json/furniture_and_terrain/furniture-plumbing.json)（2） |
| `furniture.shoot` | 2 | object | [f_bookcase](../../data/json/furniture_and_terrain/furniture-storage.json)（0） |
| `furniture.shoot.destroy_damage` | 2 | array | [f_bookcase](../../data/json/furniture_and_terrain/furniture-storage.json)（0） |
| `furniture.shoot.reduce_damage` | 2 | array | [f_bookcase](../../data/json/furniture_and_terrain/furniture-storage.json)（0） |
| `furniture.shoot.reduce_damage_laser` | 2 | array | [f_bookcase](../../data/json/furniture_and_terrain/furniture-storage.json)（0） |
| `furniture.surgery_skill_multiplier` | 1 | number | [f_autodoc](../../data/json/furniture_and_terrain/furniture-medical.json)（0） |
| `furniture.symbol` | 594 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.type` | 594 | string | [f_alien_tendril](../../data/json/furniture_and_terrain/furniture-alien.json)（0） |
| `furniture.workbench` | 18 | object | [f_fake_bench_hands](../../data/json/furniture_and_terrain/furniture-fakes.json)（1） |
| `furniture.workbench.mass` | 18 | int | [f_fake_bench_hands](../../data/json/furniture_and_terrain/furniture-fakes.json)（1） |
| `furniture.workbench.multiplier` | 18 | number | [f_fake_bench_hands](../../data/json/furniture_and_terrain/furniture-fakes.json)（1） |
| `furniture.workbench.volume` | 18 | string | [f_fake_bench_hands](../../data/json/furniture_and_terrain/furniture-fakes.json)（1） |

## 7、embedded_mapgen全部显式字段路径

归一化字段路径2种。

| 字段路径 | 声明数 | 实际类型 | 原版实例（声明序号） |
|---|---:|---|---|
| `embedded_mapgen.method` | 20 | string | [内嵌](../../data/json/overmap/overmap_terrain/overmap_terrain_hardcoded.json)（3.mapgen[0]） |
| `embedded_mapgen.name` | 20 | string | [内嵌](../../data/json/overmap/overmap_terrain/overmap_terrain_hardcoded.json)（3.mapgen[0]） |

## 八、原版地形家具的标志与检查动作取值

下列为显式出现值，并非已穷尽全部引擎支持值；同标志在同声明只计一次。字符串检查动作调用硬编码函数，对象actor的字段见地形家具指南。

### terrain flags

| 标志 | 声明数 |
|---|---:|
| `ALARMED` | 9 |
| `AUTO_WALL_SYMBOL` | 137 |
| `BARRICADABLE_DOOR` | 23 |
| `BARRICADABLE_DOOR_DAMAGED` | 7 |
| `BARRICADABLE_DOOR_REINFORCED` | 2 |
| `BARRICADABLE_DOOR_REINFORCED_DAMAGED` | 1 |
| `BARRICADABLE_WINDOW` | 31 |
| `BARRICADABLE_WINDOW_CURTAINS` | 41 |
| `BLOCKSDOOR` | 2 |
| `BLOCK_WIND` | 207 |
| `BROWSABLE` | 29 |
| `BURROWABLE` | 43 |
| `CHIP` | 12 |
| `CLIMBABLE` | 13 |
| `COLLAPSES` | 82 |
| `CONNECT_WITH_WALL` | 206 |
| `CONTAINER` | 44 |
| `CURRENT` | 4 |
| `DEEP_WATER` | 17 |
| `DESTROY_ITEM` | 1 |
| `DIFFICULT_Z` | 4 |
| `DIGGABLE` | 56 |
| `DIGGABLE_CAN_DEEPEN` | 1 |
| `DOOR` | 47 |
| `EASY_DECONSTRUCT` | 61 |
| `ELEVATOR` | 2 |
| `FIRE_CONTAINER` | 2 |
| `FISHABLE` | 16 |
| `FLAMMABLE` | 141 |
| `FLAMMABLE_ASH` | 194 |
| `FLAMMABLE_HARD` | 60 |
| `FLAT` | 240 |
| `FLAT_SURF` | 1 |
| `FRESH_WATER` | 2 |
| `FUNGUS` | 12 |
| `GOES_DOWN` | 9 |
| `GOES_UP` | 12 |
| `GRAZABLE` | 4 |
| `GRAZER_INEDIBLE` | 2 |
| `HARVESTED` | 31 |
| `HIDE_PLACE` | 2 |
| `INDOORS` | 147 |
| `LIQUID` | 33 |
| `LIQUIDCONT` | 10 |
| `LOCKED` | 14 |
| `MINEABLE` | 150 |
| `MOUNTABLE` | 86 |
| `MURKY` | 4 |
| `NANOFAB_TABLE` | 1 |
| `NOCOLLIDE` | 6 |
| `NOITEM` | 480 |
| `NO_FLOOR` | 6 |
| `NO_FLOOR_WATER` | 3 |
| `NO_SCENT` | 140 |
| `NO_SPOIL` | 1 |
| `OPENCLOSE_INSIDE` | 69 |
| `ORGANIC` | 1 |
| `PAINFUL` | 1 |
| `PERMEABLE` | 143 |
| `PICKABLE` | 9 |
| `PIT_FILLABLE` | 3 |
| `PLACE_ITEM` | 36 |
| `PLANTABLE` | 1 |
| `PLOWABLE` | 19 |
| `RAIL` | 16 |
| `RAMP` | 2 |
| `RAMP_DOWN` | 5 |
| `RAMP_END` | 1 |
| `RAMP_UP` | 5 |
| `REDUCE_SCENT` | 197 |
| `ROAD` | 135 |
| `ROUGH` | 2 |
| `RUG` | 45 |
| `SALT_WATER` | 7 |
| `SEALED` | 9 |
| `SEEN_FROM_ABOVE` | 2 |
| `SHALLOW_WATER` | 13 |
| `SHARP` | 18 |
| `SHORT` | 51 |
| `SHRUB` | 31 |
| `SMALL_HIDE` | 26 |
| `SMALL_PASSAGE` | 30 |
| `SPAWN_WITH_LIQUID` | 2 |
| `SUPPORTS_ROOF` | 509 |
| `SUPPRESS_SMOKE` | 2 |
| `SWIMMABLE` | 33 |
| `THIN_OBSTACLE` | 136 |
| `TINY` | 6 |
| `TRANSPARENT` | 660 |
| `TRANSPARENT_FLOOR` | 11 |
| `TREE` | 65 |
| `UNSTABLE` | 12 |
| `USABLE_FIRE` | 1 |
| `WALL` | 179 |
| `WATER_CUBE` | 3 |
| `WINDOW` | 99 |
| `WIRED_WALL` | 14 |
| `YOUNG` | 3 |
| `Z_TRANSPARENT` | 10 |

### terrain examine_action

| 动作 | 声明数 |
|---|---:|
| `atm` | 1 |
| `bars` | 5 |
| `cardreader_fp` | 1 |
| `cardreader_robofac` | 1 |
| `chainfence` | 9 |
| `controls_gate` | 11 |
| `curtains` | 45 |
| `cvdmachine` | 1 |
| `dirtmound` | 2 |
| `door_peephole` | 5 |
| `elevator` | 1 |
| `finite_water_source` | 3 |
| `fswitch` | 4 |
| `gaspump` | 5 |
| `harvest_ter` | 21 |
| `harvest_ter_nectar` | 21 |
| `harvested_plant` | 27 |
| `intercom` | 1 |
| `ledge` | 6 |
| `locked_object` | 15 |
| `locked_object_pickable` | 5 |
| `nanofab` | 1 |
| `pedestal_temple` | 1 |
| `pedestal_wyrm` | 1 |
| `pit` | 3 |
| `pit_covered` | 3 |
| `shrub_marloss` | 1 |
| `shrub_wildveggies` | 1 |
| `tree_hickory` | 2 |
| `tree_maple` | 1 |
| `tree_maple_tapped` | 1 |
| `tree_marloss` | 1 |
| `water_source` | 32 |
| `对象:cardreader` | 17 |
| `对象:effect_on_condition` | 7 |

### furniture flags

| 标志 | 声明数 |
|---|---:|
| `ACTIVE_GENERATOR` | 2 |
| `ALARMED` | 3 |
| `ALIGN_WORKBENCH` | 12 |
| `ALLOW_FIELD_EFFECT` | 26 |
| `ALLOW_ON_OPEN_AIR` | 5 |
| `AMMOTYPE_RELOAD` | 5 |
| `AUTODOC` | 1 |
| `AUTODOC_COUCH` | 1 |
| `BLOCKSDOOR` | 131 |
| `BLOCK_WIND` | 17 |
| `BRIDGE` | 1 |
| `BUTCHER_EQ` | 3 |
| `CAN_SIT` | 36 |
| `CLIMBABLE` | 21 |
| `CLIMB_SIMPLE` | 4 |
| `CONSOLE` | 1 |
| `CONTAINER` | 141 |
| `DIFFICULT_Z` | 5 |
| `DIGGABLE` | 1 |
| `DONT_REMOVE ROTTEN` | 8 |
| `DONT_REMOVE_ROTTEN` | 13 |
| `DOOR` | 6 |
| `EASY_DECONSTRUCT` | 170 |
| `EXAMINE_FROM_ABOVE` | 3 |
| `FIRE_CONTAINER` | 20 |
| `FLAMMABLE` | 47 |
| `FLAMMABLE_ASH` | 115 |
| `FLAMMABLE_HARD` | 20 |
| `FLAT` | 7 |
| `FLAT_SURF` | 29 |
| `FLOWER` | 27 |
| `FUNGUS` | 5 |
| `GRAZER_INEDIBLE` | 9 |
| `GROWTH_HARVEST` | 4 |
| `GROWTH_MATURE` | 4 |
| `GROWTH_SEEDLING` | 4 |
| `HIDE_PLACE` | 7 |
| `INDOORS` | 11 |
| `LADDER` | 2 |
| `LIQUIDCONT` | 14 |
| `MINEABLE` | 62 |
| `MOUNTABLE` | 146 |
| `NOCOLLIDE` | 46 |
| `NOITEM` | 125 |
| `NO_PICKUP_ON_EXAMINE` | 1 |
| `NO_SELF_CONNECT` | 13 |
| `NO_SIGHT` | 7 |
| `OBSTACLE` | 2 |
| `ORGANIC` | 103 |
| `PAINFUL` | 9 |
| `PERMEABLE` | 79 |
| `PICKABLE` | 5 |
| `PLACE_ITEM` | 172 |
| `PLANT` | 16 |
| `PLANTABLE` | 3 |
| `REDUCE_SCENT` | 14 |
| `ROAD` | 1 |
| `ROUGH` | 13 |
| `RUBBLE` | 7 |
| `SEALED` | 79 |
| `SEEN_FROM_ABOVE` | 5 |
| `SHARP` | 11 |
| `SHORT` | 63 |
| `SHRUB` | 3 |
| `SIGN` | 4 |
| `SIGN_ALWAYS` | 2 |
| `SMALL_HIDE` | 69 |
| `SUN_ROOF_ABOVE` | 15 |
| `SUPPRESS_SMOKE` | 9 |
| `THIN_OBSTACLE` | 56 |
| `TINY` | 55 |
| `TOILET_WATER` | 1 |
| `TRANSPARENT` | 425 |
| `UNSTABLE` | 9 |
| `WORKOUT_ARMS` | 3 |
| `WORKOUT_LEGS` | 2 |

### furniture examine_action

| 动作 | 声明数 |
|---|---:|
| `aggie_plant` | 12 |
| `arcfurnace_full` | 1 |
| `autoclave_empty` | 1 |
| `autoclave_full` | 1 |
| `autodoc` | 1 |
| `bulletin_board` | 1 |
| `chainfence` | 22 |
| `change_appearance` | 2 |
| `deployed_furniture` | 18 |
| `dirtmound` | 1 |
| `finite_water_source` | 1 |
| `fireplace` | 11 |
| `flower_dahlia` | 1 |
| `flower_marloss` | 1 |
| `flower_poppy` | 1 |
| `fungus` | 1 |
| `fvat_empty` | 2 |
| `fvat_full` | 2 |
| `gunsafe_el` | 1 |
| `harvest_furn` | 4 |
| `harvest_furn_nectar` | 23 |
| `harvest_plant_ex` | 4 |
| `keg` | 9 |
| `kiln_empty` | 2 |
| `kiln_full` | 2 |
| `locked_object` | 2 |
| `locked_object_pickable` | 5 |
| `open_safe` | 1 |
| `pay_gas` | 1 |
| `portable_structure` | 4 |
| `quern_examine` | 4 |
| `reload_furniture` | 5 |
| `rubble` | 6 |
| `safe` | 1 |
| `sign` | 2 |
| `smoker_options` | 4 |
| `stook_empty` | 1 |
| `stook_full` | 1 |
| `vending` | 2 |
| `workbench` | 17 |
| `workout` | 4 |
| `对象:appliance_convert` | 24 |
| `对象:effect_on_condition` | 8 |
