from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# the User class holds all the data stored in our users table in the db
class User:
    def __init__(self, data):
            self.id = data["id"]
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.password = data["password"]
            self.created_at = data["created_at"]
            self.updated_at = data["updated_at"]
            

    @classmethod
    def check_database(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        
        result = connectToMySQL("login_and_registration_db").query_db(query, data)
        
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL("login_and_registration_db").query_db(query,data)
        return cls(result[0])


#the save_user class method 
    @classmethod
    def save(cls,data):
        query = "INSERT into users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('login_and_registration_db').query_db(query,data)
         
    @classmethod
    def check_password(cls, data):
        query = "SELECT password FROM users WHERE email = %(email)s"
        
        results = connectToMySQL("login_and_registration_db").query_db(query, data)
        
        return results
    


    @staticmethod
    def is_valid(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "registration")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "registration")
            is_valid = False
        if len(user['email']) < 5:
            flash("email must be at least 5 characters.", "registration")
            is_valid = False

#password validations
        if len(user['password']) < 5:
            flash("Password must be at least 5 characters.", "registration")
            is_valid = False
        if(re.search('[0-9]', user['password']) == None ):
            flash("Password must include a number", "registration")
            is_valid = False
         
        if(re.search('[A-Z]', user['password']) == None ):
            flash("Password must include an upper case letter", "registration")
            is_valid = False
                      
        if (user['password'] != user['confirm_password']):
            flash("Passwords do not match!", "registration")
            is_valid = False
        #after checking all the above ifs return is_valid
    

        if not EMAIL_REGEX.match(user['email']): 
            flash("Please enter a valid email address.", "registration")
            is_valid = False

        if (re.fullmatch(EMAIL_REGEX, user['email'])):
            this_user = {'email': user['email']}
            results = User.check_database(this_user)
            if len(results) != 0:
                flash('There is an existing account associated with this email address; please login.', "registration")
                is_valid = False


        return is_valid