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
        return {
                'sub':payload.get('sub',''),
                'role':payload.get('role',''),
                'full_name': payload.get('full_name','')
            }
    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Token đã hết hạn')
    except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Sai token')