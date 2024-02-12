from sqlalchemy import Column, String, ForeignKey
from .connection import Base
from sqlalchemy.orm import relationship

class userTable(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key = True)
    password = Column(String, nullable = False)
    url = relationship("urlTable", back_populates = "users")

class urlTable(Base):
    __tablename__ = 'url'
    username = Column(String, ForeignKey("users.username"))
    org_url = Column(String, nullable = False)
    nickname = Column(String, nullable = False)
    short_url = Column(String, nullable = False, primary_key = True)
    users = relationship("userTable", back_populates = "url")