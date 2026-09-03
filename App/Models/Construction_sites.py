from App.Database.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
class ConstructionModel(Base):
    __tablename__ = 'Construction_sites'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(100),nullable=False,unique=True)
    description = Column(Text,nullable=True)
    owner_id = Column(Integer,ForeignKey('User.id'))
    create_at = Column(DateTime,nullable=False,default=datetime.now)
    is_delete = Column(Boolean,default=False)
    user = relationship('UserModel',back_populates='construc')
    sitemember = relationship('SiteMemberModel',back_populates='construc')
    workitem = relationship('WorkItemModel',back_populates='construc')
    