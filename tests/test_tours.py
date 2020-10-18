import unittest
import paths
from app import app


class TourTest(unittest.TestCase):
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
    def create(self,name, desc, time, tourtype ):
         return self.app.post(
            '/admin/createnewtour',
            data=dict(name = name, desc = desc, time = time, tourtype = tourtype),
            follow_redirects=True
    )

    def delete(self,tourid):
        return self.app.post(
            '/admin/tours/delete',
            data=dict(tourid=tourid),
            follow_redirects=True
    )

    def edit(self,name, desc, time, tourtype, tourid):
        return self.app.post(
            '/admin/tour/editd',
            data=dict(name = name, desc = desc,time = time, tourtype = tourtype,tourid = tourid),
            follow_redirects=True
    )
    # def addLocation()

    ### Unit Tests ###

  
    def test_create_tour(self): 
        response = self.create("test","test",0,1)
        self.assertEqual(response.status_code, 200)
   
 
    def test_edit_tour(self):
        response = self.edit("new tour1","test","20","4","45")
        self.assertEqual(response.status_code, 200)
    
    def test_delete_tour(self): 
        response = self.delete(47)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()