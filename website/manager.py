from flask import Flask, render_template, Blueprint
from .utils import managerReq
from flask_login import login_required, current_user

manager = Blueprint('manager', __name__)

@manager.route('/<manager>/manager-home')
@login_required
@managerReq
def managerHome(username):
    return render_template('manager-home.html', username=username)