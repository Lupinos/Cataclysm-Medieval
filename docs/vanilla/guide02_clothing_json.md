# 原版服装 JSON：循序渐进的编写说明与字段手册

对应策划：[02 盔甲体系](../design/design02-盔甲.md)与[03 日常衣物与随身装备](../design/design03-日常衣物.md)。本篇说明原版服装 JSON 的写法与机制，供上述装备实现时查阅。

## 怎么阅读这篇文章

第一次接触服装JSON，先读[第一部分的连续例子](#walkthrough)：从一件背心开始，每次只增加一个主要概念。已经知道要改哪个字段，直接查[第二部分字段手册](#item-fields)；准备正式编辑时再读[第三部分编辑流程](#editing-skill)。

- **先学会写**：普通衣物 → 多个覆盖分区 → 局部加固 → 单侧与层位 → 口袋 → 继承变体 → 面甲状态转换。
- **再按需查**：[护甲字段与运行时](#armor-fields)、[口袋](#pocket-fields)、[动作](#action-fields)、[原版现用字段与实例](#field-inventory)。
- 代码框前标明“完整示例”或“局部片段”；代码后的解释说明应观察的结果和常见误读。只有需要验证某项行为时再跟到源码，不要求先理解C++加载流程。

本文依据本地源码与原版数据，版本锚点为`ea81dc9fb1d204a4bbcd1d384f1f1ea5ea002a4f`。“原版”指`data/json`；护甲、普通衣物、可穿戴工具和带`armor_data`的物品都在范围内。教学定义仅存在于本文，数字用于解释字段，没有作为新游戏装备落地。

<a id="walkthrough"></a>

# 第一部分：从一件衣服开始

这一部分按编写时的顺序讲解。先做出一件普通衣服，再增加覆盖、分区材料、单侧穿戴、口袋和状态切换。例子用来解释机制，不代表所有衣物必须具备这些功能。

所有 `example_` 开头的ID都是本文教学定义，未写入游戏数据。标为“完整示例”的代码是JSON数组；可以把需要的对象放进同一个数组，或拆到同一个mod的不同文件。后续使用`copy-from`的例子需要同时保留其父定义。标为“局部片段”的代码只替换指定位置，不能单独作为完整物品。

下面的数字用于学习字段，不是已验证的平衡参数。正文解释的是JSON会表达什么；加载、穿戴、受击的实际验证仍按第三部分进行。

## 1. 先认清三种括号与四层位置

JSON只是在描述数据：

- `{ ... }`是一个对象，例如“一件物品的全部定义”。
- `[ ... ]`是一个列表，例如“一件衣服有几个防护分区”。
- `"weight": "350 g"`是一项设置：冒号左边是字段名，右边是值。字符串有引号，数字和`true`/`false`没有引号。

位置比字段名字更重要。下面这些同名键用途不同：

| 写在哪里 | 它描述什么 | 先这样理解 |
|---|---|---|
| 物品最外层的`material` | 整件物品的组成材料 | 这件东西总体由什么制成 |
| `armor`列表中的一个对象 | 一块覆盖区域的防护和负担 | 身体的哪个位置受到怎样的保护 |
| `armor`对象里面的`material`列表 | 该区域实际参与防护的材料 | 这里有多厚的布、钢或其他材料 |
| `pocket_data`列表中的一个对象 | 一个口袋的容量、限制和取物方式 | 这件衣服能怎样装东西 |

“顶层”就是当前物品对象的最外层。“分区”不是另一件装备：一件长袖衣可以分成躯干和手臂两个区，但仍是一件物品。

## 2. 第一件衣服：普通棉背心

先做一件只覆盖躯干、没有袖和口袋的普通层背心。**完整示例：**

```json
[
  {
    "id": "example_cotton_vest",
    "type": "ARMOR",
    "name": { "str": "training cotton vest" },
    "description": "A simple cotton vest used as an example.",
    "symbol": "[",
    "color": "light_gray",
    "weight": "350 g",
    "volume": "750 ml",
    "price": "12 USD",
    "material": [ "cotton" ],
    "warmth": 8,
    "flags": [ "NORMAL" ],
    "armor": [
      {
        "covers": [ "torso" ],
        "coverage": 95,
        "encumbrance": 2,
        "material": [
          { "type": "cotton", "covered_by_mat": 100, "thickness": 0.6 }
        ]
      }
    ]
  }
]
```

先按用途读，不用逐字背诵：

| 这一组设置 | 本例表达的结果 |
|---|---|
| `id`、`type` | 内部ID是`example_cotton_vest`，由服装护甲加载器读取。`ARMOR`也用于普通衣物，不意味着它是金属甲 |
| `name`、`description` | 游戏显示的名称和描述；`name.str`是单数名称。内部ID与显示名分开 |
| `symbol`、`color` | 地图字符与颜色，和物理防护无关 |
| `weight`、`volume` | 本体350g，收纳体积750ml；不是350g内容物或750ml口袋 |
| `price` | 灾前价格12美元；不是制作时间或护甲等级 |
| 顶层`material` | 总体由棉制成；本例只有一种材料，写ID即可 |
| `warmth` | 相对保暖值8，不是8摄氏度，也不是8mm |
| `flags: ["NORMAL"]` | 普通层穿着。下一节说明为什么层位和覆盖要分开 |
| `armor`中的`covers` | 覆盖躯干，不会因为名字是vest就自动生成相应部位 |
| `coverage: 95` | 对这个分区的覆盖概率设置；不表示95%全身受到保护，也不等于减伤95% |
| `encumbrance: 2` | 这个分区的未合身基础累赘；角色最终显示还可能受穿着状态等因素影响 |
| 材料层`cotton`、`100`、`0.6` | 该区采用棉，材料层覆盖100%，厚度0.6；**并不是“防御值0.6”**，防护还需要结合材料定义计算 |

本例未写`specifically_covers`。当前代码会选入`torso`下非`secondary`的子部位，不能理解为连悬挂裙摆区域都自动全包。想精确限制部位时再用下一步。

**可以怎样改？** 想加重衣服改`weight`；想让布更厚改分区材料`thickness`，然后重新核算重量；想更保暖改`warmth`。这三个字段不会自动替你完成另外两项。把名字改成“钢背心”也不会改变棉的防护。

读取依据：`Item_factory::load_basic_info`、`islot_armor::load`、`armor_portion_data::deserialize`、`part_material::deserialize`，均在[src/item_factory.cpp](../../src/item_factory.cpp)。

## 3. 从背心到长袖衣：一个物品可以有多个分区

现在要躯干用较厚布、袖子用较薄布，并给它不同的累赘。先继承背心的显示、价格等信息，再完整列出新的两个分区。**完整示例，依赖上一节背心：**

```json
[
  {
    "id": "example_cotton_shirt",
    "type": "ARMOR",
    "copy-from": "example_cotton_vest",
    "name": { "str": "training cotton shirt" },
    "description": "A long-sleeved shirt with thinner sleeves.",
    "weight": "550 g",
    "volume": "1250 ml",
    "armor": [
      {
        "covers": [ "torso" ],
        "specifically_covers": [ "torso_upper", "torso_lower" ],
        "coverage": 95,
        "encumbrance": 3,
        "material": [
          { "type": "cotton", "covered_by_mat": 100, "thickness": 0.8 }
        ]
      },
      {
        "covers": [ "arm_l", "arm_r" ],
        "coverage": 90,
        "encumbrance": 2,
        "material": [
          { "type": "cotton", "covered_by_mat": 100, "thickness": 0.5 }
        ]
      }
    ]
  }
]
```

这里发生了三件事：

1. `copy-from`先取得背心的定义；新名称、说明、重量、体积和`armor`再修改对应内容。未写的`warmth`仍沿用本例父项的8，所以加袖并不自动变暖。
2. 第一个分区限制到躯干上、下区域；第二个分区覆盖左右手臂。没有`sided: true`，因此双臂都会获得各自覆盖。
3. `armor`写出的是新的完整分区列表。它不会自动留下父背心的躯干分区，再把这里的躯干当成额外一层。

| 需要表达的设计 | 应使用的写法 | 容易发生的误读 |
|---|---|---|
| 上躯干和下躯干 | `torso_upper`、`torso_lower` | 它们不是前胸与后背，不能借此制作前后不同厚度 |
| 躯干与袖子不同厚度 | 两个`armor`对象，各自写材料 | 顶层`material`中列两种布，不会自动分配到衣身和袖 |
| 一件衣服有两只袖 | 同一分区的`covers`同时列左右臂 | 不因此拆成三件衣物 |
| 短袖只到上臂 | 写明确的上臂子部位，而非照抄整个arm范围 | 描述里写“短袖”不会自动缩小覆盖 |

身体ID从[data/json/body_parts.json](../../data/json/body_parts.json)查。不要把未注册的`front_chest`等英文词直接放进数组。

## 4. 加一层局部钢片：分清三个“比例/覆盖”

想让上躯干保留连续布料，并有一部分位置能挡到钢片，可以将上一例的第一个躯干分区替换为下列**局部片段**；下躯干另列布料分区，袖区仍沿用原方案。不要把本片段单独当成完整物品。

```json
{
  "covers": [ "torso" ],
  "specifically_covers": [ "torso_upper" ],
  "coverage": 95,
  "encumbrance": 5,
  "material": [
    { "type": "cotton", "covered_by_mat": 100, "thickness": 0.8 },
    { "type": "lc_steel", "covered_by_mat": 40, "thickness": 1.0 }
  ]
}
```

下躯干需要继续保留时，对应的另一个**局部片段**为：

```json
{
  "covers": [ "torso" ],
  "specifically_covers": [ "torso_lower" ],
  "coverage": 95,
  "encumbrance": 3,
  "material": [
    { "type": "cotton", "covered_by_mat": 100, "thickness": 0.8 }
  ]
}
```

这样是上躯干、下躯干、双臂三个分区。这里没有假装引擎已经区分胸板正面和背面。

三个看起来都像比例的东西，其实不是同一回事：

| 字段 | 回答的问题 | 本例怎样理解 |
|---|---|---|
| 分区`coverage` | 这件装备对该区域的覆盖判定怎样设置？ | 95，既不增加厚度，也不代表全身95% |
| 分区材料`covered_by_mat` | 进入材料防护计算时，这种材料是否被命中？ | 布100%，钢40%；钢被判中时用1.0厚度计算，不是每击固定用0.4mm钢 |
| 顶层材料`portion` | 总体材料组成份额怎样分配？ | 例如`cotton:9`、`lc_steel:1`是9:1的组成权重，不自动决定钢片位于哪里 |

物品顶层的组成也应相应改为棉与钢，例如下列**顶层字段片段**：

```json
{
  "material": [
    { "type": "cotton", "portion": 9 },
    { "type": "lc_steel", "portion": 1 }
  ]
}
```

9:1只是说明portion的示范值；真正选材时按用料估算，不从“钢覆盖40%”直接推出“钢占总质量40%”。新增钢片后要重设本体重量、体积和负担，不能指望上面的两处材料字段自动生成整件自重。

**材料覆盖概率也不保存精确甲片位置。** 将钢片概率写成40，并不等于做出了“左胸有钢、右胸没钢”的几何模型。需要的命中分区超出当前身体定义时，应先确认实现能力。

刚性也不是看到steel就由名字决定：当前完成计算有材料覆盖阈值等条件，本例没有HARD/SOFT覆盖标志，不据40这个数字保证获得刚性冲突行为。需要刚性装备时查[刚性与运行时参考](#armor-fields)。

## 5. 单侧护臂：左右都写，穿上只选一边

这次另做一件物品，不沿用上衣的全部覆盖。**完整示例：**

```json
[
  {
    "id": "example_leather_bracer",
    "type": "ARMOR",
    "name": { "str": "training leather bracer" },
    "description": "A leather guard for one forearm.",
    "symbol": "[",
    "color": "brown",
    "weight": "180 g",
    "volume": "250 ml",
    "material": [ "leather" ],
    "sided": true,
    "flags": [ "NORMAL" ],
    "armor": [
      {
        "covers": [ "arm_l", "arm_r" ],
        "specifically_covers": [ "arm_lower_l", "arm_lower_r" ],
        "coverage": 90,
        "encumbrance": 3,
        "material": [
          { "type": "leather", "covered_by_mat": 100, "thickness": 2.0 }
        ]
      }
    ]
  }
]
```

`covers`同时列出左右臂，是告诉系统这个类型适用于两侧；`sided: true`使具体穿戴实例只使用当前选中的一侧。`specifically_covers`限制到前臂，不保护上臂、肘和手。

- 想左右都戴，需要两件这种单侧物品。
- 想“一件物品代表一对护臂”，应另选双侧物品模型；不能把名字写成“pair”就自动生效。
- `180 g`是本例一侧的重量；不是再由`sided`自动把双侧重量减半。

这里选普通层只为讲清单侧功能。实际做02的外罩皮护臂时，应按其设计采用外套层。

### 层位应该怎样写？

上面`flags: ["NORMAL"]`给物品一个普通层默认值。想对某一个分区指定外套层，可在那个`armor`对象中写以下**分区字段片段**：

```json
{ "layers": [ "OUTER" ] }
```

普通整件外套也可以在顶层用`flags: ["OUTER"]`，让没有专门layers的分区取这个默认值。不要为了改成外套就在父NORMAL后简单追加OUTER，变成整件同时占两层。

`layers: ["NORMAL", "OUTER"]`表示占两层，不表示由玩家随意选一层。分区覆盖与层位是两件事：一个护臂即使换层，也不会因此保护另一只手臂或多出手掌覆盖。

## 6. 给背心加口袋：体积和容量分开

给第二节背心加一个500ml软口袋。**完整示例，依赖第二节背心：**

```json
[
  {
    "id": "example_pocket_vest",
    "type": "ARMOR",
    "copy-from": "example_cotton_vest",
    "name": { "str": "training pocket vest" },
    "description": "A vest with one small soft pocket.",
    "weight": "450 g",
    "volume": "1000 ml",
    "armor": [
      {
        "covers": [ "torso" ],
        "coverage": 95,
        "encumbrance": [ 2, 6 ],
        "material": [
          { "type": "cotton", "covered_by_mat": 100, "thickness": 0.6 }
        ]
      }
    ],
    "pocket_data": [
      {
        "pocket_type": "CONTAINER",
        "max_contains_volume": "500 ml",
        "max_contains_weight": "1 kg",
        "max_item_length": "20 cm",
        "moves": 100,
        "rigid": false
      }
    ]
  }
]
```

| 设置 | 本例的含义 |
|---|---|
| 顶层`volume: "1000 ml"` | 背心本体的收纳体积 |
| 口袋`max_contains_volume: "500 ml"` | 内容物总体积最多500ml，不是衣服本体体积 |
| `max_contains_weight: "1 kg"` | 总重量上限；容积够但太重仍不行 |
| `max_item_length: "20 cm"` | 单件长度限制；不因500ml装得下就能塞长枪 |
| `moves: 100` | 基础取物动作成本，不是穿衣成本 |
| `rigid: false` | 软口袋，内容物会影响外部体积和装载累赘 |
| `encumbrance: [2,6]` | 未合身基础累赘的空载/满载两端；中间随装载变化，不是随机2到6，也不是左臂2右臂6 |

本例手工选择满载6。若只写`encumbrance: 2`，当前完成计算会根据非刚性口袋容量与系数推导满载累赘；默认500ml约增加2，得到自动上限约4。显式写[2,6]不是对这个自动结果再加一次6。最后显示仍可能受角色和实例状态影响。

口袋`rigid`控制储物结构，不是让衣服获得刚性护甲。`watertight`控制口袋装液体，不是让穿戴者全身防水。两个相同口袋对象表示两个容量池，不能既写“总容量500ml”又无说明复制成两个500ml口袋。

附加甲使用的`ablative`口袋、弹药口袋和普通储物不同，等需要这些功能时再查[口袋完整字段](#pocket-fields)。

## 7. 做相近变体：先继承，再明确改动

若只想把背心做成较厚、较重的款式，可以沿用它的结构。**完整示例，依赖第二节背心：**

```json
[
  {
    "id": "example_heavy_vest",
    "type": "ARMOR",
    "copy-from": "example_cotton_vest",
    "name": { "str": "heavy training cotton vest" },
    "description": "A thicker version of the training vest.",
    "warmth": 12,
    "proportional": { "weight": 1.2, "volume": 1.1, "price": 1.5 },
    "extend": { "flags": [ "VARSIZE" ] },
    "armor": [
      {
        "covers": [ "torso" ],
        "coverage": 95,
        "encumbrance": 3,
        "material": [
          { "type": "cotton", "covered_by_mat": 100, "thickness": 0.9 }
        ]
      }
    ]
  }
]
```

按本例父项计算：重量350×1.2＝420g，体积750×1.1＝825ml，价格12×1.5＝18美元。分区材料厚度0.6改0.9、基础累赘2改3、保暖8改12，是另外明确写出的变化；乘重量不会自动完成这些变化。

`extend.flags`保留父NORMAL，再增加可改尺标志VARSIZE；它不等于实例已经合身FIT。如果直接写`flags: ["VARSIZE"]`，就不能按“自动保留父flags”理解。

### 常用继承操作怎么选？

| 需求 | 选择 | 结果/限制 |
|---|---|---|
| 只改名字、价格等少数属性 | `copy-from`＋直接字段 | 明确字段覆盖；注意并非所有特殊字段缺省都保留，查详细参考 |
| 数值随父项等比例调整 | `proportional` | 倍率，不是增加固定值；只用于reader支持的字段 |
| 添加一个特征 | `extend.flags` | 保留父flags再追加 |
| 去掉一个继承特征 | `delete.flags` | 移除指定flag，不删除父物品 |
| 覆盖区域、袖长或各区材料不同 | 明确重写`armor`完整数组 | 不依赖系统按身体部位自动替你patch |
| 替换同结构中的钢材 | `replace_materials`，然后复核结果 | 会同步相关材质且影响密度换算自重，但不会自动设计新厚度/固定累赘 |

例如想把父项OUTER换成NORMAL，可以使用以下**顶层操作片段**，并继续检查父分区是否已有显式`layers`：

```json
{
  "delete": { "flags": [ "OUTER" ] },
  "extend": { "flags": [ "NORMAL" ] }
}
```

这只改变flags；父分区若明确写了OUTER，仍需处理分区layers。继承检查应把flags、分区、口袋和动作一起看，不能只看子项短短几行。

## 8. 掀起面甲：两种状态，仍是一件头盔

需要面甲关闭和抬起两种覆盖时，可以用两个物品类型表达状态，再相互转换。**完整示例：**

```json
[
  {
    "id": "example_helmet_closed",
    "type": "ARMOR",
    "name": { "str": "training helmet with lowered visor" },
    "description": "A helmet with its visor lowered.",
    "symbol": "[",
    "color": "light_gray",
    "weight": "2 kg",
    "volume": "3 L",
    "material": [ "lc_steel" ],
    "flags": [ "OUTER" ],
    "armor": [
      {
        "covers": [ "head" ],
        "coverage": 95,
        "encumbrance": 6,
        "material": [
          { "type": "lc_steel", "covered_by_mat": 100, "thickness": 1.5 }
        ]
      },
      {
        "covers": [ "eyes", "mouth" ],
        "coverage": 90,
        "encumbrance": 2,
        "material": [
          { "type": "lc_steel", "covered_by_mat": 100, "thickness": 1.2 }
        ]
      }
    ],
    "use_action": {
      "type": "transform",
      "target": "example_helmet_open",
      "menu_text": "Raise visor",
      "msg": "You raise the visor.",
      "moves": 100,
      "need_worn": true
    }
  },
  {
    "id": "example_helmet_open",
    "type": "ARMOR",
    "copy-from": "example_helmet_closed",
    "name": { "str": "training helmet with raised visor" },
    "description": "A helmet with its visor raised.",
    "armor": [
      {
        "covers": [ "head" ],
        "coverage": 95,
        "encumbrance": 6,
        "material": [
          { "type": "lc_steel", "covered_by_mat": 100, "thickness": 1.5 }
        ]
      }
    ],
    "use_action": {
      "type": "transform",
      "target": "example_helmet_closed",
      "menu_text": "Lower visor",
      "msg": "You lower the visor.",
      "moves": 100,
      "need_worn": true
    }
  }
]
```

看懂这个例子，只需要抓住四点：

1. 关闭态有头、眼、口覆盖；抬起态只留下头部分区。抬面甲不是降低整个头部coverage，而是移除面甲原本负责的眼口覆盖。
2. 抬起态继承自关闭态，不重写重量，所以两态同为2kg。面甲还连在盔上，不因为抬起就少一块钢，也不额外生成一件面甲。
3. 两个`target`相互指向。若只写关闭→打开而没有回程，玩家就没有本文设定的关闭操作。
4. `need_worn`表示本例要求戴着才能操作；这是玩法选择。掀面甲本身不需要电池，因此本例仍为ARMOR，不需要TOOL_ARMOR或`active: true`。

这里的眼口90%是简化教学参数，并没有精确建立眼缝、通气孔或完整头盔接缝。实际头盔需要按02的覆盖方案细化。

`use_action.type`与物品顶层`type`不同：前者选动作处理器，后者选物品加载器。读取与转换行为见[src/iuse_actor.cpp](../../src/iuse_actor.cpp)的`iuse_transform::load/use/do_transform`。

## 9. 从“能读懂”到“能检查”

拿到一件原版衣服时，按这个顺序读：

1. 找`id`、`type`、`copy-from`，先确认它是谁、从哪里继承。
2. 看本体重量、体积、材料、保暖；不要把口袋内容量当自重。
3. 逐个读`armor`：保护哪个主/子部位、哪层、什么材料多厚、多大覆盖、多少基础累赘。
4. 看`sided`、flags和口袋，判断是不是单侧、是否能改尺、有无多余储物或附加甲。
5. 有动作再看`use_action`/`tick_action`及目标ID；没有动作就不需要学习所有actor。
6. 对照设计，明确哪些是内含构件、哪些独立物品、哪些只是两件装备一起穿。

| 想解决的问题 | 该查什么 |
|---|---|
| 名称、质量、体积、价格怎么写 | [通用字段表](#item-fields)第一、二节 |
| 某处材料、覆盖、层位和累赘怎么写 | [护甲完整参考](#armor-fields) |
| 怎样加储物或插板 | [口袋字段](#pocket-fields)，插板还需看护甲参考的Ablative说明 |
| 怎样掀面甲、折叠或供电 | [动作与状态](#action-fields)，有工具槽再查TOOL_ARMOR |
| 想找原版真实例子 | [原版逐字段与实例清单](#field-inventory)，按字段或物品ID搜索 |
| 正式编辑和验证应怎么做 | [编辑Skill与检查流程](#editing-skill) |

完整字段清单放在后面，是用到时查询的资料，不要求第一次从头读完。教学例子没有出现的字段仍保留在手册中，也不意味着普通衣服必须填写它们。


<a id="item-fields"></a>

# 第二部分：字段查阅手册

本部分用于查询，不是必须逐项填写的模板。先按第一部分确定自己的物品结构，再查需要的字段；工具、枪械、附魔等混合槽仅在该物品具备对应功能时阅读。

## 一、定义、加载与继承

入口为 [item_factory.cpp](../../src/item_factory.cpp)：`load_armor`（2794）、`load_tool_armor`（3165）、`load_basic_info`（4077）、`load_definition`（2535附近）；动态注册见 [init.cpp](../../src/init.cpp)。

| 字段 | 形式与用途 | 缺省、继承及边界 |
|---|---|---|
| `type` | 字符串；`ARMOR`为普通服装护甲，`TOOL_ARMOR`兼工具槽与护甲槽 | 是加载路由，不是装备游戏分类名；工具服装还需工具字段 |
| `id` | 物品ID（常用单字符串；多ID定义须核对注册层展开） | 具体物品使用；引用配方、物品组、变形目标时用它 |
| `abstract` | 抽象模板ID字符串 | 不生成实物；与具体`id`择一。模板也由相应物品加载器处理 |
| `copy-from` | 父物品/抽象ID字符串 | 先复制完整itype；找不到先延迟，最终仍缺失才报错。不是JSON文本合并 |
| `relative` | `{字段:增量}` | 仅适用实现了相对赋值的字段；单位字段按其reader写单位，不能假设所有嵌套字段都支持 |
| `proportional` | `{字段:倍率}` | 1.2表示父值乘1.2；不是增加1.2。`melee_damage`有专门处理 |
| `extend` | `{集合字段:[新增成员]}` | 保留父集合再加成员；flags、qualities、techniques各有对应reader，不能推广到任意数组 |
| `delete` | `{集合字段:[移除成员]}` | 移除父集合成员；不会删除物品定义或其引用 |
| `replace_materials` | `{旧材料ID:新材料ID}` | 不仅改顶层标签：会处理护甲分区材质并按密度调整质量；详见护甲参考 |
| `//`及注释键 | JSON字符串注释数据 | 不用C++注释；JSON无尾逗号。不要把程序读取的参数藏在注释中 |

`load_definition`复制itype后设置`was_loaded`。`load_basic_info`却并非每个字段都“缺省继承”：`name`重新读且缺失报错；`variant_type`/`variants`用`false`加载而非父`was_loaded`；`snippet_category`在缺省时回空串；`thrown_damage`缺省会重建；具体行为见源码。不要只读[JSON_INHERITANCE](../../doc/JSON_INHERITANCE.md)概括后猜字段行为。

服装`armor`数组的继承不是按“身体部位ID逐项patch”；修改必须核查护甲参考中的merge逻辑。常规标量直写通常覆盖父值，集合直写常会整体替换。删掉子定义某字段通常会恢复继承，不代表将它清零。

## 二、通用物品字段：身份、显示与体量

本节入口均为`load_basic_info`，初值见 [itype.h](../../src/itype.h) 的`itype`。除明确例外外，不写会保留复制所得值；新对象取构造初值或finalize推导。数量、重量和体积都不能代替覆盖区域与材料厚度。

| 字段 | 类型/单位/默认 | 实际用法及容易混淆的地方 |
|---|---|---|
| `name` | 翻译字符串或对象；本加载阶段要求提供 | 普通名用`{"str":"..."}`；不规则复数加`str_pl`，单复数相同用`str_sp`，消歧用`ctxt`。不是ID |
| `description` | 翻译文本；新对象空 | 描述用途和覆盖，不靠描述文本实现防护功能 |
| `symbol` | 字符串；要求单控制台格宽 | 地图字符，不改变贴图或装备槽 |
| `color` | 已注册颜色名；初值white | 字符显示颜色；不是染色工艺或材质 |
| `looks_like` | 其他物品ID | tileset后备外观；copy-from父具体物品时可自动取父ID；不继承物理参数 |
| `category` | item_category ID | 强制物品分类；没有时由系统归类。不是`type`、穿着层或部位 |
| `ascii_picture` | ascii_art ID | 查看物品时ASCII图；不会定义新的美术资源 |
| `snippet_category` | 类别ID字符串或片段数组 | 数组创建`auto:物品ID`类别；缺省在本函数回空，不能简单假定继承 |
| `expand_snippets` | bool，首次默认false | 生成实例时展开描述片段并保存；不是实时每次重抽 |
| `phase` | 枚举字符串，初值solid | 物质相态，不决定布料柔软或甲板刚性 |
| `weight` | 质量字符串，如`"2 kg"`；非负 | 服装本体重量；内容物另计，不能把整套其他独立件都计入 |
| `volume` | 体积，如`"1500 ml"` | 物品收纳体积；不是口袋容量，不是皮厚 |
| `longest_side` | 长度，如`"40 cm"` | 收纳时最长边；未写可由体积推导，不等于衣长的史料测量 |
| `integral_weight` | 质量；未写最终回退本体质量 | 作为附件整合到其他物品时增加的重量；普通独立衣物一般不用 |
| `integral_volume` | 体积；未写最终回退本体体积 | 整合时增量体积；不用于“穿上以后体积” |
| `integral_longest_side` | 长度，非负；finalize有回退处理 | 附件整合的长度增量；不是袖长 |
| `price` | 金额整数（cent）或`"10 USD"`；初值0 | 灾前价值，不是生产工时 |
| `price_postapoc` | 同金额格式；未写可在finalize回退price | 灾后交易价值；两种价值都不是直接限制玩家购买能力的脚本 |
| `stackable` | bool，初值false | 类型的堆叠方式；普通独立衣物不因左右成对就设true |
| `container` | 默认生成容器ID，可为空 | 生成时所处外容器，不是衣服自己的口袋 |
| `sealed` | bool，初值true | 上述默认外容器的封装状态；不是服装气密性 |
| `insulation` | 浮点，初值1 | 对所装内容物/车辆件的隔热系数；服装穿戴保暖另用`warmth` |
| `solar_efficiency` | 浮点，初值0 | 太阳能背包发电效率，需对应flag及工作状态；普通衣物不用 |
| `degradation_multiplier` | 数字，加载默认1 | 当前实现随后对按charges计数物品或非车辆部件分类强制关闭该类退化增量；不能照文档把它当通用衣物耐久倍率 |

内联`snippet_category[]`中`id`是片段标识，`text`是可翻译正文；不要把片段id当物品id。

名称嵌套对象的`str`、`str_pl`、`str_sp`、`ctxt`均由翻译reader解释；不把`str_pl`放在物品顶层。`description`常见为单字符串；需要上下文时按translation格式写，不能给它编造护甲参数子键。

### 条件名称与外观变体

`conditional_names`是数组，直写时清空父列表。每项：`type`为条件枚举（参见`condition_type`与[item.cpp](../../src/item.cpp)条件命名代码）；`condition`为匹配字符串；`name`为翻译名称，必需；`value`为附加匹配值，缺省空。它改变显示名称，不改变材料、覆盖和伤害。

`variant_type`目前可选`generic`、`gun`，控制外观变体选项类别。`variants`为数组；读取见`itype_variant_data::load`（item_factory.cpp:2724）。每项字段如下：

| `variants[]`字段 | 用法 |
|---|---|
| `id` | 必需，变体局部标识，不是另一个物品ID |
| `name` | 必需，翻译名称，替代基础名 |
| `description` | 必需，翻译描述 |
| `symbol` | 可选，替代字符；未给保留基础显示 |
| `color` | 可选，替代颜色 |
| `ascii_picture` | 可选，替代ASCII图 |
| `weight` | 整数选择权重，默认1；0不随机选中。**不是物理重量** |
| `append` | bool，默认false；描述追加或替换 |
| `expand_snippets` | bool，默认false；是否展开该变体描述片段 |

变体只适合这些外观差异。厚度、材料、防护或覆盖不同，应建立具体物品变体，不把参数塞进不读取的`variants[]`键。

## 三、通用物品字段：材料、攻击、品质与行为

| 字段 | 形式 | 读取与用途 |
|---|---|---|
| `material` | 单ID/ID数组，或`[{"type":"材料ID","portion":整数}]` | 顶层材料组成。写入时先清空旧映射；portion默认1，作为相对份额，非mm、非护甲每击覆盖率；首材料还记录为default_mat |
| `material[].type` | 材料ID | 顶层组成项；与`armor[].material[].type`同名但上下文不同 |
| `material[].portion` | 整数，默认1 | 例如9和1表示组成份额9:1；分区材料防护在armor中另写 |
| `repairs_with` | 材料ID集合 | 允许修理用材；finalize可从本体材料补全。不是修理工具ID |
| `repairs_like` | 其他物品ID | 为维修参考其他物品的配方/材料规则，不继承防护 |
| `melee_damage` | `{伤害类型ID:非负数值}` | 把这件物品当武器挥击的伤害，不是护甲抗性；支持专门relative/proportional映射 |
| `to_hit` | 整数，或对象 | 物品作为攻击武器的命中修正；穿在身上不会自动削弱另一把手持武器 |
| `weapon_category` | 武器分类ID集合 | 武术武器分类匹配，不能拿来表示板甲类型 |
| `thrown_damage` | 伤害实例数组 | 投掷该物品的伤害；不写时按近战bash和自重重建，不是继承所有父投掷伤害 |
| `min_strength` | 数字，初值0 | 使用条件属性门槛；不等于自动建立穿戴训练系统 |
| `min_dexterity` | 数字，初值0 | 使用敏捷要求，具体生效点查`item::is_usable`等调用 |
| `min_intelligence` | 数字，初值0 | 使用智力要求 |
| `min_perception` | 数字，初值0 | 使用感知要求 |
| `min_skills` | `[[技能ID,等级],...]` | 使用技能要求；非空列表会清旧映射，空列表不一定清除已继承技能 |
| `qualities` | `[[品质ID,等级],...]` | 无电也有效的工具品质；直写替换，支持特定extend/delete/relative操作 |
| `charged_qualities` | 同上 | 有足够电量/charges时的品质；与普通qualities分开 |
| `techniques` | 技法ID数组 | 物品用作武器时的技法；直写替换，有extend/delete专用分支 |
| `flags` | flag ID集合 | 声明给具体机制消费的标志；直写可能覆盖父集合，增删使用extend/delete |
| `properties` | 字符串到字符串映射 | 物品定义静态属性，需有消费者，不是任意新字段就生效 |
| `variables` | 字符串到字符串映射 | 创建实例时赋予变量；与静态properties不同 |
| `faults` | fault ID集合 | 可出现的故障；不是简单破损等级 |
| `source_monster` | monster ID | 尸体等特例；服装不应借此改变重量 |
| `chat_topics` | 话题ID数组 | 会话入口；显式给出清空再重建 |
| `use_action` | 字符串/对象/动作数组 | 玩家主动激活，派发到iuse或iuse_actor，见后文 |
| `tick_action` | 同类动作格式 | 活动状态逐tick调用，与主动激活不是同一时机；同一ammo_scale容器的加载须留意覆盖顺序 |
| `emits` | emit ID集合 | 激活状态发射的场等，不是光照数值 |
| `countdown_interval` | 时间量，初值0秒 | 生成实例后倒计时；与工具耗电周期不同 |
| `countdown_action` | 动作字符串或对象 | 计时终结动作；不是静态护甲防护字段 |
| `drop_action` | 动作字符串或对象 | 丢弃时的行为 |
| `revert_to` | 目标物品ID | 倒计时或工具耗尽后回退，需实际存在目标；不能代替变形use_action的target |
| `explode_in_fire` | bool，初值false | 火中爆炸行为开关 |
| `explosion` | 爆炸参数对象 | 见下；与穿戴防火抗性无关 |
| `magazines` | `[[弹药类型,[兼容弹匣ID,...]],...]` | 第一兼容弹匣为默认；直写清旧映射。工具服装的供电组件需要核查口袋 |
| `nanofab_template_group` | item_group ID | 纳米制造模板特例，普通衣物不需要 |
| `template_requirements` | requirement ID | 纳米制造需求特例，不等于衣服制作配方 |
| `memory_card` | 数据卡参数对象 | 数据功能特例；完整读取字段在item_factory.cpp:2581附近 |
| `armor_data` | 护甲槽对象 | 让其他主类型物品具备护甲数据；用与islot_armor相同字段格式，不是`armor`分区数组本身 |
| `pet_armor_data` | 动物护甲槽对象 | 兽用覆盖/尺寸字段，参见护甲参考 |
| `book_data` / `gun_data` / `bionic_data` / `ammo_data` / `seed_data` / `brewable` / `relic_data` / `milling` / `gunmod_data` | 对应功能槽对象 | 加载器支持的混合物品能力。实际服装清单中出现与否见字段盘点；不能把其他槽参数直接放顶层当衣物字段 |
| `pocket_data` | 口袋对象数组 | 服装储物、插板和可挂载容器结构，见第五节 |

`to_hit`对象四项均为必需：`grip`取bad/none/solid/weapon；`length`取hand/short/long；`surface`取point/line/any/every；`balance`取clumsy/uneven/neutral/good。由`io::acc_data`合成攻击命中分值；这些是握持攻击特征，不描述穿甲后的姿势。

`thrown_damage[]`使用伤害实例格式：`damage_type`指定类型，`amount`伤害，`armor_penetration`穿透，其他倍率由[damage.cpp](../../src/damage.cpp)的reader决定。只需要普通服装时不要为“全字段”而填攻击值。

`explosion`字段：`power`为爆炸能量量级、`distance_factor`衰减、`max_noise`最大噪声、`fire`是否产生火；`shrapnel`可为质量整数或对象，后者含`casing_mass`总壳质量、`fragment_mass`单片质量、`recovery`回收率、`drop`掉落物ID。以[explosion.cpp](../../src/explosion.cpp)的`load_explosion_data`为准，不从服装材料厚度推爆炸数据。

`memory_card`逐项：`data_chance`默认1；`on_read_convert_to`目标ID；`photos_chance`/`songs_chance`/`recipes_chance`默认0；`photos_amount`/`songs_amount`/`recipes_amount`默认0；`recipes_level_min`默认0、`recipes_level_max`默认10；`recipes_categories`缺省CC_FOOD；`secret_recipes`控制隐藏配方。它们属于数据卡功能，不会影响服装防护。

原版`petpack`使用`properties.creature_size_capacity`指定可容纳生物的尺寸上限，字符串由宠物容器使用逻辑解释；它不表示背包体积，也不改变人体穿戴部位。

`milling`对象含`into`结果物品ID与`conversion_rate`数量换算率。没有相应需求不添加。其他功能槽的完整schema超出服装防护核心；若原版可穿戴混合型使用，则需连同该槽的加载器一起编辑，不能套用护甲schema。

## 四、护甲与服装专属字段

详细逐项表和所有嵌套参数见[护甲字段参考](#armor-fields)，包括：

- 顶层护甲槽：保暖、环境防护、动力甲、尺寸/宠物护甲、材料厚度与分区数组。
- `armor[]`：`covers`、`specifically_covers`、各类coverage、累赘、重量生成累赘描述符、层位、刚性、透气率、口袋容量对累赘的影响。
- `armor[].material[]`：材料类型、材料覆盖概率、厚度和板材厚度处理。
- `armor_data`混合类型写法、继承、finalize生成部位数据与一致性检查。

护甲分区是受击与穿戴参数区域，不是物品实例。历史上肩甲、上臂甲、肘甲、前臂甲的配套关系不能仅凭JSON中四个armor分区推定；一件独立臂甲可以有四个分区，四件独立物品也可以各有自己的分区。先确定穿戴单位，再编JSON。

<a id="pocket-fields"></a>

## 五、`pocket_data[]`全部加载字段

源码：[item_pocket.cpp:120](../../src/item_pocket.cpp)、初值见[item_pocket.h](../../src/item_pocket.h)。每个对象是一个口袋，不是整件衣服的公共参数。复制几个口袋对象即表示几个独立容量池，不能既写总容量又复制相同口袋重复计容量。

| 字段 | 类型/默认（新口袋） | 用法与约束 |
|---|---|---|
| `pocket_type` | 枚举，CONTAINER | 普通口袋CONTAINER，弹药MAGAZINE、弹匣槽MAGAZINE_WELL等须匹配实际pocket_type；不得自行造字符串 |
| `name` | 翻译文本，空 | 区分口袋用途的短名 |
| `description` | 翻译文本，空 | 口袋说明，非衣物总说明 |
| `max_contains_volume` | 体积，缺省为极大哨兵容量 | 内容物总体积上限；服装必须给实际值，别利用省略获得无限容量 |
| `max_contains_weight` | 质量，缺省为极大哨兵重量 | 内容物总重量上限；不等于物品自重 |
| `min_item_volume` | 体积，0ml | 可装单件最小体积，过小会漏出等 |
| `max_item_volume` | 可选体积，无限制值 | 单件体积上限；与总容量不同 |
| `max_item_length` | 长度，缺省按容量推导 | 单件最大长度；容积够不代表长枪能塞入 |
| `min_item_length` | 长度，0mm | 可装最短物件；外部固定具等用途 |
| `extra_encumbrance` | 整数，0 | 口袋使用时额外累赘，不是衣物全部基础累赘 |
| `volume_encumber_modifier` | 浮点，1 | 该口袋对内容物体积累赘的权重；与armor分区同名字段分属两个读取位置 |
| `ripoff` | 整数，0 | 摆脱抓取时内容物被扯落机会参数；不是衣料抗撕裂 |
| `activity_noise` | 对象，默认无声 | 移动噪声；子项`volume`音量整数默认0，`chance`概率整数默认0；不是armor[]字段 |
| `spoil_multiplier` | 浮点，1 | 内容物腐败速度倍率，0停止腐败；不是防护耐久 |
| `weight_multiplier` | 浮点，1 | 计算所携内容物重量的倍率；不改变衣服自重 |
| `volume_multiplier` | 浮点，1 | 内容物对外部体积的倍率；不直接增加口袋内部容量 |
| `magazine_well` | 体积，0ml | 内容物先占用的隐藏空间，超出才增大外部体积 |
| `moves` | 整数，100动作点 | 基础取物成本；不是穿脱整件衣物耗时 |
| `fire_protection` | bool，false | 保护内容物免受火中爆炸等；不是穿戴者火抗 |
| `watertight` | bool，false | 可装液体；不等于衣服防雨/潜水密封 |
| `airtight` | bool，false | 可装气体；不直接赋予穿戴者防毒 |
| `open_container` | bool，false | 开口容器在放入其他容器时可能洒出内容物 |
| `transparent` | bool，false | 内容可见性 |
| `rigid` | bool，false | 刚性容器外部体积不随内容物扩张；不是盔甲刚性层冲突标志 |
| `forbidden` | bool，false | 禁用普通装入；仅在对应容器逻辑需要时使用 |
| `holster` | bool，false | 限制为单个物品的固定具；不等于所有武器都能放入 |
| `ablative` | bool，false | 附加护甲口袋；加载时强制holster=true，防护、层位、累赘会走附加甲逻辑 |
| `inherits_flags` | bool，false | 内容物flags传递到容器物品；不是继承父JSON的flags |
| `flag_restriction` | flag ID集合，空不限制 | 匹配任一允许flag；与ID/基底材料限制并列时是“或”，见表后说明。正确键为单数restriction，不写flag_restrictions |
| `item_restriction` | 物品ID集合，空不限制 | 单独配置时限定指定ID；与flag/基底材料限制并列时满足任一即可。显式空数组报错，首项还用于default_magazine |
| `material_restriction` | 材料ID集合 | 匹配物品`get_base_material().id`，不是任意一种组成材料；与ID/flag限制按“或”组合，不是口袋本体材料 |
| `ammo_restriction` | `{弹药类型:容量}` | 专门弹药口袋；非空时绕过下面所述普通容量字段读取 |
| `allowed_speedloaders` | 物品ID集合 | 允许使用的快速装填器 |
| `default_magazine` | 物品ID | 弹匣槽默认物品；可能受item_restriction首项覆盖 |
| `sealed_data` | 对象 | 封装口袋的差异数据；当前子字段`spoil_multiplier`，默认1 |

**三类白名单怎样组合？** `item_pocket::compatible`（`src/item_pocket.cpp:1386`起）把`item_restriction`、`flag_restriction`、`material_restriction`按“满足任一种”处理：ID匹配、任一flag匹配、基底材料匹配，三者有一个成立便通过这组筛选。它们不是三重“且”限制。例如指定某件物品ID的同时又允许一个flag，其他ID但有该flag的物品也能通过这组筛选。常规储物的尺寸、容量、重量等检查仍分别进行；通过白名单不等于最终一定装得下。

**分支约束**：`ammo_restriction`非空时，加载器不读取普通容量分支中的`min_item_volume`、`max_item_volume`、`max_contains_volume`、`max_contains_weight`、`max_item_length`、`min_item_length`、`extra_encumbrance`、`volume_encumber_modifier`、`ripoff`、`activity_noise`。不要在弹药口袋中盲目叠加全部容量键。空ammo_restriction会报错；flag空数组检查在当前源码有单复数名称不一致，不能靠该检查保证输入正确。

## 六、`TOOL_ARMOR`工具槽

`load_tool_armor`同时调用工具槽和护甲槽读取。普通ARMOR即使有use_action，也不自动获得工具充电槽；根据动作需求选择类型，而不是所有可切换衣服都改成TOOL_ARMOR。

| 字段 | 类型/约束 | 用法 |
|---|---|---|
| `ammo` | 弹药类型集合 | 电池、滤芯或其他消耗品类型，需和弹匣/口袋一致 |
| `max_charges` | 非负整数 | 容量字段，具体供电也会由口袋派生；不与max_contains_volume混用 |
| `initial_charges` | 非负整数 | 初始数量，不能大于max_charges；与rand_charges互斥 |
| `rand_charges` | 至少两元素整数数组 | 相邻端点区间随机初始量；不是任意权重池；继承时源码push_back，要留意叠加 |
| `charges_per_use` | 非负整数 | 使用消耗；与actor的need_charges前置检查不同 |
| `charge_factor` | 整数至少1 | charges换算因子 |
| `turns_per_charge` | 非负整数 | 周期耗电间隔 |
| `fuel_efficiency` | 浮点，允许值下限-1 | 燃料效率特例；不当盔甲热效率 |
| `power_draw` | 功率量，如`"10 W"`，非负 | 激活工作功耗 |
| `revert_msg` | 翻译文本 | 回退状态提示 |
| `sub` | 字符串工具子类型 | 工具兼容/替代类别，不是服装子部位 |

源代码里的assign参数常是合法下界，不是“省略后的默认值”；实际初值还需读`islot_tool`，不要把`max_charges`读取参数0误称所有父类省略都会回0。

<a id="action-fields"></a>

## 七、动作对象与状态变体

动作加载入口`set_use_methods_from_json`（item_factory.cpp:5072）接受注册动作字符串、actor对象或数组。对象中的`type`负责选择actor，`ammo_scale`是外层动作消耗倍率参数，不是装备材料份额。不同type有不同schema，不能将所有actor子键平铺到同一个对象。原版现用动作及路径见字段清单。

### `transform`：展开、收起、掀面甲等

当前实际读取位于 [iuse_actor.cpp:165](../../src/iuse_actor.cpp)。它与部分官方示例不同，目标弹药键是`target_ammo`，不是从旧示例抄`ammo_type`。

| 字段 | 形式与缺省 | 用法或限制 |
|---|---|---|
| `type` | `"transform"` | actor路由 |
| `target` | 必需物品ID | 转换目标；转换前后是同一物品的状态，不应同时生成两件装备 |
| `msg` | 翻译文本 | 转换提示 |
| `variant_type` | 变体局部ID或`<any>` | 目标外观变体；不等于物品顶层的generic/gun枚举 |
| `container` | 目标容器ID | 结果放入的容器；与target_ammo互斥 |
| `sealed` | bool | 上述生成容器是否封装，不是面甲密闭 |
| `target_charges` | 整数 | 目标charges固定值，与rand_target_charges互斥 |
| `rand_target_charges` | 至少两元素整数数组 | 相邻区间随机目标量 |
| `target_ammo` | 弹药物品ID | 目标装载类型；不能与container并存 |
| `target_timer` | 时间量 | 目标倒计时 |
| `active` | bool | 转换后是否激活运行 |
| `moves` | 非负整数动作点 | 转换耗时，不是额外护甲累赘 |
| `need_fire` | 非负整数 | 要求并消耗点火资源；负数被钳到0 |
| `need_fire_msg` | 翻译文本 | 点火条件失败提示 |
| `need_charges` | 非负整数 | 转换前置charges检查；不是对所有actor都通用的持续功耗 |
| `need_charges_msg` | 翻译文本 | 电量不足提示 |
| `need_worn` | bool | 要求已穿戴 |
| `need_wielding` | bool | 要求正持握 |
| `need_empty` | bool | 要求内部为空，避免不合逻辑转换 |
| `qualities_needed` | `{品质ID:等级}` | 所需工具品质 |
| `menu_text` | 翻译文本 | 激活菜单文本 |

actor构造初值见[iuse_actor.h](../../src/iuse_actor.h)的`iuse_transform`；不同字段`read`失败保留该初值，并非全都false或0。`delayed_transform`还读`transform_age`与`not_ready_msg`，其单位/时钟处理要检查其load和use实现。

### 其他动作

服装也可有电热、滤毒、潜水气瓶、MOLLE、枪套、展开物、效果条件等功能。它们分别由硬编码iuse或actor处理，不是所有功能都有JSON对象字段。遇到字符串动作先查`Item_factory`注册表，再查对应[iuse.cpp](../../src/iuse.cpp)；遇到对象查[iuse_actor.cpp](../../src/iuse_actor.cpp)中对应`load()`，最后看`use()`。实际现用的所有对象子路径见字段盘点；新增actor参数时必须在其schema内查证，不能以本表transform字段套用。

## 八、原版现用其他 actor 的字段用法

下列按actor分别列出字段；同时出现在对象与数组内的路径是同一schema。入口均在 `src/iuse_actor.cpp` 的对应`load()`，以下行号对应本地版本。

| actor（加载位置） | 字段逐项用法 |
|---|---|
| `unpack`（477） | `group`：展开生成的item_group ID；`items_fit`：是否让生成服装合身；`filthy_volume_threshold`：内容物容积达到该阈值时触发相应脏污处理，体积量，默认0ml。不是衣服本体防污值 |
| `message`（530） | `name`：可选动作菜单名；`message`：使用/倒计时打印的翻译文本。不是transform使用的`msg` |
| `manualnoise`（2024） | `use_message`：必需的使用提示；`noise_message`：声音描述；`noise_id`：音效类别，默认misc；`noise_variant`：默认default；`noise`：声强整数，默认0；`moves`：使用成本动作点，默认0 |
| `firestarter`（1243） | `moves`：容易点燃目标的基础动作点；`moves_slow`：较难目标耗时，默认前者10倍；`need_sunlight`：需日光，默认false。实际耗时还受角色和环境影响 |
| `holster`（2462） | `holster_prompt`：选择存入物品的提示；`holster_msg`：存入反馈。大小、重量、类型限制由pocket_data决定，不把这些限制写进actor冒充有效参数 |
| `attach_molle`（4085） | `size`：挂载兼容规模；`moves`：动作成本参数；实际use将附件容器口袋加入本体并移除外部附件实例，不是普通copy-from |
| `detach_molle`（4152） | `moves`：动作成本参数；拆卸已附加口袋还原附件，不能等同丢掉内容物 |
| `repair_item`（2646） | `materials`：必需，能修复的材料ID数组；`skill`：必需，合法技能ID；`cost_scaling`：必需，耗材量缩放浮点；`tool_quality`：工具品质值默认0；`move_cost`：每步动作点默认500；`trains_skill_to`：训练上限默认5，内部存值减1。`item_action_type`是本actor的动作注册/显示分类，参见usage_from_object，不能拿它更改服装材料 |
| `deploy_furn`（1060） | `furn_type`：必需，展开成的家具ID；不是穿戴覆盖部位 |
| `link_up`（4400） | `cable_length`：最大线长，未指定按类的回退值处理；`charge_rate`：功率量，正值给设备充电、负值向电网输出；`efficiency`：效率；`move_cost`：连接动作点；`menu_text`：菜单文案；`targets`：允许的连接状态枚举集合，如vehicle_port、ups、solarpack、no_link；`can_extend`：能延长的线缆ID，ELECTRICAL_DEVICES为特例。仅写charge_rate不会自动创建电池槽 |
| `musical_instrument`（2097，常在tick_action） | `speed_penalty`：演奏速度惩罚默认10；`volume`：必需声强；`fun`：必需基础士气量；`fun_bonus`：额外量默认0；`description_frequency`：必需描述间隔，reader同时处理旧整数turns及时间量；`player_descriptions`、`npc_descriptions`：不同角色提示列表。它们不是顶层服装fun或保暖值 |
| `explosion`（618，常在countdown_action） | `explosion`：物理爆炸数据；`draw_explosion_radius`、`draw_explosion_color`：可视爆炸显示；`do_flashbang`：闪光效果；`flashbang_player_immune`：玩家免疫；`fields_radius`：场生成半径；`fields_type`：场ID，有半径时须能读取；`fields_min_intensity`、`fields_max_intensity`：强度范围，max为0时取场最大强度；`emp_blast_radius`：EMP范围；`scrambler_blast_radius`：干扰范围 |

原版字符串动作如`GASMASK_ACTIVATE`、`GASMASK`、`DIVE_TANK_ACTIVATE`、`DIVE_TANK`、`RM13ARMOR_ON/OFF`、`SOLARPACK`、`MP3`、`TOWEL`等由注册的C++函数处理，不读取任意actor自定义键。它们的函数分工是启用/停用、消耗滤芯/气体/电量及应用效果；编辑前按注册名找到iuse函数并检查供电、环境值和状态目标。完整现用名称见字段盘点，不把名字相似视为可互换。

## 九、原版可穿戴混合物品实际出现的其他槽字段

本节补充统计中真实出现、但不属于护甲本身的字段，不要求普通服装全部填写。来源为item_factory.cpp的`load(islot_gun)`（2740）、`load(islot_gunmod)`（3410）、`load(islot_magazine)`（3490）。

| 字段 | 所属槽、形式与用法 |
|---|---|
| `ammo_effects` | 枪械：弹药效果ID集合，影响发射而非穿戴 |
| `clip_size` | 枪械：非负整数内置弹容量 |
| `dispersion` | 枪械：基础散布值；不是累赘 |
| `sight_dispersion` | 枪械/枪械改装：瞄具散布，枪械加载校验0至MAX_RECOIL |
| `durability` | 枪械：0–10耐用等级；不控制衣物受损耐久 |
| `loudness` | 枪械：发射声强修正；与口袋activity_noise不同 |
| `range` | 枪械：射程属性修正 |
| `ranged_damage` | 枪械：伤害实例对象；`damage_type`指定类型、`amount`为数值，和护甲抗性完全分开 |
| `modes` | 枪械：模式ID到模式数据的映射；模式成员为显示名称、发数、flags等，按gun_mode reader核对 |
| `reload` | 枪械：非负整数装填动作点 |
| `reload_noise_volume` | 枪械：非负整数装填声音强度 |
| `skill` | 枪械：使用技能ID；与repair_item.actor.skill位置不同 |
| `valid_mod_locations` | 枪械：`[[安装位字符串,数量],...]`，直写清旧列表 |
| `install_time` | 枪械改装：整数动作点或时间字符串，最终转动作点 |
| `location` | 枪械改装：安装位ID，非身体部位 |
| `mod_targets` | 枪械改装：允许安装的枪类别集合；直写重建 |
| `ammo_type` | 弹匣：弹药类型集合 |
| `capacity` | 弹匣：非负整数弹容量；不同于口袋体积 |
| `default_ammo` | 弹匣：默认装填弹药物品ID |
| `linkage` | 弹匣：弹链回收/分解的链节物品ID |

统计中继承修饰也出现`calories`、`fun`、`healthy`、`quench`：这些属于可食用混合物品的营养、乐趣、健康与解渴参数，`proportional`乘父值，不是衣物舒适或透气字段。源码为`load(islot_comestible)`，食用逻辑不可替代穿戴逻辑。

### `relic_data.passive_effects[]`的现用子字段

读取链为 [relic.cpp:342](../../src/relic.cpp) → `enchant_cache::load` → [magic_enchantment.cpp](../../src/magic_enchantment.cpp) 的`enchantment::load`与缓存加载。

| 路径 | 用法 |
|---|---|
| `relic_data.passive_effects` | 被动附魔对象数组，不是护甲材料数组 |
| `passive_effects[].id` | 引用已注册附魔ID；有ID时在finalize再解析对应定义 |
| `passive_effects[].has` | 携带状态枚举，缺省HELD；WORN要求穿戴，WIELD要求持握。不能认为所有被动都只在穿上时生效 |
| `passive_effects[].condition` | 激活条件枚举字符串或条件对象；字符串如ALWAYS/ACTIVE/INACTIVE依枚举检查，条件对象走对话条件reader |
| `passive_effects[].condition.not` | 对内部条件取反；内部可以是合法条件字符串/对象，不是纯备注 |
| `passive_effects[].mutations` | 赋予的mutation ID集合；不是服装材质变种 |
| `passive_effects[].values` | 修改值数组，每项指定目标值与加/乘修正 |
| `values[].value` | `enchant_vals::mod`枚举名，必须有效；如护甲或属性类参数，不是任意变量名 |
| `values[].add` | 加法修正值，缓存加载读取整数；不等于百分比。通用enchantment定义还能用动态值reader，不能据此假定relic缓存同样读取所有动态格式 |

本节只枚举当前服装数据实际出现的附魔子键。其他附魔能力如multipliers、effects等须按实际加载器和需求另查；材料抗性仍应由材料/分区表达，不用被动附魔掩盖普通衣物参数错误。


## 十、flags与外部数据的分工

`flags`是一个字段，其数组里的每个ID不是新的JSON字段。原始定义见[data/json/flags.json](../../data/json/flags.json)，说明见[JSON_FLAGS](../../doc/JSON_FLAGS.md)，实际行为仍看消费代码。尤其区分：

| 类别 | 核查重点 |
|---|---|
| 层位flag与`armor[].layers` | flags可能提供默认层；分区层能细化，不能将同义字随意换成STRAPPED |
| `VARSIZE`与`FIT` | 可改尺与实际合身状态不同；累赘显示还受实例状态影响 |
| `STURDY` | 具体耐损行为，不赋予额外覆盖或任意抗性 |
| `WATERPROOF`、`RAINPROOF` | 穿戴水环境行为，不能用口袋watertight替代 |
| `OVERSIZE`、`UNDERSIZE`等 | 体型穿戴约束，必须核对源码；不等同装饰尺寸字符串 |
| `SINGLE_USE`、`DESTROY_ON_CHARGE_USE`等 | 动作/耗尽生命周期，不能盲目从供电物品继承 |
| `ABLATIVE_*`系列 | 插板兼容限制由口袋flag_restriction与具体flag共同决定 |

配方`recipe`、物品组`item_group`、职业`profession`、材料`material`定义是不同JSON对象；它们不是衣服可直接嵌入的同名字段。只有用户要求相应接入时才编辑。



<a id="armor-fields"></a>

## 十一、护甲槽、分区与运行时完整参考

本节是护甲字段完整参考，范围是当前工作区的 `ARMOR`、`TOOL_ARMOR` 和其他物品的 `armor_data`。普通服装、头盔、背包、饰品与防弹板均可能使用同一护甲槽；名称叫衣物还是护甲不决定加载器。依据本地源码而非在线最新版。通用物品、口袋及使用动作字段另见总文章，不能把本文表格理解成所有物品字段的替代品。

### 一、从 JSON 到运行时的路径

| 阶段 | 本地源码 | 作用 |
|---|---|---|
| 护甲类型入口 | [item_factory.cpp:2794](../../src/item_factory.cpp#L2794) | `load_armor` 先解决继承，创建/沿用 `islot_armor`，再读护甲与普通物品字段 |
| 工具兼护甲 | [item_factory.cpp:3165](../../src/item_factory.cpp#L3165) | `load_tool_armor` 同时装载工具槽和护甲槽 |
| 任意类型附护甲槽 | [item_factory.cpp:4365](../../src/item_factory.cpp#L4365) | `armor_data` 读入 `islot_armor`；放在物品顶层，内部仍使用本篇同一套护甲字段 |
| 单个材料层 | [item_factory.cpp:2859](../../src/item_factory.cpp#L2859) | `part_material::deserialize` |
| 单个防护分区 | [item_factory.cpp:2870](../../src/item_factory.cpp#L2870) | `armor_portion_data::deserialize` |
| 护甲槽整体 | [item_factory.cpp:2976](../../src/item_factory.cpp#L2976) | `islot_armor::load`，包括兼容字段下发与继承修正 |
| 完成计算 | [item_factory.cpp:798](../../src/item_factory.cpp#L798) | `finalize_post_armor`：补材质、存储累赘、分区合并、层位、刚性、透气性 |
| 定义检查 | [item_factory.cpp:1970](../../src/item_factory.cpp#L1970) | 重复部位、超限覆盖、悬挂子部位、材料覆盖、片厚约束 |
| 运行时 | `src/item.cpp`、`src/character_attire.cpp`、`src/character_armor.cpp` | 根据角色、合身、实际装载、命中部位和随机材料层计算，不能仅凭原始 JSON 值解释最终结果 |

源代码行号只是本次定位锚点；修改源码后应以函数名重新搜索。内部 `islot_armor::sub_data` 对应输入的 `armor` 数组；`data` 是完成阶段按主身体部位汇总的缓存。JSON 不应编写 `sub_data`、`data`、`all_layers` 等 C++ 缓存成员。

### 二、护甲槽整体字段

这里“槽顶层”对 `ARMOR` 是物品顶层，对 `armor_data` 路径是该对象内部；普通物品 `material`、`weight`、`flags` 等仍留在物品顶层。

| 字段 | JSON 类型、默认值 | 用法、继承与边界 |
|---|---|---|
| `armor` | 分区对象数组；新槽初始为空 | 每个对象使用第三节字段。新定义应写足分区；子类直接重写数组按整体重定义理解，不能假定以身体部位ID自动深度合并。`extend`/`delete` 的通用容器语义也不能替代“按主部位精确覆盖修改”。修改其中一个分区时先检查父类完整数组。 |
| `sided` | 布尔；`false` | 单侧装备，可由玩家切换左右。输入通常同时列出左右对应部位，运行时只启用当前一侧；不是“一对护具”。两只都要保护应生成/穿戴两件单侧物品，或选择明确的双侧一件模型，不能仅靠中文名称判断。源码 `src/item.cpp:1076`、`:1157`、`:6293`。 |
| `warmth` | 整数；`0` | 衣物保暖度；是相对保暖参数，不是摄氏度，也不是 mm。槽整体字段，分区未读取 `warmth`。一个衣体的袖和身厚度不同不表示可以在 `armor[]` 中直接独立写暖度。 |
| `weight_capacity_modifier` | 数字；`1.0` | 修改基础负重能力的因子；不是物品自重乘数，也不是口袋容积。效果由穿戴负重计算使用。 |
| `weight_capacity_bonus` | 质量字符串；`"0 g"` | 负重能力的加值，可为负，例如 `"2 kg"`；不会改变自重与防护。应与通用 `weight` 区分。源码 `src/item.cpp:8052`、`:8061`。 |
| `power_armor` | 布尔；`false` | 标记动力甲类，影响特殊穿戴与配套检查；不是“非常坚硬”的普通甲开关。中世纪钢甲不应因防护强而设置。 |
| `non_functional` | 物品 ID 字符串；空 ID | 毁坏后转换目标，当前用于 ablative 附加护甲路径；不是所有衣物损坏都会自动转成这里指定的残骸。目标必须存在。`src/character_armor.cpp:312`–`:340`。 |
| `damage_verb` | 翻译文本；空 | 上述失效转换的反馈动词/短语；为空时该路径默认使用 `is shattered`。不是防具受任何伤害时都触发的通用效果。 |
| `valid_mods` | 字符串数组；空 | 白名单允许的 `clothing_mod` ID。仅受限服装改造需要列入；不负责创建或安装改造，也不等同所有物品模组兼容列表。 |
| `covers` | 身体部位字符串或数组；未指定时无顶层覆盖修正 | 兼容性整体覆写：下发到每个 `armor` 分区的主部位集合。新写内容优先在每个分区明确 `covers`；顶层字段会让本来不同覆盖的所有分区获得同一个集合。也不会自动为旧 `specifically_covers` 重建正确子部位。 |
| `material_thickness` | 数字；私有兼容值初始 `0.0` | 整体材料平均厚度的旧式/兼容参数，下发到分区 `avg_thickness`；不是额外一层钢板。显式分区材料层的 `thickness` 才是新写内容的主要入口，后续重新计算可能覆盖 `avg_thickness`。 |
| `environmental_protection` | 整数；兼容值初始 `0` | 整体环境保护，作用于环境抗性路径；不是普通斩刺钝伤害抗性。使用槽顶层可避免分区值被整体下发覆盖。 |
| `environmental_protection_with_filter` | 整数；兼容值初始 `0` | 装有滤芯时的环境保护候选，需对应 GASMASK/DIVE_TANK 等实现配合；设置数字本身不创建滤芯槽或自动启动滤芯效果。 |

**兼容下发的实际细节**：`islot_armor` 的 `_material_thickness`、`_env_resist`、`_env_resist_w_filter` 是初始即含零的 `std::optional`，不是空 optional（`src/itype.h:467`）。加载器对每个分区执行 `apply_optional`。因此不能按直觉认定“不写槽顶层字段，分区同名值就一定原样保留”；环境值尤其应在槽整体明确填写。显式材料厚度会在完成阶段重算平均厚度，但分区环境值没有同样的重算。这里记录实现现状，不为它增加额外兼容层。

### 三、`armor[]` 每个防护分区的全部直接字段

加载器的新分区字段读取一律以 `was_loaded=false` 处理；继承的是分区容器，不是按分区内部字段逐一合并继承。

| 字段 | 类型、默认值 | 详细语义及约束 |
|---|---|---|
| `covers` | 字符串或字符串数组；**每个分区必须存在且类型可读** | 当前 `assign_coverage_from_json` 直接转成身体部位ID集合。常用 `torso`、`head`、`eyes`、`mouth`、`arm_l/r`、`hand_l/r`、`leg_l/r`、`foot_l/r`。必须查询本地身体部位定义；不要复制旧手册中的 `ARM_EITHER` 等大写旧名称。源码 `src/item_factory.cpp:174`。空数组能被语法读取不表示有实用覆盖。 |
| `specifically_covers` | 子部位 ID 数组；空 | 指定分区覆盖的精细子部位。若空，加载器自动填入主部位下所有**非 secondary**子部位。不是默认包含悬挂裙片等所有子部位。必须与主 `covers` 对应，不得用上胸/下胸名称假装前胸/后背。 |
| `coverage` | 整数百分数；`0` | 对本分区可覆盖区域的基础命中护甲概率。整体主部位显示还会按子部位 `max_coverage` 缩放。不是金属厚度，也不是盔甲套装的全身覆盖率。通常0–100；定义检查明确拒绝超过100，内容应避免负数。 |
| `cover_melee` | 整数百分数；等于 `coverage` | 近战专用物理伤害的覆盖率。是否算该类由伤害类型 `physical`、`melee_only` 决定，不是简单根据攻击者手里拿什么。 |
| `cover_ranged` | 整数百分数；等于 `coverage` | 其余 physical 伤害采用的覆盖率。不要把它当成“所有子弹必然命中”的命中加成。若写了该字段或 `cover_melee` 而基础 `coverage=0`，定义检查会告警。 |
| `cover_vitals` | 整数百分数；`0` | 要害/暴击增量抑制，由穿戴装备的该值累计并钳制0–100转换为暴击系数；不是额外普通伤害减免。`Creature::get_crit_factor`（`src/creature.cpp:725`）返回 `1-total_cover/100`。100意味着消除对应暴击增量，不是免疫攻击。 |
| `encumbrance` | 整数，或恰当的两个整数数组 `[基础,满载]`；基础`0`、满载内部初始`-1` | 基础是未合身值；数组两项分别空载与满载累赘。整数时满载由非刚性口袋容量自动生成。数组不是“左臂、右臂”两项，也不是随机区间。加载器读取索引0、1；不要写长度不够的数组。 |
| `encumbrance_modifiers` | 枚举字符串数组；空 | 存在数组时**优先于** `encumbrance`，即使两者都写也不会优先采用固定值。取 `NONE`、`IMBALANCED`、`RESTRICTS_NECK`、`WELL_SUPPORTED`。根据整件重量及身体部位的重量—累赘插值表计算；当前文档定位头部装备，其他部位无相应曲线不能直接推广。 |
| `volume_encumber_modifier` | 数字；`1` | 自动最大累赘的体积系数，也用于运行时额外口袋/背挂物体积影响；与每个口袋同名字段相乘，不是择一覆盖。基准每250ml非刚性容积加1累赘，0.25即约每1000ml加1。不是重量或容量本身。 |
| `material` | 材料对象数组；缺省为空 | 第四节的精细防护材料层。缺省时完成阶段从物品顶层材料与 `material_thickness` 推导；不等于无材料防护。仍兼容字符串/字符串数组旧写法，但新内容不推荐。 |
| `material_thickness` | 数字；`0.0` | 分区旧式平均厚度，近似mm。经槽顶层兼容下发及显式材料层重新计算后可能改变；新写多材质分区应逐层写 `material[].thickness`。 |
| `environmental_protection` | 整数；`0` | 分区环境保护存储值，但随后槽整体兼容字段会下发，见第二节。不要仅看分区反序列化就认定最终值。 |
| `environmental_protection_with_filter` | 整数；`0` | 同上，对应滤芯环境保护值；并不自动创建呼吸器。 |
| `breathability` | 枚举字符串；未指定时内部`-1`，完成阶段推导 | `IMPERMEABLE=0`、`POOR=30`、`AVERAGE=50`、`GOOD=80`、`MOISTURE_WICKING=110`、`SECOND_SKIN=140`。这是游戏透气/排湿评级，超过100合法；不是材料密度或防水率。显式写入会覆盖材料推导。源码 `src/material.cpp:300`。 |
| `layers` | 层级枚举数组；空 | 指定该分区占用层位。合法枚举 `PERSONAL`、`SKINTIGHT`、`NORMAL`、`WAIST`、`OUTER`、`BELTED`、`AURA`。空时取物品层位flags，物品没有这些flags时回退 `NORMAL`。多项表示同时占多层，不是可以任意选择其中一层。`WAIST`枚举仍可读，但已弃用，新内容按 `BELTED`＋`torso_waist`。 |
| `rigid_layer_only` | 布尔；`false` | 限制刚性穿戴冲突只检查相同层。**不是把软衣变硬的开关**；最终刚性查询必须成立才有作用；除材料缓存外，顶层`HARD`/`SOFT`还可覆盖刚性结果。材料派生的刚性缓存还要求位于传统服装层之一，见本参考第六节。 |

#### 描述符如何变成累赘

`src/itype.cpp:340` 用覆盖主部位的 `encumbrance_per_weight` 曲线对**整件物品重量**插值，而非给各部件自动分配重量。`NONE`不加修正；`IMBALANCED`与`RESTRICTS_NECK`各加10；`WELL_SUPPORTED`对基数减20%。多个乘法描述符以百分数增量累计，再算平修正；最终至少1。若插值无法找到边界，产生debug并返回100，不应依赖此回退设计装备。`VARSIZE`物品在完成阶段将生成值变为 `min(e*2,e+10)`，配合合身后的修正，而非直接把描述符计算结果当角色最终累赘。

### 四、`armor[].material[]` 材料层字段

| 字段 | 类型与默认 | 约束与用途 |
|---|---|---|
| `type` | 材料ID字符串；**必填** | 引用 `material` 类型定义，不是护甲形制或物品ID。需要确认ID存在、材料抗性、soft/uncomfortable、breathability及sheet_thickness。 |
| `covered_by_mat` | 整数百分数；`100` | 每个分区被此材料遮护的比例。加载时必须1–100，不能写0来“禁用”一层；要去掉应删该层。每个分区至少一层必须100，稀疏主防护可降低该区总coverage，并配连续衬布。多个材料各100合法，不要求合计100。 |
| `thickness` | 数字；`0.0` | 该层净厚，近似mm；不是质量占比。不同材料的厚度各自参与防护；不是所有材料共享的总厚。值必须符合对应材料 `sheet_thickness` 的整数倍约束（浮点余量约0.01），除非明确豁免。 |
| `ignore_sheet_thickness` | 布尔；`false` | 只跳过该材料层片厚倍数检查，不会让厚度消失、改变材料抗性或让错误ID有效。正确为 `true`，不是字符串 `"true"`。只有确有建模理由才用，不作为批量屏蔽警告。 |

`covered_by_mat`与 `coverage` 不同：先判定攻击是否击中该护甲分区，再对每个材料层判定是否击中。`src/character_armor.cpp:231` 护甲覆盖检查通过后，以 `-1` 调用防护计算；`src/item.cpp:8764` 对每材料独立抽0–99，命中才加 `材料抗性×厚度`。因此钢层15%不是每次提供15%的钢板抗性，而是存在有钢/无钢的随机结果。连续布层100%始终参与。平均值/UI统计不能代替单次命中语义。

顶层 `material` 描述整件物品组成（维修、燃烧、一般材质等）；分区 `material` 描述命中防护，二者作用不同。当前完成阶段在顶层材料为空时也会从护甲材料反推一个近似总体组成，所以“必须两处永远重复”不是加载器硬性要求；为了明确整件组成，正常编辑仍应检查两者一致。不要把顶层 `portion` 质量/组成权重直接搬进 `covered_by_mat`。

### 五、继承与材料替换

#### 1. 一般继承

`copy-from`先得到父定义，再由子字段修改；`armor`显式数组不是按 `covers` 或子部位ID合并的字典。子类只改衣名、价格、重量而不重写 `armor` 时，可沿用父分区。若新形制覆盖不同，必须重查所有父分区、父flags、口袋与附加防具限制，不能只改描述文字。

`relative`和`proportional`在护甲槽整体有特定实现：

| 键 | `relative` | `proportional` | 边界 |
|---|---|---|---|
| `material_thickness` | 加到兼容整体值 | 乘兼容整体值 | 不会逐一修改显式分区材料的 `thickness`；完成计算仍可能从那些材料重算平均厚度 |
| `environmental_protection` | 加环境值 | 乘环境值 | 整体下发所有分区；整数转换可能截断 |
| `environmental_protection_with_filter` | 同上 | 同上 | 不会改变滤芯耗量 |
| `encumbrance` | 已定义正基础/最大值加修正 | 再乘因子 | 顺序加后乘，结果钳制至少0。只处理大于0的分区数值，0基础不会因为relative自动变非零；没有直接把每层材料改厚或改重。 |

不应将以上例子推广成“任意字段都支持任何相对操作”；必须查该字段实际load函数。

#### 2. `replace_materials`

位于物品顶层的对象，例如 `"replace_materials": { "lc_steel": "mc_steel" }`。源码 `src/item_factory.cpp:4018`、`:4427`执行：替换顶层材质，已设置的 `repairs_with`也同步替换；按该材料在总体中的占比与新旧密度比调整物品自重；同时替换所有护甲分区的匹配材料ID。**不会自动按新材料重设计厚度、覆盖率或手工基础累赘**。自重变动又可能影响重量描述符累赘，故必须复核。若总体材料里根本没有该旧ID，则不能假定密度调整会按分区几何精确计算。

### 六、完成阶段及运行时容易混淆的行为

#### 1. 子部位是几何区域，不是另一种总覆盖率

`armor_portion_data::max_coverage`（`src/itype.cpp:294`）把匹配子部位的 `max_coverage`权重相加，primary与secondary两组取较大值；无子部位定义的主部位按100处理。完成阶段将分区coverage按此比例映射到主部位。只遮胫骨的100%分区不是整条腿100%，没有对应关系的子部位也不会凭名字获得覆盖。

同一物品的多个分区应避免重复覆盖同一个子部位；检查器会告警。不要通过复制两个完全相同的torso分区模拟“两层甲”，应在同一分区材料列表表达层结构。不同子部位但同主部位的分区会按实现汇总：累赘相加、coverage按权重累加、平均厚度和环境保护按权重处理，不能只看一行局部值估计整体累赘。

`secondary`悬挂部位仅应位于 `BELTED`；当前原版gambeson裙摆就对 `leg_draped_l/r`显式使用BELTED，而衣体仍为NORMAL＋OUTER。出处 `data/json/items/armor/gambesons.json:40`。这是原版数据结构实例，不代表本模组的层位设计必须照抄。

#### 2. 刚性与舒适性：材料推导与物品标志

`finalize_post_armor`中，对覆盖超过40%的材料，非soft材料令分区rigid，soft材料可令comfortable，但材料uncomfortable又可令其不舒适。恰好40不是“大于40”。这些是缓存，不直接从 `armor[].rigid`读取。只有占 `SKINTIGHT`、`NORMAL`、`OUTER`中至少一层的分区才保留刚性；其他层会清除此刚性缓存。因此不能为避穿戴冲突把板甲改成BELTED，这会改变实际模型。

材料缓存不是最后一步。运行时`item::is_rigid`、`is_bp_rigid`与`is_bp_rigid_selective`先检查物品标志：`SOFT`令刚性分量为假，`HARD`令刚性分量为真；都没有时才用材料缓存。`is_bp_rigid_selective`还要求存在对应分区且该区启用`rigid_layer_only`，并不是加HARD就自动开启同层选择检查。`is_rigid`与`is_bp_rigid`在没有标志覆盖且存在附加甲时，还会检查相应附加甲路径。两者同时存在时当前代码先处理SOFT，不应通过同时加两个标志来“折中”。因此“其他层清除材料刚性缓存”不等于“任何带HARD的物品都会失去刚性”。

舒适性查询`item::is_comfortable`也有覆盖：SOFT、PADDED或NO_WEAR_EFFECT可直接给出舒适结果，HARD则给出不舒适结果，其后才查分区缓存。上述函数见`src/item.cpp:14129`起。

`rigid_layer_only`改变刚性冲突比较范围而不制造刚性；`HARD`可提供查询所需刚性，不要求必须从材料派生。不同子部位、同层叠穿惩罚、刚性穿戴限制是相关但不同的检查，不可合并成“同层不能穿两件”。

#### 3. 层位与累赘

分区layers优先；空分区取物品flags中的所有层位，没有层位flag则NORMAL。物品级 `all_layers`会收集局部layers用于整体查询。多层衣物可以同时占NORMAL和OUTER，不能把它解释为运行时任选一个空层。

`src/character_attire.cpp:785`开始的 `layer_item`先累计各件 `get_encumber`，每件分层贡献钳制2–10，再按子部位重叠及穿序增加叠穿罚。PERSONAL、SEMITANGIBLE有特殊处理。普通两件单层重叠装备的额外罚不是“总累赘翻倍”；逆序穿着也会影响层位罚。物品分区基础值、角色实际单件值、全套最终值必须分别记录。

`src/item.cpp:8131`的 `get_encumber`考虑实际非刚性口袋装载比例、额外口袋和ablative附甲；FIT＋VARSIZE才应用 `max(e/2,e-10)`的合身减免。还会继续处理体型和其他状态。固定值不自动由重量推导，重量变了但encumbrance没变不等于加载错误。

自动满载值：`基础累赘 + Σ(非刚性口袋容积×该口袋体积系数) ×分区体积系数 / 250ml`，整数字段最终截断。运行时则用当前装载比例插值并向上取整；显式 `[基础,满载]`取代自动默认，但附加口袋等仍可能增加。总物品 `volume`不等于口袋可装载容积。

#### 4. 透气性和保暖不是同一件事

没写分区breathability时，完成阶段将材料按透气性由差到好排序，先计最差材料覆盖，再补更好材料的额外覆盖，未遮盖部分按100%处理。不是各材料透气性的简单算术平均；多层织物同为100%时先起作用的是最差的层。warmth则来自护甲槽整体，不会由钢厚、羊毛占比或breathability自动得到一个历史正确温度。

#### 5. 环境保护与物理保护

`item::_resist`（`src/item.cpp:8739`）在伤害类型env为真时转入 `_environmental_resist`；通常物理防护由命中材料的抗性×厚度累加，缺少专门抗性时可从damage_type的derived_from派生，再叠加服装改造与损坏系数。并非JSON写了stab就必有独立全套数值，也不能假定material中没有stab就完全不抗刺。

`get_env_resist`（`src/item.cpp:8070`）取基础平均环境值、实例滤芯覆盖变量和调用覆写的最大值，再乘相对完好程度。`environmental_protection=10`不是“减10钝伤”，滤芯值也不会未经使用动作逻辑就自动覆盖一切。

#### 6. Ablative不是把另一件甲无条件套进去

附加护甲需要正确的口袋及物品限制，内装板也有自己的coverage、层位、累赘和失效路径。先决定一件甲是独立穿戴，还是放进承载衣的附件；两种结构不是同一机制。

当前`finalize_post_armor`（`src/item_factory.cpp:1239`起）遍历口袋生成`ablative`、`additional_pocket_enc`、`ripoff_chance`、`noisy`等缓存，但遇到第一个`ablative`口袋后设置标记并立即`break`。因此该口袋自身及它之后口袋的`extra_encumbrance`、`ripoff`、`activity_noise`不再参与这一次缓存汇总，不能把数组顺序当作无关细节。

实际运行时，额外口袋累赘还受`has_additional_encumbrance()`门控（`src/item.cpp:8172`），移动口袋噪声受`has_noisy_pockets()`门控（`src/character_attire.cpp:2588`）。若前面普通口袋已启用相应缓存，运行时可能继续遍历后面的口袋；若没有，就可能跳过对应处理。编辑混合插板/储物衣时，需要检查实际缓存与消费者，不应仅凭某口袋JSON写了参数就断言已生效。第一部分普通储物背心没有ablative口袋，不涉及此提前终止。

### 七、与本地官方文档的差异

本地 `doc/JSON_INFO.md:3587`之后的Armor章节可作索引，但其中示例有混用旧写法的部分，不能逐字复制后就认定可用。

| 文档或常见旧写法 | 当前源码核查结论 | 编辑方式 |
|---|---|---|
| 把 `coverage`、`cover_melee`、`encumbrance`放槽顶层 | 当前 `islot_armor::load`不直接读这些顶层普通键；读的是分区里的值 | 写进 `armor[]`对象 |
| 顶层或分区 `max_encumbrance` | 没有该字段的直接读取；满载来自encumbrance两项数组 | 写 `"encumbrance": [2,8]`或使用体积系数 |
| `armor[].activity_noise` | 分区load没有该字段；活动噪音是口袋机制的字段 | 有对应口袋需求时写入正确口袋对象，不放护甲分区 |
| `ignore_sheet_thickness: "true"` | 当前读取布尔值 | 使用 `true` |
| `rigid_layer_only`让分区必然刚性 | 实际只限制已有刚性的冲突层 | 先核SOFT/HARD覆盖，再核材料soft/覆盖/层位 |
| covered_by_mat使每次抗性固定按比例缩放 | 实际每材料独立随机命中；统计平均与单次结果不同 | 说明连续衬层与随机加固层，检查每区至少一材100 |
| 泛称 `WAIST`为正常新内容层 | 仍可解析但定义检查提示弃用 | 新内容用BELTED＋torso_waist |
| 顶层通用to_hit是穿戴攻击减值 | 通用物品近战命中不是自动转给角色手持另一武器 | 穿戴动作影响通过实际累赘等机制设计 |

### 八、两种结构示例与检查点

以下为只展示护甲结构的**JSON片段**，不是可直接装载的完整物品；缺少完整物品的ID、名称、重量、体积等顶层字段。

#### 1. 同一件衣物，胸背与双臂分别给材料

```json
{
  "warmth": 15,
  "environmental_protection": 1,
  "flags": [ "VARSIZE", "NORMAL" ],
  "armor": [
    {
      "covers": [ "torso" ],
      "coverage": 95,
      "encumbrance": 6,
      "material": [ { "type": "cotton", "covered_by_mat": 100, "thickness": 1.0 } ]
    },
    {
      "covers": [ "arm_l", "arm_r" ],
      "coverage": 95,
      "encumbrance": 4,
      "material": [ { "type": "cotton", "covered_by_mat": 100, "thickness": 0.6 } ]
    }
  ]
}
```

这里两个分区仍是一件衣服，双臂分区相同定义应用于两臂，不是把4分摊成左右各2。没有列specifically_covers时按主部位非secondary子部位填充；不获得手套防护。

#### 2. 同一分区连续衬布与稀疏加固层

```json
{
  "covers": [ "torso" ],
  "coverage": 95,
  "encumbrance": [ 3, 7 ],
  "layers": [ "OUTER" ],
  "material": [
    { "type": "cotton", "covered_by_mat": 100, "thickness": 0.4 },
    { "type": "leather", "covered_by_mat": 30, "thickness": 1.0 }
  ]
}
```

此分区基础护甲命中率95%，命中护甲后棉始终参与，皮层30%概率参与。0.4mm棉与1mm皮不代表同一材料1.4mm，更不代表物品质量或容积由这里自动精确生成。参数仅演示语义，不作为历史防护定值。

真实原版结构可核对：`data/json/items/armor/gambesons.json:1`衣体/袖/悬挂裙三分区；`data/json/items/armor/brigandine.json:20`钢与canvas并层；`data/json/items/armor/arms_armor.json:1303`单侧装备。原版参数是实现例，不自动成为本模组平衡或历史证据。

### 九、PET_ARMOR范围边界

宠物甲不是人的 `armor[]`分区同义词。`src/item_factory.cpp:2813`和`:3048`加载独立 `islot_pet_armor`：`material_thickness`（数字0）、`max_pet_vol`/`min_pet_vol`（体积字符串0ml）、`pet_bodytype`（字符串）、`environmental_protection`/`environmental_protection_with_filter`（整数0）、`power_armor`（布尔false）。它有独立身体类型与宠物体积适配，不能用人类torso/arm子部位结构代替。其他物品也可通过顶层 `pet_armor_data`赋该槽；完整宠物使用流程超出人体衣物编辑范围。


<a id="field-inventory"></a>

## 十二、全部原版现用字段与实例清单

本节是服装编写调查的逐字段统计清单。它回答“当前原版穿戴定义实际写了哪些键”，不把观测出现次数当作引擎必填规则，也不替代加载器支持字段的说明。

### 统计范围与识别方法

扫描 `data/json/**/*.json`，不扫描 `data/mods`。仅收集引擎物品类型（ARMOR、TOOL_ARMOR、GENERIC、TOOL、GUN、GUNMOD、MAGAZINE、COMESTIBLE、AMMO、BOOK、BIONIC_ITEM、TOOLMOD、ENGINE、WHEEL、PET_ARMOR、BATTERY）的顶层定义；不把 recipe、uncraft 等自己的 copy-from 当成物品继承。直接具备 ARMOR、TOOL_ARMOR 类型或 armor_data 槽者为种子，再沿 copy-from 递归识别继承穿戴槽的物品；PET_ARMOR自身不是人类穿戴槽，只有满足上述规则才计入。包括不可生成的 abstract，包含激活态与停用态分别定义。

没有展开继承后再重复计数：顶层出现次数是原始定义中显式写出该键的定义数；嵌套路径次数是该路径出现的键次数，同一个定义的多口袋、多分区可以贡献多次。数组位置统一写 `[]`，动态字典键保留原名，所以ammo_restriction.9mm等是数据ID，不是新增固定schema字段。下文清单不包含只在源码支持、当前原版没有使用的字段。

识别依据：`src/item_factory.cpp:2794`（ARMOR）、`:3165`（TOOL_ARMOR）、`:4365`（armor_data），物品继承入口`:2536`。JSON成功解析并不等于游戏完成加载和finalize，本次未启动游戏验证。

共扫描 9581 条物品定义，识别 **2871 条人类可穿戴定义，分布在 72 个JSON文件**；观察到 **92 种顶层键、253 种嵌套字段路径**。其中 `data/json/items` 内为2829条，其余原版目录42条，均纳入下表。

| 类型 | 定义数 |
|---|---:|
| `ARMOR` | 2625 |
| `TOOL_ARMOR` | 202 |
| `GENERIC` | 20 |
| `COMESTIBLE` | 3 |
| `MAGAZINE` | 5 |
| `GUN` | 13 |
| `GUNMOD` | 3 |

GENERIC、COMESTIBLE、MAGAZINE、GUN、GUNMOD出现于本表是因为可附加或继承护甲槽，不表示编辑一件普通衣服时要填写枪械或食物属性。

<details>
<summary>展开：92种现用顶层键、用法与原版实例</summary>

### 顶层字段：全部逐项列出

基础公共字段由 `Item_factory::load_basic_info`（`src/item_factory.cpp:4077`）加载；护甲专用槽见[护甲字段详解](#armor-fields)。工具、口袋与actor属于独立子系统，不能把相似名字跨槽通用。表中注释键被保留以说明扫描完整性，它们不是游戏效果字段。

| 字段 | 显式定义数 | 用法与边界 | 一个原版例子（路径；ID） |
|---|---:|---|---|
| `//` | 286 | JSON注释；无游戏数值效果。 | `data/json/items/fluff.json`；`pom_poms` |
| `//-1` | 12 | JSON注释；无游戏数值效果。 | `data/json/items/armor/gambesons.json`；`aketon_canvas` |
| `//0` | 10 | JSON注释；无游戏数值效果。 | `data/json/items/armor/gambesons.json`；`aketon_wool` |
| `//1` | 31 | JSON注释；无游戏数值效果。 | `data/json/items/armor/gambesons.json`；`gambeson_hood` |
| `//2` | 27 | JSON注释；无游戏数值效果。 | `data/json/items/armor/ballistic_armor.json`；`steel_ballistic_plate` |
| `//3` | 20 | JSON注释；无游戏数值效果。 | `data/json/items/armor/ballistic_armor.json`；`steel_ballistic_plate` |
| `//4` | 6 | JSON注释；无游戏数值效果。 | `data/json/items/armor/gambesons.json`；`gambeson_canvas` |
| `//density` | 1 | JSON注释；无游戏数值效果。 | `data/json/items/generic/bedding.json`；`sheet` |
| `abstract` | 32 | 不可直接生成的继承模板ID，与具体id分开。 | `data/json/items/armor/arms_armor.json`；`base_chainmail_arms` |
| `ammo` | 81 | 工具/武器兼容弹种ID。 | `data/json/items/tool_armor.json`；`miner_hat` |
| `ammo_effects` | 8 | 枪械附带弹药效果ID。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `ammo_type` | 4 | 弹匣弹种。 | `data/json/items/magazine/223.json`；`belt223` |
| `armor` | 1298 | 护甲分区数组，字段详见护甲专表。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `armor_data` | 34 | 通用物品附加护甲槽对象。 | `data/json/items/generic.json`；`cigar_lit` |
| `ascii_picture` | 8 | 检查界面的ASCII图ID。 | `data/json/items/armor/eyewear.json`；`glasses_reading` |
| `capacity` | 3 | 弹匣弹容量，不是衣物口袋容量。 | `data/json/items/magazine/223.json`；`belt223` |
| `category` | 493 | 物品分类ID，影响整理而非防护。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `charged_qualities` | 1 | 工具有电时提供的品质列表。 | `data/json/items/tool/integrated.json`；`integrated_welder` |
| `charges_per_use` | 38 | 工具单次使用电荷消耗。 | `data/json/items/fake.json`；`integrated_ar` |
| `clip_size` | 8 | 枪械内置弹匣容量。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `color` | 1583 | 物品颜色枚举。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `copy-from` | 1585 | 继承的物品/抽象模板ID，跨文件查找。 | `data/json/artifact/artifact_item_types.json`；`art_robe` |
| `countdown_action` | 4 | 倒计时结束时执行的actor。 | `data/json/items/armor/exotic.json`；`migo_plate` |
| `countdown_interval` | 3 | 激活倒计时长度。 | `data/json/items/armor/exotic.json`；`migo_plate` |
| `covers` | 3 | 旧式顶层覆盖部位；现代分区宜用armor[].covers。 | `data/json/items/tool_armor.json`；`tourniquet_upper_XS` |
| `damage_verb` | 6 | 损伤/攻击显示用动词。 | `data/json/items/armor/ballistic_armor.json`；`esapi_plate` |
| `default_ammo` | 2 | 弹匣默认弹药ID。 | `data/json/items/magazine/223.json`；`belt223` |
| `delete` | 13 | 删除继承集合成员的操作对象。 | `data/json/items/tool_armor.json`；`attached_ear_plugs_off` |
| `description` | 2331 | 可翻译说明，支持翻译对象。 | `data/json/artifact/artifact_item_types.json`；`art_robe` |
| `dispersion` | 10 | 枪械散布；仅复合枪械对象有意义。 | `data/json/items/gun/9mm.json`；`briefcase_smg` |
| `durability` | 11 | 枪械耐用等级，不是通用衣物耐久倍率。 | `data/json/items/gun/flammable.json`；`flamethrower` |
| `emits` | 3 | 激活物品的场发射ID。 | `data/json/items/generic.json`；`cigar_lit` |
| `environmental_protection` | 529 | 环境阻隔值；不是物理装甲抵抗。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `environmental_protection_with_filter` | 19 | 启用过滤器时环境防护值。 | `data/json/items/tool_armor.json`；`mask_filter` |
| `extend` | 763 | 对可扩展集合追加值的继承操作对象。 | `data/json/items/tool_armor.json`；`helmet_eod_on` |
| `flags` | 1364 | 特征ID列表；具体语义由flag及消费源码决定。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `fuel_efficiency` | 1 | 工具燃料转化效率。 | `data/json/items/armor/power_armor.json`；`power_armor_generator` |
| `id` | 2839 | 物品ID；字符串或ID数组，不是显示名。 | `data/json/artifact/artifact_item_types.json`；`art_robe` |
| `install_time` | 1 | 枪械配件安装时间。 | `data/json/items/gunmod/sling.json`；`shoulder_strap_simple` |
| `integral_volume` | 1 | 装入其他物体后增加的体积。 | `data/json/items/gunmod/sling.json`；`shoulder_strap_simple` |
| `linkage` | 3 | 弹链所需链节ID。 | `data/json/items/magazine/223.json`；`belt223` |
| `location` | 1 | 枪械配件安装部位。 | `data/json/items/gunmod/sling.json`；`shoulder_strap_simple` |
| `longest_side` | 125 | 物品最长边长度，用于容纳约束。 | `data/json/items/fluff.json`；`pom_poms` |
| `looks_like` | 1229 | 图块外观参照ID；不继承统计数据。 | `data/json/items/fluff.json`；`xedra_seismograph` |
| `loudness` | 10 | 枪械响度。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `material` | 1437 | 基材字符串/列表/带portion对象列表；与armor分区material不同。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `material_thickness` | 1034 | 通用旧式材料厚度；armor分区材料可另定。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `melee_damage` | 257 | 挥舞物品的近战伤害对象，不是护甲防御。 | `data/json/items/fluff.json`；`xedra_seismograph` |
| `min_strength` | 10 | 物品使用最低力量需求；常用于弓等，不自动等同穿甲力量门槛。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `mod_targets` | 1 | 配件可安装的武器类别。 | `data/json/items/gunmod/sling.json`；`shoulder_strap_simple` |
| `modes` | 1 | 枪械开火模式。 | `data/json/items/gun/flammable.json`；`flamethrower` |
| `name` | 2871 | 可翻译名称，字符串或str/str_pl/str_sp对象。 | `data/json/artifact/artifact_item_types.json`；`art_robe` |
| `non_functional` | 6 | 附加护甲失效转换的目标物品ID，不是布尔状态。 | `data/json/items/armor/ballistic_armor.json`；`esapi_plate` |
| `pocket_data` | 473 | 口袋结构数组；容量、限制、刚性与附甲槽分别定义。 | `data/json/items/fake.json`；`integrated_ar` |
| `power_armor` | 8 | 动力装甲布尔属性。 | `data/json/items/armor/power_armor.json`；`power_armor_basic` |
| `power_draw` | 31 | 工具功耗，功率单位如W，不是能量单位。 | `data/json/items/tool_armor.json`；`miner_hat_on` |
| `price` | 1277 | 正常经济价格，价格单位/整数按加载器。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `price_postapoc` | 1332 | 灾后价格，独立于防护。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `properties` | 1 | 任意具名字符串属性映射；只有消费代码赋予效果。 | `data/json/items/armor/storage.json`；`petpack` |
| `proportional` | 769 | 按比例改继承数值；仅对应加载器支持字段有效。 | `data/json/items/tool_armor.json`；`mask_fsurvivorxs` |
| `qualities` | 24 | 工具品质及等级对列表。 | `data/json/items/tool_armor.json`；`welding_mask` |
| `range` | 12 | 枪械射程修正。 | `data/json/items/gun/flammable.json`；`flamethrower` |
| `ranged_damage` | 10 | 远程伤害对象，damage_type与amount等。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `relative` | 4 | 对继承数据做相对加减；对象结构依目标属性加载器。 | `data/json/items/armor/boots.json`；`boots_acidchitin` |
| `relic_data` | 19 | 遗物/附魔槽；穿戴被动效果不应与材料防护混算。 | `data/json/items/tool_armor.json`；`rm13_armor` |
| `reload` | 8 | 装填耗时move数。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `reload_noise_volume` | 8 | 装填声音音量。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `repairs_like` | 28 | 维修时参照其他物品ID。 | `data/json/obsoletion/obsolete_items.json`；`gambeson_loose` |
| `repairs_with` | 23 | 可用于维修的材料ID集合。 | `data/json/items/armor/arms_armor.json`；`armguard_metal` |
| `replace_materials` | 293 | 继承时替换基材的旧ID到新ID映射。 | `data/json/items/armor/arms_armor.json`；`chainmail_junk_arms` |
| `revert_to` | 59 | 电荷耗尽或状态结束的目标物品ID。 | `data/json/items/tool_armor.json`；`miner_hat_on` |
| `sided` | 94 | 左右侧选择布尔开关。 | `data/json/items/fluff.json`；`xedra_seismograph` |
| `sight_dispersion` | 9 | 瞄具散布。 | `data/json/items/gun/9mm.json`；`briefcase_smg` |
| `skill` | 8 | 枪械使用技能ID。 | `data/json/items/ranged/archery.json`；`selfbow` |
| `snippet_category` | 10 | 随机说明文本类别或内联片段。 | `data/json/items/armor/coats.json`；`jacket_jean` |
| `solar_efficiency` | 1 | 太阳能效率参数。 | `data/json/items/tool_armor.json`；`solarpack_on` |
| `symbol` | 1302 | 地图物品符号。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `techniques` | 48 | 物品作为武器时提供的技法ID集合。 | `data/json/items/tool_armor.json`；`miner_hat` |
| `tick_action` | 27 | 激活后的逐tick动作。 | `data/json/items/fake.json`；`integrated_ar` |
| `to_hit` | 655 | 当物品作为近战武器使用时的命中属性；数字或细分对象，穿着不会直接降低另一把武器命中。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `turns_per_charge` | 13 | 工具消耗一电荷的时间间隔。 | `data/json/items/tool_armor.json`；`dimensional_anchor_on` |
| `type` | 2871 | 加载器类型；ARMOR或TOOL_ARMOR之外也可通过armor_data具备穿戴槽。 | `data/json/artifact/artifact_item_types.json`；`art_robe` |
| `use_action` | 416 | 手动使用动作：名称、actor对象或混合列表。 | `data/json/items/fake.json`；`integrated_ar` |
| `valid_mod_locations` | 11 | 枪械改装位置及数量对列表。 | `data/json/items/gun/9mm.json`；`briefcase_smg` |
| `valid_mods` | 37 | 允许的clothing_mod服装改造ID白名单，不是通用工具模组。 | `data/json/obsoletion/obsolete_items.json`；`k_gambeson` |
| `variant_type` | 67 | 外观变体选项类别generic/gun，不是append描述开关。 | `data/json/items/armor/ammo_pouch.json`；`chestrig` |
| `variants` | 69 | 外观变体数组，不复制出独立基础物品。 | `data/json/items/armor/ammo_pouch.json`；`chestrig` |
| `volume` | 1342 | 外体积单位字符串，不等于口袋容量。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `warmth` | 944 | 衣物保暖值，无单位整数。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `weapon_category` | 1 | 武器类别ID，不是衣物分类。 | `data/json/items/armor/integrated.json`；`integrated_giant_pincer` |
| `weight` | 1359 | 质量单位字符串，如g/kg；继承可调整。 | `data/json/artifact/artifact_item_types.json`；`art_mask` |
| `weight_capacity_bonus` | 2 | 携重能力加成；不是物品重量。 | `data/json/items/tool_armor.json`；`utility_exoskeleton_on` |


</details>

<details>
<summary>展开：253种现用嵌套字段路径与查阅入口</summary>

### 嵌套字段：全部路径

护甲分区、基材比例、口袋、继承操作、动作actor、附魔与翻译对象均纳入。`material[].type`是材料ID，`use_action.type`是actor种类，`variants[].id`是变体ID；同名字段必须结合完整路径阅读。`extend.*`/`delete.*`/`relative.*`/`proportional.*`是继承修饰，不是独立护甲槽。

| 字段路径 | 键出现次数 | 一个原版例子（路径；ID）  用法入口（按上下文查阅） |
|---|---:|------|
| `armor[].//` | 28 | `data/json/items/tool_armor.json`；`phase_immersion_suit`  注释/翻译提取提示，不是游戏参数。 |
| `armor[].//a` | 3 | `data/json/items/armor/gambesons.json`；`gambeson_gloves_canvas`  注释/翻译提取提示，不是游戏参数。 |
| `armor[].//warmth` | 17 | `data/json/items/armor/gambesons.json`；`gambeson`  注释/翻译提取提示，不是游戏参数。 |
| `armor[].breathability` | 22 | `data/json/items/armor/helmets.json`；`helmet_football`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].cover_melee` | 37 | `data/json/items/armor/arms_armor.json`；`2byarm_guard`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].cover_ranged` | 51 | `data/json/items/armor/arms_armor.json`；`2byarm_guard`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].cover_vitals` | 105 | `data/json/items/armor/ammo_pouch.json`；`xlkevlar`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].coverage` | 2138 | `data/json/artifact/artifact_item_types.json`；`art_mask`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].covers` | 2145 | `data/json/artifact/artifact_item_types.json`；`art_mask`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].encumbrance` | 1627 | `data/json/artifact/artifact_item_types.json`；`art_mask`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].encumbrance_modifiers` | 126 | `data/json/items/tool_armor.json`；`helmet_eod`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].layers` | 73 | `data/json/items/tool_armor.json`；`helmet_eod`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].material` | 777 | `data/json/items/tool_armor.json`；`flashlight_mount_wrist`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].material[].//` | 12 | `data/json/items/armor/suits_protection.json`；`robofac_enviro_suit`  注释/翻译提取提示，不是游戏参数。 |
| `armor[].material[].covered_by_mat` | 1469 | `data/json/items/tool_armor.json`；`flashlight_mount_wrist`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].material[].ignore_sheet_thickness` | 11 | `data/json/items/tool_armor.json`；`mask_h20survivor`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].material[].thickness` | 1469 | `data/json/items/tool_armor.json`；`flashlight_mount_wrist`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].material[].type` | 1469 | `data/json/items/tool_armor.json`；`flashlight_mount_wrist`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].rigid_layer_only` | 130 | `data/json/items/tool_armor.json`；`blindfold_duct`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].specifically_covers` | 1145 | `data/json/items/generic.json`；`wallet_travel`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor[].volume_encumber_modifier` | 103 | `data/json/items/tool_armor.json`；`rm13_armor`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor` | 33 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].coverage` | 33 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].covers` | 33 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].encumbrance` | 28 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].material` | 31 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].material[].covered_by_mat` | 38 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].material[].thickness` | 38 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].material[].type` | 38 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].specifically_covers` | 26 | `data/json/items/classes/magazine.json`；`magazine_belt`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.armor[].volume_encumber_modifier` | 5 | `data/json/items/armor/storage.json`；`hide_bag`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.covers` | 1 | `data/json/items/comestibles/junkfood.json`；`candy_bracelet`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.sided` | 6 | `data/json/items/armor/storage.json`；`hide_bag`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `armor_data.warmth` | 3 | `data/json/items/generic.json`；`cigar_lit`  [护甲参考](#armor-fields)：同名分区/材料字段；armor_data内为同一槽schema。 |
| `countdown_action.explosion` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.explosion.power` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.fields_max_intensity` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.fields_min_intensity` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.fields_radius` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.fields_type` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.message` | 3 | `data/json/items/armor/exotic.json`；`migo_plate`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `countdown_action.type` | 4 | `data/json/items/armor/exotic.json`；`migo_plate`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `delete.flags` | 13 | `data/json/items/tool_armor.json`；`attached_ear_plugs_off`  集合增删操作；material须查主文材料继承例外，不能一概认为集合语义生效。 |
| `description.//NOLINT(cata-text-style)` | 2 | `data/json/items/armor/torso_clothes.json`；`santa_dress`  注释/翻译提取提示，不是游戏参数。 |
| `description.//~` | 1 | `data/json/items/tool/musical_instruments.json`；`tuba`  注释/翻译提取提示，不是游戏参数。 |
| `description.str` | 9 | `data/json/items/armor/torso_clothes.json`；`ninja_dress`  翻译文本str；其注释键仅供翻译或样式检查使用。 |
| `extend.flags` | 762 | `data/json/items/tool_armor.json`；`helmet_eod_on`  集合增删操作；material须查主文材料继承例外，不能一概认为集合语义生效。 |
| `extend.material` | 1 | `data/json/items/armor/bespoke_armor/custom_underwear.json`；`nomad_bodyglove_2`  集合增删操作；material须查主文材料继承例外，不能一概认为集合语义生效。 |
| `material[].portion` | 153 | `data/json/items/tool_armor.json`；`smart_watch`  顶层组成材料：type为材料ID、portion为相对份额；不是防护概率或mm厚度。 |
| `material[].type` | 203 | `data/json/items/tool_armor.json`；`smart_watch`  顶层组成材料：type为材料ID、portion为相对份额；不是防护概率或mm厚度。 |
| `melee_damage.bash` | 252 | `data/json/items/fluff.json`；`xedra_seismograph`  末段为伤害类型ID，数值为挥舞本物品的近战伤害，不是抗性。 |
| `melee_damage.cut` | 20 | `data/json/items/armor/arms_armor.json`；`armguard_scrap`  末段为伤害类型ID，数值为挥舞本物品的近战伤害，不是抗性。 |
| `melee_damage.stab` | 4 | `data/json/items/armor/helmets.json`；`pickelhaube`  末段为伤害类型ID，数值为挥舞本物品的近战伤害，不是抗性。 |
| `name.str` | 2661 | `data/json/artifact/artifact_item_types.json`；`art_robe`  翻译名称：str单数、str_pl复数、str_sp同形、ctxt上下文，见字段手册第二节。 |
| `name.str_pl` | 1034 | `data/json/artifact/artifact_item_types.json`；`art_gloves`  翻译名称：str单数、str_pl复数、str_sp同形、ctxt上下文，见字段手册第二节。 |
| `name.str_sp` | 189 | `data/json/items/tool_armor.json`；`rx11_stimpack`  翻译名称：str单数、str_pl复数、str_sp同形、ctxt上下文，见字段手册第二节。 |
| `pocket_data[].//` | 85 | `data/json/items/armor/ammo_pouch.json`；`load_bearing_vest_sling`  注释/翻译提取提示，不是游戏参数。 |
| `pocket_data[].ablative` | 147 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].activity_noise` | 25 | `data/json/items/armor/storage.json`；`backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].activity_noise.chance` | 25 | `data/json/items/armor/storage.json`；`backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].activity_noise.volume` | 25 | `data/json/items/armor/storage.json`；`backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].airtight` | 5 | `data/json/items/tool_armor.json`；`scuba_tank`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].ammo_restriction` | 46 | `data/json/items/tool_armor.json`；`smart_watch`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].ammo_restriction.10mm` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.123ln` | 2 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.12mm` | 1 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.20x66mm` | 5 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.22` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.223` | 4 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.270win` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.300` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.3006` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.300blk` | 2 | `data/json/items/armor/bandolier.json`；`bandolier_rifle`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.303` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.308` | 5 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.32` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.338lapua` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.357mag` | 2 | `data/json/items/armor/bandolier.json`；`bandolier_pistol`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.357sig` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.36paper` | 2 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.38` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.380` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.38super` | 2 | `data/json/items/armor/bandolier.json`；`bandolier_pistol`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.40` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.40x46mm` | 2 | `data/json/items/armor/bandolier.json`；`torso_bandolier_grenade`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.40x53mm` | 2 | `data/json/items/armor/bandolier.json`；`torso_bandolier_grenade`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.410shot` | 5 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.44` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.44paper` | 2 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.45` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.450` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.454` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.4570` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.458wm` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.45colt` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.46` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.460` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.50` | 4 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.500` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.50beowulf` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.545x39` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.57` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.762` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.762R` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.762x25` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.77mm_arisaka` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.8x40mm` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.9mm` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.9x18` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.BB` | 1 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.ampoule` | 2 | `data/json/items/tool_armor.json`；`wearable_rx12`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.arrow` | 14 | `data/json/items/armor/ammo_pouch.json`；`quiver`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.battery` | 4 | `data/json/items/tool_armor.json`；`smart_watch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.blunderbuss` | 1 | `data/json/items/armor/bandolier.json`；`flintlock_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.bolt` | 6 | `data/json/items/armor/ammo_pouch.json`；`quiver`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.diesel` | 1 | `data/json/items/armor/power_armor.json`；`power_armor_generator`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.flintlock` | 2 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.gasoline` | 1 | `data/json/items/tool_armor.json`；`ice_utility_exoskeleton_off`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.nitrox` | 4 | `data/json/items/tool_armor.json`；`scuba_tank`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.paintball` | 1 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.pebble` | 3 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.rock` | 2 | `data/json/items/armor/bandolier.json`；`stone_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.shot` | 6 | `data/json/items/armor/ammo_pouch.json`；`ammo_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.shotpaper` | 1 | `data/json/items/armor/bandolier.json`；`flintlock_pouch`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.signal_flare` | 4 | `data/json/items/armor/ammo_pouch.json`；`tacvest`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.stimpack_ammo` | 2 | `data/json/items/tool_armor.json`；`rx11_stimpack`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].ammo_restriction.strange_arrow` | 2 | `data/json/items/armor/exotic.json`；`armor_star_samurai`  [字段手册第五节](#item-fields)：末段为弹药类型ID，值是该种弹药容量，不是新schema键。 |
| `pocket_data[].default_magazine` | 46 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].description` | 398 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].extra_encumbrance` | 63 | `data/json/items/armor/storage.json`；`backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].flag_restriction` | 337 | `data/json/items/generic.json`；`wallet_travel`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].holster` | 196 | `data/json/items/armor/ammo_pouch.json`；`quiver_takedown_bow`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].inherits_flags` | 5 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].item_restriction` | 11 | `data/json/items/tool_armor.json`；`holo_cloak`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].magazine_well` | 89 | `data/json/items/armor/ammo_pouch.json`；`tacvest`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].material_restriction` | 3 | `data/json/items/tool/integrated.json`；`internal_gasoline_tank`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].max_contains_volume` | 1122 | `data/json/items/fake.json`；`integrated_ar`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].max_contains_weight` | 1112 | `data/json/items/fake.json`；`integrated_ar`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].max_item_length` | 882 | `data/json/items/generic.json`；`lanyard`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].max_item_volume` | 14 | `data/json/items/armor/storage.json`；`jerrypack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].min_item_length` | 67 | `data/json/items/armor/ammo_pouch.json`；`heavy_load_bearing_vest_breacher`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].min_item_volume` | 62 | `data/json/items/armor/ammo_pouch.json`；`javelin_bag`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].moves` | 1121 | `data/json/items/generic.json`；`wallet_travel`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].name` | 4 | `data/json/items/armor/robofac_armor.json`；`robofac_robotrig`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].pocket_type` | 1116 | `data/json/items/fake.json`；`integrated_ar`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].rigid` | 123 | `data/json/items/fake.json`；`integrated_ar`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].ripoff` | 62 | `data/json/items/armor/storage.json`；`backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].sealed_data` | 2 | `data/json/items/containers/containers.json`；`bottle_gourd`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].sealed_data.spoil_multiplier` | 2 | `data/json/items/containers/containers.json`；`bottle_gourd`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].spoil_multiplier` | 4 | `data/json/items/armor/robofac_armor.json`；`robofac_armor_rig`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].transparent` | 91 | `data/json/items/armor/ammo_pouch.json`；`belt_loop_small`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].volume_encumber_modifier` | 300 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].volume_multiplier` | 1 | `data/json/items/armor/storage.json`；`debug_backpack`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].watertight` | 43 | `data/json/items/tool_armor.json`；`scuba_tank`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `pocket_data[].weight_multiplier` | 10 | `data/json/items/fake.json`；`integrated_ar`  [字段手册第五节](#item-fields)：逐字段类型、默认、单位及弹药口袋分支；activity_noise与sealed_data分别查其子项。 |
| `properties.creature_size_capacity` | 1 | `data/json/items/armor/storage.json`；`petpack`  末段为具名静态属性；creature_size_capacity由宠物容器逻辑消费，见字段手册第三节补充。 |
| `proportional.calories` | 2 | `data/json/items/armor/storage.json`；`hide_bag`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.encumbrance` | 6 | `data/json/items/armor/arms_armor.json`；`armguard_acidchitin`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.fun` | 2 | `data/json/items/armor/storage.json`；`hide_bag`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.healthy` | 2 | `data/json/items/armor/storage.json`；`hide_bag`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.price` | 670 | `data/json/items/tool_armor.json`；`mask_fsurvivorxs`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.quench` | 2 | `data/json/items/armor/storage.json`；`hide_bag`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.volume` | 743 | `data/json/items/tool_armor.json`；`mask_fsurvivorxs`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.warmth` | 7 | `data/json/items/armor/arms_armor.json`；`armguard_acidchitin`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `proportional.weight` | 764 | `data/json/items/tool_armor.json`；`mask_fsurvivorxs`  父值乘倍率；原版出现不保证当前加载器有效，护甲encumbrance等须查参考的专用分区处理。 |
| `ranged_damage.amount` | 10 | `data/json/items/ranged/archery.json`；`selfbow`  字段手册第九节：damage_type是伤害类型、amount为伤害值，属于枪械槽。 |
| `ranged_damage.damage_type` | 10 | `data/json/items/ranged/archery.json`；`selfbow`  字段手册第九节：damage_type是伤害类型、amount为伤害值，属于枪械槽。 |
| `relative.melee_damage` | 4 | `data/json/items/armor/boots.json`；`boots_acidchitin`  相对增加/减少父值；melee_damage内按伤害类型分别修改，见字段手册第三节。 |
| `relative.melee_damage.bash` | 4 | `data/json/items/armor/boots.json`；`boots_acidchitin`  相对增加/减少父值；melee_damage内按伤害类型分别修改，见字段手册第三节。 |
| `relic_data.passive_effects` | 19 | `data/json/items/tool_armor.json`；`rm13_armor`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].condition` | 10 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].condition.not` | 4 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].has` | 10 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].id` | 15 | `data/json/items/tool_armor.json`；`rm13_armor`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].mutations` | 6 | `data/json/items/armor/suits_protection.json`；`armor_nomad_plate`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].values` | 4 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].values[].add` | 4 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `relic_data.passive_effects[].values[].value` | 4 | `data/json/items/armor/integrated.json`；`integrated_claws`  [字段手册第九节](#item-fields)：附魔条件、携带状态、属性或mutation修正。 |
| `replace_materials.ch_steel` | 1 | `data/json/items/armor/head_attachments.json`；`qt_steel_facemask`  末段是旧材料ID，值是替换材料ID；同步护甲分区并调整质量，见护甲参考。 |
| `replace_materials.lc_steel` | 147 | `data/json/items/armor/ballistic_armor.json`；`mc_esapi_plate`  末段是旧材料ID，值是替换材料ID；同步护甲分区并调整质量，见护甲参考。 |
| `replace_materials.lc_steel_chain` | 64 | `data/json/items/armor/boots.json`；`mc_chainmail_feet`  末段是旧材料ID，值是替换材料ID；同步护甲分区并调整质量，见护甲参考。 |
| `replace_materials.steel` | 125 | `data/json/items/armor/arms_armor.json`；`chainmail_junk_arms`  末段是旧材料ID，值是替换材料ID；同步护甲分区并调整质量，见护甲参考。 |
| `snippet_category[].id` | 59 | `data/json/items/armor/coats.json`；`jacket_jean`  内联片段数组：id为片段标识、text为可翻译片段正文，见字段手册第二节补充。 |
| `snippet_category[].text` | 59 | `data/json/items/armor/coats.json`；`jacket_jean`  内联片段数组：id为片段标识、text为可翻译片段正文，见字段手册第二节补充。 |
| `tick_action.description_frequency` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.fun` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.fun_bonus` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.npc_descriptions` | 6 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.player_descriptions` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.speed_penalty` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.type` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `tick_action.volume` | 7 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `to_hit.balance` | 13 | `data/json/items/tool_armor.json`；`binoculars`  字段手册第三节四个枚举维度，描述物品作为攻击武器时的命中，不是穿戴惩罚。 |
| `to_hit.grip` | 13 | `data/json/items/tool_armor.json`；`binoculars`  字段手册第三节四个枚举维度，描述物品作为攻击武器时的命中，不是穿戴惩罚。 |
| `to_hit.length` | 13 | `data/json/items/tool_armor.json`；`binoculars`  字段手册第三节四个枚举维度，描述物品作为攻击武器时的命中，不是穿戴惩罚。 |
| `to_hit.surface` | 13 | `data/json/items/tool_armor.json`；`binoculars`  字段手册第三节四个枚举维度，描述物品作为攻击武器时的命中，不是穿戴惩罚。 |
| `use_action.//` | 1 | `data/json/items/tool_armor.json`；`whistle`  注释/翻译提取提示，不是游戏参数。 |
| `use_action.active` | 39 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.ammo_scale` | 24 | `data/json/items/tool_armor.json`；`miner_hat_on`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.filthy_volume_threshold` | 2 | `data/json/items/tool_armor.json`；`gobag`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.furn_type` | 1 | `data/json/items/tool/misc.json`；`grapnel`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.group` | 2 | `data/json/items/tool_armor.json`；`gobag`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.holster_msg` | 34 | `data/json/items/armor/ammo_pouch.json`；`ammo_satchel`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.holster_prompt` | 34 | `data/json/items/armor/ammo_pouch.json`；`ammo_satchel`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.items_fit` | 1 | `data/json/items/tool_armor.json`；`personal_gobag`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.menu_text` | 226 | `data/json/items/tool_armor.json`；`tourniquet_upper`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.message` | 1 | `data/json/items/tool/explosives.json`；`mininuke_act`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.moves` | 13 | `data/json/items/tool_armor.json`；`binoculars`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.moves_slow` | 5 | `data/json/items/tool_armor.json`；`binoculars`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.msg` | 259 | `data/json/items/tool_armor.json`；`tourniquet_upper`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.need_charges` | 30 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.need_charges_msg` | 30 | `data/json/items/tool_armor.json`；`miner_hat`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.need_sunlight` | 5 | `data/json/items/tool_armor.json`；`binoculars`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.need_wielding` | 1 | `data/json/items/ranged/archery.json`；`takedown_recurbow`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.need_worn` | 6 | `data/json/items/tool_armor.json`；`foodperson_mask`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.noise` | 1 | `data/json/items/tool_armor.json`；`whistle`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.noise_id` | 1 | `data/json/items/tool_armor.json`；`whistle`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.noise_message` | 1 | `data/json/items/tool_armor.json`；`whistle`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.noise_variant` | 1 | `data/json/items/tool_armor.json`；`whistle`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.target` | 259 | `data/json/items/tool_armor.json`；`tourniquet_upper`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.type` | 325 | `data/json/items/tool_armor.json`；`tourniquet_upper`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action.use_message` | 1 | `data/json/items/tool_armor.json`；`whistle`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].active` | 7 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].ammo_scale` | 4 | `data/json/items/tool_armor.json`；`electric_blanket_on`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].cable_length` | 2 | `data/json/items/tool_armor.json`；`electric_blanket`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].charge_rate` | 2 | `data/json/items/tool_armor.json`；`electric_blanket`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].cost_scaling` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].holster_msg` | 1 | `data/json/items/armor/belts.json`；`webbing_belt`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].holster_prompt` | 1 | `data/json/items/armor/belts.json`；`webbing_belt`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].item_action_type` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].materials` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].menu_text` | 7 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].move_cost` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].moves` | 3 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].moves_slow` | 3 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].msg` | 10 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].need_charges` | 4 | `data/json/items/tool_armor.json`；`electric_blanket`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].need_charges_msg` | 4 | `data/json/items/tool_armor.json`；`electric_blanket`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].size` | 25 | `data/json/items/armor/ammo_pouch.json`；`light_load_bearing_vest`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].skill` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].target` | 10 | `data/json/items/generic.json`；`cigar_lit`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].tool_quality` | 1 | `data/json/items/tool/integrated.json`；`integrated_welder`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `use_action[].type` | 79 | `data/json/items/fluff.json`；`pom_poms`  [字段手册第七节](#item-fields)：按actor的type选择对应字段表；对象/数组写法同schema，不跨actor套用。 |
| `variants[].append` | 502 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].color` | 398 | `data/json/items/armor/ballistic_armor.json`；`ballistic_vest_esapi`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].description` | 752 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].id` | 752 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].name` | 752 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].name.str` | 718 | `data/json/items/armor/ballistic_armor.json`；`ballistic_vest_esapi`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].name.str_pl` | 155 | `data/json/items/armor/ballistic_armor.json`；`ballistic_vest_light`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].name.str_sp` | 34 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].symbol` | 27 | `data/json/items/armor/ballistic_armor.json`；`ballistic_vest_light`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |
| `variants[].weight` | 679 | `data/json/items/armor/ammo_pouch.json`；`chestrig`  [字段手册第二节](#item-fields)：外观变体逐字段表；这里weight是随机权重。 |

</details>

### 动作字段的分派边界

`use_action`支持字符串函数名与具名actor对象，数组可以混合两者。当前可穿戴定义观察到的actor/函数名如下；这只是服装子集，不能推导成所有可接受动作的白名单。

- 手动动作：`CAMERA`、`PORTABLE_GAME`、`EINKTABLETPC`、`ELECTRICSTORAGE`、`EBOOKSAVE`、`EBOOKREAD`、`play_instrument`、`firestarter`、`transform`、`unpack`、`MP3`、`CALORIES_INTAKE_TRACKER`、`FITNESS_CHECK`、`DIRECTIONAL_HOLOGRAM`、`RM13ARMOR_OFF`、`RM13ARMOR_ON`、`GASMASK_ACTIVATE`、`JET_INJECTOR`、`STIMPACK`、`RADGLOVE`、`TOWEL`、`manualnoise`、`SOLARPACK`、`SOLARPACK_OFF`、`DIVE_TANK_ACTIVATE`、`link_up`、`FOODPERSON`、`holster`、`attach_molle`、`detach_molle`、`MEDITATE`、`WEATHER_TOOL`、`CAPTURE_MONSTER_ACT`、`MININUKE`、`message`、`CROWBAR`、`repair_item`、`deploy_furn`、`WATER_PURIFIER`。
- Tick动作：`EPIC_MUSIC`、`musical_instrument`、`GASMASK`、`DIVE_TANK`、`FOODPERSON_VOICE`。
- 倒计时动作：`message`、`explosion`。

字符串函数的行为在 `src/iuse.cpp`，JSON actor的字段由 `src/iuse_actor.cpp`对应 `load` 函数决定。例如`transform.target`是目标物品，`holster.target`若存在不能未经对应actor核查套用相同含义。顶层`revert_to`与`transform.target`也不是一个字段。

### 计数解释与完整性限制

本清单是在当前工作树原版数据上的静态枚举；未包含模组、存档实例JSON、物品组、配方、迁移表与单独的材料/flag/附魔定义。不存在于定义自身的继承属性不进入它的显式次数，但只要该字段在任何一个选中祖先/具体定义出现，就会被列入。数组ID定义按一条定义统计，不按展开后ID数统计。它用于定位现用字段和例子；引擎字段支持范围、默认值和运行时消费仍以主文及源码核对为准。


<a id="editing-skill"></a>

# 第三部分：源码驱动的服装 JSON 编辑 Skill

## 一、可调用的技能

本次创建的可发现技能名为 **`cdda-clothing-json`**，入口为[SKILL.md](C:/Users/Administrator/.codex/skills/cdda-clothing-json/SKILL.md)。其用途是编辑当前仓库的服装JSON：读取本篇与字段参考、确认穿戴单位与继承、按源码支持的结构编辑，并执行对应验证。这里说明它依赖的实际执行逻辑；技能入口不复制整份字段手册。

## 二、编辑前确定五件事

1. **对象边界**：一个物品是一件可穿脱装备，还是状态变体；组合清单不是另外一件重复套装。历史同套关系不能用copy-from表达。
2. **父链**：展开copy-from，确认护甲槽、材料、口袋、flag、动作和供电是否继承；不要仅看子文件几行。
3. **空间**：将历史前后/左右覆盖转换为当前已注册body_part/sub_body_part，先查[data/json/body_parts.json](../../data/json/body_parts.json)及相关子部位定义；当前上下躯干并非前胸后背方向。
4. **量纲**：本体重量、收纳体积、板厚、材料覆盖概率、衣物覆盖、口袋容量、累赘分别定量；锁环几何与游戏等效厚度不能互换。
5. **调用链**：字段在哪里load、finalize如何推导、运行时谁消费。只看到结构体成员不足以证明JSON可写。

## 三、按源码实现的顺序编辑

先选最接近的现有服装原型，再决定ARMOR或TOOL_ARMOR；确需其他主类型才用armor_data。身份与翻译名先写，再处理自重、体积和顶层组成，随后按实际覆盖分armor区段；每区写明确材料概率、厚度、累赘和层位。材料或区域变化时必须重新核对全件重量，不通过随意调整coverage来解释少一片肩甲。

口袋按真实功能添加。普通甲不要顺手继承背包容量；附加甲口袋不是普通储物袋，ablative会强制单件并改变防护路径。可切换状态检查两向target、层位、覆盖、口袋、供电和物品ID引用是否对应。修改flags时使用正确的替换或集合增删语义。

源码依据至少核对：`load_definition → 专属slot load → load_basic_info → finalize`，以及[item.cpp](../../src/item.cpp)、[character_attire.cpp](../../src/character_attire.cpp)、[character_armor.cpp](../../src/character_armor.cpp)中的实际消费者。不要把上游网页文档当本地版本行为。

## 四、验证与交付边界

- JSON语法解析只证明格式正确；随后检查引用存在、嵌套位置与字段类型，再用当前构建对应的游戏加载校验，观察debug日志的未读字段与一致性错误。
- 本地`main.cpp:310`定义`--jsonverify`；`--check-mods`接受mod ID列表。调用时先确认可执行文件与本源码匹配、实际mod ID及运行目录；不要凭目录名猜ID。
- 格式化使用项目`tools/format`对应可用工具，核对差异范围；不为文档任务自动改全库JSON。
- 涉及覆盖、刚性冲突、叠穿、口袋累赘、变形或插板时，还需验证对应穿戴/装填/受击行为。仅加载通过不能证明平衡正确。
- 代码/JSON实际编辑后依AGENTS维护对应Process；本次文档与技能编写本身不产生游戏实现进度。

交付应明确改了哪些字段、继承结果、验证实际执行情况与尚未验证的行为。遇到该分支不存在的字段，说明缺口；不要静默造兼容字段或扩展C++。
