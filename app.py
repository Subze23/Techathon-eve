import re
import random
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQL_ROOT_PASSWORD@127.0.0.1:9906/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '200701267@rajalakshmi.edu.in'#'myemail@id.com'
app.config['MAIL_PASSWORD'] = '(@Im_In_R3C_CS3!)'#'emailpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

class Users(db.Model):
    uid = db.Column("id", db.Integer, primary_key=True)
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

@app.errorhandler(404)
def page_not_found(e):
    return '''<h2>Uhuh!! There's really nothing here</h2>
                <p>Goto <a href="/signup">Signup</a> Page</p>
        ''', 404

@app.route('/signup', methods=["POST", "GET"])
def signup_page():
    if ( 'user' in session ): return redirect('/home')
    if ( request.method == "POST" ):
        email = request.form['email']
        if ( re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) ):
            session['new_user'] = Users(request.form['username'], email, request.form['password'])
            session['otp'] = send_otp(email)
            return redirect('/verify-email')
        #return '<h2>Success!!!</h2>'    
        #time.sleep(3)
    return render_template("signup.html")

@app.route('/verify-email', methods=["POST", "GET"])
def verify_email_page():
    if ( 'user' in session ): return redirect('/home')
    if ( request.method == "GET" ): return render_template("verify_email.html")
    if ( request.method == "POST" ):
        if ( session['otp'] == int(request.form['otp']) ):
            db.session.add(session['new_user'])
            db.session.commit()
            return redirect('/login')
        return ('', 204)

@app.route('/login', methods=["POST", "GET"])
def login_page():
    if ( 'user' in session ): return redirect('/home')
    if ( request.method == "POST" ):
        user = Users.query.filter_by(username=request.form['username']).first()
        if ( user and user.password == request.form['password'] ):
            session['user'] = user.uid
            return redirect('/home')
    return render_template("login.html")

@app.route('/forgot-password', methods=["POST", "GET"])
def forgot_password_page():
    if ( 'user' in session ): return redirect('/home')
    if ( request.method == "POST" ):
        print(request.form)
        if ( 'tmpusr' not in session ): session['tmpusr'] = Users.query.filter_by(username=request.form['name']).first()
        if ( 'otp' in request.form ):
            #if ( 'tries' not in session ): session['tries'] = 3
            #if ( session['tries'] == 0 ): return render_template("login.html")
            recv_otp = request.form['otp']
            print("RECV_OTP =", recv_otp)
            print("OTP =", session['otp'])
            if ( int(recv_otp) == session['otp'] ):
                session['otpid'] = session['tmpusr'].uid
                return redirect('/reset-password')
            else:
                #session['tries'] -= 1
                return ('', 204)    
        else:
            if ( '@' in request.form['name'] ): 
                email = request.form['name']
            else:
                email = session['tmpusr'].email
            print("BEFORE OTP:",request.form['name'], email)
            if ( 'otp' not in session ):
                session['otp'] = send_otp(email)
            print("OTP =", session['otp'])
            return ('', 204)

        '''return f"<p>HIii</p>"
        if ( re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) ):
            user = Users.query.filter_by(email=request.form['username']).first()
        else:
            pass'''
    else:
        return render_template("forgot.html")

@app.route('/home')
def home_page():
    if ( 'user' not in session ): return redirect('/login')
    return render_template('home.html')

@app.route('/logout')
def logout_page():
    if ( 'user' not in session ): return redirect('/login')
    session.pop('user', None)
    session.pop('otp', None)
    #session.pop('user', None)
    return redirect('/login')

@app.route('/reset-password', methods=["POST", "GET"])
def reset_password_page():
    if ( 'user' in session ): return redirect('/home')
    if ( request.method == "GET" ): return render_template('reset_password.html') 
    if ( request.method == "POST" ):
        user = Users.query.filter_by(uid=session['otpid']).first()
        if ( request.form['password'] == request.form['c-password'] ):
            user.password = request.form['password']
            db.session.commit()
            return redirect('/login')
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

def send_otp(email):
    otp = random.randint(100000, 999999)
    msg = Message(
                'OTP - Tech-A-Thon',
                sender = '200701267@rajalakshmi.edu.in',#'myemail@id.com',
                recipients = [email]#['receivermail@id.com']
               )
    msg.body = 'Hello! A OTP was requested\nThis is your OTP: ' + str(otp) + "\nDo not share with anyone"
    mail.send(msg)
    return otp

app.run(debug=True)