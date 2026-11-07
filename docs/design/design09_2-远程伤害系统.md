# 远程伤害系统：公式、参数与平衡

> 完整梳理远程伤害链路，提出 Medieval Mod 的弓弩平衡方案。
> 配套模拟工具：`tools/ranged_damage_gui.py`

---

## 一、远程伤害完整公式

### 1.1 阶段一：基础伤害（`make_gun_projectile()`）

```
proj.impact = gun.gun_damage()          ← 武器 JSON "ranged_damage"
            + ammo.damage              ← 弹药 JSON "damage"
            + 附魔 RANGED_DAMAGE 加成

proj.critical_multiplier = ammo.critical_multiplier   ← 弹药 JSON
```

弓/弩的 `ranged_damage` 提供基础 amount；箭/弩箭的 `damage` 提供叠加 amount（当前箭 amount=0，仅靠弓）。

### 1.2 阶段二：命中判定（dispersion → missed_by → goodhit）

**dispersion 构成（三种噪声源）：**

```
dispersion_total = Σ U(0, linear_source) + Σ N(normal_source)

其中：
  linear_sources:
    1. DEX 手抖      U(0, max((20-DEX)*0.5, 0))
    2. 技能惩罚       U(0, dispersion_from_skill(avgSkill, wc))
    3. 后坐力         U(0, recoil_total())

  normal_sources:
    1. 武器精度       N(json_dispersion / GUN_DISPERSION_DIVIDER)
       rng_normal(X) = 截断正态 N(μ=X/2, σ=X/4), 范围[0, X]
```

**dispersion_from_skill 公式：**

```cpp
wc = skill_constant / GUN_DISPERSION_DIVIDER  // archery=450, guns/rifle=300

if skill >= 10:   return 0
elif skill >= 5:  return 10*(10-skill) + wc*(10-skill)*0.25
else:             return 10*(10-skill) + wc*(11.25 - 2*skill)
```

**missed_by 与 goodhit：**

```
missed_by_tiles = tan(dispersion_rad / 2) × range × 2
missed_by = min(1.0, missed_by_tiles / target_size)
goodhit   = min(missed_by + dodge_factor, 2.0)
```

### 1.3 阶段三：damage_mult（命中品质分级）

```
std_hit_mult = sqrt(2.0 × crit_multiplier)
Δ = crit_multiplier − std_hit_mult

HEADSHOT  (goodhit < 0.1):  rng(0.95,1.05) × [std_hit + Δ×crit_mod]
CRITICAL  (goodhit < 0.2):  rng(0.75,1.00) × [std_hit + Δ×crit_mod]
GOOD HIT  (goodhit < 0.5):  rng(0.50,0.75) ×  std_hit
STANDARD  (goodhit < 0.8):  rng(0.50,1.00)
GRAZING   (goodhit < 1.0):  rng(0.00,0.25)
MISS      (goodhit ≥ 1.0):  无伤害
```

### 1.4 阶段四：护甲与最终伤害

```
eff_armor  = max(0, target_armor − arrow_armor_penetration)
post_armor = max(0, impact × damage_mult − eff_armor)
final_dmg  = post_armor × arrow_constant_damage_multiplier
```

---

## 二、关键参数速查

### 武器（JSON）

| 参数 | 字段 | 长弓原值 | 轻弩原值 | 作用 |
|------|------|---------|---------|------|
| 基础伤害 | `ranged_damage.amount` | 6 | 4 | impact 的主体 |
| 精度 | `dispersion` | 1000 | 375 | 武器噪声源（÷15后进入 N()） |

### 弹药（JSON）

| 参数 | 字段 | bodkin | broadhead | 作用 |
|------|------|--------|-----------|------|
| 附加伤害 | `damage.amount` | 0 | 0 | 叠加到 impact |
| 穿甲 | `damage.armor_penetration` | 3 | 1 | 降低有效护甲 |
| 伤害倍率 | `damage.constant_damage_multiplier` | 1.0 | **1.5** | 护甲后乘数 |
| 暴击倍率 | `critical_multiplier` | **10** | **10** | 决定 dmg_mult 曲线 |

> 注意：子弹的 `critical_multiplier` 默认 2.0。箭/弩箭的 10.0 是极高值，以低基础伤害换取爆头致命性。

### 系统常量（C++）

| 常量 | 位置 | 默认值 | 说明 |
|------|------|--------|------|
| `GUN_DISPERSION_DIVIDER` | 全局选项 | 15 | 所有武器 dispersion ÷ 此值 |
| archery `skill_constant` | `ranged.cpp` | 450 | 弓技能惩罚的强度参数 |
| gun `skill_constant` | `ranged.cpp` | 300 | 弩/枪技能惩罚的强度参数 |

### 目标参数

| 参数 | 典型值 | 说明 |
|------|--------|------|
| 平民/僵尸 HP | 75 | 单发秒杀阈值 |
| 无甲 stab armor | 0 | 裸体目标 |
| 轻甲 stab armor | 4-8 | 皮/布甲 |
| 中甲 stab armor | 10-14 | 锁子甲 |
| 重甲 stab armor | 16-22 | 板甲 |
| crit_mod（怪物） | 1.0 | 怪物始终满暴击因子 |
| crit_mod（NPC） | 1.0 − 护甲覆盖率 | 护甲压暴击倍率 |

---

## 三、模拟工具

### 3.1 安装

```bash
pip install matplotlib  # GUI 模式需要
# CLI 模式零依赖
```

### 3.2 命令行接口

```bash
# 单组参数
python3 tools/ranged_damage_gui.py --cli \
  --bow-dmg 6 --arrow-cdm 1.5 --json-dispersion 150 \
  --skill 10 --range 8

# 对比不同技能等级
python3 tools/ranged_damage_gui.py --compare-skills

# 对比不同距离
python3 tools/ranged_damage_gui.py --compare-ranges --skill 10

# 对比不同武器
python3 tools/ranged_damage_gui.py --compare-weapons --skill 10

# 参数扫描（最重要）
python3 tools/ranged_damage_gui.py --sweep json_dispersion \
  --sweep-values "50,100,150,200,300,500,1000" --skill 10 --range 16

python3 tools/ranged_damage_gui.py --sweep skill \
  --sweep-values "0,1,2,3,4,5,6,7,8,9,10" --range 8

# 无参数 = GUI 模式
python3 tools/ranged_damage_gui.py
```

### 3.3 可调参数（共 16 个）

| 类别 | 参数 | CLI flag | 默认 |
|------|------|----------|------|
| 武器 | 弓基础伤害 | `--bow-dmg` | 6 |
| 弹药 | 箭 damage.amount | `--arrow-amount` | 0 |
| 弹药 | 箭 cdm | `--arrow-cdm` | 1.5 |
| 弹药 | 箭 arpen | `--arrow-arpen` | 3 |
| 弹药 | 箭 crit_mult | `--arrow-crit-mult` | 10 |
| 系统 | JSON dispersion | `--json-dispersion` | 150 |
| 系统 | skill_constant | `--skill-constant` | 60 |
| 系统 | dispersion_divider | `--dispersion-divider` | 15 |
| 角色 | 技能等级 | `--skill` | 10 |
| 角色 | 敏捷 | `--dex` | 10 |
| 场景 | 距离 | `--range` | 8 |
| 场景 | 目标护甲 | `--target-armor` | 0 |
| 场景 | 目标 HP | `--target-hp` | 75 |
| 场景 | 目标体型 | `--target-size` | 0.5 |
| 场景 | 闪避 | `--dodge` | 0 |
| 场景 | crit_mod | `--crit-mod` | 1.0 |

---

## 四、核心发现

### 4.1 原版问题

1. **武器噪声淹没了技能差距。** 长弓 N(67) → mean 33.5 arcmin。skill=10 时，33.5 的武器噪声占 92% 且技能不能消除。skill=0 和 skill=10 在 8 格外的 HEADSHOT 率仅差 4 个百分点。

2. **`avgSkill = (gun_skill + weapon_skill) / 2` 惩罚纯弓手。** 无 marksmanship 训练的弓手 effective skill 被腰斩。

3. **伤害二进制化。** `crit_mult=10` 导致要么 HEADSHOT×10 秒杀，要么 GOOD HIT×2.8 刮痧。缺乏中间区间。

4. **低级射手过早强力。** skill=0 的门外汉在 8 米外用长弓+broadhead，均伤 31/箭，2.4 箭杀 75HP 僵尸。

### 4.2 建议调整

| 调整项 | 原值 | 建议值 | 效果 |
|--------|------|--------|------|
| 长弓 `dispersion` | 1000 | **150** | 满级 8 米 HEADSHOT: 20% → ~100% |
| 短弓 `dispersion` | 1000 | **200** | 满级 8 米 HEADSHOT: 20% → ~90% |
| 木弩 `dispersion` | 375 | **80** | 满级 8 米 HEADSHOT: 45% → ~100% |
| 复合弩 `dispersion` | 350 | **60** | 满级 16 米 HEADSHOT: 16% → ~95% |
| archery `skill_constant` | 450 | **1500** | 拉大技能梯度，skill=0 均伤 31→18，MISS 0%→13% |

> 注：`skill_constant` 从 450→1500 的效果等价于 `DISPERSION_DIVIDER` 从 15→50，
> 但仅影响 archery 而不影响全武器。

### 4.3 调整后的效果

| 射手 | 4 米 HEADSHOT | 8 米 HEADSHOT | 16 米 HEADSHOT | 8 米均伤 |
|------|-------------|-------------|---------------|---------|
| 入门（skill=0） | 6% | 5% | 2% | 18 |
| 入门（skill=3） | 8% | 6% | 2% | 32 |
| 熟练（skill=6） | 16% | 12% | 3% | 56 |
| 精英（skill=10） | ~100% | ~100% | 87% | 90 |

---

## 五、dispersion 直觉理解

`dispersion = 1000` 的含义：

```
1000 / 15 = 67 arcmin → rng_normal(67)
→ 均值 33.5 arcmin ≈ 0.56° ≈ 8 米外 7.8cm 散布半径
```

**arcmin（角分）= 1/60 度。** 33.5 arcmin 的半度在 8 米外展开为 15.6cm 散布直径（略小于人头宽度 18cm），16 米外直接翻倍到 31cm——超出头部范围。

三种噪声在 arcmin 空间的贡献（长弓，原版值）：

| skill | 武器 N(67) | DEX U(0,5) | 技能 U | 总计 | 8m 散布 |
|-------|-----------|------------|--------|------|---------|
| 10 | 33.5 | 2.5 | 0 | 36.5 | 17cm |
| 5 | 33.5 | 2.5 | 44 | 79.5 | 37cm |
| 0 | 33.5 | 2.5 | 219 | 254.5 | 119cm |

**武器 N(33.5) 是满级也无法消除的基底噪声——弓的物理精度上限。**

---

## 六、弓 vs 弩设计定位

| | 弓 | 弩 |
|---|---|---|
| 基础伤害 | 6 | 4 |
| 武器噪声 N | N(67) → 均值 33.5 | N(25) → 均值 12.5 |
| 爆头伤害 (broadhead) | 90 | 60 |
| 换弹时间 | 50 | 1200 |
| 玩法 | 高伤害，低命中，赌暴击 | 低伤害，高命中，每发必疼 |

弩的 `dispersion=375`（vs 弓的 1000）是"一发不准就等死"的补偿——24 倍换弹时间换来 3 倍精度。两者在中世纪 mod 中是互补而非竞争关系。
