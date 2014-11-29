from flask import Flask, abort, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import os
import logging

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
        return math.sqrt((self.x_pc - self.star.x_pc) ** 2 + (self.y_pc - self.star.y_pc) ** 2 + (self.z_pc - self.star.z_pc) ** 2)


@app.route('/')
def home():
    habstars = Habstar.query.limit(25).all()

    return render_template('index.html', habstars=habstars)


@app.route('/habstar/<id>')
def detail(id):
    habstar = Habstar.query.get(id)
    if habstar:
        return render_template('detail.html', habstar=habstar)
    else:
        abort(404)


@app.route('/find')
def find():
    center_hipparchos_num = request.args.get('c')
    dist_pc = float(request.args.get('d'))

    center_habstar = Habstar.query.get(center_hipparchos_num)

    habstars = Habstar.query.all()
    near_habstars = filter(
        lambda near_habstar: 0 < near_habstar.dist_to_star < dist_pc,
        map(lambda habstar: NearHabstar(habstar, center_habstar), habstars))

    return render_template(
        'find.html', dist_pc=dist_pc, center_hipparchos_num=center_hipparchos_num, habstars=near_habstars)


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
