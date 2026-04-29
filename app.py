#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from collections import defaultdict
from datetime import datetime
import logging
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from forms import ArtistForm, ShowForm, VenueForm
from models import Artist, Genre, Show, Venue, db

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Helpers.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = value if isinstance(value, datetime) else dateutil.parser.parse(value)
  if format == 'full':
      format = "EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format = "EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')


def show_time(value):
  return value.isoformat()


def now():
  return datetime.now()


def genres_from_names(names):
  genres = []
  for name in names or []:
    genre = Genre.query.filter_by(name=name).one_or_none()
    if genre is None:
      genre = Genre(name=name)
      db.session.add(genre)
    genres.append(genre)
  return genres


def upcoming_show_count_for_venue(venue_id):
  return Show.query.filter(
    Show.venue_id == venue_id,
    Show.start_time >= now()
  ).count()


def upcoming_show_count_for_artist(artist_id):
  return Show.query.filter(
    Show.artist_id == artist_id,
    Show.start_time >= now()
  ).count()


def venue_summary(venue):
  return {
    'id': venue.id,
    'name': venue.name,
    'num_upcoming_shows': upcoming_show_count_for_venue(venue.id),
  }


def artist_summary(artist):
  return {
    'id': artist.id,
    'name': artist.name,
    'num_upcoming_shows': upcoming_show_count_for_artist(artist.id),
  }


def show_summary(show):
  return {
    'venue_id': show.venue_id,
    'venue_name': show.venue.name,
    'artist_id': show.artist_id,
    'artist_name': show.artist.name,
    'artist_image_link': show.artist.image_link,
    'start_time': show_time(show.start_time),
  }


def venue_show_summary(show):
  return {
    'artist_id': show.artist_id,
    'artist_name': show.artist.name,
    'artist_image_link': show.artist.image_link,
    'start_time': show_time(show.start_time),
  }


def artist_show_summary(show):
  return {
    'venue_id': show.venue_id,
    'venue_name': show.venue.name,
    'venue_image_link': show.venue.image_link,
    'start_time': show_time(show.start_time),
  }


def venue_detail(venue):
  current_time = now()
  past_shows = [
    venue_show_summary(show)
    for show in venue.shows
    if show.start_time < current_time
  ]
  upcoming_shows = [
    venue_show_summary(show)
    for show in venue.shows
    if show.start_time >= current_time
  ]

  return {
    'id': venue.id,
    'name': venue.name,
    'genres': [genre.name for genre in venue.genres],
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website_link,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
  }


def artist_detail(artist):
  current_time = now()
  past_shows = [
    artist_show_summary(show)
    for show in artist.shows
    if show.start_time < current_time
  ]
  upcoming_shows = [
    artist_show_summary(show)
    for show in artist.shows
    if show.start_time >= current_time
  ]

  return {
    'id': artist.id,
    'name': artist.name,
    'genres': [genre.name for genre in artist.genres],
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website_link,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
  }


def apply_venue_form(venue, form):
  venue.name = form.name.data
  venue.city = form.city.data
  venue.state = form.state.data
  venue.address = form.address.data
  venue.phone = form.phone.data
  venue.image_link = form.image_link.data
  venue.facebook_link = form.facebook_link.data
  venue.website_link = form.website_link.data
  venue.seeking_talent = form.seeking_talent.data
  venue.seeking_description = form.seeking_description.data
  venue.genres = genres_from_names(form.genres.data)


def apply_artist_form(artist, form):
  artist.name = form.name.data
  artist.city = form.city.data
  artist.state = form.state.data
  artist.phone = form.phone.data
  artist.image_link = form.image_link.data
  artist.facebook_link = form.facebook_link.data
  artist.website_link = form.website_link.data
  artist.seeking_venue = form.seeking_venue.data
  artist.seeking_description = form.seeking_description.data
  artist.genres = genres_from_names(form.genres.data)


def save_record(record, success_message, error_message):
  try:
    db.session.add(record)
    db.session.commit()
    flash(success_message)
    return True
  except IntegrityError:
    db.session.rollback()
    flash(error_message)
  except SQLAlchemyError:
    db.session.rollback()
    flash(error_message)
  return False


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues_by_area = defaultdict(list)
  all_venues = Venue.query.order_by(Venue.city, Venue.state, Venue.name).all()
  for venue in all_venues:
    venues_by_area[(venue.city, venue.state)].append(venue_summary(venue))

  data = [
    {
      'city': city,
      'state': state,
      'venues': area_venues,
    }
    for (city, state), area_venues in venues_by_area.items()
  ]
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_term))).all()
  response = {
    'count': len(results),
    'data': [venue_summary(venue) for venue in results],
  }
  return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=search_term
  )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  return render_template('pages/show_venue.html', venue=venue_detail(venue))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    venue = Venue()
    apply_venue_form(venue, form)
    save_record(
      venue,
      'Venue ' + venue.name + ' was successfully listed!',
      'An error occurred. Venue ' + venue.name + ' could not be listed.'
    )
  else:
    flash('An error occurred. Venue could not be listed.')
  return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    return '', 204
  except SQLAlchemyError:
    db.session.rollback()
    return '', 500


#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  data = [
    {
      'id': artist.id,
      'name': artist.name,
    }
    for artist in Artist.query.order_by(Artist.name).all()
  ]
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_term))).all()
  response = {
    'count': len(results),
    'data': [artist_summary(artist) for artist in results],
  }
  return render_template(
    'pages/search_artists.html',
    results=response,
    search_term=search_term
  )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  return render_template('pages/show_artist.html', artist=artist_detail(artist))


#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)
  form.genres.data = [genre.name for genre in artist.genres]
  return render_template(
    'forms/edit_artist.html',
    form=form,
    artist=artist_detail(artist)
  )


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(request.form)
  if form.validate():
    apply_artist_form(artist, form)
    save_record(
      artist,
      'Artist ' + artist.name + ' was successfully updated!',
      'An error occurred. Artist ' + artist.name + ' could not be updated.'
    )
  else:
    flash('An error occurred. Artist could not be updated.')
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  form.genres.data = [genre.name for genre in venue.genres]
  return render_template(
    'forms/edit_venue.html',
    form=form,
    venue=venue_detail(venue)
  )


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(request.form)
  if form.validate():
    apply_venue_form(venue, form)
    save_record(
      venue,
      'Venue ' + venue.name + ' was successfully updated!',
      'An error occurred. Venue ' + venue.name + ' could not be updated.'
    )
  else:
    flash('An error occurred. Venue could not be updated.')
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate():
    artist = Artist()
    apply_artist_form(artist, form)
    save_record(
      artist,
      'Artist ' + artist.name + ' was successfully listed!',
      'An error occurred. Artist ' + artist.name + ' could not be listed.'
    )
  else:
    flash('An error occurred. Artist could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = [
    show_summary(show)
    for show in Show.query.join(Show.artist).join(Show.venue).order_by(Show.start_time).all()
  ]
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  if not form.validate():
    flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')

  artist = Artist.query.get(form.artist_id.data)
  venue = Venue.query.get(form.venue_id.data)
  if artist is None or venue is None:
    flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')

  show = Show(
    artist_id=artist.id,
    venue_id=venue.id,
    start_time=form.start_time.data
  )
  save_record(
    show,
    'Show was successfully listed!',
    'An error occurred. Show could not be listed.'
  )
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()
