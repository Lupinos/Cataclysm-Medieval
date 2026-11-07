# 营养、健康与代谢系统 (Nutrition & Health)

> Cataclysm-Medieval 的食物消耗、消化、维生素、代谢速率机制

## 核心文件

| 文件 | 作用 |
|------|------|
| `src/stomach.h` / `src/stomach.cpp` | 胃与肠道消化模拟 |
| `src/consumption.cpp` | 食物消耗、营养计算、饮食限制 |
| `src/vitamin.h` / `src/vitamin.cpp` | 维生素定义 |
| `src/addiction.h` / `src/addiction.cpp` | 成瘾系统 |
| `src/morale.h` / `src/morale.cpp` | 士气系统 |
| `src/suffer.cpp` | 被动受苦效果（饥饿、口渴、体温等） |
| `src/character.cpp` (部分) | 角色营养与健康状态 |

---

## 消化系统

### 双室模型

角色有两个消化器官：

| 器官 | `stomach_contents` 参数 | 功能 |
|------|------------------------|------|
| **胃 (Stomach)** | `is_stomach = true` | 快速消化（几小时内），直接吸收 |
| **肠道 (Guts)** | `is_stomach = false` | 慢速消化，受代谢率影响 |

### stomach_contents 结构 (`stomach.h:115-218`)

```cpp
class stomach_contents {
    bool stomach;       // true=胃, false=肠道
    nutrients nutr;     // 所含营养（卡路里+维生素）
    units::volume water;    // 含水量
    units::volume max_volume; // 基础容量
    units::volume contents;   // 当前食物容量
    time_point last_ate;     // 上次进食时间
};
```

核心方法：
- `ingest(food_summary)` — 摄入食物
- `digest(owner, metabolic_rates, five_mins, half_hours)` — 消化处理
  - 每 5 分钟处理一次水分
  - 每 30 分钟处理一次固体和热量
- `capacity(owner)` — 计算实际胃容量（含变异修正）
- `stomach_remaining(owner)` — 剩余空间（满了会吐）

### 消化速率 (stomach_digest_rates)

```cpp
struct stomach_digest_rates {
    units::volume solids;      // 每30分钟消化固体量
    units::volume water;       // 每5分钟吸收水分量
    float percent_kcal;        // 每30分钟热量吸收比例
    int min_calories;          // 每30分钟最小热量吸收
    float percent_vitamin;     // 维生素吸收比例
    int min_vitamin;           // 最小维生素吸收
};
```

---

## 营养计算

### nutrients 结构 (`stomach.h:36-93`)

```cpp
struct nutrients {
    int calories = 0;  // 1/1000 kcal (即实际单位是 cal)
    std::map<vitamin_id, int> vitamins_;
};
```

### 有效卡路里计算

`compute_default_effective_kcal()` (`consumption.cpp:178-219`)：

```
有效卡路里 = 食物基础卡路里 × 修正因子

修正因子包括：
  - 生食 ×0.75（未烹饪的 RAW 食物）
  - 砂囊 (GIZZARD) ×0.6
  - 肉食者吃植物 ×0.5
  - 腐烂食物递减（线性从100%降到0%）
  - 生化消化模块 ×1.5
```

### 食物享受度 (fun_for)

`Character::fun_for()` (`consumption.cpp:439-532`)：

| 修正因素 | 效果 |
|----------|------|
| 感冒/流感 | 正享受 ÷3 |
| 腐烂 | 惩罚 -2 到 -20 + 倍率修正 |
| 单调性 | 2天内重复吃同种食物递减 |
| 冰食 | 正享受 ×2 |
| 融化中的冷冻食品 | 正享受 ×0.5 |
| 美食家 (GOURMAND) | 正享受 ×1.5, 负享受 ÷2 |
| 味觉屏蔽生化模块 | 负享受归零 |

---

## 饮食限制

### 特质相关限制 (`consumption.cpp:740-891`)

| 特质 | 限制 |
|------|------|
| CARNIVORE（肉食者） | 不能吃植物类（蔬菜/水果/谷物），肉食 OK 标志食物例外 |
| HERBIVORE / RUMINANT | 不能吃肉类和蛋类 |
| VEGAN（纯素） | 不能吃任何动物产品（肉/蛋/奶/蜂蜜） |
| VEGETARIAN（素食） | 不能吃肉 |
| LACTOSE（乳糖不耐） | 不能吃奶制品 |
| ANTIFRUIT / ANTIWHEAT | 不能吃水果/小麦 |
| PICKYEATER（挑食） | 只吃喜欢（fun>0）的食物 |
| EATDEAD / SAPROPHAGE | 必须吃腐烂食物 |
| SAPROVORE | 可以吃腐烂食物无惩罚 |
| PROBOSCIS（口器） | 只能喝液体 |
| M_DEPENDENT | 只能吃菌丝相关食物 |

### 食人判定

- 物品有 `CANNIBALISM` 标志 → 需要 CANNIBAL 特质
- 物品有 `STRICT_HUMANITARIANISM` 标志 → 需要相应特质

### 过敏原系统

食物可标记过敏原标签：`ALLERGEN_MEAT`, `ALLERGEN_VEGGY`, `ALLERGEN_FRUIT`, `ALLERGEN_MILK`, `ALLERGEN_EGG`, `ALLERGEN_WHEAT`, `ALLERGEN_NUT`, `ALLERGEN_BREAD` 等。

---

## 维生素系统

### 维生素类型 (vitamin_type)

| 类型 | 说明 |
|------|------|
| `VITAMIN` | 标准维生素（有 RDA 日推荐量） |
| 其他 | 诱变剂、药物等 |

### 维生素管理

- `vitamin_levels`: 当前体内维生素水平（`map<vitamin_id, int>`）
- `daily_vitamins`: 每日摄入追踪
- `vitamin_mod(id, qty)`: 修改维生素量（有上下限）
- `vitamin_rate(id)`: 维生素消耗速率
- 维生素可以 `decays_into()` 转化为其他维生素
- 突变可影响维生素的 `vitamin_rates`（消耗速率）和 `vitamin_absorb_multi`（吸收倍率）

### 每日追踪

`daily_vitamins` 记录每种维生素的每日摄入量，用于 UI 显示和健康判断。

---

## 代谢率

### 基础代谢率

`Character::metabolic_rate_base()` (`consumption.cpp:684-690`)：

```
基础代谢 = PLAYER_HUNGER_RATE × (1 + 突变代谢修正)
```

### 实际代谢率

`Character::metabolic_rate()` (`consumption.cpp:695-715`)：

受饥饿程度影响的动态代谢率：

| 有效饥饿值 | 代谢倍率 |
|------------|----------|
| <300 | 1.0× |
| 300~2000 | 0.8× |
| 2000~5000 | 0.6× |
| >5000 | 0.5× |

**越饥饿 → 代谢越慢**（身体节能模式）。有效饥饿考虑了速度修正。

---

## 成瘾系统

`src/addiction.cpp` 管理角色对各种物质的成瘾状态：

- 每种成瘾有**满足度** (satisfaction) 和**强度** (intensity)
- 不满足成瘾会带来负面效果（如戒断症状）
- 成瘾影响士气（`morale`）

---

## 寄生虫与疾病

食物可能含**寄生虫** (`parasites > 0`)：
- 除非食物有 `NO_PARASITES` 标志或角色有 `PARAIMMUNE` 特质
- 食用含寄生虫食物增加感染风险

相关效果：
- `bloodworms`（血虫）
- `brainworms`（脑虫）
- `tapeworm`（绦虫）
- `foodpoison`（食物中毒）
- `common_cold` / `flu`（感冒/流感）

---

## 进食流程总结

1. 选择食物 → `can_eat()` 检查各种限制
2. 确认意愿 → `will_eat()` 评估后果（腐烂、过敏、太饱等）
3. 执行进食 → `eat()` 计算营养、添加维生素、更新胃内容
4. 消化循环 → 每5分钟处理水分，每30分钟处理热量和维生素
5. 代谢消耗 → `metabolic_rate()` 决定卡路里消耗速率
