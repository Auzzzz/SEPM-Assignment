from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'nvjsnf9384'

# DB connection 
app.config['MYSQL_HOST'] = '35.244.104.218'
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
        cursor.execute('SELECT * FROM accounts WHERE accountid = %s AND password = %s', (accountid, password))
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
        name = session['name']
        print(session)
        return render_template('index.html', name = name )
    else:
        #return to login screen
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")