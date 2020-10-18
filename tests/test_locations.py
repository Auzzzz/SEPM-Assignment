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
    def create(self,name, desc, gps, time):
         return self.app.post(
            '/admin/newlocation',
            data=dict(name = name, desc = desc, gps = gps,time = time),
            follow_redirects=True
    )

    def delete(self,locationid):
        return self.app.post(
            '/admin/deletelocation',
            data=dict(locationid=locationid),
            follow_redirects=True
    )

    def edit(self,name, gpscords, time, locationid):
        return self.app.post(
            '/admin/editlocation',
            data=dict(name = name, gpscords = gpscords,time = time,locationid = locationid),
            follow_redirects=True
    )


    ### Unit Tests ###

    def test_create_location(self):
        response = self.create("test1","test1","123.123","25")
        self.assertEqual(response.status_code, 200)
        with self.app.session_transaction() as session:
            self.assertEqual(session['msg'], "Location Registered")
    

    def test_edit_location(self):
        response = self.edit("test1","200.200","0","14")
        self.assertEqual(response.status_code, 200)

    # def test_delete_loaction(self):
    #     response = self.delete("31")
    #     self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()