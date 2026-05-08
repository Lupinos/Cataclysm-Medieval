---
name: medieval-design
description: Interactive requirements analysis and design document authoring for Cataclysm-Medieval mod. Use when the user proposes new features, gameplay mechanics, content additions, or system changes for the Medieval total conversion mod. Guides through clarifying questions, research tasks, and structured design documents in docs/design/.
---

# 中世纪 Mod 需求分析与策划案撰写

## 触发条件

当用户提出以下类型的需求时，自动启用本技能：
- 新功能/玩法机制提议（"我想让强盗能..."、"能不能加一个..."）
- 内容添加需求（"需要中世纪的武器/建筑/职业..."）
- 系统改动需求（"把 X 系统改成 Y"）
- 对现有策划案的修改/推翻
- 任何以 "策划"、"设计"、"方案" 开头的讨论

---

## 工作流程

```
用户提出笼统需求
    │
    ├── 步骤1: 交互式澄清 ──→ 追问细节直到足够具体
    │
    ├── 步骤2: 冲突检测 ──→ 扫描 docs/design/ 下已有策划案
    │
    ├── 步骤3: 调研判断 ──→ 需要了解 CDDA 机制？
    │         ├─ 是 → 执行调研，写现状文档到 docs/
    │         └─ 否 → 直接进入步骤4
    │
    ├── 步骤4: 撰写策划案 ──→ 写入 docs/design/
    │
    └── 步骤5: 更新索引 ──→ 更新 rules/doc_index.md
```

---

## 步骤1: 交互式澄清

收到笼统需求后，**不要直接假设细节**。按需求类型提出澄清问题：

### 玩法机制类
- 玩家具体能做什么？触发条件是什么？
- 是主动操作（按键/菜单）还是被动触发（条件满足自动发生）？
- 涉及哪些已有系统？（战斗/制作/地图/NPC/...）
- 期望的结果/效果是什么？

### 内容添加类
- 具体要加什么？（物品/NPC/建筑/配方/...）
- 数量规模？（几个还是几百个？）
- 是否有参考来源？（历史时期/地域/现有 mod）
- 和现有中世纪内容的区分？（新层级还是替换？）

### 系统改动类
- 当前系统的什么行为需要改变？
- 改完后的期望行为是什么？
- 是纯 JSON 配置还是需要 C++ 改动？
- 影响范围？（只影响 mod 还是影响全局？）

### 提问原则
- 每次 2-4 个问题，不要一次抛太多
- 优先问对方案方向有决定性影响的问题
- 如果用户回答仍不够具体，继续追问第二轮
- 确认理解正确后，用一句话总结需求，让用户确认

---

## 步骤2: 冲突检测

在撰写策划案前，先检查 `docs/design/` 下所有已有策划案：

1. 用 `list_dir` 列出 `docs/design/` 内容
2. 快速浏览相关策划案的标题和摘要
3. 如果新需求与已有策划案**矛盾**：
   - 明确指出冲突点
   - 以用户最新要求为准
   - 更新（search_replace）或覆写（create_file）旧策划案
   - 在旧策划案顶部添加变更记录：`> ⚠️ [日期] 因新需求 "[简述]" 修改`
4. 如果新需求与已有策划案**互补**：
   - 在新策划案中交叉引用旧策划案

---

## 步骤3: 调研判断

如果实现方案需要了解 CDDA 现有机制（用户没有直接给出足够细节），启动调研：

1. 确定调研目标：要查什么 C++ 代码 / JSON 数据 / 已有 mod
2. 使用 `grep-cpp` 搜索 C++ 源码，`read_file` 阅读关键文件
3. 调研结果写入 `docs/<topic>.md`（现状文档，纯架构分析，不混入策划）
4. 策划案中引用调研文档

**不需要调研的情况**：
- 用户已经给出足够具体的技术细节
- 纯 JSON 数据定义（item/NPC/monster 模板）
- 对已有策划案的修改

---

## 步骤4: 撰写策划案

文件路径：`docs/design/<descriptive_name>.md`

### 策划案模板

```markdown
# [标题：做什么事]

> 基于 [调研文档](../path/to/research.md) 的 Medieval Mod [分类] 设计。
> 需求来源：[用户原始需求简述]

---

## 需求概述

[一句话说清要做什么，预期效果]

## 方案

[具体实现方案，可以是多个可选方案的对比表]

### 方案 A：[名称]（推荐/备选）

[详细描述]

### 方案 B：[名称]

[详细描述]

## 技术要点

- [关键约束/注意事项]
- [需要的 JSON 类型]
- [是否需要 C++ 改动]

## 实施步骤

1. [分步实施计划]
2. ...

---

## 相关文档

| 文档 | 关系 |
|------|------|
| [research.md](../research.md) | 相关现状调研 |
| [other_design.md](other_design.md) | 相关策划案 |
```

### 命名规范
- 小写英文，连字符分隔
- 前缀 `medieval_` 表示中世纪专属
- 示例：`medieval_blacksmith_design.md`、`medieval_bandit_equipment_design.md`

---

## 步骤5: 更新索引

修改 `rules/doc_index.md`，在 "中世纪策划案" 表格中添加新行。格式与已有条目一致：

```markdown
| [filename.md](../docs/design/filename.md) | 一句话说明 |
```

---

## 重要原则

1. **用户最新要求是最高优先级** — 任何已有策划案都可能被推翻
2. **先问清楚再动笔** — 不要基于猜测撰写方案
3. **策划案要可执行** — 每个方案都要能分解为具体的实施步骤
4. **现状与策划严格分离** — 调研文档（docs/）只写 CDDA 现状，策划案（docs/design/）只写 Medieval Mod 设计
5. **保持索引同步** — 每次写新文档后立即更新 doc_index.md
