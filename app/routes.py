from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm 

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
 
@app.route('/')
@app.route('/index')
@login_required
def index():
    message = "For further specification, click on which term the topic you are trying to study falls on."
    return render_template('index.html', title='Home Page', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# term 1 is units 1-3
@app.route('/term_1')
@login_required
def term_1():
    unit1 = 'Unit 1'
    unit2 = 'Unit 2'
    unit3 = 'Unit 3'
    return render_template('term_1.html', title='Term 1', unit1=unit1, unit2=unit2, unit3=unit3)

@app.route('/unit_1')
@login_required
def unit_1():
    swbat1 = 'Fill this in later'
    return render_template('unit_1.html', title='Unit 1', swbat=swbat1)

@app.route('/unit_2')
@login_required
def unit_2():
    swbat2 = 'Fill this in later'
    return render_template('unit_2.html', title='Unit 2', swbat=swbat2)

@app.route('/unit_3')
@login_required
def unit_3():
    swbat3 = 'Fill this in later'
    return render_template('unit_3.html', title='Unit 3', swbat=swbat3)

@app.route('/term_2')
@login_required
def term_2():
    unit3_2 = ('Unit 4', 'Unit 5')
    return render_template('term_2.html', title='term 2', unit3_2 = unit3_2)

@app.route('/term_3')
@login_required
def term_3():
    unit3_3 = ('Unit 6', 'Unit 7', 'Unit 8')
    return render_template('term_3.html', title='term 3', unit3_3 = unit3_3)

@app.route('/term_4')
@login_required
def term_4():
    unit3_4 = ('Unit 9', 'Final Review')
    return render_template('term_4.html', title='term 4', unit3_4 = unit3_4)