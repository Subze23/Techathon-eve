from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQL_ROOT_PASSWORD@127.0.0.1:9906/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password = "password"

@app.route('/')
def hello_world():
    return '''<h2>Page under construction</h2>
                <p>Goto <a href="/signup">Signup</a> Page</p>
        '''

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/forgot-password')
def forgot_password_page():
    return render_template("forgot.html")

@app.route('/create')
def create():
    john = Users('John Wick', 'john.wick.124@abc.zx')
    db.session.add(john)
    db.session.commit()
    return '<h2>Success!!!</h2>'

app.run(debug=True)