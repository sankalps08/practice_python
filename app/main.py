from fastapi import FastAPI
from app import models
from app.routes import auth
from .database import engine
from .routes import posts,users,votes
from .config import settings

print(settings.database_username)
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message" : "Welcome to my blog website"}




