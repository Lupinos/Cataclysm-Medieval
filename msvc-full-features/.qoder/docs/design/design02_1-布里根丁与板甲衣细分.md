# 策划案 002_1：布里根丁与板甲衣细分及抽象化重构

> 父策划案 → [design02-盔甲.md](design02-盔甲.md)
> 实现追踪 → [medieval_armor.md](../process/medieval_armor.md)

---

## 1. 背景与重构痛点

在目前的 `data/mods/Medieval` 中，躯干过渡期防御大类（Layer 3.5）仅包含两件物品：
1. `med_coat_of_plates`（以 `lc_steel` 低碳钢为主）
2. `med_brigandine`（以 `mc_steel` 中碳钢为主）

这与 14 - 15 世纪中世纪实际战术装备的丰富度差距较大。在历史上，这两类防具代表的并不是“两件衣服”，而是两种截然不同的**制作工艺哲学**和**演变生态**。
*   **板甲衣 (Coat of Plates)**：大钢板铆接，保护极佳，但由于大钢板无法扭转，极度影响敏捷和耐力，累赘度极高。
*   **布里根丁 (Brigandine)**：成百上千小钢鳞片重叠铆接，极为贴身灵活，累赘度极低，是敏捷流派与远程兵种的至爱。

为了提供更具可玩性、战术选择深度（Stamina 与 累赘度 博弈）以及符合阶层和材质梯度的防具体系，我们需要对这两类防具进行**深度细分**与**抽象化重构**。

---

## 2. 抽象基类 (Abstract Class) 设计与退化

### 2.1 退化决策：为什么原本无后缀的 `med_brigandine` 应当退化为纯抽象类？
1.  **定位模糊性**：随着“平民版”、“射手版”、“意式版”、“骑士天鹅绒版”布里根丁的细分引入，原本属性中庸、无特定阶层和工艺描述的 `med_brigandine` 失去了生存空间。如果保留它，玩家会在选择具体变体和这个“通用版”之间感到疑惑。
2.  **代码复用与维护 (DRY 原则)**：所有布里根丁都具有共通的 CDDA 属性（如 `type: ARMOR`、`category: armor`、覆盖躯干 `torso`、覆盖子部位 `torso_upper/lower`、覆盖率、默认的 flags `[ "VARSIZE", "OUTER", "STURDY", "FIT" ]` 等）。
    *   通过将无后缀的 `med_brigandine` 退化为抽象类 `med_brigandine_base`，我们可以将所有公共的 armor sections 和 flags 封装在内，具体子类只需通过 `copy-from` 继承，再局部替换 `description`、`material`、`thickness`、`encumbrance`、`price` 等个性化数据。
3.  **引用依赖安全性**：经调研，目前整个 mod 数据中**没有任何其他地方**（包含 recipes、professions、item_groups）直接引用 `med_brigandine`。这为我们进行彻底的抽象化重构提供了绝佳的“零阻力”契机。

### 2.2 抽象基类定义规划

我们将定义两个核心抽象基类，作为后续所有细分变体的“父类”。它们在运行时不会生成实体，但为子类提供底层骨架。

#### 抽象布里根丁基类 `med_brigandine_base`
```json
{
  "id": "med_brigandine_base",
  "type": "ARMOR",
  "abstract": "med_brigandine_base",
  "category": "armor",
  "symbol": "[",
  "looks_like": "platemail",
  "color": "red",
  "flags": [ "VARSIZE", "OUTER", "STURDY", "FIT" ],
  "armor": [
    {
      "covers": [ "torso" ],
      "specifically_covers": [ "torso_upper", "torso_lower" ],
      "coverage": 95
    }
  ]
}
```

#### 抽象板甲衣基类 `med_coat_of_plates_base`
```json
{
  "id": "med_coat_of_plates_base",
  "type": "ARMOR",
  "abstract": "med_coat_of_plates_base",
  "category": "armor",
  "symbol": "[",
  "looks_like": "platemail",
  "color": "brown",
  "flags": [ "VARSIZE", "OUTER", "STURDY", "FIT" ],
  "armor": [
    {
      "covers": [ "torso" ],
      "specifically_covers": [ "torso_upper", "torso_lower" ],
      "coverage": 95
    }
  ]
}
```

---

## 3. 细分实体物品设计

### 3.1 Coat of Plates (板甲衣) 系列：大钢板防线
大板钢铆，重点防护，牺牲灵活性。

1.  **`med_cuir_bouilli_coat_of_plates` (硬化皮板甲衣)**
    *   *背景*：在铁矿匮乏时或低阶土匪民兵中使用的廉价板甲衣。内部是用硬化皮革（`hardened_leather`）制成的大皮片。
    *   *材质*：`hardened_leather` (厚 4.0mm) + `leather` (厚 1.0mm 外罩)
    *   *属性*：累赘度 15，重量 4.5kg，造价低，不生锈，但对钝击保护弱，容易在火中受损。
2.  **`med_visby_coat_of_plates` (维斯比型板甲衣 / 经典低碳钢版)**
    *   *背景*：经典的 14 世纪过渡期板甲衣，复原自 1361 年维斯比战役遗迹，适合职业军士和下级骑士。
    *   *材质*：`lc_steel` (厚 1.5mm) + `leather` (厚 1.0mm 外罩)
    *   *属性*：累赘度 16，重量 9.0kg，防割防穿刺极强，但较笨重。
3.  **`med_heavy_coat_of_plates` (重型板甲衣 / 骑士枪比武甲)**
    *   *背景*：14 世纪末重装骑兵的骄傲。前胸是巨大的整体重叠钢板，带可拆卸枪托钩（Lance rest）。
    *   *材质*：`mc_steel` (厚 2.2mm) + `leather` (厚 1.2mm 外罩)
    *   *属性*：累赘度 19，重量 11.5kg，近战命中惩罚 `to_hit: -2`。极高的胸腔防护，需要极高的力量门槛，对耐力消耗巨大。

### 3.2 Brigandine (布里根丁 / 细鳞铆甲) 系列：贴身与灵活的极致
千鳞重叠，内铆工艺，完美支持敏捷流派。

1.  **`med_commoners_brigandine` (平民布里根丁 / 粗制钢片甲)**
    *   *背景*：普通雇佣步兵和民兵所能获得的极限防具。将废旧杂钢或回收钢片（`budget_steel`）铆在厚麻布或粗皮革内侧，没有复杂的装饰。
    *   *材质*：`budget_steel` (厚 1.2mm) + `leather` (厚 0.8mm 外罩)
    *   *属性*：累赘度 13，重量 8.0kg，造价及维修难度相对低廉。
2.  **`med_archers_brigandine` (轻型/射手布里根丁)**
    *   *背景*：专门为长弓手和轻装游侠设计。去掉了影响双臂发力及拉弓姿态的腋下和肩部铁片，侧面完全镂空或仅由布带、皮革连接。
    *   *材质*：`mc_steel` (厚 1.2mm) + `leather` (厚 0.6mm 外罩)
    *   *属性*：累赘度 8，覆盖率 80%，重量仅 5.0kg。不影响远程武器发力，且不易引起高温积汗。
3.  **`med_corrazina` (科拉齐纳 / 意式过渡铆甲)**
    *   *背景*：14 世纪末意大利和德意志地区极其流行的重型混合铆甲。侧面与腹部用指甲盖大小的灵活小片，前胸则由数块较大的异型钢板拼合。
    *   *材质*：`mc_steel` (厚 2.0mm 前胸 / 1.5mm 侧面) + `leather` (厚 0.8mm 外罩)
    *   *属性*：累赘度 14，重量 8.5kg，高额提升了前胸区域的正面防穿刺强度。
4.  **`med_knights_brigandine` (天鹅绒布里根丁 / 骑士华服甲)**
    *   *背景*：15 世纪贵族和精锐其实的身份象征。外覆精美的天鹅绒，所有铆钉都采用黄铜镀金雕花，内侧钢片经过镀锡防锈处理。
    *   *材质*：`mc_steel` (厚 1.8mm) + `leather` (厚 0.8mm 夹层) + `cotton` (天鹅绒外罩)
    *   *属性*：累赘度 11，重量 7.5kg，防护性能与高频动作灵活性达成黄金平衡。
5.  **`med_chalcis_brigandine` (查尔基斯复合铆甲)**
    *   *背景*：基于爱琴海查尔基斯要塞发现的 14 世纪实物。在布里根丁的侧胸和腹股沟部位使用小鳞片，但正面心肺位置是一块或两块完整的钢胸板，将布里根丁的灵动与板甲胸甲（Cuirass）的抗冲击力合二为一。
    *   *材质*：`mc_steel` (厚 2.0mm 胸板 / 1.5mm 鳞片) + `leather` (厚 0.8mm)
    *   *属性*：累赘度 13，重量 8.2kg。

### 3.3 Jack of Plates (杰克甲) 系列：绳系铁布甲
平民手工编缀，极其坚韧。

1.  **`med_jack_of_plates` (平民杰克甲)**
    *   *背景*：民兵与荒野求生者的最爱。不用昂贵的铆钉，而是将带有小孔的废铁片用麻绳缝在多层重磅亚麻布（`linen_quilted`）之间，外罩粗糙帆布。
    *   *材质*：`budget_steel` (厚 1.0mm 鳞片) + `linen_quilted` (厚 2.5mm 内衬) + `linen` (厚 1.0mm)
    *   *属性*：累赘度 15，重量 9.0kg。虽然稍微臃肿（累赘度大），但对钝击（Bash）的缓冲吸收能力达到了不可思议的高度（多层复合亚麻的阻尼作用）。

### 3.4 Mail (锁子甲) 细分系列：铁环交织的轻重博弈
锁子甲因重叠铁环，具备极高斩击吸收，但重量相对大且惧怕 bodkin arrow 等穿刺。通过细分，可以让不同战术流派各得其所。

1.  **`med_mail_shirt` (轻型锁子甲 / 锁子衬衫)**
    *   *背景*：短袖或无袖、长不及胯的轻型锁子甲，主要保护核心躯干，方便快速穿戴，深受弓弩手、轻骑兵喜爱。
    *   *材质*：`lc_steel_chain` (厚 1.2mm)
    *   *属性*：覆盖躯干 `torso`（ specifically_covers: torso_upper ）。累赘度 10，重量 6.5kg，防护足够且极大降低敏捷与发力惩罚。
2.  **`med_hauberk` (经典及膝锁子甲大衣 - 全身重构版)**
    *   *背景*：中世纪职业军士和骑士最传统、最信赖的主防具。长袖，裙摆及膝，开叉便于骑马。
    *   *材质*：`lc_steel_chain` (厚 1.2mm) + `leather` (厚 0.5mm)
    *   *属性*：完美覆盖 `torso`, `arm_l`, `arm_r`, `leg_l`, `leg_r`（修复此前仅护躯干的缺陷）。躯干累赘度 18，手臂 12，腿部 14。重量 13.5kg，全方位无缝高 Cut/Stab 混合防护。
3.  **`med_heavy_hauberk` (重型骑士双层锁甲 / 钢环长锁甲)**
    *   *背景*：精选材质与回火工艺极佳的中碳钢（`mc_steel_chain`）编织，并在胸前、腋下等关键致死部位使用双重穿环（Double Mail）加厚。
    *   *材质*：`mc_steel_chain` (厚 2.4mm / 两倍厚度环)
    *   *属性*：覆盖全身（covers: torso/arms/legs）。躯干累赘度 22，手臂 15，腿部 16。重量 18.0kg。极致的物理斩击与刺杀防御，但对耐力消耗是极大的负担。
4.  **`med_rust_mail` (锈蚀锁子甲 / 劣质锁甲)**
    *   *背景*：土匪、强盗在战场上搜刮来的劣质回炉杂钢锁甲。环扣缺乏保养严重锈蚀，常有脱环。
    *   *材质*：`budget_steel_chain` (厚 1.2mm)
    *   *属性*：覆盖躯干 `torso`。累赘度 12，重量 8.0kg，防护性能低下。

---

## 4. 配套肢体布里根丁防具

为了给选择“布里根丁灵活流派”的战士提供统一的配套美学和属性，我们将新增两款肢体防具：

1.  **`med_brigandine_arms` (布里根丁护臂)**
    *   *背景*：将细长钢片水平排列，铆接于皮革或锦缎织物袖筒内，覆盖前臂与上臂。
    *   *材质*：`mc_steel` (厚 1.2mm) + `leather` (厚 0.6mm)
    *   *属性*：覆盖双臂，累赘度 10。重量低于全钢板甲护臂（Vambrace + Spaulder），能极大减少蓄力攻击的耐力惩罚。关节处需要自配肘甲。
2.  **`med_brigandine_legs` (布里根丁护腿)**
    *   *背景*：鳞片铆接在大腿和小腿防线。
    *   *材质*：`mc_steel` (厚 1.2mm) + `leather` (厚 0.8mm)
    *   *属性*：覆盖双腿，累赘度 12。为奔跑、跨越障碍提供最贴身灵活的防护。

---

## 5. 数据及材质映射总矩阵

| 物品 ID | 继承父类 / 属性 | 材质等级 | 厚度 (板/皮/衬) | 累赘度 | 覆盖率 | 重量 (g) | 价格 | 备注与特化效果 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `med_cuir_bouilli_coat_of_plates` | `med_coat_of_plates_base` | hardened_leather | 4.0mm / 1.0mm / — | 15 | 90% | 4500 | 12000 | 极易制作，防火差，防酸抗锈 |
| `med_visby_coat_of_plates` | `med_coat_of_plates_base` | lc_steel | 1.5mm / 1.0mm / — | 16 | 95% | 9000 | 25000 | 经典款，防护厚重，偏累赘 |
| `med_heavy_coat_of_plates` | `med_coat_of_plates_base` | mc_steel | 2.2mm / 1.2mm / — | 19 | 95% | 11500 | 38000 | `to_hit: -2`，重装前胸极度防御 |
| `med_commoners_brigandine` | `med_brigandine_base` | budget_steel | 1.2mm / 0.8mm / — | 13 | 92% | 8000 | 18000 | 平民做工，造价与维修便宜 |
| `med_archers_brigandine` | `med_brigandine_base` | mc_steel | 1.2mm / 0.6mm / — | 8 | 80% | 5000 | 28000 | 轻巧，完美契合远程拉弓角色 |
| `med_corrazina` | `med_brigandine_base` | mc_steel | 2.0mm / 0.8mm / — | 14 | 93% | 8500 | 35000 | 正面多重组合防护，防穿刺极佳 |
| `med_knights_brigandine` | `med_brigandine_base` | mc_steel | 1.8mm / 0.8mm / 0.5mm | 11 | 95% | 7500 | 50000 | 顶级工艺，天鹅绒，高社会价值 |
| `med_chalcis_brigandine` | `med_brigandine_base` | mc_steel | 2.0mm / 0.8mm / — | 13 | 95% | 8200 | 45000 | 复合前板，防御与灵活的最佳兼顾 |
| `med_jack_of_plates` | (独立定义) | budget_steel | 1.0mm / 1.0mm / 2.5mm | 15 | 92% | 9000 | 8000 | 平民自制，高 Bash 吸收缓冲 |
| `med_mail_shirt` | (独立定义) | lc_steel_chain | 1.2mm / — / — | 10 | 95% | 6500 | 22000 | 轻型无袖锁甲，高灵活性 |
| `med_hauberk` | (全身重构) | lc_steel_chain | 1.2mm / 0.5mm / — | 18/12/14 | 95% | 13500 | 35000 | 及膝长袖长锁甲，覆盖四肢 |
| `med_heavy_hauberk` | (全身重构) | mc_steel_chain | 2.4mm / — / — | 22/15/16 | 98% | 18000 | 55000 | 双层锁甲，防砍防刺极其强悍 |
| `med_rust_mail` | (独立定义) | budget_steel_chain | 1.2mm / — / — | 12 | 90% | 8000 | 9000 | 废杂钢锁甲，易脱环，高负荷 |
| `med_brigandine_arms` | (独立定义) | mc_steel | 1.2mm / 0.6mm / — | 10 | 90% | 3200 | 20000 | 双臂防护，不限灵活 |
| `med_brigandine_legs` | (独立定义) | mc_steel | 1.2mm / 0.8mm / — | 12 | 90% | 4500 | 26000 | 双腿防护，完美奔跑与屈膝 |
