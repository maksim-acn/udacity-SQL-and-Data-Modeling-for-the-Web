import os
from urllib.parse import quote

from dotenv import load_dotenv


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Enable debug mode.
DEBUG = True

# Connect to the database


def build_database_uri():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url

    host = os.environ.get('POSTGRES_HOST') or os.environ.get('DB_POSTGRESDB_HOST') or os.environ.get('DATA_NODE_IP')
    port = os.environ.get('POSTGRES_PORT') or os.environ.get('DB_POSTGRESDB_PORT') or '5432'
    database = os.environ.get('POSTGRES_DB') or os.environ.get('DB_POSTGRESDB_DATABASE') or 'udacity'
    user = os.environ.get('POSTGRES_USER') or os.environ.get('DB_POSTGRESDB_USER')
    password = os.environ.get('POSTGRES_PASSWORD') or os.environ.get('DB_POSTGRESDB_PASSWORD')

    if host and user and password:
        return 'postgresql://{}:{}@{}:{}/{}'.format(
            quote(user, safe=''),
            quote(password, safe=''),
            host,
            port,
            database,
        )

    return 'postgresql://localhost:5432/udacity'


SQLALCHEMY_DATABASE_URI = build_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
