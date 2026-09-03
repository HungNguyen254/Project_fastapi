from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Site_member_schema import *
from App.Models.Site_member import SiteMemberModel
from App.Core.config import setting
from App.Schemas.Construction_sites_schema import *
def Create_new_constructionsite(Info_create:ConstructionsSiteCreateRequest,db:Session,user_data:get_current_user):
    check_excist_construc = db.query(ConstructionModel).filter(ConstructionModel.name == Info_create.name).first()
    if check_excist_construc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Công trình đã tồn tại')
    if Info_create.name == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=setting.Db_ed)
    new_construction = ConstructionModel(
        name = Info_create.name,
        description = Info_create.description,
        owner_id = user_data['user_id']
    )
    db.add(new_construction)
    db.commit()
    db.refresh(new_construction)
    new_site_owner = SiteMemberModel(
        site_id = new_construction.id,
        user_id = user_data['user_id'],
        role = 'Owner'
    )
    db.add(new_site_owner)
    db.commit()
    db.refresh(new_site_owner)
    return new_construction
def handle_Delete_construction(user_data : dict,construc_id:int,db:Session):
    check_role =db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id'],ConstructionModel.id == construc_id).first()
    if not check_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.DB_no)
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.Db_cne)
    db.delete(check_construc)
    db.commit()
    return setting.Db_delete
def handle_Update_construction(construc_id:int,Info_update:ConstructionsSiteUpdateRequest,user_data:dict,db:Session):
    check_role =db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id'],ConstructionModel.id == construc_id).first()
    if not check_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.DB_no)
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.Db_cne)
    new_info_update = Info_update.model_dump()
    for key,value in new_info_update.items():
        setattr(check_construc,key,value)
    db.commit()
    db.refresh(check_construc)
    return setting.Db_update
def Search_list_constructionsite(construc_name:str|None,db:Session,user_data:dict=get_current_user):
    if construc_name == None:
        search_construc_2 = db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id']).all()
        return search_construc_2
    search_construc = db.query(ConstructionModel).filter(ConstructionModel.name.contains(construc_name),ConstructionModel.owner_id == user_data['user_id']).all()
    if not search_construc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Không tìm thấy công trình cần tìm')
    return search_construc
def handle_soft_Delete_construction(user_data : dict,construc_id:int,db:Session):
    check_role =db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id'],ConstructionModel.id == construc_id).first()
    if not check_role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.DB_no)
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=setting.Db_cne)
    check_construc.is_delete = True
    db.commit()
    db.refresh(check_construc)
    return {'message':'Đã thực hiện hành động xóa mềm thành công'}
