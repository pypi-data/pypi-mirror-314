# git_scripts/git_diff_fetcher.py

import subprocess
import os

class GitDiffFetcher:
    def __init__(self):
        self.repo_path = os.getcwd()

    def get_staged_diff(self):
        try:
            staged_check = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            if not staged_check.stdout.strip():
                print("No staged changes found. Have you added your changes with 'git add'?")
                return None

            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                check=True
            )
            if not result.stdout.strip():
                print("Git diff command succeeded, but returned empty output.")
                return None
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}")
            print(f"Command output: {e.output}")
            print(f"Command stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_staged_diff: {e}")
            return None
