# design07-冒险者工会：旧技术方案

> 来源：`archive/medieval-before-redo`。仅供重新设计时查阅，未迁入新基线；旧接口、数据及数值推演须重新核验。完整旧稿保存在该分支的 `msvc-full-features/.qoder/docs/`。本页不表示当前实现状态。

### 2.3 CDDA 实现

| 工会元素 | 实现方式 |
|----------|----------|
| 驻地建筑 | `mapgen` + `overmap_terrain`（`medieval-json-mapgen`） |
| 驻地 NPC | `npc` 实例 + `place_npcs` 放置到地图 |
| 任务板 | 特殊家具 + 可交互 talk_topic 入口 |
| 仓库 | mapgen 中的不刷新容器 |
| 马厩 | 生成坐骑 NPC 的特殊 mapgen |

---

## 三、声望与等级体系

### 3.3 CDDA 实现

- 声望直接用 `faction` 的 `likes_u` / `respects_u` 值
- 等级通过 `u_add_var` 存储，用 `u_has_var` 条件检查
- 任务奖励中的声望增减通过 `mission_definition.end` 的 effect 实现

---

## 四、任务体系

### 4.3 任务类型与 CDDA Goal 映射

| 任务类型 | CDDA Goal | 说明 |
|----------|-----------|------|
| 驱逐野兽 | `MGOAL_KILL_MONSTER_SPEC` | 击杀 N 只指定野生动物 |
| 赏金讨伐 | `MGOAL_KILL_MONSTER` | 击杀唯一命名目标 |
| 物资采集 | `MGOAL_FIND_ITEM` | 交付指定物品 |
| 物资批量 | `MGOAL_FIND_ITEM_GROUP` | 交付组内任意物品×N |
| 送信/传话 | `MGOAL_TALK_TO_NPC` | 与远方 NPC 对话 |
| 寻人 | `MGOAL_FIND_NPC` | 定位失踪 NPC |
| 护送 | `MGOAL_GO_TO` | 到达指定地点（与 NPC 同行） |
| 侦察 | `MGOAL_FIND_MONSTER` | 发现怪物巢穴位置 |
| 清剿据点 | `MGOAL_CONDITION` | 自定义：清除区域内所有敌对 |

### 5.2 CDDA 实现

```
npc_class (技能/属性/装备模板)
    │
    ├→ NC_GUILD_MASTER    → 高 Speech, Literacy, 中等战斗技能
    ├→ NC_GUILD_STEWARD   → 高 Bartering, Speech
    ├→ NC_GUILD_PURSER    → 高 Bartering, 商人模式
    ├→ NC_GUILD_TRAINER   → 高战斗技能, 训练对话
    ├→ NC_GUILD_HOSTLER   → 高 Riding, Survival
    ├→ NC_GUILD_GUARD     → 中高战斗技能, 驻守 AI
    ├→ NC_GUILD_TAVERNER  → 高 Cooking, Speech
    └→ NC_GUILD_RECRUIT   → 随机战斗职业模板（从 profession 池抽）
```

装备通过命名约定分配：`NC_GUILD_GUARD_worn`、`NC_GUILD_GUARD_weapon` 等。

---

## 六、服务层
