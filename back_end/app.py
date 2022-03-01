from crypt import methods
from multiprocessing import Condition, connection
from re import A
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
    def __init__(self, login, name, priviledge):
        self.login = login
        self.name = name
        self.data = {}
        self.priviledge = priviledge

    def setData(self, username, level=2):
        if(level == 2):
            uData = query.select(['*'],['persons'],f"username = '{username}'")[0]
            uData = {query.cols[i]:uData[i] for i in range(len(uData))}
        elif(level == 1):
            uData = query.select(['*'],['managers'],f"username = '{username}'")[0]
            uData = {query.cols[i]:uData[i] for i in range(len(uData))}
            rData = query.select(['*'],['managersView'],f"id = '{uData['id']}'")[0]
            rData = {query.cols[i]:rData[i] for i in range(len(rData))}
            self.rdata = rData 
        self.priviledge = level
        self.data = uData
        self.name = uData['username']

    def setDataByID(self, id):
        uData = query.select(['*'],['persons'],f"id = '{id}'")[0]
        uData = {query.cols[i]:uData[i] for i in range(len(uData))}
        if(uData['priviledge'] ==1):
            rData = query.select(['*'],['managersView'],f"id = '{uData['id']}'")[0]
            rData = {query.cols[i]:rData[i] for i in range(len(rData))}
            self.rdata = rData 
        self.data = uData

    def update_u(self, data):
        changed = {}
        prev = self.data
        table = 'persons'
        for i in data:
            val = data[i]
            if(type(val) != type(prev[i])):
                if(prev[i] == None):
                    if(val == 'None'):
                        val = None
                else:
                    val = type(prev[i])(val)

            if(val == None):
                return -1
            if(prev[i] != val):
                changed[i] = val

        query.update(table, changed, f"id = {self.data['id']} ")
        self.setDataByID(self.data['id'])
        return 0

    def update_r(self, data):
        changed = {}
        prev = self.rdata
        table = 'managersView'
        for i in data:
            if(i != 'taco_burrito'):
                val = data[i]
                if(type(val) != type(prev[i])):
                    if(prev[i] == None):
                        if(val == 'None'):
                            val = None
                    else:
                        val = type(prev[i])(val)

                if(val == None):
                    return -1
                changed[i] = val
        if(data.get('taco_burrito') == None):
            changed['taco_burrito'] = 0
        else:
            changed['taco_burrito'] = 1
        curr_query = "select * from cities where city='{}'".format(
            changed['city'])
        to_cursor.execute(curr_query)
        record1 = to_cursor.fetchall()
        curr_query = "select * from province where name='{}'".format(
            changed['pname'])
        to_cursor.execute(curr_query)
        record2 = to_cursor.fetchall()
        if (len(record2) == 0):
            return -1
        flag = False
        for r in record1:
            if (r[2] == record2[0][0]):
                flag = True
                index = r[0]
                break
        if (len(record1) == 0 or not flag):
            curr_query = "select Count(*) from cities"
            to_cursor.execute(curr_query)
            record3 = to_cursor.fetchall()
            index = record3[0][0]+1
            # curr_query = f"insert into  cities(cityId,city,province) values({index},'{changed['city']}','{record2[0][0]}')"
            query.insert('cities(cityId,city,province)', [
                         str(index), f"'{changed['city']}'", f"'{record2[0][0]}'"])
            # to_cursor.execute(curr_query)
        changed['cityid'] = index
        query.update(table, changed, f"id = {self.data['id']} ")
        self.setDataByID(self.data['id'])
        # print(self.rdata)
        return 0

    def update(self, data):
        if(self.level() == 2):
            return self.update_u(data)
        else:
            return self.update_r(data)
        
    def level(self):
        return self.priviledge

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

    
user = User(False, "", 2)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        username = request.form.get('username')
        if(username != None):
            user.name = username
            return render_template('restaurants.html', title='Restaurant', username=user.name)
    return render_template('home.html', title="Home Page")

def refresh():
    user = User(False, "", 2)
    return home()

@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
    name = request.form.get("user_name")
    return render_template('thanks.html', title="Thanks", name = name)

def available_username(username, table = 'persons'):
    cur_rows = query.select(['username'], [table], f"username= '{username}'")
    if(len(cur_rows)!=0):
        return False
    return True


def convert(input_val):
    return input_val=="on"

def addUser(username, password, firstname, lastname, gender, dob, level):
    if (available_username(username)):
    #     cur_query = query.select([''])
        
        
        len_id_query = query.select(['max(id)'], ['persons'])
        cur_id = len_id_query[0][0]+1
        gender = gender.lower()
        
        query.insert('persons(id,firstname,lastname,gender,phone,email,username,password,dob,priviledge)', [f"'{cur_id}'", f"'{firstname}'", f"'{lastname}'", f"'{gender}'", "'NULL'", "'NULL'", f"'{username}'",f"'{password}'", f"'{dob}'", "2"])
        return (0,'')
    else: 
        return (-1, 'username already taken')
        
def check_username_password(username, password, table = 'persons'):
    cur_rows = query.select(['username'], [table], f"username= '{username}' and password = '{password}'")
    if(len(cur_rows)==0):
        return False
    return True

def loginfrom(username, password, table = 'persons'):

    if(available_username(username, table)):
        return -1
    elif(not check_username_password(username, password, table)):
        return -2
    else:
        l = ['admin', 'managers', 'persons']
        user.login = True
        user.setData(username, l.index(table))
        return 0

def loginUser(username, password):

    usr = loginfrom(username, password, 'persons')
    if(usr == -1):
        mng = loginfrom(username, password, 'managers')
        if(mng == -1):
            return render_template('login.html', title= 'Login', error = 'Username does not exist')
        elif(mng == -2):
            return render_template('login.html', title= 'Login', error = 'Incorrect password')
    elif(usr == -2):
        return render_template('login.html', title= 'Login', error = 'Incorrect password')

    return render_template('restaurants.html', title='Restaurants', name=username, username = user.name)

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
    data = request.form.to_dict()
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

        restname = request.form.get('restname')
        if(restname!=""):
            restname = f"and restaurants.name='{restname}'"
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
        
            
        cur_query = f"select {columns} from restaurants, province, cities where {ratingMin} {ratingMax} {createdMin} {createdMax} {priceMin} {restname} {priceMax} {city} {province} and restaurants.cityId=cities.cityId and cities.province = province.provinceId order by {val} {order} limit {num} "

        to_cursor.execute(cur_query)
        ans = to_cursor.fetchall()

        cols = [i.split('.')[-1] for i in columns.split(", ")]
        
        return render_template('restaurants.html', title="Filter", rows=ans, cols = cols,  username = user.name, **data)

        # print(distMin, resID, num, order, val, city_check, province_check)

    return render_template('restaurants.html', title="Filter", data= {},  username = user.name)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if(user.login):
        if(request.method == 'POST'):
            data = request.form.to_dict()
            try :
                user.update(data)
                flash('Updated successfully')
            except:
                flash('Error updating')
        pages = ['update_admin.html','update_manager.html','update_user.html']
        return render_template(pages[user.level()], title="Update", data = user.getdata())
    else:
        flash('You are not logged in')
        return refresh()

def getdict(header, values):
    d = {}
    for i in range(len(header)):
        d[header[i]] = values[i]
    return d

def changeRest(site, title, data):

    if(data.get('restSelected') != None and data.get('restSelected') != ""):
        rest_id = data.get('restSelected')
        rest = query.select(['*'], ['restaurants'], f"restId={rest_id}")[0]
        return render_template(site, title=title, rest_id = rest_id, rest = getdict(query.cols,rest))   

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
            return render_template(site, title=title, error = error, **data)

        rest = query.select(['*'], ['restaurants'], f"restId={rest_id}")[0]
        return render_template(site, title=title, rest_id = rest_id, rest = getdict(query.cols,rest), **data)
    

@app.route('/review', methods=['GET', 'POST'])
def review():
    if(user.login):
        if(request.method == 'POST'):
            data = request.form.to_dict()
            if(data.get('restS') != None and data.get('restS') != ''):
                rest_id = data.get('restS')
                stars = data.get('stars')
                try:
                    query.insert('reviews',[f'{user.data["id"]}',f'{rest_id}',f'{stars}'])
                    flash("Review added")
                except:
                    flash("There was an error while adding review")
                    
                return render_template('review.html', title="Review", **data) 

            else: 
                changed = changeRest('review.html', 'Review', data)
                if(changed != None):return changed
                else: return render_template('review.html', title="Review", **data)
        return render_template('review.html', title="Review")
    else:
        flash('You are not logged in')
        return refresh()

@app.route('/locate', methods=['GET', 'POST'])
def locate():
    if(user.login):
        if(request.method == 'POST'):
            data = request.form.to_dict()
            changed = changeRest('locate.html', 'Locate', data)
            if(changed == None):
                
                if(data.get('restS') != None and data.get('restS') != ''):
                    try:
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
                            popup=ans[-1]
                        ).add_to(onmap)

                        return onmap._repr_html_()
                    
                    except:
                        flash("There was an error while locating restaurant")
                        return render_template('locate.html', title="Locate", **data)

            else: return changed 
        return render_template('locate.html', title="Locate")
    else:
        flash('You are not logged in')
        return refresh()
        


def updatePass(data):
    try:
        s = user.state
    except:
        s = None
    if(s != None or (data.get('oldpass') != None and data.get('oldpass') == user.data['password'])):
        if(data.get('newpass') == data.get('confirmpass')):
            try:
                tables = ['admin', 'managers', 'persons']
                query.update(tables[user.level()],{'password':data.get('newpass')},f'id = {user.data["id"]}')
                flash("Password changed")
                return ""
            except:
                return "There was an error while changing password"
        else:
            return "New passwords do not match"
    else:
        return "Old password is incorrect"


def checkPass(data):
    if(data.get('firstname') != None):
        firstame = data.get('firstname')
        lastname = data.get('lastname')
        dob = data.get('dob')
        ans = query.select(['id'], ['persons'], f"firstname = '{firstame}' and lastname = '{lastname}' and dob = '{dob}'")
        if(len(ans) > 0 and len(ans[0]) > 0):
            user.setDataByID(ans[0][0])
            user.login = True
            user.state = 'hold'
            return ans[0][0]
    return -1


@app.route('/changepass', methods=['GET', 'POST'])
def changepass():   

    if(request.method == 'POST'):
        data = request.form.to_dict()

        if(user.login):
            error = updatePass(data)
            if(error != ""):
                return render_template('change_password.html', title="Change Password",canchange = True, forgot=False , error = error, **data)
            else:
                return refresh()
            
        else:
            idd = checkPass(data)
            canchange = False
            if(idd == -1):
                error = "No user found with this details"
                return render_template('change_password.html', title="Change Password",canchange = False, forgot=True , error = error, **data)
            else:
                canchange = True
            return render_template('change_password.html', title="Change Password",canchange = canchange,forgot=True , **data)
            
    else:
        canchange = False
        forgot = True
        if(user.login):
            canchange = True
            forgot = False
    return render_template('change_password.html', title="Change Password", canchange = canchange, forgot = forgot)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("Logged out")
    query.dump()
    return refresh()


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
