# 怪物刷新系统

> 调查日期：2026-05-04 — 为强盗组合刷新需求调研底层机制。

---

## 1. 核心数据结构

### MonsterGroupEntry (`mongroup.h`)

怪物组中的每一条目，定义一种怪物的生成规则：

```cpp
struct MonsterGroupEntry {
    mtype_id name;          // 具体怪物 ID（单怪条目）
    mongroup_id group;      // 子组 ID（嵌套引用）
    int frequency;          // 随机权重
    int cost_multiplier;    // 消耗人口预算的倍率
    int pack_minimum;       // pack_size 下限
    int pack_maximum;       // pack_size 上限
    spawn_data data;        // 弹药/巡逻等附加数据
    std::vector<std::string> conditions;  // 季节等条件
    time_duration starts;   // 最早出现天数
    time_duration ends;     // 最晚出现天数
};
```

- 每条 entry 要么引用具体 `mtype_id`（name），要么引用另一个 `mongroup_id`（group），二选一
- `pack_size` 给出的是**同种**怪物的数量范围

### spawn_data (`mapgen.h`) — 对应 `"spawn_data"` JSON 字段

```cpp
struct spawn_data {
    std::vector<int> ammo;                       // 弹药预设（弹药类型索引）
    std::vector<int> patrol_points_rel_ms;       // 巡逻点（相对坐标，毫秒停留时间）
};
```

### mongroup (`overmap.h`)

大地图上记录的怪物群实例（运行时数据）：

```cpp
struct mongroup {
    mongroup_id type;          // 引用的 monster group
    tripoint_abs_sm pos;       // submap 绝对位置
    unsigned int population;   // 人口预算
    // ... horde/radius/target 等
};
```

---

## 2. 核心算法 GetResultFromGroup() (`mongroup.cpp` line 204-282)

### 关键行为：每次调用只选出一条 Entry

```cpp
std::vector<MonsterGroupResult> MonsterGroupManager::GetResultFromGroup(
    const mongroup_id &group_name, int *quantity, bool *mon_found,
    bool is_recursive, bool *returned_default, bool use_pack_size )
{
    // 1. 概率判定 spawn_chance
    // 2. 遍历所有 entry，按 frequency 加权随机选择一条
    // 3. 命中后：
    if( entry.is_group() ) {
        // 递归进入子组，对 pack_size 的每个单位各自做一次递归抽取
        for( int i = 0; i < pack_size; i++ ) {
            // 每次递归 = 新一轮 GetResultFromGroup，又可以抽到不同的子条目
        }
    } else {
        // 单怪类型：生成 pack_size 个同种怪物
        spawn_details.emplace_back( entry.name, pack_size, entry.data );
    }
    break;  // <-- 关键：命中一条后直接跳出，不会继续选其他 entry
}
```

**结论**：
- **单次调用只返回一种怪物的 N 个个体**（pack_size 只控制同种数量）
- 子组递归时，每个 pack_size 实例各自随机，可以抽出子组内的不同怪物
- **无法在单次调用中保证 "3个强盗 + 1个队长 + 1个法师" 这样的精确组合**

---

## 3. 五条刷新通道

| # | 通道 | 入口 | 时机 | 说明 |
|---|------|------|------|------|
| 1 | **Overmap 野怪** | `overmap::place_specials()` → mongroup 写入 overmap | 世界生成时 | 按 mongroup 的 population 预算，进入 reality bubble 时由 `spawn_monsters()` 逐次调用 GetResultFromGroup |
| 2 | **Mapgen 静态刷怪** | terrain `static_spawns` 字段 | 地图生成时 | 在 terrain JSON 中直接指定 `"monster": "mon_id"` 和数量 |
| 3 | **Mapgen JSON 单怪** | `"place_monster"` + `"group"` 字段 | 地图生成时 | `jmapgen_monster` 调用一次 GetResultFromGroup，`use_pack_size` 可选 |
| 4 | **Mapgen JSON 批量** | `"place_monsters"` + `"monster"`/`"group"` | 地图生成时 | `jmapgen_monster_group` → `place_spawns()` 内部 while 循环多次调用 GetResultFromGroup，按面积密度生成 |
| 5 | **场地刷怪** | `field_type::monster_spawn_group` | 每回合 | 在特定 field 中定时生成怪物 |

### 通道 1 详细流程（Overmap 野怪）

```
世界生成: overmap::place_specials()
  → 对 overmap_special 中的每个 "monster" spawn 点:
    → 用 population 预算创建 mongroup，写入 overmap

运行时（进入 reality bubble）:
  → map::spawn_monsters()
    → map::spawn_monsters_submap()
      → map::spawn_monsters_submap_group()
        → while( population > 0 ):
          → GetResultFromGroup(type, &quantity)  // 每次耗掉 population 预算
          → 对结果中的每个怪物，placement 到地图 tile
```

### 通道 3 详细流程（Mapgen 单怪）

```cpp
// mapgen.cpp jmapgen_monster
if( tmp.val.has_string() ) {
    const mongroup_id chosen_group = mongroup_id( tmp.val.get_string() );
    // 只调用一次！
    const std::vector<MonsterGroupResult> spawn_details =
        MonsterGroupManager::GetResultFromGroup(chosen_group, nullptr, nullptr,
                                                 false, nullptr, use_pack_size);
    // ... placement
}
```

### 通道 4 详细流程（Mapgen 批量）

```cpp
// mapgen.cpp place_spawns()
while( num_s_pawned < max_num ) {
    // 多次循环，每次各自随机
    const std::vector<MonsterGroupResult> spawn_details =
        MonsterGroupManager::GetResultFromGroup(group, &number_of_monsters,
                                                 &monster_found);
    // ... placement, num_s_pawned +=
}
```

---

## 4. 中世纪刷新方案

> 强盗组合等中世纪刷新需求的策划案已移至 → [../design/medieval_spawn_design.md](../design/medieval_spawn_design.md)

---

## 5. 关键文件索引

| 文件 | 内容 |
|------|------|
| [mongroup.h](file:///E:/Cataclysm-Medieval/src/mongroup.h) | MonsterGroupEntry, MonsterGroupResult, MonsterGroup 数据结构 |
| [mongroup.cpp](file:///E:/Cataclysm-Medieval/src/mongroup.cpp) | GetResultFromGroup() 核心算法，LoadMonsterGroup() JSON 加载 |
| [map.cpp](file:///E:/Cataclysm-Medieval/src/map.cpp) L8666-8914 | spawn_monsters_submap_group / spawn_monsters_submap / spawn_monsters |
| [mapgen.cpp](file:///E:/Cataclysm-Medieval/src/mapgen.cpp) L2288-2476 | jmapgen_monster_group / jmapgen_monster（Mapgen JSON 通道） |
| [mapgen.cpp](file:///E:/Cataclysm-Medieval/src/mapgen.cpp) L6330-6363 | place_spawns()（批量生成循环） |
| [overmap.cpp](file:///E:/Cataclysm-Medieval/src/overmap.cpp) L6600-6700 | overmap wild spawn 放置 |
| [spawn_data](file:///E:/Cataclysm-Medieval/src/mapgen.h) L190-193 | spawn_data 结构体（弹药、巡逻点） |
| [mapgen.cpp](file:///E:/Cataclysm-Medieval/src/mapgen.cpp) L6556-6593 | add_spawn()（将 spawn_point 写入 submap->spawns） |
