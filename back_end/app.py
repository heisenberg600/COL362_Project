from crypt import methods
from multiprocessing import connection
from flask import Flask, request, render_template, url_for, flash, redirect
import psycopg2 as psql
from form import Finder, LoginForm

SECRET_KEY = 'development'
APP_SETTINGS = "config.DevelopmentConfig"
DATABASE_URL = "postgresql://postgres:1234@localhost/xyz"

connection = psql.connect(user="python", password='python', host="localhost",
                          port="5432",
                          database="dbpython")
app = Flask(__name__, static_folder='./templates')
app.config.from_object(APP_SETTINGS)


class user():
    def __innit__(self, firstname, lastname, username, password, priviledge):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.priviledge = priviledge


@app.route('/')
def home():
    return render_template('home.html', title="Home Page")


@app.route("/explore", methods=['GET', 'POST'])
def explore():
    form = Finder()
    lattitude = form.lattitude.data
    longitude = form.longitude.data
    if request.method == 'POST':
        if (lattitude == None or longitude == None or lattitude < -90 or longitude > 90 or longitude < -180 or longitude > 180):
            flash('Enter correct values')
        cursor = connection.cursor()
        query = "select * from userdetails limit 10"
        cursor.execute(query)
        restaurants = cursor.fetchall()
        if len(restaurants) != 0:
            return redirect(url_for('explore', restaurants=restaurants))
        flash('Sorry could not find any restaurants near your :(')
    return render_template('explore.html', title="Explore Page", form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    username = form.username.data
    password = form.username.data
    if request.method == 'POST':
        cursor = connection.cursor()
        query1 = ""
        cursor.execute(query1)
        user = cursor.fetchall()
        if len(user) == 0:
            query2 = ""
            cursor.execute(query2)
            user = cursor.fetchall()
            if len(user == 0):
                flash('Incorrect Username')
            else:
                flash('Incorrect Password')
        else:


if __name__ == '__main__':
    app.run()
    connection.close()
