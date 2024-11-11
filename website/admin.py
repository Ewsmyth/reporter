from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from .utils import adminReq
from flask_login import login_required, current_user
from .models import db, User
from datetime import datetime
from sqlalchemy import or_
from werkzeug.security import check_password_hash

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
    if request.method == 'POST':
        createUsername = request.form.get('username-fr-usr')
        createEmail = request.form.get('email-fr-usr')
        createPassword = request.form.get('password-fr-usr')
        createAuth = request.form.get('auth-fr-usr')
        createManager = request.form.get('manager-id-fr-usr')
        createTeam = request.form.get('team-fr-usr')
        createFirstname = request.form.get('firstname-fr-usr')
        createLastname = request.form.get('lastname-fr-usr')

        existingUser = User.query.filter(or_(User.username == createUsername, User.email == createEmail)).first()

        if existingUser:
            flash('Username or email already exist', 'error')
            return redirect(url_for('admin.adminCreateUser', username=username))

        createNewUser = User(
            username=createUsername,
            email=createEmail,
            auth=createAuth,
            manager_id=createManager,
            team=createTeam,
            firstname=createFirstname,
            lastname=createLastname
        )
        print(f"{current_user.username} created a new user: {createUsername}, {createEmail}")

        createNewUser.set_password(createPassword)

        db.session.add(createNewUser)
        db.session.commit()

        print(f"New user {createUsername}, has successfully been created.")
        flash(f"You have created a new user: {createUsername}.")
        return redirect(url_for('admin.adminCreateUser', username=username))

    return render_template('admin-create-user.html', username=username)

@admin.route('/<username>/admin-home/edit-account', methods=['POST', 'GET'])
@login_required
@adminReq
def adminEditAccount(username):
    return render_template('admin-edit-account.html', username=username)