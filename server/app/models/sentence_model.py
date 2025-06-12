from sqlalchemy import and_, func, or_
from sqlalchemy.sql import exists
from app.models.models import Channel, PaliText, db, Sentence, SentenceTranslation

class SentenceModel:
    @staticmethod
    def get_translations_with_sentences(book_id, channel_id, paragraph_start=None, paragraph_end=None):
        """Get sentences with translations for a book and channel, starting from book's start paragraph"""
        start_paragraph = db.session.query(
            SentenceTranslation.paragraph
        ).filter(
            and_(
                SentenceTranslation.book == book_id,
                SentenceTranslation.channel_id == channel_id
            )
        ).order_by(SentenceTranslation.paragraph).first()
        
        start_paragraph = start_paragraph.paragraph if start_paragraph else 1

        query = db.session.query(
            Sentence.book,
            Sentence.paragraph,
            Sentence.word_start,
            Sentence.word_end,
            Sentence.content.label('sentence_content'),
            SentenceTranslation.content.label('translation_content')
        ).outerjoin(SentenceTranslation, 
            and_(
                Sentence.book == SentenceTranslation.book,
                Sentence.paragraph == SentenceTranslation.paragraph,
                Sentence.word_start == SentenceTranslation.word_start,
                Sentence.word_end == SentenceTranslation.word_end,
                SentenceTranslation.channel_id == channel_id
            )
        ).filter(
            Sentence.book == book_id,
            Sentence.paragraph >= start_paragraph
        )
        
        if paragraph_start is not None and paragraph_end is not None:
            query = query.filter(Sentence.paragraph.between(paragraph_start, paragraph_end))
        else:
            query = query.filter(
                Sentence.paragraph.between(start_paragraph, start_paragraph+10)
            )
        
        sentences = query.distinct(Sentence.book, Sentence.paragraph, Sentence.word_start, Sentence.word_end
        ).order_by(Sentence.paragraph, Sentence.word_start).all()
        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))
        return [{
            'paragraph': sentence.paragraph,
            'word_start': sentence.word_start,
            'word_end': sentence.word_end,
            'sentence_content': sentence.sentence_content,
            'translation_content': sentence.translation_content
        } for sentence in sentences]

    @staticmethod
    def get_dual_translations_with_sentences(book_id, channel_id_1, channel_id_2, paragraph_start=None, paragraph_end=None):
        """Get sentences with translations from two channels for a book"""
        from sqlalchemy import distinct
        from sqlalchemy.orm import aliased

        # Aliases for SentenceTranslation
        st1 = aliased(SentenceTranslation, name='st1')
        st2 = aliased(SentenceTranslation, name='st2')

        # Get start paragraph
        start_paragraph = db.session.query(
            SentenceTranslation.paragraph
        ).filter(
            and_(
                SentenceTranslation.book == book_id,
                SentenceTranslation.channel_id.in_([channel_id_1, channel_id_2])
            )
        ).order_by(SentenceTranslation.paragraph).first()
        
        start_paragraph = start_paragraph.paragraph if start_paragraph else 1

        # Main query with joins
        query = (
            db.session.query(
                distinct(Sentence.book),
                Sentence.paragraph,
                Sentence.word_start,
                Sentence.word_end,
                Sentence.content.label('sentence_content'),
                st1.content.label('translation_content_1'),
                st2.content.label('translation_content_2')
            )
            .outerjoin(
                st1,
                (st1.book == Sentence.book)
                & (st1.paragraph == Sentence.paragraph)
                & (st1.word_start == Sentence.word_start)
                & (st1.word_end == Sentence.word_end)
                & (st1.channel_id == channel_id_1)
            )
            .outerjoin(
                st2,
                (st2.book == Sentence.book)
                & (st2.paragraph == Sentence.paragraph)
                & (st2.word_start == Sentence.word_start)
                & (st2.word_end == Sentence.word_end)
                & (st2.channel_id == channel_id_2)
            )
            .filter(
                Sentence.book == book_id,
                Sentence.paragraph >= start_paragraph
            )
        )
        
        # Apply paragraph range filter
        if paragraph_start is not None and paragraph_end is not None:
            query = query.filter(Sentence.paragraph.between(paragraph_start, paragraph_end))
        else:
            query = query.filter(
                Sentence.paragraph.between(start_paragraph, start_paragraph + 10)
            )

        # Execute query
        sentences = query.order_by(Sentence.paragraph, Sentence.word_start).all()
        
        return [{
            'paragraph': sentence.paragraph,
            'word_start': sentence.word_start,
            'word_end': sentence.word_end,
            'sentence_content': sentence.sentence_content,
            'translation_content': sentence.translation_content_1 or "",
            'translation_content_2': sentence.translation_content_2 or ""
        } for sentence in sentences]

    @staticmethod
    def get_untranslated_sentences(book_id, orig_channel_id, trans_channel_id, paragraph_start=None, paragraph_end=None):
        """Get sentences without translations for a book, existing in orig_channel_id but not in trans_channel_id"""
        

        # Determine the starting paragraph for the book
        start_paragraph = db.session.query(
            PaliText.paragraph
        ).filter(
            and_(
                PaliText.book == book_id,
                PaliText.level == 1
            )
        ).order_by(PaliText.paragraph).first()
        
        start_paragraph = start_paragraph.paragraph if start_paragraph else 1
        
        # Build the main query
        query = db.session.query(
            Sentence.book,
            Sentence.paragraph,
            Sentence.word_start,
            Sentence.word_end,
            Sentence.content.label('sentence_content'),
            SentenceTranslation.content.label('translation_content')
        ).join(
            SentenceTranslation,
            and_(
                Sentence.book == SentenceTranslation.book,
                Sentence.paragraph == SentenceTranslation.paragraph,
                Sentence.word_start == SentenceTranslation.word_start,
                Sentence.word_end == SentenceTranslation.word_end,
                SentenceTranslation.channel_id == orig_channel_id
            )
        ).filter(
            Sentence.book == book_id,
            Sentence.paragraph >= start_paragraph
        ).filter(
            ~exists().select_from(SentenceTranslation).where(
                and_(
                    SentenceTranslation.book == Sentence.book,
                    SentenceTranslation.paragraph == Sentence.paragraph,
                    SentenceTranslation.word_start == Sentence.word_start,
                    SentenceTranslation.word_end == Sentence.word_end,
                    SentenceTranslation.channel_id == trans_channel_id
                )
            ).correlate(Sentence)
        )
        
        # Apply paragraph range filter if provided
        if paragraph_start is not None and paragraph_end is not None:
            query = query.filter(Sentence.paragraph.between(paragraph_start, paragraph_end))
        
        # Debug: Print the compiled SQL query
        # print(query.statement.compile(compile_kwargs={"literal_binds": True}))
        
        # Execute query and fetch results
        sentences = query.order_by(Sentence.paragraph, Sentence.word_start).all()
        
        # Format results as a list of dictionaries
        return [{
            'paragraph': sentence.paragraph,
            'word_start': sentence.word_start,
            'word_end': sentence.word_end,
            'sentence_content': sentence.sentence_content,
            'translation_content': sentence.translation_content
        } for sentence in sentences]


    @staticmethod
    def get_unconverted_nissaya_channels():
        """Retrieve channels with unconverted nissaya content in Burmese language."""
        query = db.session.query(
            SentenceTranslation.channel_id,
            Channel.name,
            Channel.type,
            Channel.language,
            func.count().label('sentence_count')
        ).outerjoin(
            Channel,
            SentenceTranslation.channel_id == Channel.id
        ).filter(
            and_(
                SentenceTranslation.content.like('%၊%။%'),
                ~SentenceTranslation.content.like('%{{nissaya|%'),
                Channel.type == 'nissaya',
                Channel.language == 'my'
            )
        ).group_by(
            SentenceTranslation.channel_id,
            Channel.name,
            Channel.type,
            Channel.language
        )

        results = query.all()

        return [{
            'channel_id': row.channel_id,
            'name': row.name,
            'type': row.type,
            'language': row.language,
            'sentence_count': row.sentence_count
        } for row in results]

    @staticmethod
    def convert_nissaya_sentences(channel_id, convert_func):
        """Fetch unconverted sentences for a channel, apply conversion, and update content."""
        # Query to fetch unconverted sentences
        query = db.session.query(
            SentenceTranslation.book,
            SentenceTranslation.paragraph,
            SentenceTranslation.word_start,
            SentenceTranslation.word_end,
            SentenceTranslation.channel_id,
            SentenceTranslation.content
        ).filter(
            and_(
                SentenceTranslation.channel_id == channel_id,
                SentenceTranslation.content.like('%၊%။%'),
                ~SentenceTranslation.content.like('%{{nissaya|%')
            )
        )

        sentences = query.all()

        # Process and update each sentence
        updated_count = 0
        for sentence in sentences:
            try:
                # Apply the provided conversion function
                converted_content = convert_func(sentence.content)
                
                # # Print original and converted content for testing
                # print(f"Sentence ID: {sentence.paragraph}")
                # print(f"Original Content: {sentence.content}")
                # # print(f"Converted Content: {converted_content}")
                # print("-" * 80)

                # # Update the content in the database
                db.session.query(SentenceTranslation).filter(
                    SentenceTranslation.book == sentence.book,
                    SentenceTranslation.paragraph == sentence.paragraph,
                    SentenceTranslation.word_start == sentence.word_start,
                    SentenceTranslation.word_end == sentence.word_end,
                    SentenceTranslation.channel_id == sentence.channel_id
                ).update(
                    {'content': converted_content},
                    synchronize_session=False
                )
                updated_count += 1
            except Exception as e:
                # Log error and continue with next sentence
                print(f"Error converting sentence ID {sentence.id}: {str(e)}")
                continue

        # Commit changes
        try:
            db.session.commit()
            return {
                'status': 'success',
                'updated_count': updated_count,
                'total_processed': len(sentences)
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': f"Failed to commit changes: {str(e)}",
                'updated_count': 0,
                'total_processed': len(sentences)
            }
        

