"""
Environment configuration for the Flock Energy API wrapper.
Fill in .env based on what you observe in DevTools (Step 1 of the assignment).
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    URJA_BASE_URL: str = os.getenv("URJA_BASE_URL", "https://urja-ops.flockenergy.tech")
    URJA_USERNAME: str = os.getenv("URJA_USERNAME", "operator@urja.local")
    URJA_PASSWORD: str = os.getenv("URJA_PASSWORD", "urja-ops-2026")

    # TODO: set once you know the real login endpoint from DevTools
    # e.g. "/login" or "/api/v1/auth/login" or "/api/auth/signin"
    LOGIN_PATH: str = os.getenv("URJA_LOGIN_PATH", "/login")

    # TODO: fill in once observed - some SvelteKit/Next apps use a different
    # session cookie name than the framework default
    SESSION_COOKIE_NAME: str = os.getenv("URJA_SESSION_COOKIE", "__Secure-better-auth.session_token")

    REQUEST_TIMEOUT: float = float(os.getenv("URJA_TIMEOUT", "10.0"))
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))

settings = Settings()
