# 策划案 008：野怪 NPC 体系（一）—— 强盗

## 一、装备等级原则——"强盗应该比你穷"

**核心问题**：原 008 第一版中 `bandit_medium` 就穿了 mail hauberk + arming sword——这已经是步兵级别的配置了。在秩序崩溃的世界里，大批量出现这种装备是不合理的。

### 装备稀缺性阶梯

| 装备 | 拥有者 | 理由 |
|------|--------|------|
| 破烂衣物、草叉、棍棒 | 大多数强盗 | 农民转业，捡到什么用什么 |
| Gambeson | 少数强一点的 | 从民兵尸体上扒的 |
| 锁子甲部件（袖子/护颈/半身） | 少数幸运者 | 完整的 hauberk 太贵，但捡到局部是可能的 |
| 完整的 mail hauberk | **几乎不应该出现** | 一套锁子甲够一个村子吃一年 |
| Brigandine / 板甲部件 | 仅头目 | 从骑士/军官尸体上抢的，数量极其有限 |
| 好剑（arming sword 以上） | 仅头目 | 剑比斧贵得多，强盗没有铁匠定制 |

### 贫富梯度

```
bandit_weak ────── 穿得比你还惨。他手里的"武器"你在田里就能找到。
bandit_medium ──── 有一两件像样的东西，但不成套。
bandit_strong ──── 有半套好装备，很可能杀过正经士兵。
bandit_leader ──── 才配得上 mail + 好剑。见面你就知道他是老大。
```

---

## 二、技能分布设计（取代固定值）

> 同类强盗的训练和补给存在随机差异，以下为候选分布。

### 2.1 bandit_weak

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | 随机 0—1 | 有人用过刀，有人没碰过 |
| Bashing | 随机 0—2 | 棍子和连枷是农民工具，部分人很熟 |
| Piercing | 随机 0—1 | — |
| Dodge | 固定 0 | 不会躲 |
| Throwing | 概率 1/3 → 得 1 否则 0 | 1/3 概率会扔石头 |
| Survival | 随机 0—2 | 农民出身有野外常识 |
| 特殊 | — | — |

### 2.2 bandit_medium

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | 随机 1—2 | 至少用过刀 |
| Bashing | 随机 1—2 | — |
| Piercing | 随机 0—2 | 可能用过矛 |
| Dodge | 随机 0—1 | 少数人有战场经验 |
| Throwing | 随机 0—1 | — |
| 特殊 | — | — |

### 2.3 bandit_strong

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | 随机 2—3 | 正经打过仗 |
| Bashing | 随机 2—3 | — |
| Piercing | 随机 1—2 | — |
| Dodge | 随机 1—2 | 知道怎么活下来的人 |
| 特殊 | 概率获得 概率 1/4 → 退伍士兵特质 | 额外 +1 Cutting/Bashing |

### 2.4 bandit_archer

| 技能 | 分布 | 说明 |
|------|------|------|
| Archery | 随机 1—3 | 从"会拉弦"到"偷猎老手"都有 |
| Cutting | 随机 0—1 | 近战很弱 |
| Dodge | 随机 0—1 | — |
| 特殊 | 箭矢数量 随机 5—20 | 运气好捡到多 |

### 2.5 bandit_marksman

| 技能 | 分布 | 说明 |
|------|------|------|
| Archery | 随机 3—5 | 逃兵弓箭手或职业偷猎者 |
| Cutting | 随机 1—2 | 有备用的近战能力 |
| Dodge | 随机 1—2 | — |
| 特质 | 概率 概率 1/3 → 潜行 | 埋伏型 |
| 箭矢 | 随机 8—20 | 不多但每箭都可能致命 |

### 2.6 bandit_leader

| 技能 | 分布 | 说明 |
|------|------|------|
| Cutting | 随机 2—4 | 比手下强是活下来的前提 |
| Bashing | 随机 2—3 | — |
| Piercing | 随机 1—3 | — |
| Dodge | 随机 1—2 | — |
| Speech | 随机 1—2 | 能镇住手下叫"说服力" |
| 独有 | 低概率 概率 1/10 → Literacy 1 | 极少数头目能识字 |

---

## 三、装备组（装备组合）设计

每名强盗按身份随机取得装备组合，保留贫富差异和物资稀缺性。

### 3.1 bandit_weak_worn（盔甲衣物池）

```
patched_gambeson (wt: 5)       ← 捡来的旧 gambeson
rough_wool_tunic (wt: 15)      ← 农民标配，几乎不防
linen_shirt (wt: 10)           ← 可能连外衣都没有
torn_wool_cloak (wt: 5)        ← 破斗篷
felt_hat (wt: 5)               ← 有人有帽子
no_helmet (wt: 60)             ← 大多数人没头盔
```

### 3.2 bandit_weak_weapon（武器池）

```
grain_flail (wt: 10)           ← 打谷连枷
wood_axe (wt: 8)               ← 伐木斧
club (wt: 12)                  ← 随手捡的棍子
pitchfork (wt: 5)              ← 干草叉
sling (wt: 3)                  ← 投石索
hand_axe (wt: 3)               ← 手斧（少，因为手斧比棍子"贵"）
rock_pile (wt: 8)              ← 石头也行，别嫌弃
```

### 3.3 bandit_medium_worn（盔甲衣物池）

```
gambeson (wt: 10)              ← 捡来的正经 gambeson（可能破）
leather_jerkin (wt: 8)         ← 硬皮短衣
mail_coif (wt: 2)              ← 捡漏的锁子甲头巾（稀有）
mail_sleeves_partial (wt: 1)   ← 单只锁子甲袖子（极稀有，不成套）
kettle_hat (wt: 3)             ← 锅盔
leather_cap (wt: 5)            ← 皮盔
wool_tunic (wt: 15)            ← 很多人还是穿布
```

> **注意**：不包含完整的 mail hauberk。一件完整锁子甲对一个强盗来说过于奢侈。锁子甲部件（头巾、袖子、半身）是可能出现的，但也是稀有的。

### 3.4 bandit_medium_weapon（武器池）

```
falchion (wt: 5)               ← 平民弯刃刀
hand_axe (wt: 8)               ← 手斧
spear (wt: 10)                 ← 最便宜的军用武器
arming_sword (wt: 2)           ← 捡来的骑士剑（稀有）
mace (wt: 3)                   ← 捡来的权杖
club_spiked (wt: 5)            ← 打上钉子的木棍
seax (wt: 7)                   ← 长战斗刀
```

### 3.5 bandit_strong_worn（盔甲衣物池）

```
gambeson (wt: 15)              ← 普遍有
mail_coif (wt: 5)              ← 锁子甲头巾
brigandine_partial (wt: 3)     ← 捡来的 brigandine 半身——奢侈了
mail_vest (wt: 2)              ← 锁子甲背心（不是全长 hauberk！）
plate_gauntlets (wt: 1)        ← 捡来的铁手套
bascinet_no_visor (wt: 3)      ← 无面罩尖顶盔
kettle_hat (wt: 5)             ← 锅盔（有人还是戴这个）
```

### 3.6 bandit_strong_weapon（武器池）

```
battle_axe (wt: 5)             ← 正经战斧
arming_sword (wt: 5)           ← 骑士剑
war_hammer (wt: 3)             ← 战锤
billhook (wt: 4)               ← 钩镰戟（从民兵尸体上扒的）
longsword (wt: 2)              ← 长剑（很稀有）
morning_star (wt: 3)           ← 钉头锤
```

### 3.7 bandit_archer_worn

```
gambeson_light (wt: 10)        ← 轻量 gambeson
leather_jerkin (wt: 8)         ← 硬皮短衣
wool_tunic (wt: 12)            ← 还是布
coif (wt: 5)                   ← 布头巾
```

### 3.8 bandit_archer_weapon

```
shortbow (wt: 10)              ← 短弓
light_crossbow (wt: 5)         ← 轻弩
sling (wt: 3)                  ← 更穷的弓手
```

### 3.9 bandit_marksman_weapon

```
longbow (wt: 5)                ← 长弓（逃兵弓手）
heavy_crossbow (wt: 5)         ← 重弩（逃兵弩手）
composite_bow (wt: 2)          ← 复合弓（东欧/东方背景）
```

### 3.10 bandit_leader_worn

```
bandit_strong_worn 全部 (wt: 10) ← 等同于 strong 或更好
mail_hauberk (wt: 3)           ← 终于出现了！但仍是稀有
brigandine_full (wt: 2)        ← 完整 brigandine
bascinet_visor (wt: 3)         ← 带面罩的尖顶盔
plate_greaves (wt: 1)          ← 胫甲
```

### 3.11 bandit_leader_weapon

```
longsword (wt: 3)              ← 定制长剑
arming_sword (wt: 4)           ← 配盾组合
pollaxe (wt: 2)                ← 骑士戟（扛着就显身份）
war_hammer (wt: 3)             ← 战锤
estoc (wt: 1)                  ← 穿刺剑（极稀有）
```

---

## 四、兽人强盗（技能分布）

兽人属性偏移不变（Str+4, Int-3, 大型, HP+30%），但技能也用分布替代固定值：

### orc_bandit_warrior

| 技能 | 分布 |
|------|------|
| Bashing | 随机 2—4 |
| Cutting | 随机 1—3 |
| Dodge | 固定 0 |
| Throwing | 随机 1—2 |

### orc_bandit_archer

| 技能 | 分布 |
|------|------|
| Archery | 随机 1—2（力量够、精度低） |
| Bashing | 随机 1—2（近战保底） |

### orc_bandit_chief

| 技能 | 分布 |
|------|------|
| Bashing | 随机 3—5 |
| Cutting | 随机 2—4 |
| Dodge | 随机 0—1 |

兽人装备池同理，从对应 装备组合 抽取，但偏重重型武器和粗糙拼装盔甲。

---

## 五、哥布林强盗（技能分布）

哥布林属性偏移（Str-4, Dex+4, 小型, HP-40%, 速度+10%），技能分布：

### goblin_cutthroat

| 技能 | 分布 |
|------|------|
| Cutting | 随机 1—2 |
| Piercing | 随机 1—2 |
| Dodge | 随机 2—4（小型 + 敏捷） |

### goblin_slinger

| 技能 | 分布 |
|------|------|
| Throwing | 随机 2—3 |
| Dodge | 随机 2—4 |

---

### 7.3 搜刮预期（更新后）

| 强盗 | 你大概能拿到什么 |
|------|------------------|
| weak | 草叉、破布、半块面包。几乎不值得打。 |
| medium | 也许一件 gambeson 或手斧，值一点点钱。 |
| strong | 可能有 brigandine 部件或好武器。这是 loot 的甜点区。 |
| leader | 才配出 mail、好剑、百枚硬币。真正的 reward。 |

---

## 十、设计注记

### 10.1 为什么不写死技能值

同类敌人的能力与物资应有随机差异。写死技能值有两个问题：

1. **同质化**：每个 bandit_medium 都一样，玩家第一次遇到的是老手，第 20 次遇到的还是同一个老手
2. **失去惊喜**：分布意味着你偶尔会遇到一个技能 roll 到 3 的 bandit_weak（"这农民怎么这么能打？"），或者 roll 到 1 的 bandit_strong（"穿着好甲但其实是纸老虎"）

### 10.2 装备池 = 故事

`装备组合` 的 权重 本身就是叙事：

- `arming_sword` 在 bandit_weak 池里 权重 0——不存在。农民没有剑。
- `arming_sword` 在 bandit_medium 池里 权重 2——捡来的，稀有。
- `mail_hauberk` 只在 bandit_leader 池里 权重 3——你可能杀了 10 个头目都见不到一件。见到的时候你该兴奋。

### 10.3 搜刮预期

| 强盗 | 你大概能拿到什么 |
|------|------------------|
| weak | 草叉、破布、半块面包。几乎不值得打。 |
| medium | 也许一件 gambeson 或手斧，值一点点钱。 |
| strong | 可能有 brigandine 部件或好武器。这是 loot 的甜点区。 |
| leader | 才配出 mail、好剑、百枚硬币。真正的 reward。 |

### 10.4 派系让世界活起来

CDDA 的经验告诉我们：
- **不是所有敌人都见面就打**。路匪可以先收费再动手，这比无脑 aggro 有趣得多。
- **强盗内部有社会结构**。商人（不打你但卖黑货）、军需官、头目——这让据点不只是刷怪点。
- **不同种族的强盗互相打**。兽人和人类强盗 kill on sight，意味着玩家可以利用他们内斗。

---


## 据点、交互与遭遇

- 强盗营地设置荒野入口与通路，并给玩家可辨认的危险信号。
- 收费路匪初始中立，玩家可交易、付款或拒绝；拒绝后可能出现两名喽啰伏击。
- 伪装饥民以求助诱导玩家：给食物、拒绝或揭穿均可触发不同敌对回应。旧方案中拒绝会引出两名喽啰和一名老手，其他分支为两名喽啰。
- 野外遭遇覆盖远近组合、树林冷箭、精锐双人和首领团；刷新频率与组合权重重新平衡，不沿用旧原型的验证结论。
- 后续候选内容包括大型木堡哨站、地牢俘虏与救援声望、强盗黑市和军需商人。
