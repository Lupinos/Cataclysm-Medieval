# 解剖/屠宰产物系统：完整 key 引用链

> 核验基点：CDDA `0.H-branch`，提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 改造前的维护分支快照，并非最初的 0.H 发布标签）。下述源码路径均以该提交为准。

> 调研 CDDA 原版的 harvest / dissect / butchery 系统的数据流和引用关系。

---

## 系统概述

三套 JSON 类型协作实现"杀怪→解剖→拿战利品"：

| JSON 类型 | 文件 | 定义什么 |
|-----------|------|---------|
| `harvest_drop_type` | `harvest_drop_type.json` | **怎么掉**：行为规则（屠宰/解剖/需什么技能） |
| `harvest` | `harvest.json` / `harvest_dissect.json` | **掉什么**：具体产物列表，引用上面的 type 和下面的 item |
| `MONSTER` | `monster/*.json` | **谁掉**：生物挂上 harvest 列表 |

---

## 数据引用链

```text
MONSTER.harvest / MONSTER.dissect → harvest.id
harvest.entries[].type           → harvest_drop_type.id
harvest.entries[].drop           → item.id 或 item_group.id（一般按 type.group 校验；死亡预生成有特定路径）
```

`harvest_drop_type::load()` 读取 `group`（默认 false）、`dissect_only`、`harvest_skills` 与提示文本。`harvest_list::check_consistency` 按 group 检查 drop 引用的物品或物品组；屠宰活动的普通物品分支也使用此分类。未给 `harvest_skills` 时默认 survival。

特别注意：`monster::spawn_dissectables_on_death` 对 `mtype.dissect` 的**每个** entry.drop 都直接按 item_group ID 调用，不按 group 过滤，不能用单物品 ID 代替这个组引用。

`harvest_entry::load()` 的字段：

| 字段 | 默认值 / 含义 |
|---|---|
| `drop` | 必需，引用对象 |
| `type` | drop type ID，应为有效规则类型 |
| `base_num` | `[1, 1]`，数量区间基值 |
| `scale_num` | `[0, 0]`，按本次 butchery roll 缩放的区间系数 |
| `max` | 1000，数量上限 |
| `mass_ratio` | 0；非零时按尸体重量计算，覆盖上述数量字段 |
| `flags` / `faults` | 产物旗标/故障 |

原先的火龙内容是项目设计示意，不是原版定义，也不是完整可加载 JSON。新增奇幻生物时应在设计文档定义完整物品、物品组、规则类型和怪物，再用这里的引用关系核对。

---

## 普通产物计算与死亡预存产物

这两条路径不能简单等同为两个互斥活动：DISSECT 活动先处理 CORPSE 口袋，之后仍遍历 `mtype.dissect`（非空时）或回退到 `mtype.harvest` 的产物列表。

| | 普通产物条目 | 死亡预存的解剖物 |
|---|---|---|
| 生成时机 | 屠宰/解剖活动处理适用条目时计算 | `monster::die()` 的正常死亡掉落路径调用预生成 |
| 存放 | 通常放地图；液体另走液体处理 | 有尸体时放 CORPSE 口袋，无尸体时落地图 |
| 数量 | `mass_ratio × 尸体重量`，或由 `base_num + scale_num × butchery roll` 得到区间、抽取并应用上限等修正 | dissect 的每个 drop 按物品组抽取；不使用 entry 的 base_num/scale_num 决定预生成数量 |
| 技能影响 | 与工具质量、敏捷、动作、尸体状态一起影响产量 | 取出时检定成功率 |
| 尸体损坏 | `corpse_damage_effect` 按类型调整 | 取出时的 roll 减尸体 `damage_level()`，并非免疫损坏 |

活动遍历产物列表时，仅 `entry.type->is_itype()` 的普通物品分支实际生成相应 item，不能将组条目与普通物品条目随意互换。

---

## 三层 C++ 数据流

```
游戏启动
   harvest_drop_type.json  →  harvest_drop_type_factory.load()   内存: harvest_drop_type[]
   harvest.json            →  harvest_list_factory.load()         内存: harvest_list[] (每个含 entries)
   monster.json            →  mtype.harvest / mtype.dissect = harvest ID

怪物死亡
   monster::die()
     → spawn_dissectables_on_death(corpse)
        → 读取 mtype.dissect → harvest_list
           → 遍历 dissect entries，对每个 entry.drop 按 item_group ID 调用 items_from()
              → 生成物品，dropped_from = entry.type
              → corpse.put_in(CORPSE pocket)

玩家 butcher
   activity_handlers::butcher_finish()
     → 读取 corpse.get_mtype()->harvest → harvest_list
        → 遍历适用 entries，按重量或数量区间计算，再应用工具、技能、动作与尸体状态修正
           → 生成物品，通常放角色脚下地图；液体另走液体处理

玩家 dissect
   dissect 活动完成
     → 从 corpse CORPSE 口袋取出预生成物品
        → 根据 entry.type 查 harvest_drop_type
           → 获取 harvest_skills，结合敏捷、工具和尸体damage_level检定
              → 通过 → 产物放地图，不是统一直接入背包
              → 失败 → 不产出该物品；生化模块失败可变成 burnt_out_bionic。此预存物品路径不直接调用 msg_dissect_fail
```

---

## NPC 路线的缺失环节

原版 `Character` / `npc` 死亡**不调用** `spawn_dissectables_on_death()`。

若项目希望 NPC 尸体携带自定义的预生成特殊解剖物，应另行设计死亡与尸体存储路径。不能从“NPC 不调用 monster 成员函数”推断原版人类尸体完全不可屠宰/解剖；原版存在 human 尸体与相应活动、士气和熟练度处理。

## 源码核对入口

- `src/harvest.cpp`：`harvest_drop_type::load`、`harvest_entry::load`、`harvest_list::check_consistency`。
- `src/monster.cpp`：`monster::die`、`spawn_dissectables_on_death`。
- `src/activity_handlers.cpp`：`butcher_finish` 及 harvest 辅助路径、`butchery_dissect_skill_level`、`roll_butchery_dissect`、`butcher_dissect_item`、`corpse_damage_effect`。
