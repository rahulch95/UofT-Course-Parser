from flask import Flask


def create_app():
    app = Flask(__name__)
    app.run()
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app

if __name__ == '__main__':
    app = create_app()
