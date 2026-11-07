# design04_1-quality体系：旧技术方案

> 来源：`archive/medieval-before-redo`。仅供重新设计时查阅，未迁入新基线；旧接口、数据及数值推演须重新核验。完整旧稿保存在该分支的 `msvc-full-features/.qoder/docs/`。本页不表示当前实现状态。

## 二、CDDA 现行机制

### 2.1 武器：伤害是 item 自带属性，材料影响耐久

```json
// mc_broadsword（基准定义）
material: [mc_steel]
melee_damage: { bash: 6, cut: 28 }     ← 写死在 item 上
chip_resist 由材料决定（mc_steel = 18）

// hc_broadsword（copy-from mc_broadsword）
replace_materials: { mc_steel → hc_steel }  ← 耐久提升
relative: { melee_damage: { cut: +1 } }     ← 手动微调伤害
```

**结论：武器攻击力不由材料自动计算，是手写的。** 材料变体通过 `copy-from` + `replace_materials` + `relative` 派生，成本很低（3 行一个变体）。

### 2.2 装甲：防护力由材料 resist × 厚度自动计算

```json
// armor_hc_brigandine（copy-from lc 基准）
replace_materials: { lc_steel → hc_steel }
→ 防护 = hc_steel.resist × 1.0 = { bash:10, cut:10, bullet:6.5 }
```

**结论：装甲防护完全由材料自动决定。** 换材料 = 换防护。

### 2.3 CDDA 钢材 resist 一览

| 材料 | bash | cut | chip_resist | 定位 |
|------|------|-----|-------------|------|
| budget_steel | 6 | 6 | 11 | 废料钢 |
| lc_steel | 6 | 6 | 17 | 低碳钢 |
| mc_steel | 7 | 7 | 18 | 中碳钢 |
| hc_steel | 10 | 10 | 18 | 高碳钢 |
| ch_steel | 10 | 10 | 20 | 表面硬化钢 |
| qt_steel | 11 | 11 | 20 | 淬火回火钢 |
| steel（泛称） | 6 | 6 | 20 | 工业钢泛称 |

---

## 四、最终决策

### 决策 1：材料体系沿用 CDDA 原版

中世纪 mod 的装备使用 CDDA `data/json/materials.json` 中定义的完整钢材体系（budget_steel ~ qt_steel，含 steel 泛称共 7 种以及生铁和铜等）。

每种武器的不同钢材版本通过 `copy-from` + `replace_materials` + `relative` 派生。**材料的差异在 JSON 中静态定义。**

### 决策 2：Quality 作为纯运行时属性

Quality **不写入任何 JSON 文件**，以避免质量 × 材料的组合爆炸。

Quality 是 item 实例的运行时属性，存储于 `item_vars`，存档兼容。

### 决策 3：Quality 效果可配置，区分武器与盔甲

| 维度 | 武器 | 盔甲 |
|------|------|------|
| 核心影响 | 伤害（melee_damage）| 累赘度（encumbrance）|
| 核心影响 | 速度（attack_speed） | 覆盖度（coverage） |
| 次要影响 | 暴击修正 | 厚度等效修正 |
| 可否配置 | 每个 quality 等级可配置不同乘数 | 每组装备类型可配置不同权重 |

### 决策 4：不在初版实现

Quality 系统推迟到后续版本。初版只使用 JSON 材料变体（决策 1）区分装备品质。这样做的理由是：

- 初版聚焦「世界只剩荒野」→「中世纪内容从零生长」的核心闭环
- 材料变体（`copy-from`）已能提供足够的装备差异化
- Quality 运行时系统涉及 C++ 改动（damage_melee、armor 计算、UI、配方），推迟后可作为独立迭代交付

### CDDA 耐久度机制调研（附录，供 quality 降级参考）

CDDA 的耐久度系统已经比较完善，核心要素如下：

**damage 模型：** 物品 damage 为 int 值（0-4000），`damage_scale = 1000`（每级）。`damage_level()` 返回 0-5 级：
```
damage = 0         → level 0（完好）
damage = 1-999     → level 1（微损）
damage = 1000-1999 → level 2（受损）
damage = 2000-2999 → level 3（破损）
damage = 3000-3999 → level 4（严重）
damage = 4000      → level 5（摧毁）
```
`damage_max_` 固定为 4000，不可 JSON 配置（硬编码）。

**damage 对性能的惩罚（已内置）：**
- 近战武器伤害：`× (1.0 - 0.1 × max(0, damage_level - 1))` — 每级 -10%
- 远程伤害：`- 2 × max(0, damage_level - 1)` — 每级 -2 点
- 护甲 resist：`× (1.0 - 0.125 × max(0, damage_level - 1))` — 每级 -12.5%

**近战磨损触发（`melee.cpp:201`）：**
```
damage_chance = stat_factor × material_factor / wear_multiplier
```
- `stat_factor = DEX/2 + skill_melee + 64/max(arm_str, 4)` — DEX 和近战技能越高，武器越不易损坏（合理）
- `material_factor = chip_resistance()` — `chip_resist` 越高，越耐打（合理）
- 判定：`!one_in(damage_chance)` → 触发 `inc_damage()` → damage +1000（跳 1 级）

**耐久度相关的 JSON flag：**

| Flag | 效果 | 建议 |
|------|------|------|
| `DURABLE_MELEE` | damage_chance × 4 → 武器寿命 4 倍 | **中世纪武器全部移除此 flag** |
| `UNBREAKABLE_MELEE` | 近战完全不会损坏 | **中世纪武器全部移除此 flag** |
| `UNBREAKABLE` | 任何途径都不会损坏 | 保留给极少数特殊物品 |
| `FRAGILE_MELEE` | material_factor = chip_resist / 6 → 极易损坏 | 可选用于农具、临时武器 |

**永久降级（degradation）：** 物品每次受损时，`degradation_` 也会增加，降低可修复上限。物品最大修复次数由 `degrade_increments`（默认 50）控制。JSON 字段 `degradation_multiplier` 可加速此过程。

**材质 `chip_resist` 一览：**

| 材料 | chip_resist |
|------|-------------|
| budget_steel | 11 |
| lc_steel | 17 |
| mc_steel | 18 |
| hc_steel | 18 |
| ch_steel | 20 |
| qt_steel | 20 |
| steel | 20 |
| iron | ~12 |

**初版调参建议：** 耐久度下降机制本身是合理的，不需要覆写 C++ 逻辑。只需要在 JSON 层面做三件事：
1. **移除 `DURABLE_MELEE` 和 `UNBREAKABLE_MELEE`** — 中世纪武器没有「永不磨损」的概念
2. **可选：降低 `chip_resist` 值** — 在 mod 中覆写材料定义，把各钢材的 `chip_resist` 降低 30-50%，刃器会更频繁地卷口崩刃
3. **可选：提高 `degradation_multiplier`** — 加速永久降级，使修理次数更有限

其中第 1 点是必须做的（否则「一甲传三代」无法解决），第 2/3 点视初版手感反馈再调。

---

## 六、与武器策划案的关系

本决策确认后，`design04-武器.md` 中的武器定义不需要预留 quality 字段。每种武器只需定义其**标准钢材版本**的 melee_damage 基准值，其余钢材变体通过 `copy-from` 派生。

武器清单中涉及的伤害数值均为「mc_steel + Normal quality」基准。

### 5.2 实现思路

- Quality 存于 `item::item_vars`（`std::map<string,string>`），序列化兼容
- 物品生成时计算：制造技能 → 加权随机 quality，NPC 掉落 → faction/身份决定分布
- 战斗/护甲公式末尾乘 quality 系数（方案 B：公式修正因子）
- UI 在 `tname()` 插入品质前缀（颜色区分）

### 5.4 与 CDDA 材料变体的关系

```
JSON 静态层（初版实现）：
  lc_broadsword、mc_broadsword、hc_broadsword ...
  → 不同的 damage / chip_resist / 重量

Quality 运行时层（远期）：
  同一把 mc_broadsword 可能有 SHODDY → MASTER 五种品质
  → 在 JSON 基准值上乘以品质系数
```

两层正交，互不替代。

---
