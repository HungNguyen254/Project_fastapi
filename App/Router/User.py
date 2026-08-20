from fastapi import APIRouter,status,HTTPException
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.User_schema import *
from App.Service.User import handle_register_user,handle_login_user
from App.Core.config import setting
from App.Dependencies.auth import get_current_user
from App.Dependencies.role.permission import RoleCheck
auth_router = APIRouter(
    prefix='/auth',
    tags=['Authe']
)
@auth_router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def Register_user(req_info:UserCreateRequest,db:Session=Depends(get_db)):
    new_user = handle_register_user(req_info,db)
    if new_user == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email đã được sử dụng'
        )
    return {
        'message':'Đã đăng ký tài khoản thành công',
        'id' : new_user.id,
        'email' : new_user.email,
        'full_name' : new_user.full_name,
        'role': new_user.role,
        'create_at' : new_user.create_at
    }
@auth_router.post('/login')
def Login_user(req_info:Userlogin,db:Session=Depends(get_db)):
    User_try_login = handle_login_user(req_info,db)
    if User_try_login == setting.DB_ice:
       raise HTTPException(
                   status_code=status.HTTP_400_BAD_REQUEST,
                   detail='Email hoặc mật khẩu không đúng'
               )
    if User_try_login == setting.DB_icp:
        raise HTTPException(
                           status_code=status.HTTP_400_BAD_REQUEST,
                           detail='Email hoặc mật khẩu không đúng'
                       )
    return User_try_login
@auth_router.get('/users/me',status_code=status.HTTP_200_OK)
def Take_info_from_token(data:dict=Depends(get_current_user)):
    return {'message':'Đọc dữ liệu thành công',
            'data':data}
@auth_router.get('/user',dependencies=[Depends(RoleCheck(['User']))])
def get_admin():
    return {
        'message':'login success'
    }