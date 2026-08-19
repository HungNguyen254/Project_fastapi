import bcrypt
import jwt
def handle_hash_password(raw_password:str)->str:
    return bcrypt.hashpw(raw_password.encode('utf-8'),bcrypt.gensalt()).decode()
def handle_check_password(raw_password:str,hash_password:str)->bool:
    return bcrypt.checkpw(raw_password.encode(),hash_password.encode())