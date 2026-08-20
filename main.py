from fastapi import FastAPI,APIRouter,Request
from App.Router.User import auth_router
from App.Database.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI()
app.include_router(auth_router)
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
