from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
class UserCreateRequest(BaseModel):
    email : str = Field(...) 
    full_name :str = Field(...) 
    password_hash : str = Field(...) 
class Userlogin(BaseModel):
    email : str
    password_hash : str
class UserResponse(BaseModel):
    message: str
    id : int
    email : str
    full_name : str
    role : str
    create_at : datetime = Field(default=datetime.now)
    model_config= ConfigDict(from_attributes=True)
class UserUpdateRequest(BaseModel):
    email : str = Field(...)
    full_name :str = Field(...)
    password_hash : str = Field(...)
class GetUserInfo(BaseModel):
    message:str
    data: UserResponse
class SearchUser(BaseModel):
    email: str