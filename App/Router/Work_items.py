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
    tags=['construction-site-workitem']
)