from fastapi import APIRouter,status,HTTPException
from fastapi import Depends
from App.Database.database import get_db
from sqlalchemy.orm import Session
from App.Schemas.Work_items_schema import *
from App.Service.construction_site import *
from App.Service.Work_items import *
from App.Core.config import setting
from App.Dependencies.auth import get_current_user
from App.Dependencies.role.permission import RoleCheck
from App.Schemas.Site_member_schema import  SiteMemberCreateRequest
auth_router = APIRouter(
    prefix='/construction-site',
    tags=['construction-site-workitem']
)
@auth_router.post('/Work-item',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_201_CREATED)
def add_workitem(construc_id:int,Info_workitem:WorkItemRequest,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    add_new_workitem = handle_add_workitem(construc_id,Info_workitem,user_data,db)
    return {'message':'Đã thêm hạng mục thi công thành công',
        'data':add_new_workitem}
@auth_router.get('/Work-item/{construc_id}',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_200_OK)
def search_construc_have_work_item(construc_id:int,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    check_work = handle_search_construc_have_work_item(construc_id,user_data,db)
    return check_work
@auth_router.patch('/Work-item/{work_item_id}',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_200_OK)
def update_work_item(work_item_id:int,Info_update:WorkItemUpdateRequest,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    update_work = handle_update_work_item(work_item_id,Info_update,user_data,db)
    return {'message':'Đã cập nhật thành công',
            'data':update_work}
@auth_router.delete('/Work-item/{work_item_id}',dependencies=[Depends(RoleCheck(['User','Admin']))],status_code=status.HTTP_200_OK)
def delete_work_item(work_item_id:int,user_data:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_work = Handle_delete_work_item(work_item_id,user_data,db)
    return delete_work