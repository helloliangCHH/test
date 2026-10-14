import json
from pathlib import Path
import tempfile
import unittest

from todo import TodoError, TodoStore


class TodoStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "data" / "tasks.json"
        self.store = TodoStore(self.path)

    def test_new_store_is_empty(self):
        self.assertEqual(self.store.list_tasks(), [])
        self.assertFalse(self.path.exists())

    def test_add_is_saved_and_survives_restart(self):
        task = self.store.add("  测试中文任务  ")
        restarted = TodoStore(self.path)
        self.assertEqual(restarted.list_tasks(), [task])
        self.assertEqual(task["title"], "测试中文任务")
        self.assertFalse(task["completed"])
        self.assertIn("测试中文任务", self.path.read_text(encoding="utf-8"))

    def test_complete_is_saved_and_can_be_repeated(self):
        task = self.store.add("测试完成")
        self.store.complete(task["id"])
        self.store.complete(task["id"])
        self.assertTrue(TodoStore(self.path).list_tasks()[0]["completed"])

    def test_delete_preserves_other_tasks(self):
        first = self.store.add("第一条")
        second = self.store.add("第二条")
        self.store.delete(first["id"])
        self.assertEqual(TodoStore(self.path).list_tasks(), [second])

    def test_ids_are_not_reused_after_deletion(self):
        first = self.store.add("第一条")
        self.store.delete(first["id"])
        second = self.store.add("第二条")
        self.assertGreater(second["id"], first["id"])

    def test_blank_title_does_not_change_data(self):
        self.store.add("已有任务")
        original = self.path.read_bytes()
        with self.assertRaises(TodoError):
            self.store.add("  \t ")
        self.assertEqual(self.path.read_bytes(), original)

    def test_missing_task_does_not_change_data(self):
        self.store.add("已有任务")
        original = self.path.read_bytes()
        for operation in (self.store.complete, self.store.delete):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(TodoError):
                    operation(999)
                self.assertEqual(self.path.read_bytes(), original)

    def test_corrupt_json_is_preserved(self):
        self.path.parent.mkdir()
        self.path.write_text("{broken json", encoding="utf-8")
        original = self.path.read_bytes()
        with self.assertRaises(TodoError):
            self.store.add("不应写入")
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_schema_is_preserved(self):
        self.path.parent.mkdir()
        invalid_documents = [
            [],
            {"next_id": 0, "tasks": []},
            {"next_id": 2, "tasks": [{"id": 1, "title": "任务", "completed": "yes"}]},
            {"next_id": 1, "tasks": [{"id": 1, "title": "任务", "completed": False}]},
            {"next_id": 2, "tasks": [
                {"id": 1, "title": "任务一", "completed": False},
                {"id": 1, "title": "任务二", "completed": False},
            ]},
        ]
        for document in invalid_documents:
            with self.subTest(document=document):
                self.path.write_text(json.dumps(document), encoding="utf-8")
                original = self.path.read_bytes()
                with self.assertRaises(TodoError):
                    self.store.add("不应写入")
                self.assertEqual(self.path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
