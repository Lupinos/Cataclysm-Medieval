# 原版建筑内容放置：全部通道与子字段

对应策划：[06 聚居地的类型及其分案](../design/design06-建筑.md)。本篇提供具体建筑及地块的原版 JSON 依据，建筑选型与空间关系见策划案。

入口：[建筑mapgen指南](guide06_building_json.md)。本篇字段按当前[mapgen.cpp](../../src/mapgen.cpp)中各`jmapgen_*`构造器及apply说明；源码段落附在各节。`V<ID>`表示mapgen_value，接受固定ID、param、distribution、switch；`R`表示jmapgen_int整数或闭区间；`T`表示可翻译文本。没有标为V或R的字段不能自动套用其随机语法。

## 一、全部通道对应表

符号通道放在palette或带rows的object内，格式`"通道":{"字符":负载}`。坐标通道位于object，通常为`"通道":[{"x":…,"y":…,…负载字段}]`。`mapping`可以按字符集中表达相同符号通道。下表以加载器注册结果为准，包含原版未出现但源码支持的入口。

| 符号通道 | 坐标通道 | 负载类/用途 |
|---|---|---|
| `terrain` | `place_terrain` | jmapgen_terrain；地形 |
| `furniture` | `place_furniture` | jmapgen_furniture；家具 |
| `traps` | `place_traps` | jmapgen_trap；陷阱 |
| `fields` | `place_fields` | jmapgen_field；烟、血、气体等场效应 |
| `npcs` | `place_npcs` | jmapgen_npc；NPC模板 |
| `signs` | `place_signs` | jmapgen_sign；标牌文字与家具 |
| `graffiti` | `place_graffiti` | jmapgen_graffiti；地面文字 |
| `vendingmachines` | `place_vendingmachines` | jmapgen_vending_machine；售货机 |
| `toilets` | `place_toilets` | jmapgen_toilet；马桶与水 |
| `gaspumps` | `place_gaspumps` | jmapgen_gaspump；油泵与燃料 |
| `liquids` | `place_liquids` | jmapgen_liquid_item；散落液体 |
| `corpses` | `place_corpses` | jmapgen_corpse；从怪物组选尸体 |
| `items` | `place_items` | jmapgen_item_group；物品组 |
| `item` | `place_item`，旧别名`add` | jmapgen_spawn_item；具体物品 |
| 无 | `place_loot` | jmapgen_loot；单次物品或物品组投放 |
| `monsters` | `place_monsters` | jmapgen_monster_group；密度驱动怪物组 |
| `monster` | `place_monster` | jmapgen_monster；指定怪物或择组 |
| `vehicles` | `place_vehicles` | jmapgen_vehicle；载具组/原型对应组 |
| `rubble` | `place_rubble` | jmapgen_make_rubble；瓦砾与破坏 |
| `computers` | `place_computers` | jmapgen_computer；终端及选项 |
| `sealed_item` | 无 | jmapgen_sealed_item；先放物品再封装家具 |
| `nested` | `place_nested` | jmapgen_nested；嵌套模块 |
| `translate` | `translate_ter` | jmapgen_translate；整块地图替换地形 |
| `ter_furn_transforms` | `place_ter_furn_transforms` | jmapgen_ter_furn_transform；单点转换规则 |
| `zones` | `place_zones` | jmapgen_zone；NPC/玩家区域 |
| `faction_owner_character` | `faction_owner` | jmapgen_faction；物品和载具归属 |
| `remove_vehicles` | `remove_vehicles` | jmapgen_remove_vehicles；移除指定载具 |
| `remove_all` | `place_remove_all` | jmapgen_remove_all；清理多层内容 |
| 无 | `remove_npcs` | jmapgen_remove_npcs；按模板/唯一标识删除NPC |
| 无 | `place_variables` | jmapgen_variable；记录坐标变量 |

`remove_all`对象形式是符号字典，`place_remove_all`才是坐标数组。`remove_vehicles`在两种位置同名，但结构不同。`faction_owner`不是字符字典；字符版名称是faction_owner_character。这些区别不能从英文单复数机械推导。

## 二、坐标、重复与概率总则

坐标式条目共同读取`x`、`y`（必填R）、`repeat`（可选R，默认1）。符号式使用rows坐标，无须再写x/y；部分负载自行读取repeat，故items、item的符号负载也能重复。不是每个符号负载都读取repeat，不能将坐标层能力自动套给所有符号通道。

| 消费方式 | 对x/y范围的解释 |
|---|---|
| 随机点 | terrain、furniture、traps、fields、NPC、文字、具体物品、液体、尸体、载具、瓦砾、终端、nested、sealed_item通常调用get，取一个坐标 |
| 矩形范围 | items、monsters、zones、faction_owner、remove_vehicles、remove_all消费最小最大边界 |
| 特殊 | loot先抽一个点，再将该次物品组结果集中放于该点；translate忽略坐标而作用整张局部地图；remove_npcs忽略具体坐标，筛选当前OMT内NPC；variables使用范围下界而非随机点 |

坐标范围不代表在每格执行。需要逐格放置可以使用rows符号，或按需要组织repeat。范围最小值属于其他拼图区块的条目会被过滤，当前区块内的范围最大值越界则报错。模块还要检查调用点加模块边界是否跨24×24区块。

| 位置 | chance缺省与实际算法 |
|---|---|
| `set` | 默认1，1/N；一次机会控制整个repeat循环 |
| `items/place_items` | 默认1，百分数式投放期望，受物品生成率及物品组内部规则影响；不是默认必出 |
| `item/place_item` | 默认100；100时单次必尝试一次，否则`roll_remainder(chance × ITEM_SPAWNRATE / 100)`决定尝试数，可多次 |
| `place_loot` | 默认100；百分数判定，加载时还可按高物品生成率调整chance或repeat |
| `liquids/place_liquids` | 默认1，1/N |
| `monsters/place_monsters` | 默认1，1/N；通过后数量另由密度计算 |
| `monster/place_monster` | 默认100，受SPAWN_DENSITY调整机会与数量；原始100有至少一次的特殊分支 |
| `vehicles/place_vehicles` | 默认1，百分数，意味着缺省约1%，不是必出 |
| `sealed_item` | 默认100；非100按物品生成率缩放并封顶一次 |

其他多数负载根本不读取chance，不能随意加一个chance来控制NPC、家具、瓦砾或nested。符号字典的terrain/furniture/traps数组是随机择一；多数其他通道的对象数组是全部执行。

## 三、地形、家具、陷阱与场效应

依据：`jmapgen_terrain:2829`、`jmapgen_furniture:2795`、`jmapgen_trap:2742`、`jmapgen_field:1761`。

| 类别 | 字段 | 类型/默认 | 语义 |
|---|---|---|---|
| 地形 | `ter` | 坐标负载必填V<terrain> | 放置已有地形；符号式直接写地形值。换地面可能清理或诊断原内容，详见主文flags |
| 家具 | `furn` | 坐标负载必填V<furniture> | 放置已有家具；符号式直接写家具值。f_null通常被视为不操作，明确擦除用set或清理器 |
| 陷阱 | `trap` | 必填V<trap>；符号式可直接为值 | 放置指定陷阱；对象式可带remove |
| 陷阱 | `remove` | bool，false | true则移除目标位置的陷阱；仍须指定可解析的trap值，非空值才执行 |
| 场 | `field` | 必填V<field_type> | 场效应ID，不是terrain ID |
| 场 | `intensity` | 整数或整数候选数组，默认1 | 数组是离散随机候选，不是上下界范围 |
| 场 | `age` | 整数，默认0 | 单位turn，转成time_duration；与尸体age单位不同 |
| 场 | `remove` | bool，false | 移除选定field类型，不清空全部其他场 |

## 四、物品组、具体物品与loot

依据：`jmapgen_item_group:2196`、`jmapgen_spawn_item:2689`、`jmapgen_loot:2226`、`jmapgen_objects::load_objects<jmapgen_loot>:3884`；实际组投放见`map::place_items:6440`与[map.cpp](../../src/map.cpp)的spawn_item。

### items / place_items

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `item` | 必填item_group ID或内联item_group结构 | 虽叫item，引用的是组；内联默认按collection加载，不是V<itype> |
| `chance` | R，默认1 | 通常写1–100；map::place_items拒绝≤0或>100。默认生成率下相当于组投放机会，高生成率可多次 |
| `repeat` | R，默认1 | 重复抽取；与坐标repeat执行时取较大值 |
| `faction` | 可选字符串，默认空 | 为该次生成物品赋归属，空值仍由底层所有权逻辑处理 |

矩形中抽取适当投放点；组自身可以产出多件物品。不是对矩形每格各执行chance。组内部entries、collection、distribution、概率、数量和容器等属于[itemgroup机制](json_itemgroup_organization.md)；不能把它们当作place_items的平级字段。

### item / place_item / add

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `item` | 必填V<itype> | 具体物品ID，执行前应用物品迁移 |
| `amount` | R，默认1 | 传入spawn_item的物品数量；并非通用液体charge字段 |
| `chance` | R，默认100 | 上节所述生成尝试数；源码旧注释写1/N，但apply实际不是1/N |
| `repeat` | R，默认1 | 外层执行次数 |
| `variant` | 可选字符串 | 具体物品外观变体ID，不是另一件物品 |
| `faction` | 可选字符串 | 生成物品所有权 |
| `custom-flags` | 字符串集合/数组，默认空 | 给实例附加item flags；拼写有连字符 |

spawn_item将amount作为quantity生成对应数量的物品实例，随后应用默认charge、默认容器、黑名单及合并逻辑；不是将单件物品charge设为amount。当前spawn_item即使quantity=0仍会执行一次主体，amount=0不能用来禁止生成。需精确液体charge时使用liquids；具体物品模板字段见武器、服装等独立指南。

### place_loot

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `group` | 可选固定item_group ID | 与item恰选其一；为空或同时给出都会报错 |
| `item` | 可选固定itype ID | 不接受mapgen_value；与group恰选其一 |
| `chance` | 普通整数，默认100 | 百分比；apply以rng(0,99)<chance判断 |
| `ammo` | 普通整数，默认0 | 交给内部Item_group，控制生成物携带默认弹药的百分比 |
| `magazine` | 普通整数，默认0 | 交给内部Item_group，控制可拆弹匣生成百分比 |
| `variant` | 可选字符串 | 仅具体item分支读取，group分支不应用 |

坐标repeat仍可用。加载时ITEM_SPAWNRATE>1：若repeat上界不等于1，扩大repeat；否则非100机会被放大并夹到1–100。低生成率由物品组内部处理。物品组内产出的所有物品集中在本次抽到的同一个坐标点。

## 五、液体、尸体与封装物品

依据：`jmapgen_liquid_item:2119`、`jmapgen_corpse:2168`、`jmapgen_sealed_item:3143`。

| 类别 | 字段 | 类型/默认 | 实际含义 |
|---|---|---|---|
| 液体 | `liquid` | 必填V<itype> | 按charge计数的液体物品，不是液体地形 |
| 液体 | `amount` | R，默认-1 | -1保持物品默认charges；非负设charge数量；最终charges>0才放置 |
| 液体 | `chance` | R，默认1 | one_in，1必出 |
| 尸体 | `group` | 必填固定mongroup ID | 从组的可用怪物列表随机选尸体种类；不接受V |
| 尸体 | `age` | 整数，默认0，单位天 | 死亡时间为当前时间减年龄，下限灾变起点；不是field.age的turn |
| 封装 | `furniture` | 必填V<furniture> | 最后围住物品的家具，如种植阶段家具 |
| 封装 | `chance` | R，默认100 | 外层封装机会；非100受物品生成率缩放 |
| 封装 | `item` | 可选对象 | 内部jmapgen_spawn_item完整负载，可写item/amount/chance等 |
| 封装 | `items` | 可选对象 | 内部jmapgen_item_group负载，可写item/chance等 |

sealed_item先临时清空家具，放物品，再放目标家具；至少要有item或items。普通家具允许二者都写；带PLANT标志的家具要求恰好一个来源，生成恰好一颗种子，内部chance应100，随机机会放在外层。不能直接放PLANT家具再期待自动长出作物。sealed_item多次使用坐标范围时各步骤会分别抽点，需保持同一格时使用固定坐标或符号位置。

## 六、怪物组与指定怪物

依据：`jmapgen_monster_group:2288`、`jmapgen_monster:2328`、`map::place_spawns:6314`。

### monsters / place_monsters

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `monster` | 必填V<mongroup> | 此处是怪物组，不是单种monster |
| `chance` | R，默认1 | 1/N，判定成功后计算数量 |
| `density` | float，默认-1 | -1使用mapgendata怪物密度，否则用指定密度；还乘动物/普通怪物生成选项 |

放置矩形内的生成点。底层数量约由density×对应世界生成密度×随机10–50再取整驱动，组结果还可能有pack；不能把density=1理解为一个怪物。

### monster / place_monster

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `monster` | V<mtype>或加权候选列表，列表省略权重时100 | 不使用group时必填；列表先选种类 |
| `group` | 可选V<mongroup> | 存在时优先于monster；从组取结果，不是place_monsters的密度铺设模式 |
| `chance` | R，默认100 | 基础百分数，再由SPAWN_DENSITY调整成功率与生成倍数 |
| `pack_size` | R，默认1 | 每次成功生成数量的乘数 |
| `one_or_none` | bool；未写repeat与pack_size时默认true，否则false | 限制密度放大的生成次数；不是将最终pack_size强制变1 |
| `friendly` | bool，默认false | 传给生成点的友好属性 |
| `name` | 可选T | 固定名称；random_name=snippet时作为snippet展开文本 |
| `random_name` | 字符串，默认空 | `random`、`female`、`male`、`snippet`或空；指定随机姓名方式 |
| `target` | bool，默认false | 存在当前任务时，把生成怪物关联任务ID |
| `use_pack_size` | bool，默认false | 传给怪物组结果选择器的开关；不能据名字推定等同本条pack_size |
| `spawn_data` | 可选对象 | 额外弹药与巡逻数据，见下表 |
| `spawn_data.ammo` | 对象数组 | 每项含ammo_id和qty |
| `spawn_data.ammo[].ammo_id` | 必填固定itype ID | 怪物使用的弹药种类 |
| `spawn_data.ammo[].qty` | 必填R | 弹药数量，记录在spawn_data |
| `spawn_data.patrol` | 对象数组 | 每项为当前局部地图的巡逻点 |
| `spawn_data.patrol[].x/y` | 必填R | 构造spawn_data时抽取并保存；不等于每次怪物移动再随机 |

spawn_data没有任意monster实例字段透传。怪物装备、攻击、掉落仍属于怪物模板与组数据。不要把NPC的模板、友好度、对话写成这里的自造字段。

## 七、NPC、所有权、区域与坐标变量

依据：`jmapgen_npc:1805`、`jmapgen_faction:1864`、`jmapgen_zone:3308`、`jmapgen_variable:3348`。

| 类别 | 字段 | 类型/默认 | 实际含义 |
|---|---|---|---|
| NPC | `class` | 必填V<npc_template> | 指向type=npc模板；字段名虽叫class，不直接引用npc_class定义 |
| NPC | `target` | bool，false | 当前任务的目标NPC设置为生成者 |
| NPC | `add_trait` | trait ID字符串或数组，默认空 | 对生成NPC追加mutation/trait |
| NPC | `unique_id` | 可选字符串 | 已存在此唯一NPC则跳过，否则为新NPC登记唯一标识 |
| 所有权 | `id` | 必填V<faction> | 将坐标矩形内已放内容交给阵营；阶段晚于物品与nested |
| zone | `type` | 必填V<zone_type> | 区域类型，不是JSON顶层type |
| zone | `faction` | 必填V<faction> | 区域所属阵营 |
| zone | `name` | 可选普通字符串，默认空 | 区域名称 |
| zone | `filter` | 可选字符串，默认空 | 传给zone选项，如过滤条件；具体解释由zone类型决定 |
| 变量 | `name` | 必填字符串 | 将(x下界,y下界,当前z)转绝对坐标排队记录；最终写入npctalk_var_前缀的全局变量 |

区域使用包含端点的坐标矩形；特殊玩家出生区也走zone_type规则，不是单独spawn_player字段。所有权底层调用`map::apply_faction_ownership`，会重设范围内物品所有者，但仅为尚无所有者的载具设置所有者，不会强制夺走已有主载具；不产生“地皮所有权”。update调用侧须注意执行排队变量的提交，不是任意调用路径都会自动set_queued_points。

## 八、载具及删除操作

依据：`jmapgen_vehicle:2503`、`jmapgen_remove_vehicles:3368`、`jmapgen_remove_npcs:3399`、`jmapgen_remove_all:3429`。

| 类别 | 字段 | 类型/默认 | 实际含义 |
|---|---|---|---|
| 载具 | `vehicle` | 必填V<vgroup> | 先选载具组，再由组pick原型；实际可用原型同名组取决于载具注册 |
| 载具 | `chance` | R，默认1 | 百分数，不是1/N |
| 载具 | `rotation` | 整数或整数列表，默认0 | 单位角度；列表为离散方向候选，不是范围，也不同于object.rotation的90°次数 |
| 载具 | `fuel` | 整数，默认-1 | 交给add_vehicle/vehicle初始化的燃料状态；不是物品charge数量 |
| 载具 | `status` | 整数，默认-1 | 交给载具初始化的损伤状态；不是建筑损坏程度 |
| 载具 | `faction` | 可选字符串，默认空 | 成功生成后设置载具所有者 |
| 移除载具 | `vehicles` | 字符串数组 | 需要移除的载具原型ID；非载具组ID |
| 移除NPC | `class` | 可选模板ID字符串，默认空 | 当前OMT内按npc_template筛选；空则不限制模板 |
| 移除NPC | `unique_id` | 可选字符串，默认空 | 与class共同筛选；均空会删除当前OMT中全部符合基础条件的存活NPC |
| 全清理 | 无负载专用字段 | 空对象可用 | 矩形内清家具、物品、陷阱、场、graffiti及相交载具；不清terrain、辐射、NPC或怪物 |

载具占地不能只检查锚点：完整原型可能越过24×24边界，代码检查潜在边界并发出诊断。删除载具按矩形内命中的部件销毁整辆车，不是只删除选中的部件。remove_npcs虽然坐标式语法要求x/y，实际操作范围是当前OMT，不是给定小矩形。

[vehicle.cpp](../../src/vehicle.cpp)的vehicle::init_state确认：fuel<0随机燃料比例（按燃料类型共享正态抽样，夹至5%–95%）；0无燃料；1–99为容量百分比；≥100装满。status=-1走默认轻损分支，0部件完好但仍可能有故障/安保状态，1随机破坏座椅、控制、储箱、轮胎或引擎等使其瘫痪，2为完好且清除相应故障/安保状态。OVERRIDE_VEHICLE_INIT_STATE世界选项可覆盖传入fuel/status。

## 九、文字与现代设施

依据：`jmapgen_sign:1894`、`graffiti:1952`、`vending_machine:1998`、`toilet:2037`、`gaspump:2066`、`computer:3068`。

| 类别 | 字段 | 类型/默认 | 实际含义 |
|---|---|---|---|
| 标牌 | `signage` | 可选T | 固定标牌文字，与snippet至少一个非空 |
| 标牌 | `snippet` | 字符串，默认空 | 从snippet类别抽文字，优先于signage；随后展开标签和城市名 |
| 标牌 | `furniture` | 固定furn ID，默认f_sign | 替换成该标牌家具，要求带SIGN标志 |
| graffiti | `text` | 可选T | 直接写于地块的文字，与snippet至少一个非空 |
| graffiti | `snippet` | 字符串，默认空 | 与标牌类似的snippet选择与标签展开，不放标牌家具 |
| 售货机 | `item_group` | 可选V<item_group>，默认default_vending_machine | 填充内容，先清当前家具再调用place_vending |
| 售货机 | `reinforced` | bool，false | 强化售货机分支 |
| 售货机 | `lootable` | bool，false | 控制随灾变后经过时间被洗劫的相关分支，不能直译成“是否能打开” |
| 马桶 | `amount` | R，默认0 | 非0为水charge；0调用place_toilet默认数量，不表示空马桶 |
| 油泵 | `amount` | R，默认0 | 非0为燃料charge；0随机10000–50000 |
| 油泵 | `fuel` | 可选V<itype> | 未指定时底层随机柴油或汽油；检查支持gasoline、diesel、jp8、avgas |
| 终端 | `name` | 可选T，默认空 | 终端显示名称，并放f_console家具 |
| 终端 | `access_denied` | 可选T | 非空时覆盖终端默认拒绝访问文案 |
| 终端 | `security` | 整数，默认0 | 终端安全等级 |
| 终端 | `target` | bool，false | 有当前任务时关联任务ID |
| 终端 | `options` | 对象数组，默认空 | 菜单选项，详见下表 |
| 终端 | `failures` | 对象数组，默认空 | 失败行为，详见下表 |
| 终端 | `eocs` | EOC ID字符串数组，默认空 | 为终端添加EOC接口，不是任意内联对象 |
| 终端 | `chat_topics` | 对话topic ID字符串数组，默认空 | 为终端添加对话接口 |

[computer.cpp](../../src/computer.cpp)的`computer_option::from_json/computer_failure::from_json`定义子字段：

| 子字段 | 类型/默认 | 效果 |
|---|---|---|
| `options[].name` | 可选T | 选项文字 |
| `options[].action` | 必填computer_action枚举字符串 | 执行终端动作，非EOC ID |
| `options[].security` | 整数，默认0 | 此选项的安全等级 |
| `failures[].action` | 必填computer_failure_type枚举字符串 | 失败效果 |

现代设施仍纳入原版全部字段调查；列入不代表本模组需要加入这些设施。空油泵、空马桶不能通过amount=0表达，需选择普通地形/家具及其他投放方案。

## 十、瓦砾、替换与转换

依据：`jmapgen_make_rubble:3023`、`jmapgen_translate:3278`、`jmapgen_ter_furn_transform:2997`。

| 类别 | 字段 | 类型/默认 | 实际含义 |
|---|---|---|---|
| 瓦砾 | `rubble_type` | V<furniture>，默认f_rubble | 目标瓦砾家具 |
| 瓦砾 | `items` | bool，false | 是否生成make_rubble规定的碎料，不是物品组字典 |
| 瓦砾 | `floor_type` | V<terrain>，默认t_dirt | 需要时采用的底层地形，空值诊断并改用t_dirt |
| 瓦砾 | `overwrite` | bool，false | true直接写floor_type与rubble_type；false先摧毁可砸家具及妨碍通行的可砸地形，仍不可通行才换地面，非露天空格才放瓦砾 |
| 整图替换 | `from` | 必填V<terrain> | 要替换的旧地形 |
| 整图替换 | `to` | 必填V<terrain> | 替换成的新地形 |
| 单点转换 | `transform` | 必填V<ter_furn_transform> | 在抽取坐标执行已定义转换；转换规则属于独立JSON类型 |

translate_ter的x/y仍由坐标层读取校验，但apply忽略它们，调用整张局部地图的translate。不要据坐标矩形推断它只换某个房间。transform按单点执行，规则内部可变换地形、家具、陷阱等，详见原版[TER_FURN_TRANSFORM.md](../../doc/TER_FURN_TRANSFORM.md)。

## 十一、嵌套调用全部字段与邻居条件

依据：`jmapgen_nested:3463–3844`。

| 字段 | 格式/默认 | 实际含义 |
|---|---|---|
| `chunks` | nested ID/V<nested>候选加权数组，省略权重时100 | 条件全满足时选择一个模块；可写空ID或null结果表示本次不嵌入 |
| `else_chunks` | 同上，默认空 | 任一条件族不满足时选择；为空则不放置 |
| `neighbors` | 方向→允许的地形匹配对象，默认空 | 同一方向候选为或，不同指定方向为且 |
| `joins` | 立方方向→join ID字符串或数组，默认空 | 同一方向匹配任一join，不同方向同时满足 |
| `flags` | 方向→Overmap地形flag集合，默认空 | 每个指定方向都至少命中一个flag；不是jmapgen flags |
| `flags_any` | 同flags，默认空 | 全部指定方向及flag中任意命中即可；空条件视为满足 |
| `predecessors` | 地形匹配候选数组，默认空 | 已记录前驱中任一匹配即满足；空条件通过 |
| 邻居/前驱匹配项的`om_terrain` | 必填字符串 | 待比较ID或片段 |
| 匹配项的`om_terrain_match_type` | 默认CONTAINS | EXACT、TYPE、SUBTYPE、PREFIX、CONTAINS；分别按完整ID、类型、子类型、前缀、子串规则比较 |

neighbors单方向可直接为字符串（按CONTAINS），也可为字符串或对象组成的数组；对象格式为`{"om_terrain":"…","om_terrain_match_type":"TYPE"}`。predecessors为上述字符串/对象组成的数组。具体匹配实现见[overmap.cpp](../../src/overmap.cpp)的is_ot_match，不能用大小写不同的自造枚举。

neighbors、flags、flags_any的加载器遍历[line.cpp](../../src/line.cpp)的27个direction枚举名，但[mapgendata.cpp](../../src/mapgendata.cpp)的neighbor_at实际仅支持north/east/south/west、north_east/north_west/south_east/south_west及above/below，共10个方向。center、above_north、below_south_west等其他枚举虽然可被读取，消费时会报不支持并返回north，不能据枚举表宣称它们可用。joins则使用cube_direction，支持north/east/south/west/above/below六方向。

所有条件族最终作且连接；flags_any只是其中一个条件族内部为或。这里的邻居是mapgendata中的周边地块类型，不是本房间左右相邻的单个terrain方格。用它判断“隔壁是否水岸”与直接检查本屋某格是不是墙是不同用途。

## 十二、内联数据与原版非功能字段

全量盘点保留JSON中出现的全部路径，但出现过不等于加载器支持。例如[house_general_palette.json](../../data/json/mapgen_palettes/house_general_palette.json)有两处items负载写成`repear`；jmapgen_item_group只读取`repeat`，`repear`是未消费的拼写，不能作为合法字段照抄。本调查记录差异，不修改原版数据。

内联物品组的`subtype`、`entries`、`prob`、`container-item`等由item_group加载器读取，语法见[ITEM_SPAWN.md](../../doc/ITEM_SPAWN.md)及仓库[物品组调查](json_itemgroup_organization.md)。其中collection的prob表示独立百分比，distribution的prob表示相对权重；组中container-item指定包裹容器，不是mapgen家具。inline组字段须放在items.item或掉落items的组结构内，不是与place_items.chance平级的任意属性。

terrain/furniture.examine_action.effect_on_conditions内的u_has_item、u_has_items、u_has_mission、u_has_trait、compare_int、not等属于EOC条件；u_message、popup、open_dialogue、u_teleport、u_location_variable、z_adjust、assign_mission、finish_mission、u_consume_item、u_adjust_var、var_name、adjustment、weighted_list_eocs等属于对应EOC效果及其参数。它们由[EFFECT_ON_CONDITION.md](../../doc/EFFECT_ON_CONDITION.md)、[condition.cpp](../../src/condition.cpp)及[dialogue_helpers.cpp](../../src/dialogue_helpers.cpp)等独立加载器解释，不能直接作为建筑字段。condition、effect、false_effect和涉及变量的u_val/global_val/context也须保持其内联结构；字段盘点中保留这些路径供追查，不把EOC全集混入建筑模式。
