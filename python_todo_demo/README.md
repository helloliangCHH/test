# Python 待办事项测试项目

一个适合练习运行、调试和自动化测试的小型 Python 项目。支持添加、查看、完成、删除任务，并通过本地 JSON 文件保存数据。

## 快速启动（Windows）

1. 打开 `python_todo_demo` 文件夹。
2. 双击 `run.bat`。
3. 按菜单输入数字，例如输入 `2` 添加任务，输入 `1` 查看任务，输入 `0` 退出。

双击 `run_tests.bat` 可运行全部 12 项自动化测试。显示 `OK` 代表通过。测试使用临时文件，不会修改你的任务数据。

启动脚本会依次尝试系统的 `py -3`、`python` 和当前电脑的 Codex 内置 Python。项目仅使用标准库，无需安装第三方依赖。若三个环境均不可用，请安装 Python 3.9 或更新版本。

## 命令行用法

在项目文件夹中打开终端。以下命令适用于系统已配置 `python` 的情况：

```powershell
python main.py
python main.py add "测试我的 Python 环境"
python main.py list
python main.py done 1
python main.py delete 1
python -m unittest discover -s tests -v
```

任务编号从 1 开始。删除后不会重复使用旧编号。包含空格的任务内容请使用引号。

可以指定独立的数据文件，便于隔离测试；`--data` 应写在子命令前：

```powershell
python main.py --data data/demo.json add "独立测试"
python main.py --data data/demo.json list
```

## 项目结构

```text
python_todo_demo/
├── main.py             # 菜单和命令行入口
├── todo.py             # 任务操作与文件存储
├── run.bat             # 双击启动
├── run_tests.bat       # 双击运行测试
├── scripts/python.bat  # 自动选择可用的 Python
├── tests/
│   ├── test_todo.py    # 存储、状态、异常输入测试
│   └── test_cli.py     # 命令行和菜单测试
├── data/               # 首次添加后生成 tasks.json
├── .gitignore
└── README.md
```

## 建议的手动测试

1. 添加中文任务，查看任务列表。
2. 标记任务为完成，退出后重新打开，确认数据保留。
3. 删除任务，再添加新任务，确认编号继续递增。
4. 尝试空内容、不存在的编号和非数字编号，观察错误提示。

默认数据始终保存在项目目录中的 `data/tasks.json`。删除该文件可清空全部任务并重置编号；请先退出程序。遇到损坏的数据文件时，程序会提示错误并保留原文件。

这是供本地单进程测试使用的演示项目。请避免同时打开多个窗口修改同一个数据文件。
