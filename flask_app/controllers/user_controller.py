from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask import flash

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


# home page with a register form and a login form 
@app.route('/')
def index():
    return render_template("index.html")



# here we have the registration post method route. the if statement uses a User class method to check 
# the form to see if the user inputs are acceptable. If they are acceptable the pw_hash encrypts the password,
# and the following dictionary requests the data from the form to then send to the database with the 
# User class method called save. On success, it redirects to the new user's page (this last part needs implemented still)  
@app.route('/register_new_user', methods=['POST'])
def register_new_user():
    if User.is_valid(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "confirm_password" : request.form['confirm_password']
    }
        User.save(user_data)
        session['user_id'] = user_data.id
        return redirect('/user_page')
    return redirect('/')


#individual user pages (need to add ID)
@app.route('/user_page')
def user_page():
    if 'user_id' in session:
        print("this is line 43", session['user_id'])
        # user_id = session['user_id']
        data = {'user_id': session['user_id']}
        print("this is line 46", data["user_id"])
        current_user = User.get_user_by_id(data)
        return render_template("user_page.html", current_user = current_user)
    else: return redirect('/')


@app.route('/login',methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user_in_db = User.check_database(data)
    if not user_in_db:
        flash("invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/user_page')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')