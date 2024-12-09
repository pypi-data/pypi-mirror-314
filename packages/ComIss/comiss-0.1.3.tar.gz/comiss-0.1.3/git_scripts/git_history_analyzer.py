# git_scripts/git_history_analyzer.py

import subprocess
import re

class GitHistoryAnalyzer:
    def __init__(self):
        pass

    def filter_commits(self, change_type=None, impact_area=None):
        try:
            # Fetch the git log with commit hash, author, date, and subject
            git_log_output = subprocess.check_output(
                ["git", "log", "--pretty=format:%H%n%an%n%ad%n%s%n---"],
                universal_newlines=True
            )

            # Split the log into individual commits
            commits = git_log_output.strip().split('---\n')
            filtered_commits = []

            for commit in commits:
                lines = commit.strip().split('\n')
                if len(lines) >= 4:
                    commit_hash = lines[0]
                    author = lines[1]
                    date = lines[2]
                    subject = lines[3]

                    # Parse the subject to extract change_type and impact_area
                    match = re.match(r"^\s*(?P<ChangeType>\w+)\s*\|\s*(?P<ImpactArea>[\w\s]+):",
                                     subject)
                    if match:
                        commit_change_type = match.group('ChangeType').lower()
                        commit_impact_area = match.group('ImpactArea').lower()

                        # Apply filters
                        if change_type and commit_change_type != change_type.lower():
                            continue
                        if impact_area and commit_impact_area != impact_area.lower():
                            continue

                        # Add the commit to the filtered list
                        filtered_commits.append({
                            'hash': commit_hash,
                            'author': author,
                            'date': date,
                            'subject': subject
                        })
                else:
                    # Handle malformed commit entries
                    print(f"Skipping malformed commit entry:\n{commit}")

            return filtered_commits

        except Exception as e:
            print(f"Unexpected error in filter_commits: {e}")
            return []
