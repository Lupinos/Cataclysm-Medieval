# 原版野生动物 HP 概览

> 核对基准：CDDA `0.H-branch` 提交 `6dae8435e804bc11dd85baa21954ba6297e7841f`。
> 数据来源：`data/json/monsters/mammal.json`、`bird.json`、`reptile_amphibian.json`、`fish.json`。下表为选录，包含继承值、鱼类 abstract 模板及部分变异/非 WILDLIFE 参考条目，不能作为 WILDLIFE 类别的完整清单。

原版 Monster 的这些 HP 是全局 HP。实际实例可能受世界选项和其他运行时修正影响；不是按 anatomy 分配的部位血量。`copy-from` 需沿父项读取；例如 `mon_rabbit` 从 `mon_rabbit_base` 继承 8 HP。鱼类的 `mon_fry` 与 `mon_fish_tiny/small/medium/large/huge` 是 abstract 模板 ID，不能当成可以直接生成的具体怪物。

---

## 下表选录值的范围（非全类别统计）

| 类别 | HP 范围 | 代表 |
|------|---------|------|
| 哺乳动物 | 4 ~ 160 | 黑鼠 6 / 鹿 60 / 熊 100 / 驼鹿 120 / 巨獠驼鹿 160 |
| 鸟类 | 3 ~ 35 | 蜂鸟 3 / 乌鸦 4 / 火鸡 21 / 肿胀渡鸦 35 |
| 爬行/两栖 | 1 ~ 400 | 春雨蛙 1 / 响尾蛇 12 / 下水道鳄鱼 90 / 死亡响尾蛇 400 |
| 鱼类 | 1 ~ 50 | 鱼苗 1 / 小鱼 6 / 中鱼 10 / 巨小龙虾 50 |

---

## 哺乳动物（mammal.json）

| ID | 名称 | HP |
|----|------|:--:|
| mon_chipmunk | chipmunk | 4 |
| mon_black_rat | black rat | 6 |
| mon_lab_rat | lab rat | 6 |
| mon_squirrel | squirrel | 6 |
| mon_squirrel_red | squirrel | 6 |
| mon_rabbit | rabbit | 8 |
| mon_bat | bat | 10 |
| mon_muskrat | muskrat | 10 |
| mon_cat | shorthair cat | 12 |
| mon_groundhog | groundhog | 12 |
| mon_otter | otter | 12 |
| mon_opossum | opossum | 12 |
| mon_beaver | beaver | 16 |
| mon_bobcat | bobcat | 16 |
| mon_cat_maine_coon | Maine Coon | 16 |
| mon_dog_beagle | beagle | 13 |
| mon_dog_bcollie | border collie | 19 |
| mon_dog | Labrador mutt | 30 |
| mon_dog_gshepherd | German shepherd | 36 |
| mon_dog_samoyed | Samoyed | 32 |
| mon_dog_gpyrenees | Great Pyrenees | 40 |
| mon_dog_rottweiler | rottweiler | 42 |
| mon_dog_bull | bulldog | 47 |
| mon_dog_pitbullmix | pit bull mix | 27 |
| mon_dog_chihuahua | Chihuahua | 6 |
| mon_dog_dachshund | dachshund | 10 |
| mon_fox_gray | fox | 20 |
| mon_fox_red | fox | 30 |
| mon_mink | mink | 30 |
| mon_weasel | weasel | 20 |
| mon_coyote | coyote | 22 |
| mon_coyote_wolf | coyote | 20 |
| mon_wolf | wolf | 40 |
| mon_raccoon | raccoon | 14 |
| mon_sewer_rat | sewer rat | 10 |
| mon_pig | pig | 50 |
| mon_boar_wild | wild boar | 60 |
| mon_deer | deer | 60 |
| mon_cougar | cougar | 60 |
| mon_horse_foal | foal | 35 |
| mon_horse | horse | 90 |
| mon_cow_calf | calf | 40 |
| mon_cow | cow | 100 |
| mon_bear | black bear | 100 |
| mon_moose_calf | moose calf | 40 |
| mon_moose | moose | 120 |
| mon_tusked_moose_calf | tusked moose calf | 60 |
| mon_tusked_moose | great tusked moose | 160 |
| mon_reindeer | reindeer | 120 |
| mon_sheep_lamb | lamb | 20 |
| mon_sheep | sheep | 90 |
| mon_llama_calf | llama calf | 35 |
| mon_llama | llama | 90 |
| mon_ferret | ferret | 12 |

---

## 鸟类（bird.json）

| ID | 名称 | HP |
|----|------|:--:|
| mon_bluejay | blue jay | 3 |
| mon_cardinal | cardinal | 3 |
| mon_robin | robin | 3 |
| mon_sparrow | sparrow | 3 |
| mon_hummingbird | hummingbird | 3 |
| mon_crow | crow | 4 |
| mon_raven | raven | 4 |
| mon_pigeon | pigeon | 4 |
| mon_duck | duck | 4 |
| mon_coot | coot | 5 |
| mon_chicken | chicken | 8 |
| mon_crow_mutant_small | oversized crow | 8 |
| mon_woodpecker | woodpecker | 10 |
| mon_turkey | turkey | 21 |
| mon_crow_mutant | bloated corvid | 35 |

---

## 爬行/两栖动物（reptile_amphibian.json）

| ID | 名称 | HP |
|----|------|:--:|
| mon_bullfrog_tadpole | tadpole | 2 |
| mon_odd_tadpole | tadpole | 2 |
| mon_peeper_frog | spring peeper | 1 |
| mon_gray_frog | gray treefrog | 2 |
| mon_bullfrog_frog | bullfrog | 4 |
| mon_strange_frog | strange bullfrog | 12 |
| mon_odd_toad | odd toad | 12 |
| mon_rattlesnake_s | rattlesnake snakelet | 2 |
| mon_rattlesnake | rattlesnake | 12 |
| mon_rattlesnake_big_s | mutant rattlesnake snakelet | 12 |
| mon_rattlesnake_giant | giant rattlesnake | 64 |
| mon_sewer_snake | sewer snake | 10 |
| mon_gator | sewer gator | 90 |
| mon_rattlesnake_mega | deathrattle serpent | 400 |

---

## 鱼类与水生参考（fish.json）

| ID | 名称 | HP |
|----|------|:--:|
| mon_fry | fish fry | 1 |
| mon_fish_tiny | tiny fish | 2 |
| mon_fish_small | small fish | 6 |
| mon_fish_medium | medium fish | 10 |
| mon_fish_crayfish | crayfish | 3 |
| mon_fish_lobster | lobster | 12 |
| mon_fish_eel | American eel | 10 |
| mon_fish_large | large fish | 20 |
| mon_fish_huge | huge fish | 30 |
| mon_giant_crayfish | giant crayfish | 50 |

---

## 如何使用这些原版数据

- 选录可作为体量参考：普通狼 40、鹿/野猪 60、马 90、熊/牛 100、驼鹿 120 HP。不能由 HP 单独推断需要几次命中或能否一击击杀；伤害、护甲、弱点、命中、技能等都参与计算。
- `WILDLIFE` 是数据类别，不等同于“现实普通野兽”。反过来，文件中看起来像动物的条目也不一定带此类别；如 `mon_odd_tadpole`、`mon_strange_frog`、`mon_odd_toad` 显式为 `NULL` 类别。
- 奇幻生物采用多少 HP 是项目设计决定，原版动物表不能推出龙/巨怪必须为 200–500 HP。引擎重做为部位 HP 后，还须重新定义总量、重要部位和受伤后果，不能直接复制原版全局 HP 当作同一尺度。
