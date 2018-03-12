from flask import Flask, render_template, redirect, url_for, request
from models import User
from flask_login import LoginManager, login_required, login_user, logout_user


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
@login_required
def index():
    return "Hello World!"


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.get(request.form['email'])
        login_user(user)

        redirect('index')
    
    return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login/')

if __name__ == "__main__":
    app.run(debug=True)