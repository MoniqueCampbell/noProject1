from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class LoginForm(FlaskForm):
	firstname = StringField('Firstname', validators=[InputRequired()])
	lastname = StringField('Lastname', validators=[InputRequired()])
	gender_types = [('Female', 'Female'),('Male', 'Male')]
	gender = SelectField('Gender', choices=gender_types)
	email = StringField('Email', validators=[DataRequired(), Email()])
	location = StringField('Location', validators=[InputRequired()])
	biography = TextAreaField('Biography', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
	photo = FileField('Profile Picture', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])
	
