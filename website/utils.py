from flask import Blueprint, redirect, url_for, flash
from .models import db, User
from functools import wraps
from flask_login import current_user

utils = Blueprint('utils', __name__)

def adminReq(f):
    @wraps(f)
    def adminAuthority(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        elif current_user.auth != 'admin':
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return adminAuthority

def managerReq(f):
    @wraps(f)
    def managerAuthority(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        elif current_user.auth != 'manager':
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return managerAuthority

def userReq(f):
    @wraps(f)
    def userAuthority(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

        elif current_user.auth != 'user':
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return userAuthority