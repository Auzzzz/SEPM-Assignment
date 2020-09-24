from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'nvjsnf9384'

# DB connection 
app.config['MYSQL_HOST'] = '35.244.104.154'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Banana123#"
app.config['MYSQL_DB'] = 'sepm'

#Init mysql
mysql = MySQL(app) 

#@app.route('/')
#def hello_world():
#    return 'Hello, World!'
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

@app.route('/logout')
def logout():
    session.clear()

    return render_template('login.html', msg = 'logged out')

@app.route('/home')
def home():
    if 'islogged' in session:
        #user is logged in keep them around
        #pass through values

        return render_template('index.html', session = session )
    else:
        #return to login screen
        return redirect(url_for('login'))

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
                print(cursor.lastrowid)
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

@app.route('/admin/tour/editOrder', methods=['GET', 'POST'])
def tourEditOrder():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'Test' in request.form:
                print(request.form.getlist('tourid'))
                print(request.form.getlist('order'))

                return "Yes"

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

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

                print(tours[0]['name'])
                return render_template('view_tour.html', tourid = tourid, tours = tours, len = len(tours), tour_location = tour_location, tl_len = len(tour_location), location = location, loc_len = len(location), tourtypes = tourtypes, tourlen = len(tourtypes))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))

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
                    print("location", location)
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
                print("location", location)
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


### Tour Types ###

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

@app.route('/admin/tourtypes/edit', methods=['GET', 'POST'])
def tourtypesEdit():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'tourtid' in request.form:
                tourtid = request.form['tourtid']
                
                #get all tours
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM tour_types where tourtid = %s', [tourtid])
                #fetch the record
                tourtypes = cursor.fetchall()

            return render_template('admin_tourtypes_edit.html', tourtypes = tourtypes) 
                

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


@app.route('/admin/tourtypes/edittype', methods=['GET', 'POST'])
def tourtypesEditSubmit():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            if request.method == 'POST' and 'typeid' in request.form:
                typeid = request.form['tourid']
                desc = request.form['desc']

                #update SQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("""Update tour_types set name = %s WHERE tourtid = %s""", [name, typeid])
                mysql.connection.commit()
            
            return render_template('admin_tourtypes_edit.html', tourtypes = tourtypes) 
                

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))



@app.route('/test', methods=['GET', 'POST'])
def test():

    
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
        print("location", location)
        time = location['time']
        total_time += time
        i += 1
        
        

        



    #print("Tours_locations", tour_location)

    #get all locations in the tour
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM location')
    #fetch the record
    location = cursor.fetchall()
   #print("location", location)
    tl_length = len(tour_location)

    
    for i in range (0,tl_length):
        if tour_location[i]['tourid'] == 23:
            print(tour_location[i]['locationid'])
            print(tour_location[i]['order'])
            print("YES")
            i =+ 1

    
    # #get all tours
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM tours')
    # #fetch the record
    # tours = cursor.fetchall()

    # print(tours)

    # #get all locations for each tour
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM tour_location')
    # #fetch the record
    # tour_location = cursor.fetchall()
    # tl_length = len(tour_location)

    # for i in range (0,tl_length):
    #     if tour_location[i]['tourid'] == 23:
    #         print(tour_location[i]['locationid'])
    #         print(tour_location[i]['order'])
    #         i =+ 1
    return render_template('login.html')
  
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")