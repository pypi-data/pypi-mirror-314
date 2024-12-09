# openai_integration/gpt_client.py

import os
import time
import logging
import openai

class GPTClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Ensure this is the correct model name
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def send_prompt(self, prompt):
        for _ in range(1, self.max_retries + 1):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": prompt}
                    ],
                    max_tokens=2000,
                )
                return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                logging.warning("Rate limit exceeded. Retrying in %d seconds...", self.retry_delay)
                time.sleep(self.retry_delay)
            except openai.error.OpenAIError as e:
                logging.error("OpenAI API error: %s", e)
                break
            except Exception as e:
                logging.error("Unexpected error: %s", e)
                break
        return None
