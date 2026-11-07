# CDDA 本地化与国际化 (i18n) 系统调研

> 核验基点：CDDA `0.H-branch`，提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`（Medieval 改造前的维护分支快照，并非最初的 0.H 发布标签）。下述源码路径均以该提交为准。

> 记录 CDDA 官方源码中本地化系统的架构、核心机制、JSON 文本提取工作流以及对中世纪 Mod (Medieval) 本地化的启示。

---

## 1. 整体架构与运行机制

CDDA 的本地化系统采用统一的 **Gettext** 标准机制。无论是 C++ 源码中的硬编码文案，还是 JSON 数据文件中的可配置文本（如物品名称、描述、对话等），都经过统一的翻译管道提取，并最终由游戏内置的翻译管理器在运行时统一翻译和缓存。

其核心数据流动拓扑如下：

```mermaid
graph TD
    A[C++ 源码 src/] -->|xgettext 扫描| B[gui.pot 模板]
    C[JSON 数据 data/] -->|extract_json_strings.py| D[json.pot 模板]
    B & D -->|msgcat 合并| E[cataclysm-dda.pot]
    E -->|翻译与维护| F[各语言 .po 源文件]
    F -->|msgfmt 编译| G[cataclysm-dda.mo 二进制]
    G -->|游戏启动加载| H[TranslationManager 运行时]
    H -->|C++ _ / translation| I[本地化文本输出]
```

---

## 2. C++ 核心机制

### 2.1 延迟翻译容器 `class translation`
在 CDDA 中，为了避免静态初始化时语言选项尚未加载就进行翻译，供玩家显示、且加载代码声明为可翻译文本的 JSON 属性在反序列化后并不是直接存储为普通的 `std::string`，而是存储为 `class translation`（定义于 translation.h）。

该类支持以下核心功能：
- **延迟翻译**：在需要显示给玩家时（例如 UI 渲染），才调用 `.translated()` 方法动态获取当前语言的翻译文本。
- **内置缓存**：内部维护缓存，只有当语言版本号改变（`current_language_version` 递增）或复数数量参数发生变化时，才会重新查找并刷新翻译，性能极高。
- **单复数支持**：包含可选的 `raw_pl`（复数原始字符串），在翻译时支持传入 `num`（数量）以调用 `n_gettext`。
- **反序列化形式**：
  `class translation` 在 JSON 中支持两种定义方式，极具灵活性：
  1. **简单字符串**：直接定义文本；只有该字段/translation 实例启用复数支持时才推导复数，不是所有字符串自动加 s。运行时 `translation::deserialize` 和提取器各自按字段规则处理；不规则复数应显式写出。
     ```json
     "name": "broadsword"
     ```
  2. **复杂 JSON 对象**：显式提供翻译上下文（`ctxt`）、单数（`str`）、复数（`str_pl`）或单复数同形（`str_sp`），并支持为翻译者提供注释注释（`//~`）。
     ```json
     "name": {
         "//~": "A heavy, double-edged medieval sword.",
         "ctxt": "weapon",
         "str": "broadsword",
         "str_pl": "broadswords"
     }
     ```

### 2.2 内置的翻译管理器 `TranslationManager`
与许多需要动态链接外部 `libintl.dll` 的游戏不同，CDDA 在 translation_manager_impl.cpp 中**自主实现了一套轻量级二进制 `.mo` 文件解析器**。

其关键技术细节如下：
- **多文档融合**：通过 `LoadDocuments` 可以同时加载并解析多个 `.mo` 翻译文件，索引各文档的原文条目，并通过 djb2 风格的 `Hash` 算法对原始字符串哈希化，在内存中构建极其快速的 `std::unordered_map` 哈希表查找结构。
- **Mod 翻译扫描范围**：`ScanTranslationDocuments` 递归扫描 `PATH_INFO::user_moddir()` 中的 `LC_MESSAGES` 寻找 `.mo`，另扫描 `locale_dir()` 下的核心 `cataclysm-dda.mo`。此基点不额外扫描 `PATH_INFO::moddir()`（游戏 `data/mods`）！扫描也不按当前世界启用的模组列表过滤。Medieval 后来加入的 data/mods 扫描扩展不是原版能力。
- **同键优先级**：`LoadDocuments` 按文件顺序索引，`LookupString` 返回首个相同原文；用户模组目录先于核心目录加入。不能依赖未声明的文件间遍历顺序实现稳定覆盖，也不是按模组启用顺序覆盖。
- **上下文拼接（Contextual Query）**：在翻译带上下文（`msgctxt`）的文本时，它利用了 Gettext 的规范，将 context 字符串、`"\004"`（ASCII 传输结束符，即 `\x04`）以及 raw message 字符串拼接为单个查询键进行哈希检索。

---

## 3. 本地化提取工作流 (Extraction Pipeline)

整个项目的本地化翻译模板生成由脚本 update_pot.sh 统一驱动，分为以下三步：

### Step 1: 源码字符串提取
利用 GNU gettext 工具链的 `xgettext` 扫描 `src/` 下的所有 C++ 源文件，提取带有 `_()`, `pgettext()`, `n_gettext()`, `npgettext()` 以及各种 `translation` 构造函数标志的文本，输出为 `lang/po/gui.pot` 模板。

### Step 2: JSON 字符串精密提取
调用 Python 脚本 extract_json_strings.py 递归扫描 `data/`，但排除 `data/mods/TEST_DATA` 和脚本列出的测试/特殊文件。
- **按 JSON 类型分派的解析器**：该提取器的核心位于 `lang/string_extractor/`。它在 `parser.py` 中维护了一个大字典，把 JSON 的 `type` 字段（如 `"item"`, `"recipe"`, `"terrain"`, `"monster"` 等）映射到 `parsers/` 目录下对应的专门解析子模块。
- **字段级精确提取**：例如在 `parsers/generic.py` 中，解析器仅对 `"name"`, `"description"`, `"variants"`, `"pocket_data"` 等属性值进行提取，并自动附带类型与物品名作为翻译注释，而忽略程序内部属性（如 `"weight"`, `"volume"`），避免模板污染。
- 生成 `lang/po/json.pot` 模板。

### Step 3: 合并与编译
- 使用 `msgcat` 合并 `gui.pot` 和 `json.pot` 模板，生成总模板 `lang/po/cataclysm-dda.pot`。
- 翻译人员对 `.pot` 提取出的文本在各语言 `.po` 文件中进行翻译（如 `lang/po/zh_CN.po`）。
- 最终运行 `compile_mo.sh`，使用 `msgfmt` 工具将各 `.po` 编译为二进制的 `.mo` 文件，存放于 `lang/mo/{lang}/LC_MESSAGES/cataclysm-dda.mo` 中。

---

## 4. 对中世纪 Mod (Medieval) 的本地化启示与策略选择

中世纪 Mod 作为独立 Mod 存放在 `data/mods/Medieval` 中。随着我们不断扩充中世纪的盔甲、武器、材料、聚落、NPC 与职业，本地化有以下三种可行策略：

### 策略 A：全中文直接硬编码入 JSON (快速/粗暴)
* **做法**：在 `data/mods/Medieval/` 下的所有 JSON 属性值中直接书写中文字符（如 `"name": "布里根丁板甲衣"`）。
* **优点**：无需任何翻译编译管道，即写即用，开发和调试阶段体验极爽。
* **缺点**：丧失了多语言切换支持。如果未来有英文或其他语言玩家，他们看到的依然是中文。

### 策略 B：合并至官方翻译大 PO 文件 (标准/合规)
* **做法**：我们正常用英文编写 JSON 属性，运行 `update_pot.sh` 脚本，脚本扫描 `data/`（带明确排除项），由已支持的字段解析器提取中世纪 Mod 文本至项目主 `cataclysm-dda.pot`。然后我们将其合并至 `lang/po/zh_CN.po` 并重新用 `compile_mo.sh` 编译核心 `.mo` 文件。
* **优点**：复用项目现有的主词库流程，翻译资源高度统一。
* **缺点**：`zh_CN.po` 极其庞大（体积随版本变化），直接编辑或频繁合并在开发阶段比较繁琐。

### 策略 C：独立 Mod 词库（需匹配原版扫描路径）
* **做法**：由于 `TranslationManager` 支持动态扫描 Mod 目录下的 `LC_MESSAGES` 文件夹，我们可以：
  1. 仿照官方提取脚本，写一个只针对 `data/mods/Medieval` 目录的 Python 提取命令，生成 `Medieval.pot`。
  2. 建立小型的 `Medieval_zh_CN.po`。
  3. 用 `msgfmt` 编译出 `Medieval.mo`，并放入用户模组目录内的 `LC_MESSAGES` 路径。若要随游戏 `data/mods/Medieval` 分发，需要另行调整扫描入口，或改用项目主词库；不能仅放文件便假设此基点会加载。
* **优点**：完全模块化，Medieval 的翻译与核心翻译解耦，po 文件小巧玲珑，便于协作与增量翻译。
* **限制**：扫描的是用户模组根目录，不是当前世界启用列表；词库冲突和安装位置须按实际路径处理。

## 源码核对入口

`src/translation.cpp`：`deserialize`、`translated`；`src/translation_manager_impl.cpp`：`ScanTranslationDocuments`、`LoadDocuments`、`LookupString`；`lang/update_pot.sh`、`lang/compile_mo.sh`。策略部分属于项目选择，使用翻译的构建还需启用 `LOCALIZE`。
