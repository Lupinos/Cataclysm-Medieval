# 参考文档：CDDA 战斗系统配置调研

> 原版基准：CDDA 0.H 维护分支提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 项目初始化前）。下列路径、字段与流程以该提交为准，不代表后续 Medieval 改造。
> 覆盖：techniques.json / martialarts.json / body_parts.json / anatomy.json / limb_scores.json / hit_range.json / effects.json（战斗相关部分）

---

## 一、相关文件索引

```
json/
├── techniques.json              ← ★ 技术/招式定义（3494 行，167 个技术）
├── martialarts.json             ← ★ 武术流派定义（1617 行，30+ 风格）
├── martialarts_fictional.json   ← 虚构流派（694 行，额外 8+ 风格）
├── body_parts.json              ← ★ 身体部位定义（1436 行，12 主要部位 + 子部位）
├── anatomy.json                 ← 解剖结构（12 行，human_anatomy + default_anatomy）
├── limb_scores.json             ← 肢体能力评分（94 行，12 项派生属性）
├── hit_range.json               ← 命中精度概率表（67 行，60 个数值档位）
├── effects.json                 ← ★ 状态效果定义（156 KB，含战斗核心状态）
├── melee.json                   ← 近战武器定义（含武器技术关联）
└── monster_attacks.json         ← 怪物攻击模式定义
```

> **核心要点**：CDDA 战斗系统由 6 个 JSON 类型协同构成——`technique`（招式）、`martial_art`（流派）、`body_part`（部位）、`effect_type`（状态）、`limb_score`（能力）、`hit_range`（精度）。

---

## 二、核心配置类型

### 2.1 `technique` —— 招式/技术

> 167 个定义，扣除 3 个 dummy 和约 20 个防御性/功能性技术，约 **140 个实际攻击技术**。

| 字段 | 类型 | 说明 | 取值示例 |
|------|------|------|----------|
| `id` / `name` | string | 技术标识/显示名 | `"SWEEP"` → "Sweep Attack" |
| `melee_allowed` | bool | 是否可用于近战 | 多数为 `true` |
| `unarmed_allowed` | bool | 是否可用于徒手 | 拳法/腿法为 `true` |
| `skill_requirements` | array | 技能门槛 | `[{ "name": "melee", "level": 3 }]` |
| **`crit_tec`** | bool | 是否仅暴击时触发 | 控制技/必杀技常为 `true` |
| `crit_ok` | bool | 暴击时也可触发 | 与 `crit_tec` 不同——任何攻击都可用，暴击时也兼容 |
| `defensive` | bool | 防御性技术（格挡/闪避触发） | `"grab_break"`, `"miss_recovery"` |
| **`stun_dur`** | int | 击晕持续回合 | 1~2 |
| **`down_dur`** | int | 击倒持续回合 | 1~2 |
| **`knockback_dist`** | int | 击退距离（格） | 1~2 |
| `disarms` | bool | 缴械 | 卸除对手武器 |
| `grab_break` | bool | 挣脱抓取 | 破坏对手的 grab 状态 |
| `miss_recovery` | bool | 攻击落空后恢复 | 减少落空惩罚 |
| **`aoe`** | enum | 范围攻击类型 | `"spin"` / `"wide"` / `"impale"` |
| **`condition`** | object | 触发条件（math 判定） | 见 §一— |
| **`attack_vectors`** | array | 攻击肢体 | `["WEAPON"]`, `["HAND"]`, `["FOOT"]`, `["ELBOW"]`, `["KNEE"]`, `["PALM"]`, `["GRAPPLE"]`, `["THROW"]` |
| **`weighting`** | int | 攻击自动选择权重（含玩家） | -250 ~ 100，正数越大概率越高 |
| **`mult_bonuses`** | array | 倍率加成 | `[{ "stat": "movecost", "scale": 0.5 }]` |
| **`flat_bonuses`** | array | 固定值加成 | `[{ "stat": "movecost", "scale": 100 }]` |
| `tech_effects` | array | 附加效果，是否要求伤害取决于条目on_damage | 如 disarmed 效果 |
| `messages` | array | 战斗日志文本 | `["You sweep %s!", "<npcname> sweeps %s!"]` |
| `required_buffs_all` | array | 前置 buff（流派触发链） | 如 `["buff_aikido_onblock"]` |
| **`eocs`** | array | EOC 事件钩子 | 更灵活的触发效果 |

#### attack_vectors 分布

| 攻击肢体 | 数量 | 代表技术 |
|----------|------|----------|
| `WEAPON` | ~90 | 绝大多数武器技 |
| `HAND` | ~25 | 拳法（Jab, Cross, Uppercut） |
| `FOOT` | ~10 | 腿法（Sweep Kick, Spin Kick） |
| `THROW` | ~10 | 投技（Judo Throw） |
| `KNEE` / `ELBOW` / `PALM` | ~5 | 特种技 |
| `GRAPPLE` | ~2 | 关节技 |
| 组合 `[WEAPON, HAND]` | ~5 | 武器+徒手双修技 |

#### movecost 缩放分布（从实际数据统计）

| 倍率 | 含义 | 技术数量 | 典型技 |
|------|------|----------|--------|
| 0.3x | 极快 | 1 | KRAV_MAGA_CUT |
| 0.5x | 快速 | ~15 | Jab, Sweep, 多数轻技 |
| 0.6~0.66x | 较快 | ~5 | 部分连击 |
| 0.7~0.8x | 略快 | ~40 | 多数常规技 |
| 0.9x | 近乎正常 | ~3 | — |
| 1.1~1.2x | 略慢高伤 | ~3 | SWEETSPOT (2.5x 伤害) |
| 1.5x | 重击 | ~3 | 少数双手/蓄力技 |
| 1.75x | 极重 | 1 | — |
| 不变 | 正常 | ~20 | 功能技（缴械/破抓/虚招） |

#### condition 判定系统

技术通过 `condition` 字段实现智能触发，主要判定维度：

```
condition 结构
├── math 判定
│   ├── u_val('size') >= n_val('size')     ← 攻击者体型≥目标
│   ├── n_val('size') != 1                 ← 目标不是最小体型
│   └── u_val('size') + 1 >= n_val('size') ← 攻击者体型+1≥目标（略宽松）
├── bodytype 判定
│   ├── npc_bodytype: "human"              ← 仅人形目标
│   └── npc_bodytype: "angel"              ← 天使类人形
├── effect 判定
│   ├── not npc_has_effect "stunned"       ← 目标未晕眩
│   ├── not npc_has_effect "downed"        ← 目标未倒地
│   └── not npc_has_effect "flying"         ← 目标未飞行
├── flag 判定
│   ├── npc_has_flag "FLIES"               ← 目标会飞
│   ├── npc_has_flag "DISABLE_FLIGHT"      ← 飞行被禁用
│   ├── npc_has_flag "GRAB_FILTER"          ← 可被擒拿的体型
│   └── u_has_flag "GRAB"                  ← 使用者正在擒拿
├── species 排除（BRUTAL 技术示例）
│   └── not npc_has_species: NETHER, SLIME, ROBOT, HORROR ...
└── roll_contested（对抗掷骰）
    └── u_val('strength') vs n_val('grab_strength')  ← 擒拿强度对抗
```

#### 典型技术案例

**SWEEP**（扫腿）—— 控制技模式：
```
type: technique
crit_tec: 未设置（默认false），不是暴击专属
condition: 体型≤攻击者+1, 人形, 非倒地, 不能飞行
down_dur: 2                              ← 击倒 2 回合
attack_vectors: [WEAPON]                 ← 武器柄/杆施展
weighting: 未设置（默认1）
```

**BRUTAL**（野蛮打击）—— 条件筛选链：
```
type: technique
crit_tec: true
stun_dur: 1, knockback_dist: 1           ← 击晕+击退
condition:
  1. 体型≥目标（不翻大个子）
  2. 目标未晕眩
  3. 排除 13 种非人形物种
  4. 如果目标可被擒拿且使用者正在擒拿 → 力量对抗掷骰
```

**tec_aikido_blockthrow** —— 流派 buff 链技术：
```
type: technique
crit_ok: true                            ← 非暴击也可触发
required_buffs_all: ["buff_aikido_onblock"] ← 需处于"格挡后"buff 状态
condition: 体型判定 + 人形 + 非倒地 + 不能飞行 + grab 对抗
attack_vectors: [THROW]
```

---

### 2.2 `martial_art` —— 武术流派

> 30+ 种风格，`martialarts.json` 中含 Aikido、Boxing、Brawling、Capoeira、Crane、Dragon、Eskrima、Fencing、Judo、Karate、Krav Maga、Muay Thai、Ninjutsu、Pankration、Silat、Taekwondo、Tai Chi、Wing Chun、Zui Quan 等。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | string | 风格唯一标识 | `"style_aikido"` |
| `name` | object | 显示名 | `{ "str": "Aikido" }` |
| `description` | string | 风格描述 | — |
| `priority` | int | 多个风格可用的优先级 | 0~1 |
| `learn_difficulty` | int | 学习难度 | 1（Boxing）~ 10（Crane） |
| `primary_skill` | string | 主技能 | `"bashing"`, `"cutting"` 等 |
| `arm_block` / `leg_block` | int | 手臂/腿格挡能力 | 数值越高越适合 |
| `allow_all_weapons` | bool | 是否适用所有武器 | Brawling 为 true |
| `force_unarmed` | bool | 强制徒手 | style_kicks 为 true |
| `strictly_melee` | bool | 仅限特定武器类 | Bōjutsu 仅长棍 |
| `weapon_category` | array | 可用武器类别 | `["QUARTERSTAVES"]`, `["CLAWS"]` |
| `autolearn` | array | 自动学习条件 | Brawling: melee lv1 自动学会 |
| `teachable` | bool | 是否可教授 | — |
| **`static_buffs`** | array | 常驻被动 buff（可分层级） | 见下表 |
| **`techniques`** | array | 可用技术 ID 列表 | `["tec_aikido_break", ...]` |
| **`onblock_buffs`** | array | 格挡成功时触发 | — |
| **`ondodge_buffs`** | array | 闪避成功时触发 | — |
| **`onmove_buffs`** | array | 移动时触发 | — |
| **`onattack_buffs`** | array | 攻击命中/落空时触发 | — |
| `onkill_buffs` | array | 击杀时触发 | — |
| `oncrit_buffs` | array | 暴击时触发 | — |
| `onmiss_buffs` | array | 攻击落空时触发 | — |
| `onpause_buffs` | array | 等待回合时触发（蓄力） | — |
| `onhit_buffs` | array | 命中时触发 | — |
| `onkill_eocs` | array | 击杀时 EOC 事件 | — |
| `ongethit_eocs` | array | 被击中时 EOC 事件 | — |

#### static_buffs 分层设计（以 Aikido 为例）

| 层级 | 技能要求 | buff 内容 |
|------|----------|-----------|
| Lv1 基础 | 无 | block 100% DEX, +2 block effectiveness, +1 Dodge |
| Lv2 中级 | unarmed 3 | +1 block attempt, +1 dodge attempt |
| Lv3 高级 | unarmed 5 | +1 block attempt, +1 dodge attempt（额外叠加） |

#### buff 触发链模式（6 种常见触发时机）

```
常驻 buff ─── static_buffs（被动常驻）
                  │
    ┌─────────────┼─────────────┬──────────────┐
    ▼             ▼             ▼              ▼
onblock       ondodge       onmove         onpause
(格挡后)      (闪避后)       (移动后)       (等待后)
    │             │             │              │
    └── Aikido ───┘             │              │
    -10% movecost               │              │
                 ┌──────────────┘              │
                 ▼                             │
            Capoeira                      Brawling
        解锁 Spinkick                   +1 命中 ×2
        +1 Dodge

onattack/onmiss ─── Capoeira +5% dmg ×3（无论命中与否都叠）
onkill ─── Barbaran +1 block attempt ×5 回合
oncrit ─── debug 额外电击伤害
```

#### 30+ 流派速览

| 风格 | 武器限定 | 核心机制 | 难度 |
|------|----------|----------|------|
| Aikido | 徒手 | 格挡/闪避 → -movecost → 反投技 | 5 |
| Bōjutsu | QUARTERSTAVES | 移动后 +bash dmg → 解锁横扫/刺击 | 5 |
| Barbaran Montante | 重武器 | 力量穿甲 + 格挡叠 movecost | 8 |
| Boxing | 徒手 | 移动叠闪避 → 闪避后 +25% dmg | 1 |
| Brawling | 全武器 | 等待叠命中 + 多种通用技 | 自动 |
| Capoeira | 徒手 | 移动解锁踢技 + 攻击叠伤 | 4 |
| Crane Kung Fu | 徒手 | DEX 替代 STR 计算伤害 | 10 |
| Dragon Kung Fu | 徒手 | 须按buff的真实属性加成解释，不能推断为INT替代STR | 10 |
| Eskrima | 短刃/棍 | 双手武器切换连击 | 3 |
| Fencing | 细剑类 | 格挡/闪避反击 | 4 |
| Judo | 徒手 | 投技 + 关节技 | 3 |
| Karate | 徒手 | 多种手法（掌/拳/肘/膝） | 3 |
| Krav Maga | 徒手 | 缴械 + 快速切割 + 部位打击 | 5 |
| Muay Thai | 徒手 | 膝盖/肘击重击 | 4 |
| Ninjutsu | 多种 | 缴械 + 快速打击 | 4 |
| Pankration | 徒手 | 古代搏击，综合技 | 6 |
| Silat | 徒手 | 多种卸武 + 快速连打 | 6 |
| Taekwondo | 徒手 | 踢技为主，范围攻击 | 4 |
| Tai Chi | 徒手 | 格挡 + 卸力 + 反击 | 5 |
| Wing Chun | 徒手 | 快速连打 + 近距离 | 5 |
| Zui Quan | 徒手 | INT 闪避 + 闪避叠伤 | 8 |

---


## 选择技法与buff的实际语义

源码依据 src/martialarts.cpp 的 ma_technique::load、ma_requirements::load、martialart::load，以及 src/melee.cpp 的 pick_technique、perform_technique。字段条件表是结构示意，不是可以逐行粘贴的JSON。

- weighting>1通过重复加入候选池加权；负值先按one_in(abs(weighting))决定本次资格。不是按权重排序，也不是NPC专属AI优先级。
- 技法还受暴击/反击/reach、武器、身体向量等条件过滤，可来自所用武器与可用武术，不只当前流派列表。
- 原版已支持static、onmove、onpause、onhit、onattack、ondodge、onblock、ongethit、onmiss、oncrit、onkill的buff/EOC入口。ongethit不是缺失的新钩子；任意onX名字不能新增事件。
- simultaneous_add会先检查同次buff需求再统一添加，不能假设列表前一个buff立刻解锁后一个。
- 数量、流派难度、倍率是具体数据快照，不作为永久API；实际数值以基点JSON和消费逻辑为准。

## anatomy与身体部位

原版data/json/anatomy.json的human_anatomy有12个body_part ID：

```text
eyes, head, mouth, torso,
arm_l, arm_r, hand_l, hand_r,
leg_l, leg_r, foot_l, foot_r
```

eyes是一个ID，并非eye_l/eye_r两个独立部位。default_anatomy只有torso、head，但不能据此推断“只给史莱姆用”。sub_body_part用于更细的覆盖划分，不能与独立HP主部位混同。0.H Monster仍使用全局HP，Creature有身体容器不等于Monster已完成部位伤害结算。详见code_bodypart_hp_system.md。

### 命中部位权重

anatomy::select_body_part（src/anatomy.cpp）依次：

1. 按hit_size上下限筛选缓存部位。
2. 攻击者不能打高处时，移除LIMB_UPPER，LIMB_LOWER权重乘3。
3. 正hit_roll时，权重乘pow(hit_roll, hit_difficulty)。
4. 按最终权重抽样。

hit_difficulty是命中质量的指数修正，不是概率倒数，也不是“越大就越难命中”的独立惩罚。只有无筛选、无高度修正、无hit_roll修正的特例，才简化为hit_size/总hit_size；躯干hit_size=36不等于每次攻击36%命中躯干。

原文“目标权重乘10，再除以hit_difficulty”的瞄准推演不是0.H公式。不能据此确定8～12倍推荐权重，也不能从该推演宣称无需新JSON字段。新项目应重新定义并验证瞄准模型。

## limb_score与受击状态

原版data/json/limb_scores.json有manip、lift、grip、block、breathing、vision、night_vis、reaction、move_speed、balance、footing、swim、crawl等能力。affected_by_wounds/affected_by_encumb控制伤势与累赘；grip在该版受累赘影响，lift不受累赘影响。

部位基础分数、伤势、累赘、效果与具体行为调用共同决定最终能力，不能认为有limb_score声明就让全部Creature/Monster行为自动使用它。body_part的effects_on_hit按伤害类型/阈值/概率/时长配置受击状态；effects.json再定义状态数值和旗标。downed、stunned、winded、blind的最终效果需结合消费逻辑，不能从一张表断言某状态“最严重”或所有对象反应相同。

## hit_range不等于近战命中表

hit_range.json的even_good加载到Creature::dispersion_for_even_chance_of_good_hit，由src/ranged.cpp用于枪械AI/射程评估，不是近战60档难度表。

该版melee::melee_hit_range(accuracy)返回normal_roll(accuracy*5,25.0f)，近战还经闪避等流程。even_good数组不能用于近战命中率或命中部位概率。

## 复用与改造边界

新增武术、技法、buff、EOC和状态可沿用原有解析机制。玩家逐次选技或选部位需要核对输入、目标选择、命中、伤害完整调用链；新增JSON不等于已有交互。新增部位/anatomy也需确认具体角色如何采用，不会自动修改所有NPC与Monster。Medieval后续弹道和部位HP改造不属于0.H原版能力。
