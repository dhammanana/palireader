import os
import random
from litellm import completion
from google import genai
from google.genai import types
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from app.utils.logger import get_logger

logger = get_logger("assets/log/app.log", bold_numbers=True)

# Define Pydantic models for the schema
class NissayaPair(BaseModel):
    pali: str
    meaning: str

class TranslationEntry(BaseModel):
    paragraph: int
    word_start: int
    word_end: int
    translation: str
    free_translation: str
    nissaya_pairs: List[NissayaPair]

class AiGenerator:
    def __init__(self, api_keys, lang='en', model="gemini/gemini-2.0-flash"):
        self.api_keys = api_keys
        self.model = model
        self.lang = lang

    def generate_ai_response(self, prompt):
        '''If the model is gemini, openrouter run with custom gemini, openrouter function.'''
        if self.model.startswith('gemini'):
            return self.generate_gemini_response(prompt)

        system_prompt = open(f'assets/system_prompt_{self.lang}.md', encoding='utf8').read()
        try:    
            response = completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                api_key=random.choice(self.api_keys),
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_gemini_response(self, prompt):
        self.api_key = random.choice(self.api_keys)
        logger.debug(f"Using Gemini API Key: ***{self.api_key[-4:]}")

        client = genai.Client(
            api_key=self.api_key, 
        )
        system_prompt = open(f'assets/system_prompt_{self.lang}.md', encoding='utf8').read()
            

        # Create content
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        
       # Generate content config
        generate_content_config = None
        if self.model.startswith('gemini-2.5'):
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="application/json",
                system_instruction=[
                    types.Part.from_text(text=system_prompt)
                ],
                thinking_config=genai.types.ThinkingConfig(
                  thinking_budget=1024
                )
            )
        else:
            generate_content_config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                response_mime_type="application/json",
                system_instruction=[
                    types.Part.from_text(text=system_prompt)
                ],
            )

        try:
            # Generate response
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            )
                
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"

