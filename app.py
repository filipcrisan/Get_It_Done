"""
    The app is assembled based on the database, migrations, login manager and the needed blueprints.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os


# the actual app, with config variables
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


# create the database and the migration system and link them to the app
db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

# create the login manager and link it to the app
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# register the blueprints
from auth import auth as auth_bp
app.register_blueprint(auth_bp)

from main import main as main_bp
app.register_blueprint(main_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
