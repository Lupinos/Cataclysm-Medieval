# 原版武器 JSON 编写与源码机制

对应策划：[04 武器体系及其分案](../design/design04-武器.md)。本篇提供原版武器 JSON 的编写与字段依据，具体装备选型和游戏定位见策划案。

<a id="scope"></a>
## 一、先从一把剑开始

在CDDA里，编写武器就是定义一个物品，再给它配置攻击、携带和使用方式。最省事的起点是找一件用途接近的原版物品，继承它，再修改需要改变的地方。

下面是一把武装剑的完整派生示例。它沿用原版中碳钢武装剑的工具功能、材料、格挡技巧和剑鞘标记，只重新指定名称、说明、大小和近战伤害。

```json
[
  {
    "type": "TOOL",
    "id": "example_arming_sword",
    "copy-from": "mc_arming_sword",
    "name": { "str": "example arming sword" },
    "description": "A single-handed sword selected for this example.",
    "weight": "1200 g",
    "volume": "1500 ml",
    "longest_side": "95 cm",
    "melee_damage": { "bash": 6, "cut": 26, "stab": 12 },
    "to_hit": { "grip": "weapon", "length": "long", "surface": "any", "balance": "neutral" }
  }
]
```

可以把这段定义分成四部分阅读：

1. `type`、`id`、`copy-from`说明它是什么物品、用什么ID、从哪里继承。这里使用TOOL，是因为所选原版父项也是TOOL，并带有切割等工具用途。剑并不一律必须写成TOOL。
2. `name`、`description`是玩家看到的名称和说明。ID是程序引用的名字，与显示名称分开。
3. `weight`、`volume`、`longest_side`分别是重量、收纳体积和最长边。它们会影响攻击耗时、携带或能否装入刀鞘。
4. `melee_damage`给出近战伤害，`to_hit`给出命中修正。它们仍需经过角色属性、技能、技巧和目标护甲的计算，才得到一次攻击的实际结果。

这段示例可以帮助理解结构，但不是所有武器的统一数值模板。实际制作时，还要检查从父项继承来的材料、flags、技巧和工具品质是否适合新装备。

### 这份指南怎么读

第一次编写近战武器，先读第二章的继承、第三章的物理参数和第四章的近战参数。制作投矛时再读第五章；制作弓弩时接着读第七至九章。只有需要配件、特殊技巧或状态切换时，才需要第十至十二章的详细表格。

按需跳转：[类型与继承](#identity)、[重量与材料](#common)、[近战](#melee)、[投掷](#throw)、[伤害写法](#damage-instance)、[弓弩与枪械](#gun)、[弹药](#ammo)、[弹仓与刀鞘](#magazine)、[配件](#gunmod)、[技巧](#techniques)、[状态切换](#actions)、[原版实例](#examples)、[检查方法](#validation)。

本指南保留详细字段表，方便写到某个参数时查阅。表中的“初值”是全新物品未设置该参数时的起始值；继承物品通常沿用父项的值。“读取默认”是游戏读取JSON时使用的缺省值。两者有时不同，游戏还可能在加载完成后补全数据，因此不能把代码里出现的每个0或1都当作默认值。

文中少量源码术语可按下表理解，读一般示例时不必先研究C++：

| 术语 | 在本文中的意思 |
|---|---|
| 字段 | JSON中的一个设置项，例如weight |
| 主类型 | type指定的物品类型，例如TOOL、GUN、AMMO |
| 开关 | true表示开启，false表示关闭 |
| 功能槽 | 物品具备的一组功能数据，例如射击、弹药或护甲；一个物品可以兼有几组功能 |
| 加载后的整理阶段（finalize） | 游戏读完定义后，补默认值、计算派生数据、检查引用的阶段 |
| 运行时 | 实际挥剑、装填、射击或收纳物品时 |

武器的历史形制和游戏定位由design文档确定，这里说明如何用原版支持的字段把设计写出来。需要追查依据时，可看文末的源码导航；需要查字段出现次数和原版用例时，可看[字段盘点](guide04_weapons_inventory.md)。盘点统计的是JSON定义条目，包含模板、材料变体和可作武器的日用品，不等于独立武器种类数。

<a id="identity"></a>
## 二、主类型、身份与继承

### 先决定物品类型

先看武器怎么使用，再选type：普通近战物品可以用GENERIC；要复用工具功能时可用TOOL；弓、弩和枪都用GUN，射出去的箭矢或弹丸用AMMO。CDDA没有统一的WEAPON类型。

“弓为什么也叫GUN”可以理解为引擎把它们都归入“装填弹药后发射”的系统。这里的名字指程序功能，并不表示弓在游戏世界里是一把火枪。

| type或槽 | 用途 | JSON位置 |
|---|---|---|
| `GENERIC` | 普通剑、斧、棍、矛、石块等，无专用武器槽 | 通用字段放顶层 |
| `TOOL` | 有工具供电、消耗、激活动作的物品，仍可近战 | 工具槽字段放顶层，再读通用字段 |
| `ARMOR`、`TOOL_ARMOR` | 可穿戴武器、盾或带甲功能物品 | 护甲字段及通用字段；TOOL_ARMOR另有工具槽 |
| `GUN` | 所有用射击流程的发射器，包括弓、弩、投石索 | gun槽字段放顶层 |
| `AMMO` | 箭、弩矢、弹丸、枪弹等 | ammo槽字段放顶层 |
| `MAGAZINE` | 可拆弹匣及其他弹药容器方案 | magazine槽字段放顶层；容量还需结合pocket |
| `GUNMOD` | 装在发射器上的配件、部分可独立近战配件 | gunmod槽＋mod公共槽＋通用字段 |
| `gun_data`、`ammo_data`、`gunmod_data` | 在其他主类型物品上增加对应槽 | 嵌套对象；不是任意顶层字段均自动进入槽 |
| `armor_data` | 武器或弹匣具有穿戴功能 | 复用护甲槽，细节见[服装指南](guide02_clothing_json.md) |

不要把武器实例写成 `weapon_category` 或 `technique`：这些是关联定义的type。`category`是背包分类；`weapon_category`是武术与武器适用性分类；GUN的`skill`才是射击技能，三者不同。

### 身份与文本字段

| 字段 | 格式 | 实际规则与用途 |
|---|---|---|
| `type` | 类型字符串 | 决定调用哪个加载器；必须用注册类型 |
| `id` | 字符串 | 可生成物品的唯一标识；引用的是ID，不是名称 |
| `abstract` | 字符串 | 仅作继承模板，与具体id择一；不生成实物 |
| `copy-from` | 父ID字符串 | 复制已加载的具体模板或abstract；找不到暂缓读取，不等于自动创建不存在的父物品 |
| `name` | 可翻译字符串或`{"str":"...","str_pl":"..."}` | 当前`load_basic_info`每次重建并要求读取name，不能以为子项可省略；不可数可用`str_sp` |
| `description` | 可翻译字符串/对象 | 缺失保留父说明；应表达玩家用途，结构与时代由设计确定 |
| `symbol` | 单字符字符串 | 地图字符，不决定武器类型 |
| `color` | 颜色字符串 | 地图显示颜色，不代表材质品质 |
| `looks_like` | 物品ID | 贴图回退线索，不继承战斗参数；copy-from会建立相关回退 |
| `category` | item_category ID | 强制物品分类；不提供剑术适用性 |
| `ascii_picture` | ASCII图ID | 物品信息图 |
| `snippet_category` | 片段组ID或内联数组 | 内联数组生成自动组；当前缺失会重设为空，不能按普通父值保留推断 |
| `expand_snippets` | 开关，初始false | 将说明中的片段展开到实例 |
| `//`及`//...` | 注释数据 | 不产生伤害、属性或flag；如`//range`不等于range |

### 外观变体与条件名称

`variant_type`是外观类别枚举，不是物品主type；当前通用加载缺失按generic读取；可用值为generic与gun。`variants`为数组，每项读取`id`、`name`、`description`，可选`symbol`、`color`、`ascii_picture`、`weight`、`append`、`expand_snippets`。这里`weight`是抽取权重（读取默认1），不是武器克重；`append`决定追加说明。不同伤害、材料、大小和装填结构应使用不同物品定义，不能放进外观variant。

`conditional_names`数组每项有`type`条件枚举、`condition`、`name`及可选`value`（默认空）。它只改变显示名，不能当作装备状态机；当前type枚举为FLAG、COMPONENT_ID、COMPONENT_ID_SUBSTRING、VAR、SNIPPET_ID，具体条件判断查conditional_name。

### 继承时，哪些值会保留，哪些会被替换

copy-from可以省掉大量重复配置，但不能简单理解成“只改我写出的那几个数字”。有些字段可以单项调整，有些一写就会替换整组内容。写派生物品时，先确定自己是在保留父项、追加内容，还是重新定义整项。

下面保留详细规则供查阅；初次使用时，可以先看本节后面的斩击伤害示例。

- 标量常由`assign`支持`relative`、`proportional`；能否使用这些修改方式，要看该字段的读取代码，不能对所有字段通用套用。
- `flags`、`effects`等集合直写通常替换；`extend`追加、`delete`删除由相应字段的读取代码实现。
- `melee_damage`直写重建整个伤害表；`relative.melee_damage`和`proportional.melee_damage`在加载后的整理阶段单独处理，先乘比例并向下取整，再加增量并向下取整。
- `techniques`直写先清空；缺失时读`extend.techniques`与`delete.techniques`。
- `qualities`直写先清空；缺失时支持extend、delete、relative专用分支。`charged_qualities`直写清空，没有同样完整的补丁分支。
- `material`直写先清空，再重新读取；`replace_materials`在通用读取末尾执行，按材料portion与密度比同步调整重量，也更新相关repair材料和护甲分区。不是单纯重命名材质。
- `pocket_data`、`modes`等结构不按ID或身体部位自动深度合并。`modes`直写清空重建。
- `to_hit`对象每次使用新的局部acc_data；只写一个子键时其他三键取对象默认，不从父对象逐键继承。
- 缺失`thrown_damage`时当前加载器会重建默认投掷伤害，可能覆盖父项的专用投掷定义；修改继承而来的投掷武器时，需要重新检查这一项。
- 继承时会复制父物品的数据，也会带上它原有的功能。跨主类型继承可能残留不需要的槽，不能仅改type就假定把父功能全部剥除；优先选功能接近的父项并检查最终还保留了哪些功能。

### 例：只把一把剑的斩击伤害提高2点

原版`mc_arming_sword`有6点bash、30点cut。假设我们想保留其他配置，只让cut增加2，可以这样写：

```json
{
  "type": "TOOL",
  "id": "example_sharp_sword",
  "copy-from": "mc_arming_sword",
  "name": { "str": "example sharp sword" },
  "relative": { "melee_damage": { "cut": 2 } }
}
```

这样得到的基础伤害是bash 6、cut 32。格挡技巧、材料、工具品质等仍沿用父项。

如果改为直接填写`"melee_damage": { "cut": 32 }`，意思就变成“用这张新伤害表替换旧表”，父项的bash不会被保留下来。因此，**只改一项时用相对修改，想重新指定全部伤害时才直接写完整伤害表**。

需要保留父项的flags并追加一个标记时，也使用对应的追加写法：

```json
{
  "extend": { "flags": [ "ALWAYS_TWOHAND" ] }
}
```

上面是物品定义中的局部配置，不是一件完整物品。它会保留已有flags，再加上强制双手；如果直接写`"flags": ["ALWAYS_TWOHAND"]`，则会替换原来的flags列表。

<a id="common"></a>
## 三、物理、材料、经济与使用条件

| 字段 | 格式、初值或回退 | 对武器的实际影响 |
|---|---|---|
| `weight` | 带单位质量如`"1200 g"`，初始0 | 攻速、体力、投掷、握持等使用实际重量；物品内装和配件还可能改变运行时重量 |
| `volume` | 如`"1500 ml"` | 收纳与基础近战耗时；按charges物品指stack_size对应体积，不总是单支箭体积 |
| `longest_side` | 如`"100 cm"`，初始-1mm | 影响容纳；缺失按体积估算，长矛、剑、箭应合理明写；不决定reach |
| `integral_weight` | 质量，未定回退基础自重 | 装入母武器等整合后的增量质量 |
| `integral_volume` | 体积，未定回退volume | 整合后增加的占用体积，不等于独立携带体积 |
| `integral_longest_side` | 长度，初始-1mm，输入必须非负 | 安装为部件时长度贡献，不等于完整刃长；查item相应计算 |
| `stackable` | 开关 | 普通物品堆叠行为，不等于按charges计数 |
| `stack_size` | AMMO等槽入口整数 | 基础体积、价格等对应的默认堆数；为0时，加载完成后按默认数量补全，过大值会限制至200 |
| `price` | 钱，整数为美分，亦可单位字符串 | 灾前基价，非游戏金币数量 |
| `price_postapoc` | 钱，初始-1 | 缺失的负初值在加载后的整理阶段回退price；不是只供展示 |
| `material` | 字符串/数组或`[{"type":"steel","portion":3}]` | 材料份额影响耐损、导电、燃烧、维修等；物品重量并非由体积×密度普遍自动生成 |
| `replace_materials` | `{旧材料ID:新材料ID}` | 替换、调整重量、维修材料及护甲分区；不会自动提高剑的melee_damage |
| `repairs_with` | 材料ID集合 | 可维修材料；为空时通常在加载后的整理阶段由材料推导，复杂枪械走专用维修工具 |
| `repairs_like` | 物品ID | 维修参考项，需核维修调用，不是copy-from |
| `min_strength` | 整数，初始0 | 使用条件，弓相关计算也读取；不普遍等于近战单手/双手门槛 |
| `min_dexterity`、`min_intelligence`、`min_perception` | 整数，各初始0 | 对应使用条件，受具体动作要求检查；不直接加伤害 |
| `min_skills` | `[[技能ID,等级],...]` | 使用/安装等具体路径的最低技能；当前空数组不会触发清空，不能用空数组假定清除父要求 |
| `qualities` | `[[quality ID,等级],...]` | 切割、屠宰、锤击等工具品质，可在加载后的整理阶段获得对应use；不是装备品质评级 |
| `charged_qualities` | 同qualities | 有电/有charges条件下的工具能力，核具体使用路径 |
| `flags` | flag ID集合 | 可修改握持、距离、耐久及操作，须定义有效flag；定义flag文本不会自动创造C++能力 |
| `properties` | 属性字典 | 非任意自由属性系统；必须存在消费对应键的代码，如投掷容器burst_when_filled |
| `variables` | 初始变量数据 | EOC及actor等消费的实例变量；不是任意战斗字段替代 |
| `faults` | fault ID集合 | 潜在故障定义；不是物品生成时必然已有全部故障 |
| `degradation_multiplier` | 数值，读取默认1 | 当前仅特定非charges车辆部件类别应用degrade增量；不把它当所有武器通用耐久倍率 |
| `phase` | 相态枚举，初始solid | 液体弹药、喷射等会消费相态，普通剑用solid |
| `container`、`sealed` | 默认容器ID、开关（初始true） | 默认生成包装；不能代替武器自身pocket |

[材料加载](../../src/material.cpp)的`chip_resist`进入[item::chip_resistance](../../src/item.cpp)及[handle_melee_wear](../../src/melee.cpp)。材料的护甲抗性并非剑伤害；换中碳钢、淬火钢如需伤害差别，必须显式数据或其他已实现机制支撑。

其他共享字段：`emits`为场发射器ID集合；`explode_in_fire`为受火触发爆炸条件；`insulation`为热交换隔热倍率（初始1）；`solar_efficiency`为太阳能转换效率（初始0）；`source_monster`关联来源怪物；`chat_topics`是物品对话话题数组。它们都不属于普通剑的必填参数。`memory_card`、`milling`、`nanofab_template_group`、`template_requirements`、`book_data`、`bionic_data`、`seed_data`、`brewable`、`pet_armor_data`、营养与书籍字段仅在复合物品使用相应系统时查对应加载器；字段盘点出现它们不意味着武器必须配置。

### 例：剑的重量、体积和长度各管什么

```json
{
  "weight": "1200 g",
  "volume": "1500 ml",
  "longest_side": "95 cm"
}
```

这是一把重1.2kg、收纳体积1.5L、最长边95cm的剑。三个值分别发挥作用：

- 背包承重和挥动负担要考虑1.2kg的重量。
- 放入口袋时，先要有足够容积；较小体积也会影响基础攻击耗时。
- 即使口袋有10L容量，如果只允许放入最长60cm的物品，这把95cm的剑仍放不进去。

`longest_side`不会让它自动获得隔一格攻击的能力。想做能隔开距离攻击的武器，要在第四章配置reach相关flags。

### 例：给钢刃和木柄分别记录材料

```json
{
  "weight": "1200 g",
  "material": [
    { "type": "mc_steel", "portion": 9 },
    { "type": "wood", "portion": 1 }
  ]
}
```

这里的9和1是材料组成份额，不是厚度，也不是游戏分别模拟了900g钢刃和100g木柄。整件武器的自重仍由weight指定；材料份额会参与耐损等相关计算。若要表达“换了更好的钢，刃伤也提高”，还需要明确修改melee_damage，不能只换材料名。

<a id="melee"></a>
## 四、近战伤害、命中、攻速、距离与双手

### 用melee_damage设置近战伤害

近战伤害最常用的三个名字是bash（钝击）、cut（斩切）和stab（刺击）。一把剑可以同时具有几种伤害，不必只选一种。

```json
{ "melee_damage": { "bash": 6, "cut": 28, "stab": 14 } }
```

左边的bash、cut、stab是伤害类型，右边的数字是对应的基础伤害。这里用的是简单的“伤害类型：数值”写法。`amount`、`armor_penetration`等不能直接嵌入这里。`all/physical/non_physical`还受`finalize_damage_map`聚合键规则影响；普通武器宜明确伤害类型。

`damage_type`定义里的`skill`、`physical`、`edged`、`derived_from`等影响技能、物理与刃伤处理。使用`stab`而非陈旧的STAB flag。JSON可同时给多个伤害分量，但角色伤害流程会结合攻击向量、武术、技能、属性、暴击、伤害类型与目标护甲计算，不等于界面数值就是每击扣血。

[item.cpp](../../src/item.cpp)的`damage_melee`先取melee值，再处理损坏等修正：`REDUCED_BASHING`使bash减半；`DIAMOND`对edged类型增加倍率；枪上有近战模式配件时还可能选最大近战伤害。`base_damage_melee`只把正值构造为damage_instance，不会因此自动带上固定穿甲。

继承示例：

```json
{
  "proportional": { "melee_damage": { "cut": 1.1 } },
  "relative": { "melee_damage": { "bash": 2 } }
}
```

这两项写在物品定义中。加载后先乘比例、再加增量，每步向下取整；没有显式伤害值的类型可能先由damage_type派生规则补全，不能用一个字典相加脚本冒充最终加载。

### 用to_hit设置近战命中

| 子字段 | 可用值与枚举数值 | 对象缺省 |
|---|---|---|
| `grip` | bad=0、none=1、solid=2、weapon=3 | weapon |
| `length` | hand=0、short=1、long=2 | hand |
| `surface` | point=0、line=1、any=2、every=3 | any |
| `balance` | clumsy=0、uneven=1、neutral=2、good=3 | neutral |

`m_to_hit = grip + length + surface + balance - 7`。对象全缺省得到0，全部最优得到4，全部最低得到-7。也支持直接整数，例如`"to_hit":2`。

这四个字段只合成一个近战命中加值，不分别赋予攻速、攻击距离、刺击或招架能力。对象`length`与顶层物理`longest_side`不是一回事。`doc/JSON_INFO.md`称四项必须填写，但当前`acc_data::load`允许省略并提供默认值；编写时可明确四项保证意图清晰，不能以旧文档断言加载器必报错。

### 例：两个命中对象分别得到多少加值

```json
[
  { "to_hit": { "grip": "weapon", "length": "long", "surface": "any", "balance": "neutral" } },
  { "to_hit": { "grip": "solid", "length": "long", "surface": "point", "balance": "neutral" } }
]
```

这里并列的是两种局部配置，方便比较。按前表换成数字后：

- 第一种：3＋2＋2＋2－7＝**＋2命中**。
- 第二种：2＋2＋0＋2－7＝**－1命中**。

这些结果只表示命中修正。第二种写了point，不代表游戏会自动添加刺击伤害；两种都写了long，也不代表它们能进行长距离攻击。

### 攻速与消耗

当前物品没有通用`attack_cost`、`attack_speed`、`swing_time`读取字段。基础耗时来自：

```text
item::attack_time = 65 + (实际volume / 62.5ml + 实际weight / 60g) / count()
```

随后可能由物品附魔修正。它的单位是moves，不是毫秒；常规速度100角色每秒通常获得100 moves，但角色速度变化会改变实际耗时。

`Character::attack_speed`还计算melee技能、敏捷、体力、肢体lift/balance修正、武术、附魔、突变与姿态，最终至少25 moves。具体技巧还可调整本次move_cost。所以不能只靠把剑写重就同时获得“更大伤害且同速”，也不能把质量分布的历史描述直接当作引擎已模拟的重心参数。

### 例：加重武器会怎样影响攻击耗时

仍以1.2kg、1.5L的单件武器为例，先不计附魔和角色修正：

```text
基础耗时 = 65 + 1500 / 62.5 + 1200 / 60 = 109 moves
```

如果体积保持不变，只把重量改为1.8kg，基础耗时就变成119 moves。这个比较说明，加重武器确实会提高基础挥动成本；最终一次攻击花多久，还要经过角色技能、敏捷、体力、姿态和技巧的计算。

因此，设计“轻快的剑”和“沉重的剑”时，要一起看weight、volume和技巧，不能只给其中一把添加一个不存在的attack_speed字段。

### 距离、握持与耐损

| 配置 | 当前行为 |
|---|---|
| 无reach flag | 基础近战距离1 |
| `REACH_ATTACK` | 距离2 |
| `REACH_ATTACK`＋`REACH3` | 距离3；单写REACH3不进入reach分支 |
| `POLEARM` | 有reach且未使用reach attack的贴身攻击伤害×0.7；不自动增加距离 |
| `SPEAR` | reach路径遇到THIN_OBSTACLE的处理不同；不自动添加stab伤害 |
| `ALWAYS_TWOHAND` | `is_two_handed`直接true |
| 无ALWAYS_TWOHAND | 实际重量/113g > 臂力×4时判双手；当前函数不读取体积与min_strength |
| `DURABLE_MELEE` | handle_melee_wear中的damage_chance分母×4，通常降低磨损概率，非直接伤害提升 |
| `UNBREAKABLE_MELEE`、`UNBREAKABLE` | 近战磨损提前返回；前者不是所有损坏来源都免疫 |
| `FRAGILE_MELEE` | 较脆连接/组件解体机制，需核组件与损坏分支 |
| `NONCONDUCTIVE`、`CONDUCTIVE` | 改变导电判断；材料导电性仍应结合实际flags核查 |

新武器需要格挡通常通过`techniques`中的格挡技巧；`to_hit`高不等于格挡等级高。`BLOCK_WHILE_WORN`允许穿戴护甲/盾参与格挡，与手持武器格挡区分。`UNARMED_WEAPON`等应查当前攻击向量和武术要求，不把穿戴手套等同双持两把刀。

### 例：把普通长矛与重型长枪的使用方式分开

普通长矛可以采用下面的局部配置：

```json
{
  "flags": [ "DURABLE_MELEE", "SPEAR", "REACH_ATTACK", "NONCONDUCTIVE", "SHEATH_SPEAR" ]
}
```

它能在距离2攻击；SPEAR还让这类攻击按矛的方式处理某些薄障碍。是否必须双手仍取决于重量和角色臂力。

如果设计的是必须双手、可攻击到距离3、贴身又笨重的长枪，可以采用：

```json
{
  "flags": [ "DURABLE_MELEE", "SPEAR", "REACH_ATTACK", "REACH3", "POLEARM", "ALWAYS_TWOHAND", "NONCONDUCTIVE", "SHEATH_SPEAR" ]
}
```

这三个差别分别由REACH3、POLEARM、ALWAYS_TWOHAND表达。不能只把名称改成长枪，或者把longest_side写成4m，就认为这些行为已经实现。两段都是直接填写的flags列表，实际用于继承物品时要检查是否会覆盖其他必要标记。

<a id="throw"></a>
## 五、投掷物

`thrown_damage`必须是damage_unit数组，例如：

```json
{ "thrown_damage": [ { "damage_type": "stab", "amount": 18, "armor_penetration": 2 } ] }
```

缺失时当前通用加载器会生成bash：`melee[bash] + 基础weight/1kg`。游戏会先生成这份默认伤害，再处理材料替换和加载后的数据整理；后续改重、换材料或只改relative.melee_damage不保证默认投掷值同步重算。专门投矛建议明确此数组，继承子项也检查缺省重建。

`item::base_damage_thrown`取该定义；`Character::throw_item`再加力量、技能与质量约束的bash、技能穿甲等。投掷射程由`Character::throw_range`依据实际重量、体积、臂力、投掷技能及辅助效果计算，没有普通GENERIC可写的通用`throw_range`或`range`字段。

`ACT_ON_RANGED_HIT`、激活态、玻璃材料、`properties.burst_when_filled`、`drop_action`等可影响落地行为。投掷物使用物品本体，弓弩发射使用AMMO投射物；二者的伤害、回收、射程与消耗流程不能混写。普通飞刀也可兼有melee_damage和专用thrown_damage。

### 例：同一支投矛，近战与投掷使用不同伤害

```json
{
  "type": "GENERIC",
  "id": "example_javelin",
  "copy-from": "javelin_iron",
  "name": { "str": "example javelin" },
  "melee_damage": { "bash": 5, "stab": 19 },
  "thrown_damage": [
    { "damage_type": "bash", "amount": 5 },
    { "damage_type": "stab", "amount": 17, "armor_penetration": 2 }
  ]
}
```

拿它近战时，基础伤害来自melee_damage；直接掷出时，基础伤害来自thrown_damage。投掷的stab部分还带2点固定穿甲。后续角色属性、技能和目标防护仍会改变实际效果。

这里没有设置range，因为直接投掷的射程由角色与物品的重量、体积共同计算。想增加投掷距离，应先检查这些条件，而不是照搬弓的range字段。

<a id="damage-instance"></a>
## 六、箭矢、投矛等物品的伤害怎么写

适用于GUN的`ranged_damage`、AMMO的`damage/shot_damage`、GUNMOD的`damage_modifier`；`thrown_damage`入口只接受数组。远程入口可读单对象、数组，或带`values`数组的对象。

| damage_unit字段 | 类型、读取默认 | 含义 |
|---|---|---|
| `damage_type` | 字符串，必需 | 有效damage_type ID |
| `amount` | 数值，0 | 基础伤害量 |
| `armor_penetration` | 数值，0 | 固定减甲值，成员res_pen |
| `armor_multiplier` | 数值，1 | 护甲倍率res_mult；减甲与倍率顺序看resistances |
| `damage_multiplier` | 数值，1 | 条件伤害倍率，合并同类型damage_unit时可能归一化 |
| `constant_armor_multiplier` | 数值，1 | unconditional_res_mult，独立于上述可归一化的倍率 |
| `constant_damage_multiplier` | 数值，1 | unconditional_damage_mult；原版箭头常用它改变发射器贡献的最终伤害 |
| `barrels` | `[{"barrel_length":"... mm","amount":数值}]` | 根据实际枪管长度插值的伤害曲线，不是开关或枪管数量 |

`load_damage_instance_inherit`对显式出现的同damage_type继承省略子字段；未在新列表出现的旧damage_type不自动留在新列表里。与melee_damage整张伤害表的直写替换逻辑不同。

固定穿甲不是“忽略百分之几护甲”。`resistances::get_effective_resist`按固定减甲、倍率等组合；条件与constant倍率的合并需看`damage_instance::add_damage`。不要把同一伤害在发射器、弹药及技巧各写一遍后再期待只算一次。

### 例：固定穿甲与伤害倍率分别表达什么

```json
{
  "damage": {
    "damage_type": "stab",
    "amount": 20,
    "armor_penetration": 3,
    "constant_damage_multiplier": 1.1
  }
}
```

把这段写在AMMO物品中，表示这份刺击伤害有20点基础量、3点固定穿甲，并带1.1倍的常量伤害倍率。3点固定穿甲不是“忽略3%护甲”；1.1倍也不是固定增加1.1点伤害。实际发射时，这份数据还会与弓弩或枪械的贡献合成。

若同一物品作为近战武器还需要刺击伤害，另写melee_damage。不能把damage对象原样搬进melee_damage里。

### 新增damage_type时的关联字段

一般编写剑、箭或枪弹复用现有伤害类型。确需新增类型时，修改的是全局伤害系统，须在任务授权范围内，并同时核材料、怪物抗性、显示排序与EOC消费，不只是给物品多添一个键。

| damage_type字段 | 格式/初值 | 作用 |
|---|---|---|
| `id`、`name` | ID与必需可翻译名称 | 类型身份及显示 |
| `skill` | skill ID，初始为空 | 该伤害类型的技能关联 |
| `physical` | 开关，false | 归为物理伤害，影响physical汇总与相关处理 |
| `melee_only` | 开关，false | 标记近战专用类型，具体作用见damage_type相关处理 |
| `edged` | 开关，false | 刃伤分类，DIAMOND等机制会读取 |
| `environmental` | 开关，false | 环境伤害分类，内部env |
| `material_required` | 开关，false | 材料必须显式定义此类抗性，否则一致性检查提示 |
| `mon_difficulty` | 开关，false | 参与怪物难度伤害评估的分类 |
| `no_resist` | 开关，false | 无抗性类型的标记，具体受击路径复核 |
| `derived_from` | `[damage_type ID,倍率]` | 未显式定义时的派生关系，不能形成无解循环 |
| `immune_flags.character` | 字符串集合 | 角色免疫标记 |
| `immune_flags.monster` | 字符串集合 | 怪物免疫标记 |
| `magic_color` | 颜色，首次读取默认black | 魔法等相关显示颜色 |
| `onhit_eocs` | EOC ID/内联数组 | 此伤害类型的命中事件 |
| `ondamage_eocs` | EOC ID/内联数组 | 此伤害类型造成伤害事件；上下文由on_damage消费建立 |

这些开关最初均为false，继承时由读取代码保留或覆盖；免疫、EOC和派生不是任意武器自带字段。新增类型还需相应damage_info_order，现有一致性检查会核查显示定义。

<a id="gun"></a>
## 七、GUN：弓弩、投石索与枪械

读取入口为`Item_factory::load(islot_gun&)`，新槽初值见`itype.h`。GUN继承通用物品字段，下面字段放主GUN顶层；其他物品的枪槽写在`gun_data`内。

| 字段 | 类型/初值 | 说明与约束 |
|---|---|---|
| `skill` | skill ID，初始为空 | archery、rifle、pistol等；实际射击动作耗时也通过该skill定义取得 |
| `ammo` | ammotype ID或集合 | 可用弹种，不是某支箭的物品ID；与AMMO.ammo_type、弹仓限制匹配 |
| `ranged_damage` | damage_instance，初始空 | 发射器伤害贡献；不是近战伤害。允许某些修正为负，读取下界结构不等于默认负伤害 |
| `range` | 整数，初始0 | 发射器射程贡献，不是最终唯一射程 |
| `dispersion` | 整数，初始0 | 武器机械散布贡献；越低越精确，与ammo、损坏、配件合成 |
| `sight_dispersion` | 整数，初始30，读取范围0至MAX_RECOIL | 基础瞄具可达到的瞄准下限；与武器本身dispersion分开 |
| `recoil` | 整数，初始0，非负输入 | 单次后坐贡献；与弹药及handling合成 |
| `handling` | 整数，初始-1 | 后坐操控参数；未填写时，加载完成后步枪、冲锋枪、霰弹枪取20，其他取10 |
| `durability` | 整数，初始0，输入0–10 | 射击故障、受损相关；不是近战chip_resist |
| `loudness` | 整数，初始0 | 对弹药基础噪声的发射器修正，不是现实分贝 |
| `clip_size` | 整数，初始0，非负 | 内置弹仓容量，游戏会结合这项与口袋设置生成或核对弹仓；可拆弹匣另用MAGAZINE_WELL |
| `reload` | 整数，初始100，非负 | 装填moves基数，实际受技能、flags、配件及装填路径影响 |
| `reload_noise` | 可翻译文本，初始click. | 装填声音文字 |
| `reload_noise_volume` | 整数，初始0，非负 | 装填音量，不是射击噪声 |
| `barrel_volume` | 体积，初始0ml | 枪管体积，截短等动作消费；不等于全部物品体积 |
| `barrel_length` | 长度，初始0mm | 供弹药barrels曲线及配件消费；弓长不应冒充枪管长度 |
| `built_in_mods` | 物品ID集合 | 默认安装且赋予不可拆标记的模组 |
| `default_mods` | 物品ID集合 | 默认安装、允许拆除的模组 |
| `valid_mod_locations` | `[[位置ID,数量],...]` | 允许的模组位置和槽数；直接填写会清空原列表，不自动合并 |
| `modes` | `[[模式ID,可翻译名,数量,可选flags],...]` | 射击模式；例如DEFAULT单发、AUTO连发、带MELEE的近战模式；数量含义由模式消费路径决定 |
| `energy_drain` | 能量如`"1 kJ"`，初始0 | 每次射击用电；不是工具槽power_draw的瓦数 |
| `ammo_to_fire` | 整数，初始1，允许非负 | 每次射击消耗的弹药基数，可由模组修改 |
| `blackpowder_tolerance` | 整数，初始8，输入非负 | 黑火药污垢相关概率参数，不是抗性百分比 |
| `min_cycle_recoil` | 整数，初始0，非负 | 自动循环动作的最低弹药后坐条件 |
| `ammo_effects` | 字符串集合 | 发射器附加投射物效果，合并到弹药效果 |
| `heat_per_shot` | number，初始0 | 每射击产热；非负输入 |
| `cooling_value` | number，初始100 | 每回合散热，非负输入 |
| `overheat_threshold` | number，初始-1 | 过热阈值；负值表示不启用过热 |
| `hurt_part_when_fired` | `{bodypart ID:伤害整数}` | 开火自伤部位，特殊武器功能，不是后坐或瞄准代价 |

新定义如果不写modes，游戏仍会补上DEFAULT单发模式；clip=1显示manual名称不表示所有装填机制都自动正确。REACH_ATTACK的GUN还可能获得MELEE模式，配件模式也会加入最终可用模式。

### 弓弩常用flags及实际消费

| flag | 当前意义与边界 |
|---|---|
| `RELOAD_AND_SHOOT` | 开火流程包含装填与发射；用于弓等，不等于无限弹药 |
| `STR_DRAW` | 当前`gun_range(Character*)`在满足要求后加`max(0,(str-min_str)*0.5)`射程；旧说明“需两倍最低力量才无惩罚”与当前代码不同 |
| `PRIMITIVE_RANGED_WEAPON` | 影响复杂枪械判定、维修和射击污垢等路径；不是把所有枪械特征关闭的总开关 |
| `NEVER_JAMS` | 跳过特定故障分支；不是对水、弹药、机构的所有问题完全免疫 |
| `WATERPROOF_GUN` | 对特定水下受损/锈蚀分支有效；不能由文案推断所有弹药都可水下发射 |
| `RELOAD_ONE` | 用于逐发装填等操作；缺省模式命名也读取它 |
| `BOW`、`CROSSBOW` | 结合flag定义及实际使用这些标记的代码确认；不能只加flag就使GENERIC变成可射击武器 |
| `DISABLE_SIGHTS` | 基础sight_dispersion路径用300替代，仍需结合有效瞄准方式 |

原版弓弩还可能用`CHARGE`、`BIONIC_WEAPON`等特殊flag；看盘点表确定样本，再查实际效果的实现。装备力量要求、RELOAD_AND_SHOOT及相关flags应当按原型发射方式组合，不机械复制枪械父项。

### 最终射击参数如何合成

- `item::gun_damage`按实际barrel_length读取发射器、gunmod及弹药damage，再处理损坏等。伤害倍率不是简单把JSON amount相加后结束。
- `item::gun_range`先累加gun.range、配件range、ammo.range，再乘配件与ammo的range_multiplier，限制在0至RANGE_HARD_CAP。带Character版本还做使用要求、STR_DRAW与附魔修正。
- `item::gun_dispersion`累加武器、配件、损坏，先限制非负，再加弹药散布；经选项GUN_DISPERSION_DIVIDER缩放，最终至少1。角色瞄准、视力、技巧仍在后面。
- `item::gun_recoil`还使用基础自重、臂力及handling，不能把JSON recoil当最终每发抬枪角度。
- `time_to_attack`读取`skill_id->time_to_attack()`。`reload`、开火时间、瞄准时间是不同开销，不能把reload写成0就宣称零时间射击。
- `make_gun_projectile`构造damage、range、effects、critical_multiplier、多弹丸与回收物；目标命中、护甲和弱点在投射物/生物受击流程继续计算。

### 例：调整一张弓的伤害、射程和装填时间

原版selfbow使用archery技能，发射arrow弹种。下面只演示几个常用设置，其他结构从父项继承：

```json
{
  "type": "GUN",
  "id": "example_bow",
  "copy-from": "selfbow",
  "name": { "str": "example bow" },
  "min_strength": 8,
  "ranged_damage": { "damage_type": "stab", "amount": 5 },
  "range": 10,
  "reload": 70
}
```

- min_strength 8表示使用力量要求。单独提高它，不等于提高弓的伤害。
- ranged_damage是这张弓提供的射击伤害。最终还要计入所用箭矢。
- range 10是发射器的射程贡献；弹药、配件与角色相关修正可能继续改变射程。
- reload 70是装填耗时的基础值，不包含所有瞄准与开火时间。

selfbow还带有携行用的护甲数据及一发容量的弹仓配置。这个例子会一并继承；如果新设计不需要它们，必须另行处理，不能以为改了名称就只剩上述四个参数。

<a id="ammo"></a>
## 八、AMMO、弹种与弹药效果

`AMMO`共享通用字段与melee_damage；AMMO的`damage`影响射出后伤害，melee_damage影响拿箭本体近战，thrown_damage影响直接手掷，三套用途独立。

### AMMO字段

| 字段 | 类型/读取默认或初值 | 说明 |
|---|---|---|
| `ammo_type` | ammotype ID；新定义必须填写 | 弹种，须存在ammunition_type定义 |
| `damage` | damage_instance，初始空 | 单发基础伤害与穿甲、倍率，供发射器合成 |
| `shot_damage` | damage_instance，初始空 | 多弹丸每颗的伤害，配合projectile_count |
| `projectile_count` | 整数，读取默认1 | 每发投射物数量，不是库存charges |
| `shot_spread` | 整数，读取默认0 | 多颗投射物的额外散布 |
| `critical_multiplier` | 数值，读取约束下界1；结构初值2 | 投射物暴击伤害倍率。`assign(...,1.0f)`是约束，不是把缺省改成1；继承保留父值 |
| `range` | 整数，初始0，非负 | 对最终射程的加值 |
| `range_multiplier` | 数值，初始1，读取下界1 | 对最终射程乘数；当前加载器约束应复核，不能直接用小于1值假定支持减程 |
| `dispersion` | 整数，初始0，非负 | 弹药散布贡献 |
| `recoil` | 整数，初始0，非负 | 弹药后坐贡献 |
| `count` | 整数，初始1，输入至少1 | 默认生成charges数，不是每枪弹丸数 |
| `stack_size` | 整数，至少1的输入 | 上文volume等对应的charges堆量，缺省在加载后的整理阶段处理 |
| `loudness` | 整数，初始-1 | 未填写时，按射程、伤害和穿甲估算；显式0可表达安静箭矢 |
| `casing` | 可选物品ID，缺省未设 | 射后弹壳或容器，在cycle_action掉落；不是目标处回收箭 |
| `effects` | 字符串集合 | 弹药效果，含数据驱动ammo_effect和硬编码投射物标签 |
| `drop` | 物品ID，读取默认null | 命中后指定掉落物 |
| `drop_chance` | 数值，初值1，输入0–1 | 指定掉落物概率，不是0–100百分数 |
| `drop_active` | 开关，读取默认true | 指定drop物品是否激活 |
| `show_stats` | 开关，读取默认false | 强制展示无普通damage的战斗弹药信息，不增加伤害 |

`shot_counter`出现在旧doc说明中，但当前`islot_ammo::load`没有读取它；`count/projectile_count`也不能与此混用。不凭文档复制当前代码不读取的字段。

### ammunition_type定义

```json
{ "type": "ammunition_type", "id": "example_arrow", "name": "example arrows", "default": "example_arrow_item" }
```

`id`是弹种；`default`指向该弹种的默认AMMO物品；`name`是弹种显示名。定义在[ammo.cpp](../../src/ammo.cpp)。GUN.ammo和AMMO.ammo_type使用弹种ID，默认弹药和drop/casing使用物品ID。新增弹种通常还需关联发射器与仓容限制，不能只写一个AMMO物品。

### 回收与效果标签

`RECOVER_N`不是N%回收。当前`make_gun_projectile`按`!one_in(N)`判定，例如RECOVER_2约50%、RECOVER_30约29/30，且IGNITE/EXPLOSIVE等还会限制回收；后续投射物碰撞或嵌入流程也影响最终结果。

`ACT_ON_RANGED_HIT`控制命中激活；`NO_EMBED`抑制嵌入；`NOGIB`限制碎尸；`BEANBAG`等有硬编码效果。`effects`与`flags`是不同集合，不应随意互换。自定义名字若没有ammo_effect定义或对应的C++实现不会自动造成毒伤、击退或燃烧。

### 例：给同一张弓制作另一种箭头

```json
{
  "type": "AMMO",
  "id": "example_arrow",
  "copy-from": "arrow_field_point_fletched",
  "name": { "str": "example arrow" },
  "damage": {
    "damage_type": "stab",
    "armor_penetration": 2,
    "constant_damage_multiplier": 1.1
  },
  "effects": [ "RECOVER_30" ]
}
```

它仍继承arrow弹种，因此原来能使用arrow的弓不必为了这支新箭再增加一种弹种。这里重新指定了刺击的穿甲和倍率，其他同类型伤害设置沿用父项。

注意，这个对象没有给amount增加固定伤害，修改的是穿甲与倍率。若要增加箭本身的基础伤害，还需明确填写amount。RECOVER_30表示当前回收判定约为29/30，而非30%；最终还要看燃烧、爆炸、嵌入等条件。

### ammo_effect数据定义

[ammo_effect.cpp](../../src/ammo_effect.cpp)读取以下字段。`id/type`由generic_factory处理；各效果是否运行还受投射物处理代码控制。

| 字段 | 默认 | 含义 |
|---|---|---|
| `trigger_chance` | 1 | one_in(N)触发分母；1为每次触发，见projectile.cpp |
| `aoe.field_type` | fd_null | 影响区生成的field ID |
| `aoe.intensity_min/max` | 0/0 | field强度范围 |
| `aoe.radius`、`radius_z` | 1、0 | 平面与垂直半径 |
| `aoe.chance` | 100 | 每格生成百分数，检查范围1–100，消费x_in_y(chance,100) |
| `aoe.size` | 0 | 影响区大小参数，非负 |
| `aoe.check_passable` | false | 要求地形可通行 |
| `aoe.check_sees`、`check_sees_radius` | false、0 | 可见性检查及其半径 |
| `trail.field_type` | fd_null | 飞行路径场 |
| `trail.intensity_min/max` | 0/0 | 路径场强度范围 |
| `trail.chance` | 100 | 路径生成百分数，检查1–100，在map.cpp中按x_in_y(chance,100)判定 |
| `explosion` | 未设 | 使用统一explosion结构 |
| `do_flashbang` | false | 闪光弹效果 |
| `do_emp_blast` | false | EMP效果 |
| `foamcrete_build` | false | 特定泡沫混凝土构建效果 |

<a id="magazine"></a>
## 九、弹匣、弹仓与兼容性

### MAGAZINE槽字段

| 字段 | 格式/初值 | 用途 |
|---|---|---|
| `ammo_type` | ammotype集合 | 允许弹种 |
| `capacity` | 整数，初始0 | 容量；0时通用读取末尾可从MAGAZINE口袋取最大相容容量 |
| `count` | 整数，初始0 | 默认装入量，不是容量 |
| `default_ammo` | AMMO物品ID，初始为空 | 默认装填弹药 |
| `reload_time` | 整数，初始100 | 每单位装入弹匣的moves基数，区别于GUN.reload |
| `linkage` | 可选物品ID | 弹链每消耗一发产生的链节 |

主物品顶层旧式`magazines`格式为`[[弹种ID,[弹匣ID...]],...]`，每组首项为默认弹匣，直写清空旧映射。当前更应检查`pocket_data`：MAGAZINE_WELL的item_restriction及default_magazine可反向建立弹匣映射。不要让旧式映射与口袋白名单互相矛盾。

### 武器相关pocket_data

所有pocket是独立容量池。读取见[pocket_data::load](../../src/item_pocket.cpp)；`ammo_restriction`非空时跳过普通体积、重量、长度容量分支，因此不能在这个分支中机械写满普通容器参数。

| 字段 | 格式/读取默认 | 用途 |
|---|---|---|
| `pocket_type` | 枚举，CONTAINER | 内置弹仓用MAGAZINE，可拆弹匣井用MAGAZINE_WELL；普通鞘袋用CONTAINER |
| `ammo_restriction` | `{ammotype:最大charges}` | 按弹种容量，不是具体箭ID；显式空对象会报错 |
| `item_restriction` | 物品ID集合 | 弹匣/装备白名单；当前首项会设为默认弹匣；显式空集合报错 |
| `flag_restriction` | flag集合 | 接受具有相应flag的物品；实际匹配语义查can_contain，不当作任意逻辑表达式 |
| `material_restriction` | 材料集合 | 限制收纳材料 |
| `allowed_speedloaders` | 物品ID集合 | 允许的快速装填器 |
| `default_magazine` | 物品ID | 默认弹匣，注意item_restriction首项读取覆盖 |
| `name`、`description` | 可翻译文本 | 口袋显示，不影响相容性 |
| `min_item_volume` | 体积，0ml | 单件最小体积 |
| `max_item_volume` | 可选体积 | 单件最大体积，不是总容量 |
| `max_contains_volume` | 体积，缺省内部最大容积 | 总容量 |
| `max_contains_weight` | 质量，缺省内部最大质量 | 总承重 |
| `max_item_length` | 长度，默认由容量估算 | 单件最大长度，剑鞘须匹配longest_side |
| `min_item_length` | 长度 | 单件最短长度 |
| `moves` | 整数，100 | 取物动作成本基数，实际受角色动作影响 |
| `holster` | 开关 | 限制为单件物品的鞘/枪套语义 |
| `rigid` | 开关，false | 收纳后外形体积是否扩张，不是武器材料硬度 |
| `magazine_well` | 体积，0ml | 弹匣井内不额外占体积的部分 |
| `weight_multiplier`、`volume_multiplier` | 数值，1 | 内容物对承载物重量/体积的贡献，不能无意造无重弹匣 |
| `spoil_multiplier` | 数值，1 | 内容物腐坏倍率，通常与武器无关 |
| `extra_encumbrance`、`volume_encumber_modifier` | 0、1 | 穿戴收纳对累赘的贡献，武器鞘需结合armor_data |
| `ripoff` | 整数，0 | 口袋被扯落相关参数 |
| `activity_noise` | 对象 | 使用/移动噪声；子项volume/chance分别读0/0，非护甲普通分区字段 |
| `fire_protection`、`watertight`、`airtight` | 开关，false | 火、液体、气体相关封护 |
| `open_container`、`transparent` | 开关，false | 开口、透明行为 |
| `forbidden` | 开关，false | 禁止正常使用的口袋 |
| `ablative` | 开关 | 附加甲机制，强制holster；不是普通武器槽 |
| `inherits_flags` | 开关 | 内容物flag继承行为，需结合item运行时核查 |
| `sealed_data.spoil_multiplier` | 数值，1 | 封闭态腐坏倍率；不自动创建可密封结构 |

`SHEATH_SWORD/SHEATH_KNIFE/SHEATH_AXE/SHEATH_SPEAR/SHEATH_BOW`表示相容标记，不保证任何同flag武器都能放入任意鞘；实际还检查体积、重量、长度、pocket限制与是否active。当前`holster_actor::load`仅直接读取`holster_prompt/holster_msg`，旧版actor中的容积参数不能照搬替代pocket_data。

### 例：做一个只能装剑的刀鞘

下面只展示刀鞘的口袋部分，完整的可穿戴刀鞘还需要物品身份和护甲数据：

```json
{
  "pocket_data": [
    {
      "pocket_type": "CONTAINER",
      "holster": true,
      "rigid": true,
      "flag_restriction": [ "SHEATH_SWORD" ],
      "max_contains_volume": "2 L",
      "max_contains_weight": "2 kg",
      "max_item_length": "100 cm",
      "moves": 100
    }
  ]
}
```

开头那把1.2kg、1.5L、95cm的示例剑，继承了SHEATH_SWORD标记，因而满足这里列出的重量、体积、长度与标记要求。换成一把120cm的剑，即使重量和体积都合适，仍会被长度限制挡住。

holster表示按单件武器收纳；rigid表示装入内容物后，刀鞘的外部体积不会像软袋一样继续鼓起。moves是取物成本基数。它们各有用途，不能用一个SHEATH_SWORD标记代替全部收纳设置。

<a id="gunmod"></a>
## 十、武器配件：安装条件与属性修改

主GUNMOD读取gunmod与mod两个槽。其他物品的`gunmod_data`也读取两者；工具模组仅有相应mod行为，不能据此认为都有枪伤修正。

| 字段 | 类型/初值 | 作用 |
|---|---|---|
| `location` | gunmod_location字符串 | 占用母枪的槽位，须匹配valid_mod_locations |
| `mod_targets` | gun_type_type字符串集合 | 可安装的枪型，区别于skill ID和物品ID；直写清空 |
| `damage_modifier` | damage_instance | 对母枪射击伤害贡献；不是近战伤害 |
| `dispersion_modifier` | 整数，0 | 加到母枪机械散布，可为改进或惩罚 |
| `loudness_modifier` | 整数，0 | 枪声修正 |
| `sight_dispersion` | 整数，-1 | 非负时作为可用瞄具候选，还需有效field_of_view |
| `field_of_view` | 整数，-1 | 瞄具视野参数，参与瞄准速度，不是现实角度字段 |
| `aim_speed_modifier` | number，0 | 额外瞄准速度修正 |
| `aim_speed` | 整数，-1 | 保留旧输入，未有效设置FoV时转换成field_of_view和aim_speed_modifier，不推荐把它当独立最终速度 |
| `handling_modifier` | 整数，0 | 对操控参数的增量 |
| `range_modifier` | 整数，0 | 射程加值 |
| `range_multiplier` | 数值，1 | 射程乘数 |
| `shot_spread_multiplier_modifier` | 数值，0 | 多弹丸散布倍率的增量，非普通枪械dispersion |
| `ammo_effects` | 字符串集合 | 模组追加的弹药效果 |
| `install_time` | moves整数或时间字符串，初始-1 | 安装耗时，字符串转moves；不等于拔取耗时 |
| `reload_modifier` | 整数，0 | 装填耗时百分比变化；item::reload_time使用(100+值)/100，正值变慢 |
| `min_str_required_mod` | 整数，0 | 修改使用力量要求 |
| `energy_drain_multiplier` | 数值，1 | 每发电耗乘数 |
| `energy_drain_modifier` | 能量，0kJ | 每发电耗加值 |
| `ammo_to_fire_multiplier` | 数值，1 | 单发耗弹倍数 |
| `ammo_to_fire_modifier` | 整数，0 | 单发耗弹加值 |
| `weight_multiplier` | 数值，1 | 对母武器重量的倍率；与配件自己的weight/integral_weight分开 |
| `mode_modifier` | 与GUN.modes同格式 | 添加或覆盖枪械模式，读入自身映射时直写重建 |
| `add_mod` | `[[位置,数量],...]` | 增加安装槽，直写清空自身旧列表 |
| `blacklist_mod` | 物品ID集合 | 与特定模组不相容 |
| `blacklist_slot` | gunmod_location集合 | 与母枪特定槽位不相容 |
| `barrel_length` | 长度，0mm | 指定该配件主导的有效枪管长度 |
| `overwrite_min_cycle_recoil` | 整数，-1 | 覆盖母枪循环最低后坐条件 |
| `consume_chance` | 整数，10000 | 射击时配件被消耗/受损分支中的概率分母参数，实际还受loudness/recoil等影响；不是百分数 |
| `consume_divisor` | 整数，1 | 配件消耗损坏的缩放除数，越低通常越易损，查handle_gun_damage |
| `overheat_threshold_modifier` | number，0 | 过热阈值加值 |
| `overheat_threshold_multiplier` | 数值，1 | 过热阈值倍率 |
| `cooling_value_modifier` | number，0 | 散热加值 |
| `cooling_value_multiplier` | 数值，1 | 散热倍率 |
| `heat_per_shot_modifier` | number，0 | 每发产热加值 |
| `heat_per_shot_multiplier` | 数值，1 | 每发产热倍率 |

公共mod槽：

| 字段 | 格式/初值 | 说明与继承 |
|---|---|---|
| `acceptable_ammo` | ammotype集合 | 按母物品基础弹种限制安装，直接填写会清空原列表 |
| `ammo_modifier` | ammotype字符串或数组 | 改变母物品弹种；当前手动insert，不要假定直写自动清空父集合 |
| `capacity_multiplier` | 数值，1 | 弹药容量倍率 |
| `magazine_adaptor` | `[[ammotype,[弹匣ID...]],...]` | 替换相容弹匣；非空数组才先clear |
| `pocket_mods` | pocket_data数组 | 添加/改变口袋；MAGAZINE/MAGAZINE_WELL与普通CONTAINER的整合规则不同，装卸都需核验 |

刺刀等配件的`melee_damage/techniques/flags`仍在通用字段，射击修正放gunmod槽。能否当独立长矛、是否继承reach、射击与近战模式的目标选择都需检查`gun_all_modes`和`damage_melee`，不能只看damage_modifier。

### 例：读懂一个配件的效果

```json
{
  "dispersion_modifier": -50,
  "reload_modifier": 10,
  "integral_weight": "100 g"
}
```

这是配件定义中的局部配置：机械散布减少50，基础装填耗时增加10%，装到武器上后贡献100g质量。它表达的是一个“精度改善，但装填和重量有代价”的配件。

这些数值并不保证配件能装到任何武器上。完整定义还要有GUNMOD身份、location和mod_targets，并与母武器开放的安装位置匹配；若有其他影响重量或装填的配件，还要一起计算。

<a id="techniques"></a>
## 十一、武器类别、技巧及武术适用

### weapon_category与techniques

物品的`weapon_category`是类别ID集合，类别定义type为`weapon_category`，最小结构为`id/name`。具体ID以本地[weapon_categories.json](../../data/json/weapon_categories.json)为准。

类别用于武术允许与技巧条件，不直接决定重量、伤害类型、reach、单/双手，也不是任意可发明的新战斗机制。风格的`weapons`可列具体物品，`weapon_category`可按类别接受；需与`allow_all_weapons/strictly_melee/strictly_unarmed`等风格设置共同判断。

物品`techniques`是technique ID列表。现用例如格挡、快速攻击、绊倒、招架等须从[techniques.json](../../data/json/techniques.json)找真实ID；不能把设计动作名如HALF_SWORD直接当成已注册技巧。继承关系见第二章。

### technique定义字段

`type:"technique"`，ID由factory处理；其余见`ma_technique::load`、`ma_requirements::load`及`bonus_container::load`。

| 字段 | 格式/读取默认 | 作用 |
|---|---|---|
| `id`、`name` | ID、必需可翻译名 | 技巧身份与显示 |
| `description` | 可翻译文本，空 | 技巧说明 |
| `messages` | `[玩家消息,NPC消息]` | 触发文本 |
| `crit_tec` | 开关，false | 暴击技巧筛选 |
| `crit_ok` | 开关，false | 允许暴击场景使用，具体筛选查pick_technique |
| `attack_override` | 开关，false | 攻击覆盖路径 |
| `wall_adjacent` | 开关，false | 墙邻接要求，reqs也读取此键 |
| `reach_tec`、`reach_ok` | 开关，各false | reach专用或允许reach场景 |
| `needs_ammo` | 开关，false | 技巧需要弹药条件 |
| `defensive` | 开关，false | 防御类技巧，非普通主动攻击选择 |
| `disarms`、`take_weapon` | 开关，各false | 缴械及夺取武器动作 |
| `side_switch` | 开关，false | 与目标换位 |
| `dummy` | 开关，false | 标记型技巧，用于别的判断而不常规执行攻击 |
| `dodge_counter`、`block_counter` | 开关，各false | 闪避/格挡反击 |
| `miss_recovery`、`grab_break` | 开关，各false | 失手恢复/挣脱相关筛选 |
| `weighting` | 整数，1 | 技巧随机选择权重，受筛选和特定负权重逻辑影响，不是伤害倍数 |
| `repeat_min`、`repeat_max` | 整数，各1 | 重复次数区间；perform_technique按该区间抽取 |
| `down_dur`、`stun_dur` | 整数，各0 | 按turns随机1至给定时长；击倒还检查目标throw_resist |
| `knockback_dist`、`knockback_spread` | 整数，各0 | 击退距离与方向散度 |
| `knockback_follow` | 开关，false | 击退后跟进 |
| `aoe` | 字符串，空 | 当前范围模式wide、impale、spin；不是任意几何表达式，查valid_aoe_technique |
| `flags` | technique flag集合 | 技巧标签，区别于物品flags |
| `tech_effects` | 对象数组 | 附加效果，具体字段见下 |
| `attack_vectors`、`attack_vectors_random` | 向量ID列表，空 | 固定/随机攻击向量选择；须匹配本地attack vector机制 |
| `eocs` | EOC ID或内联定义数组 | 技巧额外EOC，不与use_action相同 |
| `condition` | 条件对象 | 条件表达式，只有出现时设置has_condition |
| `condition_desc` | 文本 | condition存在时的条件描述 |

### 技巧在什么条件下能用

| 字段 | 读取默认或格式 | 用途 |
|---|---|---|
| `unarmed_allowed`、`melee_allowed` | false | 允许徒手/持械路径 |
| `unarmed_weapons_allowed` | true | 允许徒手武器 |
| `weapon_categories_allowed` | 字符串或类别集合 | 类别条件；单字符串分支与数组分支继承实现不完全相同 |
| `strictly_unarmed` | false | 严格徒手条件 |
| `required_buffs_all`、`required_buffs_any` | buff ID集合 | 必需全部/任一buff |
| `forbidden_buffs_all`、`forbidden_buffs_any` | buff ID集合 | 禁止全部/任一buff组合；具体逻辑看is_valid_character |
| `req_flags` | json_flag集合 | 武器或对应攻击条件所需flag，查is_valid_weapon |
| `required_char_flags` | 角色flag集合 | 角色条件 |
| `required_char_flags_all` | 角色flag集合 | 必需全部角色flags |
| `forbidden_char_flags` | 角色flag集合 | 禁止角色flags |
| `skill_requirements` | `[{"name":"melee","level":3}]` | 最低技能；name为skill ID，level为int |
| `weapon_damage_requirements` | `[{"type":"cut","min":10}]` | type为damage_type ID，min为int最低值 |

### 技巧数值与效果对象

`tech_effects`每项字段：`id`为必需effect ID；`duration`整数默认0；`permanent`默认false；`on_damage`默认true，当前以技巧处理时di.total_damage()!=0判断，不是护甲结算后已实际扣血的证明；`chance`默认100，以x_in_y(chance,100)判定；`message`默认空文本；`req_flag`默认NULL，为角色flag条件。效果施加给目标t，duration按turns转换；req_flag检查攻击者。见perform_technique的tech_effects循环。


`flat_bonuses`与`mult_bonuses`均为对象数组。每项读取`stat`、`scale`，可选`scaling-stat`；damage/armor/arpen还需有效`type`伤害类型。可用stat由[bonuses.cpp](../../src/bonuses.cpp)定义：`hit/crit_chance/dodge/block/block_effectiveness/speed/movecost/damage/armor/arpen/target_armor_multiplier`。scaling-stat支持str/dex/int/per；未设置时scale就是常量。flat相加、mult相乘，不要将mult里的1.2理解成增加120%。

例如原版快速攻击类技巧应查其`movecost`与`damage`倍率，而不是给物品发明`attack_cost`字段。伤害类型要求、技能要求与效果对象的完整读取格式、实际使用见字段盘点末尾的源码读取入口索引；武术buff与风格的完整系统另见[原版武术调研](json_martial.md)和[技巧机制](json_technique_deep.md)。

### 例：保留原有格挡，再增加快速攻击

```json
{
  "type": "TOOL",
  "id": "example_quick_sword",
  "copy-from": "mc_arming_sword",
  "name": { "str": "example quick sword" },
  "extend": { "techniques": [ "RAPID" ] }
}
```

mc_arming_sword已有WBLOCK_2格挡技巧。extend会保留它，再加入原版的RAPID技巧。RAPID代表一次满足条件时可以选中的攻击技巧，不表示这把剑的每一次攻击都固定变快。

如果想让一种攻击始终具有不同耗时，必须重新选择合适的现有机制，不能把“有快速攻击技巧”和“基础攻击耗时降低”写成同一件事。

<a id="actions"></a>
## 十二、工具武器、激活态与爆炸

### 工具武器的消耗与供电

| 字段 | 格式/初值 | 作用 |
|---|---|---|
| `ammo` | ammotype集合 | 工具能源/耗材类型，与GUN.ammo同名但槽不同 |
| `max_charges` | 整数，0 | 工具容量，不能小于initial_charges |
| `initial_charges` | 整数，0 | 固定生成charges，不能与rand_charges同时出现 |
| `rand_charges` | 至少两个整数的数组 | 随机charges区间；当前读取会追加，继承时核查已有数组 |
| `charges_per_use` | 整数，0 | 每次工具动作消耗，actor可能有自己的费用 |
| `charge_factor` | 整数，1，输入至少1 | charge换算因子 |
| `turns_per_charge` | 整数，0 | 激活态消耗频率，需结合process_tool |
| `power_draw` | 功率字符串，0W | 持续电耗，与GUN.energy_drain区分 |
| `fuel_efficiency` | 数值，-1 | 燃料到能量的转换效率，具体消费按工具类型 |
| `sub` | 物品ID | 工具子类型/替代工具用途，不是copy-from |
| `revert_msg` | 可翻译文本 | 工具退回状态时消息 |

新电池BATTERY的`max_capacity`为必需能量字段（如kJ），不能用max_charges冒充。本次不将电池化学、供电网络和完整服装系统作为武器专用规则重复展开。

### 动作入口

| 字段 | 格式 | 生命周期 |
|---|---|---|
| `use_action` | 注册动作字符串、actor对象或动作数组 | 玩家使用物品；对象用`type`选择actor |
| `tick_action` | 同类动作格式 | active处理中的持续动作 |
| `countdown_interval` | 时间 | 新实例倒计时，初始0秒 |
| `countdown_action` | 注册动作字符串或actor对象 | 倒计时结束动作 |
| `revert_to` | 物品ID | 倒计时/工具耗尽后的退回项，缺失可能销毁，须核process路径 |
| `drop_action` | 字符串或actor对象 | 掉落行为，不能当成所有投射物命中通用回调 |
| `explosion` | 对象 | 物品爆炸数据，还需要动作或触发条件才能爆炸 |
| `explode_in_fire` | 开关 | 受火爆炸条件 |

字符串动作查`Item_factory`注册和[iuse.cpp](../../src/iuse.cpp)，actor对象查[iuse_actor.cpp](../../src/iuse_actor.cpp)的对应load/use。普通剑不必因为可用来切割就变成TOOL，qualities可能已提供对应操作。特殊active武器必须同时核对前后态伤害、材料、重量、口袋、供电与目标引用。

### 用transform切换物品状态

当前类名`iuse_transform`，`type:"transform"`。它读的`variant_type`是目标外观ID，不是顶层variant类别。

| 字段 | 作用 |
|---|---|
| `target` | 必需目标物品ID，存在才可转换 |
| `msg`、`menu_text` | 转换消息及菜单文字 |
| `variant_type` | 目标外观variant ID |
| `container`、`sealed` | 生成于容器与密封状态 |
| `target_charges` | 固定目标charges |
| `rand_target_charges` | 至少两值的随机charges区间，与target_charges互斥 |
| `target_ammo` | 目标装入弹药；与container互斥；不是旧版ammo_type |
| `target_timer` | 目标倒计时 |
| `active` | 是否激活目标 |
| `moves` | 转换成本，禁止负值 |
| `need_fire`、`need_fire_msg` | 火源需求及失败消息，负值被归零 |
| `need_charges`、`need_charges_msg` | charges需求及失败消息，负值被归零 |
| `need_worn`、`need_wielding` | 要求穿戴/手持 |
| `need_empty` | 要求空内容物 |
| `qualities_needed` | 工具品质要求 |

未列读取默认的actor参数应查[iuse_actor.h](../../src/iuse_actor.h)构造初值，不能由obj.read没有默认参数就推断为0或false。双向转换要检查目标两侧，不在转换中凭空复制内容物或丢失电池。

### 例：让一件武器在收起和展开状态之间切换

```json
{
  "use_action": {
    "type": "transform",
    "target": "example_weapon_ready",
    "msg": "You ready the weapon.",
    "moves": 100,
    "need_wielding": true
  }
}
```

这段放在收起态物品中：使用时要求手持，花费100 moves，然后变成example_weapon_ready。目标ID只是本例的约定，必须另外定义那件物品；仅粘贴这一段不会自动创建展开态。

展开态的重量、伤害、长度、flags和口袋都由目标定义决定。若还要能够收起，就在目标上配置返回原物品的transform动作。普通展开动作不必设置active；只有确实需要持续处理或耗能时，才将其设为激活态，并补齐相关消耗。

### 爆炸与破片参数

[load_explosion_data](../../src/explosion.cpp)读取`power`、`distance_factor`（默认0.75）、`max_noise`（默认90000000）、`fire`（默认false）和`shrapnel`。power的代码注释称该项必须填写，但当前直接jo.read；编写时仍应明确提供。distance_factor用于距离指数衰减，不是直接半径。

`shrapnel`可为整数壳体质量，或对象：`casing_mass`、`fragment_mass`（默认0.08g）、`recovery`（默认0）、`drop`（默认null）。这不是给普通武器添加碎片伤害的通用字段；需由爆炸触发。EMP、闪光、毒雾等应复用现有actor/ammo_effect/EOC路径，不能只在剑上加入未知字段就期望生效。

<a id="examples"></a>
## 十三、照着原版实例继续写

前面各章已经分别给出剑、投矛、弓、箭、刀鞘和状态切换的写法。接下来按用途列出原版参考项，方便需要更多细节时直接去找同类实现。示例中的example前缀用于教学，没有接入游戏；正式编写时应采用项目约定的ID。

### 普通剑与钢材变体

在[swords_and_blades.json](../../data/json/items/melee/swords_and_blades.json)查`arming_sword/mc_arming_sword/qt_arming_sword`等ID，实际父链以文件为准。普通武器需要决定：物品单位、材料份额、自重、收纳体积、长度、伤害表、to_hit、类别、技巧、flags及工具品质。不要只改了名称和说明，却留下不适合新武器的刀鞘标记、武术类别或使用动作。

写派生项至少明示type、id、copy-from、name；name在当前加载器每次必读。改melee_damage单分量如需保留其他伤害，用已支持relative或完整重写，别用半个直写对象不知不觉清空。

### 长矛与投矛

在[spears_and_polearms.json](../../data/json/items/melee/spears_and_polearms.json)查`spear_steel/pike/javelin/javelin_iron`。区分刺击伤害、reach flags、POLEARM贴身限制、ALWAYS_TWOHAND和专用thrown_damage。SPEAR是障碍交互，不是伤害类型；REACH3需要REACH_ATTACK。

### 弓与箭

在[archery.json](../../data/json/items/ranged/archery.json)查`selfbow`及`arrow_field_point_fletched`父链。发射器写GUN ranged_damage，箭头用AMMO damage的穿甲和constant倍率修正。原版bodkin/broadhead即使名称有“宽刃”，不保证使用cut类型，不能按中文名字改写现有伤害流水线。

确认ammo_type、默认箭、弹仓口袋/clip_size、RELOAD_AND_SHOOT、力量条件和箭支回收。`RECOVER_30`约29/30而非30%，箭melee_damage不是射击伤害。

### 弩、弹仓与附件

在[crossbows.json](../../data/json/items/ranged/crossbows.json)选同结构样本，核对弩矢弹种、内置容量、reload、flags和gunmods。历史上“用绞盘上弦”不代表引擎已要求物品栏持有绞盘：若要这种游戏条件必须找到已有actor/requirements路径或明确技术需求，不能靠description声称完成。

### 工具武器与状态

查近战目录中的`combatsaw_off/combatsaw_on`等真实ID和`use_action/tick_action`。工具槽与普通近战参数可以共存。变形后的目标必须保留设计所需数据；不能把active=true当作自动增加伤害，也不能省略实际持续耗能。

<a id="validation"></a>
## 十四、校验与查错

1. 从对应design确定装备目标；选与操作结构相符的原版父项，展开完整copy-from链，核对所有槽。
2. 查字段加载器，明确初值、读取默认、直写/relative/proportional/extend/delete行为；再看加载后的数据整理，以及实际使用这些参数的代码。C++中存在一个数据成员，并不代表JSON里可以直接填写同名字段。
3. 根据变更检查引用：材料、damage_type、skill、weapon_category、technique、flags、ammo type、默认弹药、弹匣、gunmod位置、actor目标与EOC。
4. JSON语法和格式检查、`git diff --check`；仅验证当前改动和必要引用，不自动改配方、生成组、职业或平衡代码。
5. 实际改游戏JSON后用匹配当前源码的可用构建加载验证。当前[src/main.cpp](../../src/main.cpp)注册`--jsonverify`及`--check-mods [mod…]`，先取真实mod ID和依赖，不把文件夹名当ID。旧二进制不保证支持当前字段；没有匹配构建时明确未执行，不擅自重编整个游戏。
6. 行为按改动验证：近战检查命中/耗时/伤害/格挡/reach/单手双手；弓弩检查装填、瞄准、开火、弹药消耗与回收；模组检查装卸后数据；状态武器检查两个方向、耗能和内容物。

本指南和统计脚本本身的验证不是游戏平衡测试。未来新增字段先补充对应章节和真实样本，再更新盘点；不把目前未使用的字段当成不可用字段。

### 当前版本常见误写

| 误写或误解 | 当前处理 |
|---|---|
| `type: WEAPON` | 选择GENERIC/TOOL/GUN等真实类型 |
| 普通物品`damage:30`表示剑伤害 | 使用melee_damage map；damage_instance用于对应槽 |
| 顶层`attack_cost`直接设剑速 | 普通物品没有这个字段的读取代码；查重量、体积和技巧机制 |
| `to_hit.length`增加reach | 用REACH_ATTACK/REACH3 |
| `min_strength`决定所有双手武器 | 查is_two_handed与ALWAYS_TWOHAND |
| 直写`melee_damage:{cut:...}`自动保留bash | 直写替换map |
| `material:qt_steel`自动提高斩击 | 伤害需显式数据，材料影响耐损等 |
| GUN的`damage`、AMMO的`ranged_damage` | 各槽字段不同，不能互换 |
| `count`等于每发霰弹颗数 | 用projectile_count，count是默认charges |
| `RECOVER_N`是N% | 当前约1−1/N，仍有其他回收条件 |
| `reload_time`是所有枪装填字段 | GUN用reload，MAGAZINE用reload_time |
| actor的容积参数替代鞘容量 | 当前holster用pocket_data容纳检查 |
| `shot_counter`是现行AMMO字段 | 当前ammo loader未读取，旧doc不作支持依据 |
| 旧doc称ALWAYS_TWOHAND缺失按体积和重量 | 当前is_two_handed只看重量与臂力 |
| 自定义flag名自动实现半剑、缴械、破甲 | 必须有对应技巧/actor/consumer实现 |


## 附录：查源码和统计资料

以下导航供核对字段实现时使用。一般编写可以先参考正文中的例子和字段表。

| 工作 | 首查位置 | 接着核查 |
|---|---|---|
| 通用定义、继承 | [item_factory.cpp](../../src/item_factory.cpp)，`load_definition`、`load_basic_info` | 同文件`finalize_pre/post`；[itype.h](../../src/itype.h)初值 |
| 普通近战 | [items/melee](../../data/json/items/melee)、[techniques.json](../../data/json/techniques.json) | [item.cpp](../../src/item.cpp)的`attack_time/damage_melee/reach_range`；[melee.cpp](../../src/melee.cpp) |
| 武器类别与武术 | [weapon_categories.json](../../data/json/weapon_categories.json)、[martialarts.cpp](../../src/martialarts.cpp) | `weapon_category`、`ma_requirements`、`ma_technique`、`martialart` |
| 弓、弩、投石索 | [archery.json](../../data/json/items/ranged/archery.json)、[crossbows.json](../../data/json/items/ranged/crossbows.json)、[slings.json](../../data/json/items/ranged/slings.json) | GUN/AMMO加载与[ranged.cpp](../../src/ranged.cpp) |
| 枪械与配件 | [items/gun](../../data/json/items/gun)、[items/gunmod](../../data/json/items/gunmod)、[classes/gun.json](../../data/json/items/classes/gun.json) | `Item_factory::load(islot_gun/islot_gunmod/islot_mod)` |
| 弹药与弹匣 | [items/ammo](../../data/json/items/ammo)、[items/magazine](../../data/json/items/magazine) | [ammo.cpp](../../src/ammo.cpp)、[ammo_effect.cpp](../../src/ammo_effect.cpp)、`islot_ammo::load` |
| 伤害结构 | [damage.cpp](../../src/damage.cpp)、[assign.cpp](../../src/assign.cpp) | [damage_types.json](../../data/json/damage_types.json) |
| 口袋、鞘与装弹 | [item_pocket.cpp](../../src/item_pocket.cpp) | `pocket_data::load/can_contain`、[iuse_actor.cpp](../../src/iuse_actor.cpp)的`holster_actor` |
| 切换、激活、爆炸 | [iuse_actor.cpp](../../src/iuse_actor.cpp)、[explosion.cpp](../../src/explosion.cpp) | 对应actor的load与实际use/process |


[字段盘点](guide04_weapons_inventory.md)扫描data/json中的相关物品定义，分别统计具体条目与abstract模板，也列出嵌套字段和实例。它不会运行游戏，也不会计算继承后每件物品的最终属性。源码索引中的`assign(..., strict, 0)`等调用可能用0表示允许的最小值，不能仅凭最后一个参数判断默认值。
