# 原版建筑地形与家具：字段和行为

对应策划：[06 聚居地的类型及其分案](../design/design06-建筑.md)。本篇提供具体建筑及地块的原版 JSON 依据，建筑选型与空间关系见策划案。

入口：[建筑mapgen指南](guide06_building_json.md)。mapgen描述“在哪一格放什么”，本篇解释墙、门、窗、地板、床与工作台等被引用对象的定义。依据[mapdata.cpp](../../src/mapdata.cpp)、[mapdata.h](../../src/mapdata.h)、[generic_factory.h](../../src/generic_factory.h)及实际行为调用。这里的terrain是局部地形，不是Overmap地形。

## 一、身份、继承与共享字段

terrain与furniture经generic_factory加载，支持已有定义的继承；与不走该工厂的mapgen/palette区别。下表“初值”指新对象未继承时；继承子项通常保留父值，但专用重建分支另述。字段可选不等于每次缺失都重置初值。

| 字段 | 类型、必填或初值 | 作用与限制 |
|---|---|---|
| `type` | 必填terrain或furniture | 决定地形/家具加载器 |
| `id` | 具体定义ID字符串，也接受字符串数组批量定义 | mapgen引用的对象标识；不能用玩家显示名称代替 |
| `ident` | 工厂接受的旧ID字段，字符串或数组 | 兼容旧数据入口，新内容使用id；不与id混写 |
| `abstract` | 通用工厂模板ID，与具体id按工厂规则选用 | 可作copy-from父项；不是可放置地形 |
| `copy-from` | 父定义ID | 复制同一类型对象后应用本条加载；父项未就绪可延后，不跨terrain与furniture继承 |
| `alias` | 工厂别名，字符串或字符串数组 | 给定义建立其他可解析ID，不产生另一种独立墙体 |
| `name` | T；新定义必填，继承可保留 | 玩家名称 |
| `description` | T；新定义必填，继承可保留 | 玩家查看说明；不是房屋历史介绍 |
| `symbol` | 字符串或季节数组；当前load_symbol每次要求 | 一字符，或LINE_XOXO/LINE_OXOX；不是rows的字符映射键 |
| `color` | 颜色字符串或季节数组 | 与bgcolor恰选其一，即使copy-from也要求本条提供其一 |
| `bgcolor` | 背景色字符串或季节数组 | 与color互斥；不是同时给前景和背景的两属性写法 |
| `looks_like` | 可选同类ID，初始空 | 贴图回退线索；copy-from且looks_like为空时自动使用父ID；不复制运行参数 |
| `flags` | 字符串数组 | 由地形家具标志影响碰撞、透明、燃烧、支撑、容器等；与mapgen flags无关 |
| `connect_groups` | 连接组ID字符串或数组 | 本地形/家具属于哪些绘制连接组 |
| `connects_to` | 连接组ID字符串或数组 | 与哪些邻接组连接，供图形/墙体连接逻辑使用 |
| `rotates_to` | 连接组ID字符串或数组 | 朝哪些邻接组调整绘制方向；不旋转整栋建筑 |
| `coverage` | 整数，初值0 | 地块遮蔽覆盖程度；不等于结构生命值或通用减伤百分比 |
| `comfort` | 整数，初值0 | 休息舒适度，实际睡眠效果还有人物及装备条件 |
| `floor_bedding_warmth` | 旧温度尺度整数，初值0 | 休息时地面寝具保暖；代码转成温度差，不能直接当摄氏温度 |
| `light_emitted` | 整数，初值0 | 发光强度；不因描述写着火把而自动发光 |
| `max_volume` | 容积值，初值1000 L | 此格可存物品容积；terrain用assign，furniture用volume_reader。新内容用显式单位字符串 |
| `examine_action` | 字符串或对象；初次缺省none | 字符串选硬编码检查交互；对象选已注册actor，专用字段见后文 |
| `harvest_by_season` | 对象数组 | 每项`seasons`为季节集合、`id`为harvest ID；指定季节关联采收表，不是地图物品组 |
| `curtain_transform` | 可选terrain ID，初始空 | 窗帘相关交互目标；检查要求与curtains动作相匹配，不能只写该字段就有窗帘功能 |
| `shoot` | 可选对象 | 弹射物命中、减伤和破坏，全部字段见第五节 |
| `bash` | 可选对象 | 砸毁能力与结果，全部字段见第四节 |
| `deconstruct` | 可选对象 | 拆解后目标及材料，全部字段见第四节 |
| `open`、`close` | 同类ID，初值空 | 打开/关闭变换目标；terrain引用terrain，furniture引用furniture |
| `lockpick_result` | 同类ID，初值空 | 撬锁成功后的地块；不是开门的同义字段 |
| `lockpick_message` | T，初始空 | 撬锁成功文案，具体可撬锁性仍看标志与动作 |
| `oxytorch`、`boltcut`、`hacksaw`、`prying` | 可选活动对象 | 分别定义氧割、断线钳、钢锯及撬动的结果与耗时，见第六节 |
| `emissions` | emit ID数组，默认空 | 周期性环境排放，具体场效应由emit定义；不是物品掉落 |
| `//`、`//…` | 注释文字 | 不参与地形行为 |

symbol/color/bgcolor的季节写法为一个值、单元素数组或春夏秋冬顺序四元素数组，不支持任意长度。symbol的加载器按字符串字节长度检查单字符，不能把rows的UTF-8显示宽度规则照搬到这里。

连接组的分类与目标在每次加载时重置，先由flags建立部分关系，再由显式connect_groups/connects_to/rotates_to处理。flags的集合、缓存透明度与连接关系并非同一种继承过程，子定义宜明确给出需要的完整标志，不假定省略flags与重新写完整flags在所有缓存上等价。examine_action初次缺省none；继承时缺失通常保留父交互。harvest_by_season只更新指定季节；bash/deconstruct若整体缺失保留已有内容，若对象存在则其内部多数字段按自己的默认值重读。

extend/delete属于工厂及容器reader的编辑语法，不能对任意数值字段套用。mapdata并不提供统一透传的物品式material、weight、durability或建筑HP字段；墙体性能由下述地形、破坏及标志定义共同表达。

### relative、proportional与集合编辑

这些是读取器支持的字段，不是所有建筑数据通用的修改器。依据generic_factory.h的optional/mandatory、assign.h与assign.cpp：

| 字段/写法 | 支持范围及实际行为 |
|---|---|
| `relative` | 对使用普通optional读取的数值属性加差值，如coverage、comfort、light_emitted、terrain.heat_radiation及旧温度整数；也适用于shoot.chance_to_hit和prying_data的数值项。置于读取该属性的同层对象 |
| `proportional` | 同类optional数值乘倍率，倍率须为正且不等于1；直接属性优先于proportional，proportional优先于relative，整数结果按目标类型转换 |
| assign数值修改 | workbench.multiplier、plant_data的两个倍率及terrain.max_volume通过assign读取；其优先级是relative、proportional、直接字段，与optional不同 |
| `extend`、`delete` | 当前工厂alias的集合assign支持增删；必须保持相应读取器的集合类型和写法，不能据此推定flags、连接组或所有数组也支持 |
| 不适用的例子 | move_cost、move_cost_mod、required_str是mandatory直接读取，不自动使用relative/proportional；bash的str_min等直接get_int也不支持；furniture.max_volume使用专门volume_reader，不继承terrain.max_volume的assign能力 |

例如继承地形可以写`"relative":{"coverage":5}`，但不能用`"relative":{"move_cost":2}`替代必填或继承的move_cost。若要改变bash.str_min，应在bash对象直接给新值，并同时检查该子对象其他默认项被重读的影响。不要把mapgen.object、set或place_*负载放进这些修改器。

## 二、terrain专用字段

依据：`ter_t::load:1434`及检查函数。

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `move_cost` | 必填整数（继承可保留） | 局部地形移动代价，0不可通行；不是字符绘制优先级 |
| `trap` | trap ID，初始空 | 地形自带陷阱；与mapgen额外trap层区别，实际加载后解析为trap ID |
| `heat_radiation` | 整数，初值0 | 地形向周围辐射热的参数，不是核辐射 |
| `transforms_into` | terrain ID，初值空 | 供具体交互调用的变换目标；不会仅因定义该字段而自动按时间转化 |
| `roof` | terrain ID，初值空 | 当相应代码补上方地面时使用的地形；不是一个roof mapgen ID |
| `allowed_template_ids` | itype ID集合，默认空 | nanofab等对应检查动作允许的模板物品；不是建筑布局模板列表 |

terrain.open/close检查对应关系，锁门等场景存在特例；墙、门、窗本身都用terrain表示不同状态，开关动作实质是替换ID。move_cost不自动创建楼梯连接：上下通行还依赖GOES_UP/GOES_DOWN、梯子等标志及相邻层实际地块。

## 三、furniture专用字段

依据：`furn_t::load:1610`。

| 字段 | 类型/默认 | 实际含义 |
|---|---|---|
| `move_cost_mod` | 必填整数（继承可保留） | 修正地形移动代价；负值用于不可通行家具，与terrain.move_cost=0的写法不同 |
| `required_str` | 必填整数（继承可保留） | 家具移动/推拉相关需求；负值表示不可移动，不能解释成砸毁强度 |
| `bonus_fire_warmth_feet` | 旧温度尺度整数，读取缺省300 | 火源附近脚部保暖相关修正，转成温度差；不是家具主动发热值 |
| `keg_capacity` | 容积，初值0；接受legacy_volume_reader | 酒桶/液体储存容量，宜写显式单位；实际可用性取决于交互与标志 |
| `crafting_pseudo_item` | itype ID，初值空 | 让家具提供某个伪工具功能，物品模板决定品质等，不是生成可捡物品 |
| `deployed_item` | itype ID，初始空 | 家具与部署物品的关联，供对应回收/部署逻辑使用 |
| `workbench` | 可选对象，缺省无 | 工作台倍率与可处理工件上限 |
| `plant_data` | 可选对象，缺省无 | 家具形态的作物生长、收获倍率与转换 |
| `surgery_skill_multiplier` | 可选浮点数，缺省无 | 对应手术环境技能倍率；加载分支检查has_float，但json.h中该检查等同has_number，整数和小数均可读取 |

| 子对象字段 | 类型/初值 | 作用 |
|---|---|---|
| `workbench.multiplier` | float，1.0 | 工作台效率倍率，实际制造还受其他环境和角色条件影响 |
| `workbench.mass` | 质量字符串，初始质量最大值 | 工件质量开始受超限效率惩罚的阈值，不是超过立即拒绝 |
| `workbench.volume` | 容积字符串，初始容积最大值 | 工件容积的效率阈值，不是此格max_volume或硬性容纳上限 |
| `plant_data.transform` | furn ID，初始空 | 对应生长处理的转换家具 |
| `plant_data.base` | furn ID，初始空 | 收获等流程所用基础家具 |
| `plant_data.growth_multiplier` | float，1.0 | 生长所需年龄阈值的倍率，通常增大意味着更久，不应当作速度加成 |
| `plant_data.harvest_multiplier` | float，1.0 | 收获相关倍率 |

实际制造速度见[crafting.cpp](../../src/crafting.cpp)的workbench_crafting_speed_multiplier：超出质量或容积阈值后乘插值惩罚，附近足够的举升辅助还会影响质量检查，不能将阈值简化成绝对禁止制造。

workbench和plant_data在子对象出现时重新分配并读入，不能假定只覆盖某一个子字段就保留父子对象其余配置。作物放置要配合mapgen.sealed_item与种子；给普通家具加plant_data不等于地图生成时自动埋种。

## 四、bash与deconstruct全部子字段

依据：`map_bash_info::load:344`、`map_deconstruct_info::load:409`。这些定义决定破坏结果，mapgen不另提供“这堵墙更耐打”的逐格参数。

| bash字段 | 格式/读取默认 | 语义 |
|---|---|---|
| `str_min`、`str_max` | 整数，0、0 | 砸击强度的下上阈值；不是墙体HP上下限 |
| `str_min_blocked`、`str_max_blocked` | 整数，各-1 | 被BLOCKSDOOR等阻挡情形下的阈值覆盖，-1表示未提供专用值 |
| `str_min_supported`、`str_max_supported` | 整数，各-1 | 下方地块带SUPPORTS_ROOF（或关闭zlevels）时的阈值覆盖 |
| `explosive` | 整数，-1 | 特定破坏爆炸处理的参数，非通用物品爆炸对象 |
| `sound_vol`、`sound_fail_vol` | 整数，各-1 | 成功/失败音量，-1由底层推导 |
| `sound`、`sound_fail` | T，默认smash!/thump! | 成功/失败声响描述 |
| `collapse_radius` | 整数，1 | 倒塌相关搜索范围 |
| `destroy_only` | bool，false | 只在强制destroy类流程中破坏，普通砸击不按通常方式处理 |
| `bash_below` | bool，false | 破坏时涉及下层结构的开关 |
| `ter_set` | terrain的bash对象必填terrain ID | 砸毁后地形；不是所有家具破坏也需写 |
| `ter_set_bashed_from_above` | terrain ID，默认同ter_set | 从上方砸毁时采用的替换目标 |
| `furn_set` | furniture的bash读取，默认f_null | 家具破坏后的家具 |
| `items` | item_group ID或内联组；缺省空组 | 破坏掉落，按collection加载内联组 |
| `tent_centers` | furn ID数组，缺省空 | 与帐篷中心及整体拆毁识别相关 |

field主类型也借用map_bash_info并读取move_cost、msg_success，但它们不是terrain/furniture的有效bash子字段；不从共享C++结构推定建筑可以使用。

| deconstruct字段 | 格式/读取默认 | 语义 |
|---|---|---|
| `ter_set` | terrain拆解必填terrain ID | 拆解后地形 |
| `furn_set` | furn ID，默认f_null | 拆解后家具；terrain对象也可读取此项 |
| `deconstruct_above` | bool，false | 对上方对象的拆解处理开关 |
| `items` | 必填物品组ID或内联组 | 拆解材料，非bash掉落的自动复用 |

存在deconstruct对象才启用此拆解能力；完全未提供时can_do初值false。实际拆除需要的动作、时间和工具还可能由construction等独立系统控制，本对象不是完整施工配方。

## 五、shoot全部子字段

依据：`map_shoot_info::load:429`。

| 字段 | 格式/默认 | 语义 |
|---|---|---|
| `chance_to_hit` | 整数，100 | 射线击中该障碍的机会 |
| `reduce_damage` | 必填`[min,max]` | 普通弹射物穿过时的减伤范围 |
| `reduce_damage_laser` | 必填`[min,max]` | 激光对应减伤范围 |
| `destroy_damage` | 必填`[min,max]` | 弹射物对障碍破坏的伤害范围参数 |
| `no_laser_destroy` | bool，false | 激光是否禁止破坏该障碍 |

`map.cpp::shoot`先按chance_to_hit判定是否命中障碍，直接瞄准该格的hit_items分支则不作躲过判定；随后扣除对应随机减伤。破坏判定使用弹射物初始伤害D：以x_in_y(int(D)−destroy_damage.min, destroy_damage.max−destroy_damage.min)决定是否调用强制砸毁，属于阈值过渡而非随机给障碍扣一段HP。no_laser_destroy只抑制激光破坏分支。不能把coverage、chance_to_hit和reduce_damage合并成一个固定防御百分比。

## 六、切割与撬动活动对象的全部子字段

oxytorch、boltcut、hacksaw、prying均加载activity_data_ter/furn及activity_data_common，依据`mapdata.cpp:1721–1785`。

| 字段 | 格式/默认 | 语义 |
|---|---|---|
| `result` | terrain活动必填terrain ID；furniture活动默认f_null | 完成活动后的地块 |
| `duration` | 时间字符串，读取缺省1秒 | 活动基础持续时间，如`"30 seconds"`；实际时间可受工具与角色因素影响 |
| `message` | 可选T | 完成/处理文案，由对应活动消费者使用 |
| `sound` | 可选T | 活动作业声响文案 |
| `byproducts` | 可选对象数组 | 活动产物，不是item_group整体模式 |
| `byproducts[].item` | 必填itype ID | 产物物品 |
| `byproducts[].count` | 整数或`[min,max]`；成员初值0 | 固定或随机数量，负值截至0，倒序范围交换；不写时不会凭空产生一件 |
| `prying_data` | 可选对象 | 撬动机制参数 |
| `prying_data.prying_nails` | bool，false | 钉件拔除式撬动分支 |
| `prying_data.difficulty` | 整数，0 | 撬动难度 |
| `prying_data.prying_level` | 整数，0 | 撬动工具品质要求 |
| `prying_data.noisy` | bool，false | 撬动噪声相关开关 |
| `prying_data.alarm` | bool，false | 触发警报相关开关 |
| `prying_data.breakable` | bool，false | 失败时允许破坏的分支 |
| `prying_data.failure` | 可选T | 失败文案 |

每次加载terrain/furniture都会重建这四个活动数据指针；若子项继承时省略某活动对象，不应假定父对象对应活动能力仍保留。该行为不同于简单可选ID字段。

## 七、examine_action对象的全部内置actor

字符串方式调用[iexamine.cpp](../../src/iexamine.cpp)中注册的函数，不存在可任意追加的统一子字段。对象方式依据`mapdata.cpp::init_mapdata`当前仅注册三个actor；详细加载在[iexamine_actors.cpp](../../src/iexamine_actors.cpp)。

### appliance_convert

| 字段 | 格式/默认 | 作用 |
|---|---|---|
| `type` | 必填`appliance_convert` | 家具转电网设备actor |
| `item` | 必填itype ID | 对应设备物品，必须能解析到appliance部件 |
| `furn_set` | 可选furn ID，缺省无 | 转换时先替换原家具 |
| `ter_set` | 可选terrain ID，缺省无 | 转换时先替换地形 |

### cardreader

| 字段 | 格式/默认 | 作用 |
|---|---|---|
| `type` | 必填`cardreader` | 刷卡及可选黑客交互 |
| `flags` | 必填item flag集合 | 卡片有任一允许flag才可使用，非空有效性会检查 |
| `consume_card` | bool，true | 成功用卡后消耗所选卡片 |
| `allow_hacking` | bool，true | 允许黑客分支；非标准门变换需核查对应限制 |
| `despawn_monsters` | bool，true | 对当前OMT内带相应撤销标记的敌对怪物执行消除 |
| `omt_allowed_radius` | 可选整数，缺省无 | 相对卡片记录的生成OMT限制有效范围 |
| `mapgen_id` | 可选update ID | 存在时走地图更新，不再读取radius/terrain_changes/furn_changes分支 |
| `radius` | 整数，3 | 无mapgen_id时的局部变换半径 |
| `terrain_changes` | 旧terrain→新terrain对象，缺省空 | 半径内命中地形的变换 |
| `furn_changes` | 旧furniture→新furniture对象，缺省空 | 半径内命中家具的变换 |
| `query` | bool，true | 被读取并用于配置检查；当前call没有以query为条件跳过询问，有卡时仍直接query_yn(query_msg) |
| `query_msg` | 可选文案，默认空 | 询问文字，query为true而为空会诊断 |
| `success_msg` | 必填文案 | 成功文案 |
| `redundant_msg` | 必填文案 | 已打开或无目标可改变时的文案 |

allow_hacking的检查只认可特定标准金属门变换组合；自定义地图更新并不自动获得相同黑客效果。此表记录真实分支，不以通用开门器理解cardreader。

### effect_on_condition

| 字段 | 格式/默认 | 作用 |
|---|---|---|
| `type` | 必填`effect_on_condition` | EOC检查交互actor |
| `effect_on_conditions` | EOC ID或内联EOC对象数组 | 按顺序激活；为对话上下文提供this家具ID及pos绝对坐标 |

EOC本体condition/effect等属于独立表达式系统，不是地形或家具的直接属性。本篇不重新定义其全部语法。

## 八、建筑行为核对

| 编写目标 | 必须核查的层次 |
|---|---|
| 墙、窗、门是否可通行/可透视 | move_cost或move_cost_mod、TRANSPARENT及相关标志，不由rows符号形状决定 |
| 是否可开关、从哪一侧开关、是否锁住 | open/close、LOCKED及OPENCLOSE_INSIDE等标志、对应动作 |
| 是否能砸毁/拆解、掉什么 | bash、deconstruct以及活动数据，材料叙述不提供自动掉落 |
| 是否有上方楼面及室内环境 | roof补面逻辑、显式上层mapgen、INDOORS/NO_FLOOR等标志及相邻层布局 |
| 是否支撑与可能倒塌 | SUPPORTS_ROOF等标志和map破坏/倒塌函数，不是定义一个roof就完整解决 |
| 是否能制造、存液、休息或种植 | crafting_pseudo_item/workbench、keg_capacity、comfort/保暖、plant_data和对应交互标志 |
| 是否易燃、助燃或阻火 | FLAMMABLE及相关flag与火焰消费逻辑，地形不从一个自造material字段推断性质 |

flags可取值很多，字段盘点附原版实际使用集合；完整语义应同时查[JSON_FLAGS.md](../../doc/JSON_FLAGS.md)、mapdata的标志注册以及具体消费代码。地形家具标志、物品标志、Overmap标志、mapgen flags属于不同系统，名称相似也不能互换。
