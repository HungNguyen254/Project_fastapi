from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
class WorkItemRequest(BaseModel):
    title : str = Field(...)
    description : str = Field(...)
    status : str = Field(default='TODO') 
    priority : str = Field(default='Medium')
    due_date: int = Field(...)
class WorkItemResponse(BaseModel):
    id : int
    site_id : int
    title : str
    description : str
    assignee_id : int
    status : str
    priority : str
    due_date: int
    create_at : datetime
    model_config= ConfigDict(from_attributes=True)
class WorkItemUpdateRequest(BaseModel):
    site_id : int = Field(...)
    title : str = Field(...)
    description : str = Field(...)
    assignee_id : int = Field(...)
    status : str = Field(default='TODO') 
    priority : str = Field(default='Medium')
    due_date: int = Field(...)