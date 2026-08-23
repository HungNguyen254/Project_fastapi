from App.Database.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
class SiteMemberModel(Base):
    __tablename__ = 'Site_member'
    id = Column(Integer,primary_key=True,autoincrement=True)
    site_id = Column(Integer,ForeignKey('Construction_sites.id'))
    user_id = Column(Integer,ForeignKey('User.id'))
    role = Column(String(100),nullable=False)
    joined_at = Column(DateTime,nullable=False,default=datetime.now)
    user = relationship('UserModel',back_populates='sitemember')
    construc = relationship('ConstructionModel',back_populates='sitemember')