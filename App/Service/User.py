from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from App.Schemas.User_schema import *
from App.Models.User import UserModel
import jwt
from App.Dependencies.jwt_token import handle_create_access_token,Secret_key,Algorithm
from App.Dependencies.auth_user import handle_hash_password,handle_check_password
import os
from dotenv import load_dotenv
load_dotenv()
wrong_email = os.getenv('INCORRECT_EMAIl')
wrong_password = os.getenv('INCORRECT_PASSWORD')
secret_key = os.getenv('Secret_key')
Security_token = HTTPBearer
def handle_register_user(req_info:UserCreateRequest,db:Session):
    check_email = db.query(UserModel).filter(UserModel.email == req_info.email).first()
    if check_email:
        return False
    hash_password = handle_hash_password(req_info.password_hash)
    new_user = UserModel(
        email = req_info.email,
        full_name = req_info.full_name,
        password_hash = hash_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def handle_login_user(req_info:Userlogin,db:Session):
    check_user = db.query(UserModel).filter(UserModel.email == req_info.email).first()
    if not check_user:
        return wrong_email
    check_password = handle_check_password(req_info.password_hash,check_user.password_hash)
    if not check_password:
        return wrong_password
    token = handle_create_access_token(check_user.id,check_user.full_name,check_user.role)
    return {
        'token':token,
        'type_token':'Beare'
    }
def handle_take_info_from_token(cre:HTTPAuthorizationCredentials=Depends(Security_token)):
    token = cre.credentials
    try:
        payload = jwt.decode(token,secret_key,algorithms=[Algorithm])
        return {
            'id':payload.get('sub',''),
            'full_name': payload.get('full_name',''),
            'role':payload.get('role','')
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Token đã hết hạn')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Sai token')