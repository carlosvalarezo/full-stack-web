import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
DB_NAME = os.getenv("DB_NAME", "fyyur")
DB_USER = os.getenv("DB_USER", "fyyur")
DB_PASSWORD = os.getenv("DB_PASSWORD", "fyyur")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_HOST = os.getenv("DB_HOST", "db")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = True
