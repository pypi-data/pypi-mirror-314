# cli_interface/user_interface.py

import argparse
import sys
from rich import print
from rich.table import Table
import click


class UserInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="CLI tool to generate and manage commit messages."
        )
        self._setup_arguments()

    def _setup_arguments(self):
        subparsers = self.parser.add_subparsers(dest='command', help='Commands')

        # Commit command
        commit_parser = subparsers.add_parser('commit', help='Generate and commit a message.')
        commit_parser.add_argument(
            '-m', '--template',
            choices=['c', 's'],  # 'c' for complex, 's' for simple
            default='s',
            help='Select the commit message template complexity.' +
                 '(c: complex, s: simple) (Default: s)'
        )

        # Filter command
        filter_parser = subparsers.add_parser('filter', help='Filter commit history.')
        filter_parser.add_argument(
            '-c', '--change-type',
            type=str,
            help='Filter by change type (e.g., feature, bugfix).'
        )
        filter_parser.add_argument(
            '-i', '--impact-type',
            type=str,
            help='Filter by impact area (e.g., frontend, backend).'
        )

        # Retro command
        subparsers.add_parser('retro', help='Generate retroactive commit messages.')

    def parse_args(self):
        return self.parser.parse_args()

    def display_commit_message(self, commit_message):
        print(f"\nGenerated commit message:\n{commit_message}")

    def prompt_user_action(self):
        return input("\nDo you want to (a)ccept this message," +
                     " (r)egenerate, (e)dit, or (q)uit? ").lower()

    def prompt_feedback(self):
        return input("Please provide feedback for regeneration (or press Enter to skip): ")

    def prompt_manual_edit(self):
        # Ask user for change type
        change_type = self.prompt_change_type()

        # Ask user for impact area
        impact_area = self.prompt_impact_area()

        # Ask user for commit message
        commit_message = self.prompt_commit_message()

        return f"{change_type} | {impact_area}: {commit_message}"

    def prompt_change_type(self):
        change_type_short = input("Select a change type: (f)eature, (b)ugfix, (r)efactor," +
        "(d)ocs, (t)est, (c)hore.\n")
        if change_type_short == 'f':
            return "feature"
        if change_type_short == 'b':
            return "bugfix"
        if change_type_short == 'r':
            return "refactor"
        if change_type_short == 'd':
            return "docs"
        if change_type_short == 't':
            return "test"
        if change_type_short == 'c':
            return "chore"
        # No need for an 'else' here since all options are checked.
        raise ValueError(f"{change_type_short} is not short for a valid change type.")

    def prompt_impact_area(self):
        return input("Specify an impact area (e.g., frontend, backend, UI).\n")

    def prompt_commit_message(self):
        return input("Specify a commit message.\n")

    def show_error(self, message):
        print(f"Error: {message}", file=sys.stderr)

    def display_commits_paginated(self, commits, page_size=5):
        table = Table(title="Filtered Commits")
        table.add_column("Hash", style="cyan", no_wrap=True)
        table.add_column("Subject", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Date", style="yellow")

        total_commits = len(commits)
        current_index = 0

        while current_index < total_commits:
            # Add rows for the next set of commits
            for i in range(current_index, min(current_index + page_size, total_commits)):
                commit = commits[i]
                table.add_row(
                    commit['hash'],
                    commit['subject'],
                    commit['author'],
                    commit['date']
                )

            # Print the updated table
            print(table)

            current_index += page_size

            # Check if there are more commits to show
            if current_index < total_commits:
                click.confirm("Press Enter to show more commits", default=True, abort=True)
            else:
                print("[bold green]End of commits list.[/bold green]")
