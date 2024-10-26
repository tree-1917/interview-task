# Import necessary components from Pydantic for data validation and serialization
from pydantic import BaseModel  # Import the BaseModel class to create data models
import datetime  # Import datetime for handling date and time

# User creation request model
class UserCreate(BaseModel):
    username: str  # Username of the user; must be a string
    email: str  # Email address of the user; must be a string
    password: str  # Password of the user; must be a string

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
# Request details model for login functionality
class requestdetails(BaseModel):
    email: str  # Email address of the user; must be a string
    password: str  # Password of the user; must be a string
        
# Token schema model for token responses
class TokenSchema(BaseModel):
    access_token: str  # Access token; must be a string
    refresh_token: str  # Refresh token; must be a string

# Change password request model
class changepassword(BaseModel):
    email: str  # Email address of the user; must be a string
    old_password: str  # Old password of the user; must be a string
    new_password: str  # New password for the user; must be a string

# Token creation model for storing token information
class TokenCreate(BaseModel):
    user_id: str  # User ID associated with the token; must be a string
    access_token: str  # Access token; must be a string
    refresh_token: str  # Refresh token; must be a string
    status: bool  # Status indicating whether the token is active; must be a boolean
    created_date: datetime.datetime  # Timestamp of when the token was created; must be a datetime object


class OrganizationCreate(BaseModel):
    name: str
    description: str = None

class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    created_date: datetime.datetime
    members: list[UserResponse]

    class Config:
        from_attributes = True