import unittest
import requests
    
class TestRelay(unittest.TestCase):
    # Default Flask
    ApiUrl = "http://127.0.0.1:5000/"
    
    # test response ok
    def test_res_ok(self):
        res = requests.get(self.ApiUrl + "restaurant")
        self.assertEqual(res.status_code, 200)
        
    # test response not_ok
    def test_res_nok1(self):
        res = requests.get(self.ApiUrl)
        self.assertNotEqual(res.status_code, 200)
        
    def test_res_nok2(self):
        res = requests.get(self.ApiUrl + "restaurant/not_a_restaurant_really")
        self.assertNotEqual(res.status_code, 200)
        
    # test json 200
    def test_res_json(self):
        res = requests.get(self.ApiUrl + "restaurant")
        self.assertEqual(res.headers.get('content-type'), 'application/json')
        
    # test json NOT 200
    def test_res_json_err(self):
        res = requests.get(self.ApiUrl + "restaurant/not_a_restaurant_really")
        self.assertEqual(res.headers.get('content-type'), 'application/json')
    
        
if __name__ == "__main__":
        unittest.main()