from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
NAME =re.compile(r'^[a-zA-Z ]+$' )
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_user(data):
        is_valid = True
        if not NAME.match(data['first_name']):
            flash("Name must be only characters.")
            is_valid = False
        if  len(data['first_name']) < 2:
            flash("Name must be at least 2 .")
            is_valid = False
        if not NAME.match(data['last_name']):
            flash("Last name must be only characters.")
            is_valid = False
        if  len(data['first_name']) < 2:
            flash("Last ame must be at least 2 .")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) == 0 :
            flash("must ned the password")
            is_valid = False
        if len(data['confirmpassword']) == 0:
            flash("must ned the confirmation")
            is_valid = False
        if data['password'] != data['confirmpassword']:
            flash("Confirmation must match the password")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name , last_name , email , password, created_at, updated_at)  VALUES ( %(first_name)s , %(last_name)s , %(email)s  , %(password)s, now(), now())"
        # los nombres deben ser los de la bd / los valores los del html
        new_user_id=connectToMySQL('exam').query_db(query, data)
        return new_user_id
    
    @classmethod
    def find_the_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s"
        # los nombres deben ser los de la bd / los valores los del html
        result= connectToMySQL('exam').query_db(query, data)
        if len(result) == 0: #si no esta ese email
            return False 
        email = cls(result[0]) 
        return email

    @classmethod
    def user_by_id(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        result= connectToMySQL('exam').query_db(query, data)
        if len(result) == 0: #si no esta ese email
            return False 
        user = cls(result[0]) 
        return user


  