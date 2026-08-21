from fastapi import APIRouter,status,HTTPException
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.Construction_sites_schema import *
from App.Service.construction_site import Create_new_constructionsite
from App.Core.config import setting
from App.Dependencies.auth import get_current_user
from App.Dependencies.role.permission import RoleCheck
auth_router = APIRouter(
    prefix='/site',
    tags=['site']
)
@auth_router.post('/construction',response_model=ConstructionsSiteResponse,dependencies=[Depends(RoleCheck(['User']))])
def Register_new_construction(Info_create:ConstructionsSiteCreateRequest,db:Session=Depends(get_db),user_data=Depends(get_current_user)):
    new_construc = Create_new_constructionsite(Info_create,db,user_data)
    return {
        'message':'Đã thêm mới công trình thành công',
        'id': new_construc.id,
        'name': new_construc.name,
        'description':new_construc.description,
        'owner':user_data['user_name'],
        'create_at':new_construc.create_at
    }