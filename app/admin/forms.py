from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField
from wtforms.validators import ValidationError, DataRequired, Length
from wtforms.validators import Email, EqualTo
from app.models import User, Rate


class CreateUserForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField(
        'Potwierdzenie hasła',
        validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Administrator')
    submit = SubmitField('Zatwierdź')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Nazwa użytkownika jest już zajęta.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email jest już zajęty')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Usuń użytkownika')
    cancel = SubmitField('Anuluj')


class CreateRateForm(FlaskForm):
    name = StringField('Nazwa',
                       validators=[DataRequired(), Length(min=1, max=140)])
    value = IntegerField('Wartość [%]')
    submit = SubmitField('Zatwierdź')


class DeleteRateForm(FlaskForm):
    submit = SubmitField('Usuń stawkę VAT')
    cancel = SubmitField('Anuluj')

