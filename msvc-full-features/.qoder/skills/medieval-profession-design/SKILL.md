---
name: medieval-profession-design
description: Guides the design and validation of CDDA profession JSON for the Medieval mod. Use when adding or editing starting professions, selecting starting equipment, assigning skills, or troubleshooting profession load/runtime errors.
---

# Medieval Profession 设计方法论

> 用于 CDDA Medieval mod 中 `profession` JSON 的设计、校验与排错。
> 本 skill 聚焦方法论，不记录具体数值。

---

## 核心原则

### 1. 每个 ID 必须查询确认，禁止想当然

CDDA 中大量命名具有迷惑性，策划文档中的名称与实际 JSON ID 经常不一致。

**必须显式查询的 ID 类型：**
- 技能 ID（如穿刺技能是 `stabbing`，不是 `piercing`）
- 物品 ID（如大箭袋是 `quiver_large`，不是 `large_quiver`）
- 容器 ID（确认存在且可用）
- 武器/护甲/材料 ID

**查询方式（按优先级）：**
1. `grep_code` / `grep-cpp` 搜索 `data/json/` 或 `data/mods/Medieval/`
2. `read_file` 阅读目标 JSON 文件确认字段
3. 不要依赖记忆或策划文档中的中文/英文名称

**决策记录**：
- 设计文档可能写 "Piercing"，但代码层技能 ID 是 `stabbing`。
- 设计文档可能写 "长弓手 Archery"，但弩的实际武器 skill 字段是 `rifle`。

---

### 2. 技能必须与武器实际 `skill` 字段一致

武器的 `skill` 字段决定它使用哪个技能。职业的 `skills` 列表必须匹配，否则 --check-mods 会报 `skill X does not exist` 或角色无法有效使用武器。

**校验步骤：**
1. 打开武器 JSON，读取 `"skill"` 字段
2. 打开 `data/json/skills.json`，确认该技能 ID 存在
3. 职业 `skills` 中使用完全相同的小写 ID

---

### 3. 容器与内容物必须做四维匹配

`container-item` 不是"把东西放进去"就完事，必须同时检查：

| 维度 | 检查项 | 失败后果 |
|------|--------|----------|
| 存在性 | 容器 ID 是否真实存在 | `item id X is unknown` |
| 容量 | `max_contains_volume` / `max_contains_weight` 是否够 | 生成时丢出或报错 |
| 长度 | `max_item_length` 是否容纳内容物 | 长武器/水瓶放不进小袋 |
| 防水 | 液体必须放入 `watertight: true` 的容器 | `cannot contain it: 不能储存液体` |

**操作规范：**
- 用 `read_file` 阅读容器的 `pocket_data`
- 液体（water_clean 等）必须确认容器 `watertight`
- 长柄武器/弩通常无法放入普通容器，需要背包或手持方案

---

### 4. 装备体积必须做容量预算

角色开局时的 inventory 空间有限，职业物品过多或过大时会在运行时触发：

```
Could not put X into inventory. Check if the profession has enough space.
```

**容量预算方法：**
1. 列出所有物品的 `volume` 和 `longest_side`
2. 大件武器（长矛、弩）优先规划为 **手持（wield）** 或放入大容量容器
3. 多个大件同时出现时，必须提供 backpack / duffelbag 等大容量容器
4. 容器本身也有体积，要计入总负载

**默认策略：**
- 主武器手持
- 副武器/备用远程武器放入容器或 sheath
- 水、食物放入对应容器

---

### 5. 容器只声明一次，禁止重复

写了 `container-item` 就不要再单独写 `{ "item": "sheath" }`，否则 CDDA 会生成一个空容器，再生成一个装东西的同名容器，导致装备界面重复。

**正确写法：**
```json
{ "item": "medieval_seax", "container-item": "sheath" }
```

**错误写法：**
```json
{ "item": "sheath" },
{ "item": "medieval_seax", "container-item": "sheath" }
```

---

### 6. Ammo 数量用 `count`，工具/电池用 `charges`

- 箭矢、弩箭、子弹等 **AMMO** 类型：`"count": N`
- 电池、燃料、工具使用次数等：`"charges": N`

用错会导致 ammo 只生成 1 发，或加载失败。

---

## 校验流程

### Step 1: JSON 级静态校验

```powershell
cd E:\Cataclysm-Medieval
.\tools\format\json_formatter.exe data\mods\Medieval\10_medieval_core\professions.json
```

### Step 2: C++ 级加载校验

```powershell
cd E:\Cataclysm-Medieval
.\cataclysm-tiles.exe --check-mods medieval > check_output.txt 2>&1
```

这步能捕获：ID 不存在、技能不存在、JSON 语法错误、文本风格问题等。

### Step 3: 运行时验证（必须）

`--check-mods` **无法捕获** 以下问题：
- 容器容量/长度/防水不匹配
- 职业总装备超过角色 inventory 空间
- 手持武器冲突

**必须实际开一局，选择该职业，确认：**
1. 无红色 debug 弹窗
2. 装备全部正确生成且可穿戴
3. 武器可以正常使用

---

## 常见错误速查

| 报错关键词 | 根因 | 修复方向 |
|-----------|------|----------|
| `skill X does not exist` | 技能 ID 错误或武器 skill 不匹配 | 查 skills.json 和武器 skill 字段 |
| `Skill "X" is context-dependent. It cannot be assigned.` | 使用了 NPC/上下文专用技能 | 从 skills.json 中移除该技能（如 `weapon`） |
| `item id X is unknown` | 物品/容器 ID 不存在 | 用 grep 查真实 ID |
| `cannot contain it: 不能储存液体` | 非防水容器装液体 | 换 waterskin / canteen 等 |
| `Could not put X into inventory` | 总装备体积超过空间 | 加大容器、手持大件、减少物品 |
| 装备界面容器重复 | 同时写了容器本身和 container-item | 删除显式容器条目 |
| 开局只有 1 发箭 | ammo 用了 `charges` | 改为 `count` |

---

## 设计 checklist

添加/修改 profession 时逐项确认：

- [ ] 所有物品 ID 已用 grep / read_file 确认存在
- [ ] 所有技能 ID 已用 grep / read_file 确认存在、可分配，且与武器 `skill` 字段一致
- [ ] 所有 `container-item` 的容器 ID 已确认存在
- [ ] 液体内容物放入 `watertight` 容器
- [ ] 长/大物品放入足够长度/容量的容器，或规划为手持
- [ ] 没有同时显式声明容器和 `container-item`
- [ ] ammo 使用 `count`，非 `charges`
- [ ] 已运行 `json_formatter`
- [ ] 已运行 `--check-mods medieval` 且通过
- [ ] 已实际开一局测试该职业
