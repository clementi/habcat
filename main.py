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
    dist_pc = request.args.get('d')

    center_habstar = Habstar.query.get(center_hipparchos_num)

    habstars = Habstar.query.all()

    return render_template('find.html', dist_pc=dist_pc, center_hipparchos_num=center_hipparchos_num, habstars=habstars)


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


if app.debug:
    app.run(host='0.0.0.0', port=9000)
