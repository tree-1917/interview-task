import app.schemas as schemas
import app.models as models
import jwt
from datetime import datetime, timedelta
from app.models import User, TokenTable
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth_bearer import JWTBearer
from app.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "VCFPSzLwUcta0qRhfqQ7w3AtGWAvkMXlO3GGC1DziKY="  # should be kept secret
JWT_REFRESH_SECRET_KEY = "8lZV60sYpxUfT0JRLzmIIJUnM3X5V+PN26DVrX5reDA="

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

authRoute = APIRouter(
    prefix = "/auth", 
    tags = ["Auth"]
)

@authRoute.post("/signup")
async def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully"}

@authRoute.post('/signin', response_model=schemas.TokenSchema)
def login(request: schemas.requestdetails , db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.TokenTable(user_id=user.id, access_toke=access, refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    
    return {
        "access_token": access,
        "refresh_token": refresh,
    }

@authRoute.post('/refresh_token', response_model=schemas.TokenSchema)
def refresh_token(refresh_token: str, db: Session = Depends(get_session)):
    try:
        # Decode the refresh token
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        # Check if the refresh token exists in the database
        token_entry = db.query(TokenTable).filter(TokenTable.user_id == user_id, TokenTable.refresh_toke == refresh_token).first()
        if not token_entry:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")

        # Create new access and refresh tokens
        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)

        # Update the token in the database
        token_entry.access_toke = new_access_token
        token_entry.refresh_toke = new_refresh_token
        db.commit()
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")

@authRoute.get('/getusers', dependencies=[Depends(JWTBearer())])
async def get_users(session: Session = Depends(get_session)):
    users = session.query(models.User).all()
    return users
