import os
import subprocess
import logging
from cli_interface.message_maker import MessageMaker

class RetroactiveCommit:
    def __init__(self):
        self.message_maker = MessageMaker()
        # Hardcoded limit for developer testing: Set to an integer to limit commits,
        # or None to process all commits.
        self.limit_commits = None  # Change this as needed

    def generate_commit_message(self):
        # Get a list of all commit hashes from oldest to newest
        commit_hashes = subprocess.check_output(
            ['git', 'rev-list', '--reverse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().split()

        # If limit_commits is set, slice the list to only include that many recent commits
        if self.limit_commits is not None:
            commit_hashes = commit_hashes[-self.limit_commits:]
            # We'll start the rebase from HEAD~limit_commits to only affect these commits
            rebase_point = f'HEAD~{self.limit_commits}'
        else:
            # If no limit is set, rebase from the root
            rebase_point = '--root'

        # Set GIT_SEQUENCE_EDITOR to automatically convert 'pick' to 'edit'
        env = os.environ.copy()
        env['GIT_SEQUENCE_EDITOR'] = 'sed -i -e "s/^pick /edit /"'

        # Start an interactive rebase silently
        if rebase_point != '--root':
            rebase_cmd = ['git', 'rebase', '-i', rebase_point]
        else:
            rebase_cmd = ['git', 'rebase', '-i', '--root']
        subprocess.run(
            rebase_cmd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        for commit_hash in commit_hashes:
            # Extract the diff for the commit
            diff = subprocess.check_output(
                ['git', 'show', commit_hash],
                stderr=subprocess.DEVNULL
            ).decode()

            # Extract old commit message for reference
            old_message = subprocess.check_output(
                ['git', 'log', '-1', '--pretty=%s', commit_hash],
                stderr=subprocess.DEVNULL
            ).decode().strip()

            # Generate a new commit message
            new_message = self.message_maker.generate_message(diff)

            # Attempt to preserve commit dates
            try:
                env['GIT_COMMITTER_DATE'] = subprocess.check_output(
                    ['git', 'log', '-1', '--format=%cD', commit_hash],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                env['GIT_AUTHOR_DATE'] = subprocess.check_output(
                    ['git', 'log', '-1', '--format=%aD', commit_hash],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
            except subprocess.CalledProcessError:
                logging.warning(
                    "Could not retrieve dates for commit %s. Using current date/time.",
                    commit_hash
                )

            if new_message:
                # Print the summary of what we're doing for this commit
                print(f"Amending commit {commit_hash}")
                print(f"Old message: {old_message}")
                print(f"New message: {new_message}\n")

                # Amend the commit silently
                subprocess.run(
                    ['git', 'commit', '--amend', '-m', new_message],
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            else:
                print(f"No new message generated for {commit_hash}, skipping amendment.\n")

            # Continue the rebase silently
            subprocess.run(
                ['git', 'rebase', '--continue'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

        print("All specified commits have been updated with new messages.")
        print("To apply these changes to your remote repository, use:\n")
        print("    git push --force\n")
        print(
            "Note: Force pushing rewrites history on the remote repository, "
            "so ensure this is safe to do."
        )
