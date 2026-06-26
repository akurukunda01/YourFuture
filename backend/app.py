# app.py
from flask import Flask
from configure import Config
from db import close_db

from blueprints.auth import auth_bp
from blueprints.jobs import jobs_bp
from blueprints.site import site_bp
from blueprints.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS is only needed for local cross-origin dev (Vite on :5173 → API on :8000).
    # In production the SPA is served same-origin behind /api, so no CORS is applied.
    if not Config.IS_PRODUCTION:
        from flask_cors import CORS
        CORS(
            app,
            supports_credentials=True,
            resources={r"/api/*": {"origins": Config.DEV_FRONTEND_ORIGIN}},
        )

    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(site_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
