"""Initial migration

Revision ID: cfc4c03baa0d
Revises: 
Create Date: 2025-05-19 22:07:57.754813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfc4c03baa0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.Column('setting', sa.String(), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dhamma_terms',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('word', sa.String(length=1024), nullable=False),
    sa.Column('word_en', sa.String(length=1024), nullable=False),
    sa.Column('meaning', sa.String(length=1024), nullable=False),
    sa.Column('other_meaning', sa.String(length=1024), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('tag', sa.String(length=1024), nullable=True),
    sa.Column('channel_id', sa.String(length=36), nullable=True),
    sa.Column('language', sa.String(length=16), nullable=False),
    sa.Column('owner', sa.String(length=36), nullable=False),
    sa.Column('editor_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('pali_text',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('book', sa.Integer(), nullable=True),
    sa.Column('paragraph', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('toc', sa.String(), nullable=True),
    sa.Column('chapter_len', sa.Integer(), nullable=True),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.Time(), nullable=True),
    sa.Column('color', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chapter',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('book', sa.Integer(), nullable=True),
    sa.Column('paragraph', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('channel_id', sa.String(), nullable=True),
    sa.Column('progress', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentence',
    sa.Column('book', sa.Integer(), nullable=False),
    sa.Column('paragraph', sa.Integer(), nullable=False),
    sa.Column('word_start', sa.Integer(), nullable=False),
    sa.Column('word_end', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('channel_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.PrimaryKeyConstraint('book', 'paragraph', 'word_start', 'word_end', 'channel_id')
    )
    op.create_table('sentence_translation',
    sa.Column('book', sa.Integer(), nullable=False),
    sa.Column('paragraph', sa.Integer(), nullable=False),
    sa.Column('word_start', sa.Integer(), nullable=False),
    sa.Column('word_end', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('channel_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channel.id'], ),
    sa.PrimaryKeyConstraint('book', 'paragraph', 'word_start', 'word_end', 'channel_id')
    )
    op.create_table('tag_map',
    sa.Column('anchor_id', sa.String(), nullable=False),
    sa.Column('tag_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('anchor_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag_map')
    op.drop_table('sentence_translation')
    op.drop_table('sentence')
    op.drop_table('chapter')
    op.drop_table('tag')
    op.drop_table('pali_text')
    op.drop_table('dhamma_terms')
    op.drop_table('channel')
    # ### end Alembic commands ###
