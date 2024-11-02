# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://amit:<Amit2003@#>@localhost/inventory_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
