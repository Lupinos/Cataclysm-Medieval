# 策划案 005：开局职业与技能映射

## 一、CDDA 原版技能 → 中世纪映射

### 1.1 直接保留

| 原版技能 | 中世纪保留 | 理由 |
|----------|-----------|------|
| Bashing | Bashing | 锤、棍、连枷、盾击 |
| Cutting | Cutting | 剑、斧、镰刀 |
| Piercing Weapons | Piercing | 矛、箭、匕首 |
| Unarmed | Unarmed | 摔跤（中世纪徒手极重要） |
| Dodge | Dodge | 闪避 + 盾牌格挡 |
| Throwing | Throwing | 投矛、飞斧、石块 |
| Archery | Archery | 弓 + 弩 |
| Tailoring | Tailoring | 布甲、皮甲缝制 |
| Cooking | Cooking | 食物处理 |
| Construction | Construction | 木工、石工、筑防 |
| Trapping | Trapping | 陷阱、捕兽 |
| Swimming | Swimming | 不变 |
| Survival | Survival | 更核心（含草药辨识、野外采药） |
| First Aid | First Aid | 包扎、外伤处理 |
| Speech | Speech | 说服、谎言 |
| Bartering | Bartering | 以物易物为主 |

### 1.2 需要替换

| 原版技能 | 中世纪替换 | 说明 |
|----------|-----------|------|
| Driving | **Riding**（骑乘） | 马、骡子；包括马术 + 马车 |
| Mechanics | **Smithing**（锻造） | 金属制品的修理和制造 |
| Electronics | [移除] | 无替代 |
| Computers | **Literacy**（读写/学识） | 读书、解读文卷、辨别真伪 |
| Handguns | [移除] | 无替代 |
| Rifles | [移除] | 无替代 |
| Shotguns | [移除] | 无替代 |
| SMG / Launchers | [移除] | 无替代 |
| Marksmanship | [移除] | 并入 Archery |
| Lockpicking | [移除] | 原版 CDDA 不存在此技能 |

### 1.3 新增技能（仅 3 个）

| 新技能 | 替代 | 说明 |
|--------|------|------|
| Riding | Driving | 骑术 + 驾驭马车 |
| Smithing | Mechanics | 铁匠技能、金属制品修理制造 |
| Literacy | Computers | 读书识字、解读卷宗 |

> 盾牌格挡由 Dodge 覆盖，盾击由 Bashing 覆盖；木工和皮工统一由 Fabrication 覆盖；草药辨识由 Survival 覆盖。不再额外拆分独立技能。

---

## 二、开局职业设计

### 分类结构

```
职业设计总览
├── 底层出身（最难开局）
│   ├── 农奴 / 逃亡农民
│   ├── 乞丐 / 游民
│   ├── 麻风幸存者
│   └── 苦修者 / 鞭笞派
├── 手艺人与市民（中等难度）
│   ├── 铁匠
│   ├── 木匠
│   ├── 鞣皮匠
│   ├── 裁缝
│   ├── 屠夫
│   ├── 磨坊主
│   ├── 车夫
│   └── 草药师
├── 武人出身（战斗向）
│   ├── 民兵
│   ├── 猎人
│   ├── 长弓手
│   ├── 弩手
│   ├── 步兵 / 下级佣兵
│   ├── 流浪骑士
│   └── 溃兵
├── 宗教 / 学者（特殊向）
│   ├── 修士 / 托钵僧
│   ├── 朝圣者
│   └── 书记员 / 抄经士
└── 法外之徒（特殊开局）
    ├── 盗猎者
    ├── 盗贼
    └── 逃兵 / 流寇
```

---

## 三、职业详表

### 3.1 底层出身

#### 农奴 / 逃亡农民（Serf / Runaway Peasant）

| 项目 | 内容 |
|------|------|
| 一句话 | 一生在领主的田里劳作，灾难来了，你逃了。一无所有，但你的手能种出粮食。 |
| 难度 | ★★★★★（最高） |
| 技能 | Survival +2, Cooking +1, Construction +1, Trapping +1 |
| 装备 | linen shirt, rough wool tunic, braies, footwraps, rope belt, 可能有 pitchfork / wood axe / grain flail 之一 |
| 特质建议 | 坚韧、耐饿、不识字的、低社会地位 |
| 开局情景 | 一片荒野，最近的村子烧成了废墟 |

#### 乞丐 / 游民（Beggar / Vagabond）

| 项目 | 内容 |
|------|------|
| 一句话 | 什么都没有。你的同伴昨天冻死在路边了。 |
| 难度 | ★★★★★+ |
| 技能 | Speech +1, Survival +1（城市求生） |
| 装备 | 破烂 linen shirt, 破斗篷的一角, 可能有个破碗 |
| 开局情景 | 路边。温度在下降。你没有鞋子。 |

#### 麻风幸存者（Plague Survivor）

| 项目 | 内容 |
|------|------|
| 一句话 | 那场瘟疫杀了所有人。你活下来了，但身体被标记了。 |
| 难度 | ★★★★ |
| 技能 | First Aid +2, Survival +1 |
| 装备 | hood（遮脸）, 破布裹身, wooden cup |
| 特质 | 免疫力增强、面孔可怕（NPC 畏惧）、慢性疾病 |
| 特色 | 对疾病有极高抗性，但起始健康极差、社交被排斥 |

#### 苦修者 / 鞭笞派（Flagellant）

| 项目 | 内容 |
|------|------|
| 一句话 | 你相信这场灾难是神的惩罚。你用痛苦换取救赎。 |
| 难度 | ★★★★ |
| 技能 | Unarmed +1, Survival +1 |
| 装备 | 粗羊毛袍子, 绳带, 无鞋, 可能有一根鞭子或苦修棍 |
| 特质 | 高痛苦耐受、宗教狂热（有时获得士气加成）、理智不稳定 |

---

### 3.2 手艺人与市民

#### 铁匠（Blacksmith）

| 项目 | 内容 |
|------|------|
| 一句话 | 你的铁砧被劫掠了，但手艺还在骨子里。 |
| 难度 | ★★★ |
| 技能 | Smithing +3, Bashing +1, Construction +1 |
| 装备 | leather apron, wool tunic, linen shirt, hose, ankle boots + smithing hammer（可作武器） |
| 特质 | 强壮、耐久 |
| 独特价值 | 能修金属装备、能从废铁中敲出东西 |

#### 木匠（Carpenter）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Fabrication +3, Construction +2 |
| 装备 | linen shirt, wool tunic, leather apron, hose, turnshoes + wood axe / hatchet（可作武器） |
| 独特价值 | 搭设庇护所、制造木柄、修理长柄武器 |

#### 鞣皮匠（Tanner）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Fabrication +3, Tailoring +1, Survival +1 |
| 装备 | leather apron, work gloves, wool tunic, hose, ankle boots + skinning knife |
| 独特价值 | 处理猎物皮毛、制作/修理皮甲 |

#### 裁缝（Tailor）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Tailoring +3, Bartering +1 |
| 装备 | linen shirt, doublet, hose, ankle boots + sewing kit (needle + thread), shears |
| 独特价值 | 制作/修理布料和 gambeson；修理衣物不需要工具台 |

#### 屠夫（Butcher）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Cutting +2, Cooking +1, Survival +1 |
| 装备 | leather apron, wool tunic, linen shirt, hose, ankle boots + butcher's cleaver（砍刀）+ butcher's knife |
| 独特价值 | 屠宰动物出肉率更高；对血液和内脏不敏感 |

#### 磨坊主（Miller）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Cooking +2, Bartering +2 |
| 装备 | linen shirt, linen tunic, wool cloak, hose, turnshoes + stout stick, grain sack |
| 特质 | 精明（交易加成）、被怀疑（磨坊主常被指扣分量） |
| 独特价值 | 碾谷知识；开局有一袋面粉 |

#### 车夫（Carter / Wagoner）

| 项目 | 内容 |
|------|------|
| 难度 | ★★ |
| 技能 | Riding +2, Survival +1, Speech +1 |
| 装备 | sturdy wool tunic, chaperon hood, hose, ankle boots + whip, leather belt + water skin |
| 特殊 | 开局可能有匹骡子或一匹老马 |
| 独特价值 | 罕见的"开局就有坐骑"的职业 |

#### 草药师（Herbalist）

| 项目 | 内容 |
|------|------|
| 难度 | ★★ |
| 技能 | Survival +3, First Aid +2 |
| 装备 | linen chemise, wool kirtle / tunic, hood, turnshoes + herb pouch (开局含少量草药), mortar & pestle |
| 独特价值 | 能辨别和采集药用植物；能做基础药膏和止痛药 |

---

### 3.3 武人出身

#### 民兵（Militiaman）

| 项目 | 内容 |
|------|------|
| 一句话 | 镇上的钟声响了，你和邻居们扛起家伙。现在镇没了，邻居也没了。 |
| 难度 | ★★ |
| 技能 | Piercing +2, Bashing +1, Dodge +1 |
| 装备 | gambeson, kettle hat, leather gloves, hose, ankle boots + spear, 可能有 simple wooden shield |
| 定位 | 入门级武人，均衡但无特长 |

#### 猎人（Hunter）

| 项目 | 内容 |
|------|------|
| 一句话 | 你靠森林活着，森林从不对你撒谎——不像人。 |
| 难度 | ★★ |
| 技能 | Archery +3, Survival +2, Trapping +2, Cutting +1 |
| 装备 | wool hood, leather tunic, hose, ankle boots + shortbow + 箭 ×20 + seax / hunting knife |
| 特质 | 夜视、方向感、潜行加成 |
| 独特价值 | 远程 + 生存复合，开局不依赖城镇 |

#### 长弓手（Longbowman）

| 项目 | 内容 |
|------|------|
| 一句话 | 你从七岁开始拉弓。你的脊柱是弯的，但你的箭是直的。 |
| 难度 | ★★ |
| 技能 | Archery +4, Cutting +1, Survival +1 |
| 装备 | gambeson (轻), bascinet, hose, ankle boots + longbow + bodkin arrows ×30 + arming sword / falchion + bollock dagger |
| 特质 | 极强壮（长弓拉力 100–180 lb）、骨骼变形（负面社会影响） |
| 限制 | 离开英格兰/威尔士语境则稀有 |

#### 弩手（Crossbowman）

| 项目 | 内容 |
|------|------|
| 难度 | ★★ |
| 技能 | Archery +3, Cutting +1, Dodge +1 |
| 装备 | gambeson, kettle hat, hose, ankle boots + light crossbow + bolts ×20 + falchion + pavise（大盾，若开局持有则负重大） |
| 区别于长弓手 | 不需要极强壮、装填慢但命中稳、破甲力强 |
| 特质 | 耐心、沉着 |

#### 步兵 / 下级佣兵（Footman / Low Mercenary）

| 项目 | 内容 |
|------|------|
| 难度 | ★ |
| 技能 | Cutting +2, Bashing +2, Dodge +2 |
| 装备 | gambeson + mail hauberk, bascinet (无 visor), hose, ankle boots + arming sword / battle axe / mace 之一 + heater shield |
| 定位 | "标准中世纪战士"，上手门槛最低的战斗开局 |

#### 流浪骑士（Hedge Knight）

| 项目 | 内容 |
|------|------|
| 一句话 | 你曾经有封地——或至少有过誓言。现在你只剩一匹马和一身甲。 |
| 难度 | ★ |
| 技能 | Cutting +3, Piercing +2, Riding +3, Bashing +2 |
| 装备 | 全 gambeson + mail hauberk + brigandine, bascinet with hounskull visor, hourglass gauntlets, plate legs, 带马刺的靴 + longsword + rondel dagger + heater shield |
| 特殊 | 开局有**一匹战马**（destrier / courser），是本模组含金量最高的出身之一 |
| 代价 | 马需要饲料、需要照看，目标大，招人眼红 |

#### 溃兵（Deserter）

| 项目 | 内容 |
|------|------|
| 一句话 | 那场仗打输了，你跑了。现在你穿着偷来的军装，不知道谁在追你。 |
| 难度 | ★★ |
| 技能 | Cutting +2, Piercing +1, Dodge +1, Survival +1 |
| 装备 | 部分盔甲（破烂 gambeson + 可能缺件的 mail / plate），bascinet（凹痕）, arming sword 或 billhook + 少量军需品 |
| 特质 | 被一方势力通缉、开局可能在荒野被追杀 |

---

### 3.4 宗教 / 学者

#### 修士 / 托钵僧（Monk / Friar）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★ |
| 技能 | Literacy +3, Survival +1, Speech +1 |
| 装备 | 粗羊毛修道袍, 绳带, sandals 或赤脚, wooden cross, prayer book（可阅读）, scribe tools |
| 特质 | 识字（稀有！）、戒律（不能吃肉/饮酒→士气惩罚但宗教加成） |
| 独特价值 | 极少数能读拉丁文/古书的职业；宗教物品对低魔元素有潜在作用 |

#### 朝圣者（Pilgrim）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★★ |
| 技能 | Survival +1, Speech +1 |
| 装备 | 粗羊毛斗篷, 宽檐帽, wool tunic, hose, turnshoes + walking staff + scrip bag + 贝壳标志（朝圣证） |
| 特质 | 虔诚（独自祈祷有士气加成）、轻装上阵 |

#### 书记员 / 抄经士（Scribe）

| 项目 | 内容 |
|------|------|
| 难度 | ★★★★ |
| 技能 | Literacy +4, Bartering +1 |
| 装备 | linen shirt, wool tunic, chaperon, hose, turnshoes + quill & ink, parchment, 可能有一本手抄本 |
| 特质 | 极近视（读书太多）、柔弱、高智力 |
| 独特价值 | 文盲世界里能读能写的人 = 能解读地图、配方、古卷 |

---

### 3.5 法外之徒

#### 盗猎者（Poacher）

| 项目 | 内容 |
|------|------|
| 难度 | ★★ |
| 技能 | Archery +2, Trapping +3, Survival +3, Cutting +1 |
| 装备 | wool hood（深色）, leather tunic（暗色）, hose, soft turnshoes（静音） + shortbow + 箭 ×15 + skinning knife + 捕兽夹 ×2 |
| 特质 | 夜行、潜行、被当地领主通缉 |
| 独特价值 | 潜行 + 狩猎复合，擅长在无人知晓的情况下在森林里活着 |

#### 盗贼（Thief）

| 项目 | 内容 |
|------|------|
| 难度 | ★★ |
| 技能 | Dodge +2, Cutting +1, Speech +1, Fabrication +1 |
| 装备 | dark wool tunic, hood（遮脸）, soft turnshoes + baselard / bollock dagger + small bag |
| 特质 | 灵巧、惯偷、夜间视觉 |
| 独特价值 | 潜行好手；Fabrication 涵盖撬锁/拆陷阱等巧手能力 |

#### 流寇 / 强盗（Bandit）

| 项目 | 内容 |
|------|------|
| 难度 | ★ |
| 技能 | Cutting +2, Bashing +1, Throwing +1, Dodge +1 |
| 装备 | 捡来的杂牌装备：gambeson（补丁）, kettle hat 或其他杂盔, hose, ankle boots + falchion + hand axe + 可能有个 sling |
| 特质 | 暴力倾向、被悬赏 |
| 特色 | 开局可能带一小袋抢来的东西（随机杂物 + 硬币） |

---

## 四、推荐初始出身（新手友好排序）

| 排名 | 职业 | 理由 |
|------|------|------|
| 1 | 步兵 | 战斗强、装甲好、上手最省心 |
| 2 | 猎人 | 能远程能生存、不依赖城镇 |
| 3 | 草药师 | 自给自足、开局有药 |
| 4 | 民兵 | 均衡战斗、比步兵轻便 |
| 5 | 车夫 | 可能有坐骑、生存难度低 |
| 6 | 铁匠 | 能修能造、力量高 |
| 7 | 屠夫 | 肉资源充裕 |
| 8 | 盗猎者 | 生存+潜行、森林之王 |
| 9 | 流浪骑士 | 战斗力天花板但要管马 |
| 10 | 农奴 | 最难——但你一定能种出吃的 |

---

## 五、设计注记

### 5.1 技能上限原则
- 初始最高技能不超过 **4 级**（长弓手、书记员为标杆）
- 3 级是"以此为生"的专业门槛
- 2 级是"受过训练"的水平
- 1 级是"会一点"的副业水平
- 空白 ≠ 0 级——空白意味着从未接触

### 5.2 技能合并原则
- **盾牌**不单独设技能：盾牌格挡由 Dodge 抽象，盾牌击打由 Bashing 抽象
- **木工 / 皮工**不拆分：统一由 Fabrication 覆盖，与 Tailoring 的边界是"软材料 / 硬材料"
- **草药**不独立：野外采药由 Survival 覆盖，制药由 Fabrication（捣药）或 Cooking（煎药）覆盖
- **宗教**不独立：宗教行为通过特质（虔诚/戒律）+ Speech（布道）体现
- 仅新增 **Riding / Smithing / Literacy** 三个无可替代的技能

### 5.3 识字是稀有资源
中世纪末期（约 1400），平民识字率可能不足 5%。只有修士、书记员、部分贵族能读拉丁文。这意味着：

- **配方/蓝图** 对文盲角色不可读（需要有"识字"特质或找 NPC 帮你读）
- **宗教物品/古籍** 的价值翻倍——因为它们的内容无法被大多数角色获取
- 书记员一开始极弱，但一旦找到**炼金配方或稀有古卷**，立刻翻身

### 5.4 Riding（骑乘）的定位
- 替换 Driving 技能
- 影响：马匹操控、马车驾驶、马上战斗（lance / sword 的冲击力）
- 马不是汽车：马会受惊、会饿、会生病、会被野兽咬死
- 开局有马（车夫 / 流浪骑士）是极大的优势——也是极大的负担

---

## 六、待定

1. **特质系统**：识字/不识字、社会地位、宗教归属等特质如何映射到 CDDA 的 trait 系统
2. **NPC 职业**：本表是否同样用于生成 NPC 遭遇
3. **开局情景（Scenario）**：每个职业是否需要独立的开局地图/事件

---

> 当前策划案积累：001 世界观 → 002 盔甲 → 003 低端衣物 → 004 武器 → 005 职业与技能
