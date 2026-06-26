# 中世纪野怪与强盗据点/遭遇体系实现进度

> 设计策划案 → [design08-敌人.md](../design/design08-敌人.md) & [design08_1-野怪_强盗.md](../design/design08_1-野怪_强盗.md)
> 总任务追踪 → [core_work.md](../../rules/core_work.md)

本进度文档记录中世纪模组中**强盗野怪 NPC 体系（共 8 款 NPC 实例）**与野外伏击遭遇（EOC）的实装现状与未来规划。

---

## 一、 中世纪强盗 NPC 总索引 (Bandit NPC Index)

目前强盗与遭遇系统已实装 **8 款核心 NPC 实例** 与其对应的 **6 大 NPC Class 属性**。所有的武器和防具均在生成时根据身份附带随机损坏属性（`damage` 分布），完全符合中世纪荒野求生的氛围。

| NPC 实例 ID | 显示名称 (Suffix) | 关联 Class ID | 战术定位与核心武器 | 状态 | 备注 / 现状 |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `med_bandit_grunt` | Bandit | `NC_MED_BANDIT_WEAK` | 弱鸡民兵，持棍棒/叉子/连枷 | `[x]` | 穿戴破旧布衣。 |
| `med_bandit_veteran` | Bandit | `NC_MED_BANDIT_MEDIUM` | 强盗老手，持弯刀/手斧/矛 | `[x]` | 穿戴武装衣与皮盔帽。 |
| `med_bandit_elite` | Bandit Elite | `NC_MED_BANDIT_STRONG` | 精锐悍匪，持战斧/战锤/武装剑 | `[x]` | 穿戴平民铆甲/杰克甲与钢锅盔。 |
| `med_bandit_archer` | Bandit Archer | `NC_MED_BANDIT_ARCHER` | 强盗弓手，持短弓/轻弩/投石索 | `[x]` | 随身携带 15-25 支箭/弩矢或投石。 |
| `med_bandit_marksman` | Bandit Marksman | `NC_MED_BANDIT_MARKSMAN` | 森林狙击手，持长弓/重弩 | `[x]` | 随身携带 20-30 支高级锥头弹药。 |
| `med_bandit_chief` | Bandit Chief | `NC_MED_BANDIT_LEADER` | 强盗头领，持精钢大剑/战斧/战锤 | `[x]` | 身披锁子甲大衣与猪面尖顶盔。 |
| `med_bandit_beggar` | Starving Peasant | `NC_MED_BANDIT_WEAK` | 伪装乞丐，对话触发远近伏击 | `[x]` | **剧情互动型 NPC**，初始中立。 |
| `med_bandit_toll_road` | Toll Bandit | `NC_MED_BANDIT_MEDIUM` | 收费路匪，对话选择拒绝即开战 | `[x]` | **剧情互动型 NPC**，初始中立。 |

---

## 二、 强盗系统开发阶段 Checklist

中世纪强盗系统已成功推进至**阶段 2** 的完整闭环，全部核心功能已于游戏中实装且完成编译加载验证。

### 阶段 1：强盗据点（Bandit Camp）与 Melee 铁三角实装
- [x] 实装敌对强盗派系 `med_bandits`（对玩家及随从 kill on sight，同伙互助）。
- [x] 实装基础 Melee 三大 NPC 阶梯：喽啰 (`grunt`)、老手 (`veteran`)、头领 (`chief`)。
- [x] 实装嵌套式集合防具与武器池，彻底解决强盗生成时“由于 distribution 导致的全身裸露仅戴头盔”的物理 Bug。
- [x] 为各级强盗装备引入**环境损伤比例（damage 分布）**：
  - 喽啰装备必然破损 (`[1, 3]`)；
  - 老手装备中度磨损 (`[0, 2]`)；
  - 头领装备最佳保养 (`[0, 1]`)。
- [x] 实现 24×24 自然环境强盗营地 mapgen，开辟了南北双向道路出口以避免“被树木卡死无法进入”的逻辑 Bug。
- [x] 实现大地图 Special 生成在 Forest 荒野并注册高风险标识 `B`。

### 阶段 2：交互型对话路匪与多梯队野外伏击 (本阶段已完成)
- [x] **实装对话收费路匪 `med_bandit_toll_road`**：
  - 初始处于中立状态，可通过 `e` 互动触发对话。
  - 选择进行交易可顺利启动 `start_trade` 进入交易流程。
  - 选择拒绝付款，NPC 立即敌对，并精准在玩家身边召唤 2 名喽啰从两翼草丛伏击。
- [x] **实装伪装乞丐/饥民对话陷阱 `med_bandit_beggar`**：
  - 初始显示为无害的黄名“饥饿平民”，点击进入悲惨求助对白。
  - **分支 A（给予食物）**：平民冷笑翻脸，指使潜伏在四周的 2 名喽啰冲出包夹。
  - **分支 B（拒绝帮助）**：平民暴怒直起身子并立刻敌对，吹响尖声哨音引出最强包围网：2 名喽啰 + 1 名强盗老手。
  - **分支 C（揭穿识破）**：平民阴森冷笑，威胁“今日是你的忌日”并召唤 2 名喽啰。
- [x] **实装精细化 3 类新强盗 Class**：精锐 (`elite`)、强盗弓手 (`archer`)、神射手 (`marksman`)，为其赋予了合理的 `rng` 技能梯度。
- [x] **实装弹药自适应口袋携带组**，保证弓弩手必定随身在物品袋中携带有木箭/木弩矢/投石弹药。
- [x] **重构 8 组野外随机伏击遭遇（EOC）**，在野外散步以 `30 minutes`（30分钟判定周期）与 `1/20` 概率自然刷新远近组合、树林单兵冷箭、精锐双人以及高危 Boss 首领团。
- [x] **实装一键调试召唤 EOC (`EOC_MED_TEST_SPAWN_ALL`)**：可在 Debug 菜单中通过 `Activate EOC` 瞬间生成 5 款核心 NPC 直观进行对话和战斗测试，0 C++ 污染。
- [x] **模组校验通过**：使用 `cataclysm-tiles.exe --check-mods Medieval` 完美通过 Exit Code 0，无任何语义和格式报错。

### 阶段 3：强盗哨站、俘虏与黑市交易扩展 (未来计划)
- [ ] **实装多格大型“强盗木堡哨站”（2×2 Overmap Special）**：
  - 设计带有木制瞭望塔、简易吊桥及地牢的防御型强盗哨站。
  - 在哨站地牢中放置被绑架的村民 NPC，玩家解救可获得冒险者公会声望。
- [ ] **扩展黑市强盗黑货商人 NPC**：
  - 在特定据点放置中立的强盗军需官，支持玩家用偷来的赃物或通过特殊硬币交易高阶违禁品。
