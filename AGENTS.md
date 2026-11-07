# 项目协作约定

## 最小实现

- 默认只做满足当前需求的最小必要改动。禁止添加无关的防御性检查、保护逻辑、兜底回退、兼容层、抽象或配置开关。
- 不顺手重构，不为假设中的未来需求增加复杂度。验证采用能确认本次工作有效的最简单方式。

## 长程上下文与文档

长程上下文基于文档维护。以下工作归档：**架构调研、接口分析、机制推导、设计方案、开发流程/工具链沉淀。Bug 排查与 Bug 修复不入档。**

- 开始相关任务时先读 `docs/README.md`，再读对应主题；不默认重读全部历史。
- 文档以标题界定的主题章节为维护单位。更新时直接重写完整章节，不追加日期增量、补丁说明或聊天流水；旧文档的矛盾点可以直接删除。
- `docs/design/`：只写游戏玩法目标、规则、体验、内容和数值方案，不讨论技术设计、代码接口、JSON语法、存储结构或实施步骤。
- `docs/process/`：实际开始实现后才创建。每份design可分别对应 `process/json/<同名文件>.md`（JSON编写）和 `process/code/<同名文件>.md`（代码实现）。两类process分别以对应design为上游需求，单向依赖；可引用原版调研与源码作为依据，design不依赖process，技术实现不得反向改写设计规则。
- 技术设计、接口、数据组织、真实实现进度与验证事实属于对应process。只记录当前分支状态，不沿用旧完成标记，不预建占位process。
- `docs/vanilla/`：原版机制调研，JSON与C++统一归类，注明基点和真实源码依据，区分原版事实、项目改造和设计推演。
- `docs/archive/`：旧过程与技术方案参考，不是当前实现进度，不默认注入上下文。完整旧稿在 `archive/medieval-before-redo` 分支；不建立done目录。

## 编辑与文档同步

- 代码编辑后核对对应 `process/code/`，JSON编辑后核对对应 `process/json/`。只做Bug排查或修复时不创建、更新归档文档。
- 形成需要归档的技术设计或实现事实后才更新相应完整章节，没有对应设计案时先确认归属，不机械生成文档。
- 优先使用云端事件钩子；也允许能够实际触发云端agent补写process的本地钩子，不以本地打印提醒代替。接入前用临时项目验证编辑事件到文档写回，源码与design不得由文档agent修改。

## 基线与云端验证

重做基点：CDDA `0.H-branch` 的 `6dae8435e804bc11dd85baa21954ba6297e7841f`。旧Medieval代码和JSON未迁入。

首次准备云端工具链运行 `bash tools/setup-cloud.sh`；日常使用下列增量编译和最小测试入口。

```bash
cd /workspace/Cataclysm-Medieval
/workspace/cataclysm-env/venv/bin/cmake --build /workspace/cataclysm-env/build --target cataclysm cata_test --parallel 5
/workspace/cataclysm-env/build/tests/cata_test doors_should_be_able_to_open_and_close --user-dir=/workspace/cataclysm-env/redo-test-user
```

非图形构建，关闭声音、本地化与可选JSON格式化工具；测试不加载Medieval。
