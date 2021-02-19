from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from models import User
from auth import auth as auth_bp
from main import main as main_bp
import os

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)

app.config['SECRET_KEY'] = b'9\xe0_H\x03\xb1\x10TVR\xfd\x19\xda\xab\xa2\\\xe8`\xd4\xde\xa3Z\x12\xc9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

app.run(debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
