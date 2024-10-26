# Import necessary libraries and modules
import os  # For operating system dependent functionality
from passlib.context import CryptContext  # For password hashing and verification
from datetime import datetime, timedelta  # For handling date and time
from typing import Union, Any  # For type hinting
from jose import jwt  # For creating and verifying JSON Web Tokens (JWTs)

# Constants for token expiration times and algorithms
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duration for access tokens (30 minutes)
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Duration for refresh tokens (7 days)
ALGORITHM = "HS256"  # Algorithm used for encoding the JWT
JWT_SECRET_KEY = "VCFPSzLwUcta0qRhfqQ7w3AtGWAvkMXlO3GGC1DziKY="  # Secret key for access tokens; should be kept secret
JWT_REFRESH_SECRET_KEY = "8lZV60sYpxUfT0JRLzmIIJUnM3X5V+PN26DVrX5reDA="  # Secret key for refresh tokens; should also be kept secret

# Set up the password context for hashing with bcrypt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_hashed_password(password: str):
    return password_context.hash(password)  # Hash and return the given password

# Function to verify a password against a hashed password
def verify_password(password: str, hashed_pass: str) :
    return password_context.verify(password, hashed_pass)  # Return True if the password matches the hash

# Function to create an access token
def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta  # Set expiration based on the provided delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Default expiration time

    # Prepare the payload with expiration and subject
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    
    # Encode the JWT using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    
    return encoded_jwt  # Return the encoded JWT

# Function to create a refresh token
def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) :
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta  # Set expiration based on the provided delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)  # Default expiration time
    
    # Prepare the payload with expiration and subject
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    
    # Encode the JWT using the refresh secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    
    return encoded_jwt  # Return the encoded refresh token
