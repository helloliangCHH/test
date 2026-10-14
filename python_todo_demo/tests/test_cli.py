from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "tasks.json"

    def run_cli(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT / "main.py"), "--data", str(self.data), *args],
            input=input_text,
            capture_output=True,
            encoding="utf-8",
            cwd=self.temp.name,
            timeout=10,
        )

    def test_commands_work_across_processes_and_directories(self):
        result = self.run_cli("add", "命令行测试任务")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("命令行测试任务", self.run_cli("list").stdout)
        self.assertEqual(self.run_cli("done", "1").returncode, 0)
        self.assertIn("已完成", self.run_cli("list").stdout)
        self.assertEqual(self.run_cli("delete", "1").returncode, 0)
        self.assertIn("暂无任务", self.run_cli("list").stdout)

    def test_invalid_input_returns_failure(self):
        self.assertEqual(self.run_cli("add", " ").returncode, 1)
        self.assertEqual(self.run_cli("done", "99").returncode, 1)
        self.assertEqual(self.run_cli("done", "abc").returncode, 2)

    def test_interactive_menu_handles_bad_input_and_saves_tasks(self):
        result = self.run_cli(input_text="9\n2\n菜单测试任务\n3\nabc\n3\n1\n1\n0\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("任务编号必须是整数", result.stdout)
        self.assertIn("[已完成] 菜单测试任务", result.stdout)
        self.assertIn("菜单测试任务", self.run_cli("list").stdout)


if __name__ == "__main__":
    unittest.main()
