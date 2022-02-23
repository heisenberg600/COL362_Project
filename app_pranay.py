from sqlite3 import Cursor
from form_pranay import LoginForm
from flask import Flask, request, session, jsonify, render_template, url_for, flash, redirect
from query import Query

query = Query(cursor)

def CheckName(username):
    username = username.lower()
    #Could create an index over here (Not sure how feasible)
    tables = query.select(['id'],['persons'],f'username = {username}')
    if(len(tables)!=0):
        return True
    return False

def Validate(username, password):
    username = username.lower()
    #Could create an index over here (Not sure how feasible)
    tables = query.select(['id'],['persons'],f'username = {username} and password = {password}')
    if(len(tables)!=0):
        return True
    return False

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    #stringvalue -> see if it is required or not for Forgot Password and SignUp
    username = form.username.data
    password = form.password.data

    if request.method == 'POST' and Validate(username, password) and CheckName(username):
        obj.login()
    	obj.set_id(userid)
    	return redirect(url_for('search_form'))
    elif request.method=='POST' and not CheckName(username):
        flash("Username not found")
    elif request.method=='POST' and not Validate(username, password):
        flash("Password mismatch")

    return render_template('login.html', title = 'Login', form = form)

@app.route('/signup', methods=['POST','GET'])
def signup():
    form = LoginForm()
    #stringvalue -> see if it is required or not for Forgot Password and SignUp
    username = form.username.data
    password = form.password.data

    if request.method == 'POST' and Validate(username, password) and CheckName(username):
        obj.login()
    	obj.set_id(userid)
    	return redirect(url_for('search_form'))
    elif request.method=='POST' and not CheckName(username):
        flash("Username not found")
    elif request.method=='POST' and not Validate(username, password):
        flash("Password mismatch")

    return render_template('login.html', title = 'Login', form = form)


