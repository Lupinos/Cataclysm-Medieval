# 原版建筑 mapgen JSON 编写与源码机制

对应策划：[06 聚居地的类型及其分案](../design/design06-建筑.md)。本篇提供具体建筑及地块的原版 JSON 依据，建筑选型与空间关系见策划案。

## 一、范围与阅读入口

本调查以当前工作树C++实现和原版JSON为准，覆盖具体建筑的布局、地形家具、物品与生物投放、模块复用、分层和局部更新。原版没有统一的BUILDING主类型：住宅、店铺、作坊、城堡式建筑及特殊独立建筑共享mapgen体系。建筑可以横跨多个24×24地块，也可以只占其中一部分；一条mapgen声明不等于一种建筑。

本文不调查Overmap选址、出现次数、城市道路或聚居地生成；`om_terrain`仅解释为绑定生成器所必需的入口。也不将原版所有现代建筑改造成中世纪建筑。引用物品组、怪物组、NPC模板、载具、陷阱、EOC时，记录建筑侧字段与引用边界，不重复展开这些独立系统的完整数据模式。

| 文档 | 内容 |
|---|---|
| 本篇 | 声明入口、布局、palette、随机参数、set、flags、嵌套、更新与多层规则 |
| [内容放置字段](guide06_building_placement.md) | 每种符号映射和坐标放置器、子字段、默认值、概率、坐标消费方式 |
| [建筑地形与家具](guide06_building_terrain_furniture.md) | terrain/furniture全部直接加载字段及专用子对象，墙门窗、屋顶、破坏、交互 |
| [全量字段盘点](guide06_building_inventory.md) | 原版声明分布、归一化字段路径、显式出现次数与可定位实例 |

主要源码：[mapgen.cpp](../../src/mapgen.cpp)的`load_mapgen`、`setup_common`、各`jmapgen_*`、`generate/nest/update_map`；[mapgen.h](../../src/mapgen.h)的坐标及阶段定义；[mapdata.cpp](../../src/mapdata.cpp)的地形家具加载；[init.cpp](../../src/init.cpp)的类型注册。原版文档[MAPGEN.md](../../doc/MAPGEN.md)用于交叉核对，冲突时按本地执行代码说明。

## 二、声明入口全部字段

依据：`mapgen.cpp:619–752`。JSON文件顶层通常是对象数组；文件名不提供继承或绑定。`type`由类型分发器读取；mapgen与palette不走物品的通用继承流程。

| 字段 | 格式、必填及默认 | 代码效果与限制 |
|---|---|---|
| `type` | 独立声明必填，`"mapgen"` | 分发到`load_mapgen`；内嵌生成器不需要再写type |
| `om_terrain` | 普通生成器入口；字符串、字符串数组或二维字符串数组 | 字符串绑定一个mapgen key；一维数组把同一配方绑定多个key；二维数组按地块网格切分一张较大布局 |
| `nested_mapgen_id` | 嵌套生成器的字符串ID | 定义可复用局部模块，不是已有地形ID；由`place_nested/nested`调用 |
| `update_mapgen_id` | 更新生成器的字符串ID | 定义作用于已有地图的更新配方，由任务、EOC等显式触发 |
| `method` | 必填；普通为`json`或`builtin`；nested/update仅支持`json` | 不支持任意脚本方法；普通json要求object对象 |
| `object` | json方法必填，对象 | 实际布局及内容，详见后文 |
| `weight` | 普通默认1000；整数或`dbl_or_var`；nested为整数、默认1000 | 同key普通配方或同nested ID的候选权重；不是百分比。普通权重小于1不参与选择；动态权重生成时重算。update加载器不读weight，不能用它随机选择更新 |
| `disabled` | 仅普通入口读取，bool，默认false | 为true直接跳过该候选；nested/update分支不支持此开关 |
| `name` | builtin方法必填，已注册的C++函数名 | 非玩家建筑名，不等于建筑ID |
| `//`、`//…` | JSON注释成员 | 说明文字，不是生成属性；不在字段统计中当功能字段 |

入口优先级是`om_terrain`数组、`om_terrain`字符串、`nested_mapgen_id`、`update_mapgen_id`，不是同时注册多个身份。不要在一个对象中混填这些入口。普通mapgen没有通用`id`、`abstract`、`copy-from`、`extend`、`delete`继承语义；同key多条声明是候选，不是自动覆盖或合并。

`om_terrain`绑定的是生成key：普通可旋转地形使用其基础类型ID，线状地形使用带布局后缀的生成key，见[overmap.cpp](../../src/overmap.cpp)的`oter_t::get_mapgen_id`。这里不展开对应大地图定义。

## 三、object的布局与控制字段

依据：`mapgen.cpp:4327–4608`。

| 字段 | 格式及默认 | 适用性与效果 |
|---|---|---|
| `fill_ter` | 单一terrain ID字符串，普通默认t_null | 普通地图首先整体填底；不是mapgen_value，不支持直接写distribution对象。nested和update没有读取或铺设该字段 |
| `rows` | 字符串数组，可省略但须符合下面的底图条件 | 每个显示列对应一格，左上(0,0)，x向右、y向下；普通为24行×24列，二维om_terrain布局为完整拼图尺寸 |
| `terrain` | 字符→地形值的对象 | 对rows的字符放置地形，详见palette；不是在这里定义新墙体属性 |
| `furniture` | 字符→家具值的对象 | 对rows放家具；同字符可以同时有地形、家具及物品 |
| `palettes` | palette ID或mapgen_value组成的数组 | 导入符号操作与参数，可多层引用；导入顺序与追加规则见下节 |
| `mapping` | 字符→包含各放置通道的对象 | 把一个字符的terrain/furniture/items等集中写在一起；与分类字典写法共用加载器 |
| `parameters` | 参数名→参数定义 | 在palette加载路径读取；当前setup_common只在存在rows时加载临时palette，所以无rows的mapgen不能仅写此字段就期待参数生效 |
| `set` | 操作对象数组 | 点、线、矩形绘制或清理，详见第六节 |
| `flags` | jmapgen flag字符串数组，默认空 | 生成上下文控制；不是terrain flags或nested条件中的邻居flags |
| `rotation` | 整数或整数范围，默认0，单位为90°次数 | 普通mapgen在放置后旋转，并再应用地形朝向。nested读取但`nest()`未应用；update不读取object.rotation |
| `mapgensize` | nested必填`[N,N]` | 当前仅支持非零正方形模块；普通mapgen显式禁止。update也不读此字段，不因此改变24×24更新坐标范围 |
| `predecessor_mapgen` | 普通地图可选，基础地形ID | 先调用其生成器，再叠加当前布局；不是JSON字段继承。先fill_ter、再predecessor、再当前放置 |
| `fallback_predecessor_mapgen` | 普通地图可选，默认空 | 启用动态前驱模式；有记录前驱时生成前驱，无记录时用此ID兜底；与固定predecessor并用会报诊断 |

其余object字段全部属于[放置器通道表](guide06_building_placement.md)，包括现代设施、低频清理及变量字段。

### 底图、尺寸与空白符

普通mapgen需要有效fill_ter、固定/动态前驱，或带足够地形定义的rows。当前keys_with_terrain仅从分类terrain字典及导入palette登记；只在mapping内部写terrain不会登记同样的底图校验键，因此纯mapping布局应提供fill_ter或其他有效底图。没有底图时不能只放家具或物品。nested与update假设已有底图，允许只写局部操作；无地形映射的字符保持原地面，空格和点号没有通用“草地”含义。

行列数按当前布局的完整尺寸严格检查；默认单地块是24×24，坐标0–23。二维om_terrain数组的列行分别乘24，rows给出整个拼图，各生成器按自己的偏移读取24×24区域。坐标放置条目也按当前区块偏移过滤，坐标范围不能跨越某个区块的边界。不要用二维om_terrain数组表达不同楼层，它只表示平面拼图。

符号键通过UTF-8显示宽度检查，必须占一列；地图符号与terrain的渲染symbol是两套独立概念。为使布局可核查，通常采用单列ASCII。即使有fill_ter，非空格、非点号的未定义符号仍可能触发诊断。

## 四、palette及全部映射通道

依据：`mapgen.cpp:3928–4323`。

| 字段 | 格式与用途 |
|---|---|
| `type` | 命名palette声明使用`"palette"` |
| `id` | 命名palette必填字符串；相同ID再次加载会替换存储项，不是copy-from继承 |
| `palettes` | 递归引用其他palette；可用字符串或mapgen_value选择 |
| `parameters` | 与object.parameters相同；参数同名时检查scope、type、默认值一致性，不作任意覆盖 |
| `mapping` | `{"符号":{"terrain":值,"furniture":值,"items":对象,…}}` |
| 各通道字典 | `{"符号":放置值}`；所有通道与对应坐标写法见放置器文档 |

导入palette的每个符号操作列表会依次追加，再追加本地操作。本地地形通常在同阶段最后写入而呈现覆盖效果；这不是“整个符号被替换”：旧的物品、怪物等操作仍会执行，重复导入也可能重复生成。`mapping`中的同通道先加载，分类字典中的同通道再加载。

terrain、furniture、traps支持字符串、mapgen_value或候选数组；候选数组在每次放置时选一个，`[["t_a",3],["t_b",1]]`通过重复候选实现权重。这里是逐格选择，不能保证整栋建筑墙材一致。其他通道通常接受对象或对象数组，数组表示全部操作而非随机选一。`loot`没有符号通道，`place_loot`只支持坐标数组。`sealed_item`有符号通道而无`place_sealed_item`入口。

以terrain为例：分类字典的`"terrain":{"#":"t_wall_wood"}`与坐标式`"place_terrain":[{"x":5,"y":5,"ter":"t_wall_wood"}]`的负载字段不同；不能直接将分类字典的对象结构复制到坐标条目。

## 五、随机值、参数及作用域

### 整数范围 jmapgen_int

`x/y/repeat/amount/chance`等字段只有使用jmapgen_int的读取器才接受整数、`[值]`或`[最小,最大]`。范围端点包含，`get()`每次读取会重新取随机值。它不是通用“覆盖整片区域”：单物品、地形、家具、NPC通常从范围选一个点；物品组、怪物组、归属、区域等消费者会用范围边界作为矩形。各放置器详见对应文档。

`repeat`默认1。坐标和某些负载都可能读到repeat，执行时取两者随机结果的较大值，而不是两者相乘。不要用amount、repeat和pack_size互相替代。

### ID值 mapgen_value

适用于加载器使用mapgen_value的ID字段；不是每个字符串字段都支持。

| 写法/字段 | 格式与效果 |
|---|---|
| 固定值 | `"t_wall_wood"`等ID字符串 |
| `param` | 参数名字符串，取当前生成上下文的该参数 |
| `fallback` | 可选的固定ID，参数缺失时使用；overmap_special作用域的引用要求提供，以兼容已保存的参数数据 |
| `distribution` | 字符串或`[ID,整数权重]`数组，省略权重时为1；每次消费直接抽取 |
| `switch` | 一个mapgen_value对象，通常为`{"param":"参数名"}` |
| `cases` | switch结果字符串→固定ID映射；无通用default分支，必须覆盖全部可能结果，否则诊断并返回空ID |

对象识别顺序为param、distribution、switch；不要混用多个选择方式。空ID是否代表不操作取决于具体放置器；多数在执行前检查空值，不能把空ID当作跨通道的通用擦除操作。

### 参数定义的全部字段

| 字段 | 必填/默认 | 作用 |
|---|---|---|
| `type` | 必填，cata_variant类型字符串 | 常用`ter_str_id`、`furn_str_id`、`itype_id`、`palette_id`、`string`等；必须匹配消费字段 |
| `default` | 必填，固定字符串或mapgen_value对象 | 计算默认参数值。参数只通过字符串或字符串型选择表达结果，不是任意JSON嵌套对象 |
| `scope` | 默认`overmap_special` | `overmap_special`为整组地点共享的持久选择；`omt`为当前地块生成；`nest`为每次模块嵌入 |

同一distribution直接放到每个墙符号上会逐格抽样；先将分布写到参数default，再由各墙引用同一参数，才能保持对应作用域的一致材质。nested引用中非nest参数会向外合并，nest参数留给每次嵌入。随机palette选择可能创建内部overmap_special作用域参数，使多地块建筑保持一致。

普通mapgen顶层weight另外使用`dbl_or_var`，依据[condition.cpp](../../src/condition.cpp)的`get_dbl_or_var`：接受数值、上下界二元数组或变量/表达式对象。对象可为math、旧arithmetic或变量描述，由该独立表达式系统解析；此能力不能推及nested.weight、place_loot.chance等普通整数字段。

## 六、set对象的全部字段与操作

依据：`mapgen.cpp:895–1015、4739–5017`。

| 字段 | 格式/默认 | 作用 |
|---|---|---|
| `point` | 操作名字符串，与line/square择一 | 操作随机抽取的一个坐标点 |
| `line` | 操作名字符串 | 从(x,y)画到(x2,y2)，含端点 |
| `square` | 操作名字符串 | 两角围成的填充矩形，非仅轮廓 |
| `set` | 旧的point别名 | 加载器仍接受并发出弃用诊断；新内容用point |
| `x`、`y` | 必填jmapgen_int | 起点，每次操作读取时可重新抽样 |
| `x2`、`y2` | line/square必填jmapgen_int | 终点；point不使用 |
| `id` | 地形/家具/陷阱操作必填固定ID；variable为变量名 | 不支持mapgen_value；移除陷阱仍要给trap ID |
| `amount` | radiation必填jmapgen_int | 设置辐射数值；不是bash力度 |
| `chance` | 普通整数，默认1 | `one_in(chance)`，1必执行、2为一半；在repeat循环前抽一次 |
| `repeat` | jmapgen_int，默认1 | 通过chance后重复操作 |
| `rotation`、`fuel`、`status` | 整数，读取默认0、-1、-1 | 兼容读取遗留字段；当前set执行switch不消费它们，不能放置载具或旋转建筑 |

| 操作名 | 真正效果 | 形状支持 |
|---|---|---|
| `terrain` | 写地形 | point、line、square |
| `furniture` | 写家具，可明确写f_null清空 | point、line、square |
| `trap` | 设置陷阱 | point、line、square |
| `trap_remove` | 只移除指定类型陷阱 | point、line、square |
| `creature_remove` | 杀死当前位置生物，排除玩家角色 | point、line、square；与静默删除NPC不是同一机制 |
| `item_remove` | 清空地面物品 | point、line、square |
| `field_remove` | 清除全部场效应 | point、line、square |
| `radiation` | 设置辐射值 | point、line、square |
| `bash` | 以9999力度执行砸击 | 仅point有执行分支，不以amount定力度 |
| `variable` | 将绝对坐标排队写入命名变量 | 仅point有执行分支；不是设置任意数值变量 |

解析器对操作名和形状的组合没有完整拦截，line/square的bash、variable不能因“被接受”就认为可生效。set.terrain直接调用地形设置，与jmapgen_terrain对旧内容的清理诊断不同，不应假定所有地形通道具有相同副作用。

## 七、全部jmapgen flags

依据：`mapgen.cpp`的flag枚举转换、`jmapgen_terrain::apply`及`check_common`；[jmapgen_flags.h](../../src/jmapgen_flags.h)。

| flag | 效果 |
|---|---|
| `ALLOW_TERRAIN_UNDER_OTHER_DATA` | 换地形时允许保留家具、陷阱和物品 |
| `DISMANTLE_ALL_BEFORE_PLACING_TERRAIN` | 拆解家具、解除陷阱，保留物品及掉落物 |
| `ERASE_ALL_BEFORE_PLACING_TERRAIN` | 删除家具、陷阱与物品 |
| `ALLOW_TERRAIN_UNDER_FURNITURE` | 允许保留家具 |
| `DISMANTLE_FURNITURE_BEFORE_PLACING_TERRAIN` | 尝试拆解家具并产出材料，必要时沿破坏结果递归 |
| `ERASE_FURNITURE_BEFORE_PLACING_TERRAIN` | 直接清除家具及对应标牌文字 |
| `ALLOW_TERRAIN_UNDER_TRAP` | 允许保留陷阱 |
| `DISMANTLE_TRAP_BEFORE_PLACING_TERRAIN` | 按解除陷阱逻辑处理 |
| `ERASE_TRAP_BEFORE_PLACING_TERRAIN` | 直接清除陷阱 |
| `ALLOW_TERRAIN_UNDER_ITEMS` | 保留地面物品 |
| `ERASE_ITEMS_BEFORE_PLACING_TERRAIN` | 删除地面物品 |
| `NO_UNDERLYING_ROTATE` | update不为适配原地形朝向而临时反旋转已有地图 |
| `AVOID_CREATURES` | set的地形、家具、陷阱等已传递此参数的操作避开生物；不是对所有放置器的统一碰撞保证 |

全局三种清理策略彼此互斥，各类家具/陷阱/物品策略各自互斥；专用策略覆盖全局策略。flags是生成上下文；mapgendata的带flags构造器用当前配方的集合替换父集合，nested未写flags时也不自动沿用父清理策略。需要控制模块覆盖行为时应在对应模块中明确声明。普通WALL且不带PLACE_ITEM的地形会直接清理家具、陷阱和物品，即使选择保留策略也不能据此在实墙内保留这些内容。

## 八、嵌套模块与更新地图

### 嵌套模块

定义使用nested_mapgen_id、method=json、object.mapgensize=[N,N]。调用使用place_nested，字段与邻居条件全部见[放置器文档](guide06_building_placement.md)。先按chunks权重选择ID，再按该ID下候选weight选择具体配方，是两次选择。模块内部坐标以调用点为偏移，不需要另写全局坐标。

当前实现读取nested.rotation，但`mapgen_function_json_nested::nest`中应用旋转的代码仍是注释；不要依赖它随机旋转房间。应选有明确方向的模块。加载检查声称要求正数，实际条件为`x == 0 || x != y`，并未完整检查负值；新内容仍须使用正的N，不能将校验漏洞当作负尺寸功能。

### 更新地图

update使用已有底图，允许无rows直接写set或place_*。object.fill_ter、mapgensize、rotation、固定/动态predecessor未由update.setup_internal读取，不会获得普通生成器的对应能力。支持的rows、palette和放置器仍由setup_common加载。

同update ID可以存多条，但`run_mapgen_update_func`当前只调用列表第一条，不作weight随机，也不自动依次执行所有同名更新。更新调用侧可带旋转、水平/垂直镜像和参数，这些不是object字段。更新还会按已有地形朝向临时校正方向，NO_UNDERLYING_ROTATE用于抑制这一步。

verify/cancel_on_collision主要检查载具碰撞，不是完整的生物、结构或物品安全校验；set碰撞在阶段执行中检查，也不应宣称为可回滚事务。建筑稿不在此推导任务/EOC调用侧的完整字段模式。

## 九、实际执行顺序与覆盖

`mapgen.h::mapgen_phase`规定阶段：清理→地形→家具→普通内容→nested→转换→归属→zone。JSON对象键的书写先后不改变该顺序。每阶段先set操作，再其他放置器；同阶段稳定排序保留实际加载次序。坐标通道按setup_common固定顺序读入，并不是按照JSON文本顺序。

普通地图流程：fill_ter→前驱底图→分阶段操作→区域地形/家具替换→object.rotation→地形朝向旋转→写入排队坐标变量。区域伪ID在放置车辆前也会进行必要解析，以供碰撞判断。nested独立执行一轮阶段，所以它的家具或地形可以晚于父地图的普通物品放置，覆盖父内容时须选择正确策略。

物品、怪物、家具不会因为同一字符重复出现就共享一个随机结果；一致性取决于参数作用域。palette本地操作追加、嵌套后覆盖、更新已有内容三种情况须分别判断，不能统一称为“继承”。

## 十、多层建筑、墙门窗与屋顶

一条普通mapgen描述当前z层的平面，没有建筑层数、楼高、房间对象或自动房顶字段。上层、屋顶、地下室各有对应平面；上下层楼梯、梯子和洞口要在局部坐标与方向上对齐。跨层绑定由调用侧负责，本文不展开大地图声明。

墙、门、窗、地板是terrain ID；床、桌、工作台等通常是furniture ID。开门、锁门、窗帘、破坏和屋顶回填由这些地块定义及代码决定，不是mapgen符号自带能力。地形定义的roof供`map::get_roof/add_roofs`等在特定流程中补上方地面；它不生成一整栋建筑的上层室内和屋顶陈设，也不由SUPPORTS_ROOF自动绘制屋顶。完整字段见[建筑地形与家具](guide06_building_terrain_furniture.md)。

## 十一、原版实例的阅读顺序

| 实例 | 可确认的写法 |
|---|---|
| [cabin.json](../../data/json/mapgen/cabin.json) | 独立小屋、底图、rows与投放；同类候选的实际结构 |
| [house_rural.json](../../data/json/mapgen/house/house_rural.json) | 农村住宅的布局与院外空间 |
| [hunting_lodge.json](../../data/json/mapgen/hunting_lodge.json) | 多地块建筑及分层配方 |
| [lakeside_cabin.json](../../data/json/mapgen/lake_buildings/lakeside_cabin.json) | 屋内布局与水岸边界 |
| [lighthouse.json](../../data/json/mapgen/lake_buildings/lighthouse.json) | 塔状建筑的多层坐标与各层内容 |
| [domestic palettes](../../data/json/mapgen_palettes) | 通用住宅符号、物品及参数组合 |

实例只作为语法和组合参照，现代家具、怪物、物品组不因此进入中世纪选型。字段盘点提供目录外低频字段的实际实例，不只抽查住宅目录。

## 十二、最小布局示例

以下是语法完整的普通mapgen例子；om_terrain为示例绑定名，需由实际调用侧提供对应key。不是向游戏新增建筑的可直接加载补丁，不自动包含屋顶或地下室。

```json
{
  "type": "mapgen",
  "om_terrain": "example_house",
  "method": "json",
  "weight": 1000,
  "object": {
    "fill_ter": "t_grass",
    "rows": [
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "      ############      ",
      "      #..........#      ",
      "      #.b........#      ",
      "      #..........#      ",
      "      w..........w      ",
      "      #..........#      ",
      "      #..........#      ",
      "      #..........#      ",
      "      #..........#      ",
      "      #..........#      ",
      "      #####+######      ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        "
    ],
    "terrain": {
      "#": "t_wall_wood",
      ".": "t_floor",
      "+": "t_door_c",
      "w": "t_window",
      "b": "t_floor"
    },
    "furniture": {
      "b": "f_bed"
    },
    "place_items": [
      {
        "item": "bedroom",
        "x": 8,
        "y": 8,
        "chance": 50
      }
    ]
  }
}
```

示例用fill_ter承接未映射的空格，以rows明确墙、门窗、室内地板和床。物品组用独立坐标条目写明机会，不将物品内容藏在墙材参数中。房间只是这些地形、家具及出入口在平面上的组合，没有单独的room字段。

## 十三、参数化palette、模块与更新示例

下面三个声明展示各自的数据位置，示例ID尚未注册到游戏；没有写出的大地图绑定和调用侧不在本例中隐含存在。它们是独立的语法示例，不会自行嵌入上节住宅。

```json
[
  {
    "type": "palette",
    "id": "example_wall_palette",
    "parameters": {
      "example_wall": {
        "type": "ter_str_id",
        "scope": "omt",
        "default": { "distribution": [ [ "t_wall_wood", 3 ], [ "t_wall", 1 ] ] }
      }
    },
    "terrain": { "#": { "param": "example_wall" } }
  },
  {
    "type": "mapgen",
    "nested_mapgen_id": "example_bed_corner",
    "method": "json",
    "object": {
      "mapgensize": [ 3, 3 ],
      "rows": [ "...", ".b.", "..." ],
      "terrain": { ".": "t_floor", "b": "t_floor" },
      "furniture": { "b": "f_bed" }
    }
  },
  {
    "type": "mapgen",
    "update_mapgen_id": "example_clear_corner",
    "method": "json",
    "object": {
      "place_remove_all": [ { "x": [ 7, 9 ], "y": [ 7, 9 ] } ]
    }
  }
]
```

使用palette时在带rows的普通object中写`"palettes":["example_wall_palette"]`；此例scope=omt使同一地块内墙材一致。需要整个多格多层地点共享时选择overmap_special，并在param引用中提供fallback。

嵌入调用示例为`"place_nested":[{"x":10,"y":10,"chunks":[["example_bed_corner",100]]}]`，把3×3模块放在(10,10)至(12,12)。若底图已经有家具和物品，应结合模块是否换地形选择清理策略，不能依赖object字段书写顺序。

更新示例清空3×3区域的家具、物品、陷阱、场、graffiti及相交载具，保留地形；它不是“把房间恢复成空地”。执行入口需由任务/EOC或其他调用者明确指定example_clear_corner。
