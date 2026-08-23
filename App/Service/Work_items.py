from sqlalchemy.orm import Session
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Work_items_schema import *
from App.Models.Work_items import *
from App.Models.Site_member import *
from App.Core.config import setting
from App.Schemas.Construction_sites_schema import *
def handle_add_workitem(construc_id:int,Info_workitem:WorkItemRequest,user_data:dict,db:Session):
    check_construc = db.query(ConstructionModel).filter(ConstructionModel.id == construc_id).first()
    if not check_construc:
        return setting.Db_cne
    check_member_construc = db.query(SiteMemberModel).filter(SiteMemberModel.site_id == construc_id,SiteMemberModel.user_id == user_data['user_id']).first()
    if not check_member_construc:
        return setting.DB_no