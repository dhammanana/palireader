from flask import Blueprint, render_template, request
from app.models.book_model import BookModel
from app.models.channel_model import ChannelModel
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
    book = BookModel.get_book_by_id(book_id)
    channel = ChannelModel.get_channel_by_id(channel_id)
    channel2_id = request.args.get('channel2', '')
    script_lang = request.args.get('script', '')
    print(type(channel), channel)
    return render_template(
        'book.html',
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


