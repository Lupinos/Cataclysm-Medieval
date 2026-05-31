# CDDA Item JSON 类型速查

> 供 medieval-json-item Skill 在生成时参考。记录各 item 类型的关键字段和常见陷阱。

---

## ARMOR

### 最小可用定义

```json
{
  "type": "ARMOR",
  "id": "medieval_xxx",
  "name": { "str": "物品名" },
  "description": "描述文字",
  "weight": "XXX g",
  "volume": "X L",
  "price": XXXX,
  "price_postapoc": XXX,
  "material": ["material_id"],
  "symbol": "[",
  "color": "color_name",
  "armor": [
    {
      "covers": ["torso"],
      "specifically_covers": ["armor_normal"],
      "coverage": 90,
      "encumbrance": 10,
      "material_thickness": 4,
      "protection": { "bash": 5, "cut": 4, "stab": 2, "bullet": 0 }
    }
  ],
  "flags": ["VARSIZE"]
}
```

### 关键提醒

1. **`armor` 必须是数组**，每个部位一个对象
2. **`covers` 必须是数组**，即使是单个部位
3. **`specifically_covers` 控制穿着层**，缺少会导致同层冲突
4. **`name` 必须是 `{ "str": "..." }` 格式**，不可直接写字符串

### 常见材质 ID

```
cotton, wool, leather, fur, steel, iron, wood, bone, bronze
```

### 常见颜色

```
brown, dark_gray, light_gray, white, red, green, blue, yellow
```

---

## GENERIC (武器/通用物品)

```json
{
  "type": "GENERIC",
  "id": "medieval_xxx",
  "name": { "str": "武器名" },
  "description": "描述",
  "weight": "XXX g",
  "volume": "X L",
  "price": XXXX,
  "material": ["steel", "wood"],
  "symbol": "/",
  "color": "dark_gray",
  "bashing": 8,
  "cutting": 24,
  "to_hit": { "melee": 2, "grip": 0 },
  "techniques": ["WBLOCK_1", "RAPID"],
  "flags": ["DURABLE_MELEE", "STAB"],
  "qualities": [["CUT", 1]]
}
```

### 武器技术 (techniques) 常用值

- `WBLOCK_1` / `WBLOCK_2` — 武器格挡
- `RAPID` — 快速攻击
- `SWEEP` — 横扫
- `PRECISE` — 精准打击
- `BRUTAL` — 暴击增强

---

## TOOL

```json
{
  "type": "TOOL",
  "id": "medieval_xxx",
  "name": { "str": "工具名" },
  "description": "描述",
  "weight": "XXX g",
  "volume": "X L",
  "price": XXXX,
  "material": ["steel"],
  "symbol": ";",
  "color": "dark_gray",
  "qualities": [["HAMMER", 2]],
  "ammo": "battery",
  "charges_per_use": 1,
  "use_action": { "type": "repair_item" }
}
```

---

## 陷阱列表

### 🚫 绝对不要做的事

1. **`name` 直接写字符串** — 必须 `{ "str": "..." }`
2. **`material` 不写成数组** — 单材料也要 `["leather"]`
3. **`covers` 不写成数组** — `"covers": "torso"` 是错的
4. **`armor` 写成对象而非数组** — 即使只有一个部位也要 `[{...}]`
5. **ID 忘记加 `medieval_` 前缀**
6. **小数写整数** — 体积 `"2.5 L"` OK，`"2 L"` OK
7. **漏掉 `price_postapoc`** — 没有这个字段 NPC 不交易
8. **`specifically_covers` 引用不存在的层** — CDDA 标准层只有 `armor_skin`, `armor_normal`, `armor_outer`, `armor_strapped`

### ⚠️ 容易漏掉的字段

- `flags`: 至少需要 `["VARSIZE"]`（可调节大小）
- `looks_like`: 游戏内视觉回退（可选但建议）
- `warmth`: 保暖值，0-60
- `armor.coverage`: 覆盖率，0-100，不写默认 0（= 不保护）
