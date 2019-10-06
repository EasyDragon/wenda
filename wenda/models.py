from exts import db
from datetime import datetime

#先打开虚拟环境，再进入该项目目录下执行：python manage.py db migrate和python manage.py db upgrade
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(100),nullable=False)
    userpdw = db.Column(db.String(100),nullable=False)

class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    #不能用now()，不然全部是当前时间
    create_time=db.Column(db.DATETIME,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question', backref=db.backref('answers',order_by=create_time.desc()))
    author = db.relationship('User', backref=db.backref('answers'))