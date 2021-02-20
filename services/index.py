from flask import render_template, Blueprint
from flask_login import login_required


index_bp = Blueprint('index', __name__)


@index_bp.route('/')
@login_required
def index():
    return render_template('index.html')
