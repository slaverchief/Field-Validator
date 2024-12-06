import unittest
import requests
from exceptions import *


class TestFormValidation(unittest.TestCase):

    def test_invalid_forms(self):
        res1 = requests.post("http://localhost:8000", json= {"field1": "+7 929 228 28 28", "field2": "2024-03-10"}).json()
        res2 = requests.post("http://localhost:8000", json= {"phone": "+7 929 228 28 28", "date": "2024-03-10", "email": "some@mail.ru"}).json()
        res3 = requests.post("http://localhost:8000", json={"field1": "2024-50-03", "field2": "ewq"}).json()
        res4 = requests.post("http://localhost:8000", json={"username": "SOme_name", "password": "2024-03-10", "email": "dsaas@dassa.ru"}).json()
        self.assertEqual(res1, {"field1": "phone", "field2": "date"})
        self.assertEqual(res2, {"date": "date","email": "email","phone": "phone"})
        self.assertEqual(res3, {"field1": "text","field2": "text"})
        self.assertEqual(res4, {"email": "email","password": "date","username": "text"})

    def test_valid_forms(self):
        res1 = requests.post("http://localhost:8000",
                             json={"field1": "example@mail.ru", "field2": "+7 929 222 22 22", "fild3": " 2111"}).text
        res2 = requests.post("http://localhost:8000",
                             json={"username": "somtext","password": "some_pass","email": "maga@mail.ru"}).text
        res3 = requests.post("http://localhost:8000",
                             json={"price": 300, "product_name": "some_name", "date": "2024-08-12", "contact": "+7 111 111 11 11"}).text
        self.assertEqual(res1, "TestForm")
        self.assertEqual(res2, "LoginForm")
        self.assertEqual(res3, "OrderForm")

if __name__ == "__main__":
    unittest.main()