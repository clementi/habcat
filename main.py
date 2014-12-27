import os
import logging
from flask import Flask, render_template, request, abort
from flask.ext.sqlalchemy import SQLAlchemy

from api import HabstarClient


API_BASE_URL = 'http://habcat-api-twisted.herokuapp.com'
api_client = HabstarClient(API_BASE_URL)

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
    page_num = int(request.args.get('p') or '1')
    habstars = api_client.get_habstars(page_num)

    return render_template('browse.html', habstars=habstars)

@app.route('/habstar/<hip_num>')
def detail(hip_num):
    habstar = api_client.get_habstar(hip_num)
    if not habstar:
        abort(404)

    return render_template('detail.html', habstar=habstar)


@app.route('/find')
def find():
    query_type = request.args.get('t')
    page_num = int(request.args.get('p') or '1')

    reference_hipparchos_num = request.args.get('c')
    reference_habstar = Habstar.query.get(reference_hipparchos_num)

    if query_type.lower() == 'd':
        dist_pc = float(request.args.get('d'))

        filtered_habstars = api_client.get_habstars_by_distance(reference_hipparchos_num, dist_pc, page_num)
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


@app.route('/download')
def download():
    return render_template('download.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


if app.debug:
    app.run(host='0.0.0.0', port=9000)
