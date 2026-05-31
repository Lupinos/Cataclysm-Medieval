# 使用示例

---

## 示例 1：有设计文档 — 生成盔甲 JSON

**用户输入**：
> 根据 design02-盔甲.md 中 2.2 颈部的表格，生成对应的 JSON

**Skill 行为**：
1. 读取 design02-盔甲.md，定位"2.2 颈部"表格
2. 运行 `keys.py --human type=ARMOR` 发现 ARMOR 的完整字段列表
3. 提取表格中物品，映射到 CDDA 字段
4. 生成 JSON
5. 写入文件 → L0/L1/L2/L3 校验 → 通知用户

---

## 示例 2：无设计文档 — 互联网调研 → 生成武器

**用户输入**：
> 生成中世纪的农具（flail, pitchfork, scythe）作为武器

**Skill 行为**：

**Phase 1A — 互联网调研**：
```
search_web: "medieval flail weapon peasant revolt 14th century"
search_web: "medieval pitchfork as weapon history"
search_web: "medieval war scythe vs farming scythe"
```

调研结果：
- Flail（连枷）：打谷工具改造，由长柄+短棒用链连接，能绕过盾牌
- Pitchfork（干草叉）：4英尺长木柄+双/三铁齿，间距控制好
- Scythe（镰刀）：农用弯刃，需改装为 war scythe（刃转90°）才是有效武器

**Phase 1B — 向用户报告**：
> 找到 3 种农具武器：
> 1. Grain Flail — 木柄+铁链+短棒，钝击，绕过盾牌
> 2. Pitchfork — 木柄+铁齿，穿刺，长距
> 3. War Scythe — 镰刀刃旋转90°改装，斩击
> 
> 建议 CDDA type=GENERIC, techniques=[...]
> 确认后开始生成？

**Phase 1C — CDDA 格式调研**：
```powershell
python "E:\Cataclysm-Medieval\tools\json_tools\keys.py" --human type=GENERIC
python "E:\Cataclysm-Medieval\tools\json_tools\pluck.py" type=GENERIC --all 2>&1 | Select-Object -First 5
```

**Phase 1D — 用户确认后生成 JSON**

---

## 示例 3：多部位盔甲（ARMOR 特有）

**用户输入**：
> 生成 gambeson（覆盖躯干+手臂）

**关键处理**：`armor` 数组中每个部位独立定义：

```json
"armor": [
  {
    "covers": ["torso"],
    "specifically_covers": ["armor_normal"],
    "coverage": 95,
    "encumbrance": 12,
    "material_thickness": 4,
    "protection": { "bash": 6, "cut": 5, "stab": 3, "bullet": 0 }
  },
  {
    "covers": ["arm_l", "arm_r"],
    "specifically_covers": ["armor_normal"],
    "coverage": 90,
    "encumbrance": 8,
    "material_thickness": 4,
    "protection": { "bash": 5, "cut": 4, "stab": 2, "bullet": 0 }
  }
]
```
