import  os
DEBUG = True
SECRET_KEY = os.urandom(24)

dialect='mysql'
driver='pymysql'
username='root'
password='123'
host='127.0.0.1'
port='3306'
database='test'
SQLALCHEMY_DATABASE_URI= f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS=False