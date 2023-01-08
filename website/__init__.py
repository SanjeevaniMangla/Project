# made this website folder a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

UPLOAD_FOLDER = 'C:\\Users\\Dell\\OneDrive\\Desktop\\clone\\website\\static'
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__,static_folder='static')
    app.config['SECRET_KEY'] = 'jdhjhzcljzh'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #Initializing the database by giving it the flask app
    
    
    
    from .views import views
    from .auth import auth
    from .api import api
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    from .models import User, Post, Likes, Comments, Notifications, followers
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    






