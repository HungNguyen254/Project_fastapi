from sqlalchemy.orm import Session
from fastapi import HTTPException,status,UploadFile
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Work_items_schema import *
from App.Models.Work_items import *
from App.Models.Site_member import *
from App.Core.config import setting
from App.Service.page import paginate
from datetime import datetime,timedelta
from App.Schemas.Construction_sites_schema import *
import os
import uuid
import shutil
DIR_UPLOAD = 'upload/images'
os.makedirs(DIR_UPLOAD,exist_ok=True)
def handle_add_workitem(construc_id:int,Info_workitem:WorkItemRequest,user_data:dict,db:Session):
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_cne)
    check_member_construc = db.query(SiteMemberModel).filter(SiteMemberModel.site_id == construc_id,SiteMemberModel.user_id == user_data['user_id']).first()
    if not check_member_construc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=setting.DB_no)
    if Info_workitem.status.upper() not in ['TODO','INPROGRESS','COMPLETE']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_dne)
    if Info_workitem.priority.upper() not in ['LOW','MEDIUM','HIGH']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_dne)
    new_workitem = WorkItemModel(
        site_id = construc_id,
        title = Info_workitem.title,
        description = Info_workitem.description,
        status = Info_workitem.status.upper(),
        priority = Info_workitem.priority.upper(),
        due_date = datetime.now() + timedelta(days=Info_workitem.due_date)
    )
    db.add(new_workitem)
    db.commit()
    db.refresh(new_workitem)
    return new_workitem
def handle_search_construc_have_work_item(construc_id:int,user_data:dict,db:Session):
    check_work_item = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_work_item:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=setting.DB_sne)
    check_work = db.query(WorkItemModel).filter(WorkItemModel.site_id == construc_id).all()
    if not check_work:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=setting.DB_no)
    return paginate(check_work,3,1)
def handle_update_work_item(work_item_id:int,Info_update:WorkItemUpdateRequest,user_data:dict,db:Session):
    check_work_item = db.query(WorkItemModel).filter(WorkItemModel.id == work_item_id).first()
    if not check_work_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_wine)
    update_workitem = WorkItemModel(
            site_id = WorkItemModel.site_id,
            title = WorkItemModel.title,
            description = WorkItemModel.description,
            status = WorkItemModel.status.upper(),
            priority = WorkItemModel.priority.upper(),
            due_date = datetime.now() + timedelta(days=Info_update.due_date)
        )
    db.commit()
    db.refresh(update_workitem)
    return update_workitem
def Handle_delete_work_item(work_item_id:int,user_data:dict,db:Session):
    check_per = db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id']).first()
    if not check_per:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=setting.DB_no)
    check_work_item = db.query(WorkItemModel).filter(WorkItemModel.id == work_item_id).first()
    if not check_work_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_wine)
    db.delete(check_work_item)
    db.commit()
    return setting.Db_delete
def handle_upload_img(file_img:UploadFile):
    type_img = file_img.filename.split('.')[-1]
    if type_img != 'png' and type_img != 'jpg':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Wrong type file')
    new_name_file = f'{uuid.uuid4().hex}.{type_img}'
    url_img_create = os.path.join(DIR_UPLOAD,new_name_file)
    with open(url_img_create,'wb') as buffer:
        shutil.copyfileobj(file_img.file,buffer)
    return file_img