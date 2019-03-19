from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from datetime import datetime
from shop.models import User
now = datetime.now()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,10}$', message='Your password should be between 6 and 10 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
	
class PaymentForm(FlaskForm):
	cardNumber = StringField('Card Number', validators=[DataRequired(), Regexp('[0-9]{16}$', message='Please enter a valid 16 digit card number.')])
	expiryMonth = IntegerField('Expiry Date (mm/yyyy)', validators=[DataRequired(), NumberRange(min=1, max=12, message='Please enter a valid month.')])
	expiryYear = IntegerField(' ', validators=[DataRequired(), NumberRange(min=now.year, max=2100, message='Please enter a year between the present year and 2100')])
	cvv = StringField('CVV', validators=[DataRequired(), Regexp('[0-9]{3}$', message='Please enter your 3 digit CVV number (On the back of your card).')])
	submit = SubmitField('Pay Now')
	
class ReviewForm(FlaskForm):
	rating = IntegerField('Rating (0-5)' validators=[DataRequired(), NumberRange(min=0, max=5, message='Rating must be between 0 and 5')])
	review = StringField('Write a review for this book.' validators=[DataRequired(), Length(max=300, message='Your review must be under 300 characters long.')])
