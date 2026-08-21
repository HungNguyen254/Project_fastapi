from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from App.Schemas.User_schema import *
from App.Models.User import UserModel
import jwt
from App.Core.Security.jwt_token import handle_create_access_token
from App.Core.Security.auth_user import handle_hash_password,handle_check_password
from App.Core.config import setting
def handle_register_user(req_info:UserCreateRequest,db:Session):
    check_email = db.query(UserModel).filter(UserModel.email == req_info.email).first()
    if check_email:
        return False
    hash_password = handle_hash_password(req_info.password_hash)
    new_user = UserModel(
        email = req_info.email,
        full_name = req_info.full_name,
        password_hash = hash_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def handle_login_user(req_info:Userlogin,db:Session):
    check_user = db.query(UserModel).filter(UserModel.email == req_info.email).first()
    if not check_user:
        return setting.DB_ice
    check_password = handle_check_password(req_info.password_hash,check_user.password_hash)
    if not check_password:
        return setting.DB_ice
    token = handle_create_access_token(check_user.id,check_user.role,check_user.full_name)
    return {
        'token':token,
        'type_token':'Bearer'
    }
def handle_list_user(Info_search:SearchUser,db:Session):
    search_email = db.query(UserModel).filter(UserModel.email.contains(Info_search.email)).all()
    return search_email