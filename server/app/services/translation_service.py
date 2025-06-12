import json
import base64
import re
from .scriptconvert import roman_to_sinhala, TextProcessor, Script
from .compare import highlight_words_in_sentence
from app.models.sentence_model import SentenceModel
from app.utils.logger import get_logger

logger = get_logger("assets/log/app.log", bold_numbers=True)

class TranslationService:
    @staticmethod
    def get_nissaya_list(content, script_lang = Script.RO):

        """Parse the nissaya content from the specified format"""
        if not content:
            return ""
            
        parsed_output = []
        output = []
        
        lines = content.split('\n') if content else []
        
        for line in lines:
            nissaya_tags = re.findall(r'\{\{nissaya\|(.*?)\}\}', line)
            
            for tag in nissaya_tags:
                try:
                    decoded_bytes = base64.b64decode(tag)
                    decoded_str = decoded_bytes.decode('utf-8')
                    nissaya_data = json.loads(decoded_str)
                    
                    if 'pali' in nissaya_data and 'meaning' in nissaya_data:
                        if 'lang' in nissaya_data and nissaya_data['lang'] == 'my':
                            converted = TextProcessor.convert_to_sinh(nissaya_data['pali'], Script.MY)
                        elif 'lang' in nissaya_data and (nissaya_data['lang'] == 'ro' or nissaya_data['lang'] == 'en' or nissaya_data['lang'] == 'vi'):
                            converted = roman_to_sinhala(nissaya_data['pali'])

                        if script_lang != Script.SI:
                            converted = TextProcessor.convert_from_sinh(converted, script_lang)
                        parsed_output.append(f"{converted}={nissaya_data['meaning']}")
                        output.append([converted, nissaya_data['meaning']])
                
                except Exception as e:
                    logger.error(f"Error parsing nissaya tag: {tag} \n- {str(e)}")
        
        return output

    @staticmethod
    def get_parsed_translations(book_id, channel_id, paragraph_start=None, paragraph_end=None, channel_id_2=None, script_lang=Script.RO):
        """Get and parse all translations with their sentences for a specific book and channel"""
        results = []
        if channel_id_2:
            results = SentenceModel.get_dual_translations_with_sentences(book_id, channel_id, channel_id_2, paragraph_start, paragraph_end)
        else:
            results = SentenceModel.get_translations_with_sentences(book_id, channel_id, paragraph_start, paragraph_end)
        
        parsed_results = []
        
        for row in results:
            translation_content = row['translation_content']
            translation_content_2 = row.get('translation_content_2', None)
            sentence_content = row['sentence_content']
            paragraph = row['paragraph']
            word_start = row['word_start']
            word_end = row['word_end']
            
            if script_lang == Script.SI:
                sentence_content = roman_to_sinhala(sentence_content)
            elif script_lang == Script.RO:
                pass
            else:
                sentence_content = roman_to_sinhala(sentence_content)
                sentence_content = TextProcessor.convert_from_sinh(sentence_content, script_lang)

            if translation_content and '{{nissaya|' in translation_content:
                nissaya = TranslationService.get_nissaya_list(translation_content, script_lang)
                nissaya = highlight_words_in_sentence(sentence_content, nissaya)
                parsed = ' | '.join(['<b>'+it[0]+'</b>='+it[1] for it in nissaya])
            else:
                parsed = translation_content

            parsed_results.append({
                'paragraph': paragraph,
                'word_start': word_start,
                'word_end': word_end,
                'sentence_content': sentence_content or "No original sentence available",
                'translation_content': parsed,
                'translation_content_2': translation_content_2 or None
            })
        
        grouped_results = {}
        for item in parsed_results:
            para = item['paragraph']
            if para not in grouped_results:
                grouped_results[para] = []
            
            grouped_results[para].append(item)
        
        return grouped_results