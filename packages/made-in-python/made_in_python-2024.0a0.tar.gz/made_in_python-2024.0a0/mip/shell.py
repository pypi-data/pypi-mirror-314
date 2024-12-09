########################################################
# SHELL.PY                                             #
# Contains code for running shell commands from python #
########################################################

import subprocess
import os

open_shells = []


class Shell:
    def __init__(self, name: str = "bash", shell: str = "/bin/bash"):
        """
        Initializes a new shell with the executable specified in shell, with the name specified in name.

        Args:
            shell (str): The path to the executable to the shell (default bash)
            name (str): The name / identifier of the shell (default "bash")
        """
        self.shell_executable = shell
        self.name = name
        open_shells.append(self.name)
        self.process = subprocess.Popen(
            self.shell_executable,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        self.cwd_history = [os.getcwd()]  # Initialize with the current working directory

    def execute(self, command: str):
        """
        Executes a command in the shell and returns the result as a string.
        Args:
            command (str): The command to execute.
        """
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Shell is not initialized properly.")

        os.system(command)

    def cd(self, path: str):
        """
        Changes the current working directory of the shell.
        Args:
            path (str): The target directory to change to.
        """
        if not os.path.isdir(path):
            raise FileNotFoundError(f"The directory '{path}' does not exist.")
        # Change directory and update history
        os.chdir(path)
        self.cwd_history.append(os.getcwd())

    def __del__(self):
        """
        Terminates the shell and reverts to the initial working directory when the instance is deleted.
        """
        open_shells.remove(self.name)
        # Revert the working directory changes
        while len(self.cwd_history) > 1:
            previous_dir = self.cwd_history.pop()
            os.chdir(previous_dir)

        # Terminate the shell process
        if self.process:
            self.process.stdin.close()
            self.process.terminate()
            self.process.wait()