from flask import Flask, abort, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from models import Habstar


app = Flask(__name__)
engine = create_engine('sqlite:///./data/habcat.sqlite')
Session = sessionmaker(bind=engine)


@app.route('/')
def home():
    session = Session()
    random_habstars = session.query(Habstar).order_by(func.random()).limit(5)

    return render_template('index.html', random_habstars=random_habstars)


@app.route('/habstar/<id>')
def detail(id):
    session = Session()
    habstar = session.query(Habstar).get(id)
    if habstar:
        return render_template('detail.html', habstar=habstar)
    else:
        abort(404)


app.run(debug=True)