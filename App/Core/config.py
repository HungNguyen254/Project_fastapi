import os
from dotenv import load_dotenv
load_dotenv('.env')
class config():
    def __init__(self):
        self.DB_ScKey = os.getenv('Secret_key')
        self.DB_algo = os.getenv('Algorithm')
        self.DB_exp = os.getenv('exp_time')
        self.DB_icp = os.getenv('INCORRECT_PASSWORD')
        self.DB_ice = os.getenv('INCORRECT_EMAIL')
setting = config()