import os
import json
import base64
import re
from sqlalchemy import and_
import tiktoken


from app.models.channel_model import ChannelModel
from app.models.models import db, SentenceTranslation
from app.models.sentence_model import SentenceModel
from app.services.ai_generator import AiGenerator
from app.utils.logger import get_logger

logger = get_logger("assets/log/app.log", bold_numbers=True)

class PaliTranslationProcessor:
    def __init__(self, channel_id, book_id, api_keys, model="gemini/gemini-2.0-flash", lang='en', max_tokens=3000):
        self.api_keys = api_keys
        self.model = model
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")
        self.aigenerator = AiGenerator(api_keys, model=model, lang=lang)
        self.lang = lang
        self.source_channel_id = channel_id
        self.book_id = book_id
        self.output_channel = ChannelModel.create_nissaya_channel(title="Gemini", lang=self.lang)

    def count_tokens(self, text):
        """Count the number of tokens in a given text."""
        return len(self.encoding.encode(text))

    def parse_nissaya_content(self, content):
        if not content:
            return []
        
        nissaya_pairs = []
        lines = content.split('\n') if content else []
        
        for line in lines:
            nissaya_tags = re.findall(r'\{\{nissaya\|(.*?)\}\}', line)
            
            for tag in nissaya_tags:
                try:
                    decoded_bytes = base64.b64decode(tag)
                    decoded_str = decoded_bytes.decode('utf-8')
                    nissaya_data = json.loads(decoded_str)
                    
                    if 'pali' in nissaya_data and 'meaning' in nissaya_data:
                        from app.services.scriptconvert import myanmar_to_roman
                        roman = myanmar_to_roman(nissaya_data['pali'])
                        nissaya_pairs.append({
                            'pali': roman,
                            'meaning': nissaya_data['meaning']
                        })
                
                except Exception as e:
                    logger.error(f"Error parsing tag: {e}")
        
        return nissaya_pairs
    
    
    def get_book_data(self):
        """Fetch untranslated sentences from the database for a given book and channels."""
        results = SentenceModel.get_untranslated_sentences(self.book_id, self.source_channel_id, self.output_channel['nissaya'])
        logger.info(f"Fetched {len(results)} sentences for book {self.book_id} from channel {self.source_channel_id}")
        book_data = []
        for row in results:
            nissaya_pairs = self.parse_nissaya_content(row['translation_content'])
            if nissaya_pairs:
                book_data.append({
                    'paragraph': row['paragraph'],
                    'word_start': row['word_start'],
                    'word_end': row['word_end'],
                    'sentence_content': row['sentence_content'],
                    'nissaya_pairs': nissaya_pairs
                })
        
        return book_data
    
    def create_translation_chunks(self, book_data):
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence_data in book_data:
            sentence_json = json.dumps({
                'paragraph': sentence_data['paragraph'],
                'word_start': sentence_data['word_start'],
                'word_end': sentence_data['word_end'],
                'sentence_content': sentence_data['sentence_content'],
                'nissaya_pairs': sentence_data['nissaya_pairs']
            }, ensure_ascii=False)
            
            sentence_tokens = self.count_tokens(sentence_json)
            
            if current_tokens + sentence_tokens > self.max_tokens and current_chunk:
                chunks.append(current_chunk)
                current_chunk = [sentence_data]
                current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence_data)
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def create_translation_prompt(self, chunk_data):
        chunk_json = json.dumps(chunk_data, ensure_ascii=False, indent=2)
        
        prompt = f"""
Input data:
{chunk_json}"""
        
        return prompt
    
    def process_ai_response(self, response_text):
        try:
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing AI response as JSON: {e}")
            return None
    
    def create_translated_content(self, original_content, translated_pairs):
        if not original_content or not translated_pairs:
            return original_content
        
        new_content = original_content
        translated_pairs_iter = iter(translated_pairs)
        
        def replace_nissaya(match):
            try:
                next_pair = next(translated_pairs_iter, None)
                if not next_pair or 'meaning' not in next_pair:
                    return match.group(0)
                
                decoded_bytes = base64.b64decode(match.group(1))
                decoded_str = decoded_bytes.decode('utf-8')
                nissaya_data = json.loads(decoded_str)
                
                from app.services.scriptconvert import myanmar_to_roman
                roman = myanmar_to_roman(nissaya_data.get('pali', ''))
                
                if roman != next_pair['pali']:
                    logger.warning(f"Correct misspelling: {roman} => {next_pair['pali']}")
                
                nissaya_data['pali'] = next_pair['pali']
                nissaya_data['meaning'] = next_pair['meaning']
                nissaya_data['lang'] = 'ro' # self.lang
                updated_json = json.dumps(nissaya_data, ensure_ascii=False)
                updated_base64 = base64.b64encode(updated_json.encode('utf-8')).decode('utf-8')
                return f"{{{{nissaya|{updated_base64}}}}}"
            
            except Exception as e:
                logger.error(f"Error in replacing nissaya:{e}")
            
            return match.group(0)
        
        new_content = re.sub(r'\{\{nissaya\|([^}]+)\}\}', replace_nissaya, new_content)
        return new_content
    
    def save_translations(self, translated_data):

        # SAVE NISSAYA TRANSLATION
        '''replaces from the original one with the same paragraph, start to the new translated content'''
        for sentence_data in translated_data:
            original_translation = SentenceTranslation.query.filter(
                and_(
                    SentenceTranslation.book == self.book_id,
                    SentenceTranslation.paragraph == sentence_data['paragraph'],
                    SentenceTranslation.word_start == sentence_data['word_start'],
                    SentenceTranslation.word_end == sentence_data['word_end'],
                    SentenceTranslation.channel_id == self.source_channel_id
                )
            ).first()
            
            if original_translation:
                try:
                    new_content = self.create_translated_content(
                        original_translation.content,
                        sentence_data.get('nissaya_pairs', [])
                    )
                    
                    existing_translation = SentenceTranslation.query.filter(
                        and_(
                            SentenceTranslation.book == self.book_id,
                            SentenceTranslation.paragraph == sentence_data['paragraph'],
                            SentenceTranslation.word_start == sentence_data['word_start'],
                            SentenceTranslation.word_end == sentence_data['word_end'],
                            SentenceTranslation.channel_id == self.output_channel['nissaya']
                        )
                    ).first()
                    
                    if existing_translation:
                        existing_translation.content = new_content
                    else:
                        new_translation = SentenceTranslation(
                            book=self.book_id,
                            paragraph=sentence_data['paragraph'],
                            word_start=sentence_data['word_start'],
                            word_end=sentence_data['word_end'],
                            content=new_content,
                            channel_id=self.output_channel['nissaya']
                        )
                        db.session.add(new_translation)

                    # save translation and free translation to the database.
                    new_translation = SentenceTranslation(
                        book=self.book_id,
                        paragraph=sentence_data['paragraph'],
                        word_start=sentence_data['word_start'],
                        word_end=sentence_data['word_end'],
                        content=sentence_data['translation'],
                        channel_id=self.output_channel['translation']
                    )
                    db.session.add(new_translation)
                
                    new_translation = SentenceTranslation(
                        book=self.book_id,
                        paragraph=sentence_data['paragraph'],
                        word_start=sentence_data['word_start'],
                        word_end=sentence_data['word_end'],
                        content=sentence_data['free_translation'],
                        channel_id=self.output_channel['free_translation']
                    )
                    db.session.add(new_translation)
                    
                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    logger.error(f"[Error] saving nissaya translations: {e}")
        
        return True
        
    
    def get_last_processed_position(self, book_id, target_channel_id):
        last_translation = SentenceTranslation.query.filter(
            and_(
                SentenceTranslation.book == book_id,
                SentenceTranslation.channel_id == target_channel_id
            )
        ).order_by(
            SentenceTranslation.paragraph.desc(),
            SentenceTranslation.word_start.desc()
        ).first()
        
        if not last_translation:
            return None, None
        
        return last_translation.paragraph, last_translation.word_start
    
    def process_book_translation(self):
        logger.info(f"Starting translation process for book {self.book_id}")
        # logger.info(f"Source channel: {self.source_channel_id}")
        # logger.info(f"Target channel: {self.output_channel['nissaya']}")
        
        book_data = self.get_book_data()
        if not book_data:
            logger.warning("No data found for the specified book and channel")
            return
        
        logger.info(f"Found {len(book_data)} sentences to process")
        
        
        chunks = self.create_translation_chunks(book_data)
        logger.debug(f"Split into {len(chunks)} chunks")
        
        # loop through each chunk and process, if failed in the ai, it will run again with another api.
        for i, chunk in enumerate(chunks, start=1):
            #logger.debug("delay for 20 seconds to avoid rate limit")
            #sleep(20)

            logger.debug(f"Processing chunk {i}/{len(chunks)}")
            
            prompt = self.create_translation_prompt(chunk)

            #get data from file for fast testing.
            if os.path.exists('debug.json'):
                with open('debug.json', 'r') as f:
                    response = f.read()
            else:
                response = self.aigenerator.generate_ai_response(prompt)
            
            with open('responses.json', 'a+') as f:
                f.write("\n\n")
                f.write(response)
            
            if response.startswith("Error:"):
                logger.critical(f"AI Error for chunk {i}: {response}")
                continue
            
            translated_chunk = self.process_ai_response(response)
            
            if translated_chunk:
                for sentence in translated_chunk:
                    sentence['book'] = self.book_id
                
                if self.save_translations(translated_chunk):
                    logger.info(f"[Successfully processed and saved chunk {i}]")
                else:
                    logger.error(f"Failed to save chunk {i}")
            else:
                logger.error(f"Failed to parse response for chunk {i}")
