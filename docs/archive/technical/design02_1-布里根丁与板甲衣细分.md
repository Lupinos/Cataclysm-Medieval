# design02_1-布里根丁与板甲衣细分：旧技术方案

> 来源：`archive/medieval-before-redo`。仅供重新设计时查阅，未迁入新基线；旧接口、数据及数值推演须重新核验。完整旧稿保存在该分支的 `msvc-full-features/.qoder/docs/`。本页不表示当前实现状态。

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
