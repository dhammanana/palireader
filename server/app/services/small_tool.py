import os
import json
import base64
import random
import re
from datetime import datetime
from time import sleep
from sqlalchemy import and_
from litellm import completion
import tiktoken
from google import genai
from google.genai import types
from openai import OpenAI
import argparse


from app.models.models import db, SentenceTranslation
from app.models.sentence_model import SentenceModel
from app import create_app
from app.services.translation_service import TranslationService
from app.utils.logger import get_logger

LANGUAGE_CODE = "en"
logger = get_logger("assets/log/app.log", bold_numbers=True)


class SmallTool:
    @staticmethod
    def convert_func(content):
        # Split the content by '။' (Myanmar sentence-ending punctuation)
        segments = content.split('။')
        processed_segments = []
        
        for segment in segments:
            if not segment.strip():
                continue  # Skip empty segments
            
            # Check if the segment contains '၊' (Myanmar comma-like punctuation)
            if '၊' in segment:
                # Split by '၊' and ensure exactly two parts
                parts = segment.split('၊', 1)
                if len(parts) == 2:
                    pali, meaning = parts
                    # Create JSON object
                    data = {
                        "pali": pali.strip(),
                        "meaning": meaning.strip(),
                        "lang": "my"
                    }
                    # Convert to JSON string
                    json_str = json.dumps(data, ensure_ascii=False)
                    # Base64 encode the JSON string
                    base64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
                    # Wrap in {{nissaya|<base64>}}
                    processed = f"{{{{nissaya|{base64_str}}}}}"
                else:
                    # If splitting doesn't yield two parts, keep the segment unchanged
                    processed = segment
            else:
                # If no '၊', keep the segment unchanged
                processed = segment
            
            processed_segments.append(processed)
        
        # Join segments with newline
        ouput = '\n'.join(processed_segments)
        print(ouput)
        print(TranslationService.get_nissaya_list(ouput))
        print("=" * 50)
        return ouput
    
    @staticmethod
    def convert_nissaya_to_json():
        
        print("Checking for channel that has unconverted rows: ")
        unconverted_channels = SentenceModel.get_unconverted_nissaya_channels()
        print("Unconverted Nissaya Channels:")
        for channel in unconverted_channels:
            print(f"Channel ID: {channel['channel_id']}, Name: {channel['name']}, Sentence Count: {channel['sentence_count']}")
        for channel in unconverted_channels:
            print(f"converting for the channel: [{channel['name']}]")
            result = SentenceModel.convert_nissaya_sentences(
                channel_id=channel['channel_id'],
                convert_func=SmallTool.convert_func
            )
            print(result)

def main():
    app = create_app()
    with app.app_context():
        pass


if __name__ == "__main__":
    main()
