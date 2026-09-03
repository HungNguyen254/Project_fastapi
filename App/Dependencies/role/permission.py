from fastapi import HTTPException,status,Depends
from App.Dependencies.auth import get_current_user
class RoleCheck:
    def __init__(self,role_allow:list):
        self.role_allow=role_allow
    def __call__(self,user_data:dict = Depends(get_current_user)):
        role_name = user_data.get('role','')
        if role_name not in self.role_allow:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Bạn không có quyền truy cập chức năng này')
        return user_data