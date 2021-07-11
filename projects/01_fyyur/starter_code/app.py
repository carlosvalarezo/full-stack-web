# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import datetime
import json

import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from logging import Formatter, FileHandler
from flask_moment import Moment
from flask_migrate import Migrate
from flask_wtf import FlaskForm

from forms import *
import os

from models.models import db, Artist, Venue, Show

import logging

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

logging.basicConfig(level=logging.DEBUG)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    venue_data = db.session.query(Venue)
    for venue in venue_data:
        num_upcoming_shows = db.session.query(Show).filter(venue.id == Show.venue_id).count()
        data.append({"city": venue.city,
                     "state": venue.state,
                     "venues": [{
                         "id": venue.id,
                         "name": venue.name,
                         "num_upcoming_shows": num_upcoming_shows
                     }]})
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search = f"%{search_term}%"
    count = Venue.query.filter(Venue.name.ilike(search)).count()
    data = Venue.query.filter(Venue.name.ilike(search)).all()
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    past_shows_1 = []
    upcoming_shows_1 = []
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    upcoming_shows = db.session.query(Venue, Show.start_time.label("start_time"), Artist.name.label("name"),
                                      Artist.id.label("id"), Artist.image_link.label("image_link")).filter(
        Venue.id == venue_id).filter(Venue.id == Show.venue_id).filter(Artist.id == Show.artist_id).filter(
        Show.start_time > datetime.now())
    past_shows = db.session.query(Venue, Show.start_time.label("start_time"), Artist.name.label("name"),
                                  Artist.id.label("id"), Artist.image_link.label("image_link")).filter(
        Artist.id == venue_id).filter(Artist.id == Show.artist_id).filter(Venue.id == Show.venue_id).filter(
        Show.start_time < datetime.now())
    data = dict(id=venue.id, name=venue.name, genres=venue.genres, city=venue.city, state=venue.state,
                phone=venue.phone, facebook_link=venue.facebook_link, seeking_talent=venue.seeking_talent,
                image_link=venue.image_link)
    for uc in upcoming_shows:
        upcoming_shows_obj = {
            "artist_id": uc.id,
            "artist_name": uc.name,
            "artist_image_link": uc.image_link,
            "start_time": str(uc.start_time)
        }
        upcoming_shows_1.append(upcoming_shows_obj)

    for ps in past_shows:
        past_shows_obj = dict(artist_id=ps.id, artist_name=ps.name, artist_image_link=ps.image_link,
                              start_time=str(ps.start_time))
        past_shows_1.append(past_shows_obj)

    data.update({"past_shows": past_shows_1})
    data.update({"upcoming_shows": upcoming_shows_1})
    data.update({"past_shows_count": len(past_shows_1)})
    data.update({"upcoming_shows_count": len(upcoming_shows_1)})

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    venue_form = VenueForm()
    return render_template('forms/new_venue.html', form=venue_form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm()
    try:
        name = venue_form.name.data
        city = venue_form.city.data
        state = venue_form.state.data
        address = venue_form.address.data
        phone = venue_form.phone.data
        genres = venue_form.genres.data
        facebook_link = venue_form.facebook_link.data
        image_link = venue_form.image_link.data
        website_link = venue_form.website_link.data
        seeking_talent = venue_form.seeking_talent.data
        if seeking_talent == 'y':
            seeking_talent = True
        if seeking_talent == 'n':
            seeking_talent = False
        seeking_description = venue_form.seeking_description.data
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres,
                      facebook_link=facebook_link, image_link=image_link, website_link=website_link,
                      seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue {name} was successfully listed!')
    except Exception as e:
        logging.error("A Debug Logging Message")(e)
        db.session.rollback()
        flash(f'Venue {name} was unsuccessfully listed!')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_venue": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = db.session.query(Artist)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    search = f"%{search_term}%"
    count = Artist.query.filter(Artist.name.like(search)).count()
    data = Artist.query.filter(Artist.name.like(search)).all()
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    past_shows_1 = []
    upcoming_shows_1 = []
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    upcoming_shows = db.session.query(Artist, Show.start_time.label("start_time"), Venue.name.label("name"),
                                      Venue.id.label("id"), Venue.image_link.label("image_link")).filter(
        Artist.id == artist_id).filter(Artist.id == Show.artist_id).filter(Venue.id == Show.venue_id).filter(
        Show.start_time > datetime.now())
    past_shows = db.session.query(Artist, Show.start_time.label("start_time"), Venue.name.label("name"),
                                  Venue.id.label("id"), Venue.image_link.label("image_link")).filter(
        Artist.id == artist_id).filter(Artist.id == Show.artist_id).filter(Venue.id == Show.venue_id).filter(
        Show.start_time < datetime.now())
    data = dict(id=artist.id, name=artist.name, genres=artist.genres, city=artist.city, state=artist.state,
                phone=artist.phone, facebook_link=artist.facebook_link, seeking_venue=artist.seeking_venue,
                image_link=artist.image_link)
    for uc in upcoming_shows:
        upcoming_shows_obj = dict(venue_id=uc.id, venue_name=uc.name, venue_image_link=uc.image_link,
                                  start_time=str(uc.start_time))
        upcoming_shows_1.append(upcoming_shows_obj)

    for ps in past_shows:
        past_shows_obj = dict(venue_id=ps.id, venue_name=ps.name, venue_image_link=ps.image_link,
                              start_time=str(ps.start_time))
        past_shows_1.append(past_shows_obj
                            )
    data.update({"past_shows": past_shows_1})
    data.update({"upcoming_shows": upcoming_shows_1})
    data.update({"past_shows_count": len(past_shows_1)})
    data.update({"upcoming_shows_count": len(upcoming_shows_1)})

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    artist_form = ArtistForm()
    try:
        name = artist_form.name.data
        city = artist_form.city.data
        state = artist_form.state.data
        phone = artist_form.phone.data
        genres = artist_form.genres.data
        facebook_link = artist_form.facebook_link.data
        image_link = artist_form.image_link.data
        website_link = artist_form.website_link.data
        seeking_venue = artist_form.seeking_venue.data
        if seeking_venue == 'y':
            seeking_venue = True
        if seeking_venue == 'n':
            seeking_venue = False
        seeking_description = artist_form.seeking_description.data
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,
                        facebook_link=facebook_link, image_link=image_link, website_link=website_link,
                        seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash(f'Artist {name} was successfully listed!')
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(f'An error occurred. Artist {name} could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows_at_venue = Venue.query.join(Show, Venue.id == Show.venue_id).with_entities(Venue.id.label('venue_id'),
                                                                                     Venue.name.label('venue_name'),
                                                                                     Show.start_time.label(
                                                                                         'start_time'))

    shows_by_artist = Artist.query.join(Show, Artist.id == Show.artist_id).with_entities(Artist.id.label('artist_id'),
                                                                                         Artist.name.label(
                                                                                             'artist_name'),
                                                                                         Artist.image_link.label(
                                                                                             'artist_image_link'))

    data = []
    for sv, sa in [(x, y) for x in shows_at_venue for y in shows_by_artist]:
        data.append({"venue_id": sv['venue_id'],
                     "venue_name": sv['venue_name'],
                     "artist_id": sa['artist_id'],
                     "artist_name": sa['artist_name'],
                     "artist_image_link": sa['artist_image_link'],
                     "start_time": str(sv['start_time'])})
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        artist_id = request.form.get('artist_id')
        venue_id = request.form.get('venue_id')
        start_time = request.form.get('start_time', datetime.now())
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        print(show)
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
