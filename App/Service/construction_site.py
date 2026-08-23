from sqlalchemy.orm import Session
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Site_member_schema import *
from App.Models.Site_member import SiteMemberModel
from App.Core.config import setting
from App.Schemas.Construction_sites_schema import *
def Create_new_constructionsite(Info_create:ConstructionsSiteCreateRequest,db:Session,user_data:get_current_user):
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
        return setting.DB_no
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        return setting.Db_cne
    db.delete(check_construc)
    db.commit()
    return setting.Db_delete
def handle_Update_construction(construc_id:int,Info_update:ConstructionsSiteUpdateRequest,user_data:dict,db:Session):
    check_role =db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id'],ConstructionModel.id == construc_id).first()
    if not check_role:
        return setting.DB_no
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
            return setting.Db_cne
    new_info_update = Info_update.model_dump()
    for key,value in new_info_update.items():
        setattr(check_construc,key,value)
    db.commit()
    db.refresh(check_construc)
    return setting.Db_update
def Search_list_constructionsite(construc_name: str,db:Session,user_data:dict=get_current_user):
    search_construc = db.query(ConstructionModel).filter(ConstructionModel.name.contains(construc_name),ConstructionModel.owner_id == user_data['user_id']).all()
    if not search_construc:
        return False
    if construc_name == None:
        search_construc = db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id']).all()
        return search_construc
    return search_construc
