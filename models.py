from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Habstar(Base):
    __tablename__ = 'habstar'

    hipparchos_num = Column(Integer, primary_key=True)
    ra_hours = Column(Integer)
    ra_minutes = Column(Integer)
    ra_seconds = Column(Float)
    dec_degrees = Column(Integer)
    dec_minutes = Column(Integer)
    dec_seconds = Column(Float)
    johnson_mag = Column(Float)
    parallax_mas = Column(Float)
    b_minus_v = Column(Float)
