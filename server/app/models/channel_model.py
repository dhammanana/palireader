from sqlalchemy import and_, func
from app.models.models import db, Channel, SentenceTranslation

class ChannelModel:
    @staticmethod
    def get_all_channels():
        """Get all channels excluding those with 'zh' language prefix, sorted by name"""
        return Channel.query.filter(~Channel.language.like('zh%')).order_by(Channel.name).all()

    @staticmethod
    def get_channel_by_id(channel_id):
        """Get channel by ID"""
        channel = db.session.query(Channel.id, Channel.name).filter(Channel.id == channel_id).first()
        ret = {
            'id': channel.id,
            'name': channel.name
            } if channel else {
                'id': channel_id, 
                'name': f"Channel {channel_id}"
            }
        return ret
    
    @staticmethod
    def get_all_channels_with_counts():
        """Get all channels with sentence translation counts, sorted by count descending"""
        return (
            db.session.query(
                Channel.id,
                Channel.name,
                func.count(SentenceTranslation.channel_id).label('lines_count')
            )
            .outerjoin(SentenceTranslation, Channel.id == SentenceTranslation.channel_id)
            .filter(~Channel.language.like('zh%'))
            .group_by(Channel.id)
            .order_by(db.desc('lines_count'))
            .all()
        )

    @staticmethod
    def get_channels_by_book(book_id):
        """Get channels for a specific book with translation counts, sorted by count descending"""
        channels = (
            db.session.query(
                Channel.id,
                Channel.name,
                func.count(SentenceTranslation.channel_id).label('lines_count')
            )
            .join(SentenceTranslation, SentenceTranslation.channel_id == Channel.id)
            .filter(SentenceTranslation.book == book_id)
            .group_by(Channel.id, Channel.name)
            .order_by(db.desc('lines_count'))
            .all()
        )
        return [{'id': c.id, 'name': c.name, 'lines_count': c.lines_count} for c in channels]


    @staticmethod
    def create_nissaya_channel(title, lang):
        """Create or retrieve channels with nissaya, literal-translation, and free-translation names based on title and language"""
        channel_names = {
            'nissaya': f"{title}-{lang}-nissaya",
            'translation': f"{title}-{lang}-literal-translation",
            'free_translation': f"{title}-{lang}-free-translation"
        }
        
        result = {}
        for key, name in channel_names.items():
            channel = Channel.query.filter_by(name=name).first()
            print(f"Checking channel: {name}")
 
            if not channel:
                channel = Channel(
                    name=name, 
                    type="nissaya", 
                    language=lang,
                    owner_id='54065ed1-b577-4fbc-932d-bcf08a6e5fd9'
                    )
                db.session.add(channel)
                db.session.commit()
            result[key] = channel.id
        return result
    