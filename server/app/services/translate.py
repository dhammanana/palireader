import os
from litellm import completion

import argparse
from app import create_app
from app.services.pali_translation_processor import PaliTranslationProcessor
from app.utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger("assets/log/app.log", bold_numbers=True)

def get_args():
    parser = argparse.ArgumentParser(description="Translate nissaya books.")
    parser.add_argument("--book", type=int, required=True, help="Book ID (e.g., 208 for vinaya-sangaha)")
    parser.add_argument("--channel", type=str, required=True, help="Source channel ID (e.g., e37545ad-f264-44cc-a5d5-ca9efe69cb94)")
    parser.add_argument("--lang", type=str, required=True, default='en', help="Language to translate. Make sure the relavant prompt is exists.")
    parser.add_argument("--model", type=str, required=False, help="Optional model specification")
    parser.add_argument("--api", type=str, required=False, help="Optional API specification")
    return parser.parse_args()

def main():
    current_ai = api_keys_str = os.getenv("SELECTED_AI", "gemini")
    current_model = os.getenv(current_ai+'_MODEL', "gemini-2.0-flash")
    current_apis = os.getenv(current_ai+'_API_KEYS', "").split('\n')
    current_apis = [api.strip() for api in current_apis if api.strip()]

    args = get_args()
    if args.model and args.api:
        current_model = args.model
        current_apis = [args.api]

    app = create_app()
    with app.app_context():
        processor = PaliTranslationProcessor(
            args.channel,
            args.book,
            api_keys=current_apis, 
            model=current_model,
            lang=args.lang
        )
        processor.process_book_translation()

if __name__ == "__main__":
    main()

