from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from random import randint
from psycopg2.extras import RealDictCursor
import time
from ..database import SessionLocal, engine, get_db
from . import models, schema
from fastapi import Depends, FastAPI, Response, status, HTTPException
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from ..database import SessionLocal, engine, get_db
from .. import models, schema
from sqlalchemy.orm import Session

router  = {
    "prefix" : "posts"
}


@router.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public."Posts" """)
    # Posts = cursor.fetchall() 
    Posts = db.query(models.Posts).all()
    return Posts

@router.get("/posts/{id}", response_model=schema.Post)
def get_single_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public."Posts" WHERE id = %s """, (str(id)))
    # one_post = cursor.fetchone()
    one_post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not one_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    return one_post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.CreatePost)
def create_post(Posts : schema.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO public."Posts" ("Title", "Content", "Author", "Rating", "Publish") VALUES(%s, %s, %s, %s, %s) RETURNING *""", (Posts.Title, Posts.Content, Posts.Author, Posts.Rating, Posts.Publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(**Posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
@router.delete("/posts/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM public."Posts" WHERE id= %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return deleted_post

@router.put("/posts/{id}", response_model=schema.Post)
def modify_post(id:int, Posts:schema.UpdatePost , db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE public."Posts" SET "Title" = %s, "Content" = %s, "Author" = %s, "Rating" = %s, "Publish" = %s WHERE id = %s RETURNING *""", 
    #             (Posts.Title, Posts.Content, Posts.Author, Posts.Rating, Posts.Publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    getting_post = db.query(models.Posts).filter(models.Posts.id == id)
    get_update_post = getting_post.first()
    if get_update_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    getting_post.update(Posts.dict(), synchronize_session=False)
    db.commit()
  
    return getting_post.first()