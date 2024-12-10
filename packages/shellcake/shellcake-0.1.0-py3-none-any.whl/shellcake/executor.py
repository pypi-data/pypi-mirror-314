# shellcake/executor.py

import os
import subprocess

class ShellCake:
    def __init__(self, sudo=False, verbose=True):
        """
        Initializes the shell executor.

        :param sudo: If True, executes commands with sudo when necessary.
        :param verbose: If True, prints commands and outputs.
        """
        self.sudo = sudo
        self.verbose = verbose

    def _print(self, message):
        if self.verbose:
            print(message)

    def shell(self, command, cwd=None):
        """
        Executes a shell command.

        :param command: The command to execute.
        :param cwd: The working directory where the command will be executed.
        :return: The output of the command.
        """
        if self.sudo and os.geteuid() != 0:
            self._print('  * Sudo Active')
            if 'cd' not in command and 'echo' not in command:
                command = f"sudo {command}"

        if cwd:
            self._print(f'  \033[1m* Cwd:\033[0m {cwd}')
        self._print(f'  \033[1m* Command:\033[0m {command}')

        env_vars = os.environ.copy()

        process = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            cwd=cwd, env=env_vars, universal_newlines=True
        )

        output = ""
        for line in process.stdout:
            self._print(line.strip())
            output += line

        process.wait()
        if process.returncode != 0:
            self._print(f"Error executing command: {command}")
            exit(process.returncode)

        return output
