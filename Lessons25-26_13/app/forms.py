from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing up')


    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username already exists')
        
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email  already exists')
        


    def validate_password(self, password: str): # Root
        validates = {
            'digit': False,
            'upper': False,
            'lower': False
        }

        errors = []

        for i in password.data:
            if i.isdigit():
                validates['digit'] = True
            if i.isupper():
                validates['upper'] = True
            if i.islower():
                validates['lower'] = True

        if not validates['digit']:
            errors.append('Password must contain at least one number') 
        if not validates['lower']:
            errors.append('Password must contain at least one lower letter')
        if not validates['upper']:
            errors.append('Password must contain at least one upper letter')
        if len(password.data) < 8:
            errors.append('Password length must be grater or equal than 8')


        if errors:
            raise ValidationError(', '.join(errors))


    # def validate_confirmed_password(self, confirmed_password,password):
    #     if confirmed_password.data != password.data:
    #         raise ValidationError('Passwords must match')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class AddCategoryForm(FlaskForm):
    pass


class PostForm(FlaskForm):
    pass