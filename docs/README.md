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

## Git提交与文档同步

开始代码或JSON任务前，在当前检出中运行：

```bash
bash tools/setup-hooks.sh
```

该脚本设置当前仓库的 `core.hooksPath=.githooks`，启用 `.githooks/commit-msg`；`tools/setup-cloud.sh` 也会调用它。钩子文件随Git保存，但仓库配置不会随克隆迁移，所以新检出仍需执行安装。安装只需要Git和Bash，无需独立Codex CLI认证或常驻进程。

钩子检查暂存区中 `src/`、`data/`、`tests/`、`tools/`、`build-scripts/`、`.githooks/` 及根目录构建入口的代码与JSON改动，包括删除。代码要求同时暂存 `docs/process/code/*.md` 的新增或修改，JSON要求 `docs/process/json/*.md`；两类改动同时存在时分别核对。删除process文件不能替代更新。

遗漏时提交失败，提醒文字随Git命令结果返回给当前agent。当前agent根据实际改动查阅design、更新同名process的完整章节，暂存后重试。脚本不生成文档，也不验证内容语义；即使文件检查通过，agent仍须核对设计归属、实现事实和验证结果。

纯Bug排查与修复不入档。工具链知识在本README维护；没有新的可归档事实也不制造占位文档。符合这些规则时，在提交说明末尾以空行隔开，给出具体理由，例如：

```text
fix: correct door state handling

Process-Docs: skip 纯 Bug 修复，无新增设计或实现方案
```

此说明是agent对无需更新process的明确判断，不是取消文档职责。正常提交必须执行钩子，不通过 `--no-verify`、禁用钩子或API提交绕过。钩子只在执行提交的开发机上运行，不会唤醒已结束的对话。

旧的 `tools/watch-process.cjs` 已移除。旧开发机若仍有此前启动的监听进程，核实进程身份后停止；不再启动监听器或独立文档agent。

## 云端工具链

`bash tools/setup-cloud.sh` 准备隔离的构建依赖并编译游戏和测试程序。依赖、构建缓存和运行日志保存在仓库外的 `/workspace/cataclysm-env/`，不提交到Git。日常增量编译及最小测试入口见根目录AGENTS.md。

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
