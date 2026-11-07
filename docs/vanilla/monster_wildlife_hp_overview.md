# 原版野生动物 HP 概览

> 数据来源：`data/json/monsters/` 下 `categories` 含 `WILDLIFE` 的怪物条目。
> 只统计直接定义了 `hp` 字段的条目；copy-from 的幼体/变体未单独列出。

---

## 总体分布

| 类别 | HP 范围 | 代表 |
|------|---------|------|
| 哺乳动物 | 2 ~ 160 | 黑鼠 6 / 鹿 60 / 熊 100 / 驼鹿 120 / 巨獠驼鹿 160 |
| 鸟类 | 1 ~ 35 | 蜂鸟 3 / 乌鸦 4 / 火鸡 21 / 肿胀渡鸦 35 |
| 爬行/两栖 | 1 ~ 400 | 蝌蚪 1 / 响尾蛇 12 / 下水道鳄鱼 90 / 死亡响尾蛇 400 |
| 鱼类 | 1 ~ 50 | 鱼苗 1 / 小鱼 6 / 中鱼 10 / 巨小龙虾 50 |

---

## 哺乳动物

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

## 鸟类

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

## 爬行/两栖动物

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

## 鱼类

| ID | 名称 | HP |
|----|------|:--:|
| mon_fish_fry | fish fry | 1 |
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

## 对 Medieval Mod 的参考意义

- **小动物阈值**：鼠/松鼠/兔/小鸟 HP 在 3~12 之间，普通攻击即可秒杀。
- **中型猎物**：鹿/野猪/狼 60 HP，需要 2~4 次命中。
- **大型危险动物**：熊/牛/马 90~100 HP，驼鹿 120 HP，属于高威胁目标。
- **奇幻生物标尺**：若 Medieval 加入奇幻野兽，可参考上述尺度：普通狼 40 HP，熊 100 HP，龙/巨怪可按 200~500 HP 设计。
