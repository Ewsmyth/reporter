from flask import Flask, render_template, Blueprint, flash, request, redirect, url_for
from flask_login import login_user, logout_user
from .models import db, User
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    usrnm_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # This automatically handles the CSRF validation
        usrnmEmail = form.usrnm_email.data
        password = form.password.data

        usrDbCheck = User.query.filter(or_(User.email == usrnmEmail, User.username == usrnmEmail)).first()

        if usrDbCheck:
            if usrDbCheck.check_password(password):
                if usrDbCheck.is_active == True:
                    login_user(usrDbCheck)
                    if usrDbCheck.auth == 'admin':
                        return redirect(url_for('admin.adminHome', username=usrDbCheck.username))
                    elif usrDbCheck.auth == 'manager':
                        return redirect(url_for('manager.managerHome', username=usrDbCheck.username))
                    elif usrDbCheck.auth == 'user':
                        return redirect(url_for('user.userHome', username=usrDbCheck.username))
                    else:
                        flash('Invalid authority.', 'error')
                        print(f"User, {usrDbCheck.username}, does not have a valid authority.")
                else:
                    flash('The account you are trying to access has been disabled', 'error')
                    print(f"User, {usrnmEmail}, attempted to login to their account but is disabled.")
            else:
                flash('Invalid password', 'error')
                print(f"User, {usrnmEmail}, entered the wrong password.")
        else:
            flash('Invalid username or email.', 'error')
            print(f"A user attempted to login to an account that does not exist: {usrnmEmail}")
    
    return render_template('auth-login.html', form=form)  # Pass the form to the template

@auth.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        usrnm = request.form.get('usrnm-fr-usr')
        email = request.form.get('email-fr-usr')
        psswd = request.form.get('psswd-fr-usr')
        confPsswd = request.form.get('conf-psswd-fr-usr')
        mangr = request.form.get('mangr-fr-usr')
        team = request.form.get('team-fr-usr')

        if psswd != confPsswd:
            flash('Passwords do not match', 'warning')
            print(f"User, {usrnm}, did not match the passwords.")
            return redirect(url_for('auth.login'))
        
        existUsr = User.query.filter(or_(User.username == usrnm, User.email == email)).first()

        if existUsr:
            flash('Username or email already exists.', 'warning')
            return redirect(url_for('auth.login'))

        createUsr = User(username=usrnm, email=email, manager_id=mangr, team=team)
        print(f"{usrnm}, {email}, {mangr}, {team}, {psswd}")

        createUsr.set_password(psswd)

        db.session.add(createUsr)
        db.session.commit()

        print(f"New user, {usrnm}, has created an account.")
        return redirect(url_for('auth.login'))

    return render_template('auth-signup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
