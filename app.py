import re
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQL_ROOT_PASSWORD@127.0.0.1:9906/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'myemail@id.com'
app.config['MAIL_PASSWORD'] = 'emailpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/')
def hello_world():
    return '''<h2>Page under construction</h2>
                <p>Goto <a href="/signup">Signup</a> Page</p>
        '''

@app.route('/signup', methods=["POST", "GET"])
def signup_page():
    if ( request.method == "POST" ):
        email = request.form['email']
        if ( re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) ):
            new_user = Users(request.form['username'], email, request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html")
        #return '<h2>Success!!!</h2>'    
        #time.sleep(3)
    return render_template("signup.html")

@app.route('/login', methods=["POST", "GET"])
def login_page():
    if ( request.method == "POST" ):
        user = Users.query.filter_by(username=request.form['username']).first()
        if ( user and user.password == request.form['password'] ):
            return "<h2>Welcome to Tech-A-Thon!!!</h2>"
    return render_template("login.html")

@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password_page():
    if ( request.method == "POST" ):
        print(request.form)
        return f"<p>HIii</p>"
        if ( re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) ):
            user = Users.query.filter_by(email=request.form['username']).first()
        else:
            pass
    return render_template("forgot.html")

#test
@app.route('/create')
def create():
    john = Users('John Wick', 'john.wick.124@abc.zx')
    db.session.add(john)
    db.session.commit()
    return '<h2>Success!!!</h2>'

#test
@app.route("/mail")
def index():
   msg = Message(
                'Hello',
                sender ='myemail@id.com',
                recipients = ['receivermail@id.com']
               )
   msg.body = 'Hello! Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'

app.run(debug=True)