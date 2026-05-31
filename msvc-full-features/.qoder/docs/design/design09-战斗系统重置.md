# 战斗系统深度重置：手动技艺选择 + 部位瞄准

> 基于 [code_combat_system.md](../vanilla/code_combat_system.md) 和 [json_martial.md](../vanilla/json_martial.md) 的 Medieval Mod 战斗系统策划。
> 需求来源：近战手动技艺选择 + 部位瞄准系统，构建 CDDA 原版没有的"精确攻击"机制。

---

## 一、需求概述

改造 CDDA 近战流——从"移动撞上去、系统自动决定一切"变为**玩家可以主动选择技艺和目标部位**。通过"技艺选择 → 部位选择"两轮 UI，增加战斗的策略深度。

核心公式：
```
瞄准部位权重 = hit_size × n
命中惩罚 = hit_spread - k
```

其中 `n`（精准度放大）和 `k`（命中惩罚）受技能线性缩放。

---

## 二、触发方式

### 2.1 双通道设计

| 操作 | 行为 |
|------|------|
| **Tab / 移动撞敌** | 原版自动攻击：技艺随机 + 部位随机，流程不变 |
| **新快捷键（如 `Alt+F`）** | 进入"精确攻击"模式：选择敌人 → 选择技艺 → 选择部位 → 执行攻击 |

新快捷键的行为类似原版 `f` 射击——先进入目标选择模式，选中目标后再弹出子菜单。

### 2.2 精确攻击流程

```
玩家按下 Alt+F
    │
    ├── ① 目标选择（类似 f 射击的 trajectory 模式）
    │      └─ 显示可攻击范围内的 NPC/敌对生物
    │      └─ 仅限非 monster 的目标（即 Character / NPC）
    │
    ├── ② 技艺选择 UI
    │      ├─ 列出当前可用的所有技艺（已过滤：条件满足 + 技能够 + 武器/流派匹配）
    │      ├─ 每项显示：名称、movecost、伤害倍率、效果简述、攻击肢体
    │      ├─ 选择方式：方向键高亮 + Enter 确认
    │      └─ 取消键（Esc）返回上一步
    │
    ├── ③ 部位选择 UI
    │      ├─ 列出目标的所有身体部位（按 anatomy 定义）
    │      ├─ 如果技艺有 targetable_body_parts 白名单 → 仅显示可打部位
    │      ├─ 每项显示：部位名称、预估命中率（基于 n/k 计算）
    │      ├─ 默认高亮：躯干（torso）
    │      └─ 取消键（Esc）返回上一步
    │
    └── ④ 执行攻击
           ├─ 使用选定的技艺（强制 tech_id）
           ├─ 修改部位权重：目标部位 hit_size × n
           ├─ 应用命中惩罚：hit_spread -= k
           └─ 其余流程走原版 melee_attack_abstract()
```

### 2.3 适用范围

- **仅玩家可用**（NPC 继续走自动选择逻辑）
- **仅对 Character/NPC 目标可用**（monster 走原版流程，后续可扩展）
- 徒手 + 有流派 → 可用技艺
- 徒手 + 无流派 → 技艺列表为空时跳过技艺选择，直接进入部位选择

---

## 三、技艺选择 UI

### 3.1 过滤规则

从 `get_all_techniques()` 获取候选池后，按以下规则过滤（复用现有 `evaluate_techniques()` 逻辑，但在 UI 前预执行）：

1. **技能门槛**：`skill_requirements` 不满足 → 不显示
2. **武器匹配**：`melee_allowed` / `unarmed_allowed` / `weapon_categories_allowed` → 不匹配不显示
3. **条件判定**：`condition` 不满足 → 不显示（如"目标倒地才可用"在非倒地目标不显示）
4. **攻击肢体可用**：`attack_vectors` 对应的身体部位必须健康（`can_use_attack_vector()` 检查）→ 不健康不显示
5. **特殊标记**：
   - `crit_tec` = true 的技艺标注 ⚡（仅暴击时可触发，但预先显示供参考）
   - `defensive` = true 的技艺不显示（防御技不能主动发起）

### 3.2 UI 布局

```
┌─────────────────────────────────────────┐
│ 选择技艺 — [流派: 德国长剑术]  [武器: 长剑]  │
├────┬────────────────────────────────────┤
│ >  │ 强劈 (Oberhau)        85 move     │
│    │ 伤害 1.5×  |  可发动暴击           │
│    │ 攻击肢体: WEAPON                   │
│    │                                    │
│    │ 横斩 (Mittelhau)       80 move     │
│    │ 伤害 1.0×  |  范围: wide          │
│    │ 攻击肢体: WEAPON                   │
│    │                                    │
│    │ 刺击 (Thrust)          90 move     │
│    │ 伤害 0.8×  |  护甲穿透 +5          │
│    │ 攻击肢体: WEAPON                   │
│    │                                    │
│    │ 柄头打击 (Mordhau)      70 move    │
│    │ 伤害类型: bash  |  击晕 1回合       │
│    │ 攻击肢体: WEAPON                   │
│    │                                    │
│    │ 斩腿 (Low Cut) ⚡       65 move    │
│    │ 仅暴击  |  击倒 2回合              │
│    │ 攻击肢体: WEAPON  |  可瞄准: 腿     │
├────┴────────────────────────────────────┤
│  Enter: 确认  Esc: 取消  Tab: 跳过(自动) │
└─────────────────────────────────────────┘
```

### 3.3 特殊处理

- **无可用技艺**：跳过此界面，直接进入部位选择
- **仅 1 个技艺**：自动选中但不跳过——仍然显示让玩家确认
- **`crit_tec` 标记的技艺**：显示但标注"暴击时触发"，玩家仍可选择——如果攻击最终没有暴击，技艺不生效（退化为普通攻击）

---

## 四、部位选择 UI

### 4.1 白名单限制

技艺 JSON 新增可选字段 `targetable_body_parts`（字符串数组）：

```json
{
  "id": "tec_low_cut",
  "type": "technique",
  "name": "斩腿",
  "targetable_body_parts": ["leg_l", "leg_r", "foot_l", "foot_r"],
  "...": "..."
}
```

- **未声明** → 所有部位可选
- **声明了** → 仅列出白名单中的部位（不在此列的灰掉不可选）
- `attack_vectors` 的健康检查（四肢残废不能打）仍然执行

### 4.2 预估命中率显示

基于当前 `hit_roll` 和 `hit_difficulty` 计算预估命中率：

```
预估命中率 = (hit_roll - k) / (target_dodge + size_penalty) 的大致胜率
简化显示：极高 (>90%) / 高 (70-90%) / 中 (40-70%) / 低 (15-40%) / 极低 (<15%)
```

显示文案示例：

```
┌─────────────────────────────────────────┐
│ 瞄准部位 — [目标: 强盗]                    │
├────┬────────────────────────────────────┤
│ >  │ 躯干 (torso)         命中: 高 85%   │
│    │ 部位效果: winded, staggered        │
│    │                                    │
│    │ 头部 (head)          命中: 中 52%   │
│    │ 部位效果: stunned, bleed           │
│    │                                    │
│    │ 左腿 (leg_l)         命中: 高 78%   │
│    │ 部位效果: downed, bleed            │
│    │                                    │
│    │ 右臂 (arm_r)         命中: 中 65%   │
│    │ 部位效果: downed                   │
│    │                                    │
│    │ 左手 (hand_l) ⛔                   │
│    │ 技艺 "斩腿" 不可瞄准此部位           │
├────┴────────────────────────────────────┤
│  Enter: 确认  Esc: 返回技艺选择           │
└─────────────────────────────────────────┘
```

---

## 五、数值设计

### 5.1 核心公式

```
部位权重 = hit_size × n           （n > 1，放大了目标部位被命中的概率）
命中判定 = hit_spread - k          （k > 0，瞄准需要分心——降低整体命中质量）
```

- **n**：精准度放大倍数。值越大，攻击越集中到目标部位
- **k**：命中惩罚值。值越大，瞄准时越容易 miss（"瞄得越细，越容易落空"）

### 5.2 基准值（技能 5 级，约中等水准）

| 参数 | 值 | 说明 |
|------|---|------|
| n | 10 | hit_size × 10：躯干权重 360/456≈79%，头部 40/136≈29% |
| k | 17.5 | hit_spread 扣减 17.5（中等惩罚） |

### 5.3 技能线性缩放

**设计原则**：高技能 = 更精准的瞄准 + 更少的惩罚

| 技能等级 | n | k | 头部命中率(估) | 躯干命中率(估) |
|----------|---|----|--------------|--------------|
| 0 (新手) | 3 | 30 | ~5% | ~60% |
| 3 (入门) | 6.6 | 22.5 | ~10% | ~68% |
| 5 (中等) | 9 | 17.5 | ~15% | ~75% |
| 7 (熟练) | 11.4 | 12.5 | ~22% | ~82% |
| 10 (大师) | 15 | 5 | ~32% | ~90% |

**公式**：

```
effective_melee     = (melee_skill + weapon_skill) / 2
n                   = 3 + effective_melee × 1.2
k                   = 30 - effective_melee × 2.5

clamp(n, 3, 15)
clamp(k, 5, 30)
```

> **公式解读**：
> - n 范围 [3, 15]：新手瞄准基本不集中（3x），大师可高度集中（15x）
> - k 范围 [30, 5]：新手瞄准时大幅降低命中（-30），大师瞄准几乎不牺牲命中质量（-5）
> - `effective_melee` 取近战技能和武器技能的均值，保证双技能都有价值

### 5.4 不同部位的实战预期

以 effective_melee = 5（n=9, k=17.5, hit_spread 典型值 ~30）为例：

| 目标部位 | hit_size | 瞄准后权重 | 定位占比 | hit_difficulty | 修正后命中(估) |
|----------|----------|-----------|---------|----------------|--------------|
| torso | 36 | 324 | 324/456=**71%** | 1.0 | ~75% |
| leg | 13 | 117 | 117/249=**47%** | 0.9 | ~65% |
| arm | 13 | 117 | 117/249=**47%** | 0.95 | ~62% |
| head | 4 | 36 | 36/168=**21%** | 1.2 | ~52% |
| foot | 2 | 18 | 18/150=**12%** | 0.8 | ~48% |
| hand | 1.5 | 13.5 | 13.5/145=**9%** | 1.0 | ~40% |
| eye | 0.5 | 4.5 | 4.5/136=**3%** | 1.15 | ~25% |

> **战术层次**：瞄躯干几乎必中（71%）但缺乏控制效果；瞄腿/臂有中等命中且有倒地/缴械可能；瞄头是豪赌（21% → 晕眩）。这是"风险 vs 回报"的核心博弈。

---

## 六、JSON 扩展

### 6.1 `technique` 新增字段

```json
{
  "type": "technique",
  "id": "tec_low_cut",
  "targetable_body_parts": ["leg_l", "leg_r", "foot_l", "foot_r"],
  "aim_penalty_mod": 0.8
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `targetable_body_parts` | array[string] | 否 | 此技艺可瞄准的部位白名单。不填 = 所有部位可选 |
| `aim_penalty_mod` | float | 否 | 此技艺的命中惩罚修正系数。默认 1.0。<1.0 表示此技艺更易瞄准（如刺击），>1.0 表示更难（如横扫） |

### 6.2 身体部位 JSON 无需修改

现有的 `hit_size`、`hit_difficulty`、`effects_on_hit` 已经足够支撑此系统。无需新增字段。

---

## 七、C++ 改造方案

### 7.1 改造文件

| 文件 | 改造内容 |
|------|---------|
| `src/melee.cpp` | 新增 `precise_melee_attack()` 入口函数，UI 流程插入 |
| `src/handle_action.cpp` | 注册新快捷键 `Alt+F` |
| `src/martialarts.h` | `ma_technique` 新增 `targetable_body_parts` 和 `aim_penalty_mod` |
| `src/anatomy.cpp` | `select_body_part()` 新增可选参数 `target_bp` + `aim_multiplier` |
| `src/creature.cpp` | `deal_melee_hit()` 透传部位瞄准参数 |

### 7.2 核心函数签名

```cpp
// melee.cpp: 新增 —— 精确攻击入口
void Character::precise_melee_attack( Creature &target );

// anatomy.cpp: 修改 —— 选择身体部位（支持瞄准偏置）
bodypart_id anatomy::select_body_part(
    int min_hit, int max_hit, bool can_attack_high, int hit_roll,
    bodypart_id aimed_bp = bodypart_id::NULL_ID(),  // 新增：瞄准目标部位
    float aim_multiplier = 10.0f                     // 新增：权重放大倍数 n
) const;
```

### 7.3 改造后的部位选择算法

在 `anatomy::select_body_part()` 中，如果传入了 `aimed_bp`：

```cpp
for( const bodypart_id &bp : cached_bps ) {
    float weight = bp->hit_size;

    // 原有逻辑...
    
    // === 新增：瞄准偏置 ===
    if( aimed_bp.is_valid() && bp == aimed_bp ) {
        weight *= aim_multiplier;  // hit_size × n
    }
    // === 新增结束 ===

    if( hit_roll > 0 ) {
        weight *= std::pow(static_cast<float>(hit_roll), bp->hit_difficulty);
    }
    hit_weights.add(bp, weight);
}
```

### 7.4 改造后的命中判定

在 `Character::melee_attack_abstract()` 中，如果走精确攻击路径：

```cpp
// === 新增：部位瞄准惩罚 ===
if( is_precise_attack ) {
    int aim_penalty = calc_aim_penalty( effective_melee_skill, technique );
    hit_spread -= aim_penalty;  // hit_spread -= k
}
// === 新增结束 ===
```

### 7.5 ma_technique 扩展

```cpp
// martialarts.h: 新增字段
class ma_technique {
    // ... existing fields ...
    std::vector<bodypart_str_id> targetable_body_parts;  // 部位白名单
    float aim_penalty_mod = 1.0f;                        // 命中惩罚系数
};
```

---

## 八、实施步骤

### 阶段 1：数据层（JSON + C++ 加载）

1. `ma_technique` 新增 `targetable_body_parts` 和 `aim_penalty_mod` 字段
2. 在 `martialarts.cpp` 中实现 JSON 加载
3. 为现有的中世纪技艺补充 `targetable_body_parts`（初始可为空——所有部位可选）

### 阶段 2：核心逻辑

4. 实现 `calc_effect_melee_skill()` → 近战+武器技能均值
5. 实现 `calc_aim_multiplier_n(skill)` → n = clamp(3 + skill×1.2, 3, 15)
6. 实现 `calc_aim_penalty_k(skill)` → k = clamp(30 - skill×2.5, 5, 30)
7. 修改 `anatomy::select_body_part()` → 新增 `aimed_bp` + `aim_multiplier` 参数
8. 修改 `melee_attack_abstract()` → 新增 `aimed_bp` 和 `is_precise` 参数透传

### 阶段 3：UI

9. 实现技艺选择 UI（`select_technique_ui()`）→ 复用 `uilist`，显示过滤后的技艺列表
10. 实现部位选择 UI（`select_body_part_ui()`）→ 列出 anatomy 部位，标注预估命中
11. 实现精确攻击入口 `precise_melee_attack()` → 串联上述两步 UI + 核心逻辑
12. 在 `handle_action.cpp` 注册新快捷键

### 阶段 4：测试与平衡

13. 编译验证 + `--check-mods` JSON 验证
14. 测试：不同技能水平下的 n/k 体感
15. 调整公式参数（如果需要）

---

## 九、开放问题

以下问题留待实现阶段决定：

| 问题 | 现状 | 建议 |
|------|------|------|
| 精确攻击是否消耗额外 move cost？ | 未定 | 精确攻击 +10% movecost（"花时间瞄准"） |
| NPC 是否也能精确攻击玩家？ | 仅玩家可用 | 初版仅玩家，后续可给高级 NPC 加 AI 逻辑 |
| 部位命中预估显示精确数值还是区间？ | 简化文字 | 初版用"极高/高/中/低"文字，避免数字暴露底层公式 |
| monster 是否后续支持？ | 仅 NPC/Character | 如果 monster 也走部位系统（design08-敌人），后续可扩展 |

---

## 十、相关文档

| 文档 | 关系 |
|------|------|
| [code_combat_system.md](../vanilla/code_combat_system.md) | 原版战斗系统完整调研：命中/闪避/暴击/部位选择/伤害全流程 |
| [json_martial.md](../vanilla/json_martial.md) | 技艺/流派/部位 JSON 配置调研 + 瞄准系统理论模型 |
| [design04-武器.md](design04-武器.md) | 中世纪武器体系策划——武器相关的技艺设计 |
| [design08-敌人.md](design08-敌人.md) | 敌人 NPC 化方案——NPC 战斗是本系统的目标场景 |
| [code_armor_penetration_system.md](../vanilla/code_armor_penetration_system.md) | 护甲穿透系统——已实现的 STR×重量破甲 |
