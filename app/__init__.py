from flask import Flask
from flasgger import Swagger
from swagger_config import swagger_template
from .routes import main_bp
from .auth import auth_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    swagger = Swagger(app, template=swagger_template)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
