# 中世纪平民与日常衣物体系实现进度

> 策划案 → [design03-日常衣物.md](../design/design03-日常衣物.md)
> 总任务追踪 → [core_work.md](../../rules/core_work.md)

本进度文档记录中世纪模组中**所有日常/民用衣物服装项（共 37 件）**的实装现状与未来规划。战术防具参见 [medieval_armor.md](medieval_armor.md)。

---

## 一、 中世纪日常衣物总索引 (Civilian Clothing Index)

目前日常衣物系统已实装 **29 件核心衣物 + 2 种中世纪新材质**。通过此总表可以快速浏览全部现状。

### 1. 材质与底层资源 (Materials)
| 材质 ID | 中文/英文名称 | 基础复制模板 | 用途与定位 | 状态 |
| :--- | :--- | :---: | :--- | :---: |
| `straw` | 草编材料 (`Straw`) | cotton | 用于草帽等，高透气极低防护。 | `[x]` 已实装 |
| `oilcloth` | 防雨油布 (`Oilcloth`) | linen | 涂油重布，超高防风雨，透气差。 | `[x]` 已实装 |

### 2. 头部、躯干与外衣 (Head & Torso)
| 物品 ID | 中文/英文名称 | 覆盖部位 | 主要材质 | 累赘度 | 保暖值 | 状态 | 备注 / 现状 |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `med_coif_linen` | 亚麻贴帽 | 头部 | linen | 0 | 5 | `[x]` | 农民及军士常用的吸汗底层头套。 |
| `med_hat_straw` | 草编防晒帽 | 头部 | straw | 0 | 0 | `[x]` | 农夫夏日防晒草帽，高透气。 |
| `med_cap_felt` | 羊毛毡帽 | 头部 | wool | 0 | 10 | `[x]` | 经典平民及市民软毡帽。 |
| `med_hood_wool` | 羊毛兜帽风帽 | 头部、颈部 | wool | 0 | 15 | `[x]` | 经典披肩式防风保暖羊毛兜帽。 |
| `med_chaperon` | 沙佩龙卷檐帽 | 头部 | wool | 0 | 12 | `[x]` | 15世纪初流行的扭结卷檐风帽。 |
| `med_coif_leather`| 皮贴帽 | 头部 | leather | 0 | 8 | `[x]` | 贴耳小皮帽。 |
| `med_shirt_linen` | 亚麻衬衫 | 躯干、双臂 | linen | 1 | 5 | `[x]` | 通用亚麻内衬内衣。 |
| `med_braies_linen` | 亚麻内裤 | 臀部、大腿 | linen | 1 | 5 | `[x]` | 分体式亚麻短裤。 |
| `med_chemise_linen`| 亚麻女衬衫 | 躯干、腿部 | linen | 1 | 8 | `[x]` | 妇女底层亚麻内衬长裙。 |
| `med_tunic_wool` | 羊毛短衫外套 | 躯干 | wool | 1 | 15 | `[x]` | 通用中外层保暖短衫。 |
| `med_tunic_linen` | 亚麻短衫外套 | 躯干 | linen | 1 | 8 | `[x]` | 夏季外穿或工作短衫。 |
| `med_doublet` | 紧身武装衣 | 躯干、双臂 | linen_quilted | 3 | 12 | `[x]` | 精致绗缝紧身上衣，可武装板甲。 |
| `med_kirtle` | 柯特尔长袍外衣 | 躯干、双腿 | wool | 2 | 20 | `[x]` | 中世纪经典长袍外套。 |
| `med_apron_work` | 麻布工作裙 | 躯干、大腿 | linen | 1 | 5 | `[x]` | 农活及家务麻布罩裙。 |
| `med_apron_leather`| 铁匠防溅皮裙 | 躯干、大腿 | leather | 4 | 10 | `[x]` | 铁匠、石匠重皮裙，高阻燃。 |

### 3. 肢体、手足与腰带饰品 (Limb, Hands, Feet & Belt)
| 物品 ID | 中文/英文名称 | 覆盖部位 | 主要材质 | 累赘度 | 状态 | 备注 / 现状 |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `med_hose_wool` | 羊毛长统袜 | 双腿 | wool | 1 | `[x]` | 平民经典紧身统袜。 |
| `med_hose_split` | 分离式统袜 | 双腿 | wool | 1 | `[x]` | 用带子系挂在 braies 上的经典统袜。 |
| `med_hose_joined` | 连裆长统统袜裤 | 臀部、双腿 | wool | 2 | `[x]` | 连体式羊毛统袜裤。 |
| `med_leg_wraps` | 护腿裹腿带 | 小腿 | wool | 1 | `[x]` | 绑腿羊毛带，防滑防割。 |
| `med_footwraps` | 亚麻足缠 | 双足 | linen | 2 | `[x]` | 基础裹脚布。 |
| `med_turnshoes` | 翻缝皮便鞋 | 双足 | leather | 2 | `[x]` | 经典平民皮鞋（缝好后翻转过来）。 |
| `med_ankle_boots` | 皮质系带踝靴 | 双足 | leather | 4 | `[x]` | 通用皮高帮便鞋。 |
| `med_pattens` | 泥地木套鞋 | 双足 | wood | 5 | `[x]` | 套在皮鞋外的防脏木板底厚木鞋。 |
| `med_mittens_wool` | 羊毛保暖手套 | 双手 | wool | 2 | `[x]` | 基础防冻羊毛并指手套。 |
| `med_wristwraps` | 亚麻护腕缠带 | 手腕 | linen | 1 | `[x]` | 劳作绑手，吸汗减震。 |
| `med_cloak_wool` | 羊毛斗篷 | 躯干、双臂 | wool | 2 | `[x]` | 经典连帽宽大羊毛外摆。 |
| `med_cloak_oilcloth`| 油布防雨斗篷 | 躯干、双臂 | oilcloth | 3 | `[x]` | 涂油重防风雨雨衣斗篷。 |
| `med_shawl_wool` | 羊毛披肩 | 躯干 | wool | 1 | `[x]` | ✅ 已实装 |
| `med_cloak_fur` | 兽皮防寒斗篷 | 躯干、双臂 | fur | 4 | `[x]` | 极度保暖的皮草风衣。 |
| `med_belt_leather` | 皮腰带 | 腰部 | leather | 0 | `[x]` | 经典系带皮带，无储物槽。 |
| `med_belt_rope` | 粗绳束腰带 | 腰部 | cotton | 0 | `[x]` | 穷人及僧侣用粗绳。 |
| `med_pouch_belt` | 腰带挂载随身包 | 腰挂 | leather | — | `[ ]` | 挂载储物包 (CONTAINER)。 📅 **计划中** |
| `med_scrip_bag` | 斜挎朝圣布包 | 双肩斜跨 | linen | — | `[ ]` | 穷人及信徒储物包 (CONTAINER)。 📅 **计划中** |
| `med_waterskin` | 缝皮水囊袋 | 侧挂 | leather | — | `[ ]` | 经典储水工具 (TOOL/CONTAINER)。 📅 **计划中** |
| `med_tinder_pouch` | 便携火绒火石袋 | 腰挂 | leather | — | `[ ]` | 基础生火工具包 (TOOL)。 📅 **计划中** |
| `med_tabard` | 罩衫战袍斗篷 | 最外层 | linen | 0 | `[ ]` | 骑士徽章战衣外罩。 📅 **计划中** |

---

## 二、 日常衣物开发阶段 Checklist

日常衣物系统分为三个清晰阶段：

### 阶段 1：平民基础衣物及新材料实装
- [x] 实装中世纪核心两大平民新材料：草料 (`straw`)、油布 (`oilcloth`)。
- [x] 实装头部与内衣层：coif 帽、羊毛风帽、亚麻衬衫女衬衫等。
- [x] 实装平民外穿短衫：羊毛短衫 tunic、长裙 kirtle、紧身武装 doublet。
- [x] 实装统袜大类：split hose、joined hose 及 leg wraps 缠腿。
- [x] 实装民间鞋子：裹脚布、turnshoes 翻缝皮鞋、泥地木套鞋 pattens。
- [x] 实装外层及披肩：羊毛斗篷、油布斗篷、兽皮防寒大氅。
- [x] 实装基础腰带、保暖手套及护腕缠带。

### 阶段 2：随身储物与生存小挂件扩展 (将要做)
- [ ] **实装中世纪容器类 (CONTAINER) 挂件**：
  - [ ] 策划并写出腰带皮挂包 `med_pouch_belt`，提供基础储物体积。
  - [ ] 策划斜挎麻包 `med_scrip_bag`，支持挂在双肩外侧。
  - [ ] 实装缝皮便携水袋 `med_waterskin`，支持在溪流装水。
- [ ] **实装基础荒野求生挂件 (TOOL)**：
  - [ ] 策划火石火绒袋 `med_tinder_pouch`，作为中世纪极简的自制生火工具。
  - [ ] 策划腰挂木扎啤杯 `med_tankard`。

### 阶段 3：身份外袍与徽章系统 (将要做)
- [ ] **实装纹章罩衫 `med_tabard`**：支持印制不同领主/冒险者公会的图腾，并与 NPC faction 产生互动。
- [ ] **实装徽章/挂件饰品 `med_badge`**：作为信用及声望凭证。
