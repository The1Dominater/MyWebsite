from flask import Blueprint, current_app, render_template, request, abort, flash
from .form_support import ContactForm, send_mail, recaptcha_check_v3

views = Blueprint("views", __name__)

@views.context_processor
def inject_site_key():
    return dict(site_key=current_app.config['RECAPTCHA_PUBLIC_KEY_V3'])

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

    return True

@views.route('/contact_info', methods=['GET','POST'])
def contact_info():
    form = ContactForm()

    # Check valid inputs for bot behavior and send mail
    if form.validate_on_submit():
        # Honeypot fields
        honeypot1 = form.name.data
        honeypot2 = form.job_role.data
        if (honeypot1 or honeypot2):
            flash("Hideen field used! Suspicous behavior detected.", category="error")
            abort(401)

        # Verify reCAPTCHA v3 score
        secret_key = current_app.config.get('RECAPTCHA_PRIVATE_KEY_V3')
        verify_url = current_app.config.get('VERIFY_URL')
        recaptcha_token = request.form.get("g-recaptcha-response-v3") # Grab v3 token from contact-form
        if not recaptcha_check_v3(recaptcha_token, secret_key, verify_url):
            flash("reCAPTCHA verification failed. Suspicous behavior detected.", category="error")
            abort(401)
            
        # Necessary fields
        sender_email = form.email.data
        subject = form.subject.data
        message = form.message.data
        if send_mail(sender_email,subject, message):
            flash("Form submitted successfully!", category="success")
            return render_template('6_sent_successfully.html')
        else:
            return render_template('7_send_failed.html')
    # Explain why the form was considered invalid to the user
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error with "{field}". {error}', category="error")
    
    return render_template('5_contact_info.html', form=form)

@views.route('/test_email')
def test_email():
    return_email = "test@email.com"
    subject = "Test Contact Form"
    message = "Testing the contact form"
    if send_mail(return_email,subject,message):
        return render_template('6_sent_successfully.html')
    else:
        return render_template('7_send_failed.html')