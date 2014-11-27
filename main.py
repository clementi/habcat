from flask import Flask, abort, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Habstar

import os
import logging

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_CONFIG_OBJECT') or 'config.Config')
if app.debug:
    app.logger.setLevel(logging.INFO)
    app.logger.debug('Debug mode enabled.')
else:
    app.logger.setLevel(logging.WARN)

engine = create_engine('sqlite:///./data/habcat.sqlite')
Session = sessionmaker(bind=engine)


@app.route('/')
def home():
    session = Session()
    habstars = session.query(Habstar).limit(25)

    return render_template('index.html', habstars=habstars)


@app.route('/habstar/<id>')
def detail(id):
    session = Session()
    habstar = session.query(Habstar).get(id)
    if habstar:
        return render_template('detail.html', habstar=habstar)
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


if app.debug:
    app.run(host='0.0.0.0', port=9000)
