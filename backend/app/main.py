from flask import Flask
from flask_cors import CORS

from app.api.v1.routes import router as api_router
from app.core.config import get_settings
from app.core.database import Base, engine

settings = get_settings()

app = Flask(__name__)
app.config["APP_NAME"] = settings.app_name

CORS(app, origins=settings.cors_origins_list, supports_credentials=True)

Base.metadata.create_all(bind=engine)
app.register_blueprint(api_router)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=settings.app_env == "development")
