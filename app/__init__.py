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

    # Register routes
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/ping")
    def ping():
        return {"status": "ok", "msg": "Backend running"}

    return app
