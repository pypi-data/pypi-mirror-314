# openai_integration/prompt_builder.py

import textwrap

class PromptBuilder:
    def __init__(self, template='simple'):
        self.template = template

    def construct_prompt(self, changes, feedback=None, old_message=None):
        # Base instructions
        base_instructions = textwrap.dedent("""
            You are an AI assistant tasked with generating commit messages based strictly on the provided git diff changes.
            Please adhere to the following instructions carefully and do not deviate from the format or include any additional information.

            **Format:**
            <ChangeType> | <ImpactArea>: <TLDR>

            **Instructions:**
            - **ChangeType**: Select **only one** from [feature, bugfix, refactor, docs, test, chore].
            - **ImpactArea**: Specify the affected part of the project (e.g., 'frontend', 'backend', 'database', 'user interface').
            - **TLDR**: Write a concise, one-line summary of the changes in imperative mood (e.g., 'Fix crash when user inputs empty string').
            - Do not include any details beyond the TLDR unless instructed.
            - Ensure that each line in the detailed description does not start with extra spaces.
            - **Do not** add any sections or information not specified in the format.
            - Regardless of how many changes are detected, produce exactly ONE single commit message line.
            - Do not produce multiple commit message headers. Only one "<ChangeType> | <ImpactArea>: <TLDR>" line is allowed.
        """)

        # Updated detailed prompt descriptions
        detailed_instructions = ""
        if self.template == 'complex':
            detailed_instructions = textwrap.dedent("""
                After the TLDR line, start a new line and provide a single detailed description
                summarizing all changes together. This detailed description should clearly explain:
                - What was changed
                - Why it was changed

                Even if multiple changes are provided in the diff, combine them into one cohesive commit.
                Do not create multiple commit headers. Do not list separate changes as separate commits.
                Provide one TLDR line and one optional detailed section.

                **Do Not:**
                - Produce multiple lines that start with "<ChangeType> | <ImpactArea>:" for the same commit.
                - Include extra headers or multiple separate summaries.

                **If Multiple Changes are Provided:**
                - Combine them into a single TLDR and a single, cohesive detailed description block.
            """)

        # Combine base instructions with conditional detailed instructions
        base_prompt = f"{base_instructions}\n{detailed_instructions}\n"

        # Examples section demonstrating single-line commits
        examples = textwrap.dedent("""
            **Examples:**
            feature | backend: Add user authentication module
            bugfix | frontend: Fix alignment issue on login page
            refactor | database: Optimize query performance

            **Multiple Changes Example:**
            Suppose the diff shows changes to a backend function and a frontend file.
            Combine them into a single commit message:
            
            refactor | backend: Improve API response handling
            
            (For complex template)
            Detailed Description:
            Update the API endpoint to return clearer error messages and adjust the frontend code
            to handle the new response format. This ensures users receive more accurate feedback
            and improves overall user experience.
        """).strip()

        base_prompt += "\n\n" + examples + "\n"

        # Git Diff Changes section
        git_diff_section = textwrap.dedent(f"""
            **Git Diff Changes:**
            ```
            {changes}
            ```
        """)

        user_message = git_diff_section

        # If feedback and old_message are provided, include them
        if feedback and old_message:
            previous_commit = textwrap.dedent(f"""
                
                **Previous Commit Message:**
                {old_message}

                **User Feedback:**
                {feedback}
                Please revise the commit message accordingly, strictly following the format and instructions.
            """)
            user_message += previous_commit

        # Combine base_prompt with user_message
        full_prompt = f"{base_prompt}{user_message}"

        return full_prompt
