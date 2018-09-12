from string import punctuation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Group

__all__ = [
    "RegistrationForm",
    "LoginForm",
    "TopicForm",
    "CommentForm",
    "GroupForm",
    "AddUserForm",
    "SubscriptionForm",
    "UnsubscriptionForm",
    "FindUserForm",
    "LeaveGroupForm"
]

def SpecialChar(form, field):
    """Test used in RegistrationForm that checks password for a special character"""
    if len(set(punctuation).intersection(field.data)) < 1:
        ## TODO: Find a better error message
        raise ValidationError('Field must contain atleast 1 special character!')

class RegistrationForm(FlaskForm):
    """Create child of FLaskForm that defines a template for the registration form"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), SpecialChar])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    """Form for creating login"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TopicForm(FlaskForm):
    """Form for creating topics"""
    title = StringField('Title',validators=[DataRequired()])
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """Form for creating comments"""
    comment = TextAreaField('Comment',validators=[DataRequired()])
    submit = SubmitField('Submit')

class GroupForm(FlaskForm):
    """Form for creating groups"""
    name = StringField('Group Name',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddUserForm(FlaskForm):
    """Form for adding a user to a group"""
    username = StringField('Username:',validators=[DataRequired()])
    submit = SubmitField('Submit')

class FindUserForm(FlaskForm):
    """Form for the search bar to find a user"""
    username = StringField('',validators=[DataRequired()])

class SubscriptionForm(FlaskForm):
    """Form for subcribing to a thread"""
    submit = SubmitField('Subscribe')

class UnsubscriptionForm(FlaskForm):
    """Form for unsubscribing to a thread"""
    submit = SubmitField('Unsubscribe')

class LeaveGroupForm(FlaskForm):
    """Form the leave a group"""
    submit = SubmitField('Leave Group?')
