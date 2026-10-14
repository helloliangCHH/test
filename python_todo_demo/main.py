"""直接运行进入菜单，也可使用 add/list/done/delete 命令。"""

import argparse
from pathlib import Path

from todo import TodoError, TodoStore


DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "tasks.json"


def show_tasks(store):
    tasks = store.list_tasks()
    if not tasks:
        print("暂无任务，先添加一条吧。")
        return
    for task in tasks:
        status = "已完成" if task["completed"] else "待完成"
        print(f"{task['id']:>3}  [{status}] {task['title']}")


def execute(store, command, value=None):
    if command == "list":
        show_tasks(store)
    elif command == "add":
        task = store.add(value)
        print(f"已添加任务 #{task['id']}：{task['title']}")
    elif command == "done":
        task = store.complete(value)
        print(f"已完成任务 #{task['id']}：{task['title']}")
    elif command == "delete":
        task = store.delete(value)
        print(f"已删除任务 #{task['id']}：{task['title']}")


def interactive(store):
    commands = {"1": "list", "2": "add", "3": "done", "4": "delete"}
    print("欢迎使用 Python 待办事项测试项目！")
    while True:
        print("\n1. 查看任务  2. 添加任务  3. 完成任务  4. 删除任务  0. 退出")
        choice = input("请选择：").strip()
        if choice == "0":
            print("已退出，任务数据已保存。")
            return 0
        if choice not in commands:
            print("请输入 0～4 之间的选项。")
            continue
        try:
            value = None
            if choice == "2":
                value = input("任务内容：")
            elif choice in ("3", "4"):
                try:
                    value = int(input("任务编号："))
                except ValueError:
                    raise TodoError("任务编号必须是整数。") from None
            execute(store, commands[choice], value)
        except (TodoError, OSError) as exc:
            print(f"操作失败：{exc}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="简单 Python 待办事项测试项目")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="指定 JSON 数据文件")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("list", help="查看全部任务")
    add = commands.add_parser("add", help="添加任务")
    add.add_argument("title", help="任务内容，包含空格时请加引号")
    for name, help_text in (("done", "完成任务"), ("delete", "删除任务")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("task_id", type=int, help="任务编号")
    args = parser.parse_args(argv)
    store = TodoStore(args.data)
    try:
        if args.command is None:
            return interactive(store)
        value = getattr(args, "title", getattr(args, "task_id", None))
        execute(store, args.command, value)
        return 0
    except (TodoError, OSError) as exc:
        print(f"操作失败：{exc}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\n已退出。")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
