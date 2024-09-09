from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import SessionLocal, engine, get_db
from . import models, schema
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'API',user = 'postgres',password = 'Rockers08@', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failded")
        print("Error : ", error)
        time.sleep(4)
    
my_post = []

@app.get("/")
async def root():
    return {"message" : "Welcome to my blog website"}




