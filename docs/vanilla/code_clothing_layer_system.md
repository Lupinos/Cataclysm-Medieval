# CDDA 穿衣分层与叠穿累赘

## 范围与入口

本文核对当前仓库原版代码中的穿衣机制，作为设计与技术方案的参考，不代表中世纪模组已实现。相关文件：`src/character_attire.cpp`、`src/character.cpp`、`src/bodypart.cpp`、`src/item_factory.cpp`、`src/melee.cpp`、`tests/encumbrance_test.cpp`。

## 同层冲突与计算

`outfit::item_encumb()` 按穿着顺序调用 `layer_item()`。后者根据大部位取得物品实际累赘，再检查其覆盖的子部位和层位。

- 每件装备的基础累赘始终累加。
- 普通物品用于层位计算的值为 `clamp(实际累赘, 2, 10)`；这是叠穿计算的贡献值，不是物品自身累赘的上限。
- 同层子部位重叠由 `encumbrance_data::add_sub_location()` 检测。不同层穿反顺序也会引发惩罚；不同层按序穿着不因此免除基础累赘。
- `layer_details::layer()` 累加各件的层位贡献并扣除其中最大值。仅当该层存在冲突时，`item_encumb()` 才把该层结果计入部位总累赘。
- 对只有两件、单一层、覆盖相同子部位的普通物品，额外值为两件裁剪后贡献的较小值。例：实际累赘分别为 4、12，基础合计 16，额外 4，总计 20；若二者均为 12，则总计 24＋10＝34。
- 多部位、多层和多个不完全重叠物品应走完整算法，不能把上述双物品简式扩展为所有组合的通用公式。
- `SEMITANGIBLE`、`PERSONAL` 等有特例；普通织物与金属甲不应借这些标志逃避叠穿成本。

已有 `tests/encumbrance_test.cpp` 的 `same_layer_encumbrance`、`separate_layer_encumbrance`、`out_of_order_encumbrance` 覆盖同层、跨层和穿反顺序的行为。本轮做代码与数据静态核对，未声称已执行这些 C++ 测试。

## 层位、覆盖与穿戴限制

层位默认回落到 NORMAL；物品可占多层，分部位条目也可覆盖全局层位。层位以实际 `get_layer()` 结果为准，不能只按物品名称推断。

同一大部位不必冲突：肩甲与只覆盖前臂的护甲可以因子部位不重叠而共存。覆盖率百分比不是另一件甲能否共存的直接判断依据。`check_rigid_conflicts()` 和 `rigid_test()` 还会检查刚性件重叠；部分刚性件限制跨层也存在，`rigid_layer_only` 可改变检查范围。因此“不同层没有叠穿罚”不等于“一定允许穿上”。

`torso_upper` 与 `torso_lower` 是上下躯干子部位，不是正面和背面的方向模型；不能靠上下部位的厚度差自动获得正面独占防护。

## 当前数据参照

| 原版条目 | 当前数据 | 含义 |
| --- | --- | --- |
| `gambeson`（`data/json/items/armor/gambesons.json`） | 重 11850 g；全局 NORMAL＋OUTER；躯干累赘 20、手臂 25；裙摆另指定 BELTED | 描述明确定位为独立厚布甲，不适合直接作为轻薄甲下垫衣模板；裙摆层位不能推广为整件金属甲都应外挂 |
| `armor_lc_brigandine`（`data/json/items/armor/brigandine.json`） | OUTER；重 6873 g；躯干累赘 12、覆盖 95%；钢 1.0 mm、帆布 2.0 mm | 可作同口径比较的原版基准，不代表模组应照搬这些值 |
| `base_chainmail_vest` / `base_chainmail_hauberk`（`torso_armor.json` / `suits_protection.json`） | 锁甲基类是 OUTER，hauberk 继承该层；基类包含允许特定外甲的 ablative 口袋 | 原版并不是所有锁甲都走 NORMAL；口袋中的附加护甲与单独穿两件衣物不是同一条计算路径 |
| `armor_cuirass`（`data/json/items/armor/torso_armor.json`） | OUTER；重 5896 g；躯干累赘 15、覆盖 90% | 胸背甲使用外层的直接参照 |

原版锁甲通过口袋的 `flag_restriction` 限定可附加外甲，部分布里根丁带 `ABLATIVE_CHAINMAIL_TORSO` 标志；不可推断任意甲都可组合或完全没有代价。`item::get_layer()`、`get_encumber()` 也处理附加护甲，技术方案必须核对整个组合。将模组锁甲改为 NORMAL 属于待实现的层位设计，不能描述为当前原版事实。

## 命中与护甲参数的区别

`src/melee.cpp` 的 `Character::get_hit_weapon()` 使用当前攻击武器的 `m_to_hit`；穿着护甲的 `to_hit` 并非自动附加到另一把武器的攻击命中上。`Character::hit_roll()` 另通过 `melee_attack_roll_mod` 应用肢体平衡修正；躯干累赘还出现在 `get_miss_reason()` 的失误原因权重中，不能把该说明权重直接当作命中公式。故“给胸甲写负 to_hit 就产生穿戴命中罚”缺乏该代码路径支持。

护甲参数还需区别物品覆盖率、材料覆盖比例、各材料厚度及重量。板材厚度不能直接等同锁环线径；相同材料名称也不能替代结构模型。材料计算另见[材料系统调研](code_material_system.md)。
