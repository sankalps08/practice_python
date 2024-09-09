from sqlalchemy import Boolean, Column, Integer, String, DateTime, func

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
    
