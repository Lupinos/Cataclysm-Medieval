# 魔法系统 (Magic System)

> 原版基准：CDDA 0.H 维护分支提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 项目初始化前）。下列路径、字段与流程以该提交为准，不代表后续 Medieval 改造。

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/magic.h` / `src/magic.cpp` | 法术类型定义、施法逻辑、法力管理 |
| `src/magic_enchantment.h` / `src/magic_enchantment.cpp` | 附魔数据与效果 |
| `src/magic_spell_effect.cpp` | 法术效果的具体实现 |
| `src/magic_teleporter_list.cpp` | 传送点列表 |
| `src/magic_ter_fur_transform.cpp` | 地形/家具转化魔法 |

---

## 法术定义 (spell_type)

每个法术是一个 JSON 定义的数据，核心属性：

### 基础属性

| 属性 | 说明 |
|------|------|
| `id` | 法术 ID |
| `name` / `description` | 名称与描述 |
| `message` | 施放时的提示信息 |
| `skill` | 关联技能（通常为 spellcraft） |
| `spell_class` | 法术学派（trait_id，限制谁可以学） |
| `difficulty` | 施法难度 |
| `max_level` | 最大等级 |

### 伤害与效果

| 属性 | 说明 |
|------|------|
| `min_damage` / `damage_increment` / `max_damage` | 伤害（随等级递增） |
| `min_pierce` / `pierce_increment` / `max_pierce` | 护甲穿透参数，不等于新增一种穿刺伤害 |
| `min_dot` / `dot_increment` / `max_dot` | 持续伤害（每回合） |
| `dmg_type` | 伤害类型（如 bash, heat, pure 等） |
| `min_accuracy` / `accuracy_increment` / `max_accuracy` | 精度（对抗闪避/格挡/法术抵抗） |

### 范围与持续时间

| 属性 | 说明 |
|------|------|
| `min_range` / `range_increment` / `max_range` | 施法距离 |
| `min_aoe` / `aoe_increment` / `max_aoe` | 范围（半径，0=单体） |
| `min_duration` / `duration_increment` / `max_duration` | 持续时间（moves） |

### 能量消耗

| 属性 | 说明 |
|------|------|
| `base_energy_cost` / `energy_increment` / `final_energy_cost` | 能量消耗 |
| `energy_source` | 能量来源（见下方） |
| `base_casting_time` / `casting_time_increment` | 施法时间（moves） |

---

## 能量来源 (magic_energy_type)

| 类型 | 说明 |
|------|------|
| `mana` | 法力（最常用，有上限和回复速率） |
| `stamina` | 体力 |
| `hp` | 生命值 |
| `bionic` | 生化能量 |
| `none` | 无消耗 |

---

## 法术形状 (spell_shape)

| 形状 | 说明 |
|------|------|
| `blast` | 圆形爆发（以目标为中心） |
| `line` | 直线（从施法者到目标，有宽度） |
| `cone` | 锥形 |

---

## 法术标志 (spell_flag)

| 标志 | 说明 |
|------|------|
| `PERMANENT` | 召唤物永久存在 |
| `PERMANENT_ALL_LEVELS` | 任意等级召唤物都永久 |
| `PERCENTAGE_DAMAGE` | attack 效果按目标根部位当前 HP 的百分比设置伤害，仍经过该效果的减伤/伤害路径 |
| `IGNORE_WALLS` | 范围效果穿透墙壁 |
| `NO_PROJECTILE` | 可穿墙选定原始目标区域 |
| `SWAP_POS` | 投射物交换施法者与目标位置 |
| `HOSTILE_SUMMON` | 召唤物始终敌对 |
| `HOSTILE_50` | 召唤物 50% 概率友善 |
| `SILENT` | 目标处无声 |
| `LOUD` | 目标处额外噪音 |
| `VERBAL` | 需要念咒（嘴部累赘影响失败率） |
| `SOMATIC` | 需要手势（手臂累赘影响施法时间和失败率） |
| `NO_HANDS` | 手部不影响能量消耗 |
| `NO_LEGS` | 腿部不影响施法时间 |
| `CONCENTRATE` | 专注影响失败率 |
| `RANDOM_AOE` / `RANDOM_DAMAGE` / `RANDOM_DURATION` | 随机范围/伤害/持续时间 |
| `RANDOM_TARGET` / `RANDOM_CRITTER` | 随机选择有效目标 |
| `WONDER` | 随机施放额外法术中的 N 个 |
| `UNSAFE_TELEPORT` | 传送有死亡风险 |
| `NON_MAGICAL` | 无视法术抗性 |
| `PSIONIC` | 灵能（非传统魔法） |
| `NO_FAIL` | 不会失败 |
| `MUST_HAVE_CLASS_TO_LEARN` | 必须已有所属学派 |

---

## 法术效果一览 (`spell_effect`)

效果映射见 src/magic.h 的 spell_effect::effect_map（由 magic.cpp 查找）；下表为效果参考，不以数量为机制结论：

| 效果名 | 说明 |
|--------|------|
| `attack` | 标准攻击法术 |
| `pain_split` | 痛苦分担 |
| `targeted_polymorph` | 目标变形 |
| `short_range_teleport` | 短距离传送 |
| `spawn_item` | 生成物品 |
| `recover_energy` | 恢复能量 |
| `summon` | 召唤怪物 |
| `summon_vehicle` | 召唤载具 |
| `recharge_vehicle` | 给载具充能 |
| `translocate` | 跨空间传送 |
| `area_pull` | 区域拉拽 |
| `area_push` | 区域推开 |
| `directed_push` | 定向推力 |
| `timed_event` | 定时事件 |
| `ter_transform` | 地形转化 |
| `noise` | 制造噪音 |
| `vomit` | 催吐 |
| `pull_target` | 拉向施法者 |
| `explosion` | 爆炸 |
| `flashbang` | 闪光弹 |
| `mod_moves` | 修改行动点 |
| `map` | 揭示地图 |
| `morale` | 影响士气 |
| `charm_monster` | 魅惑怪物 |
| `mutate` | 变异 |
| `bash` | 冲撞 |
| `dash` | 冲刺 |
| `banishment` | 放逐 |
| `revive` | 复活为丧尸 |
| `revive_dormant` | 唤醒休眠怪物 |
| `upgrade` | 升级怪物 |
| `guilt` | 施加罪恶感 |
| `remove_effect` | 移除效果 |
| `emit` | 释放场 |
| `fungalize` | 真菌化 |
| `remove_field` | 移除场 |
| `effect_on_condition` | 触发效果链 |
| `slime_split` | 史莱姆分裂 |

---

## 法力系统 (known_magic)

`known_magic` 类 (`magic.h:646-731`)：

- **spellbook**: 法术书（`map<spell_id, spell>`）
- **mana_base**: 基础法力上限
- **mana**: 当前法力

### 法术经验与等级

- 法术有自己的 **经验值** (`experience`)
- `exp_for_level(level)` — 每级所需经验
- 成功施法获得 `casting_exp()`
- 经验积累 → 升级 → 法术效果增强

### 学习法术

- `learn_spell()` — 学习法术
- `time_to_learn_spell()` — 记忆法术所需回合数
- `can_learn_spell()` — 是否可学

---

## 触发式法术 (fake_spell)

`fake_spell` 结构 (`magic.h:142-189`)：

这是一种**不直接施放的法术配置**，用于：
- **附魔触发**：护甲/武器的命中时施法
- **变异触发**：获得变异时施法
- **生化模块触发**：激活/安装时施法

核心属性：
- `id`: 法术 ID
- JSON min_level（C++ level）：施法等级下限
- JSON hit_self（C++ self）：是否对自身施放
- JSON once_in（C++ trigger_once_in）：供相应触发入口使用的 1/N 概率
- `max_level`: 封顶等级

---

## 施法流程

准备检查与施法活动分布在 src/magic.cpp、src/activity_handlers.cpp。activity_handlers::spellcasting_finish 的主流程如下：

1. 取得已知/临时法术，选择或读取目标，检查目标。
2. 按活动参数及 spell_fail 判定成功。失败可获正常经验的五分之一，发送失败事件，不是只有成功才得经验。
3. 成功处理念咒音效和消息；先 use_components，再计算能量 cost。
4. cast_all_effects 执行主效果与伴随效果。
5. 活动参数要求支付时，按 mana/stamina/bionic/hp 扣能量，并非一律先扣能量再施放。
6. 处理经验/升级、物品 charge，发送成功事件。

min_* + level * increment 还经过边界、取整、随机旗标与具体效果解释。blast 的 aoe、line 的宽度、cone 的范围语义不同，不能把所有 aoe 都称圆形半径。fake_spell 是否由变异、附魔或模块触发取决于持有它的调用者；once_in 也只在消费该字段的触发路径生效。
