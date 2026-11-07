# 怪物刷新系统

> 原版基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 初始提交的父提交，含 0.H 发布后的维护修复）。

## 1. 三种不同的数据

- `MonsterGroup`（`src/mongroup.h`）：怪物池定义，包含默认怪物、条目、总权重、替换组等信息。
- `MonsterGroupEntry`：池内一条规则，引用怪物 `name` 或子组 `group`，有权重 `frequency`、人口成本 `cost_multiplier`、`pack_minimum/maximum`、时间/季节/事件条件及 `spawn_data`。
- `mongroup`（同一头文件）：世界中一群怪物的运行时记录，位置成员是绝对 submap 坐标 `abs_pos`，包含人口预算 `population`、horde/target 等状态。若 `monsters` 容器非空，则记录具体怪物而不使用 population 预算。

三者不能混用：JSON 组定义不是已经站在地图上的一队怪物。

### spawn_data

`src/mapgen.h` 的实际成员是：

```cpp
std::map<itype_id, jmapgen_int> ammo;
std::vector<point> patrol_points_rel_ms;
```

`ms` 指 map-square 坐标，不是毫秒。JSON 的 `spawn_data.ammo` 项使用 `ammo_id` 和 `qty`；`patrol` 项使用 `x`、`y`。加载见 `src/mapgen.cpp::jmapgen_monster`，怪物组的附加生成数据见 `src/mongroup.cpp::LoadMonsterGroup`。

## 2. GetResultFromGroup 的抽样语义

入口：`src/mongroup.cpp::MonsterGroupManager::GetResultFromGroup`。

1. 先通过 `GetUpgradedMonsterGroup` 获取时间替换后的组。
2. 在事件调整后的总权重范围内抽数；遍历条目，检查出现条件，再按权重命中一条。
3. 命中具体怪物时产生 `MonsterGroupResult`；其 `pack_size` 表示该结果的个体数。
4. 命中子组时按父条目的 pack 数量反复递归，合并各次返回值，因此一次顶层调用可能返回多种怪物。
5. 顶层没有选出有效怪物时，返回 `defaultMonster`，并使传入的人口预算至少下降一次；子组递归没有结果时不会自行补默认怪物。

`LoadMonsterGroup` 支持 `weight`（旧 `freq` 存在时优先），并计算/读取 `freq_total`、默认条目与节日权重。某条目的绝对权重不是百分比；条件过滤、总权重和默认结果都会影响最终概率。

### pack_size 的版本细节

此基点的 `use_pack_size=false` 分支产生一条 `pack_size=N` 的结果，人口预算减 `max(1, cost_multiplier*N)`。

`use_pack_size=true` 分支则循环 N 次，每次都加入一条 `pack_size=N` 的结果，并重复扣除该成本。因此调用方若逐条按结果数量生成，可能得到 N² 个体。这里是该提交的实际代码行为，不应把参数名理解为“只生成 N 个”的保证，也不应未经验证就当作目标设计。

### 对固定编队的含义

单条普通怪物条目产生同种怪物；子组能混合，但依然是随机抽取。若需要保证“3 个成员 + 1 个队长”的固定组成，应采用分别明确放置的规则或专门逻辑，不能仅靠一个随机组权重保证。Monster 刷新接口也不等于 NPC/Character 队伍刷新接口。

## 3. 常见生成通道

下表是常见入口，不是全部入口（特殊攻击、EOC、任务、调试与其他 C++ 代码也可能直接生成）。

| 通道 | 定义/调用 | 行为 |
|---|---|---|
| Overmap 怪物群 | `overmap::place_mongroups`、special 的 `spawns` | 将人口预算或具体群体写入 overmap；进入局部地图时由 `map::spawn_monsters` 系列消化 |
| OMT 静态刷新 | `overmap_terrain` 的 `spawns` 对象 | `overmap.cpp` 加载到 `static_spawns` 成员，`mapgen.cpp::map::generate` 按 group/人口设置生成；JSON 键不是 `static_spawns`，也不是直接 `monster` ID |
| Mapgen `place_monster` | `jmapgen_monster` | `monster` 是怪物 ID（也支持加权 ID），`group` 则是怪物组；支持 chance、repeat、pack_size 等，结果受密度设置影响 |
| Mapgen `place_monsters` | `jmapgen_monster_group` → `map::place_spawns` | `monster` 字段在这里是组 ID；按面积区域、chance、密度和预算循环抽取 |
| Field 生成 | field 定义的 `monster_spawn_group` 及 field 处理 | 特定场地效果的怪物生成，需结合 field 的触发条件与处理函数 |

### Overmap 到局部地图

`overmap::place_special` 读取 special 的 `spawns`，创建 mongroup 并加入地图。城市群还受城市人口/密度/horde 选项控制。`map::spawn_monsters_submap_group` 等函数在局部生成时调用组抽样，寻找可放置位置；人口预算不是最终成功站在地图上的个体数保证。

### Mapgen 批量

`map::place_spawns` 先做 chance 与密度计算，得到预算 `num`，然后 `while(num > 0)` 抽样。`GetResultFromGroup` 通过指针递减预算，调用方遍历结果并 `add_spawn`。`add_spawn` 写入 submap 的 spawn 记录，和立即构造、激活全部怪物不是同一个阶段。

## 4. 源码定位

- `src/mongroup.h`：定义与运行时群体结构。
- `src/mongroup.cpp::LoadMonsterGroup/GetResultFromGroup`：JSON 条目和抽样。
- `src/mapgen.h::spawn_data`：弹药与巡逻坐标。
- `src/mapgen.cpp::jmapgen_monster/jmapgen_monster_group/map::place_spawns/map::generate`：局部生成入口。
- `src/map.cpp::map::spawn_monsters` 及 submap/group 辅助函数：从存储记录激活怪物。
- `src/overmap.cpp::overmap::place_special/place_mongroups`：special 与城市怪物群。
