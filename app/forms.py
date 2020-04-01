from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Addqsotodb


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username take, pick new one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email take, pick new one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddQSOtoDbForm(FlaskForm):
    callsign = StringField('Call Sign', validators=[DataRequired(), Length(min=2, max=20)])
    signal_sent = StringField('Signal Sent', validators=[DataRequired(), Length(min=2, max=20)])
    signal_received = StringField('Signal Received', validators=[DataRequired(), Length(min=2, max=20)])
    custom_sent = StringField('Custom Sent', validators=[Length(min=2, max=20)])
    custom_received = StringField('Custom Received', validators=[Length(min=2, max=20)])
    frequency_used = StringField('Frequency Used', validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Log QSO')
