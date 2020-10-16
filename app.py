from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'nvjsnf9384'

# DB connection 
app.config['MYSQL_HOST'] = '167.71.112.220'
app.config['MYSQL_USER'] = "user"
app.config['MYSQL_PASSWORD'] = "Banana123#"
app.config['MYSQL_DB'] = 'sepm'

#Init mysql
mysql = MySQL(app) 

#login page first page to load
@app.route('/', methods=['GET','POST'])
def login():
    #set msg to pass through if needed
    msg = ''
    
    #Check form has been submitted
    if request.method == 'POST' and 'accountid' in request.form and 'password' in request.form:
        #username and password from form into variable
        accountid = request.form['accountid']
        password = request.form['password']

        #check db for user & password
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE accountid = %s AND password = %s', (accountid, password))
        #fetch the record
        user = cursor.fetchone()
        
        #if account exsists
        if user:
            #check user has not been disabled
            if user['accountStatus'] == 1:
                #make user exsist in some session data
                session['islogged'] = True
                session['accountid'] = user['accountid']
                session['name'] = user['name']
                session['accountTypeID'] = user['accountTypeID']
                #move user to home page (index)
                return redirect(url_for('home'))
            else:
                user = ''
                msg = 'user has been disabled by an admin'
                return render_template('login.html', msg=msg) 
        
        else:
            #account does not exsit in DB reject
            msg = 'user does not exsist please contact an administrator '
            
    return render_template('login.html', msg=msg)

#logout
@app.route('/logout')
def logout():
    session.clear()

    return render_template('login.html', msg = 'logged out')

#non admin home
@app.route('/home')
def home():
    if 'islogged' in session:
        #user is logged in keep them around
        #pass through values

        return render_template('index.html', session = session )
    else:
        #return to login screen
        return redirect(url_for('login'))

#createw a new user from a admin account
@app.route('/admin/create', methods=['GET', 'POST'])
def adminCreateUser():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            #set msg to pass through if needed
            msg = ''
            
            #get all user types for dropdowns
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accountType')
            #fetch the record
            usertypes = cursor.fetchall()

            #get all account types for dropdowns
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account_status')
            #fetch the record
            accounttypes = cursor.fetchall()

            if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'accountStatus' in request.form and 'accountType' in request.form:
                #form values into variables
                name = request.form['name']
                password = request.form['password']
                accountStatus = request.form['accountStatus']
                accountType = request.form['accountType']
            
                #insert account into DB
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', (password, name, accountType, accountStatus ))
                mysql.connection.commit()
                session['msg'] = "User Registered"

                return redirect(url_for('adminHome'))

            elif request.method == 'POST':
                # Form has no data in it
                msg = 'Please fill out the form!'

            return render_template('admin_create_users.html', usertypes = usertypes, accounttypes = accounttypes)

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#deactive a user
@app.route('/admin/deactivate', methods=['GET', 'POST'])
def adminDeactivateUser():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'accountid' in request.form:
                

                return redirect(url_for('adminHome'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


#admin home page
@app.route('/admin', methods=['GET', 'POST'])
def adminHome():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            #check db for user & password
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accountid, name, accountStatus, accountTypeID FROM account')
            #fetch the record
            allusers = cursor.fetchall()

            #get all user types for dropdowns
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accountType')
            #fetch the record
            accounttypes = cursor.fetchall()

            #get all account types for dropdowns
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM account_status')
            #fetch the record
            usertypes = cursor.fetchall()

            return render_template('admin_home.html', allusers = allusers, len = len(allusers), usertypes = usertypes, userlen = len(usertypes), accounttypes = accounttypes, accountlen = len(accounttypes))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


### Locations ###

#location homne
@app.route('/admin/locations', methods=['GET', 'POST'])
def adminHomeLocations():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            #check db for user & password
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM location')
            #fetch the record
            locations = cursor.fetchall()

            return render_template('admin_locations.html', locations = locations, len = len(locations))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#delete a location
@app.route('/admin/deletelocation', methods=['GET', 'POST'])
def adminDelLocation():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'locationid' in request.form:
                locationid = request.form['locationid']
                #check db for user & password
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM location WHERE id = %s', (locationid))

                return redirect(url_for('adminHomeLocations'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#edit the location
@app.route('/admin/editlocation', methods=['GET', 'POST'])
def adminEditLocation():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST':

                    locationid = request.form['locationid']
                    name = request.form['name']
                    desc = request.form['desc']
                    gpscords = request.form['gpscords']
                    time = request.form['time']

                    #check db for user & password
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("""Update location set name = %s, gpscords = %s, time = %s where id = %s""", [name, gpscords, time, locationid])
                    mysql.connection.commit()
                    
                    return redirect(url_for('adminHomeLocations'))
            else: 
                #return to home if not an admin
                return redirect(url_for('home'))
        else:
            #return to login screen
            return redirect(url_for('login'))

#edit the location inside a tour
@app.route('/admin/editlocationtour', methods=['GET', 'POST'])
def adminEditLocationTour():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST':

                    locationid = request.form['locationid']
                    name = request.form['name']
                    desc = request.form['desc']
                    gpscords = request.form['gpscords']
                    time = request.form['time']

                    #check db for user & password
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("""Update location set name = %s, gpscords = %s, time = %s where id = %s""", [name, gpscords, time, locationid])
                    mysql.connection.commit()
                    
                    return redirect(url_for('tours'))
            else: 
                #return to home if not an admin
                return redirect(url_for('home'))
        else:
            #return to login screen
            return redirect(url_for('login'))


#add a anew location into the db 
@app.route('/admin/newlocation', methods=['GET', 'POST'])
def newlocation():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
           
            #get post data from form
            if request.method == 'POST' and 'name' in request.form and 'desc' in request.form and 'gps' in request.form and 'time' in request.form:
                #form values into variables
                name = request.form['name']
                desc = request.form['desc']
                gpscords = request.form['gps']
                time = request.form['time']
            
                #insert account into DB
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO location VALUES (NULL, %s, %s, %s, %s)', (name, desc, gpscords, time ))
                mysql.connection.commit()
                session['msg'] = "Location Registered"

                return redirect(url_for('adminHomeLocations'))
            return render_template('admin_newlocation.html')

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


### Tours ###
#tours home, display all tours
@app.route('/admin/tours', methods=['GET', 'POST'])
def tours():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            
            #get all tours
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tours')
            #fetch the record
            tours = cursor.fetchall()

            #get all types
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tour_types')
            #fetch the record
            tourtypes = cursor.fetchall()

            return render_template('admin_tours.html', tours = tours, len = len(tours), tourtypes = tourtypes, tourlen = len(tourtypes))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#edit a tour name and details then return to tours home
@app.route('/admin/tour/editd', methods=['GET', 'POST'])
def tourEditd():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'tourid' in request.form:

                tourid = request.form['tourid']
                name = request.form['name']
                desc = request.form['desc']
                time = request.form['time']
                tourtype = request.form['tourtype']

                #check db for user & password
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("""Update tours set name = %s, desc = %s, totaltime = %s, tourTypeID = %s where tourid = %s""", [name, desc, time, tourtype, tourid])
                mysql.connection.commit()
                    
                return redirect(url_for('tours'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#edit the order of locations inside a tour
@app.route('/admin/tour/edittourlocation', methods=['GET', 'POST'])
def tourEditlocationOrder():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'utlid' in request.form:

                utlid = request.form.getlist('utlid')
                order = request.form.getlist('order')

                x = 0
                for each in utlid:
                    print(utlid[x], order[x])
                    utlids = utlid[x]
                    orders = order[x]

                    #check db for user & password
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("""UPDATE `tour_location` SET `order`= %s WHERE `utlid` = %s """, [order[x], utlid[x]])
                    mysql.connection.commit()
                    x += 1

                return redirect(url_for('tours'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


#display all tours 
@app.route('/admin/tour', methods=['GET', 'POST'])
def individualTours():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'tourid' in request.form:
                tourid = request.form['tourid']
                #get all tours
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tours WHERE tourid = %s', [tourid])
                #fetch the record
                tours = cursor.fetchall()

                #get all tour locations for each tour
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tour_location where tourid = %s', [tourid])
                #fetch the record
                tour_location = cursor.fetchall()

                #get all locations in the tour
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM location')
                #fetch the record
                location = cursor.fetchall()

                #get all types
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tour_types')
                #fetch the record
                tourtypes = cursor.fetchall()

                locationcount = []
                locationc = []
                count = 1
                for x in tour_location:
                    locationcount.append(x)
                    for i in range (0, len(locationcount)):
                        locationc.append(count)
                        count =+ 1
                        print(locationc)

                locationc = len(locationcount)

                return render_template('view_tour.html', tourid = tourid, tours = tours, len = len(tours), tour_location = tour_location, tl_len = len(tour_location), location = location, loc_len = len(location), tourtypes = tourtypes, tourlen = len(tourtypes), locationc = locationc)

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#delete a tour from the DB then returen to tours
@app.route('/admin/tours/delete', methods=['GET', 'POST'])
def toursDelete():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            if request.method == 'POST' and 'tourid' in request.form:
                tourid = request.form['tourid']
                #delete from location
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM tours WHERE tourid = %s', [tourid])
                mysql.connection.commit()
                #delete from tour_location
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM tour_location WHERE tourid = %s', [tourid])
                mysql.connection.commit()

                return redirect(url_for('tours'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#interface for user to add new tour details into
@app.route('/admin/newtour', methods=['GET', 'POST'])
def newtour():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            #get all types
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tour_types')
            #fetch the record
            tourtypes = cursor.fetchall()

            #get all locations
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM location')
            #fetch the record
            locations = cursor.fetchall()

            return render_template('admin_newtour.html', locations = locations, len = len(locations), tourtypes = tourtypes, tourlen = len(tourtypes))
        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#create a new tour into the db then return to tour home
@app.route('/admin/createnewtour', methods=['GET', 'POST'])
def createNewTour():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            if request.method == 'POST':

                #create the tour in the tour db
                name = request.form['name']
                desc = request.form['desc']
                tourtype = request.form['tourtype']
                time = 0

                #get the selected locations from the form & count how many entries
                locations = request.form.getlist('newtour')
                total = len(locations)

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO tours VALUES (NULL, %s, %s, %s, %s)', (name, desc, time, tourtype ))
                mysql.connection.commit()

                #get the id of the created tour
                tourid = cursor.lastrowid
            
                #insert the selected locations into the tour_location db as individual entrties
                order = 1
                for i in range(0,total):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO tour_location VALUES (NULL, %s, %s, %s)', (tourid, locations[i], order))
                    mysql.connection.commit()
                    order += 1
                
                #get all locations for each tour
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tour_location where tourid = %s', [tourid])
                #fetch the record
                tour_location = cursor.fetchall()
                tour_location_len = len(tour_location)
                
                total_time = 0

                for i in range (0, tour_location_len):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM location where id = %s', [tour_location[i]['locationid']])
                    location = cursor.fetchone()
                    time = location['time']
                    total_time += time
                    i += 1

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("""Update tours set totaltime = %s WHERE tourid = %s """, [total_time, tourid])
                mysql.connection.commit()

                
                
                return redirect(url_for('tours'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#edit page for the user to alter the tour, displays all locations assiged to tour
@app.route('/admin/alter', methods=['GET', 'POST'])
def alterTour():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            #get all locations
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM location')
            #fetch the record
            locations = cursor.fetchall()

            return render_template('admin_alter_tour.html', locations = locations, len = len(locations))
        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login')) 

#edit a location already in the db then return to home page of tours
@app.route('/admin/addlocation', methods=['GET', 'POST'])
def alterTourAdd():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            locations = request.form.getlist('newtour')
            total = len(locations)

            #get the id of the created tour
            tourid = request.form['tourid']
            
            #insert the selected locations into the tour_location db as individual entrties
            order = 1
            for i in range(0,total):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO tour_location VALUES (NULL, %s, %s, %s)', (tourid, locations[i], order))
                mysql.connection.commit()
                order += 1
                
            #get all locations for each tour
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tour_location where tourid = %s', [tourid])
            #fetch the record
            tour_location = cursor.fetchall()
            tour_location_len = len(tour_location)
                
            total_time = 0

            for i in range (0, tour_location_len):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM location where id = %s', [tour_location[i]['locationid']])
                location = cursor.fetchone()
                time = location['time']
                total_time += time
                i += 1

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""Update tours set totaltime = %s WHERE tourid = %s """, [total_time, tourid])
            mysql.connection.commit()

            return redirect(url_for('tours'))
        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login')) 

### Tours Non-Admin ###
@app.route('/TourSchedules', methods=['GET','POST'])
def aViewTours():
    #get all tours
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tours')
    #fetch the record
    tours = cursor.fetchall()

    #get all types
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tour_types')
    #fetch the record
    tourtypes = cursor.fetchall()

    return render_template('tourschedules.html', tours = tours, len = len(tours), tourtypes = tourtypes, tourlen = len(tourtypes))


@app.route('/TourSchedules/indivdual', methods=['GET','POST'])
def aViewToursIndivdual():
    if request.method == 'POST' and 'tourid' in request.form:
        tourid = request.form['tourid']
        #get all tours
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tours WHERE tourid = %s', [tourid])
        #fetch the record
        tours = cursor.fetchall()

        #get all tour locations for each tour
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tour_location where tourid = %s', [tourid])
        #fetch the record
        tour_location = cursor.fetchall()

        #get all locations in the tour
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM location')
        #fetch the record
        location = cursor.fetchall()

        #get all types
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tour_types')
        #fetch the record
        tourtypes = cursor.fetchall()

        return render_template('tourschedules_individual.html', tourid = tourid, tours = tours, len = len(tours), tour_location = tour_location, tl_len = len(tour_location), location = location, loc_len = len(location), tourtypes = tourtypes, tourlen = len(tourtypes))





### Tour Types ###
#tour types home, display all tour types
@app.route('/admin/tourtypes', methods=['GET', 'POST'])
def tourtypes():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            #get all tours
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tour_types')
            #fetch the record
            tourtypes = cursor.fetchall()

            return render_template('admin_tourtypes.html', tourtypes = tourtypes, len = len(tourtypes))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#add a your type to the DB
@app.route('/admin/tourtypes/create', methods=['GET', 'POST'])
def tourtypesCreate():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            if request.method == 'POST' and 'name' in request.form:
                #form values into variables
                name = request.form['name']
            
                #insert account into DB
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO tour_types VALUES (NULL, %s)', [name])
                mysql.connection.commit()
                session['msg'] = "User Registered"

                return redirect(url_for('tourtypes'))
            return render_template('admin_tourtypes_create.html')

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#delete the tour type from the data base then return to tour types home
@app.route('/admin/tourtypes/delete', methods=['GET', 'POST'])
def tourtypesDelete():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            if request.method == 'POST' and 'name' in request.form:
                typeid = request.form['id']
                #check db for user & password
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM tour_types WHERE id = %s', (typeid))
                mysql.connection.commit()
                return redirect(url_for('tourtypes'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#display the edit page for tour types and display the correct details then pass off to tourtypesEditSubmit
@app.route('/admin/tourtypes/edit', methods=['GET', 'POST'])
def tourtypesEdit():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'typeid' in request.form:
                tourtid = request.form['typeid']
                #get all tours
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tour_types where tourtid = %s', [tourtid])
                #fetch the record
                tourtypes = cursor.fetchall()
                print(tourtypes)

            return render_template('admin_tourtypes_edit.html', tourtypes = tourtypes) 
 
        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

#submit the editited tour type to the database then return to tour types main page
@app.route('/admin/tourtypes/edittype', methods=['GET', 'POST'])
def tourtypesEditSubmit():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'tourtid' in request.form:
                tourtid = request.form['tourtid']
                name = request.form['name']
                #update SQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("Update tour_types set name = %s WHERE tourtid = %s", [name, tourtid])
                mysql.connection.commit()
            
            return redirect(url_for('tourtypes'))


        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

  
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")