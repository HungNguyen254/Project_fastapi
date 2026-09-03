from fastapi import FastAPI,APIRouter,Request
from App.Router.User import auth_router
from App.Router.Construction import auth_router as auth_site
from App.Router.SiteMember import auth_router as auth_site_member
from App.Database.database import Base,engine
from App.Router.Work_items import auth_router as auth_work_item
import time
app = FastAPI()
app.include_router(auth_router)
app.include_router(auth_site)
app.include_router(auth_site_member)
app.include_router(auth_work_item)
Base.metadata.create_all(bind=engine)
@app.get('/health')
def check_health():
    return {'message':'Api is OK'}
