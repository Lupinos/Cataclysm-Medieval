# 武器体系实现进度

> 策划案 → [design04-武器.md](../design/design04-武器.md)
> 总追踪 → [core_work.md](../../rules/core_work.md)

---

## 策略

- 每种武器单独 ID，`medieval_` 前缀
- 仅使用 `steel` 单材质等级（暂不做 mc_steel / hc_steel 等分级变体）
- 剑/斧/长柄刃器用 `type: TOOL`，钝器用 `type: GENERIC`，远程用 `type: GUN`
- 所有武器 `name.str` 使用 `med_` 前缀
- 按武器类别分文件，不再合并在单个 melee.json

### 文件清单（7 个文件，52 件武器）

| 文件 | 设计章节 | 内容 | 状态 |
|------|---------|------|------|
| `weapons/swords.json` | 二 | 剑系 6 件 | ✅ 完成 |
| `weapons/axes.json` | 三 | 斧系 4 件 | ✅ 完成 |
| `weapons/hammers.json` | 四 | 锤系 5 件 | ✅ 完成 |
| `weapons/polearms.json` | 五 | 长柄武器 13 件 | ✅ 完成 |
| `weapons/daggers.json` | 六 | 匕首/短刃 7 件 | ✅ 完成 |
| `weapons/ranged.json` | 七 | 远程武器 9 件 | ✅ 完成 |
| `weapons/peasant.json` | 八 | 临时/农民武器 8 件 | ✅ 完成 |

---

## 剑系 `swords.json`（6 件）

| ID | 伤害 (bash/cut/stab) | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_arming_sword` | 6/28/- | MEDIUM_SWORDS | 1450g | 4000 |
| `medieval_longsword` | 8/30/20 | LONG_SWORDS | 1800g | 5500 |
| `medieval_estoc` | 4/-/28 | LONG_THRUSTING_SWORDS | 1600g | 6000 |
| `medieval_falchion` | 8/32/- | SHORT_SWORDS | 1300g | 2500 |
| `medieval_messer` | 6/26/- | MEDIUM_SWORDS | 1400g | 2800 |
| `medieval_shortsword` | 4/18/12 | SHORT_SWORDS | 800g | 2000 |

## 斧系 `axes.json`（4 件）

| ID | 伤害 (bash/cut) | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_hand_axe` | 6/22 | HAND_AXES | 1000g | 1500 |
| `medieval_bearded_axe` | 6/26 | HOOKING_WEAPONRY, HAND_AXES | 1400g | 2200 |
| `medieval_battle_axe` | 12/30 | GREAT_AXES | 2200g | 3500 |
| `medieval_dane_axe` | 8/36 | GREAT_AXES | 2400g | 4000 |

## 锤系 `hammers.json`（5 件）

| ID | 伤害 (bash/stab) | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_mace` | 36/- | MACES | 1500g | 3500 |
| `medieval_flanged_mace` | 38/4 | MACES | 1600g | 4200 |
| `medieval_morning_star` | 28/10 | MACES | 1700g | 3800 |
| `medieval_war_hammer` | 22/20 | HOOKING_WEAPONRY, GREAT_HAMMERS | 1400g | 4000 |
| `medieval_maul` | 48/- | GREAT_HAMMERS | 3500g | 3000 |

## 长柄武器 `polearms.json`（13 件）

| ID | 伤害 | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_spear` | b6, s22 | SPEARS | 1800g | 1200 |
| `medieval_pike` | b4, s26 | SPEARS | 4000g | 1800 |
| `medieval_halberd` | b14, c26, s10 | POLEARMS, HOOKING_WEAPONRY | 3000g | 3500 |
| `medieval_bill` | b10, c22, s8 | POLEARMS, HOOKING_WEAPONRY | 2800g | 3000 |
| `medieval_glaive` | b8, c30 | POLEARMS | 2800g | 3200 |
| `medieval_pollaxe` | b20, c12, s10 | POLEARMS, HOOKING_WEAPONRY | 3200g | 4500 |
| `medieval_bec_de_corbin` | b22, s16 | POLEARMS, HOOKING_WEAPONRY | 3000g | 4800 |
| `medieval_lucerne_hammer` | b24, s12 | POLEARMS, GREAT_HAMMERS | 3000g | 4200 |
| `medieval_guisarme` | b8, c18, s6 | POLEARMS, HOOKING_WEAPONRY | 2600g | 2500 |
| `medieval_voulge` | b10, c24, s8 | POLEARMS | 2800g | 2800 |
| `medieval_fauchard` | b6, c22 | POLEARMS | 2400g | 2200 |
| `medieval_partisan` | b6, c10, s20 | SPEARS, POLEARMS | 2200g | 3000 |
| `medieval_quarterstaff` | b16 | QUARTERSTAVES | 1800g | 300 |

## 匕首/短刃 `daggers.json`（7 件）

| ID | 伤害 | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_eating_knife` | b1, c6 | KNIVES | 80g | 300 |
| `medieval_seax` | b3, c12, s8 | KNIVES | 400g | 800 |
| `medieval_rondel_dagger` | b2, s16 | KNIVES | 350g | 2000 |
| `medieval_baselard` | b2, c12, s10 | KNIVES, SHORT_SWORDS | 500g | 1200 |
| `medieval_bollock_dagger` | b2, c10, s12 | KNIVES | 350g | 1000 |
| `medieval_stiletto` | b1, s18 | KNIVES | 200g | 1500 |
| `medieval_misericorde` | b1, s20 | KNIVES | 300g | 1800 |

## 远程武器 `ranged.json`（9 件）

| ID | 类型 | 伤害 | 射程 | 装填(moves) | 重量 | 价格(postapoc) |
|---|---|---|---|---|---|---|
| `medieval_sling` | GUN | b14 | 12 | 80 | 100g | 100 |
| `medieval_shortbow` | GUN | s3 | 14 | 40 | 500g | 1500 |
| `medieval_longbow` | GUN | s6 | 22 | 50 | 700g | 3500 |
| `medieval_composite_bow` | GUN | s5 | 20 | 35 | 600g | 5000 |
| `medieval_light_crossbow` | GUN | s3 | 10 | 800 | 2500g | 2500 |
| `medieval_heavy_crossbow` | GUN | s5 | 16 | 1500 | 4500g | 4000 |
| `medieval_arbalest` | GUN | s7 | 20 | 2000 | 6000g | 7000 |
| `medieval_javelin` | GENERIC | s18 (+throw 14) | — | melee/thrown | 800g | 800 |
| `medieval_francisca` | GENERIC | c16 (+throw 12) | — | melee/thrown | 900g | 1200 |

## 临时/农民武器 `peasant.json`（8 件）

| ID | 伤害 | 武器分类 | 重量 | 价格(postapoc) |
|---|---|---|---|---|
| `medieval_club` | b14 | BATONS | 1200g | 50 |
| `medieval_wood_axe` | b10, c24 | HAND_AXES | 2000g | 800 |
| `medieval_pickaxe` | b10, s18 | HOOKING_WEAPONRY | 3000g | 600 |
| `medieval_pitchfork` | b4, s16 | SPEARS | 2200g | 300 |
| `medieval_scythe` | b4, c24 | POLEARMS | 2400g | 400 |
| `medieval_blacksmith_hammer` | b20 | BATONS | 1200g | 500 |
| `medieval_flail` | b22 | FLAILS | 1800g | 200 |
| `medieval_rock` | b8 | BATONS | 400g | 0 |

> Quarterstaff 归入 polearms.json，不重复计数。

---

## 待完成

- [x] 剑系 6 件 ✅
- [x] 斧系 4 件 ✅
- [x] 锤系 5 件 ✅
- [x] 长柄武器 13 件 ✅
- [x] 匕首/短刃 7 件 ✅
- [x] 远程武器 9 件 ✅
- [x] 临时/农民武器 8 件 ✅
- [x] melee.json 拆分为 swords + axes + hammers ✅
- [x] L4 `--check-mods` C++ 语义校验 ✅ (exit 0)
- [ ] 游戏内全面测试验证
- [ ] `RAPID` technique 用法验证（quarterstaff 用到）
- [ ] `REACH3` flag 验证（pike 用到）
- [ ] 弓箭 `ammo: ["arrow"]` / 弩 `ammo: ["bolt"]` 确保原版弹药可用

## L4 校验修复记录

2026-05-11 `--check-mods` 首次运行发现 3 类问题，已全部修复：

| 问题 | 文件 | 修复 |
|------|------|------|
| `thrown_damage` 应为数组 | `ranged.json` javelin/francisca | `{...}` → `[{...}]` |
| `str`+`str_pl` 同值应改用 `str_sp` | `feet_cloth.json` (4处) | `{"str":"...","str_pl":"..."}` → `{"str_sp":"..."}` |
| `str`+`str_pl` 同值应改用 `str_sp` | `hands_cloth.json` (2处) | 同上 |
| `str`+`str_pl` 同值应改用 `str_sp` | `legs_cloth.json` (4处) | 同上 |
| 缺少复数形式 | `daggers.json` seax | `{"str":"med_ seax"}` → `{"str_sp":"med_ seax"}` |

**注意**：`check_errors.txt` 中包含大量原版 CDDA monster JSON (fish.json/fungus.json/insect_spider.json) 的 `flexbuffer_json.cpp:341` 既存错误，这些与 Medieval mod 无关。
