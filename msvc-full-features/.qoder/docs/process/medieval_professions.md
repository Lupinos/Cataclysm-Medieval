# 中世纪职业实现进度

> `data/mods/Medieval/10_medieval_core/professions.json` — Medieval Mod 开局职业实现进度。
> 设计规范见 [../design/design05-职业.md](../design/design05-职业.md)。

---

## 当前已实现职业

| ID | 名称 | 点数 | 核心技能 | 关键装备 | 定位 |
|----|------|:----:|----------|----------|------|
| `naked_peasant` | Naked Wanderer | 0 | 无 | loincloth / chestwrap | 纯白手起家 |
| `medieval_wandering_swordsman` | Wandering Swordsman | 1 | Cutting 2 / Dodge 1 / Survival 1 | gambeson + arming sword + bollock dagger | 近战入门 |
| `medieval_novice_bowman` | Novice Bowman | 1 | Archery 2 / Survival 1 / Cutting 1 | shortbow + 20 arrows + seax | 远程入门 |

---

## 已实现职业详情

### Wandering Swordsman（流浪剑士）

- **设计来源**：武人出身中「步兵 / 下级佣兵」的轻量漂泊版本。
- **装备**：`med_linen_shirt`、`med_gambeson`、`med_hose_wool`、`med_boots_ankle`、`medieval_arming_sword`、`medieval_bollock_dagger`、`leather_pouch`、水、hardtack。
- **性别差异**：男性 `loincloth`，女性 `chestwrap`。

### Novice Bowman（新兵弓手）

- **设计来源**：武人出身中「猎人」的新手版本。
- **装备**：`med_linen_shirt`、`med_tunic_wool`、`med_hose_wool`、`med_turnshoes`、`medieval_shortbow`、20 支 `arrow_wood_heavy`（置于 `quiver`）、`medieval_seax`（置于 `sheath`）、水（置于 `waterskin`）、`jerky`（置于 `leather_pouch`）。
- **性别差异**：男性 `loincloth`，女性 `chestwrap`。

---

## 待实现职业（按设计文档）

> 以下职业来自 [design05-职业.md](../design/design05-职业.md)，按优先级逐步落地。

### 武人出身（战斗向）

- [ ] 民兵（Militiaman）
- [ ] 猎人（Hunter）
- [ ] 长弓手（Longbowman）
- [ ] 弩手（Crossbowman）
- [ ] 步兵 / 下级佣兵（Footman）
- [ ] 流浪骑士（Hedge Knight）
- [ ] 溃兵（Deserter）

### 底层出身

- [ ] 农奴 / 逃亡农民
- [ ] 乞丐 / 游民
- [ ] 麻风幸存者
- [ ] 苦修者 / 鞭笞派

### 手艺人与市民

- [ ] 铁匠
- [ ] 木匠
- [ ] 鞣皮匠
- [ ] 裁缝
- [ ] 屠夫
- [ ] 磨坊主
- [ ] 车夫
- [ ] 草药师

### 宗教 / 学者

- [ ] 修士 / 托钵僧
- [ ] 朝圣者
- [ ] 书记员 / 抄经士

### 法外之徒

- [ ] 盗猎者
- [ ] 盗贼
- [ ] 流寇 / 强盗

---

## 实现注记

- 所有中世纪职业均绑定到单一开局场景 `medieval_peasant`（`scenarios.json` 白名单控制）。
- underwear 沿用原版 `loincloth` / `chestwrap`，因 Medieval mod 尚未自定义内衣层。
- 技能上限遵循设计文档：初始最高不超过 4 级，当前职业均控制在 2 级以内，保持新手友好。
