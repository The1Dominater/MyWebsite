from flask import Flask, render_template
from dotenv import dotenv_values
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
  
    # Setup blueprint for different pages
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_400.html'), 404
    
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('error_401.html'), 401
    
    environment_vars = dotenv_values(".env")
    # Setup reCAPTCHA secret keys
    app.config['RECAPTCHA_PUBLIC_KEY'] = environment_vars['SITE_KEY_V2']
    app.config['RECAPTCHA_PRIVATE_KEY'] = environment_vars['SECRET_KEY_V2']
    app.config['RECAPTCHA_PUBLIC_KEY_V3'] = environment_vars['SITE_KEY_V3']
    app.config['RECAPTCHA_PRIVATE_KEY_V3'] = environment_vars['SECRET_KEY_V3']
    app.config['VERIFY_URL'] = environment_vars['VERIFY_URL']
    app.config['MAIL_SERVER'] = environment_vars['MAIL_SERVER']
    app.config['MAIL_PORT'] = environment_vars['MAIL_PORT']
    app.config['MAIL_USERNAME'] = environment_vars['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = environment_vars['MAIL_PASSWORD']
    app.config['MAIL_USE_SSL'] = bool(environment_vars['MAIL_PASSWORD'])
    app.config['MAIL_DEFAULT_SENDER'] = environment_vars['MAIL_USERNAME']
    app.config['MAIL_RECIPIENTS'] = [environment_vars['MAIL_USERNAME'],environment_vars['MAIL_RECIPIENT']]

    environment_vars.clear()

    # Setup mail object
    mail = Mail(app)
    app.config['MAIL_OBJ'] = mail

    return app