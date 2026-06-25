# SOURCE-READING-MAP：源码阅读地图

> 这是按学习主线排序的源码阅读地图，不是机械列目录。

## 第一优先级：主入口与主链路

| 顺序 | 路径 | 阅读目的 | 对应课程 |
|---|---|---|---|
| 1 | `src/miniflow/cli.py` | 找到 CLI 命令入口和参数解析 | L02 |
| 2 | `src/miniflow/core/task.py` | 理解任务对象的数据结构 | L03 |
| 3 | `src/miniflow/core/scheduler.py` | 理解任务如何进入调度 | L02 / L04 |
| 4 | `src/miniflow/core/executor.py` | 理解任务如何被执行 | L05 |
| 5 | `src/miniflow/state/store.py` | 理解状态如何保存 | L03 / L07 |

## 第二优先级：扩展点

| 路径 | 阅读目的 | 对应课程 |
|---|---|---|
| `src/miniflow/tools/registry.py` | 工具如何注册和查找 | L06 |
| `src/miniflow/tools/builtin.py` | 内置工具示例 | L08 |
| `src/miniflow/config.py` | 配置如何影响运行 | L09 |

## 暂不阅读

| 路径 | 原因 |
|---|---|
| `tests/` | 第一阶段先建立主链路，测试在实现课中回看 |
| `docs/` | 作为辅助，不作为源码主线 |
| `examples/` | 等进入实现课再看 |

创建时间：2026-06-25
