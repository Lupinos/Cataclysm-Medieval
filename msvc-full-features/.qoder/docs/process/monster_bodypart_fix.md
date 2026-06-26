# 任务：Monster 部位 HP 修复

## 目标

让 Monster 系统支持部位分血——攻击打到的部位扣该部位的 HP，而非全局 HP。为野生动物/巨怪/龙类提供完整战斗体验（部位骨折、流血、不同部位不同 base_hp/hit_size）。

## 依赖

- [design08-敌人.md](../design/design08-敌人.md) 双系统分层决策
- [code_bodypart_hp_system.md](../vanilla/code_bodypart_hp_system.md) 部位分血架构现状
- [code_harvest_drop_system.md](../vanilla/code_harvest_drop_system.md) 产物系统

---

## 改造内容

### 阶段 1：C++ 核心修复（~10 行）

#### 1.1 `src/mtype.h` — 加 anatomy 字段

```cpp
anatomy_id anatomy = anatomy_id( "default_anatomy" );  // 加在 mtype 结构体中
```

#### 1.2 `src/monstergenerator.cpp` — 加载 anatomy

```cpp
optional( jo, was_loaded, "anatomy", mon.anatomy, anatomy_id( "default_anatomy" ) );
```

#### 1.3 `src/monster.cpp` — 构造时改用自身 anatomy

```cpp
// 改前：
set_anatomy( anatomy_default_anatomy );

// 改后：
set_anatomy( type->anatomy );
```

#### 1.4 `src/monster.cpp` — `apply_damage` 不再绕过 bp

```cpp
// 改前：
void monster::apply_damage( Creature *source, bodypart_id /*bp*/, int dam, ... ) {
    hp -= dam;  // 全局 HP
}

// 改后：
void monster::apply_damage( Creature *source, bodypart_id bp, int dam, ... ) {
    mod_part_hp_cur( bp, -dam );  // 部位 HP
    // 死亡判定：致命部位归零
}
```

#### 1.5 `src/monster.cpp` — `get_hp` / `get_hp_max` 委托基类

```cpp
// 移除 override 或用 super call
```

### 阶段 2：新建部位类型（JSON）

| 部位 | base_hp | hit_size | 说明 |
|------|---------|----------|------|
| `wing_l` | 40 | 18 | 左翼 |
| `wing_r` | 40 | 18 | 右翼 |
| `neck` | 30 | 5 | 颈部（可选，狮鹫需要） |
| `tail` | 20 | 8 | 尾巴（可选，龙需要） |

### 阶段 3：新建 anatomy（JSON）

| anatomy | 部位数 | 说明 |
|---------|--------|------|
| `anatomy_griffin` | 10 | head/torso/limbs×4 + wings×2 + feet×2 |
| `anatomy_drake` | 8 | head/torso/limbs×4 + tail |
| `anatomy_hydra` | 4 + 3×N | head×N/torso/limbs×2（N 个头） |

### 阶段 4：已有 Monster 的 anatomy 字段补充

现有 monster 都缺 `anatomy` 字段——不加的话默认走 `default_anatomy`（只有 head/torso 2 个部位）。

| 怪物 | 新建 anatomy | 是否急需 |
|------|-------------|---------|
| bear → `anatomy_bear` | 沿用 human_anatomy（8 部位） | 否，先用 default 也能工作 |
| wolf → `anatomy_wolf` | 6 部位（四足+头+躯干） | 否 |
| drake → `anatomy_drake` | 8 部位 | 是 |
| griffin → `anatomy_griffin` | 10 部位 | 是 |

---

## 测试点

1. `mon_bear` 受击后 `get_part_hp_cur(head)` 降低，而非全局 `hp`
2. 致命部位（is_vital）归零 → 死亡
3. 非致命部位（wing_l）归零 → 不死亡，但可能影响移动/攻击
4. `harvest` 产物在死亡时正常生成
5. `dissect` 产物在死亡时预生成进尸体口袋

---

## 风险

- `apply_damage` 修改后，所有现有 monster 的死亡判定从"全局 hp<=0"变成"致命部位 hp<=0"——需验证已有 monster（特别是 boss 级）的生存力是否下降
- 已有 UI 显示的是全局 HP 条——修复后需要确认是否显示部位总 HP（`get_hp()` 求和已自动支持）
