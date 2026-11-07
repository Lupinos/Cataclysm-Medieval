# 物品伤害与破损等级（0.H 原版）

> 核对基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 初始提交的父提交）。以下描述该基准原版，不代表旧 Medieval 引擎。源码路径均相对此基准。

## 存储、等级和销毁

`src/itype.h` 定义 `damage_scale = 1000`，普通非 charges 计数物品的 `damage_max_ = 4000`。`src/item.h` 的 `item::damage_` 保存实际损伤，另有 `degradation_` 表示不能通过普通修理消除的退化下限。

`src/itype.cpp::itype::damage_level`：

```cpp
if( damage == 0 ) return 0;
if( count_by_charges() ) return 5;
return std::clamp( 1 + 4 * damage / damage_max(), 0, 5 );
```

普通最大损伤为 4000 时：

| 实际损伤 | damage_level |
|---|---|
| 0 | 0 |
| 1–999 | 1 |
| 1000–1999 | 2 |
| 2000–2999 | 3 |
| 3000–3999 | 4 |
| 4000 | 5 |

这是离散等级映射，不是每级恰好增加 1000 的零起点等级。不要把实际损伤 4000 直接称作“等级 4”。UI 文本和符号由显示路径决定，不能把上表等级与某组竖线图案固定绑定。

`src/item.cpp::item::set_damage` 将输入夹在 `degradation_` 与 `max_damage()` 之间。普通 `mod_damage(qty)` 在 `damage_ + qty > max_damage()` 时报告销毁；恰好等于最大值不等于这个函数已经报告销毁。按 charges 计数的物品走减少数量的分支，不适用普通物品的逐级破损模型。

## 破损对数值的影响

`src/item.cpp` 的三个函数分别使用（非 charges 物品）：

```text
近战伤害 = 原值 × (1 - 0.1 × max(0, level - 1))
枪械伤害 = 原值 - 2 × max(0, level - 1)
护甲抗性 = 原值 × (1 - 0.125 × max(0, level - 1))
```

对应函数：`damage_adjusted_melee_weapon_damage`、`damage_adjusted_gun_damage`、`damage_adjusted_armor_resist`。level 0 和 1 均没有这里列出的惩罚。

## item_group 的 damage 区间

`src/item_factory.cpp` 的物品组 modifier 加载将 JSON 的 damage 上下限乘以 1000；`src/item_group.cpp::Item_modifier::modify` 随机抽取实际损伤后调用 `set_damage`，再执行 `rand_degradation()`。因此 JSON 指定的是损伤区间，不是先等概率选择离散 damage_level。

对刚生成、未受其他修正、最大损伤为 4000 的普通物品，按闭区间整数均匀抽样可算出：

| JSON 区间 | 实际抽样区间 | 离散等级分布 |
|---|---|---|
| `[1,3]` | 1000–3000 | level 2、3 各 1000/2001；level 4 为 1/2001 |
| `[0,1]` | 0–1000 | level 0、2 各 1/1001；level 1 为 999/1001 |
| `[0,2]` | 0–2000 | level 0、3 各 1/2001；level 1 为 999/2001；level 2 为 1000/2001 |
| `[0,3]` | 0–3000 | level 0、4 各 1/3001；level 1 为 999/3001；level 2、3 各 1000/3001 |

这仍是真正的随机，只是将连续整数损伤映射到少数显示等级后分布不均。`[0,1]` 的确几乎总显示 level 1；扩大区间会同时增加高破损装备，并不只是让外观更丰富。

若 n 件物品独立、同分布抽样，全部等级一致的概率是 `sum(p_i ** n)`。例如 `[1,3]` 下三件装备约为 25%；这是有条件的数学估算，不能直接说每四名某职业 NPC 必有一名如此。物品种类、生成路径、charge 计数与后续装备处理不同，结论也会变化。

## 内容配置的含义

希望特定完整度比例时，应明确配置不同损伤区间或条目的概率，先决定玩法分布，再选择 JSON 表达。原版的损伤映射本身不承诺各个显示等级等概率。Medieval 强盗各职业的具体投放值属于项目内容，不是原版机制的一部分。
