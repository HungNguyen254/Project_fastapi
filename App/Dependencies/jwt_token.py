import jwt
from datetime import datetime,timezone,timedelta
from env import *
def handle_create_access_token(user_id:int,role:str,full_name: str):
    time = datetime.now(timezone.utc)
    pay_load ={
        'sub':user_id,
        'role':role,
        'full_name':full_name,
        'iat':time,
        'exp':time + timedelta(minutes=30)
    }
    return jwt.encode(pay_load,Secret_key,algorithm=Algorithm)