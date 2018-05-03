import os
import config
from datetime import datetime
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)
app.config.from_object(config)

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))

#forms
class NameForm(FlaskForm):
    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')

#database
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


'''
@app.route('/',methods=['GET','POST'])

def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
    return render_template('index.html',form=form,name=name)
'''
#重定向
'''
@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        session['name']=form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))
'''

#flash
'''
@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you have changed your name!')
        session['name']=form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))
'''

#数据库
@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))

@app.route('/time/')
def time():
    return render_template('time.html',current_time=datetime.utcnow())

@app.route('/user/<int:id>')
def user1(id):
    return '<h1>Hello,%s!</h1>'%id

@app.route('/user/<name>')
def user2(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    manager.run()
