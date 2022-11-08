from flask import Flask, render_template
app = Flask(__name__)

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

app.run(debug=True)