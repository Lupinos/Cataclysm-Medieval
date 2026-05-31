# 中世纪盔甲与战术防护体系实现进度

> 策划案 → [design02-盔甲.md](../design/design02-盔甲.md) 与 [design02_1-布里根丁与板甲衣细分.md](../design/design02_1-布里根丁与板甲衣细分.md)
> 总任务追踪 → [core_work.md](../../rules/core_work.md)

本进度文档记录中世纪模组中**所有战术级防具/盔甲项（共 42 件）**的实装现状与未来规划。日常布织服装参见 [medieval_clothing.md](medieval_clothing.md)。

---

## 一、 中世纪战术防具总索引 (Armor Item Index)

目前中世纪盔甲系统已实装 **42 件核心物品**。通过对此总表的查阅，可以一眼了然所有装备的实装现状。

### 1. 头部与颈部防具 (Head & Neck Pack)
| 物品 ID | 中文/英文名称 | 材质等级 | 厚度 (mm) | 累赘度 | 状态 | 定位与现状 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `med_hood_linen` | 亚麻兜帽 | linen | 1.0 | NONE (0) | `[x]` | 基础底层防护。 ✅ 已实装 |
| `med_cap_leather` | 厚皮帽 | leather | 2.0 | NONE (0) | `[x]` | 铁盔廉价替代品。 ✅ 已实装 |
| `med_helm_kettle` | 锅盔 | lc_steel | 1.5 | NONE (0) | `[x]` | 视野优良，经典步兵盔。 ✅ 已实装 |
| `med_helm_bascinet` | 尖顶盔 | mc_steel | 2.0 | WELL_SUPPORTED | `[x]` | 过渡期标志性士兵盔。 ✅ 已实装 |
| `med_helm_bascinet_visor` | 猪面尖顶盔 | mc_steel | 2.0/1.5 | WELL_SUPPORTED | `[x]` | 面甲高防护与阻断偏斜。 ✅ 已实装 |
| `med_helm_great` | 巨桶盔 | mc_steel | 2.0/1.5 | RESTRICTS_NECK | `[x]` | 重型铁桶盔，重修重量。 ✅ 已实装 |
| `med_helm_sallet` | 轻钢盔 | mc_steel | 2.0/1.5 | WELL_SUPPORTED | `[x]` | 新兴流线型军用盔。 ✅ 已实装 |
| `med_aventail` | 锁甲护颈 aventail | lc_steel_chain | 1.2 | 4 | `[x]` | 尖顶盔边缘挂帘，重修重量。 ✅ 已实装 |
| `med_standard_leather` | 皮护领 standard | hardened_leather | 2.5 | 3 | `[x]` | 熟皮防刺领。 ✅ 已实装 |
| `med_gorget` | 板甲护喉 | mc_steel | 1.8 | 5 | `[x]` | 纯板甲护领。 ✅ 已实装 |
| `med_bevor` | 板甲护颚 bevor | mc_steel | 1.8/1.5 | WELL_SUPPORTED | `[x]` | Sallet 头盔金牌搭档。 ✅ 已实装 |

### 2. 躯干核心战术防具 (Torso Core Armor)
| 物品 ID | 中文/英文名称 | 材质等级 | 厚度 (mm) | 累赘度 | 状态 | 战术定位与现状 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `med_cuirass` | 钢板胸甲 | mc_steel | 2.5 | 16 | `[x]` | 顶级整体板甲防线。 ✅ 已实装 |
| `med_cuir_bouilli_coat_of_plates` | 熟皮板甲衣 | hardened_leather | 4.0 | 15 | `[x]` | 熟皮水煮，极易手工自制。 ✅ 已实装 |
| `med_visby_coat_of_plates` | 维斯比板甲衣 | lc_steel | 1.5 | 16 | `[x]` | 经典款，防护厚重但累赘。 ✅ 已实装 |
| `med_heavy_coat_of_plates` | 重型骑士板甲衣 | mc_steel | 2.2 | 19 | `[x]` | 枪比武神装，-2 命中惩罚。 ✅ 已实装 |
| `med_commoners_brigandine` | 平民粗钢布里根丁 | budget_steel | 1.2 | 13 | `[x]` | 卫兵/军士主流装，性价比高。 ✅ 已实装 |
| `med_archers_brigandine` | 射手轻型布里根丁 | mc_steel | 1.2 | 8 | `[x]` | 去除肩腋板，80%覆盖防拉弓干涉。 ✅ 已实装 |
| `med_corrazina` | 科拉齐纳意式甲 | mc_steel | 2.0/1.5 | 14 | `[x]` | 前胸加厚板，正面防穿刺佳。 ✅ 已实装 |
| `med_knights_brigandine` | 骑士天鹅绒布里根丁 | mc_steel | 1.8 | 11 | `[x]` | 华丽天鹅绒，高灵动高防。 ✅ 已实装 |
| `med_chalcis_brigandine` | 查尔基斯复合甲 | mc_steel | 2.0/1.5 | 13 | `[x]` | 胸大板与腹细鳞完美拼合。 ✅ 已实装 |
| `med_jack_of_plates` | 平民绳系杰克甲 | budget_steel | 1.0 + 2.5 | 15 | `[x]` | 铁布复合，手工自制抗砸佳。 ✅ 已实装 |
| `med_mail_shirt` | 轻型无袖锁甲衬衫 | lc_steel_chain | 1.2 | 10 | `[x]` | 轻灵短袖，只护躯干。 ✅ 已实装 |
| `med_hauberk` | 经典全身及膝锁甲大衣| lc_steel_chain | 1.2 | 18/12/14 | `[x]` | 及膝长袖，高精全身包覆重构。 ✅ 已实装 |
| `med_heavy_hauberk` | 精锐双层长锁甲大衣 | mc_steel_chain | 2.4 | 22/15/16 | `[x]` | 优质回火中碳钢，双层穿环。 ✅ 已实装 |
| `med_rust_mail` | 锈蚀锁子甲大衣 | budget_steel_chain | 1.2 | 12 | `[x]` | 强盗土匪粗制破损锁甲。 ✅ 已实装 |

### 3. 四肢与手足防具 (Limb, Hands & Feet)
| 物品 ID | 中文/英文名称 | 材质等级 | 厚度 (mm) | 累赘度 | 状态 | 覆盖细节与现状 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `med_spaulder` | 板甲护肩 | mc_steel | 1.5 | 5 | `[x]` | 覆盖肩膀。 ✅ 已实装 |
| `med_rerebrace` | 板甲上臂甲 | mc_steel | 1.5 | 5 | `[x]` | 覆盖上臂。 ✅ 已实装 |
| `med_couter` | 板甲肘甲 | mc_steel | 1.8 | 3 | `[x]` | 覆盖肘关节。 ✅ 已实装 |
| `med_vambrace` | 板甲前臂甲 | mc_steel | 1.5 | 5 | `[x]` | 覆盖前臂。 ✅ 已实装 |
| `med_cuisse` | 板甲大腿甲 | mc_steel | 1.5 | 8 | `[x]` | 覆盖大腿正面。 ✅ 已实装 |
| `med_poleyn` | 板甲膝甲 | mc_steel | 1.8 | 4 | `[x]` | 覆盖膝盖及后侧侧翼。 ✅ 已实装 |
| `med_greave` | 板甲胫甲 | mc_steel | 1.5 | 6 | `[x]` | 覆盖小腿胫骨。 ✅ 已实装 |
| `med_gauntlets_hourglass`| 沙漏板手套 | mc_steel | 1.5/1.2 | 8/4 | `[x]` | 保护手腕背，手心灵活。 ✅ 已实装 |
| `med_gauntlets_plate` | 叠片板手套 | mc_steel | 2.0/1.5 | 10/5 | `[x]` | 极致全指节覆盖板手套。 ✅ 已实装 |
| `med_sabatons_plate` | 叠片板铁鞋 | mc_steel | 2.0/1.5 | 14/4 | `[x]` | 包裹鞋面及脚后跟，鞋底空。 ✅ 已实装 |
| `med_sabatons_mail` | 锁甲鞋套 | lc_steel_chain | 1.2 | 8 | `[x]` | 罩在皮靴外的锁甲，不护鞋底。 ✅ 已实装 |
| `med_brigandine_arms` | 布里根丁护臂 | mc_steel | 1.2/0.6 | 10 | `[x]` | 小钢片内衬，提供高灵动双臂防护。 ✅ 已实装 |
| `med_brigandine_legs` | 布里根丁护腿 | mc_steel | 1.2/0.8 | 12 | `[x]` | 鳞片内衬防具，保留极佳奔跑性。 ✅ 已实装 |
| `med_gloves_leather` | 皮手套 | leather | 1.5 | 3 | `[x]` | 底层手部防擦伤皮套。 ✅ 已实装 |
| `med_boots_leather` | 皮长靴 | leather | 2.0/4.0 | 12 | `[x]` | 军民通用厚皮底长靴。 ✅ 已实装 |
| `med_mail_chausses` | 锁甲腿裤 | lc_steel_chain | 1.2 | 14 | `[x]` | 重修重量，大腿至踝高Cut防线。 ✅ 已实装 |
| `med_barding_leather` | 战马皮铠甲 | leather | — | — | `[ ]` | 马匹及骑乘防具扩展。 📅 **计划中** |
| `med_barding_steel` | 战马钢板护具 | mc_steel | — | — | `[ ]` | 骑乘重装冲锋用顶级马铠。 📅 **计划中** |

---

## 二、 盔甲系统开发阶段 Checklist

中世纪过渡期盔甲系统的开发以阶段式递进，进度如下：

### 阶段 1：首发基础盔甲实装 (基础骨架)
- [x] 实装基础亚麻内衣、武装 Gambeson (Layer 1~2)
- [x] 实装基本铁盔：锅盔、尖顶盔 (Kettle hat, Bascinet)
- [x] 实装前四肢整体板甲护具 (Vambrace, Greave 等)
- [x] 实装基础沙漏手套与板铁鞋 (Hourglass gauntlets, Plate sabatons)

### 阶段 2：重装精细化、细化与物理纠偏 (过渡盔甲期巅峰重塑)
- [x] **抽象化退化**：将无后缀 `med_brigandine` 退化为纯抽象类 `med_brigandine_base`，消除原本的实体冗余。
- [x] **板甲衣 (CoP) 细化**：实装 `cuir-bouilli` (熟皮)、`Wisby` (熟铁)、`heavy` (中碳钢重装) 3款特化板甲衣。
- [x] **布里根丁 (Brigandine) 细化**：实装平民粗钢型、长弓射手轻型、科拉齐纳正面特化型、骑士华丽天鹅绒型、查尔基斯复合型等 5 款。
- [x] **平民杰克甲实装**：手工绳系杰克甲 `med_jack_of_plates`，提供极佳抗钝击能力。
- [x] **经典锁甲全身重构**：修复原本 `med_hauberk` 只护躯干的 Bug，扩充其覆盖至双臂、大腿，上调重修其负荷重量。
- [x] **锁子甲细化实装**：实装轻型锁子衬衫 `med_mail_shirt`、精锐中碳钢双层长锁甲 `med_heavy_hauberk`、锈蚀强盗锁甲 `med_rust_mail`。
- [x] **配套肢体防具扩展**：实装布里根丁护臂 `med_brigandine_arms` 与 护腿 `med_brigandine_legs`。
- [x] **历史重量与负重纠偏**：修正锅盔偏重（下调至 1.7kg）；修正尖顶盔偏轻（上调至 2.3kg）；修正巨盔偏轻（上调至 3.8kg 且体积增加）；将锁甲护颈 aventail 与锁甲腿裤 chausses 重量纠偏为真实密度的 2.0kg 和 6.0kg，并补齐 `STURDY` 标志。

### 阶段 3：未来防护体系扩展计划 (将要做)
- [ ] **马匹与骑乘防护扩展 (Barding)**：
  - [ ] 策划战马皮质装甲 `med_barding_leather` 属性数据与合成。
  - [ ] 策划重装骑兵战马钢板护甲 `med_barding_steel`。
- [ ] **盾牌与格挡系统重置 (Shield Pack)**：
  - [ ] 实装民兵与轻步兵便携小圆盾 (Buckler)。
  - [ ] 实装主力骑士格挡熨斗盾 (Heater Shield)。
  - [ ] 实装弩手阵地防御大棑盾 (Pavise)。
  - [ ] 对原版盾牌格挡率、防具覆盖与持握 C++ 机制进行调研适配。
- [ ] **磨损、损害与高级铁匠维修服务系统**。
