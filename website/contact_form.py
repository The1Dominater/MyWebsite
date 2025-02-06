from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# ContactForm class form
class ContactForm(FlaskForm):
    # Honeypot fields
    name = StringField()
    job_role = StringField()
    # Necessary fields
    email = StringField(validators=[DataRequired(), Email(check_deliverability=True)])
    subject = StringField()
    message = TextAreaField(validators=[DataRequired(), Length(min=10, max=3000)])
    recaptcha = RecaptchaField()
    submit = SubmitField()