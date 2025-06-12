import os
import random
from litellm import completion
from google import genai
from google.genai import types
from openai import OpenAI

from app.utils.logger import get_logger

logger = get_logger("assets/log/app.log", bold_numbers=True)


class AiGenerator:
    def __init__(self, api_keys, lang='en', model="gemini/gemini-2.0-flash"):
        self.api_keys = api_keys
        self.model = model
        self.lang = lang
   
    
    def generate_ai_response(self, prompt):
        '''If the model is gemini, openrouter run with custom gemini, openrouter function.'''
        if self.model.startswith('gemini'):
            return self.generate_gemini_response(prompt)
            
        system_prompt = open('assets/system_prompt_'+self.lang+'.md', encoding='utf8').read()
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
        try:
            self.api_key = random.choice(self.api_keys)
            logger.debug(f"Using Gemini API Key: ***{self.api_key[-4:]}")
            client = genai.Client(api_key=self.api_key)
            system_prompt = open('assets/system_prompt_'+self.lang+'.md', encoding='utf8').read()
            
            
            # Safety settings
            GEMINI_SAFE_SETTINGS = [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
            ]
            
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
                    safety_settings=GEMINI_SAFE_SETTINGS,
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
                    safety_settings=GEMINI_SAFE_SETTINGS,
                    system_instruction=[
                        types.Part.from_text(text=system_prompt)
                    ],
                )
            
            # Generate response using streaming
            output = ""
            for chunk in client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                output += chunk.text
                
            return output
            
        except Exception as e:
            return f"Error: {str(e)}"
        
