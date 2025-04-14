from flask import Flask
from api.routes import api

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    
    app.register_blueprint(blueprint=api, url_prefix='/api')
    
    return app

app: Flask = create_app()