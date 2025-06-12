from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.models.models import db
from app.controllers.main import main_bp
from app.controllers.api import api_bp
from app.config import config_dict

def create_app(config_name='development'):
    """
    Application factory function to create and configure the Flask app
    """
    app = Flask(__name__)

    CORS(app)
    
    # Load configuration
    app.config.from_object(config_dict[config_name])
    app.config['JSONIFY_ENCODE_UNICODE'] = True
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app