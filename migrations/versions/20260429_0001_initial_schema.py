"""initial schema

Revision ID: 20260429_0001
Revises:
Create Date: 2026-04-29 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '20260429_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'artists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('city', sa.String(length=120), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('phone', sa.String(length=120), nullable=True),
        sa.Column('image_link', sa.String(length=500), nullable=True),
        sa.Column('facebook_link', sa.String(length=120), nullable=True),
        sa.Column('website_link', sa.String(length=500), nullable=True),
        sa.Column('seeking_venue', sa.Boolean(), nullable=False),
        sa.Column('seeking_description', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'city', 'state', name='uq_artist_location'),
    )
    op.create_table(
        'genres',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'venues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('city', sa.String(length=120), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('address', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=120), nullable=True),
        sa.Column('image_link', sa.String(length=500), nullable=True),
        sa.Column('facebook_link', sa.String(length=120), nullable=True),
        sa.Column('website_link', sa.String(length=500), nullable=True),
        sa.Column('seeking_talent', sa.Boolean(), nullable=False),
        sa.Column('seeking_description', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'city', 'state', 'address', name='uq_venue_location'),
    )
    op.create_table(
        'artist_genres',
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('genre_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artists.id']),
        sa.ForeignKeyConstraint(['genre_id'], ['genres.id']),
        sa.PrimaryKeyConstraint('artist_id', 'genre_id'),
    )
    op.create_table(
        'shows',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artists.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_shows_artist_start_time', 'shows', ['artist_id', 'start_time'], unique=False)
    op.create_index('ix_shows_venue_start_time', 'shows', ['venue_id', 'start_time'], unique=False)
    op.create_table(
        'venue_genres',
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('genre_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['genre_id'], ['genres.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id']),
        sa.PrimaryKeyConstraint('venue_id', 'genre_id'),
    )


def downgrade():
    op.drop_table('venue_genres')
    op.drop_index('ix_shows_venue_start_time', table_name='shows')
    op.drop_index('ix_shows_artist_start_time', table_name='shows')
    op.drop_table('shows')
    op.drop_table('artist_genres')
    op.drop_table('venues')
    op.drop_table('genres')
    op.drop_table('artists')
