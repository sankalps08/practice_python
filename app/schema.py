from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    Title:str
    Content:str
    Author:str
    Publish: bool = True
    
class CreatePost(Post):
    Rating:int
    
    class Config:
        orm_mode = True
    
class UpdatePost(Post):
    Rating:int