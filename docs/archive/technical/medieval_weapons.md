# 中世纪近战与远程武器体系实现方案

> 策划案 → [design04-武器.md](../../design/design04-武器.md)

本文记录中世纪模组中**所有近战与远程战术武器项（共 55 件）**的内容与规划。

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

## 二、 武器系统开发阶段 Checklist

武器体系开发按照核心战术体系稳步推演：

### 阶段 1：首发 52 件完整武器库实装 ()
- 实装经典剑系（武装剑、长剑、 estoc、 shortsword 等6件）
- 实装经典斧系与锤系（ battle axe、 dane axe、战锤、 morning star 等9件）
- 实装长枪与长柄铁器（ spear、 halberd、 pollaxe、 bec de corbin 等13件）
- 实装短刃匕首系（ rondel 穿甲针、 seax、 misericorde 慈悲锋等7件）
- 实装远程弓弩、标枪、投石索及飞斧（ longbow、 arbalest 钢弩、 javelin 等9件）
- 实装农民及劳作临时武器（干草叉、连枷、铁匠锤等8件）
- 实现原版巨大 `melee.json` 的解耦，按 swords/axes 等分立文件管理

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
