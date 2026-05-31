---
name: medieval-i18n
description: Automated independent localization workflow for Cataclysm-Medieval. Extracts translatable strings from JSON, merges them into the zh_CN.po catalog (the single source of truth), translates them dynamically using AI (prepending "中世纪" to all item names for testing), and compiles the catalog into the binary Medieval.mo package. Handles file lockouts during active gameplay.
---

# 中世纪 Mod 独立本地化与自动编译工作流 (medieval-i18n)

## 触发条件

当用户提出以下类型的需求时，自动启用本技能：
- 本地化更新/汉化工作（"汉化一下新加的物品"、"把 Mod 里的英文翻译一下"）
- 编译/重构翻译文件（"重新生成 mo"、"帮我编译翻译"、"帮我合并翻译"）
- 检测/维护翻译数据（"检查有没有漏掉的翻译"、"有没有空词条"）
- 解决本地化相关的编译或运行错误（Permission denied、mo 文件被占用等）

---

## 工作流程

```
            启动本地化管线
                 │
  ┌──────────────┴──────────────┐
  ▼                             ▼
【提取与合并】                 【AI 动态汉化】
 1. 扫描 JSON 提取字符         1. 解析 zh_CN.po 寻找空 msgstr
 2. 增量追加至 zh_CN.po        2. AI 进行专业学术翻译
                               3. 强制对物品名称添加“中世纪”前缀
                               4. 直接覆写更新 zh_CN.po
                                │
  ┌─────────────────────────────┘
  ▼
【二进制打包编译】
 1. 检查游戏进程是否关闭（解文件锁）
 2. 调用编译器生成 Medieval.mo 二进制包
 3. 0 报错通过编译
```

---

## 🛠️ 步骤详情与执行脚本

### 步骤 1: 提取与合并（增量提取）

1. **原理**：调用 JSON 提取工具扫描 `data/mods/Medieval`，生成最新的 `Medieval.pot` 模板，并将其增量合并进 `zh_CN.po` 唯一翻译源中。新字段将被置为空串 `msgstr ""`，已有翻译绝不丢失。
2. **工具脚本**：`data/mods/Medieval/tools/update_medieval_i18n.py`
3. **执行命令**：
   ```powershell
   python data/mods/Medieval/tools/update_medieval_i18n.py
   ```

### 步骤 2: 动态汉化（AI Translation Pass）

1. **原理**：AI 读取 `zh_CN.po` 里的空白词条，在上下文大模型中直接汉化，并将汉化好的内容持久化写入到唯一翻译源 `zh_CN.po` 中，彻底消除 Python 脚本中的硬编码翻译字典。
2. **测试命名规则**：为了在测试中快速甄别 Mod 特有物品，**所有的物品类词条其中文汉化名称必须强制以“中世纪”作为开头前缀**（如 `中世纪武装衣`，`中世纪战锤` 等）。
3. **自动化写入脚本**：`data/mods/Medieval/tools/workflow_ai_translate.py`
4. **执行命令**：
   ```powershell
   python data/mods/Medieval/tools/workflow_ai_translate.py
   ```
5. **空值校验脚本**：`data/mods/Medieval/tools/find_empty_keys.py`（实测空 key 数量必须为 **0**）。

### 步骤 3: 打包编译（Compile to MO）

1. **原理**：将 100% 汉化的 `zh_CN.po` 文件编译打包成 `LC_MESSAGES/Medieval.mo`。
2. ** gotcha（非常重要）**：如果在 Windows 上游戏处于运行状态，系统会强锁定 `Medieval.mo` 文件。**必须完全关闭正在运行的 `cataclysm-tiles.exe` 进程，然后才能执行编译命令**。
3. **执行命令**：
   ```powershell
   python data/mods/Medieval/tools/update_medieval_i18n.py
   ```

---

## 📋 关联文件与路径

* **JSON Extractor 脚本**: [extract_json_strings.py](file:///e:/Cataclysm-Medieval/lang/extract_json_strings.py)
* **PO-to-MO 编译器**: [compile_project_translations.py](file:///e:/Cataclysm-Medieval/data/mods/Medieval/tools/compile_project_translations.py)
* **增量更新管线脚本**: [update_medieval_i18n.py](file:///e:/Cataclysm-Medieval/data/mods/Medieval/tools/update_medieval_i18n.py)
* **动态翻译写入脚本**: [workflow_ai_translate.py](file:///e:/Cataclysm-Medieval/data/mods/Medieval/tools/workflow_ai_translate.py)
* **汉化校验脚本**: [find_empty_keys.py](file:///e:/Cataclysm-Medieval/data/mods/Medieval/tools/find_empty_keys.py)
* **唯一翻译源文件**: [zh_CN.po](file:///e:/Cataclysm-Medieval/data/mods/Medieval/lang/po/zh_CN.po)
* **二进制编译产物**: [Medieval.mo](file:///e:/Cataclysm-Medieval/data/mods/Medieval/lang/zh_CN/LC_MESSAGES/Medieval.mo)

---

## ⚠️ 重要规则

1. **唯一源头原则**：所有的汉化字典必须只存在于 [zh_CN.po](file:///e:/Cataclysm-Medieval/data/mods/Medieval/lang/po/zh_CN.po) 文件本身，禁止在 Python 代码或系统配置里残留任何硬编码翻译键值对。
2. **测试前缀原则**：物品（具有 `med_ ` 前缀或确认为物品名称）的中文译名必须强制加上“中世纪”前缀，便于联调测试。
3. **安全文件解锁**：在遇到 `Permission denied` 报错时，第一反应应是指导并确认用户完全关闭了游戏，然后再重启编译工具。
