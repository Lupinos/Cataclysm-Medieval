# 策划案 004：武器体系（14 世纪末 ~ 15 世纪初）

## 时代定位

| 项目 | 说明 |
|------|------|
| 时期 | 约 1375–1425 |
| 武器特征 | 板甲正在普及 → 武器分化出"对人"和"对甲"两条线；长柄武器爆发式多样化 |
| 关键变化 | 剑从斩切为主 → 穿刺优化（Oakeshott XV–XVIII 型）；钝器地位上升 |

---

## 一、武器分类总览

```
中世纪武器（1375-1425）
├── 单手武器（可配盾）
│   ├── 剑系：Arming Sword / Falchion / Shortsword
│   ├── 斧系：Hand Axe / Bearded Axe
│   ├── 锤系：Mace / Flanged Mace / War Hammer
│   └── 杂系：Morning Star / Flail
├── 双手武器
│   ├── 长剑系：Longsword / Estoc
│   ├── 重斩系：Battle Axe / Dane Axe
│   └── 重锤系：Maul / Polehammer
├── 长柄武器（Polearms）→ 第三节详表
├── 短刃 / 副武器
│   ├── Rondel / Baselard / Bollock / Stiletto / Misericorde
│   └── 通用小刀：Eating Knife / Seax
├── 远程
│   ├── 弓：Longbow / Shortbow / Composite Bow
│   ├── 弩：Crossbow / Arbalest
│   └── 投掷：Throwing Knife / Francisca / Javelin
└── 临时/农民武器
    ├── Club / Quarterstaff / Pitchfork / Scythe / Flail (农具版)
    └── Sling / Rock
```

---

## 二、剑系详解

本时期的剑正处于 **Oakeshott 分类 XV–XVIII 型**过渡期 —— 剑身从宽扁向尖锐收窄，穿刺能力大幅提升。

| 武器 | 握法 | 典型长度 | 伤害侧重 | 反甲能力 | 使用者 | CDDA 核心标签 |
|------|------|----------|----------|----------|--------|---------------|
| **Arming Sword**（骑士剑） | 单手 | 75–85 cm 刃 | 斩 60% / 刺 40% | 低（对板甲无效） | 骑士、重装兵 | `ONE_HANDED` `PIERCE` `CUT` |
| **Longsword**（长剑） | 一手半/双手 | 90–110 cm 刃 | 斩 40% / 刺 60% | 中（半剑术可刺缝隙） | 骑士、高级佣兵 | `TWO_HANDED` `PIERCE` `HALF_SWORD` |
| **Estoc**（穿刺剑） | 双手 | 100–120 cm 刃 | 刺 90% / 斩 10% | 高（专刺锁子甲和板甲缝） | 骑士、决斗者 | `PIERCE_ONLY` `ARMOR_PIERCING` |
| **Falchion**（弯刃大刀） | 单手 | 60–75 cm 刃 | 斩 85% / 刺 15% | 极低 | 步兵、平民、佣兵 | `CHOP` `CHEAP` |
| **Messer**（日耳曼战刀） | 一手半 | 70–80 cm 刃 | 斩 70% / 刺 30% | 低 | 平民、民兵（合法携带） | `CUT` `COMMON` |
| **Shortsword**（短剑） | 单手 | 40–55 cm 刃 | 刺 60% / 斩 40% | 低 | 城镇居民、旅行者 | `LIGHT` `FAST` |

### 半剑术（Half-Swording）

Longsword 和 Estoc 的核心技能：左手握剑刃中段，像短矛一样刺入板甲缝隙。

> CDDA 实现思路：给 Longsword / Estoc 添加 `HALF_SWORD` technique，切换后伤害类型变为纯 pierce，大幅提升对 rigid armor 的穿透效果，但攻速下降。

---

## 三、斧系

| 武器 | 握法 | 典型特征 | 伤害侧重 | 反甲能力 | 使用者 |
|------|------|----------|----------|----------|--------|
| **Hand Axe**（手斧） | 单手 | 短柄、通用工具 | 斩 80% / 钝 20% | 低 | 平民、伐木工、民兵 |
| **Bearded Axe**（山羊斧） | 单手 | 刃部下延成钩 | 斩 75% / 钩 25% | 低 | 北欧系战士 |
| **Battle Axe**（战斧） | 双手 | 重型刃、长柄 | 斩 70% / 钝 30% | 中 | 重步兵、骑士 |
| **Dane Axe**（丹麦长斧） | 双手 | 长柄 + 大弯曲刃 | 斩 80% / 钝 20% | 中 | 精锐步兵 |

### 钩技（Hooking）

Bearded Axe 的刃下钩可以挂住盾牌边缘、腿或武器。CDDA 可做成 technique：命中的同时施加短暂的"失去平衡"debuff。

---

## 四、锤与权杖系

板甲的扩散直接促成了锤系武器的爆发。

| 武器 | 握法 | 典型特征 | 伤害侧重 | 反甲能力 | 使用者 |
|------|------|----------|----------|----------|--------|
| **Mace**（权杖） | 单手 | 金属头部、八角/圆柱 | 钝 95% | 高（敲凹板甲、传震到骨头） | 骑士、神职人员（不流血） |
| **Flanged Mace**（凸缘权杖） | 单手 | 刀片状凸起 | 钝 80% + 撕裂 20% | 极高 | 骑士、重装骑兵 |
| **Morning Star**（钉头锤） | 单手 | 球头+尖刺 | 钝 60% + 刺 40% | 高 | 步兵、佣兵 |
| **War Hammer**（战锤） | 单手/双手 | 锤头 + 背刺 | 钝 70% + 刺 30% | 极高 | 骑士（对甲格斗首选） |
| **Maul**（大锤） | 双手 | 粗重木柄铁头 | 钝 100% | 极高 | 重步兵 |

### 钝击的核心价值

对身穿板甲的敌人：刀砍是挠痒，刺也需要精确找缝——**锤子砸一下就够了**。CDDA 中钝击对 rigid armor 的高穿透权重是本体系最关键的平衡点。

---

## 五、长柄武器（Polearms）—— 本时期的标志

长柄武器是 14–15 世纪步兵的王者。

| 武器 | 头型 | 伤害类型 | 特殊能力 | 使用者 | 时期准确度 |
|------|------|----------|----------|--------|------------|
| **Spear**（矛） | 尖头 | 刺 | 可投掷 | 全阶层 | 永恒 |
| **Pike**（长矛） | 极长尖头 | 刺 | 拒马、阵列 | 民兵方阵 | 极佳 |
| **Halberd**（长戟） | 斧面 + 顶刺 + 背钩 | 斩 / 刺 / 钩 | 骑乘击落 | 瑞士/德意志步兵 | 核心 |
| **Bill**（钩镰戟） | 弯曲钩刃 + 尖刺 | 斩 / 刺 / 钩 | 最强拖拽技 | 英国步兵 | 核心 |
| **Glaive**（阔刃长刀） | 单刃弯曲长刀 | 斩 / 刺 | 大范围横扫 | 步兵 | 佳 |
| **Pollaxe**（战戟锤） | 斧 + 锤背 + 顶刺 | 斩 / 钝 / 刺 | 全能对甲 | 骑士步战 | 核心 |
| **Bec de Corbin**（鸦嘴锤） | 锤头 + 长喙刺 | 钝 / 刺 | 穿透板甲头部 | 骑士步战 | 佳 |
| **Lucerne Hammer**（卢塞恩锤） | 三叉锤头 + 顶刺 | 钝 / 刺 | 同上 | 瑞士步兵 | 佳 |
| **Guisarme**（钩镰） | 镰状钩 + 背刺 | 斩 + 钩 | 拖下马、拉倒 | 平民步兵 | 渐退场 |
| **Voulge**（斧矛） | 宽刃 + 尖头 | 斩 / 刺 | 简化的早期 halberd | 法/勃艮第步兵 | 佳 |
| **Fauchard**（镰刃矛） | 弯刀型 | 斩 | 弧度斩击 | 早期步兵 | 渐退场 |
| **Partisan**（翅矛） | 矛 + 两侧翼刀 | 刺 / 斩 | 挡剑 + 斩击 | 警卫/军官 | 初期 |
| **Quarterstaff**（长棍） | 无头 | 钝 | 快攻、格挡 | 平民 | 永恒 |

### CDDA 中的长柄武器设计要点

- **Reach attack**：所有长柄武器天然有 reach 属性，可以在 2 格距离攻击
- **Hook technique**：Halberd / Bill / Guisarme 可以拖拽敌人、拉倒骑马者
- **近距离惩罚**：敌人贴近到 1 格时，pike / long spear 有命中惩罚
- **重量与体耗**：10–15 kg 的长柄需要体力来挥舞

---

## 六、匕首与短刃

| 武器 | 特征 | 伤害类型 | 使用场景 | 使用者 |
|------|------|----------|----------|--------|
| **Eating Knife**（餐刀） | 单刃、钝尖 | 切 | 吃饭、刮柴、最后挣扎 | 全阶层 |
| **Seax**（撒克逊战刀） | 单刃厚背 | 切 / 刺 | 日常工具 + 战斗 | 平民、猎人 |
| **Rondel Dagger**（圆盘匕首） | 细长菱形刃 | 刺 | **板甲对战时刺面甲缝隙/腋下** | 骑士 |
| **Basilard**（巴塞拉短剑） | H 型护手、较短 | 刺 / 切 | 城镇居民防身 | 商人、市民 |
| **Bollock Dagger**（肾形匕首） | 双肾形护手 | 刺 / 切 | 平民防身、15 世纪极流行 | 全阶层 |
| **Stiletto**（锥刺） | 极细无刃 | 刺 | 穿锁子甲环 | 刺客、骑士 |
| **Misericorde**（慈悲之刃） | 细尖刃 | 刺 | 给倒地骑士"最后一下" | 骑士、士兵 |

### 匕首的 CDDA 核心价值

- 板甲格斗中，骑士的 rondel 是**唯一能杀死穿板甲对手的东西**（刺关节缝、面甲缝）
- 餐刀 / seax 是全阶层标配，类似原版 CDDA 的 pocket knife 的定位

---

## 七、远程武器

| 武器 | 类型 | 射程 | 破甲力 | 射速 | 需要训练？ | 使用者 |
|------|------|------|--------|------|-----------|--------|
| **Sling**（投石索） | 投石 | 中近 | 极低 | 中 | 需要 | 牧民、平民 |
| **Shortbow**（短弓） | 弓 | 中 | 低 | 高 | 中等 | 猎人、轻步兵 |
| **Longbow**（长弓） | 弓 | 远（200+ yd） | 高（bodkin arrow） | 高 | 极需（从小学起） | 英国/威尔士征兵 |
| **Composite Bow**（复合弓） | 弓 | 远 | 高 | 高 | 需要 | 东欧/东方 |
| **Light Crossbow**（轻弩） | 弩 | 中 | 中 | 低 | 几乎不需 | 城镇居民、民兵 |
| **Heavy Crossbow**（重弩） | 弩 | 中远 | 高 | 极低 | 不需 | 雇佣弩兵 |
| **Arbalest**（钢臂弩） | 弩 | 远 | 极高（板甲可穿） | 极低 | 不需 | 雇佣弩兵、守城 |
| **Javelin**（投矛） | 投掷 | 近 | 高 | — | 需要 | 步兵 |
| **Francisca**（飞斧） | 投掷 | 近 | 中 | — | 需要 | 蛮族遗风 |

### 关键设计点

- **An archer is a lifestyle**：英国长弓手从 7 岁开始训练，骨骼会变形。这不能是"捡个弓就能用"的角色。
- **弩的民粹性**：不需要力量、不需要训练。一个农民可以一弩射死一个锻炼了二十年的骑士——这是中世纪最革命性的武器社会现象。
- **装填时间**：heavy crossbow 和 arbalest 需要借助 crank/spanner 装填，射一发可能要 3–5 个回合。

---

## 八、临时 / 农民武器

| 武器 | 来源 | 伤害类型 | CDDA 备注 |
|------|------|----------|-----------|
| Club（棍棒） | 粗树枝 | 钝 | 随地可获 |
| Quarterstaff（长棍） | 长木杆 | 钝 | 意外地好用、快攻、格挡强 |
| Wood Axe（伐木斧） | 工具 | 斩 | 比 Hand Axe 重，伤害高但笨重 |
| Pickaxe（镐） | 工具 | 刺+钝 | 急用时可以当 bec de corbin 的穷亲戚 |
| Pitchfork（干草叉） | 农具 | 刺 | 间距控制神器 |
| Scythe（大镰刀） | 农具 | 斩 | 横挥范围大，war scythe 需改装 |
| Blacksmith Hammer（铁匠锤） | 工具 | 钝 | 就是个小锤子 |
| Flail (Grain Flail)（打谷连枷） | 农具 | 钝 | 农民起义的经典武装，绕过盾牌 |
| Rock（石头） | 地面 | 钝 | 没有武器时的最后选择 |

---

## 九、社会阶层 × 惯用武器矩阵

| 阶层 | 典型配置 |
|------|----------|
| 农民 | 手头有什么用什么：flail → pitchfork → wood axe → club → rock |
| 民兵 | spear + 可能有的短刀 / falchion + sling |
| 猎人 | shortbow + seax / hunting knife |
| 城镇民兵 | light crossbow + falchion / messer |
| 佣兵 | spear / bill / halberd + arming sword + bollock dagger |
| 长弓手（英国） | longbow + arming sword + bollock dagger |
| 弩手（热那亚/法国） | heavy crossbow + shortsword |
| 下级骑士 | longsword + rondel dagger + 马背用 lance |
| 骑士（步战） | pollaxe / bec de corbin + arming sword + rondel dagger |
| 领主 | 定制 longsword / pollaxe + estoc + 装饰 dagger |

---

## 十、伤害类型 × 反甲逻辑

| 武器类型 | 对无甲 | 对 gambeson | 对 mail | 对 brigandine | 对 full plate |
|----------|--------|-------------|---------|---------------|---------------|
| 斩击（sword, axe） | ★★★ 致命 | ★★★ 有效 | ★★ 可伤 | ★ 勉强 | ☆ 几乎无效 |
| 穿刺（spear, arrow） | ★★★ | ★★★ | ★★★ 会破环 | ★★ 可能穿 | ★ 刺缝 |
| 钝击（mace, hammer） | ★★ 疼 | ★★ 缓冲 | ★★ 震伤 | ★★★ 传力 | ★★★ 敲凹 + 震伤 |
| 穿刺+精准（rondel, estoc） | ★★★ | ★★★ | ★★★ | ★★★ 专门刺缝 | ★★ 唯一有效方式 |

---

## 十一、与 CDDA 武器系统的映射

| 原版 CDDA 武器 | 中世纪替换方案 |
|----------------|---------------|
| 消防斧 | Hand Axe / Wood Axe |
| 棒球棍 | Club / Quarterstaff |
| 工兵铲 | 无直接对应（铲不是武器），用 pickaxe 近似 |
| 砍刀 machete | Falchion / Messer |
| 战斗匕首 | Rondel / Bollock Dagger |
| M4 卡宾枪 | Longbow（核心远程取代） |
| 霰弹枪 | 无对应 |
| 手枪 | Light Crossbow |

---

## 十二、待定议题

1. **武器制造/维修系统**：铁匠体系的技能树，不能"捡块铁就能敲剑"
2. **武器耐久**：剑刃卷口、斧柄断裂、弦断等的具体机制
3. **毒/药涂抹**：草乌头、毒芹等中世纪毒药涂在箭/匕首上
4. **盾牌系统**：独立策划案（塔盾 → kite shield → heater shield → buckler 是一条完整的退化/进化链）
5. **武器长度对战斗距离的影响**：reach attack 的详细机制
6. **马战**：长矛（lance）的冲击伤害、马上 vs 马下

---

> 下一议题建议：**盾牌系统**（与武器高度关联，决定单手武器线强度），或继续细化**武器制造与维修**。

---

## 一、 中世纪武器库总索引 (Weapons Catalog Index)

武器系统包括 **7 大分类，共 52 件核心武器**。

### 1. 经典近战武器 (Swords, Axes & Hammers)
| 物品 ID | 中文/英文名称 | 武器分类 | 伤害 (Bash/Cut/Stab) | 重量 | 战术特征 / 现状 |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `medieval_shortsword` | 短剑 | SHORT_SWORDS | 4 / 18 / 12 | 800g | 极佳攻速与近身防护。  |
| `medieval_falchion` | 弯刃剑 | SHORT_SWORDS | 8 / 32 / — | 1300g | 厚重刀背，强砍击。  |
| `medieval_messer` | 战刀 | MEDIUM_SWORDS | 6 / 26 / — | 1400g | 经典德式 Messer 单刃砍刀。  |
| `medieval_arming_sword` | 武装剑 | MEDIUM_SWORDS | 6 / 28 / — | 1450g | 经典十字手半剑。  |
| `medieval_longsword` | 手半长剑 | LONG_SWORDS | 8 / 30 / 20 | 1800g | 双手持握，格挡与刺杀兼备。  |
| `medieval_estoc` | 刺剑 (穿甲剑)| LONG_THRUSTING | 4 / — / 28 | 1600g | 纯防具缝隙攒刺，钝尖。  |
| `medieval_hand_axe` | 手斧 | HAND_AXES | 6 / 22 | 1000g | 基础轻型劈砍。  |
| `medieval_bearded_axe` | 倒钩髯斧 | HOOKING_AXES | 6 / 26 | 1400g | 斧髯钩扯盾牌及关节。  |
| `medieval_battle_axe` | 战斧 | GREAT_AXES | 12 / 30 | 2200g | 双手重型破防破甲斧。  |
| `medieval_dane_axe` | 丹麦长斧 | GREAT_AXES | 8 / 36 | 2400g | 经典维京长柄战斧。  |
| `medieval_mace` | 钉头锤 | MACES | 36 / — | 1500g | 重力砸击，板甲克星。  |
| `medieval_flanged_mace` | 翼肋钉头锤 | MACES | 38 / 4 | 1600g | 凸肋破甲，穿透压强极高。  |
| `medieval_morning_star` | 晨星锤 | MACES | 28 / 10 | 1700g | 带刺重锤，砸击带刺。  |
| `medieval_war_hammer` | 战锤 | GREAT_HAMMERS | 22 / 20 (pierce) | 1400g | 锤击/鹤嘴啄刺双面战术。  |
| `medieval_maul` | 巨木槌 | GREAT_HAMMERS | 48 / — | 3500g | 重型钝力，势大力沉。  |

### 2. 精锐长枪与长柄兵器 (Spears & Polearms)
| 物品 ID | 中文/英文名称 | 武器分类 | 伤害 (Bash/Cut/Stab) | 重量 | 战术特征 / 现状 |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `medieval_spear` | 战矛 | SPEARS | 6 / — / 22 | 1800g | 经典极简高性价一丈矛。  |
| `medieval_pike` | 长枪 | SPEARS | 4 / — / 26 | 4000g | `REACH3` 超长攻击距离，阵列武器。  |
| `medieval_halberd` | 戟 | POLEARMS | 14 / 26 / 10 | 3000g | 枪头/斧刃/背钩复合大杀器。  |
| `medieval_bill` | 钩镰枪 | POLEARMS | 10 / 22 / 8 | 2800g | 钩杀骑兵，扯倒盾牌。  |
| `medieval_glaive` | 偃月刀 (大刀) | POLEARMS | 8 / 30 / — | 2800g | 大斩击范围，长柄大刀。  |
| `medieval_pollaxe` | 战斧长戟 | POLEARMS | 20 / 12 / 10 | 3200g | 过渡期步行骑士的核心杀器。  |
| `medieval_bec_de_corbin`| 乌鸦嘴 | POLEARMS | 22 / — / 16 (pierce) | 3000g | 大破甲啄击。  |
| `medieval_lucerne_hammer`| 琉森锤 | POLEARMS | 24 / — / 12 (pierce) | 3000g | 锤啄结合重长柄。  |
| `medieval_guisarme` | 钩镰戟 | POLEARMS | 8 / 18 / 6 | 2600g |  |
| `medieval_voulge` | 佛格长柄 | POLEARMS | 10 / 24 / 8 | 2800g |  |
| `medieval_fauchard` | 长柄钩刀 | POLEARMS | 6 / 22 / — | 2400g |  |
| `medieval_partisan` | 游击戟 | SPEARS | 6 / 10 / 20 | 2200g | 枪两侧有横突。  |
| `medieval_quarterstaff` | 齐眉棍 | QUARTERSTAVES | 16 / — | 1800g | `RAPID` 极高招架与自卫长棍。  |

### 3. 短刃、远程与农民兵器 (Daggers, Ranged & Peasants)
| 物品 ID | 中文/英文名称 | 武器分类 | 伤害与射程 | 重量 | 战术定位 / 现状 |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `medieval_eating_knife` | 平民餐刀 | KNIVES | b1, c6 | 80g |  |
| `medieval_seax` | 萨克斯短刀 | KNIVES | b3, c12, s8 | 400g | 维京经典单刃大匕首。  |
| `medieval_rondel_dagger`| 轮首穿甲针 | KNIVES | b2, s16 | 350g | 轮状手柄，防具缝隙杀手。  |
| `medieval_baselard` | 巴瑟拉德匕首 | KNIVES | b2, c12, s10 | 500g | 市民自卫经典宽刃短剑。  |
| `medieval_bollock_dagger`| 肾形匕首 | KNIVES | b2, c10, s12 | 350g |  |
| `medieval_stiletto` | 刺客细剑 | KNIVES | b1, s18 | 200g | 极细剑身，忽略轻型护甲。  |
| `medieval_misericorde` | 慈悲匕首 | KNIVES | b1, s20 | 300g | 重伤终结，高破甲。  |
| `medieval_sling` | 投石索 | GUN | b14 / 射程 12 | 100g | 极简低造价远程自卫。  |
| `medieval_shortbow` | 短弓 | GUN | s3 / 射程 14 | 500g | 基础轻灵弓。  |
| `medieval_longbow` | 英格兰长弓 | GUN | s6 / 射程 22 | 700g | 重拉力大杀器。  |
| `medieval_composite_bow`| 复合弓 | GUN | s5 / 射程 20 | 600g | 游牧角弓，攻速快。  |
| `medieval_light_crossbow`| 轻型手弩 | GUN | s3 / 射程 10 | 2.5kg | 基础单手/轻便机械弩。  |
| `medieval_heavy_crossbow`| 重弩 | GUN | s5 / 射程 16 | 4.5kg | 带拉环踏板的重型弩。  |
| `medieval_arbalest` | 钢弩 (绞盘弩) | GUN | s7 / 射程 20 | 6.0kg | 纯钢弩臂，手柄绞盘，高破防。  |
| `medieval_javelin` | 掷标枪 | GENERIC | s18 / 投掷伤害 14 | 800g | Melee/Thrown 双重近投。  |
| `medieval_francisca` | 飞斧 | GENERIC | c16 / 投掷伤害 12 | 900g | 经典法兰克人投掷飞斧。  |
| `medieval_club` | 木棒 | BATONS | b14 | 1.2kg |  |
| `medieval_wood_axe` | 伐木斧 | HAND_AXES | b10, c24 | 2.0kg | 经典工具兼作防卫。  |
| `medieval_pickaxe` | 矿工鹤嘴锄 | HOOKING | b10, s18 | 3.0kg | 破甲刨刺极佳。  |
| `medieval_pitchfork` | 干草叉 | SPEARS | b4, s16 | 2.2kg |  |
| `medieval_scythe` | 割草长镰刀 | POLEARMS | b4, c24 | 2.4kg |  |
| `medieval_blacksmith_hammer`| 铁匠大锻锤 | BATONS | b20 | 1.2kg | 极强纯砸力。  |
| `medieval_flail` | 连枷 | FLAILS | b22 | 1.8kg | 破盾忽略格挡。  |
| `medieval_rock` | 防卫碎石 | BATONS | b8 | 400g |  |
| `medieval_lance` | 骑士冲锋重骑枪 | LANCES | — | — | 重装骑兵冲锋特化武器 (LANCE)。  |

---

### 阶段 2：武器弹药细化与伤害平衡 
- **弓弩配套专属中世纪箭头弹药细化**：
  - 实装 **Bodkin arrow (针式防具穿刺型箭头/弩箭)**：对 Pierce (刺击) 拥有极高破甲穿透，但 Cut 极低。
  - 实装 **Broadhead arrow (防具割裂型宽头箭头/弩箭)**：对无甲/轻甲单位产生极大 Cut 与流血效果，但极难突破铁锁甲/板甲。
  - 实装 **Blunt arrow (钝击练习木/皮头箭)**：造成小额纯 Bash 击退伤害，主要用于防卫与练习。
- **骑乘长枪 (Lance) 的重装突破机制**：
  - 实装骑兵冲锋骑枪 `medieval_lance` 实体。
  - 与 C++ 骑乘/速度系统联动，实现“根据骑马移速百分比物理叠加 Stab 穿刺伤害”的战术机制。

### 阶段 3：多材料梯度升级变体 
- 策划在保留当前通用 `steel` 单材质的基础上，未来通过 copy-from 衍生出：
  - `lc_steel` (低碳钢/熟铁) 版低价高频消耗剑
  - `ch_steel` / `qt_steel` (淬火/渗碳钢) 版顶级大师骑士定制武器（高锋利度、高耐久、强格挡值）
  - `bronze` (青铜) 仿古武器变体

---

### 1. STR × 武器重量破甲

- **逻辑**：`arpen += weapon_mass_kg × (arm_str / 10)`
  - bash 伤害：全额加成
  - stab/cut 伤害：折半（×0.5）
  - 仅对持武器攻击生效（徒手走独立的 `unarmed_arpen` 体系）

---
