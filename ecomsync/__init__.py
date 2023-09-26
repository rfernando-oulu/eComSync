"""
Init module.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

"""
SQLAlchemy.
"""
db = SQLAlchemy()
# cache = Cache()

def create_app(test_config=None):
    """
    Create and configure the Flask application.

    This function handles the application setup, including configuration, 
    database initialization, registration of command line commands, and
    blueprint registration.

    Parameters:
    test_config (dict): If provided, used as configuration settings for the app.
                        If not provided, the app will use the configuration file
                        located at instance/config.py. This is intended for testing.

    Returns:
    app (Flask): the configured Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="FileSystemCache",
        CACHE_DIR=os.path.join(app.instance_path, "cache"),
    )

    CORS(app)

    # Add Swagger configuration here
    app.config["SWAGGER"] = {
        "title": "eComSync API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/base.yml")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    ## cache.init_app(app)

    from . import models
    from . import api
    from ecomsync.utils import ManufacturerConverter

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_test_data)
    app.cli.add_command(models.generate_master_key)
    app.url_map.converters["manufacturer"] = ManufacturerConverter
    app.register_blueprint(api.api_bp)


    print(app.instance_path)
    return app
