from sqlalchemy.orm import Session
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Site_member_schema import *
from App.Models.Site_member import SiteMemberModel
from App.Core.config import setting
from App.Schemas.Construction_sites_schema import *
def Add_member_to_construcsite(user_data:dict,Member_info:SiteMemberCreateRequest,db:Session):

    check_excist_site = db.query(ConstructionModel).filter(ConstructionModel.id == Member_info.site_id).first()
    if not check_excist_site:
        return setting.DB_sne
    if check_excist_site.owner_id != int(user_data['user_id']):
        return setting.DB_no
    check_excist_member = db.query(SiteMemberModel).filter(SiteMemberModel.user_id == Member_info.user_id,SiteMemberModel.site_id == Member_info.site_id).first()
    if check_excist_member:
        return setting.DB_ecm
    new_member = SiteMemberModel(
        site_id = Member_info.site_id,
        user_id = Member_info.user_id,
        role = Member_info.role
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {
        'message':'Thêm member thành công',
        'data': new_member
    }
def handle_only_member_can_watch(member_id:int,db:Session):
    check_member = db.query(SiteMemberModel).filter(SiteMemberModel.user_id == member_id).first()
    if check_member == []:
        return setting.Db_nos
    construc = db.query(ConstructionModel).filter(ConstructionModel.id == check_member.user_id).all()
    return construc
def handle_update_member(construc_id:int,site_member_id:int,Info_member_update:SiteMemberUpdateRequest,user_data:dict,db:Session):
    check_member =db.query(SiteMemberModel).filter(SiteMemberModel.user_id == site_member_id,SiteMemberModel.site_id == construc_id).first()
    if not check_member:
        return setting.Db_mne
    check_owner = db.query(ConstructionModel).filter(ConstructionModel.id == check_member.site_id,ConstructionModel.owner_id == user_data['user_id']).first()
    if not check_owner:
        return setting.DB_no
    new_info_update = Info_member_update.model_dump()
    for key,value in new_info_update.items():
            setattr(check_member,key,value)
    db.commit()
    db.refresh(check_member)
    return setting.Db_update
def handle_Delete_member(construc_id:int,member_id:int,user_data:dict,db:Session):
    check_member =db.query(SiteMemberModel).filter(SiteMemberModel.user_id == member_id,SiteMemberModel.site_id == construc_id).first()
    if not check_member:
        return setting.Db_mne
    check_owner = db.query(ConstructionModel).filter(ConstructionModel.id == check_member.site_id,ConstructionModel.owner_id == user_data['user_id']).first()
    if not check_owner:
        return setting.DB_no
    if check_member.user_id == user_data['user_id']:
        return setting.DB_no
    db.delete(check_member)
    db.commit()
    return setting.Db_delete
def handle_get_list_site_member(site_id:int,db:Session):
    check_member = db.query(SiteMemberModel).filter(SiteMemberModel.site_id == site_id).all()
    return check_member