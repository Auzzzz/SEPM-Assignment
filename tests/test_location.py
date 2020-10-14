import unittest
import paths
from app import app


class LocationTest(unittest.TestCase):
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
    def create(self,name, desc, gpscords, time):
         return self.app.post(
            '/admin/newlocation',
            data=dict(name=name, desc=desc, gpscords= gpscords,time = time),
            follow_redirects=True
    )

    def delete(self,locationid):
        return self.app.post(
            '/admin/deletelocation',
            data=dict(locationid=locationid),
            follow_redirects=True
    )


    ### Unit Tests ###

    def test_create_location(self):
        response = self.create("test","test",123.123,25)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()