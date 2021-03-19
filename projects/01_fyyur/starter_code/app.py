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
from Models import *

# import sys
# sys.path.append("/home/alvaro/PycharmProjects/FullStack_Project1/FSND/projects/01_fyyur/starter_code")

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

print(app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)

migrate = Migrate(app, db, compare_type=True)


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
    cities = [r.city for r in db.session.query(Venue.city).distinct()]

    data = []
    aggregated_sum = 0
    for city_name in cities:

        query = db.session.query(Venue, db.func.count('num_upcoming_shows')) \
            .outerjoin(Show_Table) \
            .filter(Venue.city == city_name) \
            .group_by(Venue.id) \
            .having(db.func.count('num_upcoming_shows') > 0)
        venues = [venue for (venue, numShows) in query.all()]

        upcomingShows_LUT = dict(query
                                 .filter(Show_Table.start_time >= datetime.today())
                                 .all())

        venue_lst = []
        for venue in venues:
            aggregated_sum = aggregated_sum + upcomingShows_LUT.get(venue, 0)
            venue_info = {"id": venue.id,
                          "name": venue.name,
                          "num_upcoming_shows": aggregated_sum}
            venue_lst.append(venue_info)

        city_info = {
            'city': city_name,
            'state': venue.state,
            'venues': venue_lst}

        data.append(city_info)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    search_term = "%{}%".format(search_term)

    query = db.session.query(Venue, db.func.count('num_upcoming_shows')) \
        .outerjoin(Show_Table) \
        .filter(Venue.name.ilike(search_term)) \
        .group_by(Venue.id) \
        .having(db.func.count('num_upcoming_shows') > 0)

    response = {'count': query.count()}

    venues = [venue for (venue, numShows) in query.all()]

    upcomingShows_LUT = dict(query
                             .filter(Show_Table.start_time >= datetime.today())
                             .all())
    data = []
    for venue in venues:
        venue_info = {"id": venue.id,
                      "name": venue.name,
                      "num_upcoming_shows": upcomingShows_LUT.get(venue, 0)}
        data.append(venue_info)

    response['data'] = data
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    query_venue = db.session.query(Venue)\
                   .filter(Venue.id == venue_id)

    if not query_venue.all():
        return render_template('errors/404.html')
    else:

        data = query_venue.all()[0].__dict__

        query = db.session.query(Show_Table) \
            .outerjoin(Venue) \
            .filter(Show_Table.venue_id == venue_id)

        upcoming_shows_query = query \
            .filter(Show_Table.start_time >= datetime.today())

        result = []
        for show in upcoming_shows_query.all():
            element = {
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["upcoming_shows"] = result
        data["upcoming_shows_count"] = upcoming_shows_query.count()

        past_shows_query = query \
            .filter(Show_Table.start_time < datetime.today())

        result = []
        for show in past_shows_query.all():
            element = {
                "artist_id": show.artists.id,
                "artist_name": show.artists.name,
                "artist_image_link": show.artists.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["past_shows"] = result
        data["past_shows_count"] = past_shows_query.count()
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
    data = []
    for (record_id, name) in db.session.query(Artist.id, Artist.name):
        element = {'id': record_id,
                   'name': name}

        data.append(element)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    search_term = request.form.get('search_term', '')
    search_term = "%{}%".format(search_term)

    query = db.session.query(Artist, db.func.count('num_upcoming_shows')) \
        .outerjoin(Show_Table) \
        .filter(Artist.name.ilike(search_term)) \
        .group_by(Artist.id) \
        .having(db.func.count('num_upcoming_shows') > 0)

    response = {'count': query.count()}

    artists = [artist for (artist, numShows) in query.all()]

    upcomingShows_LUT = dict(query
                             .filter(Show_Table.start_time >= datetime.today())
                             .all())
    data = []
    for artist in artists:
        artist_info = {"id": artist.id,
                       "name": artist.name,
                       "num_upcoming_shows": upcomingShows_LUT.get(artist, 0)}
        data.append(artist_info)

    response['data'] = data

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    query_artist = db.session.query(Artist) \
        .filter(Artist.id == artist_id)

    if not query_artist.all():
        return render_template('errors/404.html')
    else:
        data = query_artist.all()[0].__dict__

        query = db.session.query(Show_Table) \
            .outerjoin(Artist) \
            .filter(Show_Table.artist_id == artist_id)

        upcoming_shows_query = query \
            .filter(Show_Table.start_time >= datetime.today())

        result = []
        for show in upcoming_shows_query.all():
            element = {
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["upcoming_shows"] = result
        data["upcoming_shows_count"] = upcoming_shows_query.count()

        past_shows_query = query \
            .filter(Show_Table.start_time < datetime.today())

        result = []
        for show in past_shows_query.all():
            element = {
                "venue_id": show.venues.id,
                "venue_name": show.venues.name,
                "venue_image_link": show.venues.image_link,
                "start_time": str(show.start_time)}
            result.append(element)

        data["past_shows"] = result
        data["past_shows_count"] = past_shows_query.count()

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
