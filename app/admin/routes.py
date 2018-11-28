from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required

from app import db
from app.admin import bp
from app.admin.forms import CreateUserForm, DeleteUserForm
from app.models import User


@bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        abort(403)

    users = User.query.order_by(User.username).all()
    return render_template('admin/index.html', title='Administracja',
                           users=users)


@bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        abort(403)

    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Dodano użytkownika {}'.format(user.username))
        return redirect(url_for('admin.index'))

    return render_template('admin/create_user.html',
                           title='Dodawanie użytkownika', form=form)


@bp.route('/delete_user/<username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    if not current_user.is_admin:
        abort(403)

    user = User.query.filter_by(username=username).first_or_404()
    form = DeleteUserForm()
    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(user)
            db.session.commit()
            flash('Usunięto użytkownika {}'.format(username))
        return redirect(url_for('admin.index'))

    return render_template('admin/delete_user.html',
                           title='Usuwanie użytkownika',
                           username=username,
                           form=form)

