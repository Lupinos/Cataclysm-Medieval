# 解剖/屠宰产物系统：完整 key 引用链

> 调研 CDDA 原版的 harvest / dissect / butchery 系统的数据流和引用关系。

---

## 系统概述

三套 JSON 类型协作实现"杀怪→解剖→拿战利品"：

| JSON 类型 | 文件 | 定义什么 |
|-----------|------|---------|
| `harvest_drop_type` | `harvest_drop_type.json` | **怎么掉**：行为规则（屠宰/解剖/需什么技能） |
| `harvest` | `harvest.json` / `harvest_dissect.json` | **掉什么**：具体产物列表，引用上面的 type 和下面的 item |
| `MONSTER` | `monster/*.json` | **谁掉**：生物挂上 harvest 列表 |

---

## 完整引用链（以火龙为例）

### 第一层：物品定义

```json
// items/medieval/monster_parts.json
{ "type": "GENERIC", "id": "dragon_meat",        "name": "龙肉" }
{ "type": "GENERIC", "id": "dragon_blood_vial",  "name": "龙血" }
{ "type": "GENERIC", "id": "dragon_scale",       "name": "龙鳞" }
{ "type": "GENERIC", "id": "dragon_bone",        "name": "龙骨" }
{ "type": "GENERIC", "id": "dragon_heart",       "name": "龙心" }
{ "type": "GENERIC", "id": "dragon_fire_gland",  "name": "龙火腺" }
```

每个物品的 `id` 被第三层的 `drop` 字段引用。

---

### 第二层：掉落类型规则

```json
// harvest_drop_type.json

// 原版已有的（不需要改）：
{ "type": "harvest_drop_type", "id": "flesh"      }  // 屠宰/解剖都行
{ "type": "harvest_drop_type", "id": "bone"       }  // 同上
{ "type": "harvest_drop_type", "id": "skin"       }  // 同上
{ "type": "harvest_drop_type", "id": "blood"      }  // 屠宰/解剖都行
{ "type": "harvest_drop_type", "id": "offal"      }  // 同上

// 中世纪新增：
{ "type": "harvest_drop_type", "id": "dragon_organ",
    "dissect_only": true,
    "harvest_skills": ["survival", "firstaid"],
    "msg_dissect_fail": "切口太深，龙心破裂了。"
}
```

`harvest_drop_type.id` 被第三层的 `entry.type` 引用，控制该条产物的**行为规则**。

---

### 第三层：harvest 列表

```json
// harvest.json

{
  "type": "harvest",
  "id": "harvest_dragon",          // 被 monster.harvest 引用
  "entries": [
    // 每条 entry 有两个引用：
    //   drop → 物品 id 或 item_group id（掉什么）
    //   type → harvest_drop_type id（怎么掉）

    { "drop": "dragon_meat",       "type": "flesh",   "mass_ratio": 0.45 },
    { "drop": "dragon_blood_vial", "type": "blood",   "mass_ratio": 0.05 },
    { "drop": "dragon_scale",      "type": "skin",    "mass_ratio": 0.08 },
    { "drop": "dragon_bone",       "type": "bone",    "mass_ratio": 0.20 },
    { "drop": "dragon_heart",      "type": "dragon_organ", "scale_num": [1,1], "max": 1 },
    { "drop": "dragon_fat",        "type": "flesh",   "mass_ratio": 0.10 }
  ]
},

{
  "type": "harvest",
  "id": "dissect_dragon",          // 被 monster.dissect 引用
  "entries": [
    // dissect 产物在龙死亡时预生成，塞进尸体 CORSE 口袋
    { "drop": "dragon_heart",      "type": "dragon_organ" },
    { "drop": "dragon_fire_gland", "type": "dragon_organ" },
    { "drop": "dragon_eye",        "type": "dragon_organ" }
  ]
}
```

---

### 第四层：生物定义

```json
// monster/spawn/dragon.json

{
  "type": "MONSTER",
  "id": "mon_dragon_fire",
  "name": "火龙",
  "harvest": "harvest_dragon",     // → harvest.id "harvest_dragon"
  "dissect": "dissect_dragon"      // → harvest.id "dissect_dragon"
}
```

---

## 三层 key 引用关系

```
harvest_drop_type.id        ←──  harvest_entry.type        （怎么掉）
                                    harvest_entry.drop      （掉什么）
                                        ↓
                                    item.id   或  item_group.id

harvest.id                  ←──  monster.harvest           （屠宰产物列表）
monster.id                                     ←──  mapgen / spawn
harvest.id                  ←──  monster.dissect           （解剖产物列表）
```

---

## harvest vs dissect 的运行时差异

| | harvest（屠宰） | dissect（解剖） |
|---|---|---|
| **产物生成时机** | 玩家 butcher 时才实时计算 | 怪物死亡瞬间预生成 |
| **产物存放** | 不预存，butcher 时凭空创建 | 存入尸体 `CORPSE` 口袋 |
| **数量决定** | `mass_ratio × 尸体重量` 或 `base_num + scale_num × skill` | 死亡时 `item_group` roll 好 |
| **技能影响** | 产出**数量**（survival 越高肉越多） | 取出**成功率**（技能不够就失败销毁） |
| **典型产物** | 肉、皮、骨、血 | 特殊器官、腺体、突变样本 |
| **尸体损坏影响** | ✅ 损坏越多产量越少 | ❌ 预生成时没算损坏 |

---

## 三层 C++ 数据流

```
游戏启动
   harvest_drop_type.json  →  harvest_drop_type_factory.load()   内存: harvest_drop_type[]
   harvest.json            →  harvest_list_factory.load()         内存: harvest_list[] (每个含 entries)
   monster.json            →  mtype.harvest = "harvest_dragon"    内存: mtype { harvest_id, dissect_id }

怪物死亡
   monster::die()
     → spawn_dissectables_on_death(corpse)
        → 读取 mtype.dissect → harvest_list
           → 遍历 entries，对每个 entry.drop 调用 item_group::items_from()
              → 生成物品，dropped_from = entry.type
              → corpse.put_in(CORPSE pocket)

玩家 butcher
   activity_handlers::butcher_finish()
     → 读取 corpse.get_mtype()->harvest → harvest_list
        → 遍历 entries，计算数量 = mass_ratio × weight
           → 生成物品，放入玩家背包

玩家 dissect
   dissect 活动完成
     → 从 corpse CORPSE 口袋取出预生成物品
        → 根据 entry.type 查 harvest_drop_type
           → 获取 harvest_skills，玩家技能检定
              → 通过 → 物品给玩家
              → 失败 → 物品销毁 + 显示 msg_dissect_fail
```

---

## NPC 路线的缺失环节

原版 `Character` / `npc` 死亡**不调用** `spawn_dissectables_on_death()`。

如果中世纪 mod 用 NPC 系统替代 monster 实现部位分血，需要**补充 NPC 死亡时的产物预生成逻辑**，否则解剖功能无法工作。
