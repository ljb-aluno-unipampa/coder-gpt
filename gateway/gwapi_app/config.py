import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
