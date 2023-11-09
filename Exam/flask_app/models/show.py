from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Shows:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.title = data['title']
        self.network= data['network']
        self.date = data['date']
        self.description= data['description']
        self.id_show = data['id_show']
      

    @classmethod
    def get_all_shows(cls):
        query = "SELECT  user.id , shows.id as id_show , user.first_name ,user.last_name, shows.title ,shows.network,shows.date,  shows.description FROM user  JOIN shows ON shows.user_id = user.id;"
        # los nombres deben ser los de la bd / los valores los del html
        results = connectToMySQL('exam').query_db(query)
        print("-----")
        print(results)
        shows = []
        # crea arreglo para guiardar los valores 
        for show in results: #itera los nombres de la base de datos 
            data = {
                "id" : show["id"],
                "first_name" : show["first_name"],
                "last_name" : show["last_name"],
                "title" : show["title"],
                "network" : show["network"],
                "date" : show["date"],
                "description" : show["description"],
                "id_show" : show["id_show"]
                }
            shows.append(cls(show))
        
            # flos mete en el arreglo -y los convierte en una clkase ususario
        return shows


    @staticmethod
    def validate_show(data):
        is_valid = True
        if  len(data['title']) < 3 or len(data['title']) == 0 :
            flash("Title must be at least characters .")
            is_valid = False
        if  len(data['network']) < 3 or len(data['title']) == 0 :
            flash("Network must be at least characters .")
            is_valid = False
        if  len(data['description']) < 3 or len(data['title']) == 0 :
            flash("Description must be at least characters .")
            is_valid = False
        if  len(data['date'])== 0 :
            flash("Must need a date.")
            is_valid = False
        return is_valid
        

    @classmethod
    def save(cls, data):
        query = " INSERT INTO  shows (title, network, description,date, created_at, updated_at, user_id) VALUES ( %(title)s , %(network)s,  %(description)s, %(date)s, NOW() , NOW(),%(user_id)s);"
        # los nombres deben ser los de la bd / los valores los del html
        new_show_id= connectToMySQL('exam').query_db(query, data)
        print(new_show_id)
        return 

  