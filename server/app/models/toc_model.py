from app.models.models import PaliText

class TocModel:
    @staticmethod
    def get_toc(book_id):
        """Get table of contents for a selected book"""
        toc = PaliText.query.filter(
            PaliText.book == book_id,
            PaliText.level.between(2, 8)
        # ).order_by(PaliText.level, PaliText.paragraph).all()
        ).all()
        return [{
            'id': item.id,
            'level': item.level,
            'toc': item.toc,
            'chapter_len': item.chapter_len,
            'paragraph': item.paragraph,
            'parent': item.parent
        } for item in toc]