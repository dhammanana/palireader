from sqlalchemy import and_, func
from app.models.models import db, PaliText, SentenceTranslation

class BookModel:
    @staticmethod
    def get_book_names():
        """Get all book names with line counts"""
        books = db.session.query(
            PaliText.book.label('book_id'),
            PaliText.toc.label('book_name'),
            func.count(SentenceTranslation.book).label('lines_count')
        ).filter(PaliText.level == 1
        ).outerjoin(SentenceTranslation, PaliText.book == SentenceTranslation.book
        ).group_by(PaliText.book, PaliText.toc
        ).order_by(db.desc('lines_count')).all()
        
        return [{
            'book_id': book.book_id,
            'book_name': book.book_name,
            'lines_count': book.lines_count
        } for book in books]
    
    @staticmethod
    def get_book_by_id(book_id):
        """Get book name by book ID"""
        book = db.session.query(
            PaliText.book.label('book_id'),
            PaliText.toc.label('book_name'),
        ).filter(PaliText.book == book_id, PaliText.level == 1
        ).first()
        
        return {
            'book_id': book.book_id,
            'book_name': book.book_name,
         } if book else {
             'book_id': book_id,
            'book_name': f"Book {book_id}"
         }

    @staticmethod
    def get_books_by_channel(channel_id):
        """Get books for a specific channel with starting paragraphs and line counts"""
        books = db.session.query(
            SentenceTranslation.book.distinct(),
            func.count(SentenceTranslation.book).label('lines_count')
        ).filter(SentenceTranslation.channel_id == channel_id
        ).group_by(SentenceTranslation.book
        ).order_by(SentenceTranslation.book).all()
        
        book_ids = [book[0] for book in books]
        book_names = {}
        
        if book_ids:
            book_names_query = db.session.query(
                PaliText.book,
                PaliText.toc,
                PaliText.paragraph
            ).filter(
                and_(
                    PaliText.book.in_(book_ids),
                    PaliText.level == 1
                )
            ).distinct().all()
            
            book_names = {book.book: {'toc': book.toc, 'start_paragraph': book.paragraph} for book in book_names_query}
        
        books_with_names = []
        for book, lines_count in books:
            book_id = book
            book_info = book_names.get(book_id, {'toc': f"Book {book_id}", 'start_paragraph': 1})
            books_with_names.append({
                'book': book_id,
                'name': book_info['toc'],
                'start_paragraph': book_info['start_paragraph'],
                'lines_count': lines_count
            })
        
        return books_with_names
