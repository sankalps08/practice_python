from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint




class UserResponse(BaseModel):
    Email: EmailStr
    Created_At: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True


    
class CreatePost(BaseModel):
    id: int
    Title:str
    Content:str
    Author:str
    Publish: bool = True
    Owners_Id: Optional[int] = None
    Rating:int
    
    class Config:
        orm_mode = True
        from_attributes = True
    
    
class Post(CreatePost):
    Owner: UserResponse
    
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
        from_attributes = True
    
class UpdatePost(CreatePost):
    Rating:int
    
class UserCreate(BaseModel):
    Email: EmailStr
    Password: str
    
    
class UserLogin(BaseModel):
    Email: EmailStr
    Password: str
    
class TokenId(BaseModel):
    id:Optional[int]
    
    
    
class Vote(BaseModel):
    Post_id: int
    dir: conint(le=1) # type: ignore
    
