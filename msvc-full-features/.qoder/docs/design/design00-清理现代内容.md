# 中世纪转换 mod 设计方案

> 将 CDDA 改造为中世纪风格游戏的 Total Conversion 技术方案。

---

## 核心策略：分层覆写式 Total Conversion Mod

**基本原则：不动 `data/json/` 下任何原始文件。** 一切通过 CDDA 的 mod 覆写系统实现。

CDDA 的 JSON 加载机制是**同名后覆盖**：mod 中声明与核心数据相同的 `type` + `id`，后加载的直接替代先加载的。

### 5层拦截架构

```
┌─────────────────────────────────────────┐
│ Layer 5: EXTERNAL_OPTION 系统开关        │  关闭城市/道路生成
├─────────────────────────────────────────┤
│ Layer 4: region_overlay 地图特征黑名单    │  屏蔽 LAB/MILITARY/URBAN/...
├─────────────────────────────────────────┤
│ Layer 3: MONSTER_WHITELIST / 场景白名单   │  只允许中世纪怪物和场景
├─────────────────────────────────────────┤
│ Layer 2: item_group 掉落物组覆写          │  现代物品 → 中世纪/空
├─────────────────────────────────────────┤
│ Layer 1: 职业/配方/制造覆写               │  替换为中世纪内容
└─────────────────────────────────────────┘
```

---

## 关键发现

### 物品过滤：不需要逐一覆盖上万个物件

核心数据中有 **2873** 个 item_group，但 `innawood`（最接近的参考 mod）只覆写了 **79** 个就达成目标。

原因：**地图黑名单的连带效应**。当 `region_overlay` 把 `LAB, MAN_MADE, MILITARY, URBAN, FARM, EXODII` 全部 blacklist 后，2794 个未覆写的 item_group 永远不会被调用——它们只在已被屏蔽的现代建筑 mapgen 中被引用。

### 物品进入游戏世界的所有通道

| 通道 | 走 item_group？ | 对中世纪的影响 |
|------|:---:|------|
| mapgen `place_items` | ✅ | 地图黑名单后只剩自然地物引用的组 |
| monster `death_drops` | ✅ | 怪物白名单后现代怪物不出现 |
| monster harvest 掉落 | ❌ 直接用ID | 天然物品（肉/骨/皮），无问题 |
| 采集/搜寻 | ✅ | `forage_*`, `trash_forest`，仅5个组需覆写 |
| 地形/家具拆解 `drop_group` | ✅ | 现代家具随建筑一同消失 |
| 挖坟/建造副产物 | ✅ | `allclothes`, `grave` 等约10个组 |
| 硬编码 `spawn_item()` | ❌ 直接用 itype_id | 仅~15个物品，都是中世纪兼容（2x4/splinter/bone等） |
| 职业起始物品 | ❌ 直接定义 | 需覆写 ~25 个职业定义 |
| 配方结果 | ❌ 直接定义 | 需 obsolete 现代配方 |

### 硬编码限制（无法通过 JSON 消除的）

| 系统 | 说明 | 处理方式 |
|------|------|---------|
| 枪械系统 `is_gun()` | 引擎理解"枪" | 覆写枪械 item_group 为弓/弩/火绳枪 |
| 车辆系统 | 引擎理解车辆 | 屏蔽现代部件，或关闭车辆生成 |
| 电力/电子系统 | 物品有 battery 属性 | 不生成电池/电子设备即无影响 |
| 技能 ID | `skill_pistol` 等在 C++ 中引用 | 不删除，但无对应物品就无影响 |
| 部分物品 ID | `itype_paper`, `itype_electrohack` 等 | 保留定义即可，大多为中世纪兼容品 |

---

## item_group 覆写策略

| 类别 | 策略 |
|------|------|
| guns/ 枪械 | → 火绳枪/弓/弩/吹箭 |
| ammo/ 弹药 | → 箭/弩箭/铅弹 |
| clothing/ 衣物 | → 皮/毛/麻/草制品 |
| tools/ 工具 | → 原始石器/骨器/铜器 |
| electronics/ 电子 | → null（直接清空） |
| science/ 科技 | → null |
| military/ 军用 | → null |
| books/ 书籍 | → 手抄本/卷轴 |
| food/ 食物 | → 去除罐头/MRE/加工食品 |
| trash/ 垃圾 | → 自然杂物 |
| medic/ 药品 | → 草药/绷带 |

---

## 参考 mod

`data/mods/innawood/` 是最重要的参考实现。它是一个 total_conversion mod，目标类似（去除人类文明痕迹），使用了与本方案相同的5层机制。

关键文件：
- `modinfo.json` — mod 元信息
- `game_balance.json` — EXTERNAL_OPTION 关闭城市/道路
- `region_overlay.json` — 地图黑名单
- `scenario_whitelist.json` — 场景白名单
- `professions.json` — 职业覆写
- `scenarios.json` — 场景覆写
- `itemgroups/*.json` — 物品组覆写（79个）
- `start_locations.json` — 起始位置定义

---

## 相关文档

| 文档 | 与本方案的关系 |
|------|---------------|
| [../vanilla/json_data_system.md](../vanilla/json_data_system.md) | JSON 加载/覆写/Mod 系统基础机制，理解 5 层架构的前提 |
| [../vanilla/city_generation_system.md](../vanilla/city_generation_system.md) | 城市/道路生成的 C++ 硬编码实现，EXTERNAL_OPTION 关闭城市后 overmap 层面的具体效果 |
| [../vanilla/monster_spawn_system.md](../vanilla/monster_spawn_system.md) | MonsterGroupEntry/GetResultFromGroup 核心算法，MONSTER_WHITELIST 的作用机制 |
| [../process/modern_content_removal.md](../process/modern_content_removal.md) | 基于本方案的实现进度追踪与执行顺序 |
