# Reference：L01 系统总览与核心目录

## 一句话总结

MiniAgentFlow 的主链路是：CLI 接收命令，Task 承载任务数据，Scheduler 负责任务调度，Executor 负责实际执行，State Store 保存状态。

## 核心模块职责

| 模块 | 职责 | 不负责什么 |
|---|---|---|
| `cli.py` | 接收命令、解析参数、创建任务 | 不负责调度策略 |
| `task.py` | 定义任务对象和任务数据 | 不负责执行 |
| `scheduler.py` | 决定任务何时进入执行 | 不直接调用工具 |
| `executor.py` | 执行任务、调用工具、产生结果 | 不负责长期状态保存策略 |
| `state/store.py` | 保存任务状态和结果 | 不决定任务如何执行 |

## 主链路

```text
User command -> CLI -> Task -> Scheduler -> Executor -> State Store
```

## 常见误区

1. Scheduler 不是 Executor。
2. State Store 不只是日志，也是后续恢复、调试和可观测性的基础。
3. 读源码不要只看入口文件，要追数据对象如何流动。

## 下一课连接

L02 将从 `src/miniflow/cli.py` 出发，追踪 CLI 如何创建任务并交给 Scheduler。
