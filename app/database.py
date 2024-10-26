# Import necessary components from SQLAlchemy
from sqlalchemy import create_engine               # To create a new SQLAlchemy engine instance
from sqlalchemy.ext.declarative import declarative_base  # To create a base class for declarative models
from sqlalchemy.orm import sessionmaker            # To create a session factory for interacting with the database
# Database connection string: specify the database type, user, password, host, port, and database name
DATABASE_URL = "sqlite:///test.db"

# Create the SQLAlchemy engine that will manage the connection pool and interact with the database
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models; all models will inherit from this base
Base = declarative_base()

# Create a configured "Session" class; this will be used to manage database sessions
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)  # expire_on_commit=False prevents automatic expiration of session objects


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
