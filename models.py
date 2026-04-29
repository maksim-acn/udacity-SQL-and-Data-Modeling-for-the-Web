from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


artist_genres = db.Table(
    'artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
)


venue_genres = db.Table(
    'venue_genres',
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
)


class Venue(db.Model):
    __tablename__ = 'venues'
    __table_args__ = (
        db.UniqueConstraint('name', 'city', 'state', 'address', name='uq_venue_location'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    genres = db.relationship(
        'Genre',
        secondary=venue_genres,
        back_populates='venues',
        order_by='Genre.name',
    )
    shows = db.relationship(
        'Show',
        back_populates='venue',
        cascade='all, delete-orphan',
        order_by='Show.start_time',
    )

    def __repr__(self):
        return '<Venue {}>'.format(self.name)


class Artist(db.Model):
    __tablename__ = 'artists'
    __table_args__ = (
        db.UniqueConstraint('name', 'city', 'state', name='uq_artist_location'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    genres = db.relationship(
        'Genre',
        secondary=artist_genres,
        back_populates='artists',
        order_by='Genre.name',
    )
    shows = db.relationship(
        'Show',
        back_populates='artist',
        cascade='all, delete-orphan',
        order_by='Show.start_time',
    )

    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    artists = db.relationship(
        'Artist',
        secondary=artist_genres,
        back_populates='genres',
    )
    venues = db.relationship(
        'Venue',
        secondary=venue_genres,
        back_populates='genres',
    )

    def __repr__(self):
        return '<Genre {}>'.format(self.name)


class Show(db.Model):
    __tablename__ = 'shows'
    __table_args__ = (
        db.Index('ix_shows_venue_start_time', 'venue_id', 'start_time'),
        db.Index('ix_shows_artist_start_time', 'artist_id', 'start_time'),
    )

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    venue = db.relationship('Venue', back_populates='shows')
    artist = db.relationship('Artist', back_populates='shows')

    def __repr__(self):
        return '<Show artist_id={} venue_id={} start_time={}>'.format(
            self.artist_id,
            self.venue_id,
            self.start_time,
        )
