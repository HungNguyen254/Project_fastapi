from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
class ConstructionsSiteCreateRequest(BaseModel):
    name : str = Field(...)
    description : str = Field(...)
    owner_id : int = Field(...)
class ConstructionsSiteResponse(BaseModel):
    id : int
    name : str
    description : str
    owner : str
    create_at : datetime
    model_config= ConfigDict(from_attributes=True)
class ConstructionsSiteUpdateRequest(BaseModel):
    name : str = Field(...)
    description : str = Field(...)
    owner_id : int = Field(...)