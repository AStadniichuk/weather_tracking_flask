import datetime
from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User, Profile, Role
from app.auth.utils import get_gravatar


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.last_visit = datetime.datetime.now()
            user.save()

            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid user credential')

    return render_template(
        'auth/login.html',
        title='Login',
        form=form
    )


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered')
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_role = Role.select().where(Role.name == 'user').first()
        user_profile = Profile(
            avatar=get_gravatar(form.email.data),
            info=form.info.data.capitalize()
        )
        user_profile.save()

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=user_role,
            profile=user_profile
        )
        user.save()
        flash(f'{user.username} has added')
        return redirect(url_for('main.index'))

    return render_template(
        'auth/registration.html',
        title='Register page',
        form=form
    )


@auth.route('/secret')
@login_required
def secret():
    return render_template(
        'main/index.html',
        title='Top secret',
        message='Top secret. Reptilians rule the world!'
    )

