# 战斗系统子系统：部位血量系统

> 对应 [design09-战斗系统重置](design09-战斗系统重置.md) 的支撑子系统。
> 实现状态：部位血量核心 ✅（C++ + Medieval 四足动物 anatomy）；伤害扩散机制 ⏳（策划已定，待实现）

---

## 一、目标

让 CDDA 的怪物从"单一全局 HP"改为"多部位 HP"，为后续"部位瞄准"和"部位伤害影响行动"提供数据基础。

---

## 二、核心设计决策

### 2.1 保留 `type->hp` 作为基准

`body_part::base_hp` 解释为 `type->hp` 的百分比系数：

```
part_hp_max = round( type->hp × base_hp / 100 )
```

- `type->hp` 是怪物类型的整体耐打基准
- `base_hp` 只表示该部位占整体的比例
- 同一 anatomy 模板可适配不同体型怪物

### 2.2 死亡判定改为 vital 部位

- 任一 `is_vital == true` 的部位 HP ≤ 0 → 怪物死亡
- 与 NPC/玩家 (`Character::is_dead_state`) 逻辑一致
- 无 vital 部位的 anatomy fallback 到总 HP ≤ 0，避免不死

### 2.3 移除 `monster::hp` 影子字段

- 删除 `monster::hp` 字段
- 删除 `monster::get_hp()` / `get_hp_max()` 覆写，让 `Creature` 基类的部位求和接管
- 所有原先读写 `hp` 的代码改为操作部位 HP

### 2.4 部位定制原则：拒绝通用模板

Medieval 的生物形态差异极大（普通野兽、牛头人、龙、狮鹫等），**不能简单复用一套"头/躯干/四肢"模板**。策划上遵循以下原则：

- **每个显著怪物类型应有自己的 head 定义**
  - 狼头 ≠ 熊头 ≠ 牛头人的角头 ≠ 龙头
  - 头部差异体现在：hit_size、视觉能力、听觉能力、角/喙/牙等特殊攻击入口
- **同一生态位共用 anatomy 模板，但关键部位可 override**
  - 例如所有四足动物共用 `medieval_quadruped_anatomy`
  - 但龙的头部应替换为 `medieval_dragon_head`，并额外增加 `wing` 部位
- **避免"人类部位换皮"**
  - 不用 `human_anatomy` 改名字来冒充怪物
  - 怪物的 limb_score、hit_size、vital 关系需重新设计

---

## 三、C++ 改造清单

| 文件 | 改造内容 |
|---|---|
| `src/monster.h` | 删除 `hp` 字段；删除 `get_hp/get_hp_max` 覆写；新增 `init_body_hp()` |
| `src/monster.cpp` | 构造函数/`is_dead_state`/`apply_damage`/`heal`/`set_hp`/`poly`/`init_from_item`/`to_item`/`explode`/`die_in_explosion`/`hp_percentage` 全面改用部位 HP |
| `src/monattack.cpp` | blob 分裂条件改为 `get_hp() > 2 * get_hp_max()` |
| `src/monster_oracle.cpp` | 同步分裂判定 |
| `src/savegame_json.cpp` | 新存档不再写 `"hp"`；旧存档读取后迁移到部位 HP |
| `tests/behavior_test.cpp` | 分裂测试适配新语义 |

### 关键函数行为

| 函数 | 行为 |
|---|---|
| `init_body_hp(total_hp)` | 按 `base_hp * total_hp / 100` 初始化所有部位 |
| `is_dead_state()` | vital 部位 ≤ 0 即死亡 |
| `apply_damage()` | 只扣部位 HP；死亡时 `set_killer` |
| `deal_damage()` | 新增溢出伤害扩散逻辑（2026-06-27 补充） |
| `heal(delta_hp)` | 按各部位 `hp_max` 比例分配治疗 |
| `set_hp(hp)` | 按比例缩放所有部位当前 HP |
| `poly()` | 按 `get_hp() / get_hp_max()` 百分比保留 |
| `explode()` | 一个 vital 部位设为 `INT_MIN + 1`，其余 vital 归零，保持 `-get_hp()` 巨大 |

---

## 四、JSON 数据

### 4.1 Medieval 四足动物部位

文件：`data/mods/Medieval/10_medieval_core/body_parts.json`

| 部位 | base_hp | hit_size | is_vital | 说明 |
|---|---|---|---|---|
| `medieval_quadruped_torso` | 80 | 24 | ✅ | 躯干 |
| `medieval_quadruped_head` | 60 | 6 | ✅ | 头 |
| `medieval_quadruped_front_leg_l` | 25 | 6 | — | 左前腿 |
| `medieval_quadruped_front_leg_r` | 25 | 6 | — | 右前腿 |
| `medieval_quadruped_hind_leg_l` | 28 | 7 | — | 左后腿 |
| `medieval_quadruped_hind_leg_r` | 28 | 7 | — | 右后腿 |
| `medieval_quadruped_tail` | 30 | 4 | — | 尾巴 |

### 4.2 Medieval 四足动物 anatomy

文件：`data/mods/Medieval/10_medieval_core/anatomy.json`

- `medieval_quadruped_anatomy`：torso / head / front_leg_l / front_leg_r / hind_leg_l / hind_leg_r / tail

### 4.3 bodytype 默认 anatomy 映射

怪物 JSON 未指定 `"anatomy"` 时，按 `bodytype` 自动选择：

| bodytype | 默认 anatomy |
|---|---|
| bear, dog, wolf, cat, pig, boar, deer, cow, horse, goat, sheep | `medieval_quadruped_anatomy` |
| human, zombie | `human_anatomy` |
| 其他 | `default_anatomy` |

---

## 五、伤害扩散机制

> 2026-06-27 补充：解决"命中已残废部位后伤害消失或只扣负 HP"的问题。

### 5.1 设计目标

当一次攻击命中的部位已经残废（或单次伤害超过该部位剩余 HP）时，溢出伤害不应浪费，而应像塔科夫一样按解剖连接关系扩散到其他部位。

### 5.2 触发条件

| 目标部位状态 | 行为 |
|---|---|
| `HP > 0` 且 `伤害 <= HP` | 全额作用于目标部位，无扩散 |
| `HP > 0` 且 `伤害 > HP` | 先打空目标部位，**溢出部分扩散** |
| `HP <= 0` | 目标部位**完全不吃伤害**，整次伤害进入扩散池 |

### 5.3 扩散目标选择

- 从命中部位出发，像 targeting_graph 那样**随机选一条扩散路径**（按 hit_size 权重选邻居）
- 路径最多 2 步，即最多扩散到 **2 个部位**
- 无论 anatomy 有多少部位，扩散目标固定为路径上的 1~2 个部位

### 5.4 扩散系数

权重随机化，但总和固定为 1.2：

| 路径位置 | 权重范围 |
|---|---|
| 距离 1（path[1]） | 0.5 ~ 0.9（随机） |
| 距离 2（path[2]） | 1.2 − 距离1（即 0.3 ~ 0.7） |

每次扩散独立掷骰，距离1 部位有时分到更多，有时更少。

### 5.5 伤害分配

1. 随机生成扩散路径 `[bp, neighbor1, neighbor2]`
2. 取 path[1]（权重 0.7）和 path[2]（权重 0.5，如存在）
3. 按权重比例分配溢出伤害
4. 整数化采用**最大余额法**（floor + 按小数部分排序补齐）
5. 扩散伤害**不再计算护甲**（视为钝力冲击/内部创伤）
6. 扩散可以进入 vital 部位，大动脉/内脏受损视为合理

### 5.6 一致性

玩家、NPC、怪物**完全一致**，没有单独优待。

### 5.7 示例

黑熊左前腿已残废（HP=0），一次弩箭命中造成 20 点伤害：

- 左前腿：不吃伤害，20 点进入扩散池
- 随机选扩散路径：左前腿 → 躯干 → 头部（路径随机，每次不同）
- 躯干（path[1]，权重 0.7）：20 × 0.7/1.2 = 11.7 → 12
- 头部（path[2]，权重 0.5）：20 × 0.5/1.2 = 8.3 → 8

如果路径只有 1 步（如命中尾部，只有躯干一个邻居）：
- 躯干（path[1]，权重 0.7）：20 × 0.7/0.7 = 20（全额给唯一目标）

---

## 六、已知限制

- 怪物目前没有 NPC 那样的 `limb_score` 系统，部位 HP 降低不会自动影响移动/攻击/感知
- 非 vital 部位 HP = 0 没有任何效果（如腿断不减速）
- 这些限制在 [design09_2-怪物部位行动影响](design09_2-怪物部位行动影响.md) 中解决

---

## 七、关联文档

- [design09-战斗系统重置](design09-战斗系统重置.md)
- [design09_2-怪物部位行动影响](design09_2-怪物部位行动影响.md)
- [process/monster_bodypart_fix.md](../process/monster_bodypart_fix.md)
