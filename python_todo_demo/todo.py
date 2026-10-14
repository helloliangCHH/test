"""待办事项与 JSON 存储，只使用 Python 标准库。"""

import json
from pathlib import Path


class TodoError(ValueError):
    """可以向用户直接展示的输入或数据错误。"""


class TodoStore:
    def __init__(self, data_file):
        self.data_file = Path(data_file)

    def _read(self):
        if not self.data_file.exists():
            return {"next_id": 1, "tasks": []}
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise TodoError("数据文件无法读取，请检查 JSON 内容；原文件已保留。") from exc
        if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
            raise TodoError("数据文件格式错误；原文件已保留。")
        next_id = data.get("next_id")
        if type(next_id) is not int or next_id < 1:
            raise TodoError("数据文件中的编号无效；原文件已保留。")
        ids = set()
        for task in data["tasks"]:
            if (
                not isinstance(task, dict)
                or type(task.get("id")) is not int
                or task["id"] < 1
                or task["id"] >= next_id
                or task["id"] in ids
                or not isinstance(task.get("title"), str)
                or not task["title"].strip()
                or type(task.get("completed")) is not bool
            ):
                raise TodoError("数据文件中的任务格式错误；原文件已保留。")
            ids.add(task["id"])
        return data

    def _write(self, data):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.data_file.with_name(self.data_file.name + ".tmp")
        temporary.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        temporary.replace(self.data_file)

    def list_tasks(self):
        return self._read()["tasks"]

    def add(self, title):
        title = title.strip()
        if not title:
            raise TodoError("任务内容不能为空。")
        data = self._read()
        task = {"id": data["next_id"], "title": title, "completed": False}
        data["tasks"].append(task)
        data["next_id"] += 1
        self._write(data)
        return task

    @staticmethod
    def _find(data, task_id):
        for task in data["tasks"]:
            if task["id"] == task_id:
                return task
        raise TodoError(f"未找到编号为 {task_id} 的任务。")

    def complete(self, task_id):
        data = self._read()
        task = self._find(data, task_id)
        task["completed"] = True
        self._write(data)
        return task

    def delete(self, task_id):
        data = self._read()
        task = self._find(data, task_id)
        data["tasks"].remove(task)
        self._write(data)
        return task
