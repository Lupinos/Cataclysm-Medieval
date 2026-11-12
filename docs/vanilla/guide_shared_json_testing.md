# JSON 内容的测试方式：命令行、自动用例与游戏内调试

共用调研：服务于[02 盔甲](../design/design02-盔甲.md)、[03 衣物](../design/design03-日常衣物.md)、[04 武器](../design/design04-武器.md)、[06 建筑](../design/design06-建筑.md)等专题，不对应单一策划案。本篇说明 JSON 内容可采用的验证方式。

## 一、现有能力与适用范围

这份调查说明当前仓库能够怎样验证新写的游戏 JSON，覆盖物品、武器、护甲、地形、家具、建筑生成及关联内容。依据为本地源码、测试用例、构建配置和游戏自带文档；基准提交为 `ea81dc9fb1`。这里调查测试手段，不修改现有 skill，也不表示其他编写指南中的示例已经通过游戏测试。

游戏已有三种不同层次的验证能力，另外还有格式工具。它们回答的问题不同：

| 方式 | 能回答什么 | 不能据此断言什么 |
|---|---|---|
| JSON 解析与原版格式化器 | 文件能否解析、是否符合格式约定 | 字段被游戏使用、引用有效、游戏行为正确 |
| 游戏 `--check-mods` | 指定模组及依赖能否加载、整理数据并通过已有一致性检查 | 每个字段都有检查、每种随机分支都执行、新武器或建筑行为符合设计 |
| `cata_test` / `cata_test-tiles` | 数据加载，以及选中 C++ 用例所断言的行为 | 新增内容自动获得完整测试覆盖 |
| 游戏内 debug 菜单 | 实际生成、查看、使用、穿戴、战斗与地图交互 | 一次观察即可证明概率分布或长期稳定性 |

`--check-mods` 和测试程序都可以不经过游戏交互界面运行。无需为了数据检查先操作角色。游戏的纯文字 curses 版本仍是交互界面，不能把“没有贴图”与“自动测试”混为一谈；相反，带 `tiles` 名字的测试程序也可以运行非交互测试。

## 二、文件解析与格式检查

### 普通解析器适合做第一步

用 Python 等工具解析 JSON，能快速找出括号、逗号、引号等语法错误。教程里的局部片段能解析，也不代表它是可独立加载的游戏定义；还需要 `type`、身份字段及相应类型所需的数据。

### 原版格式化器会修改文件

源码位于 `tools/format/format_main.cpp`。Makefile 的工具通常叫 `tools/format/json_formatter.exe`（Windows）或 `json_formatter.cgi`，CMake 的目标名是 `json_formatter`。

传入文件名会检查并在需要时直接重写文件：

```powershell
.\tools\format\json_formatter.exe .\data\mods\my_mod\items.json
```

这是准备好格式化器后的用法示意，当前工作区没有找到该可执行文件。程序有三种值得区分的结果：

- 原文件与格式化结果一致：返回成功。
- 解析成功但格式不同：重写文件，输出 `Has been linted`，返回失败。
- 解析失败：输出解析错误，返回失败。

因此非零退出码可能表示刚完成格式修改，不能直接解释成游戏数据有语义错误。无参数时从标准输入读取，将结果输出到标准输出；这条路径不重写源文件。

仓库 `.github/workflows/json.yml` 运行 `make style-all-json-parallel RELEASE=1`。这项 CI 是格式检查，不能替代游戏加载或行为测试。

## 三、直接使用游戏执行数据加载检查

### 正确入口是 `--check-mods`

从仓库根目录运行，原版内容使用模组 ID `dda`；自定义模组使用其 `MOD_INFO.id`，不是目录名或显示名称。

```powershell
.\cataclysm-tiles.exe --check-mods dda
.\cataclysm-tiles.exe --check-mods my_mod
```

上面说明参数写法。Windows GUI 子系统程序应使用后文的等待与日志收集方式，不能仅凭终端提示符返回判断检查完成。

在 `src/main.cpp` 中，这个选项设置 `test_mode = true`，启动过程跳过 `catacurses::init_interface()`，随后执行 `game::check_mod_data()`。`src/debug.cpp` 中的调试报错在 test mode 下写日志并返回，不弹出等待玩家确认的错误窗口。

`src/game.cpp` 中的检查过程是：

1. 查找模组，检查依赖是否可用。
2. 创建临时测试世界，加载核心数据。
3. 加载该模组的依赖，再加载模组自身。
4. 调用 `finalize_loaded_data()`，整理继承与派生数据，执行已注册的一致性检查。
5. 删除这次创建的测试世界，清理地图缓存。

`src/init.cpp` 的一致性检查包括物品、材料、mapgen、palette、地形家具、配方、怪物、物品相关引用、职业、场景等多个系统。具体能发现哪些错误，取决于各系统的读取和检查代码。引用有效但选择错了对象、字段合法但数值不符合设计、字段虽被读取却没有产生预期行为，都仍可能通过。

### 多个模组参数不会构成一次联合测试

```powershell
.\cataclysm-tiles.exe --check-mods mod_a mod_b
```

`check_mod_data()` 把参数转换为集合，再分别对每个目标加载核心、其依赖和自身。它不会按 `mod_a` 然后 `mod_b` 的存档加载顺序验证联合覆盖。

若要检查实际组合，可以使用测试程序的 `--mods=mod_a,mod_b`，或创建启用该组合的游戏世界。检查两个模组各自成功，并不证明二者组合成功。

命令行还有两个细节：

- 把 `--check-mods` 及模组 ID 放在其他选项后面。它的处理函数会把后续全部参数收进待检查列表，后置的路径参数可能被当成模组 ID。
- `check_mod_data()` 内部存在空列表时检查所有非废弃模组的分支，但当前 CLI 为 `--check-mods` 声明至少一个参数。直接以无参数的 `--check-mods` 结束命令会报缺少参数，不应把它作为可用的全模组命令。

### Windows 下怎样得到可靠结果

本次实测使用 `Start-Process -WindowStyle Hidden`、标准输出/错误重定向以及进程退出码。下面是一条可复用的 PowerShell 操作示例，在仓库根目录执行；它只检查 `dda`，用户目录放在系统临时目录下。

```powershell
$checkUserPath = Join-Path $env:TEMP ('cdda-json-check-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $checkUserPath 'config') -Force | Out-Null

$checkProcess = Start-Process -FilePath (Join-Path $PWD 'cataclysm-tiles.exe') `
    -ArgumentList @('--userdir', "$checkUserPath/", '--check-mods', 'dda') `
    -WorkingDirectory $PWD -WindowStyle Hidden `
    -RedirectStandardOutput (Join-Path $checkUserPath 'stdout.txt') `
    -RedirectStandardError (Join-Path $checkUserPath 'stderr.txt') -PassThru

$checkProcess.WaitForExit()
$checkProcess.ExitCode
Get-Content (Join-Path $checkUserPath 'stdout.txt')
Get-Content (Join-Path $checkUserPath 'stderr.txt')
Get-Content (Join-Path $checkUserPath 'config/debug.log')
```

路径示例使用无空格的临时目录；若改用含空格路径，需为 `Start-Process` 的参数串保留正确引号。检查自定义模组时替换最后的 `dda`。

应同时读取退出码、stdout、stderr 和 debug.log。主程序以检查函数结果和 `debug_has_error_been_observed()` 决定成功与否；不过 `check_mod_data()` 的异常分支只是向 stderr 打印错误，没有直接将函数结果设为失败。因此，不能把任何情况下的退出码 0 都解释为“无加载错误”。

当前启动路径在检查前并不保证隔离用户目录的 `config` 已建立。本次第一次使用空目录时，检查退出码为 1，且没有可读 debug.log；先创建 `config` 后重试成功。自动执行时应先准备这个目录，确保错误确实有日志可查。

`--userdir` 是游戏参数；测试程序使用的则是 `--user-dir=`，二者不能互换。隔离目录也能避免把测试产物写进现有存档目录，或让同一份模组被数据目录和用户目录重复发现。

### `--jsonverify` 不适合验证游戏内容

虽然 `--help` 对它的描述是检查 JSON，但 `src/main.cpp` 在 `g->load_static_data()` 后看到该标志便退出。`load_static_data()` 主要初始化输入、自动拾取、自动备注、安全模式等静态配置，并没有加载 `data/json` 的游戏定义与模组。

因此不能用它验证武器、盔甲、建筑 JSON，也不能把它的成功记录成这些内容已经加载通过。

## 四、测试程序与现有自动行为测试

### 测试程序是独立的构建产物

测试用例位于 `tests/*.cpp`，框架是仓库所用的 Catch2。Makefile 默认 `TESTS=1`，构建测试目标；CMake 的 `TESTS` 默认开启，`tests/CMakeLists.txt` 还受 `BUILD_TESTING` 控制：

| 构建配置 | 测试目标 |
|---|---|
| Makefile | `tests/cata_test`，Windows 构建扩展名随工具链而定 |
| CMake + CURSES | `cata_test` |
| CMake + TILES | `cata_test-tiles` |
| Visual Studio | `msvc-full-features/Cataclysm-test-vcpkg-static.vcxproj` 测试工程 |

测试程序链接游戏实现并运行真实逻辑，不是对 JSON 文本做另一轮简单扫描。当前工作区未找到测试可执行文件；不能直接把已有 `cataclysm-tiles.exe` 当成 `cata_test` 使用。构建需要沿用项目对应平台的依赖与配置，本次未重新编译。

### 只加载数据，也可以不运行任何用例

`build-scripts/gha_test_only.sh` 已采用以下方法检查模组数据。假设测试程序位于 `tests/cata_test.exe`，在仓库根目录执行：

```powershell
.\tests\cata_test.exe '~*' --mods=my_mod --user-dir=./test_user_dir/my_mod/
```

`~*` 排除所有测试用例，但 `tests/test_main.cpp` 在运行 Catch2 会话之前仍会初始化游戏、加载数据和整理定义。它还会自动添加 `dda`（若未指定）与 `test_data`。这比单纯 JSON 解析更接近真实加载，但包含专用测试数据，并非普通玩家世界的完全等价环境。

联合加载示例：

```powershell
.\tests\cata_test.exe '~*' --mods=mod_a,mod_b --user-dir=./test_user_dir/combined/
```

这里参数用逗号分隔，顺序会传入测试世界。应把实际所需依赖与顺序纳入组合，不要据此假定测试程序会替任意模组列表自动补全所有依赖。游戏正常建世界时也需要选择并解析依赖。

测试主程序会把初始化中记录的 ERROR、测试中记录的 ERROR 和断言失败计为失败。没有用例执行时，不能把输出中“无测试匹配”解释成加载步骤也没有运行；更不能把它记成行为测试通过。

### 按标签或名称运行已有测试

先以实际构建产物的 `--help` / `--list-tests` 查看支持项和测试名称。以下用法由当前仓库中的测试标签和名称对应：

```powershell
.\tests\cata_test.exe --list-tests '[coverage]'
.\tests\cata_test.exe '[coverage]' --mods=my_mod --rng-seed 12345
.\tests\cata_test.exe '[encumbrance]' --mods=my_mod --rng-seed 12345
.\tests\cata_test.exe '[pocket]' --mods=my_mod --rng-seed 12345
.\tests\cata_test.exe '[throwing]' --mods=my_mod --rng-seed 12345
.\tests\cata_test.exe 'mapgen_place_vehicles' --mods=my_mod --rng-seed 12345
```

如果产物叫 `cata_test-tiles.exe`，相应替换程序路径。固定 `--rng-seed` 有利于复现；测试监听器会在 section 开始的回调中将游戏 RNG 设为 Catch2 的种子。需要检查概率行为时还应更换种子或做足够样本的统计，单一种子成功并不覆盖所有结果。

已有测试提供了这些可借用的基础：

| 内容 | 现有文件与例子 | 覆盖边界 |
|---|---|---|
| 物品一般属性 | `tests/item_test.cpp`：体积、长度、材料密度、容器生成 | 部分用例遍历全部已加载物品，部分只测试固定 ID |
| 护甲 | `tests/coverage_test.cpp`：近战/弹道覆盖、材料比例；`tests/encumbrance_test.cpp`：叠层、插板、口袋累赘 | 主要使用预定装备与测试数据，不会自动验证每件新甲 |
| 护甲穿戴规则 | `tests/item_test.cpp` 的 `rigid_armor_compliance`、`module_inheritance` | 断言特定刚性装备、左右侧与模组行为 |
| 口袋与刀鞘 | `tests/item_pocket_test.cpp`：最大长度、体积、重量相关容纳、白名单、holster | 应对新物品补充实际配对条件，不能只跑通用标签就认为新刀鞘正确 |
| 近战 | `tests/melee_test.cpp`、`tests/melee_dodge_hit_test.cpp` | 命中、闪避、伤害与战斗场景；部分基准用例为隐藏测试 |
| 射击与投掷 | `tests/ranged_balance_test.cpp`、`tests/throwing_test.cpp` | 命中分布、射击与投掷场景；不是新弓箭的自动平衡判定器 |
| mapgen | `tests/mapgen_place_vehicles_test.cpp`、移除载具/NPC 的相应用例 | 可运行 nested/update mapgen 并检查结果，主要测试指定生成器 |
| 大地图生成 | `tests/overmap_test.cpp` | 放置、生成成功率和 OMT 出现情况，不等于检查每栋建筑内部可通行或楼梯接通 |

不要只按文件名推断覆盖范围。例如 `mapgen_function_test.cpp` 当前测试的是下水道连接方向判断，并非遍历所有建筑生成。名为 `overmap_terrain_coverage` 的测试统计大地图地形出现情况，也不验证每张局部房屋布局。

Catch2 的隐藏标签如 `[.]`、`[.melee]` 不会因普通默认运行就全部执行；需要按实际名称或标签显式选择。没有标签的 mapgen 用例也不能指望用 `[mapgen]` 一次选全。

### 新内容的专用断言需要编写用例

若要自动证明“新甲覆盖左臂、右臂不覆盖”“某柄剑能放进指定刀鞘”“某栋房屋的门与楼梯位于预期位置”，现有入口可以承载这种测试，但必须有对应 C++ 断言。

基本方式是清理角色和地图状态，按 ID 创建物品或执行生成器，先用 `REQUIRE` 确认前提，再用 `CHECK` 检查结果。涉及随机伤害或覆盖率，应参考现有统计测试，而不是一次攻击后断言固定伤害。

地图测试已有 `tests/mapgen_helpers.h/.cpp` 的 `manual_update_mapgen()`、`manual_nested_mapgen()` 和 `manual_mapgen()`。可以参考 `mapgen_place_vehicles_test.cpp` 先清图、运行生成器，再断言地图上的结果。普通建筑还需设置 OMT 及相应环境后执行生成；不存在通用的“给一个 JSON 文件就自动检查房屋是否合理”的现成命令。

测试程序默认使用 `./test_user_dir/`，可以显式指定独立目录。断言失败时会尝试保存测试世界供游戏内检查，`-D` / `--drop-world` 可禁止保留。初始化直接失败、或仅由最终错误状态判定失败的路径，不应假定一定留下可检查的存档。

## 五、游戏内 GM / debug 测试

### 进入方法与基本环境

`data/raw/keybindings.json` 定义了两个不同动作：`debug`（Debug menu）和 `debug_mode`（Toggle debug mode），都没有在默认定义中绑定按键。进入按键设置，找到“Debug menu / 调试菜单”，自行绑定，例如 F12。切换 debug mode 主要用于调试显示与过滤，它和打开完整菜单不是同一动作。

可以新建启用目标模组的测试世界，角色命名为以 `Debug` 开头的名字；游戏自带文档说明这类角色可免去普通调试菜单的成就禁用提示。测试前确认世界启用的是目标模组。

菜单入口以 `src/debug_menu.cpp` 的英文名称为依据，中文翻译可能不同。下面列的是已核实能力和可采用的验证方式，不表示本次已逐一进行游戏操作。

### 物品、武器、护甲与关联行为

| 入口 | 可以做什么 |
|---|---|
| `Spawning → Spawn an item` | 生成新物品、配套弹药、刀鞘、材料或状态转换目标 |
| `Spawning → Spawn monster` / `Spawn NPC` | 提供战斗目标或测试 NPC 的装备与行动 |
| `Player` 的角色编辑 | 修改技能、属性、熟练度、生命、体力、疼痛与需求等条件 |
| `Quick setup` | 快速准备测试角色；涉及实际伤害比较时仍要确认引入了哪些调试状态 |
| `Info → Test item group` | 测试物品组产出，区别于直接生成单件物品 |
| `Game → Activate EOC` | 手动触发 EOC，适合检查相关事件逻辑；还需另外验证正常触发条件 |

生成物品后，应通过正常玩家操作实际使用。物品信息能确认显示数值与描述，但验证穿戴限制、格挡、攻击距离、装填、抽取、收纳与状态切换，需要操作相应动作。

可按修改涉及的行为选择检查项目：

- 武器：持握和双手条件、普通与长距离攻击、投掷、射击或装填、技巧触发、收纳与取出、工具用途、展开与收起。
- 护甲：覆盖部位和左右侧、穿脱与叠层、刚性冲突、空载及装载后的累赘、口袋限制、插板、开合或供电状态，以及受击表现。
- 关联数据：从物品组或建筑实际获得物品，按配方制造或拆解，NPC 是否能穿戴或使用。直接生成物品不能证明这些获取和使用路径成立。

只检查修改实际涉及的行为，不要求每件简单物品执行全部项目。比较数值时固定属性、技能、武术、装备、疼痛、体力、距离和目标状态，重复多个样本。新生成的怪物比旧存档中的怪物更适合检查定义变更；自带测试文档明确指出已生成并保存的怪物会保留原有状态。

仓库带有 `data/mods/Standard_Combat_Tests/modinfo.json`，模组 ID 为 `standard_combat_test`，提供早期、中期和后期角色装备及场景。它是方便人工比较的标准配置，不是后台自动战斗程序；用于中世纪装备时也不能直接视为项目平衡标准。

### 地形、家具、单栋建筑与建筑群

`Map` 菜单中的工具有不同作用：

| 工具 | 适用对象与能力 |
|---|---|
| `Map editor` | 编辑局部 terrain、furniture、陷阱、场、物品和生物；其 mapgen 子功能能生成预览 |
| 地图编辑器的 mapgen 预览 | `Regenerate`、`Rotate`、`Apply`、`Change Overmap (Doesn't Apply)` |
| `Overmap editor` | 放置单个 OMT 或整个 overmap special，适合多地块建筑和建筑群 |
| `Spawn nested mapgen` | 直接选择 nested mapgen ID，在指定位置运行嵌套生成器 |
| `Spawn map extra` | 运行地图额外事件；定义采用 update mapgen 时可经此测试其包装入口 |
| `Teleport`、修改时间/天气、显示光照等 | 到达目标地块，设置环境并观察遮蔽、视线等效果 |

局部编辑器通过 `EDIT_OVERMAP` 动作进入 mapgen 选择与预览，具体按键以当前帮助为准。`Change Overmap (Doesn't Apply)` 只改 OMT 身份；要实际替换地面内容，需要 `Apply`。

大地图编辑器会高亮已生成局部内容的区域，并明确提示：这些位置修改 OMT ID 不会替换已有内容。放置 special 后去旧地图查看，可能看到旧房屋。测试新生成建筑应选未生成区域，或明确通过局部编辑器应用生成结果。

还需要区分两种旋转：预览的 `Rotate` 可以旋转已经生成的结果，不能据此证明生成器 JSON 自身的 rotation、邻居条件或多层联动正确。嵌套生成器的直接生成也不一定复现正式调用处提供的参数、偏移和邻居环境。

完整建筑应在实际放置环境中检查布局、方向、出入口、相邻地块连接、楼梯与上下层、屋顶、物品和生物生成，以及设计中存在的随机变体。地形家具则通过正常开关、撬动、砸毁、拆解、攀爬、遮蔽或其他对应交互检查行为。直接画出墙或家具只证明该地块能放置，不能证明相关操作实现正确。

当前完整 Map 菜单没有按任意 `update_mapgen_id` 直接选择并执行的通用入口。可以从原本的 map extra、EOC 或任务等触发路径测试，或使用 C++ 测试 helper。不能把 `Spawn nested mapgen` 当作 update mapgen 的入口。

### 修改 JSON 后要重新加载定义与测试对象

游戏自带 `doc/TESTING_YOUR_CHANGES.md` 建议退回主菜单再加载存档，或重启游戏。`game::setup()` 会重新加载核心和世界模组；这与仅刷新贴图不同。为了让测试环境更明确，重新启动后再生成测试对象最容易确认使用了新定义。

已经生成的地图内容不会因为修改 mapgen 文件而自动重建；应使用新地块或重新应用生成结果。物品和生物也可能带有保存下来的状态，因此修改定义后应重新生成对象，并避免把旧损坏、旧装载或旧状态当成新定义的结果。

## 六、当前工作区实测与后续 skill 可采用的层次

### 已执行与尚未执行的边界

本次使用本地 `cataclysm-tiles.exe`：

- `--help` 可用，包含 `--check-mods`、`--jsonverify`、`--datadir` 与 `--userdir`。
- 在系统临时目录建立独立用户目录及 `config` 后，运行 `--check-mods dda`，进程退出码为 **0**，stdout 为 `Checking mod Dark Days Ahead [dda]`，stderr 为空，debug.log 无 ERROR。
- 日志报告版本为 `0.H-RELEASE-24-gea81dc9fb1`，与所调查的提交后缀对应；日志有缺少 `lang/mo/` 的 WARNING，未造成这次数据检查失败。
- 未找到 `cata_test*.exe` 或格式化器可执行文件，因此本次没有运行 Catch2 用例或原版格式化器。
- 没有提取并安装其他编写指南中的教学示例，没有进行游戏内生成、穿戴、战斗或地图预览操作。游戏内能力来自源码和自带文档核实。

现有 `json_data_system.md` 的 5.4 节已经提到命令行检查，但其中引用的 `msvc-full-features/check_with_wait.ps1` 在当前工作区未找到，不能直接照抄调用。该节“所有的 JSON 语法错误与语义引用警告均在此命令中触发”的描述也应按前述覆盖边界理解，不能扩展成所有运行行为都有检查。

### 适合写进 JSON 编写 skill 的验证结构

后续编写 skill 时，可以按修改性质选择以下层次，记录实际执行到了哪一步：

1. **文件层**：确认完整 JSON 能解析，必要时按原版工具格式化。
2. **加载层**：对目标模组运行 `--check-mods`，收集进程结果与日志；涉及模组组合时按实际加载组合再验证。
3. **行为层**：针对变更选择已有 C++ 用例、专用断言或游戏内调试操作。
4. **实际路径**：涉及生成、获取、触发或地图放置时，经正常入口再走一次，避免只测试手动生成的孤立对象。

前三份编写指南中的“示例语法解析通过”属于第一层。第二层和第三层的能力已经存在，但当前没有一套会自动提取教学片段、安装为测试模组并替每个预期行为生成断言的统一工具。是否将这些步骤固化到具体 skill，应在后续明确实施时处理。

## 七、源码与文档导航

| 依据 | 查阅内容 |
|---|---|
| [游戏入口](../../src/main.cpp) | CLI 选项、test mode、跳过界面、检查退出状态 |
| [游戏数据加载](../../src/game.cpp) | `load_static_data`、`check_mod_data`、`setup`、`load_world_modfiles` |
| [加载后检查](../../src/init.cpp) | finalize 与各系统一致性检查注册 |
| [调试日志](../../src/debug.cpp) | test mode 不弹窗、ERROR 状态记录 |
| [测试主程序](../../tests/test_main.cpp) | 自定义参数、模组列表、种子、初始化、失败存档与退出码 |
| [测试 CMake 配置](../../tests/CMakeLists.txt) | 测试目标与 CTest 入口 |
| [CI 测试脚本](../../build-scripts/gha_test_only.sh) | 按标签分组、模组组合和 `~*` 加载检查 |
| [调试菜单](../../src/debug_menu.cpp) | 生成、角色编辑、地图、EOC 与信息菜单 |
| [局部地图编辑器](../../src/editmap.cpp) | mapgen 预览、重掷、旋转与应用 |
| [大地图编辑器](../../src/overmap_ui.cpp) | OMT/special 放置与已生成区域提示 |
| [地图测试 helper](../../tests/mapgen_helpers.cpp) | nested/update mapgen 的非交互执行 |
| [原版测试说明](../../doc/TESTING.md) | Catch2 用例、状态隔离、REQUIRE/CHECK |
| [原版改动验证说明](../../doc/TESTING_YOUR_CHANGES.md) | JSON 重载、debug 菜单、地图与怪物测试 |
