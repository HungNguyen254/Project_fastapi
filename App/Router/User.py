from fastapi import APIRouter,status
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.User_schema import *
from App.Service.User import handle_register_user,handle_login_user,handle_take_info_from_token
import os
from dotenv import load_dotenv
load_dotenv()
wrong_email = os.getenv('INCORRECT_EMAIl')
wrong_password = os.getenv('INCORRECT_PASSWORD')
auth_router = APIRouter(
    prefix='/auth',
    tags=['Authe']
)
@auth_router.post('/register',response_model=UserResponse)
def Register_user(req_info:UserCreateRequest,db:Session=Depends(get_db)):
    new_user = handle_register_user(req_info,db)
    if new_user == False:
        return {
            'message':'Email đã được đăng ký trước đó'
        }
    return {
        'message':'Đã đăng ký tài khoản thành công',
        'data': new_user
    }
@auth_router.post('/login')
def Login_user(req_info:Userlogin,db:Session=Depends(get_db)):
    User_try_login = handle_login_user(req_info,db)
    if User_try_login == wrong_email:
        return {'message':'Email hoặc mật khẩu không đúng'}
    if User_try_login == wrong_password:
        return {'message':'Email hoặc mật khẩu không đúng'}
    return User_try_login
@auth_router.get('/me',status_code=status.HTTP_200_OK)
def Take_info_from_token(data:dict=Depends(handle_take_info_from_token)):
    return {'message':'Đọc dữ liệu thành công',
            'data':data}