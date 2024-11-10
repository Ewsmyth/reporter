from flask import Flask, Blueprint, render_template
from .utils import adminReq
from flask_login import login_required, current_user
from .models import db, User
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/<username>/admin-home/')
@login_required
@adminReq
def adminHome(username):
    return render_template('admin-home.html', username=username)

@admin.route('/<username>/admin-home/admin-users/')
@login_required
@adminReq
def adminUsers(username):

    reporterUsers = User.query.all()

    return render_template('admin-users.html', username=username, reporterUsers=reporterUsers)

@admin.route('/<username>/admin-home/create-user/', methods=['POST', 'GET'])
@login_required
@adminReq
def adminCreateUser(username):
    return render_template('admin-create-user.html', username=username)

@admin.route('/<username>/admin-home/edit-account', methods=['POST', 'GET'])
@login_required
@adminReq
def adminEditAccount(username):
    return render_template('admin-edit-account.html', username=username)