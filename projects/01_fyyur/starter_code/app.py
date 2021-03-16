# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

# import sys
# sys.path.append("/home/alvaro/PycharmProjects/FullStack_Project1/FSND/projects/01_fyyur/starter_code")

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

# parent
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship('Show_Table', backref='venues', lazy='select')

    def __repr__(self):
        return "< [{}] id: {}, genres: {} >".format(
            self.__tablename__,
            self.id,
            self.genres)


# parent
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.PickleType)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show_Table', backref='artists', lazy='select')


# child
class Show_Table(db.Model):
    __tablename__ = 'Show_Table'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


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
    venues_list_of_tuple = Venue.query.with_entities(Venue.city, Venue).group_by(Venue.city, Venue).all()
    location_lst = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

    data = []
    for (city, state) in location_lst:
        element = {
            'city': city,
            'state': state,
            'venues': []}
        data.append(element)

    total_upcoming_shows = 0
    for (city, venue) in venues_list_of_tuple:
        data_ptr = [element for element in data if element['city'] == city]

        num_upcoming_shows = len(Show_Table.query
                                 .filter(Show_Table.venue_id == venue.id)
                                 .filter(Show_Table.start_time >= datetime.today())
                                 .all())

        total_upcoming_shows = total_upcoming_shows + num_upcoming_shows

        new_venue_info = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": total_upcoming_shows}

        data_ptr[0]['venues'].append(new_venue_info)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')

    venue_list = Venue.query.all()

    venue_result_lst = [element for element in venue_list if search_term.upper() in element.name.upper()]

    response = {'count': len(venue_result_lst)}

    data = []
    for venue in venue_result_lst:
        upcoming_shows_lst = Show_Table.query \
            .filter(Show_Table.venue_id == venue.id) \
            .filter(Show_Table.start_time >= datetime.today()) \
            .all()

        element = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcoming_shows_lst),
        }
        data.append(element)

    response['data'] = data
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    db.session.close()

    if venue is None:
        return redirect(url_for('venues'))
    else:
        data = venue.__dict__

        show_list_past = Show_Table.query \
            .filter(Show_Table.venue_id == venue_id) \
            .filter(Show_Table.start_time < datetime.today()) \
            .all()

        show_list_upcoming = Show_Table.query \
            .filter(Show_Table.venue_id == venue_id) \
            .filter(Show_Table.start_time >= datetime.today()) \
            .all()

        result = []
        for show in show_list_past:
            element = {
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["past_shows"] = result
        data["past_shows_count"] = len(result)

        result = []
        for show in show_list_upcoming:
            element = {
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["upcoming_shows"] = result
        data["upcoming_shows_count"] = len(result)

        return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    print('create_venue_submission()')
    # print( Venue.query.first() )
    # Venue.query.filter_by(id=1).delete()

    try:
        venue = Venue(name=request.form['name'],
                      city=request.form['city'],
                      state=request.form['state'],
                      address=request.form['address'],
                      phone=request.form['phone'],
                      genres=request.form.getlist('genres'),
                      image_link=request.form['image_link'],
                      facebook_link=request.form['facebook_link'],
                      website=request.form['website'],
                      seeking_talent=(request.form['seeking_talent'] == 'True'),
                      seeking_description=request.form['seeking_description'])

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()

        flash('Venue was successfully deleted!')

    except:
        db.session.rollback()
        print(sys.exc_info())

        venue = Venue.query.get(venue_id)
        flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')

    return jsonify({'success': True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artist_lst_of_tuple = list(Artist.query.with_entities(Artist.id, Artist.name))

    data = []
    for (record_id, name) in artist_lst_of_tuple:
        element = {'id': record_id,
                   'name': name}

        data.append(element)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')

    artist_list = Artist.query.all()

    artist_result_lst = [element for element in artist_list if search_term.upper() in element.name.upper()]

    response = {'count': len(artist_result_lst)}

    data = []
    for artist in artist_result_lst:
        upcoming_shows_lst = Show_Table.query \
            .filter(Show_Table.artist_id == artist.id) \
            .filter(Show_Table.start_time >= datetime.today()) \
            .all()

        element = {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(upcoming_shows_lst),
        }
        data.append(element)

    response['data'] = data

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    db.session.close()

    if artist is None:
        return redirect(url_for('artists'))
    else:
        data = artist.__dict__

        show_list_past = Show_Table.query \
            .filter(Show_Table.artist_id == artist_id) \
            .filter(Show_Table.start_time < datetime.today()) \
            .all()

        show_list_upcoming = Show_Table.query \
            .filter(Show_Table.artist_id == artist_id) \
            .filter(Show_Table.start_time >= datetime.today()) \
            .all()

        result = []
        for show in show_list_past:
            element = {
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["past_shows"] = result
        data["past_shows_count"] = len(result)

        result = []
        for show in show_list_upcoming:
            element = {
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["upcoming_shows"] = result
        data["upcoming_shows_count"] = len(result)

        return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    db.session.close()

    if artist is None:
        return redirect(url_for('artists'))
    else:
        form = ArtistForm(obj=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        column_names = Artist.__table__.columns.keys()[1:]  # skip 'id' column field
        for key in column_names:
            if key == 'seeking_venue':
                artist.__setattr__(key, request.form.get(key) == 'True')
            elif key == 'genres':
                artist.__setattr__(key, request.form.getlist(key))
            else:
                artist.__setattr__(key, request.form.get(key))

        db.session.commit()

        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    db.session.close()

    if venue is None:
        return redirect(url_for('venues'))
    else:
        form = VenueForm(obj=venue)
        return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        column_names = Venue.__table__.columns.keys()[1:]  # skip 'id' column field
        for key in column_names:
            if key == 'seeking_talent':
                venue.__setattr__(key, request.form.get(key) == 'True')
            elif key == 'genres':
                venue.__setattr__(key, request.form.getlist(key))
            else:
                venue.__setattr__(key, request.form.get(key))

        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

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
        artist = Artist(name=request.form['name'],
                        city=request.form['city'],
                        state=request.form['state'],
                        phone=request.form['phone'],
                        genres=request.form.getlist('genres'),
                        image_link=request.form['image_link'],
                        facebook_link=request.form['facebook_link'],
                        website=request.form['website'],
                        seeking_venue=(request.form['seeking_venue'] == 'True'),
                        seeking_description=request.form['seeking_description'])

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows_list = Show_Table.query.all()
    for show in shows_list:
        element = {"venue_id": show.venues.id,
                   "venue_name": show.venues.name,
                   "artist_id": show.artists.id,
                   "artist_name": show.artists.name,
                   "artist_image_link": show.artists.image_link,
                   "start_time": str(show.start_time)}

        data.append(element)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show_Table(
            venue_id=int(request.form['venue_id']),
            artist_id=int(request.form['artist_id']),
            start_time=dateutil.parser.parse(request.form['start_time']))
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
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
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
