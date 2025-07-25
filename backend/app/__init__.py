import os
from flask import Flask
from flask_dance.contrib.github import make_github_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix

from app.routes import main_bp


def create_app():
    app = Flask(
        __name__,
        static_folder="../../public",
        static_url_path="/public",
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'secret')

    os.makedirs(app.static_folder, exist_ok=True)
    app.config['CLOUD_REPOSITORY_APIKEY'] = os.environ.get('CLOUD_REPOSITORY_APIKEY')

    github_bp = make_github_blueprint(
        client_id=os.environ.get('GITHUB_OAUTH_CLIENT_ID', 'Ov23ligIOwzpGYVkuvyu'),
        client_secret=os.environ.get('GITHUB_OAUTH_CLIENT_SECRET', '5e823eef5497b276ea4679383217ecb9a912876e'),
        redirect_url=os.environ.get('GITHUB_OAUTH_REDIRECT_URL', 'https://cir.nodadyoushutup.com'),
    )
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.register_blueprint(github_bp, url_prefix="/login")

    app.register_blueprint(main_bp)

    return app
