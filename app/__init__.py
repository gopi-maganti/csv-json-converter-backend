from flask import Flask
from flasgger import Swagger
from app.routes import conversion_route


def create_app():
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["OUTPUT_FOLDER"] = "converted"
    app.config["SWAGGER"] = {"title": "File Converter API", "uiversion": 3}

    Swagger(app)  # Initialize Swagger
    app.register_blueprint(conversion_route.bp)

    @app.route("/")
    def index():
        return '<h2>Welcome to the File Converter API. Visit <a href="/apidocs/">/apidocs/</a> to try it out.</h2>'

    return app
