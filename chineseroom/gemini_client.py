import os
import logging
from wsgiref import types
from dotenv import load_dotenv
from google import genai
from google.genai import types


class GeminiClient:
    """
    Client for interacting with Google's Gemini generative AI API.
    """

    def __init__(self, api_key: str = None, model_name: str = "gemini-2.5-flash"):
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not provided. Set GEMINI_API_KEY environment variable or .env file.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.logger = logging.getLogger(self.__class__.__name__)
        self.system_instruction = "You are a CLI tool and must respond with raw," \
            " unformatted, plain text only. Do not use any markdown, including" \
            " bolding, italics, headings, lists, or code blocks. Do not use any" \
            " special characters, emojis, or styling."

    def ask(self, prompt: str, **kwargs) -> str:
        """
        Send a prompt to the Gemini model and return the response text.
        Raises RuntimeError on API/network errors.
        """
        try:
            config = types.GenerateContentConfig(
                system_instruction=self.system_instruction
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                config=config,
                contents=prompt,
                **kwargs
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error during Gemini API call: {e}")
            raise RuntimeError(f"Gemini API error: {e}")
