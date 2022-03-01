from crypt import methods
from multiprocessing import Condition, connection
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_login import current_user
from matplotlib.pyplot import title
import psycopg2 as psql
from form import Finder, LoginForm, SignUpForm
from query import Query
import folium

SECRET_KEY = 'development'
APP_SETTINGS = "config.DevelopmentConfig"
DATABASE_URL = "postgresql://postgres:1234@localhost/xyz"

connection = psql.connect(
                user="pranay", 
                password="qwerty", 
                host="localhost",
                port="5432",
                database="project")

to_cursor = connection.cursor()
query = Query(to_cursor)

app = Flask(__name__)
app.config.from_object(APP_SETTINGS)


class User():
    def __init__(self, login, data):
        self.login = login
        self.data= data


    def setData(self, username):
        uData = query.select(['*'],['persons'],f"username = '{username}'")[0]
        uData = {query.cols[i]:uData[i] for i in range(len(uData))}
        if(uData['priviledge'] ==1):
            rData = query.select(['*'],['managersView'],f"id = '{uData['id']}'")[0]
            rData = {query.cols[i]:rData[i] for i in range(len(rData))}
            self.rdata = rData 
        self.data = uData

    def setDataByID(self, id):
        uData = query.select(['*'],['persons'],f"id = '{id}'")[0]
        uData = {query.cols[i]:uData[i] for i in range(len(uData))}
        if(uData['priviledge'] ==1):
            rData = query.select(['*'],['managersView'],f"id = '{uData['id']}'")[0]
            rData = {query.cols[i]:rData[i] for i in range(len(rData))}
            self.rdata = rData 
        self.data = uData

    def update(self, data):
        changed = {}
        if(self.level() == 2):
            prev = self.data
            table = 'persons'
        else:
            prev = self.rdata
            table = 'managersView'
        for i in data:
            val = data[i]
            if(type(val) != type(prev[i])):
                if(prev[i] == None):
                    if(val == 'None'):
                        val = None
                else:
                    val = type(prev[i])(val)

            if(val == None):return -1
            if(prev[i] != val):
                changed[i] = val

        query.update(table, changed, f"id = {self.data['id']} ")
        self.setDataByID(self.data['id'])
        return 0
        
    def level(self):
        return self.data['priviledge']

    def getdata(self):
        if(self.level() == 1):
            return self.rdata
        return self.data

    def loggedin(self):
        self.login = True
    
    def loggedout(self):
        self.login = False
    
    def is_login(self):
        return self.login

    
user = User(False, {})


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home Page")

def refresh():
    user = User(False, {})
    return home()

@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
    name = request.form.get("user_name")
    return render_template('thanks.html', title="Thanks", name = name)

def available_username(username):
    cur_rows = query.select(['username'], ['persons'], f"username= '{username}'")
    if(len(cur_rows)!=0):
        return False
    return True


def convert(input_val):
    return input_val=="on"

def addUser(username, password, firstname, lastname, gender, dob, level):
    if (available_username(username)):
    #     cur_query = query.select([''])
        
        
        len_id_query = query.select(['username'], ['persons']) 
        cur_id = len(len_id_query)+1
        gender = gender.lower()
        
        query.insert('persons(id,firstname,lastname,gender,phone,email,username,password,dob,priviledge)', [f"'{cur_id}'", f"'{firstname}'", f"'{lastname}'", f"'{gender}'", "'NULL'", "'NULL'", f"'{username}'",f"'{password}'", f"'{dob}'", "2"])
        return (0,'')
    else: 
        return (-1, 'username already taken')
        
def check_username_password(username, password):
    cur_rows = query.select(['username'], ['persons'], f"username= '{username}' and password = '{password}'")
    if(len(cur_rows)==0):
        return False
    return True

def loginUser(username, password):

    if(available_username(username)==True):
        # return(-1, 'username does not exist')
        return render_template('login.html', title= 'Login', error = 'username does not exist')
    elif(check_username_password(username, password)== False):
        return render_template('login.html', title= 'Login', error = 'username and password do not match')
    else:
        user.login = True
        user.setData(username)
        # user.set_everything(True, 2, password, username, cur_info[1])
        return render_template('restaurants.html', title='Restaurants', name=username)
    # return render_template('thanks.html', title='Thanks', name=username)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed = request.form.get("confirmed")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        gender = request.form.get("Gender")
        dob = request.form.get("dob")

        # set level accordingly
        current_details = addUser(username, password, firstname, lastname, gender, dob, 0)
        if(current_details[0] == -1):
           return render_template('signup.html', title="Signup", error = current_details[1])
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
        # elif(username != password):
        #     error = 'Invalid username or password'
        if(error != None):
            return render_template('login.html', title="Login", error = error, username=username)
        else:
            # set level to what got from database
            return loginUser(username, password)

    return render_template('login.html', title="Login")


@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if(request.method == 'POST'):
        distMin = request.form.get('distMin')
        # if(distMin==""):
        #     distmin = f" distance>0 "
        # else:
        #     distmin = f" distance>{distMin} "
        distMax = request.form.get('distMax')
        # if(distMax==""):
        #     distMax = f" and distance<1000000 "
        # else:
        #     distMax = f" and distance<{distMax} "
        ratingMin = request.form.get('ratingMin')
        if(ratingMin==""):
            ratingMin = f" restaurants.avgReview>0 "
        else:
            ratingMin = f" restaurants.avgReview>{ratingMin} "
        ratingMax = request.form.get('ratingMax')
        if(ratingMax==""):
            ratingMax = f" and restaurants.avgReview<1000000 "
        else:
            ratingMax = f" and restaurants.avgReview<{ratingMax} "
        
        createdMin = request.form.get('createdMin')
        if(createdMin==""):
            createdMin = " and restaurants.dateAdded>'1900-01-01'"
        else:
            createdMin = f" and restaurants.dateAdded>'{createdMin}' "
        createdMax = request.form.get('createdMax')
        if(createdMax==""):
            createdMax = f" and restaurants.dateAdded<'2100-01-01' "
        else:
            createdMax = f" and restaurants.dateAdded<'{createdMax}' "
        priceMin = request.form.get('priceMin')
        if(priceMin==""):
            priceMin = f" and restaurants.priceRangeAvg>0 "
        else:
            priceMin = f" and restaurants.priceRangeAvg>{priceMin} "

        priceMax = request.form.get('priceMax')
        if(priceMax==""):
            priceMax = f" and restaurants.priceRangeAvg<10000000 "
        else:
            priceMax = f" and restaurants.priceRangeAvg<{priceMax} "
        city = request.form.get('city')
        if(city!=""):
            city = f"and cities.city='{city}'"
        province = request.form.get('province')
        if(province!=""):
            province = f"and province.name='{province}'"
        # country = request.form.get('country')



        columns = ""
        check_restaurant = False
        check_city_province = False

        resID = convert(request.form.get('resID'))
        if(resID):
            columns+="restaurants.restId, "
            
        name = convert(request.form.get('name'))
        if(name):
            columns+="restaurants.name, "
            
        phoneNumber = convert(request.form.get('phoneNumber'))
        if(phoneNumber):
            columns+="restaurants.phoneNo, "
            
        city_check = convert(request.form.get('city_check'))
        if(city_check):
            columns+="cities.city, "
            
        # country = convert(request.form.get('country'))
        province_check = convert(request.form.get('province_check'))
        if(province_check):
            columns+="province.name, "
            
        postalCode = convert(request.form.get('postalCode'))
        if(postalCode):
            columns+= "restaurants.postalCode, "
            
        latitude = convert(request.form.get('latitude'))
        if(latitude):
            columns+= "restaurants.latitude, "
            
        longitude = convert(request.form.get('longitude'))
        if(longitude):
            columns+= "restaurants.longitude, "
            
        avgPrice = convert(request.form.get('avgPrice'))
        if(avgPrice):
            columns+= "restaurants.priceRangeAvg, "
            
        avgRating = convert(request.form.get('avgRating'))
        if(avgRating):
            columns+= "restaurants.avgReview, "
            
        created = convert(request.form.get('created'))
        if(created):
            columns+= "restaurants.dateAdded, "
            
        url = convert(request.form.get('url'))
        if(url):
            columns+= "restaurant.websites, "
            

        num = request.form.get('num')
        if(num==""):
            num= "10"
        order = request.form.get('order')
        if(order=="least"):
            order = "ASC"
        else:
            order = "DESC"
        val = request.form.get('val')

        if(val=="number" or val=="price"):
            val= "restaurants.pricerangeAvg"

        if(val=="rating"):
            val="restaurants.avgReview"
        
        if(val=="reviewCount"):
            val= "restaurants.num_reviews"
        
        if(val=="created"):
            val= "restaurants.dateAdded"

        
        # if(val=="")


        columns = columns[:-2]

        print(order, val)
        
            
        cur_query = f"select {columns} from restaurants, province, cities where {ratingMin} {ratingMax} {createdMin} {createdMax} {priceMin} {priceMax} {city} {province} and restaurants.cityId=cities.cityId and cities.province = province.provinceId order by {val} {order} limit {num} "

        to_cursor.execute(cur_query)
        ans = to_cursor.fetchall()

        cols = [i.split('.')[-1] for i in columns.split(", ")]
        print(ans)
        return render_template('restaurants.html', title="Filter", rows=ans, cols = cols)

        # print(distMin, resID, num, order, val, city_check, province_check)


    return render_template('restaurants.html', title="Filter")

@app.route('/update', methods=['GET', 'POST'])
def update():
    if(user.login):
        if(request.method == 'POST'):
            data = request.form.to_dict()
            user.update(data)
        pages = ['update_admin.html','update_manager.html','update_user.html']
        return render_template(pages[user.level()], title="Update", data = user.getdata())
    else:return refresh()

def changeRest(site, title, data):

    if(data.get('restSelected') != None):
        rest_id = data.get('restSelected')
        return render_template(site, title=title, rest_id = rest_id)   

    elif(data.get('mode') != None):
        mode = data.get('mode')
        error = "" 

        if(mode == 'byresid'):
            rest_id = data.get('resID')
        elif(mode == 'byphone'):
            ans = query.select(['restId'], ['restaurants'], f"phoneNo = '{data.get('phone')}'")
            if(len(ans) > 0 and len(ans[0]) > 0):
                rest_id = ans[0][0]
            else:
                error = "No restaurant found with this phone number"
        elif(mode == 'bycoord'):

            ans = query.select(['restId'], ['restaurants'], f"latitude = '{data.get('lat')}' and longitude = '{data.get('long')}'")
            if(len(ans) > 0 and len(ans[0]) > 0):
                rest_id = ans[0][0]
            else:
                error = "No restaurant found with this coordinates"
        if(error != ""):
            return render_template(site, title=title, error = error)

        return render_template(site, title=title, rest_id = rest_id)
    

@app.route('/review', methods=['GET', 'POST'])
def review():
    if(request.method == 'POST'):
        data = request.form.to_dict()
        if(data.get('restS') != None):
            rest_id = data.get('restS')
            stars = data.get('stars')
            query.insert('reviews',[f'{user.data["id"]}',f'{rest_id}',f'{stars}'])
        else: return changeRest('review.html', 'Review', data)

    return render_template('review.html', title="Review")

@app.route('/locate', methods=['GET', 'POST'])
def locate():
    if(request.method == 'POST'):
        data = request.form.to_dict()
        changed = changeRest('locate.html', 'Locate', data)
        if(changed == None):
            rest_id = data.get('restS')
            ans = query.select(['latitude','longitude','name'], ['restaurants'],f'restId = {rest_id}')[0]
            coord = list(map(float,ans[:-1]))
            onmap = folium.Map(
                location=coord,
                titles='Restaurant Plotted',
                zoom_start=12
            )

            folium.Marker(
                location=coord,
                popup=ans[-1],
                tooltip='Click Here'
            ).add_to(onmap)

            return onmap._repr_html_()

        else: return changed 
    return render_template('locate.html', title="Locate")


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
