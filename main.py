from fastapi import FastAPI,APIRouter,Request
from App.Router.User import auth_router
from App.Router.Construction import auth_router as auth_site
from App.Router.SiteMember import auth_router as auth_site_member
from App.Database.database import Base,engine
from App.Router.Work_items import auth_router as auth_work_item
from fastapi.middleware.cors import CORSMiddleware
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
list_origin = [
    'http://localhost:3000'
    'http://localhost:3001'
    'http://localhost:3002'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=list_origin,
    allow_credentials=True,
    allow_methods=['*']
)
@app.middleware('http')
async def handle_calc_time_call_api(req:Request,call_next):
    start_time = time.time()
    response = await call_next(req)
    now_time = time.time() - start_time
    print(now_time)
    return response
