from flask import Flask, render_template
from dotenv import dotenv_values
import secrets

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
        
    # Create a secret key for the contact form
    app.secret_key = secrets.token_urlsafe(24)
    print("secret key: ",app.secret_key)

    # Setup reCAPTCHA secret keys
    environment_vars = dotenv_values(".env")
    app.config['RECAPTCHA_PUBLIC_KEY'] = environment_vars['SITE_KEY_V2']
    app.config['RECAPTCHA_PRIVATE_KEY'] = environment_vars['SECRET_KEY_V2']
    app.config['RECAPTCHA_PUBLIC_KEY_V3'] = environment_vars['SITE_KEY_V3']
    app.config['RECAPTCHA_PRIVATE_KEY_V3'] = environment_vars['SECRET_KEY_V3']
    app.config['VERIFY_URL'] = environment_vars['VERIFY_URL']

    return app