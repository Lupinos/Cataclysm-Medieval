# Technique (技艺) JSON 字段深度调研

> CDDA 原版 `technique` 类型的完整字段字典 —— JSON 定义、C++ 加载默认值、运行时行为。
> 源文件：`data/json/techniques.json`（3494 行，167 个技术）、`src/martialarts.h`、`src/martialarts.cpp`、`src/melee.cpp`、`src/bonuses.h`、`src/bonuses.cpp`

---

## 一、总览：39 个 JSON Key

167 个 technique 定义中共出现 39 个 JSON key（不含 `//` 注释）。按功能域分组：

| 功能域 | Key 数量 | 涵盖 |
|--------|---------|------|
| **身份/显示** | 6 | `id`, `name`, `description`, `messages`, `condition_desc`, `goal`(未用) |
| **布尔开关** | 17 | `dummy`, `crit_tec`, `crit_ok`, `defensive`, `disarms`, … |
| **整数/浮点** | 6 | `weighting`, `stun_dur`, `down_dur`, `knockback_dist`, … |
| **字符串** | 2 | `aoe`, `condition_desc` |
| **数组** | 8 | `attack_vectors`, `mult_bonuses`, `flat_bonuses`, `tech_effects`, `skill_requirements`, … |
| **嵌套对象** | 1 | `condition` |

---

## 二、字段详解（字母序）

> 每个字段列出：JSON 类型、C++ 成员变量类型、加载函数、默认值、运行时效果、注意事项。

### 2.1 `aoe`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string`（枚举 `"wide"` / `"impale"` / `"spin"`） |
| C++ 类型 | `std::string` |
| 默认值 | `""`（空字符串 = 无 AOE） |
| 使用次数 | 6（每种 2 个） |

**运行时效果**（`melee.cpp:1608-1611` 过滤 + `melee.cpp:1986-2015` 执行）：

```
"wide"  → 攻击目标左右两侧的相邻敌人
"impale" → 攻击目标身后 1 格的敌人 + 其左右
"spin"  → 攻击周围所有相邻敌人（需 ≥2 个目标）
```

**关键行为**：AOE 攻击**零消耗**——执行前保存 `moves` 和 `stamina`，对每个副目标执行 `melee_attack()` 后恢复。只有主攻击消耗资源。

---

### 2.2 `attack_override`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 未在 techniques.json 中出现（理论上可用） |

**运行时效果**（`melee.cpp:1804-1807`）：如果 `true`，**清空整个伤害实例**并将 move cost 归零。这意味着正常攻击的伤害完全消失，只有 technique 自身通过 `flat_bonuses`/`mult_bonuses` 提供的伤害会生效。适用于"技替换普通攻击"的场景。

---

### 2.3 `attack_vectors`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string[]`（优先级顺序） |
| C++ 类型 | `std::vector<std::string>` |
| 默认值 | `{}`（空） |
| 使用次数 | ~130（几乎全部技术） |

**所有有效值（11 种）**：

| Vector | 数量 | 所需健康部位 |
|--------|------|-------------|
| `WEAPON` | ~90 | 持武器手臂 |
| `HAND` | ~34 | 同侧手臂 |
| `FOOT` | ~14 | 同侧腿 |
| `THROW` | ~10 | **双臂** |
| `GRAPPLE` | ~2 | **双臂** |
| `ELBOW` | 1 | 同侧手臂 |
| `KNEE` | 2 | 同侧腿 |
| `WRIST` | 1 | 同侧手臂 |
| `HAND_BACK` | 1 | 同侧手臂 |
| `PALM` | 2 | 同侧手臂 |
| `HEAD` | 0（仅 `attack_vectors_random`） | 永远可用 |
| `TORSO` | 0（仅 `random`） | 永远可用 |

**运行时行为**：`evaluate_techniques()` 中（`melee.cpp:1621-1627`）按 `attack_vectors` 声明的顺序逐个尝试，找到第一个可用 vector 即通过。全不可用则过滤掉该技术。每个 vector 的可用性由 `can_use_attack_vector()`（`martialarts.cpp:1382-1402`）检查对应身体部位是否健康。

> **设计含义**：声明顺序 = 优先级。`["WEAPON", "HAND"]` 表示优先用武器，武器不可用时降级为徒手。

---

### 2.4 `attack_vectors_random`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string[]` |
| C++ 类型 | `std::vector<std::string>` |
| 默认值 | `{}`（空） |
| 使用次数 | 7 |

**与 `attack_vectors` 的区别**：此数组在每次检查前**打乱顺序**（`shuffle`），然后同样逐个尝试。用于实现"随机出拳"效果。

实例：`tec_krav_maga_crit` 使用 `["HAND", "FINGERS", "FOOT", "ELBOW", "KNEE", "LOWER_LEG", "HEAD"]`，每次攻击随机选择一个健康肢体。

**查找优先级**：`attack_vectors` 先检查，全部失败后才尝试 `attack_vectors_random`。

---

### 2.5 `block_counter`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 2 |

**运行时效果**：标记此技术只能在格挡后作为反击触发。在 `evaluate_techniques()` 的过滤阶段（`melee.cpp:1553`），`block_counter` 必须匹配传入的 `block_counter` 参数才不被过滤。此参数由格挡系统中的 `pick_technique(*source, shield, false, false, true)`（`melee.cpp:2255`）传入。

---

### 2.6 `condition`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object`（嵌套布尔逻辑） |
| C++ 类型 | `std::function<bool(dialogue&)>` |
| 默认值 | 无（可选，不存在则 `has_condition = false`） |
| 使用次数 | ~60 |

**完整判定维度**（7 种叶节点谓词）：

| 谓词 | 说明 | 示例值 |
|------|------|--------|
| `math` | 数值比较表达式 | `u_val('size') >= n_val('size')` |
| `npc_has_effect` | 目标的 effect | `"stunned"`, `"downed"` |
| `npc_has_flag` | 目标的 flag | `"FLIES"`, `"GRAB_FILTER"` |
| `u_has_flag` | 使用者的 flag | `"GRAB"` |
| `npc_has_species` | 目标的物种 | `"ZOMBIE"`, `"HUMAN"`, `"NETHER"` 等 16 种 |
| `npc_bodytype` | 目标的体型类别 | `"human"`, `"angel"`, `"blob"` 等 9 种 |
| `roll_contested` | 对抗掷骰 | `u_val('strength')` vs `n_val('grab_strength')` |

所有谓词可被 `"and"` / `"or"` / `"not"` 包装一层。

**运行时**：`evaluate_techniques()` 中（`melee.cpp:1526-1532`），如果 `has_condition == true`，则创建 `dialogue` 并调用 `condition(d)`，返回 `false` 则过滤掉此技术。

---

### 2.7 `condition_desc`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string` |
| C++ 类型 | `std::string` |
| 默认值 | 无（可选） |
| 使用次数 | 71 |

**纯 UI 字段**，不参与任何运行时逻辑。在 `condition` 旁边显示人类可读的条件说明。格式模板：

```
"* Only works on a <info>condition</info> target of <info>size</info> size..."
```

---

### 2.8 `crit_ok` / `crit_tec`

| 属性 | `crit_ok` | `crit_tec` |
|------|-----------|------------|
| JSON 类型 | `bool` | `bool` |
| C++ 类型 | `bool` | `bool` |
| 默认值 | `false` | `false` |
| 使用次数 | ~37 | ~49 |

**二者互斥语义**（`melee.cpp:1580`）：

```
crit_tec  crit_ok  |  非暴击时可用?  |  暴击时可用?
--------  --------  |  --------------  |  ------------
  false    false    |      是          |      否
  false    true     |      是          |      是
  true     false    |      否          |      是
  true     true     |      (无效组合，未出现)
```

`crit_tec=true, crit_ok=false` 是最常见的模式（~49 个），意味着"只有暴击才触发的大招"。

---

### 2.9 `defensive`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | ~26 |

**运行时效果**（`melee.cpp:1520`）：`evaluate_techniques()` 直接排除所有 `defensive=true` 的技术。防御性技术不参与正常攻击的选择，而是通过专门的查找函数获取（如 `get_grab_break()`、`get_miss_recovery()`）。

---

### 2.10 `disarms`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | ~14 |

**运行时**：
- **过滤**（`melee.cpp:1595`）：目标无武器时过滤掉
- **执行**（`melee.cpp:1973-1983`）：将目标武器强制掉落在地面上

---

### 2.11 `dodge_counter`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 未在 techniques.json 中直接出现（通过 buff 链间接使用） |

**运行时效果**：与 `block_counter` 对称，但用于闪避后反击。过滤逻辑相同，由闪避系统调用 `pick_technique(dodge_counter=true)`。

**额外 guard**（`melee.cpp:1564-1576`）：反击技术会检查执行后是否耗尽剩余的 moves，如果 `moves + speed - move_cost < 0` 则过滤掉（防止"反击后站着不动等死"）。

---

### 2.12 `down_dur`

| 属性 | 值 |
|------|---|
| JSON 类型 | `int` |
| C++ 类型 | `int` |
| 默认值 | `0` |
| 使用次数 | ~37（值均为 1 或 2） |

**运行时**（`melee.cpp:1840-1848`，在 repeat 循环内）：

```
if down_dur > 0:
    目标非掷投免疫 → 施加 effect_downed，持续 rng(1, down_dur) 回合
    若已有 bash 伤害 → +3 bash 奖励伤害
```

---

### 2.13 `dummy`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 4（`tec_none`, `WBLOCK_1`, `WBLOCK_2`, `WBLOCK_3`） |

**运行时**（`melee.cpp:1514`）：`evaluate_techniques()` 直接排除所有 `dummy=true` 的技术。这些技术仅通过特定 ID 查找使用（如 `WBLOCK_1/2/3` 在 `blocking_ability()` 中用于格挡等级判定）。

---

### 2.14 `eocs`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]`（EOC 定义） |
| C++ 类型 | `std::vector<effect_on_condition_id>` |
| 默认值 | `{}`（空） |
| 使用次数 | 1（`tec_debug_eoc_demo`） |

**运行时**（`melee.cpp:1854-1861`，在 repeat 循环内）：对每个 EOC 创建 `dialogue`，如果是 `ACTIVATION` 类型则调用 `eoc->activate(d)`。

---

### 2.15 `flags`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string[]` |
| C++ 类型 | `std::set<std::string>` |
| 默认值 | `{}`（空） |
| 使用次数 | `techniques.json` 中未出现 |

**⚠️ 关键发现**：`ma_technique.flags` 在整个 C++ 运行时**从未被读取**。此字段是纯 UI/显示用途（可能被前端用于过滤或分类显示）。**不要将此与 `reqs.req_flags` 混淆**——后者检查的是武器物品的 flag（如 `SHEATH_SWORD`），用于判断武器是否匹配技术。

---

### 2.16 `flat_bonuses`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]` |
| C++ 类型 | `bonus_container::bonus_map` |
| 默认值 | `{}`（空） |
| 使用次数 | 7 |

**每个元素的 JSON 结构**：

```json
{
  "stat": "damage",         // 必填："damage"|"arpen"|"movecost"|"hit"|"dodge"|...
  "type": "bash",           // 当 stat=damage/arpen 时必填
  "scale": 10,              // 必填：固定值或属性系数
  "scaling-stat": "str"     // 可选：str/dex/int/per。不填=固定值
}
```

**运行时数学**（`bonuses.cpp:263-286`）：

```
if scaling-stat == "str":  bonus = scale × u.get_str()
if scaling-stat == absent: bonus = scale  (纯固定值)
```

**flat_bonuses 是累加**：同一 stat+type 下所有条目的 `bonus` 值求和。在 `perform_technique()` 中（`melee.cpp:1809-1819`），对每个 damage_type：
- flat damage → 作为新 `damage_unit` 加入 `damage_instance`（`× rep`）
- flat arpen → 作为新 `damage_unit` 的 `res_pen`（`× rep`）
- flat movecost → 加到总 move cost 上（`× rep`）

**所有 `affected_stat` 枚举值**（`bonuses.cpp:21-34`）：

| JSON 值 | 含义 | 是否需要 `type` |
|---------|------|----------------|
| `"damage"` | 伤害量 | **是** |
| `"arpen"` | 护甲穿透 | **是** |
| `"movecost"` | 行动点消耗 | 否 |
| `"hit"` | 命中值 | 否 |
| `"dodge"` | 闪避值 | 否 |
| `"block"` | 格挡值 | 否 |
| `"block_effectiveness"` | 格挡效果 | 否 |
| `"speed"` | 速度 | 否 |
| `"crit_chance"` | 暴击率 | 否 |
| `"armor"` | 护甲值 | **是** |
| `"target_armor_multiplier"` | 目标护甲倍率 | 否 |

---

### 2.17 `forbidden_buffs_all`（JSON 中拼写为 `forbidden_buffs_all`）

| 属性 | 值 |
|------|---|
| JSON 类型 | `string` 或 `string[]` |
| C++ 类型 | `std::set<mabuff_id>` |
| 默认值 | `{}`（空） |
| 使用次数 | 4（2 种 buff） |

**运行时**：`ma_requirements::is_valid_character()` 中（`martialarts.cpp`），通过 `buff_requirements_satisfied()` 检查。如果角色拥有 `forbidden_buffs_all` 中的所有 buff，技术不可用。

**注意**：C++ 中也存在 `forbid_buffs_any`（拼写为 `forbid`而非 `forbidden`），在 `techniques.json` 中未使用。

---

### 2.18 `grab_break`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | ~14 |

**运行时**：不参与 `evaluate_techniques()`。通过专门的 `get_grab_break()` 查找函数使用：
- `character_escape.cpp:196` — 脱离擒拿时额外 +10 成功率
- `character_escape.cpp:287` — 成功脱离时显示技术消息
- `monattack.cpp:5244` — 怪兽擒拿时自动检测并逃脱

---

### 2.19 `knockback_dist` / `knockback_spread` / `knockback_follow`

| 属性 | `knockback_dist` | `knockback_spread` | `knockback_follow` |
|------|-----------------|-------------------|--------------------|
| JSON 类型 | `int` | `int` | `bool` |
| C++ 类型 | `int` | `float` | `bool` |
| 默认值 | `0` | `0` | `false` |
| 使用次数 | ~15 | 2 | 2 |

**运行时**（`melee.cpp:1904-1956`）：
1. 实际击退距离 = `rng(1, knockback_dist)`
2. 击退方向：从 spread 范围随机偏移量计算
3. `knockback_follow=true`：攻击者跟随到目标原位置
   - 多重安全检查：不会移入火/深水/移动载具，骑乘/驾驶/被擒拿时不会移动
4. 同时移除目标对攻击者的 grab

---

### 2.20 `messages`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string[2]`：`[avatar_message, npc_message]` |
| C++ 类型 | `translation` × 2 |
| 默认值 | 无（可选，但几乎所有真实技术都有） |
| 使用次数 | ~167 |

**运行时**（`melee.cpp:2608-2618`）：命中时覆盖标准的"你击中了 %s"消息。Player 用 `messages[0]`，NPC 用 `messages[1]`。

---

### 2.21 `miss_recovery`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | ~18 |

**运行时**：attack miss 时生效，**不同上下文 cost 不同**：
- 挥空（`melee.cpp:1020`）：`move_cost /= 3`
- 击中目标但被闪避（`melee.cpp:702`）：`move_cost /= 2`（stumble 惩罚后封顶 60）

---

### 2.22 `mult_bonuses`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]`（结构同 `flat_bonuses`） |
| C++ 类型 | `bonus_container::bonus_map` |
| 默认值 | `{}`（空） |
| 使用次数 | ~80 |

**与 `flat_bonuses` 的核心区别**：`mult_bonuses` 是**累乘**（所有条目乘积），`flat_bonuses` 是累加。

**运行时**（`melee.cpp:1809-1819`）：
- mult damage → `damage_unit.damage_multiplier *= mult_value`
- mult movecost → `move_cost *= mult_value`（先乘，再加 flat）

**所有出现过的 `movecost` 倍率**：`0.3`, `0.5`, `0.6`, `0.66`, `0.7`, `0.75`, `0.8`, `0.9`, `1.1`, `1.2`, `1.5`, `1.75`

**所有出现过的 `damage` 倍率**：`0.2`, `0.33`, `0.5`, `0.66`, `1.1~1.5`（常见）, `2.0`, `2.5`, `3.0`, `99`

---

### 2.23 `needs_ammo`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 1（`SWEETSPOT`） |

**运行时**：
- **过滤**（`melee.cpp:1586`）：武器弹匣不满时过滤掉
- **执行**（`melee.cpp:1864-1876`）：消耗 1 发弹药、播放枪声、如有 `RELOAD_EJECT` flag 则生成弹壳

---

### 2.24 `reach_ok` / `reach_tec`

| 属性 | `reach_ok` | `reach_tec` |
|------|-----------|------------|
| JSON 类型 | `bool` | `bool` |
| C++ 类型 | `bool` | `bool` |
| 默认值 | `false` | `false` |
| 使用次数 | 5 | 1 |

**过滤逻辑**（`melee.cpp:1541-1550`）：

```
reach_attacking=true  且 !reach_ok 且 !reach_tec  → 过滤掉
reach_attacking=false 且 reach_tec                → 过滤掉
```

即：`reach_tec` = 仅在长距攻击时可用；`reach_ok` = 长距和普通攻击都可以用。

---

### 2.25 `repeat_min` / `repeat_max`

| 属性 | 值 |
|------|---|
| JSON 类型 | `int` |
| C++ 类型 | `int` |
| 默认值 | `1` |
| 使用次数 | 未在 techniques.json 中出现（理论上可用） |

**运行时**：`rep = rng(repeat_min, repeat_max)`。`rep` 影响：
- flat damage/arpen 倍乘（`× rep`）
- `tech_effects` 施加次数（重复尝试）
- `down_dur`/`stun_dur` 效果（重复施加）
- `move_cost_penalty` 倍乘（`× rep`）

**不受 `rep` 影响**：`mult_bonuses` 的伤害倍率（只乘一次）。

---

### 2.26 `req_flags`（位于 `reqs` 内部）

| 属性 | 值 |
|------|---|
| JSON 类型 | `string[]`（flag_id） |
| C++ 类型 | `std::set<flag_id>` |
| 默认值 | `{}`（空） |
| 使用次数 | 未在 techniques.json 中出现 |

`is_valid_character()` 中（`martialarts.cpp:696`）：武器物品必须拥有**所有**列出的 flag 才通过。

> ⚠️ 不要与 `ma_technique.flags` 混淆——`reqs.req_flags` 检查的是**武器**，`technique.flags` 是自身元数据（且 C++ 不读它）。

---

### 2.27 `required_buffs_all`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string` 或 `string[]` |
| C++ 类型 | `std::set<mabuff_id>` |
| 默认值 | `{}`（空） |
| 使用次数 | 20（13 种 buff） |

**运行时**（`martialarts.cpp:150-170` `buff_requirements_satisfied()`）：角色必须拥有列表中的**每一个** buff 才通过。用于构建 buff 链——"格挡后解锁投技"等。

**命名模式**：`buff_<流派>_on<触发时机>`，如 `buff_aikido_onblock`、`buff_capoeira_onmove`。

**注意**：`tec_medievalpole_hook` 使用字符串形式 `"required_buffs_all": "buff_medievalpole_onmiss"`（非数组），C++ 接受此形式。

---

### 2.28 `skill_requirements`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]`：`{ "name": "skill_id", "level": int }` |
| C++ 类型 | `std::vector<std::pair<skill_id, int>>` |
| 默认值 | `{}`（空） |
| 使用次数 | ~133 |

**运行时**（`martialarts.cpp:637-643`）：角色在每项技能上的等级必须 ≥ `level`。

所有出现过的技能：`"melee"`（1~6 级）、`"unarmed"`（1~6 级）、`"speech"`（10 级，仅 debug）。

---

### 2.29 `side_switch`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 1（`tec_judo_backthrow`） |

**运行时**（`melee.cpp:1878-1902`）：将目标移动到攻击者身后相对位置。如果目标格不是空地（`g->is_empty()`），不移动。`IMMOBILE` 目标免疫。

---

### 2.30 `stun_dur`

| 属性 | 值 |
|------|---|
| JSON 类型 | `int` |
| C++ 类型 | `int` |
| 默认值 | `0` |
| 使用次数 | ~30（值均为 1 或 2） |

**运行时**（`melee.cpp:1850-1852`）：施加 `effect_stunned`，持续 `rng(1, stun_dur)` 回合。无免疫检查。

---

### 2.31 `take_weapon`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 1（`tec_taekwondo_disarm`） |

**运行时**：
- **过滤**（`melee.cpp:1601-1605`）：攻击者已持武器或目标徒手时过滤掉
- **执行**（`melee.cpp:1960-1971`）：卸除目标武器并装入攻击者手中

---

### 2.32 `tech_effects`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]` |
| C++ 类型 | `std::vector<tech_effect_data>` |
| 默认值 | `{}`（空） |
| 使用次数 | 11 |

**每个元素的 JSON 结构**：

```json
{
  "id": "disarmed",          // 必填：effect_type ID
  "duration": 400,            // 可选，默认 0：回合数
  "permanent": false,         // 可选，默认 false
  "on_damage": true,          // 可选，默认 true：需要造成伤害才触发
  "chance": 100,              // 可选，默认 100：触发概率 0-100
  "message": "...",           // 可选，默认 ""：触发时显示的消息
  "req_flag": "..."           // 可选，默认 "NULL"：攻击者所需 character_flag
}
```

**运行时**（`melee.cpp:1829-1838`，在 repeat 循环内）：

```
for each effect:
    if random(0,99) < chance AND (total_damage > 0 OR !on_damage):
        if req_flag == NULL OR attacker.has_flag(req_flag):
            target.add_effect(id, duration, permanent)
            show message to attacker
```

所有出现过的 effect：`"disarmed"`（10 次，duration=400）、`"maimed_arm"`（1 次，duration=44000）。

---

### 2.33 `unarmed_allowed` / `melee_allowed` / `unarmed_weapons_allowed`

| 属性 | `unarmed_allowed` | `melee_allowed` | `unarmed_weapons_allowed` |
|------|------------------|-----------------|--------------------------|
| JSON 位置 | `reqs` 内部 | `reqs` 内部 | `reqs` 内部 |
| C++ 类型 | `bool` | `bool` | `bool` |
| 默认值 | `false` | `false` | `true` |
| 使用次数 | ~67 | ~109 | 8（全为 `false`） |

**运行时**（`martialarts.cpp:620-630`）：`is_valid_character()` 中的基本判定。三者逻辑：
- `unarmed_allowed`：徒手攻击时可用
- `melee_allowed`：持近战武器时可用
- `unarmed_weapons_allowed`（默认 true）：当"徒手武器"（如指虎）装备时仍可用

没有 `melee_allowed` 也没有 `unarmed_allowed` 的技术永远不会通过此关。

---

### 2.34 `wall_adjacent`

| 属性 | 值 |
|------|---|
| JSON 类型 | `bool` |
| C++ 类型 | `bool` |
| 默认值 | `false` |
| 使用次数 | 未在 techniques.json 中出现 |

**双重检查**（`melee.cpp:1535` + `martialarts.cpp:633`）：攻击者必须毗邻墙壁。两处独立检查——一处在上层 `evaluate_techniques()`，一处在下层 `is_valid_character()`。

---

### 2.35 `weapon_categories_allowed`

| 属性 | 值 |
|------|---|
| JSON 类型 | `string` 或 `string[]` |
| C++ 类型 | `std::vector<weapon_category_id>` |
| 默认值 | `{}`（空） |
| 使用次数 | 5 |

**运行时**（`martialarts.cpp:678-689`）：武器的 `weapon_category` 必须匹配列表中的至少一项。用于限定技术只能用于特定武器类别（如仅长柄武器可用）。

---

### 2.36 `weighting`

| 属性 | 值 |
|------|---|
| JSON 类型 | `int` |
| C++ 类型 | `int` |
| **JSON 默认值** | `1` |
| **C++ 默认值** | `0`（`ma_technique()` 构造函数未初始化，取头文件 `= 0`） |
| 使用次数 | ~30 |

> ⚠️ **Gotcha**：已加载的技术未指定 `weighting` 时，JSON 默认值 = 1，C++ 未加载时默认值 = 0。这意味着永远不要依赖未加载技术的 `weighting`。

**运行时**（`melee.cpp:1614-1636`）：

```
weighting > 1  → 技术 ID 被额外加入候选池 (weighting - 1) 次
                 例：weighting=3 → 3倍选中概率
weighting < 0  → one_in(|weighting|) 随机判定
                 例：weighting=-4 → 1/4 概率不被过滤
weighting = 0  → 候选池中只出现一份（但在加载时从未出现——见上方 Gotcha）
weighting = 1  → 正常概率
```

---

### 2.37 `required_char_flags` / `required_char_flags_all` / `forbidden_char_flags`

| 属性 | `required_char_flags` | `required_char_flags_all` | `forbidden_char_flags` |
|------|----------------------|--------------------------|------------------------|
| JSON 类型 | `string[]` | `string[]` | `string[]` |
| C++ 类型 | `flat_set<jcf>` | `flat_set<jcf>` | `flat_set<jcf>` |
| 默认值 | `{}`（空） | `{}`（空） | `{}`（空） |
| 使用次数 | 未在 techniques.json 中出现 | 未出现 | 未出现 |

均为 `reqs`（`ma_requirements`）内部的成员。检查角色的 `json_character_flag`（不是物品 flag）：
- `required_char_flags`：角色必须拥有**任意一个**
- `required_char_flags_all`：角色必须拥有**全部**
- `forbidden_char_flags`：角色**不能拥有任何一个**

---

### 2.38 `weapon_damage_requirements`

| 属性 | 值 |
|------|---|
| JSON 类型 | `object[]`：`{ "type": "damage_type_id", "min": int }` |
| C++ 类型 | `std::vector<std::pair<damage_type_id, int>>` |
| 默认值 | `{}`（空） |
| 使用次数 | 未在 techniques.json 中出现 |

如果武器的基础伤害不满足最低要求，此技术不可用。用于保证"重型斩击"类技术只在足够强力的武器上触发。

---

## 三、关键 Gotcha 和 Bug

### 3.1 `STAT_NULL` 的 fall-through

`bonuses.cpp:279-282` 中 `STAT_NULL` case 没有 `break`，会 fall through 到 `NUM_STATS` case。结果碰巧正确（`NUM_STATS` 也不做任何事），但属于代码异味。

### 3.2 `weighting` 的双重默认值

`ma_technique()` 构造函数未初始化 `weighting` → 取头文件 `= 0`。但 `ma_technique::load()` 中 `optional` 默认值 = `1`。如果某个代码路径用到了未加载技术的 `weighting`，会意外得到 `0`。

### 3.3 `flags` 字段 C++ 不使用

`ma_technique.flags`（`std::set<std::string>`）虽然在 JSON 被加载，但整个 C++ 源码中没有任何地方读取它。如果是为 UI 设计的，后端不应该依赖它。

### 3.4 AOE 攻击零消耗

AOE 技术（`spin`/`wide`/`impale`）对副目标的攻击完全免费——执行前保存 `moves` 和 `stamina`，对每个副目标调用 `melee_attack()` 后恢复。只有主攻击消耗资源。

### 3.5 `crit_ok` 与 `crit_tec` 的值组合

`techniques.json` 中从未出现 `crit_tec=true, crit_ok=true` 的组合。二者实际上语义互斥，虽然代码允许同时为 true（那意味着技术仅在暴击时可用——等同于 `crit_tec=true, crit_ok=false`，只是检查路径不同）。

### 3.6 `attack_vectors` 与肢体伤残

如果一个技术只有 `["WEAPON"]` 这一个 vector 且持武器手臂残废，此技术直接不可用。这意味着**没有 fallback**——不像 `["WEAPON", "HAND"]` 可以降级为徒手攻击。

---

## 四、相关文档

| 文档 | 关系 |
|------|------|
| [json_martial.md](json_martial.md) | 战斗系统 JSON 配置总览（technique/martial_art/body_part/anatomy） |
| [code_combat_system.md](code_combat_system.md) | 完整近战流程：命中/闪避/暴击/部位选择/伤害计算 |
| [martialarts.h](file:///e:/Cataclysm-Medieval/src/martialarts.h) | `ma_technique` 类定义 |
| [martialarts.cpp](file:///e:/Cataclysm-Medieval/src/martialarts.cpp) | 技术加载 + `ma_requirements` 验证 |
| [melee.cpp](file:///e:/Cataclysm-Medieval/src/melee.cpp) | `evaluate_techniques()` + `perform_technique()` |
| [bonuses.h](file:///e:/Cataclysm-Medieval/src/bonuses.h) | `bonus_container` 结构 |
| [bonuses.cpp](file:///e:/Cataclysm-Medieval/src/bonuses.cpp) | flat/mult bonus 数学 |
