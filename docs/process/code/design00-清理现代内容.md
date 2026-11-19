# 清理现代内容的依赖查询工具

依据 [design00](../../design/design00-清理现代内容.md)。工具可导出全部声明、统计 ID、双向查询引用，并预览或执行指定定义的批量删除。游戏数据和源码以工具完成时的 `80827ae48d` 为基线。

在仓库根目录用 Python 3 运行。脚本使用标准库。查询入口见 [dependencies.py](../../../tools/json_tools/dependencies.py)，字段识别规则见 [dependency_rules.py](../../../tools/json_tools/dependency_rules.py)。

~~~sh
python3 tools/json_tools/dependencies.py stats --type item
python3 tools/json_tools/dependencies.py list --type GUN
python3 tools/json_tools/dependencies.py list --csv > definitions.csv
python3 tools/json_tools/dependencies.py query item:apple --depth 2
python3 tools/json_tools/dependencies.py delete item:usb_drive
~~~

- 默认数据范围是 data/core 和 data/json。使用多次 --root 可指定要扫描的文件、目录及顺序。默认数据范围会查 src 中的 C++ ID 字面量。指定数据根时，可以用 --code-root 指定对应源码。添加 --json 可得到结构化结果。
- stats 分别统计 JSON 声明、唯一 ID、抽象定义和匿名声明。query 按扫描顺序列出定义位置，显示双向引用的字段位置及可追溯的路径。--depth 设置查几层，--limit 0 输出全部查询结果。
- item:ID 用于查物品，其他对象可使用类型加 ID。list 默认列出全部声明，包含同名、抽象和匿名对象。CSV 包含定义位置、继承、名称、描述和删留记录列。list 和 query 显示 @文件#/数组下标，单对象文件使用 @文件#。
- delete 接受一个或多个选择项，默认预览。添加 --apply 写入本批删除，可同时选择彼此引用的对象。其余对象仍有已识别的引用时会阻止写入并列出位置，经确认有意保留这些引用时可以添加 --allow-dangling。工具按选择删除，不连带删除引用方。
- 删除保留剩余对象的文本和换行。平面 id 数组可以只删指定成员，二维 mapgen 等复合定义按完整声明处理。重复 ID 必须用位置消歧。批量写入失败时恢复已写入的文件。

当前已识别继承、物品组、地图生成、掉落与采收、配方和制作需求、部分职业与 NPC、事件与容器等字段。含动态值的已识别字段会标出，缺少目标定义的引用会标明。其他字段及运行时生成的引用需要在实际裁剪批次中继续核对。

基线的 data/core 和 data/json 有 2,774 个 JSON 文件和 47,047 条声明。原依赖工具测试验证了苹果采收链和 USB 任务引用、批量选择以及副本删除。补充用例覆盖全量和 CSV 导出、GM 清单比对及重复变体。回退后 17 项工具测试通过。

~~~sh
python3 -m unittest discover -s tools/json_tools -p 'test_*.py'
flake8 tools/json_tools/dependencies.py tools/json_tools/dependency_rules.py tools/json_tools/gm_items.py tools/json_tools/test_dependencies.py tools/json_tools/test_gm_items.py
~~~

## 已导出 GM 清单的离线核对

[gm_items.py](../../../tools/json_tools/gm_items.py)接收已有的 GM 目录 JSON。目录每行提供物品 ID、变体 ID 和显示名。工具可以生成可填写的 CSV，或用已有删留决定核对目录。出现拟移除项、未核对项或保留项缺失时，检查失败。

~~~sh
python3 tools/json_tools/gm_items.py gm-items.json > gm-items-review.csv
python3 tools/json_tools/gm_items.py gm-items.json --review tools/json_tools/medieval_gm_review.csv
~~~

[审核表](../../../tools/json_tools/medieval_gm_review.csv)保存首轮候选决定。记录供后续逐项核对和测试使用。游戏内导出入口随源码一并回退。
