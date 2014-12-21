import os
import logging
import requests

from flask import Flask, render_template, request, abort

from flask.ext.sqlalchemy import SQLAlchemy
from models import Paginated
from space import BoundingCube


app = Flask(__name__)
app.config.from_object(os.environ.get('APP_CONFIG_OBJECT') or 'config.Config')
if app.debug:
    app.logger.setLevel(logging.INFO)
    app.logger.debug('Debug mode enabled.')
else:
    app.logger.setLevel(logging.WARN)

db = SQLAlchemy(app)


class Habstar(db.Model):
    __tablename__ = 'habstar'

    hipparchos_num = db.Column(db.Integer, primary_key=True)
    ra_hours = db.Column(db.Integer)
    ra_minutes = db.Column(db.Integer)
    ra_seconds = db.Column(db.Float)
    dec_degrees = db.Column(db.Integer)
    dec_minutes = db.Column(db.Integer)
    dec_seconds = db.Column(db.Float)
    johnson_mag = db.Column(db.Float)
    parallax_mas = db.Column(db.Float)
    sigma_parallax_mas = db.Column(db.Float)
    b_minus_v = db.Column(db.Float)
    dist_pc = db.Column(db.Float)
    x_pc = db.Column(db.Float)
    y_pc = db.Column(db.Float)
    z_pc = db.Column(db.Float)


class NearHabstar(object):
    def __init__(self, habstar, star):
        self.star = star
        self.hipparchos_num = habstar.hipparchos_num
        self.ra_hours = habstar.ra_hours
        self.ra_minutes = habstar.ra_minutes
        self.ra_seconds = habstar.ra_seconds
        self.dec_degrees = habstar.dec_degrees
        self.dec_minutes = habstar.dec_minutes
        self.dec_seconds = habstar.dec_seconds
        self.johnson_mag = habstar.johnson_mag
        self.parallax_mas = habstar.parallax_mas
        self.sigma_parallax_mas = habstar.sigma_parallax_mas
        self.b_minus_v = habstar.b_minus_v
        self.dist_pc = habstar.dist_pc
        self.x_pc = habstar.x_pc
        self.y_pc = habstar.y_pc
        self.z_pc = habstar.z_pc
        self.dist_to_star = self._distance()

    def _distance(self):
        import math

        return math.sqrt(
            (self.x_pc - self.star.x_pc) ** 2 + (self.y_pc - self.star.y_pc) ** 2 + (self.z_pc - self.star.z_pc) ** 2)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/browse')
def browse():
    page_arg = request.args.get('p') or '1'
    page = int(page_arg)

    response = requests.get('http://habcat-api-twisted.herokuapp.com/?p={}'.format(page))
    habstars = Paginated(response.json())

    return render_template('browse.html', habstars=habstars)

@app.route('/habstar/<id>')
def detail(id):
    # habstar = Habstar.query.get_or_404(id)
    response = requests.get('http://habcat-api-twisted.herokuapp.com/{}'.format(id))
    if response.status_code == 404:
        abort(404)
    habstar = response.json()

    return render_template('detail.html', habstar=habstar)


@app.route('/find')
def find():
    query_type = request.args.get('t')

    reference_hipparchos_num = request.args.get('c')
    reference_habstar = Habstar.query.get(reference_hipparchos_num)

    dist_pc = 0

    if query_type.lower() == 'd':
        dist_pc = float(request.args.get('d'))

        center_coords = (reference_habstar.x_pc, reference_habstar.y_pc, reference_habstar.z_pc)
        bounding_cube = BoundingCube(center_coords, dist_pc)

        x_bounds = bounding_cube.get_x_bounds()
        y_bounds = bounding_cube.get_y_bounds()
        z_bounds = bounding_cube.get_z_bounds()

        bounded_habstars = Habstar.query\
            .filter(Habstar.x_pc > x_bounds[0])\
            .filter(Habstar.x_pc < x_bounds[1])\
            .filter(Habstar.y_pc > y_bounds[0])\
            .filter(Habstar.y_pc < y_bounds[1])\
            .filter(Habstar.z_pc > z_bounds[0])\
            .filter(Habstar.z_pc < z_bounds[1])

        filtered_habstars = filter(
            lambda filtered_habstar: 0 < filtered_habstar.dist_to_star < dist_pc,
            map(lambda habstar: NearHabstar(habstar, reference_habstar), bounded_habstars))

        title = 'Habstars within {} pc of Hipparcos {}'.format(dist_pc, reference_hipparchos_num)
    elif query_type.lower() == 'm':
        reference_mag = reference_habstar.johnson_mag
        upper_mag = reference_mag * 1.01
        lower_mag = reference_mag * 0.99
        filtered_habstars = Habstar.query.filter(Habstar.johnson_mag < upper_mag).filter(
            Habstar.johnson_mag > lower_mag)
        title = 'Habstars with similar magnitude to Hipparcos {}'.format(reference_hipparchos_num)
    elif query_type.lower() == 'c':
        reference_b_minus_v = reference_habstar.b_minus_v
        upper_b_minus_v = reference_b_minus_v * 1.01
        lower_b_minus_v = reference_b_minus_v * 0.99
        filtered_habstars = Habstar.query.filter(Habstar.b_minus_v < upper_b_minus_v).filter(
            Habstar.b_minus_v > lower_b_minus_v)
        title = 'Habstars with similar color to Hipparcos {}'.format(reference_hipparchos_num)

    return render_template(
        'find.html', title=title, center_hipparchos_num=reference_hipparchos_num, habstars=filtered_habstars)


def distance(habstar1, habstar2):
    import math

    return math.sqrt(
        (habstar1.x_pc - habstar2.x_pc) ** 2 +
        (habstar1.y_pc - habstar2.y_pc) ** 2 +
        (habstar1.z_pc - habstar2.z_pc) ** 2)


@app.route('/download')
def download():
    return render_template('download.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


if app.debug:
    app.run(host='0.0.0.0', port=9000)
