from flask import Blueprint, render_template, request, session
import sqlite3
from sqlite3 import connect


auth = Blueprint('auth', __name__)

def usersdb():
    database = './website/sqlitedb.db'
    conn = connect(database)
    c = conn.cursor()
    createUsers = conn.execute('''CREATE TABLE IF NOT EXISTS users (userid INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, account INTEGER NOT NULL);''')
    return createUsers
    

def articlesdb():
    database = './website/sqlitedb.db'
    conn = connect(database)
    c = conn.cursor()
    createArticles = conn.execute('''CREATE TABLE IF NOT EXISTS articles (articleid INTEGER NOT NULL PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, details TEXT NOT NULL, coverurl TEXT NOT NULL);''')
    return createArticles

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST" and request.form.get('loginForm') is not None: 
        database = './website/sqlitedb.db'
        conn = connect(database)
        c = conn.cursor()
        name = request.form.get('name')
        password = request.form.get('password')
        print(name,password)
        
        loginQueryStudent = "SELECT name,password,account FROM users WHERE name ='"+name+"' AND password ='"+password+"' AND account = 0"
        c.execute(loginQueryStudent)
        resultsQueryStudent = c.fetchall()

        loginQueryTeacher = "SELECT name,password,account FROM users WHERE name ='"+name+"' AND password ='"+password+"' AND account = 1"
        c.execute(loginQueryTeacher)
        resultsQueryTeacher = c.fetchall()

        loginQueryAdmin = "SELECT name,password,account FROM users WHERE name ='"+name+"' AND password ='"+password+"' AND account = 2"
        c.execute(loginQueryAdmin)
        resultsQueryAdmin = c.fetchall()

        
        if len(resultsQueryStudent) == 1:
            print("login query found a student user called '"+name+"")
            loginStudentQuery = "SELECT name,password FROM users WHERE account = 0"
            c.execute(loginStudentQuery)
            user = request.form["loginForm"]
            session["Student"] = user
        
        elif len(resultsQueryTeacher) == 1:
            print("login query found a teacher user called '"+name+"")
            loginStudentQuery = "SELECT name,password FROM users WHERE account = 0"
            c.execute(loginStudentQuery)
            user = request.form["loginForm"]
            session["Teacher"] = user
            return render_template("home.html")
        
        elif len(resultsQueryAdmin) == 1:
            print("login query found an admin user called '"+name+"")
            loginStudentQuery = "SELECT name,password FROM users WHERE account = 0"
            c.execute(loginStudentQuery)
            user = request.form["loginForm"]
            session["Admin"] = user
            
        elif "logoutButton" in request.GET:
            print("session deleted")
            
        else:
            print("login query did not find the user")
        
    elif request.method == "POST" and request.form.get('registerForm') is not None:
        database = './website/sqlitedb.db'
        conn = connect(database)
        c = conn.cursor()
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        account = request.form.get('account')
        print(name,password,email,account) 
        
        
        existingUserSearchQuery = "SELECT * FROM users WHERE password == 'Student'"
        createUser = conn.execute("""INSERT INTO users(name,password,email,account)VALUES (?,?,?,?)""",(name, password, email, account,)) 
        conn.commit()
        return createUser
        #if len(existingUserSearchQuery) < 1:
        
    return render_template("login.html") 


