from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
from . import schema,models
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from app import database
from .config import settings

outh2_param = OAuth2PasswordBearer(tokenUrl = "login")


# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.isoformat()})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    
    return access_token

def verify_access_token(token: str, credential_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        id = payload.get("users_id")
        
        if id is None:
            raise credential_exception
        token_data = schema.TokenId(id = id)
    except JWTError:
        raise credential_exception
    
    return token_data
    
def get_current_user(token: str = Depends(outh2_param), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Your credentials not validated", headers={"WWW-Authenticate": "Bearer"} )
    
    tokens = verify_access_token(token, credential_exception)
    
    user = db.query(models.Users).filter(models.Users.id == tokens.id).first()
    return user