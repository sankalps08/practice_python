from datetime import datetime
from fastapi import Depends, HTTPException, APIRouter,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils import verify_password
from ..database import get_db

from app import models, schema, Oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def Login_user(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.Email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(user_cred.password, user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token_final = Oauth2.create_access_token(data = {"users_id": user.id})
    
    return {"access_token" : access_token_final, "token_type" : "bearer", "Login_At": datetime.now()}