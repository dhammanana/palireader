import os
import tempfile
from flask import Blueprint, current_app, render_template, render_template_string, request, send_file
from app.models.book_model import BookModel
from app.models.channel_model import ChannelModel
from app.models.toc_model import TocModel
from app.services.translation_service import TranslationService
from app.models.models import PaliText, db
from sqlalchemy import and_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page with selection options"""
    channels = ChannelModel.get_all_channels_with_counts()
    books = BookModel.get_book_names()
    
    selected_channel = request.args.get('channel', '')
    selected_book = request.args.get('book', '')
    
    # If a channel is selected, get books for that channel
    channel_books = None
    if selected_channel:
        channel_books = BookModel.get_books_by_channel(selected_channel)
    
    # If a book is selected, get channels for that book
    book_channels = None
    if selected_book:
        book_channels = ChannelModel.get_channels_by_book(selected_book)
    
    
    # Get translations for first 10 paragraphs if both book and channel are selected
    translations = None
    channel_name = None
    book_name = None
    
    if selected_channel and selected_book:

        # Get channel name for display
        for channel in channels:
            if channel.id == selected_channel:
                channel_name = channel.name
                break
        
        # Get book name for display
        for book in books:
            if str(book["book_id"]) == selected_book:
                book_name = book["book_name"]
                break
    
    return render_template(
        'index.html',
        channels=channels,
        all_books=books,
        channel_books=channel_books,
        book_channels=book_channels,
        selected_channel=selected_channel,
        selected_book=selected_book,
        translations=translations,
        channel_name=channel_name,
        book_name=book_name
    )


@main_bp.route('/book/<book_id>/<channel_id>')
def view_book(book_id, channel_id):
    """View book with table of contents and expandable content"""
    
    channel2s = ChannelModel.get_channels({'name': 'Gemini-'})
    book = BookModel.get_book_by_id(book_id)
    channel = ChannelModel.get_channel_by_id(channel_id)
    channel2_id = request.args.get('channel2', '')
    script_lang = request.args.get('script', '')
    download = request.args.get('download', False)
    if download:
        # Handle download logic here
        toc = TocModel.get_toc(book_id)
        book_name = book['book_name'] if book else 'Unknown Book'
        channel_name = channel['name'] if channel else 'Unknown Channel'
        
        # Prepare translations for each TOC entry
        translations_by_toc = []
        for item in toc:
            paragraph_start = item['paragraph']
            paragraph_end = paragraph_start + item['chapter_len'] - 1
            translations = TranslationService.get_parsed_translations(
                book_id, channel_id, paragraph_start, paragraph_end, channel2_id, script_lang or 'IAST'
            )
            translations_by_toc.append({
                'toc': item['toc'],
                'level': item['level'],
                'paragraph': item['paragraph'],
                'chapter_len': item['chapter_len'],
                'translations': translations
            })

        # Render the template
        download_book_path = os.path.join(current_app.root_path, current_app.template_folder, 'download_book.html')
        html_content = render_template_string(
            open(download_book_path, encoding='utf-8').read(),
            book_name=book_name,
            channel_name=channel_name,
            toc=toc,
            translations_by_toc=translations_by_toc
        )

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        # Send the file for download
        try:
            return send_file(
                temp_file_path,
                as_attachment=True,
                download_name=f"{book_name.replace(' ', '_')}_{channel_name.replace(' ', '_')}.html",
                mimetype='text/html'
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
        
            
            
    return render_template(
        'book.html',
        channel2s = channel2s,
        book_id=book_id,
        channel_id=channel_id,
        book_name=book['book_name'] if book else 'Unknown Book',
        channel_name=channel['name'] if channel else 'Unknown Channel',
        channel2_id=channel2_id,
        script_lang=script_lang
    )

@main_bp.route('/view')
def view_translations():
    """View translations for a selected book and channel"""
    return index()


