from flask import render_template, request, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_new_user', methods=['POST'])
def register_new_user():
    # if there are errors:
    # We call the staticmethod on User model to validate
    if not User.validate_user(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/')
    # else no errors:
    User.save(request.form)
    return redirect("/")