from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from functools import wraps

from app import db
from app.admin import bp
from app.admin.forms import CreateUserForm, DeleteUserForm
from app.admin.forms import CreateRateForm, DeleteRateForm
from app.models import User, Rate


def admin_required(f):
    @wraps(f)
    def wrapper():
        if not current_user.is_admin:
            abort(403)
        return f()
    return wrapper


@bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.order_by(User.username).all()
    rates = Rate.query.all()
    return render_template('admin/index.html', title='Administracja',
                           users=users, rates=rates)


@bp.route('/create_user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Dodano użytkownika {}'.format(user.username))
        return redirect(url_for('admin.index'))
    
    return render_template('admin/form.html',
                           title='Dodawanie użytkownika',
                           header='Nowy użytkownik',
                           form=form)


@bp.route('/delete_user/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    form = DeleteUserForm()
    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(user)
            db.session.commit()
            flash('Usunięto użytkownika {}'.format(user.username))
        return redirect(url_for('admin.index'))
    
    header='Potwierdź usunięcie użytkownika {}'.format(user.username)
    return render_template('admin/form.html',
                           title='Usuwanie użytkownika',
                           header=header, form=form)


@bp.route('/create_rate', methods=['GET', 'POST'])
@login_required
@admin_required
def create_rate():
    form = CreateRateForm()
    if form.validate_on_submit():
        rate = Rate(name=form.name.data, value=form.value.data)
        db.session.add(rate)
        db.session.commit()
        flash('Dodano stawkę VAT {}'.format(rate.name))
        return redirect(url_for('admin.index'))

    return render_template('admin/form.html',
                           title='Dodawanie stawki VAT',
                           header='Nowa stawka VAT', form=form)


@bp.route('/delete_rate/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_rate(id):
    rate = Rate.query.get_or_404(id)
    form = DeleteRateForm()
    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(rate)
            db.session.commit()
            flash('Usunięto stawkę VAT {}'.format(rate.name))
        return redirect(url_for('admin.index'))

    header = 'Potwierdź usunięcie stawki VAT {}'.format(rate.name)
    return render_template('admin/form.html',
                           title='Usuwanie stawki VAT',
                           header=header, form=form)

