# cli.py

"""
This script provides a command-line interface for generating commit messages 
and filtering git commit history.

Functions:
- load_environment(): Loads environment variables.
- main(): Handles user interactions for generating commit messages or filtering
 commits based on the provided command.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from rich import print as rich_print
from cli_interface.user_interface import UserInterface
from cli_interface.message_maker import MessageMaker
from git_scripts.git_diff_fetcher import GitDiffFetcher
from git_scripts.git_history_analyzer import GitHistoryAnalyzer
from git_scripts.retroactive_commit import RetroactiveCommit


def load_environment():
    """Load environment variables from .env file."""
    cwd = Path(os.getcwd())
    dotenv_path = cwd / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)
    else:
        rich_print("Error: OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)


def handle_commit_message(ui, args, git_fetcher):
    """Handle commit message generation and commit process."""
    changes = git_fetcher.get_staged_diff()
    if not changes:
        rich_print("No changes detected.")
        return

    # Map 'c' to 'complex' and 's' to 'simple'
    template_map = {'c': 'complex', 's': 'simple'}
    selected_template = template_map.get(args.template, 'simple')

    message_maker = MessageMaker(template=selected_template)

    commit_message = message_maker.generate_message(changes)

    while True:
        if not commit_message:
            ui.show_error("Failed to generate commit message.")
            return

        ui.display_commit_message(commit_message)

        user_input = ui.prompt_user_action()

        if user_input == 'a':
            # Commit the changes using the generated commit message
            try:
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                rich_print(f"Changes committed with message: {commit_message}")
            except subprocess.CalledProcessError as e:
                ui.show_error(f"Error committing changes: {e}")
            break
        if user_input == 'r':
            # Regenerate the commit message
            feedback = ui.prompt_feedback()
            commit_message = message_maker.generate_message(changes,
                feedback, old_message=commit_message)
        elif user_input == 'e':
            try:
                commit_message = ui.prompt_manual_edit()
            except Exception as e:
                print(e)
        elif user_input == 'q':
            rich_print("Quitting without committing changes.")
            break
        else:
            ui.show_error("Invalid input. Please try again.")


def handle_filter_commits(ui, args, git_analyzer):
    """Handle commit filtering based on provided criteria."""
    filtered_commits = git_analyzer.filter_commits(
        change_type=args.change_type,
        impact_area=args.impact_type
    )
    if filtered_commits:
        ui.display_commits_paginated(filtered_commits)
    else:
        rich_print("[bold red][bold red]No commits found matching the criteria." +
        "[/bold red][/bold red]")


def handle_retroactive_commit(retro_commit):
    """Handle the retroactive commit process."""
    try:
        retro_commit.generate_commit_message()
        # Notify the user to force push the changes
    except Exception as e:
        print(f"An error occurred during retroactive commit: {e}")


def main():  # pylint: disable=too-many-branches, too-many-statements
    load_environment()

    ui = UserInterface()
    args = ui.parse_args()

    git_fetcher = GitDiffFetcher()
    git_analyzer = GitHistoryAnalyzer()
    retro_commit = RetroactiveCommit()

    if args.command == 'commit':
        handle_commit_message(ui, args, git_fetcher)

    elif args.command == 'filter':
        handle_filter_commits(ui, args, git_analyzer)

    elif args.command == 'retro':
        handle_retroactive_commit(retro_commit)

    else:
        # If no command is provided, show help
        ui.parser.print_help()


if __name__ == "__main__":
    main()
