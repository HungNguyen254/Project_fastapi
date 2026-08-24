from App.Database.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from datetime import datetime
class WorkItemModel(Base):
    __tablename__ = 'Work_items'
    id = Column(Integer,primary_key=True,autoincrement=True)
    site_id = Column(Integer,ForeignKey('Construction_sites.id'),nullable=False)
    title = Column(String(150),nullable=False)
    description = Column(Text,nullable=True)
    assignee_id = Column(Integer,ForeignKey('User.id'),nullable=True)
    status = Column(String(150),nullable=False)
    priority = Column(String(150),nullable=False)
    due_date = Column(DateTime,nullable=True)
    create_at = Column(DateTime,nullable=False,default=datetime.now)
    user = relationship('UserModel',back_populates='workitem')
    construc = relationship('ConstructionModel',back_populates='workitem')