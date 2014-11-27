class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./data/habcat.sqlite'


class DevelopmentConfig(Config):
    DEBUG = True
