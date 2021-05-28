import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://someuser:12345@localhost/blog_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5
