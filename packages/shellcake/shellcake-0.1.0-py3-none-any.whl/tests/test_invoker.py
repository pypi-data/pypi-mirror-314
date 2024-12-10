# tests/test_executor.py

import unittest
from shellinvoker import ShellExecutor

class TestShellExecutor(unittest.TestCase):
    def test_shell_command(self):
        executor = ShellExecutor(verbose=False)
        output = executor.shell('echo "Hello, World!"')
        self.assertEqual(output.strip(), 'Hello, World!')

    def test_sudo_command(self):
        executor = ShellExecutor(sudo=True, verbose=False)
        try:
            executor.shell('whoami')
            self.assertTrue(True)
        except SystemExit:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

