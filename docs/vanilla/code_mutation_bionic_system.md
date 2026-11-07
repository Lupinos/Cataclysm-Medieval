# 变异与生化改造系统 (Mutations & Bionics)

> Cataclysm-Medieval 的变异、阈值突破、生化模块系统

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/mutation.h` / `src/mutation.cpp` | 变异/特质定义、类别、阈值 |
| `src/mutation_data.cpp` | 变异数据加载 |
| `src/mutation_ui.cpp` | 变异 UI |
| `src/bionics.h` / `src/bionics.cpp` | 生化模块（CBM）定义与管理 |
| `src/bionics_ui.cpp` | 生化模块 UI |
| `src/suffer.cpp` | 变异带来的被动效果（受苦系统） |

---

## 变异体系 (mutation_branch)

### 核心结构 (`mutation.h:172-577`)

| 属性分类 | 属性 | 说明 |
|----------|------|------|
| **基础** | `id` | 变异 ID |
| | `valid` | 是否有效 |
| | `points` | 角色创建花费点数 |
| | `startingtrait` | 是否可在角色创建时选择 |
| | `purifiable` | 净化剂是否可移除 |
| | `threshold` | 是否为阈值突变 |
| | `profession` | 是否为职业专属 |
| | `vanity` | 是否纯装饰（可随时更改） |
| | `mixed_effect` | 是否同时有正面和负面效果 |
| **激活** | `activated` | 是否可主动激活 |
| | `starts_active` | 获得时是否自动激活 |
| | `cost` / `cooldown` | 激活消耗与冷却 |
| | `fatigue` / `hunger` / `thirst` | 消耗疲劳/饥饿/口渴 |
| **属性修正** | `str_modifier` | 力量倍率（不影响 HP） |
| | `hp_modifier` / `hp_adjustment` | HP 倍率/加成 |
| | `mana_modifier` / `mana_multiplier` | 法力修正 |
| | 各种 `modifier` | 闪避、移动消耗、负重、听力等 |
| **战斗** | `cut_dmg_bonus` / `bash_dmg_bonus` | 近战伤害加成 |
| | `pierce_dmg_bonus` | 穿透伤害加成 |
| | `armor` | 按身体部位的护甲值 |
| | `attacks_granted` | 特殊攻击（mut_attack） |
| **生存** | `craft_skill_bonus` | 制造技能加成 |
| | `healing_awake` / `healing_multiplier` | 治疗倍率 |
| | `metabolism_modifier` | 代谢速率倍率 |
| | `thirst_modifier` / `fatigue_modifier` | 口渴/疲劳倍率 |
| | `stamina_regen_modifier` | 体力恢复倍率 |
| | `stomach_size_multiplier` | 胃容量倍率 |
| | `weakness_to_water` | 遇水伤害 |
| | `temperature_speed_modifier` | 温度对速度影响 |
| **社交** | `social_mods` | 社交修正（说谎/说服/恐吓） |
| | `visibility` / `ugliness` | 可见度/丑陋度 |
| | `ignored_by` / `anger_relations` | 物种无视/仇恨 |
| **限制** | `restricts_gear` | 哪些身体部位需要 OVERSIZE 装备 |
| | `destroys_gear` | 是否摧毁受限部位的装备 |
| | `can_only_eat` | 限制可食用材料 |
| | `no_cbm_on_bp` | 禁止安装生化模块的身体部位 |
| | `conflicts_with_item()` | 是否与某物品冲突 |
| **法术** | `spells_learned` | 获得变异时学会的法术 |
| | `enchantments` | 变异附魔 |
| | `activated_eocs` | 激活时触发的效果链 |

### 变异攻击 (mut_attack)

`mut_attack` 结构 (`mutation.h:57-79`)：
- `attack_text_u` / `attack_text_npc` — 触发时显示的文本
- `required_mutations` / `blocker_mutations` — 前置/冲突变异
- `bp` — 需要裸露的身体部位
- `chance = one_in(chance - dex - unarmed)` — 触发概率
- `base_damage` — 基础伤害
- `strength_damage` — 力量加成伤害

### 变异类别 (mutation_category_trait)

`mutation_category_trait` 结构 (`mutation.h:579-617`)：

每个变异类别（如 BIRD、CHIMERA、FELINE 等）：
- `id` — 类别 ID
- `threshold_mut` — 突破阈值后获得的特质
- `vitamin` — 变异催化剂（维生素）
- `threshold_min` — 突破阈值所需维生素量（默认 2200）
- `base_removal_chance` — 移除基础特质的概率
- `mutagen_message` — 使用诱变剂时的消息

### 突变方式 (mutagen_technique)

```cpp
enum class mutagen_technique {
    consumed_mutagen,   // 饮用诱变剂
    injected_mutagen,   // 注射诱变剂
    consumed_purifier,  // 饮用净化剂
    injected_purifier,  // 注射净化剂
    injected_smart_purifier, // 智能净化剂
};
```

---

## 变异转换 (mut_transform)

`mut_transform` 结构 (`mutation.h:81-95`)：

一些变异可以**主动转化为另一种形态**：
- `target` — 转化目标 trait
- `active` — 转化后是否激活
- `moves` — 消耗行动点
- `safe` — 是否安全（遵循正常变异规则）

---

## 生化模块 (Bionics)

### bionic_data 结构 (`bionics.h:30-201`)

| 属性分类 | 属性 | 说明 |
|----------|------|------|
| **能量** | `power_activate` | 激活时消耗能量 |
| | `power_deactivate` | 关闭时消耗能量 |
| | `power_over_time` | 持续消耗（需 charge_time > 0） |
| | `power_trigger` | 触发特殊效果时消耗 |
| | `power_trickle` | 每回合被动产电 |
| | `capacity` | 内置电池容量 |
| **燃料** | `fuel_opts` | 可用燃料类型 |
| | `fuel_efficiency` | 燃料转化效率 |
| | `passive_fuel_efficiency` | 被动燃料转化率 |
| | `exothermic_power_gen` | 发电时是否产热 |
| | `is_remote_fueled` | 是否通过电缆供电 |
| **安装** | `occupied_bodyparts` | 占用的身体部位插槽 |
| | `encumbrance` | 造成的累赘 |
| | `installation_requirement` | 安装需求（工具/技能） |
| | `mutation_conflicts` | 冲突的变异 |
| | `canceled_mutations` | 安装后移除的变异 |
| | `required_bionic` | 前置生化模块 |
| **升级** | `upgraded_bionic` | 可升级到的模块 |
| | `available_upgrades` | 可用的升级选项 |
| **功能** | `activated` | 是否可主动开关 |
| | `stat_bonus` | 被动属性加成 |
| | `env_protec` | 环境防护 |
| | `protec` | 伤害抗性 |
| | `learned_spells` | 安装后学会的法术 |
| | `enchantments` | 模块附魔 |
| | `fake_weapon` | 假体武器 |
| | `passive_pseudo_items` / `toggled_pseudo_items` | 伪物品 |

### 安装与难度

`bionic_success_chance()` / `bionic_manip_cos()` (`bionics.h:284-285`)：

安装生化模块需要：
- **手术技能** (skill level)
- **模块难度** (difficulty)
- 使用自动医生 (autodoc) 与否影响成功率

---

## 变异与生化模块的交互

- 变异可以 `no_cbm_on_bp` 阻止在特定身体部位安装生化模块
- 生化模块可以 `canceled_mutations` 移除冲突变异（如增强视觉模块取消远视）
- 生化模块可以 `mutation_conflicts` 阻止安装时已有某些变异
- 卸除模块时可以 `give_mut_on_removal` 给予变异

---

## 人格分数 (mut_personality_score)

突变可以被**人格分数**限制：

| 人格维度 | 范围 |
|----------|------|
| aggression | 攻击性 (-10 ~ 10) |
| bravery | 勇敢 (-10 ~ 10) |
| collector | 收集癖 (-10 ~ 10) |
| altruism | 利他性 (-10 ~ 10) |
