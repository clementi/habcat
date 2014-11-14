from flask import Flask, abort, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Habstar


app = Flask(__name__)
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


app.run(debug=True)