from fastapi import APIRouter,status,HTTPException
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.Construction_sites_schema import *
from App.Service.construction_site import *
from App.Service.Site_member import *
from App.Core.config import setting
from App.Dependencies.auth import get_current_user
from App.Dependencies.role.permission import RoleCheck
from App.Schemas.Site_member_schema import  SiteMemberCreateRequest
auth_router = APIRouter(
    prefix='/construction-site',
    tags=['construction-site-member']
)
@auth_router.post('/site_member/{id}/members',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_201_CREATED)
def Add_member_to_construc(Member_info:SiteMemberCreateRequest,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    new_member = Add_member_to_construcsite(user_data,Member_info,db)
    return new_member
@auth_router.get('/site_member/{member_id}',dependencies= [Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_200_OK)
def only_member_can_watch(member_id:int,db:Session=Depends(get_db)):
    check_member = handle_only_member_can_watch(member_id,db)
    return check_member
@auth_router.delete('/site_member/{member_id}/members',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code = status.HTTP_200_OK)
def Delete_member(member_id:int,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_mem = handle_Delete_member(member_id,user_data,db)
    return delete_mem
@auth_router.patch('site_member/{member_id}/member',dependencies=[Depends(RoleCheck(['User','Admin']))])
def Update_member(construc_id:int,site_member_id:int,Info_member_update:SiteMemberUpdateRequest,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    update_mem = handle_update_member(construc_id,site_member_id,Info_member_update,user_data,db)
    return update_mem
@auth_router.get('/site_member/{site_id}/members',response_model=list[SiteMemberResponse],dependencies=[Depends(RoleCheck(['User','Admin']))])
def get_list_member(site_id:int,db:Session=Depends(get_db)):
    check_member = handle_get_list_site_member(site_id,db)
    print(len(check_member))
    print(check_member)
    return check_member