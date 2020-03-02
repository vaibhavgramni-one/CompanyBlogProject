import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

## database configuration ##
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir , 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'KEY'

db = SQLAlchemy(app)

Migrate(app , db)
## database configuration done ##

## initializing app with login manager ##

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


from puppycompanyblog.core.views import core
from puppycompanyblog.error_pages.error_handlers import error_page
from puppycompanyblog.users.views import users
from puppycompanyblog.blogpost.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_page)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
