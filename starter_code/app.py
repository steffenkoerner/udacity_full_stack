#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean())
    website = db.Column(db.String(500))
    seeking_description = db.Column(db.String(500))

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres.split(','),
            'seeking_talent': self.seeking_talent,
            'website': self.website,
            'seeking_description': self.seeking_description
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  # implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500))
    seeking_description = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean())

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres.split(','),
            'seeking_venue': self.seeking_venue,
            'website': self.website,
            'seeking_description': self.seeking_description
        }

        def __repr__(self):
            return f'I am an artist'


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = "Show"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist = db.relationship("Artist")
    venue = db.relationship("Venue")


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


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
    regions = Venue.query.with_entities(
        Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    data = []

    for region in regions:
        region_venues = Venue.query.filter(
            Venue.city == region.city, Venue.state == region.state).all()
        venues = []
        for venue in region_venues:
            venues.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(Show.query.filter(Show.venue_id == venue.id, Show.start_time > datetime.now()).all())
            })
        data.append(
            {"city": region.city, "state": region.state, "venues": venues})

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term')
    num_venues = len(Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search))).all())
    venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(search))).all()

    search_result = []
    for venue in venues:
        search_result.append({
            "id": venue.id,
            "name": venue.name,
        })

    response = {
        "count": num_venues,
        "data": search_result,
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    query = Venue.query.get(venue_id)
    data = query.to_dict()
    data['upcoming_shows_count'] = len(Show.query.filter(
        Show.venue_id == venue_id, Show.start_time > datetime.now()).all())
    data['past_shows_count'] = len(Show.query.filter(
        Show.venue_id == venue_id, Show.start_time < datetime.now()).all())

    past_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.start_time < datetime.now()).all()
    data['past_shows'] = []
    for past_show in past_shows:
        data['past_shows'].append({
            "artist_id": past_show.artist_id,
            "artist_name": past_show.artist.name,
            "artist_image_link": past_show.artist.image_link,
            "start_time": past_show.start_time.strftime('%Y-%m-%d')
        })

    upcoming_shows = Show.query.filter(
        Show.venue_id == venue_id, Show.start_time > datetime.now()).all()
    data['upcoming_shows'] = []
    for upcoming_show in upcoming_shows:
        data['upcoming_shows'].append({
            "artist_id": upcoming_show.artist_id,
            "artist_name": upcoming_show.artist.name,
            "artist_image_link": upcoming_show.artist.image_link,
            "start_time": upcoming_show.start_time.strftime('%Y-%m-%d')
        })

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()

    venue = Venue()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            facebook_link=request.form['facebook_link'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            seeking_venue=True if request.form.get(
                'seeking_venue') == 'y' else False,
            seeking_description=request.form['seeking_description']

        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'success': False})
    finally:
        db.session.close()

    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    query = Artist.query.all()
    data = []
    for result in query:
        data += [{"id": result.id, "name": result.name}]

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term')
    num_artists = len(Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search))).all())
    artists = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search))).all()

    search_result = []
    for artist in artists:
        search_result.append({
            "id": artist.id,
            "name": artist.name,
        })

    response = {
        "count": num_artists,
        "data": search_result,
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    data = artist.to_dict()

    data['upcoming_shows_count'] = len(Show.query.filter(
        Show.artist_id == artist_id, Show.start_time > datetime.now()).all())
    data['past_shows_count'] = len(Show.query.filter(
        Show.artist_id == artist_id, Show.start_time < datetime.now()).all())

    past_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.start_time < datetime.now()).all()
    data['past_shows'] = []
    for past_show in past_shows:
        data['past_shows'].append({
            "artist_id": past_show.artist_id,
            "artist_name": past_show.artist.name,
            "artist_image_link": past_show.artist.image_link,
            "start_time": past_show.start_time.strftime('%Y-%m-%d')
        })

    upcoming_shows = Show.query.filter(
        Show.artist_id == artist_id, Show.start_time > datetime.now()).all()
    data['upcoming_shows'] = []
    for upcoming_show in upcoming_shows:
        data['upcoming_shows'].append({
            "artist_id": upcoming_show.artist_id,
            "artist_name": upcoming_show.artist.name,
            "artist_image_link": upcoming_show.artist.image_link,
            "start_time": upcoming_show.start_time.strftime('%Y-%m-%d')
        })

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    current_artist = Artist.query.get(artist_id)
    try:
        current_artist.name = request.form['name']
        current_artist.city = request.form['city']
        current_artist.state = request.form['state']
        current_artist.phone = request.form['phone']
        current_artist.facebook_link = request.form['facebook_link']
        current_artist.image_link = requst.form['image_link']
        current_artist.website = request.form['website']
        current_artist.seeking_venue = True if request.form.get(
            'seeking_venue') == 'y' else False
        current_artist.seeking_description = requst.form['seeking_description']
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(artist_id)
    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link']
        venue.image_link = request.form['image_link']
        venue.website = request.form['website']
        venue.seeking_talent = True if request.form.get(
            'seeking_talent') == 'y' else False,
        venue.seeking_description = requst.form['seeking_description']

        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist = Artist(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            genres=request.form['genres'],
            phone=request.form['phone'],
            facebook_link=request.form['facebook_link'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            seeking_venue=True if request.form.get(
                'seeking_venue') == 'y' else False,
            seeking_description=request.form['seeking_description']
        )

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d')
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
