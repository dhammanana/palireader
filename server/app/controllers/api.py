from flask import Blueprint, jsonify, request
from app.models.book_model import BookModel
from app.models.channel_model import ChannelModel
from app.models.sentence_model import SentenceModel
from app.models.tag_model import TagModel
from app.models.toc_model import TocModel
from app.services.scriptconvert import SCRIPT_LANG
from app.services.translation_service import TranslationService
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/menu')
def get_menu():
    with open('assets/menu.json', encoding="utf8") as f:
        data = json.load(f)
        return jsonify(data)
    return jsonify({})

@api_bp.route('/books')
def get_all_books():
    """API endpoint to get all books with line counts"""
    books = BookModel.get_book_names()
    return jsonify([{
        'book_id': book['book_id'],
        'book_name': book['book_name'],
        'lines_count': book['lines_count']
    } for book in books])

@api_bp.route('/books/<channel_id>')
def get_books_by_channel(channel_id):
    """API endpoint to get books for a selected channel with line counts"""
    books = BookModel.get_books_by_channel(channel_id)
    return jsonify([{
        'book': book['book'],
        'name': book['name'],
        'lines_count': book['lines_count'],
        'start_paragraph': book['start_paragraph']
    } for book in books])

@api_bp.route('/channels/<book_id>')
def get_channels_by_book(book_id):
    """API endpoint to get channels for a selected book"""
    channels = ChannelModel.get_channels_by_book(book_id)
    return jsonify([{
        'id': channel['id'],
        'name': channel['name'],
        'lines_count': channel['lines_count']
    } for channel in channels])

@api_bp.route('/translations')
def get_translations():
    """API endpoint to get translations for a selected book and channel with optional paragraph range"""
    channel_id = request.args.get('channel', '')
    book_id = request.args.get('book', '')
    paragraph_start = request.args.get('paragraph_start', type=int)
    paragraph_end = request.args.get('paragraph_end', type=int)
    
    if not channel_id or not book_id:
        return jsonify({'error': 'Missing channel_id or book_id parameter'}), 400
    
    translations = TranslationService.get_parsed_translations(book_id, channel_id, paragraph_start, paragraph_end)
    return jsonify(translations)


@api_bp.route('/toc/<book_id>')
def get_toc(book_id):
    """API endpoint to get table of contents for a selected book"""
    toc = TocModel.get_toc(book_id)
    return jsonify(toc)

@api_bp.route('/palitext')
def search_pali_text():
    """API endpoint to search chapters by tags"""
    tags = request.args.get('tags', '').split(',')
    view = request.args.get('view', 'palitext')
    
    if view == 'chapter':
        results = TagModel.search_chapters_by_tags(tags)
        return jsonify({"status":"success", "data": results, "count": len(results)})
    elif view == 'palitext':
        results = TagModel.search_palitext_by_tags(tags)
        return jsonify({"status":"success", "data": results, "count": len(results)})
    else:
        return jsonify({"status":"error", "error": "Not yet implemented"}), 400
    
   
    

@api_bp.route('/toc/content/<book_id>/<channel_id>')
def get_toc_content(book_id, channel_id):
    """API endpoint to get content for a selected table of contents entry"""
    paragraph_start = request.args.get('paragraph_start', type=int)
    paragraph_end = request.args.get('paragraph_end', type=int)

    channel2_id = request.args.get('channel2', type=str)

    script_lang_name = request.args.get('script', type=str)
    script_lang = SCRIPT_LANG['Latn']
    if script_lang_name in SCRIPT_LANG:
        script_lang = SCRIPT_LANG[script_lang_name]

    content = TranslationService.get_parsed_translations(book_id, channel_id, paragraph_start, paragraph_end, channel2_id, script_lang)
    
    return jsonify(content)
