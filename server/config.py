import os

POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" f"@{POSTGRES_SERVER}:5432/{POSTGRES_DB}"
