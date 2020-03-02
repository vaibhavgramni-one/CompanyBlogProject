# inside user.forms.py file ##

from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField , PasswordField
from wtforms.validators import DataRequired , EqualTo , Email
from wtforms import ValidationError
from flask_wtf.file import FileField , FileAllowed
from puppycompanyblog.models import User

class LoginForm(FlaskForm):

    email = StringField('Email : ' , validators = [DataRequired(), Email()])

    password = PasswordField('Password : ' , validators = [DataRequired()])

    submit = SubmitField('Login!')


class RegisterForm(FlaskForm):

    username = StringField('Username : ' , validators = [DataRequired()])

    email = StringField('Email : ', validators = [DataRequired() , Email()])

    password = PasswordField('Password : ' , validators =[DataRequired() , EqualTo('confirm_pass' , message = 'Passwords must match!')])

    confirm_pass = PasswordField('Confirm Password : ' , validators = [DataRequired()])

    submit = SubmitField('Register!')


    def check_email(self , field):

        if User.query.filter_by(email = field.data).first():
            raise ValidationError('YOur email id is already registered!')

    def check_username(self , field):

        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username is already registered!')


class UpdateForm(FlaskForm):

    username = StringField('Username : ' , validators = [ DataRequired() ])

    email = StringField('Email : ' , validators = [DataRequired() , Email()])

    picture = FileField('Upload Profile Picture' , validators = [FileAllowed(['jpg' , 'png'])])

    submit = SubmitField('Update!')


    def check_email(self , field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('YOur email id is already registered! ')


    def check_username(self , field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username is already regiseterd!')


