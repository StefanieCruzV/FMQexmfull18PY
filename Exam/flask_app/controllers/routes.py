from cgi import print_form
from crypt import methods
import re
from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.show import Shows
from flask_app.models.showonly import Shows_only
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    return render_template("login.html") 

@app.route("/register", methods=["POST"])
def register():   
    if not User.validate_user(request.form): # is la validacion es falso mandamos a index
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # crear Hash del password
    print(pw_hash)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    } 
    # print(request.form)
    this_user = User.find_the_email(data)
    if  this_user: # if the query return  o == falrse
        flash("email is already use!")
        return redirect("/")


    use_id= User.save(data)
    session['logged_id'] = use_id
    return redirect("/success")


@app.route("/success")
def success():
    if"logged_id" not in session:
        return redirect("/")
    data ={
        "id" : session['logged_id']
    }
    loged_user= User.user_by_id(data)

    shows =Shows.get_all_shows()


    # return f"you are logged in as user # {session['logged_id']} !"
    return render_template("showshows.html",loged_user=loged_user,shows=shows) 


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#----------------------------------------------------registration


@app.route('/login', methods=["POST"])
def login():
    data ={
        "email" : request.form["email"]
    }
    this_user = User.find_the_email(data)
    if not this_user: # if the query return  o == falrse
        flash("invalid email/password")
        return redirect("/")
    #if user exist
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("password is wrong")
        return redirect("/")
    #-chec and cpompare the password

    session['logged_id']= this_user.id
 
    return redirect("/success")

#----------------------------------------------------loggin

@app.route('/create')
def create():
    if"logged_id" not in session:
        return redirect("/")

    return render_template("addnewshow.html") 


@app.route('/create_show', methods=["POST"])
def create_recipe():
    print(request.form)
    data = {
    "title": request.form["title"],
    "network": request.form["network"],
    "date": request.form["date"],
    "description": request.form["description"],
    "user_id":  session['logged_id']
    }
    # print("+++++=================")
    print(data)
    # shows = Shows.validate_show(data)
    if not Shows.validate_show(data): # is la validacion es falso mandamos a index
        return redirect('/create')
    
    this_show = Shows.save(data)
 
    return redirect('/success')
#----------------------------------------------------CREATE

@app.route('/update_show/<int:id>')
def update_show(id):
    if"logged_id" not in session:
        return redirect("/")
   
    data = {
        "id": id,
        }
    print(id)
    show = Shows_only.get_show_by_id(data)
    print(show)
    return render_template("editeshow.html", show=show) 

@app.route('/send_update_show', methods=["POST"])
def send_update_show():
    if"logged_id" not in session:
        return redirect("/")
    print(request.form)
    data = {
        "id":request.form["show_id"],
        "title": request.form["title"],
        "network": request.form["network"],
        "date": request.form["date"],
        "description": request.form["description"]
    }
    Shows_only.update_show_by_id(data)
    return redirect('/success')
#----------------------------------------------------Update

@app.route('/delete_show/<int:id>')
def delete_show(id):
    if"logged_id" not in session:
        return redirect("/")
    print(id)
    data = {
        "id": id
        }
    Shows_only.dele_show_by_id(data)
    return redirect('/success')
#----------------------------------------------------Delete

@app.route('/show_show/<int:id>')
def show_show(id):
    if"logged_id" not in session:
        return redirect("/")
    data ={
        "id" : session['logged_id']
    }
    loged_user= User.user_by_id(data)
    print(id)
    data = {
        "id": id
        }
    show =  Shows_only.get_show_by_id(data)
    data_user={
        "id": show.user_id
        }
    creator_show=User.user_by_id(data_user)
    return render_template("oneshow.html",show=show,loged_user=loged_user,creator_show=creator_show) 

#----------------------------------------------------Show