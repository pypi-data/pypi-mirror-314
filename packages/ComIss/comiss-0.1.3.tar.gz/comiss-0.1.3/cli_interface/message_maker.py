"""
The message_maker module provides the MessageMaker class,
which generates commit messages based on the changes
detected in the codebase and user feedback.
"""

from openai_integration.prompt_builder import PromptBuilder
from openai_integration.gpt_client import GPTClient
from openai_integration.response_processor import ResponseProcessor

"""
The MessageMaker class is responsible for generating commit messages
based on the changes detected in the codebase and user feedback. 
It uses the PromptBuilder to construct prompts for the GPT-3 model, 
the GPTClient to interact with the OpenAI API, 
and the ResponseProcessor to process the model's response
into a valid commit message.
"""
class MessageMaker:
    def __init__(self, template='simple'):
        self.prompt_builder = PromptBuilder(template)
        self.gpt_client = GPTClient()
        self.response_processor = ResponseProcessor()

    def generate_message(self, changes, feedback=None, old_message=None):
        prompt = self.prompt_builder.construct_prompt(changes, feedback, old_message)
        raw_response = self.gpt_client.send_prompt(prompt)
        commit_message = self.response_processor.process_response(raw_response)
        return commit_message
    