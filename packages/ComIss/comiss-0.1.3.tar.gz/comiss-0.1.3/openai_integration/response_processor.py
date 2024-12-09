# openai_integration/response_processor.py

import re

class ResponseProcessor:
    def __init__(self):
        pass

    def process_response(self, raw_response):
        if not raw_response:
            return None

        # Remove any leading/trailing whitespace from the entire response
        response_text = raw_response.strip()

        # Define the regex pattern to match the commit message format
        pattern = (
            r"^\s*(?P<ChangeType>feat|feature|bugfix|fix|refactor|docs|doc|test|tests|chore)"
            r"\s*\|\s*(?P<ImpactArea>[\w\s\-]+):\s*(?P<TLDR>.+?)(?:\n|$)"
        )

        # Match against the main components of the commit message
        match = re.match(pattern, response_text, re.IGNORECASE)

        if not match:
            # If the main components do not match, reject the input
            print("Generated commit message does not match the required format.")
            print("Response from GPT:\n", response_text)
            return None

        # Get the remaining text after the match without stripping
        remaining_text = response_text[match.end():]

        # Remove leading spaces and tabs but preserve newlines
        remaining_text_lstripped = remaining_text.lstrip(' \t')

        # Ensure there are no unexpected extra sections
        if remaining_text_lstripped and not remaining_text_lstripped.startswith("\n"):
            # If there's unexpected content beyond the matched portion, return None
            print("Generated commit message contains unexpected extra sections.")
            print("Response from GPT:\n", response_text)
            return None

        # Extract the summary components
        change_type = match.group('ChangeType').strip().lower()
        impact_area = match.group('ImpactArea').strip().lower()
        tldr = match.group('TLDR').strip()

        # Validate the impact area to ensure it's not missing or empty
        if not impact_area:
            print("Commit message is missing an impact area.")
            print("Response from GPT:\n", response_text)
            return None

        # Normalize ChangeType
        change_type_mapping = {
            'feat': 'feature',
            'fix': 'bugfix',
            'doc': 'docs',
            'tests': 'test',
        }
        change_type = change_type_mapping.get(change_type, change_type)

        # Build the commit message
        if remaining_text_lstripped.startswith("\n"):
            # There is a detailed description
            detailed_description = remaining_text_lstripped.lstrip('\n')

            # Normalize whitespace in the detailed description
            detailed_description_lines = detailed_description.split('\n')
            stripped_lines = (line.lstrip() for line in detailed_description_lines)
            detailed_description_normalized = '\n'.join(stripped_lines)

            # Build the final commit message
            commit_message = (
                f"{change_type} | {impact_area}: {tldr}\n\n"
                f"{detailed_description_normalized}"
            )
        else:
            # No detailed description
            commit_message = f"{change_type} | {impact_area}: {tldr}"

        return commit_message
