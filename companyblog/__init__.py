# puppycompanyblog/__init__.py  copied
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)
Migrate(app,db)

#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



##################################################

from flask_dance.contrib.google import make_google_blueprint
from companyblog.core.views import core
from companyblog.users.views import users
from companyblog.blog_post.views import blog_posts
from companyblog.donation.view import donation
from companyblog.error_pages.handlers import error_pages

blueprint = make_google_blueprint(
    client_id="644025900860-hha7ilkb51abqeq0jklbi1hvg4itllch.apps.googleusercontent.com",
    client_secret="bITmYRUmY7eVhkbSmSk_PQyM",
    # reprompt_consent=True,
    offline=True,
    scope=["https://www.googleapis.com/auth/userinfo.email", "openid",
           "https://www.googleapis.com/auth/userinfo.profile"]
)

app.register_blueprint(blueprint, url_prefix='/oalogin')
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(donation)
app.register_blueprint(error_pages)