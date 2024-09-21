from itertools import count
from pyexpat import model
from typing import Optional, List
from random import randint
from datetime import datetime

from sqlalchemy import func

from app import Oauth2
from app.Oauth2 import get_current_user
from ..database import SessionLocal, engine, get_db
from .. import models, schema
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from random import randint

from ..database import SessionLocal, engine, get_db
from .. import models, schema
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # Querying posts with vote count
    posts = db.query(models.Posts, func.count(models.Votes.Post_id).label("votes")).join(
        models.Votes, models.Votes.Post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).all()
    
    # Convert the results into the expected Pydantic models
    result = [
        schema.PostOut(
            Post=schema.Post.from_orm(post_data),
            votes=votes
        )
        for post_data, votes in posts
    ]
    
    return result
    

@router.get("/{id}", response_model=schema.PostOut)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # Fetch post along with vote count
    post = db.query(models.Posts, func.count(models.Votes.Post_id).label("votes")).join(
        models.Votes, models.Votes.Post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    # If no post is found, raise a 404 error
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    post_data, votes = post  # Since it's a tuple, unpack it here

    # Convert the SQLAlchemy model into a Pydantic model using from_orm()
    post_out = schema.PostOut(
        Post=schema.Post.from_orm(post_data),
        votes=votes
    )

    return post_out

    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.CreatePost)
def create_post(Posts : schema.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute(""" INSERT INTO public."Posts" ("Title", "Content", "Author", "Rating", "Publish") VALUES(%s, %s, %s, %s, %s) RETURNING *""", (Posts.Title, Posts.Content, Posts.Author, Posts.Rating, Posts.Publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(Owners_Id=current_user.id, **Posts.dict(exclude={"Owners_Id"})) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
@router.delete("/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute(""" DELETE FROM public."Posts" WHERE id= %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    
    post = deleted_post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    if post.Owners_Id != current_user.id: # type: ignore
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Post with id: {id} has not thhe access to delete it")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return deleted_post_query

@router.put("/{id}", response_model=schema.Post)
def modify_post(id:int, Posts:schema.UpdatePost , db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # cursor.execute(""" UPDATE public."Posts" SET "Title" = %s, "Content" = %s, "Author" = %s, "Rating" = %s, "Publish" = %s WHERE id = %s RETURNING *""", 
    #             (Posts.Title, Posts.Content, Posts.Author, Posts.Rating, Posts.Publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    getting_post = db.query(models.Posts).filter(models.Posts.id == id)
    get_update_post = getting_post.first()
    if get_update_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    if get_update_post.Owners_Id != current_user.id: # type: ignore
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Post with id: {id} has not thhe access to delete it")
    
    getting_post.update(Posts.dict(), synchronize_session=False) # type: ignore
    db.commit()
  
    return getting_post.first()