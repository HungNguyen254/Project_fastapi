import os
from dotenv import load_dotenv
load_dotenv('env_s.env')
class config():
    def __init__(self):
        self.DB_ScKey = os.getenv('Secret_key')
        self.DB_algo = os.getenv('Algorithm')
        self.DB_exp = os.getenv('exp_time')
        self.DB_icp = os.getenv('INCORRECT_PASSWORD')
        self.DB_ice = os.getenv('INCORRECT_EMAIL')
        self.DB_ecm = os.getenv('Excist_member')
        self.DB_sne = os.getenv('Site_not_excist')
        self.DB_no = os.getenv('not_owner')
        self.Db_nos = os.getenv('none_site')
        self.Db_cne = os.getenv('construc_not_excist')
        self.Db_delete = os.getenv('Delete_success')
        self.Db_update = os.getenv('update_success')
        self.Db_mne = os.getenv('Member_not_excist')
setting = config()
