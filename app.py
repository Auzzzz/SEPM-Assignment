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
            msg = 'user does not exsist please contact someone who cares'
            
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
            if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'accountStatus' in request.form and 'accountType' in request.form:
                #form values into variables
                name = request.form['name']
                password = request.form['password']
                accountStatus = request.form['accountStatus']
                accountType = request.form['accountType']
            
                #insert account into DB
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', (name, password, accountType, accountStatus ))
                mysql.connection.commit()
                session['msg'] = "User Registered"

                return redirect(url_for('adminHome'))

            elif request.method == 'POST':
                # Form has no data in it
                msg = 'Please fill out the form!'

            return render_template('admin_create_users.html')

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


@app.route('/admin/deactivate', methods=['GET', 'POST'])
def adminCreateUser():
    if 'islogged' in session:
        if session['accountTypeID'] == 1:
            
            #check db for user & password
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accountid, name, accountStatus, accountTypeID FROM account')
            #fetch the record
            allusers = cursor.fetchall()

            return redirect(url_for('adminHome'))

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def adminHome():
    msg = ''
    if 'islogged' in session:
        if session['accountTypeID'] == 1:

            #check db for user & password
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT accountid, name, accountStatus, accountTypeID FROM account')
            #fetch the record
            allusers = cursor.fetchall()

            return render_template('admin_home.html', allusers = allusers, len = len(allusers), msg = session['msg'])

        else: 
            #return to home if not an admin
            return redirect(url_for('home'))
    else:
        #return to login screen
        return redirect(url_for('login'))


    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")