# Imported for WTForms 
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, HiddenField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
# Imported for reCAPTCHA assessment
import requests
# Imported for sending mail
from flask import current_app
from flask_mail import Mail, Message

# ContactForm class form
class ContactForm(FlaskForm):
    # Honeypot fields
    name = StringField()
    job_role = HiddenField()
    # Necessary fields
    email = StringField(validators=[DataRequired(), Email(check_deliverability=True)])
    subject = StringField()
    message = TextAreaField(validators=[DataRequired(), Length(min=10, max=3000)])
    recaptcha = RecaptchaField()
    submit = SubmitField()

def send_mail(return_email:str, subject:str, message:str):
    # Grab configuration variables
    mail = current_app.config.get('MAIL_OBJ')
    recipients = current_app.config.get('MAIL_RECIPIENTS')

    # Send an email
    try:
        # Create a mail object
        if return_email and message:
            msg = Message(f'[CONTACT FORM] {subject}',
                        recipients=recipients,
                        body=f'From: {return_email}\n\n{message}')
            mail.send(msg)

            return True
    except Exception as e:
        print(e)

    # Return False if email failed to send
    return False

def recaptcha_check_v3(token: str, secret_key: str, verify_url: str):
    # Request an assessment from Google's API
    recaptcha_response = requests.post(
        verify_url,
        data={
            "secret": secret_key,
            "response": token
        }
    ).json()

    # Check if reCAPTCHA validation was successful
    if (not recaptcha_response.get("success")) or recaptcha_response.get("score", 0) < 0.7:
        return False

    return True