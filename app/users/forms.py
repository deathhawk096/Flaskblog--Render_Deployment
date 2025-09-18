from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import data_required,length,Email,EqualTo,ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from app.models import User



class RegistrationForm(FlaskForm):

    username=StringField('Username',validators=[data_required(),length(min=3,max=20)])

    email=StringField("Email",validators=[data_required(),Email()])

    password=PasswordField("Password",validators=[data_required()])

    confirm_password=PasswordField("Confirm Password",validators=[data_required(),EqualTo('password')])

    submit=SubmitField("SignUp")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That Username Is Taken! Please Choose Another One")
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already In Use! Please Select A Diffrent Email")
        

class LoginForm(FlaskForm):

    email=StringField("Email",validators=[data_required(),Email()])

    password=PasswordField("Password",validators=[data_required()])

    remember_me=BooleanField("Remember Me")

    submit=SubmitField("Log In")

class update_form(FlaskForm):

    username=StringField("Username",validators=[data_required(),length(min=3,max=20)])

    email=StringField("Email",validators=[data_required(),Email()])

    pic=FileField("Update Profile Picture!",validators=[FileAllowed(['jpg','png'])])

    submit=SubmitField("Update")


    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That Username Is Taken! Please Choose Another One")
        

    def validate_email(self,email):

        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email Already In Use! Please Select A Diffrent Email")
            

class RequestResetForm(FlaskForm):

    email=StringField("Email",validators=[data_required(),Email()])

    submit=SubmitField("Send Reset Link")


    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError("No Account with that email exists!")
        
class ResetPasswordForm(FlaskForm):

    new_password=PasswordField("New Password",validators=[data_required()])

    confirm_password=PasswordField("Confirm Password",validators=[data_required(),EqualTo('new_password')])

    submit=SubmitField("Submit")