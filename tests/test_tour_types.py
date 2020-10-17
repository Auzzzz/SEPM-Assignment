import unittest
import paths
from app import app


class TourTypesTest(unittest.TestCase):
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
    def create(self,name):
         return self.app.post(
            '/admin/tourtypes/create',
            data=dict(name = name),
            follow_redirects=True
    )

    def delete(self,typeid):
        return self.app.post(
            '/admin/tourtypes/delete',
            data=dict(typeid = typeid),
            follow_redirects=True
    )

    def edit(self,name, tourtid):
        return self.app.post(
            '/admin/tourtypes/edittype',
            data=dict(name = name, tourtid = tourtid),
            follow_redirects=True
    )


    ### Unit Tests ###
    ## works
    def test_create_tour_types(self): 
        response = self.create("test")
        self.assertEqual(response.status_code, 200)

    ## works
    def test_edit_tour_types(self):
        response = self.edit("test2",10)
        self.assertEqual(response.status_code, 200)
    
    ## not working
    def test_delete_tour_types(self): 
        response = self.delete(12)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()