from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped

from .database import Base


class Posts(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, unique=True)
    Title = Column(String(50), nullable=False)
    Content = Column(String(500), nullable=False)
    Author = Column(String(50), nullable=False)
    Rating = Column(Integer, nullable=True)
    Created_At = Column(DateTime, server_default=func.now(), comment='Account creation timestamp')
    Publish = Column(Boolean, nullable=False, server_default='true')
    Mobile_Number = Column(String(15), nullable=True)
    Owners_Id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    
    Owner: Mapped["Users"] = relationship("Users")    
    
class Users(Base):
    __tablename__  = "Users"
    
    id = Column(Integer, primary_key=True, unique=True, nullable = False)
    Email = Column(String(35), unique=True, nullable = False)
    Password = Column(String, unique=True, nullable = False)
    Created_At = Column(DateTime, server_default=func.now(), comment='Account creation timestamp')
    
class Votes(Base):
    __tablename__  = "Votes"
    
    User_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True)
    Post_id = Column(Integer, ForeignKey(
        "Posts.id", ondelete="CASCADE"), primary_key=True)