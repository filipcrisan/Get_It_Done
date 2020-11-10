from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_migrate import Migrate 
import config

db = SQLAlchemy() 
migrate = Migrate()


app = Flask(__name__)

app.config['SECRET_KEY'] = config.secret_key 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app) 
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

from auth import auth as auth_bp
app.register_blueprint(auth_bp)

from main import main as main_bp
app.register_blueprint(main_bp)


app.run(debug=True)