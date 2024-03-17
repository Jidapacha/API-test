import unittest
import requests
import json
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app import app, users, texts, balance, translator  # import Flask application และข้อมูล users



### Authentication ###
class TestAuthentication(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'
    def setUp(self):
        self.app = app.test_client()

    #1 Valid login
    def test_valid_login(self):
        response = self.app.post('/login?username=user1&password=pass1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Login successful')

    #2 Invalid username
    def test_invalid_username(self):
        response = self.app.post('/login?username=invalid_user&password=pass1')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid username or password')

    #3 Invalid password
    def test_invalid_password(self):
        response = self.app.post('/login?username=user1&password=invalid_pass')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid username or password')

    #4 Empty data
    def test_empty_fields(self):
        response = self.app.post('/login?username=&password=')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username and password are required!')
    
### 5 HTTP status ###
class TestHTTPresponse(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'
    def setUp(self):
        self.app = app.test_client()

    def test_status_http(self):
        response = self.app.post('/login?username=user1&password=pass1')
        self.assertEqual(response.status_code, 200)

### 6 Idempotent ###
class TestIdempotent(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_valid_login_idempotent(self):
        response1 = self.app.post('/login?username=user1&password=pass1')
        data1 = response1.get_json()

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(data1['message'], 'Login successful')
        
        response2 = self.app.post('/login?username=user1&password=pass1')
        data2 = response2.get_json()

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data2['message'], 'Login successful')
        self.assertEqual(data1, data2)


### 7 Safe ###
class TestSafe(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'
    def test_safe(self):
        endpoint = '/user-info'
        params = {'username': 'user1'}  
        response = requests.get(self.base_url + endpoint, params=params)
        
        self.assertEqual(response.status_code, 200)
        expected_data = {'username': 'user1', 'password': 'pass1'}  
        self.assertEqual(response.json(), expected_data)

### 8 Translate ###
class TestTranslate(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_translate_text(self):
        payload = {'text': 'สวัสดี', 'target_lang': 'en'}
        response = self.client.post('/translate', json=payload)

        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        translated_text = response_data.get('translated_text', '')

        self.assertEqual(translated_text.lower(), 'hello')

### Deposit ###
class TestDeposit(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'
    
    def setUp(self):
        self.app = app.test_client()

    def test_valid_deposit(self):
        response = self.app.post('/deposit?amount=50')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Deposited 50 successfully')

    def test_invalid_deposit(self):
        response = self.app.post('/deposit?amount=-50')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid amount')

### Withdraw ###
class TestWithdraw(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'

    def setUp(self):
        self.app = app.test_client()

    def test_valid_withdrawal(self):
        response = self.app.post('/withdraw?amount=50')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Withdraw succeed')

    def test_exceed_balance(self):
        response = self.app.post('/withdraw?amount=1000')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Amount should be less than Balance')
    

if __name__ == '__main__':
    unittest.main()

