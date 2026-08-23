from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
class SiteMemberCreateRequest(BaseModel):
    site_id:int = Field(...)
    user_id : int = Field(...)
    role : str = Field(default='Member')
class SiteMemberResponse(BaseModel):
    id : int
    site_id:int
    user_id : int
    role : str
    joined_at : datetime
    model_config= ConfigDict(from_attributes=True)
class SiteMemberUpdateRequest(BaseModel):
    site_id:int = Field(...)
    user_id : int = Field(...)
    role : str = Field(...)