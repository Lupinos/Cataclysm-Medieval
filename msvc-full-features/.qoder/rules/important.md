---
trigger: always_on
alwaysApply: true
---
用户如果提到important文档，就是指本文档

# 项目文档自动归纳规则

你需要在每次对话中，主动将项目中发现的任何有价值信息归纳整理到 `.qoder/docs/` 目录中，并维护文档索引。

## docs/ 目录结构

```
docs/
├── vanilla/     # CDDA 原版系统调研（纯现状分析）
├── design/      # Medieval Mod 策划案（未来规划与方案设计）
└── process/     # 实现进度跟踪（已完成与待完成的任务状态）
```

- **vanilla/**：调研 CDDA 现有机制时写入，不混入中世纪策划
- **design/**：中世纪改造的方案设计，每个策划案一个文件
- **process/**：每次完成/推进改造任务后，必须更新对应的 process 文档进度

## 自动执行要求

自动归纳任务覆盖两个目录，**无需用户主动提出**：

### vanilla/ — 调研发现自动记录

当你调研 CDDA C++ 源码或 JSON 数据时，如果遇到了重要的类、函数、模块设计、实现机制、架构模式等信息，应主动归纳到 `docs/vanilla/`。

### process/ — 任务完成自动更新

每次完成或推进中世纪改造任务后，**必须**更新对应的 `docs/process/` 文档进度（勾选 checklist、更新完成状态、补充新发现的问题）。

---

### design/ — 技能驱动，非自动

策划案**不是自动任务**。仅当用户明确提出策划需求时，通过 `medieval-design` Skill 交互式澄清后，才写入 `docs/design/`。你不要在用户未要求的情况下自行撰写策划案。
## vanilla/ 归纳标准

以下 CDDA 原版信息应在调研时记录到 `docs/vanilla/`：
1. **关键类/接口/结构体**：核心业务类、重要抽象、关键数据结构等，说明其职责和所在文件。
2. **重要实现机制**：如事件系统、序列化机制、数据流处理、插件架构、工厂模式等核心设计。
3. **模块职责划分**：各个模块（静态库/子项目）的核心功能和模块间依赖关系。
4. **配置和约定**：构建配置、编码约定、命名规范等。
5. **关键依赖**：项目依赖的第三方库及其用途。

## 文档组织方式

- 针对不同的主题建立独立的 `.md` 文件，按类型存放在 `.qoder/docs/` 的对应子目录下：
  - **CDDA 原版调研** → `docs/vanilla/<topic>.md`
  - **Medieval 策划案** → `docs/design/<topic>.md`
  - **实现进度** → `docs/process/<topic>.md`
- 文件名应简洁有意义，如 `json_data_system.md`、`medieval_city_design.md`、`modern_content_removal.md` 等。
- 每个文档文件内部应有清晰的结构：模块概述、关键类、核心机制、依赖关系等。
- 修改每个文档时，可以修改错误的、已过时的信息
- Medieval本体在data\mods\Medieval

## 索引维护

- 所有文档文件的索引写入到 `.qoder/rules/doc_index.md` 中。
- 索引格式应包含：模块名称、文档文件路径、简要说明（一句话即可）。
- 新建或更新文档后，务必同步更新索引。
- 每次对话开始时，你应该会自动包含 `doc_index.md` 文档，避免重复调研。

## 回合结束自检清单

每轮对话结束前，必须自检以下几项，未完成的立即补做：

- [ ] **vanilla/**：本轮是否调研了 CDDA 源码/JSON？如有新发现，是否已写入 `docs/vanilla/`？
- [ ] **process/**：本轮是否完成/推进了中世纪改造任务？是否已更新 `docs/process/` 对应文档的进度？
- [ ] **doc_index**：本轮是否新建/修改了 `docs/` 下任何文件？是否已同步 `.qoder/rules/doc_index.md`？
- [ ] **skill/**：本轮是否发现了skill相关的问题，可以改进的部分写进去。

---

# 项目环境与工具能力矩阵

## 项目结构

- **工作区根目录**：`E:\Cataclysm-Medieval\msvc-full-features\`（MSVC 构建配置层）
- **C++ 源码**：`E:\Cataclysm-Medieval\src\`（805 项）
- **测试代码**：`E:\Cataclysm-Medieval\tests\`（226 项）
- **工具代码**：`E:\Cataclysm-Medieval\tools\`（39 项）
- **游戏数据**：`E:\Cataclysm-Medieval\data\`
- 所有目录均支持 Write / Edit / DeleteFile 直接操作，无跨工作区限制

## 各工具能力表

| 工具 | 工作区内 | 跨边界(父目录源码) | 说明 |
|------|---------|-------------------|------|
| `list_dir` | ✅ | ✅ 可用绝对路径 | 列出目录内容 |
| `read_file` | ✅ | ✅ 可用绝对路径 | 阅读文件，自动返回≥200行上下文 |
| `search_file` | ✅ | ✅ 指定父目录绝对路径 | 查找文件，支持 glob 模式 |
| `grep_code` | ✅ | ❌ | 正则搜索文件内容，仅限工作区 |
| `search_codebase` | ⚠️ | ❌ | 语义搜索，工作区内可用但噪声较多；不支持 `target_directories` 跨工作区 |
| `search_symbol` | ❌ | ❌ | 符号搜索，工作区无 C++ 源码可索引，完全不可用 |
| `run_in_terminal` | ✅ | ✅ | PowerShell 环境；后台模式最长 30 分钟 |
| `search_web` | ✅ | ✅ | 网络搜索，不依赖工作区 |
| `get_problems` | ✅ | ⚠️ | 可检查文件编译问题，路径不存在时静默返回 |

## 调研源码的实操策略

由于 `search_symbol` 和 `search_codebase` 无法索引 C++ 源码，调研 `src/` 下代码时：

1. 用 `search_file` + 父目录绝对路径定位目标文件（如 `search_file path=E:\Cataclysm-Medieval\src query=calendar*`）
2. 用 `read_file` + 绝对路径阅读内容
3. 手动跟踪 `#include` 依赖链跳转到关联文件
4. 用 `grep_code` 搜索工作区内的 `.vcxproj`/`.props`/`.json` 了解模块结构和构建配置
5. 项目文档（`.qoder/docs/vanilla/`、`.qoder/docs/design/`）中对各模块的调研记录可减少重复劳动

## 已知限制

- 联接/符号链接（`mklink /J`）对 `read_file` 和 `list_dir` 透明，但对 `search_file`/`grep_code`/`search_symbol`/`search_codebase` 无效——这些索引工具明确跳过联接目标
- `grep_code` 不支持 `.cs`（C#）源文件
- `run_in_terminal` 后台模式上限 30 分钟
- `Write` / `Edit` / `DeleteFile`：所有 `E:\Cataclysm-Medieval\` 下目录均可直接操作，无限制。
- **严禁在 `run_in_terminal` 中发送多行命令（含 Here-String `@'...'@`、`@"..."@`、`>>` 重定向）。** 持久 Shell 的历史残留会把 Here-String 起始标记吞掉，导致 Shell stdin 缓冲区永久损坏，后续所有命令全部失败。一旦腐蚀发生，必须重启 IDE。
