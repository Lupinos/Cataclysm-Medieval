# 制作与技能系统 (Crafting & Skills)

> 核验基点：CDDA `0.H-branch`，提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 改造前的维护分支快照，并非最初的 0.H 发布标签）。下述源码路径均以该提交为准。

> CDDA 原版的制作配方、技能升级、熟练度系统

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
- 生疏处理主要改变实践经验；实践训练同时推进知识，实践升级超过知识时会把知识等级抬到实践等级（`SkillLevel::on_exercise_change`）
- `level()`: 只返回 `min(_level, MAX_SKILL)`，不会再取知识等级的最小值；理论等级由独立的 `knowledgeLevel()` 查询

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
| `batch_rsize` | 批量折扣曲线的尺度参数 |
| `result_mult` | 批量产出倍数 |
| `byproducts` | 副产品 |
| `hot_result()` | 产出是否热的（影响营养计算） |

### 配方学习途径

1. **自动学会** (`autolearn`): 技能达到 `autolearn_requirements` 等级时自动解锁
2. **书籍学习**: `booksets` 中的书籍，需要对应技能等级阅读
3. **拆解学习** (`learn_by_disassembly`): 拆解物品时有概率学会
4. **对话授予**: `talk_effect_fun_t::set_learn_recipe` 等对话效果可授予指定配方；普通技能教学不自动教授任意配方
5. **练习配方** (`practice_data`): 特殊配方，制作时难度动态调整

### 制作时间计算

```
单件时间 local_time = 基础 moves × proficiency_time_maluses / 制作速度倍率
无批量折扣、无助手时：总时间 = local_time × 数量
```

- 依据 `recipe::time_to_craft_moves()`、`recipe::batch_time()`：缺失熟练度时间倍率相乘；制作速度是除数，并非统一的“技能线性修正”。
- 有批量折扣时按 logistic 曲线逐件累计，`batch_rsize` 是曲线参数，不是硬性触发阈值；1 个助手乘 0.75，至少 2 个乘 0.60，总时间不低于单件时间。
- 批量制作可有时间折扣（`batch_rscale`）
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

须区分两条路径：`construction.cpp` 的普通建造定义通过 `pre_terrain` / `post_terrain` 及前后置函数处理格子；营地蓝图配方可引用 `update_mapgen_id` 并计算资源需求。不是所有建造都经过 update_mapgen。

---

## 书架与配方隐藏

`book_recipe_data` (`recipe.h:63-70`)：

- `skill_req`: 书中显示配方所需技能等级
- `alt_name`: 可选替代名称
- `hidden`: 是否隐藏（不显示在配方书中）

## 源码核对入口

- `src/skill.h`：`SkillLevel::level`、`knowledgeLevel`；`src/skill.cpp`：`train`、`readBook`、`rust`、`on_exercise_change`。
- `src/recipe.cpp`：`time_to_craft_moves`、`batch_time`、`proficiency_time_maluses`、`proficiency_skill_maluses`。
- `src/crafting.cpp`：`Character::crafting_speed_multiplier`、`crafting_success_roll`。
