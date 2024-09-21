from ..database import get_db
from .. import models, schema
from fastapi import Depends,status, APIRouter, HTTPException
from .. import models, schema
from sqlalchemy.orm import Session
from app import utils


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def Create_User(Users : schema.UserCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO public."Posts" ("Title", "Content", "Author", "Rating", "Publish") VALUES(%s, %s, %s, %s, %s) RETURNING *""", (Posts.Title, Posts.Content, Posts.Author, Posts.Rating, Posts.Publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    hashed_password = utils.get_password_hash(Users.Password)
    Users.Password = hashed_password
    new_user = models.Users(**Users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schema.UserResponse)
def get_single_user(id:int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public."Posts" WHERE id = %s """, (str(id)))
    # one_post = cursor.fetchone()
    one_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not one_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} was not found")
    return one_user