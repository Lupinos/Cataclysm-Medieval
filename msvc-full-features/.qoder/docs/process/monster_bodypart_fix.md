# 任务：Monster 部位 HP 修复

## 目标

让 Monster 系统支持部位分血——攻击打到的部位扣该部位的 HP，而非全局 HP。为野生动物/巨怪/龙类提供完整战斗体验（部位骨折、流血、不同部位不同 base_hp/hit_size）。

## 依赖

- [design08-敌人.md](../design/design08-敌人.md) 双系统分层决策
- [code_bodypart_hp_system.md](../vanilla/code_bodypart_hp_system.md) 部位分血架构现状
- [code_harvest_drop_system.md](../vanilla/code_harvest_drop_system.md) 产物系统

---

## 改造内容

### 阶段 1：C++ 核心修复（已完成）

#### 1.1 `src/mtype.h` — 加 anatomy 字段 ✅

```cpp
anatomy_id anatomy = anatomy_id( "default_anatomy" );
```

#### 1.2 `src/monstergenerator.cpp` — 加载 anatomy ✅

```cpp
optional( jo, was_loaded, "anatomy", mon.anatomy, anatomy_id( "default_anatomy" ) );
```

#### 1.3 `src/monster.cpp` — 构造时改用自身 anatomy ✅

```cpp
set_anatomy( type->anatomy );
```

#### 1.4 `src/monster.cpp` — `apply_damage` 同步部位 HP ✅（过渡方案）

```cpp
void monster::apply_damage( Creature *source, bodypart_id bp, int dam, ... ) {
    if( has_part( bp, body_part_filter::next_best ) ) {
        mod_part_hp_cur( bp, -dam );  // 部位 HP
    }
    hp -= dam;  // 全局 HP 保持同步，避免破坏依赖 hp 字段的代码
}
```

> 注：当前为过渡方案。全局 HP 仍用于死亡判定与旧代码，部位 HP 用于远程瞄准等新增系统。后续可切换为纯部位 HP + vital 部位死亡判定。

#### 1.5 `src/monster.cpp` — 部位 HP 按 `type->hp` 百分比缩放 ✅

`body_part::base_hp` 解释为 `type->hp` 的百分比系数：

```cpp
part_hp_max = round( type->hp * base_hp / 100 )
```

使同一 anatomy 模板能适配不同体型的怪物（熊大血多，狼小血少）。

#### 1.6 `src/monstergenerator.cpp` — `bodytype` 默认 anatomy 映射 ✅

怪物 JSON 未指定 `"anatomy"` 时，按 `bodytype` 自动选择：

| bodytype | 默认 anatomy |
|---|---|
| `bear`, `dog`, `wolf`, `cat`, `pig`, `boar`, `deer`, `cow`, `horse`, `goat`, `sheep` | `medieval_quadruped_anatomy` |
| `human`, `zombie` | `human_anatomy` |
| 其他 | `default_anatomy` |

### 阶段 2：新建部位类型（JSON）

#### 2.1 四足动物部位（已完成 ✅）

文件：`data/mods/Medieval/10_medieval_core/body_parts.json`

| 部位 | base_hp（系数） | hit_size | is_vital | 说明 |
|------|-----------------|----------|----------|------|
| `medieval_quadruped_torso` | 80 | 24 | ✅ | 躯干 |
| `medieval_quadruped_head` | 60 | 6 | ✅ | 头 |
| `medieval_quadruped_front_leg_l` | 25 | 6 | — | 左前腿 |
| `medieval_quadruped_front_leg_r` | 25 | 6 | — | 右前腿 |
| `medieval_quadruped_hind_leg_l` | 28 | 7 | — | 左后腿 |
| `medieval_quadruped_hind_leg_r` | 28 | 7 | — | 右后腿 |
| `medieval_quadruped_tail` | 30 | 4 | — | 尾巴 |

> `base_hp` 是 `type->hp` 的百分比系数，非绝对血量。

#### 2.2 奇幻生物部位（待做）

| 部位 | base_hp | hit_size | 说明 |
|------|---------|----------|------|
| `wing_l` | 40 | 18 | 左翼 |
| `wing_r` | 40 | 18 | 右翼 |
| `neck` | 30 | 5 | 颈部（狮鹫） |
| `tail` | 20 | 8 | 尾巴（龙） |

### 阶段 3：新建 anatomy（JSON）

#### 3.1 四足动物 anatomy（已完成 ✅）

- `medieval_quadruped_anatomy`：torso / head / front_legs / hind_legs / tail

#### 3.2 奇幻生物 anatomy（待做）

| anatomy | 部位数 | 说明 |
|---------|--------|------|
| `anatomy_griffin` | 10 | head/torso/limbs×4 + wings×2 + feet×2 |
| `anatomy_drake` | 8 | head/torso/limbs×4 + tail |
| `anatomy_hydra` | 4 + 3×N | head×N/torso/limbs×2（N 个头） |

### 阶段 4：已有 Monster 的 anatomy 字段补充

现有 monster 都缺 `anatomy` 字段——不加的话默认走 `default_anatomy`（只有 head/torso 2 个部位）。

| 怪物 | 新建 anatomy | 是否急需 |
|------|-------------|---------|
| bear → `anatomy_bear` | 沿用 human_anatomy（8 部位） | 否，先用 default 也能工作 |
| wolf → `anatomy_wolf` | 6 部位（四足+头+躯干） | 否 |
| drake → `anatomy_drake` | 8 部位 | 是 |
| griffin → `anatomy_griffin` | 10 部位 | 是 |

### 阶段 5：移除 `monster::hp` 全局血，改纯部位 HP（已完成 ✅）

#### 5.1 `src/monster.h` — 删除 `hp` 字段与 `get_hp/get_hp_max` 覆写 ✅

让 `Creature` 基类的部位求和实现接管。

#### 5.2 `src/monster.cpp` — 核心函数改造 ✅

| 函数 | 改造 |
|---|---|
| 默认/id 构造函数 | 新增 `init_body_hp(total_hp)`，按 `base_hp * total_hp / 100` 初始化部位 |
| `is_dead_state()` | 任一 `is_vital` 部位 HP ≤ 0 即死亡；无 vital 部位时 fallback 到总 HP ≤ 0 |
| `apply_damage()` | 只扣部位 HP；死亡时 `set_killer` |
| `heal()` | 按各部位 `hp_max` 比例分配治疗量 |
| `set_hp()` | 按比例缩放所有部位当前 HP |
| `poly()` | 按 `get_hp() / get_hp_max()` 百分比转换到新类型 |
| `init_from_item()` | 用 `set_hp()` 处理尸体损坏/灼烧；机器人复活同样处理 |
| `to_item()` | 用 `get_hp() / get_hp_max()` 计算物品损坏 |
| `explode()` | 把一个 vital 部位设为 `INT_MIN + 1`，其余 vital 归零，保持 `-get_hp()` 巨大 |
| `die_in_explosion()` | 所有 vital 部位设为 -9999 |
| `hp_percentage()` | 改为 `get_hp() * 100 / get_hp_max()` |
| 运行时引用 M1-M6 | morale regen、SUNDEATH、速度恢复等改用 `get_hp() / get_hp_max()` |

#### 5.3 `src/monattack.cpp` / `src/monster_oracle.cpp` — 分裂逻辑 ✅

原条件 `hp / 2 > type->hp` 在改后永远为 false。改为：

```cpp
while( get_hp() > 2 * get_hp_max() ) {
    set_hp( get_hp() - get_hp_max() );
}
```

#### 5.4 `src/savegame_json.cpp` — 序列化兼容 ✅

- 写入：不再写 `"hp"` 字段（body parts 已由 `Creature::store` 保存）
- 读取：若旧存档有 `"hp"`，读取后 `set_hp(legacy_hp)` 迁移到部位 HP

#### 5.5 `tests/behavior_test.cpp` ✅

分裂测试的 new_hp 从 `type->hp * 2 + 2` 改为 `get_hp_max() * 2 + 2`。

---

## 测试点

1. `mon_bear` 受击后 `get_part_hp_cur(head)` 降低，而非全局 `hp`
2. 致命部位（is_vital）归零 → 死亡
3. 非致命部位（wing_l）归零 → 不死亡，但可能影响移动/攻击
4. `harvest` 产物在死亡时正常生成
5. `dissect` 产物在死亡时预生成进尸体口袋

---

### 阶段 6：部位伤害影响怪物行动（进行中 ⏳，方案 A：limb_score）

#### 6.1 设计决策

- 采用 **方案 A**：让怪物使用与 NPC/玩家统一的 `limb_score` 体系
- 本期只接入三层：移动速度、视觉、近战/撕咬
- 无 limb_score 贡献的怪物返回 1.0，避免破坏原版/default_anatomy 怪物

#### 6.2 Medieval body_part limb_scores 补全（已完成 ✅）

文件：`data/mods/Medieval/10_medieval_core/body_parts.json`

| 部位 | limb_scores |
|---|---|
| `medieval_quadruped_torso` | `balance` 0.7 |
| `medieval_quadruped_head` | `reaction` 0.2, `vision` 0.3, `night_vis` 0.3 |
| `medieval_quadruped_front_leg_l` | `grip` 0.15, `manip` 0.05 |
| `medieval_quadruped_front_leg_r` | `grip` 0.15, `manip` 0.05 |
| `medieval_quadruped_hind_leg_l` | `move_speed` 0.25 |
| `medieval_quadruped_hind_leg_r` | `move_speed` 0.25 |
| `medieval_quadruped_tail` | `balance` 0.3 |

#### 6.3 C++ 实现（进行中）

| 文件 | 改造 |
|---|---|
| `src/monster.h` | 新增 `get_speed() override` 和 `get_limb_score()` 声明 |
| `src/monster.cpp` | 实现 `get_limb_score()`；`get_speed()` 乘 `move_speed` score；`sight_range()` / `get_eff_per()` 乘 vision score；`melee_attack()` 乘 grip/manip score |

#### 6.4 效果规则

| 能力 | 依赖 score | 效果 |
|---|---|---|
| 移动速度 | `move_speed` | 后腿受伤 → 减速；两腿全断 → 接近爬行 |
| 视觉 | `vision` / `night_vis` | 头部/眼睛受伤 → 视野缩短 |
| 近战/撕咬 | `grip` / `manip` | 前肢/口器受伤 → 伤害下降，最低 25% |

---

## 测试点

1. `mon_bear` 受击后 `get_part_hp_cur(head)` 降低，而非全局 `hp`
2. 致命部位（is_vital）归零 → 死亡
3. 非致命部位（wing_l）归零 → 不死亡，但可能影响移动/攻击
4. `harvest` 产物在死亡时正常生成
5. `dissect` 产物在死亡时预生成进尸体口袋
6. 狼/熊后腿受伤后移动速度下降
7. 头部受伤后怪物视觉范围缩短
8. 前肢受伤后近战伤害下降

---

### 阶段 7：伤害扩散机制（进行中 ⏳：代码已实现，待编译测试）

基于 [design09_1-部位血量系统](../design/design09_1-部位血量系统.md) 中新增的伤害扩散设计。

| 文件 | 改造 |
|---|---|
| `src/creature.cpp` — `deal_damage()` | 溢出/残废部位伤害按 BFS 距离加权扩散到全身；扩散伤害不重新计算护甲；玩家/NPC/怪物一致 |

#### 7.1 核心规则

- 触发：`HP > 0` 但单次伤害超过剩余 HP 时，溢出部分扩散；`HP <= 0` 时整次伤害扩散
- 原部位：`HP <= 0` 后完全不吃伤害
- 目标：随机选一条扩散路径（按 hit_size 权重），最多 2 个部位
- 系数：距离1 ∈ [0.5, 0.9] 随机，距离2 = 1.2 − 距离1（总和固定 1.2）
- 分配：按权重比例分配，最大余额法整数化
- 护甲：扩散伤害不再计算护甲
- 一致性：玩家、NPC、怪物完全一致

#### 7.2 测试点

1. 命中满血部位，伤害未溢出时，只扣目标部位
2. 命中残废非 vital 部位，伤害扩散到躯干等相邻部位
3. 扩散伤害可进入 vital 部位并触发死亡
4. 玩家被怪物打残腿后，继续打腿的伤害会扩散到躯干

#### 7.3 工作量评估

| 工作项 | 复杂度 | 说明 |
|---|---|---|
| `src/anatomy.h` / `src/anatomy.cpp` | 低 | 新增 `get_distance_map(root)` 或复用 `targeting_graph`，返回 root 到各部位的 BFS 距离（限制 ≤2） |
| `src/creature.cpp` — `Creature::deal_damage()` | 中 | 在 `apply_damage` 前插入扩散逻辑：计算溢出 → 查询距离 → 按系数加权分配 → 对每个候选部位调用 `apply_damage` |
| `src/character.cpp` — `Character::deal_damage()` | 低（复用） | `Character::deal_damage()` 会先调用 `Creature::deal_damage()`，扩散自动生效；但出血/感染/疼痛等后续效果仍基于原始命中部位，需在测试中确认是否可接受 |
| 调试输出 | 低 | 可加临时 log 显示溢出伤害、扩散目标及分配量 |
| 平衡测试 | 中高 | 需验证：满级角色/怪物是否因扩散过快击杀；玩家被围攻时是否暴毙 |

**预估**：约 1.5~2 小时编码 + 1~2 小时测试调参。

**主要风险**：
- `Creature::deal_damage()` 是核心路径，改动影响所有生物（怪物、NPC、玩家）
- 扩散伤害绕过护甲后，高伤武器可能异常强力
- Character 的后续效果（出血、感染、疼痛）不会为扩散部位分别触发，可能需要在 `spread_damage` 中手动补一些效果，或接受其作为"内部创伤"不触发外伤效果

---

## 风险

- `apply_damage` 修改后，所有现有 monster 的死亡判定从"全局 hp<=0"变成"致命部位 hp<=0"——需验证已有 monster（特别是 boss 级）的生存力是否下降
- 已有 UI 显示的是全局 HP 条——修复后需要确认是否显示部位总 HP（`get_hp()` 求和已自动支持）
- 怪物 `get_limb_score` 对无贡献 anatomy 返回 1.0 的兜底逻辑，需确认不会意外放大能力
- 伤害扩散机制会显著改变"打腿刮痧"体验，需关注玩家生存压力是否过大
