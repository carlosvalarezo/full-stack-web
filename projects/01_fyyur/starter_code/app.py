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


def _format_generes(genres_param):
    genres = []
    genre = ""
    for v in genres_param:
        if v == '{' or v == '"':
            continue
        if v == ',' or v == '}':
            genres.append(genre)
            genre = ""
        if v is not ',':
            genre += v
    return genres


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
    genres = _format_generes(venue.genres)
    data = dict(id=venue.id, name=venue.name, genres=genres, address=venue.address, city=venue.city, state=venue.state,
                phone=venue.phone, website_link=venue.website_link, facebook_link=venue.facebook_link,
                seeking_talent=venue.seeking_talent,
                image_link=venue.image_link, seeking_description=venue.seeking_description)
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
    venue_form = VenueForm()
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    try:
        venue_form.name.data = venue.name
        venue_form.city.data = venue.city
        venue_form.state.data = venue.state
        venue_form.phone.data = venue.phone
        venue_form.genres.data = venue.genres
        venue_form.facebook_link.data = venue.facebook_link
        venue_form.image_link.data = venue.image_link
        venue_form.website_link.data = venue.website_link
        venue_form.seeking_talent.data = venue.seeking_talent
        venue_form.seeking_description.data = venue.seeking_description
        flash(f'Artist {venue.name} was successfully updated!')
    except Exception as e:
        logging.error("A Debug Logging Message")(e)
        db.session.rollback()
        flash(f'Venue {venue.name} was unsuccessfully listed!')
    finally:
        db.session.close()
    return render_template('forms/edit_venue.html', form=venue_form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue_form = VenueForm()
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    try:
        venue.name = venue_form.name.data
        venue.city = venue_form.city.data
        venue.state = venue_form.state.data
        venue.address = venue_form.address.data
        venue.phone = venue_form.phone.data
        venue.genres = venue_form.genres.data
        venue.facebook_link = venue_form.facebook_link.data
        venue.image_link = venue_form.image_link.data
        venue.website_link = venue_form.website_link.data
        seeking_talent = venue_form.seeking_talent.data
        if seeking_talent == 'y':
            venue.seeking_talent = True
        if seeking_talent == 'n':
            venue.seeking_talent = False
        venue.seeking_description = venue_form.seeking_description.data
        db.session.commit()
        flash(f'Venue {venue.name} was successfully updated!')
    except Exception as e:
        logging.error("A Debug Logging Message")(e)
        db.session.rollback()
        flash(f'Venue {venue.name} was unsuccessfully listed!')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
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
    genres = _format_generes(artist.genres)
    data = dict(id=artist.id, name=artist.name, genres=genres, city=artist.city, state=artist.state,
                phone=artist.phone, website_link=artist.website_link, facebook_link=artist.facebook_link,
                seeking_venue=artist.seeking_venue,
                seeking_description=artist.seeking_description, image_link=artist.image_link)
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
    artist_form = ArtistForm()
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    try:
        artist_form.name.data = artist.name
        artist_form.city.data = artist.city
        artist_form.state.data = artist.state
        artist_form.phone.data = artist.phone
        artist_form.genres.data = artist.genres
        artist_form.facebook_link.data = artist.facebook_link
        artist_form.image_link.data = artist.image_link
        artist_form.website_link.data = artist.website_link
        artist_form.seeking_venue.data = artist.seeking_venue
        artist_form.seeking_description.data = artist.seeking_description
        flash(f'Artist {artist.name} was successfully updated!')
    except Exception as e:
        logging.error("A Debug Logging Message")(e)
        db.session.rollback()
        flash(f'Artis {artist.name} was unsuccessfully listed!')
    finally:
        db.session.close()
    return render_template('forms/edit_artist.html', form=artist_form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist_form = ArtistForm()
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    try:
        artist.name = artist_form.name.data
        artist.city = artist_form.city.data
        artist.state = artist_form.state.data
        artist.phone = artist_form.phone.data
        artist.genres = artist_form.genres.data
        artist.facebook_link = artist_form.facebook_link.data
        artist.image_link = artist_form.image_link.data
        artist.website_link = artist_form.website_link.data
        artist.seeking_venue = artist_form.seeking_venue.data
        artist.seeking_description = artist_form.seeking_description.data
        db.session.commit()
        flash(f'Artist {artist.name} was successfully updated!')
    except Exception as e:
        logging.error("A Debug Logging Message")(e)
        db.session.rollback()
        flash(f'Artis {artist.name} was unsuccessfully listed!')
    finally:
        db.session.close()
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
        seeking_description = artist_form.seeking_description.data
        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres,
                        facebook_link=facebook_link, image_link=image_link, website_link=website_link,
                        seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        flash(f'Artist {name} was successfully listed!')
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        flash(f'An error occurred. Artist {name} could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows_data = Show.query.join(Artist, Venue).with_entities(Venue.id.label('venue_id'),
                                                              Venue.name.label('venue_name'),
                                                              Show.start_time.label(
                                                                  'start_time'),
                                                              Artist.id.label('artist_id'),
                                                              Artist.name.label(
                                                                  'artist_name'),
                                                              Artist.image_link.label(
                                                                  'artist_image_link')
                                                              ).all()
    for s in shows_data:
        data.append({"venue_id": s.venue_id,
                     "venue_name": s.venue_name,
                     "artist_id": s.artist_id,
                     "artist_name": s.artist_name,
                     "artist_image_link": s.artist_image_link,
                     "start_time": str(s.start_time)})
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    show_form = ShowForm()
    try:
        artist_id = show_form.artist_id.data
        venue_id = show_form.venue_id.data
        start_time = show_form.start_time.data
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        print(show)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception as e:
        logging.error(e)
        db.session.rollback()
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
