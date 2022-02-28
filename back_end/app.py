from crypt import methods
from multiprocessing import Condition, connection
from flask import Flask, request, render_template, url_for, flash, redirect
from matplotlib.pyplot import title
import psycopg2 as psql
from form import Finder, LoginForm, SignUpForm
from query import Query

SECRET_KEY = 'development'
APP_SETTINGS = "config.DevelopmentConfig"
# DATABASE_URL = "postgresql://postgres:1234@localhost/xyz"

# connection = psql.connect(
#                 user="python", 
#                 password='python', 
#                 host="localhost",
#                 port="5432",
#                 database="dbpython")

app = Flask(__name__)
app.config.from_object(APP_SETTINGS)

# query = Query(curser)

class User():
    def __init__(self, data, level):
        self.data = data
        self.level = level

    def change_username(self, username):
        self.data['username'] = username

    def change_password(self, password):
        self.data['password'] = password

    def change_privildedge(self, priviledge):
        self.data['priviledge'] = priviledge

currUser = None

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home Page")

@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
    name = request.form.get("user_name")
    return render_template('thanks.html', title="Thanks", name = name)


def addUser(username, password, name, gender, dob, level):
    return 0

def loginUser(username, password):
    currUser = User("something", 0)
    return render_template('thanks.html', title='Thanks', name=username)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed = request.form.get("confirmed")
        name = request.form.get("name")
        gender = request.form.get("gender")
        dob = request.form.get("dob")

        print(username, password, confirmed, name, gender, dob)

        # set level accordingly
        if(addUser(username, password, name, gender, dob, 0) == -1):
           return render_template('signup.html', title="Signup", error = "Please Enter Valid details")
        else:
            return loginUser(username, password)

    return render_template('signup.html', title="Signup")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        if (username == "" or password == ""):
            error = "Please enter username and password" 
        # check if user exists and password is correct
        elif(username != password):
            error = 'Invalid username or password'
        
        if(error != None):
            return render_template('login.html', title="Login", error = error, username=username)
        else:
            # set level to what got from database
            return loginUser(username, password)

    return render_template('login.html', title="Login")


@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    return render_template('restaurants.html', title="Filter")

@app.route('/locate', methods=['GET', 'POST'])
def locate():
    return render_template('locate.html', title="Locate")

@app.route('/update_admin', methods=['GET', 'POST'])
def update_admin():
    return render_template('update_admin.html', title="Update")

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    return render_template('update_user.html', title="Update")

@app.route('/update_manager', methods=['GET', 'POST'])
def update_manager():
    return render_template('update_manager.html', title="Update")

@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template('review.html', title="Review")


# @app.route("/explore", methods=['GET', 'POST'])
# def explore():
#     form = Finder()
#     lattitude = form.lattitude.data
#     longitude = form.longitude.data
#     restaurants = []
#     if request.method == 'POST':
#         print(lattitude)
#         print(longitude)
#         if (lattitude == None or longitude == None or lattitude < -90 or longitude > 90 or longitude < -180 or longitude > 180):
#             flash('Enter correct values')
#         cursor = connection.cursor()
#         query = "select * from userdetails limit 10"
#         cursor.execute(query)
#         restaurants = cursor.fetchall()
#         if len(restaurants) == 0:
#             flash('Sorry could not find any restaurants near your :(')
#     return render_template('explore.html', title="Explore Page", form=form, restaurants=restaurants)



if __name__ == '__main__':
    app.run(debug = True)
    connection.close()
