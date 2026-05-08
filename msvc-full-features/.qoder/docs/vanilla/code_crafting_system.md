# 制作与技能系统 (Crafting & Skills)

> Cataclysm-Medieval 的制作配方、技能升级、熟练度系统

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/recipe.h` / `src/recipe.cpp` | 配方数据结构 |
| `src/recipe_dictionary.cpp` / `src/recipe_dictionary.h` | 配方字典与查询 |
| `src/requirements.cpp` / `src/requirements.h` | 制作材料需求 |
| `src/crafting.cpp` / `src/crafting.h` | 制作流程逻辑 |
| `src/crafting_gui.cpp` | 制作 UI |
| `src/construction.cpp` / `src/construction.h` | 建造系统 |
| `src/skill.h` / `src/skill.cpp` | 技能定义 |
| `src/proficiency.h` / `src/proficiency.cpp` | 熟练度系统 |

---

## 技能系统 (Skill)

### Skill 类 (`skill.h:32-120`)

```cpp
class Skill {
    skill_id _ident;
    translation _name;          // 技能名称
    translation _description;   // 技能描述
    std::set<std::string> _tags; // 标签
    time_info_t _time_to_attack; // 攻击时间参数
    skill_displayType_id _display_type; // 显示分类
    int _sort_rank;             // 排序权重
    bool _teachable;            // 是否可传授
    bool _obsolete;             // 是否已废弃
};
```

### time_info_t — 攻击时间 (`skill.h:23-30`)

```cpp
struct time_info_t {
    int min_time = 50;                  // 攻击最短时间
    int base_time = 220;                // 基础攻击时间
    int time_reduction_per_level = 25;  // 每级减少时间
};
```

每种武器技能定义了使用该技能攻击的时间曲线。

### SkillLevel — 技能等级 (`skill.h:122-242`)

双轨制技能系统：

| 属性 | 说明 |
|------|------|
| `_level` | 实践等级（实际使用的能力） |
| `_knowledgeLevel` | 理论知识等级（学习获得，不会生疏） |
| `_exercise` | 练习经验（积累到阈值则升级） |
| `_knowledgeExperience` | 理论知识经验 |
| `_lastPracticed` | 最后练习时间 |
| `_isTraining` | 是否开启训练 |
| `_rustAccumulator` | 生疏累积 |

**核心机制：**
- 实践技能通过**使用**提升（`practice()`）
- 理论知识通过**读书**提升（`readBook()`）
- 实践技能会**生疏** (rust)（长时间不用下降）
- 理论知识永不生疏，但实践技能不能超过理论知识
- `level()`: 取 min(实践等级, MAX_SKILL)，但不会超过知识等级

### 技能分类 (SkillDisplayType)

技能按显示分类组织，每个技能属于一个 `skill_displayType_id`，用于 UI 中的分类展示。

---

## 熟练度系统 (Proficiency)

### recipe_proficiency (`recipe.h:50-61`)

```cpp
struct recipe_proficiency {
    proficiency_id id;
    bool required = false;          // 是否必须
    float time_multiplier = 0.0f;   // 时间倍率（缺则减速）
    float skill_penalty = 0.0f;     // 技能惩罚（缺则等效降级）
    float learning_time_mult = 1.0f; // 练习时的学习效率
    std::optional<time_duration> max_experience; // 经验上限
};
```

制作配方可以关联熟练度：
- **required = true**: 缺少此熟练度则完全不能制作
- **required = false**: 缺少则增加制作时间和降低等效技能等级

---

## 配方系统 (recipe)

### recipe 类 (`recipe.h:86-378`)

| 属性 | 说明 |
|------|------|
| `ident_` | 配方 ID |
| `result_` | 产出物品 |
| `time` | 制作时间（moves，100=1回合） |
| `difficulty` | 制作难度 |
| `skill_used` | 主技能 |
| `required_skills` | 所需技能及其等级 |
| `proficiencies` | 所需/相关熟练度 |
| `requirements_` | 材料需求（requirement_data） |
| `autolearn_requirements` | 自动学会所需技能等级 |
| `learn_by_disassembly` | 拆解学会所需技能等级 |
| `booksets` | 包含此配方的书籍 |
| `reversible` | 是否可逆向拆解 |
| `batch_rscale` | 批量制作时间折扣 |
| `batch_rsize` | 触发批量折扣的最小批量 |
| `result_mult` | 批量产出倍数 |
| `byproducts` | 副产品 |
| `hot_result()` | 产出是否热的（影响营养计算） |

### 配方学习途径

1. **自动学会** (`autolearn`): 技能达到 `autolearn_requirements` 等级时自动解锁
2. **书籍学习**: `booksets` 中的书籍，需要对应技能等级阅读
3. **拆解学习** (`learn_by_disassembly`): 拆解物品时有概率学会
4. **NPC 教学**: 通过 NPC 互动学习
5. **练习配方** (`practice_data`): 特殊配方，制作时难度动态调整

### 制作时间计算

```
实际时间 = 基础时间 × 批量倍率 × (1 - 技能修正) × (1 - 熟练度缺失惩罚)
```

- 批量制作有时间折扣（`batch_rscale`）
- 缺少非必需熟练度会增加时间（`proficiency_time_maluses()`）
- 缺少熟练度也会等效降低技能等级（`proficiency_skill_maluses()`）

### 练习配方 (Practice Recipes)

`practice_recipe_data` (`recipe.h:72-84`)：

- `min_difficulty` / `max_difficulty`: 难度在技能提升时动态变化
- `skill_limit`: 可提升的技能上限
- 专为技能训练设计，不侧重产出

---

## 建造系统 (Construction)

`construction.cpp` / `recipe.h` 中的蓝图相关：

- `is_blueprint()` / `get_blueprint()` — 蓝图配方
- `blueprint_resources()` / `blueprint_provides()` / `blueprint_requires()` — 营地建造需求
- `bp_autocalc` — 自动计算建造需求

建造配方通过 `update_mapgen_id` 修改地图/地形/家具，用于营地建设。

---

## 书架与配方隐藏

`book_recipe_data` (`recipe.h:63-70`)：

- `skill_req`: 书中显示配方所需技能等级
- `alt_name`: 可选替代名称
- `hidden`: 是否隐藏（不显示在配方书中）
