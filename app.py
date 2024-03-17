from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

users = {
    'user1': {'username': 'user1', 'password': 'pass1'},
    'user2': {'username': 'user2', 'password': 'pass2'}
}
texts = {
    "text": "สวัสดี",
    "target_lang": "en"
}

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password are required!'}), 400
        
        if username in users and users[username]['password'] == password:
            return jsonify({'message': 'Login successful'}), 200 
    
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user-info', methods=['GET'])
def get_user_info():
    username = request.args.get('username')

    if username in users:
        return jsonify(users[username]), 200 
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.json.get('text')
    target_lang = request.json.get('target_lang')

    if not text or not target_lang:
        return jsonify({'error': 'Missing text or target_lang in the request body'}), 400

    try:
        translated_text = translator.translate(text, dest=target_lang).text
        return jsonify({'translated_text': translated_text}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred during translation: {str(e)}'}), 500
    
# Initial balance
balance = 100

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    try:
        amount = int(request.args.get('amount', 0))

        if amount <= 0 or not isinstance(amount, int):
            return jsonify({'message': 'Invalid amount'}), 400
        
        balance += amount
        return jsonify({'message': f'Deposited {amount} successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    amount = int(request.args.get('amount', 0))
    
    if not amount or amount <= 0 or isinstance(amount, str):
        return jsonify({'message': 'Invalid amount'}), 400
    
    if amount > balance:
        return jsonify({'message': 'Amount should be less than Balance'}), 400

    balance -= amount
    return jsonify({'message': 'Withdraw succeed', 'balance': balance}), 200


if __name__ == '__main__':
    app.run(debug=True)
