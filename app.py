import config
from datetime import datetime
from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config.from_object(config)

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

class NameForm(Form):
    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')

@app.route('/')
def hello_world():
    return render_template('index.html',current_time=datetime.utcnow())

@app.route('/user/<int:id>')
def index(id):
    return '<h1>Hello,%s!</h1>'%id

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    manager.run()
