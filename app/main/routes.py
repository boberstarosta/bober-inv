from flask import redirect, render_template, url_for, request
from flask_login import login_required

from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html')


@bp.route('/new_invoice', methods=['GET', 'POST'])
@login_required
def new_invoice():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('edit_invoice.html', header='Nowa faktura VAT')
