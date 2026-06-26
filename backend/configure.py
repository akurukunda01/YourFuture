import os


class Config:
    # Secret key for signing session cookies. MUST be set in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # Stateless, serverless-safe signed-cookie sessions (Flask default).
    SESSION_PERMANENT = False

    # Cookie hardening. In production (HTTPS) the cookie is marked Secure.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"

    # PostgreSQL connection string (Neon / Supabase / local), e.g.
    #   postgresql://user:pass@host:5432/dbname
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Origin allowed to call the API in local development (Vite dev server).
    # In production the SPA is same-origin, so CORS is not needed.
    DEV_FRONTEND_ORIGIN = os.environ.get("DEV_FRONTEND_ORIGIN", "http://localhost:5173")

    IS_PRODUCTION = os.environ.get("FLASK_ENV") == "production"
