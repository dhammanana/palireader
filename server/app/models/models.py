from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'channel'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    type = db.Column(db.String)
    language = db.Column(db.String)
    summary = db.Column(db.String)
    owner_id = db.Column(db.String)
    setting = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sentence_translations = db.relationship('SentenceTranslation', backref='channel', lazy=True)
    #sentences = db.relationship('Sentence', backref='channel', lazy=True)
    chapters = db.relationship('Chapter', backref='channel', lazy=True)
    
    def __repr__(self):
        return f'<Channel {self.name}>'


class PaliText(db.Model):
    __tablename__ = 'pali_text'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    book = db.Column(db.Integer)
    paragraph = db.Column(db.Integer)
    level = db.Column(db.Integer)
    toc = db.Column(db.String)
    chapter_len = db.Column(db.Integer)
    parent = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<PaliText book={self.book} paragraph={self.paragraph}>'


class Sentence(db.Model):
    __tablename__ = 'sentence'
    
    # Composite primary key
    book = db.Column(db.Integer, primary_key=True)
    paragraph = db.Column(db.Integer, primary_key=True)
    word_start = db.Column(db.Integer, primary_key=True)
    word_end = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    channel_id = db.Column(db.String) # not in use anymore.
    
    # Relationships
    translations = db.relationship(
        'SentenceTranslation',
        primaryjoin="and_(Sentence.book==SentenceTranslation.book, "
                    "Sentence.paragraph==SentenceTranslation.paragraph, "
                    "Sentence.word_start==SentenceTranslation.word_start, "
                    "Sentence.word_end==SentenceTranslation.word_end)",
        backref='original_sentence',
        lazy=True
    )
    
    def __repr__(self):
        return f'<Sentence book={self.book} para={self.paragraph} words={self.word_start}-{self.word_end}>'

class SentenceTranslation(db.Model):
    __tablename__ = 'sentence_translation'
    
    # Composite primary key
    book = db.Column(db.Integer, primary_key=True)
    paragraph = db.Column(db.Integer, primary_key=True)
    word_start = db.Column(db.Integer, primary_key=True)
    word_end = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    channel_id = db.Column(db.String, db.ForeignKey('channel.id'), primary_key=True)
    
    # Define composite foreign key constraint
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['book', 'paragraph', 'word_start', 'word_end'],
            ['sentence.book', 'sentence.paragraph', 'sentence.word_start', 'sentence.word_end']
        ),
    )
    
    def __repr__(self):
        return f'<SentenceTranslation book={self.book} para={self.paragraph} words={self.word_start}-{self.word_end}>'


class Chapter(db.Model):
    __tablename__ = 'chapter'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    book = db.Column(db.Integer)
    paragraph = db.Column(db.Integer)
    language = db.Column(db.String)
    title = db.Column(db.Text)
    channel_id = db.Column(db.String, db.ForeignKey('channel.id'))
    progress = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Chapter {self.title}>'


class DhammaTerms(db.Model):
    __tablename__ = 'dhamma_terms'
    
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    word = db.Column(db.String(1024), nullable=False)
    word_en = db.Column(db.String(1024), nullable=False)
    meaning = db.Column(db.String(1024), nullable=False)
    other_meaning = db.Column(db.String(1024))
    note = db.Column(db.Text)
    tag = db.Column(db.String(1024))
    channel_id = db.Column(db.String)
    language = db.Column(db.String(16), default='zh-hans', nullable=False)
    owner = db.Column(db.String(36), nullable=False)
    editor_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<DhammaTerms {self.word}>'


class Tag(db.Model):
    __tablename__ = 'tag'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    description = db.Column(db.Time)
    color = db.Column(db.Integer)
    owner_id = db.Column(db.String)
    
    # Relationships
    tag_maps = db.relationship('TagMap', backref='tag', lazy=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'


class TagMap(db.Model):
    __tablename__ = 'tag_map'
    
    anchor_id = db.Column(db.String, primary_key=True)
    tag_id = db.Column(db.String, db.ForeignKey('tag.id'), primary_key=True)
    
    def __repr__(self):
        return f'<TagMap anchor={self.anchor_id} tag={self.tag_id}>'