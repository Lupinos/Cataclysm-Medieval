# design09-战斗系统重置：旧技术方案

> 来源：`archive/medieval-before-redo`。仅供重新设计时查阅，未迁入新基线；旧接口、数据及数值推演须重新核验。完整旧稿保存在该分支的 `msvc-full-features/.qoder/docs/`。本页不表示当前实现状态。

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

## 十、相关文档

| 文档 | 关系 |
|------|------|
| [code_combat_system.md](../../vanilla/code_combat_system.md) | 原版战斗系统完整调研：命中/闪避/暴击/部位选择/伤害全流程 |
| [json_martial.md](../../vanilla/json_martial.md) | 技艺/流派/部位 JSON 配置调研 + 瞄准系统理论模型 |
| [design04-武器.md](design04-武器.md) | 中世纪武器体系策划——武器相关的技艺设计 |
| [design08-敌人.md](design08-敌人.md) | 敌人 NPC 化方案——NPC 战斗是本系统的目标场景 |
| [code_armor_penetration_system.md](../../vanilla/code_armor_penetration_system.md) | 护甲穿透系统——已实现的 STR×重量破甲 |


```json
{
  "id": "tec_low_cut",
  "type": "technique",
  "name": "斩腿",
  "targetable_body_parts": ["leg_l", "leg_r", "foot_l", "foot_r"],
  "...": "..."
}
```
