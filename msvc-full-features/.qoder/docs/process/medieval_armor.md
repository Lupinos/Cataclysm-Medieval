# 盔甲体系实现进度

> 策划案 → [design02-盔甲.md](../design/design02-盔甲.md)
> 总追踪 → [core_work.md](../../rules/core_work.md)

## 文件组织方案

按**身体部位 × 盔甲层次**分文件，每个文件内含该部位所有钢材等级（brigandine 多级 copy-from 模式）。

### 文件清单（13 个）

| 文件 | 设计章节 | 计划内容 | 状态 |
|------|---------|---------|------|
| `head.json` | 2.1 头部 | Kettle Hat, Bascinet, Bascinet+Visor, Great Helm, Sallet (单钢级 mc_steel, 7件) | ✅ 完成 (med_ 前缀) |
| `neck.json` | 2.2 颈部 | Mail Aventail (lc_steel_chain), Leather Standard (hardened_leather), Gorget (mc_steel), Bevor (mc_steel) — 4件 | ✅ 完成 (med_ 前缀) |
| `torso_cloth.json` | 2.3 内衣 (Layer1) | Linen Shirt, Linen Braies (单材料级 linen, 2件) | ✅ 完成 (med_ 前缀) |
| `torso_gambeson.json` | 2.3 武装衣 (Layer2) | Quilted Linen Gambeson (单材料级 linen_quilted, 1件) | ✅ 完成 (med_ 前缀) |
| `torso_leather.json` | 2.3 皮甲 (Layer2.5) | Leather Armor, Cuir Bouilli (单材料级 leather/hardened_leather, 2件) | ✅ 完成 (med_ 前缀) |
| `torso_mail.json` | 2.3 锁子甲 (Layer3) | Mail Hauberk (单材料级 lc_steel_chain, 1件) | ✅ 完成 (med_ 前缀) |
| `torso_brigandine.json` | 2.3 Brigandine (Layer3.5) | Coat of Plates (lc_steel), Brigandine (mc_steel) — 2件 | ✅ 完成 (med_ 前缀) |
| `torso_plate.json` | 2.3 板甲躯干 (Layer4) | Cuirass (单材料级 mc_steel, 1件) | ✅ 完成 (med_ 前缀) |
| `arms.json` | 2.4 手臂 | Spaulder, Rerebrace, Couter, Vambrace (单钢级 mc_steel, 4件) | ✅ 完成 (med_ 前缀) |
| `hands.json` | 2.5 手 | Leather Gloves (leather), Mail Mittens (lc_steel_chain), Hourglass Gauntlets (mc_steel), Plate Gauntlets (mc_steel) — 4件 | ✅ 完成 (med_ 前缀) |
| `legs.json` | 2.6 腿部 | Mail Chausses (lc_steel_chain), Cuisses, Poleyn, Greaves (单钢级 mc_steel, 4件) | ✅ 完成 (med_ 前缀) |
| `feet.json` | 2.7 脚 | Leather Boots (leather), Mail Sabatons (lc_steel_chain), Plate Sabatons (mc_steel) — 3件 | ✅ 完成 (med_ 前缀) |
| `cloaks.json` | — | Wool Cloak, Hooded Cloak | 空占位 |

## 写作规范（已验证）

1. **`encumbrance` 与 `encumbrance_modifiers` 互斥（同一 section）** — 一个 armor section 只能二选一，同一 item 内可混合（主 section 用 modifiers，eyes/mouth 等子 section 用直接 encumbrance）
2. **head 部位推荐 `encumbrance_modifiers`** — 让引擎从重量推导基础负重，通过 modifier 组合表达人体工学设计：`NONE`(简单) → `WELL_SUPPORTED`(×0.8, 中期设计) → `RESTRICTS_NECK+WELL_SUPPORTED`(×0.8+10, 古早设计偏移)
3. **非 head 部位必须用直接 `encumbrance`** — `calc_encumbrance` 仅 head 有 `encumbrance_per_weight` 表，torso/arm/leg 等会报错
4. **多级钢材用 `copy-from` + `replace_materials`** — 基础定义写全部字段，升级版3行搞定
5. **Per-section material 格式** — 必须用 `[{type, covered_by_mat, thickness}]` 而非旧式顶层 `protection`
6. **头盔面甲用 `rigid_layer_only: true`** — 限制只对硬质层生效
7. **锁子甲用 `_chain` 变体材料** — `steel_chain` 而非 `steel`
8. **Name 前缀 `med_`** — 所有物品 `name.str` 以 `med_ ` 开头（如 `"med_ kettle hat"`），方便控制台 `med_` 过滤搜索。ID 不需要此前缀
9. **不生成 XL/XS 变种** — 初版只做标准尺寸
10. **占位文件用 `[]` 空数组** — CDDA 解析器要求数组中所有对象必须有 `type` 字段，注释对象也不行
11. **`torso_neck` 等 secondary sub-location 仅限 BELTED 层** — 源码 `item_factory.cpp:2006` 检查。颈部装备正确做法：`covers: ["head"]` + `specifically_covers: ["head_throat", "head_nape"]`（参照原版 aventail）
12. **`*_steel_chain` 材料 thickness 必须是 1.2 的整数倍** — 链钢材料 `sheet_thickness: 1.2`，引擎用 `std::fmod` 校验。有效值: 1.2, 2.4, 3.6... 普通 steel 材料无此限制
13. **VARSIZE 盔甲需加 `FIT` flag** — `VARSIZE` 表示"可调整"而非"已合身"，无 `FIT` 时初始显示 `(poor fit)`。中世纪装备加 FIT 确保初始即合身

## 测试历史

- 2026-05-07: `armor.json` (13件测试用钢甲) 写入并通过 L0 验证和游戏加载
  - **关键修复**: `encumbrance` + `encumbrance_modifiers` 共存导致 "Invalid field" 错误
  - 测试文件随后删除，正式文件用占位符重建
- 2026-05-08: 
  - `head.json` 填充完成 (7件)
  - **关键修复**: 占位符中的 `{"//": "TODO..."}` 对象导致 "missing required field 'type'" 错误，全部改为 `[]` 空数组
  - `materials.json` 创建 (3种新材料: `linen`, `linen_quilted`, `hardened_leather`)，用 `copy-from` 复用原版模板
  - `head.json` 亚麻兜帽材质从 `cotton` 修正为 `linen`
  - `neck.json` 填充完成 (3件: aventail / leather standard / gorget)
  - **关键修复**: `encumbrance_modifiers` (RESTRICTS_NECK等) 仅适用于 `head` 部位。`calc_encumbrance` 依赖 body part 的 `encumbrance_per_weight` 表，torso 无合适范围，700g gorget 低于最小阈值触发 "Can't find a notable point" 错误。非 head 部位一律使用直接 `encumbrance` 值
  - **关键修复**: `torso_neck` 是 secondary sub-body-part，源码强制要求 BELTED 层（`item_factory.cpp:2006`）。移除 neck.json 所有 `specifically_covers: ["torso_neck"]`，仅用 `covers: ["torso"]` + coverage 表达局部覆盖
  - **关键修复**: `*_steel_chain` 材料 `sheet_thickness: 1.2`，引擎 `std::fmod` 校验 thickness 必须是其整数倍。med_aventail 的 lc_steel_chain thickness 从 1.5 修正为 1.2
  - **关键修复**: 全部 10 件装备 `name.str` 添加 `med_` 前缀（如 `"med_ linen hood"`）用于控制台搜索。ID 保留原样
  - **关键修复**: VARSIZE 装束初始显示 `(poor fit)` — `item.cpp:3501` 要求 FIT flag 才显示 `(fits)`。全部 10 件装备添加 FIT flag
  - 全部 14 文件通过 JSON 语法验证
  - **关键修复: encumbrance 体系重新设计** — 从"永远不用 modifiers"转为学习原版方案，head 部位用 `encumbrance_modifiers`（重量驱动 + modifier 组合表达人体工学年代），非 head 部位用直接 `encumbrance`。规则更新：`NONE`(简单) → `WELL_SUPPORTED`(中期设计, ×0.8) → `RESTRICTS_NECK+WELL_SUPPORTED`(古早设计, ×0.8+10偏移)
  - `head.json` 全部 7 件改用 `encumbrance_modifiers`；`neck.json` covers 改为 `head` + `head_throat`/`head_nape`（现可安全使用 head modifiers）
  - `neck.json` **新增 Bevor (板甲护颚, mc_steel)** — sallet 搭档，覆盖 head_throat + mouth(下颌/脸颊/唇)，2 armor sections（head 用 WELL_SUPPORTED, mouth 用 encumbrance: 10 + rigid_layer_only）
  - `design02-盔甲.md` 2.2 节补充 Bevor 条目及 Gorget vs Bevor 区分说明
  - `arms.json` 填充完成 (4件: spaulder / rerebrace / couter / vambrace, 单 mc_steel 级)
  - `legs.json` 填充完成 (4件: mail chausses / cuisse / poleyn / greave, 单 mc_steel/lc_steel_chain 级)
  - 臂/腿非 head 部位统一用直接 `encumbrance`；`covers` 左右肢并列 + `specifically_covers` 子部位
  - 关节盔甲(couter/poleyn)用 1.8mm 略厚钢板，其余 plate 用 1.5mm
  - Mail chausses 用 lc_steel_chain thickness 1.2（1.2 整数倍），无 specifically_covers（覆盖全腿）
  - 全部 8 件通过 JSON 语法验证和规范检查
  - `hands.json` 填充完成 (4件: leather gloves / mail mittens / hourglass gauntlets / plate gauntlets, 单材料级)
  - `feet.json` 填充完成 (3件: leather boots / mail sabatons / plate sabatons, 单材料级)
  - 手部/脚部统一用直接 `encumbrance`（非 head 部位）；每件 `covers: ["hand_l", "hand_r"]` 或 `["foot_l", "foot_r"]` + `specifically_covers` 子部位
  - Leather boots 分两层 section：upper (2mm leather) + sole (4mm leather, encum 0)
  - Hourglass gauntlets/plate gauntlets 分两层 section：back+wrist (较厚钢板) + palm+fingers (较薄钢板/低encum)
  - Mail sabatons 不覆盖 foot_sole（锁子甲穿在靴外，不包鞋底）
  - 全部 7 件通过 L0 (json_formatter.exe) 和 L2 (list_duplicates.py) 验证
  - `torso_cloth.json` 填充完成 (2件: linen shirt / linen braies, 单 linen 级)
  - `torso_gambeson.json` 填充完成 (1件: gambeson, 单 linen_quilted 级)
  - `torso_leather.json` 填充完成 (2件: leather armor / cuir bouilli, 单 leather/hardened_leather 级)
  - `torso_mail.json` 填充完成 (1件: mail hauberk, 单 lc_steel_chain 级)
  - `torso_brigandine.json` 填充完成 (2件: coat of plates [lc_steel] / brigandine [mc_steel])
  - `torso_plate.json` 填充完成 (1件: cuirass, 单 mc_steel 级)
  - 全部 torso 9 件使用 `covers: ["torso"]` + `specifically_covers: ["torso_upper", "torso_lower"]`，回避 `torso_neck`/`torso_waist`（secondary sub-location，需 BELTED 层）
  - 非 head 部位统一用直接 `encumbrance`（遵循规范3）
  - Linen 内衣: encum 1, thickness 0.5mm；Gambeson: encum 10, thickness 4.0mm
  - Leather / Cuir Bouilli: encum 6-7, thickness 2.5mm
  - Mail Hauberk: encum 18, lc_steel_chain 1.2mm (1.2整数倍) + leather 0.5mm lining
  - Coat of Plates: encum 14, lc_steel 1.5mm + leather 1.0mm shell
  - Brigandine: encum 12, mc_steel 1.8mm + leather 0.8mm shell
  - Cuirass: encum 16, mc_steel 2.5mm + leather 0.5mm lining, to_hit -2
  - 锁甲/板甲类均加 `STURDY` flag + `melee_damage`（bash 1-3），皮布类不加
  - 全部 torso 9 件通过 L0 (json_formatter.exe) 和 L2 (list_duplicates.py) 验证
  - 全部 13 个 armor 文件均已完成（仅剩 `cloaks.json` 空占位）
