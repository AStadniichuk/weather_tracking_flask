from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from flask_paginate import get_parameter, Pagination

from app import User, Profile
from app.main import main
from app.main.forms import GenerateDataForm, EditUserForm
from utils.fake_users.db_manager import main as write_fake_profiles


@main.route('/', methods=['GET', 'POST'])
def index():
    form = GenerateDataForm()
    if form.validate_on_submit():
        qty = int(form.qty.data)
        write_fake_profiles(qty)
        flash('Database filled with test data')
    return render_template(
        'main/index.html',
        title='Home page',
        form=form
    )


@main.route('/show/users')
@login_required
def show_users():
    """Show users information"""
    per_page = 10
    page = request.args.get(get_parameter(), type=int, default=1)
    total = User.select().count()
    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='users')

    users = User.select().paginate(page, per_page)
    return render_template(
        'main/show_users.html',
        title='Show users',
        users=users,
        pagination=pagination)


@main.route('/edit/user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id: int):
    """Edit user"""
    if not current_user.is_admin():
        abort(403)

    user = User.select().where(User.id == user_id).first()
    if not user:
        abort(404)

    form = EditUserForm()
    form.id.label.text = ''
    form.id.data = user.id
    form.username.data = user.username
    form.email.data = user.email
    return render_template(
        'main/edit_user.html',
        title=f'Edit user {user.username}',
        form=form
    )


@main.route('/update/user', methods=['POST'])
@login_required
def update_user():
    form = EditUserForm()
    if form.validate_on_submit():
        user = User.get(User.id == int(form.id.data))
        user.username = form.username.data.strip().lower()
        user.email = form.email.data.strip().lower()
        user.save()
        flash(f'{user.username} updated')
    else:
        flash(form.errors)
    return redirect(url_for('.show_users'))


@main.route('/delete/users', methods=['POST'])
@login_required
def delete_users():
    """Delete selected users"""
    if not current_user.is_admin():
        flash('You don\'t have access to delete users', 'error')
        return redirect(url_for('.show_users'))

    selectors = list(map(int, request.form.getlist('selectors')))

    if current_user.id in selectors:
        flash('You can\'t delete yourself use profile page for this')
        return redirect(url_for('.show_users'))

    if not selectors:
        flash('Nothing to delete')
        return redirect(url_for('.show_users'))

    message = 'Deleted: '
    for selector in selectors:
        user = User.get(User.id == selector)
        profile = Profile.get(Profile.id == user.profile.id)
        message += f'{user.email} '
        user.delete_instance()
        profile.delete_instance()
    flash(message)
    return redirect(url_for('.show_users'))
