from flask import Flask,render_template,request,redirect,url_for,session
import  config
from models import User,Question,Answer
from exts import db
from decorator import login_limit

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context={
        'questions':Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template("index.html",**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username=request.form.get('username')
        userpdw=request.form.get('password')
        user = User.query.filter(User.username==username,User.userpdw==userpdw).first()
        if user:
            session['user_id']=user.id
            session.permenent=True
            return redirect(url_for('index'))
        else:
            return '用户名或密码错误！'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template("regist.html")
    else:
        username = request.form.get('username')
        telephone = request.form.get('phone')
        userpdw1 = request.form.get('password1')
        userpdw2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机号码已被注册，请更换手机号码！"
        else:
            if userpdw1 != userpdw2:
                return "两次输入的密码不一致，请重新输入！"
            else:
                user = User(username=username, telephone=telephone, userpdw=userpdw1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_limit
def question():
    if request.method == 'GET':
        return  render_template("question.html")
        #return render_template(url_for('question'))
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        if title:
            if content:
                question=Question(title=title,content=content)
                user_id=session.get("user_id")
                user= User.query.filter(User.id==user_id).first()
                question.author=user
                db.session.add(question)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                return "内容不能为空"
        else:
            return "标题不能为空"

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    answer_count=Answer.query.filter(Answer.question_id==question_model.id).count()
    return render_template("detail.html",question=question_model,answer_count=answer_count)

@app.route('/answer/',methods=['POST'])
@login_limit
def answer():
    answer_content=request.form.get('answer-content')
    if answer_content:
        question_id=request.form.get('question_id')
        answer=Answer(content=answer_content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()
        answer.author=user
        question=Question.query.filter(Question.id==question_id).first()
        answer.question=question
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail',question_id=question_id))
    else:
        return "评论不能为空"


@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return {'user':user}
    else:
        return {}

if __name__ == '__main__':
    app.run()
