# 任务：射击部位瞄准系统

## 目标

玩家在射击/投掷瞄准界面（`target_ui`）中，可以主动选择攻击目标的特定部位。选中后：

1. **命中率变化**：瞄小部位 → `target_size` 缩小 → 自然更难命中（无需额外惩罚公式）
2. **命中后落点**：弹丸沿 `targeting_graph` 从瞄准部位出发扩散，更大概率落在瞄准部位或其近邻

## 依赖

- `monster_bodypart_fix.md`（部位 HP 修复必须先完成，否则 Monster 目标没有可瞄的部位）
- [code_bodypart_hp_system.md](../vanilla/code_bodypart_hp_system.md)

---

## 核心设计决策

### 为什么不用 `missed_by` 惩罚

早期方案考虑过 `missed_by += 10.0 / hit_size`。但这样有两层逻辑（先算 miss/miss，再算部位），而且 `10.0` 是魔法数字。

**改用 `target_size` 缩放：** `target_size` 本身就是 `missed_by` 计算的分母。把 `target_size` 缩小，命中率自然下降——**不需要额外代码**。

### 为什么不用 `hit_difficulty`

远程弹道代码 (`select_body_part_projectile_attack`) **根本不读 `hit_difficulty`**。这个字段只在近战 `select_body_part` 里出现。远程用的是 `targeting_graph`，依赖 `hit_size` 和 `connected_to`。

### 等效面积算法（BFS 距离加权）

对每一个瞄准部位，跑 BFS 计算它到 anatomy 中所有其他部位的最短距离。用 `hit_size / distance` 加权求和，得到这个部位的「等效面积」。

```cpp
double effective_size( const bodypart_id &root ) {
    map<bodypart_id, int> dist;
    queue<bodypart_id> q;
    q.push( root );
    dist[root] = 0;
    while( !q.empty() ) {
        auto cur = q.front(); q.pop();
        for( auto &nb : graph[cur] ) {
            if( !dist.count( nb ) ) {
                dist[nb] = dist[cur] + 1;
                q.push( nb );
            }
        }
    }
    double total = 0;
    for( auto &[bp, d] : dist ) {
        total += bp->hit_size / ( d + 1.0 );   // +1 避免自除零
    }
    return total;
}
```

然后 `target_size *= effective_size(aimed) / effective_size(biggest_bp)`。

**为什么合理：** 瞄 torso 时，它的邻域包含了四肢和头——等效面积大。瞄 eyes 时，邻域只有 head 和 mouth——等效面积小。但因为 torso 在 head 的下一跳，eyes 的等效面积不会缩到荒谬的小值（约 0.44 倍），体现了「头连着躯干」的直觉。

### 换 root 的 targeting_graph

命中后，不取 `biggest_bp` 为 root，而是取 `aimed_part`：

```cpp
const bodypart_id root = aimed_part.is_valid()
    ? aimed_part
    : *std::max_element( cached_bps.begin(), cached_bps.end(),
        []( auto &lhs, auto &rhs ) { return lhs->hit_size < rhs->hit_size; } );

targeting_graph<bodypart_id, bp_wrapper> graph;
graph.generate( root, cached_bps );
return graph.select( range_min, range_max, value );
```

`targeting_graph` 的算法不变：从 root 出发按 `hit_size` 权重随机选子节点，走一条路径到叶子，`value` 决定在这条路径上走多远。root 越小，停留在 root 或其近邻的概率越高。

---

## 对人类 anatomy 的推演

图结构（`connected_to`）：

```
torso(36) ─── arm_l(13), arm_r(13), leg_l(13), leg_r(13), head(4)
head(4) ─── eyes(0.5), mouth(0.5)
arm_l(13) ─── hand_l(1.5)
arm_r(13) ─── hand_r(1.5)
leg_l(13) ─── foot_l(2)
leg_r(13) ─── foot_r(2)
```

### 等效面积

| 瞄准部位 | d=0 | d=1 | d=2 | d=3 | d=4 | 等效面积 | ratio |
|---------|-----|-----|-----|-----|-----|---------|-------|
| torso | 36/1=36 | 56/2=28 | 8/3=2.67 | — | — | **66.67** | **1.000** |
| head | 4/1=4 | 37/2=18.5 | 52/3=17.33 | 7/4=1.75 | — | **41.58** | **0.624** |
| arm_l | 13/1=13 | 37.5/2=18.75 | 43/3=14.33 | 6.5/4=1.625 | — | **47.71** | **0.715** |
| hand_l | 1.5/1=1.5 | 13/2=6.5 | 37.5/3=12.5 | 43/4=10.75 | 7/5=1.4 | **32.25** | **0.484** |
| eyes | 0.5/1=0.5 | 4.5/2=2.25 | 36/3=12 | 52/4=13 | 7/5=1.4 | **29.15** | **0.437** |

### 最终效果

| 瞄准部位 | ratio | target_size 缩放 | 相当于 missed_by 倍数 |
|---------|-------|-----------------|----------------------|
| torso | 1.000 | ×1.00 | ×1.00 |
| head | 0.624 | ×0.62 | ×1.60 |
| arm/leg | ~0.72 | ×0.72 | ×1.39 |
| hand/foot | ~0.49 | ×0.49 | ×2.04 |
| eyes | 0.437 | ×0.44 | ×2.29 |

梯度自然：
- **torso**： easiest，基本无惩罚
- **head/arm/leg**：中等难度（命中率约降 30~40%）
- **hand/foot/eyes**：高难度（命中率约降 50~55%）

没有魔法数字。全部来自图结构 + `hit_size`。

---

## 快捷键设计

瞄准界面（`target_ui`）现有按键：`f` 开火、`a` 瞄准、`s` 切换模式、`p` 切换弹药、`↑↓←→` 移光标、`Tab` 切换目标。

**新增：**

| 按键 | 动作 |
|------|------|
| `` ` `` / `~` | **循环切换瞄准部位**（在目标所有部位间轮转） |

> `1-5` 固定映射取消。因为九头蛇有 5 个头，固定映射会冲突。纯列表轮转由 anatomy 决定顺序。

---

## C++ 改动

### 1. `src/anatomy.h` / `anatomy.cpp` — 等效面积 + 换 root

```cpp
// anatomy.h
class anatomy {
    // 新增：缓存等效面积（只算一次）
    double calc_effective_size( const bodypart_id &root ) const;
    mutable std::map<bodypart_id, double> effective_size_cache;
public:
    double effective_size( const bodypart_id &root ) const;
    double effective_size_ratio( const bodypart_id &root ) const;
    
    // 原函数加 aimed_part 参数
    bodypart_id select_body_part_projectile_attack(
        double range_min, double range_max, double value,
        bodypart_id aimed_part = bodypart_str_id::NULL_ID() ) const;
};
```

```cpp
// anatomy.cpp

double anatomy::calc_effective_size( const bodypart_id &root ) const {
    // BFS 建距离图
    std::map<bodypart_id, int> dist;
    std::queue<bodypart_id> q;
    q.push( root );
    dist[root] = 0;
    while( !q.empty() ) {
        bodypart_id cur = q.front(); q.pop();
        for( const bodypart_id &bp : cached_bps ) {
            if( dist.count( bp ) ) continue;
            // 双向邻接：connected_to 或互相连接
            if( bp->connected_to == cur || cur->connected_to == bp ) {
                dist[bp] = dist[cur] + 1;
                q.push( bp );
            }
        }
    }
    double total = 0.0;
    for( const auto &[bp, d] : dist ) {
        total += static_cast<double>( bp->hit_size ) / ( d + 1.0 );
    }
    return total;
}

double anatomy::effective_size( const bodypart_id &root ) const {
    auto it = effective_size_cache.find( root );
    if( it != effective_size_cache.end() ) return it->second;
    double es = calc_effective_size( root );
    effective_size_cache[root] = es;
    return es;
}

double anatomy::effective_size_ratio( const bodypart_id &root ) const {
    bodypart_id biggest = *std::max_element( cached_bps.begin(), cached_bps.end(),
        []( const bodypart_id &lhs, const bodypart_id &rhs ) {
            return lhs->hit_size < rhs->hit_size;
        } );
    return effective_size( root ) / effective_size( biggest );
}

bodypart_id anatomy::select_body_part_projectile_attack(
    double range_min, double range_max, double value,
    bodypart_id aimed_part ) const
{
    const bodypart_id root = aimed_part.is_valid()
        ? aimed_part
        : *std::max_element( cached_bps.begin(), cached_bps.end(),
            []( const bodypart_id &lhs, const bodypart_id &rhs ) {
                return lhs->hit_size < rhs->hit_size;
            } );

    targeting_graph<bodypart_id, bp_wrapper> graph;
    graph.generate( root, cached_bps );
    return graph.select( range_min, range_max, value );
}
```

### 2. `src/creature.h` / `creature.cpp` — 调用点传 aimed_part + target_size 缩放

```cpp
// creature.cpp: deal_projectile_attack 中

// ① 如果有 aimed_part，缩放 target_size
if( aimed_part.is_valid() ) {
    double ratio = get_anatomy()->effective_size_ratio( aimed_part );
    target_size *= ratio;
}

// ② 重新计算 missed_by（因为 target_size 变了）
missed_by = min( 1.0, missed_by_tiles / target_size );

// ③ 判定 hit/miss
goodhit = missed_by + dodge_factor;
if( goodhit >= 1.0 ) {
    // miss — 弹丸偏转，不进入部位选择
    return;
}

// ④ hit → 部位选择，传 aimed_part
projectile_attack_results hit_selection = select_body_part_projectile_attack(
    proj, goodhit, missed_by, aimed_part );
```

### 3. `src/ranged.h` / `ranged.cpp` — target_ui 加部位状态

```cpp
// target_ui 私有成员
bodypart_id aimed_part;
std::vector<bodypart_id> target_parts;

// init_window_and_input() 中
ctxt.register_action( "TOGGLE_AIMED_PART" );   // ~

// run() 事件循环中
if( action == "TOGGLE_AIMED_PART" ) {
    cycle_aimed_part();
    // 改变 aimed_part 后，target_size 变化 → 需要重算命中率显示
    recalc_aim_chances();
    return true;
}

void target_ui::cycle_aimed_part() {
    if( !dst_critter ) return;
    if( target_parts.empty() ) {
        target_parts = dst_critter->get_all_body_parts();
    }
    auto it = std::find( target_parts.begin(), target_parts.end(), aimed_part );
    if( it == target_parts.end() || ++it == target_parts.end() ) {
        aimed_part = target_parts.front();
    } else {
        aimed_part = *it;
    }
}
```

### 4. `src/ranged.cpp` — UI 绘制加部位面板

```cpp
// draw_ui_window() 中
if( dst_critter ) {
    panel_aimed_part( text_y );
    text_y++;
}

void target_ui::panel_aimed_part( int &line ) {
    if( !aimed_part.is_valid() ) {
        print_colored_text( w_target, point( 1, line++ ), c_dark_gray, c_dark_gray,
            _( "Aiming: <color_dark_gray>No part selected</color>" ) );
        return;
    }
    double ratio = dst_critter->get_anatomy()->effective_size_ratio( aimed_part );
    std::string text = string_format(
        _( "Aiming: <color_white>%s</color>  Size: <color_yellow>%.0f%%</color>" ),
        aimed_part->name.translated().c_str(), ratio * 100.0 );
    print_colored_text( w_target, point( 1, line++ ), c_light_gray, c_light_gray, text );
}
```

### 5. `src/ranged.cpp` — 命中率显示纳入 target_size 缩放

```cpp
// calculate_ranged_chances() 中，confidence_estimate 调用前
// 需要把 aimed_part 的缩放传入 Target_attributes

Target_attributes attributes( ... );
if( aimed_part.is_valid() && dst_critter ) {
    double ratio = dst_critter->get_anatomy()->effective_size_ratio( aimed_part );
    attributes.size *= ratio;
}
```

> `Target_attributes` 目前只有 `size` 和 `range`。需要在 `ranged.cpp` 里找到 `confidence_estimate` 调用链，把 `aimed_part` 的缩放因子注入进去。

### 6. `src/ranged.cpp` — fire_gun 传 aimed_part

`aimed_part` 保存在 `aim_activity_actor` 的状态中。`fire_gun()` 时从 activity 读出，传给 `projectile_attack()`。

```cpp
// aim_activity_actor 结构体中加：
bodypart_id aimed_part;

// fire_gun() 中 projectile_attack 调用时：
dealt_projectile_attack shot = projectile_attack(
    proj, pos(), aim, dispersion, this, in_veh, wp_attack, first, activity.aimed_part );
```

`projectile_attack()` 和 `deal_projectile_attack()` 的签名都需要新增 `bodypart_id aimed_part` 参数。

---

## JSON 改动（按键绑定）

```json
{
  "type": "keybinding",
  "id": "TOGGLE_AIMED_PART",
  "category": "TARGET",
  "name": "Cycle aimed body part",
  "bindings": [ { "input_method": "keyboard", "key": "`" } ]
}
```

---

## 效果预期

| 部位 | ratio | 原 target_size | 缩放后 | 体验 |
|------|-------|---------------|--------|------|
| torso | 1.000 | 0.5 | 0.50 | 基准，无惩罚 |
| head | 0.624 | 0.5 | 0.31 | 中等难度，好射手可稳定命中 |
| arm/leg | ~0.72 | 0.5 | 0.36 | 略低于头 |
| hand/foot | ~0.49 | 0.5 | 0.24 | 高难度 |
| eyes | 0.437 | 0.5 | 0.22 | 极高难度，基本只有贴脸神射手能中 |

命中后 `targeting_graph(root=aimed_part)`：
- 瞄 torso → 大概率 torso，小概率四肢/头
- 瞄 head → 大概率 head，小概率 torso，极小概率 eyes
- 瞄 eyes → 大概率 head（eyes 太小，value 稍大就滑到 head），极小概率 eyes

---

## 测试点

1. 按 `~` 切换部位，UI 面板显示部位名和 `Size: 62%` 等比例
2. 瞄 head 后，`confidence_estimate` 显示的命中率显著低于瞄 torso
3. 瞄 eyes 后，命中率极低（贴脸才可能 >50%）
4. 实际开火：
   - goodhit < 1.0 → `select_body_part_projectile_attack` 返回 aimed_part 概率高于随机
   - goodhit ≥ 1.0 → miss，弹丸偏转，与部位无关
5. 对狮鹫按 `~`：torso → head → arm_l → arm_r → ... → wing_l → wing_r → 循环
6. 对九头蛇按 `~`：head_1 → head_2 → ... → head_5 → torso → ...

---

## 文件清单

| 文件 | 改/新 | 内容 |
|------|-------|------|
| `src/anatomy.h` | 改 | `effective_size()` / `effective_size_ratio()` / `select_body_part_projectile_attack` 签名 |
| `src/anatomy.cpp` | 改 | BFS 等效面积计算、缓存、换 root 的 `select_body_part_projectile_attack` |
| `src/creature.h` | 改 | `select_body_part_projectile_attack` 传 `aimed_part` |
| `src/creature.cpp` | 改 | `deal_projectile_attack` 中 `target_size` 缩放 + 部位选择传参 |
| `src/ballistics.h` | 改 | `projectile_attack` 签名加 `aimed_part` |
| `src/ballistics.cpp` | 改 | `projectile_attack` 传参到 `deal_projectile_attack` |
| `src/ranged.h` | 改 | `target_ui` 加 `aimed_part`、`target_parts`、`cycle_aimed_part()` |
| `src/ranged.cpp` | 改 | 按键注册、按键处理、UI 绘制、命中率重算、`fire_gun` 传参 |
| `data/raw/keybindings.json` | 改 | `TOGGLE_AIMED_PART` 绑定 |

---

## 关联任务

- `monster_bodypart_fix.md` — 必须先完成，否则 Monster 没有可瞄部位
- `example_griffin.md` — 狮鹫有 wing_l/r，是测试部位瞄准的好样本
