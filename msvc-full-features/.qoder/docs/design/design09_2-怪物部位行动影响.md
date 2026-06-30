# 战斗系统子系统：怪物部位伤害对行动的影响

> 对应 [design09-战斗系统重置](design09-战斗系统重置.md) 的延伸设计。
> 实现状态：**进行中** ⏳（方案 A 已选定，优先实现移动/视觉/近战三层）

---

## 一、设计目标

在 [design09_1-部位血量系统](design09_1-部位血量系统.md) 基础上，让怪物受伤后**真实地变弱**，而不是只影响总血量。

 Medieval 阶段只聚焦三层最直观的效果：
1. **移动**：腿伤 → 减速/无法移动
2. **视觉**：头/眼伤 → 视野缩短
3. **近战/撕咬**：口器/前肢伤 → 伤害下降/攻击禁用

特殊攻击、飞行坠落、感知细分等放到后续版本。

---

## 二、方案选择：方案 A（limb_score 统一架构）

### 2.1 选择理由

- 与 NPC/玩家共享同一套能力评分体系，规则一致
- 怪物能力随伤口自然衰减，不需要为每种行动硬编码
- Medieval 当前 body_part 数量很少（5 个主部位），补全 limb_scores 工作量可控
- 后续奇幻生物（龙角、狮鹫翼等）可以通过自定义 body_part + limb_scores 自然扩展

### 2.2 实现范围

| 层级 | 本期做 | 后续做 |
|---|---|---|
| 移动速度 | ✅ `move_speed` score | — |
| 视觉 | ✅ `vision` / `night_vis` score | 嗅觉、听觉 |
| 近战/撕咬 | ✅ `grip` / `manip` score | 特殊攻击禁用 |
| 飞行 | — | 翅膀部位 + 坠落 |
| 平衡/闪避 | — | `balance` score |
| 游泳 | — | `swim` score |

---

## 三、怪物行动与 limb_score 的映射

| 怪物行动 | 相关能力 | 本期是否接入 |
|---|---|---|
| 地面行走 | `move_speed` | ✅ |
| 游泳 | `swim` | ❌ |
| 飞行 | `move_speed` + 翅膀部位 | ❌ |
| 近战基础攻击 | `grip` / `manip` | ✅ |
| 撕咬 | `grip` / `manip` | ✅ |
| 格挡 | `block` | ❌ |
| 闪避 | `balance` / `reaction` | ❌ |
| 视觉 | `vision` / `night_vis` | ✅ |
| 听觉/嗅觉 | 暂无对应 score | ❌ |

---

## 四、部位功能设计

 Medieval 不追求通用模板，而是**每个生态位有自己的部位定义**。

### 4.1 四足动物基础模板

文件：`data/mods/Medieval/10_medieval_core/body_parts.json`

| 部位 | limb_type | 本期 limb_scores | 功能 |
|---|---|---|---|
| `medieval_quadruped_torso` | torso | `balance` 0.7 | 躯干平衡（hit_size 24） |
| `medieval_quadruped_head` | head | `reaction` 0.2, `vision` 0.3, `night_vis` 0.3 | 头：感知与反应 |
| `medieval_quadruped_front_leg_l` | arm | `grip` 0.15, `manip` 0.05 | 左前肢：抓握/扑击 |
| `medieval_quadruped_front_leg_r` | arm | `grip` 0.15, `manip` 0.05 | 右前肢：抓握/扑击 |
| `medieval_quadruped_hind_leg_l` | leg | `move_speed` 0.25 | 左后腿：主要动力 |
| `medieval_quadruped_hind_leg_r` | leg | `move_speed` 0.25 | 右后腿：主要动力 |
| `medieval_quadruped_tail` | tail | `balance` 0.3 | 尾巴：平衡 |

### 4.2 部位定制原则

- **每个显著怪物类型应有自己的 head**
  - 狼头、熊头、牛头人的角头、龙头各自独立定义
  - 差异体现在 hit_size、视觉 score、是否带角/喙/牙
- **同一生态位可共用模板，但关键部位可 override**
  - 四足动物共用躯干/腿/尾模板
  - 龙替换头部为 `medieval_dragon_head`，并额外增加 `wing_l` / `wing_r`
- **避免人类部位换皮**
  - 不使用 `human_anatomy` 修改名字冒充怪物

---

## 五、伤害对行动的影响规则

### 5.1 移动速度

怪物实际移动速度 = `type->speed` × `move_speed` limb_score

- 后腿 HP 下降 → `move_speed` score 下降 → 速度下降
- 两腿都坏 → `move_speed` 接近 0 → 怪物无法主动移动
- 最低保留少量移动能力（爬行），除非两腿全断

### 5.2 视觉

怪物实际视觉 = `type->vision_day` × `vision` score

- 头部/眼睛 HP 下降 → `vision` score 下降 → 视野缩短
- 头部 HP = 0 → 死亡（vital，已有）

### 5.3 近战与撕咬

怪物近战伤害倍率 = `grip` / `manip` score

- 前肢/口器 HP 下降 → 伤害下降
- 前肢/口器 HP = 0 → 基础近战伤害极低，撕咬类攻击禁用

---

## 六、实施阶段

### 阶段 1：C++ 基础设施

- 将 `get_limb_score` 相关逻辑从 `Character` 下放到 `Creature`，或给 `monster` 单独实现等价逻辑
- 让 `monster` 能够读取自身 body 的 limb_scores

### 阶段 2：补全 Medieval body_part 数据

- 为 5 个四足动物部位配置完整 limb_scores
- 后续为奇幻生物新增专属部位

### 阶段 3：接入怪物行动

- 移动：`monster::speed_rating()` / `get_speed()` 读取 `move_speed`
- 视觉：`vision_day` / `vision_night` 读取 `vision` / `night_vis`
- 近战/撕咬：基础近战伤害读取 `grip` / `manip`

### 阶段 4：测试

- 测试狼/熊后腿受伤后是否减速
- 测试头部受伤后视野是否缩短
- 测试前肢受伤后近战伤害是否下降

---

## 七、风险与待决策

| 问题 | 本期处理 |
|---|---|
| 怪物 body_part 没有 `is_limb` 是否影响 limb_score？ | 调研后确认，本期按 `limb_type` 处理 |
| `get_limb_score` 从 `Character` 提升到 `Creature` 会不会破坏 NPC 逻辑？ | 保持 `Character` 现有接口不变，仅把核心计算逻辑下沉 |
| 多腿怪物如何计算 move_speed？ | 汇总所有 leg 类型部位的 score，与玩家双腿逻辑一致 |
| 飞行怪物本期如何处理？ | 本期不处理，保持 `FLIES` 标志原行为 |

---

## 八、关联文档

- [design09-战斗系统重置](design09-战斗系统重置.md)
- [design09_1-部位血量系统](design09_1-部位血量系统.md)
- [process/monster_bodypart_fix.md](../process/monster_bodypart_fix.md)
