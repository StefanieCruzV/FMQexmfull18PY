from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Shows_only:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network= data['network']
        self.date = data['date']
        self.description= data['description']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
      
    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows  WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        result= connectToMySQL('exam').query_db(query, data)
        print(result)
        single_show= cls(result[0]) 
        print("single show------")
        print(single_show)
        return single_show
    
    @classmethod
    def update_show_by_id(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, date= %(date)s, description = %(description)s, updated_at = now() WHERE id = %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        return   connectToMySQL('exam').query_db(query, data)

    @classmethod
    def dele_show_by_id(cls, data):
        query = "DELETE FROM shows WHERE id= %(id)s"
        # los nombres deben ser los de la bd / los valores los del html
        return  connectToMySQL('exam').query_db(query, data)