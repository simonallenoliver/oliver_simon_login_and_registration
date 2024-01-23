from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

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
    def save(cls,data):
        query = "INSERT into surveys (name,location,language,comments) VALUES (%(name)s,%(location)s,%(language)s,%(comments)s);"
        return connectToMySQL('login_and_registration_db').query_db(query,data)
         


    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        return is_valid