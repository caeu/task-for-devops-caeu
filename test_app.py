import unittest
from app import app
    
class TestRelay(unittest.TestCase):
    
    # required for app testing
    app.testing = True
    
    def test_res_ok(self):
        with app.test_client() as c:
            res = c.get("/restaurant")
            self.assertEqual(res.status_code, 200)

    # test response not_ok
    def test_res_nok1(self):
        with app.test_client() as c:
            res = c.get()
            self.assertNotEqual(res.status_code, 200)
    
           
    def test_res_nok2(self):
        with app.test_client(self) as c:
            res = c.get("restaurant/not_a_restaurant_really")
            self.assertNotEqual(res.status_code, 200)
    
    # test json 200       
    def test_res_json(self):
        with app.test_client(self) as c:
            res = c.get("restaurant")
            self.assertEqual(res.headers.get("content-type"), "application/json")
    
    # test json Not 200        
    def test_res_json_err(self):
        with app.test_client(self) as c:
            res = c.get("restaurant/not_a_restaurant_really")
            self.assertEqual(res.headers.get("content-type"), "application/json")

        
if __name__ == "__main__":
        unittest.main()