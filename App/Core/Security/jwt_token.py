import jwt
from datetime import datetime,timezone,timedelta
from App.Core.config import setting
from fastapi import HTTPException,status
def handle_create_access_token(user_id:int,role:str,full_name: str):
    time = datetime.now(timezone.utc)
    pay_load ={
        'type':'access',
        'sub':str(user_id),
        'role':role,
        'full_name':full_name,
        'iat':time,
        'exp':time + timedelta(seconds=30)
    }
    return jwt.encode(pay_load,setting.DB_ScKey,algorithm=setting.DB_algo)
def handle_create_refresh_access_token(user_id:int,role:str,full_name: str):
    time = datetime.now(timezone.utc)
    pay_load ={
        'type':'refresh',
        'sub':str(user_id),
        'role':role,
        'full_name':full_name,
        'exp':time + timedelta(hours=3)
    }
    return jwt.encode(pay_load,setting.DB_ScKey,algorithm=setting.DB_algo)
def verify_token(token:str):
    try:
        payload =  jwt.decode(token,setting.DB_ScKey,algorithms=[setting.DB_algo])
        return payload
    except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Token đã hết hạn')
    except jwt.InvalidTokenError:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Sai token')