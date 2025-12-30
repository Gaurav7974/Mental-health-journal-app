from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from pymongo import MongoClient
import os

jwt = JWTManager()
db = None

def create_app():
    global db

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    jwt.init_app(app)

    # MongoDB 
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["health_journal"]
    print("MongoDB connected")

    # Import blueprints AFTER setup to avoid circular imports
    from .routes.auth import auth_bp
    from .routes.journal import journal_bp
    from .routes.mood import mood_bp
    from .routes.conversation import conversation_bp
    from .routes.voice_conversation import voice_bp
    from .routes.insights import insights_bp

    # Register routes
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(journal_bp, url_prefix="/journal")
    app.register_blueprint(mood_bp, url_prefix="/mood")
    app.register_blueprint(conversation_bp, url_prefix="/conversation")
    app.register_blueprint(voice_bp, url_prefix="/conversation/voice") 
    app.register_blueprint(insights_bp, url_prefix="/insights") 

    @app.route("/ping")
    def ping():
        return {"status": "ok", "msg": "Backend running"}

    return app