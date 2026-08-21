from sqlalchemy.orm import Session
from App.Models.Construction_sites import ConstructionModel
from App.Dependencies.auth import get_current_user
from App.Schemas.Construction_sites_schema import ConstructionsSiteCreateRequest
def Create_new_constructionsite(Info_create:ConstructionsSiteCreateRequest,db:Session,user_data:get_current_user):
    new_construction = ConstructionModel(
        name = Info_create.name,
        description = Info_create.description,
        owner_id = user_data['user_id']
    )
    db.add(new_construction)
    db.commit()
    db.refresh(new_construction)
    return new_construction
def Search_list_constructionsite(construc_name: str,db:Session,user_data:get_current_user):
    search_construc = db.query(ConstructionModel).filter(ConstructionModel.name.contains(construc_name)).all()
    search_owner = db.query(ConstructionModel).filter(ConstructionModel.owner_id == user_data['user_id']).all()
    if not search_construc and search_owner:
        return False
    return search_construc