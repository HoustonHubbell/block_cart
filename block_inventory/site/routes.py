from flask import Blueprint, render_template
from flask_login.utils import login_required
from block_inventory.api.api import get_top_5


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@site.route('/dashboard')
@login_required
def dashboard():
    data = get_top_5()
    return render_template('dashboard.html', data=data)