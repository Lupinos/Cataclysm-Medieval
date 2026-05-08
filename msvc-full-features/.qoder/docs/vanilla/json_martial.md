# 参考文档：CDDA 战斗系统配置调研

> 来源：`cataclysm-dda/json/` 目录实地分析
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
| **`weighting`** | int | AI 自动选择权重 | -250 ~ 100，正数越大概率越高 |
| **`mult_bonuses`** | array | 倍率加成 | `[{ "stat": "movecost", "scale": 0.5 }]` |
| **`flat_bonuses`** | array | 固定值加成 | `[{ "stat": "movecost", "scale": 100 }]` |
| `tech_effects` | array | 附加效果（on_damage 时触发） | 如 disarmed 效果 |
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
crit_tec: true                           ← 仅暴击时触发
condition: 体型≤攻击者+1, 人形, 非倒地, 不能飞行
down_dur: 2                              ← 击倒 2 回合
attack_vectors: [WEAPON]                 ← 武器柄/杆施展
weighting: 未设置（默认 0）
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
| Dragon Kung Fu | 徒手 | INT 替代？, 连击技 | 10 |
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

### 2.3 `body_part` —— 身体部位

> 12 个主要部位 + 若干子部位。每个部位独立定义命中参数和受击效果。

#### 主要部位表

| 部位 ID | 中文 | hit_size | hit_difficulty | is_vital | 连接 | limb_scores |
|---------|------|----------|----------------|----------|------|-------------|
| `torso` | 躯干 | 36 | 1.0 | ✓ | head | balance 0.7 |
| `head` | 头部 | 4 | 1.2 | ✓ | mouth | — |
| `arm_l` / `arm_r` | 手臂 | 13 | 0.95 | — | hand_l/r | manip, lift, grip, block |
| `hand_l` / `hand_r` | 手 | 1.5 | 1.0 | — | — | manip |
| `leg_l` / `leg_r` | 腿 | 13 | 0.9 | — | foot_l/r | move_speed, balance, footing |
| `foot_l` / `foot_r` | 脚 | 2 | 0.8 | — | — | footing, balance |
| `mouth` | 嘴 | 0.5 | — | — | — | breathing |
| `eye_l` / `eye_r` | 眼 | 0.5 | — | — | — | vision, night_vis |

> **hit_size 解读**：不是命中概率的绝对值，而是加权权重。在默认目标（未指定部位）下，torso 被命中的概率 = 36 / (36+4+13×2+1.5×2+13×2+2×2+0.5×2+0.5×2) ≈ 36/100 = 36%。
>
> **hit_difficulty 解读**：命中难度倍率。torso=1.0 为基准，head=1.2 表示头部更难命中，feet=0.8 表示脚部更容易命中。

#### 子部位结构（torso 为例）

```
torso
├── torso_upper       (上半身)
├── torso_lower       (下腹部)
├── torso_neck        (颈部)
├── torso_hanging_front (前挂饰物)
├── torso_hanging_back  (后挂饰物)
└── torso_waist       (腰部)
```

#### effects_on_hit —— 受击自动效果

按伤害类型和伤害量触发，每个部位不同：

| 部位 | 条件 | 效果 | 概率 | 最大持续时间 |
|------|------|------|------|-------------|
| torso | cut dmg ≥ 3 | bleed | — | 1800 |
| torso | stab dmg ≥ 1 | bleed | — | — |
| torso | bash dmg ≥ 10 | winded（喘不上气） | 10% | 15 回合 |
| torso | bash dmg ≥ 5 | staggered（失衡） | 20% | 15 回合 |
| torso | bash dmg ≥ 15 | downed（倒地） | 5% | — |
| head | bash dmg ≥ 5 | staggered | 20% | 15 回合 |
| head | bash dmg ≥ 15 | stunned（晕眩） | 5% | — |
| head | cut dmg ≥ 3 | bleed | — | — |
| arm | bash dmg ≥ 10 | downed | 5% | — |
| leg | bash dmg ≥ 10 | downed | 10% | — |
| leg | cut dmg ≥ 3 | bleed | — | — |
| eye | cut/stab dmg ≥ 1 | blind（致盲）| 50% | — |

> **关键洞察**：打腿 > 打躯干更容易击倒（10% vs 5%），但没有喘不上气。打头概率晕眩。这套"按部位 × 按伤害类型 × 概率触发"的模型是整个 CDDA 战斗反馈的基础。

---

### 2.4 `anatomy` —— 解剖结构

人体解剖结构定义了 NPC/角色拥有的部位集合（不是所有生物都有手有脚）：

```
human_anatomy:
  torso, head, eyes (×2), mouth, arm (×2), hand (×2), leg (×2), foot (×2)
  = 12 个部位

default_anatomy:
  torso, head
  = 2 个部位（用于史莱姆、流体等简单生物）
```

---

### 2.5 `limb_score` —— 肢体能力评分

> 12 项派生属性，每项有两个 bool 开关：`affected_by_wounds` 和 `affected_by_encumb`。

| 能力 | 说明 | affected_by_wounds | affected_by_encumb |
|------|------|--------------------|--------------------|
| `manip` | 手部操作（开锁、制作等非战斗） | ✓ | ✓ |
| `lift` | 举重/搬运 | ✓ | ✗ |
| `grip` | 抓握（武器控制） | ✓ | ✗ |
| `block` | 格挡能力 | ✓ | ✓ |
| `breathing` | 呼吸 | ✓ | ✓ |
| `vision` | 白天视觉 | ✓ | ✓ |
| `night_vis` | 夜间视觉 | ✓ | ✓ |
| `reaction` | 反应速度 | ✓ | ✓ |
| `move_speed` | 移动速度 | ✓ | ✓ |
| `balance` | 平衡 | ✓ | ✓ |
| `footing` | 立足稳定性 | ✓ | ✓ |
| `swim` | 游泳 | ✓ | ✓ |
| `crawl` | 爬行 | ✓ | ✓ |

> **与战斗的关联**：状态效果通过 `limb_score_mods` 降低这些能力值。例如 `stunned` 效果将 balance 降至 0.2、reaction 降至 0.0。

---

### 2.6 `hit_range` —— 命中精度表

60 个数值的查表数组，决定命中概率曲线：

```
位置   值    位置   值    位置   值    位置   值
  1   1724    16    102   31    63    46    36
  2    860    17    101   32    61    47    35
  3    573    18     95   33    59    48    35
  4    429    19     90   34    57    49    34
  5    343    20     85   35    55    50    33
  6    286    21     81   36    53    51    33
  7    245    22     78   37    52    52    32
  8    214    23     74   38    50    53    31
  9    191    24     71   39    49    54    31
 10    171    25     68   40    47    55    30
 11    156    26     66   41    46    56    30
 12    141    27     63   42    45    57    29
 13    127    28     61   43    44    58    29
 14    122    29     59   44    42    59    28
 15    114    30     57   45    41    60    28
```

> **解读**：这个表是 `even_good` 分布——数值越高命中越容易。第 1 档（最易）1724，第 60 档（最难）28，呈指数衰减。具体公式需要看 C++ 源码，但从数值分布可推断：高精度区域宽容度大（前 10 档跨度 1724→171），低精度区域梯度平缓（后 30 档从 63→28 均匀递减）。

---

### 2.7 `effect_type` —— 战斗状态效果

| 效果 ID | 中文 | limb_score 惩罚 | 其他效果 | 属性/速度惩罚 |
|----------|------|-----------------|----------|--------------|
| `staggered` | 失衡 | — | 打断 grab | speed -20% |
| `downed` | 倒地 | balance 0.1, reaction 0.5, block 0.5 | 禁用飞行 | — |
| `winded` | 喘不上气 | reaction 0.5, lift 0.75, block 0.75, manip 0.5, swim 0.3 | — | speed -30%, str -3, dex -1 |
| `stunned` | 晕眩 | balance 0.2, reaction 0.0 | 禁用飞行/法术/灵能 | 移动随机化 |
| `dazed` | 恍惚 | balance 0.5, reaction 0.35, vision 0.75 | — | speed 每级 -3% |
| `disarmed` | 缴械 | — | 禁用武器攻击 | — |
| `blind` | 致盲 | vision 0.5, night_vis 0.1 | — | — |

> **winded 是最严重的战斗 debuff**：同时降低速度、力量、敏捷和 5 项肢体能力，持续时间可达 30 秒（回合）。

---

## 三、战斗流程（JSON 视角还原）

```
玩家移动（消耗 move points）
        │
        ▼
  进入相邻格 → 自动触发近战碰撞判定
        │
        ├──① 命中判定（hit_range 查表 + 技能/属性修正）
        │
        ├──② 部位判定 ──→ 默认：按 body_part.hit_size 加权随机
        │                  └─ 受 hit_difficulty 修正
        │
        ├──③ 技术选择 ──→ 当前 martial_art.techniques 列表
        │                  ├─ 过滤：condition 不满足的跳过
        │                  ├─ 排序：weighting 越大概率越高
        │                  ├─ 随机：在可用池中加权随机
        │                  └─ 某些技术 crit_tec=true 仅暴击时可用
        │
        ├──④ 伤害计算 ──→ 武器基础伤害 × 技术 mult_bonuses
        │                  ± 技术 flat_bonuses
        │                  ± martial_art buff 修正
        │
        ├──⑤ 效果触发 ──→ body_part.effects_on_hit（按伤害类型+阈值）
        │                  + 技术 tech_effects（缴械等）
        │
        ├──⑥ buff 触发 ──→ 命中→ onattack_buffs / onhit_buffs
        │                   格挡→ onblock_buffs
        │                   闪避→ ondodge_buffs
        │                   击杀→ onkill_buffs
        │                   落空→ onmiss_buffs
        │
        └──⑦ movecost 消耗 ──→ 基础 movecost × 技术 mult_bonuses
                                 ± 技术 flat_bonuses
                                 ± active buff 修正
       （玩家剩余 move points 决定能否继续行动）
```

> **关键发现**：步骤 ② 和 ③ 是**完全自动的**，没有玩家选择环节。这就是"移动撞上去"——玩家只控制"移动到哪个格子"，系统自动判定"打中哪里、用什么招"。

---

## 四、自动选择 vs 手动选择：JSON 能做什么

### 4.1 纯 JSON 可实现的功能（不需要源码修改）

| 功能 | 实现方式 | 示例 |
|------|----------|------|
| 新增武术流派 | 新建 `martial_art` + 关联 `technique` | 完全可行，可定义 buff/技术列表/武器限制 |
| 新增技术/招式 | 新建 `technique` | 定义伤害/movecost/条件/效果/攻击肢体 |
| 新增身体部位 | 新建 `body_part` | 为特定 NPC 设计特化 anatomy |
| 新增部位受击效果 | 在 `body_part.effects_on_hit` 中追加 | 如"打头 10% 概率混乱" |
| 新增战斗状态 | 新建 `effect_type` + 在技术/部位中引用 | 可定义 limb_score 惩罚和属性惩罚 |
| NPC 装备特定流派 | 在 npc_class 中设定 martial art | NPC 自动使用对应技术池 |
| 通过环境/状态锁定技术 | condition 字段 | "只有目标倒地时才可用" |
| buff 触发链 | 各种 onX_buffs | 格挡后 → 移速加快 → 解锁反技 |
| 调整技术权重 | weighting 字段 | 控制 NPC AI 的选择倾向 |
| 通过 EOC 触发战斗效果 | `eocs` 字段 | 击杀触发区域效果、对话等 |

### 4.2 需要 C++ 源码改造的功能

| 功能 | 原因 |
|------|------|
| **玩家手动选择目标部位** | 当前攻击流程无交互——碰撞时自动加权随机 |
| **玩家手动选择技术** | 当前自动按 weighting 选择，无招式菜单 |
| NPC AI 战术决策（选择部位、博弈） | 选择逻辑在 C++ 中，JSON 只提供权重 |
| 修改命中判定公式 | `hit_range` 表用法在 C++ 中 |
| 新增 buff 触发时机类型 | 当前只有 onattack/onblock/ondodge/onmove/onmiss/onkill/oncrit/onpause/onhit |
| UI 交互（招式选择界面、部位瞄准高亮） | 纯 UI 层 |

---

## 五、战斗系统数据规模一览

| 数据类型 | 文件 | 数量 | 设计复杂度 |
|----------|------|------|------------|
| `technique` | techniques.json | 167 (140 攻击技) | ★★★★ 高——condition/movecost/buff 三维平衡 |
| `martial_art` | martialarts.json + _fictional | 30+ | ★★★★ 高——buff 链 + 技术池 + 武器限定 |
| `body_part` | body_parts.json | 12 主要 + 子部位 | ★★ 中——hit_size + effects_on_hit |
| `effect_type` | effects.json (战斗部分) | ~10 战斗核心 | ★★ 中——limb_score_mods + stat_mods |
| `limb_score` | limb_scores.json | 12 | ★ 低——单一派生属性 |
| `anatomy` | anatomy.json | 2 | ★ 低——部位集合 |
| `hit_range` | hit_range.json | 1 | ★ 低——查表 |

---

## 六、设计参考：从已有数据中提取的模式

### 6.1 技术分类模式

```
控制型（↓ target, ↑ 战术优势）
  SWEEP:     down 2 回合, 仅暴击, 体型条件
  PRECISE:   stun 2 回合, 仅暴击, 人形限定
  BRUTAL:    stun 1 + knockback 1, 仅暴击, 排除非人形

爆发型（↓ move speed, ↑ damage）
  SWEETSPOT:    damage 2.5x, movecost 1.1x, stun+knockback
  各类蓄力技:    damage 1.5~2.0x, movecost 1.2~1.5x

快速型（↓ movecost, ↓ damage）
  Jab 类:       movecost 0.5x
  Rapid 类:     movecost 0.5x, 连击

功能型（不直接伤害，改变战斗状态）
  DISARM:       卸除武器
  GRAB_BREAK:   挣脱抓取
  FEINT:        虚招，减少落空惩罚

范围型（AOE）
  SPIN:         攻击相邻所有格
  WIDE:         攻击前方弧线
  IMPALE:       穿刺并命中后排
```

### 6.2 流派 buff 模式

```
防御反击型（Aikido 模式）
  常驻: +block +dodge
  格挡后: -10% movecost → 解锁投技
  闪避后: -10% movecost → 解锁投技
  核心循环: 防 → 省 → 反

移动累积型（Capoeira 模式）
  常驻: +dodge
  移动后: +dodge → 解锁踢技
  攻击后: +5% dmg（无论命中与否，叠 3 层）
  核心循环: 动 → 攒 → 踢

属性缩放型（Crane 模式 / Barbaran 模式）
  Crane:  bash dmg 按 DEX 计算，替代 STR
  Barbaran: arpen 按 STR×0.75 计算
  核心思路: 让非主流属性成为主战属性

待命蓄力型（Brawling 模式）
  等待后: +1 命中，叠 2 层
  高级后: +1 block attempt
  核心循环: 等 → 精准 → 致命

击杀滚雪球型（Barbaran 模式）
  击杀后: +1 block attempt，持续 5 回合
  核心循环: 杀 → 强 → 继续杀
```

---

## 七、瞄准系统的理论模型

> **前提**：以下基于 `hit_size` 是部位加权采样的权重值这一假设。具体实现需查看 C++ 源码确认。本模型仅从 JSON 数据出发，推导"手动选择目标部位"的数值框架。

### 7.1 原理

CDDA 默认攻击的命中部位由 `body_part.hit_size` 加权随机决定：

```
部位命中概率 = 该部位 hit_size / Σ(所有部位 hit_size)
```

如果玩家能**指定目标部位**，本质上是将均匀加权分布变为**偏置加权分布**——对目标部位 hit_size 施加 multiplier，其他部位保持原值：

```
瞄准后部位权重 = hit_size × multiplier (目标部位)
                  hit_size              (其他部位)

瞄准后命中概率 = 目标权重 / Σ(所有部位权重)
最终命中概率   = 瞄准后命中概率 × (1 / 目标部位 hit_difficulty)
```

### 7.2 数值推演

以人类解剖结构 12 部位为基础（Σ hit_size = 100），假设 multiplier = **10x**：

#### 默认分布（不瞄准）

| 部位 | hit_size | 命中比例 |
|------|----------|----------|
| torso | 36 | 36.0% |
| arm_l/r | 13×2 | 26.0% |
| leg_l/r | 13×2 | 26.0% |
| head | 4 | 4.0% |
| foot_l/r | 2×2 | 4.0% |
| hand_l/r | 1.5×2 | 3.0% |
| eye_l/r | 0.5×2 | 1.0% |
| mouth | 0.5 | 0.5% |
| **合计** | **100** | **100%** |

#### 瞄准各部位的收益/风险对比（multiplier = 10x）

| 目标 | 权重偏置 | 瞄准后占比 | hit_difficulty | 最终命中估算 | 命中动机 |
|------|----------|-----------|----------------|-------------|----------|
| torso | 36→360 | 360/456=**79%** | 1.0 | ~79% | 最稳，触发 winded/downed |
| leg | 13→130 | 130/226=**58%** | 0.9 | ~64% | downed 概率最高 (10%) |
| arm | 13→130 | 130/226=**58%** | 0.95 | ~61% | 削弱攻击手 |
| head | 4→40 | 40/136=**29%** | 1.2 | ~24% | stunned 概率 |
| foot | 2→20 | 20/116=**17%** | 0.8 | ~22% | 减速/失衡 |
| hand | 1.5→15 | 15/111=**14%** | 1.0 | ~14% | 缴械相关 |
| eye | 0.5→5 | 5/101=**5%** | (>1.0 推测) | <5% | blind 效果 50% |
| mouth | 0.5→5 | 5/101=**5%** | — | ~5% | breathing 相关 |

> **核心博弈**：部位越小 → 权重偏置效果越弱 → 命中骤降 → 但效果越强（晕眩/致盲/窒息）。这正好构成了"风险 vs 回报"的战术深度。

### 7.3 与现有系统的天然契合

CDDA 已有数据完全支撑这个模型：

```
① hit_size          → 部位基准权重（已有）
② hit_difficulty    → 瞄准精度惩罚（已有）
③ effects_on_hit    → 命中后的状态效果（已有，按伤害类型+阈值）
④ limb_score_mods   → 状态效果对身体能力的连锁削弱（已有）
```

不需要新增任何 JSON 字段。multiplier 的行为是**纯流程层的参数**（在命中判定中插入一次权重变换），源码介入后 multiplier 本身可以硬编码在流程中，也可以做成 JSON 可配置的全局参数。

### 7.4 multiplier 的设计考量

multiplier 越大 → 瞄准越精准但也越"游戏化"。需要平衡：

| multiplier | 头部命中占比 | 头部最终命中 | 评价 |
|------------|-------------|-------------|------|
| 3x | 12/108=11% | ~9% | 太弱，瞄不瞄差别不大 |
| 5x | 20/116=17% | ~14% | 保守，有体感但不高 |
| **10x** | 40/136=**29%** | **~24%** | **推荐基准：明显提升但非必中** |
| 20x | 80/176=45% | ~38% | 过强，几乎一半命中 |
| ∞ (必中) | 100% | 100%/1.2=83% | 破坏平衡 |

> **推荐**：multiplier 设为 8~12 区间，与目标的 hit_difficulty 形成制衡——瞄躯干几乎必中（79%），瞄头部需要赌（24%）。

### 7.5 实现位置（源码层面，待验证）