# 项目文档

## 阅读与维护

长程上下文由文档维护，归档范围和规则见根目录 [AGENTS.md](../AGENTS.md)。按主题标题更新完整章节，不追加时间线或修订日志。设计中的候选数值不表示已经实现，也不表示所有旧讨论均已重新确认。

## 当前目录

- `design/`：游戏设计，技术接口、数据语法和实施步骤已移出。
- `process/`：当前为空。实际开始JSON或代码实现后，分别创建 `json/<设计案同名文件>.md` 和 `code/<设计案同名文件>.md`，不预建占位。
- `vanilla/`：以 `6dae8435e8` 为基点勘正的原版机制调研，JSON与C++不分目录。
- `archive/technical/`：旧技术方案和过程摘要，只供重新设计时查阅，不继承为当前进度。旧done没有可迁入文件，不保留done目录。

## 单向依赖

游戏设计是两类process的需求来源。每份process注明对应design，维护该类别的技术设计、实际完成内容、未完成事项和必要验证事实。design不引用process，不随代码或JSON变动自动改变。

## 历史来源

旧实现与原始旧文档保存在 `archive/medieval-before-redo` 分支，原路径为 `msvc-full-features/.qoder/docs/`。其中原版调研的勘正内容已恢复到当前vanilla目录。

旧分支独有的远程伤害方案迁入 `design09_3`，相关公式与工具研究留在archive。怪物行动影响仍为 `design09_2`，远程部位瞄准整理为 `design09_4`。

## 游戏设计主题

- [项目内容边界](design/design00-内容边界.md)
- [策划案 001：世界观与威胁体系](design/design01-世界观.md)
- [策划案 002：盔甲体系（14 世纪末 ~ 15 世纪初过渡期）](design/design02-盔甲.md)
- [策划案 002_1：布里根丁与板甲衣细分](design/design02_1-布里根丁与板甲衣细分.md)
- [策划案 003：低端衣物与日常装备（平民层）](design/design03-日常衣物.md)
- [策划案 004：武器体系（14 世纪末 ~ 15 世纪初）](design/design04-武器.md)
- [策划案 004_1：装备 Quality 体系](design/design04_1-quality体系.md)
- [策划案 005：开局职业与技能映射](design/design05-职业.md)
- [策划案 006：中世纪聚落与建筑体系](design/design06-建筑.md)
- [策划案 007：冒险者工会](design/design07-冒险者工会.md)
- [敌人与生态体系](design/design08-敌人.md)
- [策划案 008：野怪 NPC 体系（一）—— 强盗](design/design08_1-野怪_强盗.md)
- [策划案 008_2：野怪体系（二）—— 野生动物](design/design08_2-野怪_野生动物.md)
- [策划案 008_3：野怪体系（三）—— 奇幻生物](design/design08_3-野怪_奇幻.md)
- [精确近战：手动技艺与部位选择](design/design09-战斗系统重置.md)
- [部位血量与伤害扩散](design/design09_1-部位血量系统.md)
- [怪物部位受伤对行动的影响](design/design09_2-怪物部位行动影响.md)
- [远程伤害与弓弩平衡](design/design09_3-远程伤害系统.md)
- [远程部位瞄准](design/design09_4-远程部位瞄准.md)
