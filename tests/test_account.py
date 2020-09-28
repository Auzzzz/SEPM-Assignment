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
        app.config['MYSQL_HOST'] = '35.244.104.154'
        app.config['MYSQL_USER'] = "root"
        app.config['MYSQL_PASSWORD'] = "Banana123#"
        app.config['MYSQL_DB'] = 'sepm'

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
    
    def load_routes_after_login(self, route, data):
        response = self.app.get(route, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data, response.data)

    ### Unit Test ###

    # Test login as Admin user
    def test_valid_admin_login(self):
        response = self.login('1', '123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome back, Admin - Chris K!', response.data)
   
    # Test login as Worker user
    def test_valid_admin_worker(self):
        response = self.login('145', '123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome back, ATest!', response.data)

    # Test login with invalid credential
    def test_invalid_login(self):
        response = self.login('user', 'user')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user does not exsist please contact an administrator', response.data)
    
    
    # Test logout
    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged out', response.data)

    # Test routes after login
    def test_load_routes_after_login(self):
        response = self.login('1', '123')
        self.assertEqual(response.status_code, 200)
        self.load_routes_after_login('/home','Welcome back, Admin - Chris K!')
        self.load_routes_after_login('/admin/create','Create Users')
        self.load_routes_after_login('/admin','All users')
        self.load_routes_after_login('/admin/locations','All Locations')
        self.load_routes_after_login('/admin/newlocation','Create a Location')
        self.load_routes_after_login('/admin/tours','All Tours')
        self.load_routes_after_login('/admin/newtour','Create new Tour')
        self.load_routes_after_login('/admin/alter','Add Location to a Tour')
        self.load_routes_after_login('/admin/tourtypes','All types')
        self.load_routes_after_login('/admin/tourtypes/create','Create a New tour type')

if __name__ == "__main__":
    unittest.main()