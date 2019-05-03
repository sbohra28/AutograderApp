# Run with command "python app.py"
# Will reload on save

from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/AutoGrader"
mongo = PyMongo(app)

app.secret_key = os.urandom(24);
print(app.secret_key)

#routing for the main page
@app.route('/')
def main():
    return render_template('pages/main.html')

#routing for the login page
@app.route('/login')
def login():
    return render_template('pages/login.html', error="")

#check the login request
@app.route('/login', methods=["POST"])
def validateLogin():
    #redirect as post
    user = mongo.db.User.find_one({'emailAddress' : request.form['email']})
    if user != None and user['password'] == request.form['password']:
        session['user'] = str(user['_id'])
        session['type'] = user['type']
        print(session)
        return redirect(url_for('dashboard'), code=307)
    return render_template('pages/login.html', error="error")

@app.route('/signup', methods=["POST"])
def createUser():
    print(request.form)
    type = 'student'
    if(len(request.form.getlist('type')) < 1):
        type = 'professor'
    error = mongo.db.User.insert_one({
        'name' : request.form['name'],
        'classes' : [],
        'type' : type,
        'emailAddress' : request.form['email'],
        'password' : request.form['password']
    })
    print(error)
    return redirect(url_for('login'))

#routing for the dashboard
@app.route('/dashboard', methods=["POST"])
def dashboard():
    if(session['type'] == 'student'):
        return render_template('pages/dashboard.html')
    else:
        return render_template('pages/dashboardProfessor.html')

@app.route('/assignment', methods=["POST"])
def assignment():
    return render_template('pages/assignment.html')

@app.route('/class', methods=["POST"])
def classPage():
    return render_template('pages/class.html')

@app.route('/create', methods=["POST"])
def create():
    return render_template('pages/create.html')

@app.route('/signout', methods=["POST"])
def signOut():
    #redirect as post
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
