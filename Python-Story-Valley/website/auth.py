from flask import Blueprint, flash, redirect, render_template, request, session, url_for
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
            return render_template("home.html")
        
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
            return render_template("adminpanel-users.html")
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
        render_template("login.html") 
        return createUser
    return render_template("login.html") 

@auth.route('/logout')
def logout():
    session.pop("Student", None)
    session.pop("Teacher", None)
    session.pop("Admin", None)
    return render_template("login.html") 

@auth.route('/categories')
def categories():
    return render_template("categories.html") 

@auth.route('/articleuploader')
def articleuploader():
    if "Teacher" in session:        
        database = './website/sqlitedb.db'
        conn = connect(database)
        return render_template("articleuploader.html")     
    else:
        return render_template("login.html") 
    
@auth.route('/articleadd', methods=['GET','POST'])
def articleadd():
    if "Teacher" in session or "Admin" in session:        
        database = './website/sqlitedb.db'
        conn = connect(database)
        
        if request.form.get('addarticle') is not None:
            name = request.form.get("name)")
            category = request.form.get('category')
            details = request.form.get('details')
            coverurl = request.form.get('coverurl')
            createarticle = conn.execute("""INSERT INTO articles(name,category,details,coverurl)VALUES (?,?,?,?)""",(name,category,details,coverurl)) 
            conn.commit()
            return createarticle
        
        return render_template("articleuploader.html")     
    else:
        return render_template("login.html") 

@auth.route('/useradd', methods=['GET','POST'])
def useradd():
    if "Teacher" in session or "Admin" in session:        
        database = './website/sqlitedb.db'
        conn = connect(database)
        
        if request.form.get('addarticle') is not None:
            name = request.form.get('name')
            password = request.form.get('password')
            email = request.form.get('email')
            account = request.form.get('account')
            createuser = conn.execute("""INSERT INTO users(name,password,email,account)VALUES (?,?,?,?)""",(name, password, email, account,)) 
            conn.commit()
            return createuser
        
        return render_template("articleuploader.html")     
    else:
        return render_template("login.html") 


@auth.route('/adminpanel-users')
def adminpanelusers():
    if "Admin" in session:        
        database = './website/sqlitedb.db'
        conn = connect(database)
        return render_template("adminpanel-articles.html") 
    else: 
        return render_template("login.html")
@auth.route('/adminpanel-articles')

def adminpanelarticles():
    if "Admin" in session:        
        database = './website/sqlitedb.db'
        conn = connect(database)
        return render_template("adminpanel-articles.html") 
    else: 
        return render_template("login.html") 
