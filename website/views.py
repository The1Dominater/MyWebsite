from flask import Blueprint, current_app, render_template, request, abort, flash
from .contact_form import ContactForm
import requests

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def about_me():
    return render_template('2_about_me.html')

@views.route('/resume')
def resume():
    return render_template('3_resume.html')

@views.route('/my_projects')
def my_projects():
    return render_template('4_my_projects.html')

def send_msg(sender_email:str, subject:str, message:str):
    print(sender_email)
    print(subject)
    print(message)

    return

@views.route('/contact_info', methods=['GET','POST'])
def contact_info():
    form = ContactForm()
    reCAPTCHA_site_key = current_app.config.get('RECAPTCHA_PUBLIC_KEY_V3')

    if form.validate_on_submit():
        # Honeypot fields
        honeypot1 = form.name.data
        honeypot2 = form.job_role.data
        # print(honeypot1)
        # print(honeypot2)

        if (honeypot1 or honeypot2):
            abort(401)

        # Verify reCAPTCHA v3 score
        reCAPTCHA_secret_key = current_app.config.get('RECAPTCHA_PRIVATE_KEY_V3')
        verify_url = current_app.config.get('VERIFY_URL')
        recaptcha_token = request.form.get("g-recaptcha-response")
        print(recaptcha_token)
        recaptcha_response = requests.post(
            verify_url,
            data={
                "secret": reCAPTCHA_secret_key,
                "response": recaptcha_token
            }
        ).json()

        # Check if reCAPTCHA validation was successful
        print(recaptcha_response)
        if not (recaptcha_response.get("success") and recaptcha_response.get("score", 0) > 0.5):
            flash("reCAPTCHA verification failed. Suspicous behavior detected.", category="error")
            abort(401)
            

        # Necessary fields
        sender_email = form.email.data
        subject = form.subject.data
        message = form.message.data

        if send_msg(sender_email,subject, message):
            flash("Form submitted successfully!", category="success")
            return render_template('6_sent_successfully.html')
        else:
           return render_template('7_send_failed.html') 
    elif form.errors:
        print(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error with "{field}". {error}', category="error")
    #     return render_template('7_send_failed.html')
    
    return render_template('5_contact_info.html', form=form, reCAPTCHA_site_key=reCAPTCHA_site_key)
    