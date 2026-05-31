# 日常衣物体系实现进度

> 策划案 → [design03-日常衣物.md](../design/design03-日常衣物.md)
> 总追踪 → [core_work.md](../../rules/core_work.md)

## 实现概览

基于设计文档003创建中世纪平民日常衣物体系，覆盖头、躯干、腿、脚、外层、手部及腰带部位。

## 文件清单（9 个新/更新文件）

| 文件 | 设计章节 | 内容 | 状态 |
|------|---------|------|------|
| `materials.json` | 一、物料体系 | 新增 straw、oilcloth 材料 | ✅ 完成 |
| `head_cloth.json` | 2.1 头部 | linen coif, straw hat, felt cap, wool hood, chaperon, leather coif — 6件 | ✅ 完成 |
| `torso_cloth.json` | 2.2 躯干内衣 | 新增 linen chemise（已有 linen shirt + braies）| ✅ 完成 |
| `torso_outerwear.json` | 2.3 躯干主衣 | wool tunic, linen tunic, doublet, kirtle, work apron, leather apron — 6件 | ✅ 完成 |
| `legs_cloth.json` | 2.4 腿部 | wool hose, split hose, joined hose, leg wraps — 4件 | ✅ 完成 |
| `feet_cloth.json` | 2.5 脚部 | linen footwraps, turnshoes, ankle boots, pattens — 4件 | ✅ 完成 |
| `cloaks.json` | 2.6 外层 | wool cloak, oilcloth cloak, wool shawl, fur cloak — 4件（填充原有空文件）| ✅ 完成 |
| `hands_cloth.json` | 2.7 手部 | wool mittens, linen wristwraps — 2件（leather gloves 已在 hands.json）| ✅ 完成 |
| `accessories.json` | 三、腰带 | leather belt, rope belt — 2件（pouch/scrip/waterskin等非ARMOR类型待后续）| ✅ 完成 |

## 物品统计

| 类别 | 件数 |
|------|------|
| 头部衣物 | 6 |
| 躯干内衣 | 1（新增） |
| 躯干外衣 | 6 |
| 腿部衣物 | 4 |
| 足部衣物 | 4 |
| 外层斗篷 | 4 |
| 手部衣物 | 2 |
| 腰带 | 2 |
| **合计** | **29 件新物品 + 2 种新材料** |

## 新材料

| 材料 ID | 名称 | 基于 | 用途 |
|--------|------|------|------|
| `straw` | Straw | copy-from cotton | 草帽（极低防护、良好透气） |
| `oilcloth` | Oilcloth | copy-from linen | 油布斗篷（高 wind_resist: 95, POOR breathability） |

## 设计覆盖情况

### 已实现

- **头部（2.1）** — 6/6 全部：coif (linen), straw hat, felt cap, wool hood, chaperon, leather coif
- **躯干内衣（2.2）** — 3/3 全部：linen shirt（已有）, linen braies（已有）, linen chemise（新增）
- **躯干主衣（2.3）** — 6/6 全部：wool/linen tunic, doublet, kirtle, work/leather apron
- **腿部（2.4）** — 4/4 全部：wool hose, split hose, joined hose, leg wraps
  - Linen Braies (outer) 跳过 — 复用已有 underwear braies 即可
- **脚部（2.5）** — 4/5：footwraps, turnshoes, ankle boots, pattens（Barefoot 无需物品）
- **外层（2.6）** — 4/4 全部：wool/oilcloth/fur cloak, wool shawl
- **手部（2.7）** — 2/3：wool mittens, linen wristwraps（Leather gloves 已在 hands.json）
- **腰带（三）** — 2/2 ARMOR类型：leather belt, rope belt

### 待后续实现

- **腰带随身物品（三）** — belt pouch, scrip bag, waterskin, eating knife, tinder pouch, tankard（需 CONTAINER/TOOL/GENERIC 类型，非纯 ARMOR）

## 验证记录

- 2026-05-11: 全部 29 件物品 + 2 种材料通过 `--check-mods medieval` C++ 级验证
  - Exit code: 0（mod 加载成功）
  - 10 个 LOW 级别 `translation.cpp:234` 建议（脚/腿/手部双数物品 name 用 `str`+`str_pl` 替代 `str_sp`）
  - 0 个 CRITICAL 或 HIGH 错误

## 写作规范

1. **Name 前缀 `med_`** — 所有物品 `name` 以 `med_ ` 开头
2. **Head 部位用 `encumbrance_modifiers`** — 遵循项目通用规范
3. **非 head 部位用直接 `encumbrance`** — torso/leg/foot/hand 等
4. **`specifically_covers`** — 精确指定子部位覆盖
5. **`FIT` flag** — 所有 VARSIZE 物品加 FIT
6. **`OUTER` flag** — 外层装备加 OUTER
7. **Description 双空格** — 句号后双空格 `.  `
8. **`str` + `str_pl` 格式** — 双数物品同步指定单复数（尽管 translation.cpp 建议用 `str_sp`，但 flexbuffer 拒绝纯 `str_sp`）
