from sqlalchemy import func
from sqlalchemy.sql import text
from app.models.models import db, PaliText, Chapter, Tag, TagMap

class TagModel:
    @staticmethod
    def search_chapters_by_tags(tags):
        """Search chapters by multiple tags with partial match, returning formatted JSON"""
        query = (db.session.query(
                    Chapter.id,
                    Chapter.book,
                    Chapter.paragraph,
                    PaliText.level,
                    Chapter.title,
                    PaliText.chapter_len,
                    PaliText.parent,
                    PaliText.toc.label('path'),
                    Chapter.progress.label('progress_line')
                )
                .join(TagMap, Chapter.id == TagMap.anchor_id)
                .join(Tag, TagMap.tag_id == Tag.id)
                .filter(db.or_(*[Tag.name.like(f'%{tag}%') for tag in tags]))
                .join(PaliText, Chapter.book == PaliText.book and Chapter.paragraph == PaliText.paragraph)  
                .order_by(Chapter.book, Chapter.paragraph)
                )
        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))
        results = query.all()
        return [{
            'id': r.id,
            'book': r.book,
            'paragraph': r.paragraph,
            'level': r.level,
            'title': r.title,
            'chapter_strlen': r.chapter_len,
            'parent': r.parent,
            'path': r.path,
            'progress_line': r.progress_line
        } for r in results]


    @staticmethod
    def search_palitext_by_tags(tags):
        """Search PaliText by multiple tags, returning only IDs where all tags exist"""
        # Build subqueries for each tag
        subqueries = [
            db.session.query(TagMap.anchor_id.label('anchor_id'))
            .join(Tag, TagMap.tag_id == Tag.id)
            .filter(Tag.name.like(f'%{tag}%'))
            for tag in tags
        ]
        
        # Combine subqueries with INTERSECT
        intersect_query = subqueries[0]
        for subquery in subqueries[1:]:
            intersect_query = intersect_query.intersect_all(subquery)
        
        # Create subquery with explicit column
        intersect_subquery = intersect_query.subquery()
        aliased_subquery = db.session.query(intersect_subquery.columns[0].label('anchor_id')).subquery()

        
        # Main query to join with PaliText and fetch required columns
        query = (
            db.session.query(
                PaliText.id,
                PaliText.book,
                PaliText.paragraph,
                PaliText.level,
                PaliText.toc,
                PaliText.chapter_len,
                PaliText.parent
            )
            # .join(subquery, PaliText.id == subquery.c.anchor_id)
            .join(aliased_subquery, PaliText.id == aliased_subquery.c.anchor_id)
            .order_by(PaliText.book, PaliText.paragraph)
        )
        
        # Execute query and format results
        results = query.all()
        return [{
            'id': r.id,
            'book': r.book,
            'paragraph': r.paragraph,
            'level': r.level,
            'title': r.toc,
            'chapter_len': r.chapter_len,
            'parent': r.parent
        } for r in results]