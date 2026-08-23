from fastapi.security import HTTPBearer
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
import jwt
from App.Core.config import setting
Security_token = HTTPBearer()
def get_current_user(cre:HTTPAuthorizationCredentials=Depends(Security_token)):
    token = cre.credentials
    try:
        payload = jwt.decode(token,setting.DB_ScKey,algorithms=[setting.DB_algo])
        user_name = payload.get('full_name')
        role = payload.get('role')
        user_id = payload.get('sub')
        data =  {
                'user_name' :  user_name,
                'role' : role,
                'user_id' : user_id
            }
        return data
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Token đã hết hạn')
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Sai token')