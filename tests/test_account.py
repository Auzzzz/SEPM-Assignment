import unittest
import paths
from app import app


class AccountTest(unittest.TestCase):
    # executed prior to each test
    @classmethod
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        #db conifg
        app.config['MYSQL_HOST'] = '167.71.112.220'
        app.config['MYSQL_USER'] = "user"
        app.config['MYSQL_PASSWORD'] = "Banana123#"
        app.config['MYSQL_DB'] = 'sepm'

        with self.app.session_transaction() as session:
            session['islogged'] = True
            session['accountid'] = 1
            session['name'] = "Admin - Chris K"
            session['accountTypeID'] = 1
        


    # executed after each test
    @classmethod
    def tearDown(self):
        pass
    
    ### Helper functions ###
    
    def login(self, accountid, password):
        return self.app.post(
            '/',
            data=dict(accountid=accountid, password=password),
            follow_redirects=True
    )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
    )
    def create(self,name,password,accountStatus,accountType):
        return self.app.post('/admin/create',
        data = dict(name = name,password = password,
        accountStatus = accountStatus, accountType = accountType),follow_redirects=True) 
  

    ### Unit Test ###
    def test_create_user(self):
        response = self.create('test1','test1','1','1')
        self.assertEqual(response.status_code, 200)
        with self.app.session_transaction() as session:
            self.assertEqual(session['msg'], "User Registered")
    

if __name__ == "__main__":
    unittest.main()