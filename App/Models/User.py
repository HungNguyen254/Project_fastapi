from App.Database.database import Base
from datetime import datetime
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
class UserModel(Base):
    __tablename__ = 'User'
    id = Column(Integer,primary_key=True,autoincrement=True)
    email = Column(String(100),nullable=False,unique=True)
    password_hash = Column(String(150),nullable=False)
    full_name = Column(String(100),nullable=False)
    role = Column(String(20),nullable=False,default='User')
    is_active = Column(Boolean,default=True)
    create_at = Column(DateTime,nullable=False,default=datetime.now)
    construc = relationship('ConstructionModel',back_populates='user')
    sitemember = relationship('SiteMemberModel',back_populates='user')
    workitem = relationship('WorkItemModel',back_populates='user')