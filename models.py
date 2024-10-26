# Import necessary components from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean  # Import column types for model definitions
from database import Base  # Import the base class for SQLAlchemy models
import datetime  # Import the datetime module for handling date and time

# User model representing the 'users' table in the database
class User(Base):
    __tablename__ = 'users'  # Specify the name of the table in the database

    # Define the columns of the 'users' table
    id = Column(Integer, primary_key=True)  # Primary key column for user identification
    username = Column(String(50), nullable=False)  # Username column; cannot be null
    email = Column(String(100), unique=True, nullable=False)  # Email column; must be unique and cannot be null
    password = Column(String(100), nullable=False)  # Password column; cannot be null

# TokenTable model representing the 'token' table in the database
class TokenTable(Base):
    __tablename__ = "token"  # Specify the name of the table in the database

    # Define the columns of the 'token' table
    user_id = Column(Integer)  # Foreign key column referencing the user ID
    access_toke = Column(String(450), primary_key=True)  # Access token column; primary key for the token table
    refresh_toke = Column(String(450), nullable=False)  # Refresh token column; cannot be null
    status = Column(Boolean)  # Status column indicating whether the token is active
    created_date = Column(DateTime, default=datetime.datetime.now)  # Timestamp of when the token was created; defaults to current time
