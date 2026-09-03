from fastapi import APIRouter,status,HTTPException
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.Construction_sites_schema import *
from App.Service.construction_site import *
from App.Core.config import setting
from App.Dependencies.auth import get_current_user
from App.Dependencies.role.permission import RoleCheck
from App.Schemas.Site_member_schema import  SiteMemberCreateRequest
auth_router = APIRouter(
    prefix='/construction-site',
    tags=['construction-site']
)
@auth_router.post('/construction',response_model=ConstructionsSiteResponse,dependencies=[Depends(RoleCheck(['User','Admin']))])
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
@auth_router.get('/construction',response_model=ConstrucResponseSearch,dependencies=[Depends(RoleCheck(['User','Admin']))])
def Search_construc(construc_name = None,db:Session=Depends(get_db),user_data:dict=Depends(get_current_user)):
    search_construc_by_name = Search_list_constructionsite(construc_name,db,user_data)
    return {
            'message':'Đã tìm thấy công trình',
            'data': search_construc_by_name
        }
@auth_router.delete('/construction/{construc_id}',dependencies=[Depends(RoleCheck(['User','Admin']))])
def Delete_construc(construc_id:int,user_data : dict=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_con = handle_Delete_construction(user_data,construc_id,db)
    return delete_con
@auth_router.patch('/construction/{construc_id}',dependencies=[Depends(RoleCheck(['User','Admin']))])
def Update_construc(construc_id:int,Info_update:ConstructionsSiteUpdateRequest,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    update_con = handle_Update_construction(construc_id,Info_update,user_data,db)
    return update_con
@auth_router.delete('/construction/{construc_id}/solf_delete',dependencies=[Depends(RoleCheck(['User','Admin']))])
def Solf_delete_construc(construc_id:int,user_data : dict=Depends(get_current_user),db:Session=Depends(get_db)):
    solf_delete = handle_soft_Delete_construction(user_data,construc_id,db)
    return solf_delete